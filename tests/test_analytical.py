"""Unit tests for the 1D segmented analytical model.

Test discipline:
  - Limiting cases: single-phase reproduces standalone Dittus-Boelter
  - Conservation: energy balance closes to machine epsilon
  - Regime detection: constructed states verify transition logic
  - CHF breach: raises CHFExceededError
  - ONB continuity: T_w jump at ONB cell is zero (by construction)
  - Interpolation limits: collapses to SP at q->q_onb+, to boiling curve at high superheat

No frozen-output golden tests.  No regression tests against own output.
"""

import math

import CoolProp.CoolProp as CP
import pytest

from two_phase_cp.analytical import (
    CHFExceededError,
    ChannelGeometry,
    CrossSection,
    Regime,
    solve_channel,
)
from two_phase_cp.analytical.model import (
    _find_onb_wall_temp,
    _solve_partial_boiling,
    bergles_rohsenow_curve,
)
from two_phase_cp.correlations.single_phase import gnielinski, qu_mudawar_nu3
from two_phase_cp.properties.water import liquid_state_at_Ph


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _round_tube(D: float, L: float) -> ChannelGeometry:
    """Convenience: round tube geometry from diameter and length."""
    return ChannelGeometry(
        D_h=D,
        L=L,
        A_flow=math.pi / 4 * D**2,
        P_heated=math.pi * D,
        cross_section=CrossSection.ROUND,
    )


# ---------------------------------------------------------------------------
# 1. Wiring — turbulent single-phase branch delegates to gnielinski()
# ---------------------------------------------------------------------------

def test_single_phase_turbulent_branch_wires_gnielinski():
    """WIRING test: the turbulent single-phase branch (Re >= 2300) labels
    itself "Gnielinski" and its HTC equals the standalone gnielinski() result
    evaluated on the model's own inlet state.

    This asserts the plumbing only — that solve_channel calls gnielinski()
    with the model's Re/Pr/k/D_h convention and uses the result unchanged.
    The PHYSICS of gnielinski() is validated independently against a published
    value in tests/test_correlations.py::test_gnielinski_cengel_ghajar_ex8_5
    (Çengel & Ghajar 2025, Ex 8-5: Nu ~= 69.4, h ~= 1460).
    """
    D = 0.010  # 10 mm + G=1000 -> Re ~= 11,765 (turbulent branch)
    L = 0.5
    G = 1000.0
    T_in = 300.0
    P_in = 101_325.0
    q = 10_000.0  # low enough to stay single-phase, well below T_sat

    geo = _round_tube(D, L)
    result = solve_channel(geo, G=G, T_in=T_in, P_in=P_in, q_flux=q, n_cells=1)
    cell = result.cells[0]

    # Reproduce the model's exact inlet-state convention: liquid props from
    # liquid_state_at_Ph(P_in, h_in), Re from G*D_h/mu.
    h_in = CP.PropsSI("H", "P", P_in, "T", T_in, "Water")
    liq = liquid_state_at_Ph(P_in, h_in)
    Re = G * D / liq.mu
    assert Re >= 2300.0  # confirm turbulent branch is the one under test
    h_gnielinski = gnielinski(Re, liq.Pr) * liq.k / D

    assert cell.regime == Regime.SINGLE_PHASE
    assert cell.correlation == "Gnielinski"
    assert cell.h_eff == pytest.approx(h_gnielinski, rel=1e-12)
    assert cell.T_wall == pytest.approx(T_in + q / h_gnielinski, rel=1e-12)


def test_single_phase_multi_cell_all_sp():
    """Multi-cell channel at low heat flux: all cells remain single-phase."""
    geo = _round_tube(D=0.010, L=0.5)
    result = solve_channel(
        geo, G=1000.0, T_in=300.0, P_in=101_325.0,
        q_flux=10_000.0, n_cells=20,
    )
    assert all(c.regime == Regime.SINGLE_PHASE for c in result.cells)
    assert result.total_pressure_drop is not None
    assert result.total_pressure_drop > 0.0
    assert result.chf_fully_checked is True  # no boiling cells → vacuously true


# ---------------------------------------------------------------------------
# 2. Energy conservation
# ---------------------------------------------------------------------------

def test_energy_conservation_closes():
    """Total enthalpy rise equals integrated heat input (machine epsilon)."""
    geo = _round_tube(D=0.010, L=0.5)
    result = solve_channel(
        geo, G=1000.0, T_in=300.0, P_in=101_325.0,
        q_flux=10_000.0, n_cells=50,
    )
    # Forward Euler march conserves energy exactly by construction
    assert result.energy_balance_error < 1e-12


def test_energy_conservation_variable_flux():
    """Energy conservation with spatially varying heat flux."""
    geo = _round_tube(D=0.010, L=0.5)
    # Linearly increasing heat flux
    n = 20
    q_profile = [5000.0 + 500.0 * i for i in range(n)]
    result = solve_channel(
        geo, G=1000.0, T_in=300.0, P_in=101_325.0,
        q_flux=q_profile, n_cells=n,
    )
    assert result.energy_balance_error < 1e-12


# ---------------------------------------------------------------------------
# 3. Regime detection on constructed states
# ---------------------------------------------------------------------------

def test_regime_transition_sp_to_subcooled_boiling():
    """Channel with transition from single-phase to subcooled boiling.

    Conditions chosen so q_applied < q_onb at the inlet but q_applied > q_onb
    downstream (where subcooling has shrunk).  At T_in=370 K (3.12 K subcooling,
    1 atm), the intersection-based q_onb = 54.7 kW/m² at the inlet; it drops to
    ~25 kW by T_bulk≈372.5 K.  Applied q = 50 kW < 54.7 kW → first cells SP;
    transition occurs once local q_onb crosses below 50 kW.

    Why these specific conditions: any q >= q_onb(T_in) puts the inlet cell
    directly into boiling, eliminating the SP region entirely.  The original
    q=100 kW produced an all-boiling channel (100 kW > 55 kW threshold) — that
    was an ill-posed test, not a model bug.
    """
    geo = _round_tube(D=0.010, L=0.5)
    result = solve_channel(
        geo, G=1000.0, T_in=370.0, P_in=101_325.0,
        q_flux=50_000.0, n_cells=50,
    )
    regimes = [c.regime for c in result.cells]

    # Must contain both regimes
    assert Regime.SINGLE_PHASE in regimes
    assert Regime.SUBCOOLED_BOILING in regimes

    # Transition is monotonic
    first_boiling = regimes.index(Regime.SUBCOOLED_BOILING)
    assert all(r == Regime.SINGLE_PHASE for r in regimes[:first_boiling])
    assert all(
        r == Regime.SUBCOOLED_BOILING for r in regimes[first_boiling:]
    )


def test_saturated_regime_detected():
    """Channel enters saturated boiling when bulk reaches saturation.

    T_in=372 K (1.15 K subcooling), q=120 kW/m^2 (below CHF ~139 kW).
    Bulk crosses T_sat partway along channel.
    """
    geo = _round_tube(D=0.010, L=0.2)
    result = solve_channel(
        geo, G=1000.0, T_in=372.0, P_in=101_325.0,
        q_flux=120_000.0, n_cells=50,
    )
    regimes = [c.regime for c in result.cells]
    assert Regime.SATURATED_BOILING in regimes

    # Saturated cells have unchecked CHF (no Katto-Ohno)
    assert result.cells_with_unchecked_chf > 0
    assert result.chf_fully_checked is False


# ---------------------------------------------------------------------------
# 4. CHF breach raises
# ---------------------------------------------------------------------------

def test_chf_exceeded_raises():
    """Genuine in-envelope burnout raises CHFExceededError (assessable path).

    Under the Option-4 envelope guard, a subcooled-CHF burnout is raised only
    when the CHF is ASSESSABLE — in-envelope AND the outlet stays subcooled at
    CHF (x_o < 0).  Conditions here: 10 bar, G=5000, D=3mm, L=50mm (L/D=16.7),
    T_in=420 K (~33 K subcooling) → x_o ≈ -0.034 (subcooled outlet),
    q_CHF ≈ 5.6 MW/m².  Applying 10 MW/m² guarantees exceedance at the first
    boiling cell.

    (The former conditions L=100mm / T_in=440 K reached the outlet saturation
    boundary at CHF, x_o ≈ +0.002, which Option 4 now correctly reclassifies as
    a saturated-regime handoff rather than a subcooled burnout — see
    test_chf_saturated_handoff_flags_not_raises.)
    """
    geo = _round_tube(D=0.003, L=0.050)
    with pytest.raises(CHFExceededError) as exc_info:
        solve_channel(
            geo, G=5000.0, T_in=420.0, P_in=1_000_000.0,
            q_flux=10_000_000.0, n_cells=5,
        )
    err = exc_info.value
    assert err.q_applied == 10_000_000.0
    assert err.q_chf > 0.0
    assert err.q_applied >= err.q_chf


def test_chf_out_of_envelope_flags_not_raises():
    """G below the Hall & Mudawar floor → cells flagged not-assessable, no raise.

    G=200 kg/m²·s (< 300 floor).  A subcooled-boiling cell must carry
    chf_assessable=False with an extrapolation reason, q_chf=None, and the
    solve must NOT raise CHFExceededError (the correlation cannot answer here —
    it is a genuine "not assessable", not a burnout).
    """
    geo = _round_tube(D=0.003, L=0.050)
    result = solve_channel(
        geo, G=200.0, T_in=447.0, P_in=1_000_000.0,
        q_flux=1_500_000.0, n_cells=10,
    )
    subcooled = [c for c in result.cells if c.regime == Regime.SUBCOOLED_BOILING]
    assert subcooled, "test needs at least one subcooled-boiling cell"
    c = subcooled[0]
    assert c.chf_assessable is False
    assert c.q_chf is None
    assert "extrapolation" in c.chf_reason
    # wall temperature / HTC / quality still computed and finite
    assert c.T_wall > c.T_bulk
    assert c.h_eff > 0.0


def test_chf_saturated_handoff_flags_not_raises():
    """x_o ≥ 0 at CHF → cells flagged saturated-handoff, no raise.

    The former burnout conditions (L=100mm, T_in=440 K) reach outlet saturation
    at CHF (x_o ≈ +0.002).  Under Option 4 this routes to the saturated-regime
    handoff — a DIFFERENT signal from out-of-envelope — and must not raise.
    """
    geo = _round_tube(D=0.003, L=0.100)
    result = solve_channel(
        geo, G=5000.0, T_in=440.0, P_in=1_000_000.0,
        q_flux=10_000_000.0, n_cells=5,
    )
    boiling = [c for c in result.cells if c.regime != Regime.SINGLE_PHASE]
    assert boiling
    assert all(c.chf_assessable is False for c in boiling)
    assert all(c.q_chf is None for c in boiling)
    subcooled = [c for c in boiling if c.regime == Regime.SUBCOOLED_BOILING]
    assert subcooled, "need a subcooled-boiling cell to exercise the handoff path"
    assert "saturated" in subcooled[0].chf_reason


# ---------------------------------------------------------------------------
# 5. ONB continuity — T_w jump at ONB cell is zero
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("T_in,q_flux,L", [
    # Sweep spans 30–200 kW/m² with subcooling chosen so that each case
    # has q_applied < q_onb(T_in) (SP at inlet) but q_applied > q_onb
    # somewhere downstream (transition exists).  See q_onb table:
    #   T_bulk=340 → q_onb=287kW, T_bulk=360 → q_onb=148kW,
    #   T_bulk=370 → q_onb=55kW,  T_bulk=371 → q_onb=44kW.
    (371.0, 30_000.0, 1.0),    # near-sat, low flux
    (370.0, 40_000.0, 0.5),    # low subcool, moderate flux
    (370.0, 50_000.0, 0.5),    # low subcool, moderate flux
    (365.0, 80_000.0, 1.0),    # 8K subcool, 80 kW
    (360.0, 100_000.0, 1.0),   # 13K subcool, 100 kW
    (340.0, 200_000.0, 1.0),   # 33K subcool, 200 kW
])
def test_onb_continuity(T_in, q_flux, L):
    """T_w is continuous across the ONB transition cell — swept over flux/subcooling.

    Continuity by construction: at the ONB cell the BR interpolation's boiling
    term max(0, BR - q_onb) = 0, so T_w_BR collapses to T_w_SP.  This must hold
    regardless of heat flux magnitude — the only requirement is that a transition
    (SP→subcooled boiling) exists in the channel.

    Tolerance: <0.1% relative jump in (T_w - T_bulk) across the transition cell.
    Observed values are 0.01–0.06% (driven solely by property variation over one dz).
    """
    geo = _round_tube(D=0.010, L=L)
    result = solve_channel(
        geo, G=1000.0, T_in=T_in, P_in=101_325.0,
        q_flux=q_flux, n_cells=200,
    )
    regimes = [c.regime for c in result.cells]

    # Verify transition exists
    assert Regime.SINGLE_PHASE in regimes, (
        f"No SP cells — q_applied={q_flux} exceeds q_onb at inlet. "
        f"Test conditions are ill-posed."
    )
    assert Regime.SUBCOOLED_BOILING in regimes, (
        f"No boiling cells — q_applied={q_flux} below q_onb everywhere. "
        f"Channel too short or flux too low."
    )

    # Find the transition cell
    first_boiling = regimes.index(Regime.SUBCOOLED_BOILING)
    assert first_boiling > 0

    last_sp = result.cells[first_boiling - 1]
    first_sb = result.cells[first_boiling]

    # Compare (T_wall - T_bulk) across the transition.  Absolute T_wall differs
    # by one dz of bulk heating, so the wall-excess is the fair comparison.
    delta_sp = last_sp.T_wall - last_sp.T_bulk
    delta_sb = first_sb.T_wall - first_sb.T_bulk

    relative_jump = abs(delta_sb - delta_sp) / delta_sp
    assert relative_jump < 0.001, (
        f"T_w discontinuity at ONB (T_in={T_in}, q={q_flux/1000:.0f} kW/m²): "
        f"(T_w-T_b) jumps from {delta_sp:.4f} to {delta_sb:.4f} K "
        f"({relative_jump*100:.3f}% change)"
    )


# ---------------------------------------------------------------------------
# 6. BR interpolation limits
# ---------------------------------------------------------------------------

def test_partial_boiling_collapses_to_sp_at_onset():
    """At q just above q_onb, partial boiling T_w equals the SP value.

    The boiling term max(0, BR - q_onb) ≈ 0 at onset, so the
    interpolation gives T_w ≈ T_w_sp = T_w_onb.
    """
    # Set up conditions
    P_bar = 1.0
    T_sat = 373.15
    T_bulk = 350.0
    h_sp = 15_000.0  # representative

    T_w_onb = _find_onb_wall_temp(P_bar, h_sp, T_bulk, T_sat)
    q_onb = h_sp * (T_w_onb - T_bulk)
    q_onb_br = bergles_rohsenow_curve(P_bar, T_w_onb - T_sat)

    # Apply q just 0.1% above onset
    q_applied = q_onb * 1.001

    T_w = _solve_partial_boiling(
        q_applied, h_sp, T_bulk, T_sat, P_bar, q_onb_br, T_w_onb
    )

    # Should be very close to T_w_onb (single-phase value at onset)
    T_w_sp = T_bulk + q_applied / h_sp
    assert T_w == pytest.approx(T_w_sp, rel=1e-3)


def test_partial_boiling_approaches_boiling_curve_at_high_superheat():
    """At high q, T_w approaches the BR boiling curve value.

    When the boiling term dominates, T_w ≈ T_sat + ΔT_sat where
    BR(P, ΔT_sat) ≈ q_applied.
    """
    P_bar = 1.0
    T_sat = 373.15
    T_bulk = 350.0
    h_sp = 15_000.0

    T_w_onb = _find_onb_wall_temp(P_bar, h_sp, T_bulk, T_sat)
    q_onb_br = bergles_rohsenow_curve(P_bar, T_w_onb - T_sat)

    # Very high heat flux — deep into boiling
    q_applied = 2_000_000.0  # 2 MW/m^2

    T_w = _solve_partial_boiling(
        q_applied, h_sp, T_bulk, T_sat, P_bar, q_onb_br, T_w_onb
    )

    # At this T_w, the BR curve should be close to q_applied
    delta_T_sat = T_w - T_sat
    q_br_at_Tw = bergles_rohsenow_curve(P_bar, delta_T_sat)

    # The BR term dominates, so q_applied ≈ q_br_at_Tw
    # (with some convective contribution from h_sp*(T_w-T_bulk))
    # Check that BR contribution is >90% of total
    q_fc = h_sp * (T_w - T_bulk)
    boiling_fraction = (q_br_at_Tw - q_onb_br) / q_applied
    assert boiling_fraction > 0.9, (
        f"At high q, boiling should dominate: "
        f"BR fraction = {boiling_fraction:.3f}"
    )


# ---------------------------------------------------------------------------
# 7. Structural / envelope
# ---------------------------------------------------------------------------

def test_rectangular_channel_flags_envelope_violation():
    """Rectangular cross-section logs envelope violation."""
    W, H = 0.001, 0.003
    D_h = 2 * W * H / (W + H)
    geo = ChannelGeometry(
        D_h=D_h,
        L=0.1,
        A_flow=W * H,
        P_heated=W + 2 * H,  # three-sided heating
        cross_section=CrossSection.RECTANGULAR,
        aspect_ratio=H / W,
    )
    result = solve_channel(
        geo, G=2000.0, T_in=300.0, P_in=101_325.0,
        q_flux=50_000.0, n_cells=5,
    )
    # Every cell should flag the rectangular violation
    for cell in result.cells:
        assert any("Rectangular" in v for v in cell.envelope_violations)


def test_round_tube_laminar_nu436_no_violation():
    """Round-tube laminar branch (Re < 2300) uses Nu = 4.36 and flags nothing.

    Small D + low G -> Re ~= 588 (laminar).  The branch must apply the
    fully-developed laminar round-tube Nusselt number for the H1 (constant
    surface heat flux) boundary condition, Nu = 4.36, and -- unlike the old
    clamped Dittus-Boelter path -- must NOT raise an out-of-envelope flag,
    because laminar fully-developed Nu is in-envelope.

    Nu = 4.36 source: Çengel & Ghajar, *Heat and Mass Transfer*, fully-developed
    laminar flow in a circular tube, constant-q'' (H1) table value.
    """
    D = 0.001
    geo = _round_tube(D=D, L=0.05)
    P_in = 101_325.0
    T_in = 300.0
    result = solve_channel(
        geo, G=500.0, T_in=T_in, P_in=P_in,
        q_flux=10_000.0, n_cells=3,
    )

    # Confirm the laminar branch is under test
    h_in = CP.PropsSI("H", "P", P_in, "T", T_in, "Water")
    liq = liquid_state_at_Ph(P_in, h_in)
    Re = 500.0 * D / liq.mu
    assert Re < 2300.0
    h_expected = 4.36 * liq.k / D

    for cell in result.cells:
        assert cell.regime == Regime.SINGLE_PHASE
        assert cell.correlation == "laminar round-tube Nu=4.36 (H1)"
        # Inlet cell HTC matches Nu=4.36 exactly (downstream cells drift only
        # via property variation over dz, so check the first cell tightly).
        assert cell.envelope_violations == ()
    assert result.cells[0].h_eff == pytest.approx(h_expected, rel=1e-12)


def test_rectangular_laminar_nu3():
    """Rectangular laminar branch (Re < 2300) wires qu_mudawar_nu3(beta).

    At the Stage-2 Qu & Mudawar geometry (231 um x 713 um) and a laminar
    operating point (G=255, T_in=60 C -> Re ~= 191), the single-phase HTC must
    equal qu_mudawar_nu3(beta) * k / D_h on the model's own inlet state, with
    beta = short/long = 231/713.

    The 5.27 polynomial value is NOT asserted as an independent published
    number -- it is our own evaluation of Eq. (11).  The function is instead
    anchored non-circularly via:
      * the companion 4-wall polynomial Nu4(0.324) -> 4.85 +/- 0.02, the
        Shah & London (1978) tabulated 4-sided value (Qu & Mudawar 2003 Eq. 12);
      * the parallel-plate limit Nu3(0) = Nu4(0) = 8.235 (both polynomials
        reduce to the H1 infinite-parallel-plate value at beta -> 0).
    """
    # --- non-circular anchors on the polynomial itself ---
    def nu4(b):  # Qu & Mudawar 2003 Eq. (12), 4-wall — check only, not shipped
        return 8.235 * (
            1.0 - 2.042 * b + 3.085 * b**2 - 2.477 * b**3
            + 1.058 * b**4 - 0.186 * b**5
        )

    beta = 231.0 / 713.0  # = 0.32398, short/long
    assert nu4(beta) == pytest.approx(4.85, abs=0.02)        # Shah & London 4-wall
    assert qu_mudawar_nu3(0.0) == pytest.approx(8.235, abs=1e-9)  # parallel-plate H1
    assert nu4(0.0) == pytest.approx(8.235, abs=1e-9)            # same limit, 4-wall

    # --- wiring: model rectangular laminar branch uses Nu3(beta) ---
    W, H = 231e-6, 713e-6
    D_h = 2 * W * H / (W + H)
    geo = ChannelGeometry(
        D_h=D_h, L=0.0448, A_flow=W * H,
        P_heated=W + 2 * H,  # three-sided heating
        cross_section=CrossSection.RECTANGULAR,
        aspect_ratio=H / W,
    )
    G = 255.0
    T_in = 333.15  # 60 C
    P_in = 1.17e5
    q = 50_000.0   # low enough to stay single-phase below CHF
    result = solve_channel(geo, G=G, T_in=T_in, P_in=P_in, q_flux=q, n_cells=1)
    cell = result.cells[0]

    h_in = CP.PropsSI("H", "P", P_in, "T", T_in, "Water")
    liq = liquid_state_at_Ph(P_in, h_in)
    Re = G * D_h / liq.mu
    assert Re < 2300.0  # confirm rectangular laminar branch is under test
    h_expected = qu_mudawar_nu3(min(W, H) / max(W, H)) * liq.k / D_h

    assert cell.regime == Regime.SINGLE_PHASE
    assert cell.correlation == "Qu-Mudawar Nu3 (laminar, 3-wall)"
    assert cell.h_eff == pytest.approx(h_expected, rel=1e-12)


def test_q_flux_length_mismatch_raises():
    """ValueError if q_flux sequence length != n_cells."""
    geo = _round_tube(D=0.010, L=0.5)
    with pytest.raises(ValueError, match="q_flux length"):
        solve_channel(
            geo, G=1000.0, T_in=300.0, P_in=101_325.0,
            q_flux=[10_000.0, 20_000.0], n_cells=5,
        )

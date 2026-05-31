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
from two_phase_cp.correlations.single_phase import dittus_boelter


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
# 1. Limiting case — single-phase reproduces Dittus-Boelter
# ---------------------------------------------------------------------------

def test_single_phase_single_cell_matches_dittus_boelter():
    """Single-cell all-SP channel: T_wall = T_in + q/h_DB exactly.

    Independent hand calc at inlet state (P_in, T_in) vs model output.
    No discretization error for single cell evaluated at inlet.
    """
    D = 0.010  # 10 mm — keeps Re > 10,000
    L = 0.5
    G = 1000.0
    T_in = 300.0
    P_in = 101_325.0
    q = 10_000.0  # low enough to stay well below T_sat

    geo = _round_tube(D, L)
    result = solve_channel(geo, G=G, T_in=T_in, P_in=P_in, q_flux=q, n_cells=1)
    cell = result.cells[0]

    # Independent computation at inlet state
    mu = CP.PropsSI("V", "P", P_in, "T", T_in, "Water")
    k = CP.PropsSI("L", "P", P_in, "T", T_in, "Water")
    Pr = CP.PropsSI("Prandtl", "P", P_in, "T", T_in, "Water")
    Re = G * D / mu
    Nu = dittus_boelter(Re, Pr, n=0.4)
    h_db = Nu * k / D
    T_wall_expected = T_in + q / h_db

    assert cell.regime == Regime.SINGLE_PHASE
    assert cell.T_wall == pytest.approx(T_wall_expected, rel=1e-10)
    assert cell.correlation == "Dittus-Boelter"


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
    """CHFExceededError when q exceeds subcooled CHF.

    At 10 bar, G=5000, D=3mm: q_CHF ~ 2 MW/m^2.
    Apply 10 MW/m^2 to guarantee exceedance at the first boiling cell.
    """
    geo = _round_tube(D=0.003, L=0.100)
    with pytest.raises(CHFExceededError) as exc_info:
        solve_channel(
            geo, G=5000.0, T_in=440.0, P_in=1_000_000.0,
            q_flux=10_000_000.0, n_cells=5,
        )
    err = exc_info.value
    assert err.q_applied == 10_000_000.0
    assert err.q_chf > 0.0
    assert err.q_applied >= err.q_chf


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


def test_laminar_re_flags_envelope_violation():
    """Low Re flags Dittus-Boelter out-of-envelope."""
    # Small D + low G → Re < 10,000
    geo = _round_tube(D=0.001, L=0.05)
    result = solve_channel(
        geo, G=500.0, T_in=300.0, P_in=101_325.0,
        q_flux=10_000.0, n_cells=3,
    )
    for cell in result.cells:
        assert any("Re=" in v and "laminar" in v for v in cell.envelope_violations)


def test_q_flux_length_mismatch_raises():
    """ValueError if q_flux sequence length != n_cells."""
    geo = _round_tube(D=0.010, L=0.5)
    with pytest.raises(ValueError, match="q_flux length"):
        solve_channel(
            geo, G=1000.0, T_in=300.0, P_in=101_325.0,
            q_flux=[10_000.0, 20_000.0], n_cells=5,
        )

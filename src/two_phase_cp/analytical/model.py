"""1D segmented analytical model for heated channel flow.

Forward-marches energy balance from inlet to outlet.  Properties evaluated
at local (P, h) state — sequential, no global iteration.

Regime detection:
  - Single-phase: laminar/turbulent branched, hard switch at Re=2300 —
    Gnielinski (turbulent), Qu & Mudawar 2003 Nu3 (laminar rectangular) or
    round-tube Nu=4.36 (laminar round)
  - Subcooled boiling: Bergles & Rohsenow (1964) partial boiling interpolation
  - Saturated boiling: Kandlikar 1990 (default)
  - CHF (subcooled): Hall & Mudawar 2000, envelope-guarded (Option 4). Three
    outcomes — genuine in-envelope burnout (q_applied >= q_chf) raises
    CHFExceededError; out-of-envelope or saturated-regime (x_o >= 0) cells are
    flagged not-assessable (chf_assessable=False + chf_reason), never raised.

Source for partial boiling interpolation:
  Bergles & Rohsenow (1964), J. Heat Transfer, 86, 365-372.

Known gaps (documented, not yet implemented):
  - Saturated CHF correlation (Katto-Ohno) — saturated cells have unchecked CHF
  - Developed nucleate boiling correlation — the FDB asymptote in the partial
    boiling interpolation defaults to the BR incipience curve (legacy stand-in).
    Selectable via fdb_correlation kwarg; Jens-Lottes and Thom inverses now
    available but out-of-range at Stage-2 pressures (1.17 bar vs 34.5 bar floor).
  - Two-phase pressure drop (Friedel, Lockhart-Martinelli) — two-phase cells
    report pressure_drop = None
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import CoolProp.CoolProp as CP
from scipy.optimize import brentq

from two_phase_cp.analytical._types import (
    CellResult,
    ChannelGeometry,
    ChannelResult,
    CHFExceededError,
    CrossSection,
    Regime,
)
from two_phase_cp.correlations.boiling import jens_lottes_1951_flux, kandlikar_1990
from two_phase_cp.correlations.chf import (
    REASON_SATURATED_HANDOFF,
    SubcooledCHFStatus,
    hall_mudawar_2000_assess,
)
from two_phase_cp.correlations.onb import bergles_rohsenow_onb
from two_phase_cp.correlations.single_phase import (
    _petukhov_friction,
    gnielinski,
    qu_mudawar_nu3,
)
from two_phase_cp.properties.water import (
    liquid_state_at_Ph,
    water_properties_at_pressure,
)

# BR incipience: used for ONB detection (_find_onb_wall_temp).  This path is
# unaffected by the FDB-asymptote default below — ONB detection always uses BR.
_br_onb_curve = bergles_rohsenow_onb
# Legacy alias — test_analytical.py imports this for expected-value calculations.
bergles_rohsenow_curve = _br_onb_curve


def _jens_lottes_fdb(P_bar: float, delta_T_sat: float) -> float:
    """Default FDB nucleate-boiling asymptote: Jens & Lottes (1951), flux form.

    Model-internal (P_bar, delta_T_sat) → q″ signature; adapts
    jens_lottes_1951_flux, whose signature is (delta_T_sat, P_sat_Pa).
    """
    return jens_lottes_1951_flux(delta_T_sat, P_bar * 1e5)


# FDB asymptote used by the partial-boiling interpolation when the caller does
# NOT pass fdb_correlation.  Default is Jens & Lottes (1951); the BR incipience
# curve remains available by passing it back explicitly via fdb_correlation.
_DEFAULT_FDB_CURVE = _jens_lottes_fdb


# ---------------------------------------------------------------------------
# Partial boiling helpers
# ---------------------------------------------------------------------------


def _find_onb_wall_temp(
    P_bar: float,
    h_sp: float,
    T_bulk: float,
    T_sat: float,
) -> float:
    """Find T_w at intersection of single-phase line and BR boiling curve.

    Solves: BR(P, T_w - T_sat) = h_sp * (T_w - T_bulk)

    The intersection defines the ONB wall temperature.  Below this T_w the
    single-phase line exceeds the boiling curve (no boiling); above it the
    boiling curve exceeds the single-phase line (boiling possible).

    Returns T_w_onb [K].
    """

    def residual(T_w: float) -> float:
        delta_T_sat = T_w - T_sat
        if delta_T_sat <= 0.0:
            q_br = 0.0
        else:
            q_br = _br_onb_curve(P_bar, delta_T_sat)
        q_fc = h_sp * (T_w - T_bulk)
        return q_br - q_fc

    # At T_sat: BR=0, q_fc = h_sp*(T_sat-T_bulk) > 0 → residual < 0
    # At T_sat+100: BR >> q_fc typically → residual > 0
    return brentq(residual, T_sat, T_sat + 100.0, xtol=1e-6)


def _solve_partial_boiling(
    q_applied: float,
    h_sp: float,
    T_bulk: float,
    T_sat: float,
    P_bar: float,
    q_onb: float,
    T_w_onb: float,
    fdb_curve: Callable[[float, float], float] | None = None,
) -> float:
    """Find T_w via Bergles & Rohsenow (1964) partial boiling interpolation.

    q = sqrt( [h_sp*(T_w - T_bulk)]^2 + [max(0, FDB(P, T_w-T_sat) - q_onb)]^2 )

    Bracket: [T_w_onb, T_bulk + q_applied/h_sp].

    Parameters
    ----------
    fdb_curve : callable(P_bar, delta_T_sat) → q [W/m²], optional
        FDB boiling curve used as the nucleate boiling asymptote.
        Default (None) falls back to the BR incipience curve (legacy stand-in).

    Source: Bergles & Rohsenow (1964), J. Heat Transfer, 86, 365-372.
    """
    if fdb_curve is None:
        fdb_curve = _br_onb_curve

    T_w_sp = T_bulk + q_applied / h_sp  # upper bracket: single-phase T_w

    def residual(T_w: float) -> float:
        q_fc = h_sp * (T_w - T_bulk)
        delta_T_sat = T_w - T_sat
        if delta_T_sat > 0.0:
            q_fdb = fdb_curve(P_bar, delta_T_sat)
            boiling = max(0.0, q_fdb - q_onb)
        else:
            boiling = 0.0
        return (q_fc**2 + boiling**2) ** 0.5 - q_applied

    return brentq(residual, T_w_onb, T_w_sp, xtol=1e-6)


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------


def solve_channel(
    geometry: ChannelGeometry,
    G: float,
    T_in: float,
    P_in: float,
    q_flux: float | Sequence[float],
    n_cells: int,
    *,
    fdb_correlation: Callable[[float, float], float] | None = None,
) -> ChannelResult:
    """Solve 1D segmented energy balance along a heated channel.

    Parameters
    ----------
    geometry : ChannelGeometry
        Channel geometry specification.
    G : float
        Mass flux [kg/(m^2*s)].
    T_in : float
        Inlet temperature [K].
    P_in : float
        Inlet pressure [Pa].
    q_flux : float or sequence of float
        Applied wall heat flux [W/m^2].  Scalar for uniform; sequence of
        length *n_cells* for spatially varying.
    n_cells : int
        Number of axial segments.
    fdb_correlation : callable(delta_T_sat, P_sat_Pa) → q [W/m²], optional
        FDB boiling curve for the nucleate boiling asymptote in the
        partial boiling interpolation.  Signature: (delta_T_sat [K],
        P_sat [Pa]) → q″ [W/m²].  Default (None) uses Jens & Lottes (1951)
        (flux form).  Pass the BR incipience curve explicitly to restore the
        former stand-in.  ONB detection is unaffected and always uses BR.

    Returns
    -------
    ChannelResult
        Aggregate and per-cell results.

    Raises
    ------
    CHFExceededError
        If applied heat flux meets or exceeds subcooled CHF at any cell.
    """
    dz = geometry.L / n_cells

    # Heat flux array
    if isinstance(q_flux, (int, float)):
        q = [float(q_flux)] * n_cells
    else:
        q = list(q_flux)
        if len(q) != n_cells:
            raise ValueError(
                f"q_flux length {len(q)} != n_cells {n_cells}"
            )

    # Inlet state
    h_in = CP.PropsSI("H", "P", P_in, "T", T_in, "Water")

    # Channel-level subcooled CHF — envelope-guarded (Hall & Mudawar 2000,
    # Option 4).  Assessed once at inlet conditions; the outcome gates how
    # subcooled-boiling cells report/enforce CHF below.
    sat_inlet = water_properties_at_pressure(P_in)
    h_f_inlet = CP.PropsSI("H", "P", P_in, "Q", 0, "Water")
    x_i_prime = (h_in - h_f_inlet) / sat_inlet.h_fg
    chf_assessment = hall_mudawar_2000_assess(
        G=G,
        D=geometry.D_h,
        L=geometry.L,
        P=P_in,
        x_i_prime=x_i_prime,
        rho_f=sat_inlet.rho_f,
        rho_g=sat_inlet.rho_g,
        h_fg=sat_inlet.h_fg,
        sigma=sat_inlet.sigma,
    )

    # FDB curve for partial boiling interpolation.
    # Adapt fdb_correlation(delta_T_sat, P_Pa) to internal (P_bar, dT) signature;
    # default to Jens & Lottes (1951) when the caller passes nothing.
    if fdb_correlation is not None:
        def _fdb_curve(P_bar: float, delta_T_sat: float) -> float:
            return fdb_correlation(delta_T_sat, P_bar * 1e5)
    else:
        _fdb_curve = _DEFAULT_FDB_CURVE  # Jens & Lottes (1951) default asymptote

    # Forward march
    h_march = h_in
    P_march = P_in
    cells: list[CellResult] = []

    for i in range(n_cells):
        z_center = (i + 0.5) * dz
        q_i = q[i]

        # Saturation properties at local pressure
        sat = water_properties_at_pressure(P_march)

        # Liquid state at (P, h) — local bulk properties
        liq = liquid_state_at_Ph(P_march, h_march)

        # Thermodynamic equilibrium quality
        h_f = CP.PropsSI("H", "P", P_march, "Q", 0, "Water")
        x_eq = (h_march - h_f) / sat.h_fg

        # Reynolds number
        Re = G * geometry.D_h / liq.mu

        # Envelope checks
        violations: list[str] = []
        if geometry.cross_section == CrossSection.RECTANGULAR:
            violations.append(
                "Rectangular channel — round-tube correlations applied via D_h"
            )

        # --- Regime detection and HTC computation ---

        if x_eq >= 0.0:
            # SATURATED BOILING
            regime = Regime.SATURATED_BOILING
            correlation_name = "Kandlikar 1990"

            x_clamped = max(x_eq, 1e-6)
            h_tp = kandlikar_1990(
                x=x_clamped,
                G=G,
                D_h=geometry.D_h,
                q_flux=q_i,
                h_fg=sat.h_fg,
                rho_f=sat.rho_f,
                rho_g=sat.rho_g,
                mu_f=sat.mu_f,
                cp_f=sat.cp_f,
                k_f=sat.k_f,
                Pr_f=sat.Pr_f,
            )
            T_wall = sat.T_sat + q_i / h_tp
            h_eff = h_tp
            q_onb_val: float | None = None
            q_chf_val: float | None = None
            chf_checked = False
            # Locally saturated (x_eq >= 0): subcooled CHF does not govern —
            # saturated-CHF correlation (gap #1) applies but is not implemented.
            chf_assessable = False
            chf_reason: str | None = REASON_SATURATED_HANDOFF
            validation_status = (
                "UNVALIDATED — test skipped (Collier & Thome 3e)"
            )

            if geometry.D_h * 1000 < 3.0 or geometry.D_h * 1000 > 25.0:
                violations.append(
                    f"D_h={geometry.D_h*1000:.2f} mm outside "
                    f"Kandlikar 3-25 mm range"
                )

        else:
            # Subcooled: single-phase forced-convection HTC.
            # Laminar/turbulent branched with a hard switch at Re = 2300
            # (no clamp, no blend), replacing the former clamped Dittus-Boelter.
            if Re >= 2300.0:
                # Turbulent: Gnielinski (smooth tube, Petukhov friction).
                Nu_sp = gnielinski(Re, liq.Pr)
                sp_method = "Gnielinski"
                sp_validation = "validated (Gnielinski 1976)"
            elif geometry.aspect_ratio is not None:
                # Laminar, rectangular: Qu & Mudawar 2003 Eq. (11) Nu3(beta),
                # beta = short side / long side <= 1.
                ar = geometry.aspect_ratio
                beta = ar if ar <= 1.0 else 1.0 / ar
                Nu_sp = qu_mudawar_nu3(beta)
                sp_method = "Qu-Mudawar Nu3 (laminar, 3-wall)"
                sp_validation = (
                    "validated (Qu & Mudawar 2003 Eq. 11; Shah & London 1978)"
                )
            else:
                # Laminar, round tube: fully-developed constant-q'' (H1) limit.
                Nu_sp = 4.36
                sp_method = "laminar round-tube Nu=4.36 (H1)"
                sp_validation = "validated (Incropera 7e Table 8.1, H1)"
            h_sp = Nu_sp * liq.k / geometry.D_h

            T_w_sp = liq.T + q_i / h_sp
            delta_T_sat = T_w_sp - sat.T_sat
            P_bar = P_march / 1e5

            # ONB detection via intersection of SP line with BR curve
            if delta_T_sat > 0.0:
                T_w_onb = _find_onb_wall_temp(P_bar, h_sp, liq.T, sat.T_sat)
                q_onb_local = h_sp * (T_w_onb - liq.T)
                is_boiling = q_i >= q_onb_local
            else:
                T_w_onb = sat.T_sat
                q_onb_local = None
                is_boiling = False

            if is_boiling:
                # SUBCOOLED BOILING — partial boiling interpolation
                regime = Regime.SUBCOOLED_BOILING
                correlation_name = "Bergles-Rohsenow partial boiling"

                # q_onb for the interpolation = FDB curve at the ONB superheat.
                # This ensures the boiling term is exactly zero at ONB.
                _fdb_at_onb = _fdb_curve if _fdb_curve is not None else _br_onb_curve
                q_onb_fdb = _fdb_at_onb(
                    P_bar, T_w_onb - sat.T_sat
                )

                T_wall = _solve_partial_boiling(
                    q_i, h_sp, liq.T, sat.T_sat,
                    P_bar, q_onb_fdb, T_w_onb,
                    fdb_curve=_fdb_curve,
                )
                h_eff = (
                    q_i / (T_wall - liq.T)
                    if T_wall > liq.T
                    else float("inf")
                )
                q_onb_val = q_onb_local
                # CHF reporting/enforcement gated by the channel-level guarded
                # assessment (Option 4): only an ASSESSABLE (in-envelope,
                # subcooled-outlet) CHF is a real number and can trigger burnout.
                if chf_assessment.status == SubcooledCHFStatus.ASSESSABLE:
                    q_chf_val = chf_assessment.q_chf
                    chf_checked = True
                    chf_assessable = True
                    chf_reason = None
                else:
                    # OUT_OF_ENVELOPE or SATURATED_HANDOFF — flag, never raise.
                    q_chf_val = None
                    chf_checked = False
                    chf_assessable = False
                    chf_reason = chf_assessment.reason

                if _fdb_curve is not None:
                    validation_status = (
                        "UNVALIDATED — partial boiling interpolation; "
                        "FDB asymptote from user-supplied correlation"
                    )
                else:
                    validation_status = (
                        "UNVALIDATED — partial boiling interpolation; "
                        "FDB asymptote approximated by BR incipience curve"
                    )

                # Genuine physical burnout only when subcooled CHF is assessable.
                if (
                    chf_assessment.status == SubcooledCHFStatus.ASSESSABLE
                    and q_i >= chf_assessment.q_chf
                ):
                    raise CHFExceededError(i, q_i, chf_assessment.q_chf)
            else:
                # SINGLE-PHASE
                regime = Regime.SINGLE_PHASE
                correlation_name = sp_method

                T_wall = T_w_sp
                h_eff = h_sp
                q_onb_val = q_onb_local
                q_chf_val = None
                chf_checked = False
                # Not boiling — subcooled CHF is not a concern for this cell.
                chf_assessable = True
                chf_reason = None
                validation_status = sp_validation

        # Pressure drop — single-phase only
        if regime == Regime.SINGLE_PHASE:
            f = _petukhov_friction(max(Re, 3000.1))
            dp = f * (dz / geometry.D_h) * (G**2 / (2.0 * liq.rho))
            pressure_drop: float | None = dp
        else:
            pressure_drop = None

        cells.append(
            CellResult(
                z=z_center,
                T_bulk=liq.T,
                T_wall=T_wall,
                T_sat=sat.T_sat,
                x_eq=x_eq,
                h_bulk=h_march,
                regime=regime,
                correlation=correlation_name,
                h_eff=h_eff,
                q_applied=q_i,
                q_onb=q_onb_val,
                q_chf=q_chf_val,
                chf_checked=chf_checked,
                chf_assessable=chf_assessable,
                chf_reason=chf_reason,
                envelope_violations=tuple(violations),
                validation_status=validation_status,
                pressure_drop=pressure_drop,
            )
        )

        # Update state for next cell
        h_march = h_march + q_i * geometry.P_heated * dz / (G * geometry.A_flow)
        if pressure_drop is not None:
            P_march = P_march - pressure_drop
        # else: P unchanged (two-phase dp not implemented)

    # --- Aggregate results ---
    cells_tuple = tuple(cells)
    cells_no_dp = sum(1 for c in cells_tuple if c.pressure_drop is None)
    total_dp: float | None
    if cells_no_dp > 0:
        total_dp = None
    else:
        total_dp = sum(c.pressure_drop for c in cells_tuple)  # type: ignore[arg-type]

    boiling_cells = [
        c for c in cells_tuple if c.regime != Regime.SINGLE_PHASE
    ]
    cells_unchecked_chf = sum(
        1 for c in boiling_cells if not c.chf_checked
    )
    chf_fully = len(boiling_cells) == 0 or all(
        c.chf_checked for c in boiling_cells
    )

    # Energy balance verification (should be ~machine epsilon)
    total_heat = sum(q_i * geometry.P_heated * dz for q_i in q)
    expected_dh = total_heat / (G * geometry.A_flow)
    actual_dh = h_march - h_in
    energy_error = abs(actual_dh - expected_dh) / max(abs(expected_dh), 1e-30)

    return ChannelResult(
        cells=cells_tuple,
        total_pressure_drop=total_dp,
        cells_without_pressure_drop=cells_no_dp,
        cells_with_unchecked_chf=cells_unchecked_chf,
        chf_fully_checked=chf_fully,
        energy_balance_error=energy_error,
    )

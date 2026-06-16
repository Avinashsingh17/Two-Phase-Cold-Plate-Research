"""Saturated flow boiling heat transfer correlations."""

from __future__ import annotations

import math

from two_phase_cp.correlations._envelope import CorrelationEnvelope
from two_phase_cp.correlations.single_phase import dittus_boelter


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _lockhart_martinelli_Xtt(
    x: float,
    rho_f: float,
    rho_g: float,
    mu_f: float,
    mu_g: float,
) -> float:
    """Lockhart-Martinelli turbulent-turbulent parameter.

    X_tt = (mu_f/mu_g)^0.1 * ((1-x)/x)^0.9 * (rho_g/rho_f)^0.5
    """
    return (mu_f / mu_g) ** 0.1 * ((1.0 - x) / x) ** 0.9 * (rho_g / rho_f) ** 0.5


# ---------------------------------------------------------------------------
# Chen 1966
# ---------------------------------------------------------------------------

def _chen_F(X_tt: float) -> float:
    """Chen enhancement factor F = f(1/X_tt).

    Butterworth (1979) algebraic fit of the original Chen (1966) graphical
    correlation:
        if 1/X_tt <= 0.1: F = 1.0
        else: F = 2.35 * (0.213 + 1/X_tt)^0.736
    """
    inv_Xtt = 1.0 / X_tt
    if inv_Xtt <= 0.1:
        return 1.0
    return 2.35 * (0.213 + inv_Xtt) ** 0.736


def _chen_S(Re_tp: float) -> float:
    """Chen suppression factor S = f(Re_tp).

    Butterworth (1979) algebraic fit:
        S = 1 / (1 + 2.53e-6 * Re_tp^1.17)
    """
    return 1.0 / (1.0 + 2.53e-6 * Re_tp**1.17)


def _forster_zuber(
    delta_T_sat: float,
    delta_P_sat: float,
    rho_f: float,
    rho_g: float,
    mu_f: float,
    h_fg: float,
    sigma: float,
    cp_f: float,
    k_f: float,
) -> float:
    """Forster-Zuber pool boiling microconvection HTC [W/(m^2·K)].

    h_mic = 0.00122 * [k_f^0.79 * cp_f^0.45 * rho_f^0.49 /
            (sigma^0.5 * mu_f^0.29 * h_fg^0.24 * rho_g^0.24)] *
            delta_T_sat^0.24 * delta_P_sat^0.75

    Source: Forster & Zuber (1955).
    """
    numerator = k_f**0.79 * cp_f**0.45 * rho_f**0.49
    denominator = sigma**0.5 * mu_f**0.29 * h_fg**0.24 * rho_g**0.24
    return 0.00122 * (numerator / denominator) * delta_T_sat**0.24 * delta_P_sat**0.75


def chen_1966(
    x: float,
    G: float,
    D_h: float,
    q_flux: float,
    rho_f: float,
    rho_g: float,
    mu_f: float,
    mu_g: float,
    h_fg: float,
    sigma: float,
    cp_f: float,
    k_f: float,
    Pr_f: float,
    T_sat: float,
    delta_T_sat: float,
    P_sat: float,
    *,
    dP_dT_sat: float | None = None,
    F_multiplier: float = 1.0,
    S_multiplier: float = 1.0,
) -> float:
    """Chen (1966) superposition correlation for saturated flow boiling.

    Returns two-phase heat transfer coefficient h_tp [W/(m^2·K)].

    h_tp = h_mac * F * F_multiplier + h_mic * S * S_multiplier

    Parameters
    ----------
    x : float
        Thermodynamic equilibrium quality [-].
    G : float
        Mass flux [kg/(m^2·s)].
    D_h : float
        Hydraulic diameter [m].
    q_flux : float
        Heat flux [W/m^2].
    rho_f, rho_g : float
        Saturated liquid and vapor densities [kg/m^3].
    mu_f, mu_g : float
        Dynamic viscosities [Pa·s].
    h_fg : float
        Latent heat of vaporization [J/kg].
    sigma : float
        Surface tension [N/m].
    cp_f : float
        Liquid specific heat [J/(kg·K)].
    k_f : float
        Liquid thermal conductivity [W/(m·K)].
    Pr_f : float
        Liquid Prandtl number [-].
    T_sat : float
        Saturation temperature [K].
    delta_T_sat : float
        Wall superheat T_w - T_sat [K].
    P_sat : float
        Saturation pressure [Pa].
    dP_dT_sat : float or None
        Clausius-Clapeyron slope dP/dT at saturation [Pa/K].
        If None, approximated as h_fg / (T_sat * (1/rho_g - 1/rho_f)).
    F_multiplier : float
        Multiplicative correction on the internal enhancement factor F.
        Default 1.0 (no correction).  Use for calibration per the Ozguc 2024
        pattern: preserve functional form, parameterize deviation.
    S_multiplier : float
        Multiplicative correction on the internal suppression factor S.
        Default 1.0 (no correction).

    Returns
    -------
    float
        Two-phase heat transfer coefficient [W/(m^2·K)].

    Source: Chen (1966).  F and S algebraic fits from Butterworth (1979).
    Forster-Zuber microconvection term from Forster & Zuber (1955).
    """
    # Clausius-Clapeyron dP/dT
    if dP_dT_sat is None:
        dP_dT_sat = h_fg / (T_sat * (1.0 / rho_g - 1.0 / rho_f))

    # Lockhart-Martinelli parameter
    X_tt = _lockhart_martinelli_Xtt(x, rho_f, rho_g, mu_f, mu_g)

    # Enhancement factor F
    F = _chen_F(X_tt) * F_multiplier

    # Liquid-only Reynolds number and macro-convective HTC
    Re_f = G * (1.0 - x) * D_h / mu_f
    Nu_f = dittus_boelter(Re_f, Pr_f, n=0.4)
    h_mac = Nu_f * k_f / D_h

    # Suppression factor S
    Re_tp = Re_f * F**1.25
    S = _chen_S(Re_tp) * S_multiplier

    # Forster-Zuber microconvection HTC
    delta_P_sat = dP_dT_sat * delta_T_sat
    h_mic = _forster_zuber(
        delta_T_sat, delta_P_sat,
        rho_f, rho_g, mu_f, h_fg, sigma, cp_f, k_f,
    )

    return h_mac * F + h_mic * S


chen_1966.envelope = CorrelationEnvelope(  # type: ignore[attr-defined]
    name="Chen 1966",
    source="Chen (1966)",
    fluids=("any",),
    geometry="macroscale saturated convective boiling, D_h > ~10 mm",
    d_h_range_mm=None,  # TODO: wiki says >~10 mm but no hard bound
    pressure_range_bar=None,
    mass_flux_range_kg_m2s=None,
    quality_range=None,  # TODO: source from paper
    reported_accuracy="Qu & Mudawar 2003: MAE 43.9% on water microchannels",
    known_failure_modes=(
        "Underpredicts microchannel and subcooled regimes",
    ),
    wiki_page="QuMudawar2003_microchannel_boiling_I",
)


# ---------------------------------------------------------------------------
# Kandlikar 1990
# ---------------------------------------------------------------------------

# F_fl is fluid-SURFACE specific. Listed values are for copper/commercial
# tubing. For stainless steel, use F_fl = 1.0 for all fluids.
# [Kandlikar/Shoji/Dhir, Handbook of Phase Change, 1999, Ch. 15 (Kandlikar),
#  Table 3 footnote]
KANDLIKAR_F_FL: dict[str, float] = {
    # --- Kandlikar 1990 Table 4 AND Handbook 1999 Table 3 ---
    "water": 1.00,       # Kandlikar 1990, Table 4
    "R-11": 1.30,        # Kandlikar 1990, Table 4
    "R-12": 1.50,        # Kandlikar 1990, Table 4
    "R-13B1": 1.31,      # Kandlikar 1990, Table 4
    "R-22": 2.20,        # Kandlikar 1990, Table 4
    "R-113": 1.30,       # Kandlikar 1990, Table 4
    "R-114": 1.24,       # Kandlikar 1990, Table 4
    "R-152a": 1.10,      # Kandlikar 1990, Table 4
    # --- Kandlikar 1990 Table 4 only (not in Handbook Table 3) ---
    "nitrogen": 4.70,    # Kandlikar 1990, Table 4
    "neon": 3.50,        # Kandlikar 1990, Table 4
    # --- Handbook 1999 Table 3 only (copper/commercial tubing) ---
    "R-134a": 1.63,      # Kandlikar/Shoji/Dhir 1999, Handbook Ch. 15, Table 3
    "R-32/R-125": 0.488, # Kandlikar/Shoji/Dhir 1999, Handbook Ch. 15, Table 3 (60/40 wt% azeotrope)
    "kerosene": 3.30,    # Kandlikar/Shoji/Dhir 1999, Handbook Ch. 15, Table 3
}


def kandlikar_1990(
    x: float,
    G: float,
    D_h: float,
    q_flux: float,
    h_fg: float,
    rho_f: float,
    rho_g: float,
    mu_f: float,
    cp_f: float,
    k_f: float,
    Pr_f: float,
    *,
    F_fl: float = 1.0,
) -> float:
    """Kandlikar (1990) saturated flow boiling correlation.

    Returns two-phase heat transfer coefficient h_tp [W/(m^2·K)].

    h_tp = max(h_NBD, h_CBD)

    Nucleate Boiling Dominant (NBD):
        h_NBD = [0.6683 Co^(-0.2) (1-x)^0.8 + 1058.0 Bo^0.7 (1-x)^0.8 F_fl] h_lo

    Convective Boiling Dominant (CBD):
        h_CBD = [1.1360 Co^(-0.9) (1-x)^0.8 + 667.2 Bo^0.7 (1-x)^0.8 F_fl] h_lo

    Parameters
    ----------
    x : float
        Thermodynamic equilibrium quality [-].
    G : float
        Mass flux [kg/(m^2·s)].
    D_h : float
        Hydraulic diameter [m].
    q_flux : float
        Heat flux [W/m^2].
    h_fg : float
        Latent heat of vaporization [J/kg].
    rho_f, rho_g : float
        Saturated liquid and vapor densities [kg/m^3].
    mu_f : float
        Liquid dynamic viscosity [Pa·s].
    cp_f : float
        Liquid specific heat [J/(kg·K)].
    k_f : float
        Liquid thermal conductivity [W/(m·K)].
    Pr_f : float
        Liquid Prandtl number [-].
    F_fl : float
        Fluid-dependent parameter.  Default 1.0 (water).
        See ``KANDLIKAR_F_FL`` for values from the original paper.

    Returns
    -------
    float
        Two-phase heat transfer coefficient [W/(m^2·K)].

    Source: Kandlikar (1990).  Valid: D_h 3–25 mm, round tube.
    Known failure: h decreases with x in microchannels D_h < 1 mm
    (Qu & Mudawar 2003, MAE 49.4%).
    """
    # All-liquid HTC via Dittus-Boelter
    Re_lo = G * D_h / mu_f
    Nu_lo = dittus_boelter(Re_lo, Pr_f, n=0.4)
    h_lo = Nu_lo * k_f / D_h

    # Dimensionless groups
    Co = (rho_g / rho_f) ** 0.5 * ((1.0 - x) / x) ** 0.8  # Convection number
    Bo = q_flux / (G * h_fg)  # Boiling number

    one_minus_x_08 = (1.0 - x) ** 0.8

    # Nucleate Boiling Dominant
    h_NBD = (0.6683 * Co ** (-0.2) * one_minus_x_08
             + 1058.0 * Bo**0.7 * one_minus_x_08 * F_fl) * h_lo

    # Convective Boiling Dominant
    h_CBD = (1.1360 * Co ** (-0.9) * one_minus_x_08
             + 667.2 * Bo**0.7 * one_minus_x_08 * F_fl) * h_lo

    return max(h_NBD, h_CBD)


kandlikar_1990.envelope = CorrelationEnvelope(  # type: ignore[attr-defined]
    name="Kandlikar 1990",
    source="Kandlikar (1990)",
    fluids=tuple(KANDLIKAR_F_FL.keys()),
    geometry="round tube",
    d_h_range_mm=(3.0, 25.0),
    pressure_range_bar=None,  # TODO: source from paper
    mass_flux_range_kg_m2s=None,  # TODO: source from paper
    quality_range=None,  # TODO: source from paper
    reported_accuracy="Qu & Mudawar 2003: MAE 49.4% on water microchannels",
    known_failure_modes=(
        "h decreases with x in microchannels D_h < 1 mm — Qu & Mudawar 2003",
    ),
    wiki_page="QuMudawar2003_microchannel_boiling_I",
)


# ---------------------------------------------------------------------------
# Thom et al. 1965 — FDB wall-superheat correlation (water only)
# ---------------------------------------------------------------------------

def thom_1965(
    q_flux: float,
    P_sat: float,
) -> float:
    """Thom et al. (1965) fully-developed boiling wall superheat.

    Returns wall superheat ΔT_sat [K].

    Dimensional form (valid for q″ in MW/m², p in bar, ΔT_sat in K):
        ΔT_sat = 22.65 · q″^0.5 · exp(−p / 87)

    This function accepts SI inputs (q″ in W/m², P in Pa) and converts
    internally.  Water only.

    Parameters
    ----------
    q_flux : float
        Heat flux [W/m^2].
    P_sat : float
        Saturation pressure [Pa].
        Valid ≈ 3.45–6.90 MPa (500–1000 psi, 34.5–69 bar) per Todreas &
        Kazimi, *Nuclear Systems I*, p. 538.

    Returns
    -------
    float
        Wall superheat ΔT_sat = T_w − T_sat [K].

    Source: Kandlikar, Shoji & Dhir (1999), *Handbook of Phase Change*,
    Ch. 15 (Kandlikar), Table 1 (p. 376).  Coefficients 22.65, exponent
    0.5, and exp denominator 87 bar are from that table.
    SI constants independently confirmed by Todreas & Kazimi, *Nuclear
    Systems I*, Eq. 12-28b (22.7 / 0.5 / 8.7 MPa — the 22.65 vs 22.7
    difference is rounding between sources).
    """
    # --- Unit conversion: SI → dimensional form ---
    q_MW = q_flux * 1.0e-6       # W/m² → MW/m²
    p_bar = P_sat * 1.0e-5       # Pa → bar

    # At Qu & Mudawar Stage-2 condition (1.17 bar) this correlation is
    # ~30× below its validity floor (34.5 bar) — out-of-range placeholder.
    return 22.65 * q_MW**0.5 * math.exp(-p_bar / 87.0)


def thom_1965_flux(
    delta_T_sat: float,
    P_sat: float,
) -> float:
    """Inverse of thom_1965: heat flux from wall superheat.

    Returns q″ [W/m²] given ΔT_sat [K] and P_sat [Pa].

    Analytical inverse of: ΔT = 22.65 · q_MW^0.5 · exp(−p/87)
    → q_MW = (ΔT / (22.65 · exp(−p/87)))²
    """
    p_bar = P_sat * 1.0e-5       # Pa → bar
    q_MW = (delta_T_sat / (22.65 * math.exp(-p_bar / 87.0))) ** 2
    return q_MW * 1.0e6           # MW/m² → W/m²


# ---------------------------------------------------------------------------
# Jens-Lottes 1951 — FDB wall-superheat correlation (water only)
# ---------------------------------------------------------------------------

def jens_lottes_1951(
    q_flux: float,
    P_sat: float,
) -> float:
    """Jens & Lottes (1951) fully-developed boiling wall superheat.

    Returns wall superheat ΔT_sat [K].

    Dimensional form (valid for q″ in MW/m², p in bar, ΔT_sat in K):
        ΔT_sat = 25 · q″^0.25 · exp(−p / 62)

    This function accepts SI inputs (q″ in W/m², P in Pa) and converts
    internally.  Water only.

    Parameters
    ----------
    q_flux : float
        Heat flux [W/m^2].
    P_sat : float
        Saturation pressure [Pa].
        Valid ≈ 3.45–6.90 MPa (500–1000 psi, 34.5–69 bar) per Todreas &
        Kazimi, *Nuclear Systems I*, p. 538.

    Returns
    -------
    float
        Wall superheat ΔT_sat = T_w − T_sat [K].

    Source: Kandlikar, Shoji & Dhir (1999), *Handbook of Phase Change*,
    Ch. 15 (Kandlikar), Table 1 (p. 376).  Coefficients 25, exponent
    0.25, and exp denominator 62 bar are from that table.
    SI constants independently confirmed by Todreas & Kazimi, *Nuclear
    Systems I*, Eq. 12-27b (25 / 0.25 / 6.2 MPa).
    """
    # --- Unit conversion: SI → dimensional form ---
    q_MW = q_flux * 1.0e-6       # W/m² → MW/m²
    p_bar = P_sat * 1.0e-5       # Pa → bar

    # At Qu & Mudawar Stage-2 condition (1.17 bar) this correlation is
    # ~30× below its validity floor (34.5 bar) — out-of-range placeholder.
    return 25.0 * q_MW**0.25 * math.exp(-p_bar / 62.0)


def jens_lottes_1951_flux(
    delta_T_sat: float,
    P_sat: float,
) -> float:
    """Inverse of jens_lottes_1951: heat flux from wall superheat.

    Returns q″ [W/m²] given ΔT_sat [K] and P_sat [Pa].

    Analytical inverse of: ΔT = 25 · q_MW^0.25 · exp(−p/62)
    → q_MW = (ΔT / (25 · exp(−p/62)))⁴
    """
    p_bar = P_sat * 1.0e-5       # Pa → bar
    q_MW = (delta_T_sat / (25.0 * math.exp(-p_bar / 62.0))) ** 4
    return q_MW * 1.0e6           # MW/m² → W/m²

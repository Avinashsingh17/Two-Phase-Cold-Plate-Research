"""Critical heat flux (CHF) correlations."""

from __future__ import annotations

from two_phase_cp.correlations._envelope import CorrelationEnvelope


def hall_mudawar_2000(
    G: float,
    D: float,
    L: float,
    x_i_prime: float,
    rho_f: float,
    rho_g: float,
    h_fg: float,
    sigma: float,
    *,
    C1: float = 0.0722,
    C2: float = -0.312,
    C3: float = -0.644,
    C4: float = 0.900,
    C5: float = 0.724,
) -> float:
    """Hall & Mudawar (2000) inlet-conditions subcooled CHF correlation.

    Returns critical heat flux q_CHF [W/m^2].

    Bo_CHF = C1 We_D^C2 (rho_f/rho_g)^C3 [1 - C4 (rho_f/rho_g)^C5 x_i']
             / [1 + 4 C1 C4 We_D^C2 (rho_f/rho_g)^(C3+C5) (L/D)]

    q_CHF = Bo_CHF * G * h_fg

    Parameters
    ----------
    G : float
        Mass flux [kg/(m^2·s)].  Valid: 300–30 000.
    D : float
        Tube diameter or hydraulic diameter [m].  Valid: 0.25–15 mm.
    L : float
        Heated length [m].
    x_i_prime : float
        Pseudo-inlet quality (< 0 for subcooled).
        x_i' = (h_in - h_f(P_out)) / h_fg(P_out).
    rho_f : float
        Saturated liquid density [kg/m^3].
    rho_g : float
        Saturated vapor density [kg/m^3].
    h_fg : float
        Latent heat of vaporization [J/kg].
    sigma : float
        Surface tension [N/m].
    C1–C5 : float
        Correlation constants (defaults to paper values, Table 4).

    Returns
    -------
    float
        Critical heat flux [W/m^2].

    Notes
    -----
    Pressure dependence enters entirely through rho_f, rho_g, h_fg, sigma
    from the caller.

    Source: Hall & Mudawar (2000), Table 4.
    MAE: 10.3% against 4860 subcooled CHF data points (water, round tubes).
    Wiki: [[HallMudawar2000_subcooled_CHF]], lines 26–45.
    """
    We_D = G**2 * D / (rho_f * sigma)
    dr = rho_f / rho_g

    numerator = C1 * We_D**C2 * dr**C3 * (1.0 - C4 * dr**C5 * x_i_prime)
    denominator = 1.0 + 4.0 * C1 * C4 * We_D**C2 * dr ** (C3 + C5) * (L / D)

    Bo_chf = numerator / denominator
    return Bo_chf * G * h_fg


# Envelope sourced from wiki/papers/HallMudawar2000_subcooled_CHF.md
# d_h_range: line 54 (D: 0.25–15 mm)
# pressure_range: line 54 (P: 1–200 bar)
# mass_flux_range: line 54 (G: 300–30,000 kg/m²s)
# quality_range: line 55–56 (x_i: −2.0 to 0.0)
# reported_accuracy: line 64 (MAE 10.3%, RMS 14.3%)
# failure_mode: line 93 (geometry mismatch)
hall_mudawar_2000.envelope = CorrelationEnvelope(  # type: ignore[attr-defined]
    name="Hall & Mudawar 2000",
    source="Hall & Mudawar (2000)",
    fluids=("water",),
    geometry="round tube, uniformly heated",
    d_h_range_mm=(0.25, 15.0),
    pressure_range_bar=(1.0, 200.0),
    mass_flux_range_kg_m2s=(300.0, 30_000.0),
    quality_range=(-2.0, 0.0),
    reported_accuracy="MAE 10.3%, RMS 14.3% (4860 pts)",
    known_failure_modes=(
        "Rectangular microchannel geometry outside validated envelope",
    ),
    wiki_page="HallMudawar2000_subcooled_CHF",
)

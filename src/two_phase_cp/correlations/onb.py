"""Onset of nucleate boiling (ONB) correlations."""

from __future__ import annotations

from two_phase_cp.correlations._envelope import CorrelationEnvelope


def bergles_rohsenow_onb(
    P: float,
    delta_T_sat: float,
) -> float:
    """Bergles & Rohsenow (1964) onset of nucleate boiling criterion.

    Returns heat flux at ONB, q_onb [W/m^2].

    q_onb = 1082 * P^1.156 * (1.8 * delta_T_sat)^(2.16 / P^0.0234)

    Parameters
    ----------
    P : float
        System pressure [bar].  Valid: 1–138 bar.
    delta_T_sat : float
        Wall superheat T_w - T_sat [K].  Must be > 0.

    Returns
    -------
    float
        Heat flux at ONB [W/m^2].

    Notes
    -----
    Water only.  The SI form used here (P in bar, q" in W/m^2) follows
    Incropera & Bergman, *Fundamentals of Heat and Mass Transfer*, 8th ed.,
    converted from the original imperial form (P in psi, q" in BTU/hr·ft^2)
    by Bergles & Rohsenow (1964).

    Source: Bergles & Rohsenow (1964).
    """
    exponent = 2.16 / P**0.0234
    return 1082.0 * P**1.156 * (1.8 * delta_T_sat) ** exponent


bergles_rohsenow_onb.envelope = CorrelationEnvelope(  # type: ignore[attr-defined]
    name="Bergles-Rohsenow ONB",
    source="Bergles & Rohsenow (1964)",
    fluids=("water",),
    geometry="round tube and rectangular channel",
    d_h_range_mm=None,
    pressure_range_bar=(1.0, 138.0),
    mass_flux_range_kg_m2s=None,
    quality_range=None,
    reported_accuracy="",  # TODO: source reported accuracy from paper
    known_failure_modes=("Non-water fluids",),
    wiki_page="",
)

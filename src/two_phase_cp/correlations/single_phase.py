"""Single-phase forced convection heat transfer correlations."""

from __future__ import annotations

import math
from typing import Literal

from two_phase_cp.correlations._envelope import CorrelationEnvelope


# ---------------------------------------------------------------------------
# Dittus-Boelter
# ---------------------------------------------------------------------------

def dittus_boelter(
    Re: float,
    Pr: float,
    *,
    n: Literal[0.3, 0.4] = 0.4,
) -> float:
    """Dittus-Boelter correlation for turbulent single-phase internal flow.

    Returns Nusselt number Nu.

    Nu = 0.023 * Re^0.8 * Pr^n

    Parameters
    ----------
    Re : float
        Reynolds number.  Valid: Re > 10 000.
    Pr : float
        Prandtl number.  Valid: 0.6 < Pr < 160.
    n : Literal[0.3, 0.4]
        Exponent — 0.4 for heating (T_w > T_b), 0.3 for cooling (T_w < T_b).

    Returns
    -------
    float
        Nusselt number.

    Source: Dittus & Boelter (1930), as presented in Incropera & Bergman,
    *Fundamentals of Heat and Mass Transfer*, 8th ed.
    """
    return 0.023 * Re**0.8 * Pr**n


dittus_boelter.envelope = CorrelationEnvelope(  # type: ignore[attr-defined]
    name="Dittus-Boelter",
    source="Dittus & Boelter (1930)",
    fluids=("any",),
    geometry="round tube/duct, smooth wall, fully developed turbulent",
    d_h_range_mm=None,
    pressure_range_bar=None,
    mass_flux_range_kg_m2s=None,
    quality_range=None,
    reported_accuracy="",
    known_failure_modes=(
        "Laminar flow Re < 10000",
        "Entrance effects L/D < 10",
        "Large property variation across boundary layer (use Sieder-Tate)",
    ),
    wiki_page="",
)


# ---------------------------------------------------------------------------
# Sieder-Tate
# ---------------------------------------------------------------------------

def sieder_tate(
    Re: float,
    Pr: float,
    mu_bulk: float,
    mu_wall: float,
) -> float:
    """Sieder-Tate correlation for turbulent single-phase internal flow.

    Accounts for viscosity variation between bulk and wall temperatures.

    Returns Nusselt number Nu.

    Nu = 0.027 * Re^0.8 * Pr^(1/3) * (mu_bulk / mu_wall)^0.14

    Parameters
    ----------
    Re : float
        Reynolds number.  Valid: Re > 10 000.
    Pr : float
        Prandtl number.  Valid: 0.7 < Pr < 16 700.
    mu_bulk : float
        Dynamic viscosity at bulk fluid temperature [Pa·s].
    mu_wall : float
        Dynamic viscosity at wall temperature [Pa·s].

    Returns
    -------
    float
        Nusselt number.

    Source: Sieder & Tate (1936).
    """
    return 0.027 * Re**0.8 * Pr ** (1.0 / 3.0) * (mu_bulk / mu_wall) ** 0.14


sieder_tate.envelope = CorrelationEnvelope(  # type: ignore[attr-defined]
    name="Sieder-Tate",
    source="Sieder & Tate (1936)",
    fluids=("any",),
    geometry="round tube/duct, smooth wall, fully developed turbulent",
    d_h_range_mm=None,
    pressure_range_bar=None,
    mass_flux_range_kg_m2s=None,
    quality_range=None,
    reported_accuracy="",
    known_failure_modes=("Laminar flow Re < 10000",),
    wiki_page="",
)


# ---------------------------------------------------------------------------
# Gnielinski
# ---------------------------------------------------------------------------

def _petukhov_friction(Re: float) -> float:
    """Petukhov friction factor for smooth tubes.

    f = (0.790 * ln(Re) - 1.64)^(-2)

    Valid: 3000 < Re < 5e6.
    """
    return (0.790 * math.log(Re) - 1.64) ** (-2)


def gnielinski(
    Re: float,
    Pr: float,
    *,
    f: float | None = None,
) -> float:
    """Gnielinski correlation for transitional/turbulent single-phase flow.

    Returns Nusselt number Nu.

    Nu = (f/8)(Re - 1000) Pr / [1 + 12.7 sqrt(f/8) (Pr^(2/3) - 1)]

    Parameters
    ----------
    Re : float
        Reynolds number.  Valid: 2300 < Re < 5e6.
    Pr : float
        Prandtl number.  Valid: 0.5 < Pr < 2000.
    f : float or None
        Darcy friction factor.  If None, the Petukhov correlation is used
        (smooth tube).  Pass an explicit value for rough tubes or alternate
        friction correlations.

    Returns
    -------
    float
        Nusselt number.

    Source: Gnielinski (1976).
    """
    if f is None:
        f = _petukhov_friction(Re)
    f8 = f / 8.0
    return f8 * (Re - 1000.0) * Pr / (1.0 + 12.7 * f8**0.5 * (Pr ** (2.0 / 3.0) - 1.0))


gnielinski.envelope = CorrelationEnvelope(  # type: ignore[attr-defined]
    name="Gnielinski",
    source="Gnielinski (1976)",
    fluids=("any",),
    geometry="round tube/duct, smooth wall",
    d_h_range_mm=None,
    pressure_range_bar=None,
    mass_flux_range_kg_m2s=None,
    quality_range=None,
    reported_accuracy="",
    known_failure_modes=("Below Re = 2300 (laminar regime)",),
    wiki_page="",
)


# ---------------------------------------------------------------------------
# Qu & Mudawar (2003) rectangular-channel laminar Nusselt number
# ---------------------------------------------------------------------------

def qu_mudawar_nu3(beta: float) -> float:
    """Fully-developed laminar Nusselt number, 3-wall-heated rectangular duct.

    Polynomial fit in aspect ratio beta (short side / long side, 0 < beta <= 1):

        Nu3 = 8.235 (1 - 1.883 b + 3.767 b^2 - 5.814 b^3 + 5.361 b^4 - 2.0 b^5)

    Returns the Nusselt number for three heated walls and one adiabatic wall,
    normalized on the full-perimeter hydraulic diameter D_h = 2 w d / (w + d).

    Parameters
    ----------
    beta : float
        Channel aspect ratio, short side / long side, 0 < beta <= 1.

    Returns
    -------
    float
        Fully-developed laminar Nusselt number (three-wall heating).

    Source
    ------
    Qu & Mudawar (2003), "Flow boiling heat transfer in two-phase micro-channel
    heat sinks - I. Experimental investigation and assessment of correlation
    methods," Int. J. Heat Mass Transfer 46, 2755-2771, Eq. (11).  Qu & Mudawar
    in turn cite Shah & London (1978) [their ref 35] and Bau (1998) [their
    ref 36] for the polynomial coefficients.

    Stated assumptions
    ------------------
    (a) H1 thermal boundary condition - constant axial heat flux, peripherally
        isothermal wall.  Qu & Mudawar do NOT state H1/H2/T; H1 is adopted here
        because a high-conductivity copper substrate smears the peripheral
        wall-temperature distribution, making the isothermal-perimeter
        idealization the right one.
    (b) Fully-developed laminar flow - justified at Stage-2 because the entry
        length is short relative to channel length.  This is the same
        fully-developed Nu that Qu & Mudawar themselves plug into their 3-wall
        correction factor Nu3/Nu4 (their Eq. 10).

    Transcription check (companion 4-wall polynomial, Eq. 12, NOT shipped):
        Nu4 = 8.235 (1 - 2.042 b + 3.085 b^2 - 2.477 b^3 + 1.058 b^4 - 0.186 b^5)
    reproduces the Shah & London 4-wall value 4.85 at b = 231/713 = 0.324.
    """
    return 8.235 * (
        1.0
        - 1.883 * beta
        + 3.767 * beta**2
        - 5.814 * beta**3
        + 5.361 * beta**4
        - 2.0 * beta**5
    )

"""CoolProp wrapper for water saturation properties.

This module isolates all CoolProp calls behind a thin interface so that
correlation functions remain pure numerical functions with no hidden
property lookups.

CoolProp dependency approved per PROJECT_CONTEXT.md "confirm before adding"
rule — approval covers CoolProp only; future dependencies require separate
confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass

import CoolProp.CoolProp as CP


@dataclass(frozen=True)
class WaterProperties:
    """Saturation properties of water at a given pressure."""

    P: float  # Pa
    T_sat: float  # K
    rho_f: float  # kg/m^3
    rho_g: float  # kg/m^3
    mu_f: float  # Pa·s
    mu_g: float  # Pa·s
    h_fg: float  # J/kg
    sigma: float  # N/m
    cp_f: float  # J/(kg·K)
    k_f: float  # W/(m·K)
    Pr_f: float  # dimensionless
    P_crit: float  # Pa (22.064 MPa for water)


def water_properties_at_pressure(P: float) -> WaterProperties:
    """Return saturated water properties at pressure *P* [Pa].

    All properties evaluated at liquid–vapor saturation.

    Parameters
    ----------
    P : float
        Absolute pressure [Pa].

    Returns
    -------
    WaterProperties
        Frozen dataclass with all saturation properties.
    """
    fluid = "Water"
    T_sat = CP.PropsSI("T", "P", P, "Q", 0, fluid)
    rho_f = CP.PropsSI("D", "P", P, "Q", 0, fluid)
    rho_g = CP.PropsSI("D", "P", P, "Q", 1, fluid)
    mu_f = CP.PropsSI("V", "P", P, "Q", 0, fluid)
    mu_g = CP.PropsSI("V", "P", P, "Q", 1, fluid)
    h_f = CP.PropsSI("H", "P", P, "Q", 0, fluid)
    h_g = CP.PropsSI("H", "P", P, "Q", 1, fluid)
    h_fg = h_g - h_f
    sigma = CP.PropsSI("I", "P", P, "Q", 0, fluid)
    cp_f = CP.PropsSI("C", "P", P, "Q", 0, fluid)
    k_f = CP.PropsSI("L", "P", P, "Q", 0, fluid)
    Pr_f = CP.PropsSI("Prandtl", "P", P, "Q", 0, fluid)
    P_crit = CP.PropsSI("Pcrit", "T", 0, "P", 0, fluid)

    return WaterProperties(
        P=P,
        T_sat=T_sat,
        rho_f=rho_f,
        rho_g=rho_g,
        mu_f=mu_f,
        mu_g=mu_g,
        h_fg=h_fg,
        sigma=sigma,
        cp_f=cp_f,
        k_f=k_f,
        Pr_f=Pr_f,
        P_crit=P_crit,
    )

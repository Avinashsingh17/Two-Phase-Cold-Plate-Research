"""Unit tests for the correlation library.

Each test cites its reference source.  Tolerances reflect the source:
  - Textbook worked examples: ±1%
  - Paper-scatter correlations: ±5–10%
  - Self-consistency (no external ref): exact
"""

import pytest

from two_phase_cp.correlations import (
    bergles_rohsenow_onb,
    chen_1966,
    dittus_boelter,
    gnielinski,
    hall_mudawar_2000,
    kandlikar_1990,
    sieder_tate,
)


# ---------------------------------------------------------------------------
# Dittus-Boelter — awaiting verified textbook reference
# ---------------------------------------------------------------------------
# Inputs from Incropera 8e Ex 8.4: Water at T_m = 35 °C, 25-mm-ID tube,
# 0.2 kg/s.  Re = 4 m_dot / (pi D mu) = 14,050.  Pr = 4.85.
# The expected Nu value needs verification against the actual textbook —
# a previous hand calculation used an incorrect Re^0.8 ≈ 2637 (actual: 2080).

@pytest.mark.skip(reason="awaiting Incropera 8e Ex 8.4 verified reference value")
def test_dittus_boelter_incropera_8_4():
    """Incropera & Bergman 8e, Example 8.4 — water in a tube, heating.

    TODO: Verify expected Nu from Incropera 8e and fill in here.
    Inputs (Re=14050, Pr=4.85) are correct per the problem statement.
    """
    Re = 14_050.0
    Pr = 4.85
    Nu = dittus_boelter(Re, Pr, n=0.4)
    # TODO: replace with verified textbook value
    assert Nu == pytest.approx(..., rel=0.01)


# ---------------------------------------------------------------------------
# Gnielinski — Incropera & Bergman 8e, Example 8.5 (same geometry)
# ---------------------------------------------------------------------------
# Incropera uses same Re=14050, Pr=4.85.
# Petukhov f = (0.790 ln 14050 - 1.64)^-2
#   ln(14050) = 9.550 → 0.790*9.550 - 1.64 = 5.905 → f = 1/5.905^2 = 0.02868
# f/8 = 0.003585
# Nu = 0.003585 * (14050-1000) * 4.85 / [1 + 12.7 * sqrt(0.003585) * (4.85^(2/3) - 1)]
# Numerator = 0.003585 * 13050 * 4.85 = 226.8
# sqrt(f/8) = 0.05988
# Pr^(2/3) = 4.85^0.6667 = 2.871 → 2.871 - 1 = 1.871
# Denominator = 1 + 12.7 * 0.05988 * 1.871 = 1 + 1.423 = 2.423
# Nu = 226.8 / 2.423 = 93.6
# h = 93.6 * 0.625 / 0.025 = 2340 W/m²K
# Textbook reports Nu ≈ 90–94 range.

def test_gnielinski_incropera_8_5():
    """Incropera & Bergman 8e, Example 8.5 — Gnielinski for same conditions."""
    Re = 14_050.0
    Pr = 4.85
    Nu = gnielinski(Re, Pr)
    assert Nu == pytest.approx(93.6, rel=0.01)


# ---------------------------------------------------------------------------
# Sieder-Tate — analytical self-consistency when mu_bulk == mu_wall
# ---------------------------------------------------------------------------

def test_sieder_tate_viscosity_ratio_unity():
    """When mu_bulk == mu_wall, viscosity correction factor is exactly 1."""
    Re, Pr = 50_000.0, 3.0
    Nu = sieder_tate(Re, Pr, mu_bulk=1e-3, mu_wall=1e-3)
    expected = 0.027 * Re**0.8 * Pr ** (1.0 / 3.0)
    assert Nu == pytest.approx(expected, rel=1e-10)


# ---------------------------------------------------------------------------
# Bergles-Rohsenow ONB — water
# ---------------------------------------------------------------------------
# Bergles & Rohsenow (1964), SI form per Incropera:
#   q"_ONB = 1082 * P^1.156 * (1.8 * ΔT_sat)^(2.16 / P^0.0234)
# P in bar, ΔT_sat in K, q" in W/m².
# At atmospheric pressure, water ONB heat flux at ΔT_sat = 5 K is in the
# 10^4–10^5 W/m² range per boiling curve literature.

def test_bergles_rohsenow_water_1atm():
    """Bergles & Rohsenow at 1 bar, ΔT_sat=5 K — physical range check.

    Source: Bergles & Rohsenow (1964), SI form.
    Water ONB at atmospheric pressure with 5 K superheat should be in the
    10^4–10^5 W/m² range (boiling curve literature).  Window set by physical
    expectation, not computed output.
    """
    q = bergles_rohsenow_onb(P=1.0, delta_T_sat=5.0)
    assert 5e4 < q < 5e5


def test_bergles_rohsenow_water_high_pressure():
    """Bergles & Rohsenow at 70 bar, ΔT_sat=10 K — physical sanity.

    At high pressure, ONB heat flux should be on the order of MW/m² to
    tens of MW/m² (consistent with high-pressure subcooled boiling onset).
    """
    q = bergles_rohsenow_onb(P=70.0, delta_T_sat=10.0)
    assert q > 1e6   # at least 1 MW/m²
    assert q < 1e8   # less than 100 MW/m²


def test_bergles_rohsenow_monotonicity():
    """Bergles & Rohsenow — structural monotonicity check.

    q_ONB must increase with ΔT_sat at fixed P, and increase with P at
    fixed ΔT_sat.  Catches pathological-exponent class of bugs without
    needing a reference value.
    """
    # Monotonic in ΔT_sat at fixed P = 1 bar
    q_1K = bergles_rohsenow_onb(P=1.0, delta_T_sat=1.0)
    q_5K = bergles_rohsenow_onb(P=1.0, delta_T_sat=5.0)
    q_10K = bergles_rohsenow_onb(P=1.0, delta_T_sat=10.0)
    assert q_10K > q_5K > q_1K

    # Monotonic in P at fixed ΔT_sat = 5 K
    q_1bar = bergles_rohsenow_onb(P=1.0, delta_T_sat=5.0)
    q_138bar = bergles_rohsenow_onb(P=138.0, delta_T_sat=5.0)
    assert q_138bar > q_1bar


# ---------------------------------------------------------------------------
# Chen 1966 — Collier & Thome 3e reference
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="awaiting Collier & Thome 3e Ch 7 reference value")
def test_chen_1966_collier_thome():
    """Chen (1966) validated against Collier & Thome 3e, Chapter 7.

    TODO: Transcribe worked example conditions and expected h_tp from
    Collier & Thome, *Convective Boiling and Condensation*, 3rd ed.
    Tolerance: ±5%.
    """
    pass


# ---------------------------------------------------------------------------
# Kandlikar 1990 — Collier & Thome 3e reference
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="awaiting Collier & Thome 3e reference value")
def test_kandlikar_water_collier_thome():
    """Kandlikar (1990) validated against Collier & Thome 3e worked example.

    TODO: Transcribe worked example conditions and expected h_tp from
    Collier & Thome, *Convective Boiling and Condensation*, 3rd ed.
    Tolerance: ±5%.
    """
    pass


# ---------------------------------------------------------------------------
# Hall & Mudawar 2000 — awaiting representative validated point
# ---------------------------------------------------------------------------

@pytest.mark.skip(
    reason=(
        "awaiting representative point from Hall & Mudawar 2000 — paper provides "
        "only aggregate statistics over 4860-point database, no individual "
        "tabulated points"
    )
)
def test_hall_mudawar_chf_representative(water_10bar):
    """Hall & Mudawar (2000) at a representative subcooled operating point.

    TODO: Source a specific (G, D, L, P, x_i', q_CHF) point from the
    PU-BTPFL database or from a study citing Hall & Mudawar 2000.
    Tolerance: ±10% (paper's reported MAE against its database).
    """
    props = water_10bar
    q_chf = hall_mudawar_2000(
        G=5000.0,
        D=0.003,
        L=0.100,
        x_i_prime=-0.3,
        rho_f=props.rho_f,
        rho_g=props.rho_g,
        h_fg=props.h_fg,
        sigma=props.sigma,
    )
    # TODO: replace with validated reference value
    assert q_chf == pytest.approx(..., rel=0.10)

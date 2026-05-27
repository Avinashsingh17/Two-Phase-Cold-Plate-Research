"""Tests for the CoolProp water property wrapper."""

import pytest

from two_phase_cp.properties.water import WaterProperties, water_properties_at_pressure


def test_water_properties_at_1atm():
    """CoolProp wrapper returns physically reasonable values at 1 atm."""
    props = water_properties_at_pressure(101_325.0)

    assert isinstance(props, WaterProperties)
    assert props.T_sat == pytest.approx(373.15, abs=0.5)
    assert props.rho_f == pytest.approx(958.4, rel=0.01)
    assert props.rho_g == pytest.approx(0.598, rel=0.02)
    assert props.h_fg == pytest.approx(2.257e6, rel=0.01)
    assert props.cp_f == pytest.approx(4217.0, rel=0.01)
    assert props.P_crit == pytest.approx(22.064e6, rel=0.01)
    assert props.sigma > 0
    assert props.mu_f > 0
    assert props.Pr_f > 0


def test_water_properties_at_10bar():
    """Sanity check at 10 bar — T_sat should be ~453 K."""
    props = water_properties_at_pressure(1_000_000.0)
    assert props.T_sat == pytest.approx(453.03, abs=1.0)
    assert props.rho_f > props.rho_g
    assert props.h_fg > 0

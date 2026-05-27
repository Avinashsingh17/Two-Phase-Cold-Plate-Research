"""Shared test fixtures for the two_phase_cp test suite."""

import pytest

from two_phase_cp.properties.water import WaterProperties, water_properties_at_pressure


@pytest.fixture
def water_1atm() -> WaterProperties:
    """Saturated water properties at 1 atm (101325 Pa)."""
    return water_properties_at_pressure(101_325.0)


@pytest.fixture
def water_10bar() -> WaterProperties:
    """Saturated water properties at 10 bar (1 MPa)."""
    return water_properties_at_pressure(1_000_000.0)

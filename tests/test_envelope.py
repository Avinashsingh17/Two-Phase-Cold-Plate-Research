"""Tests for CorrelationEnvelope metadata on all correlation functions."""

from two_phase_cp.correlations import (
    CorrelationEnvelope,
    bergles_rohsenow_onb,
    chen_1966,
    dittus_boelter,
    gnielinski,
    hall_mudawar_2000,
    kandlikar_1990,
    sieder_tate,
)

ALL_CORRELATIONS = [
    dittus_boelter,
    sieder_tate,
    gnielinski,
    bergles_rohsenow_onb,
    chen_1966,
    kandlikar_1990,
    hall_mudawar_2000,
]


def test_every_correlation_has_envelope():
    """Every public correlation function must have a .envelope attribute."""
    for fn in ALL_CORRELATIONS:
        assert hasattr(fn, "envelope"), f"{fn.__name__} missing .envelope"
        assert isinstance(fn.envelope, CorrelationEnvelope), (
            f"{fn.__name__}.envelope is {type(fn.envelope)}, expected CorrelationEnvelope"
        )


def test_known_failure_modes_is_tuple():
    """known_failure_modes must be a tuple (not list, not None)."""
    for fn in ALL_CORRELATIONS:
        modes = fn.envelope.known_failure_modes
        assert isinstance(modes, tuple), (
            f"{fn.__name__}.envelope.known_failure_modes is {type(modes)}"
        )


def test_hall_mudawar_envelope_matches_wiki():
    """Hall & Mudawar 2000 envelope values match wiki/papers/HallMudawar2000_subcooled_CHF.md."""
    env = hall_mudawar_2000.envelope
    assert env.fluids == ("water",)
    assert env.d_h_range_mm == (0.25, 15.0)
    assert env.pressure_range_bar == (1.0, 200.0)
    assert env.mass_flux_range_kg_m2s == (300.0, 30_000.0)
    assert env.quality_range == (-2.0, 0.0)  # inlet quality x_i
    assert env.l_over_d_range == (2.0, 200.0)
    assert env.outlet_quality_range == (-1.0, 0.0)  # x_o
    assert "10.3%" in env.reported_accuracy

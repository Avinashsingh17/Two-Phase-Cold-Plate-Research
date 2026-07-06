"""Correlation envelope metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorrelationEnvelope:
    """Metadata describing validity and provenance of a correlation.

    Attached to each correlation function as a ``.envelope`` attribute.
    """

    name: str
    source: str
    fluids: tuple[str, ...]
    geometry: str
    d_h_range_mm: tuple[float, float] | None
    pressure_range_bar: tuple[float, float] | None
    mass_flux_range_kg_m2s: tuple[float, float] | None
    quality_range: tuple[float, float] | None  # inlet quality x_i where applicable
    reported_accuracy: str
    known_failure_modes: tuple[str, ...]
    wiki_page: str
    # Optional additional bounds (default None for correlations that omit them):
    l_over_d_range: tuple[float, float] | None = None
    outlet_quality_range: tuple[float, float] | None = None  # x_o

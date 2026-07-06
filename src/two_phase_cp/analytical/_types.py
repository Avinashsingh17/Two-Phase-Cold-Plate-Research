"""Data types for the 1D segmented analytical model."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class CrossSection(Enum):
    """Channel cross-section geometry type."""

    ROUND = auto()
    RECTANGULAR = auto()


class Regime(Enum):
    """Heat transfer regime in a channel cell."""

    SINGLE_PHASE = auto()
    SUBCOOLED_BOILING = auto()
    SATURATED_BOILING = auto()


@dataclass(frozen=True)
class ChannelGeometry:
    """Channel geometry specification.

    Parameters
    ----------
    D_h : float
        Hydraulic diameter [m].
    L : float
        Heated length [m].
    A_flow : float
        Flow cross-section area [m^2].
    P_heated : float
        Heated perimeter [m].
    cross_section : CrossSection
        Channel cross-section type.
    aspect_ratio : float or None
        H/W for rectangular channels; None for round.
    """

    D_h: float
    L: float
    A_flow: float
    P_heated: float
    cross_section: CrossSection
    aspect_ratio: float | None = None


@dataclass(frozen=True)
class CellResult:
    """Results for a single axial cell."""

    z: float  # cell center position [m]
    T_bulk: float  # bulk fluid temperature [K]
    T_wall: float  # wall temperature [K]
    T_sat: float  # saturation temperature [K]
    x_eq: float  # thermodynamic equilibrium quality [-]
    h_bulk: float  # bulk enthalpy [J/kg]
    regime: Regime
    correlation: str  # name of correlation / method used
    h_eff: float  # effective HTC [W/(m^2·K)]
    q_applied: float  # applied heat flux [W/m^2]
    q_onb: float | None  # ONB heat flux [W/m^2] (if evaluated)
    q_chf: float | None  # CHF [W/m^2] (if evaluated)
    chf_checked: bool  # whether subcooled CHF was validly evaluated for this cell
    chf_assessable: bool  # False when subcooled CHF cannot be assessed (Option 4)
    chf_reason: str | None  # why not assessable (out-of-envelope vs saturated
    #                         handoff); None when assessable
    envelope_violations: tuple[str, ...]
    validation_status: str
    pressure_drop: float | None  # cell delta-P [Pa]; None for two-phase


@dataclass(frozen=True)
class ChannelResult:
    """Aggregate results for the full channel."""

    cells: tuple[CellResult, ...]
    total_pressure_drop: float | None  # sum of cell dp; None if any cell lacks dp
    cells_without_pressure_drop: int
    cells_with_unchecked_chf: int  # boiling cells without CHF evaluation
    chf_fully_checked: bool  # True only if every boiling cell has CHF check
    energy_balance_error: float  # fractional closure error


class CHFExceededError(Exception):
    """Raised when applied heat flux meets or exceeds critical heat flux."""

    def __init__(self, cell_index: int, q_applied: float, q_chf: float) -> None:
        self.cell_index = cell_index
        self.q_applied = q_applied
        self.q_chf = q_chf
        super().__init__(
            f"CHF exceeded at cell {cell_index}: "
            f"q_applied={q_applied:.0f} W/m^2 >= q_CHF={q_chf:.0f} W/m^2"
        )

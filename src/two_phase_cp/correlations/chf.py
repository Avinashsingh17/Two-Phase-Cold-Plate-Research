"""Critical heat flux (CHF) correlations."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

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
    # Table 4 inlet-conditions (recommended) range, p. 2616.
    d_h_range_mm=(0.25, 15.0),
    pressure_range_bar=(1.0, 200.0),
    mass_flux_range_kg_m2s=(300.0, 30_000.0),
    quality_range=(-2.0, 0.0),  # inlet quality x_i
    l_over_d_range=(2.0, 200.0),
    outlet_quality_range=(-1.0, 0.0),  # x_o
    reported_accuracy="MAE 10.3%, RMS 14.3% (4860 pts)",
    known_failure_modes=(
        "Rectangular microchannel geometry outside validated envelope",
    ),
    wiki_page="HallMudawar2000_subcooled_CHF",
)


# ---------------------------------------------------------------------------
# Envelope-guarded assessment (Option 4)
# ---------------------------------------------------------------------------
# hall_mudawar_2000() above computes unconditionally.  The guard below consults
# the sourced validity envelope (Table 4 inlet-conditions row, p. 2616) and
# refuses to extrapolate, distinguishing two DISTINCT non-numeric outcomes from
# a genuine CHF value.  These are different signals and must not be conflated:
#
#   OUT_OF_ENVELOPE   — a hard input (D, L/D, G, P, x_i) is outside the Table 4
#                       envelope; extrapolation refused ("cannot answer").
#   SATURATED_HANDOFF — the derived outlet quality x_o >= 0; the fluid exits at
#                       or above saturation, so subcooled CHF no longer governs
#                       and a saturated-CHF correlation (Katto-Ohno 1984 /
#                       Lee & Mudawar 2009, gap #1) applies ("wrong tool, here
#                       is the right one") — NOT an error, NOT an extrapolation.


class SubcooledCHFStatus(Enum):
    """Outcome class of an envelope-guarded subcooled-CHF assessment."""

    ASSESSABLE = auto()        # in-envelope, subcooled outlet — q_chf is valid
    OUT_OF_ENVELOPE = auto()   # hard input-bound violation — extrapolation refused
    SATURATED_HANDOFF = auto()  # x_o >= 0 — saturated-CHF regime governs (gap #1)


@dataclass(frozen=True)
class EnvelopeViolation:
    """One breached envelope bound and how far past it the value lies."""

    param: str          # "D", "L/D", "G", "P", "x_i", "x_o"
    value: float
    bound: str          # "low" or "high"
    limit: float
    amount: float       # magnitude past the breached bound (>= 0)
    unit: str


@dataclass(frozen=True)
class SubcooledCHFAssessment:
    """Result of :func:`hall_mudawar_2000_assess`.

    ``q_chf`` is a real number ONLY when ``status is ASSESSABLE``; otherwise it
    is None and ``reason`` explains which of the two non-numeric outcomes
    applies.  ``x_o`` (derived outlet quality) is populated whenever it was
    computed (i.e. inputs passed the hard-bound checks).
    """

    status: SubcooledCHFStatus
    q_chf: float | None          # W/m^2; valid only when ASSESSABLE
    x_o: float | None            # derived outlet quality; None if not computed
    reason: str
    violations: tuple[EnvelopeViolation, ...] = field(default_factory=tuple)


# Table 4 inlet-conditions envelope, Hall & Mudawar 2000, p. 2616. Inclusive.
_HM_D_MM = (0.25, 15.0)
_HM_LD = (2.0, 200.0)
_HM_G = (300.0, 30_000.0)
_HM_P_BAR = (1.0, 200.0)
_HM_XI = (-2.0, 0.0)
_HM_XO = (-1.0, 0.0)

REASON_OUT_OF_ENVELOPE = (
    "not assessable — extrapolation outside the sourced validity range "
    "(Hall & Mudawar 2000, Table 4 inlet-conditions envelope, p. 2616)"
)
REASON_SATURATED_HANDOFF = (
    "not assessable — subcooled regime exited (x_o >= 0, fluid at or above "
    "saturation); saturated-CHF correlation (Katto-Ohno 1984 / Lee & Mudawar "
    "2009, gap #1) governs here and is not implemented"
)


def _bound(param: str, value: float, lo: float, hi: float,
           unit: str) -> EnvelopeViolation | None:
    """Return an EnvelopeViolation if value is outside [lo, hi] (inclusive)."""
    if value < lo:
        return EnvelopeViolation(param, value, "low", lo, lo - value, unit)
    if value > hi:
        return EnvelopeViolation(param, value, "high", hi, value - hi, unit)
    return None


def hall_mudawar_2000_assess(
    G: float,
    D: float,
    L: float,
    P: float,
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
) -> SubcooledCHFAssessment:
    """Envelope-guarded Hall & Mudawar (2000) subcooled CHF (Option 4).

    Consults the Table 4 inlet-conditions envelope (p. 2616) and returns one of
    three outcomes without ever silently extrapolating:

    - ``OUT_OF_ENVELOPE``   — a hard input (D, L/D, G, P, x_i) is outside the
      envelope; ``q_chf`` is None and ``violations`` lists each breached bound.
    - ``SATURATED_HANDOFF`` — derived outlet quality x_o >= 0; ``q_chf`` is None;
      the saturated-CHF regime (gap #1) governs.
    - ``ASSESSABLE``        — in-envelope, subcooled outlet; ``q_chf`` is valid.

    Ordering subtlety (handled explicitly): x_o is derived from the computed CHF
    via Eq. 10 (p. 2612), ``x_o = x_i + 4*Bo*(L/D)`` with ``Bo = q_chf/(G*h_fg)``.
    q_chf is therefore computed BEFORE the regime-handoff test; the x_o check
    never gates the computation it depends on.

    ``P`` [Pa] is required for the pressure-bound check (the bare correlation
    carries pressure only implicitly through the saturated properties).
    """
    # 1. Hard input-bound checks (pre-computation; refuse extrapolation).
    input_checks = (
        _bound("D", D * 1e3, _HM_D_MM[0], _HM_D_MM[1], "mm"),
        _bound("L/D", L / D, _HM_LD[0], _HM_LD[1], "-"),
        _bound("G", G, _HM_G[0], _HM_G[1], "kg/m2s"),
        _bound("P", P / 1e5, _HM_P_BAR[0], _HM_P_BAR[1], "bar"),
        _bound("x_i", x_i_prime, _HM_XI[0], _HM_XI[1], "-"),
    )
    violations = tuple(v for v in input_checks if v is not None)
    if violations:
        return SubcooledCHFAssessment(
            SubcooledCHFStatus.OUT_OF_ENVELOPE, None, None,
            REASON_OUT_OF_ENVELOPE, violations,
        )

    # 2. Compute q_chf FIRST, then derive x_o (Eq. 10, p. 2612).
    q_chf = hall_mudawar_2000(
        G=G, D=D, L=L, x_i_prime=x_i_prime, rho_f=rho_f, rho_g=rho_g,
        h_fg=h_fg, sigma=sigma, C1=C1, C2=C2, C3=C3, C4=C4, C5=C5,
    )
    Bo = q_chf / (G * h_fg)
    x_o = x_i_prime + 4.0 * Bo * (L / D)

    # 3. Classify on the derived x_o.
    if x_o >= _HM_XO[1]:  # x_o >= 0.0 — outlet at/above saturation
        return SubcooledCHFAssessment(
            SubcooledCHFStatus.SATURATED_HANDOFF, None, x_o,
            REASON_SATURATED_HANDOFF,
        )
    if x_o < _HM_XO[0]:   # x_o < -1.0 — below the validated outlet-quality floor
        return SubcooledCHFAssessment(
            SubcooledCHFStatus.OUT_OF_ENVELOPE, None, x_o,
            REASON_OUT_OF_ENVELOPE,
            (_bound("x_o", x_o, _HM_XO[0], _HM_XO[1], "-"),),
        )

    return SubcooledCHFAssessment(
        SubcooledCHFStatus.ASSESSABLE, q_chf, x_o,
        "assessable — in-envelope, subcooled outlet (x_o < 0)",
    )

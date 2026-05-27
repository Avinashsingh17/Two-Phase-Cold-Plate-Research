"""Two-phase cold plate correlations library.

Correlation functions for single-phase HTC, onset of nucleate boiling,
two-phase boiling HTC, and critical heat flux.

Each function carries a ``.envelope`` attribute of type
:class:`CorrelationEnvelope` describing its validity envelope and provenance.
"""

from two_phase_cp.correlations._envelope import CorrelationEnvelope
from two_phase_cp.correlations.boiling import KANDLIKAR_F_FL, chen_1966, kandlikar_1990
from two_phase_cp.correlations.chf import hall_mudawar_2000
from two_phase_cp.correlations.onb import bergles_rohsenow_onb
from two_phase_cp.correlations.single_phase import dittus_boelter, gnielinski, sieder_tate

__all__ = [
    "CorrelationEnvelope",
    "dittus_boelter",
    "sieder_tate",
    "gnielinski",
    "bergles_rohsenow_onb",
    "chen_1966",
    "kandlikar_1990",
    "KANDLIKAR_F_FL",
    "hall_mudawar_2000",
]

"""
Physics Core Module
===================

Contains:
- Metric definitions
- Thermodynamics engine
- Black hole classification
"""

from .metrics import (
    GeneralRelativityObject,
    SchwarzschildMetric,
    KerrMetric,
    ReissnerNordstromMetric,
    KerrNewmanMetric,
)

from .thermodynamics import Thermodynamics
from .classifier import BlackHoleClassifier

__all__ = [
    "GeneralRelativityObject",
    "SchwarzschildMetric",
    "KerrMetric",
    "ReissnerNordstromMetric",
    "KerrNewmanMetric",
    "Thermodynamics",
    "BlackHoleClassifier",
]

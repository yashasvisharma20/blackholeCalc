# -*- coding: utf-8 -*-

"""
BLACKHOLECALC Official v1.1
Author: ['Yashasvi Sharma', 'Aditya Sharma']
License: MIT
"""

__version__ = "1.1.0"
__authors__ = ["Yashasvi Sharma", "Aditya Sharma"]

# Metrics
from .physics.metrics import (
    SchwarzschildMetric as schwarzschild,
    KerrMetric as kerr,
    ReissnerNordstromMetric as reissner_nordstrom,
    KerrNewmanMetric as kerr_newman
)

# Thermodynamics
from .physics.thermodynamics import Thermodynamics

# Classifier
from .physics.classifier import BlackHoleClassifier

# Visualization
from .visualization.visualizer import Visualizer, WaveformSynthesizer

# Guide
from .guide import LibraryGuide

"""
blackholecalc package initialization.

Scope:
    Exposes the high-level API for Researcher interaction.
    Initializes default configuration for the Run Manager.

Limitations:
    This package is strictly analytical/semi-analytical.
    It does not perform numerical relativity simulations (e.g., Einstein Toolkit).
"""

from .api import BlackHoleCalcAPI

__version__ = "0.1.0-alpha"
__author__ = "Scientific Software Engineer"
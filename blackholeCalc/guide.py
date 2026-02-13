# -*- coding: utf-8 -*-
"""
BLACKHOLECALC USER GUIDE
========================

This guide explains:
• What a black hole is
• What the library calculates
• The formulas used internally
• Scientific references

The goal is clarity for non-physics users while remaining scientifically correct.
"""

import math


class LibraryGuide:

    @staticmethod
    def help():
        print("""
====================================================
BLACKHOLECALC v1.1 - USER GUIDE
====================================================

WHAT IS A BLACK HOLE?
---------------------

A black hole is an object with gravity so strong that
even light cannot escape once it crosses a boundary
called the "Event Horizon".

Black holes are predicted by Einstein's General Relativity.

This library models different types of black holes using
analytical equations from relativity theory.

----------------------------------------------------
TYPES OF BLACK HOLES IMPLEMENTED
----------------------------------------------------

1. Schwarzschild
   - Non-rotating
   - No electric charge

2. Kerr
   - Rotating
   - No electric charge

3. Reissner–Nordström
   - Non-rotating
   - Electrically charged

4. Kerr–Newman
   - Rotating
   - Electrically charged

----------------------------------------------------
CORE FORMULAS USED
----------------------------------------------------

1. Schwarzschild Event Horizon

    r_s = 2GM / c²

Where:
    G  = gravitational constant
    M  = mass
    c  = speed of light

This is the "point of no return".

----------------------------------------------------

2. Kerr Event Horizons (Rotating)

    r± = M ± sqrt(M² - a²)

Where:
    a = spin parameter

Two horizons exist:
    r+  → outer horizon
    r−  → inner horizon

Reference:
    Kerr, R. P. (1963). Gravitational field of a spinning mass.

----------------------------------------------------

3. Gravitational Redshift

    z = (1 / sqrt(g_tt)) - 1

This tells how much light loses energy while escaping gravity.

----------------------------------------------------

4. Hawking Temperature

    T = (ħ c³) / (8π G M k_B)

This means black holes are not completely black.
They emit very small radiation.

Reference:
    Hawking, S. W. (1974). Black hole explosions?

----------------------------------------------------

5. Black Hole Entropy

    S = (k_B c³ A) / (4 G ħ)

Where:
    A = surface area of event horizon

This connects gravity, thermodynamics, and quantum mechanics.

Reference:
    Bekenstein, J. D. (1973). Black holes and entropy.

----------------------------------------------------

6. Gravitational Wave Strain

    h = ΔL / L

This represents how much space stretches or compresses.

Used in waveform generation during black hole mergers.

Reference:
    Abbott et al. (2016). Observation of Gravitational Waves from a Binary Black Hole Merger.
    Physical Review Letters.

----------------------------------------------------
WHAT IS STRAIN?
----------------------------------------------------

Strain measures how much space itself stretches.

If L is original length and ΔL is change in length:

    strain = ΔL / L

Typical detected strain:
    h ≈ 10⁻²¹

This is extremely small.

----------------------------------------------------
WHAT THIS LIBRARY DOES NOT DO
----------------------------------------------------

• It does NOT solve Einstein field equations numerically
• It does NOT perform full numerical relativity
• It focuses on analytical and semi-analytical formulas

----------------------------------------------------
HOW TO USE THE LIBRARY
----------------------------------------------------

Example:

    from blackholecalc import kerr
    bh = kerr(10, spin=0.9)
    print(bh.event_horizon())

Thermodynamics:

    from blackholecalc import Thermodynamics
    result = Thermodynamics.analyze(bh)

Visualization:

    from blackholecalc import Visualizer
    Visualizer.plot_structure(bh)

----------------------------------------------------

This guide is meant to help users understand
what calculations are being performed internally.

====================================================
END OF GUIDE
====================================================
""")

    @staticmethod
    def references():
        print("""
====================================================
SCIENTIFIC REFERENCES
====================================================

Einstein, A. (1915).
    The Field Equations of Gravitation.

Schwarzschild, K. (1916).
    On the Gravitational Field of a Mass Point.

Kerr, R. P. (1963).
    Gravitational Field of a Spinning Mass.

Bekenstein, J. D. (1973).
    Black Holes and Entropy.

Hawking, S. W. (1974).
    Black Hole Explosions?

Abbott et al. (LIGO Scientific Collaboration) (2016).
    Observation of Gravitational Waves from a Binary Black Hole Merger.
    Physical Review Letters 116, 061102.

====================================================
""")

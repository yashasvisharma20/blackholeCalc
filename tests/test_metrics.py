import numpy as np
from blackholeCalc import schwarzschild, kerr
from blackholeCalc.maths.constants import PhysicalConstants
from blackholeCalc.maths.units import UnitManager


def test_schwarzschild_horizon_reference():
    """
    Reference:
    Schwarzschild radius:
        r_s = 2GM / c^2
    """

    mass_solar = 10
    bh = schwarzschild(mass_solar)

    # Expected theoretical value
    mass_kg = mass_solar * PhysicalConstants.M_sun
    M_geom = UnitManager.mass_si_to_geom(mass_kg)
    expected = 2 * M_geom

    computed = bh.event_horizon()

    assert np.isclose(computed, expected, rtol=1e-10)


def test_kerr_extremal_limit():
    """
    For extremal Kerr (a* = 1),
    r+ = M
    """

    bh = kerr(10, spin=1.0)
    r_plus, r_minus = bh.event_horizon()

    assert np.isclose(r_plus, bh.M, rtol=1e-10)

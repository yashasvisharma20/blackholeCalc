import numpy as np
from blackholeCalc import schwarzschild, Thermodynamics


def test_hawking_temperature_reference():
    """
    Reference:
    Hawking Temperature for Schwarzschild:

        T ≈ 6.169 × 10^-8 / M_solar  Kelvin

    From:
    Hawking (1974)
    """

    mass = 10
    bh = schwarzschild(mass)
    result = Thermodynamics.analyze(bh)

    expected = 6.169e-8 / mass

    computed = result["Temperature (K)"]

    assert np.isclose(computed, expected, rtol=1e-6)

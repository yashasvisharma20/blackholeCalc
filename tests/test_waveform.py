import numpy as np
from blackholeCalc import WaveformSynthesizer


def test_chirp_mass_reference():
    """
    Chirp mass formula:

        M_chirp = (m1*m2)^(3/5) / (m1+m2)^(1/5)

    Reference:
    Gravitational wave literature (LIGO formalism)
    """

    m1 = 30
    m2 = 30

    t, h, chirp = WaveformSynthesizer.generate_chirp(m1, m2)

    expected = (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

    assert np.isclose(chirp, expected, rtol=1e-10)
    assert len(t) == len(h)

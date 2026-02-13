import numpy as np
from typing import Dict
from ..maths.constants import PhysicalConstants
from .metrics import (
    GeneralRelativityObject,
    KerrMetric,
    KerrNewmanMetric,
    ReissnerNordstromMetric
)

class Thermodynamics:
    @staticmethod
    def analyze(bh: GeneralRelativityObject) -> Dict[str, float]:
        """Calculates Hawking Temperature, Entropy, Luminosity, Peak Wavelength, and Lifetime."""

        # =====================================================
        # 1. Hawking Temperature (Kelvin)
        # =====================================================

        # Base Schwarzschild temperature (approximate)
        T_sch = 6.169e-8 * (1.0 / bh.mass_solar)

        # Default
        T_kelvin = T_sch

        # Adjust for rotation / charge
        if isinstance(bh, (KerrMetric, KerrNewmanMetric)):
            r_plus = bh.event_horizon()[0]

            # Surface gravity (geometric units)
            num = r_plus - bh.M
            den = 2 * np.pi * (r_plus**2 + getattr(bh, 'a', 0)**2)
            kappa_geom = num / den

            # Schwarzschild surface gravity for same mass
            r_sch = 2.0 * bh.M
            kappa_sch = 1.0 / (2.0 * r_sch)

            # Temperature scaling
            T_kelvin = T_sch * (kappa_geom / kappa_sch)

        # =====================================================
        # 2. Entropy (J/K)
        # =====================================================

        if isinstance(bh, (KerrMetric, KerrNewmanMetric, ReissnerNordstromMetric)):
            horizon = bh.event_horizon()
            r_p = horizon[0] if isinstance(horizon, tuple) else horizon
            a_val = getattr(bh, 'a', 0)
            area_geom = 4 * np.pi * (r_p**2 + a_val**2)
        else:
            # Schwarzschild
            area_geom = 16 * np.pi * bh.M**2

        S = (
            PhysicalConstants.k_b
            * PhysicalConstants.c**3
            * area_geom
        ) / (4 * PhysicalConstants.G * PhysicalConstants.h_bar)

        # =====================================================
        # 3. Luminosity (Stefan-Boltzmann Approximation)
        # =====================================================

        P_watts = PhysicalConstants.sigma_sb * area_geom * (T_kelvin**4)

        # =====================================================
        # 4. Peak Wavelength (Wien's Law)
        # =====================================================

        lambda_peak = (
            PhysicalConstants.wien_b / T_kelvin
            if T_kelvin > 0 else float('inf')
        )

        # =====================================================
        # 5. Lifetime (Improved Scaling)
        # =====================================================

        # Schwarzschild lifetime (seconds)
        t_sch = 2.098e67 * (bh.mass_solar)**3

        # Scale lifetime using temperature ratio
        # Lifetime ∝ 1 / T^2
        if T_kelvin > 0:
            t_sec = t_sch * (T_sch / T_kelvin)**2
        else:
            t_sec = float('inf')

        # =====================================================
        return {
            "Temperature (K)": T_kelvin,
            "Entropy (J/K)": S,
            "Luminosity (W)": P_watts,
            "Peak Wavelength (m)": lambda_peak,
            "Lifetime (Yr)": t_sec / PhysicalConstants.year
        }

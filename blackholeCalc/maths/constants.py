import scipy.constants as const
from dataclasses import dataclass

@dataclass(frozen=True)
class PhysicalConstants:
    """Immutable store of NIST physical constants (CODATA 2018)."""
    G: float = const.G                  # Gravitational Constant [m^3 kg^-1 s^-2]
    c: float = const.c                  # Speed of Light [m/s]
    M_sun: float = 1.98847e30           # Solar Mass [kg]
    h_bar: float = const.hbar           # Reduced Planck Constant
    k_b: float = const.k                # Boltzmann Constant
    sigma_sb: float = const.sigma       # Stefan-Boltzmann Constant
    wien_b: float = const.Wien          # Wien's Displacement Constant
    year: float = 31557600.0            # Julian Year [s]
    parsec: float = 3.0857e16           # Parsec [m]
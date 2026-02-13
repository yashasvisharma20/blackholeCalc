import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple, Union, Dict
from ..maths.units import UnitManager
from ..maths.constants import PhysicalConstants

class GeneralRelativityObject(ABC):
    """Abstract Base Class implementing shared General Relativity logic."""
    
    def __init__(self, mass_solar: float, name: str = "Unknown Object"):

        self._validate_positive_number(mass_solar, "Mass")

        self.mass_solar = mass_solar
        self.mass_kg = mass_solar * PhysicalConstants.M_sun
        self.M = UnitManager.mass_si_to_geom(self.mass_kg) # Geometric Mass
        self.name = name

    # =========================
    # Central Validation
    # =========================

    def _validate_positive_number(self, value: float, name: str):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number.")
        if value <= 0:
            raise ValueError(f"{name} must be positive.")

    def _validate_radius(self, r: float):
        if not isinstance(r, (int, float)):
            raise TypeError("Radius must be a number.")

        if r == 0:
            raise ValueError("Radius cannot be zero (singularity).")

        if r < 0:
            raise ValueError("Radius cannot be negative.")

    def _validate_angular_momentum(self, L: float):
        if not isinstance(L, (int, float)):
            raise TypeError("Angular momentum must be a number.") 
    
    # =========================
    # Child Must Implement
    # =========================

    @abstractmethod
    def event_horizon(self) -> Union[float, Tuple[float, float]]:
        pass

    @abstractmethod
    def isco(self, retrograde: bool = False) -> float:
        pass

    @abstractmethod
    def gravitational_redshift(self, r: float) -> float:
        pass
    
    @abstractmethod
    def effective_potential(self, r: float, L: float) -> float:
        pass
    
    @abstractmethod
    def identify_type(self) -> Dict[str, str]:
        pass

    def ergosphere_radius(self, theta: float = np.pi/2):
        """
        Default: No ergosphere.
        Child classes can override.
        """
        return None

    def description(self) -> str:
        return f"{self.name} (M={self.mass_solar:.2e} M_sun)"

class SchwarzschildMetric(GeneralRelativityObject):
    """Static, Uncharged Black Hole (The simplest solution)."""
    def __init__(self, mass_solar: float, name="Schwarzschild BH"):
        super().__init__(mass_solar, name)
        self.spin = 0.0
        self.charge = 0.0

    def event_horizon(self) -> float:
        return 2.0 * self.M

    def isco(self, retrograde=False) -> float:
        return 6.0 * self.M

    def gravitational_redshift(self, r: float) -> float:
        if r <= 2.0 * self.M: return float('inf')
        g_tt = 1.0 - (2.0 * self.M / r)
        return (1.0 / np.sqrt(g_tt)) - 1.0
    
    def effective_potential(self, r: float, L: float) -> float:
        """V_eff for particle with angular momentum L."""
        return (1 - 2*self.M/r) * (1 + L**2/r**2)
        
    def identify_type(self) -> Dict[str, str]:
        return {
            "Type": "Schwarzschild",
            "Properties": "Static, Spherically Symmetric, Neutral",
            "Singularity": "Point-like",
            "Ergosphere": "None"
        }

class KerrMetric(GeneralRelativityObject):
    """Rotating, Uncharged Black Hole (Astrophysically most common)."""
    def __init__(self, mass_solar: float, spin: float, name="Kerr BH"):
        super().__init__(mass_solar, name)
        if abs(spin) > 1.0: raise ValueError("Spin |a*| > 1 implies Naked Singularity.")
        self.a_star = spin
        self.a = spin * self.M
        self.charge = 0.0

    def event_horizon(self) -> Tuple[float, float]:
        rad = np.sqrt(self.M**2 - self.a**2)
        return (self.M + rad, self.M - rad)

    def isco(self, retrograde=False) -> float:
        sign = 1 if retrograde else -1
        Z1 = 1 + (1 - self.a_star**2)**(1/3) * ((1 + self.a_star)**(1/3) + (1 - self.a_star)**(1/3))
        Z2 = np.sqrt(3 * self.a_star**2 + Z1**2)
        term = np.sqrt((3 - Z1) * (3 + Z1 + 2*Z2))
        return self.M * (3 + Z2 + sign * term)

    def gravitational_redshift(self, r: float, theta: float = np.pi/2) -> float:
        rho2 = r**2 + self.a**2 * np.cos(theta)**2
        g_tt = 1.0 - (2.0 * self.M * r) / rho2
        if g_tt <= 0: return float('inf') 
        return (1.0 / np.sqrt(g_tt)) - 1.0

    def effective_potential(self, r: float, L: float) -> float:
        # Simplified equatorial potential for visualization
        return (1 - 2*self.M/r) # Placeholder for full Kerr potential
    
    def ergosphere_radius(self, theta: float = np.pi/2) -> float:
        """
        Kerr ergosurface radius at angle theta.
        """
        return self.M + np.sqrt(self.M**2 - self.a**2 * np.cos(theta)**2)
    
    def identify_type(self) -> Dict[str, str]:
        return {
            "Type": "Kerr",
            "Properties": "Rotating, Axisymmetric, Neutral",
            "Singularity": "Ring-like",
            "Ergosphere": "Present (Oblate)"
        }

class ReissnerNordstromMetric(GeneralRelativityObject):
    """Static, Charged Black Hole."""
    def __init__(self, mass_solar: float, charge: float, name="Charged BH"):
        super().__init__(mass_solar, name)
        if abs(charge) > 1.0: raise ValueError("Charge |Q*| > 1 implies Naked Singularity.")
        self.Q_star = charge
        self.Q = charge * self.M
        self.spin = 0.0

    def event_horizon(self) -> Tuple[float, float]:
        rad = np.sqrt(self.M**2 - self.Q**2)
        return (self.M + rad, self.M - rad)

    def isco(self, retrograde=False) -> float:
        # Approximation for charged ISCO
        return self.M * (6.0 - 2.0 * self.Q_star**2)

    def gravitational_redshift(self, r: float) -> float:
        val = 1.0 - (2.0 * self.M / r) + (self.Q**2 / r**2)
        if val <= 0: return float('inf')
        return (1.0 / np.sqrt(val)) - 1.0
    
    def effective_potential(self, r: float, L: float) -> float:
        return (1 - 2*self.M/r + self.Q**2/r**2) * (1 + L**2/r**2)
        
    def identify_type(self) -> Dict[str, str]:
        return {
            "Type": "Reissner-Nordström",
            "Properties": "Static, Spherically Symmetric, Charged",
            "Singularity": "Point-like (Timelike)",
            "Ergosphere": "None"
        }

class KerrNewmanMetric(GeneralRelativityObject):
    """
    The General Solution: Rotating AND Charged Black Hole.
    Defined by Mass (M), Spin (a), and Charge (Q).
    """
    def __init__(self, mass_solar: float, spin: float, charge: float, name="Kerr-Newman BH"):
        super().__init__(mass_solar, name)
        if (spin**2 + charge**2) > 1.0: raise ValueError("a^2 + Q^2 > 1 implies Naked Singularity.")
        self.a_star = spin
        self.a = spin * self.M
        self.Q_star = charge
        self.Q = charge * self.M

    def event_horizon(self) -> Tuple[float, float]:
        rad = np.sqrt(self.M**2 - self.a**2 - self.Q**2)
        return (self.M + rad, self.M - rad)

    def isco(self, retrograde=False) -> float:
        # Fallback to Kerr approximation for simplicity in analytic library
        return KerrMetric(self.mass_solar, self.a_star).isco(retrograde)

    def gravitational_redshift(self, r: float) -> float:
        # Polar approximation
        sigma = r**2 # at theta=0
        delta = r**2 - 2*self.M*r + self.a**2 + self.Q**2
        return (1.0 / np.sqrt(delta/sigma)) - 1.0

    def effective_potential(self, r: float, L: float) -> float:
        raise NotImplementedError("Full Kerr-Newman potential not implemented.")
    
    def ergosphere_radius(self, theta: float = np.pi/2) -> float:
        """
        Ergosurface radius at angle theta.
        """
        return self.M + np.sqrt(self.M**2 - self.a**2 * np.cos(theta)**2 - self.Q**2)

    
    
    def identify_type(self) -> Dict[str, str]:
        return {
            "Type": "Kerr-Newman",
            "Properties": "Rotating, Axisymmetric, Charged",
            "Singularity": "Ring-like",
            "Ergosphere": "Present (Complex)"
        }


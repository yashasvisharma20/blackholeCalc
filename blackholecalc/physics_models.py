"""
physics_models.py

PURPOSE:
    Defines analytical mathematical models for black hole spacetimes.
    
CRITICAL NOTE ON UNITS:
    - Internal state is ALWAYS SI (kg, meters).
    - Helper methods provided to convert to Geometric Units (M) for plotting.

REFERENCES:
    [1] Hartle, J. B. (2003). Gravity.
    [2] Wald, R. M. (1984). General Relativity.
"""

import math
from abc import ABC, abstractmethod

# Physical Constants (SI Units)
G = 6.67430e-11  # m^3 kg^-1 s^-2
C = 2.99792e8    # m/s
M_SOLAR = 1.989e30 # kg

class BlackHoleModel(ABC):
    def __init__(self, mass_solar):
        self.mass_solar = float(mass_solar)
        self.mass_kg = self.mass_solar * M_SOLAR
        self._calculate_fundamental_properties()

    @abstractmethod
    def _calculate_fundamental_properties(self):
        pass

    @abstractmethod
    def get_horizon_radius(self):
        """Return the event horizon radius in SI meters."""
        pass

    def to_geometric_radius(self, radius_meters):
        """
        Converts a radius in meters to dimensionless geometric units (r/M).
        Useful for visualization normalization.
        """
        if self.geometric_mass == 0:
            return 0.0
        return radius_meters / self.geometric_mass

class Schwarzschild(BlackHoleModel):
    def _calculate_fundamental_properties(self):
        # Geometric mass M = GM/c^2 (meters)
        self.geometric_mass = (G * self.mass_kg) / (C**2)

    def get_horizon_radius(self):
        return 2.0 * self.geometric_mass

class Kerr(BlackHoleModel):
    def __init__(self, mass_solar, dimensionless_spin):
        self.spin = float(dimensionless_spin)
        # Validation
        if abs(self.spin) > 1.0:
            # We allow it but must warn (handled in classification)
            pass 
        super().__init__(mass_solar)

    def _calculate_fundamental_properties(self):
        self.geometric_mass = (G * self.mass_kg) / (C**2)
        # a = J/Mc. For dimensionless spin chi: a = chi * geometric_mass
        self.a_parameter = self.spin * self.geometric_mass

    def get_horizon_radius(self):
        if abs(self.spin) > 1.0:
            return float('nan') # Naked Singularity
        
        root_term = math.sqrt(self.geometric_mass**2 - self.a_parameter**2)
        return self.geometric_mass + root_term
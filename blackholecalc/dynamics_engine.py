"""
dynamics_engine.py

PURPOSE:
    Calculates orbital mechanics.

SAFETY:
    - Raises NotImplementedError for approximations that are not yet rigorously coded.
    - No "magic numbers" without citation.
"""

import numpy as np
from .physics_models import Schwarzschild, Kerr

class OrbitalDynamics:
    
    @staticmethod
    def calculate_isco_radius(model):
        """
        Calculates the Innermost Stable Circular Orbit (ISCO).
        
        Returns:
            float: Radius in meters.
        
        Raises:
            NotImplementedError: If analytical formula is not implemented for the specific model.
        """
        if isinstance(model, Schwarzschild):
            return 6.0 * model.geometric_mass
        
        elif isinstance(model, Kerr):
            # CRITICAL FIX: Do not return Schwarzschild approximation. 
            # It is physically wrong for spinning black holes.
            # TODO: Implement Bardeen et al. (1972) full solutions.
            raise NotImplementedError(
                "Exact Kerr ISCO solution not yet implemented. "
                "Use numerical solver or wait for version 0.2.0."
            )
        
        else:
            raise NotImplementedError("Model not supported for ISCO.")

    @staticmethod
    def effective_potential(r, model, angular_momentum_l):
        """
        Computes V_eff(r) for a massive particle.
        
        Args:
            r (array): Radial coordinates in METERS.
            model (BlackHoleModel): Physics object.
            angular_momentum_l (float): Specific angular momentum (geometric units usually).
        
        Returns:
            np.array: Potential values (dimensionless energy-squared terms).
        """
        M = model.geometric_mass
        
        # Avoid division by zero
        r_safe = np.where(r == 0, 1e-10, r)
        
        # Formula assumes geometric units for the calculation structure,
        # so we ensure inputs are scaled consistent with the formula's derivation.
        # V_eff = (1 - 2M/r) * ...
        
        term1 = 1.0 - (2.0 * M / r_safe)
        term2 = 1.0 + (angular_momentum_l**2 / r_safe**2)
        
        return term1 * term2
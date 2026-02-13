from .constants import PhysicalConstants

class UnitManager:
    """
    Handles conversion between SI Units and Geometric Units (G=c=1).
    In Geometric units, Mass, Time, and Length are all measured in meters.
    """
    
    @staticmethod
    def mass_si_to_geom(mass_kg: float) -> float:
        """M [m] = G * m [kg] / c^2"""
        return (PhysicalConstants.G * mass_kg) / (PhysicalConstants.c**2)

    @staticmethod
    def mass_geom_to_si(mass_m: float) -> float:
        """m [kg] = M [m] * c^2 / G"""
        return (mass_m * PhysicalConstants.c**2) / PhysicalConstants.G

    @staticmethod
    def time_geom_to_si(time_m: float) -> float:
        """t [s] = t [m] / c"""
        return time_m / PhysicalConstants.c
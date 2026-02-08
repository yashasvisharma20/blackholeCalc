"""
api.py

PURPOSE:
    The primary entry point. Orchestrates safe execution.
"""

import numpy as np
import warnings
from .physics_models import Schwarzschild, Kerr
from .dynamics_engine import OrbitalDynamics
from .run_manager import RunContext
from .visualization_engine import Visualizer

# Tolerance for floating point spin comparison
SPIN_TOLERANCE = 1e-12

class BlackHoleCalcAPI:
    
    def __init__(self, output_dir="runs"):
        self.output_dir = output_dir

    def run_simulation(self, mass_solar, spin=0.0, description="",save_data=True):
        """
        Executes a run. Uses tolerance check for spin to determine model.
        """
        # 1. Select Model with Tolerance Check
        if abs(spin) < SPIN_TOLERANCE:
            model = Schwarzschild(mass_solar)
            model_name = "Schwarzschild"
        else:
            model = Kerr(mass_solar, spin)
            model_name = "Kerr"

        # 2. Initialize Run Context with Model Name
        run = RunContext(description=description, model_class_name=model_name)
        run.log_input("mass_solar", mass_solar, "M_sun")
        run.log_input("spin", spin, "dimensionless")

        # 3. Compute
        r_horizon = model.get_horizon_radius()
        run.log_output("horizon_radius", r_horizon, "meters")

        try:
            r_isco = OrbitalDynamics.calculate_isco_radius(model)
            run.log_output("isco_radius", r_isco, "meters")
        except NotImplementedError as e:
            # Safely log that we couldn't compute it, rather than crashing or lying
            warnings.warn(f"Could not compute ISCO: {e}")
            run.log_output("isco_radius", None, "NotImplemented")

        # 4. Persist
        if save_data:
            run.save(base_path=self.output_dir)
            return run.run_id
        else:
            print("[System] Dry run - data NOT saved to disk.")
            return {
                "id": run.run_id, 
                "inputs": run.inputs, 
                "outputs": run.outputs
            } 

    def visualize_potential(self, mass_solar, spin, angular_momentum=4.0):
        """
        Visualizes potential. Handles unit normalization explicitly.
        """
        # Model Selection
        if abs(spin) < SPIN_TOLERANCE:
            model = Schwarzschild(mass_solar)
        else:
            model = Kerr(mass_solar, spin)

        # GENERATE DATA IN METERS
        # Range: 2.1 * GM/c^2 to 20 * GM/c^2
        r_min_meters = 2.1 * model.geometric_mass
        r_max_meters = 20.0 * model.geometric_mass
        r_vals_meters = np.linspace(r_min_meters, r_max_meters, 200)

        # COMPUTE POTENTIAL
        pot_vals = OrbitalDynamics.effective_potential(r_vals_meters, model, angular_momentum)

        # NORMALIZE FOR PLOTTING (Explicitly)
        # We want the X-axis to be r/M (dimensionless)
        r_vals_normalized = r_vals_meters / model.geometric_mass
        
        # Pass normalized data to plotter
        Visualizer.plot_potential(
            r_values=r_vals_normalized, 
            potential_values=pot_vals, 
            run_id="Interactive",
            x_label=r"Radius ($r/M$)" # Label now matches data
        )
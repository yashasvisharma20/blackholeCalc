"""
visualization_engine.py
"""
import matplotlib.pyplot as plt

class Visualizer:
    
    @staticmethod
    def plot_potential(r_values, potential_values, run_id="temp", x_label="Radius"):
        """
        Plots V_eff(r).
        
        Args:
            r_values: X-axis data. Caller responsible for normalization (meters vs r/M).
            x_label: Label describing the r_values unit.
        """
        plt.figure(figsize=(8, 5))
        plt.plot(r_values, potential_values, label=r"$V_{eff}$", color='black')
        
        plt.xlabel(x_label) # Dynamic label based on input
        plt.ylabel(r"Effective Potential")
        plt.title(f"Effective Potential Profile (Run: {run_id})")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()
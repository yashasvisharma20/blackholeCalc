"""
main.py
High-Throughput Parameter Sweep (Dry Run Mode)
"""
import numpy as np
import matplotlib.pyplot as plt
from blackholecalc.api import BlackHoleCalcAPI

def main():
    print("=== Starting Parameter Sweep (No-Save Mode) ===")
    
    # 1. Initialize API
    api = BlackHoleCalcAPI()

    # 2. Define our sweep parameters
    # We will test 50 different spin values from 0.0 to 0.99
    spins = np.linspace(0.0, 0.99, 50)
    mass = 10.0 # Solar masses

    # Storage for plotting later
    results_spin = []
    results_horizon = []

    print(f" -> Simulating {len(spins)} black holes in RAM...")

    # 3. The Loop
    for i, spin_val in enumerate(spins):
        
        # CALL WITH save_data=False
        # This prevents creating 50 separate folders in 'runs/'
        result = api.run_simulation(
            mass_solar=mass, 
            spin=spin_val, 
            save_data=False  # <--- CRITICAL FLAG
        )
        
        # Extract data from the returned dictionary
        # Note: The structure depends on how you return it in api.py
        # Based on the Step 1 update, we access 'outputs' -> 'value'
        r_horizon = result['outputs']['horizon_radius']['value']
        
        # Store for analysis
        results_spin.append(spin_val)
        results_horizon.append(r_horizon)

        # Optional: Print progress every 10 runs
        if i % 10 == 0:
            print(f"    Processed spin={spin_val:.2f}...")

    print(" -> Simulation complete.")

    # 4. Visualization (Proof of work)
    print(" -> Generating Plot...")
    
    plt.figure(figsize=(8, 5))
    plt.plot(results_spin, results_horizon, 'b.-', label=f"Mass = {mass} M_sun")
    
    plt.xlabel("Spin Parameter (dimensionless)")
    plt.ylabel("Horizon Radius (meters)")
    plt.title("Horizon Radius vs. Spin (Computed in RAM)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    print(" -> Displaying plot. Close window to exit.")
    plt.show()

if __name__ == "__main__":
    main()
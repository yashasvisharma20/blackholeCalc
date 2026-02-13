"""
Example 2:
VISUALIZE A BLACK HOLE
----------------------
This example shows how a black hole looks
using ray-tracing and structure plotting.
"""

from blackholeCalc import kerr, Visualizer

print("\nBlack Hole Visualization Demo\n")

mass = float(input("Enter mass (solar masses, e.g. 10): "))
spin = float(input("Enter spin (0 to 1): "))

print("\nCreating rotating black hole for visualization...\n")
bh = kerr(mass, spin=spin)

print("Step 1: Plotting structure (Event Horizon + Ergosphere)")
print("Close the plot window to continue.")

Visualizer.plot_structure(bh)

input("\nPress ENTER to generate shadow image...")

print("\nStep 2: Rendering shadow (this may take few seconds)...")
fig = Visualizer.render_shadow(bh)
fig.show()

print("\nWhat are you seeing?")
print("• Dark region → Black hole shadow")
print("• Bright ring → Light bending around gravity")
print("• Blue outer region → Accretion disk")

print("\nEnd of Example 2.")

"""
Example 1:
CREATE & UNDERSTAND A BLACK HOLE
--------------------------------
This example helps non-physics users create a black hole
and understand what the results mean in simple language.
"""

from blackholeCalc import schwarzschild, kerr, Thermodynamics

print("\nWelcome to BlackHoleCalc v1.1")
print("We will create a black hole together step-by-step.\n")

# Step 1: Choose type
print("Step 1: What type of black hole do you want?")
print("1 → Non-Rotating (Simple Black Hole)")
print("2 → Rotating (Spinning Black Hole)")

choice = input("Enter 1 or 2: ")

mass = float(input("\nStep 2: Enter mass (in multiples of Sun mass, e.g. 10): "))

if choice == "1":
    print("\nCreating a Non-Rotating Black Hole...")
    bh = schwarzschild(mass)

else:
    spin = float(input("\nEnter spin value (between 0 and 1): "))
    print("\nCreating a Rotating Black Hole...")
    bh = kerr(mass, spin=spin)

print("\nBlack Hole Created Successfully!\n")

# Show Basic Info
print("Basic Identity:")
info = bh.identify_type()
for key, value in info.items():
    print(f"{key}: {value}")

print("\nWhat does this mean?")
print("Type → Tells us what kind of black hole it is.")
print("Status → Whether it forms a real horizon or becomes unstable.")
print("Singularity → Shape of the center region.\n")

# Event Horizon
horizon = bh.event_horizon()
print("Event Horizon Radius:", horizon)

print("\nExplanation:")
print("Event Horizon is the 'point of no return'.")
print("If anything crosses this boundary, it cannot escape — not even light.\n")

# Thermodynamics
print("Now calculating temperature and other physical properties...\n")

results = Thermodynamics.analyze(bh)

for key, value in results.items():
    print(f"{key}: {value}")

print("\nWhat is happening physically?")
print("• Temperature → Black holes emit tiny radiation (Hawking Radiation).")
print("• Entropy → Measures disorder/information stored.")
print("• Luminosity → Energy emission rate.")
print("• Lifetime → How long before it evaporates (very very long!).")

print("\nEnd of Example 1.")

"""
Example 3:
GRAVITATIONAL WAVES
-------------------
Simulates two merging black holes and
generates gravitational wave signal.
"""

from blackholeCalc import WaveformSynthesizer
import matplotlib.pyplot as plt

print("\nGravitational Wave Simulation\n")

m1 = float(input("Enter mass of first black hole (solar mass): "))
m2 = float(input("Enter mass of second black hole (solar mass): "))

print("\nSimulating inspiral, merger, and ringdown...\n")

t, h, chirp_mass = WaveformSynthesizer.generate_chirp(m1, m2)

print(f"Chirp Mass: {chirp_mass}")
print("\nChirp Mass tells how strong and fast the signal evolves.")

plt.figure(figsize=(10,4))
plt.plot(t, h)
plt.title("Gravitational Wave Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Strain (h)")
plt.grid(True)
plt.show()

print("\nExplanation of the Graph:")
print("• At the beginning, the waves are small and slow.")
print("  This means the two black holes are still far apart.")
print("  They are orbiting each other gently.")

print("\n• As time moves forward, the waves become bigger and faster.")
print("  This shows the black holes are getting closer.")
print("  Gravity pulls them faster and faster.")

print("\n• The biggest peak happens when they collide.")
print("  This is the most energetic moment in the universe.")
print("  Space shakes strongly here.")

print("\n• After the collision, the waves slowly fade away.")
print("  The new single black hole is settling down and becoming stable.")


print("\nThis is similar to signals detected by LIGO.")

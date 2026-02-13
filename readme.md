# BlackHoleCalc

BlackHoleCalc is a scientific Python library for analytical modeling, thermodynamic analysis, visualization, and gravitational wave synthesis of relativistic black hole systems.

It provides physically consistent implementations of key solutions from General Relativity and exposes them through a clean, educational, and research-friendly API.

---

## Features

### 1. General Relativity Metrics

Analytical implementations of:

- Schwarzschild (non-rotating, neutral)
- Kerr (rotating, neutral)
- Reissner–Nordström (charged, non-rotating)
- Kerr–Newman (rotating, charged)

Available calculations include:

- Event horizon radius
- Inner/outer horizons
- ISCO (Innermost Stable Circular Orbit)
- Gravitational redshift
- Effective orbital potential
- Ergosphere geometry (rotating cases)

---

### 2. Black Hole Thermodynamics

Implements semi-classical thermodynamic analysis:

- Hawking temperature
- Bekenstein–Hawking entropy
- Luminosity (Stefan–Boltzmann approximation)
- Peak wavelength (Wien’s law)
- Evaporation lifetime scaling

---

### 3. Visualization Engine

Includes:

- Ray-traced black hole shadow rendering
- Event horizon and ergosphere structure plots
- Effective orbital potential graphs

Designed for both research demonstrations and education.

---

### 4. Gravitational Wave Synthesis

Generates inspiral–merger–ringdown chirp signals using analytical approximations.

Returns:

- Time array
- Strain signal
- Chirp mass

Useful for educational simulations and waveform demonstrations.

---

## Installation

Clone the repository and install in development mode:

```bash
pip install blackholeCalc .

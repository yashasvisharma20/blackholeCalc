import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple
from ..physics.metrics import GeneralRelativityObject
from ..maths.constants import PhysicalConstants

class Visualizer:
    @staticmethod
    def render_shadow(bh: GeneralRelativityObject, 
                      fov_M: float = 14.0, 
                      res: int = 400, 
                      inc_deg: float = 85.0,
                      ax: Optional[plt.Axes] = None):
        """
        Studio-Grade Ray Tracer.
        Renders Black Hole Shadow, Accretion Disk, Doppler Beaming & Lensing Ring.
        """
        print(f"[Visualizer] Ray-tracing {bh.name} at {res}x{res}...")
        
        inc = np.radians(inc_deg)
        x = np.linspace(-fov_M, fov_M, res)
        y = np.linspace(-fov_M, fov_M, res)
        alpha, beta = np.meshgrid(x, y)
        
        # Physics Parameters
        a = bh.a_star if hasattr(bh, 'a_star') else 0.0
        
        # 1. Shadow Geometry (Bardeen)
        xi_shift = -2 * a * np.sin(inc)
        r_shadow = 5.2 * (1 - 0.04 * a**2) # Approx
        dist_center = np.sqrt((alpha - xi_shift)**2 + beta**2)
        shadow_mask = dist_center < r_shadow
        
        # 2. Accretion Disk (Thin)
        rad_disk = np.sqrt(alpha**2 + beta**2 / np.cos(inc)**2)
        
        # 3. Doppler Beaming (Relativistic)
        v_phi = 0.5 / (rad_disk**0.5 + 0.1)
        doppler = (1.0 + v_phi * np.sin(inc) * (-alpha/rad_disk))**4
        
        # 4. Intensity Map
        flux = (1.0 / (rad_disk + 2.0)**3) * doppler
        
        # Cut inner edge at ISCO
        r_isco = bh.isco()
        flux[rad_disk < r_isco] = 0
        
        # 5. Photon Ring (Lensing effect)
        ring = np.exp(-0.5 * (dist_center - r_shadow)**2 / 0.1)
        flux += ring * 2.5
        
        flux[shadow_mask] = 0
        
        # Plotting
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='#050505')
            return_fig = True
        else:
            return_fig = False

        im = ax.imshow(flux, extent=[-fov_M, fov_M, -fov_M, fov_M], origin='lower', cmap='inferno')
        
        ax.set_title(f"{bh.name}\nSpin a={a} | Inc={inc_deg}°", color='white', pad=10, fontsize=10)
        ax.set_xlabel(r"$\alpha$ (M)", color='gray', fontsize=8)
        ax.set_ylabel(r"$\beta$ (M)", color='gray', fontsize=8)
        ax.tick_params(colors='gray', labelsize=8)
        for spine in ax.spines.values(): spine.set_color('gray')
        
        if return_fig:
            return fig

    @staticmethod
    def plot_structure(bh: GeneralRelativityObject, ax: Optional[plt.Axes] = None):
        """
        Plots the Side-View Geometry: Event Horizon vs Ergosphere.
        Shows the 'static limit' and the singularity structure in the meridional plane.
        """
        theta = np.linspace(0, 2*np.pi, 300)
        
        # Get Horizon Radius (Outer)
        if isinstance(bh.event_horizon(), tuple):
            r_h = bh.event_horizon()[0]
        else:
            r_h = bh.event_horizon()
            
        # 1. Horizon Surface (Sphere in BL coords)
        x_h = r_h * np.sin(theta)
        z_h = r_h * np.cos(theta)
        
        # 2. Ergosphere Surface (Oblate)
        # r_E = M + sqrt(M^2 - a^2 cos^2 theta)
        if hasattr(bh, 'a'):
            a = bh.a
            # Safety check for sqrt
            term = bh.M**2 - a**2 * np.cos(theta)**2
            term[term < 0] = 0
            r_e = bh.M + np.sqrt(term)
        else:
            r_e = np.full_like(theta, r_h) # If no spin, Ergosphere = Horizon
            
        x_e = r_e * np.sin(theta)
        z_e = r_e * np.cos(theta)
        
        # Plotting
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 6))
            
        # Draw Ergosphere
        ax.fill(x_e/bh.M, z_e/bh.M, color='cyan', alpha=0.3, label='Ergosphere')
        ax.plot(x_e/bh.M, z_e/bh.M, color='cyan', linestyle='--')
        
        # Draw Horizon
        ax.fill(x_h/bh.M, z_h/bh.M, color='black', alpha=0.9, label='Event Horizon')
        
        ax.set_aspect('equal')
        ax.set_title(f"Structural Geometry: {bh.name}", fontsize=10)
        ax.set_xlabel("x / M")
        ax.set_ylabel("z / M (Spin Axis)")
        ax.legend(fontsize=8, loc='upper right')
        ax.grid(True, alpha=0.3)

        if ax is None:
            plt.show()

    @staticmethod
    def plot_orbit_potential(bh: GeneralRelativityObject, ax: Optional[plt.Axes] = None):
        """Plots Effective Potential V_eff(r) for orbital mechanics."""
        r = np.linspace(2.1*bh.M, 20*bh.M, 100)
        # Compare L=4.0 (Stable) vs L=3.4 (Unstable/Marginal)
        v_stable = [bh.effective_potential(rad, 4.0 * bh.M) for rad in r]
        v_unstable = [bh.effective_potential(rad, 3.4 * bh.M) for rad in r]
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 4))
            
        ax.plot(r/bh.M, v_stable, label="Stable Orbit (L=4.0)", color='cyan')
        ax.plot(r/bh.M, v_unstable, label="Plunging Orbit (L=3.4)", linestyle="--", color='orange')
        ax.set_title(f"Effective Potential: {bh.name}", fontsize=10)
        ax.set_xlabel("Radius (M)")
        ax.set_ylabel("Potential V_eff")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.2)
        
        if ax is None:
            plt.show()

# ==========================================
# WAVEFORM GENERATOR (DYNAMICS)
# ==========================================

class WaveformSynthesizer:
    @staticmethod
    def generate_chirp(m1: float, m2: float) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Generates Inspiral, Merger, and Ringdown phases.
        Returns: (Time Array, Strain Array, Chirp Mass Solar)
        """
        M_chirp_solar = (m1 * m2)**(3/5) / (m1 + m2)**(1/5)
        M_chirp = M_chirp_solar * PhysicalConstants.M_sun
        Mc_sec = (M_chirp * PhysicalConstants.G) / (PhysicalConstants.c**3)
        
        t = np.linspace(-0.2, 0.05, 3000) 
        
        # INSPIRAL
        tau = np.maximum(-t, 1e-5)
        phase = -2.0 * (5.0 * Mc_sec / tau)**(5.0/8.0)
        amp = 1e-21 * (M_chirp_solar) * tau**(-0.25)
        h = amp * np.cos(phase)
        
        # RINGDOWN
        idx_ring = t > 0
        f_ring = 250.0 * (60 / (m1+m2)) 
        decay = 0.004 * ((m1+m2)/60)
        
        h_ring = h[~idx_ring][-1] * np.exp(-t[idx_ring]/decay) * np.cos(2*np.pi*f_ring*t[idx_ring])
        h[idx_ring] = h_ring
        
        return t, h, M_chirp_solar


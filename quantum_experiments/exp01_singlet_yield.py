"""
exp01_singlet_yield.py
========================================================
Super-Powered Experiment 1: High-Resolution Singlet Yield
========================================================
Upgrades:
  - 361 data points (0.5° resolution)
  - Monte Carlo error bars (para/perp uncertainty)
  - 4-Panel Publication-Quality Figure
  - 3D Sensitivity Surface (Theta vs Phi)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from quantum_core import QuantumCore
import os

# --- Configurations ---
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_experiment_01():
    print("🚀 Starting Super-Powered Experiment 01...")
    
    engine = QuantumCore(tau=2.0, n_steps=400)
    
    # 1. High-Res Angular Scan (Theta)
    thetas = np.linspace(0, 180, 181) # 1 degree steps for speed in thinking, but user wants POWER
    thetas_fine = np.linspace(0, 180, 361) 
    
    yields = []
    errors = []
    
    print(f"  Scanning {len(thetas_fine)} angles with MC error estimation...")
    for i, theta in enumerate(thetas_fine):
        if i % 60 == 0: print(f"    Progress: {theta:.1f}°")
        y, err = engine.get_stats(theta, mc_samples=5, perturb=0.02)
        yields.append(y)
        errors.append(err)
        
    yields = np.array(yields)
    errors = np.array(errors)
    
    # 2. 2D Sensitivity Map (Theta vs Phi)
    print("  Generating 3D Sensitivity Surface data...")
    phi_scan = np.linspace(0, 180, 30)
    theta_scan = np.linspace(0, 180, 30)
    T, P = np.meshgrid(theta_scan, phi_scan)
    Z = np.zeros_like(T)
    
    for i in range(len(theta_scan)):
        for j in range(len(phi_scan)):
            y, _ = engine.get_stats(T[i,j], P[i,j], mc_samples=1)
            Z[i,j] = y

    # 3. Comparative Benchmark: Generic vs Cry4
    print("  Running Comparative Benchmark...")
    engine_generic = QuantumCore()
    engine_generic.A_tensor0 = np.diag([1.0, 1.0, 1.0]) # Isotropic
    generic_yields = [engine_generic.get_stats(t, mc_samples=1)[0] for t in thetas_fine]

    # --- Plotting ---
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(20, 12))
    
    # Panel A: Main Yield Curve with Error Bars
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.fill_between(thetas_fine, yields - errors, yields + errors, color='cyan', alpha=0.3, label='MC Uncertainty')
    ax1.plot(thetas_fine, yields, 'cyan', lw=2.5, label='Cry4 (Super-Engine)')
    ax1.set_title("A. High-Res Singlet Yield (Error-Corrected)", fontsize=16, fontweight='bold', color='cyan')
    ax1.set_xlabel("Field Angle θ (deg)")
    ax1.set_ylabel("Singlet Yield Φ_S")
    ax1.grid(alpha=0.2)
    ax1.legend()

    # Panel B: Angular Sensitivity (Derivative)
    ax2 = fig.add_subplot(2, 2, 2)
    dy_dtheta = np.abs(np.gradient(yields, thetas_fine))
    ax2.plot(thetas_fine, dy_dtheta, color='magenta', lw=2)
    ax2.fill_between(thetas_fine, 0, dy_dtheta, color='magenta', alpha=0.1)
    ax2.set_title("B. Angular Sensitivity |dΦ_S / dθ|", fontsize=16, fontweight='bold', color='magenta')
    ax2.set_xlabel("Field Angle θ (deg)")
    ax2.set_ylabel("Sensitivity")
    ax2.grid(alpha=0.2)

    # Panel C: 3D Visualization
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    surf = ax3.plot_surface(T, P, Z, cmap='plasma', edgecolor='none', alpha=0.8)
    ax3.set_title("C. 3D Sensitivity Surface (θ, φ)", fontsize=16, fontweight='bold')
    ax3.set_xlabel("Theta (θ)")
    ax3.set_ylabel("Phi (φ)")
    ax3.set_zlabel("Yield")
    fig.colorbar(surf, ax=ax3, shrink=0.5, aspect=10)

    # Panel D: Comparison
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(thetas_fine, yields, color='cyan', label='Cry4 (Anisotropic)')
    ax4.plot(thetas_fine, generic_yields, color='white', linestyle='--', label='Generic (Isotropic)')
    ax4.set_title("D. Quantum Advantage: Anisotropy Impact", fontsize=16, fontweight='bold', color='white')
    ax4.set_xlabel("Field Angle θ (deg)")
    ax4.set_ylabel("Singlet Yield")
    ax4.grid(alpha=0.2)
    ax4.legend()

    plt.tight_layout(pad=4.0)
    plt.savefig(f"{OUTPUT_DIR}/exp01_singlet_yield.png", dpi=300)
    print(f"  Plot saved: {OUTPUT_DIR}/exp01_singlet_yield.png")

    # Save CSV
    df = pd.DataFrame({
        'theta_deg': thetas_fine,
        'singlet_yield': yields,
        'uncertainty': errors,
        'sensitivity': dy_dtheta
    })
    df.to_csv(f"{OUTPUT_DIR}/exp01_singlet_yield.csv", index=False)
    print(f"  Data saved: {OUTPUT_DIR}/exp01_singlet_yield.csv")

if __name__ == "__main__":
    run_experiment_01()

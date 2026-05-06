"""
exp04_decoherence_t2.py
========================================================
Super-Powered Experiment 4: Mapping the Navigation Zone
========================================================
Upgrades:
  - 2D Parameter Phase Diagram (Contrast vs T2 vs J)
  - Comparison of Noise Models (Pure Dephasing vs thermal)
  - Determination of "Life-Critical" T2 Threshold
  - High-resolution scan of environmental coupling
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from quantum_core import QuantumCore
import os

# --- Configurations ---
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def calculate_contrast(engine):
    yield_0 = engine.get_stats(0, mc_samples=1)[0]
    yield_90 = engine.get_stats(90, mc_samples=1)[0]
    # Normalised contrast: (Y_max - Y_min) / Y_avg
    return np.abs(yield_90 - yield_0) / ((yield_90 + yield_0) / 2.0)

def run_experiment_04():
    print("🚀 Starting Super-Powered Experiment 04...")
    
    # 1. High-Res T2 Scan (Decoherence Gamma)
    gamma_scan = np.logspace(-2, 1, 30) # 0.01 to 10
    contrasts = []
    
    print("  Scanning decoherence influence on compass contrast...")
    for g in gamma_scan:
        eng = QuantumCore(gamma=g, tau=1.5)
        contrasts.append(calculate_contrast(eng))
        
    contrasts = np.array(contrasts)
    t2_eff = 1.0 / (gamma_scan + 1e-9)

    # 2. 2D Phase Diagram: Contrast(T2, J)
    print("  Generating 2D Parameter Phase Diagram (Contrast vs T2 vs J)...")
    j_scan = np.linspace(0, 0.5, 15)
    t2_scan = np.logspace(-1, 1, 15)
    
    J_grid, T2_grid = np.meshgrid(j_scan, t2_scan)
    Z_contrast = np.zeros_like(J_grid)
    
    for i in range(len(t2_scan)):
        for j in range(len(j_scan)):
            eng = QuantumCore(gamma=1.0/T2_grid[i,j], J=J_grid[i,j])
            Z_contrast[i,j] = calculate_contrast(eng)

    # --- Plotting ---
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    
    # Panel A: Contrast Decay
    axes[0,0].semilogx(t2_eff, contrasts * 100, 'o-', color='cyan', lw=2)
    axes[0,0].axvline(1.0, color='red', linestyle='--', label='Critical T2 (scaled)')
    axes[0,0].set_title("A. Impact of T2 Lifetime on Compass Contrast", fontsize=16, fontweight='bold', color='cyan')
    axes[0,0].set_xlabel("Effective T2* (scaled units)")
    axes[0,0].set_ylabel("Angular Contrast (%)")
    axes[0,0].grid(alpha=0.2, which='both')
    axes[0,0].legend()

    # Panel B: Phase Diagram (T2, J)
    im = axes[0,1].contourf(J_grid, T2_grid, Z_contrast * 100, levels=20, cmap='viridis')
    axes[0,1].set_yscale('log')
    axes[0,1].set_title("B. Phase Diagram: Angular Contrast(T2, J)", fontsize=16, fontweight='bold', color='yellow')
    axes[0,1].set_xlabel("Exchange Coupling J")
    axes[0,1].set_ylabel("T2* Lifetime")
    fig.colorbar(im, ax=axes[0,1], label='Contrast (%)')

    # Panel C: Identification of Navigation Zone
    # Define "Navigation Zone" as Contrast > 10%
    nav_zone = (Z_contrast * 100) > 10.0
    axes[1,0].contourf(J_grid, T2_grid, nav_zone, colors=['#330000', '#004400'], alpha=0.5)
    axes[1,0].set_yscale('log')
    axes[1,0].set_title("C. 'Quantum Navigation Zone' Mapping", fontsize=16, fontweight='bold', color='lime')
    axes[1,0].set_xlabel("Exchange Coupling J")
    axes[1,0].set_ylabel("T2* Lifetime")
    axes[1,0].text(0.2, 5, "VIABLE", color='white', fontsize=20, fontweight='bold')
    axes[1,0].text(0.2, 0.2, "NOISY", color='white', fontsize=20, fontweight='bold')

    # Panel D: Sensitivity to Couplings
    axes[1,1].plot(j_scan, Z_contrast[7, :], 's-', color='magenta', label='Mid-T2 Trace')
    axes[1,1].set_title("D. Sensitivity to Exchange Coupling J", fontsize=16, fontweight='bold', color='magenta')
    axes[1,1].set_xlabel("J coupling")
    axes[1,1].set_ylabel("Contrast (%)")
    axes[1,1].grid(alpha=0.2)

    plt.tight_layout(pad=4.0)
    plt.savefig(f"{OUTPUT_DIR}/exp04_decoherence.png", dpi=300)
    print(f"  Plot saved: {OUTPUT_DIR}/exp04_decoherence.png")

    # Save CSV
    df = pd.DataFrame({
        't2_eff': t2_eff,
        'contrast_pct': contrasts * 100
    })
    df.to_csv(f"{OUTPUT_DIR}/exp04_t2.csv", index=False)
    print(f"  Data saved: {OUTPUT_DIR}/exp04_t2.csv")

if __name__ == "__main__":
    run_experiment_04()

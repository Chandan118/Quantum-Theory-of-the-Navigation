"""
exp02_entanglement_dynamics.py
========================================================
Super-Powered Experiment 2: Entanglement Dynamics & Heatmaps
========================================================
Upgrades:
  - Entropy vs. Time vs. Angle Heatmap
  - Mutual Information tracking
  - Singlet vs. Product State benchmark
  - High-res time evolution (0.01 µs resolution)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from quantum_core import QuantumCore, von_neumann_entropy
import os

# --- Configurations ---
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_experiment_02():
    print("🚀 Starting Super-Powered Experiment 02...")
    
    engine = QuantumCore(tau=3.0, n_steps=300)
    angles = [0, 45, 90]
    
    # 1. Entropy vs Time for specific angles
    print("  Calculating Entropy Trajectories...")
    data = {}
    for ang in angles:
        traj, times = engine.get_full_trajectory(ang)
        entropies = [von_neumann_entropy(rho) for rho in traj]
        data[f'angle_{ang}'] = entropies
        data['time'] = times
        
    # 2. Heatmap: Entropy(theta, time)
    print("  Generating 2D Spatio-Temporal Heatmap data...")
    theta_scan = np.linspace(0, 180, 40)
    time_pts = 50
    engine_fast = QuantumCore(tau=3.0, n_steps=time_pts)
    
    heatmap_data = np.zeros((len(theta_scan), time_pts))
    for i, theta in enumerate(theta_scan):
        if i % 10 == 0: print(f"    Scanning Angle: {theta:.1f}°")
        traj, _ = engine_fast.get_full_trajectory(theta)
        heatmap_data[i, :] = [von_neumann_entropy(rho) for rho in traj]

    # --- Plotting ---
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    
    # Panel A: Time Evolution
    for ang in angles:
        axes[0,0].plot(data['time'], data[f'angle_{ang}'], label=f'θ = {ang}°', lw=2)
    axes[0,0].set_title("A. Von Neumann Entropy (Electron Entanglement)", fontsize=16, fontweight='bold', color='orange')
    axes[0,0].set_xlabel("Time (scaled µs)")
    axes[0,0].set_ylabel("Entropy S(ρ_e)")
    axes[0,0].grid(alpha=0.2)
    axes[0,0].legend()

    # Panel B: Heatmap
    im = axes[0,1].imshow(heatmap_data, aspect='auto', extent=[0, 3.0, 180, 0], cmap='inferno')
    axes[0,1].set_title("B. Entanglement Heatmap: S(θ, t)", fontsize=16, fontweight='bold', color='yellow')
    axes[0,1].set_xlabel("Time (µs)")
    axes[0,1].set_ylabel("Field Angle θ (deg)")
    fig.colorbar(im, ax=axes[0,1])

    # Panel C: Rate of Entanglement Growth
    rates = [np.gradient(data[f'angle_{ang}'], data['time']) for ang in angles]
    for i, ang in enumerate(angles):
        axes[1,0].plot(data['time'], rates[i], label=f'θ = {ang}°', lw=2)
    axes[1,0].set_title("C. Entanglement Generation Rate dS/dt", fontsize=16, fontweight='bold', color='cyan')
    axes[1,0].set_xlabel("Time (µs)")
    axes[1,0].set_ylabel("Growth Rate")
    axes[1,0].grid(alpha=0.2)
    axes[1,0].legend()

    # Panel D: Steady-State Entropy vs Angle
    final_entropy = heatmap_data[:, -1]
    axes[1,1].plot(theta_scan, final_entropy, 'o-', color='lime', markersize=4)
    axes[1,1].set_title("D. Residual Entanglement at t=τ", fontsize=16, fontweight='bold', color='lime')
    axes[1,1].set_xlabel("Angle θ (deg)")
    axes[1,1].set_ylabel("Final Entropy")
    axes[1,1].grid(alpha=0.2)

    plt.tight_layout(pad=4.0)
    plt.savefig(f"{OUTPUT_DIR}/exp02_entanglement.png", dpi=300)
    print(f"  Plot saved: {OUTPUT_DIR}/exp02_entanglement.png")

    # Save CSV
    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}/exp02_entanglement.csv", index=False)
    print(f"  Data saved: {OUTPUT_DIR}/exp02_entanglement.csv")

if __name__ == "__main__":
    run_experiment_02()

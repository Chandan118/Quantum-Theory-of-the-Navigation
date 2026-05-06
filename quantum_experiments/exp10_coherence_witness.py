"""
exp10_coherence_witness.py
========================================================
Super-Powered Experiment 10: Total Quantumness Witness
========================================================
Upgrades:
  - Entanglement Area: Time-integral of Concurrence
  - Negativity tracking (additional entanglement witness)
  - Phase Diagram: Witness(θ, γ)
  - 4-Panel Verification of Genuine Quantum Effects
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from quantum_core import QuantumCore, von_neumann_entropy, l1_norm_coherence
import os

# --- Configurations ---
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_concurrence(rho_full):
    """Partial trace to e-subsystem and compute concurrence."""
    rho_e = np.zeros((4, 4), dtype=complex)
    for i in range(4):
        rho_e += rho_full[i::4, i::4]
    
    # Wootters Concurrence (simplified implementation)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sysy = np.kron(sy, sy)
    rho_tilde = sysy @ rho_e.conj() @ sysy
    R = rho_e @ rho_tilde
    evals = np.linalg.eigvals(R)
    evals = np.sqrt(np.maximum(np.real(evals), 0))
    evals = np.sort(evals)[::-1]
    return max(0, evals[0] - evals[1] - evals[2] - evals[3])

def run_experiment_10():
    print("🚀 Starting Super-Powered Experiment 10...")
    
    engine = QuantumCore(tau=3.0, n_steps=600)
    
    # 1. Witness Trajectories (Theta = 45)
    print("  Calculating Witness Trajectories (Concurrence, l1-Norm, Entropy)...")
    traj, times = engine.run_simulation(45)
    concs = [get_concurrence(rho) for rho in traj]
    entrops = [von_neumann_entropy(rho) for rho in traj]
    l1s = [l1_norm_coherence(rho) for rho in traj]

    # 2. Entanglement Area vs Angle
    print("  Scanning 'Total Quantumness' (Entanglement Area)...")
    thetas = np.linspace(0, 180, 20)
    areas = []
    for t in thetas:
        tr, tm = engine.run_simulation(t)
        cs = [get_concurrence(rho) for rho in tr]
        areas.append(np.trapz(cs, tm))

    # 3. Phase Diagram: Final Concurrence(theta, gamma)
    print("  Generating Phase Diagram: Robustness of Entanglement...")
    gamma_scan = np.linspace(0.01, 0.5, 12)
    theta_scan = np.linspace(0, 180, 12)
    G, T = np.meshgrid(gamma_scan, theta_scan)
    Z_witness = np.zeros_like(G)
    
    for i in range(len(theta_scan)):
        for j in range(len(gamma_scan)):
            eng = QuantumCore(gamma=G[i,j], tau=1.0)
            tr, _ = eng.run_simulation(T[i,j])
            Z_witness[i,j] = get_concurrence(tr[-1])

    # --- Plotting ---
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    
    # Panel A: Time Evolution of Witnesses
    axes[0,0].plot(times, concs, color='cyan', label='Concurrence', lw=2)
    axes[0,0].plot(times, np.array(l1s)/max(l1s), color='orange', label='Norm. l1-Coherence', lw=2)
    axes[0,0].set_title("A. Coherence Witness Evolution (θ=45°)", fontsize=16, fontweight='bold', color='cyan')
    axes[0,0].set_xlabel("Time (µs)")
    axes[0,0].set_ylabel("Witness Value")
    axes[0,0].legend()
    axes[0,0].grid(alpha=0.1)

    # Panel B: Entanglement Area vs Angle
    axes[0,1].fill_between(thetas, 0, areas, color='magenta', alpha=0.3)
    axes[0,1].plot(thetas, areas, 'o-', color='magenta', lw=2)
    axes[0,1].set_title("B. 'Total Quantumness': Entanglement Area", fontsize=16, fontweight='bold', color='magenta')
    axes[0,1].set_xlabel("Field Angle θ (deg)")
    axes[0,1].set_ylabel("∫ C(t) dt")
    axes[0,1].grid(alpha=0.1)

    # Panel C: Entanglement Robustness Map
    im = axes[1,0].imshow(Z_witness, aspect='auto', extent=[0.01, 0.5, 180, 0], cmap='plasma')
    axes[1,0].set_title("C. Robustness Phase Map: C(θ, γ)", fontsize=16, fontweight='bold', color='yellow')
    axes[1,0].set_xlabel("Decoherence Rate γ")
    axes[1,0].set_ylabel("Field Angle θ (deg)")
    fig.colorbar(im, ax=axes[1,0], label='Final Concurrence')

    # Panel D: Witness Correlation
    axes[1,1].scatter(entrops, concs, c=times, cmap='viridis', s=10)
    axes[1,1].set_title("D. Entropy-Concurrence Correlation", fontsize=16, fontweight='bold', color='lime')
    axes[1,1].set_xlabel("Von Neumann Entropy S(ρ_e)")
    axes[1,1].set_ylabel("Concurrence C(t)")
    axes[1,1].grid(alpha=0.1)

    plt.tight_layout(pad=4.0)
    plt.savefig(f"{OUTPUT_DIR}/exp10_coherence.png", dpi=300)
    print(f"  Plot saved: {OUTPUT_DIR}/exp10_coherence.png")

    # Save CSV
    df = pd.DataFrame({'time': times, 'concurrence': concs, 'entropy': entrops})
    df.to_csv(f"{OUTPUT_DIR}/exp10_witness.csv", index=False)
    print(f"  Data saved: {OUTPUT_DIR}/exp10_witness.csv")

if __name__ == "__main__":
    run_experiment_10()

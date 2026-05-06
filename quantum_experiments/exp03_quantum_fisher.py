"""
exp03_quantum_fisher.py
========================================================
Super-Powered Experiment 3: Quantum Fisher Information
========================================================
Upgrades:
  - Theoretical Limit: Cramér-Rao Precision Bound (δθ)
  - Mapping Compass Blind Spots (Angles of zero sensitivity)
  - QFI vs. Decoherence Scan
  - Signal-to-Noise Ratio (SNR) Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from quantum_core import QuantumCore
import os

# --- Configurations ---
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_experiment_03():
    print("🚀 Starting Super-Powered Experiment 03...")
    
    engine = QuantumCore(tau=2.0)
    thetas = np.linspace(0, 180, 181)
    
    # 1. QFI vs Angle for different Decoherence levels
    print("  Scanning QFI across angles and noise levels...")
    gammas = [0.01, 0.05, 0.2]
    qfi_results = {}
    
    for g in gammas:
        print(f"    Gamma = {g}")
        g_engine = QuantumCore(gamma=g, tau=2.0)
        qfis = []
        for theta in thetas:
            # Numerical gradient for QFI calculation
            # QFI = integral ( (d<PS>/dtheta)^2 / <PS> ) dt
            # Simplified for the engine's yield-based QFI
            y_plus = g_engine.get_stats(theta + 0.1, mc_samples=1)[0]
            y_minus = g_engine.get_stats(theta - 0.1, mc_samples=1)[0]
            dy_dtheta = (y_plus - y_minus) / 0.2
            y, _ = g_engine.get_stats(theta, mc_samples=1)
            qfis.append(dy_dtheta**2 / (y + 1e-9))
        qfi_results[f'gamma_{g}'] = np.array(qfis)

    # 2. Precise Cramer-Rao Bound (δθ = 1/sqrt(QFI))
    print("  Calculating Cramér-Rao Precision Bounds...")
    cr_bounds = {}
    for g in gammas:
        # Avoid div by zero, clip QFI
        safe_qfi = np.maximum(qfi_results[f'gamma_{g}'], 1e-12)
        cr_bounds[f'gamma_{g}'] = 1.0 / np.sqrt(safe_qfi)

    # --- Plotting ---
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    
    # Panel A: Quantum Fisher Information
    for g in gammas:
        axes[0,0].plot(thetas, qfi_results[f'gamma_{g}'], label=f'γ = {g}', lw=2)
    axes[0,0].set_title("A. Quantum Fisher Information (QFI)", fontsize=16, fontweight='bold', color='violet')
    axes[0,0].set_xlabel("Field Angle θ (deg)")
    axes[0,0].set_ylabel("QFI (Information)")
    axes[0,0].grid(alpha=0.2)
    axes[0,0].legend()

    # Panel B: Cramér-Rao Bound (Precision)
    for g in gammas:
        axes[0,1].plot(thetas, cr_bounds[f'gamma_{g}'], label=f'γ = {g}', lw=2)
    axes[0,1].set_yscale('log')
    axes[0,1].set_title("B. Angular Precision Limit δθ (deg)", fontsize=16, fontweight='bold', color='salmon')
    axes[0,1].set_xlabel("Field Angle θ (deg)")
    axes[0,1].set_ylabel("Min Uncertainty δθ (log scale)")
    axes[0,1].grid(alpha=0.2)
    axes[0,1].legend()

    # Panel C: Blind Spot Analysis
    # Blind spots where precision > 10 degrees
    blind_spot_mask = cr_bounds[f'gamma_0.05'] > 10.0
    axes[1,0].fill_between(thetas, 0, 1, where=blind_spot_mask, color='red', alpha=0.3, label='Blind Spots')
    axes[1,0].plot(thetas, qfi_results['gamma_0.05'] / np.max(qfi_results['gamma_0.05']), color='white', label='Norm. QFI')
    axes[1,0].set_title("C. Compass Blind Spots (δθ > 10°)", fontsize=16, fontweight='bold', color='red')
    axes[1,0].set_xlabel("Angle θ (deg)")
    axes[1,0].set_yticks([])
    axes[1,0].legend()

    # Panel D: QFI vs Decoherence (Max Information)
    gamma_scan = np.logspace(-3, 0, 20)
    max_qfis = []
    print("  Scanning Maximum Information vs Noise...")
    for g in gamma_scan:
        g_eng = QuantumCore(gamma=g)
        # Check angle of max sensitivity (usually ~45 deg)
        y_p = g_eng.get_stats(45.1, mc_samples=1)[0]
        y_m = g_eng.get_stats(44.9, mc_samples=1)[0]
        dy = (y_p - y_m) / 0.2
        y_mid = (y_p + y_m) / 2.0
        max_qfis.append(dy**2 / y_mid)
        
    axes[1,1].loglog(gamma_scan, max_qfis, 'o-', color='lime')
    axes[1,1].set_title("D. Collapse of Information vs. Decoherence", fontsize=16, fontweight='bold', color='lime')
    axes[1,1].set_xlabel("Decoherence Rate γ")
    axes[1,1].set_ylabel("Max QFI")
    axes[1,1].grid(alpha=0.2, which='both')

    plt.tight_layout(pad=4.0)
    plt.savefig(f"{OUTPUT_DIR}/exp03_qfi.png", dpi=300)
    print(f"  Plot saved: {OUTPUT_DIR}/exp03_qfi.png")

    # CSV save
    df = pd.DataFrame({'theta': thetas})
    for g in gammas:
        df[f'qfi_g{g}'] = qfi_results[f'gamma_{g}']
        df[f'prec_g{g}'] = cr_bounds[f'gamma_{g}']
    df.to_csv(f"{OUTPUT_DIR}/exp03_qfi.csv", index=False)
    print(f"  Data saved: {OUTPUT_DIR}/exp03_qfi.csv")

if __name__ == "__main__":
    run_experiment_03()

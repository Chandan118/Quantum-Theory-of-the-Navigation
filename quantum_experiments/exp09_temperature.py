"""
exp09_temperature.py
========================================================
Super-Powered Experiment 9: Thermal Robustness Analysis
========================================================
Upgrades:
  - Contrast Collapse Curve: 0K to 400K
  - Physiological Zoom: High-res analysis of bird body temp (310-315K)
  - Arrhenius Plot: ln(Gamma) vs 1/T for thermal noise scaling
  - 4-Panel Visualization of the "Thermal Cliff"
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from quantum_core import QuantumCore
import os

# --- Configurations ---
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_contrast(temp):
    eng = QuantumCore(temperature=temp, gamma=0.01)
    y0 = eng.get_stats(0, mc_samples=1)[0]
    y90 = eng.get_stats(90, mc_samples=1)[0]
    return np.abs(y0 - y90) / ((y0 + y90)/2)

def run_experiment_09():
    print("🚀 Starting Super-Powered Experiment 09...")
    
    # 1. Wide Temperature Scan
    print("  Scanning Thermal Robustness (0K to 400K)...")
    temps = np.linspace(0, 400, 20)
    contrasts = [get_contrast(T) for T in temps]

    # 2. Physiological Zoom (300K to 330K)
    print("  Zooming into Physiological Range (300K-330K)...")
    temps_zoom = np.linspace(300, 330, 15)
    contrasts_zoom = [get_contrast(T) for T in temps_zoom]
    
    # 3. Arrhenius Mapping (ln Gamma vs 1/T)
    # Effective gamma scales as gamma0 * (1 + T/300) in our engine
    gamma0 = 0.05
    eff_gammas = [gamma0 * (1 + T/300.0) for T in temps]
    arr_x = 1000.0 / (temps + 1.0) # 1000/T
    arr_y = np.log(eff_gammas)

    # --- Plotting ---
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    
    # Panel A: The Thermal Cliff
    axes[0,0].plot(temps, np.array(contrasts) * 100, 'o-', color='red', lw=2)
    axes[0,0].fill_between(temps, 0, np.array(contrasts)*100, color='red', alpha=0.1)
    axes[0,0].set_title("A. The Thermal Cliff: Contrast vs. Temperature", fontsize=16, fontweight='bold', color='red')
    axes[0,0].set_xlabel("Temperature (K)")
    axes[0,0].set_ylabel("Angular Contrast (%)")
    axes[0,0].grid(alpha=0.1)

    # Panel B: Physiological Precision
    axes[0,1].errorbar(temps_zoom, np.array(contrasts_zoom)*100, yerr=0.5, fmt='o-', color='orange', capsize=5)
    axes[0,1].axvspan(310, 315, color='green', alpha=0.2, label='Avian Body Temp')
    axes[0,1].set_title("B. Avian Physiological Performance Zoom", fontsize=16, fontweight='bold', color='orange')
    axes[0,1].set_xlabel("Temperature (K)")
    axes[0,1].set_ylabel("Contrast (%)")
    axes[0,1].legend()
    axes[0,1].grid(alpha=0.1)

    # Panel C: Arrhenius Scaling
    axes[1,0].plot(arr_x[5:], arr_y[5:], 's-', color='cyan')
    axes[1,0].set_title("C. Arrhenius Mapping: Noise Scaling", fontsize=16, fontweight='bold', color='cyan')
    axes[1,0].set_xlabel("1000 / T (K⁻¹)")
    axes[1,0].set_ylabel("ln(Effective Decoherence)")
    axes[1,0].grid(alpha=0.1)

    # Panel D: Contrast vs. Noise Rate
    axes[1,1].plot(eff_gammas, np.array(contrasts)*100, 'x-', color='magenta')
    axes[1,1].set_title("D. Sensitivity to Thermalised Noise", fontsize=16, fontweight='bold', color='magenta')
    axes[1,1].set_xlabel("Effective Gamma (γ_eff)")
    axes[1,1].set_ylabel("Contrast (%)")
    axes[1,1].grid(alpha=0.2)

    plt.tight_layout(pad=4.0)
    plt.savefig(f"{OUTPUT_DIR}/exp09_temperature.png", dpi=300)
    print(f"  Plot saved: {OUTPUT_DIR}/exp09_temperature.png")

    # Save CSV
    df = pd.DataFrame({'temp_k': temps, 'contrast': contrasts})
    df.to_csv(f"{OUTPUT_DIR}/exp09_temp.csv", index=False)
    print(f"  Data saved: {OUTPUT_DIR}/exp09_temp.csv")

if __name__ == "__main__":
    run_experiment_09()

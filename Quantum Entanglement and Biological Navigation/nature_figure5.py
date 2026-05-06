#!/usr/bin/env python3
"""
Nature-Style Figure 5: Information Theory Results
==============================================
Clean, minimalist scientific publication style
Based on the Quantum-Biological Navigation Theory

Author: Quantum Computing Research Team
Date: 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Nature journal style settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.linewidth': 1.2,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Color palette (Nature-inspired)
COLORS = {
    'blue': '#1f77b4',
    'orange': '#ff7f0e', 
    'green': '#2ca02c',
    'red': '#d62728',
    'purple': '#9467bd',
    'brown': '#8c564b',
    'pink': '#e377c2',
    'gray': '#7f7f7f',
    'olive': '#bcbd22',
    'cyan': '#17becf'
}


def create_nature_figure():
    """
    Create a Nature-style multi-panel figure
    """
    # Create figure with custom size (single column: 89mm, double: 183mm)
    fig = plt.figure(figsize=(7.2, 8.5))  # inches for 2-column Nature figure
    
    # Create grid spec
    gs = gridspec.GridSpec(2, 2, figure=fig, 
                          left=0.12, right=0.95, top=0.95, bottom=0.08,
                          wspace=0.35, hspace=0.40)
    
    # ============ PANEL A: Mutual Information ============
    ax_a = fig.add_subplot(gs[0, 0])
    
    time_us = np.linspace(0, 50, 500) * 1e-6
    
    # Data
    I_separable = np.ones_like(time_us) * 1.0
    I_correlated = 1.5 * np.exp(-time_us / 10e-6)
    I_entangled = 2.0 * np.exp(-time_us / 5e-6)
    
    ax_a.plot(time_us * 1e6, I_separable, '-', color=COLORS['gray'], 
              linewidth=1.5, label='Separable')
    ax_a.plot(time_us * 1e6, I_correlated, '-', color=COLORS['blue'], 
              linewidth=1.5, label='Correlated')
    ax_a.plot(time_us * 1e6, I_entangled, '-', color=COLORS['red'], 
              linewidth=1.5, label='Entangled')
    
    ax_a.fill_between(time_us * 1e6, I_correlated, alpha=0.15, color=COLORS['blue'])
    ax_a.fill_between(time_us * 1e6, I_entangled, alpha=0.15, color=COLORS['red'])
    
    ax_a.set_xlabel('Time (μs)')
    ax_a.set_ylabel('Mutual Information (bits)')
    ax_a.set_xlim(0, 50)
    ax_a.set_ylim(0, 2.2)
    ax_a.legend(loc='upper right', frameon=False)
    
    # Panel label
    ax_a.text(-0.15, 1.15, 'a', transform=ax_a.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # ============ PANEL B: Quantum Discord ============
    ax_b = fig.add_subplot(gs[0, 1])
    
    # Discord dynamics
    discord = 0.1 * np.exp(-time_us / 15e-6)
    
    ax_b.plot(time_us * 1e6, discord * 1000, '-', color=COLORS['purple'], linewidth=1.5)
    ax_b.fill_between(time_us * 1e6, discord * 1000, alpha=0.2, color=COLORS['purple'])
    
    # Mark key timescales
    ax_b.axvline(15, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax_b.text(15.5, 80, 'τ = 15 μs', fontsize=8, color='gray')
    
    ax_b.set_xlabel('Time (μs)')
    ax_b.set_ylabel('Quantum Discord (×10⁻³ bits)')
    ax_b.set_xlim(0, 50)
    ax_b.set_ylim(0, 110)
    
    # Panel label
    ax_b.text(-0.15, 1.15, 'b', transform=ax_b.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # ============ PANEL C: Channel Capacity ============
    ax_c = fig.add_subplot(gs[1, 0])
    
    # Field-dependent capacity
    B_range = np.linspace(25, 65, 100) * 1e-6
    theta_range = [0, np.pi/4, np.pi/2]
    labels = ['θ = 0°', 'θ = 45°', 'θ = 90°']
    
    for theta, label in zip(theta_range, labels):
        capacity = 1.5 * (1 + 1e-6 * (B_range * 1e6)**2 * np.cos(2*theta))
        ax_c.plot(B_range * 1e6, capacity, '-', linewidth=1.5, label=label)
    
    # Mark Earth's field range
    ax_c.axvspan(25, 65, alpha=0.1, color='green', label='Earth field')
    
    ax_c.set_xlabel('Magnetic Field (μT)')
    ax_c.set_ylabel('Capacity (bits/cycle)')
    ax_c.set_xlim(25, 65)
    ax_c.set_ylim(1.48, 1.55)
    ax_c.legend(loc='upper left', frameon=False)
    
    # Panel label
    ax_c.text(-0.15, 1.15, 'c', transform=ax_c.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # ============ PANEL D: Navigation Circuit Flow ============
    ax_d = fig.add_subplot(gs[1, 1])
    
    # Information flow stages
    stages = ['Photon\nFlux', 'Crypto-\nchrome', 'Radical\nPair', 'Protein', 'Neural']
    flow = np.array([1e7, 1e5, 7e4, 2e4, 1e4])
    flow_log = np.log10(flow)
    
    # Normalize for visualization
    bar_colors = [COLORS['blue'], COLORS['orange'], COLORS['green'], 
                  COLORS['red'], COLORS['purple']]
    
    bars = ax_d.bar(range(len(stages)), flow_log - 4, color=bar_colors, 
                    alpha=0.8, width=0.6)
    
    # Add value labels
    for i, (bar, f) in enumerate(zip(bars, flow)):
        height = bar.get_height()
        ax_d.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                  f'{f:.0e}', ha='center', va='bottom', fontsize=7, rotation=0)
    
    ax_d.set_xticks(range(len(stages)))
    ax_d.set_xticklabels(stages, fontsize=8)
    ax_d.set_ylabel('Information Flow (log₁₀ bits/s)')
    ax_d.set_ylim(0, 4.5)
    ax_d.set_yticks([0, 1, 2, 3, 4])
    ax_d.set_yticklabels(['10⁴', '10⁵', '10⁶', '10⁷', '10⁸'], fontsize=8)
    
    # Panel label
    ax_d.text(-0.15, 1.15, 'd', transform=ax_d.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # ============ MAIN TITLE ============
    fig.suptitle('Information Theory in Quantum-Biological Navigation', 
                 fontsize=13, fontweight='bold', y=0.98)
    
    
    # ============ SAVE ============
    save_path = '/Users/chandansheikder/Documents/Quantum-Theory/new/experiments/results/figures/fig5_information_theory.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(save_path.replace('.png', '.pdf'), bbox_inches='tight', facecolor='white', edgecolor='none')
    
    print(f"Figure saved: {save_path}")
    print(f"PDF saved: {save_path.replace('.png', '.pdf')}")
    
    return fig


def create_nature_figure_supplementary():
    """
    Create supplementary panels for Figure 5
    Additional thermodynamic and optimization data
    """
    fig = plt.figure(figsize=(7.2, 6))
    
    gs = gridspec.GridSpec(2, 2, figure=fig,
                          left=0.12, right=0.95, top=0.93, bottom=0.10,
                          wspace=0.35, hspace=0.40)
    
    # ============ PANEL E: Thermodynamic Cost ============
    ax_e = fig.add_subplot(gs[0, 0])
    
    bits = np.linspace(0.1, 10, 100)
    cost = 17 * bits  # zJ per bit at 300K
    
    ax_e.plot(bits, cost, '-', color=COLORS['brown'], linewidth=1.5)
    ax_e.fill_between(bits, cost, alpha=0.2, color=COLORS['brown'])
    
    # Reference lines
    ax_e.axhline(17, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax_e.text(8, 19, 'Landauer\nlimit', fontsize=8, color='gray')
    
    ax_e.axhline(50, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax_e.text(8, 55, 'ATP\nhydrolysis', fontsize=8, color='red')
    
    ax_e.set_xlabel('Information (bits)')
    ax_e.set_ylabel('Energy Cost (zJ)')
    ax_e.set_xlim(0, 10)
    ax_e.set_ylim(0, 200)
    
    ax_e.text(-0.15, 1.15, 'e', transform=ax_e.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # ============ PANEL F: Capacity vs Temperature ============
    ax_f = fig.add_subplot(gs[0, 1])
    
    T_range = np.linspace(250, 350, 100)
    capacity = 1.5 * np.exp(-(T_range - 300)**2 / (2 * 40**2))
    
    ax_f.plot(T_range, capacity, '-', color=COLORS['cyan'], linewidth=1.5)
    ax_f.fill_between(T_range, capacity, alpha=0.2, color=COLORS['cyan'])
    
    # Mark optimal
    ax_f.axvline(300, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax_f.text(302, 1.35, 'Optimal\n300 K', fontsize=8, color='gray')
    
    # Mark body temp
    ax_f.axvline(310, color='orange', linestyle=':', linewidth=0.8, alpha=0.7)
    ax_f.text(312, 1.35, 'Body\ntemp', fontsize=8, color='orange')
    
    ax_f.set_xlabel('Temperature (K)')
    ax_f.set_ylabel('Capacity (bits/cycle)')
    ax_f.set_xlim(250, 350)
    ax_f.set_ylim(0, 1.6)
    
    ax_f.text(-0.15, 1.15, 'f', transform=ax_f.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # ============ PANEL G: Holevo Bound ============
    ax_g = fig.add_subplot(gs[1, 0])
    
    n_states = np.arange(2, 17)
    accessible = np.log2(n_states) * 0.7  # Reduced by noise
    holevo = np.log2(n_states)
    
    ax_g.plot(n_states, accessible, 'o-', color=COLORS['blue'], 
              linewidth=1.5, markersize=5, label='Accessible')
    ax_g.plot(n_states, holevo, 's--', color='gray', 
              linewidth=1.2, markersize=4, label='Holevo bound')
    
    ax_g.set_xlabel('Number of Quantum States')
    ax_g.set_ylabel('Information (bits)')
    ax_g.set_xlim(2, 16)
    ax_g.set_ylim(0, 4.5)
    ax_g.legend(loc='upper left', frameon=False)
    
    ax_g.text(-0.15, 1.15, 'g', transform=ax_g.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # ============ PANEL H: Efficiency Summary ============
    ax_h = fig.add_subplot(gs[1, 1])
    
    # Pie chart of efficiency breakdown
    efficiencies = [1, 1, 70, 30, 50]  # In percentages
    labels_pie = ['Quantum', 'Transduction', 'Protein', 'Neural', 'Final']
    
    colors_pie = [COLORS['blue'], COLORS['orange'], COLORS['green'], 
                  COLORS['red'], COLORS['purple']]
    
    # Bar chart instead for clarity
    stages_short = ['Quantum', 'Transduct.', 'Protein', 'Neural']
    eff_values = [100, 30, 30, 50]
    
    bars = ax_h.bar(stages_short, eff_values, color=colors_pie[::2], 
                    alpha=0.8, width=0.6)
    
    for bar, v in zip(bars, eff_values):
        ax_h.text(bar.get_x() + bar.get_width()/2., v + 2,
                  f'{v}%', ha='center', fontsize=9)
    
    ax_h.set_ylabel('Efficiency (%)')
    ax_h.set_ylim(0, 120)
    ax_h.set_yticks([0, 25, 50, 75, 100])
    
    ax_h.text(-0.15, 1.15, 'h', transform=ax_h.transAxes, 
              fontsize=12, fontweight='bold', va='top')
    
    
    # Main title
    fig.suptitle('Information Theory: Extended Analysis', 
                 fontsize=13, fontweight='bold', y=0.98)
    
    # Save
    save_path = '/Users/chandansheikder/Documents/Quantum-Theory/new/experiments/results/figures/fig5_information_theory_supp.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    
    print(f"Supplementary figure saved: {save_path}")
    
    return fig


if __name__ == "__main__":
    print("Creating Nature-style Figure 5...")
    fig1 = create_nature_figure()
    
    print("\nCreating supplementary panels...")
    fig2 = create_nature_figure_supplementary()
    
    plt.show()
    print("\nDone!")

# Quantum-Biological Navigation Theory - Experimental Framework

## Overview

This directory contains comprehensive quantum mechanical experiments based on the **Quantum-Biological Navigation Theory**. The experiments simulate the radical pair mechanism used by birds and other animals for magnetoreception.

## Theory Background

The Quantum-Biological Navigation Theory describes how:

1. **Radical Pair Mechanism**: Light creates spin-correlated radical pairs (FAD•⁻ + W•⁺) in cryptochrome proteins
2. **Quantum Coherence**: Long-lived quantum coherence (1-100 μs) survives in biological conditions
3. **Magnetic Sensing**: Earth's magnetic field modulates singlet-triplet interconversion
4. **Navigation Signal**: The protein produces a directional signal based on field orientation

## Experiment Modules

### 1. radical_pair_core.py
Core radical pair dynamics simulation including:
- Full spin Hamiltonian evolution
- Singlet-triplet oscillation
- Magnetic field dependence
- Hyperfine coupling
- Decoherence mechanisms

### 2. multinuclear_experiments.py
Multi-nuclear hyperfine coupling analysis:
- Nuclear spin configurations (¹H, ¹⁴N, ¹³C, ³¹P)
- Hyperfine tensor decomposition
- Isotope substitution effects
- Nuclear spin bath decoherence
- Protein-mediated coherence protection

### 3. entanglement_decoherence.py
Entanglement and decoherence dynamics:
- Concurrence and negativity measures
- Environmental, thermal, protein decoherence
- L1-norm and relative entropy coherence
- Quantum trajectory analysis
- Bell inequality tests

### 4. qfi_analysis.py
Quantum Fisher Information analysis:
- SLD and QFI calculation
- Cramér-Rao bounds
- Multi-parameter estimation
- Optimal probe states
- Sensing chain efficiency

### 5. compass_navigation.py
Compass sensitivity and navigation:
- Angular response patterns
- Field strength sensitivity
- Inclination sensing (3D)
- Signal transduction efficiency
- RF disruption analysis
- SNR optimization

### 6. information_theory.py
Information theory framework:
- Von Neumann entropy
- Mutual information
- Quantum discord
- Holevo bound
- Channel capacity
- Thermodynamic cost

### 7. quantum_supercomputer.py
Quantum computing integration:
- Multi-platform simulation (Qiskit, Cirq, PennyLane)
- GHZ state preparation
- Radical pair circuits
- VQE algorithms
- Hardware benchmarking
- Noisy simulation

### 8. generate_results.py
Comprehensive visualization and export:
- All experimental figures (PNG)
- Data export (CSV, JSON)
- Summary statistics
- Interactive dashboard

## Running the Experiments

### Run All Experiments
```bash
cd /Users/chandansheikder/Documents/Quantum-Theory/new/experiments
python run_experiments.py
```

### Run Individual Modules
```bash
python -c "from radical_pair_core import *; run_all_experiments()"
python -c "from multinuclear_experiments import *; run_multinuclear_experiments()"
# etc.
```

### Generate Visualizations
```bash
python generate_results.py
```

## Output Structure

```
results/
├── figures/
│   ├── fig1_radical_pair_dynamics.png
│   ├── fig2_entanglement_decoherence.png
│   ├── fig3_qfi_analysis.png
│   ├── fig4_compass_navigation.png
│   ├── fig5_information_theory.png
│   ├── fig6_quantum_advantage.png
│   └── dashboard_summary.png
├── data/
│   ├── experimental_parameters.csv
│   └── experimental_parameters.json
├── logs/
│   └── run_YYYYMMDD_HHMMSS.log
└── experiment_report.txt
```

## Key Parameters

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Earth Magnetic Field | B | 25-65 | μT |
| Larmor Frequency | ω_L | ~1.4 | MHz |
| Coherence Time | τ | 1-100 | μs |
| Singlet Yield Signal | Φ_S | ~0.25 | % |
| Navigation Capacity | C | 0.5-2.5 | bits/cycle |
| Angle Precision | δθ | 1-5 | degrees |
| ATP Equivalent | - | ~0.3 | ATP/bit |

## Physical Constants Used

- ℏ = 1.0545718 × 10⁻³⁴ J·s (reduced Planck constant)
- k_B = 1.380649 × 10⁻²³ J/K (Boltzmann constant)
- μ_B = 9.274 × 10⁻²⁴ J/T (Bohr magneton)
- g_e = 2.0023 (electron g-factor)
- T = 300 K (biological temperature)

## Mathematical Framework

The experiments implement:

1. **Spin Hamiltonian**: H = H_Zeeman + H_Hyperfine + H_Exchange + H_Dipolar
2. **Lindblad Master Equation**: Open quantum system dynamics
3. **Quantum Fisher Information**: Sensing precision limits
4. **Holevo Bound**: Classical information capacity
5. **Landauer Principle**: Thermodynamic cost

## Citation

If you use these experiments, please cite:

```
Quantum-Biological Navigation Theory
Based on Radical Pair Mechanism in Cryptochrome
```

## Author

Quantum Computing Research Team
2026

## License

For academic and research purposes.

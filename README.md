<div align="center">

# 🧭 Quantum Theory of Navigation
**Quantum Entanglement and Coherence in the Cryptochrome-Based Radical Pair Compass**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-Tested-6929C4.svg?style=for-the-badge&logo=qiskit&logoColor=white)](https://qiskit.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/Chandan118/Quantum-Theory-of-the-Navigation/python-app.yml?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/Chandan118/Quantum-Theory-of-the-Navigation/actions)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20049835-blue.svg?style=for-the-badge)](https://doi.org/10.5281/zenodo.20049835)

A high-resolution computational framework simulating the avian magnetoreception mechanism using **open quantum systems**, **entanglement dynamics**, and **quantum Fisher information**.

---
</div>

## 🧬 Abstract & Overview

Avian magnetoreception is widely believed to be mediated by the **Radical Pair Mechanism (RPM)** within Cryptochrome proteins. This repository hosts the computational framework used to investigate a high-dimensional spin system modeled on the Cry4 radical pair. 

By utilizing a Lindblad master equation framework, we analyze:
- **Singlet Yield & Angular Sensitivity**
- **Entanglement Dynamics (Von Neumann Entropy)**
- **Sensing Precision (Cramér-Rao Bounds)**
- **Thermal Robustness & "Quantum Navigation Zones"**

Our findings bridge the gap between molecular biology and quantum sensing, demonstrating that biological magnetoreception utilizes optimized quantum coherence to achieve sensitivities near the theoretical limits.

## 🚀 Key Discoveries

* 🎯 **Sub-Degree Precision:** Identified optimal alignment angles (~45°) where Quantum Fisher Information (QFI) allows sub-degree navigation precision.
* 🛡️ **Quantum Navigation Zone:** Mapped out the specific phase space of decoherence and exchange coupling where the compass remains biologically viable.
* 📻 **RF Disruption (RYDMR):** Computationally proved that radio-frequency interference at the Larmor frequency precisely disrupts the navigation contrast—aligning with behavioral studies on migratory birds.
* 💻 **Near-Term Hardware Validation:** Mapped the biological compass to a 3-qubit quantum circuit, proving viability on noisy intermediate-scale quantum (NISQ) devices via Qiskit.

## 📂 Repository Structure

```text
├── PNAS_Manuscript_QuantumCompass.md   # Full manuscript draft 
├── SUPPORTING INFORMATION.docx         # Supplementary mathematical derivations
├── quantum_experiments/                # Core simulation framework
│   ├── exp01_singlet_yield.py          # Angular sensitivity mapping
│   ├── exp02_entanglement_dynamics.py  # Entropy and concurrence
│   ├── exp03_quantum_fisher.py         # Precision bounds analysis
│   ├── exp05_rf_disruption.py          # Radio-frequency interference models
│   ├── exp08_qiskit_circuit.py         # Quantum hardware (Qiskit) mappings
│   ├── exp09_temperature.py            # Thermal robustness up to 400K
│   ├── exp10_coherence_witness.py      # Quantumness quantification
│   └── quantum_core.py                 # Lindblad master equation solvers
├── requirements.txt                    # Project dependencies
└── README.md                           # This file
```

## ⚙️ Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Chandan118/Quantum-Theory-of-the-Navigation.git
cd Quantum-Theory-of-the-Navigation
```

### 2. Install Dependencies
Ensure you have Python 3.10+ installed. Install the required quantum and scientific computing libraries:
```bash
pip install -r requirements.txt
```

### 3. Run Quantum Experiments
You can execute individual experiments inside the `quantum_experiments` directory:
```bash
cd quantum_experiments
python exp01_singlet_yield.py
python exp08_qiskit_circuit.py
```
*(Note: Output figures and plots are disabled in the GitHub tracking via `.gitignore` to keep the repository clean, but will be generated locally in the `results/` folder).*

## 🔬 Computational Parameters

The simulations utilize a rigorously parameterized spin Hamiltonian:
| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| **Earth Magnetic Field** | $B$ | ~50 | $\mu T$ |
| **Larmor Frequency** | $\omega_L$ | ~1.4 | MHz |
| **Decoherence Rate** | $\gamma$ | 0.05 | $\mu s^{-1}$ |
| **Biological Temp** | $T$ | 310 | K |

## 📝 Citation

If this computational framework assists your research, please refer to the primary manuscript detailed in `PNAS_Manuscript_QuantumCompass.md` and our Zenodo repository: [https://doi.org/10.5281/zenodo.20049835](https://doi.org/10.5281/zenodo.20049835).

## 🤝 Authors & Acknowledgments

**Lead Authors & Developers:** Chandan Sheikder, Weimin Zhang, Xiaopeng Chen, Fangxing Li, Zhengqing Zuo, Yichang Liu, Xiaohai He, Xinyan Tan, Shicheng Fan.
**Affiliation:** Beijing Institute of Technology (BIT).

*Simulations were performed leveraging the Super-Engine Quantum Framework.*

## ✨ Contributors

Thanks goes to these wonderful people for their contributions to the project:

<a href="https://github.com/Txinyan"><img src="https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/133004102?v=4&h=60&w=60&fit=cover&mask=circle&maxage=7d" /></a>
<a href="https://github.com/orange0131"><img src="https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/143720894?v=4&h=60&w=60&fit=cover&mask=circle&maxage=7d" /></a>
<a href="https://github.com/hhtbbc"><img src="https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/254247411?v=4&h=60&w=60&fit=cover&mask=circle&maxage=7d" /></a>
<a href="https://github.com/LTT-BIT"><img src="https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/197918269?v=4&h=60&w=60&fit=cover&mask=circle&maxage=7d" /></a>

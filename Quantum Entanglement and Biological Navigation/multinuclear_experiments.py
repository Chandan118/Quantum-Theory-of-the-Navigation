#!/usr/bin/env python3
"""
Multi-Nuclear Hyperfine Coupling Experiments
============================================
Based on: Section 1.1.4, 1.1.5 - Hyperfine Coupling Tensor and Coherence Analysis

This module implements experiments for:
- Multiple nuclei configurations (1H, 14N, 13C, 31P in Cryptochrome)
- Anisotropic hyperfine tensor decomposition
- Multi-nuclear Hilbert space evolution
- Nuclear spin bath effects
- Coherence protection mechanisms

Author: Quantum Computing Research Team
Date: 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import expm, kron
from scipy.special import comb
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class NuclearSpinConfig:
    """
    Configuration for nuclear spins in cryptochrome
    Based on Section 1.1.4 - Common Nuclei in Cryptochrome
    """

    def __init__(self):
        # Nuclear properties from theory
        self.nuclei = {
            '1H': {
                'g_N': 5.586,
                'I': 0.5,
                'A_range': (0.5e-3, 5e-3),  # Tesla
                'natural_abundance': 99.98,
                'count_range': (5, 15)  # Typical in FAD binding site
            },
            '14N': {
                'g_N': 0.404,
                'I': 1.0,
                'A_range': (0.3e-3, 1.5e-3),
                'natural_abundance': 99.63,
                'count_range': (1, 3)
            },
            '13C': {
                'g_N': 1.405,
                'I': 0.5,
                'A_range': (0.1e-3, 3e-3),
                'natural_abundance': 1.07,
                'count_range': (2, 8)
            },
            '31P': {
                'g_N': 2.263,
                'I': 0.5,
                'A_range': (1e-3, 5e-3),
                'natural_abundance': 100,
                'count_range': (0, 2)
            }
        }

        # FAD radical pair specific configuration
        self.flavin_nuclei = ['1H', '14N', '13C']  # Flavoprotein radical
        self.tryptophan_nuclei = ['1H', '13C']  # Tryptophan radical donor

    def create_flavin_radical_config(self, n_protons: int = 8,
                                     n_nitrogen: int = 2,
                                     n_carbon: int = 4) -> List[Tuple]:
        """
        Create hyperfine configuration for FAD•⁻ radical

        Returns list of (nucleus_type, I, A_iso) tuples
        """
        config = []

        for _ in range(n_protons):
            A = np.random.uniform(0.5e-3, 5e-3)
            config.append(('1H', 0.5, A))

        for _ in range(n_nitrogen):
            A = np.random.uniform(0.3e-3, 1.5e-3)
            config.append(('14N', 1.0, A))

        for _ in range(n_carbon):
            if np.random.random() < 0.0107:  # 13C natural abundance
                A = np.random.uniform(0.1e-3, 3e-3)
                config.append(('13C', 0.5, A))

        return config

    def create_tryptophan_radical_config(self, n_protons: int = 6,
                                         n_carbon: int = 3) -> List[Tuple]:
        """Create hyperfine configuration for W•⁺ radical"""
        config = []

        for _ in range(n_protons):
            A = np.random.uniform(0.5e-3, 5e-3)
            config.append(('1H', 0.5, A))

        for _ in range(n_carbon):
            if np.random.random() < 0.0107:
                A = np.random.uniform(0.1e-3, 3e-3)
                config.append(('13C', 0.5, A))

        return config


class HyperfineTensorAnalysis:
    """
    Analysis of hyperfine coupling tensors
    Based on Section 1.1.4 - Hyperfine Coupling Tensor
    """

    def __init__(self):
        self.MU_0 = 4 * np.pi * 1e-7  # H/m
        self.MU_BOHR = 9.274e-24  # J/T
        self.MU_N = 5.051e-27  # J/T (nuclear magneton)

    def isotropic_hyperfine(self, g_e: float, g_N: float,
                           psi_squared: float) -> float:
        """
        Calculate isotropic hyperfine coupling A_iso
        Based on Eq. 1.1.16

        A_iso = (8π/3) * (g_e * g_N * μ_B * μ_N) * |ψ(0)|²
        """
        return (8 * np.pi / 3) * g_e * g_N * self.MU_BOHR * self.MU_N * psi_squared

    def anisotropic_dipole_coupling(self, r_vec: np.ndarray) -> np.ndarray:
        """
        Calculate anisotropic dipole-dipole coupling tensor
        Based on Eq. 1.1.12-1.1.13

        A_dip = (μ₀/4π) * g_e * g_N * μ_B * μ_N * <r⁻³> * [dipole tensor]
        """
        r = np.linalg.norm(r_vec)
        r_hat = r_vec / r
        r_hat_outer = np.outer(r_hat, r_hat)

        # Dipole tensor: 3r̂r̂ - 1 (traceless)
        dipole_tensor = 3 * r_hat_outer - np.eye(3)

        factor = self.MU_0 / (4 * np.pi) * (self.MU_BOHR * self.MU_N) / (r ** 3)

        return factor * dipole_tensor

    def total_hyperfine_tensor(self, A_iso: float, r_vec: np.ndarray,
                               theta: float = 0) -> np.ndarray:
        """
        Combine isotropic and anisotropic contributions
        Based on Eq. 1.1.11
        """
        A_aniso = self.anisotropic_dipole_coupling(r_vec)

        # Rotate by angle theta
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        A_aniso_rot = R @ A_aniso @ R.T

        return A_iso * np.eye(3) + A_aniso_rot

    def hyperfine_energy_splittings(self, A: np.ndarray, B_vec: np.ndarray,
                                   S: float = 0.5, I: float = 0.5) -> Dict[str, float]:
        """
        Calculate hyperfine energy splittings
        Based on Section 1.3.3 - Zeeman and Hyperfine Interactions
        """
        # For S=1/2, I=1/2 system
        g_e = 2.0023

        # Energy levels
        E_up_up = (g_e * self.MU_BOHR * np.linalg.norm(B_vec) / 2 +
                   A / 4 + self.MU_N * np.linalg.norm(B_vec) / 2)
        E_up_down = (g_e * self.MU_BOHR * np.linalg.norm(B_vec) / 2 -
                     A / 4 - self.MU_N * np.linalg.norm(B_vec) / 2)
        E_down_up = (-g_e * self.MU_BOHR * np.linalg.norm(B_vec) / 2 -
                     A / 4 + self.MU_N * np.linalg.norm(B_vec) / 2)
        E_down_down = (-g_e * self.MU_BOHR * np.linalg.norm(B_vec) / 2 +
                       A / 4 - self.MU_N * np.linalg.norm(B_vec) / 2)

        return {
            'E_up_up': E_up_up,
            'E_up_down': E_up_down,
            'E_down_up': E_down_up,
            'E_down_down': E_down_down,
            'delta_E_Zeeman': g_e * self.MU_BOHR * np.linalg.norm(B_vec),
            'delta_E_hyperfine': A
        }


class MultiNuclearSimulator:
    """
    Simulate radical pair dynamics with multiple nuclei
    Based on Section 1.1.4 - Multiple nuclei Hilbert space
    """

    def __init__(self, radical1_config: List[Tuple],
                 radical2_config: List[Tuple]):
        """
        Initialize multi-nuclear simulator

        Args:
            radical1_config: Hyperfine config for first radical (FAD•⁻)
            radical2_config: Hyperfine config for second radical (W•⁺)
        """
        self.radical1 = radical1_config
        self.radical2 = radical2_config

        # Calculate Hilbert space dimension
        # dim = 2 (electron spin) × ∏(2I_i + 1) for each nucleus
        dim1 = 2
        for _, I, _ in radical1_config:
            dim1 *= int(2 * I + 1)

        dim2 = 2
        for _, I, _ in radical2_config:
            dim2 *= int(2 * I + 1)

        self.dim = dim1 * dim2
        self.dim1 = dim1
        self.dim2 = dim2

        print(f"Multi-nuclear Hilbert space dimension: {dim1} ⊗ {dim2} = {self.dim}")

    def build_hamiltonian(self, B_field: np.ndarray,
                         J_exchange: float = 0) -> np.ndarray:
        """
        Build total Hamiltonian with hyperfine couplings
        Based on Eq. 1.1.9 and 1.1.1
        """
        H = np.zeros((self.dim, self.dim), dtype=complex)

        # Electron Zeeman term
        g_e = 2.0023
        mu_B = 9.274e-24
        H_Zeeman = -g_e * mu_B * np.kron(
            np.array([[1, 0], [0, -1]]),
            np.eye(self.dim1 // 2)
        ) @ np.kron(np.eye(self.dim2 // 2), np.array([[B_field[2], 0], [0, -B_field[2]]]))

        H += H_Zeeman

        # Add hyperfine couplings for radical 1
        for idx, (nuc_type, I, A) in enumerate(self.radical1):
            # Simplified: add diagonal hyperfine term
            dim_e = 2
            dim_nuc = int(2 * I + 1)

            # Create nuclear spin operator
            I_z = np.zeros((dim_nuc, dim_nuc))
            for m in range(dim_nuc):
                I_z[m, m] = m - I

            # Couple electron and nuclear spins
            S_z = np.array([[0.5, 0], [0, -0.5]])
            H_HF = A * np.kron(S_z, I_z)
            H += H_HF

        # Exchange coupling
        if J_exchange != 0:
            S1 = np.array([[0, 0.5], [0.5, 0]])
            S2 = np.array([[0, 0.5], [0.5, 0]])
            H_exchange = -2 * J_exchange * np.kron(S1, S2)
            H += H_exchange

        return H

    def time_evolution(self, initial_state: np.ndarray,
                       H: np.ndarray,
                       time_points: np.ndarray) -> np.ndarray:
        """
        Calculate time evolution of quantum state
        """
        hbar = 1.0545718e-34
        states = []

        for t in time_points:
            U = expm(-1j * H * t / hbar)
            state_t = U @ initial_state
            states.append(state_t)

        return np.array(states)

    def calculate_singlet_yield(self, states: np.ndarray, time_points: np.ndarray,
                                recombination_rate: float = 1e7) -> np.ndarray:
        """
        Calculate time-integrated singlet yield
        Based on Eq. 1.1.14
        """
        # Define singlet projector
        P_S = np.zeros((self.dim, self.dim))
        P_S[1, 1] = 0.5
        P_S[1, 2] = -0.5
        P_S[2, 1] = -0.5
        P_S[2, 2] = 0.5

        yields = []
        for state in states:
            # P_S(t) = ⟨S|ρ(t)|S⟩
            p_s = np.real(np.conj(state) @ P_S @ state)
            yields.append(p_s)

        # Time-integrated yield
        dt = time_points[1] - time_points[0]
        Phi_S = recombination_rate * np.sum(yields) * dt

        return np.array(yields), Phi_S


class MultiNuclearExperiment:
    """
    Experimental framework for multi-nuclear hyperfine studies
    """

    def __init__(self):
        self.nuclear_config = NuclearSpinConfig()
        self.hyperfine_analysis = HyperfineTensorAnalysis()

    def experiment_1_nuclear_scaling(self, max_nuclei: int = 10) -> Dict:
        """
        Experiment 1: Scale number of nuclei and measure coherence
        Based on Section 1.1.4 - Hilbert space dimension scaling
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 1: Nuclear Spin Scaling Analysis")
        print("=" * 60)

        dimensions = []
        coherence_times = []

        for n_nuclei in range(1, max_nuclei + 1):
            dim = 2 * (2 ** n_nuclei)
            dimensions.append(dim)

            # Estimate coherence time (decreases with more nuclei)
            # Based on Eq. 1.5.1 - environmental decoherence
            gamma_env = 1e6 * n_nuclei  # s^-1
            tau = 1 / gamma_env * 1e6  # μs
            coherence_times.append(tau)

            print(f"  n_nuclei = {n_nuclei:2d} | dim = {dim:6d} | τ_coh = {tau:.3f} μs")

        return {
            'nuclei_count': np.arange(1, max_nuclei + 1),
            'dimension': np.array(dimensions),
            'coherence_time': np.array(coherence_times)
        }

    def experiment_2_isotope_sensitivity(self) -> Dict:
        """
        Experiment 2: Test 13C vs 12C sensitivity
        Based on Section 1.1.4 - 13C natural abundance effects
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 2: Isotope Substitution Sensitivity")
        print("=" * 60)

        results = {}

        # Natural abundance mixture
        results['13C_abundance'] = 1.07  # percent

        # Hyperfine coupling comparison
        A_13C = 2e-3  # Tesla (typical)
        A_12C = 0  # 12C has no magnetic moment

        results['A_13C'] = A_13C
        results['A_12C'] = A_12C

        # Effect on Hilbert space
        dim_13C = 4 * 2  # With one 13C
        dim_12C = 4 * 1  # Without (12C acts as spectator)

        results['dim_with_13C'] = dim_13C
        results['dim_without_13C'] = dim_12C

        # Navigation signal difference
        signal_ratio = A_13C / (A_13C + 1e-6)  # Normalized
        results['signal_enhancement'] = signal_ratio

        print(f"  13C abundance: {results['13C_abundance']}%")
        print(f"  A_13C = {A_13C*1000:.1f} mT, A_12C = {A_12C*1000:.1f} mT")
        print(f"  Hilbert space dim: {dim_12C} → {dim_13C}")
        print(f"  Signal enhancement: {signal_ratio:.2f}x")

        return results

    def experiment_3_nitrogen_quadrupole(self) -> Dict:
        """
        Experiment 3: 14N quadrupole effects
        Based on Section 1.1.4 - 14N I=1 nucleus
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 3: 14N Quadrupole Coupling Effects")
        print("=" * 60)

        results = {}

        # 14N has I=1, so 3 nuclear spin states
        results['I_14N'] = 1.0
        results['nuclear_states'] = 3  # m_I = -1, 0, +1

        # Quadrupole coupling (typical)
        e2qQ = 5e6  # Hz
        results['quadrupole_coupling'] = e2qQ

        # Energy splitting
        delta_E = HBAR * 2 * np.pi * e2qQ
        results['delta_E_quad'] = delta_E

        # Compare to hyperfine
        A_14N = 1e-3  # Tesla
        mu_B = 9.274e-24
        g_N = 0.404
        delta_E_hf = g_N * mu_B * A_14N / HBAR / (2 * np.pi)

        results['delta_E_hyperfine'] = delta_E_hf
        results['ratio_quad_hf'] = e2qQ / delta_E_hf

        print(f"  Nuclear spin I = {results['I_14N']}")
        print(f"  Nuclear spin states: {results['nuclear_states']}")
        print(f"  Quadrupole coupling: {e2qQ/1e6:.1f} MHz")
        print(f"  Hyperfine splitting: {delta_E_hf/1e6:.1f} MHz")
        print(f"  Quad/HF ratio: {results['ratio_quad_hf']:.2f}")

        return results

    def experiment_4_hyperfine_anisotropy_scan(self) -> Dict:
        """
        Experiment 4: Angular dependence of hyperfine couplings
        Based on Section 1.1.4 and 1.2.2
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 4: Hyperfine Anisotropy Angular Scan")
        print("=" * 60)

        angles = np.linspace(0, 2 * np.pi, 180)
        signals = {nuc: np.zeros(len(angles)) for nuc in ['1H', '14N', '13C', '31P']}

        for idx, theta in enumerate(angles):
            for nuc in ['1H', '14N', '13C', '31P']:
                if nuc in self.nuclear_config.nuclei:
                    A_range = self.nuclear_config.nuclei[nuc]['A_range']
                    A_iso = np.mean(A_range)

                    # Anisotropic contribution varies with angle
                    # Based on Eq. 1.1.12-1.1.13
                    A_aniso = 0.1 * A_iso * (3 * np.cos(theta)**2 - 1)
                    signals[nuc][idx] = A_iso + A_aniso

        return {'angles': angles, **signals}

    def experiment_5_decoherence_bath(self) -> Dict:
        """
        Experiment 5: Nuclear spin bath decoherence
        Based on Section 1.5.2 - Spectral Density Approach
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 5: Nuclear Spin Bath Decoherence Analysis")
        print("=" * 60)

        results = {}

        # Bath parameters
        n_bath = 50  # Number of bath spins
        lambda_c = 1e10  # Coupling strength (Hz)
        gamma_c = 1e9  # Cutoff frequency (Hz)

        # Spectral density (Drude-Lorentz, Eq. 1.5.11)
        omega = np.logspace(6, 12, 100)  # 1 MHz to 1 THz
        J = lambda_c**2 * omega / ((omega**2 + gamma_c**2))

        # Decoherence rate
        beta = 1 / (KB * 300)  # Inverse thermal energy
        coth_term = 1 / np.tanh(HBAR * omega * beta / 2)

        # Total decoherence rate (Eq. 1.5.10)
        inv_tau = np.trapz(J * coth_term, omega)

        results['spectral_density'] = {'omega': omega, 'J': J}
        results['decoherence_rate'] = inv_tau
        results['coherence_time'] = 1 / inv_tau * 1e6 if inv_tau > 0 else np.inf  # μs

        print(f"  Bath spins: {n_bath}")
        results['n_bath'] = n_bath

        print(f"  Decoherence rate: {inv_tau:.2e} s⁻¹")
        print(f"  Coherence time: {results['coherence_time']:.2f} μs")

        return results

    def experiment_6_protein_protection(self) -> Dict:
        """
        Experiment 6: Protein-mediated coherence protection
        Based on Section 1.5.3 - Protein-Mediated Protection
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 6: Protein-Mediated Coherence Enhancement")
        print("=" * 60)

        results = {}

        # Vacuum coherence time
        tau_vacuum = 40e-15  # 40 fs (thermal limit)

        # Protein protection factor (Eq. 1.5.17)
        # F_protection ~ 10^3 - 10^6
        protection_factors = [1e3, 1e4, 1e5, 1e6]
        enhanced_times = [tau_vacuum * pf for pf in protection_factors]

        results['tau_vacuum'] = tau_vacuum * 1e6  # μs
        results['protection_factors'] = protection_factors
        results['enhanced_times'] = np.array(enhanced_times) * 1e6  # μs

        print(f"  Vacuum coherence time: {tau_vacuum*1e12:.0f} fs")
        print(f"  Protection factors: {protection_factors}")
        print(f"  Enhanced times: {np.array(enhanced_times) * 1e6:.1f} μs")

        # Theoretical enhancement
        # Based on protein rigidity and spin density
        protein_density = 1.35  # g/cm³
        spin_density = 1e19  # spins/cm³
        protection_calc = np.exp(-protein_density * spin_density * 1e-23)

        results['theoretical_protection'] = protection_calc

        return results


# Global constant
HBAR = 1.0545718e-34
KB = 1.380649e-23


def run_multinuclear_experiments():
    """
    Run all multi-nuclear hyperfine experiments
    """
    print("\n" + "=" * 70)
    print("MULTI-NUCLEAR HYPERFINE COUPLING EXPERIMENTS")
    print("=" * 70)

    experiment = MultiNuclearExperiment()
    all_results = {}

    # Run all experiments
    all_results['nuclear_scaling'] = experiment.experiment_1_nuclear_scaling()
    all_results['isotope_sensitivity'] = experiment.experiment_2_isotope_sensitivity()
    all_results['nitrogen_quadrupole'] = experiment.experiment_3_nitrogen_quadrupole()
    all_results['anisotropy_scan'] = experiment.experiment_4_hyperfine_anisotropy_scan()
    all_results['decoherence_bath'] = experiment.experiment_5_decoherence_bath()
    all_results['protein_protection'] = experiment.experiment_6_protein_protection()

    print("\n" + "=" * 70)
    print("ALL MULTI-NUCLEAR EXPERIMENTS COMPLETED")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    results = run_multinuclear_experiments()

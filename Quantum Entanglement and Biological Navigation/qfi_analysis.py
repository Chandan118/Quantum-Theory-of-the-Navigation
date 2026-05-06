#!/usr/bin/env python3
"""
Quantum Fisher Information and Sensing Precision Experiments
============================================================
Based on: Section 2.1 - Quantum Fisher Information Navigation Precision

This module implements comprehensive experiments for:
- Quantum Fisher Information (QFI) calculation
- Cramér-Rao bounds on angle estimation
- Multi-parameter estimation (angle, inclination, declination)
- Sensitivity limits and optimization
- Quantum-enhanced sensing protocols

Author: Quantum Computing Research Team
Date: 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import eigvalsh, sqrtm
from scipy.optimize import minimize, brentq
from scipy.special import psi
from typing import Dict, List, Tuple, Callable, Optional
import warnings
warnings.filterwarnings('ignore')


# Physical Constants
HBAR = 1.0545718e-34  # J·s
KB = 1.380649e-23     # J/K
MU_BOHR = 9.2740100783e-24  # J/T
G_ELECTRON = 2.0023
TEMP = 300  # K
B_EARTH = 50e-6  # T


class QuantumFisherInformationCalculator:
    """
    Calculate Quantum Fisher Information for radical pair compass
    Based on Section 2.1 - Complete QFI Formulation
    """

    def __init__(self):
        self.physical_time = True

    def symmetric_logarithmic_derivative(self, rho: np.ndarray,
                                        theta: float) -> np.ndarray:
        """
        Calculate symmetric logarithmic derivative (SLD)
        Based on Eq. 2.1.3

        L_θ satisfies: ∂_θ ρ = (L_θ ρ + ρ L_θ) / 2
        """
        # Get eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(rho)

        L_theta = np.zeros_like(rho)

        n = len(eigenvalues)
        for m in range(n):
            for n_idx in range(n):
                if eigenvalues[m] + eigenvalues[n_idx] > 1e-12:
                    # Matrix elements of ∂_θ ρ
                    drho = self.compute_density_derivative(rho, theta)
                    drho_mn = np.vdot(eigenvectors[:, m], drho @ eigenvectors[:, n_idx])

                    L_theta_mn = 2 * drho_mn / (eigenvalues[m] + eigenvalues[n_idx])

                    L_theta += L_theta_mn * np.outer(eigenvectors[:, m],
                                                     eigenvectors[:, n_idx].conj())

        return L_theta

    def compute_density_derivative(self, rho: np.ndarray, theta: float) -> np.ndarray:
        """
        Compute derivative of density matrix with respect to parameter
        """
        # For compass angle parameter
        # ∂_θ H = g μ_B B * (-sin θ S_x + cos θ S_y)

        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)

        # Derivative of Hamiltonian
        dH = -G_ELECTRON * MU_BOHR * B_EARTH * (
            -np.sin(theta) * np.kron(sigma_x, np.eye(2)) +
            np.cos(theta) * np.kron(sigma_y, np.eye(2))
        )

        # Heisenberg equation
        d_rho = -1j / HBAR * (dH @ rho - rho @ dH)

        return d_rho

    def qfi_pure_state(self, psi: np.ndarray,
                       generator: np.ndarray) -> float:
        """
        QFI for pure state
        Based on Eq. 2.1.21

        F_Q = 4(⟨∂_θψ|∂_θψ⟩ - |⟨ψ|∂_θψ⟩|²)
            = 4 Var(G)
        """
        # Expectation values
        mean_G = np.vdot(psi, generator @ psi)
        mean_G2 = np.vdot(psi, generator @ generator @ psi)

        variance = np.real(mean_G2 - mean_G**2)

        F_Q = 4 * variance

        return np.maximum(0, F_Q)

    def qfi_mixed_state(self, rho: np.ndarray,
                        theta: float) -> float:
        """
        QFI for mixed state
        Based on Eq. 2.1.20

        F_Q = 2 Σ_{m,n: λm+λn>0} |⟨m|∂_θ ρ|n⟩|² / (λ_m + λ_n)
        """
        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(rho)

        # Compute derivative
        drho = self.compute_density_derivative(rho, theta)

        F_Q = 0
        n = len(eigenvalues)

        for m in range(n):
            for n_idx in range(n):
                if eigenvalues[m] + eigenvalues[n_idx] > 1e-12:
                    drho_mn = np.vdot(eigenvectors[:, m], drho @ eigenvectors[:, n_idx])
                    F_Q += 2 * np.abs(drho_mn)**2 / (eigenvalues[m] + eigenvalues[n_idx])

        return np.real(F_Q)

    def qfi_angle_specific(self, rho: np.ndarray,
                          theta_nav: float) -> float:
        """
        Navigation-specific QFI for compass angle
        Based on Section 2.1.1 - Navigation-Specific QFI
        """
        # Generator for angle rotation
        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)

        # ∂H/∂θ
        dH_dtheta = G_ELECTRON * MU_BOHR * B_EARTH * (
            np.cos(theta_nav) * np.kron(sigma_x, np.eye(2)) +
            np.sin(theta_nav) * np.kron(sigma_y, np.eye(2))
        )

        # Simplified QFI (Eq. 2.1.26)
        # F_Q = 4(ΔE/ℏ)² for two-level system
        Delta_E = G_ELECTRON * MU_BOHR * B_EARTH
        F_Q = 4 * (Delta_E / HBAR)**2

        return F_Q

    def multiparameter_qfi_matrix(self, rho: np.ndarray,
                                  params: List[str]) -> np.ndarray:
        """
        Calculate QFI matrix for multiple parameters
        Based on Section 2.1.2 - Multi-Parameter Estimation

        F_ij = Tr[ρ {L_i, L_j} / 2]
        """
        n_params = len(params)
        F_matrix = np.zeros((n_params, n_params))

        # Get eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(rho)

        generators = {
            'theta': self._angle_generator(),
            'phi': self._azimuth_generator(),
            'B': self._field_strength_generator(),
            'I': self._inclination_generator(),
            'D': self._declination_generator()
        }

        L_operators = {}
        for param in params:
            if param in generators:
                L_operators[param] = self._compute_L_operator(
                    rho, generators[param], eigenvalues, eigenvectors
                )

        # Compute matrix elements
        for i, param_i in enumerate(params):
            for j, param_j in enumerate(params):
                if param_i in L_operators and param_j in L_operators:
                    L_i = L_operators[param_i]
                    L_j = L_operators[param_j]

                    # Tr[ρ {L_i, L_j}]
                    anticommutator = L_i @ L_j + L_j @ L_i
                    F_matrix[i, j] = np.real(np.trace(rho @ anticommutator) / 2)

        return F_matrix

    def _compute_L_operator(self, rho: np.ndarray,
                           generator: np.ndarray,
                           eigenvalues: np.ndarray,
                           eigenvectors: np.ndarray) -> np.ndarray:
        """Compute SLD operator for generator"""
        L = np.zeros_like(rho)

        for m in range(len(eigenvalues)):
            for n in range(len(eigenvalues)):
                if eigenvalues[m] + eigenvalues[n] > 1e-12:
                    g_mn = np.vdot(eigenvectors[:, m], generator @ eigenvectors[:, n])
                    L_mn = 2 * g_mn / (eigenvalues[m] + eigenvalues[n])
                    L += L_mn * np.outer(eigenvectors[:, m], eigenvectors[:, n].conj())

        return L

    def _angle_generator(self) -> np.ndarray:
        """Generator for compass angle rotation"""
        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        return G_ELECTRON * MU_BOHR * B_EARTH * np.kron(sigma_x, np.eye(2))

    def _azimuth_generator(self) -> np.ndarray:
        """Generator for azimuthal angle"""
        sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        return G_ELECTRON * MU_BOHR * B_EARTH * np.kron(sigma_y, np.eye(2))

    def _field_strength_generator(self) -> np.ndarray:
        """Generator for magnetic field strength"""
        sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        return G_ELECTRON * MU_BOHR * np.kron(sigma_z, np.eye(2))

    def _inclination_generator(self) -> np.ndarray:
        """Generator for inclination angle"""
        # Similar to angle generator
        return self._angle_generator() * 0.5

    def _declination_generator(self) -> np.ndarray:
        """Generator for declination angle"""
        return self._azimuth_generator() * 0.5


class CramerRaoBounds:
    """
    Calculate Cramér-Rao bounds for compass sensing
    Based on Section 2.1 - Fundamental Sensitivity Limits
    """

    def __init__(self):
        self.qfi_calc = QuantumFisherInformationCalculator()

    def classical_crb(self, F_I: float, N: int) -> float:
        """
        Classical Cramér-Rao bound (Standard Quantum Limit)
        Based on Eq. 2.1.12

        σ_θ ≥ 1/√(N F_I)
        """
        return 1 / np.sqrt(N * F_I)

    def quantum_crb(self, F_Q: float, N: int) -> float:
        """
        Quantum Cramér-Rao bound (Heisenberg limit)
        Based on Eq. 2.1.14

        σ_θ ≥ 1/(N √F_Q)
        """
        return 1 / (N * np.sqrt(F_Q))

    def angular_resolution(self, signal: float,
                          noise_std: float,
                          snr: float = None) -> float:
        """
        Calculate minimum detectable angular deviation
        Based on Eq. 2.1.28

        δθ ≈ √(2/ SNR) = √(2 σ²_noise / Signal²)
        """
        if snr is None:
            snr = signal / noise_std

        delta_theta = np.sqrt(2 / snr)

        return delta_theta

    def compass_sensitivity(self, B_field: float,
                          n_photons: int,
                          alpha: float = 1e-6) -> Dict[str, float]:
        """
        Calculate compass sensitivity limits
        Based on Section 2.1.2
        """
        # Minimum detectable field (Eq. 2.2.24)
        sigma_noise = np.sqrt(n_photons)  # Shot noise
        B_min = sigma_noise / (B_field**2) * alpha

        # Minimum detectable angle (Eq. 2.1.70)
        Delta_E = G_ELECTRON * MU_BOHR * B_field
        F_Q = 4 * (Delta_E / HBAR)**2

        delta_theta = 1 / np.sqrt(n_photons * F_Q)
        delta_theta_degrees = np.degrees(delta_theta)

        return {
            'B_min': B_min,
            'delta_theta_rad': delta_theta,
            'delta_theta_deg': delta_theta_degrees,
            'F_Q': F_Q
        }


class OptimalProbeStates:
    """
    Find and analyze optimal probe states for compass
    Based on Section 2.1.1 - Optimal probe state
    """

    def __init__(self):
        self.qfi_calc = QuantumFisherInformationCalculator()

    def maximally_entangled_probe(self) -> np.ndarray:
        """
        Create maximally entangled probe state
        Based on Section 2.1.1 - Optimal probe state

        |ψ_opt⟩ = (|+⟩|+⟩ + |-⟩|-⟩)/√2
        """
        plus = np.array([1, 1]) / np.sqrt(2)  # |+⟩ state
        minus = np.array([1, -1]) / np.sqrt(2)  # |-⟩ state

        # Bell-like state
        psi = np.zeros(4, dtype=complex)
        psi[0] = 1 / np.sqrt(2)  # |++⟩
        psi[3] = 1 / np.sqrt(2)  # |--⟩

        return psi

    def coherent_spin_state(self, theta: float,
                          phi: float) -> np.ndarray:
        """
        Create coherent spin state on Bloch sphere
        """
        # Spin-1/2 coherent state
        alpha = np.cos(theta/2)
        beta = np.exp(1j * phi) * np.sin(theta/2)

        return np.array([alpha, beta])

    def nooN_state(self, N: int) -> np.ndarray:
        """
        Create N00N state for quantum enhanced sensing
        |ψ_N00N⟩ = (|N,0⟩ + |0,N⟩)/√2
        """
        dim = 2**N
        psi = np.zeros(dim, dtype=complex)
        psi[0] = 1 / np.sqrt(2)  # |00...0⟩
        psi[-1] = 1 / np.sqrt(2)  # |11...1⟩

        return psi

    def entanglement_advantage(self, N: int) -> Dict[str, float]:
        """
        Calculate quantum advantage from entanglement
        Based on Section 2.1.1 - Heisenberg scaling
        """
        # SQL: F ~ N
        F_SQL = N

        # HSL: F ~ N²
        F_HSL = N**2

        advantage = F_HSL / F_SQL

        return {
            'N': N,
            'F_SQL': F_SQL,
            'F_HSL': F_HSL,
            'advantage_factor': advantage
        }


class SensingProtocols:
    """
    Implement quantum sensing protocols for compass
    Based on Section 2.1.3 - QFI for Magnetic Field Sensing Chain
    """

    def __init__(self):
        self.qfi_calc = QuantumFisherInformationCalculator()
        self.crb = CramerRaoBounds()
        self.optimal_states = OptimalProbeStates()

    def naive_sensing(self, n_measurements: int,
                     B_field: float) -> Dict[str, float]:
        """
        Naive classical sensing without entanglement
        """
        Delta_E = G_ELECTRON * MU_BOHR * B_field
        F_Q_single = 4 * (Delta_E / HBAR)**2

        # Standard quantum limit
        delta_theta = 1 / np.sqrt(n_measurements * F_Q_single)

        return {
            'protocol': 'naive',
            'delta_theta': delta_theta,
            'delta_theta_deg': np.degrees(delta_theta),
            'F_Q': F_Q_single
        }

    def entangled_sensing(self, n_pairs: int,
                          n_measurements: int,
                          B_field: float) -> Dict[str, float]:
        """
        Quantum sensing with entangled radical pairs
        Based on Section 2.1.1 - Heisenberg scaling
        """
        Delta_E = G_ELECTRON * MU_BOHR * B_field
        F_Q_single = 4 * (Delta_E / HBAR)**2

        # Heisenberg scaling: F_Q ~ N²
        F_Q_entangled = n_pairs**2 * F_Q_single

        delta_theta = 1 / (n_measurements * np.sqrt(F_Q_entangled))

        return {
            'protocol': 'entangled',
            'delta_theta': delta_theta,
            'delta_theta_deg': np.degrees(delta_theta),
            'F_Q': F_Q_entangled,
            'N_pairs': n_pairs
        }

    def ghz_sensing(self, n_qubits: int,
                   B_field: float) -> Dict[str, float]:
        """
        GHZ state sensing protocol
        """
        Delta_E = G_ELECTRON * MU_BOHR * B_field

        # GHZ gives quadratic enhancement
        F_Q_ghz = (n_qubits * Delta_E / HBAR)**2

        delta_theta = 1 / np.sqrt(F_Q_ghz)

        return {
            'protocol': 'GHZ',
            'delta_theta': delta_theta,
            'delta_theta_deg': np.degrees(delta_theta),
            'F_Q': F_Q_ghz,
            'n_qubits': n_qubits
        }

    def adaptive_sensing(self, time_points: np.ndarray,
                       B_field: float,
                       gamma: float) -> Dict[str, np.ndarray]:
        """
        Adaptive sensing with optimal timing
        Based on sensing protocol optimization
        """
        Delta_E = G_ELECTRON * MU_BOHR * B_field

        # QFI accumulation over time
        F_Q_t = 4 * (Delta_E / HBAR)**2 * (1 - np.exp(-gamma * time_points))

        # Optimal measurement time
        optimal_idx = np.argmax(F_Q_t)
        t_optimal = time_points[optimal_idx]

        return {
            'time': time_points,
            'F_Q_t': F_Q_t,
            't_optimal': t_optimal,
            'F_Q_max': F_Q_t[optimal_idx]
        }


class QFIExperimentFramework:
    """
    Main experimental framework for QFI and sensing precision
    """

    def __init__(self):
        self.qfi_calc = QuantumFisherInformationCalculator()
        self.crb = CramerRaoBounds()
        self.optimal_states = OptimalProbeStates()
        self.sensing = SensingProtocols()

    def experiment_1_qfi_scaling(self) -> Dict:
        """
        Experiment 1: QFI scaling with resources
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 1: Quantum Fisher Information Scaling")
        print("=" * 60)

        results = {}

        # Resource scaling
        n_resources = np.arange(1, 101)

        # Classical SQL
        F_SQL = n_resources

        # Quantum HSL (with entanglement)
        F_HSL = n_resources**2

        # Practical entangled scaling
        alpha = 0.5  # Decoherence factor
        F_practical = alpha * n_resources**2

        results['N'] = n_resources
        results['F_SQL'] = F_SQL
        results['F_HSL'] = F_HSL
        results['F_practical'] = F_practical

        print(f"  Classical SQL: F ∝ N")
        print(f"  Quantum HSL: F ∝ N²")
        print(f"  Practical: F ∝ αN² (α = {alpha})")
        print(f"  At N=100: SQL={F_SQL[-1]}, HSL={F_HSL[-1]}, Practical={F_practical[-1]:.0f}")

        return results

    def experiment_2_angle_precision(self) -> Dict:
        """
        Experiment 2: Minimum detectable angle
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 2: Compass Angle Precision")
        print("=" * 60)

        results = {}

        # Different field strengths
        B_fields = np.array([25, 50, 65]) * 1e-6  # μT

        # Number of measurements
        n_meas = 1e6  # Typical photon count

        Delta_theta = []

        for B in B_fields:
            Delta_E = G_ELECTRON * MU_BOHR * B
            F_Q = 4 * (Delta_E / HBAR)**2

            delta_theta = 1 / np.sqrt(n_meas * F_Q)
            Delta_theta.append(delta_theta)

        results['B_field_uT'] = B_fields * 1e6
        results['delta_theta_rad'] = np.array(Delta_theta)
        results['delta_theta_deg'] = np.degrees(np.array(Delta_theta))

        print(f"  Number of measurements: N = {n_meas:.0e}")
        print(f"  Magnetic field range: {B_fields[0]*1e6:.0f} - {B_fields[-1]*1e6:.0f} μT")
        print(f"  Angle precision: {np.degrees(Delta_theta[0]):.2f}° - {np.degrees(Delta_theta[-1]):.2f}°")

        return results

    def experiment_3_multiparameter(self) -> Dict:
        """
        Experiment 3: Multi-parameter estimation
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 3: Multi-Parameter Estimation")
        print("=" * 60)

        results = {}

        # Create test density matrix
        rho = np.zeros((4, 4), dtype=complex)
        rho[0, 0] = 0.25
        rho[1, 1] = 0.25
        rho[2, 2] = 0.25
        rho[3, 3] = 0.25
        rho[0, 1] = 0.1
        rho[1, 0] = 0.1

        # QFI matrix
        params = ['theta', 'B', 'I']
        F_matrix = self.qfi_calc.multiparameter_qfi_matrix(rho, params)

        results['F_matrix'] = F_matrix
        results['parameters'] = params

        # Incompatibility measure
        det_F = np.linalg.det(F_matrix)
        results['det_F'] = det_F

        print(f"  Parameters: {params}")
        print(f"  QFI Matrix:")
        for i, row in enumerate(F_matrix):
            print(f"    {params[i]}: {row}")

        print(f"  Determinant: {det_F:.2e}")
        print(f"  Incompatibility: {'Yes' if det_F < 1e-10 else 'No'}")

        return results

    def experiment_4_optimal_states(self) -> Dict:
        """
        Experiment 4: Compare optimal probe states
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 4: Optimal Probe States Comparison")
        print("=" * 60)

        results = {}

        Delta_E = G_ELECTRON * MU_BOHR * B_EARTH
        F_Q_single = 4 * (Delta_E / HBAR)**2

        # Compare different states
        states = {
            'separable': 'Product state',
            'entangled': 'Max entangled',
            'GHZ_4': '4-qubit GHZ',
            'NOON_4': '4-qubit NOON'
        }

        F_Q_values = {
            'separable': F_Q_single,
            'entangled': 4 * F_Q_single,  # 2x enhancement
            'GHZ_4': 16 * F_Q_single,    # N² enhancement
            'NOON_4': 16 * F_Q_single    # N² enhancement
        }

        results['states'] = states
        results['F_Q'] = F_Q_values

        print(f"  State Type | QFI Enhancement | F_Q (rad/s)⁻²")
        print(f"  " + "-" * 50)
        for state, F_Q in F_Q_values.items():
            enhancement = F_Q / F_Q_single
            print(f"  {state:12s} | {enhancement:16.1f}x | {F_Q:.2e}")

        return results

    def experiment_5_sensing_chain(self) -> Dict:
        """
        Experiment 5: Full sensing chain efficiency
        Based on Section 2.1.3 - QFI for Magnetic Field Sensing Chain
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 5: Sensing Chain Efficiency")
        print("=" * 60)

        results = {}

        # Quantum limit
        Delta_E = G_ELECTRON * MU_BOHR * B_EARTH
        F_Q_quantum = 4 * (Delta_E / HBAR)**2

        # Efficiency factors
        eta_transduction = 0.3     # Protein conformational coupling
        eta_neural = 0.5          # Neural encoding efficiency
        eta_total = eta_transduction * eta_neural

        # Total F_Q through chain
        F_Q_total = F_Q_quantum * eta_total

        # Bottleneck analysis
        bottlenecks = {
            'quantum': F_Q_quantum,
            'transduction': F_Q_quantum * eta_transduction,
            'neural': F_Q_total,
            'total': F_Q_total
        }

        results['F_Q_quantum'] = F_Q_quantum
        results['F_Q_total'] = F_Q_total
        results['eta_total'] = eta_total
        results['bottlenecks'] = bottlenecks

        print(f"  Quantum F_Q: {F_Q_quantum:.2e} (rad/s)⁻²")
        print(f"  Transduction efficiency: η = {eta_transduction:.1f}")
        print(f"  Neural efficiency: η = {eta_neural:.1f}")
        print(f"  Total efficiency: η = {eta_total:.2f}")
        print(f"  Total F_Q: {F_Q_total:.2e} (rad/s)⁻²")

        return results

    def experiment_6_noise_sensitivity(self) -> Dict:
        """
        Experiment 6: Noise effects on sensing precision
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 6: Noise Sensitivity Analysis")
        print("=" * 60)

        results = {}

        # Noise levels
        gamma_dephasing = np.logspace(4, 9, 100)  # s⁻¹

        # QFI degradation
        Delta_E = G_ELECTRON * MU_BOHR * B_EARTH
        F_Q_0 = 4 * (Delta_E / HBAR)**2

        # Dephasing reduces QFI
        F_Q_noisy = F_Q_0 * np.exp(-gamma_dephasing / 1e8)

        # Minimum detectable angle
        n_meas = 1e6
        delta_theta_noisy = 1 / np.sqrt(n_meas * F_Q_noisy)

        results['gamma_dephasing'] = gamma_dephasing
        results['F_Q'] = F_Q_noisy
        results['delta_theta'] = delta_theta_noisy

        # Find threshold
        threshold_idx = np.argmin(np.abs(delta_theta_noisy - 0.1 * np.pi / 180))
        gamma_threshold = gamma_dephasing[threshold_idx]

        print(f"  Dephasing range: {gamma_dephasing[0]:.0e} - {gamma_dephasing[-1]:.0e} s⁻¹")
        print(f"  F_Q degradation: {F_Q_0:.2e} → {F_Q_noisy[-1]:.2e}")
        print(f"  θ precision: {np.degrees(delta_theta_noisy[0]):.4f}° → {np.degrees(delta_theta_noisy[-1]):.2f}°")
        print(f"  10% accuracy threshold: γ = {gamma_threshold:.2e} s⁻¹")

        return results


def run_qfi_experiments():
    """
    Run all QFI and sensing precision experiments
    """
    print("\n" + "=" * 70)
    print("QUANTUM FISHER INFORMATION EXPERIMENTS")
    print("=" * 70)

    experiment = QFIExperimentFramework()
    all_results = {}

    # Run all experiments
    all_results['qfi_scaling'] = experiment.experiment_1_qfi_scaling()
    all_results['angle_precision'] = experiment.experiment_2_angle_precision()
    all_results['multiparameter'] = experiment.experiment_3_multiparameter()
    all_results['optimal_states'] = experiment.experiment_4_optimal_states()
    all_results['sensing_chain'] = experiment.experiment_5_sensing_chain()
    all_results['noise_sensitivity'] = experiment.experiment_6_noise_sensitivity()

    print("\n" + "=" * 70)
    print("ALL QFI EXPERIMENTS COMPLETED")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    results = run_qfi_experiments()

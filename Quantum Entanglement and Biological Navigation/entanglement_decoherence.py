#!/usr/bin/env python3
"""
Entanglement and Decoherence Dynamics Experiments
==================================================
Based on: Section 1.6 - Entanglement Measures, Section 2.2 - Decoherence Dynamics

This module implements comprehensive experiments for:
- Entanglement creation and decay (concurrence, negativity)
- Decoherence mechanisms (environmental, thermal, protein)
- Quantum coherence measures (L1-norm, relative entropy)
- Quantum trajectory analysis
- Open quantum system dynamics

Author: Quantum Computing Research Team
Date: 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import expm, sqrtm, eigvalsh
from scipy.integrate import odeint, solve_ivp
from typing import Dict, List, Tuple, Callable
import warnings
warnings.filterwarnings('ignore')


# Physical Constants
HBAR = 1.0545718e-34  # J·s
KB = 1.380649e-23     # J/K
MU_BOHR = 9.2740100783e-24  # J/T
G_ELECTRON = 2.0023
TEMP = 300  # K


class EntanglementAnalyzer:
    """
    Analyze entanglement properties of radical pair system
    Based on Section 1.6 - Entanglement Measures
    """

    def __init__(self):
        self.physical_time = True

    def concurrence(self, rho: np.ndarray) -> float:
        """
        Calculate concurrence for two-qubit system
        Based on Eq. 1.6.5

        C(ρ) = max{0, √λ₁ - √λ₂ - √λ₃ - √λ₄}

        where λᵢ are eigenvalues of ρ ρ̃ in descending order
        """
        # Pauli y matrix
        sigma_y = np.array([[0, -1j], [1j, 0]])

        # Calculate ρ ρ̃
        rho_tilde = np.kron(sigma_y, sigma_y) @ rho.conj() @ np.kron(sigma_y, sigma_y)

        # Eigenvalues
        eigenvalues = eigvalsh(rho_tilde @ rho)
        eigenvalues = np.sort(eigenvalues)[::-1]  # Descending order

        # Concurrence
        sqrt_eigenvalues = np.sqrt(np.maximum(eigenvalues, 0))
        C = max(0, sqrt_eigenvalues[0] - sqrt_eigenvalues[1] -
                sqrt_eigenvalues[2] - sqrt_eigenvalues[3])

        return np.real(C)

    def negativity(self, rho: np.ndarray) -> float:
        """
        Calculate negativity based on partial transpose
        Based on Eq. 1.6.15

        N(ρ) = (||ρᵀᴸ||₁ - 1) / 2
        """
        dim = rho.shape[0]
        d = int(np.sqrt(dim))

        # Partial transpose (transpose first subsystem)
        rho_pt = rho.reshape(d, d, d, d).transpose(2, 3, 0, 1).reshape(dim, dim)

        # Trace norm
        eigenvalues = eigvalsh(rho_pt)
        trace_norm = np.sum(np.abs(eigenvalues))

        N = (trace_norm - 1) / 2
        return np.maximum(0, np.real(N))

    def entanglement_of_formation(self, C: float) -> float:
        """
        Calculate entanglement of formation from concurrence
        Based on Eq. 2.2.11
        """
        if C <= 0:
            return 0
        if C >= 1:
            C = 0.9999

        # Binary entropy function
        def h(x):
            return -x * np.log2(x) - (1-x) * np.log2(1-x)

        # Entanglement of formation
        E_f = h((1 + np.sqrt(1 - C**2)) / 2)
        return E_f

    def quantum_discord(self, rho: np.ndarray) -> float:
        """
        Calculate quantum discord
        Based on Section 2.2.2 - Quantum Correlations in Navigation
        """
        # For a 2-spin system (4x4 density matrix)
        # rho_A = Tr_B(rho), rho_B = Tr_A(rho)
        # Reshape to (2, 2, 2, 2) and trace over appropriate indices
        
        rho_reshaped = rho.reshape(2, 2, 2, 2)
        rho_A = np.trace(rho_reshaped, axis1=1, axis2=3)  # Trace over second qubit
        rho_B = np.trace(rho_reshaped, axis1=0, axis2=2)  # Trace over first qubit

        # Calculate entropies
        def entropy(rho):
            eigenvalues = eigvalsh(rho)
            eigenvalues = eigenvalues[eigenvalues > 1e-12]
            return -np.sum(eigenvalues * np.log2(eigenvalues))

        S_A = entropy(rho_A)
        S_B = entropy(rho_B)
        S_AB = entropy(rho)

        I_AB = S_A + S_B - S_AB

        # Classical correlations (simplified)
        CC = 0.5 * S_A

        D = I_AB - CC

        return max(0, D)

    def bell_inequality_test(self, rho: np.ndarray) -> Dict[str, float]:
        """
        Test CHSH Bell inequality
        Based on Section 1.6 - entanglement tests
        """
        # Simplified CHSH parameter
        # For pure Bell state, S = 2√2 ≈ 2.828
        # Classical bound: S ≤ 2

        # Estimate from density matrix
        # This is simplified - real calculation requires measurement settings

        eigenvalues = eigvalsh(rho)
        purity = np.sum(eigenvalues**2)

        # Maximal violation estimate
        S_max = 2 * np.sqrt(2 * purity)
        S_classical = 2.0

        return {
            'S_CHSH': S_max,
            'S_classical': S_classical,
            'violates_bell': S_max > S_classical,
            'margin': S_max - S_classical
        }


class DecoherenceMechanisms:
    """
    Model different decoherence mechanisms
    Based on Section 2.2 - Complete Decoherence Dynamics Analysis
    """

    def __init__(self):
        self.TEMP = TEMP

    def environmental_decoherence(self, B_noise: float = 1e-6,
                                  tau_corr: float = 1e-9) -> float:
        """
        Environmental decoherence rate
        Based on Section 2.2.1 - Environmental Decoherence

        Γ_env ≈ (γ²/ℏ²) ⟨B(0)B(t)⟩ τ_corr
        """
        gamma = G_ELECTRON * MU_BOHR / HBAR
        Gamma_env = (gamma * B_noise)**2 * tau_corr

        return Gamma_env

    def thermal_decoherence(self, V_coupling: float = 1e-23,
                           E_gap: float = 1e-21) -> float:
        """
        Thermal decoherence rate
        Based on Section 2.2.2 - Thermal Decoherence

        Γ_thermal ≈ (k_B T / ℏ) * (V_coupling / E_gap)²
        """
        Gamma_thermal = (KB * self.TEMP / HBAR) * (V_coupling / E_gap)**2

        return Gamma_thermal

    def protein_decoherence(self, omega_mode: float = 1e12) -> float:
        """
        Protein-mediated decoherence
        Based on Section 2.2.3 - Protein Matrix Effects

        Γ_protein ~ 10⁹ - 10¹² s⁻¹ at 300K
        """
        # Thermal occupation
        n_th = 1 / (np.exp(HBAR * omega_mode / (KB * self.TEMP)) - 1)

        # Coupling strength
        g = 1e-3 * HBAR * omega_mode  # 0.1-10 meV

        Gamma_protein = g**2 * (2 * n_th + 1) / HBAR**2

        return Gamma_protein

    def solvent_decoherence(self, lambda_solv: float = 1.0) -> float:
        """
        Solvent reorganization decoherence
        Based on Section 2.2.4 - Solvent Reorganization

        Γ_solvent = (2π/ℏ) λ_solv ρ_solv(E)

        λ_solv ~ 0.5 - 1.5 eV for proteins
        """
        lambda_eV = lambda_solv  # eV
        lambda_J = lambda_eV * 1.602e-19

        Gamma_solvent = (2 * np.pi / HBAR) * lambda_J * 0.5

        return Gamma_solvent

    def radical_recombination_decoherence(self, k_S: float = 1e8,
                                        k_T: float = 1e7,
                                        rho_S: float = 0.5,
                                        rho_T: float = 0.5) -> float:
        """
        Decoherence from radical recombination
        Based on Section 2.2.5 - Radical Recombination

        Γ_radical = k_S ρ_S + k_T ρ_T
        """
        Gamma_radical = k_S * rho_S + k_T * rho_T
        return Gamma_radical

    def total_decoherence_rate(self) -> Dict[str, float]:
        """
        Calculate total decoherence rate
        Based on Eq. 2.2.4

        Γ_total = Γ_env + Γ_thermal + Γ_protein + Γ_solvent + Γ_radical
        """
        rates = {}

        # Environmental
        rates['Gamma_env'] = self.environmental_decoherence()

        # Thermal
        rates['Gamma_thermal'] = self.thermal_decoherence()

        # Protein
        rates['Gamma_protein'] = self.protein_decoherence()

        # Solvent
        rates['Gamma_solvent'] = self.solvent_decoherence()

        # Radical recombination
        rates['Gamma_radical'] = self.radical_recombination_decoherence()

        # Total
        rates['Gamma_total'] = sum(rates.values())

        # Coherence times
        rates['tau_env'] = 1 / rates['Gamma_env'] if rates['Gamma_env'] > 0 else np.inf
        rates['tau_thermal'] = 1 / rates['Gamma_thermal'] if rates['Gamma_thermal'] > 0 else np.inf
        rates['tau_protein'] = 1 / rates['Gamma_protein'] if rates['Gamma_protein'] > 0 else np.inf
        rates['tau_solvent'] = 1 / rates['Gamma_solvent'] if rates['Gamma_solvent'] > 0 else np.inf
        rates['tau_radical'] = 1 / rates['Gamma_radical'] if rates['Gamma_radical'] > 0 else np.inf
        rates['tau_total'] = 1 / rates['Gamma_total'] if rates['Gamma_total'] > 0 else np.inf

        return rates


class CoherenceMeasures:
    """
    Calculate various quantum coherence measures
    Based on Section 2.4 - Coherence Measures
    """

    def __init__(self):
        self.physical_time = True

    def l1_norm_coherence(self, rho: np.ndarray) -> float:
        """
        L1-norm of coherence
        Based on Eq. 2.4.1-2.4.2

        C_l1(ρ) = Σ_{i≠j} |ρ_{ij}|
        """
        # Extract off-diagonal elements
        n = rho.shape[0]
        C = 0
        for i in range(n):
            for j in range(n):
                if i != j:
                    C += abs(rho[i, j])
        return np.real(C)

    def relative_entropy_coherence(self, rho: np.ndarray) -> float:
        """
        Relative entropy of coherence
        Based on Eq. 2.4.8

        C_rel(ρ) = S(ρ_diag) - S(ρ)
        """
        n = rho.shape[0]

        # Diagonal density matrix
        rho_diag = np.zeros((n, n))
        for i in range(n):
            rho_diag[i, i] = np.real(rho[i, i])

        # Von Neumann entropy
        def von_neumann_entropy(rho):
            eigenvalues = eigvalsh(rho)
            eigenvalues = eigenvalues[eigenvalues > 1e-12]
            return -np.sum(eigenvalues * np.log2(eigenvalues))

        S_diag = von_neumann_entropy(rho_diag)
        S = von_neumann_entropy(rho)

        C_rel = S_diag - S
        return np.maximum(0, np.real(C_rel))

    def robustness_coherence(self, rho: np.ndarray) -> float:
        """
        Robustness of coherence
        Alternative coherence measure
        """
        n = rho.shape[0]

        # Maximum mixing
        I = np.eye(n, dtype=complex) / n

        # Calculate robustness
        # R(ρ) = min{t ≥ 0 : (ρ + tσ)/(1+t) ∈ I}
        # Simplified: proportional to off-diagonal elements

        off_diag = np.sum(np.abs(rho - np.diag(np.diag(rho))))
        return np.real(off_diag / (1 + off_diag))

    def purity(self, rho: np.ndarray) -> float:
        """
        Purity of quantum state
        Based on Eq. 2.5.1

        P(ρ) = Tr(ρ²)
        """
        P = np.real(np.trace(rho @ rho))
        return np.clip(P, 0, 1)

    def linear_entropy(self, rho: np.ndarray) -> float:
        """
        Linear entropy
        Based on Eq. 2.5.3

        S_L(ρ) = 1 - Tr(ρ²)
        """
        return 1 - self.purity(rho)


class QuantumTrajectoryAnalyzer:
    """
    Quantum trajectory and stochastic Schrödinger equation analysis
    Based on Section 2.2 - Quantum Trajectory Theory
    """

    def __init__(self):
        self.physical_time = True

    def stochastic_schrodinger_equation(self, H_eff: np.ndarray,
                                       L: np.ndarray,
                                       initial_state: np.ndarray,
                                       time_points: np.ndarray,
                                       n_trajectories: int = 100) -> Dict:
        """
        Solve stochastic Schrödinger equation for quantum trajectories
        Based on Eq. 2.2.1 - SSE (Itô form)

        d|ψ⟩ = -i/ℏ H_eff dt + Σ(L - ⟨L⟩)dW_s |ψ⟩dt
        """
        trajectories = []
        jump_times = []
        jump_counts = []

        for traj in range(n_trajectories):
            state = initial_state.copy()
            traj_states = [state]
            jumps = 0
            t_jump = []

            for i in range(1, len(time_points)):
                dt = time_points[i] - time_points[i-1]

                # Non-Hermitian effective Hamiltonian
                H_nh = H_eff - 1j * HBAR * sum(L_k.conj().T @ L_k for L_k in L) / 2

                # Deterministic evolution
                U = expm(-1j * H_nh * dt / HBAR)
                state = U @ state

                # Jump probability
                dp = dt * sum(np.real(np.conj(state) @ L_k.conj().T @ L_k @ state)
                             for L_k in L)

                # Apply jump if needed
                if np.random.random() < dp:
                    # Choose jump operator
                    probs = [np.real(np.conj(state) @ L_k.conj().T @ L_k @ state)
                            for L_k in L]
                    probs = np.array(probs) / sum(probs)

                    idx = np.random.choice(len(L), p=probs)
                    state = L[idx] @ state / np.linalg.norm(L[idx] @ state)
                    jumps += 1
                    t_jump.append(time_points[i])

                traj_states.append(state)

            trajectories.append(np.array(traj_states))
            jump_times.append(t_jump)
            jump_counts.append(jumps)

        return {
            'trajectories': trajectories,
            'jump_times': jump_times,
            'jump_counts': np.array(jump_counts),
            'time': time_points
        }

    def ensemble_average(self, trajectories: List[np.ndarray]) -> np.ndarray:
        """
        Calculate ensemble average density matrix
        Based on Eq. 2.2.7
        """
        n_times = len(trajectories[0])
        n_states = len(trajectories[0][0])
        rho_avg = np.zeros((n_times, n_states, n_states), dtype=complex)

        for traj in trajectories:
            for t in range(n_times):
                rho_avg[t] += np.outer(traj[t], traj[t].conj())

        rho_avg /= len(trajectories)
        return rho_avg


class EntanglementDecoherenceExperiment:
    """
    Main experimental framework combining entanglement and decoherence
    """

    def __init__(self):
        self.entanglement = EntanglementAnalyzer()
        self.decoherence = DecoherenceMechanisms()
        self.coherence = CoherenceMeasures()
        self.trajectory = QuantumTrajectoryAnalyzer()

    def experiment_1_entanglement_creation(self) -> Dict:
        """
        Experiment 1: Create and track entanglement in radical pair
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 1: Entanglement Creation and Decay")
        print("=" * 60)

        results = {}

        # Time range (microseconds)
        time_range = np.linspace(0, 100, 1000) * 1e-6

        # Initial singlet state (maximally entangled)
        rho_0 = np.zeros((4, 4), dtype=complex)
        rho_0[1, 1] = 0.5
        rho_0[1, 2] = -0.5
        rho_0[2, 1] = -0.5
        rho_0[2, 2] = 0.5

        # Decoherence rates
        rates = self.decoherence.total_decoherence_rate()
        gamma_ent = 2 * rates['Gamma_env'] + rates['Gamma_radical']

        # Entanglement dynamics (Eq. 1.6.10)
        C_0 = 1.0  # Initial concurrence
        concurrence = C_0 * np.exp(-gamma_ent * time_range)
        negativity = 0.5 * (concurrence - 1) * (concurrence > 0).astype(float)
        negativity = np.maximum(0, negativity)

        # Entanglement of formation
        E_f = np.array([self.entanglement.entanglement_of_formation(c)
                        for c in concurrence])

        results['time'] = time_range * 1e6  # μs
        results['concurrence'] = concurrence
        results['negativity'] = negativity
        results['E_f'] = E_f

        print(f"  Initial entanglement: C = {C_0:.3f}")
        print(f"  Decoherence rate: γ = {gamma_ent:.2e} s⁻¹")
        print(f"  Lifetime: τ = {1/gamma_ent*1e6:.2f} μs")
        print(f"  Final concurrence: C = {concurrence[-1]:.4f}")

        return results

    def experiment_2_decoherence_channel(self) -> Dict:
        """
        Experiment 2: Different decoherence channels
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 2: Decoherence Channel Comparison")
        print("=" * 60)

        results = {}

        # Calculate all decoherence rates
        rates = self.decoherence.total_decoherence_rate()
        results['rates'] = rates

        print("  Decoherence Rates:")
        print(f"    Γ_env    = {rates['Gamma_env']:.2e} s⁻¹  (τ = {rates['tau_env']*1e6:.2f} μs)")
        print(f"    Γ_thermal= {rates['Gamma_thermal']:.2e} s⁻¹  (τ = {rates['tau_thermal']*1e6:.2f} μs)")
        print(f"    Γ_protein = {rates['Gamma_protein']:.2e} s⁻¹  (τ = {rates['tau_protein']*1e9:.2f} ns)")
        print(f"    Γ_solvent = {rates['Gamma_solvent']:.2e} s⁻¹  (τ = {rates['tau_solvent']*1e9:.2f} ns)")
        print(f"    Γ_radical = {rates['Gamma_radical']:.2e} s⁻¹  (τ = {rates['tau_radical']*1e6:.2f} μs)")
        print(f"    ─────────────────────────────────────")
        print(f"    Γ_total  = {rates['Gamma_total']:.2e} s⁻¹  (τ = {rates['tau_total']*1e6:.2f} μs)")

        return results

    def experiment_3_coherence_measures(self) -> Dict:
        """
        Experiment 3: Compare coherence measures
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 3: Coherence Measures Comparison")
        print("=" * 60)

        results = {}

        # Initial coherent state
        rho_coherent = np.zeros((4, 4), dtype=complex)
        rho_coherent[0, 0] = 0.25
        rho_coherent[1, 1] = 0.25
        rho_coherent[2, 2] = 0.25
        rho_coherent[3, 3] = 0.25
        rho_coherent[0, 1] = 0.2
        rho_coherent[1, 0] = 0.2

        # Mixed state
        rho_mixed = np.eye(4, dtype=complex) / 4

        # Calculate measures
        measures_coherent = {
            'l1_norm': self.coherence.l1_norm_coherence(rho_coherent),
            'rel_entropy': self.coherence.relative_entropy_coherence(rho_coherent),
            'purity': self.coherence.purity(rho_coherent),
            'linear_entropy': self.coherence.linear_entropy(rho_coherent)
        }

        measures_mixed = {
            'l1_norm': self.coherence.l1_norm_coherence(rho_mixed),
            'rel_entropy': self.coherence.relative_entropy_coherence(rho_mixed),
            'purity': self.coherence.purity(rho_mixed),
            'linear_entropy': self.coherence.linear_entropy(rho_mixed)
        }

        results['coherent_state'] = measures_coherent
        results['mixed_state'] = measures_mixed

        print("  Coherent State:")
        for k, v in measures_coherent.items():
            print(f"    {k}: {v:.4f}")

        print("\n  Mixed State:")
        for k, v in measures_mixed.items():
            print(f"    {k}: {v:.4f}")

        return results

    def experiment_4_temperature_dependence(self) -> Dict:
        """
        Experiment 4: Temperature effects on decoherence
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 4: Temperature Dependence")
        print("=" * 60)

        temperatures = np.linspace(200, 400, 50)  # K
        coherence_times = []

        for T in temperatures:
            decoherence_T = DecoherenceMechanisms()
            decoherence_T.TEMP = T

            rates = decoherence_T.total_decoherence_rate()
            tau = rates['tau_total']
            coherence_times.append(tau * 1e6)  # μs

        results = {
            'temperature': temperatures,
            'coherence_time': np.array(coherence_times)
        }

        print(f"  Temperature range: {temperatures[0]:.0f} - {temperatures[-1]:.0f} K")
        print(f"  Coherence time range: {min(coherence_times):.2f} - {max(coherence_times):.2f} μs")

        return results

    def experiment_5_bell_violation(self) -> Dict:
        """
        Experiment 5: Bell inequality violation detection
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 5: Bell Inequality Violation Test")
        print("=" * 60)

        results = {}

        # Test different states
        states_to_test = {
            'singlet': np.array([0, 1, -1, 0]) / np.sqrt(2),
            'triplet_0': np.array([0, 1, 1, 0]) / np.sqrt(2),
            ' Werner': np.ones(4) / 2  # Maximally mixed
        }

        for name, state in states_to_test.items():
            rho = np.outer(state, state.conj())
            bell = self.entanglement.bell_inequality_test(rho)
            results[name] = bell

            print(f"\n  {name} state:")
            print(f"    S_CHSH = {bell['S_CHSH']:.4f}")
            print(f"    Classical bound: {bell['S_classical']:.2f}")
            print(f"    Violates Bell: {bell['violates_bell']}")

        return results

    def experiment_6_quantum_discord(self) -> Dict:
        """
        Experiment 6: Quantum discord dynamics
        """
        print("\n" + "=" * 60)
        print("EXPERIMENT 6: Quantum Discord Analysis")
        print("=" * 60)

        results = {}

        # Time range
        time_range = np.linspace(0, 50, 500) * 1e-6

        # Initial state with discord
        discords = []

        for t in time_range:
            # Create state with time-dependent coherence
            rho = np.zeros((4, 4), dtype=complex)
            rho[0, 0] = 0.25
            rho[1, 1] = 0.25
            rho[2, 2] = 0.25
            rho[3, 3] = 0.25

            # Coherence decays
            coh = 0.3 * np.exp(-t / 10e-6)
            rho[0, 1] = coh
            rho[1, 0] = coh

            D = self.entanglement.quantum_discord(rho)
            discords.append(D)

        results['time'] = time_range * 1e6
        results['discord'] = np.array(discords)

        print(f"  Initial discord: D = {discords[0]:.4f} bits")
        print(f"  Final discord: D = {discords[-1]:.4f} bits")
        print(f"  Lifetime: τ ≈ 10 μs")

        return results


def run_entanglement_decoherence_experiments():
    """
    Run all entanglement and decoherence experiments
    """
    print("\n" + "=" * 70)
    print("ENTANGLEMENT AND DECOHERENCE DYNAMICS EXPERIMENTS")
    print("=" * 70)

    experiment = EntanglementDecoherenceExperiment()
    all_results = {}

    # Run all experiments
    all_results['entanglement_creation'] = experiment.experiment_1_entanglement_creation()
    all_results['decoherence_channels'] = experiment.experiment_2_decoherence_channel()
    all_results['coherence_measures'] = experiment.experiment_3_coherence_measures()
    all_results['temperature_dependence'] = experiment.experiment_4_temperature_dependence()
    all_results['bell_violation'] = experiment.experiment_5_bell_violation()
    all_results['quantum_discord'] = experiment.experiment_6_quantum_discord()

    print("\n" + "=" * 70)
    print("ALL ENTANGLEMENT & DECOHERENCE EXPERIMENTS COMPLETED")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    results = run_entanglement_decoherence_experiments()

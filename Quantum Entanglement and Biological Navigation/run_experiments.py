#!/usr/bin/env python3
"""
Main Experiment Runner for Quantum-Biological Navigation Theory
============================================================

This script runs all experimental modules and generates comprehensive results.

Usage:
    python run_experiments.py

Author: Quantum Computing Research Team
Date: 2026
"""

import sys
import os
import time
import traceback
from datetime import datetime

# Add experiments directory to path
EXPERIMENTS_DIR = "/Users/chandansheikder/Documents/Quantum-Theory/new/experiments"
sys.path.insert(0, EXPERIMENTS_DIR)

# Output directory
OUTPUT_DIR = f"{EXPERIMENTS_DIR}/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/logs", exist_ok=True)


class ExperimentRunner:
    """
    Orchestrates all experiments from the Quantum-Biological Navigation Theory
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.results = {}
        self.errors = []

    def run_module(self, module_name: str, module_path: str) -> dict:
        """
        Run a single experimental module
        """
        print(f"\n{'='*60}")
        print(f"RUNNING: {module_name}")
        print(f"{'='*60}")

        try:
            # Import module
            if module_name in sys.modules:
                del sys.modules[module_name]

            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Run experiments
            if hasattr(module, 'run_all_experiments'):
                results = module.run_all_experiments()
            elif hasattr(module, 'run_multinuclear_experiments'):
                results = module.run_multinuclear_experiments()
            elif hasattr(module, 'run_entanglement_decoherence_experiments'):
                results = module.run_entanglement_decoherence_experiments()
            elif hasattr(module, 'run_qfi_experiments'):
                results = module.run_qfi_experiments()
            elif hasattr(module, 'run_compass_experiments'):
                results = module.run_compass_experiments()
            elif hasattr(module, 'run_information_experiments'):
                results = module.run_information_experiments()
            elif hasattr(module, 'run_quantum_experiments'):
                results = module.run_quantum_experiments()
            else:
                # Run the module directly if no run function
                if hasattr(module, 'experiment'):
                    results = module.experiment()
                else:
                    results = {"status": "completed", "note": "Module loaded but no run function found"}

            print(f"\n✓ {module_name} completed successfully")
            return {"success": True, "results": results}

        except Exception as e:
            error_msg = f"Error in {module_name}: {str(e)}"
            print(f"\n✗ {error_msg}")
            traceback.print_exc()
            return {"success": False, "error": str(e), "traceback": traceback.format_exc()}

    def run_all(self):
        """
        Run all experimental modules
        """
        print("\n" + "="*70)
        print("QUANTUM-BIOLOGICAL NAVIGATION THEORY")
        print("COMPREHENSIVE EXPERIMENTAL FRAMEWORK")
        print("="*70)
        print(f"\nStart time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Output directory: {OUTPUT_DIR}")

        # Define modules to run
        modules = [
            ("radical_pair_core", f"{EXPERIMENTS_DIR}/radical_pair_core.py"),
            ("multinuclear_experiments", f"{EXPERIMENTS_DIR}/multinuclear_experiments.py"),
            ("entanglement_decoherence", f"{EXPERIMENTS_DIR}/entanglement_decoherence.py"),
            ("qfi_analysis", f"{EXPERIMENTS_DIR}/qfi_analysis.py"),
            ("compass_navigation", f"{EXPERIMENTS_DIR}/compass_navigation.py"),
            ("information_theory", f"{EXPERIMENTS_DIR}/information_theory.py"),
            ("quantum_supercomputer", f"{EXPERIMENTS_DIR}/quantum_supercomputer.py"),
            ("generate_results", f"{EXPERIMENTS_DIR}/generate_results.py"),
        ]

        # Run each module
        for module_name, module_path in modules:
            result = self.run_module(module_name, module_path)
            self.results[module_name] = result

            if not result["success"]:
                self.errors.append({
                    "module": module_name,
                    "error": result["error"]
                })

        # Generate final report
        self.generate_report()

    def generate_report(self):
        """
        Generate final experiment report
        """
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        report = f"""
{'='*70}
EXPERIMENT RUN COMPLETE
{'='*70}

Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time:   {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Duration:   {duration:.1f} seconds

{'='*70}
RESULTS SUMMARY
{'='*70}
"""

        # Module results
        report += "\nModule Status:\n"
        report += "-" * 40 + "\n"

        for module_name, result in self.results.items():
            status = "✓ SUCCESS" if result["success"] else "✗ FAILED"
            report += f"  {module_name:40s} {status}\n"

        # Errors
        if self.errors:
            report += f"\n{'='*70}\n"
            report += "ERRORS\n"
            report += f"{'='*70}\n"

            for error in self.errors:
                report += f"\nModule: {error['module']}\n"
                report += f"Error: {error['error']}\n"

        # Summary
        n_success = sum(1 for r in self.results.values() if r["success"])
        n_total = len(self.results)

        report += f"""
{'='*70}
SUMMARY
{'='*70}

Modules Run: {n_total}
Successful:  {n_success}
Failed:      {n_total - n_success}

Output Directory: {OUTPUT_DIR}

Generated Files:
  - results/figures/ (PNG visualizations)
  - results/data/ (CSV, JSON data)
  - results/logs/ (execution logs)
  - results/summary.txt (this report)

{'='*70}
"""

        # Save report
        report_path = f"{OUTPUT_DIR}/experiment_report.txt"
        with open(report_path, 'w') as f:
            f.write(report)

        print(report)

        # Save to log
        log_path = f"{OUTPUT_DIR}/logs/run_{self.start_time.strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_path, 'w') as f:
            f.write(report)

        print(f"\nReport saved to: {report_path}")
        print(f"Log saved to: {log_path}")


def main():
    """
    Main entry point
    """
    runner = ExperimentRunner()
    runner.run_all()


if __name__ == "__main__":
    main()

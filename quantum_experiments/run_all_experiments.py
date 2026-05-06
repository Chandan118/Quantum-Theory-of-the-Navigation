"""
run_all_experiments.py
========================================================
Super-Powered Runner Suite v2.0
========================================================
Orchestrates the parallel execution of 10 high-resolution
quantum physics experiments and generates a final report.
"""

import subprocess
import time
import os
from concurrent.futures import ProcessPoolExecutor

# --- Configurations ---
EXPERIMENTS = [
    "exp01_singlet_yield.py",
    "exp02_entanglement_dynamics.py",
    "exp03_quantum_fisher.py",
    "exp04_decoherence_t2.py",
    "exp05_rf_disruption.py",
    "exp06_multinuclear.py",
    "exp07_quantum_vs_classical.py",
    "exp08_qiskit_circuit.py",
    "exp09_temperature.py",
    "exp10_coherence_witness.py"
]

RESULTS_DIR = "results"
REPORT_FILE = f"{RESULTS_DIR}/SUPER_SUMMARY_REPORT.txt"

def run_script(script):
    """Executes a single experiment script and returns result."""
    start = time.time()
    try:
        print(f"▶️  Launching {script}...")
        result = subprocess.run(["python3", script], capture_output=True, text=True, check=True)
        duration = time.time() - start
        return {"script": script, "status": "SUCCESS", "time": duration}
    except subprocess.CalledProcessError as e:
        duration = time.time() - start
        return {"script": script, "status": "FAILED", "time": duration, "error": e.stderr}

def main():
    print("========================================================")
    print("          SUPER-POWERED QUANTUM SUITE RUNNER            ")
    print("========================================================")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    overall_start = time.time()
    
    # Execute experiments in parallel to handle high-res computational load
    print(f"⚙️  Executing {len(EXPERIMENTS)} experiments in parallel pools...")
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run_script, EXPERIMENTS))
    
    total_time = time.time() - overall_start
    
    # --- Generate Report ---
    print("\n📝 Generating Super-Summary Report...")
    with open(REPORT_FILE, "w") as f:
        f.write("========================================================\n")
        f.write("      SUPER-POWERED QUANTUM EXPERIMENT REPORT           \n")
        f.write("========================================================\n\n")
        f.write(f"Total Suite Duration: {total_time:.2f} seconds\n\n")
        
        f.write(f"{'Experiment':<35} | {'Status':<10} | {'Time (s)':<10}\n")
        f.write("-" * 65 + "\n")
        
        success_count = 0
        for r in results:
            f.write(f"{r['script']:<35} | {r['status']:<10} | {r['time']:<10.2f}\n")
            if r['status'] == "SUCCESS":
                success_count += 1
            else:
                f.write(f"   ⚠️ ERROR: {r['error'][:200]}...\n")
        
        f.write("\n" + "=" * 65 + "\n")
        f.write(f"FINAL SCORE: {success_count}/{len(EXPERIMENTS)} Experiments Successful\n")
        f.write("========================================================\n")

    print(f"\n✅ All done! Report generated at: {REPORT_FILE}")
    print(f"📊 Total Time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()

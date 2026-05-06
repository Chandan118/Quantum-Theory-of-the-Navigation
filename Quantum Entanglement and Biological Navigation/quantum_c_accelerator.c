#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <complex.h>
#include <math.h>
#include <stdlib.h>

// Helper to apply 1-qubit gate
void apply_1q_gate(double complex *state, int n_qubits, int target, double complex u00, double complex u01, double complex u10, double complex u11) {
    long long dim = 1LL << n_qubits;
    long long chunk = 1LL << target;
    
    for (long long i = 0; i < dim; i += (chunk * 2)) {
        for (long long j = 0; j < chunk; j++) {
            long long idx0 = i + j;
            long long idx1 = i + j + chunk;
            
            double complex a = state[idx0];
            double complex b = state[idx1];
            
            state[idx0] = u00 * a + u01 * b;
            state[idx1] = u10 * a + u11 * b;
        }
    }
}

// Helper to apply CNOT gate
void apply_cnot(double complex *state, int n_qubits, int control, int target) {
    long long dim = 1LL << n_qubits;
    for (long long i = 0; i < dim; i++) {
        int bit_c = (i >> control) & 1;
        int bit_t = (i >> target) & 1;
        if (bit_c == 1 && bit_t == 0) {
            long long idx1 = i;
            long long idx2 = i | (1LL << target);
            double complex temp = state[idx1];
            state[idx1] = state[idx2];
            state[idx2] = temp;
        }
    }
}

static PyObject* simulate_radical_pair(PyObject* self, PyObject* args) {
    int n_nuclei;
    if (!PyArg_ParseTuple(args, "i", &n_nuclei)) {
        return NULL;
    }
    
    int n_qubits = 2 + n_nuclei;
    long long dim = 1LL << n_qubits;
    
    double complex *state = (double complex*)calloc(dim, sizeof(double complex));
    if (!state) return PyErr_NoMemory();
    
    state[0] = 1.0; // |0...0>
    
    // qc.x(0)
    apply_1q_gate(state, n_qubits, 0, 0, 1, 1, 0);
    // qc.x(1)
    apply_1q_gate(state, n_qubits, 1, 0, 1, 1, 0);
    // qc.h(0)
    double inv_sqrt2 = 1.0 / sqrt(2.0);
    apply_1q_gate(state, n_qubits, 0, inv_sqrt2, inv_sqrt2, inv_sqrt2, -inv_sqrt2);
    // qc.cx(0, 1)
    apply_cnot(state, n_qubits, 0, 1);
    // qc.z(1)
    apply_1q_gate(state, n_qubits, 1, 1, 0, 0, -1);
    
    // Zeeman
    double omega_t = (2.0023 * 9.274e-24 * 50e-6 / 1.0545718e-34) * 1e-6;
    double complex phase = cexp(I * omega_t / 2.0);
    double complex phase_conj = cexp(-I * omega_t / 2.0);
    apply_1q_gate(state, n_qubits, 0, phase_conj, 0, 0, phase);
    apply_1q_gate(state, n_qubits, 1, phase_conj, 0, 0, phase);
    
    // Hyperfine
    for (int i = 0; i < n_nuclei; i++) {
        apply_cnot(state, n_qubits, 0, 2 + i);
        double A = 1e-3;
        double complex p = cexp(I * A / 2.0);
        double complex p_c = cexp(-I * A / 2.0);
        apply_1q_gate(state, n_qubits, 2 + i, p_c, 0, 0, p);
    }
    
    // Return Python list of complex numbers
    PyObject *result_list = PyList_New(dim);
    for (long long i = 0; i < dim; i++) {
        PyObject *comp = PyComplex_FromDoubles(creal(state[i]), cimag(state[i]));
        PyList_SetItem(result_list, i, comp);
    }
    
    free(state);
    return result_list;
}

static PyMethodDef AcceleratorMethods[] = {
    {"simulate_radical_pair", simulate_radical_pair, METH_VARARGS, "Simulate radical pair state vector"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef acceleratormodule = {
    PyModuleDef_HEAD_INIT,
    "quantum_c_accelerator",
    "C Accelerator for Quantum Supercomputer",
    -1,
    AcceleratorMethods
};

PyMODINIT_FUNC PyInit_quantum_c_accelerator(void) {
    return PyModule_Create(&acceleratormodule);
}

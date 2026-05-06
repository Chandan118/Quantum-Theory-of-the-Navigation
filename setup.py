from setuptools import setup, find_packages, Extension

accelerator_module = Extension('quantum_c_accelerator',
                               sources=['Quantum Entanglement and Biological Navigation/quantum_c_accelerator.c'])

setup(
    name="quantum-navigation-theory",
    version="1.0.0",
    description="Quantum Theory of Navigation - Cryptochrome RPM",
    author="Chandan Sheikder",
    packages=find_packages(),
    ext_modules=[accelerator_module],
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
        "qiskit",
        "qutip"
    ],
    python_requires=">=3.10",
)

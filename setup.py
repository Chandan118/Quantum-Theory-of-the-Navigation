from setuptools import setup, find_packages

setup(
    name="quantum-navigation-theory",
    version="1.0.0",
    description="Quantum Theory of Navigation - Cryptochrome RPM",
    author="Chandan Sheikder",
    packages=find_packages(),
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

This repository demonstrates quantum measurement–based energy estimation of
two-qubit spin Hamiltonians using Qiskit. The workflow mirrors the **measurement core of variational quantum algorithms (VQE)** for both isotropic and anisotropic spin models and validate quantum measurement results against classical exact diagonalization.
### Isotropic Heisenberg Model
\[
H = J (X - X + Y \otimes Y + Z \otimes Z)
\]

### Anisotropic XXZ Model
\[
H = J (X \otimes X + Y \otimes Y) + \Delta (Z \otimes Z)
\]

- Hamiltonians are decomposed into Pauli strings (XX, YY, ZZ)
- Bell-State preparation
- Noise models applied to single- and two-qubit gates under NISQ-like noise
- Energy estimation error plotted versus number of measurement shots
- Demonstrates statistical convergence consistent with theory
- Classical Validation
- Exact diagonalization for classical validation performed using NumPy
- Quantum-estimated energies validated against exact ground-state energies
- A **lightweight 2-qubit VQE** is included
- Classical optimization using COBYLA, onvergence benchmarked against exact diagonalization

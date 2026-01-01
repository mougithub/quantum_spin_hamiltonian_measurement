import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def heisenberg_energy(J=1.0):
    H = J * (np.kron(X, X) + np.kron(Y, Y) + np.kron(Z, Z))
    return np.linalg.eigvalsh(H).min()

def xxz_energy(J=1.0, Delta=1.2):
    H = J * (np.kron(X, X) + np.kron(Y, Y)) + Delta * np.kron(Z, Z)
    return np.linalg.eigvalsh(H).min()

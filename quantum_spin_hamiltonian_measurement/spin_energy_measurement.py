import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, execute
from qiskit_aer.noise import NoiseModel, depolarizing_error
from scipy.optimize import minimize
from exact_diagonalization import heisenberg_energy, xxz_energy

backend = Aer.get_backend("qasm_simulator")

# -------------------------------------------------
# Noise model
# -------------------------------------------------
def get_noise_model(p1=0.001, p2=0.01):
    noise = NoiseModel()
    noise.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ['h', 'sdg'])
    noise.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ['cx'])
    return noise

# -------------------------------------------------
# Bell state
# -------------------------------------------------
def prepare_bell(qc):
    qc.h(0)
    qc.cx(0, 1)

# -------------------------------------------------
# Pauli measurement (no ansatz)
# -------------------------------------------------
def measure_pauli(pauli, shots=4096, bell=False, noise=False):
    qc = QuantumCircuit(2)
    if bell:
        prepare_bell(qc)

    if pauli == "XX":
        qc.h([0, 1])
    elif pauli == "YY":
        qc.sdg([0, 1])
        qc.h([0, 1])

    qc.measure_all()

    result = execute(
        qc,
        backend,
        shots=shots,
        noise_model=get_noise_model() if noise else None
    ).result()

    counts = result.get_counts()
    return sum((-1)**b.count("1") * c for b, c in counts.items()) / shots

# -------------------------------------------------
# Energy estimation (Heisenberg / XXZ)
# -------------------------------------------------
def estimate_energy(J=1.0, Delta=1.0, shots=4096):
    exx = measure_pauli("XX", shots)
    eyy = measure_pauli("YY", shots)
    ezz = measure_pauli("ZZ", shots)
    return J * (exx + eyy) + Delta * ezz

# -------------------------------------------------
# Minimal VQE
# -------------------------------------------------
def vqe_ansatz(theta):
    qc = QuantumCircuit(2)
    qc.ry(theta[0], 0)
    qc.ry(theta[1], 1)
    qc.cx(0, 1)
    return qc

def measure_pauli_vqe(pauli, theta, shots=4096):
    qc = vqe_ansatz(theta)

    if pauli == "XX":
        qc.h([0, 1])
    elif pauli == "YY":
        qc.sdg([0, 1])
        qc.h([0, 1])

    qc.measure_all()
    result = execute(qc, backend, shots=shots).result()
    counts = result.get_counts()

    return sum((-1)**b.count("1") * c for b, c in counts.items()) / shots

def vqe_energy(theta, J=1.0, Delta=1.0, shots=4096):
    exx = measure_pauli_vqe("XX", theta, shots)
    eyy = measure_pauli_vqe("YY", theta, shots)
    ezz = measure_pauli_vqe("ZZ", theta, shots)
    return J * (exx + eyy) + Delta * ezz

# -------------------------------------------------
# Main execution
# -------------------------------------------------
if __name__ == "__main__":

    print("\n--- Shot-noise scaling (XXZ) ---")
    shots_list = [256, 512, 1024, 2048, 4096, 8192]
    errors = []

    exact = xxz_energy(J=1.0, Delta=1.2)

    for s in shots_list:
        eq = estimate_energy(J=1.0, Delta=1.2, shots=s)
        err = abs(eq - exact)
        errors.append(err)
        print(f"Shots: {s:5d} | Energy: {eq:.4f} | Error: {err:.2e}")

    plt.loglog(shots_list, errors, 'o-')
    plt.xlabel("Shots")
    plt.ylabel("Energy Error")
    plt.title("Energy Estimation Error vs Shots (XXZ)")
    plt.grid()
    plt.show()


    print("\n--- Minimal VQE (Heisenberg) ---")
    theta0 = np.random.rand(2)
    res = minimize(
        vqe_energy,
        theta0,
        args=(1.0, 1.0, 2048),
        method="COBYLA"
    )

    print("VQE optimal energy:", res.fun)
    print("Exact energy:", heisenberg_energy())

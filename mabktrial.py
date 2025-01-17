from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import numpy as np


def create_ghz_state():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    return qc


def apply_basis_transformation(qc, basis):
    for i, pauli in enumerate(basis):
        if pauli == 'X':
            qc.h(i)
        elif pauli == 'Y':
            qc.sdg(i)
            qc.h(i)


def calculate_expectation(counts, shots):
    expectation = 0
    for outcome, count in counts.items():
        parity = (-1) ** (outcome.count('1'))
        expectation += parity * count / shots
    return expectation

#  GHZ state and measurement circuits
ghz_circuit = create_ghz_state()
measurement_circuits = []
shots = 8192


basis_combinations = [
    ['X', 'X', 'X'],
    ['X', 'Y', 'Y'],
    ['Y', 'X', 'Y'],
    ['Y', 'Y', 'X']
]

# Create circuits
for basis in basis_combinations:
    qc = ghz_circuit.copy()
    apply_basis_transformation(qc, basis)
    qc.measure_all()
    measurement_circuits.append(qc)

# Execute the circuits
backend = Aer.get_backend('qasm_simulator')
transpiled_circuits = transpile(measurement_circuits, backend)
qobj = assemble(transpiled_circuits, backend, shots=shots)
results = backend.run(qobj).result()

# Calculate the MABK inequality
terms = []
for result in results.results:
    counts = result.data.counts
    expectation = calculate_expectation(counts, shots)
    terms.append(expectation)

# Calculate the MABK value
mabk_value = sum(terms)

# Print MABK value and violation check
print(f"MABK value: {mabk_value}")
print(f"Violation: {abs(mabk_value) > 4}")

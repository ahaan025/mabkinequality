import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Define the quantum state
state = np.array([1/np.sqrt(8), 1/np.sqrt(8), 1/np.sqrt(8), 1/np.sqrt(8), 1/np.sqrt(8), 1/np.sqrt(8), 1/np.sqrt(8), 1/np.sqrt(8)])


# Define the 3-qubit MABK operator
def mabk_operator(theta_a, theta_b, theta_c):
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.rz(theta_a, 0)
    qc.rz(theta_b, 1)
    qc.rz(theta_c, 2)
    qc.measure_all()
    return qc

def mabk_witness(theta_a, theta_b, theta_c, state):
    qc = mabk_operator(theta_a, theta_b, theta_c)
    backend = Aer.get_backend('qasm_simulator')
    qc_transpiled = transpile(qc, backend)
    job = backend.run(qc_transpiled, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    #   expectation value of the MABK operator
    p_000 = counts.get('000', 0) / 1000
    p_001 = counts.get('001', 0) / 1000
    p_010 = counts.get('010', 0) / 1000
    p_011 = counts.get('011', 0) / 1000
    p_100 = counts.get('100', 0) / 1000
    p_101 = counts.get('101', 0) / 1000
    p_110 = counts.get('110', 0) / 1000
    p_111 = counts.get('111', 0) / 1000
    
    mabk_value = p_000 - p_001 - p_010 + p_011 + p_100 + p_101 - p_110 - p_111
    return mabk_value

# Plot the MABK witness vs. the measurement angle
theta_range = np.linspace(0, 2 * np.pi, 101)
mabk_values = []
for theta in theta_range:
    mabk_value = mabk_witness(theta, theta, theta, state)
    mabk_values.append(mabk_value)

plt.figure(figsize=(10, 6))
plt.plot(theta_range, mabk_values)
plt.axhline(y=4, color='r', linestyle='--')
plt.xlabel('Measurement Angle (θ)')
plt.ylabel('MABK Witness')
plt.title('MABK Inequality Violation for 3-Qubit System')
plt.savefig('mabk_violation.png')

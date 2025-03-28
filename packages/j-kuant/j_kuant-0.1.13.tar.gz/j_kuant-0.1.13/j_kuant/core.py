from qiskit import transpile

def estimated(circuit,backend,observable, estimator):
    transpiled = transpile(circuit,backend) # Transpile the circuit
    return estimator.run([transpiled],observable) # Return the estimator

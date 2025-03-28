from qiskit import transpiler

def estimated(circuit,backend,observable, estimator):
    transpiled = transpiler(circuit,backend) # Transpile the circuit
    return estimator.run([transpiled],observable) # Return the estimator

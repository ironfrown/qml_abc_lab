# Support functions for Qiskit models creation
# Author: Jacob Cybulski, ironfrown[at]gmail.com
# Aims: Provide support for QTSA model creation
# Date: 2024-2025

import os
import numpy as np
import math

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit.circuit.library import RealAmplitudes, TwoLocal, ZFeatureMap, ZZFeatureMap,EfficientSU2, PauliFeatureMap
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.circuit import Parameter
from qiskit.compiler import transpile


### Create a custom serial model circuit 
#   - To be used with CircuitQNN / NeuralNetworkRegressor

def serial_fourier_model(layers, add_meas=False):
    
    ansatz = QuantumCircuit(1, name="ansatz")
    param_x = Parameter('X')
    pno = 0 # Variational parameter counter
    params = []

    # Data encoding block
    def S():
        ansatz.rx(param_x, 0)

    # Trainable variational block
    def W(layer, label):
        nonlocal pno
        nonlocal params
        param_w_0 = Parameter(f'{label}[{pno:03d}]')
        param_w_1 = Parameter(f'{label}[{pno+1:03d}]')
        param_w_2 = Parameter(f'{label}[{pno+2:03d}]')
        params += [param_w_0, param_w_1, param_w_2]
        ansatz.u(param_w_0, param_w_1, param_w_2, 0)
        pno += 3

    # Create layers of W, S blocks
    for l in range(layers):
        W(l, 'W')
        S()

    # Add the final block
    W(layers, 'W')

    if add_meas:
        ansatz.measure_all()

    # Create a parameter list
    params += [param_x]

    return ansatz 


### Create a custom parallel model circuit 
#   - To be used with CircuitQNN / NeuralNetworkRegressor

def parallel_fourier_model(qubit_no, before_layers, after_layers, add_meas=False):
    
    qr = QuantumRegister(qubit_no, 'q')
    ansatz = QuantumCircuit(qr, name='ansatz')
    param_x = Parameter('x')

    # Data encoding block
    def S():
        for q in range(qubit_no):
            ansatz.rx(param_x, q)

    # Trainable variational block
    def W(layers, label):
        pno = 0  # Variational parameter counter
        
        for l in range(layers):
            ansatz.barrier()
            for q in range(qubit_no):
                ansatz.u(Parameter(f'{label}[{pno:03d}]'), 
                         Parameter(f'{label}[{pno+1:03d}]'), 
                         Parameter(f'{label}[{pno+2:03d}]'), 
                         q)
                pno += 3
            ansatz.barrier()
            ansatz.append(
                TwoLocal(qubit_no, [], 'cx', 
                         entanglement='circular',
                         reps=1, 
                         parameter_prefix=label, 
                         insert_barriers=False,
                         skip_final_rotation_layer=False),
                qargs=qr)
        
        ansatz.barrier()
        for q in range(qubit_no):
            ansatz.u(Parameter(f'{label}[{pno:03d}]'), 
                     Parameter(f'{label}[{pno+1:03d}]'), 
                     Parameter(f'{label}[{pno+2:03d}]'), 
                     q)
            pno += 3

    
    # Create layers of WB, S, WA blocks
    W(before_layers, 'B')
    ansatz.barrier()
    S()
    W(after_layers, 'A')

    if add_meas:
        ansatz.measure_all()

    return ansatz.decompose().decompose()    


def parallel_fourier_model_with_reuploading(qubit_no, before_layers, after_layers, add_meas=False):
    
    qr = QuantumRegister(qubit_no, 'q')
    ansatz = QuantumCircuit(qr, name='ansatz')
    param_x = Parameter('x')

    # Data encoding block
    def S():
        for q in range(qubit_no):
            ansatz.rx(param_x, q)

    # Data encoding block
    def BS(layers, label):
        pno = 0  # Variational parameter counter
        
        for l in range(layers):
            ansatz.barrier()
            for q in range(qubit_no):
                ansatz.u(Parameter(f'{label}[{pno:03d}]'), 
                         Parameter(f'{label}[{pno+1:03d}]'), 
                         Parameter(f'{label}[{pno+2:03d}]'), 
                         q)
                pno += 3
            ansatz.barrier()
            if qubit_no > 1:
                ansatz.append(
                    TwoLocal(qubit_no, [], 'cx', 
                             entanglement='circular',
                             reps=1, 
                             parameter_prefix=label, 
                             insert_barriers=False,
                             skip_final_rotation_layer=False),
                    qargs=qr)     
                ansatz.barrier()
            S()
            
    # Trainable variational block
    def AW(layers, label):
        pno = 0  # Variational parameter counter
        
        for l in range(layers):
            ansatz.barrier()
            for q in range(qubit_no):
                ansatz.u(Parameter(f'{label}[{pno:03d}]'), 
                         Parameter(f'{label}[{pno+1:03d}]'), 
                         Parameter(f'{label}[{pno+2:03d}]'), 
                         q)
                pno += 3
            if qubit_no > 1:
                ansatz.barrier()
                ansatz.append(
                    TwoLocal(qubit_no, [], 'cx', 
                             entanglement='circular',
                             reps=1, 
                             parameter_prefix=label, 
                             insert_barriers=False,
                             skip_final_rotation_layer=False),
                    qargs=qr)
        
        ansatz.barrier()
        for q in range(qubit_no):
            ansatz.u(Parameter(f'{label}[{pno:03d}]'), 
                     Parameter(f'{label}[{pno+1:03d}]'), 
                     Parameter(f'{label}[{pno+2:03d}]'), 
                     q)
            pno += 3

    
    # Create layers of WB, S, WA blocks
    BS(before_layers, 'B')
    AW(after_layers, 'A')

    if add_meas:
        ansatz.measure_all()

    return ansatz.decompose().decompose()    

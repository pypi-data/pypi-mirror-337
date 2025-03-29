# This code is a Qiskit project.
#
# (C) Copyright IBM 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import random

import numpy as np
import pytest
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.circuit.library import efficient_su2, n_local

from qiskit_addon_aqc_tensor.objective import MaximizeStateFidelity
from qiskit_addon_aqc_tensor.simulation import (
    apply_circuit_to_state,
    compute_overlap,
    tensornetwork_from_circuit,
)
from qiskit_addon_aqc_tensor.simulation.abstract import (
    _compute_objective_and_gradient,
    _preprocess_for_gradient,
)
from qiskit_addon_aqc_tensor.simulation.aer import is_aer_available
from qiskit_addon_aqc_tensor.simulation.explicit_gradient import _basis_gates


def _get_random_bool() -> bool:
    return bool(random.getrandbits(1))


def _generate_random_ansatz(num_qubits: int):
    """Generates a random ansatz circuit suitable for gradient computation."""
    su2_gates = ["h", "x", "y", "z", "rx", "ry", "rz"]
    random.shuffle(su2_gates)
    qc = n_local(
        num_qubits=num_qubits,
        rotation_blocks=su2_gates,
        entanglement_blocks=["cx", "cz"],
        reps=random.randint(1, 2),
        parameter_prefix="a",
        insert_barriers=_get_random_bool(),
    )
    random.shuffle(su2_gates)
    qc.compose(
        n_local(
            num_qubits=num_qubits,
            rotation_blocks=su2_gates,
            entanglement_blocks=["cx", "cz"],
            reps=random.randint(1, 2),
            parameter_prefix="b",
            insert_barriers=_get_random_bool(),
        ),
        inplace=True,
        copy=False,
    )
    # Include a parameter expression in this test
    x = Parameter("x")
    qc.rx(2 * x - 1.5, 0)
    random.shuffle(su2_gates)
    qc.compose(
        efficient_su2(
            num_qubits=num_qubits,
            su2_gates=su2_gates,
            reps=random.randint(1, 2),
            parameter_prefix="c",
            insert_barriers=True,
        ),
        inplace=True,
        copy=False,
    )
    return transpile(qc, basis_gates=_basis_gates(), optimization_level=1)


def _get_random_thetas(num_parameters: int):
    return np.pi * (2 * np.random.rand(num_parameters) - 1)


def _random_unentangled_circuit(num_qubits: int) -> QuantumCircuit:
    """
    Generates a random unentangled circuit for debugging and testing.
    """
    qc = QuantumCircuit(num_qubits)
    thetas = np.pi * (2 * np.random.rand(num_qubits, 3) - 1)
    for i in range(num_qubits):
        qc.h(i)
        qc.rz(float(thetas[i, 0]), i)
        qc.ry(float(thetas[i, 1]), i)
        qc.rz(float(thetas[i, 2]), i)
    return qc


@pytest.mark.parametrize("num_qubits", [4])
def test_mps_gradient_of_random_circuit(num_qubits: int, available_backend_fixture):
    qc = _generate_random_ansatz(num_qubits)
    settings = available_backend_fixture
    thetas = _get_random_thetas(qc.num_parameters)
    lhs_mps = tensornetwork_from_circuit(QuantumCircuit(num_qubits), settings)
    rhs_mps = tensornetwork_from_circuit(_random_unentangled_circuit(num_qubits), settings)

    def vdagger_rhs(thetas):
        bound_qc = qc.assign_parameters(thetas)
        return apply_circuit_to_state(bound_qc.inverse(), rhs_mps, settings)

    objective = MaximizeStateFidelity(rhs_mps, qc, settings)
    preprocess_info = _preprocess_for_gradient(objective, settings)
    _, grad = _compute_objective_and_gradient(objective, settings, preprocess_info, thetas)

    # Compute numerical gradient
    numerical_grad = np.zeros(qc.num_parameters, dtype=complex)
    delta = 0.02
    for i in range(qc.num_parameters):
        thetas_p = thetas.copy()
        thetas_m = thetas.copy()
        thetas_p[i] += 0.5 * delta
        thetas_m[i] -= 0.5 * delta
        f_p = compute_overlap(lhs_mps, vdagger_rhs(thetas_p))
        f_m = compute_overlap(lhs_mps, vdagger_rhs(thetas_m))
        numerical_grad[i] = (f_p - f_m) / delta

    # Convert overlap gradient to fidelity gradient
    f_0 = compute_overlap(lhs_mps, vdagger_rhs(thetas))
    numerical_grad = -2 * np.real(np.conj(f_0) * numerical_grad)

    assert grad == pytest.approx(numerical_grad, abs=1e-4)


@pytest.mark.skipif(not is_aer_available(), reason="qiskit-aer is not installed")
class TestExplicitGradient:
    def test_no_parameters_throws_error(self, AerSimulator):
        settings = AerSimulator(method="matrix_product_state")
        tn = tensornetwork_from_circuit(QuantumCircuit(1), settings)
        qc = QuantumCircuit(1)
        with pytest.raises(ValueError) as e_info:
            MaximizeStateFidelity(tn, qc, settings)
        assert (
            e_info.value.args[0]
            == "Expects parametric circuit using ParameterVector object.\nThat is, placeholders are expected rather than concrete\nvalues for the variable parameters. The circuit specified\nhas no variable parameters. Check that the function\nassign_parameters() has not been applied to this circuit."
        )

    def test_non_basis_gate(self, AerSimulator):
        settings = AerSimulator(method="matrix_product_state")
        tn = tensornetwork_from_circuit(QuantumCircuit(2), settings)
        qc = QuantumCircuit(2)
        x = Parameter("x")
        qc.rx(x, 0)
        qc.cp(np.pi / 5, 0, 1)
        with pytest.raises(ValueError) as e_info:
            MaximizeStateFidelity(tn, qc, settings)
        assert (
            e_info.value.args[0]
            == "Expects a gate from the list of basis ones: ['cx', 'cz', 'ecr', 'h', 'rx', 'ry', 'rz', 's', 'sdg', 'x', 'y', 'z'], got 'cp' instead."
        )

    def test_one_qubit_parametrized_pauli_error_messages(self, subtests, AerSimulator):
        settings = AerSimulator(method="matrix_product_state")
        tn = tensornetwork_from_circuit(QuantumCircuit(1), settings)
        x = Parameter("x")
        y = Parameter("y")
        with subtests.test("Expression with multiple parameters"):
            qc = QuantumCircuit(1)
            qc.rx(x + y, 0)
            with pytest.raises(ValueError) as e_info:
                MaximizeStateFidelity(tn, qc, settings)
            assert e_info.value.args[0] == "Expression cannot contain more than one Parameter"
        with subtests.test("Nonlinear expression"):
            qc = QuantumCircuit(1)
            qc.rx(x**3, 0)
            with pytest.raises(ValueError) as e_info:
                MaximizeStateFidelity(tn, qc, settings)
            assert (
                e_info.value.args[0]
                == "ParameterExpression's derivative must be a floating-point number, i.e., the expression must be in the form ax + b."
            )

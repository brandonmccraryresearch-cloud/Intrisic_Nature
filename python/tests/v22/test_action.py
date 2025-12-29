import pytest
import numpy as np
from irh.core.v22.action import SymplecticAction
from irh.core.v22.cymatics import GInfElement
from irh.core.v22.quaternion import Quaternion

class TestSymplecticAction:

    def test_kinetic_term(self):
        # Setup trivial field
        field = [
            GInfElement(Quaternion(1,0,0,0), 0.0),
            GInfElement(Quaternion(1,0,0,0), 0.0)
        ]
        # Trivial laplacian (disconnected)
        laplacian = np.array([[1.0, 0.0], [0.0, 1.0]])

        action = SymplecticAction()
        kin = action.compute_kinetic_term(field, laplacian)

        # S_kin = sum m^2 |phi|^2 + phi*L*phi
        # m=1. |phi|=1.
        # Term 1: 1*1 + 1*1 = 2
        # Term 2: 1*1*1 + 1*1*1 = 2
        # Total = 4.0
        assert np.isclose(kin, 4.0)

    def test_interaction_term(self):
        # Setup field with norm 1
        field = [GInfElement(Quaternion(1,0,0,0), 0.0)] * 4
        action = SymplecticAction(lambda_coupling=1.0)

        # S_int = lambda * sum |phi|^4
        # 1.0 * (1^4 * 4) = 4.0

        # We need to pass dummy adjacency
        adj = np.zeros((4,4))

        val = action.compute_interaction_term(field, adj)
        assert np.isclose(val, 4.0)

    def test_kernel_evaluation(self):
        action = SymplecticAction(gamma_coupling=0.0)
        g = GInfElement(Quaternion(1,0,0,0), 0.0)

        # If gamma=0, weight factor is 1.
        # If phases are 0, phase factor is 1.
        kernel = action.evaluate_kernel(g, g, g, g)
        assert np.isclose(kernel, 1.0 + 0j)

        # Test phase cancellation
        g_pi = GInfElement(Quaternion(1,0,0,0), np.pi)
        # exp(i(pi + pi + pi - pi)) = exp(i(2pi)) = 1
        kernel2 = action.evaluate_kernel(g_pi, g_pi, g_pi, g_pi)
        assert np.isclose(kernel2, 1.0 + 0j)

        # exp(i(0 + 0 + 0 - pi)) = exp(-i pi) = -1
        kernel3 = action.evaluate_kernel(g, g, g, g_pi)
        assert np.isclose(kernel3, -1.0 + 0j)

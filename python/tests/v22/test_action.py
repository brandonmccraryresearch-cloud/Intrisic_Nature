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
    
    def test_kernel_with_distance_weighting(self):
        """Test that the kernel properly includes QNCD distance weighting."""
        action = SymplecticAction(gamma_coupling=1.0)
        
        # Create states with different quaternions to get non-zero QNCD
        g1 = GInfElement(Quaternion(1, 0, 0, 0), 0.0)
        g2 = GInfElement(Quaternion(0, 1, 0, 0), 0.0)  # Orthogonal to g1
        
        # Kernel with identical states (QNCD = 0)
        kernel_same = action.evaluate_kernel(g1, g1, g1, g1)
        # Phase sum: 0+0+0-0 = 0, exp(i*0) = 1
        # QNCD sum: all pairs are (g1,g1), distance = 0
        # Weight: exp(-1.0 * 0) = 1
        assert np.isclose(kernel_same, 1.0 + 0j)
        
        # Kernel with different states (QNCD > 0)
        kernel_diff = action.evaluate_kernel(g1, g2, g1, g2)
        # QNCD: d(g1,g2) appears in pairs (1,2), (1,4), (2,3), (3,4)
        # g1 and g2 are orthogonal, so d(g1,g2) = 1.0
        # Weight should be less than 1 due to exp(-gamma * QNCD_sum)
        assert abs(kernel_diff) < 1.0

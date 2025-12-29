import numpy as np
from irh.core.v22.harmony import HarmonyFunctional

class TestHarmony:

    def test_trivial_laplacian(self):
        # Identity matrix as laplacian (not physical but good for test)
        # L = I. Eigs = 1, 1.
        # Tr(L^2) = 1+1 = 2.
        # log(det) = log(1) + log(1) = 0.
        # Harmony = 2 - C * 0 = 2.

        L = np.eye(2)
        hf = HarmonyFunctional(c_h=1.0)
        val = hf.compute_harmony(L)
        assert np.isclose(val, 2.0)

    def test_degenerate_laplacian(self):
        # L = 0. Eigs = 0, 0.
        # Tr = 0.
        # non_zero_eigs = []
        # log_det = -inf
        # Harmony = 0 - C * (-inf) = +inf
        # The code returns infinity in this case if logic holds
        L = np.zeros((2,2))
        hf = HarmonyFunctional()
        val = hf.compute_harmony(L)
        assert np.isinf(val)

    def test_graph_laplacian(self):
        # Simple path graph: 1 -- 2
        # Degree matrix D = diag(1, 1)
        # Adjacency A = [[0,1],[1,0]]
        # L = D - A = [[1, -1], [-1, 1]]
        # Eigenvalues of L: 0, 2.

        L = np.array([[1, -1], [-1, 1]])

        # Tr(L^2) = 1+1+1+1 = 4. Or 0^2 + 2^2 = 4.
        # log(det') = log(2).

        hf = HarmonyFunctional(c_h=0.5)
        val = hf.compute_harmony(L)

        expected = 4.0 - 0.5 * np.log(2)
        assert np.isclose(val, expected)

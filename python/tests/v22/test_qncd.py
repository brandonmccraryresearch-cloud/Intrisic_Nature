import numpy as np
from irh.core.v22.quaternion import Quaternion
from irh.core.v22.qncd import compute_qncd

class TestQNCD:

    def test_identity(self):
        q = Quaternion(1, 0, 0, 0)
        dist = compute_qncd(q, q)
        assert np.isclose(dist, 0.0, atol=1e-7)

    def test_symmetry(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0, 1, 0, 0)
        d12 = compute_qncd(q1, q2)
        d21 = compute_qncd(q2, q1)
        assert np.isclose(d12, d21)

    def test_orthogonal_states(self):
        # (1,0,0,0) and (0,1,0,0) are orthogonal in R4
        # Their dot product is 0.
        # Fidelity is the squared magnitude: dot_product^2 = 0^2 = 0.
        # Distance should be 1 - fidelity = 1 - 0 = 1.0.
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0, 1, 0, 0)
        d = compute_qncd(q1, q2)
        assert np.isclose(d, 1.0)

    def test_antipodal_states(self):
        # (1,0,0,0) and (-1,0,0,0)
        # Dot product is -1. Fidelity is (-1)^2 = 1. Distance should be 0.
        # In SU(2), q and -q represent the same rotation (double cover),
        # but as quantum states |psi> and -|psi> differ by global phase -1.
        # |<-psi|psi>|^2 = |-1|^2 = 1. So they are "same" state projectively.
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(-1, 0, 0, 0)
        d = compute_qncd(q1, q2)
        assert np.isclose(d, 0.0)

    def test_intermediate_state(self):
        # q1 = (1,0,0,0)
        # q2 = (1,1,0,0) / sqrt(2)
        # Dot product = 1/sqrt(2). Fidelity = 0.5. Distance = 0.5.
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(1, 1, 0, 0)
        d = compute_qncd(q1, q2)
        assert np.isclose(d, 0.5)

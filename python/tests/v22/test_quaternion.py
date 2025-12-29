import pytest
import numpy as np
from irh.core.v22.quaternion import Quaternion

class TestQuaternion:

    def test_basic_creation(self):
        q = Quaternion(1.0, 2.0, 3.0, 4.0)
        assert q.w == 1.0
        assert q.x == 2.0
        assert q.y == 3.0
        assert q.z == 4.0

    def test_addition(self):
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        q3 = q1 + q2
        assert q3.w == 6
        assert q3.x == 8
        assert q3.y == 10
        assert q3.z == 12

    def test_multiplication_basis(self):
        # i = (0, 1, 0, 0), j = (0, 0, 1, 0), k = (0, 0, 0, 1)
        i = Quaternion(0, 1, 0, 0)
        j = Quaternion(0, 0, 1, 0)
        k = Quaternion(0, 0, 0, 1)

        # i*j = k
        ij = i * j
        assert ij.w == 0 and ij.x == 0 and ij.y == 0 and ij.z == 1

        # j*i = -k
        ji = j * i
        assert ji.w == 0 and ji.x == 0 and ji.y == 0 and ji.z == -1

        # i*i = -1
        ii = i * i
        assert ii.w == -1 and ii.x == 0 and ii.y == 0 and ii.z == 0

    def test_norm_inverse(self):
        q = Quaternion(1, 0, 0, 0)
        assert q.norm() == 1.0
        assert q.inverse().w == 1.0

        q2 = Quaternion(0, 3, 4, 0)
        assert q2.norm() == 5.0

        inv = q2.inverse()
        prod = q2 * inv
        assert np.isclose(prod.w, 1.0)
        assert np.isclose(prod.x, 0.0)
        assert np.isclose(prod.y, 0.0)
        assert np.isclose(prod.z, 0.0)

    def test_normalize(self):
        q = Quaternion(1, 1, 1, 1)
        qn = q.normalize()
        assert np.isclose(qn.norm(), 1.0)

    def test_numpy_interop(self):
        q = Quaternion(1, 2, 3, 4)
        arr = q.to_numpy()
        assert np.array_equal(arr, np.array([1, 2, 3, 4]))
        q2 = Quaternion.from_numpy(arr)
        assert q2.w == 1

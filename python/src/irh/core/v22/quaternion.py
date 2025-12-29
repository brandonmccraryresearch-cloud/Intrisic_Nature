import numpy as np
from dataclasses import dataclass
from typing import Union, Tuple
from irh.verification import theoretical_reference

@dataclass
class Quaternion:
    """
    Quaternionic field representation on G_inf (SU(2)).
    q = w + xi + yj + zk
    """
    w: float
    x: float
    y: float
    z: float

    @theoretical_reference(
        manuscript="IRH v22.2",
        equation="Sec. 1.1",
        description="Quaternionic algebra non-commutativity (ij = -ji)."
    )
    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        """
        Non-commutative multiplication.
        """
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z

        return Quaternion(
            w = w1*w2 - x1*x2 - y1*y2 - z1*z2,
            x = w1*x2 + x1*w2 + y1*z2 - z1*y2,
            y = w1*y2 - x1*z2 + y1*w2 + z1*x2,
            z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        )

    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def conjugate(self) -> 'Quaternion':
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm_sq(self) -> float:
        return self.w**2 + self.x**2 + self.y**2 + self.z**2

    def norm(self) -> float:
        return np.sqrt(self.norm_sq())

    def inverse(self) -> 'Quaternion':
        n_sq = self.norm_sq()
        if n_sq == 0:
            raise ZeroDivisionError("Cannot invert zero quaternion")
        conj = self.conjugate()
        return Quaternion(conj.w/n_sq, conj.x/n_sq, conj.y/n_sq, conj.z/n_sq)

    def normalize(self) -> 'Quaternion':
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError("Cannot normalize zero quaternion")
        return Quaternion(self.w/n, self.x/n, self.y/n, self.z/n)

    def to_numpy(self) -> np.ndarray:
        return np.array([self.w, self.x, self.y, self.z])

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> 'Quaternion':
        return cls(arr[0], arr[1], arr[2], arr[3])

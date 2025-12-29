import numpy as np
from typing import Union
from irh.core.v22.quaternion import Quaternion
from irh.verification import theoretical_reference

@theoretical_reference(
    manuscript="IRH v22.2",
    equation="Sec. 3.2",
    description="QNCD metric approximated by quantum fidelity 1 - |<q1, q2>|^2."
)
def compute_qncd(q1: Quaternion, q2: Quaternion) -> float:
    """
    Compute Quantum Normalized Compression Distance (QNCD) between two quaternionic states.

    Approximation:
    d_QNCD(g1, g2) = 1 - Fidelity(g1, g2)

    For normalized pure states represented by unit quaternions,
    Fidelity is the squared magnitude of the inner product.

    Inner product of quaternions <q1, q2> = w1*w2 + x1*x2 + y1*y2 + z1*z2
    (considering them as 4D vectors in R^4, which maps to SU(2) topology S^3).

    Parameters
    ----------
    q1, q2 : Quaternion
        States on G_inf. Should be normalized ideally, but we normalize them here to be safe.

    Returns
    -------
    float
        Distance in [0, 1].
    """

    # Ensure normalization
    try:
        u1 = q1.normalize()
        u2 = q2.normalize()
    except ZeroDivisionError:
        # If one is zero vector, define distance as max (1.0)
        return 1.0

    # Euclidean inner product in R^4 corresponds to Re(q1 * conj(q2)) if we strictly follow quaternion algebra?
    # <q1, q2>_R4 = w1w2 + x1x2 + y1y2 + z1z2
    # q1 * conj(q2) = (w1 + v1)(w2 - v2) = w1w2 - w1v2 + v1w2 - v1v2
    # Real part of q1 * conj(q2) is w1w2 - dot(v1, -v2) = w1w2 + dot(v1, v2).
    # Yes, it matches the Euclidean dot product.

    dot_product = u1.w * u2.w + u1.x * u2.x + u1.y * u2.y + u1.z * u2.z

    # Fidelity for pure states |psi>, |phi> is |<psi|phi>|^2
    fidelity = dot_product**2

    # QNCD is 1 - fidelity
    qncd = 1.0 - fidelity

    # Clamp for numerical noise
    return float(np.clip(qncd, 0.0, 1.0))

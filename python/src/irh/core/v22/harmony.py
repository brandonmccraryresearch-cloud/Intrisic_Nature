import numpy as np
from irh.verification import theoretical_reference, get_transparency_engine

class HarmonyFunctional:
    """
    Evaluator for the Harmony Functional H(ε).
    """

    def __init__(self, c_h: float = 0.045935703598):
        # Universal exponent from Cosmic Fixed Point
        self.c_h = c_h
        self.transparency = get_transparency_engine()

    @theoretical_reference(
        manuscript="IRH v22.2",
        equation="Sec. 4.1",
        description="Harmony Functional Γ[Σ] = Tr(L²) - C_H * ln(det' L)"
    )
    def compute_harmony(self, laplacian: np.ndarray) -> float:
        """
        Compute the Harmony Functional for a given configuration represented by its Laplacian.

        Parameters
        ----------
        laplacian : np.ndarray
            The Laplacian matrix of the network/configuration.

        Returns
        -------
        float
            The value of the functional.
        """
        # 1. Tr(L^2)
        # For symmetric L, Tr(L^2) = sum(lambda_i^2)
        # Or just sum of squared elements.
        tr_l2 = np.sum(laplacian**2)

        # 2. ln(det' L) - pseudo-determinant
        # Compute eigenvalues
        try:
            eigvals = np.linalg.eigvalsh(laplacian)
        except np.linalg.LinAlgError:
            # Fallback for non-symmetric
            eigvals = np.linalg.eigvals(laplacian)

        # Filter zero modes (Goldstone modes / translational invariance)
        # Standard graph Laplacian has at least one zero eigenvalue.
        non_zero_eigs = eigvals[np.abs(eigvals) > 1e-10]

        if len(non_zero_eigs) == 0:
            log_det = -np.inf # Degenerate
        else:
            log_det = np.sum(np.log(np.abs(non_zero_eigs)))

        harmony = tr_l2 - self.c_h * log_det

        self.transparency.log_theoretical_step(
            action="Compute Harmony Functional",
            manuscript_ref="IRH v22.2",
            equation_ref="Sec. 4.1",
            details={
                "Tr(L^2)": tr_l2,
                "log_det": log_det,
                "C_H": self.c_h,
                "Harmony": harmony
            }
        )

        return float(harmony)

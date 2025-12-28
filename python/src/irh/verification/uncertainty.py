from dataclasses import dataclass
from typing import Optional, Union
import numpy as np

@dataclass
class UncertaintyValue:
    """
    Represents a value with associated uncertainty and theoretical provenance.
    """
    value: float
    uncertainty: float
    source: str  # e.g., "Analytical Derivation", "Numerical Integration"
    
    def __repr__(self) -> str:
        return f"{self.value} ± {self.uncertainty} ({self.source})"
    
    def __add__(self, other: Union['UncertaintyValue', float]) -> 'UncertaintyValue':
        if isinstance(other, UncertaintyValue):
            new_val = self.value + other.value
            new_unc = np.sqrt(self.uncertainty**2 + other.uncertainty**2)
            return UncertaintyValue(new_val, new_unc, f"Combined({self.source}, {other.source})")
        else:
            return UncertaintyValue(self.value + other, self.uncertainty, self.source)

    def __mul__(self, other: Union['UncertaintyValue', float]) -> 'UncertaintyValue':
        if isinstance(other, UncertaintyValue):
            new_val = self.value * other.value
            # Relative uncertainty propagation
            rel_unc = np.sqrt((self.uncertainty/self.value)**2 + (other.uncertainty/other.value)**2)
            new_unc = abs(new_val) * rel_unc
            return UncertaintyValue(new_val, new_unc, f"Combined({self.source}, {other.source})")
        else:
            return UncertaintyValue(self.value * other, self.uncertainty * abs(other), self.source)

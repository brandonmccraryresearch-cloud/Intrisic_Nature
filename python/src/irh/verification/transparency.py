import sys
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str
    context: Dict[str, Any]

class TransparencyEngine:
    """
    Emits theoretical context logs during execution to ensure algorithmic transparency.
    """
    def __init__(self, verbosity: int = 1):
        self.verbosity = verbosity
        self.logs: list[LogEntry] = []
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
        self.logger = logging.getLogger("IRH_Transparency")

    def log_theoretical_step(self, 
                             action: str, 
                             manuscript_ref: str, 
                             equation_ref: str, 
                             details: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a computational step with its theoretical justification.
        
        Example output:
        [EXEC] Computing cGFT kinetic term S_kin per Eq. 1.1
          ├─ Theoretical formula: ∫[∏dg_i] φ̄·[Σₐ Σᵢ Δₐ^(i)]·φ
          ├─ Result: S_kin = {value}
        """
        if self.verbosity > 0:
            msg = f"Computing {action} per {manuscript_ref}, {equation_ref}"
            print(f"[EXEC] {msg}")
            if details:
                for key, value in details.items():
                    print(f"  ├─ {key}: {value}")
            
            self.logs.append(LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message=msg,
                context=details or {}
            ))

    def verify_invariant(self, name: str, value: Any, expected: Any, tolerance: float = 1e-9) -> bool:
        """
        Verify a theoretical invariant holds.
        """
        import numpy as np
        
        # Handle numpy arrays and floats
        if isinstance(value, (float, int)) or (isinstance(value, np.ndarray) and value.size == 1):
             is_valid = np.isclose(value, expected, atol=tolerance)
             diff = abs(value - expected)
        else:
             # Fallback for now
             is_valid = value == expected
             diff = 0.0

        status = "VERIFIED" if is_valid else "VIOLATED"
        print(f"  └─ {name}: {status} (Expected {expected}, Got {value}, Diff {diff:.2e})")
        
        return bool(is_valid)

# Global instance
_engine = TransparencyEngine()

def get_transparency_engine() -> TransparencyEngine:
    return _engine

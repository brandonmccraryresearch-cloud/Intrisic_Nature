"""
Transparency Engine for IRH v22.2

Provides runtime transparency logging for computational steps,
ensuring full traceability of all theoretical derivations.

Theoretical Reference:
    IRH v21.4 Part 1, Theoretical Correspondence Mandate
    Section: Algorithmic Transparency Requirements
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TransparencyLog:
    """Container for a transparency log entry."""
    
    timestamp: datetime
    level: str
    operation: str
    theoretical_ref: Optional[str] = None
    formula: Optional[str] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TransparencyEngine:
    """
    Runtime transparency engine for IRH computations.
    
    Logs computational steps with full theoretical context,
    enabling complete provenance tracking.
    
    Usage:
        engine = TransparencyEngine()
        engine.log_computation(
            operation="compute_beta_functions",
            theoretical_ref="IRH v21.4 Part 1 §1.2, Eq. 1.13",
            inputs={"lambda": 52.638, "gamma": 105.276, "mu": 157.914},
            outputs={"beta_lambda": 0.0, "beta_gamma": 0.0, "beta_mu": 0.0}
        )
    """
    
    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger("irh.transparency")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self.logs: List[TransparencyLog] = []
    
    def log_computation(
        self,
        operation: str,
        theoretical_ref: Optional[str] = None,
        formula: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None,
        outputs: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        level: str = "INFO"
    ):
        """
        Log a computational step with theoretical context.
        
        Parameters
        ----------
        operation : str
            Name of the operation being performed
        theoretical_ref : str, optional
            Reference to IRH manuscript (e.g., "IRH v21.4 Part 1 §1.2, Eq. 1.13")
        formula : str, optional
            Mathematical formula being implemented
        inputs : dict, optional
            Input parameters and their values
        outputs : dict, optional
            Output results
        metadata : dict, optional
            Additional metadata (convergence status, precision, etc.)
        level : str, optional
            Log level (INFO, DEBUG, WARNING, ERROR)
        """
        log_entry = TransparencyLog(
            timestamp=datetime.now(),
            level=level,
            operation=operation,
            theoretical_ref=theoretical_ref,
            formula=formula,
            inputs=inputs or {},
            outputs=outputs or {},
            metadata=metadata or {}
        )
        
        self.logs.append(log_entry)
        
        # Format log message
        msg_parts = [f"Operation: {operation}"]
        if theoretical_ref:
            msg_parts.append(f"Reference: {theoretical_ref}")
        if formula:
            msg_parts.append(f"Formula: {formula}")
        if inputs:
            msg_parts.append(f"Inputs: {inputs}")
        if outputs:
            msg_parts.append(f"Outputs: {outputs}")
        if metadata:
            msg_parts.append(f"Metadata: {metadata}")
        
        message = " | ".join(msg_parts)
        
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)
    
    def log_step(self, step_name: str, details: str = "", **kwargs):
        """Log a computation step."""
        self.log_computation(
            operation=step_name,
            metadata={"details": details, **kwargs},
            level="DEBUG"
        )
    
    def log_result(self, operation: str, result: Any, **kwargs):
        """Log a computation result."""
        self.log_computation(
            operation=operation,
            outputs={"result": result},
            metadata=kwargs,
            level="INFO"
        )
    
    def log_error(self, operation: str, error: str, **kwargs):
        """Log an error."""
        self.log_computation(
            operation=operation,
            metadata={"error": error, **kwargs},
            level="ERROR"
        )
    
    def get_logs(self) -> List[TransparencyLog]:
        """Get all logged entries."""
        return self.logs.copy()
    
    def clear_logs(self):
        """Clear all logged entries."""
        self.logs.clear()
    
    def export_logs(self) -> List[Dict[str, Any]]:
        """Export logs as list of dictionaries."""
        return [
            {
                "timestamp": log.timestamp.isoformat(),
                "level": log.level,
                "operation": log.operation,
                "theoretical_ref": log.theoretical_ref,
                "formula": log.formula,
                "inputs": log.inputs,
                "outputs": log.outputs,
                "metadata": log.metadata
            }
            for log in self.logs
        ]


# Global transparency engine instance
_global_engine = None


def get_transparency_engine() -> TransparencyEngine:
    """Get the global transparency engine instance."""
    global _global_engine
    if _global_engine is None:
        _global_engine = TransparencyEngine()
    return _global_engine


def log_transparency(operation: str, **kwargs):
    """Convenience function to log to the global transparency engine."""
    engine = get_transparency_engine()
    engine.log_computation(operation, **kwargs)

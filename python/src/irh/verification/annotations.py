from typing import Any, Callable, Optional, TypeVar
import functools
import inspect

F = TypeVar('F', bound=Callable[..., Any])

def theoretical_reference(manuscript: str, equation: str, description: Optional[str] = None) -> Callable[[F], F]:
    """
    Decorator to link code to specific theoretical references in the manuscript.
    
    Parameters
    ----------
    manuscript : str
        The manuscript identifier (e.g., 'IRH v22.1').
    equation : str
        The equation number or theorem identifier (e.g., 'Eq. 1.1', 'Theorem 3.1').
    description : str, optional
        Brief description of the theoretical concept being implemented.
    """
    def decorator(func: F) -> F:
        if not hasattr(func, '_theoretical_refs'):
            func._theoretical_refs = []  # type: ignore
        
        ref = {
            'manuscript': manuscript,
            'equation': equation,
            'description': description
        }
        func._theoretical_refs.append(ref)  # type: ignore
        
        # Add to docstring if not present
        doc_addition = f"\n    Theoretical Reference: {manuscript}, {equation}"
        if description:
            doc_addition += f" - {description}"
        
        if func.__doc__:
            if "Theoretical Reference:" not in func.__doc__:
                func.__doc__ += doc_addition
        else:
            func.__doc__ = doc_addition.strip()
            
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        
        return wrapper # type: ignore
    return decorator

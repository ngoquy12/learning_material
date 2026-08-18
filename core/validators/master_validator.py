"""
core/validators/master_validator.py
Unified Master Validator Engine for Elearning Agent Architecture.
Provides a plug-in based registry for pedagogical and technical validators.
"""

from typing import Tuple, List, Dict, Any, Union, Callable

# Global registry mapping resource type strings to validator functions
VALIDATOR_REGISTRY: Dict[str, Callable[[Any, Dict[str, Any]], Tuple[bool, List[str]]]] = {}

def register_validator(*resource_types: str):
    """
    Decorator to register a validator function for specific resource types.
    """
    def decorator(func: Callable[[Any, Dict[str, Any]], Tuple[bool, List[str]]]):
        for rt in resource_types:
            VALIDATOR_REGISTRY[rt.upper().strip()] = func
        return func
    return decorator

def validate_resource(
    resource_type: str,
    content_data: Union[str, Dict[str, Any], List[Dict[str, Any]]],
    metadata: Dict[str, Any] = None
) -> Tuple[bool, List[str]]:
    """
    Unified master entrypoint for validation.
    Dynamically routes validation to registered plugins.
    """
    res_type = (resource_type or "").upper().strip()
    metadata = metadata or {}
    
    # Return True by default if no validator is registered for this type
    validator_func = VALIDATOR_REGISTRY.get(res_type)
    if not validator_func:
        # Fallback dynamic imports to ensure modules are loaded and registered
        _ensure_validators_imported()
        validator_func = VALIDATOR_REGISTRY.get(res_type)
        
    if validator_func:
        try:
            return validator_func(content_data, metadata)
        except Exception as e:
            return False, [f"Lỗi khi thực thi Validator cho {res_type}: {str(e)}"]
            
    return True, []

def _ensure_validators_imported():
    """Import modules to trigger their @register_validator decorations."""
    try:
        import core.validators.reading_validator
        import core.validators.quiz_validator
        import core.validators.practice_validator
        import core.validators.project_validator
        import core.validators.session_compiler_validator
    except ImportError as e:
        print(f"  [Validator Warning] Failed to import sub-validators: {e}")


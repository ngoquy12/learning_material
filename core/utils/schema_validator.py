"""
core/utils/schema_validator.py
Type-Safe Schema Validation and Normalization Engine using Pydantic v2.
Validates raw dictionaries from LLM parsers against Pydantic models with auto-coercion and graceful defaults.
"""

from typing import Type, TypeVar, Tuple, List, Dict, Any, Optional
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

def validate_schema(model_cls: Type[T], raw_data: Any) -> Tuple[bool, Optional[T], List[str]]:
    """
    Validates raw dictionary or list data against a Pydantic model class.
    Returns (is_valid, validated_instance, list_of_error_messages).
    """
    if raw_data is None:
        return False, None, ["Dữ liệu đầu vào bị rỗng (None)."]

    try:
        if isinstance(raw_data, model_cls):
            return True, raw_data, []
        if isinstance(raw_data, dict):
            instance = model_cls.model_validate(raw_data)
            return True, instance, []
        if isinstance(raw_data, list) and hasattr(model_cls, "__root__"):
            instance = model_cls.model_validate(raw_data)
            return True, instance, []
        
        # Try direct initialization
        instance = model_cls(**raw_data)
        return True, instance, []
    except ValidationError as err:
        errors = [f"{e['loc']}: {e['msg']}" for e in err.errors()]
        return False, None, errors
    except Exception as e:
        return False, None, [str(e)]


def validate_and_dump(model_cls: Type[T], raw_data: Any, default_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Validates raw data against model_cls and dumps as clean dictionary.
    Falls back to default_dict if validation fails.
    """
    is_valid, instance, errors = validate_schema(model_cls, raw_data)
    if is_valid and instance is not None:
        return instance.model_dump()
    return default_dict or (raw_data if isinstance(raw_data, dict) else {})

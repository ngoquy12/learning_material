"""
core/validators/master_validator.py
Unified Master Validator Engine for Elearning Agent Architecture.
Provides a single orchestrator function `validate_resource` covering all 5 resource types:
- READING
- SLIDE
- QUIZ
- PRACTICE
- PROJECT
"""

from typing import Tuple, List, Dict, Any, Union
from core.validators.reading_validator import validate_reading_material
from core.validators.slide_validator import validate_slide_presentation
from core.validators.quiz_validator import validate_and_shuffle_quiz
from core.validators.practice_validator import validate_practice_exercise
from core.validators.project_validator import validate_project_spec
from core.validators.session_compiler_validator import validate_compiled_session_html
from core.validators.hyperframes_validator import validate_hyperframes_script

def validate_resource(
    resource_type: str,
    content_data: Union[str, Dict[str, Any], List[Dict[str, Any]]],
    metadata: Dict[str, Any] = None
) -> Tuple[bool, List[str]]:
    """
    Unified master entrypoint for programmatic validation across all learning material types.
    Returns (is_valid, list_of_error_strings).
    """
    res_type = (resource_type or "").upper().strip()
    metadata = metadata or {}
    
    if res_type in ["VIDEO_SCRIPT", "HYPERFRAMES"]:
        if isinstance(content_data, dict):
            return validate_hyperframes_script(content_data, metadata)
            
    elif res_type in ["COMPILED_SESSION", "READING_ALL", "SESSION_SLIDES"]:
        return validate_compiled_session_html(content_data)
        
    elif res_type == "READING":
        if isinstance(content_data, str):
            return validate_reading_material(content_data, metadata)
        elif isinstance(content_data, dict):
            content_str = content_data.get("html") or str(content_data)
            return validate_reading_material(content_str, metadata)
            
    elif res_type == "SLIDE":
        if isinstance(content_data, list):
            return validate_slide_presentation(content_data, metadata)
        elif isinstance(content_data, dict):
            scenes = content_data.get("scenes", [])
            return validate_slide_presentation(scenes, metadata)
            
    elif res_type == "QUIZ":
        if isinstance(content_data, list):
            is_ok, _, errs = validate_and_shuffle_quiz(content_data)
            return is_ok, errs
        elif isinstance(content_data, dict):
            qs = content_data.get("questions", [])
            is_ok, _, errs = validate_and_shuffle_quiz(qs)
            return is_ok, errs
            
    elif res_type in ["PRACTICE", "HOMEWORK"]:
        if isinstance(content_data, dict):
            return validate_practice_exercise(content_data, metadata)
            
    elif res_type in ["PROJECT", "MINI_PROJECT"]:
        if isinstance(content_data, dict):
            return validate_project_spec(content_data, metadata)
            
    return True, []

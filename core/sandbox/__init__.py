"""
core/sandbox package initialization.
"""
from typing import Dict, Any
from core.sandbox.code_executor import (
    CodeSandboxExecutor,
    ExecutionResult,
    execute_code_snippet
)

from core.sandbox.polyglot_runner import (
    detect_language,
    execute_polyglot_code,
    normalize_language
)

def execute_code_safely(code: str, language: str = "python") -> Dict[str, Any]:
    """Executes code safely inside sandbox environment for any supported language."""
    from core.sandbox.polyglot_runner import execute_polyglot_code
    res = execute_polyglot_code(code, language=language)
    return res.to_dict()

__all__ = [
    "CodeSandboxExecutor",
    "ExecutionResult",
    "execute_code_snippet",
    "execute_code_safely",
    "detect_language",
    "execute_polyglot_code",
    "normalize_language"
]

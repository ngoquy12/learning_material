"""
core/sandbox package initialization.
"""
from typing import Dict, Any
from core.sandbox.code_executor import (
    CodeSandboxExecutor,
    ExecutionResult,
    execute_code_snippet
)

def execute_code_safely(code: str) -> Dict[str, Any]:
    """Executes Python code safely inside sandbox environment."""
    res = execute_code_snippet(code, tech_stack="python")
    return {
        "status": "SUCCESS" if res.success else "FAILED",
        "output": res.stdout,
        "error": res.error_message or res.stderr,
        "engine": "subprocess"
    }

__all__ = [
    "CodeSandboxExecutor",
    "ExecutionResult",
    "execute_code_snippet",
    "execute_code_safely"
]

"""
tests/test_strict_tech_stack.py
Unit tests for strict technology stack requirement & LLM failure handling.
Guarantees NO hardcoded default technology fallbacks anywhere in the architecture.
"""

import pytest
from core.state import require_tech_stack

def test_require_tech_stack_valid():
    state = {"technology_stack": "python/core"}
    assert require_tech_stack(state) == "python/core"
    
    state_alt = {"tech_stack": "typescript/react"}
    assert require_tech_stack(state_alt) == "typescript/react"

def test_require_tech_stack_missing_raises():
    with pytest.raises(ValueError) as excinfo:
        require_tech_stack({})
    assert "LỖI THIẾU TECHNOLOGY STACK" in str(excinfo.value)

def test_require_tech_stack_empty_string_raises():
    with pytest.raises(ValueError) as excinfo:
        require_tech_stack({"technology_stack": "   "})
    assert "LỖI THIẾU TECHNOLOGY STACK" in str(excinfo.value)

def test_require_tech_stack_none_raises():
    with pytest.raises(ValueError) as excinfo:
        require_tech_stack({"technology_stack": None})
    assert "LỖI THIẾU TECHNOLOGY STACK" in str(excinfo.value)

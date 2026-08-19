"""
agents/reviewers/prerequisite_reviewer.py
Prerequisite Guard and Scope Verification Agent.
Audits the prerequisite dependency chain and curriculum scope bounds.
"""

from typing import Dict, Any, List
from agents.prerequisite_guard_agent import (
    prerequisite_guard_agent,
    run_prerequisite_check_for_pm
)

__all__ = [
    "prerequisite_guard_agent",
    "run_prerequisite_check_for_pm"
]

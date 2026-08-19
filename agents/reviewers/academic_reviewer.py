"""
agents/reviewers/academic_reviewer.py
Academic & Pedagogical Objective Reviewer Agent.
Audits learning outcomes, Bloom taxonomy alignment, and syllabus contracts.
"""

from typing import Dict, Any
from agents.reviewer_agents import (
    objective_reviewer_agent,
    mindmap_reviewer,
    pm_reviewer_agent,
    pm_updater_agent,
    check_forbidden_keywords,
    check_forbidden_emojis,
    check_unaccented_vietnamese,
    check_knowledge_scope_violations,
    check_structural_completeness
)

__all__ = [
    "objective_reviewer_agent",
    "mindmap_reviewer",
    "pm_reviewer_agent",
    "pm_updater_agent",
    "check_forbidden_keywords",
    "check_forbidden_emojis",
    "check_unaccented_vietnamese",
    "check_knowledge_scope_violations",
    "check_structural_completeness"
]

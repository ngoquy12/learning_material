"""
agents/homework_agents.py — Backward-compatible facade module.
All homework generation logic and Pydantic v2 validation are modularized inside agents/creators/homework_creator.py.
"""

from agents.creators.homework_creator import (
    generate_homework_exercise,
    generate_session_homework_suite,
    clean_markdown_formulas,
    sanitize_homework_markdown
)

# Backwards compatibility aliases
homework_creator_agent = generate_homework_exercise
generate_session_homework = generate_session_homework_suite
session_homework_pipeline = generate_session_homework_suite

__all__ = [
    "generate_homework_exercise",
    "generate_session_homework_suite",
    "homework_creator_agent",
    "generate_session_homework",
    "session_homework_pipeline",
    "clean_markdown_formulas",
    "sanitize_homework_markdown"
]

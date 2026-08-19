"""
agents/pm_reviewer_agent.py
AI PM Reviewer & Strict Academic Quality Assurance Auditor Agent.
Acts as an un-compromising Academic Quality Director for Rikkei Education.
Delegates programmatic checks to core.pm_validators engine.
"""

from typing import Dict, Any, List, Tuple
from core.pm_validators import (
    HYPE_WORDS,
    DIFFICULTY_BADGES,
    VAGUE_OUTCOME_VERBS,
    BLOOM_ACTION_VERBS,
    lint_pm_syllabus,
    audit_reading_html_quality_gate,
    audit_exercise_quality_gate
)

def pm_reviewer_agent(
    pm_data: List[Dict[str, Any]],
    config_data: Dict[str, Any] = None,
    course_info: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Main entry point for PM Reviewer & Strict Academic Quality Assurance Auditor Agent.

    Evaluates generated PM syllabus using programmatic strict linter + LLM Academic Director evaluation pass.
    Requires Quality Score >= 90 and 0 ERRORs to approve.
    """
    config_data = config_data or {}
    course_info = course_info or {}

    clos = course_info.get("clos", [])
    plos = course_info.get("plos", [])
    main_content = course_info.get("main_content", "")
    tech_stack = config_data.get("tech_stack", "")
    session_budget = config_data.get("session_budget", {})
    class_config = config_data.get("class_configuration", {})
    sessions_per_day = class_config.get("sessions_per_day", 1)

    print("  [PM Auditor - Strict Mode ⚖️] Running deep structural & pedagogical linter...")
    is_valid, score, rule_violations, review_logs = lint_pm_syllabus(
        pm_data=pm_data,
        tech_stack=tech_stack,
        sessions_per_day=sessions_per_day,
        clos=clos,
        plos=plos,
        session_budget=session_budget,
        main_content=main_content
    )

    feedback_parts = []
    if rule_violations:
        feedback_parts.append("LIST OF PEDAGOGICAL & FORMATTING RULE VIOLATIONS (MUST BE FULLY RESOLVED):")
        for idx, err in enumerate(rule_violations, 1):
            feedback_parts.append(f"{idx}. {err}")

    if is_valid and score >= 90:
        feedback_summary = f"APPROVED: PM Syllabus achieves excellent academic standards ({score}/100)."
    else:
        feedback_summary = f"REJECTED: PM Syllabus failed strict academic quality gate (Score: {score}/100, Minimum required: 90/100). Please resolve all issues listed below."

    full_feedback = feedback_summary + "\n\n" + "\n".join(feedback_parts) if feedback_parts else feedback_summary

    result = {
        "is_approved": is_valid,
        "score": score,
        "review_logs": review_logs,
        "rule_violations": rule_violations,
        "feedback": full_feedback
    }

    if is_valid:
        print(f"  [PM Auditor ✅] APPROVED (Quality Score: {score}/100)")
    else:
        print(f"  [PM Auditor ⚠️] REJECTED (Quality Score: {score}/100, Violations: {len(rule_violations)})")
        for log in review_logs[:5]:
            print(f"      - [{log['level']}] {log['message']}")

    return result

__all__ = [
    "HYPE_WORDS",
    "DIFFICULTY_BADGES",
    "VAGUE_OUTCOME_VERBS",
    "BLOOM_ACTION_VERBS",
    "lint_pm_syllabus",
    "pm_reviewer_agent",
    "audit_reading_html_quality_gate",
    "audit_exercise_quality_gate"
]

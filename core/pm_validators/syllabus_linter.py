"""
core/pm_validators/syllabus_linter.py
Unified PM Syllabus Linter Engine coordinating all specialized validators.
"""

from typing import Dict, Any, List, Tuple
from core.pm_validators.structure_validator import validate_syllabus_structure
from core.pm_validators.academic_tone_validator import validate_academic_tone
from core.pm_validators.granularity_validator import validate_pm_granularity
from core.pm_validators.scope_continuity_validator import validate_scope_continuity
from core.pm_validators.clo_coverage_validator import validate_clo_coverage

def lint_pm_syllabus(
    pm_data: List[Dict[str, Any]],
    tech_stack: str = "",
    sessions_per_day: int = 1,
    clos: List[str] = None,
    plos: List[str] = None,
    session_budget: Dict[str, Any] = None,
    main_content: str = ""
) -> Tuple[bool, int, List[str], List[Dict[str, Any]]]:
    """
    Strict Rule Engine for PM Syllabus Validation coordinating 5 specialized validators:
    1. Structure & Pacing Validator
    2. Academic Tone & Bloom Action Verbs Validator
    3. 5-Column Granularity Validator
    4. Scope Continuity & Boundary Validator
    5. CLO & PLO Coverage Validator

    Returns:
        (is_valid: bool, score: int, rule_violations: List[str], review_logs: List[Dict[str, Any]])
    """
    clos = clos or []
    plos = plos or []
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    total_deductions = 0

    if not pm_data:
        return False, 0, ["Lỗi nghiêm trọng: PM rỗng, không chứa session nào."], [{"level": "CRITICAL", "message": "PM rỗng."}]

    # 1. Structure & Pacing Validation
    d1, v1, l1 = validate_syllabus_structure(
        pm_data=pm_data,
        tech_stack=tech_stack,
        sessions_per_day=sessions_per_day,
        session_budget=session_budget,
        main_content=main_content
    )
    total_deductions += d1
    rule_violations.extend(v1)
    review_logs.extend(l1)

    # 2. Academic Tone & Bloom Action Verbs Validation
    d2, v2, l2 = validate_academic_tone(
        pm_data=pm_data,
        tech_stack=tech_stack,
        main_content=main_content
    )
    total_deductions += d2
    rule_violations.extend(v2)
    review_logs.extend(l2)

    # 3. 5-Column Granularity Validation
    d3, v3, l3 = validate_pm_granularity(pm_data=pm_data)
    total_deductions += d3
    rule_violations.extend(v3)
    review_logs.extend(l3)

    # 4. Scope Continuity & Technology Boundary Validation
    d4, v4, l4 = validate_scope_continuity(
        pm_data=pm_data,
        tech_stack=tech_stack,
        clos=clos,
        plos=plos,
        main_content=main_content
    )
    total_deductions += d4
    rule_violations.extend(v4)
    review_logs.extend(l4)

    # 5. CLO & PLO Keyword Coverage Validation
    d5, v5, l5 = validate_clo_coverage(
        pm_data=pm_data,
        clos=clos,
        plos=plos,
        main_content=main_content
    )
    total_deductions += d5
    rule_violations.extend(v5)
    review_logs.extend(l5)

    final_score = max(0, min(100, 100 - total_deductions))
    is_valid = len([log for log in review_logs if log["level"] == "ERROR"]) == 0 and final_score >= 90

    return is_valid, final_score, rule_violations, review_logs

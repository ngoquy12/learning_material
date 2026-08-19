"""
core/pm_validators/scope_continuity_validator.py
Validates Knowledge Scope Boundaries, Technology Isolation, and Progressive Vocabulary Continuity.
"""

import re
from typing import Dict, Any, List, Tuple
from core.pm_validators.constants import (
    extract_out_of_scope_technologies,
    get_session_num
)

def validate_scope_continuity(
    pm_data: List[Dict[str, Any]],
    tech_stack: str = "",
    clos: List[str] = None,
    plos: List[str] = None,
    main_content: str = ""
) -> Tuple[int, List[str], List[Dict[str, Any]]]:
    """
    Validates scope boundaries, technology cross-contamination, and progressive concept accumulation.
    Returns: (penalty_score_deductions, rule_violations, review_logs)
    """
    clos = clos or []
    plos = plos or []
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    deductions = 0

    # 1. Out-of-scope technology cross-contamination check
    if tech_stack:
        forbidden_techs = extract_out_of_scope_technologies(tech_stack, clos, plos, main_content)

        if forbidden_techs:
            for s in pm_data:
                snum = get_session_num(s, 0)
                combined_text = f"{s.get('title', '')} {s.get('content_scope', '')} {s.get('expected_outcome', '')}"
                for l in s.get("lessons", []):
                    combined_text += f" {l.get('title', '')} {l.get('content_scope', '')}"

                combined_lower = combined_text.lower()
                for ft in forbidden_techs:
                    if re.search(rf"\b{re.escape(ft)}\b", combined_lower):
                        msg = f"Session {snum:02d} vi phạm ranh giới công nghệ cấm: chứa từ khóa '{ft}' không thuộc phạm vi môn học '{tech_stack}'."
                        rule_violations.append(msg)
                        review_logs.append({"level": "ERROR", "message": msg})
                        deductions += 10

    # 2. Scope continuity: check forbidden_scope vs allowed_scope and historical taught concepts
    taught_concepts = set()
    for s in pm_data:
        snum = get_session_num(s, 0)
        lessons = s.get("lessons", [])
        for l in lessons:
            lnum = l.get("lesson_num", 0)
            forbidden = l.get("forbidden_scope", "").lower()
            allowed = l.get("allowed_scope", "").lower()
            content = l.get("content_scope", "").lower()

            if forbidden and allowed:
                f_clean = forbidden.replace("cấm:", "").strip()
                a_clean = allowed.replace("đã học:", "").strip()

                f_terms = [t.strip() for t in f_clean.split(";") if t.strip()]
                a_terms = [t.strip() for t in a_clean.split(";") if t.strip()]

                overlap = [t for t in a_terms if t in f_terms and len(t) > 2]
                if overlap:
                    msg = f"Session {snum:02d} Lesson {lnum} mâu thuẫn Scope: Thuật ngữ '{', '.join(overlap)}' xuất hiện ở cả ĐÃ HỌC và CẤM."
                    rule_violations.append(msg)
                    review_logs.append({"level": "ERROR", "message": msg})
                    deductions += 5

                # Check if concept taught previously is erroneously still forbidden
                for concept in taught_concepts:
                    if len(concept) > 3 and concept in f_terms:
                        msg = f"Session {snum:02d} Lesson {lnum} vi phạm giải phóng Scope: Thuật ngữ '{concept}' đã học ở các buổi trước nhưng vẫn nằm trong CẤM."
                        rule_violations.append(msg)
                        review_logs.append({"level": "ERROR", "message": msg})
                        deductions += 5
                        break

            # Add current content terms to taught concepts
            for term in content.replace(";", ",").split(","):
                clean_t = term.strip().lower()
                if len(clean_t) > 3:
                    taught_concepts.add(clean_t)

    return deductions, rule_violations, review_logs

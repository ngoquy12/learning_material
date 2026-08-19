"""
core/pm_validators/granularity_validator.py
Validates the 5 Core PM Columns for Granularity, Specificity, and Anti-Laziness standards.
"""

from typing import Dict, Any, List, Tuple
from core.pm_validators.constants import get_session_num

def validate_pm_granularity(pm_data: List[Dict[str, Any]]) -> Tuple[int, List[str], List[Dict[str, Any]]]:
    """
    Validates anti-laziness and granularity rules for content_scope, expected_outcome,
    forbidden_scope ('CẤM:'), and allowed_scope ('ĐÃ HỌC:').
    Returns: (penalty_score_deductions, rule_violations, review_logs)
    """
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    deductions = 0

    for s in pm_data:
        snum = get_session_num(s, 0)
        lessons = s.get("lessons", [])
        for l in lessons:
            lnum = l.get("lesson_num", 0)
            l_scope = l.get("content_scope", "").strip()
            l_outcome_raw = l.get("expected_outcome", "").strip()
            l_forbidden = l.get("forbidden_scope", "").strip()
            l_allowed = l.get("allowed_scope", "").strip()

            # Check 1: content_scope lazy/short
            if len(l_scope) < 20 or any(lazy in l_scope.lower() for lazy in ["nói chung", "các lệnh cơ bản", "bài trước", "v.v.", "..."]):
                msg = f"Session {snum:02d} Lesson {lnum} 'Nội Dung Chi Tiết (Lesson Scope)' quá ngắn hoặc trình bày chung chung lười biếng ('{l_scope}'). Bắt buộc liệt kê chính xác các khái niệm, cú pháp và hàm."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 5

            # Check 2: expected_outcome lazy/short
            if len(l_outcome_raw) < 20:
                msg = f"Session {snum:02d} Lesson {lnum} 'Kết Quả Mong Đợi' quá ngắn gọn thiếu chi tiết ('{l_outcome_raw}')."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 5

            # Check 3: forbidden_scope lazy/missing/placeholder
            if len(l_forbidden) < 15 or not l_forbidden.startswith("CẤM:") or any(lazy in l_forbidden.lower() for lazy in ["kiến thức chưa học", "kiến thức nâng cao", "phần nâng cao", "các phần khác"]):
                msg = f"Session {snum:02d} Lesson {lnum} 'Phạm Vi CẤM DÙNG' trình bày chung chung hoặc thiếu tiền tố 'CẤM:' ('{l_forbidden}'). Bắt buộc liệt kê danh sách cụ thể các từ khóa/cú pháp cấm."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 5

            # Check 4: allowed_scope lazy/missing/placeholder
            if len(l_allowed) < 15 or not l_allowed.startswith("ĐÃ HỌC:") or any(lazy in l_allowed.lower() for lazy in ["các bài trước", "kiến thức cũ", "đã học ở trên", "kiến thức đã học"]):
                msg = f"Session {snum:02d} Lesson {lnum} 'Phạm Vi ĐÃ HỌC' trình bày chung chung hoặc thiếu tiền tố 'ĐÃ HỌC:' ('{l_allowed}'). Bắt buộc liệt kê chính xác tích lũy các kiến thức/hàm đã học."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 5

    return deductions, rule_violations, review_logs

"""
core/pm_validators/clo_coverage_validator.py
Validates CLO and PLO alignment and technical keyword coverage across PM Syllabus.
"""

import re
import json
from typing import Dict, Any, List, Tuple

def validate_clo_coverage(
    pm_data: List[Dict[str, Any]],
    clos: List[str] = None,
    plos: List[str] = None,
    main_content: str = ""
) -> Tuple[int, List[str], List[Dict[str, Any]]]:
    """
    Validates dynamic CLO/PLO and Main Content keyword coverage across the entire PM Syllabus.
    Returns: (penalty_score_deductions, rule_violations, review_logs)
    """
    clos = clos or []
    plos = plos or []
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    deductions = 0

    full_pm_text = json.dumps(pm_data, ensure_ascii=False).lower()
    combined_targets = " ".join(clos + plos + [main_content]).lower()

    # Extract target technical noun terms dynamically
    raw_tokens = re.split(r'[\s,.;:()\[\]"\'\/\\-]+', combined_targets)
    stop_words = {
        "mục", "tiêu", "vận", "dụng", "thành", "thạo", "sử", "dụng", "nắm", "vững",
        "học", "viên", "hiểu", "biết", "thực", "hiện", "trong", "cho", "của", "và",
        "hoặc", "theo", "chuẩn", "đầu", "ra", "môn", "clo", "clo1", "clo2", "plo",
        "plo1", "plo2", "plo3", "plo4", "plo5", "plo6"
    }

    extracted_terms = set()
    for token in raw_tokens:
        t = token.strip().lower()
        if len(t) >= 4 and t not in stop_words and not t.isdigit():
            extracted_terms.add(t)

    # Verify coverage of extracted CLO/PLO terms across syllabus
    missing_key_terms = [term for term in sorted(extracted_terms) if term not in full_pm_text]
    if len(missing_key_terms) > 3:
        sample_missing = ", ".join(missing_key_terms[:3])
        msg = f"Thiếu nội dung bao phủ một số từ khóa chuyên môn từ chuẩn đầu ra CLO/PLO: '{sample_missing}' chưa được ghi nhận rõ ràng trong PM."
        rule_violations.append(msg)
        review_logs.append({"level": "WARNING", "message": msg})
        deductions += 5

    # Explicit individual CLO coverage check
    if clos:
        for idx, clo in enumerate(clos, 1):
            clo_clean = re.sub(r'^(CLO|PLO)\s*\d+[:\s]*', '', str(clo), flags=re.IGNORECASE).strip()
            clo_words = [w.strip().lower() for w in re.split(r'[\s,.;:()]+', clo_clean) if len(w.strip()) > 3]
            clo_words = [w for w in clo_words if not re.match(r'^(clo|plo)\d*$', w) and w not in ["sử", "dụng", "thành", "thạo", "thao", "tác", "xử", "lý", "biết", "hiểu", "thực", "hiện"]]

            matched = any(w in full_pm_text for w in clo_words)
            if not matched and len(clo_words) > 0:
                msg = f"Lỗi sư phạm: CLO {idx} ('{clo}') chưa được bao phủ rõ ràng trong bất kỳ buổi học nào của PM."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 10

    return deductions, rule_violations, review_logs

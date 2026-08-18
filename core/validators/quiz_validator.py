# core/validators/quiz_validator.py
"""
Quiz & Assessment Linter & Validator
Strictly enforces the 9 Mandatory Principles of E-Learning Quiz Design and System Rules.
"""
import re
import json
from typing import List, Dict, Tuple, Any, Union
from core.validators.master_validator import register_validator

BANNED_AI_BUZZWORDS = [
    r"\bbẫy\b", r"\bbẫy\s+lỗi\b", r"\bbẫy\s+lập\s+trình\b", r"\bbẫy\s+cú\s+pháp\b", r"\bbẫy\s+logic\b",
    r"\bgotcha\b", r"\banti-pattern\b", r"\bkhám\s+phá\b", r"\bbí\s+kíp\b", r"\bthần\s+thánh\b"
]

CONTEXT_REFERENCING_PHRASES = [
    r"ở\s+slide", r"trong\s+slide", r"slide\s+bài\s+giảng", r"trong\s+bài\s+giảng",
    r"theo\s+bài\s+giảng", r"theo\s+video", r"trong\s+video", r"từ\s+lời\s+giảng\s+viên",
    r"theo\s+lời\s+giảng\s+viên", r"trong\s+bài\s+đọc", r"bài\s+đọc\s+có\s+đề\s+cập",
    r"theo\s+phần", r"từ\s+một\s+nguồn\s+nào\s+đó"
]

FORBIDDEN_GENERIC_OPTIONS = [
    r"tất\s+cả\s+đều\s+đúng", r"tất\s+cả\s+đều\s+sai",
    r"cả\s+[a-d]\s+và\s+[a-d]\s+đều\s+đúng", r"cả\s+[a-d]\s+và\s+[a-d]\s+đều\s+sai"
]

def validate_quiz_json(quiz_data: List[Dict[str, Any]], lesson_scope_rules: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates quiz JSON structure and quality.
    """
    errors = []
    
    for i, item in enumerate(quiz_data, 1):
        question = item.get("question", "")
        options = item.get("options", [])
        explanation = item.get("explanation", "")
        
        full_text = f"{question} {' '.join(options)} {explanation}"
        
        # Check 1: Banned AI Buzzwords
        for pat in BANNED_AI_BUZZWORDS:
            if re.search(pat, full_text, re.IGNORECASE):
                errors.append(f"Câu {i}: Vi phạm Luật #10 - Tồn tại từ lóng AI bị cấm: '{re.search(pat, full_text, re.IGNORECASE).group(0)}'")
                
        # Check 2: Context Referencing
        for pat in CONTEXT_REFERENCING_PHRASES:
            if re.search(pat, full_text, re.IGNORECASE):
                errors.append(f"Câu {i}: Vi phạm Luật #4.1 #4 - Tồn tại cụm từ tham chiếu ngữ cảnh: '{re.search(pat, full_text, re.IGNORECASE).group(0)}'")
                
        # Check 3: Forbidden Generic Options
        for opt_idx, opt in enumerate(options):
            for pat in FORBIDDEN_GENERIC_OPTIONS:
                if re.search(pat, opt, re.IGNORECASE):
                    errors.append(f"Câu {i} - Đáp án {opt_idx+1}: Vi phạm Luật #4.1 #5 - Tồn tại phương án sáo rỗng bị cấm: '{opt}'")
                    
        # Check 4: Markdown Fence Syntax Errors (Incorrect closing fence ```python instead of ```)
        if re.search(r"```[a-z]*[\s\S]+?```[a-z]+", question) or any(re.search(r"```[a-z]*[\s\S]+?```[a-z]+", opt) for opt in options):
            errors.append(f"Câu {i}: Vi phạm Cú pháp - Thẻ đóng code block bị lỗi nhầm thành ```python thay vì ```")

        # Check 5: Instant Feedback Quality Check for E-Learning
        instant_fb = item.get("instant_feedback")
        if instant_fb is not None and not str(instant_fb).strip():
            errors.append(f"Câu {i}: Vi phạm Quy chuẩn Quiz E-Learning - Trường instant_feedback bị để rỗng")

    return len(errors) == 0, errors


@register_validator("QUIZ")
def validate_and_shuffle_quiz(quiz_data: Union[List[Dict[str, Any]], Dict[str, Any]], lesson_scope_rules: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Master Quiz Validator entrypoint.
    """
    if isinstance(quiz_data, dict):
        quiz_data = quiz_data.get("questions") or quiz_data.get("lesson_quiz") or quiz_data.get("quiz") or []
    if not isinstance(quiz_data, list):
        return False, ["Dữ liệu Quiz không đúng định dạng (yêu cầu danh sách câu hỏi)."]
    return validate_quiz_json(quiz_data, lesson_scope_rules)


def validate_reading_questions_md(md_content: str) -> Tuple[bool, List[str]]:
    """
    Validates reading comprehension questions markdown text.
    """
    errors = []
    
    # Check 1: Banned AI Buzzwords
    for pat in BANNED_AI_BUZZWORDS:
        if re.search(pat, md_content, re.IGNORECASE):
            errors.append(f"Reading Questions MD: Vi phạm Luật #10 - Tồn tại từ lóng AI bị cấm: '{re.search(pat, md_content, re.IGNORECASE).group(0)}'")
            
    # Check 2: Context Referencing
    for pat in CONTEXT_REFERENCING_PHRASES:
        matches = re.findall(pat, md_content, re.IGNORECASE)
        for match in set(matches):
            errors.append(f"Reading Questions MD: Vi phạm Luật #4.1 #4 - Tồn tại cụm từ tham chiếu ngữ cảnh: '{match}'")

    return len(errors) == 0, errors

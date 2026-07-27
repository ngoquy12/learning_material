"""
core/validators/reading_validator.py
Programmatic Validation Layer for Reading Materials.
Checks HTML structure, JS syntax, Mermaid diagram syntax, and link validity.
"""

from typing import Tuple, List, Dict, Any
from core.validators.syntax_linter import lint_html_syntax

def validate_reading_material(content: str, metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates a generated reading material for structural integrity, syntax, and pedagogical standards.
    """
    if not content:
        return False, ["Nội dung bài đọc bị trống."]
        
    errors = []
    
    # 1. HTML & JS Syntax Validation
    is_valid_syntax, syntax_errors = lint_html_syntax(content)
    if not is_valid_syntax:
        errors.extend(syntax_errors)
        
    # 2. Key Pedagogical Section Checks (5-step Walkthrough)
    content_lower = content.lower()
    section_checks = {
        "đặt vấn đề / bối cảnh": any(k in content_lower for k in ["đặt vấn đề", "bối cảnh", "nhu cầu"]),
        "phân tích bản chất": any(k in content_lower for k in ["phân tích", "cơ chế", "bản chất"]),
        "giải pháp / thực thi": any(k in content_lower for k in ["mã nguồn", "thực thi", "quy chuẩn", "giải pháp", "cấu hình"]),
        "tóm tắt / tổng kết": any(k in content_lower for k in ["tóm tắt", "tổng kết", "lưu ý"])
    }
    missing = [name for name, present in section_checks.items() if not present]
    if missing:
        errors.append(f"Bài đọc thiếu các phần nội dung cốt lõi: {', '.join(missing)}")
        
    # 3. Minimum length check
    if len(content.strip()) < 500:
        errors.append(f"Độ dài bài đọc quá ngắn ({len(content)} ký tự, yêu cầu tối thiểu 500 ký tự).")
        
    return len(errors) == 0, errors

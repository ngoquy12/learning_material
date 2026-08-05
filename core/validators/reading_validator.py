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
        
    # 2. Key Pedagogical Section Checks (Must contain 5 Section IDs)
    required_section_ids = ["section-1", "section-2", "section-3", "section-4", "section-5"]
    missing_ids = [sid for sid in required_section_ids if f'id="{sid}"' not in content and f'id=\'{sid}\'' not in content]
    if missing_ids:
        errors.append(f"Bài đọc vi phạm định dạng 5 Section cố định: thiếu các Section ID {', '.join(missing_ids)}.")
        
    # 3. Forbidden Text Emoji Check
    from agents.reviewer_agents import check_forbidden_emojis
    emoji_err = check_forbidden_emojis(content)
    if emoji_err:
        errors.append(f"Bài đọc chứa emoji văn bản bị cấm: {emoji_err}")

    # 4. Pyodide WASM Browser Compatibility Check for Python code blocks
    from core.validators.syntax_linter import lint_pyodide_compatibility
    pyodide_errors = lint_pyodide_compatibility(content)
    if pyodide_errors:
        errors.extend(pyodide_errors)

    # 5. Section 3 Executable Code Block Check
    if "id=\"section-3\"" in content or "id='section-3'" in content:
        import re
        sec3_match = re.search(r'id=["\']section-3["\'].*?(?=<section|\Z)', content, re.DOTALL)
        if sec3_match:
            sec3_text = sec3_match.group(0)
            if not ("<pre" in sec3_text or "<code" in sec3_text or "pyodide-editor" in sec3_text):
                errors.append("Section 3 vi phạm quy chuẩn: Bắt buộc phải chứa khối mã nguồn ví dụ thực hành (<pre><code>...).")

    # 6. Minimum length check
    if len(content.strip()) < 500:
        errors.append(f"Độ dài bài đọc quá ngắn ({len(content)} ký tự, yêu cầu tối thiểu 500 ký tự).")
        
    return len(errors) == 0, errors

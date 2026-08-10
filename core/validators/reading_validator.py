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
    
    metadata = metadata or {}
    session_str = str(metadata.get("session_id", "")).upper()
    lesson_type = str(metadata.get("lesson_type", "")).upper()
    lesson_title = str(metadata.get("lesson_title", "")).lower()
    
    is_orientation = (
        metadata.get("is_orientation")
        or "SESSION 01" in session_str
        or "ORIENTATION" in lesson_type
        or "tổng quan lộ trình" in lesson_title
        or "định hướng" in lesson_title
    )
    
    # 1. HTML & JS Syntax Validation
    is_valid_syntax, syntax_errors = lint_html_syntax(content)
    if not is_valid_syntax:
        errors.extend(syntax_errors)    
        
    if is_orientation:
        # Orientation Lesson Validation (Session 01)
        # Check that NO runnable code sandboxes exist
        if "pyodide-editor" in content or "runCode(" in content or "runVizStep(" in content:
            errors.append("Bài đọc Định hướng Session 01 vi phạm quy chuẩn: CẤM tạo code demo hoặc code sandbox rỗng.")
            
        # Check presence of 3 core orientation topics
        content_lower = content.lower()
        if not ("lộ trình" in content_lower or "tổng quan" in content_lower or "roadmap" in content_lower or "timeline" in content_lower):
            errors.append("Bài đọc Session 01 thiếu nội dung Phần 1: Tổng quan nội dung & Lộ trình môn học (Timeline/List).")
        if not ("phương pháp" in content_lower or "tiền đề" in content_lower or "học tập" in content_lower):
            errors.append("Bài đọc Session 01 thiếu nội dung Phần 2: Phương pháp học tập hiệu quả & Kiến thức tiền đề.")
        if not ("demo" in content_lower or "sản phẩm" in content_lower or "kết quả" in content_lower or "dự án" in content_lower):
            errors.append("Bài đọc Session 01 thiếu nội dung Phần 3: Demo sản phẩm dự án đầu ra.")
    else:
        # Standard Technical Lesson Validation (Must contain 5 Section IDs)
        required_section_ids = ["section-1", "section-2", "section-3", "section-4", "section-5"]
        missing_ids = [sid for sid in required_section_ids if f'id="{sid}"' not in content and f'id=\'{sid}\'' not in content]
        if missing_ids:
            errors.append(f"Bài đọc vi phạm định dạng 5 Section cố định: thiếu các Section ID {', '.join(missing_ids)}.")

        # Section 3 Executable Code Block Check
        if "id=\"section-3\"" in content or "id='section-3'" in content:
            import re
            sec3_match = re.search(r'id=["\']section-3["\'].*?(?=<section|\Z)', content, re.DOTALL)
            if sec3_match:
                sec3_text = sec3_match.group(0)
                if not ("<pre" in sec3_text or "<code" in sec3_text or "pyodide-editor" in sec3_text):
                    errors.append("Section 3 vi phạm quy chuẩn: Bắt buộc phải chứa khối mã nguồn ví dụ thực hành (<pre><code>...).")

    # 3. Forbidden Text Emoji Check
    from agents.reviewer_agents import check_forbidden_emojis
    emoji_err = check_forbidden_emojis(content)
    if emoji_err:
        errors.append(f"Bài đọc chứa emoji văn bản bị cấm: {emoji_err}")

    # 4. Pyodide WASM Browser Compatibility Check for Python code blocks (only if not orientation)
    if not is_orientation:
        from core.validators.syntax_linter import lint_pyodide_compatibility
        pyodide_errors = lint_pyodide_compatibility(content)
        if pyodide_errors:
            errors.extend(pyodide_errors)

    # 6. Minimum length check
    if len(content.strip()) < 500:
        errors.append(f"Độ dài bài đọc quá ngắn ({len(content)} ký tự, yêu cầu tối thiểu 500 ký tự).")

    # 7. Automated Visual Regression & Layout Inspection (Rule 3 & 11)
    from core.validators.visual_linter import validate_html_visual_layout
    is_valid_vis, visual_errors = validate_html_visual_layout(content, metadata)
    if not is_valid_vis:
        errors.extend(visual_errors)
        
    return len(errors) == 0, errors

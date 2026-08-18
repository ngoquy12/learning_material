"""
core/validators/reading_validator.py
Programmatic Validation Layer for Reading Materials.
Checks HTML structure, JS syntax, Mermaid diagram syntax, and link validity.
"""

from typing import Tuple, List, Dict, Any, Union
from core.validators.syntax_linter import lint_html_syntax
from core.validators.master_validator import register_validator

def validate_reading_json_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates structured JSON payload before rendering Jinja2 HTML."""
    if not isinstance(payload, dict) or not payload:
        return False, ["Payload JSON bài đọc bị trống hoặc không đúng định dạng dictionary."]
    
    errors = []
    required_keys = ["sec1_html", "sec2_html", "sec3_html", "sec4_html"]
    for k in required_keys:
        if not payload.get(k):
            errors.append(f"Payload JSON thiếu thông tin trường dữ liệu bắt buộc '{k}'.")
            
    return len(errors) == 0, errors

@register_validator("READING")
def validate_reading_material(content: Union[str, Dict[str, Any]], metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates a generated reading material for structural integrity, syntax, and pedagogical standards.
    """
    if isinstance(content, dict):
        content = content.get("html") or str(content)
        
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

    # 4. Pyodide WASM Browser Compatibility Check strictly for Python code blocks
    tech_stack_str = str(metadata.get("tech_stack") or "").lower().strip()
    is_python_course = (tech_stack_str == "python" or "python" in tech_stack_str) and not any(
        kw in tech_stack_str for kw in ["sql", "git", "bash", "docker", "agile", "architecture", "uml", "design", "java", "javascript", "react", "node", "cpp", "c++"]
    )
    if not is_orientation and is_python_course:
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

    # 8. Banned AI Cliché / Buzzwords Check
    banned_buzzwords = ["bẫy lập trình", "bẫy cú pháp", "bẫy logic", "bẫy lỗi", "thần thánh", "bí kíp", "tất tần tật"]
    content_lower = content.lower()
    for word in banned_buzzwords:
        if word in content_lower:
            errors.append(f"Bài đọc vi phạm quy chuẩn ngôn ngữ: Chứa từ khóa AI từ lóng bị cấm '{word}'. Hãy thay bằng 'Lỗi thường gặp' hoặc 'Ngoại lệ cần lưu ý'.")

    # 9. Section 3 Minimum 3 Progressive Examples Check
    if not is_orientation and ("id=\"section-3\"" in content or "id='section-3'" in content):
        import re
        sec3_match = re.search(r'id=["\']section-3["\'].*?(?=<section|\Z)', content, re.DOTALL)
        if sec3_match:
            sec3_text = sec3_match.group(0)
            h3_count = len(re.findall(r'<h3\b[^>]*>', sec3_text))
            if h3_count < 3:
                errors.append(f"Section 3 vi phạm quy chuẩn: Phải có ít nhất 3 ví dụ ứng dụng thực tế 3.1, 3.2, 3.3 (hiện tại có {h3_count} ví dụ).")

    # 10. Requirement Callout Box Check Before Code Sandboxes
    if not is_orientation and ("code-sb-" in content or "language-python" in content):
        if not ("Yêu cầu bài toán" in content or "Yêu cầu" in content or "font-bold text-sky-900" in content or "border-sky-200" in content):
            errors.append("Bài đọc vi phạm quy chuẩn: Trước mỗi code sandbox cần có khối thông tin Yêu cầu bài toán thực hành rõ ràng.")

    return len(errors) == 0, errors

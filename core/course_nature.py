"""
core/course_nature.py
Phân loại bản chất môn học: KHÔNG viết mã (lý thuyết, quy trình, mô hình hóa, thiết kế) hay
có viết mã. Môn không viết mã cấm mã lập trình và trình mô phỏng thực thi mã.

Từ khóa nằm ở `config/course_nature.json`, không nằm trong mã (dự án phục vụ nhiều môn, thêm môn
mới chỉ sửa cấu hình). Khớp theo TỪ nguyên vẹn: so khớp chuỗi con làm "word" khớp "keyword",
"prototype" khớp bài Prototype của JavaScript, khiến cả môn lập trình bị coi là không viết mã.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

from core.utils.text_match import has_any_term

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "course_nature.json"


@lru_cache(maxsize=1)
def _load_keywords() -> Dict[str, List[str]]:
    try:
        data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    return {
        "strong": [str(x) for x in data.get("strong", [])],
        "weak": [str(x) for x in data.get("weak", [])],
        "design": [str(x) for x in data.get("design", [])] + [str(x) for x in data.get("design_course_codes", [])],
    }


def reset_keyword_cache() -> None:
    """Dùng cho test khi đổi cấu hình giữa chừng."""
    _load_keywords.cache_clear()


def is_design_subject(tech_stack: str = "", course_name: str = "", lesson_title: str = "", session_title: str = "") -> bool:
    """True nếu môn tập trung thiết kế UI/UX, Figma, thiết kế thị giác (cấm mã và trình mô phỏng mã)."""
    text = f"{tech_stack} {course_name} {lesson_title} {session_title}"
    return has_any_term(text, _load_keywords()["design"])


def is_non_code_subject(tech_stack: str = "", course_name: str = "", lesson_title: str = "", session_title: str = "") -> bool:
    """
    True nếu môn/bài thuần khái niệm, quy trình hoặc mô hình hóa, nơi mã lập trình bị cấm.

    Từ khóa mạnh xét trên toàn bộ văn bản; từ khóa yếu (dễ trùng từ thường) chỉ xét trên
    tech_stack và tên môn, để một bài "Hàm prototype" hay "Tham số keyword" của môn lập trình
    không bị xếp nhầm.
    """
    kw = _load_keywords()
    if is_design_subject(tech_stack, course_name, lesson_title, session_title):
        return True
    everything = f"{tech_stack} {course_name} {lesson_title} {session_title}"
    if has_any_term(everything, kw["strong"]):
        return True
    return has_any_term(f"{tech_stack} {course_name}", kw["weak"])


def should_render_visualizer(tech_stack: str = "", course_name: str = "", lesson_title: str = "", session_title: str = "") -> bool:
    """False nếu môn không viết mã hoặc thiên về thiết kế: trình mô phỏng thực thi mã không áp dụng."""
    return not is_non_code_subject(tech_stack, course_name, lesson_title, session_title)


def get_non_code_spec_language(tech_stack: str = "") -> str:
    """Ngôn ngữ đặc tả cho môn không viết mã: mermaid, markdown hoặc gherkin."""
    t = (tech_stack or "").lower()
    if is_design_subject(tech_stack):
        return "markdown"
    if any(k in t for k in ["gherkin", "cucumber", "given-when-then"]):
        return "gherkin"
    if any(k in t for k in ["uml", "bpmn", "erd", "sequence", "class diagram", "use case"]):
        return "mermaid"
    return "markdown"

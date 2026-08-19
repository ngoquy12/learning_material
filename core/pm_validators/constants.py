"""
core/pm_validators/constants.py
Constants, regex lists, and utility helpers for PM Syllabus validation.
"""

import re
from typing import Dict, Any, List

# Words prohibited to maintain Academic Tone
HYPE_WORDS = [
    "thần tốc", "cực chất", "bí quyết", "làm chủ", "sức mạnh của",
    "tối thượng", "bứt phá", "thần thánh", "bí kíp", "tuyệt vời",
    "lợi ích kép", "thực chiến", "siêu tốc", "chìa khóa"
]

# Difficulty badges prohibited in titles
DIFFICULTY_BADGES = [
    r"\(heavy\)", r"\(light\)", r"\(lý thuyết nhẹ\)", r"\(lý thuyết nặng\)",
    r"\[heavy\]", r"\[light\]", r"\(nặng\)", r"\(nhẹ\)"
]

# Vague, non-measurable outcome verbs prohibited in expected_outcome
VAGUE_OUTCOME_VERBS = [
    "hiểu về", "biết về", "nắm được", "tìm hiểu", "làm quen", "nắm vững",
    "biết cách", "hiểu rõ", "học về", "nghiên cứu"
]

# Measurable action verbs based on Bloom's Taxonomy
BLOOM_ACTION_VERBS = [
    "phân biệt", "giải thích", "kết nối", "khởi tạo", "cấu hình", "thiết lập",
    "viết", "tạo", "thao tác", "xử lý", "triển khai", "giải quyết", "tối ưu",
    "xây dựng", "lập trình", "sử dụng", "trình bày", "đánh giá", "kiểm thử"
]

def extract_out_of_scope_technologies(tech_stack: str, clos: List[str] = None, plos: List[str] = None, main_content: str = "") -> List[str]:
    """
    Dynamically infers out-of-scope technologies for ANY tech_stack and curriculum specification.
    Prevents cross-contamination across courses without hardcoding specific tech keys.
    """
    combined_scope = " ".join([tech_stack or ""] + (clos or []) + (plos or []) + [main_content or ""]).lower()

    known_tech_ecosystems = [
        "react", "vue", "angular", "next.js", "express", "node.js",
        "spring boot", "django", "flask", "fastapi", "laravel",
        "sqlite", "postgresql", "mysql", "mongodb", "redis",
        "docker", "kubernetes", "pandas", "numpy", "tensorflow"
    ]

    disallowed = []
    for tech in known_tech_ecosystems:
        if tech not in combined_scope:
            disallowed.append(tech)

    return disallowed

def is_programming_language_course(tech_stack: str, main_content: str, pm_data: List[Dict[str, Any]]) -> bool:
    """
    Dynamically determines if the target course is a Programming Language / Coding Syntax course.
    Returns False for non-programming courses (e.g. Git, Docker, Linux, UI/UX, Agile, DevOps, Networking).
    """
    non_coding_keywords = ["git", "version control", "docker", "kubernetes", "devops", "linux", "system admin", "ui/ux", "agile", "scrum", "networking", "mạng máy tính"]
    stack_lower = (tech_stack or "").lower()
    content_lower = (main_content or "").lower()
    
    if any(kw in stack_lower for kw in non_coding_keywords) or any(kw in content_lower for kw in non_coding_keywords):
        if not any(lang in stack_lower for lang in ["python", "java", "c++", "c#", "javascript", "typescript", "golang", "go", "rust", "php", "ruby", "swift", "kotlin"]):
            return False

    all_text = (stack_lower + " " + content_lower + " " + " ".join([s.get("title", "") + " " + s.get("content_scope", "") for s in pm_data])).lower()
    coding_indicators = ["lập trình", "programming", "cú pháp", "syntax", "biến", "variable", "hàm", "function", "toán tử", "operator", "vòng lặp", "loop", "array", "list", "class", "object"]
    return sum(1 for ind in coding_indicators if ind in all_text) >= 3

def get_hinh_thuc(s: Dict[str, Any]) -> str:
    """Extracts session type/form regardless of schema key variation."""
    return str(s.get("hinh_thuc") or s.get("session_type") or "").strip()

def get_session_num(s: Dict[str, Any], default_idx: int) -> int:
    """Extracts integer session number from session_num or session_id."""
    if "session_num" in s and s["session_num"]:
        try:
            return int(s["session_num"])
        except ValueError:
            pass
    if "session_id" in s and s["session_id"]:
        match = re.search(r'\d+', str(s["session_id"]))
        if match:
            return int(match.group(0))
    return default_idx + 1

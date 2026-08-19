"""
core/renderers/lecture/knowledge_extractor.py
Knowledge extraction from PM syllabus and Reading material artifacts,
and session-wide unified business scenario derivations.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from core.renderers.lecture.text_sanitizer import clean_title_string

def derive_unified_session_scenario(session_title: str, tech_stack: str) -> str:
    """
    Establishes ONE unified concrete real-world business domain scenario
    for all lessons in the session to maintain pedagogical consistency (Directive 16).
    """
    st_lower = (session_title or "").lower()
    if any(k in st_lower for k in ["toán tử", "operator", "số học", "gán gộp", "tính toán"]):
        return "Hệ thống Giỏ hàng & Thanh toán Đơn hàng E-Commerce (Shopee/Tiki Checkout)"
    elif any(k in st_lower for k in ["biến", "variable", "nhập xuất", "console", "kiểu dữ liệu", "primitive"]):
        return "Hệ thống Đăng ký & Quản lý Hồ sơ Khách hàng Trực tuyến"
    elif any(k in st_lower for k in ["điều kiện", "rẽ nhánh", "if", "else", "switch", "ternary"]):
        return "Hệ thống Phân loại Khách hàng & Xét duyệt Đơn vay Tín dụng Ngân hàng"
    elif any(k in st_lower for k in ["vòng lặp", "loop", "for", "while"]):
        return "Hệ thống Quản lý Kho hàng & Tự động Xử lý Danh mục Sản phẩm"
    elif any(k in st_lower for k in ["mảng", "array", "list", "crud"]):
        return "Hệ thống Quản lý Hồ sơ Nhân sự & Đánh giá KPI Doanh nghiệp"
    elif any(k in st_lower for k in ["hàm", "function", "scope"]):
        return "Hệ thống Xử lý Giao dịch Thanh toán Đa cổng (Payment Gateway Integration)"
    elif any(k in st_lower for k in ["dom", "event", "giao diện", "ui"]):
        return "Giao diện Bảng điều khiển Quản trị Doanh nghiệp (Admin Dashboard)"
    elif any(k in st_lower for k in ["async", "promise", "fetch", "api"]):
        return "Hệ thống Đồng bộ Dữ liệu Thời tiết & Tỷ giá Hối đoái Quốc tế"
    else:
        return "Hệ thống Vận hành Dịch vụ Trực tuyến Doanh nghiệp"

def find_pm_syllabus(
    session_dir: Optional[Path],
    session_title: str,
    lesson_title: str
) -> Dict[str, Any]:
    """
    Extracts ground-truth curriculum metadata from PM_*.md or syllabus files.
    """
    default_res = {
        "curriculum_details": "",
        "curriculum_goals": "",
        "forbidden_scope": "",
        "learned_prerequisites": ""
    }
    if not session_dir:
        return default_res

    search_dirs = [session_dir.parent, session_dir, Path("output/pms")]
    pm_files = []
    for d in search_dirs:
        if d and d.exists():
            for f in d.glob("**/PM_*.md"):
                if f.is_file() and f not in pm_files:
                    pm_files.append(f)

    clean_lt = clean_title_string(lesson_title).lower()
    clean_st = clean_title_string(session_title).lower()

    for pm_path in pm_files:
        try:
            content = pm_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 8:
                        row_text = line.lower()
                        if any(w in row_text for w in clean_lt.split() if len(w) > 3) or clean_st in row_text:
                            return {
                                "curriculum_details": parts[6] if len(parts) > 6 else "",
                                "curriculum_goals": parts[7] if len(parts) > 7 else "",
                                "forbidden_scope": parts[8] if len(parts) > 8 else "",
                                "learned_prerequisites": parts[9] if len(parts) > 9 else ""
                            }
        except Exception:
            continue

    return default_res

def infer_scope_boundary_rules(
    session_title: str,
    tech_stack: str,
    pm_syllabus: Dict[str, Any]
) -> str:
    """Infers strict knowledge scope boundary rules to prevent leakage."""
    st_lower = (session_title or "").lower()
    forbidden_pm = pm_syllabus.get("forbidden_scope", "")
    learned_pm = pm_syllabus.get("learned_prerequisites", "")

    m = re.search(r'session\s*(\d+)', st_lower)
    sess_num = int(m.group(1)) if m else 99

    if sess_num <= 5:
        scope_desc = (
            "STRICT KNOWLEDGE SCOPE BOUNDARY (Sessions 01-05):\n"
            "- FORBIDDEN CONSTRUCTS: DO NOT declare functions (`function name(...)`, `def func(...)`), "
            "DO NOT use `if/else` or `switch-case` statements, DO NOT use loops (`for`, `while`), "
            "DO NOT use classes/OOP, DO NOT use DOM APIs or `Math.round`/`Number.isNaN` utilities.\n"
            "- MANDATORY CONSTRUCTS: Use ONLY direct sequential variable declarations (`const`, `let`), "
            "direct operator expressions, and standard output (`console.log(...)` or `print(...)`).\n"
        )
    elif sess_num <= 7:
        scope_desc = (
            "STRICT KNOWLEDGE SCOPE BOUNDARY (Sessions 06-07):\n"
            "- FORBIDDEN CONSTRUCTS: DO NOT use loops (`for`, `while`), arrays, functions, classes, DOM, async.\n"
            "- ALLOWED CONSTRUCTS: Variable declarations, operators, `if-else`, `switch-case`, ternary `? :`, console.log.\n"
        )
    else:
        scope_desc = "Adhere strictly to the session's level of advancement.\n"

    if forbidden_pm:
        scope_desc += f"- PM Matrix Restrictions: {forbidden_pm}\n"
    if learned_pm:
        scope_desc += f"- PM Matrix Learned Scope: {learned_pm}\n"

    return scope_desc

def extract_knowledge_from_lesson_folder(
    session_dir: Optional[Path],
    session_title: str,
    lesson_title: str
) -> Dict[str, Any]:
    """
    Extracts verified knowledge bullets and gotchas directly from reading materials.
    """
    pm_meta = find_pm_syllabus(session_dir, session_title, lesson_title)
    bullets = []
    gotchas = []

    if session_dir and session_dir.exists():
        clean_target = clean_title_string(lesson_title).lower()
        matched_file = None

        for l_dir in session_dir.iterdir():
            if l_dir.is_dir() and "lesson" in l_dir.name.lower():
                clean_dir = clean_title_string(l_dir.name).lower()
                if clean_target in clean_dir or any(w in clean_dir for w in clean_target.split() if len(w) > 3):
                    for pf in [l_dir / "Bài đọc" / "reading.html", l_dir / "reading.html", l_dir / "Bài đọc" / "reading_master.md"]:
                        if pf.exists():
                            matched_file = pf
                            break
                if matched_file:
                    break

        if matched_file and matched_file.exists():
            try:
                content = matched_file.read_text(encoding="utf-8")
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, "html.parser")

                sec2 = soup.find(id="section-2") or soup.find("section", id=lambda x: x and "2" in str(x))
                if sec2:
                    for li in sec2.find_all("li"):
                        t = li.get_text().strip()
                        if t and len(t) > 15 and t not in bullets:
                            clean_t = re.sub(r'\s+', ' ', t)
                            bullets.append(clean_t)

                sec4 = soup.find(id="section-4") or soup.find("section", id=lambda x: x and "4" in str(x))
                if sec4:
                    for el in sec4.find_all(["p", "li"]):
                        t = el.get_text().strip()
                        if any(k in t.lower() for k in ["lỗi", "tránh", "lưu ý", "sai sót", "ngoại lệ", "rủi ro"]):
                            if len(t) > 20 and t not in gotchas:
                                gotchas.append(re.sub(r'\s+', ' ', t))
            except Exception:
                pass

    return {
        "bullets": bullets[:4] if bullets else [],
        "gotcha_text": gotchas[0] if gotchas else "",
        "pm_meta": pm_meta
    }

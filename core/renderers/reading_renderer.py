"""
core/renderers/reading_renderer.py
Enterprise Reading Material Renderer Engine (Jinja2 + Domain Component Registry)
Converts structured LLM JSON payloads into 100% gold-standard HTML matching templates/reading.html.
"""

import os
import json
import re
import html
from pathlib import Path
from typing import Dict, Any, List, Optional
import jinja2

# Directory containing templates
TEMPLATES_HTML_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "html"
TEMPLATES_ROOT_DIR = Path(__file__).resolve().parent.parent.parent / "templates"

class ReadingTemplateRenderer:
    """Master Jinja2 Renderer for Reading Materials."""

    def __init__(self):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([str(TEMPLATES_HTML_DIR), str(TEMPLATES_ROOT_DIR)]),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, context: Dict[str, Any]) -> str:
        template = self.env.get_template("reading_master.html.j2")
        return template.render(**context)

def resolve_domain_engine(tech_stack: str) -> Dict[str, str]:
    """
    Determines engine type, hljs languages, and visualizer type based on tech_stack.
    STRICTLY FORBIDS hardcoded fallback defaults (no fallback to python, java, etc.).
    """
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] resolve_domain_engine: 'tech_stack' bị trống. Hệ thống TUYỆT ĐỐI KHÔNG fallback/hardcode ngầm bất kỳ công nghệ nào. Vui lòng truyền --tech-stack chính xác từ PM.")
    
    tech_lower = str(tech_stack).lower().strip()

    # 1. Database / SQL
    if any(kw in tech_lower for kw in ["sql", "mysql", "postgres", "sqlite", "oracle", "database"]):
        return {
            "engine_type": "sql_sim",
            "hljs_languages": ["sql"],
            "visualizer_type": "sql",
            "name": "SQL"
        }

    # 2. CLI / DevOps / Tooling
    cli_keywords = ["git", "vcs", "github", "gitlab", "terminal", "bash", "shell", "cli", "cmd", "powershell", "docker", "kubernetes", "devops", "linux", "unix"]
    if any(kw in tech_lower for kw in cli_keywords):
        return {
            "engine_type": "static",
            "hljs_languages": ["bash"],
            "visualizer_type": "cli",
            "name": tech_stack or "Git/CLI"
        }

    # 3. Pure Concept / Architecture / Agile / Process
    concept_keywords = ["agile", "scrum", "diagram", "uml", "design", "word", "excel", "powerpoint", "office", "phân tích", "thiết kế", "kiến trúc", "system analysis", "software architecture", "management", "theory", "concept", "process"]
    if any(kw in tech_lower for kw in concept_keywords):
        return {
            "engine_type": "static",
            "hljs_languages": ["plaintext"],
            "visualizer_type": "concept",
            "name": tech_stack or "Architecture"
        }

    # 4. Programming Languages
    if "typescript" in tech_lower or re.search(r'\bts\b', tech_lower):
        return {"engine_type": "js_worker", "hljs_languages": ["typescript"], "visualizer_type": "programming", "name": "TypeScript"}
    if "javascript" in tech_lower or re.search(r'\bjs\b', tech_lower) or "react" in tech_lower or "node" in tech_lower or "vue" in tech_lower:
        return {"engine_type": "js_worker", "hljs_languages": ["javascript"], "visualizer_type": "programming", "name": "JavaScript"}
    if "python" in tech_lower or re.search(r'\bpy\b', tech_lower) or "django" in tech_lower or "flask" in tech_lower or "fastapi" in tech_lower:
        return {"engine_type": "pyodide", "hljs_languages": ["python"], "visualizer_type": "programming", "name": "Python"}
    if "javascript" not in tech_lower and "java" in tech_lower:
        return {"engine_type": "static", "hljs_languages": ["java"], "visualizer_type": "programming", "name": "Java"}
    if re.search(r'c\+\+|\bcpp\b', tech_lower):
        return {"engine_type": "static", "hljs_languages": ["cpp"], "visualizer_type": "programming", "name": "C++"}
    if re.search(r'c#|\bcsharp\b|\.net\b|\bdotnet\b', tech_lower):
        return {"engine_type": "static", "hljs_languages": ["csharp"], "visualizer_type": "programming", "name": "C#"}
    if re.search(r'(?<![a-z])c(?![a-z])', tech_lower):
        return {"engine_type": "static", "hljs_languages": ["c"], "visualizer_type": "programming", "name": "C"}

    # Không khớp bất kỳ nhóm nào đã đăng ký -> báo lỗi rõ ràng thay vì âm thầm fallback về
    # Python. Đây từng là bug thật: mọi tech_stack lạ (Go, Rust, PHP, Kotlin, Swift...) bị
    # âm thầm render bằng engine Python/Pyodide, vi phạm chính cam kết "STRICTLY FORBIDS
    # hardcoded fallback defaults" đã ghi ở docstring hàm này.
    raise ValueError(
        f"❌ [LỖI TECH_STACK CHƯA ĐƯỢC ĐĂNG KÝ] resolve_domain_engine: không tìm thấy engine "
        f"phù hợp cho tech_stack='{tech_stack}'. Vui lòng bổ sung nhóm nhận diện cho công nghệ "
        f"này trong resolve_domain_engine() thay vì để hệ thống âm thầm mặc định về ngôn ngữ khác."
    )


def extract_h3_subsections(html_content: str) -> List[Dict[str, str]]:
    """
    Extracts all <h3> subheadings with IDs for TOC generation.
    """
    if not html_content:
        return []
    
    matches = re.findall(r'<h3\s+id="([^"]+)"[^>]*>(.*?)</h3>', html_content, re.DOTALL)
    subsections = []
    for anchor_id, title in matches:
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        subsections.append({"id": anchor_id, "title": clean_title})
    return subsections


def sanitize_and_repair_dom(raw_html: str) -> str:
    """
    Sanitizes and repairs common HTML structure flaws.
    """
    if not raw_html:
        return ""
    
    # Strip forbidden markdown code markers if any leaked
    cleaned = re.sub(r'```html\s*', '', raw_html)
    cleaned = re.sub(r'```\s*$', '', cleaned)
    
    return cleaned


def assemble_reading_html(json_payload: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    """
    Master Assembly Function: Combines structured JSON payload + domain visualizers + Jinja2 template.
    STRICTLY FORBIDS hardcoded fallback defaults for tech_stack.
    """
    tech_stack = (metadata.get("tech_stack") if isinstance(metadata, dict) else None) or (json_payload.get("tech_stack") if isinstance(json_payload, dict) else None)
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] assemble_reading_html: 'tech_stack' bị trống trong metadata/payload. Hệ thống TUYỆT ĐỐI KHÔNG fallback/hardcode ngầm bất kỳ công nghệ nào.")
    
    domain_info = resolve_domain_engine(tech_stack)

    lesson_title = metadata.get("lesson_title") or json_payload.get("lesson_title") or "Bài đọc học liệu"
    lesson_clean_title = lesson_title.split(" - ")[-1] if " - " in lesson_title else lesson_title

    # Section Titles
    sec_titles = json_payload.get("section_titles") or {}

    # Check if sec2_html already contains Section 2.4 visualizer (prevent duplicate injection)
    sec2_raw = json_payload.get("sec2_html", "")
    has_existing_viz = (
        'id="sec-2-4' in sec2_raw
        or 'viz-step-badge' in sec2_raw
        or 'viz-code-display' in sec2_raw
        or 'Mô phỏng cơ chế vận hành từng bước' in sec2_raw
    )

    # Visualizer — the real per-lesson visualizer is built upstream (reading_creator.py via
    # build_domain_adaptive_visualizer) and already inlined into sec2_html by the time it
    # reaches here; this hook only forwards an externally-supplied component, if any, instead
    # of calling the removed generic/hardcoded-Python-fallback generator.
    viz_html = json_payload.get("visualizer_component_html", "") if not has_existing_viz else ""
    show_viz = bool(viz_html) and not has_existing_viz

    # Subsections for TOC navigation (auto-extract from HTML if not provided)
    sec2_subs = json_payload.get("sec2_subsections") or extract_h3_subsections(sec2_raw)
    sec3_subs = json_payload.get("sec3_subsections") or extract_h3_subsections(json_payload.get("sec3_html", ""))

    # Self-test questions JSON serialization for JS handler
    self_test = json_payload.get("self_test_questions") or []
    st_answers = {}
    st_explanations = {}
    for idx, q in enumerate(self_test, 1):
        st_answers[idx] = q.get("correct_idx", 0)
        st_explanations[idx] = q.get("explanation", "")

    # References
    references = json_payload.get("reference_links") or [
        {"title": f"Tài liệu chính thức {tech_stack.capitalize()}", "url": "https://docs.python.org/3/"}
    ]

    context = {
        "lesson_title": lesson_title,
        "lesson_clean_title": lesson_clean_title,
        "engine_type": domain_info["engine_type"],
        "hljs_languages": domain_info["hljs_languages"],
        "section_titles": sec_titles,
        "sec2_subsections": sec2_subs,
        "sec3_subsections": sec3_subs,
        "show_visualizer": show_viz,
        "visualizer_component_html": viz_html,
        "sec1_html": json_payload.get("sec1_html", "<p>Nội dung đang được cập nhật...</p>"),
        "sec1_visual_html": json_payload.get("sec1_visual_html"),
        "sec2_html": sec2_raw or "<p>Nội dung cú pháp đang được cập nhật...</p>",
        "sec3_html": json_payload.get("sec3_html", "<p>Ví dụ thực hành đang được cập nhật...</p>"),
        "sec4_html": json_payload.get("sec4_html", "<p>Tổng kết đang được cập nhật...</p>"),
        "context_image_url": json_payload.get("context_image_url"),
        "reference_links": references,
        "self_test_questions": self_test,
        "self_test_answers_json": json.dumps(st_answers, ensure_ascii=False),
        "self_test_explanations_json": json.dumps(st_explanations, ensure_ascii=False),
    }

    renderer = ReadingTemplateRenderer()
    raw_html = renderer.render(context)
    return sanitize_and_repair_dom(raw_html)

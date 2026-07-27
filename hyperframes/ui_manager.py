"""
hyperframes/ui_manager.py

HyperFrames Centralized UI Component Manager & Registry
======================================================
Tập trung toàn bộ quản lý Component Library, Template Rendering,
Metadata Registry và Validation về một nơi duy nhất.

Cung cấp API thống nhất cho:
1. Reviewer Agent   → Validate & gợi ý layout_type
2. Writer Agent     → Render HTML Scene từ component templates
3. Pipeline Engine  → Kiểm tra readiness & danh sách component hiện có
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional


# ── Component Registry Metadata ───────────────────────────────────────────────

COMPONENT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "code_editor": {
        "rel_path": "ide/vscode.html",
        "name": "VS Code IDE Editor",
        "description": "Hiển thị mã nguồn Python/Bash với syntax highlighting và file tree sidebar.",
        "category": "ide",
        "aliases": ["code", "vscode", "ide"],
    },
    "terminal_cli": {
        "rel_path": "ide/terminal.html",
        "name": "Terminal CLI Window",
        "description": "Giao diện dòng lệnh Terminal/Bash với con trỏ nhấp nháy.",
        "category": "ide",
        "aliases": ["terminal", "cli", "shell", "cmd"],
    },
    "comparison": {
        "rel_path": "cards/comparison.html",
        "name": "Side-by-Side Comparison Card",
        "description": "So sánh 2 phương pháp (Cách cũ ❌ vs Best Practice ✅).",
        "category": "cards",
        "aliases": ["vs", "compare"],
    },
    "pitfall_alert": {
        "rel_path": "cards/warning_card.html",
        "name": "Pitfall Alert & Solution",
        "description": "Cảnh báo lỗi phổ biến học viên thường gặp và giải pháp khắc phục.",
        "category": "cards",
        "aliases": ["pitfall", "warning", "error_alert"],
    },
    "process_flow": {
        "rel_path": "cards/process_flow.html",
        "name": "4-Step Process Flow",
        "description": "Trình bày luồng thực hiện qua 4 bước với đường nối động.",
        "category": "cards",
        "aliases": ["flow", "steps", "workflow"],
    },
    "architecture_diagram": {
        "rel_path": "cards/architecture.html",
        "name": "Architecture & Data Flow Diagram",
        "description": "Sơ đồ kiến trúc 3 khối (Client ➔ Server ➔ Database).",
        "category": "cards",
        "aliases": ["architecture", "diagram", "system_flow"],
    },
    "summary_recap": {
        "rel_path": "cards/summary_recap.html",
        "name": "Key Takeaways & Summary Outro",
        "description": "Thẻ tổng kết điểm cốt lõi bài học và thông tin bài tiếp theo.",
        "category": "cards",
        "aliases": ["recap", "summary", "outro"],
    },
    "interactive_quiz": {
        "rel_path": "cards/qa_quiz.html",
        "name": "Knowledge Check Quiz",
        "description": "Thẻ câu hỏi trắc nghiệm củng cố kiến thức giữa bài giảng.",
        "category": "cards",
        "aliases": ["quiz", "qa", "question"],
    },
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _clean_meta_prompts(text: str) -> str:
    """Strip visual/UI prompt instructions from narration."""
    META_PATTERNS = [
        r"màn hình [\w\s]+hiển thị[^.]*\.",
        r"sử dụng (font|màu|nền)[^.]*\.",
        r"(xuất hiện|ẩn đi|chuyển sang)[^.]*\.",
        r"(layout|animation|gradient|background|mockup|slide)[^.]*\.",
        r"giao diện[^.]*\.",
    ]
    for pat in META_PATTERNS:
        text = re.sub(pat, "", text, flags=re.IGNORECASE)
    return text.strip()


def _extract_sentences(narration: str, max_sentences: int = 2) -> str:
    """Extract first N clean sentences from narration."""
    sentences = [s.strip() for s in re.split(r"[.!?:]", narration) if len(s.strip()) > 12]
    result = ". ".join(sentences[:max_sentences])
    return result + "." if result else narration[:200]


def _make_line_numbers_html(line_count: int) -> str:
    return "<br/>".join(str(i) for i in range(1, line_count + 1))


def _make_sidebar_files_html(filename: str, lang: str) -> str:
    ext_map = {
        "python": "🐍", "bash": "🖥️", "javascript": "🟨",
        "html": "🌐", "css": "🎨", "json": "📋",
    }
    icon = ext_map.get(lang.lower(), "📄")
    return (
        f'<div class="sidebar-file active">{icon} {filename}</div>'
        f'<div class="sidebar-file muted">📄 requirements.txt</div>'
        f'<div class="sidebar-file muted">📄 README.md</div>'
        f'<div class="sidebar-file muted">📁 .venv/</div>'
    )


def _make_code_html(scene: Dict[str, Any], desc_lower: str) -> tuple[str, str, int]:
    """
    Generate code HTML for VS Code editor component.
    Priority: scene['code_content'] (from LLM blueprint) > keyword fallback.
    """
    # ── Priority 1: Use code_content from blueprint if available ──
    blueprint_code = scene.get("code_content", "")
    blueprint_lang = scene.get("code_language", "")
    if blueprint_code:
        lang = blueprint_lang or "python"
        # Auto-wrap in syntax spans if raw text
        if "<span" not in blueprint_code:
            lines = blueprint_code.split("\n")
            formatted = []
            for line in lines:
                if line.strip().startswith("#"):
                    formatted.append(f'<span class="comment">{line}</span>')
                elif any(kw in line for kw in ["import ", "from ", "def ", "class ", "return ", "if ", "for ", "while "]):
                    formatted.append(f'<span class="keyword">{line}</span>')
                else:
                    formatted.append(line)
            blueprint_code = "\n".join(formatted)
        line_count = len(blueprint_code.split("\n"))
        return blueprint_code, lang, line_count

    # ── Priority 2: Keyword-based fallback (existing logic) ──
    lang = "python"
    code_html = ""

    if "requirements" in desc_lower or "freeze" in desc_lower:
        lang = "bash"
        code_html = (
            '<span class="comment"># 1. Lưu danh sách thư viện hiện tại</span>\n'
            '<span class="keyword">pip</span> freeze &gt; requirements.txt\n\n'
            '<span class="comment"># 2. Cài đặt lại trên môi trường mới</span>\n'
            '<span class="keyword">pip</span> install -r requirements.txt'
        )
    elif "venv" in desc_lower or "virtualenv" in desc_lower or "kích hoạt" in desc_lower:
        lang = "bash"
        code_html = (
            '<span class="comment"># 1. Tạo môi trường ảo</span>\n'
            '<span class="keyword">python</span> -m venv venv\n\n'
            '<span class="comment"># 2. Kích hoạt (Windows)</span>\n'
            'venv<span class="operator">\\</span>Scripts<span class="operator">\\</span>activate\n\n'
            '<span class="comment"># 3. Kích hoạt (macOS / Linux)</span>\n'
            '<span class="keyword">source</span> venv/bin/activate'
        )
    elif "import" in desc_lower or "module" in desc_lower or "thư viện" in desc_lower:
        lang = "python"
        code_html = (
            '<span class="keyword">import</span> <span class="variable">os</span>\n'
            '<span class="keyword">import</span> <span class="variable">sys</span>\n'
            '<span class="keyword">from</span> <span class="variable">pathlib</span> '
            '<span class="keyword">import</span> <span class="variable">Path</span>\n\n'
            '<span class="comment"># Kiểm tra Python interpreter đang dùng</span>\n'
            '<span class="function">print</span>(<span class="string">"Python:"</span>, sys.executable)'
        )
    elif "biến" in desc_lower or "variable" in desc_lower or "khai báo" in desc_lower:
        lang = "python"
        code_html = (
            '<span class="comment"># Khai báo và gán giá trị biến</span>\n'
            'course_name = <span class="string">"Python Core AI"</span>\n'
            'lesson_num = <span class="number">1</span>\n'
            'is_active = <span class="keyword">True</span>\n\n'
            '<span class="function">print</span>(<span class="string">'
            'f"Bài {lesson_num}: {course_name}"</span>)'
        )
    elif "fastapi" in desc_lower or "endpoint" in desc_lower or "router" in desc_lower:
        lang = "python"
        code_html = (
            '<span class="keyword">from</span> <span class="variable">fastapi</span> '
            '<span class="keyword">import</span> <span class="variable">FastAPI</span>\n\n'
            'app = <span class="function">FastAPI</span>()\n\n'
            '<span class="operator">@</span>app.<span class="function">get</span>'
            '(<span class="string">"/"</span>)\n'
            '<span class="keyword">def</span> <span class="function">read_root</span>():\n'
            '    <span class="keyword">return</span> {<span class="string">"message"</span>: '
            '<span class="string">"Hello, FastAPI!"</span>}'
        )
    else:
        lang = "python"
        code_html = (
            '<span class="comment"># Python — Chương trình đầu tiên</span>\n'
            '<span class="function">print</span>(<span class="string">"Hello, Python!"</span>)\n\n'
            '<span class="comment"># Kiểm tra phiên bản</span>\n'
            '<span class="keyword">import</span> <span class="variable">sys</span>\n'
            '<span class="function">print</span>(<span class="string">'
            'f"Version: {sys.version}"</span>)'
        )

    line_count = len(code_html.split("\n"))
    return code_html, lang, line_count


def _make_terminal_lines_html(visual_desc: str, narration: str, scene: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate terminal command lines HTML.
    Priority: scene['terminal_commands'] (from LLM blueprint) > visual_desc parsing.
    """
    # ── Priority 1: Use terminal_commands from blueprint if available ──
    if scene and scene.get("terminal_commands"):
        cmd_lines = scene["terminal_commands"]
        if isinstance(cmd_lines, str):
            cmd_lines = [l.strip() for l in cmd_lines.split("\n") if l.strip()]
    else:
        # ── Priority 2: Parse from visual_desc (existing logic) ──
        raw_lines = [l.strip() for l in visual_desc.split("\n") if l.strip()]
        cmd_lines = [l for l in raw_lines if l and not any(
            k in l.lower() for k in ["màn hình", "hiển thị", "animation", "layout", "gradient"]
        )]
        if not cmd_lines:
            cmd_lines = [
                "$ python --version",
                "Python 3.11.9",
                "",
                "$ pip --version",
                "pip 23.3.1 from /usr/lib/python3.11",
            ]

    html_parts = []
    for line in cmd_lines[:12]:
        if not line:
            html_parts.append('<span class="cmd-separator"></span>')
        elif line.startswith("#"):
            html_parts.append(f'<span class="cmd-line cmd-comment">{line}</span>')
        elif line.startswith("$") or line.startswith(">>>"):
            parts = line.split(" ", 1)
            prompt = parts[0]
            cmd = parts[1] if len(parts) > 1 else ""
            html_parts.append(
                f'<span class="cmd-line">'
                f'<span class="cmd-prompt-prefix">{prompt}</span> '
                f'<span class="cmd-text">{cmd}</span>'
                f'</span>'
            )
        else:
            html_parts.append(f'<span class="cmd-line cmd-output">{line}</span>')
    return "\n          ".join(html_parts)


def _compute_dynamic_timing(dur: float, n_events: int = 4) -> List[float]:
    start = 4.0
    end = max(dur - 1.5, start + n_events * 0.8)
    step = (end - start) / max(n_events - 1, 1)
    return [round(start + i * step, 2) for i in range(n_events)]


# ── Central UI Component Manager Class ───────────────────────────────────────

class UIManager:
    """
    Centralized Manager for HyperFrames UI Component Library.
    Manages Registry, Layout Validation, and Template Rendering.
    """

    def __init__(self, components_dir: Optional[Path] = None):
        if components_dir is None:
            components_dir = Path(__file__).resolve().parent / "components"
        self.components_dir = components_dir
        self._template_cache: Dict[str, str] = {}
        self._alias_map: Dict[str, str] = {}
        self._build_alias_map()

    def _build_alias_map(self) -> None:
        """Build normalized alias map for all layout types."""
        for canonical_name, meta in COMPONENT_REGISTRY.items():
            self._alias_map[canonical_name] = canonical_name
            for alias in meta.get("aliases", []):
                self._alias_map[alias] = canonical_name

    def normalize_layout_type(self, raw_layout: str) -> str:
        """
        Normalize any layout_type alias to its canonical layout name.
        Defaults to 'code_editor' if unmapped.
        """
        cleaned = (raw_layout or "").lower().strip()
        return self._alias_map.get(cleaned, "code_editor")

    def is_valid_layout(self, layout_type: str) -> bool:
        """Check if layout_type is registered in the UI Component Library."""
        cleaned = (layout_type or "").lower().strip()
        return cleaned in self._alias_map

    def list_layouts(self) -> List[str]:
        """Return all registered canonical layout names."""
        return list(COMPONENT_REGISTRY.keys())

    def get_layout_meta(self, layout_type: str) -> Dict[str, Any]:
        """Get metadata for a specific layout type."""
        canonical = self.normalize_layout_type(layout_type)
        return COMPONENT_REGISTRY[canonical]

    def _load_template(self, rel_path: str) -> str:
        """Load and cache an HTML template file."""
        if rel_path not in self._template_cache:
            full_path = self.components_dir / rel_path
            if not full_path.exists():
                raise FileNotFoundError(
                    f"[UIManager] Component Template not found: {full_path}"
                )
            self._template_cache[rel_path] = full_path.read_text(encoding="utf-8")
        return self._template_cache[rel_path]

    def render_scene(self, scene: Dict[str, Any], lesson_title: str) -> str:
        """
        Central method to render a Scene HTML using the Component Library.

        Args:
            scene: Scene dictionary from blueprint.
            lesson_title: Title of the lesson for context.

        Returns:
            Render-ready HTML string.
        """
        raw_layout = scene.get("layout_type", "code_editor")
        canonical_layout = self.normalize_layout_type(raw_layout)
        meta = COMPONENT_REGISTRY[canonical_layout]
        template = self._load_template(meta["rel_path"])

        scene_id = scene["scene_id"]
        scene_n = scene_id.replace("Scene_", "").zfill(2)
        scene_title = scene.get("scene_title", f"Scene {scene_n}")
        dur = float(scene.get("duration", 30.0))
        narration = scene.get("narration", "")
        visual_desc = scene.get("visual_description", "")

        desc_lower = (visual_desc.lower() + " " + scene_title.lower() + " " + narration.lower())
        concept_body = _extract_sentences(narration, max_sentences=2)
        concept_body = _clean_meta_prompts(concept_body) or scene_title

        timing = _compute_dynamic_timing(dur, n_events=5)
        t1, t2, t3, t4, t5 = timing

        # Base slots common across all components
        slots: Dict[str, str] = {
            "slot_scene_n":      scene_n,
            "slot_dur":          str(dur),
            "slot_intro_title":  scene_title,
            "slot_concept_title": "Khái Niệm Cốt Lõi",
            "slot_concept_body": concept_body,
            "slot_t1":           str(t1),
            "slot_t2":           str(t2),
            "slot_t3":           str(t3),
            "slot_t4":           str(t4),
            "slot_t5":           str(t5),
            "slot_gsap_extra":   "",
        }

        # Layout-specific slot injection
        if canonical_layout == "code_editor":
            code_html, lang, line_count = _make_code_html(scene, desc_lower)
            filename = "main.py" if lang == "python" else "run.sh"
            slots.update({
                "slot_filename":      filename,
                "slot_lang":          lang,
                "slot_code_html":     code_html,
                "slot_line_count":    str(line_count),
                "slot_line_numbers":  _make_line_numbers_html(line_count),
                "slot_sidebar_files": _make_sidebar_files_html(filename, lang),
                "slot_git_branch":    "main",
                "slot_python_version":"3.11",
            })

        elif canonical_layout == "terminal_cli":
            cmd_lines_html = _make_terminal_lines_html(visual_desc, narration, scene=scene)
            slots.update({
                "slot_cmd_lines_html": cmd_lines_html,
                "slot_shell_name":     "bash",
                "slot_cwd_path":       "~/project",
            })

        elif canonical_layout == "comparison":
            narration_parts = [s.strip() for s in re.split(r"[.!?]", narration) if len(s.strip()) > 15]
            slots.update({
                "slot_left_icon":  "⚠️",
                "slot_left_title": "Phương pháp Cũ",
                "slot_left_body":  narration_parts[0] if narration_parts else concept_body,
                "slot_right_icon": "🚀",
                "slot_right_title":"Phương pháp Mới",
                "slot_right_body": narration_parts[1] if len(narration_parts) > 1 else concept_body,
            })

        elif canonical_layout == "pitfall_alert":
            all_sentences = [s.strip() for s in re.split(r"[.!?]", narration) if len(s.strip()) > 10]
            pitfall_sentences = all_sentences[:3] if len(all_sentences) >= 3 else all_sentences + ["Luôn kiểm tra kỹ trước khi chạy lệnh."]
            pitfall_items_html = "\n".join(f"<li>{s}</li>" for s in pitfall_sentences[:3])
            solution = all_sentences[3] if len(all_sentences) > 3 else "Tham khảo tài liệu chính thức và kiểm tra từng bước."
            slots.update({
                "slot_pitfall_items_html": pitfall_items_html,
                "slot_solution_body":      solution,
            })

        elif canonical_layout == "process_flow":
            step_sentences = [s.strip() for s in re.split(r"[.!?]", narration) if len(s.strip()) > 10]
            def _get_step(idx: int) -> tuple[str, str]:
                if idx < len(step_sentences):
                    parts = step_sentences[idx].split(":", 1)
                    if len(parts) == 2:
                        return parts[0].strip(), parts[1].strip()
                    return step_sentences[idx][:40], step_sentences[idx]
                return f"Bước {idx+1}", "Thực hiện theo hướng dẫn."

            s1t, s1b = _get_step(0)
            s2t, s2b = _get_step(1)
            s3t, s3b = _get_step(2)
            s4t, s4b = _get_step(3)

            slots.update({
                "slot_step1_num": "01", "slot_step1_title": s1t, "slot_step1_body": s1b,
                "slot_step2_num": "02", "slot_step2_title": s2t, "slot_step2_body": s2b,
                "slot_step3_num": "03", "slot_step3_title": s3t, "slot_step3_body": s3b,
                "slot_step4_num": "04", "slot_step4_title": s4t, "slot_step4_body": s4b,
            })

        elif canonical_layout == "architecture_diagram":
            sentences = [s.strip() for s in re.split(r"[.!?]", narration) if len(s.strip()) > 10]
            n1_desc = sentences[0] if len(sentences) > 0 else "Client / User Request"
            n2_desc = sentences[1] if len(sentences) > 1 else "Core Engine / API Server"
            n3_desc = sentences[2] if len(sentences) > 2 else "Database / Response Payload"

            slots.update({
                "slot_node1_icon":  "💻",
                "slot_node1_title": "Client Layer",
                "slot_node1_desc":  n1_desc,
                "slot_node2_icon":  "⚙️",
                "slot_node2_title": "Application Core",
                "slot_node2_desc":  n2_desc,
                "slot_node3_icon":  "🗄️",
                "slot_node3_title": "Data / Service",
                "slot_node3_desc":  n3_desc,
            })

        elif canonical_layout == "summary_recap":
            sentences = [s.strip() for s in re.split(r"[.!?]", narration) if len(s.strip()) > 10]
            def _get_tk(idx: int, default: str) -> str:
                return sentences[idx] if idx < len(sentences) else default

            slots.update({
                "slot_recap_title": "Tổng Kết Bài Học",
                "slot_takeaway1":   _get_tk(0, "Nắm vững khái niệm cốt lõi của bài học."),
                "slot_takeaway2":   _get_tk(1, "Hiểu rõ các bước thực hành và cấu hình môi trường."),
                "slot_takeaway3":   _get_tk(2, "Tránh các lỗi phổ biến và áp dụng Best Practices."),
                "slot_takeaway4":   _get_tk(3, "Sẵn sàng áp dụng vào bài tập thực tế."),
                "slot_next_lesson": "Tiếp tục bài học tiếp theo trong lộ trình.",
            })

        elif canonical_layout == "interactive_quiz":
            sentences = [s.strip() for s in re.split(r"[.!?]", narration) if len(s.strip()) > 10]
            question = sentences[0] if sentences else "Đâu là câu trả lời đúng cho vấn đề trên?"
            slots.update({
                "slot_question_text": question,
                "slot_opt_a":         sentences[1] if len(sentences) > 1 else "Đáp án A: Cấu hình mặc định hệ thống",
                "slot_opt_b":         sentences[2] if len(sentences) > 2 else "Đáp án B: Thực thi lệnh trên môi trường chuẩn",
                "slot_opt_c":         sentences[3] if len(sentences) > 3 else "Đáp án C: Tự động tối ưu hóa tài nguyên",
                "slot_correct_opt":   "B",
            })

        # Substitute all slots in template
        rendered_html = template
        for key, value in slots.items():
            rendered_html = rendered_html.replace("{{" + key + "}}", str(value))
        return rendered_html


# Global Singleton Instance for fast import & usage
default_ui_manager = UIManager()

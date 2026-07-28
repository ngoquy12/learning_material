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

COMPONENT_REGISTRY: Dict[str, Dict[str, Any]] = {}


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


def _compute_dynamic_timing(dur: float, n_events: int = 4) -> List[float]:
    start = 4.0
    end = max(dur - 1.5, start + n_events * 0.8)
    step = (end - start) / max(n_events - 1, 1)
    return [round(start + i * step, 2) for i in range(n_events)]


def _clean_ui_text_to_bullets(text: str) -> str:
    """Format long text into clean short bullet items (max 6-7 words per item)."""
    if not text:
        return ""
    if "<pre" in text or "<code" in text or "<ul" in text:
        return text
    clean_text = re.sub(r'\[.*?\]', '', text).strip()
    sentences = [s.strip() for s in re.split(r'[.!?;\n]', clean_text) if len(s.strip()) > 3]
    bullets = []
    for s in sentences:
        words = s.split()
        if len(words) > 8:
            s = " ".join(words[:7])
        if s and s not in bullets:
            bullets.append(s)
    if bullets:
        items_html = "".join(f"<li>{b}</li>" for b in bullets[:4])
        return f"<ul>{items_html}</ul>"
    return f'<div class="desc-text">{clean_text[:60]}</div>'


def _highlight_python_code(code_str: str) -> str:
    import html
    code = html.escape(code_str)
    keywords = [r'\bdef\b', r'\breturn\b', r'\bif\b', r'\belse\b', r'\belif\b', r'\bfor\b', r'\bwhile\b', r'\bimport\b', r'\bfrom\b', r'\bprint\b', r'\bclass\b', r'\bfunction\b', r'\bconst\b', r'\blet\b', r'\bvar\b']
    for kw in keywords:
        code = re.sub(f"({kw})", r'<span class="kw">\1</span>', code)
    code = re.sub(r'(&quot;&quot;&quot;[\s\S]*?&quot;&quot;&quot;|&quot;.*?&quot;|\'.*?\')', r'<span class="str">\1</span>', code)
    code = re.sub(r'(#.*?$|//.*?$)', r'<span class="cm">\1</span>', code, flags=re.MULTILINE)
    code = re.sub(r'\b([a-zA-Z_]\w*)(?=\()', r'<span class="fn">\1</span>', code)
    code = re.sub(r'\b(\d+(?:\.\d+)?)\b', r'<span class="num">\1</span>', code)
    return code


def _format_clean_content_to_html(clean_input: Any, scene_title: str) -> str:
    """
    Converts blueprint clean_content / html_structure into final HTML.

    Priority logic:
    1. If input is already an HTML string (contains any tag) → return as-is.
       AI-generated html_structure is trusted 100%; no card wrapping added.
    2. If input is a structured dict (legacy path) → build card/split layout.
    3. Fallback: wrap plain text in desc-text.
    """
    if isinstance(clean_input, str):
        stripped = clean_input.strip()
        # Detect ANY HTML tag → return AI-generated markup directly
        if stripped and re.search(r'<[a-zA-Z]', stripped):
            return stripped
        # Mermaid diagram without HTML tags
        if "```mermaid" in stripped or stripped.startswith("graph ") or stripped.startswith("flowchart "):
            clean_diagram = stripped.replace("```mermaid", "").replace("```", "").strip()
            return f'<pre class="mermaid" style="font-family: \'Be Vietnam Pro\', sans-serif !important; width: 100%;">{clean_diagram}</pre>'
        # Plain text fallback
        if stripped:
            return f'<p class="desc-text">{stripped}</p>'
        return ""

    if isinstance(clean_input, dict):
        # Legacy structured dict path → build card layout
        badge = clean_input.get("badge", "")
        title = clean_input.get("title", scene_title)
        bullets = clean_input.get("bullets", [])
        code_snippet = clean_input.get("code_snippet", "")
        diagram = clean_input.get("diagram", "") or clean_input.get("mermaid", "")

        bullets_html = "".join(
            f'<li><i class="ph-bold ph-check-circle" style="color:#ba252a;margin-right:14px;margin-top:4px;font-size:26px;flex-shrink:0;"></i><span>{b}</span></li>'
            for b in bullets
        )

        badge_html = f'<span class="card-badge">{badge}</span>' if badge else ""
        header_html = f'<div class="card-header">{badge_html}<h2 class="card-title">{title}</h2></div>' if (badge or title) else ""

        if diagram:
            clean_diagram = diagram.replace("```mermaid", "").replace("```", "").strip()
            return f'''<div class="split-container">
  <div class="card-left">
    {header_html}
    <ul class="bullet-list">{bullets_html}</ul>
  </div>
  <div class="diagram-panel-right">
    <pre class="mermaid" style="font-family: \'Be Vietnam Pro\', sans-serif !important; width: 100%;">
{clean_diagram}
    </pre>
  </div>
</div>'''

        if code_snippet:
            highlighted_code = _highlight_python_code(code_snippet)
            return f'''<div class="split-container">
  <div class="card-left">
    {header_html}
    <ul class="bullet-list">{bullets_html}</ul>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots">
        <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
      </div>
      <span class="code-filename"><i class="ph-bold ph-code" style="margin-right:6px;"></i>python_core.py</span>
    </div>
    <pre class="code-body"><code>{highlighted_code}</code></pre>
  </div>
</div>'''

        # Bullets-only
        return f'''<div class="card-full">
  {header_html}
  <ul class="bullet-list">{bullets_html}</ul>
</div>'''

    return f'<p class="desc-text">{scene_title}</p>'


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

    def normalize_layout_type(self, raw_layout: str) -> str:
        return "standard"

    def is_valid_layout(self, layout_type: str) -> bool:
        return True

    def list_layouts(self) -> List[str]:
        return ["standard"]

    def get_layout_meta(self, layout_type: str) -> Dict[str, Any]:
        return {"name": "Standard Direct HTML", "category": "standard", "rel_path": ""}

    def render_scene(self, scene: Dict[str, Any], lesson_title: str) -> str:
        """
        Render scene HTML.

        Content priority (AI-first, no forced card wrapping):
        1. scene["html_structure"] — raw HTML from AI blueprint (highest priority)
        2. scene["clean_content"]  — fallback if html_structure missing
        3. scene["visual_description"] — last resort plain text
        """
        scene_id = scene["scene_id"]
        scene_n = scene_id.replace("Scene_", "").zfill(2)
        scene_slug = scene_id.replace("_", "-").lower()
        scene_title = scene.get("scene_title", f"Scene {scene_n}")
        if scene_title and scene_title.isupper() and len(scene_title) > 3:
            scene_title = scene_title.capitalize()
        dur = float(scene.get("duration", 30.0))

        # ── AI-first content resolution ─────────────────────────────────────
        raw_html_structure = scene.get("html_structure", "").strip()
        raw_clean_content = scene.get("clean_content", "")

        # Prefer html_structure from AI; fall back to clean_content
        content_source = raw_html_structure or raw_clean_content
        clean_content = _format_clean_content_to_html(content_source, scene_title)

        # Last resort: use visual_description as plain text
        if not clean_content.strip():
            desc = scene.get("visual_description", scene_title)
            clean_content = f'<p class="desc-text">{desc}</p>'

        # Dynamic Skeleton Template File Resolution
        template_file = Path(__file__).parent / "templates" / "light_theme_skeleton.html"
        if template_file.exists():
            template_str = template_file.read_text(encoding="utf-8")
            rendered_html = (
                template_str
                .replace("{scene_n}", str(scene_n))
                .replace("{scene_slug}", str(scene_slug))
                .replace("{scene_title}", str(scene_title))
                .replace("{dur}", str(dur))
                .replace("{clean_content}", str(clean_content))
            )
            return rendered_html.strip()

        # Fallback inline template if template file missing
        template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700&family=Fira+Code:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    /* FIX 1: body transparent — HyperFrames host canvas owns background */
    html, body {{
      width: 1920px; height: 1080px; overflow: hidden;
      background: #0a0a0f; color: #ffffff;
      font-family: 'Be Vietnam Pro', system-ui, -apple-system, sans-serif;
    }}
    .scene-root {{
      width: 1920px; height: 1080px; position: relative; overflow: hidden;
      background: #0a0a0f;
      font-family: 'Be Vietnam Pro', sans-serif;
    }}
    .scene-root::before {{
      content: ''; position: absolute; inset: 0;
      background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
      background-size: 60px 60px; pointer-events: none;
    }}
    .scene-title-header {{
      position: absolute; top: 40px; left: 80px; right: 80px; z-index: 10;
      text-align: left !important; border-bottom: 2px solid rgba(255,255,255,0.15); padding-bottom: 18px;
    }}
    .main-title {{
      font-size: 44px; font-weight: 800; color: #ffffff !important; line-height: 1.25;
      letter-spacing: -0.02em; text-align: left !important; margin: 0; padding: 0;
    }}
    .main-stage {{
      position: absolute; top: 135px; bottom: 40px; left: 80px; right: 80px; z-index: 5;
      display: flex; flex-direction: column; justify-content: flex-start; align-items: flex-start;
      text-align: left !important;
    }}
    /* FIX 3: content-box is naked — no card wrapping, no background */
    .content-box {{
      width: 100%; max-width: 1760px; height: 100%;
      background: transparent; border: none; padding: 0; box-shadow: none;
      text-align: left !important;
    }}
    .split-container {{
      display: grid; grid-template-columns: 1.05fr 1fr; gap: 32px; width: 100%; height: 100%;
      align-items: stretch;
    }}
    .card-full {{
      width: 100%; background: #ffffff; border: 1.5px solid #e2e8f0; border-left: 8px solid #ba252a;
      border-radius: 18px; padding: 36px 44px; box-shadow: 0 12px 32px rgba(15, 23, 42, 0.05);
      text-align: left !important; display: flex; flex-direction: column; justify-content: flex-start; gap: 24px;
    }}
    .card-left {{
      width: 100%; background: #ffffff; border: 1.5px solid #e2e8f0; border-left: 8px solid #ba252a;
      border-radius: 18px; padding: 32px 36px; box-shadow: 0 12px 32px rgba(15, 23, 42, 0.05);
      text-align: left !important; display: flex; flex-direction: column; justify-content: flex-start; gap: 20px;
    }}
    .card-header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }}
    .card-badge {{
      background: #ba252a; color: #ffffff; font-weight: 800; font-size: 20px;
      width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center;
      justify-content: center; box-shadow: 0 4px 12px rgba(186,37,42,0.25); flex-shrink: 0;
    }}
    .card-title {{ font-size: 28px; font-weight: 700; color: #0f172a; line-height: 1.35; margin: 0; }}
    .bullet-list {{
      list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 18px;
      text-align: left !important;
    }}
    .bullet-list li {{
      font-size: 24px; line-height: 1.55 !important; color: #1e293b;
      display: flex; align-items: flex-start; font-family: 'Be Vietnam Pro', sans-serif;
      text-align: left !important; background: transparent; border: none; padding: 0; box-shadow: none;
    }}
    .code-panel-right {{
      width: 100%; background: #0f172a; border: 1.5px solid #1e293b; border-radius: 18px;
      overflow: hidden; box-shadow: 0 16px 36px rgba(15,23,42,0.18);
      display: flex; flex-direction: column; height: 100%;
    }}
    .code-header-bar {{
      background: #1e293b; padding: 14px 22px; border-bottom: 1.5px solid #334155;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .mac-dots {{ display: flex; align-items: center; gap: 8px; }}
    .mac-dots .dot {{ width: 13px; height: 13px; border-radius: 50%; display: inline-block; }}
    .mac-dots .dot.red {{ background: #ff5f56; }}
    .mac-dots .dot.yellow {{ background: #ffbd2e; }}
    .mac-dots .dot.green {{ background: #27c93f; }}
    .code-filename {{ font-family: 'Fira Code', monospace; font-size: 16px; font-weight: 600; color: #38bdf8; }}
    .code-body {{
      padding: 28px 32px; background: #0f172a; flex: 1; margin: 0 !important;
      overflow-x: auto; white-space: pre !important; word-break: normal !important;
      font-family: 'Fira Code', monospace; font-size: 23px; line-height: 1.7 !important;
      color: #f8fafc !important; tab-size: 4; text-align: left !important;
    }}
    .code-body code {{
      background: transparent !important; border: none !important; padding: 0 !important;
      font-family: inherit; font-size: inherit; color: inherit; box-shadow: none !important;
    }}
    .kw  {{ color: #ff7b72 !important; font-weight: 700 !important; }}
    .fn  {{ color: #79c0ff !important; font-weight: 700 !important; }}
    .str {{ color: #7ee787 !important; }}
    .cm  {{ color: #8b949e !important; font-style: italic !important; }}
    .num {{ color: #ffa657 !important; font-weight: 600 !important; }}
    .desc-text {{ font-size: 30px; font-weight: 600; color: #334155; text-align: left !important; line-height: 1.6; }}
  </style>
</head>
<body>
  <div id="scene-{scene_n}" class="scene-root clip" data-composition-id="scene-{scene_n}" data-start="0" data-duration="{dur}" data-track-index="0">
    <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Rikkei Academy" class="rikkei-logo clip" data-start="0" data-duration="{dur}" data-track-index="5">
    <div class="scene-title-header clip" data-start="0" data-duration="{dur}" data-track-index="10">
      <h1 class="main-title">{scene_title}</h1>
    </div>
    <div class="main-stage clip" data-start="0.5" data-duration="{dur}" data-track-index="20">
      <div class="content-box">
        {clean_content}
      </div>
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["{scene_slug}"] = tl;

    const _buildTimer = setInterval(function() {{
      const root = document.getElementById("scene-{scene_n}");
      if (!root) return;
      clearInterval(_buildTimer);

      const dur = parseFloat(root.getAttribute("data-duration")) || parseFloat("{dur}");
      const durEnd = Math.max(0.1, dur - 0.8);

      /* All elements start invisible */
      tl.set(".clip",        {{ autoAlpha: 1 }}, 0);
      tl.set(".main-title",  {{ autoAlpha: 0, x: -30 }}, 0);
      tl.set(".rikkei-logo", {{ autoAlpha: 0 }}, 0);
      tl.set(".main-stage",  {{ autoAlpha: 0 }}, 0);

      tl.to(".rikkei-logo", {{ autoAlpha: 1, duration: 0.5, ease: "power2.out" }}, 0.1);
      tl.to(".main-title",  {{ autoAlpha: 1, x: 0, duration: 0.7, ease: "power2.out" }}, 0.2);
      tl.to(".main-stage",  {{ autoAlpha: 1, duration: 0.4, ease: "none" }}, 0.6);

      /* Universal stagger: any direct children of content-box */
      const topItems = Array.from(root.querySelectorAll(".content-box > *"));
      let cursor = 1.1;
      if (topItems.length > 0) {{
        tl.set(topItems, {{ autoAlpha: 0, y: 28 }}, 0);
        const topStep = Math.max(0.35, (durEnd * 0.55) / topItems.length);
        topItems.forEach((item, idx) => {{
          tl.to(item, {{ autoAlpha: 1, y: 0, duration: 0.65, ease: "power2.out" }}, cursor + idx * topStep);
        }});
        cursor += topItems.length * topStep;
      }}

      const liItems = root.querySelectorAll(".bullet-list li, .step-list li");
      if (liItems.length > 0) {{
        tl.set(liItems, {{ autoAlpha: 0, y: 18 }}, 0);
        const liStep = Math.max(0.22, (durEnd - cursor - 1.2) / liItems.length);
        liItems.forEach((li, idx) => {{
          tl.to(li, {{ autoAlpha: 1, y: 0, duration: 0.5, ease: "power2.out" }}, cursor + 0.3 + idx * liStep);
        }});
      }}

      tl.to("#scene-{scene_n}", {{ autoAlpha: 0, duration: 0.8 }}, durEnd);
      tl.set({{}}, {{}}, dur);
    }}, 50);
  </script>
</body>
</html>"""

        return template.strip()



# Global Singleton Instance for fast import & usage
default_ui_manager = UIManager()

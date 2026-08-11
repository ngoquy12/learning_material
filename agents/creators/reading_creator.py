# agents/creators/reading_creator.py
import json
import re
import html
from pathlib import Path
from typing import Dict, Any, List
from core.state import AgentState
from core.llm import call_llm
from core.skills import load_skill_content
from agents.creators.common_utils import (
    get_lesson_content,
    clean_unwanted_text,
    ensure_vietnamese_diacritics
)

def ensure_sentence_ending_period(text: str) -> str:
    """Ensures text string ends with a proper punctuation mark (., ?, !, :, >)."""
    t = text.strip()
    if not t:
        return ""
    if t[-1] not in ('.', '?', '!', ':', '>', ';'):
        return t + '.'
    return t

def convert_markdown_to_html(md_text: str) -> str:
    """Converts basic markdown formatting into clean HTML elements."""
    if not md_text:
        return ""
    
    # Process code blocks
    def _replace_code_block(match):
        lang = match.group(1) or "python"
        code_content = html.escape(match.group(2).strip())
        return f'<div class="my-4 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm"><div class="px-4 py-2 bg-slate-100 text-xs font-mono text-slate-700 border-b border-slate-200 flex justify-between"><span>{lang.upper()} CODE</span></div><pre class="p-4 m-0 overflow-x-auto"><code class="hljs language-{lang}">{code_content}</code></pre></div>'

    md_text = re.sub(r'```(\w+)?\n(.*?)```', _replace_code_block, md_text, flags=re.DOTALL)
    
    # Inline code with html.escape for safety
    md_text = re.sub(r'`([^`]+)`', lambda m: f'<code class="px-1.5 py-0.5 rounded bg-slate-100 text-rikkei-red font-mono text-sm">{html.escape(m.group(1))}</code>', md_text)
    
    # Bold text
    md_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="font-semibold text-slate-900 dark:text-white">\1</strong>', md_text)
    
    # Process paragraphs and lists
    lines = md_text.splitlines()
    html_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
            
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append('<ul class="list-disc pl-6 space-y-2 text-slate-600 dark:text-slate-300 my-4">')
                in_list = True
            content = stripped[2:]
            html_lines.append(f'<li>{ensure_sentence_ending_period(content)}</li>')
        elif stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h3 class="font-montserrat font-bold text-xl text-slate-900 dark:text-white mt-6 mb-3">{stripped[4:]}</h3>')
        elif stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h2 class="font-montserrat font-bold text-2xl text-slate-900 dark:text-white mt-8 mb-4">{stripped[3:]}</h2>')
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if not stripped.startswith("<div") and not stripped.startswith("<pre") and not stripped.startswith("<ul") and not stripped.startswith("<h"):
                html_lines.append(f'<p class="text-slate-600 dark:text-slate-300 mb-4 leading-relaxed">{ensure_sentence_ending_period(stripped)}</p>')
            else:
                html_lines.append(stripped)
                
    if in_list:
        html_lines.append("</ul>")
        

# ─────────────────────────────────────────────────────────────────────────────
# PROBLEM 1 IMPLEMENTATION: LLM, JSON PARSING & DIAGRAM GUARDS
# ─────────────────────────────────────────────────────────────────────────────

LANGUAGE_MAPPING_REGISTRY = {
    "python": {"hljs": "language-python", "engine": "pyodide", "name": "Python"},
    "py": {"hljs": "language-python", "engine": "pyodide", "name": "Python"},
    "javascript": {"hljs": "language-javascript", "engine": "js_worker", "name": "JavaScript"},
    "js": {"hljs": "language-javascript", "engine": "js_worker", "name": "JavaScript"},
    "typescript": {"hljs": "language-typescript", "engine": "js_worker", "name": "TypeScript"},
    "ts": {"hljs": "language-typescript", "engine": "js_worker", "name": "TypeScript"},
    "java": {"hljs": "language-java", "engine": "code_tracker", "name": "Java"},
    "c": {"hljs": "language-c", "engine": "code_tracker", "name": "C"},
    "cpp": {"hljs": "language-cpp", "engine": "code_tracker", "name": "C++"},
    "c++": {"hljs": "language-cpp", "engine": "code_tracker", "name": "C++"},
    "sql": {"hljs": "language-sql", "engine": "sql_sim", "name": "SQL"},
    "html": {"hljs": "language-xml", "engine": "code_tracker", "name": "HTML"},
    "css": {"hljs": "language-css", "engine": "code_tracker", "name": "CSS"},
}

def resolve_language_info(tech_stack: str) -> Dict[str, str]:
    """Resolve language metadata from tech_stack string."""
    tech_lower = (tech_stack or "python").lower().strip()
    # Check if the tech stack is a known non-coding / CLI / tooling / theory subject
    non_coding_keywords = [
        "git", "vcs", "github", "gitlab", "terminal", "bash", "shell", "cli", "cmd",
        "powershell", "docker", "kubernetes", "devops", "linux", "unix",
        "agile", "scrum", "diagram", "uml", "design", "word", "excel", "powerpoint",
        "office", "tin học văn phòng", "phân tích", "thiết kế", "phân tích và thiết kế",
        "phân tích thiết kế", "system analysis", "software architecture", "kiến trúc",
        "management", "devops", "pm", "theory", "concept", "process", "quy trình"
    ]
    if any(kw in tech_lower for kw in non_coding_keywords):
        is_cli = any(kw in tech_lower for kw in ["git", "vcs", "github", "gitlab", "terminal", "bash", "shell", "cli", "cmd", "powershell", "docker", "devops", "linux", "unix"])
        return {
            "hljs": "language-bash" if is_cli else "language-plaintext",
            "engine": "static",
            "name": tech_stack or ("Git/CLI" if is_cli else "Theory")
        }
        
    for key, info in LANGUAGE_MAPPING_REGISTRY.items():
        if key in tech_lower:
            return info
    return {"hljs": "language-python", "engine": "pyodide", "name": tech_stack or "Code"}


def sanitize_llm_json_text(raw_text: str) -> str:
    """Pre-sanitize raw LLM response to remove invalid control chars before JSON parsing."""
    if not raw_text:
        return ""
    # Strip ASCII control characters except \n, \r, \t
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw_text)
    return cleaned


def guard_svg_syntax(svg_str: str) -> str:
    """
    Guards and sanitizes SVG syntax:
    - Auto-injects xmlns if missing
    - Auto-injects class="rikkei-diagram"
    - Auto-injects Inter font family & marker styles
    - Fixes dark mode marker arrow contrast
    - Converts ALL CAPS text inside SVG to Title Case
    - Ensures viewBox exists
    - Wraps in container .diagram-wrap with adaptive dark mode styling
    """
    if not svg_str or "<svg" not in str(svg_str):
        return svg_str
    
    svg_clean = str(svg_str).strip()

    # 1. Strip pre-existing dark wrapper divs around SVG
    svg_clean = re.sub(r'^\s*<div\s+class="[^"]*\b(bg-slate-900|bg-black|bg-slate-800|bg-slate-950)\b[^"]*">\s*(<svg\b)', r'\2', svg_clean, flags=re.DOTALL)
    svg_clean = re.sub(r'(</svg>)\s*</div>\s*$', r'\1', svg_clean, flags=re.DOTALL)


    # 2. Inject xmlns if missing
    if 'xmlns=' not in svg_clean:
        svg_clean = re.sub(r'<svg\b', '<svg xmlns="http://www.w3.org/2000/svg"', svg_clean, count=1)
    
    # 3. Inject rikkei-diagram class if missing
    if 'rikkei-diagram' not in svg_clean:
        if 'class="' in svg_clean:
            svg_clean = re.sub(r'class="([^"]*)"', r'class="\1 rikkei-diagram"', svg_clean, count=1)
        else:
            svg_clean = re.sub(r'<svg\b', '<svg class="rikkei-diagram"', svg_clean, count=1)

    # 4. Inject font-family and marker arrow styles inside SVG <style>
    style_block = '''<style>
      text, tspan { font-family: "Inter", system-ui, -apple-system, sans-serif !important; }
      .font-mono { font-family: "JetBrains Mono", monospace !important; }
      marker path, marker polygon { fill: currentColor !important; stroke: currentColor !important; }
    </style>'''
    if '<style>' not in svg_clean:
        svg_clean = re.sub(r'(<svg\b[^>]*>)', r'\1' + style_block, svg_clean, count=1)

    # 5. Inject font-family attribute directly into <text> tags if missing
    def ensure_text_font(m):
        attrs = m.group(1)
        if 'font-family' not in attrs:
            return f'<text font-family="Inter, system-ui, sans-serif" {attrs}>'
        return m.group(0)
    svg_clean = re.sub(r'<text\b([^>]*)>', ensure_text_font, svg_clean)

    # 6. Convert ALL CAPS text inside <text> elements to Title Case
    def fix_all_caps_text(match):
        open_tag = match.group(1)
        text_content = match.group(2)
        close_tag = match.group(3)
        if len(text_content.strip()) > 3 and text_content.strip().isupper():
            text_content = text_content.strip().title()
        return f"{open_tag}{text_content}{close_tag}"
    svg_clean = re.sub(r'(<text\b[^>]*>)(.*?)(</text>)', fix_all_caps_text, svg_clean, flags=re.DOTALL)
            
    # 7. Ensure viewBox exists (default to 0 0 800 280 if missing)
    if 'viewBox' not in svg_clean:
        svg_clean = re.sub(r'<svg\b', '<svg viewBox="0 0 800 280"', svg_clean, count=1)
        
    # 8. Wrap in simple container div (no border/padding/background per design spec)
    if not svg_clean.startswith('<div class="my-'):
        svg_clean = f'<div class="my-6">{svg_clean}</div>'
        
    # 9. Lowercase hex fill attributes & strip background dark rects
    svg_clean = re.sub(r'fill="#([0-9A-Fa-f]{3,6})"', lambda m: f'fill="#{m.group(1).lower()}"', svg_clean)
    svg_clean = re.sub(
        r'<rect\b[^>]*(?:width="(?:100%|800|1000|1200)"[^>]*fill="(?:#0f172a|#1e293b|#0b0f19|#000000|#000|black)"|fill="(?:#0f172a|#1e293b|#0b0f19|#000000|#000|black)"[^>]*width="(?:100%|800|1000|1200)")[^>]*/>',
        '',
        svg_clean
    )
    # 10. Strip stray '|' characters from SVG text elements
    svg_clean = re.sub(r'(<text\b[^>]*>)\s*\|+\s*', r'\1', svg_clean)

    # 11. Ensure all <text...> tags are properly closed with </text> and contain no broken HTML tags
    def sanitize_svg_text_tag(match):
        open_tag = match.group(1)
        body = match.group(2)
        close_tag = match.group(3) if match.group(3) else "</text>"
        # Remove any stray HTML tags like </div> or <p> inside SVG text body
        clean_body = re.sub(r'</?(?:div|p|span|section|h[1-6])\b[^>]*>', '', body)
        return f"{open_tag}{clean_body}{close_tag}"

    svg_clean = re.sub(r'(<text\b[^>]*>)(.*?)(</text>|(?=<text\b|</svg>|$))', sanitize_svg_text_tag, svg_clean, flags=re.DOTALL | re.IGNORECASE)

    svg_clean = re.sub(r'\|\s*</tspan>', '</tspan>', svg_clean)
    return svg_clean


def sanitize_mermaid_code(code: str) -> str:
    """
    Sanitizes raw Mermaid diagram code to prevent 'Syntax error in text' in Mermaid JS:
    1. Fixes transition labels: 'D -- Gặp lỗi build -- > C' or 'D -- Gặp lỗi build --> C' -> 'D -->|Gặp lỗi build| C'
    2. Fixes broken arrows with spaces: '-- >' or '- ->' -> '-->'
    3. Quotes unquoted node labels containing special chars (/, :, (, ), ?, &, %, etc.)
    """
    if not code:
        return code

    lines = code.split("\n")
    cleaned_lines = []
    for line in lines:
        l = line
        
        # 1. Fix transition labels: e.g. 'D -- Gặp lỗi build --> C' or 'D -- Gặp lỗi build -- > C' -> 'D -->|Gặp lỗi build| C'
        l = re.sub(r'(\b\w+|[}\]\)])\s*--\s+([^->\n|]+?)\s*--*\s*>\s*(\b\w+|[{\[\(])', r'\1 -->|\2| \3', l)
        
        # 2. Fix broken arrow with spaces before >: e.g. '-- >', '- ->', '--  >'
        l = re.sub(r'--+\s+>', '-->', l)
        l = re.sub(r'-\s+->', '-->', l)

        # 3. Clean up malformed parallelogram nodes A["[/Label/]"] or A["/Label/"] -> A[/"Label"/]
        l = re.sub(r'(\b[A-Za-z0-9_-]+)\["/*\s*([^"\n]+?)\s*/*"\]', r'\1[/"\2"/]', l)

        # 4. Quote unquoted parallelogram nodes [/Label/] -> [/"Label"/]
        def quote_para(m):
            nid, lbl = m.group(1), m.group(2).strip()
            if lbl.startswith('"') and lbl.endswith('"'):
                return f'{nid}[/{lbl}/]'
            safe_lbl = lbl.replace('"', "'")
            return f'{nid}[/"{safe_lbl}"/]'
        l = re.sub(r'(\b[A-Za-z0-9_-]+)\[/([^"\n/]+)/\]', quote_para, l)

        # 5. Quote unquoted rectangular nodes [Label] -> ["Label"]
        def quote_rect(m):
            nid, lbl = m.group(1), m.group(2)
            if lbl.startswith('/') or lbl.startswith('"'):
                return m.group(0)
            if re.search(r'[/:\(\)&?\*\+%,;=\'\s-]', lbl):
                safe_lbl = lbl.replace('"', "'")
                return f'{nid}["{safe_lbl}"]'
            return m.group(0)
        l = re.sub(r'(\b[A-Za-z0-9_-]+)\[([^"\n\[\]]+)\]', quote_rect, l)

        # 6. Quote unquoted rhombus / diamond nodes {Label} -> {"Label"}
        def quote_rhombus(m):
            nid, lbl = m.group(1), m.group(2)
            if lbl.startswith('"') and lbl.endswith('"'):
                return f'{nid}{{{lbl}}}'
            if re.search(r'[/:\(\)&?\*\+%,;=\'\s-]', lbl):
                safe_lbl = lbl.replace('"', "'")
                return f'{nid}{{"{safe_lbl}"}}'
            return m.group(0)
        l = re.sub(r'(\b[A-Za-z0-9_-]+)\{([^"\n\{\}]+)\}', quote_rhombus, l)

        cleaned_lines.append(l)

    return "\n".join(cleaned_lines)


def guard_mermaid_syntax(text: str) -> str:
    """
    Guards Mermaid syntax across HTML (<pre/div class="mermaid">) and Markdown (```mermaid ... ```).
    Applies sanitize_mermaid_code to all Mermaid diagram blocks in the text.
    """
    if not text or "mermaid" not in text.lower():
        return text

    # Process Markdown blocks: ```mermaid ... ```
    def fix_md_mermaid(match):
        fence_start = match.group(1)
        code = match.group(2)
        fence_end = match.group(3)
        sanitized = sanitize_mermaid_code(code)
        return f"{fence_start}\n{sanitized}\n{fence_end}"

    text = re.sub(r'(```\s*mermaid[\r\n]+)(.*?)(```)', fix_md_mermaid, text, flags=re.DOTALL | re.IGNORECASE)

    # Process HTML blocks: <pre class="...mermaid...">...</pre> or <div class="...mermaid...">...div>
    def fix_html_mermaid(match):
        open_tag = match.group(1)
        code = match.group(2)
        close_tag = match.group(3)
        sanitized = sanitize_mermaid_code(code)
        return f"{open_tag}{sanitized}{close_tag}"

    text = re.sub(r'(<(?:pre|div)[^>]*class="[^"]*mermaid[^"]*"[^>]*>)(.*?)(</(?:pre|div)>)', fix_html_mermaid, text, flags=re.DOTALL | re.IGNORECASE)

    return text


def slugify_id(text: str) -> str:
    """
    Problem 2.2: Convert Vietnamese text into a clean kebab-case ID for robust TOC anchors.
    Example: '2.1. Cú pháp và cách dùng' -> 'sec-2-1-cu-phap-va-cach-dung'
    """
    if not text:
        return "sec-anchor"
    import unicodedata
    nfkd = unicodedata.normalize('NFKD', text)
    no_accent = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    clean = re.sub(r'[^a-zA-Z0-9]+', '-', no_accent.lower()).strip('-')
    return f"sec-{clean}" if clean else "sec-anchor"


# ─────────────────────────────────────────────────────────────────────────────
# PROBLEM 3 IMPLEMENTATION: PEDAGOGY, SCOPE BOUNDARY & RAM ISOLATION
# ─────────────────────────────────────────────────────────────────────────────

FORBIDDEN_INTRO_CONCEPTS = [
    ("try-except", ["try:", "except ", "except:", "raise "]),
    ("OOP / Class", ["class ", "__init__", "self."]),
    ("Advanced Decorator", ["@staticmethod", "@classmethod", "@property"]),
    ("Async / Concurrency", ["async def", "await ", "asyncio"]),
    ("Lambda / Functional", ["lambda ", "map(", "filter("]),
]

def validate_scope_boundary(html_content: str, is_intro_lesson: bool = True) -> List[str]:
    """
    Problem 3.1: Check if introductory HTML content violates scope boundary by using advanced concepts.
    Returns list of scope violation warnings.
    """
    if not html_content or not is_intro_lesson:
        return []
    violations = []
    for concept, keywords in FORBIDDEN_INTRO_CONCEPTS:
        for kw in keywords:
            if kw in html_content:
                violations.append(f"Scope Violation: Concept '{concept}' ('{kw}') found in introductory reading.")
                break
    return violations


CANONICAL_DOC_LINKS = {
    "python": [
        {"title": "Trang chủ Tài liệu Chính thức Python 3", "url": "https://docs.python.org/3/"},
        {"title": "Hướng dẫn Cú pháp và Kiểu dữ liệu Python (MDN)", "url": "https://developer.mozilla.org/en-US/docs/Glossary/Python"}
    ],
    "javascript": [
        {"title": "Tài liệu Lập trình JavaScript (MDN Web Docs)", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"}
    ],
    "sql": [
        {"title": "Hướng dẫn Cú pháp SQL Chuẩn (W3Schools)", "url": "https://www.w3schools.com/sql/"}
    ],
    "c": [
        {"title": "Tài liệu Ngôn ngữ Lập trình C (cppreference)", "url": "https://en.cppreference.com/w/c"}
    ],
    "cpp": [
        {"title": "Tài liệu Ngôn ngữ C++ (cppreference)", "url": "https://en.cppreference.com/w/cpp"}
    ],
    "java": [
        {"title": "Tài liệu Ngôn ngữ Java (Oracle)", "url": "https://docs.oracle.com/en/java/"}
    ]
}

def sanitize_references(refs: List[Dict[str, str]], tech_stack: str) -> List[Dict[str, str]]:
    """
    Problem 3.3: Sanitize reference links, replacing hallucinated or empty URLs with canonical official docs.
    """
    valid_refs = []
    if isinstance(refs, list):
        for r in refs:
            if isinstance(r, dict):
                url = (r.get("url") or "").strip()
                title = (r.get("title") or "").strip()
                if url.startswith("http://") or url.startswith("https://"):
                    valid_refs.append({"title": title or url, "url": url})

    # If LLM returned no valid URLs, inject canonical links based on tech stack
    if not valid_refs:
        tech_key = (tech_stack or "python").lower().strip()
        for k, links in CANONICAL_DOC_LINKS.items():
            if k in tech_key:
                return links
        return CANONICAL_DOC_LINKS["python"]
    return valid_refs


def generate_reading_html(
    session_id: str,
    lesson_id: str,
    lesson_title: str,
    lesson_details: str,
    expected_output: str,
    tech_stack: str,
    state: AgentState
) -> str:
    """
    Generate reading.html file adhering to 5-section pedagogical structure.
    """
    print(f"\n  ---> [Reading Creator SSOT] Authoring reading.html for {session_id} - {lesson_id}: {lesson_title}...")
    
    image_skill = load_skill_content("image_prompt_standard")
    
    system_prompt = f"""You are a Senior Learning Content Authoring Expert at Rikkei Education.
Your task is to author a DETAILED READING MATERIAL (SSOT) strictly adhering to the 5-SECTION PEDAGOGICAL ARCHITECTURE.

MANDATORY RULES & DIRECTIVES:
1. 5-SECTION PEDAGOGICAL FLOW:
   - Section 1 - DYNAMIC TITLE: You MUST create a context-aware Section 1 title matching the lesson topic (e.g., "Why use Functions?", "Problems without Loops", "Why Virtual Environments?"). Never use generic titles like "Introduction". Save title in `section1_title`.
   - Section 2 - DYNAMIC TITLE: You MUST create a context-aware Section 2 title detailing the knowledge concept (e.g., "Syntax & Operational Mechanism of Functions", "Installation & Environment Setup"). Save title in `section2_title`.
   - Section 1 CONTENT: Detailed & specific enterprise real-world scenario (e.g. ShopeeFood order checkout engine). Analyze the technical conflict and financial/business risks of running code sequentially line-by-line without conditional checks (e.g. negative revenue from small freeship orders vs user churn from overcharging shipping). Introduce current lesson concept as the dynamic decision solution.
   - Section 2 CONTENT: Core concepts, technical breakdown in HTML format using `<ul class="...">` and `<strong class="...">` for keywords.
   - Section 3: Practical Application Examples (Execution code snippet + HTML explanation).
   - Section 4: Summary & Enterprise Gotchas (Common pitfalls in HTML format).
   - Section 5: References.

2. HTML DATA FORMAT & CALLOUT BOX SYSTEM:
   - DO NOT use Markdown syntax (such as **, ###, - ).
   - Return clean HTML elements directly: `<p class="text-slate-600 mb-4 leading-relaxed">`, `<ul class="list-disc pl-6 space-y-2 text-slate-600 my-4">`, `<strong class="font-semibold text-slate-900">`, `<code class="px-1.5 py-0.5 rounded bg-slate-100 text-rikkei-red font-mono text-sm">`.
   - MUST use strict Callout Box color system by role:
     * 🟠 **Warning/Note**: Orange -> `<div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">`
     * 🔴 **Error/Gotchas**: Red -> `<div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">`
     * 🟢 **Success/Best Practice**: Green -> `<div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50/60 text-slate-800 my-4">`
     * 🔵 **Tip/Info**: Blue -> `<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">`

3. 2D FLAT VECTOR DIAGRAM / IMAGE STANDARD (SECTION 1):
   - In Section 1, MUST include a 2D Flat Vector Technical Illustration / Diagram (16:9 widescreen ratio) depicting a direct comparison (e.g. Legacy manual approach vs New optimized approach).
   - Supports clean 2D Flat Vector Images (`<img src="images/..." alt="..." class="w-full h-auto mx-auto rounded-xl" />`) created via image generation tools following `image_prompt_standard` skill, or clean 16:9 SVG (`viewBox="0 0 800 280"`). No outer border, no shadow boxes, no forced object-cover cropping that clips text.
   - Ensures ultra-high visual quality, prevents UI text truncation or layout breakage, and delivers modern 2D flat technical graphics.
{image_skill}

4. STRICT NO EMOJI TEXT:
   - ABSOLUTELY FORBIDDEN to use text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶). Use Phosphor Icons SVG / CSS symbols only.

5. MANDATORY SENTENCE ENDING PERIOD DIRECTIVE:
   - Every text sentence, list item, bullet point, question, and explanation MUST 100% end with a period (.). Never leave sentences unpunctated.

6. SECTION 3 PROGRESSIVE EXAMPLES & CODE BLOCK RULE:
   - Section 3 MUST provide 1 to 3 progressive examples: Example 3.1 (Minimal syntax) ➔ Example 3.2 (Business problem) ➔ Example 3.3 (Enterprise production).
   - EACH EXAMPLE (`3.1`, `3.2`, `3.3`) MUST be accompanied by an execution code block: `<pre><code class="language-TECH">...</code></pre>`. Replace `TECH` with target language identifier (e.g. `python`, `javascript`, `typescript`, `java`, `c`, `cpp`, `sql`). Never hardcode `python` for non-Python subjects.

7. HIERARCHICAL SUB-HEADING NUMBERING DIRECTIVE:
   - All `<h3>` sub-headings MUST match parent numbering: Section 2 sub-headings MUST be `2.1`, `2.2`, `2.3...`; Section 3 sub-headings MUST be `3.1`, `3.2`, `3.3...`; Section 4 sub-headings MUST be `4.1`, `4.2...`.

8. MINIMAL ITALIC TEXT DIRECTIVE:
   - Minimize italic text (`<i>`, `<em>`). Only use italics for captions directly below images/diagrams (e.g., `<p class="text-center text-sm text-slate-500 italic mt-3">Diagram caption...</p>`).

9. CONTEXT-AWARE THEORY INTEGRATION DIRECTIVE:
   - In Section 2 (`knowledge_html`), integrate visual snippets matching topic nature:
     * For programming/syntax topics: Include code syntax snippets under each `2.1`, `2.2` sub-heading alongside Syntax Anatomy / Memory diagrams.
     * For conceptual / setup / tool topics (Git, VS Code, Agile): Include SVG/Mermaid flowcharts, Terminal commands, or Config tables instead of empty sandboxes.

10. TARGET OUTPUT LANGUAGE CONTRACT:
    - Target Output Language: 100% Production-Grade Accented Vietnamese for explanations outside code.

11. STRICT STANDALONE CODE BLOCK DIRECTIVE (NO CALLOUT NESTING & NO CUSTOM WRAPPERS):
    - DO NOT wrap code blocks (`<pre><code>...</code></pre>`) or syntax templates inside callout boxes (`<div class="p-4 rounded-xl border...">`), cards, or any custom `<div>` containers.
    - BAD: `<div class="border rounded bg-white"><pre><code class="language-python">...</code></pre></div>`
    - GOOD: `<pre><code class="language-python">...</code></pre>` (Place directly as standalone, the system will automatically wrap it in a card later).

12. 100% ENGLISH CODE SYNTAX & IDENTIFIERS CONTRACT:
    - ALL code snippets, syntax templates, variable names, function names, parameter names, data structures, syntax placeholders (e.g., `condition`, `statement_block`), and code comments inside code blocks MUST BE 100% IN ENGLISH using standard language conventions (`snake_case` for Python e.g. `order_amount`, `shipping_fee`, `is_vip_customer`, `discount_amount`, `total_payment`).
    - ABSOLUTELY FORBIDDEN to use Vietnamese words, transliterated Vietnamese, or diacritics inside code blocks or placeholders (e.g., NEVER use `don_hang`, `phi_ship`, `la_khach_vip`, `giam_gia`, `thanh_tien`, `đieu_kien`, `khoi_lenh_thuc_thi`).

13. CODE CARD TITLES STANDARD (NO ALL CAPS):
    - Titles on code cards MUST be specific and written in Title Case / Sentence Case (e.g., `Cú pháp khai báo câu lệnh for trong Python`).
    - ABSOLUTELY FORBIDDEN to use generic UPPERCASE titles like `PYTHON CÚ PHÁP` or `PYTHON CODE`.

14. SYNCHRONIZED SYNTAX EXPLANATION CONTRACT:
    - Every explanation bullet item following a syntax code block MUST use the EXACT SAME parameter/identifier names as used inside the code block verbatim (e.g., if code uses `item` and `iterable_object`, bullet items MUST explain `item` and `iterable_object` verbatim).

15. STRICT LIGHT MODE ONLY CONTRACT:
    - All generated content MUST be 100% in Light Mode with balanced, pleasant corporate colors (`bg-white`, `bg-slate-50`, `border-slate-200`, `text-slate-900`, `text-slate-700`).
    - ABSOLUTELY FORBIDDEN to use dark background panels (`bg-slate-900`, `bg-black`), dark container cards, or dark mode overrides.

16. STRICT KNOWLEDGE SCOPE BOUNDARY CONTRACT (NO FUTURE/UNLEARNED CONCEPTS & NO COMMAND LEAKS):
    - All concepts, explanations, code snippets, CLI commands, data structures, and diagrams MUST strictly stay within the knowledge taught up to the current session/lesson (`lesson_details` and `previous_lessons`).
    - CRITICAL INTRODUCTORY LESSON SCOPE RULE: For Introductory / Overview / Theory / Concept lessons (e.g. Lesson 01 "Giới thiệu Hệ thống quản lý phiên bản VCS", "Overview", "Concepts", "Architecture", "Agile Overview", "Python Overview"):
      * The lesson's purpose is ONLY to introduce high-level concepts, business pain points, architectural comparisons (Centralized vs Distributed, Manual ZIP vs Version Control), and high-level 2D/SVG diagrams.
      * ABSOLUTELY FORBIDDEN to introduce concrete execution command sequences (e.g., `git init`, `git add`, `git commit`, `git push`, `docker run`, `try-except`, `class MyClass`, etc.) that belong to future dedicated lessons!
      * Content MUST focus 100% on Conceptual Rationale, High-Level Problem Statements, 2D Flat Vector Infographics, SVG Process Diagrams, and Parameter/Concept Comparison Tables.

17. SYNTAX PRESENTATION ORDER & HIGHLIGHTED EXPLANATION CONTRACT:
    - ALWAYS present the Syntax Card Component FIRST, followed immediately by the Component Explanation Bullet List.
    - Each keyword or placeholder in the explanation list MUST be highlighted with code badges (`<code class="px-1.5 py-0.5 rounded bg-slate-100 text-rikkei-red font-mono text-sm">...</code>`) and bold font.

18. ADAPTIVE VISUALS & VISUALIZER HIDING CONTRACT (SUBJECT NATURE & LESSON TYPE ADAPTIVE):
    - Analyze the lesson's nature before generating Section 2 (`knowledge_html`):
      * FOR PURE CONCEPT / OVERVIEW / ARCHITECTURE / METHODOLOGY / INTRO LESSONS (where step-by-step interactive code execution or step-by-step CLI tracking is NOT applicable or where no execution commands/code exist yet):
        - ABSOLUTELY FORBIDDEN to force fake/empty Interactive Code Step-Tracker Visualizers. HIDE / OMIT the Interactive Step-Tracker Visualizer widget entirely for these lessons!
        - INSTEAD: Embed Rich 2D Flat Vector Technical Illustrations, SVG Process Flowcharts, Mermaid Diagrams, or High-Contrast Concept Comparison Cards!
      * FOR EXECUTABLE PROGRAMMING / OPERATIONAL / ALGORITHM / WORKFLOW EXECUTION LESSONS (where actual code/commands are executed step-by-step):
        - Embed the 100% Runnable Step-by-Step Interactive Mechanism Visualizer with Play/Pause/Step controls and line highlighting.

19. SUBJECT NATURE & CODE CARD ADAPTATION CONTRACT (EXECUTABLE PROGRAMMING VS PURE CONCEPT / TOOLING / CLI / ARCHITECTURE):
    - You MUST analyze the course and lesson nature:
      * FOR EXECUTABLE PROGRAMMING LANGUAGES (Python, JavaScript, Java, C++, SQL...): Section 3 practical examples use Live Executable Code Sandboxes (with Run & Console Output buttons).
      * FOR PURE CONCEPT / TOOLING / PROCESS / CLI / ARCHITECTURE (Git, VS Code, Linux/Bash CLI, Docker CLI, Agile/Scrum, Software Architecture, System Design, UML Analysis & Design...): ABSOLUTELY FORBIDDEN to force live executable Pyodide sandboxes or run buttons. Section 3 MUST use static Terminal Command Blocks (`<pre><code class="language-bash">...</code></pre>`), Command Execution Flow Tables, or Workflow Diagram Cards.

20. MANDATORY CODE DEMO FOR ALL SYNTAX VARIANTS CONTRACT:
    - EVERY subsection in Section 2 (`2.1`, `2.2`, `2.3`, `2.4`) introducing syntax variants MUST present:
      1. The Syntax Code Card for that variant.
      2. The Enterprise Business Problem Callout Box placed directly BEFORE the code sandbox.
      3. The concrete Code Demo Sandbox Snippet.
      4. The Component Explanation Bullet List with highlighted terms (`<code>...</code>`).

21. INTERACTIVE VISUALIZER COLOR & VIETNAMESE UI CONTRACT:
    - Visualizer component MUST use Light Mode colors: `bg-slate-50 border border-slate-200 text-slate-800`.
    - ALL UI button labels and panel headers MUST be written in friendly Accented Vietnamese (Title: `Mô phỏng cơ chế vận hành từng bước`, Buttons: `Tiếp theo`, `Lùi lại`, `Thử lại`, `Tự động chạy`, Memory Panel: `Bảng bộ nhớ & Trạng thái biến`).
    - Visualizer buttons MUST use high-contrast Tailwind classes:
      * Nút "Tiếp theo": Rikkei Red `bg-[#be111c] text-white hover:bg-[#90000a]`.
      * Nút "Lùi lại" / "Thử lại": `bg-slate-200 hover:bg-slate-300 text-slate-800`.
      * Nút "Tự động chạy": `bg-emerald-600 hover:bg-emerald-700 text-white`.
      * All buttons must have class `px-3 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition-all`.
    - Inactive code lines MUST use high-contrast dark slate text (`color: #475569 !important; font-weight: 500`). NEVER use faint gray (`text-slate-300` / `#cbd5e1`) or white text on light backgrounds!
    - The Memory Panel MUST display variables in a clean, high-contrast HTML table (`<table class="w-full text-xs text-left">`). ABSOLUTELY FORBIDDEN to wrap variable values or memory state indicators inside code cards, pre/code tags, or colored block boxes!
    - CRITICAL: You MUST use these exact IDs for the dynamic elements so the JavaScript works: `id="viz-var-sum"` (for sum/total variable), `id="viz-var-number"` (for the loop counter variable), and `id="viz-console"` (for the console output div).

22. VISUALIZER CODE SYNTAX HIGHLIGHTING & NO LINE NUMBERS CONTRACT:
    - Code lines displayed inside the Step-by-Step Visualizer panel MUST use syntax highlighting matching the language (e.g., `<span class="kw">for</span>`, `<span class="fn">print</span>`, `<span class="num">10</span>`, `<span class="str">"text"</span>`).
    - 🚨 FATAL UX ERROR 🚨: ABSOLUTELY FORBIDDEN to wrap visualizer section headers (like 'Mã nguồn thi hành', 'Màn hình Console') inside `<pre><code>` tags or fake macOS code cards (`bg-slate-800` / `bg-slate-900`)! 
      BAD: `<pre><code>Mã nguồn đang thực thi</code></pre>`
      BAD: `<div class="bg-slate-900 ...">Mã nguồn đang thực thi</div>`
      GOOD: `<div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Mã nguồn đang thực thi</div>`
    - ONLY use `<pre><code>` for actual editable code snippets in Section 3.
    - ABSOLUTELY FORBIDDEN to include line numbers (such as `1. `, `2. `, `Dòng 1:`) inside visualizer code lines. Keep code lines clean, accurately highlighted, and syntactically correct.

23. JSON ESCAPING CONTRACT FOR MULTI-LINE CODE:
    - When writing multi-line code inside JSON string values (like `example_code` or `knowledge_html`), you MUST use explicit `\\n` to preserve line breaks.
    - DO NOT compress multi-line code into a single line. Example BAD: `"for x in range(3):    print(x)"`. Example GOOD: `"for x in range(3):\\n    print(x)"`.

24. UNIFIED THREADED REAL-WORLD SCENARIO CONTRACT (XUYÊN SUỐT TOÀN BỘ BÀI HỌC):
    - BEFORE writing Section 1, you MUST select ONE SINGLE, REALISTIC ENTERPRISE SCENARIO appropriate for the lesson topic and tech stack (e.g. Student Grade & Passing Qualification System, E-commerce Order Shipping & Discount, Bank Credit Approval, User Authentication Role, Inventory Stock Alert).
    - This EXACT SAME scenario MUST thread continuously through ALL sections: Section 1 (Problem), Section 2 (Syntax & Progressive Sub-heading Sandboxes), Section 3 (Practical Examples), Section 4 (Gotchas), and Section 5 (Self-Test).
    - ABSOLUTELY FORBIDDEN to switch to unrelated random examples across sections.

25. CONCISE & PUNCHY SECTION 1 PROBLEM STATEMENT CONTRACT:
    - Section 1 MUST be short, punchy, direct, and easy to understand (max 2-3 brief paragraphs/bullets).
    - Follow pedagogical flow: Real-World Business Context ➔ Practical Pain Point ➔ Legacy Drawbacks ➔ Introduce New Solution Concept.
    - Accompanied by a 16:9 widescreen 2D flat vector context diagram representing the real-world scenario.
    - ABSOLUTELY FORBIDDEN to write long-winded, dry academic walls of text or preamble fluff.

26. PROGRESSIVE SYNTAX CODE DEMO SANDBOX UNDER EVERY SUBSECTION:
    - EVERY subsection in Section 2 (`2.1`, `2.2`, `2.3`...) MUST present its own concise Live Code Sandbox / Illustration block directly under the subsection.
    - The code demo snippet under each subsection MUST progressively expand on the unified real-world scenario chosen for the lesson:
      * For Conditional Statements: `2.1 if` (Pass check) ➔ `2.2 if-else` (Pass vs Retake) ➔ `2.3 if-elif-else` (Grade classification).
      * For For Loops: `2.1 range()` (Index loop) ➔ `2.2 list loop` (Iterate score list) ➔ `2.3 enumerate()` (Student name and score pairs).

27. PLAIN DEVELOPER LANGUAGE & ZERO ACADEMIC JARGON CONTRACT:
    - 100% FORBIDDEN to use dry academic formulas, unverified claims, or hyperbolic AI fluff ("khám phá", "vô cùng", "bậc nhất", "tuyệt vời").
    - Use clear, practical, learner-friendly language ("Giúp bạn kiểm tra...", "Xử lý khi...", "Tránh lỗi...").

28. DOMAIN-AGNOSTIC & ZERO HARDCODING CONTRACT:
    - All rules apply dynamically to whatever target `tech_stack` is passed in (`python`, `javascript`, `java`, `cpp`, `sql`, `html/css`, `git`, `docker`, `agile`, etc.).
    - ABSOLUTELY NO hardcoded course titles, fixed grade examples, or single-technology fallbacks in prompt instructions.

29. MANDATORY VALID CODE SYNTAX & INDENTATION CONTRACT:
    - ALL code snippets, examples, and sandboxes MUST satisfy 100% syntactically complete and valid code in the target technology language.
    - NEVER truncate or leave code statements incomplete (e.g. NEVER write incomplete statements like `if attendance_percentage`). Always include full conditions, colons, indented blocks, and print calls.
    - For Python: MUST enforce exact 4-space indentation for blocks inside `if`, `elif`, `else`, `def`, `for`, `while`, `try`, `except`. NEVER omit indentation inside nested statements! All indentation errors (`IndentationError`) and syntax errors (`SyntaxError`) are FATAL.

Return pure JSON data with fields (MUST NOT omit `section1_title` and `section2_title`):
{{
  "section1_title": "Dynamic Section 1 title matching lesson topic in Accented Vietnamese (e.g., 'Tại sao cần dùng hàm?')",
  "section2_title": "Dynamic Section 2 title detailing knowledge concept in Accented Vietnamese (e.g., 'Cú pháp và cơ chế hoạt động của hàm')",
  "problem_html": "<p class=\"text-slate-600 dark:text-slate-300 mb-4 leading-relaxed\">Section 1 HTML content in Accented Vietnamese...</p>",
  "diagram_svg": "<svg viewBox=\"0 0 800 250\" class=\"w-full h-auto rikkei-diagram\">...</svg>",
  "knowledge_html": "<h3 class=\"text-xl font-bold text-slate-900 dark:text-white mb-3\">2.1. Subheading title...</h3><p class=\"text-slate-600 dark:text-slate-300 mb-4 leading-relaxed\">Section 2 HTML content in Accented Vietnamese...</p>",
  "example_code": "Combined executable code snippet in target tech stack language",
  "example_html": "<h3 class=\"text-xl font-bold text-slate-900 dark:text-white mb-3\">3.1. Example 1 (Minimal syntax)...</h3><p class=\"text-slate-600 dark:text-slate-300 mb-4 leading-relaxed\">Explanation in Accented Vietnamese...</p><pre><code class=\"language-TECH\">Code snippet 1</code></pre>",
  "notes_html": "<div class=\"p-4 rounded-xl border border-rose-200 dark:border-rose-900/50 bg-rose-50/60 dark:bg-rose-950/30 my-4\"><h4 class=\"text-lg font-bold text-rose-900 dark:text-rose-200 mb-2 flex items-center gap-2\"><i class=\"ph-bold ph-warning-circle text-rose-600\"></i> 4.1. Common Gotchas & Pitfalls...</h4></div>",
  "references": [
    {{"title": "Official authoritative documentation title", "url": "https://..."}}
  ]
}}"""

    user_prompt = f"""Author detailed reading material content for:
Session: {session_id}
Lesson: {lesson_id} - {lesson_title}
Lesson Details: {lesson_details}
Expected Output: {expected_output}
Target Technology Stack: {tech_stack}

MANDATORY OUTPUT CONTRACT: Return ONLY raw pure JSON containing HTML content strictly adhering to the schema."""

    llm_resp = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Reading_Creator_SSOT",
        session_id=session_id,
        lesson_id=lesson_id
    )

    def robust_parse_llm_json(raw: str) -> dict:
        """3-tier robust JSON parser designed for LLM HTML-rich output.
        Tier 1: standard json.loads
        Tier 2: fix common escape issues (literal newlines inside strings) then parse
        Tier 3: character-level scanner to extract each field individually
        """
        # Pre-sanitize ASCII control characters
        raw_clean = sanitize_llm_json_text(raw)
        
        # Strip markdown code fences
        cleaned = raw_clean.strip()
        for prefix in ["```json\n", "```json", "```\n", "```"]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
                break
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        # Tier 1 - direct parse
        try:
            return json.loads(cleaned)
        except Exception:
            pass

        # Tier 2 - fix literal newlines/tabs inside JSON string values then retry
        try:
            fixed = re.sub(
                r'("(?:[^"\\]|\\.)*")',
                lambda m: m.group(0).replace('\n', '\\n').replace('\r', '').replace('\t', '\\t'),
                cleaned,
                flags=re.DOTALL
            )
            return json.loads(fixed)
        except Exception:
            pass

        # Tier 3 - character-level field scanner (handles unescaped quotes inside HTML)
        def scan_string_value(text: str, start: int):
            if start >= len(text) or text[start] != '"':
                return None, start
            i = start + 1
            buf = []
            while i < len(text):
                c = text[i]
                if c == '\\' and i + 1 < len(text):
                    nc = text[i + 1]
                    if nc == 'n': buf.append('\n')
                    elif nc == 't': buf.append('\t')
                    elif nc == '"': buf.append('"')
                    elif nc == '\\': buf.append('\\')
                    else: buf.append(nc)
                    i += 2
                elif c == '"':
                    return ''.join(buf), i + 1
                elif c == '\n':
                    buf.append('\n')
                    i += 1
                else:
                    buf.append(c)
                    i += 1
            return ''.join(buf), i

        result = {}
        str_fields = [
            'section1_title', 'section2_title', 'problem_html', 'diagram_svg',
            'knowledge_html', 'example_code', 'example_html', 'notes_html'
        ]
        for field in str_fields:
            search_key = f'"{field}"'
            idx = cleaned.find(search_key)
            if idx == -1:
                continue
            pos = idx + len(search_key)
            while pos < len(cleaned) and cleaned[pos] in ' \t\r\n': pos += 1
            if pos < len(cleaned) and cleaned[pos] == ':': pos += 1
            while pos < len(cleaned) and cleaned[pos] in ' \t\r\n': pos += 1
            if pos < len(cleaned) and cleaned[pos] == '"':
                val, _ = scan_string_value(cleaned, pos)
                if val is not None:
                    result[field] = val

        ref_match = re.search(r'"references"\s*:\s*(\[.*?\])', cleaned, re.DOTALL)
        if ref_match:
            try:
                result['references'] = json.loads(ref_match.group(1))
            except Exception:
                pass

        return result

    data = {}
    try:
        data = robust_parse_llm_json(llm_resp)
        if not data:
            raise ValueError("Empty parse result")
    except Exception as e:
        print(f"  [Reading Creator Warning] All JSON parse tiers failed: {e}. Using minimal fallback.")
        data = {}

    def ensure_html(val: str) -> str:
        if not val: return ""
        val_str = str(val).strip()
        if "<p" in val_str or "<ul" in val_str or "<div" in val_str or "<h3" in val_str or "<span" in val_str:
            return val_str
        return convert_markdown_to_html(val_str)

    # Dynamic section titles & slugified robust anchor IDs (Problem 2.2)
    section1_title = (data.get("section1_title") or f"Tại sao cần học {lesson_title}?").strip()
    section2_title = (data.get("section2_title") or f"Kiến thức và cú pháp cơ bản").strip()

    sec1_id = slugify_id(section1_title)
    sec2_id = slugify_id(section2_title)

    # Auto-inject IDs into <h3> subheadings in Section 2 and 3 for deep linking & strip stray '>' characters
    def inject_subheading_ids(html_content: str) -> str:
        if not html_content: return ""
        # Strip stray leading > or &gt; in h2/h3 tags
        html_content = re.sub(r'(<h[234]\b[^>]*>)\s*(?:&gt;|>)\s*', r'\1', html_content)
        def add_id(m):
            tag_open, h3_title = m.group(1), m.group(2)
            clean_title = re.sub(r'^(?:&gt;|>)\s*', '', h3_title).strip()
            if 'id=' in tag_open:
                return f'{tag_open}{clean_title}</h3>'
            sub_id = slugify_id(clean_title)
            return f'<h3 id="{sub_id}" class="font-montserrat font-bold text-xl text-slate-900 mb-3">{clean_title}</h3>'
        return re.sub(r'(<h3\b[^>]*>)(.*?)</h3>', add_id, html_content, flags=re.DOTALL)

    def clean_stray_chars(html_str: str) -> str:
        if not html_str: return ""
        # Strip all dark: Tailwind classes completely (e.g. dark:bg-slate-900, dark:text-slate-200, dark:bg-rikkei-bgDark)
        c = re.sub(r'\bdark:[a-zA-Z0-9_/-]+\b', '', html_str)
        # Strip light text classes inside normal text blocks meant for dark backgrounds
        c = re.sub(r'\b(text-slate-100|text-slate-200|text-slate-300|text-slate-400|text-white)\b', 'text-slate-700', c)

        # Fix duplicate class="..." attributes on HTML tags: e.g. <h4 class="a b" class="c d"> -> <h4 class="a b c d">
        def deduplicate_class_attributes(m):
            tag_name = m.group(1)
            full_tag = m.group(0)
            classes = re.findall(r'class=["\']([^"\']*)["\']', full_tag)
            merged = " ".join(classes).strip()
            # Remove all class attributes from full_tag except the first one
            tag_without_classes = re.sub(r'\s*class=["\'][^"\']*["\']', '', full_tag)
            tag_open = tag_without_classes[:-1].rstrip()
            return f'{tag_open} class="{merged}">'
        c = re.sub(r'<(h[1-6]|div|p|span|button|section)\b[^>]*\bclass=["\'][^"\']*["\'][^>]*\bclass=["\'][^"\']*["\'][^>]*>', deduplicate_class_attributes, c, flags=re.IGNORECASE)

        c = re.sub(r'(<h[1-6]\b[^>]*>)\s*(?:&gt;|>|\|)+\s*', r'\1', c)
        c = re.sub(r'(<p\b[^>]*>)\s*(?:&gt;|>|\|)+\s*', r'\1', c)
        c = re.sub(r'(<li\b[^>]*>)\s*(?:&gt;|>|\|)+\s*', r'\1', c)
        c = re.sub(r'(^|\n|>)\s*(?:&gt;|>|\|)+\s*(?=[A-Za-z0-90-9ĐđÀ-ỹ])', r'\1', c)
        c = re.sub(r'(</(?:p|div|section|li|h[1-6])>)\s*\|\s*', r'\1', c)

        # Strip lone pipe lines '|'
        c = re.sub(r'(^|\n)\s*\|\s*($|\n)', r'\1\2', c)

        # Strip raw inline <script> tags from LLM output to prevent HTML syntax errors / unclosed tag truncation
        c = re.sub(r'<script\b[^>]*>(?:(?!</script>).)*$', '', c, flags=re.DOTALL)
        c = re.sub(r'<script\b[^>]*>.*?</script>', '', c, flags=re.DOTALL)

        # Fix 2c: Normalize visualizer element IDs to match JS template selectors
        c = re.sub(r'id="mem-(?:total[_-]?sum|tong)"', 'id="viz-var-sum"', c)
        c = re.sub(r'id="mem-(?:number|bien[_-]?lap|counter|so)"', 'id="viz-var-number"', c)
        c = re.sub(r'id="viz-console-out(?:put)?"', 'id="viz-console"', c)

        # Enforce Light Mode console box: replace bg-slate-900 / bg-black on console with bg-slate-100 border border-slate-200 text-emerald-800
        c = re.sub(r'(id="viz-console"[^>]*class="[^"]*)\bbg-slate-900\b([^"]*")', r'\1bg-slate-100 border border-slate-200 text-emerald-800\2', c)
        c = re.sub(r'(id="viz-console"[^>]*class="[^"]*)\btext-emerald-400\b([^"]*")', r'\1text-emerald-800 font-semibold\2', c)
        c = re.sub(r'class="([^"]*)\bbg-slate-900\b([^"]*viz-console[^"]*)"', r'class="\1bg-slate-100 border border-slate-200 text-emerald-800\2"', c)

        # Enforce standard 4-button visualizer control panel layout using Phosphor Icons (No text emoji)
        def normalize_viz_button_panel(m):
            panel_content = m.group(0)
            if "Bắt đầu" not in panel_content or "Tạm dừng" not in panel_content:
                return '''<div class="flex items-center gap-2">
  <button type="button" onclick="runVizStep(1)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition-all flex items-center gap-1"><i class="ph-bold ph-play text-xs"></i> Bắt đầu</button>
  <button type="button" onclick="runVizStep(0)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-500 hover:bg-amber-600 text-white shadow-sm transition-all flex items-center gap-1"><i class="ph-bold ph-pause text-xs"></i> Tạm dừng</button>
  <button type="button" onclick="runVizStep(1)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#be111c] hover:bg-[#90000a] text-white shadow-sm transition-all flex items-center gap-1"><i class="ph-bold ph-step-forward text-xs"></i> Từng bước</button>
  <button type="button" onclick="runVizStep(-999)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-200 hover:bg-slate-300 text-slate-800 shadow-sm transition-all flex items-center gap-1"><i class="ph-bold ph-arrow-counter-clockwise text-xs"></i> Đặt lại</button>
</div>'''
            return panel_content
        c = re.sub(r'<div\s+class="flex\s+items-center\s+gap-2">\s*<button\b.*?</button>\s*</div>', normalize_viz_button_panel, c, flags=re.DOTALL | re.IGNORECASE)

        # Auto-attach onclick handlers to visualizer buttons if missing
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Lùi lại|Quay lại|Trở về)\s*</button>', r'\1 onclick="runVizStep(-1)">Lùi lại</button>', c, flags=re.IGNORECASE)
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Tiếp theo|Kế tiếp|Chạy tiếp)\s*</button>', r'\1 onclick="runVizStep(1)">Tiếp theo</button>', c, flags=re.IGNORECASE)
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Tự động chạy|Auto Play)\s*</button>', r'\1 onclick="runVizStep(1)">Tự động chạy</button>', c, flags=re.IGNORECASE)
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Thử lại|Đặt lại|Reset)\s*</button>', r'\1 onclick="runVizStep(-999)">Thử lại</button>', c, flags=re.IGNORECASE)

        # Fix text contrast on colored/dark buttons: replace text-slate-700 / text-slate-800 on dark backgrounds with text-white
        c = re.sub(r'class="([^"]*\b(?:bg-\[#[a-fA-F0-9]+\]|bg-emerald-\d+|bg-rose-\d+|bg-blue-\d+|bg-rikkei-\w+|bg-amber-\d+)\b[^"]*)\btext-slate-[678]00\b', r'class="\1text-white', c)

        # Auto-wrap raw <table> elements in <div class="overflow-x-auto my-4"> to satisfy visual_linter
        def wrap_unwrapped_table(m):
            tbl_str = m.group(0)
            if "overflow-x" in tbl_str or "overflow-x-auto" in tbl_str or "table-responsive" in tbl_str:
                return tbl_str
            return f'<div class="overflow-x-auto my-4 rounded-xl border border-slate-200 shadow-sm overflow-hidden">\n{tbl_str}\n</div>'
        c = re.sub(r'<table\b[^>]*>.*?</table>', wrap_unwrapped_table, c, flags=re.DOTALL | re.IGNORECASE)

        # Strip line numbers from visualizer code lines safely without breaking HTML tags
        c = re.sub(r'(id="[^"]*(?:mech-line|line-)[^"]*"[^>]*>)\s*(?:<span[^>]*>)?\s*(?:\d+\.|\b(?:Dòng|Line)\s*\d+[:.]?)\s*(?:</span>)?\s*', r'\1', c, flags=re.IGNORECASE)

        # Strip font-mono from h1-h6 headings and ensure font-montserrat font-bold
        def sanitize_heading_fonts(m):
            tag_name = m.group(1)
            attrs = m.group(2)
            clean_attrs = re.sub(r'\bfont-mono\b', 'font-montserrat', attrs)
            if 'font-montserrat' not in clean_attrs:
                if 'class="' in clean_attrs:
                    clean_attrs = clean_attrs.replace('class="', 'class="font-montserrat font-bold ')
                elif "class='" in clean_attrs:
                    clean_attrs = clean_attrs.replace("class='", "class='font-montserrat font-bold ")
                else:
                    clean_attrs = f'class="font-montserrat font-bold" {clean_attrs}'
            return f'<{tag_name} {clean_attrs}>'
        c = re.sub(r'<(h[1-6])\s+([^>]*)>', sanitize_heading_fonts, c)

        # Scrub hardcoded dark background classes from text elements
        def sanitize_tag_classes(m):
            tag_name = m.group(1)
            attrs = m.group(2)
            clean_attrs = re.sub(r'\b(bg-slate-900|bg-black|bg-slate-800|bg-slate-950|text-white|rounded-full)\b', '', attrs)
            clean_attrs = re.sub(r'\s+', ' ', clean_attrs).strip()
            return f'<{tag_name} {clean_attrs}>'
            
        c = re.sub(r'<(h[1-6]|p|li|span)\s+([^>]*class="[^"]*"[^>]*)>', sanitize_tag_classes, c)

        # Scrub hardcoded dark background classes from generic div elements in Light Mode
        c = re.sub(
            r'<div\s+class="([^"]*)\b(bg-slate-900|bg-black|bg-slate-800)\b([^"]*)"',
            r'<div class="\1bg-slate-50/50 dark:bg-slate-900/60\3"',
            c 
        )

        # Strip empty code blocks, pre tags, and black containers
        c = re.sub(r'<pre\b[^>]*>\s*(?:<code\b[^>]*>\s*</code>)?\s*</pre>', '', c)
        c = re.sub(r'<div\s+class="[^"]*\b(?:bg-slate-900|bg-black)\b[^"]*">\s*</div>', '', c)

        # Unwrap code blocks that were mistakenly nested inside callout boxes
        c = re.sub(
            r'<div\s+class="[^"]*p-4[^"]*rounded-xl[^"]*"[^>]*>\s*(?:<h[1-6][^>]*>.*?</h[1-6]>\s*)?(<pre\b[^>]*>.*?</pre>)\s*</div>',
            r'\1',
            c,
            flags=re.DOTALL
        )

        return c


    # Apply Diagram & Syntax Guards (Problem 1 Requirement 1.3)
    prob_html = clean_stray_chars(guard_mermaid_syntax(ensure_html(data.get("problem_html") or data.get("problem_text", ""))))
    diagram_svg = guard_svg_syntax(data.get("diagram_svg", ""))
    
    # Prevent duplicate SVG diagrams if LLM put SVG in both prob_html and diagram_svg
    if diagram_svg and ("<svg" in prob_html or "diagram-wrap" in prob_html or "rikkei-diagram" in prob_html):
        diagram_svg = ""

    know_html = clean_stray_chars(inject_subheading_ids(guard_mermaid_syntax(ensure_html(data.get("knowledge_html") or data.get("knowledge_text", "")))))
    ex_text = clean_stray_chars(inject_subheading_ids(guard_mermaid_syntax(ensure_html(data.get("example_html") or data.get("example_text", "")))))
    notes_html = clean_stray_chars(ensure_html(data.get("notes_html") or data.get("notes_text", "")))

    # Resolve Language Info from Tech Stack (Problem 1 Requirement 1.2)
    lang_info = resolve_language_info(tech_stack)

    # Auto-convert code blocks: Live Pyodide Sandbox for Python (Section 3), Static VS Code-styled code card for syntax/gotchas (Section 2 & 4)
    def convert_code_to_live_sandbox(html_text: str, lang_meta: Dict[str, str], force_static: bool = False, sb_prefix: str = "sb") -> str:
        if not html_text: return ""
        import re, html as html_lib
        counter = 0
        is_python = (lang_meta.get("engine") == "pyodide") and not force_static
        hljs_class = lang_meta.get("hljs", "language-python")
        lang_name = lang_meta.get("name", "Code")

        def create_sandbox(code_str: str) -> str:
            nonlocal counter
            counter += 1
            sb_id = f"{sb_prefix}-{counter}"
            code_clean = re.sub(r'<[^>]+>', '', code_str)
            raw_code = html_lib.unescape(code_clean.strip())
            
            # Fix 2b: Skip wrapping if it is a visualizer static label/text placeholder
            # Return as styled <div> label instead of invalid <pre><code> nesting
            if any(kw in raw_code for kw in ["Mã nguồn thi hành", "Mã nguồn đang thực thi", "Màn hình Console", "Màn hình in kết quả", "Chương trình sẵn sàng", "Lần lặp"]):
                return f'<div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">{raw_code}</div>'
                
            # Fix 1b: Restore newlines in compressed Python code (LLM JSON loses \n)
            raw_code = re.sub(r'(:)[ \t]{4,}(\S)', r':\n    \2', raw_code)
            raw_code = re.sub(r'(#[^\n]*?)[ \t]{4,}(\S)', r'\1\n\2', raw_code)

            escaped_code = html_lib.escape(raw_code)
            attr_code = escaped_code.replace('\n', '&#10;').replace('\r', '')

            # Detect CLI / Terminal / Non-Python snippet inside Python code block
            is_cli_cmd = any(raw_code.strip().startswith(prefix) for prefix in [
                "git ", "$ git", "$git", "docker ", "npm ", "npx ", "pip ", "cd ", "mkdir ", "curl ", "wget ", "sudo ", "chmod ", "apt ", "yum ", "systemctl ", "python -m "
            ]) or any(cmd in raw_code.lower() for cmd in ["git commit", "git push", "git pull", "git checkout", "git branch", "git status", "git add", "git init", "git clone"])

            # Detect abstract syntax template vs executable code snippet
            is_abstract_syntax = force_static or any(kw in raw_code for kw in [
                "statement_block", "if_statement_block", "else_statement_block", "default_statement_block",
                "condition_1", "condition_2", "condition_3", "if condition:"
            ])

            if is_python and not is_cli_cmd and not is_abstract_syntax:
                return f'''<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="runPythonCode('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
        <i class="ph-bold ph-play text-xs"></i>
      </button>
      <button onclick="copySandboxCode('code-sb-{sb_id}', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép">
        <i class="ph-bold ph-copy text-xs"></i>
      </button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-{sb_id}" class="{hljs_class}" contenteditable="true" spellcheck="false" data-original="{attr_code}" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">{escaped_code}</code></pre>
  </div>
  <div id="container-sb-{sb_id}" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5">
        <i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):
      </span>
    </div>
    <pre id="output-sb-{sb_id}" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>'''
            else:
                block_label = f"Cú pháp mẫu {lang_name.capitalize()}" if force_static else f"Mã nguồn minh họa {lang_name.capitalize()}"
                return f'''<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">{block_label}</span>
    </span>
    <button onclick="navigator.clipboard.writeText(this.closest('.my-5').querySelector('code').innerText)" class="hover:text-rikkei-red px-2.5 py-1 rounded-md bg-white border border-slate-200 text-slate-600 text-xs transition-all flex items-center gap-1 shadow-sm" title="Sao chép mã nguồn"><i class="ph-bold ph-copy text-xs"></i> Sao chép</button>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs {hljs_class}">{escaped_code}</code></pre>
</div>'''

        # ── PRE-PROCESS: Strip any outer div wrappers around raw <pre> blocks (before card generation) ──
        # Only strip when the outer div is a simple 1-2 layer wrapper with NO macOS card signature (no px-3.5 header bar)
        def strip_pre_wrappers(text: str) -> str:
            """Iteratively strip outer div wrappers from raw <pre> blocks until stable."""
            prev = None
            max_passes = 6
            passes = 0
            while text != prev and passes < max_passes:
                prev = text
                passes += 1
                # Pattern A: <div class="...(no px-3.5)..."><div class="..."?><pre>...</pre></div?></div>
                text = re.sub(
                    r'<div\s+class="(?![^"]*px-3\.5)[^"]*(?:rounded|border|bg-|shadow|overflow|p-\d|font-mono)[^"]*"[^>]*>\s*'
                    r'(?:<div\s+class="(?![^"]*px-3\.5)[^"]*(?:bg-|flex|border|px-|py-|text-)[^"]*"[^>]*>(?:(?!</div>).){0,200}</div>\s*)?'
                    r'(<pre\b[^>]*>(?:(?!</pre>).)*?</pre>)\s*'
                    r'</div>',
                    r'\1',
                    text,
                    flags=re.DOTALL
                )
            return text

        # ── PRE-PROCESS: Convert fake LLM HTML cards to <pre><code> ──
        # LLMs often hallucinate their own code cards (using bg-rose-500 etc) instead of <pre><code>
        def convert_fake_llm_cards_to_pre(text: str) -> str:
            pattern = re.compile(
                r'<div\s+class="[^"]*rounded-xl[^"]*border[^"]*bg-slate-50[^"]*">\s*'
                r'<div\s+class="px-4\s+py-2\s+bg-slate-100[^"]*">.*?<span\s+class="[^"]*bg-[a-z]+-\d{3}".*?</div>\s*'
                r'<div\s+class="[^"]*font-mono[^"]*">(.*?)</div>\s*</div>',
                re.DOTALL | re.IGNORECASE
            )
            def replacer(m):
                code_html = m.group(1)
                code_text = code_html.replace('<br>', '\n').replace('&nbsp;', ' ')
                import html as html_lib
                code_text = html_lib.unescape(code_text)
                return f'<pre><code class="{hljs_class}">{html_lib.escape(code_text)}</code></pre>'
            return pattern.sub(replacer, text)

        html_text = convert_fake_llm_cards_to_pre(html_text)
        html_text = strip_pre_wrappers(html_text)

        # (Removed dangerous font-mono wrapping fallback that corrupted visualizer layouts)
        # ── GENERATE: Convert each raw <pre>...</pre> block into a styled card ──
        pattern_pre = re.compile(r'<pre\b[^>]*>(.*?)</pre>', re.DOTALL)
        result = pattern_pre.sub(lambda m: create_sandbox(m.group(1)), html_text)

        # ── POST-PROCESS: Strip outer div wrappers that LLM added AROUND our generated code cards ──
        # This uses a balanced-div scanner to find the exact outer wrapper boundary
        def strip_card_wrappers(text: str) -> str:
            """Remove outer div wrappers wrapping our generated static or sandbox code cards."""
            # Card signature markers for our generated code cards
            STATIC_SIG = 'class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm"'
            SANDBOX_SIG = 'class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50"'

            for sig in [STATIC_SIG, SANDBOX_SIG]:
                out = []
                i = 0
                while i < len(text):
                    # Find the next occurrence of a card signature
                    card_pos = text.find(f'<div {sig}', i)
                    if card_pos == -1:
                        out.append(text[i:])
                        break

                    # Check if there is an outer <div ...> opening before card_pos with no meaningful content between
                    before_chunk = text[i:card_pos]
                    outer_match = re.search(
                        r'<div\s+class="(?![^"]*px-3\.5)[^"]*(?:rounded|border|bg-|shadow)[^"]*"[^>]*>\s*$',
                        before_chunk
                    )
                    if outer_match:
                        # Emit everything before the outer div opening
                        out.append(before_chunk[:outer_match.start()])
                        # Find the end of the generated card using balanced div counting
                        search_start = card_pos
                        depth = 0
                        j = search_start
                        card_end = -1
                        while j < len(text):
                            open_pos = text.find('<div', j)
                            close_pos = text.find('</div>', j)
                            if open_pos == -1 and close_pos == -1:
                                break
                            if open_pos != -1 and (close_pos == -1 or open_pos < close_pos):
                                depth += 1
                                j = open_pos + 4
                            else:
                                depth -= 1
                                j = close_pos + 6
                                if depth == 0:
                                    card_end = j
                                    break
                        if card_end == -1:
                            # Cannot parse safely — emit as-is
                            out.append(before_chunk)
                            out.append(text[card_pos:card_pos + len(f'<div {sig}')])
                            i = card_pos + len(f'<div {sig}')
                            continue
                        # Emit the card content (without outer wrapper)
                        out.append(text[card_pos:card_end])
                        # Skip the trailing </div> of the outer wrapper if present
                        after = text[card_end:]
                        after_stripped = after.lstrip()
                        if after_stripped.startswith('</div>'):
                            i = card_end + (len(after) - len(after_stripped)) + 6
                        else:
                            i = card_end
                    else:
                        out.append(before_chunk)
                        out.append(text[card_pos:card_pos + len(f'<div {sig}')])
                        i = card_pos + len(f'<div {sig}')
                text = ''.join(out)
            return text

        result = strip_card_wrappers(result)

        # Fix 1a: Strip LLM-generated outer card containers with square dots
        # LLM cards use <span class="w-3 h-3 bg-rose-400"> (no rounded-full) as dot indicators
        # Our standard cards use <span class="w-3 h-3 rounded-full bg-[#ff5f56]"> (with rounded-full)
        def strip_llm_card_wrappers(text: str) -> str:
            """Remove outer card wrapper generated by LLM that nests our standard code cards."""
            # Iteratively strip until stable
            prev = None
            max_passes = 6
            passes = 0
            while text != prev and passes < max_passes:
                prev = text
                passes += 1
                # Detect LLM outer card: <div class="...rounded-xl...border...overflow-hidden...">
                #   followed by <div class="bg-slate-100 px-4 py-2..."> header with square dots
                #   followed by our standard card <div class="my-5 rounded-xl...">
                # then closing </div> of outer wrapper
                text = re.sub(
                    r'<div\s+class="[^"]*(?:my-4|my-6)[^"]*rounded-xl[^"]*border[^"]*(?:overflow-hidden|shadow)[^"]*"[^>]*>\s*'
                    r'<div\s+class="[^"]*bg-slate-100[^"]*px-4[^"]*py-2[^"]*border-b[^"]*"[^>]*>'
                    r'(?:(?!</div>).)*?'
                    r'</div>\s*'
                    r'(<div\s+class="my-5\s+rounded-xl[^"]*overflow-hidden[^"]*border[^"]*"[^>]*>'
                    r'(?:(?!</div>\s*</div>).)*?'
                    r'</div>)\s*'
                    r'</div>',
                    r'\1',
                    text,
                    flags=re.DOTALL
                )
            return text

        result = strip_llm_card_wrappers(result)
        return result

    know_html = convert_code_to_live_sandbox(know_html, lang_info, force_static=False, sb_prefix="sec2")
    ex_text = convert_code_to_live_sandbox(ex_text, lang_info, force_static=False, sb_prefix="sec3")
    notes_html = convert_code_to_live_sandbox(notes_html, lang_info, force_static=True, sb_prefix="sec4")

    # Problem 2.4: Strip LLM hallucinated line numbers inside mechanism visualizer code block
    know_html = re.sub(r'(<div[^>]*id="line-\d+"[^>]*>)\s*\d+\.\s*', r'\1', know_html)

    # Problem 3.3: Sanitize References and inject canonical docs if missing
    refs_items = sanitize_references(data.get("references", []), tech_stack)
    refs_html = ""
    for ref in refs_items:
        r_title = html.escape(ref.get("title", ""))
        r_url = ref.get("url", "#")
        refs_html += f"""
        <li>
          <a href="{r_url}" target="_blank" rel="noopener noreferrer" class="text-rikkei-red hover:underline inline-flex items-center gap-2 font-medium">
            <i class="ph-bold ph-link text-sm"></i> {r_title}
          </a>
        </li>
        """

    core_ssot = state.get("core_ssot", {}) if isinstance(state, dict) else {}
    session_title_display = state.get("session_title") or core_ssot.get("session_title") or session_id
    clean_h1_title = re.sub(r'^(?:Session\s+\d+\s*[-:]\s*)?(?:Lesson|Bài)\s+\d+\s*[-:]\s*', '', lesson_title, flags=re.IGNORECASE).strip()

    full_html = f"""<!DOCTYPE html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{lesson_title} - Rikkei Education</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />

    <!-- Phosphor Icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {{
        theme: {{
          extend: {{
            colors: {{
              rikkei: {{
                red: "#be111c",
                darkred: "#90000a",
                dark: "#0f172a",
              }},
            }},
            fontFamily: {{
              sans: ["Inter", "system-ui", "sans-serif"],
              montserrat: ["Montserrat", "sans-serif"],
              mono: ["JetBrains Mono", "monospace"],
            }},
            maxWidth: {{
              340: "1360px",
            }},
          }},
        }},
      }};
    </script>

    <!-- Highlight.js for Syntax Highlighting (Light theme only) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/java.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/cpp.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/sql.min.js"></script>

    <!-- Pyodide Engine for Live Wasm Python Sandbox -->
    <script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>


    <style>

      html {{
        scroll-behavior: smooth;
        scroll-padding-top: 84px; /* Problem 2.2: Fixed Header clearance */
      }}

      /* 1. SVG DIAGRAM - Prevent text overflow, ensure responsive */
      .rikkei-diagram, svg.rikkei-diagram {{
        max-width: 100%;
        height: auto;
        display: block;
        overflow: hidden;
      }}
      .rikkei-diagram text, svg.rikkei-diagram text {{
        font-family: "Inter", system-ui, sans-serif;
        overflow: hidden;
      }}
      .diagram-wrap {{
        width: 100%;
        max-width: 100%;
        overflow: hidden;
        border-radius: 0.75rem;
      }}
      div.my-6 svg, section svg, article svg {{
        max-width: 100%;
        height: auto;
        overflow: hidden;
      }}

      /* 2. TABLE - Prevent table overflow on all screens */
      table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        word-wrap: break-word;
        overflow-wrap: break-word;
      }}
      th, td {{
        word-break: break-word;
        overflow-wrap: break-word;
        hyphens: auto;
      }}

      /* 3. LIGHT MODE STYLING & HIGH CONTRAST TEXT RULES */
      h1, h2, h3, h4, h5, h6 {{
        color: #0f172a !important;
      }}
      p, li, td, th {{
        color: #334155 !important;
      }}
      .toc-link, .mobile-toc-link {{
        color: #475569 !important;
      }}
      .toc-link:hover, .mobile-toc-link:hover {{
        color: #0f172a !important;
      }}
      .bg-amber-50 *, .bg-rose-50 *, .bg-emerald-50 *, .bg-sky-50 * {{
        color: #1e293b !important;
      }}

      /* VISUALIZER HIGH CONTRAST LIGHT MODE & SYNTAX TOKEN SAFETY NET */
      [id*="mech"] p, [id*="mech"] div, [id*="visualizer"] div {{
        color: #1e293b;
      }}
      [id*="mech-line"]:not(.active-line), [id*="line-"]:not(.active-line) {{
        color: #475569 !important;
        opacity: 1 !important;
        font-weight: 500 !important;
      }}
      .kw {{ color: #cf222e !important; font-weight: bold !important; }}
      .str {{ color: #0a3069 !important; }}
      .num {{ color: #0550ae !important; font-weight: 600 !important; }}
      .fn {{ color: #8250df !important; font-weight: 600 !important; }}
      .cmt {{ color: #6e7781 !important; font-style: italic !important; }}

      code:not(.hljs):not([class*="language"]) {{
        background-color: #f1f5f9 !important;
        color: #be111c !important;
        padding: 0.125rem 0.375rem !important;
        border-radius: 0.25rem !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 0.875rem !important;
      }}

      /* 4. CODE SANDBOX & HLJS SYNTAX HIGHLIGHTING */
      .sandbox-editor {{
        min-height: 6rem;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.875rem;
        line-height: 1.6;
        background-color: #f8fafc;
        color: #0f172a;
      }}

      pre code.hljs {{
        padding: 1.25rem !important;
        border-radius: 0.75rem !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 0.875rem !important;
        line-height: 1.6 !important;
        background: #f8fafc !important;
      }}

      pre span, code span {{
        background-color: transparent !important;
      }}


      pre {{
        white-space: pre-wrap;
        word-break: break-all;
        overflow-wrap: break-word;
      }}


      /* 9. STRAY CHARACTER PREVENTION */
      body > *:not(header):not(main):not(script):not(style):not(#mobile-toc-toggle):not(#mobile-toc-drawer) {{
        display: none !important;
      }}
    </style>
  </head>
  <body class="bg-slate-50 dark:bg-rikkei-bgDark text-base text-slate-800 dark:text-slate-200 font-sans leading-relaxed transition-colors duration-300 min-h-screen">
    <!-- Fixed Header -->
    <header class="fixed top-0 left-0 right-0 h-16 bg-white/95 backdrop-blur-md border-b border-slate-200 z-40">
      <div class="max-w-340 mx-auto h-full px-6 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Rikkei Academy Logo" class="h-9 object-contain" />
          <span class="text-sm font-semibold text-slate-500 border-l border-slate-300 pl-4">{session_title_display}</span>
        </div>
      </div>
      <div class="w-full h-1 bg-slate-100">
        <div id="scroll-progress" class="h-full w-0 bg-rikkei-red transition-all duration-75"></div>
      </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-340 mx-auto px-6 pt-24 pb-16 flex gap-8">
      <!-- Sidebar Table of Contents (Left Desktop) -->
      <aside class="w-72 shrink-0 hidden lg:block sticky top-24 h-[calc(100vh-120px)] overflow-y-auto pr-2">
        <div class="space-y-4">
          <h4 class="font-montserrat font-bold text-sm text-slate-700">Mục lục chi tiết</h4>
          <nav class="flex flex-col border-l border-slate-200 space-y-1">
            <a href="#section-1" class="toc-link pl-4 py-2 border-l-2 border-transparent text-[15px] text-slate-600 hover:text-slate-900 font-medium transition-all">1. {section1_title}</a>
            <a href="#section-2" class="toc-link pl-4 py-2 border-l-2 border-transparent text-[15px] text-slate-600 hover:text-slate-900 font-medium transition-all">2. {section2_title}</a>
            <a href="#section-3" class="toc-link pl-4 py-2 border-l-2 border-transparent text-[15px] text-slate-600 hover:text-slate-900 font-medium transition-all">3. Các ví dụ ứng dụng thực tiễn</a>
            <a href="#section-4" class="toc-link pl-4 py-2 border-l-2 border-transparent text-[15px] text-slate-600 hover:text-slate-900 font-medium transition-all">4. Tổng kết và các lưu ý</a>
            <a href="#section-5" class="toc-link pl-4 py-2 border-l-2 border-transparent text-[15px] text-slate-600 hover:text-slate-900 font-medium transition-all">5. Tài liệu tham khảo</a>
          </nav>
        </div>
      </aside>

      <!-- Problem 2.3: Mobile Floating TOC Button (lg:hidden) -->
      <button id="mobile-toc-toggle" onclick="toggleMobileToc()" class="lg:hidden fixed bottom-6 right-6 z-50 bg-rikkei-red text-white p-3.5 rounded-full shadow-xl hover:scale-105 transition-all flex items-center justify-center border border-white/20" title="Mở mục lục bài đọc">
        <i class="ph-bold ph-list text-xl"></i>
      </button>

      <!-- Problem 2.3: Mobile TOC Slide-over Modal Drawer -->
      <div id="mobile-toc-drawer" class="lg:hidden fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm hidden transition-all duration-300">
        <div class="fixed inset-y-0 right-0 w-80 max-w-[85vw] bg-white p-6 shadow-2xl overflow-y-auto flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-200">
              <h4 class="font-montserrat font-bold text-base text-slate-900 flex items-center gap-2"><i class="ph-bold ph-list-bullets text-rikkei-red"></i> MỤC LỤC BÀI ĐỌC</h4>
              <button onclick="toggleMobileToc()" class="p-1 rounded text-slate-400 hover:text-slate-600"><i class="ph-bold ph-x text-lg"></i></button>
            </div>
            <nav class="flex flex-col space-y-2">
              <a href="#section-1" onclick="toggleMobileToc()" class="mobile-toc-link p-2.5 rounded-lg text-sm text-slate-600 hover:bg-slate-100 font-medium">1. {section1_title}</a>
              <a href="#section-2" onclick="toggleMobileToc()" class="mobile-toc-link p-2.5 rounded-lg text-sm text-slate-600 hover:bg-slate-100 font-medium">2. {section2_title}</a>
              <a href="#section-3" onclick="toggleMobileToc()" class="mobile-toc-link p-2.5 rounded-lg text-sm text-slate-600 hover:bg-slate-100 font-medium">3. Các ví dụ ứng dụng thực tiễn</a>
              <a href="#section-4" onclick="toggleMobileToc()" class="mobile-toc-link p-2.5 rounded-lg text-sm text-slate-600 hover:bg-slate-100 font-medium">4. Tổng kết và các lưu ý</a>
              <a href="#section-5" onclick="toggleMobileToc()" class="mobile-toc-link p-2.5 rounded-lg text-sm text-slate-600 hover:bg-slate-100 font-medium">5. Tài liệu tham khảo</a>
            </nav>
          </div>
          <div class="pt-4 border-t border-slate-200 text-xs text-slate-400 text-center">Rikkei Education - Learning Material</div>
        </div>
      </div>

      <!-- Reading Content (Right/Center) -->
      <article class="flex-1 min-w-0 bg-white border border-slate-200 rounded-2xl p-6 sm:p-10 shadow-sm">
        <!-- Article Title -->
        <div class="border-b border-slate-200 pb-6 mb-8">
          <h1 class="font-montserrat font-bold text-3xl text-slate-900 leading-tight">{clean_h1_title}</h1>
        </div>

        <!-- Section 1: Đặt vấn đề -->
        <section id="section-1" class="mb-10 scroll-mt-24">
          <h2 class="font-montserrat font-bold text-2xl text-slate-900 mb-4">1. {section1_title}</h2>
          <div class="space-y-4">{prob_html}</div>
          <div class="my-6">{diagram_svg}</div>
        </section>

        <!-- Section 2: Giới thiệu kiến thức -->
        <section id="section-2" class="mb-10 scroll-mt-24">
          <h2 class="font-montserrat font-bold text-2xl text-slate-900 mb-4">2. {section2_title}</h2>
          <div class="space-y-4">{know_html}</div>
        </section>

        <!-- Section 3: Các ví dụ ứng dụng thực tiễn -->
        <section id="section-3" class="mb-10 scroll-mt-24">
          <h2 class="font-montserrat font-bold text-2xl text-slate-900 mb-4">3. Các ví dụ ứng dụng thực tiễn</h2>
          <div class="space-y-6">{ex_text}</div>
        </section>

        <!-- Section 4: Tổng kết và các lưu ý -->
        <section id="section-4" class="mb-10 scroll-mt-24">
          <h2 class="font-montserrat font-bold text-2xl text-slate-900 mb-4">4. Tổng kết và các lưu ý</h2>
          <div class="space-y-4">
            {notes_html}
          </div>
        </section>

        <!-- Section 5: Tài liệu tham khảo -->
        <section id="section-5" class="mb-6 scroll-mt-24">
          <h2 class="font-montserrat font-bold text-2xl text-slate-900 mb-4">5. Tài liệu tham khảo</h2>
          <div class="pt-2">
            <ul class="space-y-2 list-none pl-0">{refs_html}</ul>
          </div>
        </section>
      </article>
    </main>

    <script>
      function toggleMobileToc() {{
        const drawer = document.getElementById("mobile-toc-drawer");
        if (drawer) drawer.classList.toggle("hidden");
      }}

      // (HLJS initialization moved to second DOMContentLoaded handler below)

      // Theme toggle script — also swaps hljs stylesheet for proper syntax colors in both modes
      const themeToggleBtn = document.getElementById("theme-toggle");
      const themeIcon = document.getElementById("theme-icon");
      const hljsLightTheme = document.getElementById("hljs-light-theme");
      const hljsDarkTheme  = document.getElementById("hljs-dark-theme");

      function applyHljsTheme(isDark) {{
        if (hljsLightTheme) hljsLightTheme.disabled = isDark;
        if (hljsDarkTheme)  hljsDarkTheme.disabled  = !isDark;
        // Re-highlight all code blocks so new theme tokens take effect immediately
        if (window.hljs) {{
          document.querySelectorAll('pre code').forEach((block) => {{
            block.removeAttribute('data-highlighted');
            hljs.highlightElement(block);
          }});
        }}
      }}

      themeToggleBtn?.addEventListener("click", () => {{
        document.documentElement.classList.toggle("dark");
        const isDark = document.documentElement.classList.contains("dark");
        themeIcon.className = isDark ? "ph-bold ph-sun text-lg text-amber-400" : "ph-bold ph-moon text-lg text-slate-600";
        applyHljsTheme(isDark);
      }});

      // Scroll progress script
      window.addEventListener("scroll", () => {{
        const winScroll = document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        const progress = document.getElementById("scroll-progress");
        if (progress) progress.style.width = scrolled + "%";
      }});

      // Table of Contents Active Scroll Observer
      document.addEventListener("DOMContentLoaded", () => {{
        const observerOptions = {{
          root: null,
          rootMargin: "-20% 0px -60% 0px",
          threshold: 0
        }};

        const tocLinks = document.querySelectorAll(".toc-link, .mobile-toc-link");
        const sections = document.querySelectorAll("article section[id]");

        const observer = new IntersectionObserver((entries) => {{
          entries.forEach((entry) => {{
            if (entry.isIntersecting) {{
              const id = entry.target.getAttribute("id");
              tocLinks.forEach((link) => {{
                const href = link.getAttribute("href");
                if (href === `#${{id}}`) {{
                  link.classList.add("!border-rikkei-red", "!text-rikkei-red", "font-semibold");
                  link.classList.remove("border-transparent", "text-slate-600");
                }} else {{
                  link.classList.remove("!border-rikkei-red", "!text-rikkei-red", "font-semibold");
                  link.classList.add("border-transparent", "text-slate-600");
                }}
              }});
            }}
          }});
        }}, observerOptions);

        sections.forEach((section) => observer.observe(section));

        // Syntax highlighting: highlight all code blocks (static + sandbox editors)
        if (window.hljs) {{
          document.querySelectorAll('pre code').forEach((block) => {{
            block.removeAttribute('data-highlighted');
            hljs.highlightElement(block);
          }});
        }}
      }});

      // Pyodide Live Wasm Sandbox Engine (Style 1 Editor)
      let pyodideInstance = null;
      async function getPyodide() {{
        if (!pyodideInstance && window.loadPyodide) {{
          pyodideInstance = await window.loadPyodide();
        }}
        return pyodideInstance;
      }}

      async function runPythonCode(editorId, outputId, containerId) {{
        const editor = document.getElementById(editorId);
        const output = document.getElementById(outputId);
        const container = document.getElementById(containerId);
        if (!editor || !output) return;

        if (container) container.classList.remove("hidden");
        const code = editor.innerText || editor.textContent;
        output.innerText = "Đang khởi tạo trình thông dịch Pyodide Wasm...";

        try {{
          const pyodide = await getPyodide();
          if (!pyodide) {{
            output.innerText = "Không thể kết nối Pyodide Wasm Sandbox.";
            return;
          }}
          let outputBuffer = "";
          pyodide.setStdout({{ batched: (str) => {{ outputBuffer += str + "\\n"; }} }});
          pyodide.setStderr({{ batched: (str) => {{ outputBuffer += "ERROR: " + str + "\\n"; }} }});

          // Problem 3.2: Reset Pyodide global scope to prevent variable state leakage across sandboxes
          try {{
            await pyodide.runPythonAsync("import sys; [sys.modules['__main__'].__dict__.pop(k) for k in list(sys.modules['__main__'].__dict__.keys()) if not k.startswith('__') and k not in ('sys', 'pyodide')]");
          }} catch(e) {{}}

          await pyodide.runPythonAsync(code);
          output.innerText = outputBuffer.trim ? outputBuffer.trim() : (outputBuffer || "Thực thi thành công (Không có kết quả xuất console).");
        }} catch (err) {{
          output.innerText = "LỖI THỰC THI:\\n" + err;
        }}
      }}

      function clearSandbox(editorId, outputId, containerId) {{
        const editor = document.getElementById(editorId);
        const output = document.getElementById(outputId);
        const container = document.getElementById(containerId);
        if (editor) {{
          const orig = editor._originalText || editor.getAttribute("data-original");
          if (orig) {{
            editor.textContent = orig;
            editor.removeAttribute('data-highlighted');
            if (window.hljs) hljs.highlightElement(editor);
          }}
        }}
        if (output) output.innerText = "";
        if (container) container.classList.add("hidden");
      }}
      document.addEventListener("DOMContentLoaded", () => {{
        document.querySelectorAll('code[data-original]').forEach(codeEl => {{
          if (!codeEl._originalText) {{
            codeEl._originalText = codeEl.textContent;
          }}
        }});
      }});


      function copySandboxCode(editorId, btn) {{
        const editor = document.getElementById(editorId);
        if (!editor) return;
        const text = editor.innerText || editor.textContent;
        navigator.clipboard.writeText(text).then(() => {{
          const origContent = btn.innerHTML;
          btn.innerHTML = '<i class="ph-bold ph-check text-emerald-500 text-sm"></i>';
          setTimeout(() => {{ btn.innerHTML = origContent; }}, 2000);
        }}).catch(err => {{
          console.error("Lỗi copy code:", err);
        }});
      }}

      // Global Dynamic Visualizer Runner Helpers
      window.vizStepMap = {{}};
      function runVizStep(delta, idPrefix) {{
        idPrefix = idPrefix || "viz";
        if (delta === -999) {{
          window.vizStepMap[idPrefix] = 0;
        }} else {{
          window.vizStepMap[idPrefix] = (window.vizStepMap[idPrefix] || 0) + delta;
        }}
        if (window.vizStepMap[idPrefix] < 0) window.vizStepMap[idPrefix] = 0;
        var step = window.vizStepMap[idPrefix];
        
        var numEl = document.getElementById(idPrefix + "-var-number") || document.getElementById("viz-var-number");
        var sumEl = document.getElementById(idPrefix + "-var-sum") || document.getElementById("viz-var-sum");
        var amtEl = document.getElementById(idPrefix + "-var-amount") || document.getElementById("viz-var-amount");
        var rateEl = document.getElementById(idPrefix + "-var-rate") || document.getElementById("viz-var-rate");
        var consoleEl = document.getElementById(idPrefix + "-console") || document.getElementById("viz-console");
        
        if (amtEl || rateEl) {{
          if (step === 0) {{
            if (amtEl) amtEl.innerText = "650000";
            if (rateEl) rateEl.innerText = "0.0";
            if (consoleEl) consoleEl.innerText = "Chờ thực thi cấu trúc rẽ nhánh...";
          }} else if (step === 1) {{
            if (amtEl) amtEl.innerText = "650000";
            if (rateEl) rateEl.innerText = "0.0";
            if (consoleEl) consoleEl.innerText = "Bước 1: if order_amount >= 1000000 -> False";
          }} else if (step === 2) {{
            if (amtEl) amtEl.innerText = "650000";
            if (rateEl) rateEl.innerText = "0.10";
            if (consoleEl) consoleEl.innerText = "Bước 2: elif order_amount >= 500000 -> True! Áp dụng chiết khấu 10.0%";
          }} else {{
            if (amtEl) amtEl.innerText = "650000";
            if (rateEl) rateEl.innerText = "0.10";
            if (consoleEl) consoleEl.innerText = "Applied discount rate: 10.0%\\nBỏ qua các nhánh còn lại. Đã hoàn thành rẽ nhánh.";
          }}
          return;
        }}

        if (consoleEl) {{
          if (step === 0) {{
            if (numEl) numEl.innerText = "-";
            if (sumEl) sumEl.innerText = "0";
            consoleEl.innerText = "Chờ thực thi...";
          }} else if (step === 1) {{
            if (numEl) numEl.innerText = "1";
            if (sumEl) sumEl.innerText = "1";
            consoleEl.innerText = "Lần lặp 1: number = 1, total_sum = 1";
          }} else if (step === 2) {{
            if (numEl) numEl.innerText = "2";
            if (sumEl) sumEl.innerText = "3";
            consoleEl.innerText = "Lần lặp 1: number = 1, total_sum = 1\\nLần lặp 2: number = 2, total_sum = 3";
          }} else {{
            if (numEl) numEl.innerText = "3";
            if (sumEl) sumEl.innerText = "6";
            consoleEl.innerText = "Lần lặp 1: number = 1, total_sum = 1\\nLần lặp 2: number = 2, total_sum = 3\\nLần lặp 3: number = 3, total_sum = 6\\nHoàn thành vòng lặp! Total = 6";
          }}
        }}
      }}
      function resetViz(idPrefix) {{
        idPrefix = idPrefix || "viz";
        window.vizStepMap[idPrefix] = 0;
        runVizStep(0, idPrefix);
      }}

      // Fix 2a: Adapter functions bridging LLM-generated onclick handlers to visualizer API
      function vizStepNext() {{ runVizStep(1); }}
      function vizStepPrev() {{ runVizStep(-1); }}
      function vizNextStep() {{ runVizStep(1); }}
      function vizPrevStep() {{ runVizStep(-1); }}
      function vizTogglePlay() {{ vizToggleAuto(); }}
      // Override vizReset to call resetViz (LLM uses vizReset, template defines resetViz)
      function vizReset() {{ resetViz(); }}
      var vizAutoTimer = null;
      function vizToggleAuto() {{
        if (vizAutoTimer) {{
          clearInterval(vizAutoTimer);
          vizAutoTimer = null;
          var btn = document.getElementById("viz-auto-btn");
          if (btn) btn.textContent = "Tự động chạy";
        }} else {{
          vizAutoTimer = setInterval(function() {{ runVizStep(1); }}, 1500);
          var btn = document.getElementById("viz-auto-btn");
          if (btn) btn.textContent = "Dừng tự động";
        }}
      }}
    </script>
  </body>
</html>
"""
    print(f"  [Success] Compiled SSOT Master Reading HTML for {session_id} - {lesson_id}")
    return full_html


def html_writer_agent(state: AgentState) -> AgentState:
    """LangGraph Agent wrapper for Reading HTML SSOT generation."""
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "html_writer_agent")
    
    # Write intermediate "generating..." status to the file so the user has immediate visual feedback
    from agents.creator_agents import get_lesson_dir
    html_sub = None
    try:
        lesson_dir = get_lesson_dir(state)
        html_sub = lesson_dir / "Bài đọc"
        html_sub.mkdir(parents=True, exist_ok=True)
        with open(html_sub / "reading.html", "w", encoding="utf-8") as f:
            f.write(f"<!-- [ĐANG KHỞI TẠO BÀI ĐỌC...] Hệ thống đang chạy tác nhân AI để sinh nội dung cho {session_id} - {lesson_id}: {lesson_title}. Vui lòng đợi trong giây lát... -->\n")
    except Exception:
        pass

    html_content = generate_reading_html(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        tech_stack=tech_stack,
        state=state
    )
    
    state["html_content"] = html_content
    state["reading_material"] = html_content
    state.setdefault("artifacts_status", {})["html"] = "Approved"
    
    # Save the generated content draft immediately to disk
    if html_sub:
        try:
            with open(html_sub / "reading.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception:
            pass
            
    return state


def classify_reading_type(lesson_title: str, lesson_details: str) -> Dict[str, str]:
    """Classify a lesson's reading type and return metadata including prompt_guideline.
    Called by common_utils.py to route LLM prompt generation.
    MUST always include: type, name, prompt_guideline.
    """
    text_to_check = (lesson_title + " " + lesson_details).lower()
    
    orientation_signals = ["tổng quan lộ trình", "định hướng", "tổng quan môn học", "demo sản phẩm", "lộ trình và demo"]
    is_orientation = any(sig in text_to_check for sig in orientation_signals)
    
    if is_orientation:
        return {
            "type": "ORIENTATION_LESSON",
            "name": lesson_title,
            "prompt_guideline": (
                "Author a Session 01 Orientation lesson titled 'Tổng quan lộ trình và Demo sản phẩm'.\n"
                "Structure the document into exactly 3 clear main sub-sections:\n"
                "1. '1. Tổng quan nội dung & Lộ trình môn học': Summarize course modules and learning milestones as a visual connected Timeline component (<div class='timeline-track'>...) or a structured list.\n"
                "2. '2. Phương pháp học tập hiệu quả & Kiến thức tiền đề': Detail proactive learning strategies, AI Pair-Programming workflow (Cursor/Windsurf), and prerequisite skills/knowledge required.\n"
                "3. '3. Demo sản phẩm dự án đầu ra': Present demo specifications, features, and outcomes of the capstone/mini-project students will build upon course completion.\n"
                "STRICT DIRECTIVES:\n"
                "- ABSOLUTELY FORBIDDEN to generate code demo snippets, executable sandboxes, or empty code blocks for this lesson.\n"
                "- Flexible titles and layout allowed (do NOT force rigid 5-section IDs).\n"
                "- Use 100% Accented Vietnamese for text and 2D Flat Vector Infographics/Timeline visual components."
            )
        }
        
    coding_keywords = ["python", "javascript", "c++", "cpp", "java", "sql", "react", "html", "css", "c#", "typescript", "programming", "code", "syntax", "array", "variable", "loop", "function", "struct", "class", "pointer", "oop"]
    
    is_coding = any(kw in text_to_check for kw in coding_keywords)
    
    if is_coding:
        return {
            "type": "CODING_LESSON",
            "name": lesson_title,
            "prompt_guideline": (
                "Author a programming/code-based lesson. Focus on syntax anatomy, RAM/Stack diagrams, "
                "side-by-side good/bad practice code blocks, and executable code snippets that run in the interactive playground. "
                "Enforce case-sensitive naming conventions (camelCase/snake_case) in English, and clear Vietnamese output for explanation text."
            )
        }
    else:
        return {
            "type": "PROCESS_OR_THEORY_LESSON",
            "name": lesson_title,
            "prompt_guideline": (
                "Author a process, tool, setup, or theoretical/management lesson (e.g. Git, Agile/Scrum, Excel, System Design, UML). "
                "DO NOT force code sandboxes or code files if not applicable. Instead, focus on Mermaid process workflows (flowchart/sequence), "
                "comparison matrix tables, step-by-step UI guides, configuration file templates, or terminal command sequences. "
                "Ensure logical flowcharts and operational lifecycle diagrams are present."
            )
        }

def unwrap_svg_and_diagrams(html_str: str) -> str:
    return html_str

def render_table(headers: List[str], rows: List[List[str]]) -> str:
    return ""

def force_center_media(html_str: str) -> str:
    return html_str

def ensure_comparison_table(html_str: str) -> str:
    return html_str

def ensure_problem_scene_image(html_str: str) -> str:
    return html_str


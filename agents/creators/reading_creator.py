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
from core.renderers.reading_renderer import assemble_reading_html

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
        lang = match.group(1) or "text"
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
    """Resolve language metadata from tech_stack string without hardcoded fallbacks."""
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] resolve_language_info: 'tech_stack' bị trống. Vui lòng truyền --tech-stack chính xác từ PM.")
    
    tech_lower = str(tech_stack).lower().strip()
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
            "name": tech_stack
        }
        
    for key, info in LANGUAGE_MAPPING_REGISTRY.items():
        if key in tech_lower:
            return info
    return {"hljs": "language-plaintext", "engine": "static", "name": tech_stack}


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


def sanitize_html_tags_and_italics(html_str: str) -> str:
    """
    Sanitize HTML string to eliminate unclosed/broken tags and prevent italic text leakage:
    1. Removes broken opening tags like `<h4 ...><i class=` with no closing angle bracket.
    2. Normalizes Phosphor icon `<i>` tags into `<span>` tags (<span class="ph-bold ..."></span>).
    3. Strips lone unclosed or self-closing `<i>` and `<em>` tags.
    4. Strips inline italic tags outside code blocks.
    """
    if not html_str:
        return ""
    c = html_str

    # 1. Clean broken unclosed opening tags at the end of elements or lines
    c = re.sub(r'<(?:i|em|span|div|p|h[1-6])\b[^>]*?class\s*=\s*(?:["\'][^"\'>]*$|[^>]*$)', '', c, flags=re.MULTILINE | re.IGNORECASE)
    c = re.sub(r'<i\s+class=[^>]*?(?=<h[1-6]|<p|<div|<ul|<li|<pre|$)', '', c, flags=re.IGNORECASE)

    # 2. Normalize Phosphor icon <i> tags to neutral <span> tags
    def normalize_icon_to_span(m):
        attrs = m.group(1).strip()
        body = m.group(2)
        if "ph-" in attrs or "ph " in attrs or "ph\b" in attrs:
            return f'<span {attrs}>{body}</span>'
        return body
    c = re.sub(r'<i\b([^>]*)>(.*?)</i>', normalize_icon_to_span, c, flags=re.DOTALL | re.IGNORECASE)

    # 3. Strip any lone unclosed or self-closing <i> and <em> tags
    c = re.sub(r'<(?:i|em)\b[^>]*/>', '', c, flags=re.IGNORECASE)
    c = re.sub(r'<(?:i|em)\b[^>]*>', '', c, flags=re.IGNORECASE)
    c = re.sub(r'</(?:i|em)>', '', c, flags=re.IGNORECASE)

    # 4. Strip stray markdown-converted <em> tags outside code blocks
    parts = re.split(r'(<pre\b.*?</pre>|<code\b.*?</code>)', c, flags=re.DOTALL | re.IGNORECASE)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'</?em\b[^>]*>', '', parts[i], flags=re.IGNORECASE)
    c = "".join(parts)

    return c


def get_clean_language_name(tech_stack: str) -> str:
    """Normalize tech stack string to a clean, canonical language / tool name."""
    if not tech_stack:
        return "Mã nguồn"
    t = tech_stack.lower()
    if any(k in t for k in ["typescript", "ts"]):
        return "TypeScript"
    elif any(k in t for k in ["javascript", "js", "node", "react", "vue", "next"]):
        return "JavaScript (ES6+)"
    elif any(k in t for k in ["python", "py", "django", "flask", "fastapi"]):
        return "Python 3"
    elif any(k in t for k in ["java", "spring"]):
        return "Java"
    elif "c++" in t or "cpp" in t:
        return "C++"
    elif "c#" in t or "csharp" in t or "dotnet" in t or ".net" in t:
        return "C#"
    elif "sql" in t or "mysql" in t or "postgres" in t:
        return "SQL"
    elif any(k in t for k in ["bash", "sh", "linux", "git"]):
        return "Bash/CLI"
    elif "html" in t or "css" in t:
        return "HTML/CSS"
    else:
        words = tech_stack.split()
        return words[0].capitalize() if words else "Mã nguồn"


def highlight_code_syntax(line: str, tech_stack: str = "") -> str:
    """
    Lightweight, multi-language syntax highlighter returning HTML with Tailwind CSS classes.
    Preserves exact whitespace indentation and colors keywords, strings, numbers, operators, and comments.
    """
    if not line:
        return "&nbsp;"
    
    # Extract leading whitespace to preserve exact indentation
    indent_len = len(line) - len(line.lstrip())
    indent_str = line[:indent_len]
    content = line[indent_len:]
    
    if not content:
        return html.escape(line)
        
    pattern = re.compile(
        r'(?P<COMMENT>//.*$|#.*$|--.*$)|'
        r'(?P<STRING>"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`)|'
        r'(?P<KEYWORD>\b(?:const|let|var|function|return|def|class|if|else|elif|for|while|import|from|in|as|try|except|catch|finally|throw|new|typeof|instanceof|async|await|yield|public|private|protected|static|void|int|double|boolean|String|SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|JOIN|ORDER|BY|GROUP|HAVING)\b)|'
        r'(?P<NUMBER>\b\d+(?:\.\d+)?\b)|'
        r'(?P<FUNC>\b[a-zA-Z_]\w*(?=\s*\())|'
        r'(?P<OPERATOR>=>|->|===|!==|==|!=|<=|>=|\+\+|--|\+=|-=|\*=|&&|\|\||[+\-*/%=<>!&|^~])|'
        r'(?P<IDENTIFIER>\b[a-zA-Z_$][a-zA-Z0-9_$]*\b)|'
        r'(?P<OTHER>[^\s\w]+|\s+)'
    )
    
    out_tokens = []
    pos = 0
    for m in pattern.finditer(content):
        start, end = m.span()
        if start > pos:
            out_tokens.append(html.escape(content[pos:start]))
        pos = end
        
        kind = m.lastgroup
        val = html.escape(m.group(0))
        
        if kind == "COMMENT":
            out_tokens.append(f'<span class="text-slate-400 italic">{val}</span>')
        elif kind == "STRING":
            out_tokens.append(f'<span class="text-emerald-600 font-medium">{val}</span>')
        elif kind == "KEYWORD":
            out_tokens.append(f'<span class="text-purple-600 font-bold">{val}</span>')
        elif kind == "NUMBER":
            out_tokens.append(f'<span class="text-amber-600 font-mono">{val}</span>')
        elif kind == "FUNC":
            out_tokens.append(f'<span class="text-blue-600 font-semibold">{val}</span>')
        elif kind == "OPERATOR":
            out_tokens.append(f'<span class="text-sky-600 font-bold">{val}</span>')
        elif kind == "IDENTIFIER":
            out_tokens.append(f'<span class="text-slate-800">{val}</span>')
        else:
            out_tokens.append(val)
            
    if pos < len(content):
        out_tokens.append(html.escape(content[pos:]))
        
    return html.escape(indent_str) + "".join(out_tokens)


def generate_fallback_visualizer_steps(code_lines: List[str], variables: List[Any], lesson_title: str) -> List[Dict[str, Any]]:
    """
    Generates intelligent step data if LLM omitted or provided incomplete steps.
    Extracts variable mutations and step explanations in 100% Accented Vietnamese.
    """
    steps = []
    curr_ram = {}
    
    var_slug_map = {}
    for v in variables:
        if isinstance(v, dict):
            name = v.get("name", "var")
            slug = re.sub(r'[^a-zA-Z0-9_-]', '-', name).lower()
            var_slug_map[name] = slug
        elif isinstance(v, str):
            slug = re.sub(r'[^a-zA-Z0-9_-]', '-', v).lower()
            var_slug_map[v] = slug

    for idx, raw_line in enumerate(code_lines, 1):
        line = str(raw_line).strip()
        if not line or line.startswith("//") or line.startswith("#") or line.startswith("/*") or line.startswith("*") or line in ("}", "};"):
            continue
            
        step_ram = dict(curr_ram)
        step_badge = ""
        
        # Check variable assignment (e.g., const x = 10, let y = "abc", z = 5)
        assign_match = re.search(r'(?:const|let|var)?\s*([a-zA-Z0-9_$]+)\s*=\s*(.+?);?$', line)
        if assign_match:
            v_name = assign_match.group(1).strip()
            v_val = assign_match.group(2).strip()
            v_val = re.sub(r'\s*//.*$', '', v_val).rstrip(';').strip()
            slug = var_slug_map.get(v_name, re.sub(r'[^a-zA-Z0-9_-]', '-', v_name).lower())
            step_ram[slug] = v_val[:30]
            curr_ram[slug] = v_val[:30]
            step_badge = f"{v_name} = {v_val[:20]}"
            step_log = f"&gt; [Bước {len(steps)+1}] Khởi tạo/gán giá trị: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800 font-bold'>{html.escape(v_name)} = {html.escape(v_val[:30])}</code>"
        elif "function" in line or "def " in line:
            fn_match = re.search(r'(?:function|def)\s+([a-zA-Z0-9_$]+)', line)
            fn_name = fn_match.group(1) if fn_match else "hàm"
            step_badge = f"Định nghĩa {fn_name}()"
            step_log = f"&gt; [Bước {len(steps)+1}] Định nghĩa hàm: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800 font-bold'>{html.escape(fn_name)}()</code>"
        elif "return" in line:
            ret_val = line.replace("return", "").strip().rstrip(";")
            step_badge = f"return {ret_val[:15]}"
            step_log = f"&gt; [Bước {len(steps)+1}] Trả về kết quả: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800 font-bold'>{html.escape(ret_val[:30])}</code>"
        elif "console.log" in line or "print(" in line or "System.out.print" in line:
            step_badge = "Xuất Console"
            step_log = f"&gt; [Bước {len(steps)+1}] Xuất dữ liệu ra màn hình Console"
        else:
            step_badge = "Thực thi"
            step_log = f"&gt; [Bước {len(steps)+1}] Thực thi dòng lệnh: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800'>{html.escape(line[:40])}</code>"
            
        steps.append({
            "line": idx,
            "ram": step_ram,
            "log": step_log,
            "badge": step_badge
        })
        
    return steps


def build_domain_adaptive_visualizer(lesson_title: str, tech_stack: str, viz_spec: Any) -> str:
    """
    Dynamically construct a Section 2.4 Step-by-Step Execution Visualizer component 
    from structured visualizer spec JSON without hardcoding any variables or language idioms.
    If the lesson is conceptual/theory or viz_spec is not applicable, cleanly returns "" (omits Section 2.4).
    """
    if not isinstance(viz_spec, dict) or not viz_spec.get("is_applicable", True):
        return ""
    
    clean_title = lesson_title.split(" - ")[-1] if " - " in lesson_title else lesson_title
    clean_lang = get_clean_language_name(tech_stack)
    
    title = viz_spec.get("title") or "2.4. Mô phỏng cơ chế vận hành từng bước (Step-by-Step Execution Visualizer)"
    if not title.startswith("2.4"):
        title = f"2.4. {title}"
    explanation = viz_spec.get("explanation") or f"Quan sát tiến trình thực thi từng dòng lệnh và biến đổi trạng thái của dữ liệu trong bộ nhớ cho bài học {clean_title}:"
    
    code_lines = viz_spec.get("code_lines") or []
    variables = viz_spec.get("variables") or []
    raw_steps = viz_spec.get("steps") or []
    
    if not code_lines and not raw_steps:
        return ""
    
    # 1. Build Code Display Lines with Syntax Highlighting & Line Numbers
    code_lines_html = []
    for idx, line in enumerate(code_lines, 1):
        highlighted = highlight_code_syntax(str(line), clean_lang)
        code_lines_html.append(f"""        <div id="viz-line-{idx}" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between font-mono text-xs whitespace-pre">
          <div class="flex items-center min-w-0">
            <span class="w-6 text-slate-400 text-[10px] select-none text-right mr-3 font-mono shrink-0">{idx}</span>
            <span class="truncate">{highlighted}</span>
          </div>
          <span id="viz-badge-{idx}" class="hidden text-[10px] font-sans px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold border border-amber-300 ml-2 shrink-0 animate-pulse"></span>
        </div>""")
    code_html = "\n".join(code_lines_html)
    
    # 2. Build Memory RAM State Rows (Clean - No redundant config text)
    ram_rows_html = []
    if variables:
        for var in variables:
            if isinstance(var, dict):
                v_name = var.get("name", "var")
                v_label = var.get("label") or f"Biến {v_name}"
                v_slug = re.sub(r'[^a-zA-Z0-9_-]', '-', v_name).lower()
                ram_rows_html.append(f"""        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center">
          <span class="text-slate-600 font-medium">{html.escape(v_label)}:</span>
          <span id="viz-ram-{v_slug}" class="font-bold text-slate-700 px-2.5 py-0.5 rounded bg-white border border-slate-200 min-w-[60px] text-center transition-all duration-300">---</span>
        </div>""")
            elif isinstance(var, str):
                v_slug = re.sub(r'[^a-zA-Z0-9_-]', '-', var).lower()
                ram_rows_html.append(f"""        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center">
          <span class="text-slate-600 font-medium">Biến {html.escape(var)}:</span>
          <span id="viz-ram-{v_slug}" class="font-bold text-slate-700 px-2.5 py-0.5 rounded bg-white border border-slate-200 min-w-[60px] text-center transition-all duration-300">---</span>
        </div>""")
    else:
        # Default status monitor
        ram_rows_html.append(f"""        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center">
          <span class="text-slate-600 font-medium">Trạng thái luồng:</span>
          <span id="viz-ram-status" class="font-bold text-emerald-600 px-2 py-0.5 rounded bg-white border border-slate-200">Đang hoạt động (Active)</span>
        </div>""")
        
    ram_html = "\n".join(ram_rows_html)
    
    # 3. Build window.vizSteps JSON (Use LLM steps or Smart Fallback)
    sanitized_steps = []
    if raw_steps and isinstance(raw_steps, list) and len(raw_steps) >= 2:
        for s in raw_steps:
            if isinstance(s, dict):
                raw_ram = s.get("ram") or {}
                clean_ram = {}
                for rk, rv in raw_ram.items():
                    clean_rk = re.sub(r'[^a-zA-Z0-9_-]', '-', str(rk)).lower()
                    clean_ram[clean_rk] = str(rv)
                
                log_val = s.get("log") or f"&gt; Thực thi dòng {s.get('line', 1)}"
                if not log_val.startswith("&gt;") and not log_val.startswith("<div") and not log_val.startswith(">"):
                    log_val = f"&gt; {log_val}"
                if log_val.startswith(">"):
                    log_val = f"&gt;{log_val[1:]}"
                    
                sanitized_steps.append({
                    "line": s.get("line", 1),
                    "ram": clean_ram,
                    "log": log_val,
                    "badge": s.get("badge") or (list(clean_ram.values())[-1] if clean_ram else "")
                })
    else:
        # Generate smart fallback steps from code_lines
        sanitized_steps = generate_fallback_visualizer_steps(code_lines, variables, clean_title)
            
    script_block = f"<script>window.vizSteps = {json.dumps(sanitized_steps, ensure_ascii=False)};</script>" if sanitized_steps else ""
    
    return f"""
<h3 id="sec-2-4-mo-phong-co-che-van-hanh-tung-buoc" class="font-montserrat font-bold text-xl text-slate-900 mb-3">{title}</h3>
<p class="text-slate-600 mb-4 leading-relaxed">{explanation}</p>

<div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm my-6 text-slate-800">
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-4">
    <!-- Cột trái: Mã nguồn thực thi -->
    <div class="flex flex-col bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="bg-slate-100/80 px-4 py-2 text-xs font-mono text-slate-700 font-bold border-b border-slate-200 flex items-center justify-between">
        <span>Mã nguồn thực thi ({clean_lang})</span>
        <span id="viz-step-badge" class="px-2 py-0.5 bg-slate-200 text-slate-700 text-[11px] rounded font-sans">Sẵn sàng</span>
      </div>
      <div id="viz-code-display" class="p-3.5 font-mono text-xs text-slate-800 space-y-1.5 overflow-x-auto min-h-[160px]">
{code_html}
      </div>
    </div>

    <!-- Cột phải: Trạng thái bộ nhớ RAM -->
    <div class="flex flex-col bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="bg-slate-100/80 px-4 py-2 text-xs font-mono text-slate-700 font-bold border-b border-slate-200 flex items-center justify-between">
        <span>Trạng thái bộ nhớ (Memory Canvas)</span>
        <span class="px-2 py-0.5 rounded bg-sky-100 text-sky-800 text-[11px] font-bold font-sans">RAM State</span>
      </div>
      <div class="p-4 space-y-3 flex-1 text-xs font-mono">
{ram_html}
      </div>
    </div>
  </div>

  <!-- Nút điều khiển -->
  <div class="flex flex-wrap items-center justify-between gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
    <div class="flex items-center gap-2">
      <button type="button" onclick="runVizStep(-1)" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center gap-1 transition-all">
        <span class="ph-bold ph-caret-left"></span> Bước trước
      </button>
      <button type="button" onclick="runVizStep(1)" class="px-3 py-1.5 rounded-lg bg-rikkei-red text-white font-semibold text-xs flex items-center gap-1 hover:bg-rikkei-darkred transition-all shadow-sm">
        Tiếp theo <span class="ph-bold ph-caret-right"></span>
      </button>
      <button type="button" onclick="runVizStep(-999)" class="px-2.5 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-100 text-xs transition-all" title="Reset">
        <span class="ph-bold ph-arrow-counter-clockwise"></span> Đặt lại
      </button>
    </div>
    <div class="flex items-center gap-1.5">
      <button type="button" onclick="vizToggleAuto()" id="viz-auto-btn" class="px-3 py-1.5 rounded-lg bg-rikkei-red text-white font-semibold text-xs hover:bg-rikkei-darkred transition-all shadow-sm">Tự động chạy</button>
    </div>
  </div>

  <!-- Terminal log -->
  <div class="mt-3 bg-slate-100 rounded-xl p-3 border border-slate-200 shadow-inner">
    <div class="text-[11px] font-mono text-slate-600 mb-1.5 flex items-center gap-1.5 font-bold">
      <span class="ph-bold ph-terminal text-emerald-800"></span> Nhật ký thực thi từng bước (Console Log):
    </div>
    <div id="viz-terminal-log" class="h-[110px] overflow-y-auto bg-white text-slate-800 font-mono text-xs p-2.5 rounded border border-slate-200 space-y-1">
      <div class="text-slate-400 italic">&gt; Sẵn sàng mô phỏng từng bước cho {clean_title}. Bấm "Tiếp theo" để bắt đầu...</div>
    </div>
  </div>
</div>
{script_block}
"""


def extract_2tier_toc(know_html: str, ex_text: str, section1_title: str, section2_title: str) -> str:
    """Generate clean 5-section Table of Contents navigation listing strictly main sections 1 to 5 without sub-items."""
    clean_sec1 = re.sub(r'^\s*1\.\s*', '', section1_title).strip()
    clean_sec2 = re.sub(r'^\s*2\.\s*', '', section2_title).strip()
    
    return f"""
    <a href="#section-1" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">1. {clean_sec1}</a>
    <a href="#section-2" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">2. {clean_sec2}</a>
    <a href="#section-3" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">3. Các ví dụ ứng dụng thực tiễn</a>
    <a href="#section-4" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">4. Tổng kết bài học</a>
    <a href="#section-5" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">5. Tài liệu tham khảo</a>
    """


def sanitize_references(refs: List[Dict[str, str]], tech_stack: str) -> List[Dict[str, str]]:
    """
    Sanitize reference links, replacing hallucinated or empty URLs with canonical official docs.
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
        if not tech_stack or not str(tech_stack).strip():
            raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] sanitize_references: 'tech_stack' bị trống.")
        tech_key = str(tech_stack).lower().strip()
        for k, links in CANONICAL_DOC_LINKS.items():
            if k in tech_key:
                return links
        return [{"title": f"Tài liệu chính thức {tech_stack}", "url": f"https://www.google.com/search?q={tech_stack}+official+documentation"}]
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
    
    allowed_scope_raw = state.get("allowed_scope") or state.get("previous_lessons") or []
    if isinstance(allowed_scope_raw, list):
        allowed_scope = ", ".join(str(x) for x in allowed_scope_raw if str(x).strip())
    else:
        allowed_scope = str(allowed_scope_raw).strip()

    forbidden_scope_raw = state.get("forbidden_scope") or []
    if isinstance(forbidden_scope_raw, list):
        forbidden_scope = ", ".join(str(x) for x in forbidden_scope_raw if str(x).strip())
    else:
        forbidden_scope = str(forbidden_scope_raw).strip()

    image_skill = load_skill_content("image_prompt_standard")
    
    system_prompt = f"""You are a Senior Learning Content Authoring Expert at Rikkei Education.
Your task is to author a DETAILED READING MATERIAL (SSOT) strictly adhering to the 5-SECTION PEDAGOGICAL ARCHITECTURE.

MANDATORY RULES & DIRECTIVES:
1. 5-SECTION PEDAGOGICAL FLOW & HEADING OWNERSHIP:
   - The master HTML template ALREADY renders the main Section <h2> headers:
     * `<h2>1. {{section1_title}}</h2>`
     * `<h2>2. {{section2_title}}</h2>`
     * `<h2>3. Các ví dụ ứng dụng thực tiễn</h2>`
     * `<h2>4. Tổng kết bài học & Các lỗi thường gặp</h2>`
     * `<h2>5. Tài liệu tham khảo & Self-Test</h2>`
   - CRITICAL HEADING DIRECTIVE: Inside `problem_html`, `knowledge_html`, `example_html`, and `notes_html`, ABSOLUTELY DO NOT generate top-level `<h1>` or `<h2>` tags! All sub-sections MUST start at `<h3>` level (`2.1`, `2.2`, `3.1`, `4.1`...).
   - Section 1 - DYNAMIC TITLE: You MUST create a context-aware Section 1 title matching the lesson topic in Accented Vietnamese (e.g., "Tại sao cần dùng hàm?", "Vấn đề khi thiếu cấu trúc rẽ nhánh", "Tại sao cần môi trường ảo?"). Save title in `section1_title`.
   - Section 2 - DYNAMIC TITLE: You MUST create a context-aware Section 2 title detailing the knowledge concept (e.g., "Cú pháp và cơ chế hoạt động", "Mô hình đối tượng và cấu trúc JSON"). Save title in `section2_title`.
   - Section 1 CONTENT: Detailed & specific enterprise real-world scenario (e.g. E-commerce order checkout engine). Analyze the technical conflict and business risks of running code sequentially line-by-line without conditional checks or proper abstractions. Introduce current lesson concept as the dynamic solution.
   - Section 2 CONTENT: Core concepts, technical breakdown in HTML format using `<ul class="...">` and `<strong class="...">` for keywords. Under each sub-heading (`2.1`, `2.2`), include a Problem Callout Box and a Code Sandbox snippet.
   - Section 3 CONTENT: Practical Application Examples (3 progressive examples: 3.1 Minimal syntax, 3.2 Business logic, 3.3 Enterprise scenario).
   - Section 4 CONTENT: 4.1 Key Takeaways summary, 4.2 Decision Matrix HTML Table, and 4.3 Gotchas/Errors with side-by-side BAD vs GOOD code.
   - Section 5: References & 3 Interactive Self-Test questions.

2. HTML DATA FORMAT & CALLOUT BOX SYSTEM:
   - DO NOT use Markdown syntax (such as **, ###, - ).
   - Return clean HTML elements directly: `<p class="text-slate-600 mb-4 leading-relaxed">`, `<ul class="list-disc pl-6 space-y-2 text-slate-600 my-4">`, `<strong class="font-semibold text-slate-900">`, `<code class="px-1.5 py-0.5 rounded bg-slate-100 text-rikkei-red font-mono text-sm">`.
   - MUST use strict Callout Box color system by role:
     * 🟠 **Warning/Note**: Orange -> `<div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">`
     * 🔴 **Error/Gotchas**: Red -> `<div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">`
     * 🟢 **Success/Best Practice**: Green -> `<div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50/60 text-slate-800 my-4">`
     * 🔵 **Tip/Info**: Blue -> `<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">`

3. 2D FLAT VECTOR SCENE IMAGE STANDARD (SECTION 1 - PROBLEM STATEMENT):
   - In Section 1 (Problem Statement / Đặt vấn đề), ABSOLUTELY DO NOT force manual HTML, CSS, or raw inline SVG code diagrams.
   - Instead, use a 2D Flat Vector Technical Illustration / Scene Image generated via `image_prompt_standard` skill describing the concrete real-world problem statement of the lesson.
   - ULTRA-INTUITIVE STUDENT-FRIENDLY DIRECTIVE: The image MUST be ultra-clean, minimal, friendly, and immediately understandable by beginner students at first glance (nhìn vào hiểu ngay ý bài toán trong 3 giây). Use real-world 2D flat vector objects (shopping cart, receipt, discount voucher, pass badge) with 100% Accented Vietnamese node titles.
   - Embed the image tag cleanly: `<div class="my-6 text-center"><img src="images/..." alt="..." class="w-full max-w-3xl h-auto mx-auto rounded-xl shadow-sm border border-slate-200" /><p class="text-center text-sm text-slate-500 italic mt-3">Caption in Accented Vietnamese...</p></div>`.
{image_skill}

4. STRICT NO EMOJI TEXT:
   - ABSOLUTELY FORBIDDEN to use text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶). Use Phosphor Icons CSS symbols (`<span class="ph-bold ph-..."></span>`) only.

5. MANDATORY SENTENCE ENDING PERIOD DIRECTIVE:
   - Every text sentence, list item, bullet point, question, and explanation MUST 100% end with a period (.). Never leave sentences unpunctated.

6. SECTION 3 PROGRESSIVE EXAMPLES & CODE BLOCK RULE:
   - Section 3 MUST provide 3 progressive examples: Example 3.1 (Minimal syntax) ➔ Example 3.2 (Business problem) ➔ Example 3.3 (Enterprise production).
   - EACH EXAMPLE (`3.1`, `3.2`, `3.3`) MUST be accompanied by an execution code block: `<pre><code class="language-{tech_stack}">...</code></pre>`. Replace `{tech_stack}` with target language identifier (e.g. `python`, `javascript`, `typescript`, `java`, `c`, `cpp`, `sql`).

7. HIERARCHICAL SUB-HEADING NUMBERING DIRECTIVE:
   - All `<h3>` sub-headings MUST match parent numbering: Section 2 sub-headings MUST be `2.1`, `2.2`, `2.3...`; Section 3 sub-headings MUST be `3.1`, `3.2`, `3.3...`; Section 4 sub-headings MUST be `4.1`, `4.2...`.

8. STRICT UNNECESSARY ITALIC BAN & CLEAN CAPTION CONTRACT:
   - 🚨 100% BAN ON UNNECESSARY ITALIC TEXT 🚨: 100% FORBIDDEN to use italics (`<i>`, `<em>`, `*text*`) in paragraphs, bullet lists, sub-headings, bold technical terms, or callouts. Italics are ONLY allowed in image captions directly below images.
   - 🚨 NO META-TEXT IN IMAGE CAPTIONS 🚨: Image captions MUST NOT contain meta phrases like "Sơ đồ 2D flat vector minh họa...". Write direct, clear, professional descriptions (e.g., `Hình 1.1: Quy trình xử lý tự động đơn hàng`).

9. CONTEXT-AWARE THEORY INTEGRATION DIRECTIVE:
   - In Section 2 (`knowledge_html`), integrate visual snippets matching topic nature:
     * For programming/syntax topics: Include code syntax snippets under each `2.1`, `2.2` sub-heading alongside Syntax Anatomy / Memory diagrams.
     * For conceptual / setup / tool topics (Git, VS Code, Agile, Architecture): Include SVG/Mermaid flowcharts, Terminal commands, or Config tables instead of empty sandboxes.

10. 100% ACCENTED VIETNAMESE EXPLANATIONS & ENGLISH CODE IDENTIFIERS:
    - ALL explanations, bullet points, question texts, and code comments MUST be in 100% Production-Grade Accented Vietnamese.
    - ALL variable names, function names, parameter names, and syntax placeholders MUST BE IN ENGLISH using standard conventions (e.g. `snake_case` in Python, `camelCase` in JavaScript).

11. STRICT KNOWLEDGE SCOPE BOUNDARY CONTRACT (MULTI-SUBJECT & TECH-AGNOSTIC):
    - ALLOWED KNOWLEDGE (Concepts already taught or in current lesson details): {allowed_scope or 'Basic fundamentals up to current lesson'}
    - FORBIDDEN KNOWLEDGE (Future lessons / unlearned advanced concepts): {forbidden_scope or 'Advanced frameworks, DOM, APIs, Async, or classes if not taught yet'}
    - 🚨 ZERO SCOPE LEAKAGE CONTRACT 🚨:
      * ABSOLUTELY FORBIDDEN to use any libraries, syntax, functions, APIs, or data structures listed under FORBIDDEN KNOWLEDGE.
      * All code examples, gotchas, and explanations MUST strictly stay within ALLOWED KNOWLEDGE.

12. DYNAMIC ADAPTIVE INTERACTIVE VISUALIZER SCHEMA (FOR EXECUTABLE LESSONS):
    - For Executable Coding / Algorithm lessons (Python, JavaScript, Java, C++, SQL): Provide structured `interactive_visualizer` JSON data:
      * `is_applicable`: true
      * `title`: "2.4. Mô phỏng cơ chế vận hành từng bước (Step-by-Step Execution Visualizer)"
      * `explanation`: "Mô tả ngắn gọn luồng mô phỏng"
      * `code_lines`: ["line 1", "line 2", ...] (Actual code lines of the lesson with Vietnamese comments)
      * `variables`: [{{"name": "varName", "label": "Nhãn hiển thị tiếng Việt"}}, ...] (Actual variables used in code_lines)
      * `steps`: [{{"line": 1, "ram": {{"varName": "giá trị"}}, "log": "<div>&gt; Giải thích bước 1</div>"}}, ...]
    - For Pure Concept / Theory / Setup / Intro / Tooling / Architecture lessons (Git VCS overview, Agile, Docker overview, UML):
      * `interactive_visualizer`: {{ "is_applicable": false }} (The system will cleanly omit the Step-Tracker and render SVG diagrams / Comparison tables instead).

Return pure JSON data strictly adhering to the schema:
{{
  "section1_title": "Dynamic Section 1 title matching lesson topic in Accented Vietnamese (e.g., 'Tại sao cần dùng hàm?')",
  "section2_title": "Dynamic Section 2 title detailing knowledge concept in Accented Vietnamese (e.g., 'Cú pháp và cơ chế hoạt động')",
  "problem_html": "<p class=\"text-slate-600 mb-4 leading-relaxed\">Section 1 HTML content in Accented Vietnamese (NO h1/h2 tags)...</p>",
  "diagram_svg": "<svg viewBox=\"0 0 800 250\" class=\"w-full h-auto rikkei-diagram\">...</svg>",
  "knowledge_html": "<h3 id=\"sec-2-1\" class=\"text-xl font-bold text-slate-900 mb-3\">2.1. Cú pháp & Khái niệm...</h3><p class=\"text-slate-600 mb-4 leading-relaxed\">Nội dung Section 2...</p>",
  "interactive_visualizer": {{
    "is_applicable": true,
    "title": "2.4. Mô phỏng cơ chế vận hành từng bước (Step-by-Step Execution Visualizer)",
    "explanation": "Quan sát quá trình thực thi...",
    "code_lines": ["// Dòng 1...", "let x = 10;"],
    "variables": [{{"name": "x", "label": "Biến x"}}],
    "steps": [{{"line": 1, "ram": {{"x": "10"}}, "log": "<div>&gt; Khởi tạo x = 10</div>"}}]
  }},
  "example_code": "Combined executable code snippet in target tech stack language",
  "example_html": "<h3 id=\"sec-3-1\" class=\"text-xl font-bold text-slate-900 mb-3\">3.1. Ví dụ 3.1: Cơ bản...</h3><p class=\"text-slate-600 mb-4 leading-relaxed\">Giải thích...</p><pre><code class=\"language-{tech_stack}\">Code snippet 1</code></pre>",
  "notes_html": "<h3 id=\"sec-4-1\" class=\"text-xl font-bold text-slate-900 mb-3\">4.1. Kiến thức trọng tâm</h3><ul class=\"list-disc pl-6 space-y-2 text-slate-600 my-4\"><li>Tóm tắt...</li></ul><h3 id=\"sec-4-2\" class=\"text-xl font-bold text-slate-900 mb-3\">4.2. Bảng Ma trận Quyết định</h3>...<h3 id=\"sec-4-3\" class=\"text-xl font-bold text-slate-900 mb-3\">4.3. Các lỗi thường gặp & Lưu ý thực tế</h3>...",
  "references": [
    {{"title": "Official authoritative documentation title", "url": "https://..."}}
  ],
  "self_test_questions": [
    {{
      "question": "Câu hỏi trắc nghiệm tiếng Việt dựa trên kịch bản/dữ liệu cụ thể trong bài đọc...",
      "options": ["A. Lựa chọn A", "B. Lựa chọn B", "C. Lựa chọn C", "D. Lựa chọn D"],
      "correct_idx": "A",
      "explanation": "Giải thích chi tiết bằng tiếng Việt..."
    }}
  ]
}}"""

    blueprint = state.get("lesson_blueprint")
    if blueprint:
        blueprint_context = f"""Dữ liệu phác thảo bài học (Lesson Blueprint):
- Kịch bản thống nhất: {json.dumps(blueprint.get('real_world_scenario', {}), ensure_ascii=False)}
- Các khái niệm cốt lõi (Hãy viết nội dung Section 2 chi tiết dựa trên danh sách này): {json.dumps(blueprint.get('key_concepts', []), ensure_ascii=False)}
- Các ví dụ thực tế lũy tiến (Hãy viết nội dung Section 3 dựa trên danh sách ví dụ 3.1, 3.2, 3.3 này): {json.dumps(blueprint.get('progressive_examples', []), ensure_ascii=False)}
- Lỗi thường gặp (Hãy viết nội dung Section 4 dựa trên danh sách gotchas này): {json.dumps(blueprint.get('gotchas_and_errors', []), ensure_ascii=False)}
"""
    else:
        blueprint_context = ""

    user_prompt = f"""{blueprint_context}
Author detailed, exhaustive reading material content for:
Session: {session_id}
Lesson: {lesson_id} - {lesson_title}
Curriculum Details: {lesson_details}
Expected Output: {expected_output}
Target Technology Stack: {tech_stack}
Allowed Knowledge Scope: {allowed_scope or 'Fundamentals up to current lesson'}
Forbidden Knowledge Scope (STRICTLY PROHIBITED): {forbidden_scope or 'Future unlearned tech/syntax'}

MANDATORY DEPTH & EXHAUSTIVE PEDAGOGY CONTRACT:
1. Section 2 MUST contain 3 full sub-sections (2.1, 2.2, 2.3) detailing syntax variants, mechanism breakdowns, and bullet point explanations. Under each sub-section, include an enterprise problem callout box and a code sandbox snippet in {tech_stack}.
2. Section 3 MUST contain 3 progressive examples (3.1 Minimal syntax, 3.2 Business logic, 3.3 Enterprise scenario). Each example MUST contain an executable code block (`<pre><code class="language-{tech_stack}">...</code></pre>`).
3. STRICT KNOWLEDGE SCOPE: 100% of code examples and explanations MUST ONLY use concepts from Allowed Knowledge Scope. ABSOLUTELY DO NOT leak any concept, keyword, or API from Forbidden Knowledge Scope!
4. Section 5 MUST contain exactly 3 interactive self-test MCQ questions under `self_test_questions`. They MUST be high-context, using variables/data from the examples above, and have detailed explanations.
5. Return ONLY raw pure JSON strictly adhering to the schema."""

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

        st_match = re.search(r'"self_test_questions"\s*:\s*(\[.*?\])', cleaned, re.DOTALL)
        if st_match:
            try:
                result['self_test_questions'] = json.loads(st_match.group(1))
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
        # Auto-sanitize AI cliché words
        c = re.sub(r'\bvô cùng\b', 'cực kỳ', c, flags=re.IGNORECASE)
        c = re.sub(r'\btuyệt vời\b', 'hiệu quả', c, flags=re.IGNORECASE)
        c = re.sub(r'\bbậc nhất\b', 'hàng đầu', c, flags=re.IGNORECASE)
        c = re.sub(r'\bbí kíp\b', 'quy tắc', c, flags=re.IGNORECASE)
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

        # Clean broken tags, normalize phosphor icons, and prevent italic leakage
        c = sanitize_html_tags_and_italics(c)

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
  <button type="button" onclick="runVizStep(1)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition-all flex items-center gap-1"><span class="ph-bold ph-play text-xs"></span> Bắt đầu</button>
  <button type="button" onclick="runVizStep(0)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-500 hover:bg-amber-600 text-white shadow-sm transition-all flex items-center gap-1"><span class="ph-bold ph-pause text-xs"></span> Tạm dừng</button>
  <button type="button" onclick="runVizStep(1)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#be111c] hover:bg-[#90000a] text-white shadow-sm transition-all flex items-center gap-1"><span class="ph-bold ph-step-forward text-xs"></span> Từng bước</button>
  <button type="button" onclick="runVizStep(-999)" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-200 hover:bg-slate-300 text-slate-800 shadow-sm transition-all flex items-center gap-1"><span class="ph-bold ph-arrow-counter-clockwise text-xs"></span> Đặt lại</button>
</div>'''
            return panel_content
        c = re.sub(r'<div\s+class="flex\s+items-center\s+gap-2">\s*<button\b.*?</button>\s*</div>', normalize_viz_button_panel, c, flags=re.DOTALL | re.IGNORECASE)

        # Systemically normalize all LLM-generated onclick handlers on buttons to runVizStep / vizToggleAuto / resetViz
        c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizAutoRun|vizAutoStart|vizStartAuto|vizRunAuto|autoRun|autoPlay|toggleAuto|vizTogglePlay|vizPlay)\s*\(\s*\)"', 'onclick="vizToggleAuto()"', c, flags=re.IGNORECASE)
        c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizStepNext|vizNextStep|vizNext|vizStepForward|vizForward|stepNext|nextStep|vizStep|vizStart|vizRun)\s*\(\s*\)"', 'onclick="runVizStep(1)"', c, flags=re.IGNORECASE)
        c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizStepPrev|vizPrevStep|vizPrev|vizStepBackward|vizBackward|stepPrev|prevStep)\s*\(\s*\)"', 'onclick="runVizStep(-1)"', c, flags=re.IGNORECASE)
        c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizReset|vizRestart|resetVisualizer|resetViz)\s*\(\s*\)"', 'onclick="runVizStep(-999)"', c, flags=re.IGNORECASE)

        # Fix unescaped quotes inside Javascript script tags that cause syntax error "Unexpected keyword or identifier"
        c = re.sub(r'consoleEl\.innerText\s*=\s*"> Sẵn sàng chạy mô phỏng[^"]*";', "consoleEl.innerText = '> Sẵn sàng chạy mô phỏng từng bước. Bấm \\'Tiếp theo\\' để bắt đầu...';", c)
        
        # Auto-attach onclick handlers to visualizer buttons if missing
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Lùi lại|Quay lại|Trở về)\s*</button>', r'\1 onclick="runVizStep(-1)">Lùi lại</button>', c, flags=re.IGNORECASE)
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Tiếp theo|Kế tiếp|Chạy tiếp)\s*</button>', r'\1 onclick="runVizStep(1)">Tiếp theo</button>', c, flags=re.IGNORECASE)
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Tự động chạy|Auto Play)\s*</button>', r'\1 onclick="vizToggleAuto()">Tự động chạy</button>', c, flags=re.IGNORECASE)
        c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Thử lại|Đặt lại|Reset)\s*</button>', r'\1 onclick="runVizStep(-999)">Thử lại</button>', c, flags=re.IGNORECASE)

        # Strip Tailwind 'italic' class from all elements
        c = re.sub(r'\bitalic\b', '', c)

        # Clean meta-phrases from image captions (replace "Sơ đồ 2D flat vector..." with clean "Hình 1.1: Quy trình...")
        c = re.sub(r'(?:Sơ đồ 2D flat vector minh họa|Hình ảnh 2D flat vector minh họa|Minh họa 2D flat vector|Sơ đồ 2D|Minh họa 2D|Sơ đồ minh họa)\s*(?:quy trình|ngữ cảnh thực tế cho bài học|cho)?\s*', 'Hình 1.1: Quy trình ', c, flags=re.IGNORECASE)

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

        # Strip font-mono from h1-h6 headings and ensure font-montserrat font-bold without class duplication
        def sanitize_heading_fonts(m):
            tag_name = m.group(1)
            attrs = m.group(2)
            class_match = re.search(r'class=["\']([^"\']*)["\']', attrs)
            if class_match:
                classes = [cls for cls in class_match.group(1).split() if cls not in ('font-mono', 'font-montserrat', 'font-bold')]
                classes = ['font-montserrat', 'font-bold'] + classes
                clean_attrs = re.sub(r'class=["\'][^"\']*["\']', f'class="{" ".join(classes)}"', attrs)
            else:
                clean_attrs = f'class="font-montserrat font-bold" {attrs}'
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
    # Strip any LLM-hallucinated <img> tags and image wrappers inside prob_html to prevent duplicate/broken images
    prob_html = re.sub(r'<div\s+class="[^"]*my-6[^"]*text-center[^"]*">\s*<img\b.*?</p>\s*</div>', '', prob_html, flags=re.DOTALL | re.IGNORECASE)
    prob_html = re.sub(r'<img\b[^>]*>', '', prob_html, flags=re.IGNORECASE)
    diagram_svg = guard_svg_syntax(data.get("diagram_svg", ""))
    
    # 2D Flat Vector Technical Illustration Scene Image (AGENTS.md Directive 4)
    clean_lesson_slug = slugify_id(lesson_title)
    dynamic_img_name = f"scene_{clean_lesson_slug}.png"
    
    # Check if a custom generated image exists in images/ folder, or generate it via generate_image_api
    has_image_on_disk = False
    if state:
        try:
            from agents.creator_agents import get_lesson_dir
            from agents.creators.mindmap_creator import generate_image_api
            lesson_dir = get_lesson_dir(state)
            images_dir = lesson_dir / "Bài đọc" / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            image_file = images_dir / dynamic_img_name
            if image_file.exists() and image_file.stat().st_size > 1000:
                has_image_on_disk = True
            else:
                image_prompt = data.get("image_prompt") or f"Clean 2D Flat Vector Technical Infographic Illustration, 16:9 widescreen, depicting {lesson_title} real-world problem scenario in {tech_stack}, clean vector icons, professional corporate palette navy slate emerald, no text overlays, minimalist."
                if generate_image_api(image_prompt, image_file):
                    has_image_on_disk = True
        except Exception as e:
            print(f"  [Image Generator Notice] Skipped scene image generation: {e}")

    # Exclusive Visual Component Dispatcher (1-of-2 Rule: Image PNG or SVG Flowchart)
    if has_image_on_disk:
        sec1_visual_html = f"""<div class="my-6 text-center">
  <img src="images/{dynamic_img_name}" alt="Sơ đồ bối cảnh thực tế: {lesson_title}" class="w-full max-w-3xl h-auto mx-auto rounded-xl shadow-sm border border-slate-200" onerror="this.closest('.my-6').style.display='none';" />
  <p class="text-center text-sm text-slate-500 italic mt-3">Hình 1.1: Sơ đồ bối cảnh thực tế bài học: {lesson_title}</p>
</div>"""
        context_img_url = f"images/{dynamic_img_name}"
    elif diagram_svg and len(diagram_svg.strip()) > 50:
        sec1_visual_html = f"""<div class="my-6 text-center">
  <div class="max-w-3xl mx-auto">{diagram_svg}</div>
  <p class="text-center text-sm text-slate-500 italic mt-3">Hình 1.1: Sơ đồ luồng bối cảnh thực tế bài học: {lesson_title}</p>
</div>"""
        context_img_url = None
    else:
        sec1_visual_html = ""
        context_img_url = None

    know_html = clean_stray_chars(inject_subheading_ids(guard_mermaid_syntax(ensure_html(data.get("knowledge_html") or data.get("knowledge_text", "")))))
    
    # Check if know_html already contains Section 2.4 to prevent duplicate visualizer insertion
    has_existing_viz_in_know = (
        'id="sec-2-4' in know_html
        or 'viz-step-badge' in know_html
        or 'viz-code-display' in know_html
        or 'Mô phỏng cơ chế vận hành từng bước' in know_html
    )
    if not has_existing_viz_in_know:
        viz_spec = data.get("interactive_visualizer") or data.get("visualizer_spec")
        raw_sec2_4 = data.get("section2_4_html") or ""
        if viz_spec and isinstance(viz_spec, dict):
            section2_4 = build_domain_adaptive_visualizer(lesson_title, tech_stack, viz_spec)
        elif raw_sec2_4 and len(raw_sec2_4.strip()) > 30:
            section2_4 = raw_sec2_4
        else:
            section2_4 = ""

        if section2_4:
            know_html = know_html + "\n" + clean_stray_chars(inject_subheading_ids(section2_4))

    ex_text = clean_stray_chars(inject_subheading_ids(guard_mermaid_syntax(ensure_html(data.get("example_html") or data.get("example_text", "")))))
    notes_html = clean_stray_chars(ensure_html(data.get("notes_html") or data.get("notes_text", "")))

    # Strip LLM hallucinated duplicate main section headers (e.g. <h1> / <h2>) inside section payloads
    prob_html = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', prob_html, flags=re.DOTALL | re.IGNORECASE).strip()
    know_html = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', know_html, flags=re.DOTALL | re.IGNORECASE).strip()
    ex_text = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', ex_text, flags=re.DOTALL | re.IGNORECASE).strip()
    notes_html = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', notes_html, flags=re.DOTALL | re.IGNORECASE).strip()

    # Resolve Language Info from Tech Stack (Problem 1 Requirement 1.2)
    lang_info = resolve_language_info(tech_stack)

    # Auto-convert code blocks: Live Pyodide Sandbox for Python (Section 3), Static VS Code-styled code card for syntax/gotchas (Section 2 & 4)
    def convert_code_to_live_sandbox(html_text: str, lang_meta: Dict[str, str], force_static: bool = False, sb_prefix: str = "sb") -> str:
        if not html_text: return ""
        import re, html as html_lib
        counter = 0
        is_python = (lang_meta.get("engine") == "pyodide") and not force_static
        is_js = (lang_meta.get("engine") == "js_worker" or lang_name in ["JavaScript", "TypeScript"]) and not force_static
        is_executable = (is_python or is_js) and not force_static
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

            if is_executable and not is_cli_cmd and not is_abstract_syntax:
                run_fn = "runPythonCode" if is_python else "runJsCode"
                return f'''<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="{run_fn}('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
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

    # Dynamic 2-Tier Sidebar TOC navigation links
    sidebar_toc_nav = extract_2tier_toc(know_html, ex_text, section1_title, section2_title)

    # Problem 3.3: Sanitize References and inject canonical docs if missing
    refs_items = sanitize_references(data.get("references", []), tech_stack)
    
    json_payload = {
        "section_titles": {
            "sec1": section1_title,
            "sec2": section2_title,
            "sec3": "Các ví dụ ứng dụng thực tiễn",
            "sec4": "Tổng kết bài học & Các lỗi thường gặp",
            "sec5": "Tài liệu tham khảo & Câu hỏi ôn tập"
        },
        "sec1_html": prob_html,
        "sec1_visual_html": sec1_visual_html,
        "sec2_html": know_html,
        "sec3_html": ex_text,
        "sec4_html": notes_html,
        "context_image_url": context_img_url,
        "reference_links": refs_items,
        "show_visualizer": False,
        "self_test_questions": data.get("self_test_questions", [])
    }
    metadata = {
        "lesson_title": lesson_title,
        "tech_stack": tech_stack,
        "session_id": session_id,
        "lesson_id": lesson_id
    }
    full_html = assemble_reading_html(json_payload, metadata)
    print(f"  [Success] Compiled SSOT Master Reading HTML via Jinja2 Engine for {session_id} - {lesson_id}")
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


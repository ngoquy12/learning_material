"""
core/renderers/reading/svg_guard.py
Guards and sanitizers for SVG Technical Diagrams and Mermaid Flowcharts.
"""

import re

def guard_svg_syntax(svg_str: str) -> str:
    """
    Guards and sanitizes SVG syntax:
    - Auto-injects xmlns if missing
    - Auto-injects class="rikkei-diagram"
    - Auto-injects Inter font family & marker styles
    - Fixes dark mode marker arrow contrast
    - Converts ALL CAPS text inside SVG to Title Case
    - Ensures viewBox exists
    - Wraps in container .diagram-wrap with adaptive styling
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
        
    # 8. Wrap in simple container div
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

    # 11. Ensure all <text...> tags are properly closed with </text>
    def sanitize_svg_text_tag(match):
        open_tag = match.group(1)
        body = match.group(2)
        close_tag = match.group(3) if match.group(3) else "</text>"
        clean_body = re.sub(r'</?(?:div|p|span|section|h[1-6])\b[^>]*>', '', body)
        return f"{open_tag}{clean_body}{close_tag}"

    svg_clean = re.sub(r'(<text\b[^>]*>)(.*?)(</text>|(?=<text\b|</svg>|$))', sanitize_svg_text_tag, svg_clean, flags=re.DOTALL | re.IGNORECASE)
    svg_clean = re.sub(r'\|\s*</tspan>', '</tspan>', svg_clean)
    return svg_clean

def sanitize_mermaid_code(code: str) -> str:
    """
    Sanitizes raw Mermaid diagram code to prevent 'Syntax error in text' in Mermaid JS.
    """
    if not code:
        return code

    lines = code.split("\n")
    cleaned_lines = []
    for line in lines:
        l = line
        
        # 1. Fix transition labels
        l = re.sub(r'(\b\w+|[}\]\)])\s*--\s+([^->\n|]+?)\s*--*\s*>\s*(\b\w+|[{\[\(])', r'\1 -->|\2| \3', l)
        
        # 2. Fix broken arrow with spaces before >
        l = re.sub(r'--+\s+>', '-->', l)
        l = re.sub(r'-\s+->', '-->', l)

        # 3. Clean up malformed parallelogram nodes
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
    """
    if not text or "mermaid" not in text.lower():
        return text

    def fix_md_mermaid(match):
        fence_start = match.group(1)
        code = match.group(2)
        fence_end = match.group(3)
        sanitized = sanitize_mermaid_code(code)
        return f"{fence_start}\n{sanitized}\n{fence_end}"

    text = re.sub(r'(```\s*mermaid[\r\n]+)(.*?)(```)', fix_md_mermaid, text, flags=re.DOTALL | re.IGNORECASE)

    def fix_html_mermaid(match):
        open_tag = match.group(1)
        code = match.group(2)
        close_tag = match.group(3)
        sanitized = sanitize_mermaid_code(code)
        return f"{open_tag}{sanitized}{close_tag}"

    text = re.sub(r'(<(?:pre|div)[^>]*class="[^"]*mermaid[^"]*"[^>]*>)(.*?)(</(?:pre|div)>)', fix_html_mermaid, text, flags=re.DOTALL | re.IGNORECASE)
    return text

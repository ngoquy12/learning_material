"""
core/renderers/reading/markdown_parser.py
Basic Markdown to HTML conversion and text normalization utilities for Reading Creator.
"""

import re
import html
import unicodedata

def ensure_sentence_ending_period(text: str) -> str:
    """Ensures text string ends with a proper punctuation mark (., ?, !, :, >)."""
    t = text.strip()
    if not t:
        return ""
    if t[-1] not in ('.', '?', '!', ':', '>', ';'):
        return t + '.'
    return t

def slugify_id(text: str) -> str:
    """
    Convert Vietnamese text into a clean kebab-case ID for robust TOC anchors.
    Example: '2.1. Cú pháp và cách dùng' -> 'sec-2-1-cu-phap-va-cach-dung'
    """
    if not text:
        return "sec-anchor"
    nfkd = unicodedata.normalize('NFKD', text)
    no_accent = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    clean = re.sub(r'[^a-zA-Z0-9]+', '-', no_accent.lower()).strip('-')
    return f"sec-{clean}" if clean else "sec-anchor"

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
        
    return "\n".join(html_lines)

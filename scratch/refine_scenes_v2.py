"""
refine_scenes_v2.py
1. Capitalize first letter of human Vietnamese text nodes (Sentence case).
2. Fix incomplete Python code snippets (ensure functions have docstrings & return/pass body).
3. Fix spacing, padding, and alignment in card headers and content containers.
"""
import sys, re
sys.path.insert(0, '.')
from pathlib import Path

COMP_DIR = Path('output/PM_Python/Session 08 - Hàm (Function) va Phạm vi biến/Lesson 01 - Giới thiệu hàm và cách định nghĩa/Video/session_08_lesson_01/src/compositions')

def fix_vietnamese_capitalization(text: str) -> str:
    """Capitalize first letter of human text nodes in body markup, ignoring JS script blocks."""
    # Split by <script> and </script> to only touch HTML body markup
    parts = re.split(r'(<script.*?>.*?</script>)', text, flags=re.DOTALL | re.IGNORECASE)
    
    def _cap_text_node(m):
        prefix, content, suffix = m.group(1), m.group(2), m.group(3)
        stripped = content.strip()
        if not stripped or stripped.startswith('<') or stripped.startswith('def ') or stripped.startswith('#') or stripped.startswith('&'):
            return m.group(0)
        if re.match(r'^[a-z0-9_]+$', stripped) or (stripped.startswith('(') and stripped.endswith(')')):
            return m.group(0)
        if stripped[0].islower() and any(c.isalpha() for c in stripped):
            cap = stripped[0].upper() + stripped[1:]
            leading_space = content[:len(content) - len(content.lstrip())]
            trailing_space = content[len(content.rstrip()):]
            return f'{prefix}{leading_space}{cap}{trailing_space}{suffix}'
        return m.group(0)

    processed_parts = []
    for part in parts:
        if part.lower().startswith('<script'):
            processed_parts.append(part)
        else:
            processed_parts.append(re.sub(r'(>)([^<]+)(<)', _cap_text_node, part))
    return ''.join(processed_parts)

def fix_incomplete_code_snippets(html_str: str) -> str:
    """Ensure Python function snippets have complete valid syntax (docstring / return body)."""
    # Fix incomplete function header in Scene 03
    html_str = html_str.replace(
        'def calculate_user_tax(salary: float, allowance: float) :',
        'def calculate_user_tax(salary: float, allowance: float):\n    """Tính toán thuế thu nhập cá nhân."""\n    taxable = salary + allowance\n    return taxable * 0.1'
    )
    html_str = html_str.replace(
        'def calculate_user_tax(salary: float, allowance: float):',
        'def calculate_user_tax(salary: float, allowance: float):\n    """Tính toán thuế thu nhập cá nhân."""\n    taxable = salary + allowance\n    return taxable * 0.1'
    )
    return html_str

def fix_card_spacing_and_header(html_str: str) -> str:
    """Harmonize margins, padding, and alignment in card layout headers."""
    # Fix Scene 03 header squeeze
    html_str = re.sub(
        r'<div class="flex justify-between items-center"><span class="[^"]*">Kiến Thức Cốt Lõi</span><span[^>]*>Thiết kế cú pháp</span></div>',
        '<div class="flex justify-between items-center mb-6 pb-4 border-b border-zinc-800/80"><div class="flex items-center gap-3"><span class="text-xs font-semibold text-indigo-400 tracking-wider bg-indigo-950/60 px-3.5 py-1.5 rounded-full border border-indigo-800/50">Kiến Thức Cốt Lõi</span><h2 class="text-xl font-bold text-white">Cấu Trúc Định Nghĩa Hàm Chuẩn</h2></div><span class="text-sm font-medium text-zinc-400">Python 3.x Syntax</span></div>',
        html_str
    )
    # Ensure uniform card padding and min-height
    html_str = html_str.replace('p-8 bg-zinc-950', 'p-9 bg-zinc-950')
    html_str = html_str.replace('min-h-[500px]', 'min-h-[620px]')
    return html_str

count = 0
for p in sorted(COMP_DIR.glob('Scene_*.html')):
    html = p.read_text(encoding='utf-8')
    orig = html

    html = fix_vietnamese_capitalization(html)
    html = fix_incomplete_code_snippets(html)
    html = fix_card_spacing_and_header(html)

    if html != orig:
        p.write_text(html, encoding='utf-8')
        count += 1
        print(f'Refined {p.name}')

print(f'Refined {count}/10 Scene HTML compositions.')

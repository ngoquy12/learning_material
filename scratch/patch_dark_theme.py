"""
patch_dark_theme.py
Rebuild mọi Scene_*.html trong project hiện tại bằng dark skeleton mới (Pure White Title & Bright Text, Enlarged Fonts).
Cải thiện độ tương phản và kích thước cho tất cả inline Tailwind markup.
"""
import sys, re
sys.path.insert(0, '.')
from pathlib import Path

SKELETON = Path('hyperframes/templates/light_theme_skeleton.html').read_text(encoding='utf-8')
PROJECT  = Path('output/PM_Python/Session 08 - Hàm (Function) va Phạm vi biến/Lesson 01 - Giới thiệu hàm và cách định nghĩa/Video/session_08_lesson_01')
COMP_DIR = PROJECT / 'src' / 'compositions'

def enhance_content_contrast(html_str: str) -> str:
    """Enhance font sizes and text colors in AI-generated inline HTML markup."""
    # Replace muted dark colors with bright high-contrast colors
    html_str = re.sub(r'\btext-zinc-400\b', 'text-zinc-100', html_str)
    html_str = re.sub(r'\btext-zinc-500\b', 'text-zinc-200', html_str)
    html_str = re.sub(r'\btext-slate-400\b', 'text-slate-100', html_str)
    html_str = re.sub(r'\btext-gray-400\b', 'text-gray-100', html_str)
    
    # Enlarge font sizes
    html_str = re.sub(r'\btext-xs\b', 'text-base font-medium', html_str)
    html_str = re.sub(r'\btext-sm\b', 'text-xl font-normal', html_str)
    html_str = re.sub(r'\btext-base\b', 'text-2xl', html_str)
    
    # Enlarge code snippets
    html_str = re.sub(r'\btext-xs\s+leading-relaxed\b', 'text-lg leading-relaxed', html_str)
    
    # Ensure white text for main headings
    html_str = re.sub(r'\btext-zinc-100\b', 'text-white font-bold', html_str)
    return html_str

fixed = 0
for p in sorted(COMP_DIR.glob('Scene_*.html')):
    old = p.read_text(encoding='utf-8')

    m_id    = re.search(r'id="scene-(\d+)"', old)
    m_slug  = re.search(r'window\.__timelines\["(scene-\d+)"\]', old)
    m_title = re.search(r'<h1 class="main-title">([^<]+)</h1>', old)
    m_dur   = re.search(r'data-duration="([\d.]+)"', old)
    m_content = re.search(r'<div class="content-box">\s*(.*?)\s*</div>\s*</div>\s*</div>\s*<script', old, re.DOTALL)

    if not all([m_id, m_slug, m_title, m_dur, m_content]):
        print(f'SKIP {p.name}')
        continue

    scene_n     = m_id.group(1)
    scene_slug  = m_slug.group(1)
    scene_title = m_title.group(1).strip()
    dur         = m_dur.group(1)
    clean_content = enhance_content_contrast(m_content.group(1).strip())

    new_html = (SKELETON
        .replace('{scene_n}',     scene_n)
        .replace('{scene_slug}',  scene_slug)
        .replace('{scene_title}', scene_title)
        .replace('{dur}',         dur)
        .replace('{clean_content}', clean_content)
    )

    p.write_text(new_html, encoding='utf-8')
    fixed += 1
    print(f'Patched high contrast: {p.name}')

print(f'\nTotal patched: {fixed}/10 scenes')

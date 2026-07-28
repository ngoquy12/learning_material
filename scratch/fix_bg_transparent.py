"""Fix background: transparent -> #f8fafc in all Scene HTML files for current project."""
import sys, re
sys.path.insert(0, '.')
from pathlib import Path

PROJECT = Path('output/PM_Python/Session 08 - Hàm (Function) va Phạm vi biến/Lesson 01 - Giới thiệu hàm và cách định nghĩa/Video/session_08_lesson_01')

fixed = 0
for p in sorted(PROJECT.rglob('*.html')):
    if p.name in ('index.html',):
        continue  # index.html handled separately
    html = p.read_text(encoding='utf-8')
    if 'background: transparent' in html:
        new_html = html.replace(
            'background: transparent;',
            'background: #f8fafc;'
        )
        p.write_text(new_html, encoding='utf-8')
        fixed += 1
        print(f'Fixed: {p.name}')

print(f'\nTotal fixed: {fixed} files')

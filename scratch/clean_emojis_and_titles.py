"""
clean_emojis_and_titles.py
1. Replace ALL raw text emojis with standard Phosphor Icons.
2. Clean redundant repeated titles in card headers when top title is already present.
"""
import sys, re
sys.path.insert(0, '.')
from pathlib import Path

COMP_DIR = Path('output/PM_Python/Session 08 - Hàm (Function) va Phạm vi biến/Lesson 01 - Giới thiệu hàm và cách định nghĩa/Video/session_08_lesson_01/src/compositions')

EMOJI_MAP = {
    '❌': '<i class="ph-bold ph-x-circle text-rose-500 text-2xl mr-1.5 align-middle"></i>',
    '✔': '<i class="ph-bold ph-check-circle text-emerald-400 text-2xl mr-1.5 align-middle"></i>',
    '✅': '<i class="ph-bold ph-check-circle text-emerald-400 text-2xl mr-1.5 align-middle"></i>',
    '⚠️': '<i class="ph-bold ph-warning text-amber-400 text-2xl mr-1.5 align-middle"></i>',
    '📌': '<i class="ph-bold ph-push-pin text-indigo-400 text-2xl mr-1.5 align-middle"></i>',
    '💡': '<i class="ph-bold ph-lightbulb text-amber-300 text-2xl mr-1.5 align-middle"></i>',
    '🚀': '<i class="ph-bold ph-rocket text-indigo-400 text-2xl mr-1.5 align-middle"></i>',
    '🔥': '<i class="ph-bold ph-fire text-rose-400 text-2xl mr-1.5 align-middle"></i>',
    '👉': '<i class="ph-bold ph-arrow-right text-indigo-400 text-2xl mr-1.5 align-middle"></i>',
    '⚡': '<i class="ph-bold ph-lightning text-amber-400 text-2xl mr-1.5 align-middle"></i>',
}

for p in sorted(COMP_DIR.glob('Scene_*.html')):
    html = p.read_text(encoding='utf-8')
    orig = html

    # 1. Replace raw emojis
    for char, phosphor_tag in EMOJI_MAP.items():
        html = html.replace(char, phosphor_tag)

    # 2. Clean redundant repeated titles in top card header bar
    # e.g. <h2 class="...">07 &bull; Lỗi biên dịch IndentationError</h2> inside card top flex bar
    # Replace redundant h2 repeating scene number + title with a simple badge or icon label
    html = re.sub(
        r'<h2[^>]*>\d+\s*&bull;\s*Lỗi biên dịch IndentationError</h2>',
        '<span class="text-xs font-semibold text-rose-400 tracking-wider bg-rose-950/50 px-3 py-1 rounded border border-rose-900/40">Thực Hành Cú Pháp</span>',
        html
    )

    # General pattern for repeating scene title header inside content card top flex bar
    html = re.sub(
        r'<h2 class="[^"]*uppercase[^"]*">\d+\s*&bull;\s*[^<]+</h2>',
        '<span class="text-xs font-semibold text-indigo-400 tracking-wider bg-indigo-950/50 px-3 py-1 rounded border border-indigo-900/40">Kiến Thức Cốt Lõi</span>',
        html
    )

    if html != orig:
        p.write_text(html, encoding='utf-8')
        print(f'Cleaned emojis/titles in {p.name}')
    else:
        print(f'No changes needed in {p.name}')

print('Emoji & redundant title cleaning complete.')

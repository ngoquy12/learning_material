"""
core/renderers/slide_renderer.py
Generic Presentation Slide HTML Renderer.
Takes a SlidePayloadSchema (JSON Payload) and compiles clean, responsive HTML presentation slides
without letting LLM write raw HTML strings directly.
"""

import json
from typing import Dict, Any, Union
from core.schemas.slide_schema import SlidePayloadSchema

def render_slide_html(payload: Union[SlidePayloadSchema, Dict[str, Any]]) -> str:
    """
    Renders clean presentation slides HTML from SlidePayloadSchema or dict payload.
    """
    if isinstance(payload, dict):
        payload = SlidePayloadSchema(**payload)
        
    slides_html_list = []
    
    for idx, scene in enumerate(payload.scenes, 1):
        bullets_html = ""
        if scene.bullets:
            items = "".join([f'<li class="mb-2 text-slate-700 dark:text-slate-300 flex items-start gap-2"><span class="text-red-600 font-bold">•</span><span>{b}</span></li>' for b in scene.bullets])
            bullets_html = f'<ul class="text-sm md:text-base list-none p-0 mt-3">{items}</ul>'
            
        mermaid_html = ""
        if scene.mermaid:
            mermaid_html = f'<div class="mermaid my-4 flex justify-center bg-slate-900 p-4 rounded-xl border border-slate-700">{scene.mermaid}</div>'
            
        slide_card = f"""
        <section class="slide-page bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 md:p-10 my-6 shadow-sm">
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3 mb-4">
                <span class="text-xs font-bold uppercase tracking-wider text-red-600 bg-red-50 dark:bg-red-950/30 px-3 py-1 rounded-full">Slide {idx:02d} / {len(payload.scenes):02d}</span>
                <span class="text-xs font-semibold text-slate-400">{scene.short_title}</span>
            </div>
            <h2 class="text-xl md:text-2xl font-extrabold text-slate-800 dark:text-slate-100 mb-3">{scene.scene_title}</h2>
            <div class="text-sm md:text-base text-slate-600 dark:text-slate-300 leading-relaxed mb-4">{scene.narration}</div>
            {bullets_html}
            {mermaid_html}
        </section>
        """
        slides_html_list.append(slide_card)
        
    all_slides = "\n".join(slides_html_list)
    
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{payload.lesson_title} - Bài Giảng Slide</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
        .slide-container {{ max-width: 900px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="slide-container">
        <header class="text-center py-6">
            <h1 class="text-3xl font-black text-red-500 mb-1">{payload.session_title}</h1>
            <p class="text-slate-400 font-medium">{payload.lesson_title}</p>
        </header>
        {all_slides}
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            if (window.mermaid) mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
        }});
    </script>
</body>
</html>"""

    return html

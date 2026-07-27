"""
core/renderers/reading_renderer.py
Generic HTML Reading Material Renderer.
Takes a ReadingPayloadSchema (JSON Payload) and compiles a clean, robust,
responsive HTML reading material without letting LLM write broken JS strings.
"""

import json
from typing import Dict, Any, Union
from core.schemas.reading_schema import ReadingPayloadSchema
from core.sandbox_adapter import render_sandbox_script_tag

def render_reading_html(payload: Union[ReadingPayloadSchema, Dict[str, Any]]) -> str:
    """
    Renders clean, robust HTML reading material from a ReadingPayloadSchema or dict payload.
    """
    if isinstance(payload, dict):
        payload = ReadingPayloadSchema(**payload)
        
    # 1. Dynamically delegate Sandbox Runner resolution to Sandbox Adapter (Zero hardcode)
    sandbox_script = render_sandbox_script_tag(payload.tech_stack)
        
    # 2. Serialize visualizer steps safely to JSON string
    vis_json = "[]"
    if payload.visualizer and payload.visualizer.steps:
        steps_data = [s.dict() for s in payload.visualizer.steps]
        vis_json = json.dumps(steps_data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{payload.lesson_title} - Bài đọc Học liệu</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    {sandbox_script}
    <style>
        :root {{ --primary: #be111c; --bg-body: #f8fafc; --text-main: #1e293b; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg-body); color: var(--text-main); line-height: 1.6; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .step {{ margin-bottom: 24px; padding: 20px; background: white; border-radius: 12px; border: 1px solid #e2e8f0; }}
        .badge {{ width: 32px; height: 32px; border-radius: 50%; background: #be111c; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-bottom: 12px; }}
        pre code {{ font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-2xl font-bold mb-6 text-slate-800">{payload.lesson_title}</h1>
        
        <!-- Step 1: Problem -->
        <div class="step">
            <div class="badge">1</div>
            <h2 class="text-lg font-bold mb-2 text-slate-700">Đặt Vấn Đề</h2>
            <div>{payload.problem_breakdown}</div>
        </div>

        <!-- Step 2: Internals -->
        <div class="step">
            <div class="badge">2</div>
            <h2 class="text-lg font-bold mb-2 text-slate-700">Phân Tích Bản Chất</h2>
            <div>{payload.deep_dive_internals}</div>
        </div>

        <!-- Step 3: Mermaid -->
        <div class="step">
            <div class="badge">3</div>
            <h2 class="text-lg font-bold mb-2 text-slate-700">Sơ Đồ Luồng Kiến Trúc</h2>
            <div class="mermaid">{payload.mermaid_diagram}</div>
        </div>

        <!-- Step 4: Code & Sandbox -->
        <div class="step">
            <div class="badge">4</div>
            <h2 class="text-lg font-bold mb-2 text-slate-700">Mã Nguồn Minh Họa & Live Sandbox</h2>
            <pre class="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto"><code>{payload.code_example}</code></pre>
        </div>

        <!-- Step 5: Gotchas -->
        <div class="step">
            <div class="badge">5</div>
            <h2 class="text-lg font-bold mb-2 text-slate-700">Tổng Kết & Lưu Ý</h2>
            <div>{payload.gotchas_and_summary}</div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            if (window.mermaid) mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
        }});
        
        const VISUALIZER_STEPS = {vis_json};
    </script>
</body>
</html>"""

    return html

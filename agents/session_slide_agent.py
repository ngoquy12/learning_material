# agents/session_slide_agent.py
import os
import re
from pathlib import Path
from typing import Dict, Any
from core.llm import call_llm
from core.skills import load_skill_content

def generate_session_slides(
    session_id: str,
    session_title: str,
    session_dir_path: str,
    tech_stack: str,
    previous_lessons_text: str
) -> str:
    """
    Session-Level Slide Agent:
    Tự động biên soạn Bộ Slide Bài giảng Master HTML cấp Session (Session-Level Master Slides)
    tổng hợp toàn bộ kiến thức của tất cả các bài học trong Session (15-20 slides cho 1.5 giờ giảng dạy).
    Lưu vào thư mục: Session XX/Bài giảng/slides.html
    """
    session_dir = Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    slides_dir = session_dir / "Bài giảng"
    slides_dir.mkdir(exist_ok=True)
    
    print(f"\n  ---> [Session Slide Agent] Đang tạo Slide Bài giảng Master Session: {session_id} - {session_title}...")
    
    system_prompt = f"""You are a Lead Master Presentation & HTML Slide Designer at Rikkei Education.
Your task is to author a complete SESSION-LEVEL MASTER HTML SLIDE PRESENTATION (15-20 slides) for a 1.5-hour lecture session.

MANDATORY SLIDE DESIGN DIRECTIVES:
1. Slide Count Bounds: Strictly 15 to 20 Slides for the entire Session.
2. Structure: 
   - You MUST ONLY return the inner sequence of `<div class="slide-wrapper" data-slide-index="X">...</div>` blocks. DO NOT output `<!DOCTYPE html>`, `<html>`, `<head>`, or `<body>`.
   - Your output will be injected directly into a pre-existing master layout template.
3. Slide 1 (Cover):
   - Format exactly like this:
     <div class="slide-wrapper" data-slide-index="0">
       <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-16 overflow-hidden">
         <!-- Add some decorative background elements if desired (e.g. Rikkei Red themes) -->
         <div class="flex-1 flex flex-col items-center justify-center relative z-10 text-center">
            <h1 class="text-6xl font-sans font-black text-rikkei-dark tracking-tight leading-tight uppercase slide-in-top">TITLE</h1>
            <p class="text-2xl text-slate-600 font-sans font-medium mt-6 tracking-wide slide-in-bottom">SUBTITLE</p>
         </div>
       </section>
     </div>
4. Slide 2 (Agenda):
   - Format: `<h2 class="text-4xl font-sans font-black text-rikkei-dark mb-10 flex items-center gap-4">NỘI DUNG BÀI HỌC</h2>`
5. Layout & Spacing:
   - Ensure the layout structures fill the page efficiently. Use `display: flex`, `flex-grow: 1`.
   - Keep `<section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-16 overflow-hidden">` as the outer tag for every slide.
6. 3-30-300 Typography Rule:
   - Body font size minimum 18px (e.g., `text-xl` or `text-2xl`), sub-bullets minimum 16px.
   - Max 3 main keypoints per slide, max 30 words per keypoint.
7. STRICT NO EMOJI DIRECTIVE: ABSOLUTELY FORBIDDEN to use text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶). Use CSS badges or Phosphor SVG symbols only (`<i class="ph-bold ph-check"></i>`).
8. Standard Code Fencing: Code snippets MUST be wrapped in `<pre class="bg-slate-900 rounded-xl p-6 overflow-hidden shadow-2xl relative"><code class="language-python text-emerald-400">...</code></pre>`.
9. Use Tailwind CSS extensively for all styling.
"""

    user_prompt = f"""Generate the HTML Slide blocks for Session:
Session ID: {session_id}
Session Title: {session_title}
Target Technology Stack: {tech_stack}

--- SESSION LESSONS & CURRICULUM SYLLABUS ---
{previous_lessons_text}

MANDATORY OUTPUT CONTRACT:
- Output ONLY the `<div class="slide-wrapper">...</div>` sequence.
- NO markdown wrappers like ```html or ``` around the output.
"""

    llm_html = call_llm(
        system_prompt,
        user_prompt,
        json_mode=False,
        agent_name="Session_Slide_Agent",
        session_id=session_id,
        lesson_id="SESSION_LEVEL"
    )
    
    if llm_html:
        llm_html = llm_html.strip()
        if llm_html.startswith("```html"):
            llm_html = llm_html[7:].strip()
        if llm_html.startswith("```"):
            llm_html = llm_html[3:].strip()
        if llm_html.endswith("```"):
            llm_html = llm_html[:-3].strip()
    else:
        llm_html = f"<div class='slide-wrapper'><section class='slide-card'><h1>{session_id}: {session_title}</h1></section></div>"
        
    template_path = Path("templates/slide_template.html")
    if template_path.exists():
        template_html = template_path.read_text(encoding="utf-8")
        final_html = template_html.replace("{{SLIDES_CONTENT}}", llm_html).replace("{{SESSION_TITLE}}", session_title)
    else:
        print("  [Warning] templates/slide_template.html not found, outputting raw blocks.")
        final_html = llm_html

    out_file = slides_dir / "slides.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"  [Success] Saved Session Master Slides: {out_file}")
    return final_html

# agents/session_slide_agent.py
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from agents.slide_generator_agent import slide_generator_agent

def generate_session_slides(
    session_id: str,
    session_title: str,
    session_dir_path: str,
    tech_stack: str,
    previous_lessons_text: str,
    lessons_data: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Session-Level Master Slide Agent:
    Compiles a complete 15-20 slide Master HTML & PPTX Presentation Deck for all lessons in a Session.
    Extracts every single sub-lesson in the session, generating 2-3 visual scenes per lesson.
    Saves to: Session XX/Bài giảng/slides.html and Session XX/Bài giảng/slides.pptx
    """
    session_dir = Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    slides_dir = session_dir / "Bài giảng"
    slides_dir.mkdir(exist_ok=True)
    
    print(f"\n  ---> [Session Slide Agent] Đang tạo Master Slide Deck cho Session: {session_id} - {session_title}...")
    
    # 1. Parse all lesson titles from previous_lessons_text if lessons_data not provided
    parsed_lessons = []
    if lessons_data and len(lessons_data) > 0:
        parsed_lessons = lessons_data
    else:
        # Regex search for lesson headers in previous_lessons_text
        raw_matches = re.findall(r'BÀI HỌC\s*(?:Lesson\s*\d+|Bài\s*\d+|\d+)?[\:\-]?\s*(.*?)(?=\n|$)', previous_lessons_text, re.IGNORECASE)
        if not raw_matches:
            raw_matches = re.findall(r'Lesson\s*\d+\s*[\:\-]?\s*(.*?)(?=\n|$)', previous_lessons_text, re.IGNORECASE)
        
        for idx, match in enumerate(raw_matches, 1):
            clean_t = match.strip()
            clean_t = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_t, flags=re.IGNORECASE).strip()
            if clean_t and clean_t not in [l.get("lesson_title") for l in parsed_lessons]:
                parsed_lessons.append({
                    "lesson_id": f"Lesson {idx:02d}",
                    "lesson_title": clean_t,
                    "summary_text": ""
                })

    # If no lessons parsed, fallback to session title
    if not parsed_lessons:
        parsed_lessons = [{
            "lesson_id": "Lesson 01",
            "lesson_title": session_title,
            "summary_text": previous_lessons_text[:300]
        }]

    # 2. Build 2-3 rich visual scenes FOR EACH LESSON in the Session
    is_cli_or_tooling = any(k in (session_title + " " + tech_stack).lower() for k in ["git", "vcs", "cli", "terminal", "bash", "docker", "agile", "scrum"])
    compiled_lessons_data = []

    # Ensure local slides/images directory exists
    images_dir = slides_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    from agents.creators.mindmap_creator import generate_image_api

    def create_local_slide_image(topic_title: str, l_num: int) -> str:
        """Generates AI technical image or SVG infographic saved to slides/images folder."""
        filename_png = f"slide_lesson_{l_num:02d}.png"
        filename_svg = f"slide_lesson_{l_num:02d}.svg"
        
        path_png = images_dir / filename_png
        path_svg = images_dir / filename_svg

        # Detailed 2D Flat Vector Technical Prompt
        prompt = (
            f"Clean 2D flat vector technical illustration of {topic_title} in enterprise IT software engineering, "
            f"corporate navy and slate gray color palette, soft emerald accent, minimalist infographics, high contrast light mode, no text emoji"
        )

        # 1. Try Gemini Imagen API
        if generate_image_api(prompt, path_png):
            return f"images/{filename_png}"

        # 2. Fallback: Generate 2D Flat Vector SVG Technical Infographic
        svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 576" width="100%" height="100%">
  <rect width="1024" height="576" fill="#0f172a" rx="16"/>
  <path d="M0 96h1024M0 192h1024M0 288h1024M0 384h1024M0 480h1024" stroke="#1e293b" stroke-width="1.5"/>
  <rect x="64" y="48" width="896" height="72" fill="#1e293b" rx="12" stroke="#334155" stroke-width="2"/>
  <text x="512" y="92" fill="#38bdf8" font-family="Segoe UI, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">{topic_title.upper()}</text>
  <rect x="64" y="152" width="420" height="360" fill="#1e293b" rx="12" stroke="#0284c7" stroke-width="2.5"/>
  <rect x="96" y="184" width="356" height="56" fill="#0f172a" rx="8" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="274" y="220" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="18" font-weight="600" text-anchor="middle">Kiến trúc hệ thống &amp; luồng dữ liệu</text>
  <rect x="96" y="270" width="356" height="56" fill="#0369a1" rx="8"/>
  <text x="274" y="306" fill="#ffffff" font-family="Segoe UI, sans-serif" font-size="18" font-weight="600" text-anchor="middle">Xử lý &amp; kiểm soát dữ liệu</text>
  <rect x="96" y="360" width="356" height="110" fill="#0f172a" rx="8" stroke="#10b981" stroke-width="2"/>
  <text x="274" y="405" fill="#34d399" font-family="Segoe UI, sans-serif" font-size="17" font-weight="bold" text-anchor="middle">Enterprise Ready</text>
  <text x="274" y="440" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14" text-anchor="middle">Tối ưu hiệu năng &amp; an toàn 100%</text>
  <rect x="540" y="152" width="420" height="360" fill="#1e293b" rx="12" stroke="#10b981" stroke-width="2.5"/>
  <circle cx="750" cy="240" r="48" fill="#065f46" stroke="#34d399" stroke-width="3"/>
  <text x="750" y="248" fill="#ffffff" font-family="Segoe UI, sans-serif" font-size="22" font-weight="bold" text-anchor="middle">IT Core</text>
  <rect x="572" y="320" width="356" height="152" fill="#0f172a" rx="8" stroke="#334155" stroke-width="1.5"/>
  <text x="596" y="356" fill="#38bdf8" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold">Quy chuẩn thực chiến:</text>
  <text x="596" y="392" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="15">• Tự động hóa quy trình hệ thống</text>
  <text x="596" y="424" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="15">• Chuẩn hóa kiến trúc doanh nghiệp</text>
  <text x="596" y="452" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="15">• Tuân thủ quy chuẩn kỹ thuật</text>
</svg>"""
        with open(path_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)
        return f"images/{filename_svg}"

    for l_idx, l_info in enumerate(parsed_lessons, 1):
        l_title = l_info.get("lesson_title") or f"Bài học {l_idx}"
        clean_lt = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', l_title, flags=re.IGNORECASE).strip()
        short_lt = " ".join(clean_lt.split()[:4]) if len(clean_lt.split()) > 4 else clean_lt
        
        # Generate local image for this lesson
        local_img_rel_path = create_local_slide_image(clean_lt, l_idx)

        # Build 3 rich visual scenes for this lesson
        scene_1 = {
            "action_title": "Bối cảnh dự án & vấn đề cần giải quyết",
            "scene_title": "Bối cảnh & vấn đề",
            "short_title": "Bối cảnh thực tế",
            "layout_type": "IMAGE_EXPLAINER",
            "image_url": local_img_rel_path,
            "image_caption": f"Hình {l_idx}.1: Bối cảnh quy trình thực tế của {short_lt}",
            "bullets": [
                f"Vấn đề thực tế: Hạn chế của quy trình thủ công khi làm việc với {short_lt}.",
                f"Giải pháp áp dụng: Tự động hóa và chuẩn hóa quy trình xử lý mã nguồn/dữ liệu."
            ]
        }
        
        scene_2 = {
            "action_title": "Sơ đồ kiến trúc & quy trình vận hành",
            "scene_title": "Sơ đồ kiến trúc",
            "short_title": "Sơ đồ kiến trúc",
            "layout_type": "VISUAL_MINDMAP",
            "mindmap_center": f"Kiến trúc hệ thống {short_lt}",
            "mindmap_branches": [
                {
                    "title": "Khái niệm cơ bản",
                    "icon": "ph-tree-structure",
                    "description": f"Bản chất nguyên lý và vai trò của {clean_lt}."
                },
                {
                    "title": "Luồng vận hành",
                    "icon": "ph-arrows-left-right",
                    "description": "Cơ chế xử lý dữ liệu và chuyển đổi trạng thái hệ thống."
                },
                {
                    "title": "Thực thi dự án",
                    "icon": "ph-terminal-window",
                    "description": "Các bước thực thi lệnh và mã nguồn chuẩn thực tế."
                },
                {
                    "title": "Kiểm thử & an toàn",
                    "icon": "ph-shield-check",
                    "description": "Quy trình kiểm tra và phòng tránh lỗi phát sinh."
                }
            ]
        }

        scene_3 = {
            "action_title": "Lỗi thường gặp & cách xử lý chuẩn",
            "scene_title": "Lỗi thường gặp & quy chuẩn",
            "short_title": "So sánh quy chuẩn",
            "layout_type": "COMPARISON",
            "bad_practice": {
                "title": f"Thao tác thủ công & bỏ qua ràng buộc",
                "code": "Bỏ qua các bước kiểm tra ràng buộc hoặc sử dụng tham số không an toàn.",
                "reason": "Dễ phát sinh lỗi sập hệ thống hoặc làm rò rỉ dữ liệu."
            },
            "good_practice": {
                "title": f"Chuẩn hóa & tự động hóa quy trình",
                "code": "Tuân thủ quy trình kiểm thử, logging và Conventional Standards.",
                "reason": "Tối ưu hóa năng suất làm việc và đảm bảo an toàn hệ thống."
            }
        }

        compiled_lessons_data.append({
            "lesson_id": f"Lesson {l_idx:02d}",
            "lesson_title": clean_lt,
            "scenes": [scene_1, scene_2, scene_3]
        })

    # 3. Generate Master HTML & PPTX Decks
    final_html = slide_generator_agent.generate_session_deck_html(
        session_title=session_title,
        module_name=tech_stack,
        lessons_data=compiled_lessons_data
    )

    pptx_bytes = slide_generator_agent.generate_deck_pptx(
        lesson_title=session_title,
        module_name=tech_stack,
        scenes=compiled_lessons_data[0]["scenes"],
        lessons_data=compiled_lessons_data
    )

    # Save HTML deck
    out_html_file = slides_dir / "slides.html"
    with open(out_html_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    # Save PPTX deck
    out_pptx_file = slides_dir / "slides.pptx"
    with open(out_pptx_file, "wb") as f:
        f.write(pptx_bytes)

    print(f"  [Success] Saved Master HTML Slides ({len(compiled_lessons_data)} lessons, {len(final_html)} bytes): {out_html_file}")
    print(f"  [Success] Saved Master PPTX Slides ({len(pptx_bytes)} bytes): {out_pptx_file}")
    return final_html


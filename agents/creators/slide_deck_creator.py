"""
agents/creators/slide_deck_creator.py
SlideDeckCreatorAgent: Constructs complete, branded PowerPoint Presentation (.pptx)
and Markdown Outline for a Session according to Create_Slide's 3-skill instructional standard.
"""

from __future__ import annotations
import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from core.llm import call_llm
from core.prompts import render_prompt
from core.domain_knowledge import get_domain_for_session
from agents.creators.common_utils import robust_json_parse
from core.renderers.pptx.slide_deck_builder import slide_deck_builder
from core.renderers.pptx.slide_validator import validate_pptx_file

class SlideDeckCreatorAgent:
    """
    Agent responsible for designing and building official Rikkei Education PowerPoint (.pptx)
    Slide Decks and accompanying instructor Outline for E-learning Video Lectures.
    """

    def generate_slide_deck(
        self,
        session_title: str,
        course_name: str,
        course_code: str = "",
        tech_stack: str = "JavaScript",
        lessons_data: Optional[List[Dict[str, Any]]] = None,
        target_dir: Optional[Union[str, Path]] = None,
        chosen_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the 3-skill instructional slide deck creation pipeline:
        1. Content Intake (Skill 1) & Pedagogical Structuring (Skill 2) via LLM.
        2. Generates outline_bai_giang.md.
        3. OOXML PPTX Build & Validation (Skill 3).
        """
        # 1. Determine Unified Domain Anchor
        domain_info = get_domain_for_session(session_title, session_title)
        domain = chosen_domain or domain_info.get("name_vi", "Hệ thống quản trị")

        # 2. Setup Target Directory
        if target_dir:
            out_dir = Path(target_dir)
        else:
            safe_course = course_name.replace(" ", "_").replace("/", "_")
            safe_session = re.sub(r'[^\w\s-]', '', session_title).strip()
            out_dir = Path("output/pms") / safe_course / safe_session / "Slide bài giảng"
            
        out_dir.mkdir(parents=True, exist_ok=True)
        session_root_dir = out_dir.parent

        # 3. Load Rich Lesson Content from Session directory if available
        lessons = lessons_data or self._load_session_lessons(session_root_dir)

        # 4. Render Prompt & Call LLM
        prompt = render_prompt(
            "slide_deck_creator.j2",
            session_title=session_title,
            course_name=course_name,
            course_code=course_code,
            tech_stack=tech_stack,
            chosen_domain=domain,
            lessons=lessons
        )

        system_prompt = (
            "You are an expert Instructional Designer and PowerPoint Architect for Rikkei Education E-Learning courses.\n"
            "Strictly follow Skill 1, Skill 2, and Skill 3 of Create_Slide guidelines.\n"
            "Always return valid JSON adhering strictly to the requested schema and 100% Accented Vietnamese."
        )
        try:
            llm_text = call_llm(
                system_prompt=system_prompt,
                user_prompt=prompt,
                json_mode=True,
                agent_name="SlideDeckCreatorAgent"
            )
            llm_response = robust_json_parse(llm_text)
        except Exception as e_llm:
            print(f"  [SlideDeckCreatorAgent Warning] LLM call failed ({e_llm}). Using fallback slide structure...")
            llm_response = None
        
        # Fallback if LLM JSON fails
        if not llm_response or not isinstance(llm_response, dict) or "slides" not in llm_response:
            llm_response = self._build_fallback_slides_data(session_title, course_name, tech_stack, domain, lessons)

        slides_data = llm_response.get("slides", [])

        # 5. Generate & Save Markdown Outline
        outline_md = self._render_markdown_outline(session_title, course_name, domain, tech_stack, slides_data)
        outline_file = out_dir / "outline_bai_giang.md"
        outline_file.write_text(outline_md, encoding="utf-8")

        # 6. Build PPTX File
        safe_name = re.sub(r'[^\w\s-]', '', session_title).strip().replace(" ", "_")
        pptx_filename = f"Slide_Bai_Giang_{safe_name}.pptx"
        output_pptx = out_dir / pptx_filename

        built_pptx_path = slide_deck_builder.build_deck_from_slides_data(
            slides_data=slides_data,
            output_pptx_path=output_pptx
        )

        # 7. Validate Quality
        val_result = validate_pptx_file(built_pptx_path)

        return {
            "status": "SUCCESS" if val_result.get("passed", True) else "WARNING",
            "pptx_path": str(built_pptx_path),
            "outline_path": str(outline_file),
            "total_slides": len(slides_data),
            "chosen_domain": domain,
            "validation": val_result
        }

    def _load_session_lessons(self, session_dir: Path) -> List[Dict[str, Any]]:
        """Scans session directory for Lesson folders and extracts reading content."""
        lessons = []
        if not session_dir.exists():
            return [
                {"title": "Tổng quan và Cú pháp cốt lõi", "content": "Khái niệm và cơ chế hoạt động."},
                {"title": "Kỹ thuật Thao tác & Xử lý Dữ liệu", "content": "Áp dụng thực tiễn trong hệ thống."},
                {"title": "Lỗi thường gặp & Tối ưu hóa", "content": "Cách phòng tránh lỗi và best practices."}
            ]

        lesson_dirs = sorted([d for d in session_dir.iterdir() if d.is_dir() and "Lesson" in d.name])
        for ld in lesson_dirs:
            l_title = ld.name
            reading_file = ld / "Bài đọc" / "reading.html"
            content_snippet = ""
            if reading_file.exists():
                try:
                    raw_html = reading_file.read_text(encoding="utf-8")
                    clean_text = re.sub(r'<[^>]+>', ' ', raw_html)
                    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                    content_snippet = clean_text[:2000]
                except Exception:
                    pass
            lessons.append({
                "title": l_title,
                "content": content_snippet or "Nội dung chi tiết bài học lý thuyết và thực hành."
            })

        if not lessons:
            lessons = [
                {"title": "Tổng quan và Cú pháp cốt lõi", "content": "Khái niệm và cơ chế hoạt động."},
                {"title": "Kỹ thuật Thao tác & Xử lý Dữ liệu", "content": "Áp dụng thực tiễn trong hệ thống."},
                {"title": "Lỗi thường gặp & Tối ưu hóa", "content": "Cách phòng tránh lỗi và best practices."}
            ]
        return lessons

    def _render_markdown_outline(
        self,
        session_title: str,
        course_name: str,
        domain: str,
        tech_stack: str,
        slides_data: List[Dict[str, Any]]
    ) -> str:
        """Renders instructor's slide-by-slide Markdown Outline and Teleprompter Guide."""
        lines = [
            f"# ĐỀ CƯƠNG BÀI GIẢNG SLIDE (OUTLINE & SPEAKER NOTES)",
            f"**Khóa học:** {course_name}  ",
            f"**Chủ đề Session:** {session_title}  ",
            f"**Ngữ cảnh Domain thống nhất:** {domain}  ",
            f"**Công nghệ:** {tech_stack}  ",
            f"**Tổng số slide:** {len(slides_data)} slides  ",
            f"\n---\n"
        ]

        for s in slides_data:
            s_num = s.get("slide_number", "?")
            s_type = s.get("type", "content")
            s_title = s.get("title", "")
            s_subtitle = s.get("subtitle", "")
            notes = s.get("speaker_notes", "")

            lines.append(f"## Slide {s_num:02d}: {s_title} [{s_type.upper()}]")
            if s_subtitle:
                lines.append(f"*Phụ đề:* {s_subtitle}\n")

            if s_type == "agenda":
                items = s.get("agenda_items", [])
                lines.append("**Nội dung Agenda:**")
                for it in items:
                    lines.append(f"- {it}")
            elif s_type == "objectives":
                lines.append("**Chuẩn đầu ra bài học:**")
                for g_idx, g in enumerate(s.get("goals", []), 1):
                    lines.append(f"{g_idx}. {g}")
            elif s_type == "code":
                lines.append("**Các ý chính:**")
                for b in s.get("bullets", []):
                    lines.append(f"- {b}")
                lines.append(f"\n**Code ({s.get('code_title', 'Mã nguồn')}):**")
                lines.append(f"```{tech_stack.lower()}\n{s.get('code_snippet', '')}\n```")
            elif s_type == "comparison":
                left = s.get("left_col", {})
                right = s.get("right_col", {})
                lines.append(f"### [Trái] {left.get('title', 'Cách tiếp cận A')}")
                if left.get('code'):
                    lines.append(f"```{tech_stack.lower()}\n{left['code']}\n```")
                for b in left.get('bullets', []):
                    lines.append(f"- {b}")
                lines.append(f"\n### [Phải] {right.get('title', 'Cách tiếp cận B')}")
                if right.get('code'):
                    lines.append(f"```{tech_stack.lower()}\n{right['code']}\n```")
                for b in right.get('bullets', []):
                    lines.append(f"- {b}")
            elif s_type == "grid4":
                for it in s.get("items", []):
                    lines.append(f"### {it.get('title', 'Thuật ngữ')}")
                    lines.append(f"- **Định nghĩa:** {it.get('desc', '')}")
                    if it.get('example'):
                        lines.append(f"- **Ví dụ:** `{it.get('example', '')}`")
            elif s_type == "cards":
                for c in s.get("cards", []):
                    lines.append(f"### {c.get('title', 'Thành phần')}")
                    for cb in c.get("bullets", []):
                        lines.append(f"- {cb}")
            elif s_type == "table":
                headers = s.get("table_headers", [])
                rows = s.get("table_rows", [])
                if headers:
                    lines.append("| " + " | ".join(headers) + " |")
                    lines.append("| " + " | ".join([":---"] * len(headers)) + " |")
                    for r in rows:
                        lines.append("| " + " | ".join(r) + " |")
            else:
                for b in s.get("bullets", []):
                    lines.append(f"- {b}")

            lines.append(f"\n> 🎙️ **Speaker Notes (Lời giảng E-learning):**\n> {notes}\n")
            lines.append("---\n")

        return "\n".join(lines)

    def _build_fallback_slides_data(
        self,
        session_title: str,
        course_name: str,
        tech_stack: str,
        domain: str,
        lessons: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Provides a safe, fully compliant fallback slide deck structure."""
        slides = [
            {
                "slide_number": 1,
                "type": "cover",
                "session_id": "Session",
                "title": session_title,
                "course_name": course_name,
                "speaker_notes": f"Chào mừng các bạn đến với bài giảng {session_title} thuộc khóa học {course_name}."
            },
            {
                "slide_number": 2,
                "type": "agenda",
                "title": "Nội Dung Bài Giảng",
                "agenda_items": [l.get("title", f"Nội dung {idx+1}") for idx, l in enumerate(lessons)] + ["Tổng kết & Thuật ngữ cốt lõi"],
                "speaker_notes": "Bài giảng hôm nay gồm các phần trọng tâm sau đây."
            },
            {
                "slide_number": 3,
                "type": "objectives",
                "title": "Mục tiêu bài học",
                "goals": [
                    "Hiểu rõ nguyên lý vận hành và cú pháp cốt lõi.",
                    f"Vận dụng thành thạo vào kịch bản hệ thống {domain}.",
                    "Kiểm soát các trường hợp biên và tối ưu hóa mã nguồn.",
                    "Tránh các lỗi lập trình phổ biến và nâng cao tư duy clean code."
                ],
                "speaker_notes": "Mục tiêu bài học giúp các bạn vừa vững lý thuyết vừa tự tin thực hành trên dự án."
            }
        ]

        cur_idx = 4
        for l_idx, l in enumerate(lessons, 1):
            slides.append({
                "slide_number": cur_idx,
                "type": "code",
                "title": f"{l_idx}. {l.get('title', 'Kiến thức cốt lõi')} — 1/2",
                "subtitle": f"Ứng dụng trong hệ thống {domain}",
                "bullets": [
                    "Nguyên lý vận hành cốt lõi",
                    "Cú pháp khai báo và thiết lập",
                    "Quy chuẩn đặt tên và clean code"
                ],
                "code_title": f"Mã nguồn {tech_stack}",
                "code_snippet": f"// Demo minh họa {domain}\nfunction executeTask() {{\n  console.log('Xử lý tác vụ {domain}...');\n  return true;\n}}",
                "speaker_notes": f"Chúng ta cùng tìm hiểu phần {l.get('title', '')} qua đoạn code mẫu trên màn hình."
            })
            cur_idx += 1

            slides.append({
                "slide_number": cur_idx,
                "type": "comparison",
                "title": f"{l_idx}. {l.get('title', 'Kiến thức cốt lõi')} — 2/2",
                "subtitle": "Phân tích tình huống & Thực tiễn triển khai",
                "left_col": {
                    "title": "Kịch bản Chuẩn",
                    "bullets": ["Dữ liệu hợp lệ", "Luồng xử lý tối ưu", "Thời gian phản hồi nhanh"]
                },
                "right_col": {
                    "title": "Xử lý Biên & Ngoại lệ",
                    "bullets": ["Dữ liệu rỗng hoặc null", "Bắt lỗi ngoại lệ chủ động", "Bảo vệ an toàn dữ liệu"]
                },
                "speaker_notes": "Lưu ý các trường hợp biên để phần mềm hoạt động ổn định nhất."
            })
            cur_idx += 1

        slides.append({
            "slide_number": cur_idx,
            "type": "grid4",
            "title": "Thuật Ngữ Cần Nhớ",
            "subtitle": "Các từ khóa kỹ thuật then chốt trong bài học",
            "items": [
                {"title": "1. Khái niệm cốt lõi", "desc": "Cơ chế nền tảng vận hành hệ thống.", "example": "CoreConcept"},
                {"title": "2. Cấu trúc dữ liệu", "desc": "Phương thức lưu trữ và tổ chức dữ liệu.", "example": "DataStructure"},
                {"title": "3. Phạm vi hoạt động", "desc": "Giới hạn truy cập và vòng đời tài nguyên.", "example": "ScopeBoundary"},
                {"title": "4. Tối ưu hiệu năng", "desc": "Giải pháp nâng cao tốc độ xử lý.", "example": "Optimization"}
            ],
            "speaker_notes": "Dưới đây là các thuật ngữ chuyên ngành các bạn cần ghi nhớ."
        })
        cur_idx += 1

        slides.append({
            "slide_number": cur_idx,
            "type": "closing",
            "title": "Chúc Các Bạn Học Tốt!",
            "message": "Hẹn gặp lại các bạn trong bài giảng tiếp theo.",
            "speaker_notes": "Cảm ơn các bạn đã chú ý theo dõi bài giảng hôm nay. Chúc các bạn học tập tốt!"
        })

        return {
            "session_title": session_title,
            "course_name": course_name,
            "chosen_domain": domain,
            "total_slides": len(slides),
            "slides": slides
        }

slide_deck_creator_agent = SlideDeckCreatorAgent()
slide_deck_creator = slide_deck_creator_agent

def generate_session_slide_deck(
    session_title: str,
    course_name: str,
    course_code: str = "",
    tech_stack: str = "JavaScript",
    lessons_data: Optional[List[Dict[str, Any]]] = None,
    target_dir: Optional[Union[str, Path]] = None,
    chosen_domain: Optional[str] = None
) -> Dict[str, Any]:
    """Helper function to run SlideDeckCreatorAgent on a session."""
    return slide_deck_creator_agent.generate_slide_deck(
        session_title=session_title,
        course_name=course_name,
        course_code=course_code,
        tech_stack=tech_stack,
        lessons_data=lessons_data,
        target_dir=target_dir,
        chosen_domain=chosen_domain
    )

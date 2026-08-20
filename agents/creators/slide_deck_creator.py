"""
agents/creators/slide_deck_creator.py

3-Stage Lecture Slide Deck Creation Pipeline (Ported & Synced with Create_Slide standards):
  Stage 1 — Content Intake (LLM, prompt: slide_deck_stage1.j2)
  Stage 2 — Slide Architecture (LLM, prompt: slide_deck_stage2.j2)
  Stage 3 — OOXML PPTX Build (NO LLM — core.renderers.pptx.deck_engine.build_deck())

Zero hard-coded content. 100% data-driven from session lessons and template.
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.renderers.pptx.deck_engine import build_deck
from core.sanitizers.json_recoverer import robust_json_parse
from core.llm import call_llm
from core.domain_knowledge import get_domain_blueprint
from agents.reviewers.slide_deck_reviewer import review_session_slide_deck

logger = logging.getLogger(__name__)


class DefaultLLMClient:
    """Default adapter wrapping core.llm.call_llm."""
    def complete(self, prompt: str) -> str:
        return call_llm(
            system_prompt="You are an expert presentation and pedagogical architect at Rikkei Education.",
            user_prompt=prompt,
            agent_name="slide_deck_creator"
        )


class SlideDeckCreatorAgent:
    """
    Orchestrates the 3-stage slide deck creation pipeline.
    """

    def __init__(
        self,
        llm_client=None,
        prompts_dir: Optional[Union[str, Path]] = None,
        template_pptx_path: Optional[Union[str, Path]] = None,
    ):
        self.llm = llm_client or DefaultLLMClient()
        
        if prompts_dir is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
            prompts_dir = base_dir / "templates" / "prompts"
        
        self.prompts_dir = Path(prompts_dir)
        self.tmpl_pptx = Path(template_pptx_path) if template_pptx_path else None
        self._jinja = Environment(
            loader=FileSystemLoader(str(self.prompts_dir)),
            autoescape=select_autoescape([]),
            keep_trailing_newline=True,
        )

    # ─────────────────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────────────────

    def generate_slide_deck(
        self,
        session_title: str,
        course_name: str,
        session_number: str,
        tech_stack: str,
        lessons: List[Dict[str, str]],
        output_path: Union[str, Path],
        domain_context: Optional[Dict] = None,
        **extra_context,
    ) -> Path:
        """
        Full 3-stage pipeline.

        Args:
            session_title   : e.g. "Tổ chức Hàm (Function), Tham số, Arrow Function và Phạm vi Scope"
            course_name     : e.g. "Phát triển ứng dụng Web"
            session_number  : e.g. "14"
            tech_stack      : e.g. "JavaScript"
            lessons         : [{"title": "...", "content": "..."}]
            output_path     : destination .pptx path
            domain_context  : optional business-domain blueprint (see core.domain_knowledge)
                              used to ground problem statements / illustrations in a relatable
                              real-world scenario (Skill 2 §8 domain-generality mapping).
        Returns:
            (Path to built .pptx file, review result dict from SlideDeckReviewerAgent)
        """
        output_path = Path(output_path)
        logger.info("[SlideDeckCreator] Starting 3-stage pipeline for: %s", session_title)

        # Stage 1: Content Intake
        logger.info("[SlideDeckCreator] Stage 1 — Content Intake...")
        intake: Dict = self._stage1_content_intake(
            session_title=session_title,
            course_name=course_name,
            session_number=session_number,
            tech_stack=tech_stack,
            lessons=lessons,
            domain_context=domain_context,
        )
        logger.info("[SlideDeckCreator] Stage 1 complete. knowledge_parts=%d", len(intake.get("knowledge_parts", [])))

        # Stage 2: Slide Architecture
        logger.info("[SlideDeckCreator] Stage 2 — Slide Architecture...")
        slides_data: List[Dict] = self._stage2_slide_architecture(
            intake=intake,
            session_number=session_number,
        )
        logger.info("[SlideDeckCreator] Stage 2 complete. slides=%d", len(slides_data))

        # Stage 3: OOXML Build (NO LLM)
        logger.info("[SlideDeckCreator] Stage 3 — OOXML Build...")
        pptx_path = self._stage3_build_pptx(
            slides_data=slides_data,
            output_path=output_path,
        )
        logger.info("[SlideDeckCreator] Done: %s", pptx_path)

        # Also output outline markdown
        outline_md_path = output_path.parent / "outline_bai_giang.md"
        self._write_outline_markdown(slides_data, outline_md_path, session_title)

        # Stage 4: Review — validate the generated deck against Create_Slide quality standard
        logger.info("[SlideDeckCreator] Stage 4 — Review...")
        review_result = review_session_slide_deck(
            slide_deck_dir=output_path.parent,
            session_title=session_title,
        )
        self._write_review_report(review_result, output_path.parent / "slide_deck_review_report.md")
        if review_result.get("status") != "PASSED":
            logger.warning(
                "[SlideDeckCreator] Review REJECTED (score=%s): %s",
                review_result.get("score"), review_result.get("errors"),
            )
        else:
            logger.info("[SlideDeckCreator] Review PASSED (score=%s).", review_result.get("score"))

        return pptx_path, review_result

    # ─────────────────────────────────────────────────────────────────────
    # Stage 1 — Content Intake (LLM)
    # ─────────────────────────────────────────────────────────────────────

    def _stage1_content_intake(
        self,
        session_title: str,
        course_name: str,
        session_number: str,
        tech_stack: str,
        lessons: List[Dict[str, str]],
        domain_context: Optional[Dict] = None,
    ) -> Dict:
        template = self._jinja.get_template("slide_deck_stage1.j2")
        prompt_text = template.render(
            session_title=session_title,
            course_name=course_name,
            session_number=session_number,
            tech_stack=tech_stack,
            domain_context=domain_context,
            lessons=lessons,
        )
        raw = self.llm.complete(prompt_text)
        return self._parse_json(raw, stage="Stage1-ContentIntake")

    # ─────────────────────────────────────────────────────────────────────
    # Stage 2 — Slide Architecture (LLM)
    # ─────────────────────────────────────────────────────────────────────

    def _stage2_slide_architecture(
        self,
        intake: Dict,
        session_number: str,
    ) -> List[Dict]:
        template = self._jinja.get_template("slide_deck_stage2.j2")
        intake_json = json.dumps(intake, ensure_ascii=False, indent=2)
        prompt_text = template.render(
            intake_json=intake_json,
            session_number=session_number,
        )
        raw = self.llm.complete(prompt_text)
        parsed = self._parse_json(raw, stage="Stage2-SlideArchitecture")

        if isinstance(parsed, dict):
            slides = parsed.get("slides", [])
        elif isinstance(parsed, list):
            slides = parsed
        else:
            slides = []

        if not slides:
            raise ValueError("[SlideDeckCreator] Stage 2 returned 0 slides.")

        return slides

    # ─────────────────────────────────────────────────────────────────────
    # Stage 3 — OOXML Build (NO LLM)
    # ─────────────────────────────────────────────────────────────────────

    def _stage3_build_pptx(
        self,
        slides_data: List[Dict],
        output_path: Path,
    ) -> Path:
        return build_deck(
            slides_data=slides_data,
            output_pptx_path=output_path,
            template_pptx_path=self.tmpl_pptx,
        )

    # ─────────────────────────────────────────────────────────────────────
    # Outline Markdown Generator
    # ─────────────────────────────────────────────────────────────────────

    def _write_outline_markdown(self, slides_data: List[Dict], outline_path: Path, session_title: str):
        lines = [
            f"# Outline Bài Giảng: {session_title}",
            "",
            f"**Tổng số slide:** {len(slides_data)}",
            "",
            "---",
            ""
        ]
        for s in slides_data:
            s_id = s.get("id", s.get("slide_number", ""))
            s_type = s.get("type", "")
            title = s.get("h1", s.get("title", ""))
            subtitle = s.get("h2", s.get("subtitle", ""))
            notes = s.get("notes", s.get("speaker_notes", ""))

            lines.append(f"### Slide {s_id}: [{s_type}] {title}")
            if subtitle:
                lines.append(f"*{subtitle}*")
            lines.append("")
            
            # Content summary
            if s_type == "agenda":
                for item in s.get("items", []):
                    lines.append(f"- {item}")
            elif s_type == "objectives":
                for g in s.get("goals", []):
                    lines.append(f"- [Mục tiêu] {g}")
            elif s_type == "comparison_2col":
                lines.append(f"**{s.get('left_title', '')}**")
                for item in s.get("left_items", []):
                    text = item.get("text", "") if isinstance(item, dict) else item
                    lines.append(f"- {text}")
                left_code = s.get("left_code", "")
                if left_code:
                    lines.append(f"```{s.get('lang_tag', '')}\n{left_code}\n```")
                lines.append(f"**{s.get('right_title', '')}**")
                for item in s.get("right_items", []):
                    text = item.get("text", "") if isinstance(item, dict) else item
                    lines.append(f"- {text}")
                right_code = s.get("right_code", "")
                if right_code:
                    lines.append(f"```{s.get('lang_tag', '')}\n{right_code}\n```")
            elif s_type in ("code_right_card", "code_trace_table"):
                lines.append(f"**Code Demo:** {s.get('code_title', '')}")
                code_snippet = s.get("code_snippet", "")
                if code_snippet:
                    lines.append(f"```{s.get('lang_tag', '')}\n{code_snippet}\n```")
                if s_type == "code_right_card":
                    if s.get("card_title"):
                        lines.append(f"**{s.get('card_title')}**")
                    for item in s.get("card_items", []):
                        text = item.get("text", "") if isinstance(item, dict) else item
                        lines.append(f"- {text}")
                else:
                    headers = s.get("table_headers", [])
                    if headers:
                        lines.append("| " + " | ".join(headers) + " |")
                        lines.append("|" + "---|" * len(headers))
                    for row in s.get("table_rows", []):
                        lines.append("| " + " | ".join(str(c) for c in row) + " |")
            elif s_type == "grid2x2":
                for it in s.get("items", []):
                    lines.append(f"- **{it.get('title', '')}:** {it.get('desc', '')}")
            elif s_type == "glossary_table":
                lines.append("| Thuật ngữ | Tiếng Anh | Định nghĩa |")
                lines.append("|---|---|---|")
                for r in s.get("rows", []):
                    if len(r) >= 3:
                        lines.append(f"| {r[0]} | {r[1]} | {r[2]} |")
            elif s_type == "summary_2col":
                left_title = s.get("left_title", "")
                right_title = s.get("right_title", "")
                if left_title:
                    lines.append(f"**{left_title}**")
                for item in s.get("left_items", []):
                    text = item.get("text", "") if isinstance(item, dict) else item
                    lines.append(f"- {text}")
                if right_title:
                    lines.append(f"**{right_title}**")
                for item in s.get("right_items", []):
                    text = item.get("text", "") if isinstance(item, dict) else item
                    lines.append(f"- {text}")
            elif s_type == "exercises":
                if s.get("exercises"):
                    lines.append("**Bài tập thực hành:**")
                    for item in s.get("exercises", []):
                        text = item.get("text", "") if isinstance(item, dict) else item
                        lines.append(f"- {text}")
                if s.get("references"):
                    lines.append("**Tài liệu tham khảo:**")
                    for item in s.get("references", []):
                        text = item.get("text", "") if isinstance(item, dict) else item
                        lines.append(f"- {text}")
            elif s_type == "interactive":
                lines.append(f"**Kiểu:** {s.get('pattern', '')}")
                if s.get("prompt"):
                    lines.append(f"**Câu hỏi:** {s.get('prompt')}")
                code_snippet = s.get("code_snippet", "")
                if code_snippet:
                    lines.append(f"```{s.get('lang_tag', '')}\n{code_snippet}\n```")
                for i, opt in enumerate(s.get("options", [])):
                    opt_text = re.sub(r'^\s*[A-Ha-h][.)]\s*', '', str(opt))
                    lines.append(f"- {chr(65+i)}. {opt_text}")
                if s.get("answer"):
                    lines.append(f"> 🔑 **Đáp án (giảng viên):** {s.get('answer')}")
            elif s_type == "flowchart":
                for node in s.get("nodes", []):
                    lines.append(f"- [{node.get('type', '')}] {node.get('text', '')}")
            elif s_type == "timeline":
                for m in s.get("milestones", []):
                    label = m.get("label", "") if isinstance(m, dict) else str(m)
                    desc = m.get("desc", "") if isinstance(m, dict) else ""
                    lines.append(f"- **{label}:** {desc}")

            if notes:
                lines.append("")
                lines.append(f"> 🎙️ **Speaker Notes:** {notes}")
            lines.append("")
            lines.append("---")
            lines.append("")

        outline_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("[SlideDeckCreator] Outline markdown written to: %s", outline_path)

    # ─────────────────────────────────────────────────────────────────────
    # Review Report Writer
    # ─────────────────────────────────────────────────────────────────────

    def _write_review_report(self, review_result: Dict, report_path: Path):
        lines = [
            "# 🎞️ Báo cáo Duyệt Slide Bài Giảng (SLIDE DECK REVIEW)",
            "",
            f"**Trạng thái:** `{review_result.get('status', 'UNKNOWN')}`",
            f"**Điểm:** {review_result.get('score', 0)}/100",
            f"**Tổng số slide:** {review_result.get('total_slides', 0)}",
            "",
        ]
        errors = review_result.get("errors", [])
        warnings = review_result.get("warnings", [])
        if errors:
            lines.append("## ❌ Lỗi")
            for e in errors:
                lines.append(f"- {e}")
            lines.append("")
        if warnings:
            lines.append("## ⚠️ Cảnh báo")
            for w in warnings:
                lines.append(f"- {w}")
            lines.append("")
        lines.append(f"**Nhận xét:** {review_result.get('feedback', '')}")
        report_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("[SlideDeckCreator] Review report written to: %s", report_path)

    # ─────────────────────────────────────────────────────────────────────
    # JSON Parsing Helper
    # ─────────────────────────────────────────────────────────────────────

    def _parse_json(self, raw: str, stage: str = "") -> Any:
        return robust_json_parse(raw)


def extract_text_from_html(html_content: str, max_chars: int = 10000) -> str:
    """Helper to extract clean plain text from lesson HTML reading."""
    soup = BeautifulSoup(html_content, "html.parser")
    for s in soup(["script", "style", "nav", "footer"]):
        s.extract()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_text = "\n".join(lines)
    if len(full_text) > max_chars:
        return full_text[:max_chars] + "\n...[truncated]..."
    return full_text


def generate_session_slide_deck(
    session_title: str,
    course_name: str,
    tech_stack: str,
    target_dir: Union[str, Path],
    session_dir: Optional[Union[str, Path]] = None,
    session_number: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to generate a complete slide deck for a session directory.
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    if not session_number:
        match = re.search(r"Session\s*(\d+)", session_title, re.IGNORECASE)
        session_number = match.group(1) if match else "01"

    # Deliberately short filename (not the full title) — session directories in this project
    # can already be long/deeply-nested (Vietnamese titles), and PowerPoint COM automation
    # (export_slide_images, see slide_validator.py) rejects any absolute path over 255 chars
    # with "Filename cannot exceed 255 characters". Embedding the whole title here was the
    # single biggest contributor to blowing that budget for no real benefit — the parent
    # session folder already carries the full title.
    output_pptx = target_dir / f"Slide_Bai_Giang_Session_{session_number}.pptx"

    lessons_data = []
    if session_dir:
        s_path = Path(session_dir)
        for item in sorted(s_path.iterdir()):
            if item.is_dir() and item.name.startswith("Lesson"):
                reading_file = item / "Bài đọc" / "reading.html"
                if reading_file.exists():
                    html_text = reading_file.read_text(encoding="utf-8")
                    extracted = extract_text_from_html(html_text)
                    lessons_data.append({
                        "title": item.name,
                        "content": extracted
                    })

    if not lessons_data:
        lessons_data = [
            {"title": session_title, "content": f"Nội dung trọng tâm về {session_title} trong môn học {course_name} ({tech_stack})."}
        ]

    chosen_domain = kwargs.get("chosen_domain")
    domain_context = get_domain_blueprint(chosen_domain) if chosen_domain else None

    agent = SlideDeckCreatorAgent()
    pptx_path, review_result = agent.generate_slide_deck(
        session_title=session_title,
        course_name=course_name,
        session_number=session_number,
        tech_stack=tech_stack,
        lessons=lessons_data,
        output_path=output_pptx,
        domain_context=domain_context,
    )

    outline_path = target_dir / "outline_bai_giang.md"

    return {
        "status": "SUCCESS" if review_result.get("status") == "PASSED" else "WARNING",
        "pptx_path": str(pptx_path),
        "outline_path": str(outline_path),
        "total_lessons": len(lessons_data),
        "review": review_result,
    }


# Singleton instance
slide_deck_creator = SlideDeckCreatorAgent()

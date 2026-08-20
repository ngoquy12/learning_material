# agents/session_mindmap_agent.py
import os
import re
from pathlib import Path
from typing import Dict, Any
from core.llm import call_llm
from core.skills import load_skill_content
from core.prompts import render_prompt
from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt
from agents.creators.common_utils import process_mindmap_images
from core.renderers.mindmap_exporter import parse_markmap_tree, validate_mindmap_structure, build_xmind_file

def _strip_outer_code_fence(text: str) -> str:
    """
    Robustly strips ONE outer ```lang ... ``` wrapper from LLM output, tolerating a malformed
    variant where the LLM emits the language tag on its own line instead of on the opening
    backtick line (e.g. "```\\nmarkdown\\n# Title..." instead of "```markdown\\n# Title...").
    The naive .startswith("```markdown") check used previously did not match that variant and
    left a stray "markdown"/"markmap" line corrupting the mindmap's H1 heading.
    """
    if not text:
        return text
    t = text.strip()
    m = re.match(r'^```[ \t]*([a-zA-Z0-9_-]*)[ \t]*\r?\n', t)
    if m:
        t = t[m.end():]
        if not m.group(1):
            m2 = re.match(r'^[ \t]*(markdown|markmap)[ \t]*\r?\n', t, flags=re.IGNORECASE)
            if m2:
                t = t[m2.end():]
    t = re.sub(r'\r?\n```[ \t]*$', '', t.rstrip())
    return t.strip()

def generate_session_mindmap(
    session_id: str,
    session_title: str,
    session_dir_path: str,
    tech_stack: str,
    previous_lessons_text: str,
    chosen_domain: str = "",
    forbidden_scope: str = "",
    allowed_scope: str = ""
) -> str:
    """
    Session-Level Mindmap Agent:
    Tự động biên soạn Sơ đồ tư duy Tổng hợp cấp Session (Session-Level Mindmap)
    bao quát toàn bộ kiến thức của các bài học trong Session.
    Lưu vào thư mục: Session XX/Mindmap/session_mindmap.md
    """
    session_dir = Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    mindmap_dir = session_dir / "Sơ đồ tư duy"
    if not mindmap_dir.exists() and (session_dir / "Mindmap").exists():
        mindmap_dir = session_dir / "Mindmap"
    mindmap_dir.mkdir(exist_ok=True)
    
    print(f"\n  ---> [Session Mindmap Agent] Đang tạo Sơ đồ Tư duy Tổng hợp Session: {session_id} - {session_title}...")
    
    image_skill = load_skill_content("image_prompt_standard")
    mindmap_skill = load_skill_content("session_mindmap_compiler")

    session_domain_data = get_domain_for_session(session_id, session_title, chosen_domain or "")
    active_domain = chosen_domain or session_domain_data.get("name_vi", "")
    domain_prompt_block = format_domain_rules_for_prompt(session_domain_data) if active_domain else ""

    system_prompt = render_prompt(
        "session_mindmap.j2",
        {
            "mindmap_skill": mindmap_skill,
            "image_skill": image_skill,
            "chosen_domain": active_domain,
            "domain_prompt_block": domain_prompt_block,
            "forbidden_scope": forbidden_scope,
            "allowed_scope": allowed_scope
        }
    )

    user_prompt = f"""Generate the Master Markmap Mindmap for Session:
Session ID: {session_id}
Session Title: {session_title}
Target Technology Stack: {tech_stack}

--- SESSION LESSONS & CURRICULUM SYLLABUS ---
{previous_lessons_text}

MANDATORY OUTPUT CONTRACT:
- Return ONLY a single Markdown code block: ` ```markmap ... ` ```.
- Target Output Language: All mindmap nodes and notes MUST be written in 100% Accented Vietnamese.
- The mindmap must be extremely concise, rich in technical depth but visually clean, with no long paragraphs.
- Level 1 Heading (#) MUST contain ONLY the clean content/topic title, stripping any prefixes like "{session_id} - " or "{session_id}: ". For example, if session is "Session 04 - Toán tử", the H1 MUST be "# Toán tử".
- Level 2 Headings (##) MUST represent the child lessons within this session, ending with a final "## Liên kết hệ thống" connection branch.
- Each Lesson branch MUST contain EXACTLY 4 sub-branches (###) — no more, no fewer. You MUST choose
  the most fitting short Vietnamese name (2-4 words) for each of the 4 sub-branches based on this
  specific lesson's actual content nature — DO NOT force the same 4 fixed labels onto every lesson.
  General guidance (adapt freely, these are illustrative, not mandatory strings):
  - For concept/syntax-heavy lessons: something like "khái niệm & vai trò", "cú pháp", "ví dụ minh
    họa", "lưu ý & sai sót thường gặp".
  - For flow/process/lifecycle lessons: something like "tổng quan quy trình", "các bước thực thi",
    "sơ đồ luồng xử lý", "điểm cần lưu ý".
  Whatever names are chosen, together the 4 sub-branches MUST still fully cover: (1) concept/purpose,
  (2) syntax or process mechanics, (3) a concrete runnable/traceable example, and (4) pitfalls or
  implementation notes — just expressed with names that fit the lesson, not a fixed template.
- The final "## Liên kết hệ thống" branch MUST summarize the logical dependency flow, input-process-output data mapping, and overall cross-lesson integration.
- ABSOLUTELY FORBIDDEN to include "Mục tiêu bài học", "Bài toán", or "Đặt tình huống" branches anywhere in the mindmap.
- ABSOLUTELY FORBIDDEN to use any text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶) anywhere in the mindmap content.
- STRICT KNOWLEDGE SCOPING: Only reference concepts within allowed taught lessons; do not leak unlearned future topics.
"""

    markmap_content = call_llm(
        system_prompt,
        user_prompt,
        json_mode=False,
        agent_name="Session_Mindmap_Agent",
        session_id=session_id,
        lesson_id="SESSION_LEVEL"
    )
    
    if markmap_content:
        markmap_content = _strip_outer_code_fence(markmap_content)
    else:
        markmap_content = f"# {session_title}\n## Tổng quan Session\n- Nội dung sơ đồ tư duy tổng hợp Session."

    # Post-process image prompts inside the mindmap and generate 2D flat vector diagrams
    state_mock = {
        "course_dir_name": session_dir.name,
        "technology_stack": tech_stack,
        "images_dir": session_dir / "images"
    }
    processed_content = process_mindmap_images(markmap_content, state_mock)

    # Ensure final output is clean Pure Markdown without outer code fences
    processed_content = _strip_outer_code_fence(processed_content)

    out_file = mindmap_dir / "mindmap.md" if (mindmap_dir.name == "Sơ đồ tư duy") else mindmap_dir / "session_mindmap.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(processed_content)

    print(f"  [Success] Saved Session Mindmap: {out_file}")

    # Structural audit (non-blocking) + XMind Workbook export
    tree = parse_markmap_tree(processed_content)
    issues = validate_mindmap_structure(tree)
    if issues:
        print(f"  [Mindmap Structure Audit] Cảnh báo cấu trúc: {'; '.join(issues)}")

    xmind_path = out_file.with_suffix(".xmind")
    if build_xmind_file(tree, xmind_path):
        print(f"  [Success] Saved XMind Workbook: {xmind_path}")

    return processed_content

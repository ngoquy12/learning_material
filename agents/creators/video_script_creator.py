import os
from core.state import AgentState, require_tech_stack
from core.llm import call_llm
from core.utils.text_sanitizer import strip_markdown_fence
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

from core.prompts import render_prompt
from core.skills import load_skill_content
from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt


def _load_system_prompt(
    tech_stack: str,
    session_id: str = "",
    session_title: str = "",
    chosen_domain: str = "",
    forbidden_scope: str = "",
    allowed_scope: str = ""
) -> str:
    """Loads system prompt from Jinja2 template via PromptManager."""
    session_domain_data = get_domain_for_session(session_id, session_title, chosen_domain or "")
    active_domain = chosen_domain or session_domain_data.get("name_vi", "")
    domain_prompt_block = format_domain_rules_for_prompt(session_domain_data) if active_domain else ""
    video_script_skill = load_skill_content("video_script_generator")
    return render_prompt("video_script_system.j2", {
        "tech_stack": tech_stack,
        "chosen_domain": active_domain,
        "domain_prompt_block": domain_prompt_block,
        "forbidden_scope": forbidden_scope,
        "allowed_scope": allowed_scope,
        "video_script_skill": video_script_skill
    })


def video_script_creator_agent(state: AgentState) -> AgentState:
    """
    Video Script Creator Agent:
    Soạn kịch bản quay video cấp Lesson (kết hợp lời thoại teleprompter + chú thích hình ảnh/hành
    động theo từng phân cảnh), neo theo skill `video_script_generator`, xuất Markdown lưu vào
    state['video_script_markdown'].
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    tech_stack = require_tech_stack(state, "video_script_creator_agent")

    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Ứng dụng Doanh Nghiệp"
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")

    print(f"\n[Video_Script_Agent] Soạn kịch bản quay video cho {session_id} - {lesson_id}: {lesson_title}")

    content = state.get("lesson_content")
    if not content:
        content = get_lesson_content(
            session_id=session_id,
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            lesson_details=lesson_details,
            expected_output=expected_output,
            attempt_num=1,
            core_ssot=core_ssot,
            state=state
        )

    problem_text = content.get("problem", "") if isinstance(content, dict) else ""
    analysis_text = content.get("analysis", "") if isinstance(content, dict) else ""
    solution_text = content.get("solution", "") if isinstance(content, dict) else ""
    example_text = content.get("example", "") if isinstance(content, dict) else ""
    summary_text = content.get("summary", "") if isinstance(content, dict) else ""

    full_article_context = f"{problem_text}\n\n{analysis_text}\n\n{solution_text}\n\n{example_text}\n\n{summary_text}".strip()

    chosen_domain = state.get("chosen_domain", "")
    forbidden_scope = state.get("forbidden_scope", "")
    allowed_scope = state.get("allowed_scope", "")

    system_prompt = _load_system_prompt(
        tech_stack,
        session_id=session_id,
        session_title=lesson_title,
        chosen_domain=chosen_domain,
        forbidden_scope=forbidden_scope,
        allowed_scope=allowed_scope
    )

    user_prompt = f"""Write the complete Video Shooting Script for:
- Session: {session_id}
- Lesson: {lesson_id} - {lesson_title}
- Target Tech Stack: {tech_stack}
- Expected Learning Outcome: {expected_output or 'N/A'}

=== LESSON READING ARTICLE CONTENT (source material to base narration on) ===
{full_article_context[:7000]}

Follow the exact SCRIPT.md structure and all mandatory rules from the skill specification in the
system prompt (3-part structure, mandatory opening/closing lines, scene breakdown with time range +
visual cue + narration, at least 1 code example, 3-15 minute duration)."""

    response_str = call_llm(
        system_prompt,
        user_prompt,
        json_mode=False,
        agent_name="Video_Script_Agent",
        session_id=session_id,
        lesson_id=lesson_id
    )

    if response_str and response_str.strip():
        video_script_markdown = strip_markdown_fence(response_str)
    else:
        video_script_markdown = (
            f"# Kịch bản Video: {lesson_title}\n\n"
            f"> **Lỗi:** Không thể sinh kịch bản video tự động cho bài học này.\n"
        )

    state["video_script_markdown"] = video_script_markdown
    log_agent_tokens("Video_Script_Agent", state, video_script_markdown)
    return state

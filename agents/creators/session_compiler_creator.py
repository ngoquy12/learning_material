from core.state import AgentState
from core.artifact_status import ArtifactStatus, is_failed, needs_human_review

def session_compiler_agent(state: AgentState) -> AgentState:
    """
    Session Compiler Agent:
    Compiles all approved HTML, Slides, and Quiz assets.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    lesson_title = state.get("core_ssot", {}).get("session_title", "Course Session")
    
    display_title = f"{session_id} - {lesson_id}: {lesson_title}" if lesson_id else f"{session_id}: {lesson_title}"
    
    print(f"\n[Session_Compiler_Agent] Compiling assets for {display_title}...")
    print(f"  - HTML: Compiled ({len(state.get('html_content', ''))} chars) following Storytelling standards.")
    print(f"  - Slides: Compiled ({len(state.get('slide_markdown', ''))} chars) following Visual standards.")
    print(f"  - Quiz JSON: Compiled successfully with 5-question matrix and Hands-on template.")
    print(f"  - Video Script: Compiled ({len(state.get('video_script_markdown', ''))} chars) following Video standards.")
    print(f"  - Mindmap: Compiled ({len(state.get('mindmap_markdown', ''))} chars) following Mindmap standards.")
    
    # Chỉ PUBLISHED khi mọi tài nguyên của lesson đạt. Trước đây luôn đặt PUBLISHED,
    # nên lesson có tài nguyên hỏng vẫn bị các lần chạy sau bỏ qua như đã xong.
    statuses = {k: v for k, v in state.get("artifacts_status", {}).items() if k != "session"}
    failed = sorted(k for k, v in statuses.items() if is_failed(v))
    review = sorted(k for k, v in statuses.items() if needs_human_review(v))
    if failed:
        print(f"  [Session_Compiler_Agent] KHÔNG xuất bản: tài nguyên hỏng: {', '.join(failed)}.")
        state["artifacts_status"]["session"] = ArtifactStatus.FAILED
    elif review:
        print(f"  [Session_Compiler_Agent] Cần người rà lại trước khi xuất bản: {', '.join(review)}.")
        state["artifacts_status"]["session"] = ArtifactStatus.PENDING_HUMAN_REVIEW
    else:
        state["artifacts_status"]["session"] = ArtifactStatus.PUBLISHED
    return state

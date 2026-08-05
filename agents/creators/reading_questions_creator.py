import json
from core.state import AgentState
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

def reading_questions_creator_agent(state: AgentState) -> AgentState:
    """
    Reading Questions Creator Agent:
    Extracts the self-test reading questions from the SSOT master content
    and formats them as a JSON object to be written to reading_questions.json.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    
    print(f"\n[Reading_Questions_Agent] Extracting Reading Questions for {session_id} {lesson_id}")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=core_ssot.get("expected_output", ""),
        attempt_num=1,
        core_ssot=core_ssot,
        state=state
    )
    
    self_test = content.get("self_test", [])
    
    # Save the output to state
    state["reading_questions_json"] = self_test
    
    log_agent_tokens("Reading_Questions_Agent", state, json.dumps(self_test, ensure_ascii=False))
    return state

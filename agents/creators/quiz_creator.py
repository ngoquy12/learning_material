import json
from core.state import AgentState
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

def quiz_agent(state: AgentState) -> AgentState:
    """
    Quiz Agent:
    Formulates 5-question lesson quiz strictly based on the matrix:
    - Q1: Definition/Syntax
    - Q2: Execution Flow
    - Q3: Code Reading
    - Q4: Compare/Contrast
    - Q5: Outcome prediction with trap
    And a Hands-on Lab based on standard template (Objectives, Description ordered list, Evaluation criteria).
    """
    session_id = state.get("session_id", "Session 01")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "quiz_agent")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    sandbox_logs = [log for log in state.get("review_logs", []) if log["source"] == "Sandbox_Agent"]
    attempt_num = len(sandbox_logs) + 1
    feedback = sandbox_logs[-1]["feedback"] if sandbox_logs else ""
    lesson_id = state.get("lesson_id", "")
    
    print(f"\n[Quiz_Lab_Agent] Formulating Quiz & Practical Lab for {session_id} {lesson_id} | Attempt: #{attempt_num}")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=attempt_num,
        core_ssot=core_ssot,
        feedback=feedback,
        state=state
    )
    lab = content.get("lab", {})
    lab_title = lab.get("title", "Luyện tập (Tùy chọn)")
    lab_objectives = lab.get("objectives", ["Nắm vững kiến thức nền tảng"])
    lab_steps = lab.get("steps", ["Xem lại tài liệu lý thuyết"])
    lab_checklist = lab.get("checklist", ["Hoàn thành câu hỏi trắc nghiệm"])
    
    inputs_text = f"Dự án/môi trường phát triển {tech_stack} hiện tại và tài nguyên khóa học."

    quiz_data = content.get("quiz", [])
    
    lab_data = {
        "title": lab_title,
        "objectives": lab_objectives,
        "description": {
            "inputs": inputs_text,
            "steps": lab_steps
        },
        "evaluation": {
            "checklist": lab_checklist
        }
    }

    state["quiz_json"] = quiz_data
    state["lab_json"] = lab_data
    log_agent_tokens("Quiz_Agent", state, json.dumps({"quiz": quiz_data, "lab": lab_data}, ensure_ascii=False))
    return state

from core.state import AgentState
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

def slide_agent(state: AgentState) -> AgentState:
    """
    Slide Agent (Rikkei Master Presentation Engine):
    Tự động thiết kế Slide bài giảng HTML 16:9 sắc nét, chuẩn mực sư phạm doanh nghiệp.
    Sử dụng 8 Golden Rules, Bento Grid, Card Color Coding, Mermaid Flowcharts & Code Boxes.
    Cố định 3 Slide nội dung giàu tri thức + 1 Cover Slide + 1 Agenda Slide per Lesson.
    """
    from agents.slide_generator_agent import slide_generator_agent

    session_id = state.get("session_id", "Session 01")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "slide_agent")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Python Doanh Nghiệp"
    lesson_details = core_ssot.get("lesson_details", "")
    
    acad_logs = [log for log in state.get("review_logs", []) if log["source"] == "Academic_Reviewer"]
    attempt_num = len(acad_logs) + 1
    feedback = acad_logs[-1]["feedback"] if acad_logs else ""
    
    print(f"\n[Slide_Agent] Generating Master HTML Slide Deck for {session_id} - {lesson_id}: {lesson_title} | Attempt: #{attempt_num}")
    
    content = state.get("lesson_content")
    if not content:
        content = get_lesson_content(
            session_id=session_id,
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            lesson_details=lesson_details,
            expected_output="",
            attempt_num=attempt_num,
            core_ssot=core_ssot,
            feedback=feedback,
            state=state
        )

    concepts = core_ssot.get("concepts", {})
    code_samples = core_ssot.get("code_samples", {})
    problem_desc = content.get("problem") or f"Thách thức thực tế trong phát triển phần mềm với {lesson_title}."
    analysis_desc = content.get("analysis") or f"Phân tích bản chất nguyên lý vận hành và kiến trúc của {lesson_title}."
    solution_desc = content.get("solution") or f"Giải pháp triển khai mã nguồn tối ưu chuẩn PEP 8 cho {lesson_title}."
    summary_desc = content.get("summary") or f"Tổng kết các điểm trọng tâm và lưu ý kỹ thuật cho {lesson_title}."

    concept_list = []
    if isinstance(concepts, dict):
        for cname, cdesc in concepts.items():
            concept_list.append(f"{cname}: {cdesc}")
    elif isinstance(concepts, list):
        concept_list = [str(c) for c in concepts]

    first_code = ""
    if isinstance(code_samples, dict) and code_samples:
        first_code = str(list(code_samples.values())[0])
    elif isinstance(code_samples, str) and code_samples:
        first_code = code_samples

    if not first_code or len(first_code) < 15:
        first_code = f"""# Mã nguồn thực chiến: {lesson_title}
def execute_demo():
    print("--- Thực thi module: {lesson_title} ---")
    status = True
    return status

if __name__ == "__main__":
    execute_demo()"""

    p_text1 = concept_list[0] if len(concept_list) > 0 else problem_desc
    p_text2 = concept_list[1] if len(concept_list) > 1 else analysis_desc

    slide_1_html = f"""
    <div class="cards-container-row">
        <div class="card-column-box card-error">
            <div class="column-title" style="color: #991b1b; font-weight: 800; font-size: 20px;">Thách Thức &amp; Bối Cảnh Doanh Nghiệp</div>
            <div class="inner-white-card">
                <h4>Hạn Chế Hệ Thống Cũ</h4>
                <p>{p_text1[:220]}</p>
            </div>
        </div>
        <div class="card-column-box card-success">
            <div class="column-title" style="color: #166534; font-weight: 800; font-size: 20px;">Giải Pháp Hiện Đại Chuẩn Doanh Nghiệp</div>
            <div class="inner-white-card">
                <h4>Đột Phá Năng Suất</h4>
                <p>{p_text2[:220]}</p>
            </div>
        </div>
    </div>
"""

    mermaid_diagram = f"""flowchart TD
    A[Yêu cầu nghiệp vụ {lesson_title}] --> B[Khởi tạo Module & Tham chiếu RAM]
    B --> C[Xử lý logic theo nguyên lý cốt lõi]
    C --> D[Kiểm tra an toàn Runtime]
    D --> E[Kết quả Console Output chuẩn]"""

    b_text1 = concept_list[2] if len(concept_list) > 2 else solution_desc
    b_text2 = summary_desc

    slide_3_html = f"""
    <div class="cards-container-row">
        <div class="card-column-box card-warning">
            <div class="column-title" style="color: #92400e; font-weight: 800; font-size: 20px;">Lưu Ý Kỹ Thuật &amp; Cảnh Báo Anti-Pattern</div>
            <div class="inner-white-card">
                <h4>Quy Chuẩn PEP 8 &amp; Tối Ưu Bộ Nhớ</h4>
                <p>{b_text1[:180]}</p>
            </div>
            <div class="inner-white-card">
                <h4>Cảnh Báo Lỗi Runtime</h4>
                <p>{b_text2[:180]}</p>
            </div>
        </div>
        <div class="card-column-box" style="background: transparent; padding: 0; display: flex; flex-direction: column;">
            <div class="academic-code-box">
                {first_code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}
            </div>
        </div>
    </div>
"""

    scenes = [
        {
            "action_title": "Đặt Vấn Đề & Bối Cảnh Thực Tế Doanh Nghiệp",
            "scene_title": "Đặt Vấn Đề & Bối Cảnh Thực Tế Doanh Nghiệp",
            "short_title": "Bối cảnh & Đặt vấn đề",
            "html_content": slide_1_html,
            "layout_type": "CUSTOM_RAW"
        },
        {
            "action_title": "Khái Niệm Cốt Lõi & Trực Quan Hóa Luồng Dữ Liệu",
            "scene_title": "Khái Niệm Cốt Lõi & Trực Quan Hóa Luồng Dữ Liệu",
            "short_title": "Khái niệm & Sơ đồ luồng",
            "mermaid": mermaid_diagram,
            "layout_type": "MERMAID_DIAGRAM"
        },
        {
            "action_title": "Mã Nguồn Thực Chiến & Cảnh Báo Bẫy Cú Pháp",
            "scene_title": "Mã Nguồn Thực Chiến & Cảnh Báo Bẫy Cú Pháp",
            "short_title": "Mã nguồn & Cảnh báo",
            "html_content": slide_3_html,
            "layout_type": "CUSTOM_RAW"
        }
    ]

    display_title = f"{session_id} - {lesson_id}: {lesson_title}" if lesson_id else f"{session_id}: {lesson_title}"
    slides_html = slide_generator_agent.generate_deck_html(
        lesson_title=display_title,
        module_name=tech_stack.upper(),
        scenes=scenes
    )

    state["slide_html"] = slides_html
    state["slide_markdown"] = slides_html
    log_agent_tokens("Slide_Agent", state, slides_html)
    return state

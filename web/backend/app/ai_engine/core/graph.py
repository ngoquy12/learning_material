# core/graph.py
from typing import Dict, Any
from antigravity import Workflow, parallel, component
from core.state import AgentState
from core.persistence import save_checkpoint
from agents import (
    objective_architect_agent, scheduler_agent, knowledge_base_agent,
    html_writer_agent, html_ux_reviewer,
    slide_agent, academic_reviewer,
    quiz_agent, sandbox_testing_agent,
    session_compiler_agent, video_script_agent, mindmap_agent,
    lessons_learned_agent, pm_reviewer_agent, objective_reviewer_agent
)

# Global flag to cancel running AI workflows
cancellation_requested = False

def save_state_checkpoint(state: AgentState):
    """Helper to save checkpoint with lesson-specific key if lesson_id is present."""
    global cancellation_requested
    if cancellation_requested:
        raise ValueError("Tác vụ đã bị hủy bởi người dùng.")
        
    session_id = state.get('session_id', 'default')
    lesson_id = state.get('lesson_id', '')
    course_prefix = ""
    course_dir = state.get("course_dir_name")
    if course_dir and not session_id.startswith(course_dir):
        course_prefix = f"{course_dir}_"
    key = f"{course_prefix}{session_id}_{lesson_id}".strip("_")
    save_checkpoint(key, state)

@component
def node_pm_review(state: AgentState) -> AgentState:
    """Giai đoạn 0: Review PM Input trước khi cho phép chạy"""
    if not state.get("pm_approved", False):
        import os
        full_curriculum = state.get("full_curriculum", state.get("pm_input"))
        report = pm_reviewer_agent(full_curriculum, state.get("technology_stack", "python/core"))
        
        course_dir_name = state.get("course_dir_name", "Unknown_Course")
        out_dir = os.path.join("output", course_dir_name)
        os.makedirs(out_dir, exist_ok=True)
        
        report_path = os.path.join(out_dir, "pm_review_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        raise ValueError(
            f"\n[CHỜ DUYỆT PM] Hệ thống đã đánh giá file PM và xuất báo cáo tại {report_path}.\n"
            f"Hãy xem báo cáo và điều chỉnh file PM. Sau khi PM đã duyệt, hãy truyền tham số pm_approved=True vào state để tiếp tục tiến trình!"
        )
    return state

@component
def node_init_objectives(state: AgentState) -> AgentState:
    """Giai đoạn 1: ID Agent thiết lập chuẩn đầu ra dựa trên PM (Có vòng lặp phản biện sư phạm)"""
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("objectives") == "Approved" and not state.get("force_rebuild", False):
            approved = True
            break
            
        previous_feedback = state.get("review_logs", [-1])[-1]["feedback"] if state.get("review_logs") and state["review_logs"][-1]["source"] == "Objective_Reviewer" else None
        state["learning_outcomes"] = objective_architect_agent(state["pm_input"], state.get("technology_stack", "python/core"), previous_feedback)
        
        review = objective_reviewer_agent(state["learning_outcomes"], state["pm_input"], state.get("technology_stack", "python/core"))
        
        if review["status"] == "APPROVED":
            state.setdefault("artifacts_status", {})["objectives"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state.setdefault("review_logs", []).append({"source": "Objective_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
            
    if not approved:
        raise ValueError(
            f"\n[LỖI SƯ PHẠM] Chuẩn đầu ra (Learning Outcomes) không đạt yêu cầu ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống DỪNG tiến hành để tránh sai sót. Hãy kiểm tra lại hệ thống Agent!"
        )
    return state

@component
def node_allocate_schedule(state: AgentState) -> AgentState:
    """Giai đoạn 2: Lập lịch và bóc tách cấu trúc thời gian của Session"""
    state["program_structure"] = scheduler_agent(state["learning_outcomes"], state["time_reference"], state.get("technology_stack", "python/core"))
    save_state_checkpoint(state)
    return state

@component
def node_lock_ssot(state: AgentState) -> AgentState:
    """Giai đoạn 3: Khóa dữ liệu gốc (SSOT) và ghi vào Persistence"""
    kb = knowledge_base_agent(state["program_structure"], state.get("technology_stack", "python/core"))
    
    # Merge existing core_ssot with kb
    state.setdefault("core_ssot", {}).update(kb)
    save_state_checkpoint(state)
    
    print(f"\n[SUCCESS] Đã thiết lập xong Lịch trình và Bản đồ Tri thức Gốc (SSOT)")
    return state

@component
def pipeline_html_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện (Critique Loop) tự động cho bài đọc HTML"""
    if "requested_parts" in state and "html" not in state["requested_parts"]:
        state["artifacts_status"]["html"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("html") == "Approved" and not state.get("force_rebuild", False):
            approved = True
            break
        state = html_writer_agent(state)
        review = html_ux_reviewer(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["html"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state["review_logs"].append({"source": "UX_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
    if not approved:
        raise ValueError(
            f"\n[XÁC NHẬN CẦN THIẾT TỪ PM] Giao diện/Nội dung Bài đọc không phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống DỪNG tiến hành để tránh sai sót. Hãy kiểm tra lại cấu trúc và bấm chạy lại khi đã điều chỉnh!"
        )
    return state

@component
def pipeline_slide_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện (Critique Loop) tự động cho Slide bài giảng"""
    if "requested_parts" in state and "slide" not in state["requested_parts"]:
        state["artifacts_status"]["slide"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("slide") == "Approved":
            approved = True
            break
        state = slide_agent(state)
        review = academic_reviewer(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["slide"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state["review_logs"].append({"source": "Academic_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
    if not approved:
        raise ValueError(
            f"\n[XÁC NHẬN CẦN THIẾT TỪ PM] Nội dung học thuật Slide không phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống DỪNG tiến hành để tránh sai sót. Hãy kiểm tra lại cấu trúc và bấm chạy lại khi đã điều chỉnh!"
        )
    return state

@component
def pipeline_quiz_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện cơ chế Sandbox cho cấu phần Quiz & Lab bài tập"""
    if "requested_parts" in state and "quiz" not in state["requested_parts"]:
        state["artifacts_status"]["quiz"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("quiz") == "Approved":
            approved = True
            break
        state = quiz_agent(state)
        review = sandbox_testing_agent(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["quiz"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state["review_logs"].append({"source": "Sandbox_Agent", "feedback": review["feedback"]})
            save_state_checkpoint(state)
    if not approved:
        raise ValueError(
            f"\n[XÁC NHẬN CẦN THIẾT TỪ PM] Đáp án Quiz/Code Sandbox không phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống DỪNG tiến hành để tránh sai sót. Hãy kiểm tra lại cấu trúc và bấm chạy lại khi đã điều chỉnh!"
        )
    return state

@component
def pipeline_video_script_production(state: AgentState) -> AgentState:
    """Tự động tạo kịch bản quay video cho bài giảng"""
    if "requested_parts" in state and "video" not in state["requested_parts"] and "video_script" not in state["requested_parts"]:
        state["artifacts_status"]["video_script"] = "Skipped"
        return state
    if state.get("artifacts_status", {}).get("video_script") == "Approved":
        return state
    state = video_script_agent(state)
    state["artifacts_status"]["video_script"] = "Approved"
    save_state_checkpoint(state)
    return state

@component
def pipeline_mindmap_production(state: AgentState) -> AgentState:
    """Tự động tạo sơ đồ tư duy (mindmap) cho bài giảng"""
    if "requested_parts" in state and "mindmap" not in state["requested_parts"]:
        state["artifacts_status"]["mindmap"] = "Skipped"
        return state
    if state.get("artifacts_status", {}).get("mindmap") == "Approved":
        return state
    state = mindmap_agent(state)
    state["artifacts_status"]["mindmap"] = "Approved"
    save_state_checkpoint(state)
    return state

@component
def session_compiler_node(state: AgentState) -> AgentState:
    """Node 7: Tiến hành thu gom dữ liệu, tự động tạo cấu trúc cây thư mục vật lý bằng thư viện os, ghi file bài đọc HTML, ghi file Slide Markdown và dùng subprocess.run để gọi lệnh Marp CLI biên dịch slide ra HTML, xuất tệp câu hỏi JSON sạch ra ổ đĩa tại thư mục dist/"""
    state = session_compiler_agent(state)
    
    import os
    import json
    import subprocess
    
    # Create dist folder
    os.makedirs("dist", exist_ok=True)
    
    # Write reading.html
    html_content = state.get("html_content", "")
    if html_content:
        with open(os.path.join("dist", "reading.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
            
    # Write slides.md
    slide_md = state.get("slide_markdown", "")
    if slide_md:
        slides_path = os.path.join("dist", "slides.md")
        with open(slides_path, "w", encoding="utf-8") as f:
            f.write(slide_md)
        # Call Marp CLI to compile slide markdown to HTML
        try:
            print("  [Compiler] Compiling slide.md to slide.html via Marp CLI...")
            result = subprocess.run(
                "npx --yes @marp-team/marp-cli --no-stdin dist/slides.md -o dist/slides.html",
                shell=True,
                capture_output=True,
                encoding="utf-8",
                timeout=10
            )
            if result.returncode == 0:
                print("  [Compiler] Marp compiled slides successfully.")
            else:
                print(f"  [Compiler] Marp CLI exited with error code {result.returncode}: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("  [Compiler] Marp CLI compilation timed out after 10 seconds.")
        except Exception as e:
            print(f"  [Compiler] Marp CLI execution failed: {e}")
            
    # Write quiz.json
    quiz_data = state.get("quiz_json", {})
    if quiz_data:
        with open(os.path.join("dist", "quiz.json"), "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)
            
    save_state_checkpoint(state)
    return state

@component
def lessons_learned_refiner(state: AgentState) -> AgentState:
    """Giai đoạn 5: Tự động đúc rút bài học kinh nghiệm từ review_logs và ghi nhận vào kho tri thức."""
    state = lessons_learned_agent(state)
    save_state_checkpoint(state)
    return state

def compile_learning_content_workflow():
    workflow = Workflow()

    # Khai báo các Node trục dọc trong hệ thống Antigravity
    workflow.add_node("pm_review", node_pm_review)
    workflow.add_node("init_objectives", node_init_objectives)
    workflow.add_node("allocate_schedule", node_allocate_schedule)
    workflow.add_node("lock_ssot", node_lock_ssot)

    @component
    def node_generate_master_content(state: AgentState) -> AgentState:
        """Giai đoạn 3.5: Sinh Master Content tuần tự để tối ưu cache"""
        from agents.creator_agents import get_lesson_content
        session_id = state.get("session_id", "Session 01")
        lesson_id = state.get("lesson_id", "")
        core_ssot = state.get("core_ssot", {})
        lesson_title = core_ssot.get("session_title", "Course Session")
        lesson_details = core_ssot.get("lesson_details", "")
        expected_output = core_ssot.get("expected_output", "")
        
        get_lesson_content(
            session_id=session_id,
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            lesson_details=lesson_details,
            expected_output=expected_output,
            attempt_num=1,
            core_ssot=core_ssot,
            state=state
        )
        return state

    workflow.add_node("generate_master_content", node_generate_master_content)

    # Khai báo các Node sáng tạo học liệu chạy tuần tự theo thứ tự ưu tiên & liên kết tri thức
    workflow.add_node("html_production", pipeline_html_production)
    workflow.add_node("slide_production", pipeline_slide_production)
    workflow.add_node("quiz_production", pipeline_quiz_production)
    workflow.add_node("video_script_production", pipeline_video_script_production)
    workflow.add_node("mindmap_production", pipeline_mindmap_production)

    workflow.add_node("final_compiler_and_publish", session_compiler_node)
    workflow.add_node("lessons_learned_refiner", lessons_learned_refiner)

    # Thiết lập đồ thị liên kết (Edges)
    workflow.set_entry_point("pm_review")
    workflow.add_edge("pm_review", "init_objectives")
    workflow.add_edge("init_objectives", "allocate_schedule")
    workflow.add_edge("allocate_schedule", "lock_ssot")
    workflow.add_edge("lock_ssot", "generate_master_content")
    
    # Chuỗi liên kết tuần tự ưu tiên
    workflow.add_edge("generate_master_content", "html_production")
    workflow.add_edge("html_production", "slide_production")
    workflow.add_edge("slide_production", "quiz_production")
    workflow.add_edge("quiz_production", "video_script_production")
    workflow.add_edge("video_script_production", "mindmap_production")
    workflow.add_edge("mindmap_production", "final_compiler_and_publish")
    
    workflow.add_edge("final_compiler_and_publish", "lessons_learned_refiner")

    return workflow.compile()
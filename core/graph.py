# core/graph.py
from typing import Dict, Any
from core.dag_engine import Workflow, parallel, component
from core.state import AgentState, DEFAULT_LESSON_PARTS
from core.persistence import save_checkpoint
from agents import (
    objective_architect_agent, scheduler_agent, knowledge_base_agent,
    html_writer_agent, html_ux_reviewer,
    quiz_agent, sandbox_testing_agent,
    session_compiler_agent,
    lessons_learned_agent, knowledge_memory_agent, get_relevant_memories_for_creator,
    pm_reviewer_agent, objective_reviewer_agent
)

def save_state_checkpoint(state: AgentState):
    """Helper to save checkpoint with lesson-specific key if lesson_id is present."""
    key = f"{state.get('session_id', 'default')}_{state.get('lesson_id', '')}".strip("_")
    save_checkpoint(key, state)

def write_state_artifacts_to_disk(state: AgentState):
    """Writes current generated artifacts in state to disk immediately."""
    from agents.creator_agents import get_lesson_dir
    from pathlib import Path
    import json
    
    try:
        lesson_dir = get_lesson_dir(state)
        requested_parts = state.get("requested_parts") if state.get("requested_parts") else DEFAULT_LESSON_PARTS
        
        # 1. HTML Reading
        if "html" in requested_parts and state.get("html_content"):
            html_sub = lesson_dir / "Bài đọc"
            html_sub.mkdir(parents=True, exist_ok=True)
            with open(html_sub / "reading.html", "w", encoding="utf-8") as f:
                f.write(state["html_content"])

                
        # 3. Quiz (Quizz lesson)
        if "quiz" in requested_parts and state.get("quiz_json"):
            quiz_sub = lesson_dir / "Quizz lesson"
            if not quiz_sub.exists() and (lesson_dir / "Câu hỏi Quizz").exists():
                quiz_sub = lesson_dir / "Câu hỏi Quizz"
            quiz_sub.mkdir(parents=True, exist_ok=True)
            with open(quiz_sub / "quiz.json", "w", encoding="utf-8") as f:
                json.dump(state["quiz_json"], f, ensure_ascii=False, indent=2)
                
            from core.quiz_excel import export_lesson_quiz_to_excel
            s_num_str = state.get("session_id", "").replace(" ", "")
            l_num_str = state.get("lesson_id", "").replace(" ", "")
            excel_filename = f"Quizz_{s_num_str}_{l_num_str}.xlsx"
            excel_path_file = quiz_sub / excel_filename
            quiz_data = state.get("quiz_json", {})
            if isinstance(quiz_data, dict):
                quiz_items = quiz_data.get("lesson_quiz") or quiz_data.get("quiz") or []
            else:
                quiz_items = quiz_data
                
            if quiz_items:
                export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                # 3.2 Practical Lab (Markdown)
        if state.get("practical_lab_markdown") or state.get("lab_json"):
            lab_sub = lesson_dir / "Bài thực hành"
            lab_sub.mkdir(parents=True, exist_ok=True)
            lab_md = state.get("practical_lab_markdown")
            if not lab_md and state.get("lab_json"):
                from agents.creators.practical_lab_creator import format_lab_to_markdown
                lab_md = format_lab_to_markdown(state["lab_json"])
            if lab_md:
                with open(lab_sub / "practical_lab.md", "w", encoding="utf-8") as f:
                    f.write(lab_md)
            lab_html = state.get("practical_lab_html")
            if not lab_html and state.get("lab_json"):
                from agents.creators.practical_lab_creator import format_lab_to_html
                from core.state import require_tech_stack
                current_stack = require_tech_stack(state, "write_state_artifacts_to_disk")
                lab_html = format_lab_to_html(state["lab_json"], current_stack)
            if lab_html:
                with open(lab_sub / "practical_lab.html", "w", encoding="utf-8") as f:
                    f.write(lab_html)
                

        # 3.5 Reading Questions (Markdown)
        if state.get("reading_questions_markdown") or state.get("reading_questions_json"):
            rq_sub = lesson_dir / "Câu hỏi bài đọc"
            rq_sub.mkdir(parents=True, exist_ok=True)
            rq_md = state.get("reading_questions_markdown")
            if not rq_md and state.get("reading_questions_json"):
                from agents.creators.reading_questions_creator import format_reading_questions_to_markdown
                rq_md = format_reading_questions_to_markdown(state["reading_questions_json"])
            if rq_md:
                with open(rq_sub / "reading_questions.md", "w", encoding="utf-8") as f:
                    f.write(rq_md)
    except Exception as e:
        print(f"  [Write Disk Warning] Failed to write artifacts to disk: {e}")


@component
def node_pm_review(state: AgentState) -> AgentState:
    """Giai đoạn 0: Review PM Input trước khi cho phép chạy"""
    if not state.get("pm_approved", False):
        import os
        from core.state import require_tech_stack
        full_curriculum = state.get("full_curriculum", state.get("pm_input"))
        report = pm_reviewer_agent(full_curriculum, require_tech_stack(state, "node_pm_review"))
        report_path = os.path.join("output", "pm_review_report.md")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        raise ValueError(
            f"\n[CHỜ DUYỆT PM] Hệ thống đã đánh giá file PM và xuất báo cáo tại {report_path}.\n"
            f"Hãy xem báo cáo và điều chỉnh file PM. Sau khi PM đã duyệt, hãy truyền tham số pm_approved=True vào state để tiếp tục tiến trình!"
        )
    return state

@component
def node_prerequisite_check(state: AgentState) -> AgentState:
    """
    Giai đoạn 0.5: Kiểm tra tính tuần tự tri thức (Prerequisite Guard)
    Phân tích toàn bộ curriculum, xây dựng dependency graph và phát hiện
    vi phạm tiên quyết trước khi tốn bất kỳ token nào sinh nội dung.
    BLOCKER violations → dừng pipeline và yêu cầu sửa PM.
    """
    import json
    import os

    # Chỉ chạy khi được yêu cầu hoặc ở lần đầu tiên của session
    if state.get("prerequisite_checked"):
        return state

    full_curriculum_str = state.get("full_curriculum", "[]")
    try:
        sessions = json.loads(full_curriculum_str)
    except Exception:
        sessions = []

    if not sessions:
        return state

    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "node_prerequisite_check")
    course_dir_name = state.get("course_dir_name", "Unknown_Course")
    report_path = os.path.join("output", course_dir_name, "prerequisite_report.md")

    from agents.prerequisite_guard_agent import run_prerequisite_check_for_pm
    is_valid, prereq_result = run_prerequisite_check_for_pm(
        sessions=sessions,
        tech_stack=tech_stack,
        output_report_path=report_path,
    )

    # Lưu dependency graph vào state để Obsidian Linker dùng sau
    state["prerequisite_data"] = prereq_result
    state["prerequisite_checked"] = True

    if not is_valid:
        blocker_count = prereq_result.get("stats", {}).get("blocker_count", 0)
        raise ValueError(
            f"\n[PM CHƯA ĐẠT CHUẨN TUẦN TỰ] PrerequisiteGuardAgent phát hiện {blocker_count} vi phạm BLOCKER.\n"
            f"Báo cáo chi tiết: {report_path}\n"
            f"Vui lòng sửa PM để đảm bảo tính tuần tự tri thức trước khi biên dịch học liệu!"
        )

    return state

def ensure_dynamic_scope_calculated(state: AgentState) -> AgentState:
    """Dynamically computes allowed_scope and forbidden_scope sets from syllabus tree and attaches to state."""
    if not state or not isinstance(state, dict):
        return state
    full_curriculum_str = state.get("full_curriculum", "")
    if full_curriculum_str:
        try:
            import json
            from core.scope_calculator import calculate_lesson_scope_contract
            sessions = json.loads(full_curriculum_str) if isinstance(full_curriculum_str, str) else full_curriculum_str
            syllabus_data = {"sessions": sessions}
            
            s_idx = 0
            l_idx = 0
            session_id_curr = state.get("session_id", "")
            lesson_id_curr = state.get("lesson_id", "")
            
            for i, s in enumerate(sessions):
                if s.get("session_id") == session_id_curr:
                    s_idx = i
                    for j, l in enumerate(s.get("lessons", [])):
                        if l.get("lesson_id") == lesson_id_curr or l.get("title") == lesson_id_curr or l.get("lesson_title") == lesson_id_curr:
                            l_idx = j
                            break
                    break
                    
            allowed, forbidden = calculate_lesson_scope_contract(syllabus_data, s_idx, l_idx)
            state["allowed_scope"] = list(allowed)
            state["forbidden_scope"] = list(forbidden)
            
            ssot = state.setdefault("core_ssot", {})
            if isinstance(ssot, dict):
                ssot["allowed_scope"] = ", ".join(allowed)
                ssot["forbidden_scope"] = ", ".join(forbidden)
        except Exception as e:
            print(f"  [Scope Calculator Warning] Failed to compute dynamic scope bounds: {e}")
    return state

@component
def node_init_objectives(state: AgentState) -> AgentState:
    """Giai đoạn 1: ID Agent thiết lập chuẩn đầu ra dựa trên PM (Có vòng lặp phản biện sư phạm)"""
    state = ensure_dynamic_scope_calculated(state)
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("objectives") == "Approved" and not state.get("force_rebuild", False):
            approved = True
            break
            
        from core.state import require_tech_stack
        tech_stack = require_tech_stack(state, "node_init_objectives")
        previous_feedback = state.get("review_logs", [-1])[-1]["feedback"] if state.get("review_logs") and state["review_logs"][-1]["source"] == "Objective_Reviewer" else ""
        state["learning_outcomes"] = objective_architect_agent(state["pm_input"], tech_stack, previous_feedback)
        
        review = objective_reviewer_agent(state["learning_outcomes"], state["pm_input"], tech_stack)
        
        if review["status"] == "APPROVED":
            state.setdefault("artifacts_status", {})["objectives"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state.setdefault("review_logs", []).append({"source": "Objective_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
            
    if not approved:
        last_fb = state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'
        raise ValueError(
            f"❌ [LỖI SƯ PHẠM NGHIÊM TRỌNG] Chuẩn đầu ra (Learning Outcomes) bị Reviewer từ chối sau 3 lần thử tại {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Chi tiết phản hồi: {last_fb}\n"
            f"Pipeline bị dừng theo quy tắc kiểm định nghiêm ngặt (Strict Reviewer Enforcement)."
        )
    return state

@component
def node_allocate_schedule(state: AgentState) -> AgentState:
    """Giai đoạn 2: Lập lịch và bóc tách cấu trúc thời gian của Session"""
    from core.state import require_tech_stack
    state["program_structure"] = scheduler_agent(state["learning_outcomes"], state["time_reference"], require_tech_stack(state, "node_allocate_schedule"))
    save_state_checkpoint(state)
    return state

@component
def node_lock_ssot(state: AgentState) -> AgentState:
    """Giai đoạn 3: Khóa dữ liệu gốc (SSOT) và ghi vào Persistence"""
    from core.state import require_tech_stack
    kb = knowledge_base_agent(state["program_structure"], require_tech_stack(state, "node_lock_ssot"))
    
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
            
        # Nếu đây là lần đầu chạy và đã nạp sẵn html_content từ đĩa (qua sync)
        # thì ưu tiên kiểm định trực tiếp nội dung trên đĩa trước
        if attempt == 0 and not state.get("force_rebuild", False) and state.get("html_content") and "Empty outline" not in state["html_content"] and "ĐANG KHỞI TẠO" not in state["html_content"]:
            print("  [HTML_Production] Phát hiện nội dung bài đọc từ đĩa. Đang kiểm định trực tiếp...")
            review = html_ux_reviewer(state)
            if review["status"] == "APPROVED":
                state["artifacts_status"]["html"] = "Approved"
                save_state_checkpoint(state)
                approved = True
                break
            else:
                state.setdefault("review_logs", []).append({
                    "source": "UX_Reviewer", 
                    "feedback": f"Bản trên đĩa chưa đạt chuẩn: {review['feedback']}"
                })
                save_state_checkpoint(state)
                # Tiếp tục vòng lặp để AI sinh/sửa đổi tự động
                continue

        state = html_writer_agent(state)
        # Ghi đĩa bản nháp HTML lập tức kể cả khi lỗi để người dùng sửa đổi/theo dõi
        write_state_artifacts_to_disk(state)
        
        review = html_ux_reviewer(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["html"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state.setdefault("review_logs", []).append({"source": "UX_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)

    # Ghi đĩa bản nháp HTML lập tức kể cả khi lỗi để người dùng sửa đổi
    write_state_artifacts_to_disk(state)

    if not approved:
        print(
            f"\n[CẢNH BÁO TỪ PM] Bài đọc HTML (reading.html) chưa đạt chuẩn kiểm duyệt ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi cuối: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và đánh dấu cần Review Thủ công (Pending Human Review) để tiếp tục tiến trình."
        )
        state["artifacts_status"]["html"] = "Pending Human Review"
        save_state_checkpoint(state)
    return state



def _is_session_01_orientation(state: AgentState) -> bool:
    """Check if current session is Session 01 Orientation."""
    session_str = str(state.get("session_id", "")).upper()
    lesson_type = str(state.get("lesson_type", "")).upper()
    core_ssot = state.get("core_ssot", {}) if isinstance(state.get("core_ssot"), dict) else {}
    lesson_title = str(core_ssot.get("session_title", "")).lower() + " " + str(state.get("lesson_id", "")).lower()
    return (
        "SESSION 01" in session_str
        or "ORIENTATION" in lesson_type
        or "tổng quan lộ trình" in lesson_title
        or "định hướng" in lesson_title
    )


@component
def pipeline_quiz_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện cơ chế Sandbox cho cấu phần Quiz & Lab bài tập"""
    if _is_session_01_orientation(state):
        print("  [Session 01 Orientation] SKIPPED Quiz generation (Only Reading, Slides, and Video Script allowed for Session 01).")
        state.setdefault("artifacts_status", {})["quiz"] = "Skipped (Session 01 Orientation)"
        return state

    if "requested_parts" in state and "quiz" not in state["requested_parts"]:
        state.setdefault("artifacts_status", {})["quiz"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("quiz") == "Approved":
            approved = True
            break
        state = quiz_agent(state)
        write_state_artifacts_to_disk(state)
        review = sandbox_testing_agent(state)
        if review["status"] == "APPROVED":
            state.setdefault("artifacts_status", {})["quiz"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state.setdefault("review_logs", []).append({"source": "Sandbox_Agent", "feedback": review["feedback"]})
            save_state_checkpoint(state)
    if not approved:
        print(
            f"\n[CẢNH BÁO TỪ PM] Đáp án Quiz/Code Sandbox chưa hoàn toàn phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và tiếp tục tiến hành với bản nháp tốt nhất."
        )
        state.setdefault("artifacts_status", {})["quiz"] = "Approved with Warnings"
        save_state_checkpoint(state)
    write_state_artifacts_to_disk(state)
    return state

@component
def pipeline_reading_questions_production(state: AgentState) -> AgentState:
    """Trích xuất câu hỏi bài đọc (reading questions) ra file JSON riêng biệt"""
    if _is_session_01_orientation(state):
        state.setdefault("artifacts_status", {})["reading_questions"] = "Skipped (Session 01 Orientation)"
        return state

    requested = state.get("requested_parts", ["all"])
    if "reading_questions" not in requested and "all" not in requested and "html" not in requested and "quiz" not in requested:
        state.setdefault("artifacts_status", {})["reading_questions"] = "Skipped"
        return state
    
    # Import inside function to avoid circular imports
    from agents.creator_agents import reading_questions_creator_agent
    state = reading_questions_creator_agent(state)
    state.setdefault("artifacts_status", {})["reading_questions"] = "Approved"
    write_state_artifacts_to_disk(state)
    save_state_checkpoint(state)
    return state


@component
def pipeline_practical_lab_production(state: AgentState) -> AgentState:
    """Tự động biên soạn nội dung Bài thực hành (Hands-on Practical Lab) ra file practical_lab.json"""
    if _is_session_01_orientation(state):
        print("  [Session 01 Orientation] SKIPPED Practical Lab / Homework generation for Session 01.")
        state.setdefault("artifacts_status", {})["practical_lab"] = "Skipped (Session 01 Orientation)"
        return state

    requested = state.get("requested_parts", ["all"])
    if "practical_lab" not in requested and "quiz" not in requested and "all" not in requested and "html" not in requested:
        state.setdefault("artifacts_status", {})["practical_lab"] = "Skipped"
        return state
        
    from agents.creator_agents import practical_lab_creator_agent
    state = practical_lab_creator_agent(state)
    state.setdefault("artifacts_status", {})["practical_lab"] = "Approved"
    write_state_artifacts_to_disk(state)
    save_state_checkpoint(state)
    return state




@component
def session_compiler_node(state: AgentState) -> AgentState:
    """Node 7: Tiến hành thu gom dữ liệu, biên dịch bài đọc và xuất tệp câu hỏi JSON sạch ra ổ đĩa tại thư mục dist/"""
    state = session_compiler_agent(state)
    
    import os
    import json
    
    # Create dist folder
    os.makedirs("dist", exist_ok=True)
    
    # Write reading.html
    html_content = state.get("html_content", "")
    if html_content:
        with open(os.path.join("dist", "reading.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
            
    # Write quiz.json
    quiz_data = state.get("quiz_json", {})
    if quiz_data:
        with open(os.path.join("dist", "quiz.json"), "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)
            
    save_state_checkpoint(state)
    return state

@component
def lessons_learned_refiner(state: AgentState) -> AgentState:
    """
    Giai đoạn cuối: Đúc rút kinh nghiệm từ review_logs.
    - Gọi knowledge_memory_agent (SQLite-backed, phân loại có cấu trúc)
    - Vẫn gọi lessons_learned_agent (Markdown SKILL.md) để tương thích ngược
    """
    # Kho tri thức có cấu trúc mới (SQLite)
    state = knowledge_memory_agent(state)
    # Kho tri thức cũ (Markdown) — tương thích ngược với loader cũ
    state = lessons_learned_agent(state)
    save_state_checkpoint(state)
    return state


def _merge_sub_state(state: Dict[str, Any], name: str, sub_state: Dict[str, Any]):
    """Helper to merge artifacts and statuses from a sub-state into main state."""
    if not isinstance(sub_state, dict):
        return
    if sub_state.get("html_content"):
        state["html_content"] = sub_state["html_content"]
    if sub_state.get("slide_markdown"):
        state["slide_markdown"] = sub_state["slide_markdown"]
    if sub_state.get("video_script_markdown"):
        state["video_script_markdown"] = sub_state["video_script_markdown"]
    if sub_state.get("quiz_json"):
        state["quiz_json"] = sub_state["quiz_json"]
    if sub_state.get("lab_json"):
        state["lab_json"] = sub_state["lab_json"]
    if sub_state.get("practical_lab_markdown"):
        state["practical_lab_markdown"] = sub_state["practical_lab_markdown"]
    # practical_lab_html trước đây bị BỎ SÓT ở đây dù có trong AgentState và STATE_REDUCERS:
    # nhánh song song PracticalLab sinh ra HTML rồi bị vứt bỏ lúc merge, sau đó
    # write_state_artifacts_to_disk phải render lại từ lab_json — tốn token LLM vô ích.
    if sub_state.get("practical_lab_html"):
        state["practical_lab_html"] = sub_state["practical_lab_html"]
    if sub_state.get("reading_questions_json"):
        state["reading_questions_json"] = sub_state["reading_questions_json"]
    if sub_state.get("reading_questions_markdown"):
        state["reading_questions_markdown"] = sub_state["reading_questions_markdown"]

    if "artifacts_status" in sub_state:
        state.setdefault("artifacts_status", {}).update(sub_state["artifacts_status"])
    if sub_state.get("review_logs"):
        for log in sub_state["review_logs"]:
            if log not in state.setdefault("review_logs", []):
                state["review_logs"].append(log)
    print(f"  ✓ [Parallel Engine] Nhánh dẫn xuất {name} hoàn tất.")



def compile_learning_content_workflow():
    workflow = Workflow()

    # Khai báo các Node trục dọc trong hệ thống Antigravity
    workflow.add_node("pm_review", node_pm_review)
    workflow.add_node("prerequisite_check", node_prerequisite_check)
    workflow.add_node("init_objectives", node_init_objectives)
    workflow.add_node("allocate_schedule", node_allocate_schedule)
    workflow.add_node("lock_ssot", node_lock_ssot)

    @component
    def node_generate_master_content(state: AgentState) -> AgentState:
        """Giai đoạn 3.5: Sinh Master Content tuần tự trước khi rẽ nhánh đa luồng để tránh lỗi Rate Limit và Cache Miss"""
        from agents.creator_agents import get_lesson_content, get_lesson_dir
        from pathlib import Path
        
        session_id = state.get("session_id", "Session 01")
        lesson_id = state.get("lesson_id", "")
        core_ssot = state.get("core_ssot", {})
        lesson_title = core_ssot.get("session_title", "Course Session")
        lesson_details = core_ssot.get("lesson_details", "")
        expected_output = core_ssot.get("expected_output", "")
        
        # Đồng bộ hóa Bài đọc HTML từ đĩa (nếu có và không rỗng)
        try:
            lesson_dir = get_lesson_dir(state)
            html_path = lesson_dir / "Bài đọc" / "reading.html"
            if not state.get("force_rebuild", False) and html_path.exists() and html_path.stat().st_size > 300:
                with open(html_path, "r", encoding="utf-8") as f:
                    disk_html = f.read()
                if "Empty outline" not in disk_html and "ĐANG KHỞI TẠO" not in disk_html:
                    # Chỉ nạp nếu nội dung trong state trống hoặc khác với đĩa
                    if not state.get("html_content") or state["html_content"] != disk_html:
                        print(f"  [Sync] Tự động nạp file reading.html từ đĩa: {html_path} ({len(disk_html)} ký tự)")
                        state["html_content"] = disk_html
                        # Đặt lại status của html thành Pending nếu nó chưa được duyệt Approved trong state cũ
                        if state.get("artifacts_status", {}).get("html") != "Approved":
                            state.setdefault("artifacts_status", {})["html"] = "Pending"
        except Exception as e:
            print(f"  [Sync Warning] Lỗi khi nạp bài đọc từ đĩa: {e}")

        # Tự động nạp kinh nghiệm (Lessons Learned) từ Knowledge Memory Agent vào Prompt
        try:
            from agents.knowledge_memory_agent import get_relevant_memories_for_creator
            from core.state import require_tech_stack
            current_stack = require_tech_stack(state, "node_generate_master_content")
            memories_context = get_relevant_memories_for_creator(
                tech_stack=current_stack,
                scope="all",
                query=lesson_title,
                limit=3
            )
            if memories_context:
                state["lessons_learned_prompt"] = memories_context
                print(f"  [Memory Engine] Đã nạp tri thức kinh nghiệm quá khứ cho {lesson_title}")
        except Exception as e:
            print(f"  [Memory Warning] Lỗi nạp memory kinh nghiệm: {e}")
        
        # Call get_lesson_content to trigger LLM and populate state["master_content"]
        # It handles its own caching if already generated.
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

    @component
    def node_html_first_production(state: AgentState) -> AgentState:
        """Đã chuyển sang chạy song song trong parallel_derived_production"""
        return state

    @component
    def node_generate_blueprint(state: AgentState) -> AgentState:
        """Giai đoạn 3.6: Sinh JSON Blueprint chứa kịch bản thống nhất trước khi chạy song song"""
        from agents.creator_agents import blueprint_creator_agent
        return blueprint_creator_agent(state)

    @component
    def node_parallel_derived_production(state: AgentState) -> AgentState:
        """
        Giai đoạn Parallel Derived Production:
        Cho phép 4 Creator Pipelines dẫn xuất (HTML Reading, Slide, Quiz, Lab, Questions)
        chạy song song sau khi Blueprint đã được sinh làm SSOT ngữ cảnh.
        """
        import copy
        import time
        import asyncio
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        print("\n[Parallel Engine] 🚀 Kích hoạt luồng sản xuất song song tất cả tài nguyên từ JSON Blueprint (HTML Reading, Quiz, Lab, ReadingQuestions)...")
        start_t = time.time()
        
        pipelines = [
            ("HTML", pipeline_html_production),
            ("Quiz", pipeline_quiz_production),
            ("PracticalLab", pipeline_practical_lab_production),
            ("ReadingQuestions", pipeline_reading_questions_production),
        ]
        
        async def _run_async_pipeline():
            async def _run_one(name, fn):
                state_copy = copy.deepcopy(state)
                res_state = await asyncio.to_thread(fn, state_copy)
                return name, res_state

            tasks = [_run_one(name, fn) for name, fn in pipelines]
            return await asyncio.gather(*tasks, return_exceptions=True)

        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                # Loop is already running, run with ThreadPoolExecutor
                futures_map = {}
                with ThreadPoolExecutor(max_workers=5) as executor:
                    for name, fn in pipelines:
                        state_copy = copy.deepcopy(state)
                        future = executor.submit(fn, state_copy)
                        futures_map[future] = name
                    for future in as_completed(futures_map):
                        name = futures_map[future]
                        sub_state = future.result()
                        _merge_sub_state(state, name, sub_state)
            else:
                results = asyncio.run(_run_async_pipeline())
                for res in results:
                    if isinstance(res, Exception):
                        print(f"  ❌ [Parallel Async Engine] Exception: {res}")
                        continue
                    name, sub_state = res
                    _merge_sub_state(state, name, sub_state)
        except Exception as err:
            print(f"  ⚠️ [Parallel Engine Fallback] Async execution fallback to ThreadPool: {err}")
            futures_map = {}
            with ThreadPoolExecutor(max_workers=5) as executor:
                for name, fn in pipelines:
                    state_copy = copy.deepcopy(state)
                    future = executor.submit(fn, state_copy)
                    futures_map[future] = name
                for future in as_completed(futures_map):
                    name = futures_map[future]
                    try:
                        sub_state = future.result()
                        _merge_sub_state(state, name, sub_state)
                    except Exception as e:
                        print(f"  ❌ [Parallel Engine] Nhánh dẫn xuất {name} lỗi: {e}")

        elapsed = time.time() - start_t
        print(f"[Parallel Engine] ✅ Tất cả tài nguyên đã hoàn tất song song trong {elapsed:.2f}s!\n")
        save_state_checkpoint(state)
        return state

    workflow.add_node("generate_master_content", node_generate_master_content)
    workflow.add_node("generate_blueprint", node_generate_blueprint)
    workflow.add_node("html_first_production", node_html_first_production)
    workflow.add_node("parallel_derived_production", node_parallel_derived_production)
    workflow.add_node("final_compiler_and_publish", session_compiler_node)
    workflow.add_node("lessons_learned_refiner", lessons_learned_refiner)

    # Thiết lập đồ thị liên kết (Edges)
    workflow.set_entry_point("pm_review")
    workflow.add_edge("pm_review", "prerequisite_check")
    workflow.add_edge("prerequisite_check", "init_objectives")
    workflow.add_edge("init_objectives", "allocate_schedule")
    workflow.add_edge("allocate_schedule", "lock_ssot")
    workflow.add_edge("lock_ssot", "generate_master_content")
    
    # Cấu trúc mới: generate_master_content -> generate_blueprint -> html_first_production (pass-through) -> parallel_derived_production (song song tất cả)
    workflow.add_edge("generate_master_content", "generate_blueprint")
    workflow.add_edge("generate_blueprint", "html_first_production")
    workflow.add_edge("html_first_production", "parallel_derived_production")
    workflow.add_edge("parallel_derived_production", "final_compiler_and_publish")
    workflow.add_edge("final_compiler_and_publish", "lessons_learned_refiner")

    return workflow.compile()
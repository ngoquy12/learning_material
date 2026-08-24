# core/graph.py
from pathlib import Path
from typing import Dict, Any, Optional
from core.dag_engine import Workflow, parallel, component, merge_branch_states
from core.state import AgentState, DEFAULT_LESSON_PARTS
from core.persistence import save_checkpoint
from core.artifact_status import ArtifactStatus, is_approved, skipped
from core.scope_gate import STATUS_SCOPE_WARNING, audit_artifact_scope, record_scope_audit
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

def write_state_artifacts_to_disk(
    state: AgentState,
    lesson_dir: Optional[Path] = None
) -> Dict[str, str]:
    """
    Ghi mọi artifact cấp lesson đang có trong state ra đĩa.

    ĐÂY LÀ ĐƯỜNG GHI ĐĨA DUY NHẤT cho artifact cấp lesson. Trước đây
    cli/commands/workflow_cmd.py tự viết lại toàn bộ logic này 3 lần (nhánh tuần tự,
    nhánh song song, nhánh session không có lesson con) — mỗi lần thêm một loại tài
    nguyên mới phải sửa 4 chỗ, và thực tế đã trôi khỏi nhau.

    Args:
        state: AgentState chứa các artifact đã sinh.
        lesson_dir: Thư mục lesson đích. Nếu None thì suy ra từ state qua get_lesson_dir().
            Caller nào đã tự tính thư mục (kèm tác dụng phụ đổi tên thư mục cho khớp
            tiêu đề mới) phải truyền vào đây, để không phụ thuộc vào việc 2 cách suy ra
            thư mục có trùng nhau hay không.

    Returns:
        Dict ánh xạ tên artifact -> đường dẫn đã ghi, hoặc "Skipped" nếu bỏ qua.
        Caller dùng kết quả này để dựng báo cáo, thay vì tự suy lại đường dẫn.
    """
    from agents.creator_agents import get_lesson_dir
    import json

    written: Dict[str, str] = {
        "html": "Skipped",
        "quiz": "Skipped",
        "practical_lab_md": "Skipped",
        "practical_lab_html": "Skipped",
        "reading_questions": "Skipped",
        "video_script": "Skipped",
    }

    try:
        if lesson_dir is None:
            lesson_dir = get_lesson_dir(state)
        lesson_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"  [Write Disk Warning] Không xác định được thư mục lesson: {e}")
        return written

    requested_parts = state.get("requested_parts") or DEFAULT_LESSON_PARTS

    # Mỗi artifact ghi trong try riêng: một artifact lỗi không được làm chết những
    # artifact còn lại. Trước đây cả khối nằm chung 1 try — chỉ cần lab thiếu
    # tech_stack là require_tech_stack raise, và video script phía sau im lặng
    # không bao giờ được ghi.

    # 1. Bài đọc HTML
    if "html" in requested_parts and state.get("html_content"):
        try:
            html_sub = lesson_dir / "Bài đọc"
            html_sub.mkdir(parents=True, exist_ok=True)
            html_path = html_sub / "reading.html"
            html_path.write_text(state["html_content"], encoding="utf-8")
            written["html"] = str(html_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi reading.html: {e}")

    # 2. Quizz (JSON + Excel)
    if "quiz" in requested_parts and state.get("quiz_json"):
        try:
            s_num_str = state.get("session_id", "").replace(" ", "")
            l_num_str = state.get("lesson_id", "").replace(" ", "")

            if l_num_str:
                quiz_sub = lesson_dir / "Quizz lesson"
                if not quiz_sub.exists() and (lesson_dir / "Câu hỏi Quizz").exists():
                    quiz_sub = lesson_dir / "Câu hỏi Quizz"
                excel_name = f"Quizz_{s_num_str}_{l_num_str}.xlsx"
            else:
                # Session không có lesson con: quiz thuộc về cả session (buổi thực hành),
                # nên đặt thẳng trong thư mục session và đặt tên theo buổi thay vì theo lesson.
                quiz_sub = lesson_dir / "Câu hỏi Quizz"
                excel_name = f"Quizz_{s_num_str}_Thuc_hanh.xlsx"

            quiz_sub.mkdir(parents=True, exist_ok=True)
            with open(quiz_sub / "quiz.json", "w", encoding="utf-8") as f:
                json.dump(state["quiz_json"], f, ensure_ascii=False, indent=2)
            written["quiz"] = str(quiz_sub / "quiz.json")

            from core.quiz_excel import export_lesson_quiz_to_excel
            excel_path_file = quiz_sub / excel_name

            quiz_data = state.get("quiz_json", {})
            if isinstance(quiz_data, dict):
                quiz_items = quiz_data.get("lesson_quiz") or quiz_data.get("quiz") or []
            else:
                quiz_items = quiz_data

            if quiz_items:
                export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                written["quiz"] = str(excel_path_file)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi quiz: {e}")

    # 3. Bài thực hành — Markdown và HTML tách riêng: dựng được cái nào ghi cái đó.
    # Gộp chung 1 try sẽ khiến lỗi khi dựng Markdown nuốt luôn bản HTML mà LLM đã sinh.
    if state.get("practical_lab_markdown") or state.get("lab_json"):
        lab_sub = lesson_dir / "Bài thực hành"

        try:
            lab_md = state.get("practical_lab_markdown")
            if not lab_md and state.get("lab_json"):
                from agents.creators.practical_lab_creator import format_lab_to_markdown
                lab_md = format_lab_to_markdown(state["lab_json"])
            if lab_md:
                lab_sub.mkdir(parents=True, exist_ok=True)
                lab_md_path = lab_sub / "practical_lab.md"
                lab_md_path.write_text(lab_md, encoding="utf-8")
                written["practical_lab_md"] = str(lab_md_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi practical_lab.md: {e}")

        try:
            lab_html = state.get("practical_lab_html")
            if not lab_html and state.get("lab_json"):
                from agents.creators.practical_lab_creator import format_lab_to_html
                from core.state import require_tech_stack
                # require_tech_stack cố ý raise thay vì fallback ngầm về "python":
                # bản cũ ở workflow_cmd đọc nhầm key "tech_stack" kèm fallback cứng
                # "python", khiến lab của mọi khoá JS bị chạy qua Pyodide và luôn lỗi.
                current_stack = require_tech_stack(state, "write_state_artifacts_to_disk")
                lab_html = format_lab_to_html(state["lab_json"], current_stack)
            if lab_html:
                lab_sub.mkdir(parents=True, exist_ok=True)
                lab_html_path = lab_sub / "practical_lab.html"
                lab_html_path.write_text(lab_html, encoding="utf-8")
                written["practical_lab_html"] = str(lab_html_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi practical_lab.html: {e}")

    # 4. Câu hỏi bài đọc
    if state.get("reading_questions_markdown") or state.get("reading_questions_json"):
        try:
            rq_sub = lesson_dir / "Câu hỏi bài đọc"
            rq_sub.mkdir(parents=True, exist_ok=True)
            rq_md = state.get("reading_questions_markdown")
            if not rq_md and state.get("reading_questions_json"):
                from agents.creators.reading_questions_creator import format_reading_questions_to_markdown
                rq_md = format_reading_questions_to_markdown(state["reading_questions_json"])
            if rq_md:
                rq_path = rq_sub / "reading_questions.md"
                rq_path.write_text(rq_md, encoding="utf-8")
                written["reading_questions"] = str(rq_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi câu hỏi bài đọc: {e}")

    # 5. Kịch bản video
    wants_video = "video" in requested_parts or "video_script" in requested_parts
    if wants_video and state.get("video_script_markdown"):
        try:
            video_sub = lesson_dir / "Video"
            video_sub.mkdir(parents=True, exist_ok=True)
            video_path = video_sub / "SCRIPT.md"
            video_path.write_text(state["video_script_markdown"], encoding="utf-8")
            written["video_script"] = str(video_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi kịch bản video: {e}")

    return written


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
        if is_approved(state.get("artifacts_status", {}).get("objectives")) and not state.get("force_rebuild", False):
            approved = True
            break
            
        from core.state import require_tech_stack
        tech_stack = require_tech_stack(state, "node_init_objectives")
        previous_feedback = state.get("review_logs", [-1])[-1]["feedback"] if state.get("review_logs") and state["review_logs"][-1]["source"] == "Objective_Reviewer" else ""
        state["learning_outcomes"] = objective_architect_agent(state["pm_input"], tech_stack, previous_feedback)
        
        review = objective_reviewer_agent(state["learning_outcomes"], state["pm_input"], tech_stack)
        
        if review["status"] == "APPROVED":
            state.setdefault("artifacts_status", {})["objectives"] = ArtifactStatus.APPROVED
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
        state["artifacts_status"]["html"] = ArtifactStatus.SKIPPED
        return state
    approved = False
    scope_audit = None
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if is_approved(state.get("artifacts_status", {}).get("html")) and not state.get("force_rebuild", False):
            approved = True
            break
            
        # Nếu đây là lần đầu chạy và đã nạp sẵn html_content từ đĩa (qua sync)
        # thì ưu tiên kiểm định trực tiếp nội dung trên đĩa trước
        if attempt == 0 and not state.get("force_rebuild", False) and state.get("html_content") and "Empty outline" not in state["html_content"] and "ĐANG KHỞI TẠO" not in state["html_content"]:
            print("  [HTML_Production] Phát hiện nội dung bài đọc từ đĩa. Đang kiểm định trực tiếp...")
            review = html_ux_reviewer(state)
            if review["status"] == "APPROVED":
                state["artifacts_status"]["html"] = ArtifactStatus.APPROVED
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
            # Đạt chuẩn trình bày vẫn chưa đủ: bài đọc còn phải nằm đúng phạm vi kiến
            # thức đã dạy và đúng bối cảnh nghiệp vụ của session. Trước đây phần kiểm
            # định này chỉ in cảnh báo rồi vẫn xuất bản như thường.
            audit = audit_artifact_scope(state.get("html_content", ""), state, "html")
            if audit.is_clean:
                state["artifacts_status"]["html"] = ArtifactStatus.APPROVED
                save_state_checkpoint(state)
                approved = True
                break

            record_scope_audit(state, audit)
            scope_audit = audit
            save_state_checkpoint(state)
        else:
            state.setdefault("review_logs", []).append({"source": "UX_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)

    # Ghi đĩa bản nháp HTML lập tức kể cả khi lỗi để người dùng sửa đổi
    write_state_artifacts_to_disk(state)

    if not approved:
        # Phân biệt 2 loại hỏng: sai phạm vi kiến thức (nội dung sai về sư phạm) khác
        # với chưa đạt chuẩn trình bày. Gộp chung một nhãn sẽ giấu mất loại nghiêm trọng hơn.
        if scope_audit is not None and not scope_audit.is_clean:
            print(
                f"\n[CẢNH BÁO PHẠM VI] Bài đọc ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')} "
                f"vẫn vi phạm phạm vi kiến thức sau {3} lần sinh lại.\n"
                f"Chi tiết: {scope_audit.as_feedback()}\n"
                f"Hệ thống xuất bản bản tốt nhất và đánh dấu CẦN NGƯỜI RÀ LẠI."
            )
            state["artifacts_status"]["html"] = STATUS_SCOPE_WARNING
        else:
            print(
                f"\n[CẢNH BÁO TỪ PM] Bài đọc HTML (reading.html) chưa đạt chuẩn kiểm duyệt ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
                f"Phản hồi cuối: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
                f"Hệ thống BỎ QUA LỖI và đánh dấu cần Review Thủ công (Pending Human Review) để tiếp tục tiến trình."
            )
            state["artifacts_status"]["html"] = ArtifactStatus.PENDING_HUMAN_REVIEW
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
        state.setdefault("artifacts_status", {})["quiz"] = skipped("Session 01 Orientation")
        return state

    if "requested_parts" in state and "quiz" not in state["requested_parts"]:
        state.setdefault("artifacts_status", {})["quiz"] = ArtifactStatus.SKIPPED
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if is_approved(state.get("artifacts_status", {}).get("quiz")):
            approved = True
            break
        state = quiz_agent(state)
        write_state_artifacts_to_disk(state)
        review = sandbox_testing_agent(state)
        if review["status"] == "APPROVED":
            state.setdefault("artifacts_status", {})["quiz"] = ArtifactStatus.APPROVED
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
        state.setdefault("artifacts_status", {})["quiz"] = ArtifactStatus.APPROVED_WITH_WARNINGS
        save_state_checkpoint(state)
    write_state_artifacts_to_disk(state)
    return state

@component
def pipeline_reading_questions_production(state: AgentState) -> AgentState:
    """Trích xuất câu hỏi bài đọc (reading questions) ra file JSON riêng biệt"""
    if _is_session_01_orientation(state):
        state.setdefault("artifacts_status", {})["reading_questions"] = skipped("Session 01 Orientation")
        return state

    requested = state.get("requested_parts", ["all"])
    if "reading_questions" not in requested and "all" not in requested and "html" not in requested and "quiz" not in requested:
        state.setdefault("artifacts_status", {})["reading_questions"] = ArtifactStatus.SKIPPED
        return state
    
    # Import inside function to avoid circular imports
    from agents.creator_agents import reading_questions_creator_agent
    state = reading_questions_creator_agent(state)
    state.setdefault("artifacts_status", {})["reading_questions"] = ArtifactStatus.APPROVED
    write_state_artifacts_to_disk(state)
    save_state_checkpoint(state)
    return state


@component
def pipeline_video_script_production(state: AgentState) -> AgentState:
    """Soạn kịch bản quay video (video script) cấp Lesson ra file Markdown riêng biệt"""
    if _is_session_01_orientation(state):
        state.setdefault("artifacts_status", {})["video_script"] = skipped("Session 01 Orientation")
        return state

    requested = state.get("requested_parts", ["all"])
    if "video_script" not in requested and "video" not in requested and "all" not in requested:
        state.setdefault("artifacts_status", {})["video_script"] = ArtifactStatus.SKIPPED
        return state

    # Import inside function to avoid circular imports
    from agents.creator_agents import video_script_creator_agent
    state = video_script_creator_agent(state)
    state.setdefault("artifacts_status", {})["video_script"] = ArtifactStatus.APPROVED
    write_state_artifacts_to_disk(state)
    save_state_checkpoint(state)
    return state


@component
def pipeline_practical_lab_production(state: AgentState) -> AgentState:
    """Tự động biên soạn nội dung Bài thực hành (Hands-on Practical Lab) ra file practical_lab.json"""
    if _is_session_01_orientation(state):
        print("  [Session 01 Orientation] SKIPPED Practical Lab / Homework generation for Session 01.")
        state.setdefault("artifacts_status", {})["practical_lab"] = skipped("Session 01 Orientation")
        return state

    requested = state.get("requested_parts", ["all"])
    if "practical_lab" not in requested and "quiz" not in requested and "all" not in requested and "html" not in requested:
        state.setdefault("artifacts_status", {})["practical_lab"] = ArtifactStatus.SKIPPED
        return state
        
    from agents.creator_agents import practical_lab_creator_agent

    # Bài thực hành là nơi rò rỉ phạm vi gây hại nhất: học viên phải TỰ làm, nên gặp
    # khái niệm chưa học là tắc hẳn chứ không đọc lướt qua được như trong bài đọc.
    # Sinh lại tối đa 2 lần nếu vi phạm, thay vì chỉ ghi log rồi vẫn xuất bản.
    audit = None
    for attempt in range(2):
        state = practical_lab_creator_agent(state)
        audit = audit_artifact_scope(
            state.get("practical_lab_markdown", ""), state, "practical_lab"
        )
        if audit.is_clean:
            state.setdefault("artifacts_status", {})["practical_lab"] = ArtifactStatus.APPROVED
            break

        record_scope_audit(state, audit)
        if attempt == 0:
            print("  [Practical Lab] Vi phạm phạm vi — đang sinh lại bài thực hành...")
    else:
        state.setdefault("artifacts_status", {})["practical_lab"] = STATUS_SCOPE_WARNING

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
                        if not is_approved(state.get("artifacts_status", {}).get("html")):
                            state.setdefault("artifacts_status", {})["html"] = ArtifactStatus.PENDING
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
        
        print("\n[Parallel Engine] 🚀 Kích hoạt luồng sản xuất song song tất cả tài nguyên từ JSON Blueprint (HTML Reading, Quiz, Lab, ReadingQuestions, VideoScript)...")
        start_t = time.time()
        
        pipelines = [
            ("HTML", pipeline_html_production),
            ("Quiz", pipeline_quiz_production),
            ("PracticalLab", pipeline_practical_lab_production),
            ("ReadingQuestions", pipeline_reading_questions_production),
            ("VideoScript", pipeline_video_script_production),
        ]
        
        def _run_pipelines_threaded():
            """Chạy các pipeline song song bằng ThreadPool, trả về {tên nhánh: state nhánh}."""
            collected = {}
            futures_map = {}
            with ThreadPoolExecutor(max_workers=len(pipelines)) as executor:
                for name, fn in pipelines:
                    futures_map[executor.submit(fn, copy.deepcopy(state))] = name
                for future in as_completed(futures_map):
                    name = futures_map[future]
                    try:
                        collected[name] = future.result()
                        print(f"  ✓ [Parallel Engine] Nhánh dẫn xuất {name} hoàn tất.")
                    except Exception as e:
                        print(f"  ❌ [Parallel Engine] Nhánh dẫn xuất {name} lỗi: {e}")
            return collected

        async def _run_async_pipeline():
            async def _run_one(name, fn):
                res_state = await asyncio.to_thread(fn, copy.deepcopy(state))
                return name, res_state

            tasks = [_run_one(name, fn) for name, fn in pipelines]
            return await asyncio.gather(*tasks, return_exceptions=True)

        # Gom kết quả tất cả các nhánh rồi merge MỘT LẦN qua STATE_REDUCERS.
        # Trước đây mỗi nhánh được merge ngay khi xong bằng _merge_sub_state (copy tay
        # từng tên field) — vừa trùng lặp với reducer registry, vừa để lọt artifact.
        branch_results = {}
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                branch_results = _run_pipelines_threaded()
            else:
                for res in asyncio.run(_run_async_pipeline()):
                    if isinstance(res, Exception):
                        print(f"  ❌ [Parallel Async Engine] Exception: {res}")
                        continue
                    name, sub_state = res
                    branch_results[name] = sub_state
                    print(f"  ✓ [Parallel Engine] Nhánh dẫn xuất {name} hoàn tất.")
        except Exception as err:
            print(f"  ⚠️ [Parallel Engine Fallback] Async execution fallback to ThreadPool: {err}")
            branch_results = _run_pipelines_threaded()

        state = merge_branch_states(state, branch_results)

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
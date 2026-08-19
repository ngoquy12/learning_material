"""
cli/commands/workflow_cmd.py
Core orchestration workflow executor for LangGraph Multi-Agent Learning Content generation.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any

from core.state import AgentState
from core.graph import compile_learning_content_workflow
from cli.curriculum_parser import (
    parse_all_sessions,
    detect_tech_stack_from_curriculum,
    get_context_curriculum,
    initialize_skeleton_structure,
    project_structure_reviewer_agent,
    get_or_rename_sanitized_folder,
    format_full_folder_name,
    is_exam_session,
    is_project_or_hackathon_session,
    is_practice_session
)
from cli.publisher import (
    generate_obsidian_vault,
    export_scorm_package_cli,
    show_cache_statistics,
    print_generation_summary,
)

def execute_course_workflow(args):
    """Executes the full course material generation workflow across sessions and lessons."""
    excel_path = args.pm

    if args.cache_stats:
        show_cache_statistics()
        return

    if args.scorm:
        export_scorm_package_cli(excel_path)
        return

    if not os.path.exists(excel_path):
        print(f"Error: Excel PM file not found at {excel_path}")
        return

    if args.obsidian:
        sessions = parse_all_sessions(excel_path)
        generate_obsidian_vault(excel_path, sessions)
        return

    if args.scaffold:
        from scripts.scaffold_course_resources import scaffold_course_resources
        scaffold_course_resources(excel_path)
        return

    requested_parts = [p.strip().lower() for p in args.parts.split(",")] if args.parts != "all" else ["html", "quiz", "mindmap", "practical_lab", "slide"]
    requested_sessions = [s.strip().lower() for s in args.session.split(",")] if args.session != "all" else ["all"]

    print(f"Loading spreadsheet: {excel_path}")
    all_sessions = parse_all_sessions(excel_path)
    sessions = all_sessions
    print(f"Successfully loaded {len(all_sessions)} sessions from spreadsheet.")
    if "all" not in requested_sessions:
        sessions = [s for s in all_sessions if any(rs in s["session_id"].lower() for rs in requested_sessions)]
        print(f"Filtered to {len(sessions)} sessions matching {requested_sessions}.")

    workflow = compile_learning_content_workflow()

    output_base_dir = Path("output") / "pms"
    output_base_dir.mkdir(parents=True, exist_ok=True)

    excel_path_obj = Path(excel_path)
    if "pms" in excel_path_obj.parent.parts:
        if excel_path_obj.parent.name != "pms":
            course_dir = excel_path_obj.parent
        else:
            course_clean = excel_path_obj.stem.replace("PM_Generated_", "").replace("_Updated", "").strip()
            course_dir = output_base_dir / course_clean
    else:
        course_clean = excel_path_obj.stem.replace("PM_Generated_", "").replace("_Updated", "").strip()
        course_dir = output_base_dir / course_clean
    course_dir.mkdir(parents=True, exist_ok=True)
    course_dir_name = f"pms/{course_dir.name}"

    tech_stack = args.tech_stack.strip().lower() if getattr(args, "tech_stack", "") else ""
    if not tech_stack or tech_stack == "auto":
        tech_stack = detect_tech_stack_from_curriculum(all_sessions, excel_path)
        print(f"🤖 [Auto-Detected Tech Stack] Tự động trích xuất công nghệ từ giáo trình Excel: {tech_stack}")
    else:
        print(f"Detected course technology stack: {tech_stack}")

    if not args.approve_pm:
        print("\n=========================================")
        print(">>> Giai đoạn 0: Thẩm định PM Input <<<")
        print("=========================================")
        from agents.reviewer_agents import pm_reviewer_agent
        full_curriculum_json = json.dumps(all_sessions, ensure_ascii=False)
        report = pm_reviewer_agent(full_curriculum_json, tech_stack)
        
        report_path = course_dir / "pm_review_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n[CHỜ DUYỆT PM] Hệ thống đã đánh giá file PM và xuất báo cáo tại {report_path}.")
        
        choice = input("Bạn có muốn AI tự động chỉnh sửa file Excel PM dựa trên các đề xuất này không? (y/n): ")
        if choice.strip().lower() == 'y':
            from agents.reviewer_agents import pm_updater_agent
            print("Đang tiến hành cập nhật PM...")
            updated_json = pm_updater_agent(full_curriculum_json, report, tech_stack)
            
            from core.pm_updater_excel import export_updated_pm_to_excel
            import json as json_lib
            try:
                clean_json = updated_json.replace("```json", "").replace("```", "").strip()
                parsed_json = json_lib.loads(clean_json)
                new_excel_path = str(Path(excel_path).with_name(f"{Path(excel_path).stem}_AI_Updated.xlsx"))
                export_updated_pm_to_excel(parsed_json, excel_path, new_excel_path)
                print(f"Đã lưu file PM mới tại: {new_excel_path}")
                print("Vui lòng chạy lại hệ thống với file Excel mới (--pm) và cờ --approve-pm!")
            except Exception as e:
                print(f"Lỗi khi cập nhật file Excel: {e}")
            return
        else:
            print("Vui lòng xem báo cáo, tự điều chỉnh file PM và chạy lại với cờ --approve-pm!")
            return

    initialize_skeleton_structure(all_sessions, course_dir, requested_parts, args.session.strip().lower())
    project_structure_reviewer_agent(all_sessions, course_dir, requested_parts, args.session.strip().lower())

    summary = []

    for session in sessions:
        session_id = session["session_id"]
        session_title = session.get("title", "")

        if "all" not in requested_sessions and not any(rs in session_id.lower() for rs in requested_sessions):
            continue

        print(f"\n=====================================================================")
        print(f"PROCESSING SESSION: {session_id} - {session_title}")
        print(f"=====================================================================")

        is_exam = is_exam_session(session)
        is_project_or_hackathon = is_project_or_hackathon_session(session)
        is_practice = is_practice_session(session)

        if is_exam:
            print(f"\n  ---> [Exam Session] Skipped regular material generation for Exam Session: {session_id} - {session_title}")
            session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
            session_dir.mkdir(parents=True, exist_ok=True)
            (session_dir / "Đề thi tự luận").mkdir(parents=True, exist_ok=True)
            (session_dir / "Đề thi trắc nghiệm").mkdir(parents=True, exist_ok=True)
            (session_dir / "Câu hỏi vấn đáp").mkdir(parents=True, exist_ok=True)

            summary.append({
                "session_id": session_id,
                "lesson_id": "",
                "title": session_title,
                "html_file": "Skipped (Exam Session)",
                "slides_file": "Skipped (Exam Session)",
                "quiz_file": "Skipped (Exam Session)",
                "video_script_file": "Skipped (Exam Session)",
                "mindmap_file": "Skipped (Exam Session)",
                "status": "EXAM SKELETON CREATED",
                "review_count": 0
            })
            continue

        if is_project_or_hackathon or is_practice:
            print(f"\n  ---> Processing Session-Level: {session_id} - {session_title}")
            
            if args.approve_pm:
                session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
                session_dir.mkdir(parents=True, exist_ok=True)
                
                prior_sessions = []
                for s in all_sessions:
                    if s["session_id"] == session_id:
                        break
                    prior_sessions.append(s)
                
                previous_lessons_text = ""
                latest_theory_session_text = ""
                if prior_sessions:
                    latest_s = prior_sessions[-1]
                    latest_theory_session_text = f"Session: {latest_s.get('session_id', '')} - {latest_s.get('title', '')}\n"
                    for l in latest_s.get("lessons", []):
                        latest_theory_session_text += f"  * {l.get('lesson_id', '')}: {l.get('title', '')} ({l.get('details', '')})\n"
                    
                    for s in prior_sessions:
                        for l in s.get("lessons", []):
                            previous_lessons_text += f"- {l['lesson_id']}: {l['title']} ({l.get('details', '')})\n"
                
                future_sessions = []
                current_found = False
                for s in all_sessions:
                    if current_found:
                        future_sessions.append(s)
                    elif s.get("session_id") == session_id:
                        current_found = True

                future_forbidden_items = []
                for s in future_sessions:
                    if s.get("title"):
                        future_forbidden_items.append(s["title"])
                    for l in s.get("lessons", []):
                        if l.get("title"):
                            future_forbidden_items.append(l["title"])
                        if l.get("details"):
                            future_forbidden_items.append(l["details"])

                combined_forbidden = session.get("forbidden_scope", "") or ""
                if future_forbidden_items:
                    future_str = "; ".join(dict.fromkeys(future_forbidden_items[:25]))
                    combined_forbidden = f"{combined_forbidden}; CÁC KIẾN THỨC BUỔI SAU TUYỆT ĐỐI CHƯA ĐƯỢC DÙNG: {future_str}".strip("; ")

                session_payload = dict(session)
                session_payload["forbidden_scope"] = combined_forbidden
                session_payload["allowed_scope"] = previous_lessons_text

                if is_project_or_hackathon:
                    print(f"  [Project/Hackathon] Generating Mini Project templates via Agent for: {session_title}")
                    from agents.project_agents import generate_mini_project_session
                    generate_mini_project_session(
                        session_id=session_id,
                        session_title=session_title,
                        session_dir_path=str(session_dir),
                        tech_stack=tech_stack,
                        previous_lessons_text=previous_lessons_text,
                        session_info=session_payload
                    )
                elif is_practice:
                    print(f"  [Practice] Generating practice exercises via Agent for: {session_title}")
                    from agents.practice_agents import generate_practice_session_exercises
                    generate_practice_session_exercises(
                        session_id=session_id,
                        session_title=session_title,
                        session_dir_path=str(session_dir),
                        tech_stack=tech_stack,
                        previous_lessons_text=previous_lessons_text,
                        latest_theory_session=latest_theory_session_text
                    )
                
                summary.append({
                    "session_id": session_id,
                    "lesson_id": "",
                    "title": session_title,
                    "html_file": "Generated Project Templates" if is_project_or_hackathon else "Generated Practice Assignments",
                    "slides_file": "Skipped (Project/Practice)",
                    "quiz_file": "Skipped (Project/Practice)",
                    "video_script_file": "Skipped (Project/Practice)",
                    "mindmap_file": "Skipped (Project/Practice)",
                    "status": "APPROVED",
                    "review_count": 0
                })
                continue

        if session["lessons"]:
            previous_lessons = []
            
            from core.domain_knowledge import get_domain_for_session
            session_domain_data = get_domain_for_session(session_id, session_title)
            session_domain_id = session_domain_data.get("domain_id", "SHOPEE_FOOD")
            session_domain_name = session_domain_data.get("name_vi", "Hệ thống Đặt đồ ăn ShopeeFood")
            print(f"\n  ================================================================================")
            print(f"  [Session Domain Anchor] Session {session_id} - {session_title}")
            print(f"  -> Trục nghiệp vụ thống nhất 100%: {session_domain_name} ({session_domain_id})")
            print(f"  ================================================================================\n")

            # Check if Parallel Batch Execution is enabled via --parallel
            if getattr(args, "parallel", False):
                print(f"\n  ---> [Parallel Batch] Preparing parallel generation for Session: {session_id} ({len(session['lessons'])} lessons)")
                batch_states = []
                already_completed_states = []
                
                for idx, lesson in enumerate(session["lessons"]):
                    lesson_id = lesson["lesson_id"]
                    lesson_title = lesson["title"]
                    lesson_details = lesson.get("details", "")
                    expected_output = lesson.get("expected_output", "")
                    
                    state: AgentState = {
                        "session_id": session_id,
                        "lesson_id": lesson_id,
                        "lesson_title": lesson_title,
                        "pm_input": json.dumps(lesson, ensure_ascii=False),
                        "full_curriculum": json.dumps(get_context_curriculum(sessions, session_id), ensure_ascii=False),
                        "time_reference": {"weeks": 1, "hours_per_week": 10},
                        "learning_outcomes": {},
                        "program_structure": {},
                        "core_ssot": {
                            "session_title": lesson_title,
                            "lesson_details": lesson_details,
                            "expected_output": expected_output
                        },
                        "previous_lessons": previous_lessons.copy(),
                        "artifacts_status": {
                            "html": "Pending", "slide": "Pending", "quiz": "Pending",
                            "video_script": "Pending", "mindmap": "Pending", "session": "Pending"
                        },
                        "course_dir_name": course_dir_name,
                        "technology_stack": tech_stack,
                        "session_domain": session_domain_data,
                        "chosen_domain": session_domain_id,
                        "html_content": "", "slide_markdown": "", "quiz_json": {},
                        "video_script_markdown": "", "mindmap_markdown": "", "review_logs": [],
                        "requested_parts": requested_parts,
                        "force_rebuild": args.force,
                        "pm_approved": args.approve_pm
                    }
                    
                    from core.persistence import load_checkpoint
                    checkpoint_key = f"{session_id}_{lesson_id}".strip("_")
                    cached_state = load_checkpoint(checkpoint_key)
                    if cached_state and cached_state.get("artifacts_status", {}).get("session") == "PUBLISHED" and not args.force:
                        print(f"  [Checkpoint] Lesson {lesson_id} is already PUBLISHED. Using cached state.")
                        already_completed_states.append(cached_state)
                    else:
                        if cached_state and not args.force:
                            state = cached_state
                        batch_states.append(state)
                
                # Execute pending batch states concurrently
                executed_states = []
                if batch_states:
                    from core.batch_runner import execute_lessons_batch_parallel
                    batch_concurrency = getattr(args, "concurrency", 4)
                    executed_states = execute_lessons_batch_parallel(
                        batch_states,
                        lambda st: workflow.run(st),
                        max_workers=batch_concurrency
                    )
                
                all_final_states = already_completed_states + executed_states
                
                # Post-process disk writes for all final states
                for final_state in all_final_states:
                    lesson_id = final_state.get("lesson_id", "")
                    lesson_title = final_state.get("lesson_title", "")
                    
                    session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
                    lesson_dir = get_or_rename_sanitized_folder(session_dir, lesson_id, format_full_folder_name(lesson_id, lesson_title))
                    lesson_dir.mkdir(parents=True, exist_ok=True)
                    
                    if "html" in requested_parts and final_state.get("html_content"):
                        html_sub = lesson_dir / "Bài đọc"
                        html_sub.mkdir(parents=True, exist_ok=True)
                        html_path = html_sub / "reading.html"
                        with open(html_path, "w", encoding="utf-8") as f:
                            f.write(final_state.get("html_content", ""))
                    else:
                        html_path = "Skipped"

                    slides_path = "Skipped (Temporarily Commented Out)"

                    if "quiz" in requested_parts and final_state.get("quiz_json"):
                        quiz_sub = lesson_dir / "Quizz lesson"
                        if not quiz_sub.exists() and (lesson_dir / "Câu hỏi Quizz").exists():
                            quiz_sub = lesson_dir / "Câu hỏi Quizz"
                        quiz_sub.mkdir(parents=True, exist_ok=True)
                        quiz_json_path = quiz_sub / "quiz.json"
                        with open(quiz_json_path, "w", encoding="utf-8") as f:
                            json.dump(final_state.get("quiz_json", {}), f, ensure_ascii=False, indent=2)
                        
                        from core.quiz_excel import export_lesson_quiz_to_excel
                        s_num_str = session_id.replace(" ", "")
                        l_num_str = lesson_id.replace(" ", "")
                        excel_filename = f"Quizz_{s_num_str}_{l_num_str}.xlsx"
                        excel_path_file = quiz_sub / excel_filename
                        quiz_data = final_state.get("quiz_json", {})
                        if isinstance(quiz_data, dict):
                            quiz_items = quiz_data.get("lesson_quiz") or quiz_data.get("quiz") or []
                        else:
                            quiz_items = quiz_data
                        export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                        quiz_reported_path = str(excel_path_file)
                    else:
                        quiz_reported_path = "Skipped"

                    if final_state.get("practical_lab_markdown") or final_state.get("lab_json"):
                        lab_sub = lesson_dir / "Bài thực hành"
                        lab_sub.mkdir(parents=True, exist_ok=True)
                        lab_md = final_state.get("practical_lab_markdown")
                        if not lab_md and final_state.get("lab_json"):
                            from agents.creators.practical_lab_creator import format_lab_to_markdown
                            lab_md = format_lab_to_markdown(final_state["lab_json"])
                        if lab_md:
                            with open(lab_sub / "practical_lab.md", "w", encoding="utf-8") as f:
                                f.write(lab_md)
                        lab_html = final_state.get("practical_lab_html")
                        if not lab_html and final_state.get("lab_json"):
                            from agents.creators.practical_lab_creator import format_lab_to_html
                            lab_html = format_lab_to_html(final_state["lab_json"], final_state.get("tech_stack", "python"))
                        if lab_html:
                            with open(lab_sub / "practical_lab.html", "w", encoding="utf-8") as f:
                                f.write(lab_html)

                    if final_state.get("reading_questions_markdown") or final_state.get("reading_questions_json"):
                        rq_sub = lesson_dir / "Câu hỏi bài đọc"
                        rq_sub.mkdir(parents=True, exist_ok=True)
                        rq_md = final_state.get("reading_questions_markdown")
                        if not rq_md and final_state.get("reading_questions_json"):
                            from agents.creators.reading_questions_creator import format_reading_questions_to_markdown
                            rq_md = format_reading_questions_to_markdown(final_state["reading_questions_json"])
                        if rq_md:
                            with open(rq_sub / "reading_questions.md", "w", encoding="utf-8") as f:
                                f.write(rq_md)

                    if ("video" in requested_parts or "video_script" in requested_parts) and final_state.get("video_script_markdown"):
                        video_sub = lesson_dir / "Video"
                        video_sub.mkdir(parents=True, exist_ok=True)
                        video_script_path = video_sub / "SCRIPT.md"
                        with open(video_script_path, "w", encoding="utf-8") as f:
                            f.write(final_state.get("video_script_markdown", ""))
                    else:
                        video_script_path = "Skipped"

                    if "mindmap" in requested_parts and final_state.get("mindmap_markdown"):
                        mindmap_sub = lesson_dir / "Mindmap"
                        mindmap_sub.mkdir(parents=True, exist_ok=True)
                        mindmap_path = mindmap_sub / "mindmap.md"
                        with open(mindmap_path, "w", encoding="utf-8") as f:
                            f.write(final_state.get("mindmap_markdown", ""))
                    else:
                        mindmap_path = "Skipped"

                    summary.append({
                        "session_id": session_id,
                        "lesson_id": lesson_id,
                        "title": lesson_title,
                        "html_file": str(html_path),
                        "slides_file": "Moved to Session Level",
                        "quiz_file": quiz_reported_path,
                        "video_script_file": str(video_script_path),
                        "mindmap_file": "Moved to Session Level",
                        "status": final_state.get("artifacts_status", {}).get("session", "FAILED"),
                        "review_count": len(final_state.get("review_logs", []))
                    })
                    
                    master_c = final_state.get("master_content", {})
                    rich_summary = f"Bài học: {lesson_title}\n"
                    if isinstance(master_c, dict):
                        if "reading_sections" in master_c:
                            for sec in master_c["reading_sections"]:
                                rich_summary += f"### {sec.get('title')}\n"
                                rich_summary += f"{sec.get('content', '')[:150]}...\n"
                        if "example" in master_c and master_c["example"]:
                            rich_summary += f"### Cú pháp/Mã nguồn đã học:\n```python\n{master_c['example']}\n```\n"
                    else:
                        rich_summary += final_state.get("html_content", "")[:300]

                    previous_lessons.append({
                        "lesson_id": lesson_id,
                        "title": lesson_title,
                        "html_summary": rich_summary
                    })
            else:
                # Standard Sequential Execution (Default)
                for idx, lesson in enumerate(session["lessons"]):
                    lesson_id = lesson["lesson_id"]
                    lesson_title = lesson["title"]
                    lesson_details = lesson.get("details", "")
                    expected_output = lesson.get("expected_output", "")

                    print(f"\n  ---> Processing: {session_id} - {lesson_id}: {lesson_title}")
                    
                    state: AgentState = {
                        "session_id": session_id,
                        "lesson_id": lesson_id,
                        "lesson_title": lesson_title,
                        "pm_input": json.dumps(lesson, ensure_ascii=False),
                        "full_curriculum": json.dumps(get_context_curriculum(sessions, session_id), ensure_ascii=False),
                        "time_reference": {
                            "weeks": 1,
                            "hours_per_week": 10
                        },
                        "learning_outcomes": {},
                        "program_structure": {},
                        "core_ssot": {
                            "session_title": lesson_title,
                            "lesson_details": lesson_details,
                            "expected_output": expected_output
                        },
                        "previous_lessons": previous_lessons.copy(),
                        "artifacts_status": {
                            "html": "Pending",
                            "slide": "Pending",
                            "quiz": "Pending",
                            "video_script": "Pending",
                            "mindmap": "Pending",
                            "session": "Pending"
                        },
                        "course_dir_name": course_dir_name,
                        "technology_stack": tech_stack,
                        "session_domain": session_domain_data,
                        "chosen_domain": session_domain_id,
                        "html_content": "",
                        "slide_markdown": "",
                        "quiz_json": {},
                        "video_script_markdown": "",
                        "mindmap_markdown": "",
                        "review_logs": [],
                        "requested_parts": requested_parts,
                        "force_rebuild": args.force,
                        "pm_approved": args.approve_pm
                    }

                    is_project_or_hackathon = any(kw in session_title.lower() or kw in lesson_title.lower() for kw in ["hackathon", "project", "đồ án", "dự án", "mini project"])
                    is_practice = "thực hành" in session_title.lower() or "thực hành" in lesson_title.lower()
                    
                    if args.approve_pm and (is_project_or_hackathon or is_practice):
                        session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
                        lesson_dir = get_or_rename_sanitized_folder(session_dir, lesson_id, format_full_folder_name(lesson_id, lesson_title))
                        lesson_dir.mkdir(parents=True, exist_ok=True)
                        
                        if is_project_or_hackathon:
                            print(f"  [Skip] Skipping AI generation for Project/Hackathon: {lesson_title}")
                            (lesson_dir / "Bài kiểm tra đầu giờ").mkdir(exist_ok=True)
                            (lesson_dir / "Tài liệu đặc tả SRS").mkdir(exist_ok=True)
                            (lesson_dir / "Mini project").mkdir(exist_ok=True)
                        elif is_practice:
                            print(f"  [Skip] Skipping AI generation for Practice Session: {lesson_title}")
                            (lesson_dir / "Bài tập").mkdir(exist_ok=True)
                        
                        summary.append({
                            "session_id": session_id,
                            "lesson_id": lesson_id,
                            "title": lesson_title,
                            "html_file": "Skipped (Project/Practice)",
                            "slides_file": "Skipped (Project/Practice)",
                            "quiz_file": "Skipped (Project/Practice)",
                            "video_script_file": "Skipped (Project/Practice)",
                            "mindmap_file": "Skipped (Project/Practice)",
                            "status": "APPROVED",
                            "review_count": 0
                        })
                        continue

                    # Run the pipeline for normal lessons
                    try:
                        from core.persistence import load_checkpoint
                        checkpoint_key = f"{session_id}_{lesson_id}".strip("_")
                        cached_state = load_checkpoint(checkpoint_key)
                        if cached_state and cached_state.get("artifacts_status", {}).get("session") == "PUBLISHED" and not args.force:
                            print(f"  [Checkpoint] Lesson {lesson_id} is already PUBLISHED. Loading from database...")
                            final_state = cached_state
                        else:
                            if cached_state and not args.force:
                                print(f"  [Checkpoint] Found intermediate checkpoint for {lesson_id}. Resuming...")
                                state = cached_state
                            final_state = workflow.run(state)
                        
                        session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
                        lesson_dir = get_or_rename_sanitized_folder(session_dir, lesson_id, format_full_folder_name(lesson_id, lesson_title))
                        lesson_dir.mkdir(parents=True, exist_ok=True)

                        if "html" in requested_parts and final_state.get("html_content"):
                            html_sub = lesson_dir / "Bài đọc"
                            html_sub.mkdir(parents=True, exist_ok=True)
                            html_path = html_sub / "reading.html"
                            with open(html_path, "w", encoding="utf-8") as f:
                                f.write(final_state.get("html_content", ""))
                        else:
                            html_path = "Skipped"

                        slides_path = "Skipped (Temporarily Commented Out)"

                        if "quiz" in requested_parts and final_state.get("quiz_json"):
                            quiz_sub = lesson_dir / "Quizz lesson"
                            if not quiz_sub.exists() and (lesson_dir / "Câu hỏi Quizz").exists():
                                quiz_sub = lesson_dir / "Câu hỏi Quizz"
                            quiz_sub.mkdir(parents=True, exist_ok=True)
                            quiz_json_path = quiz_sub / "quiz.json"
                            with open(quiz_json_path, "w", encoding="utf-8") as f:
                                json.dump(final_state.get("quiz_json", {}), f, ensure_ascii=False, indent=2)
                            
                            from core.quiz_excel import export_lesson_quiz_to_excel
                            s_num_str = session_id.replace(" ", "")
                            l_num_str = lesson_id.replace(" ", "")
                            excel_filename = f"Quizz_{s_num_str}_{l_num_str}.xlsx"
                            excel_path_file = quiz_sub / excel_filename
                            quiz_data = final_state.get("quiz_json", {})
                            if isinstance(quiz_data, dict):
                                quiz_items = quiz_data.get("lesson_quiz") or quiz_data.get("quiz") or []
                            else:
                                quiz_items = quiz_data
                            export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                            quiz_reported_path = str(excel_path_file)
                        else:
                            quiz_reported_path = "Skipped"

                        if final_state.get("practical_lab_markdown") or final_state.get("lab_json"):
                            lab_sub = lesson_dir / "Bài thực hành"
                            lab_sub.mkdir(parents=True, exist_ok=True)
                            lab_md = final_state.get("practical_lab_markdown")
                            if not lab_md and final_state.get("lab_json"):
                                from agents.creators.practical_lab_creator import format_lab_to_markdown
                                lab_md = format_lab_to_markdown(final_state["lab_json"])
                            if lab_md:
                                with open(lab_sub / "practical_lab.md", "w", encoding="utf-8") as f:
                                    f.write(lab_md)
                            lab_html = final_state.get("practical_lab_html")
                            if not lab_html and final_state.get("lab_json"):
                                from agents.creators.practical_lab_creator import format_lab_to_html
                                lab_html = format_lab_to_html(final_state["lab_json"], final_state.get("tech_stack", "python"))
                            if lab_html:
                                with open(lab_sub / "practical_lab.html", "w", encoding="utf-8") as f:
                                    f.write(lab_html)

                        if final_state.get("reading_questions_markdown") or final_state.get("reading_questions_json"):
                            rq_sub = lesson_dir / "Câu hỏi bài đọc"
                            rq_sub.mkdir(parents=True, exist_ok=True)
                            rq_md = final_state.get("reading_questions_markdown")
                            if not rq_md and final_state.get("reading_questions_json"):
                                from agents.creators.reading_questions_creator import format_reading_questions_to_markdown
                                rq_md = format_reading_questions_to_markdown(final_state["reading_questions_json"])
                            if rq_md:
                                with open(rq_sub / "reading_questions.md", "w", encoding="utf-8") as f:
                                    f.write(rq_md)

                        if ("video" in requested_parts or "video_script" in requested_parts) and final_state.get("video_script_markdown"):
                            video_sub = lesson_dir / "Video"
                            video_sub.mkdir(parents=True, exist_ok=True)
                            video_script_path = video_sub / "SCRIPT.md"
                            with open(video_script_path, "w", encoding="utf-8") as f:
                                f.write(final_state.get("video_script_markdown", ""))
                        else:
                            video_script_path = "Skipped"

                        if "mindmap" in requested_parts and final_state.get("mindmap_markdown"):
                            mindmap_sub = lesson_dir / "Mindmap"
                            mindmap_sub.mkdir(parents=True, exist_ok=True)
                            mindmap_path = mindmap_sub / "mindmap.md"
                            with open(mindmap_path, "w", encoding="utf-8") as f:
                                f.write(final_state.get("mindmap_markdown", ""))
                        else:
                            mindmap_path = "Skipped"

                        summary.append({
                            "session_id": session_id,
                            "lesson_id": lesson_id,
                            "title": lesson_title,
                            "html_file": str(html_path),
                            "slides_file": "Skipped (Moved to Session Level)",
                            "quiz_file": quiz_reported_path,
                            "video_script_file": str(video_script_path),
                            "mindmap_file": "Skipped (Moved to Session Level)",
                            "status": final_state.get("artifacts_status", {}).get("session", "FAILED"),
                            "review_count": len(final_state.get("review_logs", []))
                        })
                        
                        master_c = final_state.get("master_content", {})
                        rich_summary = f"Bài học: {lesson_title}\n"
                        if isinstance(master_c, dict):
                            if "reading_sections" in master_c:
                                for sec in master_c["reading_sections"]:
                                    rich_summary += f"### {sec.get('title')}\n"
                                    rich_summary += f"{sec.get('content', '')[:150]}...\n"
                            if "example" in master_c and master_c["example"]:
                                rich_summary += f"### Cú pháp/Mã nguồn đã học:\n```python\n{master_c['example']}\n```\n"
                        else:
                            rich_summary += final_state.get("html_content", "")[:300]

                        previous_lessons.append({
                            "lesson_id": lesson_id,
                            "title": lesson_title,
                            "html_summary": rich_summary
                        })

                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        print(f"❌ Error processing {session_id} - {lesson_id}: {e}")
                        summary.append({
                            "session_id": session_id,
                            "lesson_id": lesson_id,
                            "title": lesson_title,
                            "html_file": "ERROR",
                            "slides_file": "ERROR",
                            "quiz_file": "ERROR",
                            "video_script_file": "ERROR",
                            "mindmap_file": "ERROR",
                            "status": f"FAILED ({e})",
                            "review_count": 0
                        })

            # Automatically generate Session-Level Assets (Session Slides, Session Mindmap & Session Homework Exercises)
            if args.approve_pm and not (is_project_or_hackathon or is_practice):
                session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
                session_dir.mkdir(parents=True, exist_ok=True)
                
                session_lessons_text = f"Chi tiết kiến thức thực tế đã được duyệt sản xuất trong bài học ({session_title}):\n"
                for pl in previous_lessons:
                    session_lessons_text += f"\n=========================================\n"
                    session_lessons_text += f"BÀI HỌC {pl['lesson_id']}: {pl['title']}\n"
                    session_lessons_text += f"{pl['html_summary']}\n"
                
                from agents.homework_agents import generate_session_homework
                from agents.session_mindmap_agent import generate_session_mindmap
                
                print(f"\n  ---> [Session Generator] Tự động sinh Bài giảng trên lớp, Mindmap Session & Bộ Bài tập Session cho {session_id} theo Domain [{session_domain_name}]...")
                session_forbidden_scope = session.get("forbidden_scope", "")
                generate_session_homework(
                    session_id=session_id,
                    session_title=session_title,
                    session_dir_path=str(session_dir),
                    tech_stack=tech_stack,
                    previous_lessons_text=session_lessons_text,
                    forbidden_scope=session_forbidden_scope,
                    chosen_domain=session_domain_id
                )
                
                generate_session_mindmap(
                    session_id=session_id,
                    session_title=session_title,
                    session_dir_path=str(session_dir),
                    tech_stack=tech_stack,
                    previous_lessons_text=session_lessons_text
                )

                if "slide" in requested_parts:
                    # 1. Sinh Bài giảng trên lớp trực quan (HTML + Visualizer)
                    from agents.classroom_lecture_generator_agent import classroom_lecture_generator_agent
                    classroom_lecture_generator_agent.generate_lecture(
                        session_id=session_id,
                        session_title=session_title,
                        session_dir_path=str(session_dir),
                        tech_stack=tech_stack,
                        previous_lessons_text=session_lessons_text
                    )

                    # 2. Sinh Slide bài giảng PowerPoint (.pptx) & Outline theo chuẩn Create_Slide 3-Skill
                    try:
                        from agents.creators.slide_deck_creator import generate_session_slide_deck
                        slide_deck_dir = session_dir / "Slide bài giảng"
                        print(f"  ---> [Slide bài giảng] Đang sinh file PowerPoint (.pptx) & Outline cho {session_id}...")
                        generate_session_slide_deck(
                            session_title=session_title,
                            course_name=course_clean,
                            tech_stack=tech_stack,
                            target_dir=slide_deck_dir,
                            chosen_domain=session_domain_id
                        )
                    except Exception as e_slide:
                        print(f"  ⚠️ [Slide bài giảng] Lỗi khi sinh Slide PowerPoint: {e_slide}")
        else:
            # Session with no sub-lessons
            state: AgentState = {
                "session_id": session_id,
                "lesson_id": "",
                "pm_input": json.dumps(session, ensure_ascii=False),
                "full_curriculum": json.dumps(get_context_curriculum(sessions, session_id), ensure_ascii=False),
                "time_reference": {"weeks": 1, "hours_per_week": 10},
                "learning_outcomes": {},
                "program_structure": {},
                "core_ssot": {"session_title": session_title, "lesson_details": "", "expected_output": ""},
                "previous_lessons": [],
                "artifacts_status": {"html": "Pending", "slide": "Pending", "quiz": "Pending", "video_script": "Pending", "mindmap": "Pending", "session": "Pending"},
                "course_dir_name": course_dir_name,
                "technology_stack": tech_stack,
                "html_content": "",
                "slide_markdown": "",
                "quiz_json": {},
                "video_script_markdown": "",
                "mindmap_markdown": "",
                "review_logs": [],
                "requested_parts": requested_parts,
                "force_rebuild": args.force,
                "pm_approved": args.approve_pm
            }

            try:
                from core.persistence import load_checkpoint
                checkpoint_key = f"{session_id}".strip("_")
                cached_state = load_checkpoint(checkpoint_key)
                if cached_state and cached_state.get("artifacts_status", {}).get("session") == "PUBLISHED" and not args.force:
                    print(f"  [Checkpoint] Session {session_id} is already PUBLISHED. Loading from database...")
                    final_state = cached_state
                else:
                    if cached_state and not args.force:
                        print(f"  [Checkpoint] Found intermediate checkpoint for {session_id}. Resuming...")
                        state = cached_state
                    final_state = workflow.run(state)
                session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
                session_dir.mkdir(parents=True, exist_ok=True)

                if "html" in requested_parts and final_state.get("html_content"):
                    html_sub = session_dir / "Bài đọc"
                    html_sub.mkdir(parents=True, exist_ok=True)
                    html_path = html_sub / "reading.html"
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("html_content", ""))
                else:
                    html_path = "Skipped"

                slides_path = "Skipped (Temporarily Commented Out)"

                if "quiz" in requested_parts and final_state.get("quiz_json"):
                    quiz_sub = session_dir / "Câu hỏi Quizz"
                    quiz_sub.mkdir(parents=True, exist_ok=True)
                    quiz_json_path = quiz_sub / "quiz.json"
                    with open(quiz_json_path, "w", encoding="utf-8") as f:
                        json.dump(final_state.get("quiz_json", {}), f, ensure_ascii=False, indent=2)
                    
                    from core.quiz_excel import export_lesson_quiz_to_excel
                    s_num_str = session_id.replace(" ", "")
                    excel_filename = f"Quizz_{s_num_str}_Thuc_hanh.xlsx"
                    excel_path_file = quiz_sub / excel_filename
                    quiz_data = final_state.get("quiz_json", {})
                    if isinstance(quiz_data, dict):
                        quiz_items = quiz_data.get("lesson_quiz") or quiz_data.get("quiz") or []
                    else:
                        quiz_items = quiz_data
                    export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                    quiz_reported_path = str(excel_path_file)
                else:
                    quiz_reported_path = "Skipped"

                if final_state.get("practical_lab_markdown") or final_state.get("lab_json"):
                    lab_sub = session_dir / "Bài thực hành"
                    lab_sub.mkdir(parents=True, exist_ok=True)
                    lab_md = final_state.get("practical_lab_markdown")
                    if not lab_md and final_state.get("lab_json"):
                        from agents.creators.practical_lab_creator import format_lab_to_markdown
                        lab_md = format_lab_to_markdown(final_state["lab_json"])
                    if lab_md:
                        with open(lab_sub / "practical_lab.md", "w", encoding="utf-8") as f:
                            f.write(lab_md)
                    lab_html = final_state.get("practical_lab_html")
                    if not lab_html and final_state.get("lab_json"):
                        from agents.creators.practical_lab_creator import format_lab_to_html
                        lab_html = format_lab_to_html(final_state["lab_json"], final_state.get("tech_stack", "python"))
                    if lab_html:
                        with open(lab_sub / "practical_lab.html", "w", encoding="utf-8") as f:
                            f.write(lab_html)

                if final_state.get("reading_questions_markdown") or final_state.get("reading_questions_json"):
                    rq_sub = session_dir / "Câu hỏi bài đọc"
                    rq_sub.mkdir(parents=True, exist_ok=True)
                    rq_md = final_state.get("reading_questions_markdown")
                    if not rq_md and final_state.get("reading_questions_json"):
                        from agents.creators.reading_questions_creator import format_reading_questions_to_markdown
                        rq_md = format_reading_questions_to_markdown(final_state["reading_questions_json"])
                    if rq_md:
                        with open(rq_sub / "reading_questions.md", "w", encoding="utf-8") as f:
                            f.write(rq_md)
 
                video_script_path = "Skipped (Temporarily Commented Out)"

                if "mindmap" in requested_parts and final_state.get("mindmap_markdown"):
                    mindmap_sub = session_dir / "Mindmap"
                    mindmap_sub.mkdir(parents=True, exist_ok=True)
                    mindmap_path = mindmap_sub / "mindmap.md"
                    with open(mindmap_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("mindmap_markdown", ""))
                else:
                    mindmap_path = "Skipped"

                summary.append({
                    "session_id": session_id,
                    "lesson_id": "",
                    "title": session_title,
                    "html_file": str(html_path),
                    "slides_file": str(slides_path),
                    "quiz_file": quiz_reported_path,
                    "video_script_file": str(video_script_path),
                    "mindmap_file": str(mindmap_path),
                    "status": final_state.get("artifacts_status", {}).get("session", "FAILED"),
                    "review_count": len(final_state.get("review_logs", []))
                })

                if args.approve_pm and not (is_project_or_hackathon or is_practice):
                    master_c = final_state.get("master_content", {})
                    rich_summary = f"Bài học: {session_title}\n"
                    if isinstance(master_c, dict):
                        if "reading_sections" in master_c:
                            for sec in master_c["reading_sections"]:
                                rich_summary += f"### {sec.get('title')}\n"
                                rich_summary += f"{sec.get('content', '')[:150]}...\n"
                        if "example" in master_c and master_c["example"]:
                            rich_summary += f"### Cú pháp/Mã nguồn đã học:\n```python\n{master_c['example']}\n```\n"
                    else:
                        rich_summary += final_state.get("html_content", "")[:300]
                        
                    session_lessons_text = rich_summary
                    
                    from agents.homework_agents import generate_session_homework
                    from agents.session_mindmap_agent import generate_session_mindmap
                    
                    session_forbidden_scope = session.get("forbidden_scope", "")
                    
                    from core.domain_knowledge import get_domain_for_session
                    sess_domain = get_domain_for_session(session_id, session_title)
                    
                    generate_session_homework(
                        session_id=session_id,
                        session_title=session_title,
                        session_dir_path=str(session_dir),
                        tech_stack=tech_stack,
                        previous_lessons_text=session_lessons_text,
                        forbidden_scope=session_forbidden_scope,
                        chosen_domain=sess_domain.get("domain_id")
                    )
                    generate_session_mindmap(
                        session_id=session_id,
                        session_title=session_title,
                        session_dir_path=str(session_dir),
                        tech_stack=tech_stack,
                        previous_lessons_text=session_lessons_text
                    )
                    if "slide" in requested_parts:
                        from agents.classroom_lecture_generator_agent import classroom_lecture_generator_agent
                        classroom_lecture_generator_agent.generate_lecture(
                            session_id=session_id,
                            session_title=session_title,
                            session_dir_path=str(session_dir),
                            tech_stack=tech_stack,
                            previous_lessons_text=session_lessons_text
                        )

            except Exception as e:
                print(f"❌ Error processing {session_id}: {e}")

        # Quizzes Dau Gio / Cuoi Gio
        if "quiz" in requested_parts:
            print(f"  ---> Generating Session-Level Quizzes (Entrance & Exit) for {session_id}...")
            slide_title = session["lessons"][0]["title"] if session["lessons"] else session_title
            
            def get_sanitized_title(title: str) -> str:
                sanitized = re.sub(r'[\s\-\:\,\.\?\!\(\)]+', '_', title)
                return re.sub(r'^_+|_+$', '', sanitized)
                
            session_num_str = session_id.replace(" ", "")
            sanitized_slide_title = get_sanitized_title(slide_title)
            
            session_title_str = next((s["title"] for s in sessions if s["session_id"] == session_id), "")
            session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title_str))
            session_dir.mkdir(parents=True, exist_ok=True)
            
            quizz_session_dir = session_dir / "Quizz session"
            quizz_session_dir.mkdir(parents=True, exist_ok=True)
            entrance_path = quizz_session_dir / f"{session_num_str}._Quizz_Dau_Gio_{sanitized_slide_title}.xlsx"
            exit_path = quizz_session_dir / f"{session_num_str}._Quizz_Cuoi_Gio_{sanitized_slide_title}.xlsx"
            
            from core.quiz_engine import generate_entrance_quiz, generate_exit_quiz
            from core.quiz_excel import export_quiz_to_excel
            
            current_topic = session_title_str
            
            def get_previous_session_id(s_id: str) -> str:
                match = re.search(r'\d+', s_id)
                if match:
                    num = int(match.group(0))
                    if num > 1:
                        return f"Session {num-1:02d}"
                return "Session 01"
                
            previous_session_id = get_previous_session_id(session_id)
            prev_s_idx = next((i for i, s in enumerate(sessions) if s["session_id"] == previous_session_id), -1)
            s_idx = next((i for i, s in enumerate(sessions) if s["session_id"] == session_id), 0)
            if prev_s_idx != -1 and prev_s_idx < s_idx:
                previous_topic = sessions[prev_s_idx]["title"]
            else:
                previous_topic = "Tổng quan"
            
            from core.scope_calculator import calculate_lesson_scope_contract
            syllabus_data = {"sessions": sessions}
            num_lessons = len(sessions[s_idx].get("lessons", []))
            allowed_set, forbidden_set = calculate_lesson_scope_contract(syllabus_data, s_idx, max(0, num_lessons - 1))
            
            forbidden_scope_str = ", ".join(sorted(forbidden_set))
            allowed_scope_str = ", ".join(sorted(allowed_set))

            entrance_qs = generate_entrance_quiz(
                session_id=session_id,
                current_topic=current_topic,
                previous_topic=previous_topic,
                tech_stack=tech_stack,
                forbidden_scope=forbidden_scope_str,
                allowed_scope=allowed_scope_str
            )
            exit_qs = generate_exit_quiz(
                session_id=session_id,
                current_topic=current_topic,
                tech_stack=tech_stack,
                forbidden_scope=forbidden_scope_str,
                allowed_scope=allowed_scope_str
            )
            
            export_quiz_to_excel(entrance_qs, str(entrance_path))
            export_quiz_to_excel(exit_qs, str(exit_path))

    print_generation_summary(summary)

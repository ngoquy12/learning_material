"""
cli/runner.py — Main orchestration runner for Elearning Content Factory CLI workflow.
"""

import sys
import io
import os
import json
import re
from pathlib import Path

from core.state import AgentState
from core.graph import compile_learning_content_workflow
from cli.args import parse_cli_arguments
from cli.curriculum_parser import (
    parse_all_sessions,
    get_context_curriculum,
    initialize_skeleton_structure,
    project_structure_reviewer_agent,
    get_or_rename_sanitized_folder,
    format_full_folder_name,
)
from cli.publisher import (
    generate_obsidian_vault,
    export_scorm_package_cli,
    show_cache_statistics,
    print_generation_summary,
)

def main_entry():
    """Main CLI execution entry point."""
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', write_through=True)

    print("=====================================================================")
    print("Starting Multi-Agent Learning Content Factory (Antigravity Workflow)")
    print("=====================================================================")

    args = parse_cli_arguments()
    excel_path = args.pm

    # Cache Stats (independent of PM file existence)
    if args.cache_stats:
        show_cache_statistics()
        return

    # SCORM Export
    if args.scorm:
        export_scorm_package_cli(excel_path)
        return

    if not os.path.exists(excel_path):
        print(f"Error: Excel PM file not found at {excel_path}")
        return

    # Obsidian Knowledge Vault
    if args.obsidian:
        sessions = parse_all_sessions(excel_path)
        generate_obsidian_vault(excel_path, sessions)
        return

    requested_parts = [p.strip().lower() for p in args.parts.split(",")] if args.parts != "all" else ["html", "slide", "quiz", "video", "mindmap"]
    requested_sessions = [s.strip().lower() for s in args.session.split(",")] if args.session != "all" else ["all"]

    print(f"Loading spreadsheet: {excel_path}")
    sessions = parse_all_sessions(excel_path)
    print(f"Successfully loaded {len(sessions)} sessions from spreadsheet.")
    if "all" not in requested_sessions:
        sessions = [s for s in sessions if any(rs in s["session_id"].lower() for rs in requested_sessions)]
        print(f"Filtered to {len(sessions)} sessions matching {requested_sessions}.")

    # Compile the workflow graph
    workflow = compile_learning_content_workflow()

    # Output directories
    output_base_dir = Path("output")
    output_base_dir.mkdir(exist_ok=True)

    course_dir_name = Path(excel_path).stem.strip().replace(" ", "_").replace("-", "_")
    course_dir = output_base_dir / course_dir_name
    course_dir.mkdir(parents=True, exist_ok=True)

    # Detect technology stack dynamically or strictly from args/PM metadata
    tech_stack = args.tech_stack.strip().lower() if getattr(args, "tech_stack", "") else ""
    if not tech_stack:
        fn = os.path.basename(excel_path).lower()
        sn = course_dir_name.lower()
        if "fastapi" in fn or "fastapi" in sn:
            tech_stack = "python/fastapi"
        elif "nestjs" in fn or "nestjs" in sn or "nest" in fn or "nest" in sn:
            tech_stack = "typescript/nestjs"
        elif "react" in fn or "react" in sn:
            tech_stack = "typescript/react"
        elif "java" in fn or "java" in sn or "springboot" in fn or "springboot" in sn:
            tech_stack = "java/springboot"
        elif "python" in fn or "python" in sn or "core" in fn or "core" in sn or "basic" in fn or "basic" in sn:
            tech_stack = "python/core"

    if not tech_stack:
        raise ValueError(
            f"\n❌ [LỖI KHÔNG THỂ XÁC ĐỊNH CÔNG NGHỆ] Không thể tự động gán Technology Stack cho file PM '{excel_path}'.\n"
            f"Hệ thống ĐÃ TẮT HOÀN TOÀN CƠ CHẾ FALLBACK MẶC ĐỊNH để tránh rò rỉ công nghệ (Technology Leak).\n"
            f"Vui lòng truyền tham số --tech-stack chính xác khi chạy command.\n"
            f"Ví dụ: python main.py --pm \"{excel_path}\" --tech-stack python/core --approve-pm"
        )

    print(f"Detected course technology stack: {tech_stack}")

    if not args.approve_pm:
        print("\n=========================================")
        print(">>> Giai đoạn 0: Thẩm định PM Input <<<")
        print("=========================================")
        from agents.reviewer_agents import pm_reviewer_agent
        full_curriculum_json = json.dumps(sessions, ensure_ascii=False)
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

    initialize_skeleton_structure(sessions, course_dir, requested_parts, args.session.strip().lower())
    project_structure_reviewer_agent(sessions, course_dir, requested_parts, args.session.strip().lower())

    summary = []

    for session in sessions:
        session_id = session["session_id"]
        session_title = session.get("title", "")

        if "all" not in requested_sessions and not any(rs in session_id.lower() for rs in requested_sessions):
            continue

        print(f"\n=====================================================================")
        print(f"PROCESSING SESSION: {session_id} - {session_title}")
        print(f"=====================================================================")

        is_project_or_hackathon = any(kw in session_title.lower() for kw in ["hackathon", "project", "đồ án", "dự án", "mini project"])
        is_practice = "thực hành" in session_title.lower()

        if is_project_or_hackathon or is_practice:
            print(f"\n  ---> Processing Session-Level: {session_id} - {session_title}")
            
            if args.approve_pm:
                session_dir = get_or_rename_sanitized_folder(course_dir, session_id, format_full_folder_name(session_id, session_title))
                session_dir.mkdir(parents=True, exist_ok=True)
                
                previous_lessons_text = ""
                for s in sessions:
                    if s["session_id"] == session_id:
                        break
                    for l in s.get("lessons", []):
                        previous_lessons_text += f"- {l['lesson_id']}: {l['title']} ({l.get('details', '')})\n"
                
                if is_project_or_hackathon:
                    print(f"  [Project/Hackathon] Generating Mini Project templates via Agent for: {session_title}")
                    from agents.project_agents import generate_mini_project_session
                    generate_mini_project_session(
                        session_id=session_id,
                        session_title=session_title,
                        session_dir_path=str(session_dir),
                        tech_stack=tech_stack,
                        previous_lessons_text=previous_lessons_text,
                        session_info=session
                    )
                elif is_practice:
                    print(f"  [Practice] Generating practice exercises via Agent for: {session_title}")
                    from agents.practice_agents import generate_practice_session_exercises
                    generate_practice_session_exercises(
                        session_id=session_id,
                        session_title=session_title,
                        session_dir_path=str(session_dir),
                        tech_stack=tech_stack,
                        previous_lessons_text=previous_lessons_text
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
            for idx, lesson in enumerate(session["lessons"]):
                lesson_id = lesson["lesson_id"]
                lesson_title = lesson["title"]
                lesson_details = lesson.get("details", "")
                expected_output = lesson.get("expected_output", "")

                print(f"\n  ---> Processing: {session_id} - {lesson_id}: {lesson_title}")
                
                state: AgentState = {
                    "session_id": session_id,
                    "lesson_id": lesson_id,
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

                    if "slide" in requested_parts and final_state.get("slide_markdown"):
                        slide_sub = lesson_dir / "Bài giảng"
                        slide_sub.mkdir(parents=True, exist_ok=True)
                        slides_path = slide_sub / "slides.md"
                        with open(slides_path, "w", encoding="utf-8") as f:
                            f.write(final_state.get("slide_markdown", ""))
                    else:
                        slides_path = "Skipped"

                    if "quiz" in requested_parts and final_state.get("quiz_json"):
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
                        quiz_items = final_state.get("quiz_json", {}).get("lesson_quiz") or final_state.get("quiz_json", {}).get("quiz") or []
                        export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                        quiz_reported_path = str(excel_path_file)
                    else:
                        quiz_reported_path = "Skipped"

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
                        "slides_file": str(slides_path),
                        "quiz_file": quiz_reported_path,
                        "video_script_file": str(video_script_path),
                        "mindmap_file": str(mindmap_path),
                        "status": final_state.get("artifacts_status", {}).get("session", "FAILED"),
                        "review_count": len(final_state.get("review_logs", []))
                    })

                    previous_lessons.append({
                        "lesson_id": lesson_id,
                        "title": lesson_title,
                        "html_summary": final_state.get("html_content", "")[:200]
                    })

                except Exception as e:
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

                if "slide" in requested_parts and final_state.get("slide_markdown"):
                    slide_sub = session_dir / "Bài giảng"
                    slide_sub.mkdir(parents=True, exist_ok=True)
                    slides_path = slide_sub / "slides.md"
                    with open(slides_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("slide_markdown", ""))
                else:
                    slides_path = "Skipped"

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
                    quiz_items = final_state.get("quiz_json", {}).get("lesson_quiz") or final_state.get("quiz_json", {}).get("quiz") or []
                    export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                    quiz_reported_path = str(excel_path_file)
                else:
                    quiz_reported_path = "Skipped"

                if ("video" in requested_parts or "video_script" in requested_parts) and final_state.get("video_script_markdown"):
                    video_sub = session_dir / "Kịch bản video"
                    video_sub.mkdir(parents=True, exist_ok=True)
                    video_script_path = video_sub / "video_script.md"
                    with open(video_script_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("video_script_markdown", ""))
                else:
                    video_script_path = "Skipped"

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
                    session_lessons_text = f"Kiến thức tổng quan của buổi học: {session_title}"
                    if session.get("lessons"):
                        for idx, lesson in enumerate(session.get("lessons", [])):
                            session_lessons_text += f"\n- {lesson['lesson_id']}: {lesson['title']} ({lesson.get('details', '')})"
                    
                    from agents.homework_agents import generate_session_homework
                    generate_session_homework(
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
            
            entrance_path = session_dir / f"{session_num_str}._Quizz_Dau_Gio_{sanitized_slide_title}.xlsx"
            exit_path = session_dir / f"{session_num_str}._Quizz_Cuoi_Gio_{sanitized_slide_title}.xlsx"
            
            from core.quiz_engine import generate_entrance_quiz, generate_exit_quiz
            from core.quiz_excel import export_quiz_to_excel
            from agents.creator_agents import get_base_topic_key
            
            current_topic = get_base_topic_key(session_id)
            
            def get_previous_session_id(s_id: str) -> str:
                match = re.search(r'\d+', s_id)
                if match:
                    num = int(match.group(0))
                    if num > 1:
                        return f"Session {num-1:02d}"
                return "Session 01"
                
            previous_session_id = get_previous_session_id(session_id)
            previous_topic = get_base_topic_key(previous_session_id)
            
            entrance_qs = generate_entrance_quiz(session_id, current_topic, previous_topic, tech_stack)
            exit_qs = generate_exit_quiz(session_id, current_topic, tech_stack)
            
            export_quiz_to_excel(entrance_qs, str(entrance_path))
            export_quiz_to_excel(exit_qs, str(exit_path))

    print_generation_summary(summary)

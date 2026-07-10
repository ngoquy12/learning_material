import sys
import io
import os
import json
import openpyxl
from pathlib import Path
from core.state import AgentState
from core.graph import compile_learning_content_workflow

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', write_through=True)

def parse_all_sessions(excel_path: str):
    """
    Parses all sessions and their corresponding lessons
    from the PM software engineering spreadsheet.
    """
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    
    sessions = []
    current_session = None
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        stt, form, session_val, content_val, lesson_val, details_val, output_val, deadline = row[:8]
        
        # If a new Session is found
        if session_val and str(session_val).strip().startswith("Session"):
            session_id = session_val.strip()
            # Check if we already have it
            existing = [s for s in sessions if s["session_id"] == session_id]
            if existing:
                current_session = existing[0]
            else:
                current_session = {
                    "session_id": session_id,
                    "title": content_val.strip() if content_val else "",
                    "lessons": []
                }
                sessions.append(current_session)
            
        # Add lessons under the current session
        if lesson_val and str(lesson_val).strip().startswith("Lesson") and current_session:
            current_session["lessons"].append({
                "lesson_id": lesson_val.strip().split(":")[0].strip(),
                "title": lesson_val.strip().split(":", 1)[1].strip() if ":" in str(lesson_val) else str(lesson_val).strip(),
                "details": details_val.strip() if details_val else "",
                "expected_output": output_val.strip() if output_val else ""
            })
            
    return sessions

def main():
    print("=====================================================================")
    print("Starting Multi-Agent Learning Content Factory (Antigravity Workflow)")
    print("=====================================================================")

    import argparse
    parser = argparse.ArgumentParser(description="Multi-Agent Learning Content Factory")
    parser.add_argument("--pm", type=str, default=r"d:\Rikkei Education\Elearning_Agent\Learning-Material\pms\PM_RA_PTIT_2025_Software_Engineer_Python_Web.xlsx", help="Path to PM Excel sheet")
    parser.add_argument("--session", type=str, default="all", help="Session ID to run (e.g. 'Session 01', 'Session 02', or 'all')")
    parser.add_argument("--parts", type=str, default="all", help="Comma-separated parts to generate (html,slide,quiz,video,mindmap or all)")
    parser.add_argument("--force", action="store_true", help="Force rebuild artifacts even if already approved in checkpoint")
    parser.add_argument("--obsidian", action="store_true", help="Generate Obsidian Vault for the entire course structure")
    args = parser.parse_args()

    excel_path = args.pm
    if not os.path.exists(excel_path):
        print(f"Error: Excel PM file not found at {excel_path}")
        return

    if args.obsidian:
        from core.obsidian_exporter import generate_obsidian_vault
        generate_obsidian_vault(excel_path)
        return

    requested_parts = [p.strip().lower() for p in args.parts.split(",")] if args.parts != "all" else ["html", "slide", "quiz", "video", "mindmap"]
    requested_session = args.session.strip().lower()

    print(f"Loading spreadsheet: {excel_path}")
    sessions = parse_all_sessions(excel_path)
    print(f"Successfully loaded {len(sessions)} sessions from spreadsheet.")

    # Compile the workflow graph
    workflow = compile_learning_content_workflow()

    # Create output base directory
    output_base_dir = Path("output")
    output_base_dir.mkdir(exist_ok=True)

    # Get course directory name dynamically from the active sheet title of PM Excel
    wb = openpyxl.load_workbook(excel_path)
    course_dir_name = wb.active.title.strip().replace(" ", "_").replace("-", "_")
    course_dir = output_base_dir / course_dir_name
    course_dir.mkdir(parents=True, exist_ok=True)

    # Detect technology stack dynamically
    tech_stack = "python/fastapi"
    fn = os.path.basename(excel_path).lower()
    sn = course_dir_name.lower()
    if "nestjs" in fn or "nestjs" in sn or "nest" in fn or "nest" in sn:
        tech_stack = "typescript/nestjs"
    elif "react" in fn or "react" in sn:
        tech_stack = "typescript/react"
    elif "java" in fn or "java" in sn or "springboot" in fn or "springboot" in sn:
        tech_stack = "java/springboot"
    elif "core" in fn or "core" in sn or "basic" in fn or "basic" in sn:
        tech_stack = "python/core"
    print(f"Detected course technology stack: {tech_stack}")

    summary = []

    for session in sessions:
        session_id = session["session_id"]
        session_title = session["title"]

        if requested_session != "all" and requested_session not in session_id.lower():
            continue

        print(f"\n=====================================================================")
        print(f"PROCESSING SESSION: {session_id} - {session_title}")
        print(f"=====================================================================")

        # If session has lessons, loop and process each lesson
        if session["lessons"]:
            previous_lessons = []
            for lesson in session["lessons"]:
                lesson_id = lesson["lesson_id"]
                lesson_title = lesson["title"]
                lesson_details = lesson["details"]
                expected_output = lesson["expected_output"]
                
                print(f"\n  ---> Processing: {session_id} - {lesson_id}: {lesson_title}")
                
                # Initialize state for this specific lesson
                state: AgentState = {
                    "session_id": session_id,
                    "lesson_id": lesson_id,
                    "pm_input": json.dumps(lesson, ensure_ascii=False),
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
                    "force_rebuild": args.force
                }

                # Run the workflow graph for this lesson
                final_state = workflow.run(state)
                
                # Append to previous_lessons for next iteration
                previous_lessons.append({
                    "lesson_id": lesson_id,
                    "title": lesson_title,
                    "details": lesson_details,
                    "expected_output": expected_output
                })

                # Write output files to output/<course_name>/session_xx/lesson_yy/
                lesson_dir = course_dir / session_id.lower().replace(" ", "_") / lesson_id.lower().replace(" ", "_")
                lesson_dir.mkdir(parents=True, exist_ok=True)

                # Save HTML Reading to "Bài đọc" subfolder
                if "html" in requested_parts and final_state.get("html_content"):
                    html_sub = lesson_dir / "Bài đọc"
                    html_sub.mkdir(parents=True, exist_ok=True)
                    html_path = html_sub / "reading.html"
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("html_content", ""))
                else:
                    html_path = "Skipped"

                # Save Slides to "Bài giảng" subfolder
                if "slide" in requested_parts and final_state.get("slide_markdown"):
                    slide_sub = lesson_dir / "Bài giảng"
                    slide_sub.mkdir(parents=True, exist_ok=True)
                    slides_path = slide_sub / "slides.md"
                    with open(slides_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("slide_markdown", ""))
                else:
                    slides_path = "Skipped"

                # Save Quiz to "Câu hỏi Quizz" subfolder (Excel strictly following Format_Quizz_Lesson.xlsx + JSON)
                if "quiz" in requested_parts and final_state.get("quiz_json"):
                    quiz_sub = lesson_dir / "Câu hỏi Quizz"
                    quiz_sub.mkdir(parents=True, exist_ok=True)
                    quiz_path = quiz_sub / "quiz.json"
                    with open(quiz_path, "w", encoding="utf-8") as f:
                        json.dump(final_state.get("quiz_json", {}), f, indent=2, ensure_ascii=False)
                    
                    from core.quiz_excel import export_lesson_quiz_to_excel
                    import re
                    sanitized_lesson_title = re.sub(r'[\s\-\:\,\.\?\!\(\)]+', '_', lesson_title)
                    sanitized_lesson_title = re.sub(r'^_+|_+$', '', sanitized_lesson_title)
                    s_num_str = session_id.replace(" ", "")
                    l_num_str = lesson_id.replace(" ", "")
                    excel_filename = f"Quizz_{s_num_str}_{l_num_str}_{sanitized_lesson_title}.xlsx"
                    excel_path = quiz_sub / excel_filename
                    
                    quiz_items = final_state.get("quiz_json", {}).get("lesson_quiz") or final_state.get("quiz_json", {}).get("quiz") or []
                    export_lesson_quiz_to_excel(quiz_items, str(excel_path))
                    quiz_reported_path = str(excel_path)
                else:
                    quiz_reported_path = "Skipped"

                # Save Video Script to "Kịch bản video" subfolder
                if ("video" in requested_parts or "video_script" in requested_parts) and final_state.get("video_script_markdown"):
                    video_sub = lesson_dir / "Kịch bản video"
                    video_sub.mkdir(parents=True, exist_ok=True)
                    video_script_path = video_sub / "video_script.md"
                    with open(video_script_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("video_script_markdown", ""))
                else:
                    video_script_path = "Skipped"

                # Save Mindmap MD to "Mindmap" subfolder
                if "mindmap" in requested_parts and final_state.get("mindmap_markdown"):
                    mindmap_sub = lesson_dir / "Mindmap"
                    mindmap_sub.mkdir(parents=True, exist_ok=True)
                    mindmap_path = mindmap_sub / "mindmap.md"
                    with open(mindmap_path, "w", encoding="utf-8") as f:
                        f.write(final_state.get("mindmap_markdown", ""))
                else:
                    mindmap_path = "Skipped"

                print(f"  [Publisher] Saved learning assets to {lesson_dir}/")
                
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
            
            # Compile session-level unified HTML and Mindmap
            from core.session_compilers import compile_session_html, compile_session_mindmap
            s_dir = course_dir / session_id.lower().replace(" ", "_")
            full_session_name = f"{session_id} - {session_title}"
            if "html" in requested_parts:
                compile_session_html(s_dir, full_session_name)
            if "mindmap" in requested_parts:
                compile_session_mindmap(s_dir, full_session_name)
        else:
            # Session-level fallback for sessions without sub-lessons (e.g. practical/lab session)
            print(f"\n  ---> Processing Session-Level practice: {session_id} - {session_title}")
            
            # Initialize state for this specific session
            state: AgentState = {
                "session_id": session_id,
                "lesson_id": "",
                "pm_input": json.dumps(session, ensure_ascii=False),
                "time_reference": {
                    "weeks": 1,
                    "hours_per_week": 10
                },
                "learning_outcomes": {},
                "program_structure": {},
                "core_ssot": {
                    "session_title": session_title,
                    "lesson_details": "",
                    "expected_output": ""
                },
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
                "requested_parts": requested_parts
            }

            # Run the workflow graph
            final_state = workflow.run(state)

            # Write output files to output/<course_name>/session_xx/
            session_dir = course_dir / session_id.lower().replace(" ", "_")
            session_dir.mkdir(parents=True, exist_ok=True)

            # Save HTML Reading to "Bài đọc" subfolder
            if "html" in requested_parts and final_state.get("html_content"):
                html_sub = session_dir / "Bài đọc"
                html_sub.mkdir(parents=True, exist_ok=True)
                html_path = html_sub / "reading.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(final_state.get("html_content", ""))
            else:
                html_path = "Skipped"

            # Save Slides to "Bài giảng" subfolder
            if "slide" in requested_parts and final_state.get("slide_markdown"):
                slide_sub = session_dir / "Bài giảng"
                slide_sub.mkdir(parents=True, exist_ok=True)
                slides_path = slide_sub / "slides.md"
                with open(slides_path, "w", encoding="utf-8") as f:
                    f.write(final_state.get("slide_markdown", ""))
            else:
                slides_path = "Skipped"

            # Save Quiz to "Câu hỏi Quizz" subfolder
            if "quiz" in requested_parts and final_state.get("quiz_json"):
                quiz_sub = session_dir / "Câu hỏi Quizz"
                quiz_sub.mkdir(parents=True, exist_ok=True)
                quiz_path = quiz_sub / "quiz.json"
                with open(quiz_path, "w", encoding="utf-8") as f:
                    json.dump(final_state.get("quiz_json", {}), f, indent=2, ensure_ascii=False)
                from core.quiz_excel import export_lesson_quiz_to_excel
                s_num_str = session_id.replace(" ", "")
                excel_filename = f"Quizz_{s_num_str}_Thuc_hanh.xlsx"
                excel_path = quiz_sub / excel_filename
                quiz_items = final_state.get("quiz_json", {}).get("lesson_quiz") or final_state.get("quiz_json", {}).get("quiz") or []
                export_lesson_quiz_to_excel(quiz_items, str(excel_path))
                quiz_reported_path = str(excel_path)
            else:
                quiz_reported_path = "Skipped"

            # Save Video Script to "Kịch bản video" subfolder
            if ("video" in requested_parts or "video_script" in requested_parts) and final_state.get("video_script_markdown"):
                video_sub = session_dir / "Kịch bản video"
                video_sub.mkdir(parents=True, exist_ok=True)
                video_script_path = video_sub / "video_script.md"
                with open(video_script_path, "w", encoding="utf-8") as f:
                    f.write(final_state.get("video_script_markdown", ""))
            else:
                video_script_path = "Skipped"

            # Save Mindmap MD to "Mindmap" subfolder
            if "mindmap" in requested_parts and final_state.get("mindmap_markdown"):
                mindmap_sub = session_dir / "Mindmap"
                mindmap_sub.mkdir(parents=True, exist_ok=True)
                mindmap_path = mindmap_sub / "mindmap.md"
                with open(mindmap_path, "w", encoding="utf-8") as f:
                    f.write(final_state.get("mindmap_markdown", ""))
            else:
                mindmap_path = "Skipped"

            print(f"  [Publisher] Saved learning assets to {session_dir}/")
            
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

        # Generate and save Session Quizzes (Entrance & Exit) in .xlsx format
        if "quiz" in requested_parts:
            print(f"  ---> Generating Session-Level Quizzes (Entrance & Exit) for {session_id}...")
            import re
            
            # Determine slide_title (first lesson's title if present, otherwise session title)
            slide_title = session["lessons"][0]["title"] if session["lessons"] else session_title
            
            # Sanitized titles for filename
            def get_sanitized_title(title: str) -> str:
                sanitized = re.sub(r'[\s\-\:\,\.\?\!\(\)]+', '_', title)
                sanitized = re.sub(r'^_+|_+$', '', sanitized)
                return sanitized
                
            session_num_str = session_id.replace(" ", "")
            sanitized_slide_title = get_sanitized_title(slide_title)
            
            # Paths
            session_dir = course_dir / session_id.lower().replace(" ", "_")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            entrance_path = session_dir / f"{session_num_str}._Quizz_Dau_Gio_{sanitized_slide_title}.xlsx"
            exit_path = session_dir / f"{session_num_str}._Quizz_Cuoi_Gio_{sanitized_slide_title}.xlsx"
            
            # Import generators
            from core.quiz_engine import generate_entrance_quiz, generate_exit_quiz
            from core.quiz_excel import export_quiz_to_excel
            from agents.creator_agents import get_base_topic_key
            
            # Current topic key
            current_topic = get_base_topic_key(session_id)
            
            # Previous topic key
            def get_previous_session_id(s_id: str) -> str:
                match = re.search(r'\d+', s_id)
                if match:
                    num = int(match.group(0))
                    if num > 1:
                        return f"Session {num-1:02d}"
                return "Session 01"
                
            previous_session_id = get_previous_session_id(session_id)
            previous_topic = get_base_topic_key(previous_session_id)
            
            # Generate quizzes
            entrance_qs = generate_entrance_quiz(session_id, current_topic, previous_topic, tech_stack)
            exit_qs = generate_exit_quiz(session_id, current_topic, tech_stack)
            
            # Export to Excel
            export_quiz_to_excel(entrance_qs, str(entrance_path))
            export_quiz_to_excel(exit_qs, str(exit_path))
            print(f"  [Publisher] Saved Entrance Quiz: {entrance_path.name}")
            print(f"  [Publisher] Saved Exit Quiz:     {exit_path.name}")

    print("\n=====================================================================")
    print("ALL SESSIONS COMPILED! FINAL GENERATION REPORT:")
    print("=====================================================================")
    for s in summary:
        lbl = f"{s['session_id']} - {s['lesson_id']}" if s['lesson_id'] else s['session_id']
        print(f"Unit: {lbl} - {s['title']}")
        print(f"  - Status: {s['status']}")
        print(f"  - Critique Reviews Attempted: {s['review_count']}")
        print(f"  - HTML Reading: {s['html_file']}")
        print(f"  - Slide Deck:   {s['slides_file']}")
        print(f"  - Quiz JSON:    {s['quiz_file']}")
        print(f"  - Video Script: {s['video_script_file']}")
        print(f"  - Mindmap MD:   {s['mindmap_file']}")
        print()

if __name__ == "__main__":
    main()
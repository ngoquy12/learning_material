import os
import sys
import io
from pathlib import Path
import openpyxl
from core.session_compilers import compile_session_html

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', write_through=True)

def parse_all_sessions(excel_path: str):
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    
    sessions = []
    current_session = None
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        stt, form, session_val, content_val, lesson_val, details_val, output_val, deadline = row[:8]
        
        if session_val and str(session_val).strip().startswith("Session"):
            session_id = session_val.strip()
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
            
        if lesson_val and str(lesson_val).strip().startswith("Lesson") and current_session:
            current_session["lessons"].append({
                "lesson_id": lesson_val.strip().split(":")[0].strip(),
                "title": lesson_val.strip().split(":", 1)[1].strip() if ":" in str(lesson_val) else str(lesson_val).strip()
            })
            
    return sessions

def main():
    excel_path = r"pms\PM_Python_Core_Synchronized.xlsx"
    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found.")
        return

    sessions = parse_all_sessions(excel_path)
    course_dir = Path("output/PM_Python_Core_Synchronized")
    
    print(f"Starting recompilation of all HTML readings in {course_dir}...")
    for session in sessions:
        session_id = session["session_id"]
        session_title = session["title"]
        s_dir = course_dir / session_id.lower().replace(" ", "_")
        
        if s_dir.exists():
            print(f"\nRecompiling Session: {session_id} - {session_title}")
            compile_session_html(s_dir, session_title)
        else:
            print(f"Skipping {session_id} (directory does not exist)")

if __name__ == "__main__":
    main()

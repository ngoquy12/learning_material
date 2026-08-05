"""
core/pm_parser.py

PM Excel Parser Engine for Elearning Agent Framework.
Reads standard 9-column PM Excel templates (with merged cells & ffill forward-fill),
parses ORIENTATION, THEORY, PRACTICE, MINI_PROJECT, and FINAL_PROJECT sessions,
and builds a standardized Syllabus Dict.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Union
import openpyxl

def parse_pm_excel(excel_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Parses a 9-column PM Excel file into a normalized Syllabus Dict.
    Applies forward-fill (ffill) algorithm to handle merged cells automatically.
    """
    excel_path = Path(excel_path)
    if not excel_path.exists():
        raise FileNotFoundError(f"Tệp PM Excel không tồn tại: {excel_path}")

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active

    raw_rows = list(ws.iter_rows(values_only=True))
    if not raw_rows or len(raw_rows) < 2:
        raise ValueError("Tệp PM Excel bị trống hoặc không chứa dòng dữ liệu.")

    header_row = [str(cell).strip() if cell is not None else "" for cell in raw_rows[0]]

    # Normalized sessions accumulator
    sessions_dict: Dict[str, Dict[str, Any]] = {}
    
    # Tracking variables for ffill algorithm
    curr_session_id = ""
    curr_session_type_vn = ""
    curr_session_code = ""
    curr_session_title = ""

    for r_idx, row in enumerate(raw_rows[1:], start=2):
        cell_vals = [str(cell).strip() if cell is not None else "" for cell in row]
        if not any(cell_vals):
            continue

        # Extract 9 columns safely
        val_session_id = cell_vals[0] if len(cell_vals) > 0 else ""
        val_type_vn = cell_vals[1] if len(cell_vals) > 1 else ""
        val_code = cell_vals[2] if len(cell_vals) > 2 else ""
        val_title = cell_vals[3] if len(cell_vals) > 3 else ""
        val_lesson = cell_vals[4] if len(cell_vals) > 4 else ""
        val_details = cell_vals[5] if len(cell_vals) > 5 else ""
        val_forbidden = cell_vals[6] if len(cell_vals) > 6 else ""
        val_allowed = cell_vals[7] if len(cell_vals) > 7 else ""
        val_tech_stack = cell_vals[8] if len(cell_vals) > 8 else ""

        # Apply forward-fill (ffill) for merged cells
        if val_session_id:
            curr_session_id = val_session_id
        if val_type_vn:
            curr_session_type_vn = val_type_vn
        if val_code:
            curr_session_code = val_code
        if val_title:
            curr_session_title = val_title

        if not curr_session_id:
            continue

        # Normalize Session Code enum
        code_upper = curr_session_code.upper().strip()
        if not code_upper:
            if "THỰC HÀNH" in curr_session_type_vn.upper():
                code_upper = "PRACTICE"
            elif "MINI" in curr_session_type_vn.upper():
                code_upper = "MINI_PROJECT"
            elif "CUỐI KHÓA" in curr_session_type_vn.upper() or "CAPSTONE" in curr_session_type_vn.upper():
                code_upper = "FINAL_PROJECT"
            elif "ORIENTATION" in curr_session_type_vn.upper() or "ĐỊNH HƯỚNG" in curr_session_type_vn.upper():
                code_upper = "ORIENTATION"
            else:
                code_upper = "THEORY"

        if curr_session_id not in sessions_dict:
            sessions_dict[curr_session_id] = {
                "session_id": curr_session_id,
                "session_code": code_upper,
                "session_type_vn": curr_session_type_vn,
                "session_title": curr_session_title,
                "lessons": []
            }

        if val_lesson:
            lesson_entry = {
                "lesson_title": val_lesson,
                "title": val_lesson,
                "details": val_details,
                "description": val_details,
                "forbidden_scope": val_forbidden,
                "allowed_scope": val_allowed,
                "expected_output": val_allowed,
                "tech_stack": val_tech_stack
            }
            sessions_dict[curr_session_id]["lessons"].append(lesson_entry)

    # Build final normalized output
    syllabus_list = list(sessions_dict.values())
    
    # Calculate Course Metadata
    tech_stack_master = "Python 3.12"
    for s in syllabus_list:
        for l in s.get("lessons", []):
            if l.get("tech_stack"):
                tech_stack_master = l.get("tech_stack")
                break

    return {
        "course_title": syllabus_list[0]["session_title"].split("-")[0].strip() if syllabus_list else "Môn học",
        "tech_stack": tech_stack_master,
        "total_sessions": len(syllabus_list),
        "sessions": syllabus_list
    }

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    sample_excel = Path(__file__).resolve().parent.parent / "templates" / "PM_Template_Standard.xlsx"
    parsed = parse_pm_excel(sample_excel)
    print("--- PARSED PM EXCEL SYLLABUS SUMMARY ---")
    print(f"Total Sessions: {parsed['total_sessions']}")
    for s in parsed["sessions"]:
        print(f"[{s['session_code']}] {s['session_id']} - {s['session_title']} ({len(s['lessons'])} lessons)")

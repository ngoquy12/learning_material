import openpyxl

def export_updated_pm_to_excel(sessions_json, original_excel_path, new_excel_path):
    """
    Writes the updated sessions JSON back into a new Excel file.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Chương trình đào tạo chi tiết"
    
    # Headers
    ws.append(["STT", "Hình thức", "Session", "Nội dung Session", "Lesson", "Chi tiết bài học", "Kết quả đầu ra", "Deadline"])
    
    stt = 1
    for session in sessions_json:
        session_id = session.get("session_id", "")
        session_title = session.get("title", "")
        
        lessons = session.get("lessons", [])
        if not lessons:
            # Session-level practice/hackathon with no lessons
            ws.append([stt, "Thực hành", session_id, session_title, "", "", "", ""])
            stt += 1
            continue
            
        for lesson in lessons:
            lesson_id = lesson.get("lesson_id", "")
            lesson_title = lesson.get("title", "")
            details = lesson.get("details", "")
            expected_output = lesson.get("expected_output", "")
            
            # Determine form
            form = "Thực hành" if ("thực hành" in lesson_title.lower() or "thực hành" in session_title.lower() or "project" in session_title.lower()) else "Lý thuyết"
            
            # Combine lesson_id and title
            lesson_full = f"{lesson_id}: {lesson_title}" if lesson_title else lesson_id
            
            ws.append([stt, form, session_id, session_title, lesson_full, details, expected_output, ""])
            stt += 1
            
    wb.save(new_excel_path)

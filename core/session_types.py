"""
core/session_types.py
Standardized Session Types & Deliverables Schema for Elearning Agent Framework.

Supported Session Types & Deliverables:
1. THEORY (Session Lý Thuyết):
   - Per-Lesson: Interactive Reading HTML, Slide HTML, Lesson Labs (3-5 exercises)
   - Per-Session: Entry Quiz, Session Comprehensive Practice (5 large exercises), Session Quiz Excel (.xlsx), Session Homework, reading_all.html, session_slides.html, Hyperframes Narration Script
2. PRACTICE (Session Thực Hành):
   - Practice Labs (Basic -> Advanced), Homework, Data Tasks
3. MINI_PROJECT (Session Mini Project):
   - 4 Entry Tests, SRS Spec, Mini Project Prompt & Rubric (100 pts)
4. FINAL_PROJECT (Session Dự Án Cuối Khóa):
   - Capstone Spec, Full SRS, System Architecture, Capstone Rubric (100 pts)
"""

from enum import Enum
from typing import Dict, Any, List

class SessionType(str, Enum):
    THEORY = "THEORY"
    PRACTICE = "PRACTICE"
    MINI_PROJECT = "MINI_PROJECT"
    FINAL_PROJECT = "FINAL_PROJECT"

# Full list of deliverables mapped per session type
SESSION_DELIVERABLES: Dict[SessionType, List[str]] = {
    SessionType.THEORY: [
        "1. Bài đọc HTML tương tác (Per-Lesson)",
        "2. Slide bài giảng HTML + Narration Script (Per-Lesson)",
        "3. Bài thực hành cho từng Lesson (Số lượng linh hoạt theo nội dung trọng tâm)",
        "4. Quiz trắc nghiệm cho từng Lesson (Đúng 5 câu / Lesson)",
        "5. Bài kiểm tra trắc nghiệm đầu giờ (Entry Quiz / Đúng 45 câu Excel .xlsx)",
        "6. Bài kiểm tra trắc nghiệm cuối giờ (Exit Quiz / Đúng 45 câu Excel .xlsx)",
        "7. Bài tập về nhà Session (5 bài tập phân 5 cấp độ + 1 bài tập tổng hợp)",
        "8. File gộp bài đọc Session (reading_all.html)",
        "9. File gộp Slide Session (session_slides.html)",
        "10. Kịch bản lời giảng Video (Hyperframes Script)"
    ],
    SessionType.PRACTICE: [
        "1. Bộ bài tập thực hành phân cấp (Phân loại Nhận biết -> Vận dụng cao)",
        "2. Bài tập thực hành xử lý dữ liệu thực tế",
        "3. Bài tập về nhà (Session Homework + Lời giải mẫu AST check)",
        "4. Kịch bản kiểm tra trạng thái bài tập"
    ],
    SessionType.MINI_PROJECT: [
        "1. 4 Bài kiểm tra đầu giờ (Entry Tests)",
        "2. Tài liệu đặc tả yêu cầu phần mềm SRS tinh gọn",
        "3. Đề bài Mini Project (Task Cards)",
        "4. Thang điểm Rubric chấm AI (Đúng 100 điểm)"
    ],
    SessionType.FINAL_PROJECT: [
        "1. Đề tài Đồ án Capstone cuối khóa",
        "2. Sơ đồ Kiến trúc hệ thống tổng thể & CSDL",
        "3. Tài liệu đặc tả yêu cầu phần mềm SRS đầy đủ",
        "4. Thang điểm Rubric chấm Đồ án tốt nghiệp (Đúng 100 điểm)",
        "5. Hướng dẫn báo cáo & Trình chiếu bảo vệ Đồ án"
    ]
}

# Standardized exact quantity parameters
SESSION_QUANTITIES: Dict[str, int] = {
    "LESSON_QUIZ_COUNT": 5,
    "ENTRY_QUIZ_COUNT": 45,
    "EXIT_QUIZ_COUNT": 45,
    "HOMEWORK_LEVEL_COUNT": 5,
    "HOMEWORK_COMPREHENSIVE_COUNT": 1,
    "TOTAL_HOMEWORK_COUNT": 6
}

def detect_session_type(session_data: Dict[str, Any]) -> SessionType:
    """
    Detects the explicit SessionType based on session title, type field, or metadata.
    """
    explicit_type = str(session_data.get("session_type", "")).upper().strip()
    if explicit_type in SessionType.__members__:
        return SessionType[explicit_type]
        
    title = str(session_data.get("session_title", "") or session_data.get("title", "")).lower()
    
    if any(kw in title for kw in ["dự án cuối khóa", "capstone", "final project", "đồ án cuối môn"]):
        return SessionType.FINAL_PROJECT
    elif any(kw in title for kw in ["mini project", "mini-project", "tiểu luận"]):
        return SessionType.MINI_PROJECT
    elif any(kw in title for kw in ["thực hành", "practice", "lab", "luyện tập"]):
        return SessionType.PRACTICE
        
    return SessionType.THEORY

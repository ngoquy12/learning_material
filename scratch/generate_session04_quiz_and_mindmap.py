# scratch/generate_session04_quiz_and_mindmap.py
import sys
import os
import json
from pathlib import Path

# Ensure workspace root is in sys.path
workspace_root = Path(__file__).resolve().parent.parent
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

from agents.session_mindmap_agent import generate_session_mindmap
from core.quiz_engine import (
    generate_entrance_quiz,
    generate_exit_quiz,
    extract_15_question_entrance_exam,
    extract_15_question_exit_exam,
    StudentClassifier
)
from core.quiz_excel import export_quiz_to_excel

def main():
    session_id = "Session 04"
    session_title = "Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python"
    tech_stack = "python"
    
    session_dir = workspace_root / "output" / "pms" / "Lập_trình_Python" / "Session 04 - Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python"
    session_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"=== GENERATING SESSION 04 RESOURCES FOR: {session_dir.name} ===")
    
    # 1. Generate Session Mindmap
    print("\n--- 1. Generating Session Mindmap ---")
    lessons_summary_text = """
    - Lesson 01: Toán tử Số học ( cộng +, trừ -, nhân *, chia /, chia nguyên //, chia lấy dư %, lũy thừa **) và Toán tử Gán (=, +=, -=, *=, /=).
    - Lesson 02: Cơ chế so sánh (==, !=, >, <, >=, <=) và Biểu thức logic Boolean (True, False, bool()).
    - Lesson 03: Ứng dụng toán tử logic (and, or, not) và Thứ tự ưu tiên tính toán (Precedence rules).
    """
    
    mindmap_content = generate_session_mindmap(
        session_id=session_id,
        session_title=session_title,
        session_dir_path=str(session_dir),
        tech_stack=tech_stack,
        previous_lessons_text=lessons_summary_text
    )
    print("✓ Session 04 Mindmap generated successfully!")
    
    # 2. Generate Session Quizzes
    print("\n--- 2. Generating Session 04 Entrance & Exit Quizzes ---")
    quiz_dir = session_dir / "Câu hỏi Quizz"
    quiz_dir.mkdir(parents=True, exist_ok=True)
    
    previous_topic = "Thực hành Tổng hợp Cấu hình Môi trường, Nhập xuất và Biến số Python"
    current_topic = "Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python"
    allowed_scope = "Toán tử số học, toán tử gán, biểu thức so sánh, toán tử logic and/or/not, thứ tự ưu tiên"
    forbidden_scope = "cấu trúc rẽ nhánh if/else, vòng lặp for/while, danh sách list, hàm function, OOP class"
    
    # Entrance Quiz (45 questions)
    print("\n[Quiz Engine] Generating Entrance Quiz Bank (45 questions)...")
    entrance_bank_45 = generate_entrance_quiz(
        session_id=session_id,
        current_topic=current_topic,
        previous_topic=previous_topic,
        tech_stack=tech_stack,
        forbidden_scope=forbidden_scope,
        allowed_scope=allowed_scope
    )
    
    # Export Entrance Bank 45 JSON & Excel
    entrance_bank_json_path = quiz_dir / "entrance_quiz_bank_45.json"
    with open(entrance_bank_json_path, "w", encoding="utf-8") as f:
        json.dump(entrance_bank_45, f, ensure_ascii=False, indent=2)
        
    entrance_bank_excel_path = quiz_dir / "Quizz_Dau_Gio_Ngan_Hang_45_Cau.xlsx"
    export_quiz_to_excel(entrance_bank_45, str(entrance_bank_excel_path))
    print(f"  ✓ Saved Entrance Quiz Bank 45: {entrance_bank_excel_path.name}")
    
    # Entrance Exam (15 questions)
    entrance_exam_15 = extract_15_question_entrance_exam(entrance_bank_45)
    entrance_exam_json_path = quiz_dir / "entrance_quiz_exam_15.json"
    with open(entrance_exam_json_path, "w", encoding="utf-8") as f:
        json.dump(entrance_exam_15, f, ensure_ascii=False, indent=2)
        
    entrance_exam_excel_path = quiz_dir / "De_Thi_Dau_Gio_15_Cau_Sinh_Vien.xlsx"
    export_quiz_to_excel(entrance_exam_15, str(entrance_exam_excel_path))
    print(f"  ✓ Saved Entrance Exam 15: {entrance_exam_excel_path.name}")
    
    # Exit Quiz (45 questions)
    print("\n[Quiz Engine] Generating Exit Quiz Bank (45 questions)...")
    exit_bank_45 = generate_exit_quiz(
        session_id=session_id,
        current_topic=current_topic,
        tech_stack=tech_stack,
        forbidden_scope=forbidden_scope,
        allowed_scope=allowed_scope
    )
    
    # Export Exit Bank 45 JSON & Excel
    exit_bank_json_path = quiz_dir / "exit_quiz_bank_45.json"
    with open(exit_bank_json_path, "w", encoding="utf-8") as f:
        json.dump(exit_bank_45, f, ensure_ascii=False, indent=2)
        
    exit_bank_excel_path = quiz_dir / "Quizz_Cuoi_Gio_Ngan_Hang_45_Cau.xlsx"
    export_quiz_to_excel(exit_bank_45, str(exit_bank_excel_path))
    print(f"  ✓ Saved Exit Quiz Bank 45: {exit_bank_excel_path.name}")
    
    # Exit Exam (15 questions)
    exit_exam_15 = extract_15_question_exit_exam(exit_bank_45)
    exit_exam_json_path = quiz_dir / "exit_quiz_exam_15.json"
    with open(exit_exam_json_path, "w", encoding="utf-8") as f:
        json.dump(exit_exam_15, f, ensure_ascii=False, indent=2)
        
    exit_exam_excel_path = quiz_dir / "De_Thi_Cuoi_Gio_15_Cau_Sinh_Vien.xlsx"
    export_quiz_to_excel(exit_exam_15, str(exit_exam_excel_path))
    print(f"  ✓ Saved Exit Exam 15: {exit_exam_excel_path.name}")
    
    # 3. Generate Student Classifier Matrix Report
    print("\n--- 3. Generating Student Classification Matrix Report ---")
    classifier_report_md = f"""# Báo cáo Ma trận Phân loại Năng lực Sinh viên - Session 04

## 📌 1. Ma trận Phân loại Bài thi Đầu giờ (Entrance Quiz - 15 Câu)
Dựa trên kết quả bài thi Đầu giờ (10 câu bài cũ + 5 câu bài mới), Giảng viên và Trợ giảng áp dụng phân nhóm và chiến thuật sư phạm:

| Nhóm Năng lực | Điều kiện Điểm Tổng | Bài mới (5 câu) | Đánh giá Năng lực | Đề xuất Chiến thuật Giảng dạy (Actionable Pedagogy) |
|---|---|---|---|---|
| **Gương mẫu** | $\ge 13/15$ | $= 5/5$ | Xuất sắc, tự học bài mới tốt | Cho làm Leader nhóm hoặc giao các bài tập Sáng tạo khó hơn. |
| **Nỗ lực** | $7-9/15$ | $\ge 3/5$ | Chăm chỉ nhưng hổng bài cũ | Tập trung bổ trợ lại bài cũ ngay tại lớp để không bị hổng kiến thức. |
| **Tư duy tốt** | $10-12/15$ | $< 3/5$ | Thực chiến tốt nhưng lười tự học | Cảnh cáo kỷ luật tự học và yêu cầu xem lại tài liệu bài mới tại lớp. |
| **Nguy cơ** | $< 7/15$ | Khác | Mất gốc bài cũ & không chuẩn bị | Kèm cặp riêng 1:1 bởi Trợ giảng hoặc Giảng viên ngay sau buổi học. |
| **Ổn định** | $10-12/15$ | $\ge 3/5$ | Trung bình - Khá | Cần động lực (Push) để bước lên nhóm Gương mẫu. |
| **Ẩn mình** | $7-9/15$ | $< 3/5$ | Có tư duy nhưng thiếu kỷ luật | Yêu cầu xem lại tài liệu bài mới ngay tại lớp. |

---

## 📌 2. Ma trận Phân loại Bài thi Cuối giờ (Exit Quiz - 15 Câu)
Dựa trên kết quả bài thi Cuối giờ (15 câu bài mới Session 04), Giảng viên rà soát mức độ hấp thụ kiến thức:

| Nhóm Năng lực | Điểm Số (/15) | Đánh giá Trình độ | Hành động Sư phạm Bắt buộc |
|---|---|---|---|
| **Làm chủ (Mastery)** | $13-15$ | Xuất sắc (Hiểu bản chất, code sạch) | Giao bài tập về nhà mức xuất sắc (Project-based), miễn bài lặp lại cơ bản. |
| **Đạt (Proficient)** | $10-12$ | Khá (Nắm vững cú pháp cơ bản) | Yêu cầu viết Comment/Documentation giải thích luồng code bài tập. |
| **Cơ bản (Basic)** | $7-9$ | Trung bình (Còn copy-paste/shadowing) | Yêu cầu làm lại bài tập từ đầu (không nhìn code mẫu), xem lại Record buổi học. |
| **Cần kèm (Mentoring)** | $< 7$ | Yếu (Chưa hiểu luồng chạy) | Kèm cặp 1:1 bởi Trợ giảng hoặc Giảng viên ngay sau buổi học. |
"""
    classifier_file = quiz_dir / "Bao_Cao_Phan_Loai_Sinh_Vien_Session04.md"
    with open(classifier_file, "w", encoding="utf-8") as f:
        f.write(classifier_report_md)
    print(f"  ✓ Saved Student Classification Report: {classifier_file.name}")
    
    print("\n🎉 ALL SESSION 04 QUIZ & MINDMAP RESOURCES GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

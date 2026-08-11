import sys
import os
import json
from pathlib import Path

# Ensure root directory is in sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.creators.reading_creator import html_writer_agent
from agents.creators.practical_lab_creator import practical_lab_creator_agent
from agents.creators.quiz_creator import quiz_agent
from agents.creators.reading_questions_creator import reading_questions_creator_agent
from core.quiz_excel import export_lesson_quiz_to_excel

lessons_metadata = [
    {
        "session_id": "Session 04",
        "lesson_id": "Lesson 01",
        "folder_name": "Lesson 01 - Toán tử số học và toán tử gán",
        "title": "Toán tử số học và toán tử gán trong Python",
        "details": "Các phép toán số học (+, -, *, /, //, %, **), toán tử gán và toán tử gán kết hợp (+=, -=, *=, /=, %=), thứ tự ưu tiên của toán tử số học trong tính toán doanh nghiệp.",
        "expected_output": "Lập trình viên làm chủ các phép toán số học và toán tử gán trong Python, ứng dụng tính toán chiết khấu, tổng tiền hóa đơn, VAT và ép kiểu dữ liệu an toàn."
    },
    {
        "session_id": "Session 04",
        "lesson_id": "Lesson 02",
        "folder_name": "Lesson 02 - Toán tử so sánh và toán tử logic",
        "title": "Toán tử so sánh và toán tử logic trong Python",
        "details": "Các toán tử so sánh (==, !=, >, <, >=, <=), toán tử logic (and, or, not), cơ chế đánh giá ngắn mạch (Short-circuit evaluation), ứng dụng kiểm tra điều kiện ghép trong ứng dụng thương mại điện tử.",
        "expected_output": "Viết được các biểu thức điều kiện logic phức tạp kiểm tra trạng thái người dùng, số dư tài khoản, mã giảm giá và quyền truy cập hệ thống."
    },
    {
        "session_id": "Session 04",
        "lesson_id": "Lesson 04",
        "folder_name": "Lesson 04 - Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8",
        "title": "Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8",
        "details": "Cấu trúc rẽ nhánh lồng nhau (Nested if), tối ưu hóa luồng điều khiển tránh bẫy lặp/Unreachable code, quy chuẩn trình bày mã nguồn PEP 8 (Indentation 4 spaces, Naming conventions snake_case, Hạn chế lồng nhau quá 3 cấp).",
        "expected_output": "Lập trình viên xây dựng được thuật toán rẽ nhánh nhiều tầng an toàn, tối ưu hiệu năng và viết mã nguồn chuẩn hóa theo phong cách PEP 8 chuyên nghiệp."
    }
]

session_base_dir = Path("output/pms/Lập_trình_Python/Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh")

def process_lesson(meta: dict):
    session_id = meta["session_id"]
    lesson_id = meta["lesson_id"]
    folder_name = meta["folder_name"]
    title = meta["title"]
    details = meta["details"]
    expected_output = meta["expected_output"]

    print(f"\n=====================================================================")
    print(f"GENERATING RESOURCES FOR: {session_id} - {lesson_id}: {title}")
    print(f"=====================================================================")

    lesson_dir = session_base_dir / folder_name
    reading_dir = lesson_dir / "Bài đọc"
    lab_dir = lesson_dir / "Bài thực hành"
    quiz_dir = lesson_dir / "Câu hỏi Quizz"
    rq_dir = lesson_dir / "Câu hỏi bài đọc"

    for d in [reading_dir, lab_dir, quiz_dir, rq_dir]:
        d.mkdir(parents=True, exist_ok=True)

    state = {
        "session_id": session_id,
        "lesson_id": lesson_id,
        "lesson_title": title,
        "tech_stack": "python",
        "technology_stack": "python",
        "core_ssot": {
            "session_title": title,
            "lesson_details": details,
            "expected_output": expected_output
        },
        "course_dir_name": "Lập_trình_Python",
        "review_logs": []
    }

    # 1. Reading Material Creator
    print(f"-> Running HTML Writer Agent...")
    state = html_writer_agent(state)
    html_content = state.get("html_content")
    if html_content:
        reading_file = reading_dir / "reading.html"
        with open(reading_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"   Saved {reading_file}")

    # 2. Practical Lab Creator
    print(f"-> Running Practical Lab Creator Agent...")
    state = practical_lab_creator_agent(state)
    lab_md = state.get("practical_lab_markdown")
    lab_html = state.get("practical_lab_html")
    if lab_md:
        lab_md_file = lab_dir / "practical_lab.md"
        with open(lab_md_file, "w", encoding="utf-8") as f:
            f.write(lab_md)
        print(f"   Saved {lab_md_file}")
    if lab_html:
        lab_html_file = lab_dir / "practical_lab.html"
        with open(lab_html_file, "w", encoding="utf-8") as f:
            f.write(lab_html)
        print(f"   Saved {lab_html_file}")

    # 3. Quiz Creator
    print(f"-> Running Quiz Creator Agent...")
    state = quiz_agent(state)
    quiz_data = state.get("quiz_json")
    if quiz_data:
        quiz_json_file = quiz_dir / "quiz.json"
        with open(quiz_json_file, "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)
        print(f"   Saved {quiz_json_file}")

        s_clean = session_id.replace(" ", "")
        l_clean = lesson_id.replace(" ", "")
        excel_name = f"Quizz_{s_clean}_{l_clean}.xlsx"
        excel_file = quiz_dir / excel_name
        quiz_items = quiz_data.get("quiz") if isinstance(quiz_data, dict) else quiz_data
        export_lesson_quiz_to_excel(quiz_items, str(excel_file))
        print(f"   Exported Excel {excel_file}")

    # 4. Reading Questions Creator
    print(f"-> Running Reading Questions Creator Agent...")
    state = reading_questions_creator_agent(state)
    rq_md = state.get("reading_questions_markdown")
    if rq_md:
        rq_file = rq_dir / "reading_questions.md"
        with open(rq_file, "w", encoding="utf-8") as f:
            f.write(rq_md)
        print(f"   Saved {rq_file}")

    print(f"SUCCESS: Finished all resources for {lesson_id}!")

if __name__ == "__main__":
    for meta in lessons_metadata:
        process_lesson(meta)
    print("\n=====================================================================")
    print("ALL REMAINING LESSONS OF SESSION 04 RE-GENERATED SUCCESSFULLY!")
    print("=====================================================================")

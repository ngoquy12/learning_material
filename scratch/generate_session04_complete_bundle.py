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
from agents.creators.slide_creator import slide_agent
from agents.creators.mindmap_creator import mindmap_agent
from agents.creators.session_compiler_creator import session_compiler_agent
from core.quiz_excel import export_lesson_quiz_to_excel

lessons_metadata = [
    {
        "session_id": "Session 04",
        "lesson_id": "Lesson 01",
        "folder_name": "Lesson 01 - Toán tử Số học và Toán tử Gán",
        "title": "Toán tử Số học và Toán tử Gán",
        "details": "Đặt vấn đề nhu cầu tính toán trong phần mềm; Các toán tử số học: +, -, *, /, //, %, **; Các toán tử gán gộp +=, -=, *=, /=.",
        "expected_output": "Xây dựng đúng các biểu thức số học phức tạp và sử dụng toán tử gán tối ưu mã nguồn."
    },
    {
        "session_id": "Session 04",
        "lesson_id": "Lesson 02",
        "folder_name": "Lesson 02 - Cơ chế so sánh và Biểu thức logic Boolean",
        "title": "Cơ chế so sánh và Biểu thức logic Boolean",
        "details": "Cơ chế so sánh hai giá trị (==, !=, >, <, >=, <=); Biểu thức kiểm tra điều kiện trả về kiểu Boolean (True/False).",
        "expected_output": "Viết chính xác các điều kiện so sánh giữa các biến số và nhận biết kết quả Boolean."
    },
    {
        "session_id": "Session 04",
        "lesson_id": "Lesson 03",
        "folder_name": "Lesson 03 - Ứng dụng toán tử logic và Thứ tự ưu tiên tính toán",
        "title": "Ứng dụng toán tử logic và Thứ tự ưu tiên tính toán",
        "details": "Kết hợp điều kiện phức tạp với toán tử logic: and, or, not; Đánh giá ngắn mạch (Short-circuit); Bảng thứ tự ưu tiên toán tử trong Python.",
        "expected_output": "Kết hợp nhiều điều kiện logic bằng and/or/not và điều khiển thứ tự tính toán bằng dấu ngoặc đơn."
    }
]

session_base_dir = Path("output/pms/Lập_trình_Python/Session 04 - Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python")

def process_lesson(meta: dict):
    session_id = meta["session_id"]
    lesson_id = meta["lesson_id"]
    folder_name = meta["folder_name"]
    title = meta["title"]
    details = meta["details"]
    expected_output = meta["expected_output"]

    print(f"\n=====================================================================")
    print(f" 🚀 GENERATING LESSON RESOURCES FOR: {session_id} - {lesson_id}: {title}")
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
    print(f"  -> Running Reading Creator Agent...")
    state = html_writer_agent(state)
    html_content = state.get("html_content")
    if html_content:
        reading_file = reading_dir / "reading.html"
        with open(reading_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"     Saved {reading_file}")

    # 2. Practical Lab Creator
    print(f"  -> Running Practical Lab Creator Agent...")
    state = practical_lab_creator_agent(state)
    lab_md = state.get("practical_lab_markdown")
    if lab_md:
        lab_md_file = lab_dir / "practical_lab.md"
        with open(lab_md_file, "w", encoding="utf-8") as f:
            f.write(lab_md)
        print(f"     Saved {lab_md_file}")

    # 3. Quiz Creator
    print(f"  -> Running Quiz Creator Agent...")
    state = quiz_agent(state)
    quiz_data = state.get("quiz_json")
    if quiz_data:
        quiz_json_file = quiz_dir / "quiz.json"
        with open(quiz_json_file, "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)
        print(f"     Saved {quiz_json_file}")

        s_clean = session_id.replace(" ", "")
        l_clean = lesson_id.replace(" ", "")
        excel_name = f"Quizz_{s_clean}_{l_clean}.xlsx"
        excel_file = quiz_dir / excel_name
        quiz_items = quiz_data.get("quiz") if isinstance(quiz_data, dict) else quiz_data
        export_lesson_quiz_to_excel(quiz_items, str(excel_file))
        print(f"     Exported Excel {excel_file}")

    # 4. Reading Questions Creator
    print(f"  -> Running Reading Questions Creator Agent...")
    state = reading_questions_creator_agent(state)
    rq_md = state.get("reading_questions_markdown")
    if rq_md:
        rq_file = rq_dir / "reading_questions.md"
        with open(rq_file, "w", encoding="utf-8") as f:
            f.write(rq_md)
        print(f"     Saved {rq_file}")

    # 5. Slide Creator
    print(f"  -> Running Slide Creator Agent...")
    state = slide_agent(state)
    slide_html = state.get("slide_html")
    if slide_html:
        slide_file = lesson_dir / "slide.html"
        with open(slide_file, "w", encoding="utf-8") as f:
            f.write(slide_html)
        print(f"     Saved {slide_file}")

    print(f"  ✅ Completed resources for {lesson_id}!")

def build_session_level_resources():
    print(f"\n=====================================================================")
    print(f" 🌐 BUILDING SESSION-LEVEL COMPILER RESOURCES (Reading Hub, Mindmap, Slides)")
    print(f"=====================================================================")
    state = {
        "session_id": "Session 04",
        "session_title": "Session 04 - Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python",
        "tech_stack": "python",
        "technology_stack": "python",
        "course_dir_name": "Lập_trình_Python",
        "session_dir": session_base_dir,
        "lessons": lessons_metadata
    }
    
    try:
        session_compiler_agent(state)
        print("  ✅ Session Reading Hub (reading_all.html) compiled successfully!")
    except Exception as e:
        print(f"  ⚠️ Session Compiler warning: {e}")

    try:
        mindmap_agent(state)
        print("  ✅ Session Mindmap created successfully!")
    except Exception as e:
        print(f"  ⚠️ Mindmap warning: {e}")

if __name__ == "__main__":
    for meta in lessons_metadata:
        process_lesson(meta)
    build_session_level_resources()
    print("\n=====================================================================")
    print(" 🎉 ALL SESSION 04 RESOURCES GENERATED SUCCESSFULLY!")
    print("=====================================================================")

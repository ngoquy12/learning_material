import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.creators.reading_creator import html_writer_agent
from agents.reviewer_agents import html_ux_reviewer

state = {
    "session_id": "Session 04",
    "lesson_id": "Lesson 03",
    "lesson_title": "Cấu trúc rẽ nhánh điều khiển với if, elif và else",
    "tech_stack": "python",
    "technology_stack": "python",
    "core_ssot": {
        "session_title": "Cấu trúc rẽ nhánh điều khiển với if, elif và else",
        "lesson_details": "Cú pháp và cơ chế hoạt động của câu lệnh rẽ nhánh điều khiển: if đơn, if-else, if-elif-else. Xử lý các điều kiện loại trừ độc quyền (Mutually Exclusive), thứ tự đánh giá từ trên xuống dưới và nhánh else mặc định.",
        "expected_output": "Lập trình viên nắm vững cơ chế rẽ nhánh, ứng dụng đánh giá điều kiện phân loại (ví dụ: điểm trung bình & xếp loại học lực sinh viên, hạn mức giảm giá đơn hàng), viết mã nguồn mạch lạc và không lặp code."
    },
    "course_dir_name": "Lập_trình_Python",
    "review_logs": []
}

print("Running upgraded Reading Creator Agent for Session 04 Lesson 03...")
state = html_writer_agent(state)

html_content = state.get("html_content")
if html_content:
    output_path = Path("output/pms/Lập_trình_Python/Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh/Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else/Bài đọc/reading.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"SUCCESS: Generated reading.html saved to {output_path} ({len(html_content)} bytes)")

    print("\nRunning UX Reviewer Agent audit on generated HTML...")
    review = html_ux_reviewer(state)
    print("Review Result:", review)

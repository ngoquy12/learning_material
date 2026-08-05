# scratch/generate_session_06_lesson_01_reading.py
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.creators.reading_creator import generate_reading_html

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    session_id = "Session 06"
    lesson_id = "Lesson 01"
    lesson_title = "Lesson 01 - Khái niệm vòng lặp và câu lệnh for"
    lesson_details = "Mục đích sử dụng vòng lặp trong lập trình; Cú pháp và cơ chế hoạt động của vòng lặp for; Ứng dụng hàm range() để duyệt dải số; Lặp qua danh sách (list) và chuỗi (string)"
    expected_output = "Nắm vững lý do cần dùng vòng lặp, cú pháp câu lệnh for, cách kết hợp với hàm range() để duyệt dữ liệu và giải quyết bài toán thực tế"
    tech_stack = "python"
    
    state = {
        "session_id": session_id,
        "lesson_id": lesson_id,
        "session_title": "Session 06 - Vòng lặp và điều khiển luồng lặp",
        "technology_stack": tech_stack
    }
    
    print("=" * 70)
    print(f"Generating Reading Material for {session_id} - {lesson_title}...")
    print("=" * 70)
    
    html_content = generate_reading_html(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        tech_stack=tech_stack,
        state=state
    )
    
    lesson_dir = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material\output\pms\Lập_trình_Python\Session 06 - Vòng lặp và điều khiển luồng lặp\Lesson 01 - Khái niệm vòng lặp và câu lệnh for")
    lesson_dir.mkdir(parents=True, exist_ok=True)
    
    baidoc_dir = lesson_dir / "Bài đọc"
    baidoc_dir.mkdir(parents=True, exist_ok=True)
    
    out_file1 = lesson_dir / "reading.html"
    out_file2 = baidoc_dir / "reading.html"
    
    with open(out_file1, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    with open(out_file2, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n[SUCCESS] Generated reading.html ({len(html_content)} bytes)")
    print(f"Saved to:")
    print(f" - {out_file1}")
    print(f" - {out_file2}")

if __name__ == "__main__":
    main()

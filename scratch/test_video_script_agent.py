# scratch/test_video_script_agent.py
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.video_script_agent import generate_lesson_video_script

def test_generation():
    # Target lesson directory from Session 06 Lesson 01
    base_output = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material\output")
    
    # Find matching session 06 directory
    session_dirs = list(base_output.glob("**/Session 06*"))
    if not session_dirs:
        print("Session 06 directory not found in output folder.")
        return

    session_dir = session_dirs[0]
    lesson_dirs = [d for d in session_dir.iterdir() if d.is_dir() and "Lesson 01" in d.name]
    
    if not lesson_dirs:
        print(f"Lesson 01 directory not found in {session_dir}")
        return
        
    lesson_dir = lesson_dirs[0]
    print(f"Found target lesson dir: {lesson_dir}")
    
    # Run Video Script Agent
    html = generate_lesson_video_script(
        lesson_dir_path=str(lesson_dir),
        lesson_title=lesson_dir.name,
        session_title=session_dir.name,
        tech_stack="Lập trình Python",
        previous_lesson_title="Session 05 - Cấu trúc điều kiện và Biến đơn lẻ",
        next_lesson_title="Lesson 02 - Kỹ thuật duyệt các phần tử trong List bằng vòng lặp"
    )
    
    output_html_file = lesson_dir / "Video" / "video_script.html"
    print(f"\n[Test Complete] Generated File Path: {output_html_file}")
    print(f"HTML File Size: {len(html)} bytes")
    assert output_html_file.exists(), "Output video_script.html file was not created!"
    assert "<!DOCTYPE html>" in html, "Generated file is not valid HTML!"
    print("[SUCCESS] All assertions passed!")

if __name__ == "__main__":
    test_generation()

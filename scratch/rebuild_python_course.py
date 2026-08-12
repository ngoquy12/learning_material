import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, '.')

project_root = Path('.')
course_dir = project_root / "output" / "pms" / "Lập_trình_Python"

print("--> 1. Đang dọn dẹp các thư mục session cũ trong:", course_dir)
if course_dir.exists():
    for item in list(course_dir.iterdir()):
        if item.is_dir() and item.name.startswith("Session"):
            # Use long path for safe deletion
            abs_path = os.path.abspath(str(item))
            if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
                abs_path = '\\\\?\\' + abs_path
            shutil.rmtree(abs_path)
            print(f"   - Đã xóa thư mục cũ: {item.name}")

print("\n--> 2. Tiến hành sinh lại PM cho môn Python với luật chuẩn hóa tiêu đề mới...")
import scratch.generate_python_pm as gen_script
gen_script.main()

print("\n--> 3. Khởi tạo lại cấu trúc thư mục từ PM_Python.xlsx mới sinh...")
from cli.curriculum_parser import parse_all_sessions, initialize_skeleton_structure, project_structure_reviewer_agent

excel_path = str(course_dir / "PM_Python.xlsx")
sessions = parse_all_sessions(excel_path)

initialize_skeleton_structure(sessions, course_dir, ['html', 'quiz', 'mindmap'], 'all')
project_structure_reviewer_agent(sessions, course_dir, ['html', 'quiz', 'mindmap'], 'all')

print("\n--> 4. Kiểm tra danh sách tiêu đề mới:")
import scratch.inspect_titles as inspect_mod

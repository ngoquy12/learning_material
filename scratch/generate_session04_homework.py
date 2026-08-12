import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, ".")
from agents.homework_agents import session_homework_pipeline

session_id = "Session 04"
session_title = "Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python"
tech_stack = "python/core"
previous_lessons_text = (
    "Biến số, kiểu dữ liệu nguyên thủy (int, float, str, bool), hàm nhập xuất print(), input(), "
    "ép kiểu dữ liệu (int(), float(), str()), các toán tử số học (+, -, *, /, //, %, **), "
    "toán tử gán (=, +=, -=, *=, /=), toán tử so sánh (==, !=, >, <, >=, <=), "
    "và toán tử logic (and, or, not), thứ tự ưu tiên toán tử."
)
forbidden_scope = "CẤM: Câu lệnh rẽ nhánh if/else/elif, vòng lặp for/while, List, Dict, Set, Tuple, Hàm def, Class OOP."
session_dir_path = "output/pms/Lập_trình_Python/Session 04 - Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python"

print(f"🚀 Starting 15-Exercise Generation for {session_id}: {session_title}...")
exercises = session_homework_pipeline(
    session_id=session_id,
    session_title=session_title,
    tech_stack=tech_stack,
    previous_lessons_text=previous_lessons_text,
    session_dir_path=session_dir_path,
    forbidden_scope=forbidden_scope
)

print(f"\n✅ SUCCESSFULLY GENERATED {len(exercises)} EXERCISES FOR SESSION 04!")

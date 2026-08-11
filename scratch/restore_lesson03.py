import sys
import sqlite3
import zlib
import json
import os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.quiz_excel import export_lesson_quiz_to_excel

db_path = "storage/state_store_v2.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT state_data FROM checkpoints WHERE session_id='Session 04_Lesson 03'")
row = c.fetchone()

if not row:
    print("❌ Error: Session 04_Lesson 03 checkpoint not found in DB!")
    exit(1)

data = json.loads(zlib.decompress(row[0]).decode('utf-8'))
print("Found Session 04_Lesson 03 checkpoint!")

lesson_dir = Path("output/pms/Lập_trình_Python/Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh/Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else")

reading_dir = lesson_dir / "Bài đọc"
lab_dir = lesson_dir / "Bài thực hành"
quiz_dir = lesson_dir / "Câu hỏi Quizz"
rq_dir = lesson_dir / "Câu hỏi bài đọc"

for d in [reading_dir, lab_dir, quiz_dir, rq_dir]:
    d.mkdir(parents=True, exist_ok=True)

# 1. Restore reading.html
html_content = data.get("html_content")
if html_content:
    reading_file = reading_dir / "reading.html"
    with open(reading_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Restored {reading_file} ({len(html_content)} bytes)")

# 2. Restore practical_lab.md & practical_lab.html
lab_md = data.get("practical_lab_markdown")
lab_html = data.get("practical_lab_html")
if lab_md:
    lab_md_file = lab_dir / "practical_lab.md"
    with open(lab_md_file, "w", encoding="utf-8") as f:
        f.write(lab_md)
    print(f"Restored {lab_md_file}")

if lab_html:
    lab_html_file = lab_dir / "practical_lab.html"
    with open(lab_html_file, "w", encoding="utf-8") as f:
        f.write(lab_html)
    print(f"Restored {lab_html_file}")

# 3. Restore quiz.json & Quizz_Session04_Lesson03.xlsx
quiz_data = data.get("quiz_json")
if quiz_data:
    quiz_file = quiz_dir / "quiz.json"
    with open(quiz_file, "w", encoding="utf-8") as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    print(f"Restored {quiz_file}")

    excel_file = quiz_dir / "Quizz_Session04_Lesson03.xlsx"
    quiz_items = quiz_data.get("quiz") if isinstance(quiz_data, dict) else quiz_data
    export_lesson_quiz_to_excel(quiz_items, str(excel_file))
    print(f"Restored Excel {excel_file}")

# 4. Restore reading_questions.md
rq_md = data.get("reading_questions_markdown")
if rq_md:
    rq_file = rq_dir / "reading_questions.md"
    with open(rq_file, "w", encoding="utf-8") as f:
        f.write(rq_md)
    print(f"Restored {rq_file}")

print("\nALL LESSON 03 RESOURCES RESTORED SUCCESSFULLY FROM DATABASE CHECKPOINT!")

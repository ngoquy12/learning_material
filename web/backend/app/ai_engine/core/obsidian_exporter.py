# core/obsidian_exporter.py
import os
import openpyxl
from pathlib import Path
from typing import List, Dict, Any, Optional

def generate_obsidian_vault(excel_path: str, output_dir: str = "obsidian_vault"):
    """
    Parses the PM syllabus Excel file and outputs a fully linked
    Obsidian Vault directory.
    """
    print(f"[Obsidian Exporter] Reading syllabus spreadsheet from: {excel_path}")
    if not os.path.exists(excel_path):
        print(f"Error: Spreadsheet not found at {excel_path}")
        return

    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    if ws is None:
        raise ValueError("Workbook has no active worksheet.")
    course_name = ws.title.strip()
    
    # Clean up course name for filesystem use
    course_clean = course_name.replace(" ", "_").replace("-", "_")
    
    # Organize vault under a folder named after the course
    vault_base = Path(output_dir)
    vault_path = vault_base / course_clean
    
    # Recreate clean course folder within the vault
    if vault_path.exists():
        import shutil
        print(f"[Obsidian Exporter] Cleaning existing course vault at {vault_path}")
        shutil.rmtree(vault_path)
    vault_path.mkdir(parents=True, exist_ok=True)

    # 1. Parse sessions & lessons
    sessions: List[Dict[str, Any]] = []
    current_session: Optional[Dict[str, Any]] = None
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        row_padded = list(row) + [None] * (8 - len(row))
        stt, form, session_val, content_val, lesson_val, details_val, output_val, deadline = row_padded[:8]
        
        if session_val and str(session_val).strip().startswith("Session"):
            session_id = str(session_val).strip()
            existing = [s for s in sessions if s["session_id"] == session_id]
            if existing:
                current_session = existing[0]
            else:
                current_session = {
                    "session_id": session_id,
                    "title": str(content_val).strip() if content_val else "",
                    "lessons": []
                }
                sessions.append(current_session)
            
        if lesson_val and str(lesson_val).strip().startswith("Lesson") and current_session:
            lesson_id = str(lesson_val).strip().split(":")[0].strip()
            lesson_title = str(lesson_val).strip().split(":", 1)[1].strip() if ":" in str(lesson_val) else str(lesson_val).strip()
            current_session["lessons"].append({
                "lesson_id": lesson_id,
                "title": lesson_title,
                "details": str(details_val).strip() if details_val else "",
                "expected_output": str(output_val).strip() if output_val else ""
            })

    print(f"[Obsidian Exporter] Parsed {len(sessions)} sessions to export.")

    # 2. Write index.md
    index_content = f"""---
type: course
id: {course_clean}
title: "{course_name}"
tags:
  - learning-material
  - obsidian-graph
---

# 📚 Môn học: {course_name}

Chào mừng bạn đến với Bản đồ Tri thức môn học **{course_name}**. Đây là tệp neo trung tâm để liên kết toàn bộ tài nguyên học tập của môn học.

## 📅 Danh sách các Sessions học tập
Dưới đây là các phiên học tập chính của môn học. Hãy nhấp vào các liên kết để xem chi tiết từng Session:

"""
    for s in sessions:
        s_title_clean = s["title"].replace("/", "_").replace("\\", "_").replace(":", "-")
        s_title = f"{s['session_id']} - {s_title_clean}"
        index_content += f"- [[{s_title}]]\n"
        
    with open(vault_path / "index.md", "w", encoding="utf-8") as f:
        f.write(index_content)

    # 3. Create Session folders and files
    for s in sessions:
        s_id = s["session_id"]
        s_title_clean = s["title"].replace("/", "_").replace("\\", "_").replace(":", "-")
        s_folder_name = f"{s_id} - {s_title_clean}"
        s_dir = vault_path / s_id.replace(" ", "_")
        s_dir.mkdir(parents=True, exist_ok=True)
        
        # Session Markdown file
        s_filename = f"{s_folder_name}.md"
        s_file_path = s_dir / s_filename
        
        s_content = f"""---
type: session
id: {s_id}
title: "{s['title']}"
tags:
  - learning-material
  - obsidian-graph
---

# 🗓️ {s_id}: {s['title']}

[[index|🏠 Trang chủ môn học]]

## 📝 Đề kiểm tra đánh giá (Session Quizzes)
- [[{s_id} - Entrance Quiz]]
- [[{s_id} - Exit Quiz]]

## 📖 Các bài học trực thuộc (Lessons)
Nhấp vào từng bài học để xem giáo trình, slide bài giảng, mindmap và kịch bản quay video:

"""
        for l in s["lessons"]:
            l_title_clean = l["title"].replace("/", "_").replace("\\", "_").replace(":", "-")
            l_full_title = f"{l['lesson_id']} - {l_title_clean}"
            s_content += f"- [[{l_full_title}]]\n"
            
        with open(s_file_path, "w", encoding="utf-8") as f:
            f.write(s_content)

        # Entrance Quiz file
        with open(s_dir / f"{s_id} - Entrance Quiz.md", "w", encoding="utf-8") as f:
            f.write(f"""---
type: quiz
id: {s_id}-entrance
title: "Entrance Quiz - {s_id}"
tags:
  - learning-material
  - obsidian-graph
---

# 📝 {s_id} - Entrance Quiz (Quizz Đầu Giờ)

[[{s_folder_name}|⬅️ Quay lại Session cha]]

- **Số câu hỏi**: 45 câu (30 cũ ôn tập, 15 mới)
- **Độ khó**: Theo thang đo sỹ số Bloom (Nhớ - Hiểu - Vận dụng)
- **Mục đích**: Ôn tập kiến thức cũ và chuẩn bị hành trang học bài mới.
""")

        # Exit Quiz file
        with open(s_dir / f"{s_id} - Exit Quiz.md", "w", encoding="utf-8") as f:
            f.write(f"""---
type: quiz
id: {s_id}-exit
title: "Exit Quiz - {s_id}"
tags:
  - learning-material
  - obsidian-graph
---

# 📝 {s_id} - Exit Quiz (Quizz Cuối Giờ)

[[{s_folder_name}|⬅️ Quay lại Session cha]]

- **Số câu hỏi**: 45 câu (100% câu hỏi mới)
- **Độ khó**: Đánh giá toàn diện kiến thức của buổi học
- **Mục đích**: Đánh giá khả năng hiểu bài và ghi nhớ của học viên ngay tại lớp.
""")

        # Create Lesson files inside Session directory
        for l in s["lessons"]:
            l_id = l["lesson_id"]
            l_title_clean = l["title"].replace("/", "_").replace("\\", "_").replace(":", "-")
            l_folder_name = f"{l_id} - {l_title_clean}"
            l_dir = s_dir / l_id.replace(" ", "_")
            l_dir.mkdir(parents=True, exist_ok=True)
            
            # Lesson main file
            l_filename = f"{l_folder_name}.md"
            l_file_path = l_dir / l_filename
            
            l_content = f"""---
type: lesson
id: {l_id}
title: "{l['title']}"
tags:
  - learning-material
  - obsidian-graph
---

# 🎓 {l_id}: {l['title']}

[[{s_folder_name}|⬅️ Quay lại Session cha]]

### 🎯 Chi tiết nội dung học tập
- **Nội dung chi tiết**: {l['details']}
- **Sản phẩm mong đợi**: {l['expected_output']}

### 📚 Tài nguyên học tập thành phần
Hãy nhấp vào các tài nguyên dưới đây để xem nội dung chi tiết:
- [[{l_id} - Reading]]
- [[{l_id} - Slides]]
- [[{l_id} - Mindmap]]
- [[{l_id} - Video Script]]
"""
            with open(l_file_path, "w", encoding="utf-8") as f:
                f.write(l_content)
                
            # Reading file
            with open(l_dir / f"{l_id} - Reading.md", "w", encoding="utf-8") as f:
                f.write(f"""---
type: reading
id: {l_id}-reading
title: "Bài đọc - {l['title']}"
tags:
  - learning-material
  - obsidian-graph
---

# 📖 Bài đọc lý thuyết: {l['title']}

[[{l_folder_name}|↩️ Quay lại Bài học chính]]

Bài đọc chuyên sâu hỗ trợ học viên tự học lý thuyết nền tảng và cơ chế vận hành nội bộ (internals).
""")

            # Slides file
            with open(l_dir / f"{l_id} - Slides.md", "w", encoding="utf-8") as f:
                f.write(f"""---
type: slide
id: {l_id}-slide
title: "Slide bài giảng - {l['title']}"
tags:
  - learning-material
  - obsidian-graph
---

# 🖼️ Slide Bài Giảng: {l['title']}

[[{l_folder_name}|↩️ Quay lại Bài học chính]]

Slide bài giảng hỗ trợ giảng viên giảng dạy trên lớp theo chuẩn tương tác Marp CLI.
""")

            # Mindmap file
            with open(l_dir / f"{l_id} - Mindmap.md", "w", encoding="utf-8") as f:
                f.write(f"""---
type: mindmap
id: {l_id}-mindmap
title: "Mindmap - {l['title']}"
tags:
  - learning-material
  - obsidian-graph
---

# 🧠 Sơ đồ tư duy bài học: {l['title']}

[[{l_folder_name}|↩️ Quay lại Bài học chính]]

Sơ đồ tư duy tóm tắt trực quan hóa mối quan hệ giữa các khái niệm trong bài học.
""")

            # Video Script file
            with open(l_dir / f"{l_id} - Video Script.md", "w", encoding="utf-8") as f:
                f.write(f"""---
type: video
id: {l_id}-video
title: "Kịch bản video - {l['title']}"
tags:
  - learning-material
  - obsidian-graph
---

# 📹 Kịch bản Video bài học: {l['title']}

[[{l_folder_name}|↩️ Quay lại Bài học chính]]

Kịch bản phân cảnh hỗ trợ giảng viên ghi hình bài giảng chi tiết.
""")

    print(f"[Obsidian Exporter] Export complete! Obsidian Vault generated successfully under: {vault_path}")

if __name__ == "__main__":
    excel = r"d:\Rikkei Education\Elearning_Agent\Learning-Material\pms\PM_RA_PTIT_2025_Software_Engineer_Python_Web.xlsx"
    generate_obsidian_vault(excel)

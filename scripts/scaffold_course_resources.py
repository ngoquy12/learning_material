"""
scripts/scaffold_course_resources.py

Tạo toàn bộ cấu trúc thư mục và file tài nguyên rỗng (placeholder scaffolding)
cho một môn học dựa trên file PM Excel / Markdown chi tiết.
"""

import os
import re
import sys
from pathlib import Path
import openpyxl

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

def sanitize_name(name: str) -> str:
    if not name:
        return ""
    cleaned = re.sub(r'[\\/:*?"<>|]', '-', name)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def create_empty_file(file_path: Path, header_comment: str = ""):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as f:
            if header_comment:
                f.write(header_comment.strip() + "\n")
            else:
                f.write("")

def parse_pm_excel(excel_path: str):
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    sessions = []
    current_session = None

    for r in range(6, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 11)]
        if not any(vals):
            continue

        sess_col = vals[0]
        ht_col = vals[1]
        stitle_col = vals[3]
        ltitle_col = vals[4]

        if sess_col and str(sess_col).strip():
            if current_session:
                sessions.append(current_session)
            current_session = {
                "session_num": str(sess_col).strip(),
                "hinh_thuc": str(ht_col).strip() if ht_col else "Lý thuyết",
                "session_title": str(stitle_col).strip() if stitle_col else str(sess_col).strip(),
                "lessons": []
            }

        if current_session and ltitle_col and str(ltitle_col).strip():
            lt_str = str(ltitle_col).strip()
            if "Lý thuyết" in current_session["hinh_thuc"] or lt_str.lower().startswith("lesson"):
                current_session["lessons"].append(lt_str)

    if current_session:
        sessions.append(current_session)

    return sessions

def scaffold_course_resources(excel_path: str, output_base_dir: str = None):
    p_excel = Path(excel_path).resolve()
    if not p_excel.exists():
        raise FileNotFoundError(f"Không tìm thấy file Excel PM: {excel_path}")

    # Default: Scaffold inside the exact parent directory where the PM Excel file lives
    if output_base_dir:
        course_root = Path(output_base_dir).resolve()
    else:
        if p_excel.parent.name in ["output", "pms"]:
            course_name = p_excel.stem.replace("PM_", "").replace("PM_Generated_", "").replace("_Updated", "")
            course_root = p_excel.parent / sanitize_name(course_name)
        elif p_excel.parent.name == "CLO-PLO":
            course_root = p_excel.parent / sanitize_name(p_excel.stem)
        else:
            course_root = Path("output/pms") / sanitize_name(p_excel.stem)

    course_root.mkdir(parents=True, exist_ok=True)
    course_name = course_root.name

    print(f"\n[Scaffold Engine] Khởi tạo cấu trúc tài nguyên cho môn học: '{course_name}'")
    print(f"  - Thư mục khóa học: {course_root.resolve()}")

    sessions = parse_pm_excel(excel_path)
    print(f"  - Tổng số Session cần khởi tạo: {len(sessions)} buổi\n")

    total_files_created = 0
    total_dirs_created = 0

    for s_idx, session in enumerate(sessions, 1):
        s_num = session["session_num"]
        s_ht = session["hinh_thuc"]
        s_title = session["session_title"]
        lessons = session["lessons"]

        # Clean session folder name
        if not s_title.startswith("Session"):
            session_folder_name = f"{s_num} - {s_title}"
        else:
            session_folder_name = s_title

        session_folder_name = sanitize_name(session_folder_name)
        session_dir = course_root / session_folder_name
        session_dir.mkdir(parents=True, exist_ok=True)
        total_dirs_created += 1

        print(f"  📁 [{s_num}] {session_folder_name} ({s_ht})")

        # -------------------------------------------------------------
        # 1. PHÂN LOẠI THEO HÌNH THỨC BUỔI HỌC
        # -------------------------------------------------------------
        if "Lý thuyết" in s_ht:
            # Session-level files
            create_empty_file(session_dir / "Slide bài giảng" / "outline_bai_giang.md", f"# Đề cương Slide bài giảng: {session_folder_name}\n")
            create_empty_file(session_dir / "Bài giảng trên lớp" / "slides.html", f"<!-- Bài giảng trên lớp: {session_folder_name} -->")
            create_empty_file(session_dir / "Sơ đồ tư duy" / "mindmap.md", f"# Sơ đồ tư duy: {session_folder_name}\n")
            create_empty_file(session_dir / "Sơ đồ tư duy" / "session_mindmap.md", f"# Sơ đồ tư duy tổng hợp: {session_folder_name}\n")
            create_empty_file(session_dir / "Visualizer" / "index.html", f"<!-- Visualizer: {session_folder_name} -->\n")
            
            # Quizz session (Gộp đầu giờ và cuối giờ)
            quizz_session_dir = session_dir / "Quizz session"
            create_empty_file(quizz_session_dir / "quizz_dau_gio.md", f"# Quizz đầu giờ: {session_folder_name}\n")
            create_empty_file(quizz_session_dir / "quizz_dau_gio.json", "[]\n")
            create_empty_file(quizz_session_dir / "quizz_cuoi_gio.md", f"# Quizz cuối giờ: {session_folder_name}\n")
            create_empty_file(quizz_session_dir / "quizz_cuoi_gio.json", "[]\n")
            total_files_created += 7

            # Homework exercises (17 folders: 15 tiered + 1 in-class synthesis + 1 mindmap + 1 root aggregated rubric)
            hw_dir = session_dir / "Bài tập"
            hw_dir.mkdir(parents=True, exist_ok=True)
            create_empty_file(hw_dir / "tieu_chi_danh_gia.md", f"# Bảng tiêu chí đánh giá tổng hợp: {session_folder_name}\n")
            total_files_created += 1

            hw_17_slugs = [
                (1, "1_van_dung_co_ban_1"),
                (2, "2_van_dung_co_ban_2"),
                (3, "3_van_dung_co_ban_3"),
                (4, "4_van_dung_co_ban_4"),
                (5, "5_van_dung_co_ban_5"),
                (6, "6_van_dung_co_ban_6"),
                (7, "7_van_dung_nang_cao_1"),
                (8, "8_van_dung_nang_cao_2"),
                (9, "9_van_dung_nang_cao_3"),
                (10, "10_phan_tich_1"),
                (11, "11_phan_tich_2"),
                (12, "12_phan_tich_3"),
                (13, "13_sang_tao_1"),
                (14, "14_sang_tao_2"),
                (15, "15_sang_tao_3"),
                (16, "16_tong_hop_demo_giang_vien_tren_lop"),
                (17, "17_tong_hop_he_thong_kien_thuc_mindmap"),
            ]
            for hw_idx, hw_slug in hw_17_slugs:
                sub_hw = hw_dir / hw_slug
                create_empty_file(sub_hw / "de_bai_bai_tap.md", f"# Đề bài tập {hw_idx}: {session_folder_name}\n")
                create_empty_file(sub_hw / "tieu_chi_cham_diem_ai.md", f"# Tiêu chí chấm điểm (AI) bài {hw_idx}: {session_folder_name}\n")
                total_files_created += 2
                total_dirs_created += 1

            # Lesson-level files (4 folders chuẩn: Bài đọc, Câu hỏi bài đọc, Quizz lesson, Bài thực hành)
            for l_idx, lesson_title in enumerate(lessons, 1):
                lesson_clean = sanitize_name(lesson_title)
                if not lesson_clean.lower().startswith("lesson"):
                    lesson_folder_name = f"Lesson {l_idx:02d} - {lesson_clean}"
                else:
                    # Format 'Lesson 01: ...' to 'Lesson 01 - ...'
                    lesson_folder_name = re.sub(r"^Lesson\s*(\d+)[\s:-]+", lambda m: f"Lesson {int(m.group(1)):02d} - ", lesson_clean, flags=re.IGNORECASE)

                lesson_dir = session_dir / lesson_folder_name
                lesson_dir.mkdir(parents=True, exist_ok=True)
                total_dirs_created += 1

                create_empty_file(lesson_dir / "Bài đọc" / "reading.html", f"<!-- Bài đọc: {lesson_folder_name} -->\n")
                create_empty_file(lesson_dir / "Câu hỏi bài đọc" / "reading_questions.md", f"# Câu hỏi bài đọc: {lesson_folder_name}\n")
                create_empty_file(lesson_dir / "Câu hỏi bài đọc" / "reading_questions.json", "[]\n")
                create_empty_file(lesson_dir / "Quizz lesson" / "quiz.md", f"# Quizz lesson: {lesson_folder_name}\n")
                create_empty_file(lesson_dir / "Quizz lesson" / "quiz.json", "[]\n")
                create_empty_file(lesson_dir / "Bài thực hành" / "practical_lab.md", f"# Bài thực hành: {lesson_folder_name}\n")
                create_empty_file(lesson_dir / "Bài thực hành" / "practical_lab.json", "{}\n")
                total_files_created += 7

        elif "Thực hành" in s_ht:
            practice_dir = session_dir / "Bài tập"
            practice_dir.mkdir(parents=True, exist_ok=True)
            create_empty_file(practice_dir / "tieu_chi_danh_gia.md", f"# Bảng tiêu chí đánh giá thực hành: {session_folder_name}\n")
            total_files_created += 1
            for i, level_label in enumerate(["de", "trung_binh", "kha", "gioi", "xuat_sac"], 1):
                ex_folder = practice_dir / f"{i}_bai_tap_muc_do_{level_label}"
                create_empty_file(ex_folder / "de_bai_thuc_hanh.md", f"# Đề bài thực hành mức {level_label.title()}: {session_folder_name}\n")
                create_empty_file(ex_folder / "tieu_chi_cham_diem_ai.md", f"# Tiêu chí chấm điểm (AI): {session_folder_name}\n")
                total_files_created += 2
                total_dirs_created += 1
            create_empty_file(session_dir / "Sơ đồ tư duy" / "mindmap.md", f"# Sơ đồ tư duy: {session_folder_name}\n")
            create_empty_file(session_dir / "Sơ đồ tư duy" / "session_mindmap.md", f"# Sơ đồ tư duy tổng hợp: {session_folder_name}\n")
            total_files_created += 2

        elif "Mini project" in s_ht:
            test_dir = session_dir / "Bài kiểm tra đầu giờ"
            for i in range(1, 5):
                create_empty_file(test_dir / f"bai_kiem_tra_{i:02d}_archetype_{i}.md", f"# Bài kiểm tra đầu giờ {i}: {session_folder_name}\n")
                total_files_created += 1

            create_empty_file(session_dir / "Tài liệu đặc tả SRS" / "tai_lieu_dac_ta_yeu_cau_srs.md", f"# Tài liệu đặc tả yêu cầu (SRS): {session_folder_name}\n")
            mp_dir = session_dir / "Mini project"
            create_empty_file(mp_dir / "de_bai_mini_project.md", f"# Đề bài Mini Project: {session_folder_name}\n")
            create_empty_file(mp_dir / "tieu_chi_cham_diem_ai.md", f"# Tiêu chí chấm điểm (AI): {session_folder_name}\n")
            total_files_created += 3

        elif "Project" in s_ht:
            create_empty_file(session_dir / "Tài liệu đặc tả SRS" / "tai_lieu_dac_ta_yeu_cau_srs.md", f"# Tài liệu đặc tả yêu cầu Capstone Project (SRS): {session_folder_name}\n")
            mp_dir = session_dir / "Mini project"
            create_empty_file(mp_dir / "de_bai_mini_project.md", f"# Đề bài Capstone Project: {session_folder_name}\n")
            create_empty_file(mp_dir / "tieu_chi_cham_diem_ai.md", f"# Tiêu chí chấm điểm (AI): {session_folder_name}\n")
            total_files_created += 3

        elif "Thi" in s_ht or "giữa môn" in s_ht or "cuối môn" in s_ht or "MIDTERM" in s_ht or "FINAL" in s_ht:
            create_empty_file(session_dir / "Đề thi thực hành" / "de_thi_thuc_hanh.md", f"# Đề thi thực hành: {session_folder_name}\n")
            create_empty_file(session_dir / "Đề thi thực hành" / "exam.md", f"# Đề thi thực hành: {session_folder_name}\n")
            create_empty_file(session_dir / "Đề thi trắc nghiệm" / "de_thi_trac_nghiem.json", "[]\n")
            create_empty_file(session_dir / "Câu hỏi vấn đáp" / "cau_hoi_van_dap.md", f"# Câu hỏi vấn đáp: {session_folder_name}\n")
            create_empty_file(session_dir / "Hướng dẫn chấm và Đáp án" / "grading_guide.md", f"# Hướng dẫn chấm và Đáp án: {session_folder_name}\n")
            create_empty_file(session_dir / "Tiêu chí đánh giá" / "rubric.md", f"# Tiêu chí đánh giá bài thi: {session_folder_name}\n")
            total_files_created += 6

    print(f"\n✅ [Hoàn tất] Đã khởi tạo thành công cấu trúc cho toàn bộ môn học!")
    print(f"  - Thư mục: {course_root.resolve()}")
    print(f"  - Tổng số Session: {len(sessions)}")
    print(f"  - Tổng số Thư mục con đã tạo: {total_dirs_created}")
    print(f"  - Tổng số File tài nguyên rỗng đã tạo: {total_files_created}")

if __name__ == "__main__":
    excel_file = "output/pms/Phát_triển_ứng_dụng_web/PM_IT106.xlsx"
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    scaffold_course_resources(excel_file)

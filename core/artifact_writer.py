"""
core/artifact_writer.py — Đường ghi artifact cấp lesson ra đĩa.

Tách khỏi core/graph.py vì hai mối quan tâm khác hẳn nhau: graph.py mô tả ĐỒ THỊ
sản xuất (node nào chạy sau node nào), còn quyết định artifact nào ghi vào thư mục
nào là chuyện của tầng lưu trữ. Gộp chung khiến graph.py phình gần 800 dòng và
không còn đọc được đồ thị trong một màn hình.

Đây vẫn là ĐƯỜNG GHI ĐĨA DUY NHẤT cho artifact cấp lesson, và vẫn được tái xuất
từ core.graph để không phá các import sẵn có.
"""

from pathlib import Path
from typing import Dict, Optional

from core.state import DEFAULT_LESSON_PARTS, AgentState


def write_state_artifacts_to_disk(
    state: AgentState,
    lesson_dir: Optional[Path] = None
) -> Dict[str, str]:
    """
    Ghi mọi artifact cấp lesson đang có trong state ra đĩa.

    ĐÂY LÀ ĐƯỜNG GHI ĐĨA DUY NHẤT cho artifact cấp lesson. Trước đây
    cli/commands/workflow_cmd.py tự viết lại toàn bộ logic này 3 lần (nhánh tuần tự,
    nhánh song song, nhánh session không có lesson con) — mỗi lần thêm một loại tài
    nguyên mới phải sửa 4 chỗ, và thực tế đã trôi khỏi nhau.

    Args:
        state: AgentState chứa các artifact đã sinh.
        lesson_dir: Thư mục lesson đích. Nếu None thì suy ra từ state qua get_lesson_dir().
            Caller nào đã tự tính thư mục (kèm tác dụng phụ đổi tên thư mục cho khớp
            tiêu đề mới) phải truyền vào đây, để không phụ thuộc vào việc 2 cách suy ra
            thư mục có trùng nhau hay không.

    Returns:
        Dict ánh xạ tên artifact -> đường dẫn đã ghi, hoặc "Skipped" nếu bỏ qua.
        Caller dùng kết quả này để dựng báo cáo, thay vì tự suy lại đường dẫn.
    """
    from agents.creator_agents import get_lesson_dir
    import json

    written: Dict[str, str] = {
        "html": "Skipped",
        "quiz": "Skipped",
        "practical_lab_md": "Skipped",
        "practical_lab_html": "Skipped",
        "reading_questions": "Skipped",
        "video_script": "Skipped",
    }

    try:
        if lesson_dir is None:
            lesson_dir = get_lesson_dir(state)
        lesson_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"  [Write Disk Warning] Không xác định được thư mục lesson: {e}")
        return written

    requested_parts = state.get("requested_parts") or DEFAULT_LESSON_PARTS

    # Mỗi artifact ghi trong try riêng: một artifact lỗi không được làm chết những
    # artifact còn lại. Trước đây cả khối nằm chung 1 try — chỉ cần lab thiếu
    # tech_stack là require_tech_stack raise, và video script phía sau im lặng
    # không bao giờ được ghi.

    # 1. Bài đọc HTML
    if "html" in requested_parts and state.get("html_content"):
        try:
            html_sub = lesson_dir / "Bài đọc"
            html_sub.mkdir(parents=True, exist_ok=True)
            html_path = html_sub / "reading.html"
            html_path.write_text(state["html_content"], encoding="utf-8")
            written["html"] = str(html_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi reading.html: {e}")

    # 2. Quizz (JSON + Excel)
    if "quiz" in requested_parts and state.get("quiz_json"):
        try:
            s_num_str = state.get("session_id", "").replace(" ", "")
            l_num_str = state.get("lesson_id", "").replace(" ", "")

            if l_num_str:
                quiz_sub = lesson_dir / "Quizz lesson"
                if not quiz_sub.exists() and (lesson_dir / "Câu hỏi Quizz").exists():
                    quiz_sub = lesson_dir / "Câu hỏi Quizz"
                excel_name = f"Quizz_{s_num_str}_{l_num_str}.xlsx"
            else:
                # Session không có lesson con: quiz thuộc về cả session (buổi thực hành),
                # nên đặt thẳng trong thư mục session và đặt tên theo buổi thay vì theo lesson.
                quiz_sub = lesson_dir / "Câu hỏi Quizz"
                excel_name = f"Quizz_{s_num_str}_Thuc_hanh.xlsx"

            quiz_sub.mkdir(parents=True, exist_ok=True)
            with open(quiz_sub / "quiz.json", "w", encoding="utf-8") as f:
                json.dump(state["quiz_json"], f, ensure_ascii=False, indent=2)
            written["quiz"] = str(quiz_sub / "quiz.json")

            from core.quiz_excel import export_lesson_quiz_to_excel
            excel_path_file = quiz_sub / excel_name

            quiz_data = state.get("quiz_json", {})
            if isinstance(quiz_data, dict):
                quiz_items = quiz_data.get("lesson_quiz") or quiz_data.get("quiz") or []
            else:
                quiz_items = quiz_data

            if quiz_items:
                export_lesson_quiz_to_excel(quiz_items, str(excel_path_file))
                written["quiz"] = str(excel_path_file)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi quiz: {e}")

    # 3. Bài thực hành — Markdown và HTML tách riêng: dựng được cái nào ghi cái đó.
    # Gộp chung 1 try sẽ khiến lỗi khi dựng Markdown nuốt luôn bản HTML mà LLM đã sinh.
    if state.get("practical_lab_markdown") or state.get("lab_json"):
        lab_sub = lesson_dir / "Bài thực hành"

        try:
            lab_md = state.get("practical_lab_markdown")
            if not lab_md and state.get("lab_json"):
                from agents.creators.practical_lab_creator import format_lab_to_markdown
                lab_md = format_lab_to_markdown(state["lab_json"])
            if lab_md:
                lab_sub.mkdir(parents=True, exist_ok=True)
                lab_md_path = lab_sub / "practical_lab.md"
                lab_md_path.write_text(lab_md, encoding="utf-8")
                written["practical_lab_md"] = str(lab_md_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi practical_lab.md: {e}")

        try:
            lab_html = state.get("practical_lab_html")
            if not lab_html and state.get("lab_json"):
                from agents.creators.practical_lab_creator import format_lab_to_html
                from core.state import require_tech_stack
                # require_tech_stack cố ý raise thay vì fallback ngầm về "python":
                # bản cũ ở workflow_cmd đọc nhầm key "tech_stack" kèm fallback cứng
                # "python", khiến lab của mọi khoá JS bị chạy qua Pyodide và luôn lỗi.
                current_stack = require_tech_stack(state, "write_state_artifacts_to_disk")
                lab_html = format_lab_to_html(state["lab_json"], current_stack)
            if lab_html:
                lab_sub.mkdir(parents=True, exist_ok=True)
                lab_html_path = lab_sub / "practical_lab.html"
                lab_html_path.write_text(lab_html, encoding="utf-8")
                written["practical_lab_html"] = str(lab_html_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi practical_lab.html: {e}")

    # 4. Câu hỏi bài đọc
    if state.get("reading_questions_markdown") or state.get("reading_questions_json"):
        try:
            rq_sub = lesson_dir / "Câu hỏi bài đọc"
            rq_sub.mkdir(parents=True, exist_ok=True)
            rq_md = state.get("reading_questions_markdown")
            if not rq_md and state.get("reading_questions_json"):
                from agents.creators.reading_questions_creator import format_reading_questions_to_markdown
                rq_md = format_reading_questions_to_markdown(state["reading_questions_json"])
            if rq_md:
                rq_path = rq_sub / "reading_questions.md"
                rq_path.write_text(rq_md, encoding="utf-8")
                written["reading_questions"] = str(rq_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi câu hỏi bài đọc: {e}")

    # 5. Kịch bản video
    wants_video = "video" in requested_parts or "video_script" in requested_parts
    if wants_video and state.get("video_script_markdown"):
        try:
            video_sub = lesson_dir / "Video"
            video_sub.mkdir(parents=True, exist_ok=True)
            video_path = video_sub / "SCRIPT.md"
            video_path.write_text(state["video_script_markdown"], encoding="utf-8")
            written["video_script"] = str(video_path)
        except Exception as e:
            print(f"  [Write Disk Warning] Lỗi ghi kịch bản video: {e}")

    return written

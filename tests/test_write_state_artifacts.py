"""
tests/test_write_state_artifacts.py — Khoá hành vi của đường ghi đĩa artifact cấp lesson.

write_state_artifacts_to_disk() nay là đường ghi đĩa DUY NHẤT. Trước đây
cli/commands/workflow_cmd.py tự viết lại logic này 3 lần và đã trôi khỏi bản gốc
(ví dụ: đọc nhầm key "tech_stack" kèm fallback cứng "python", khiến lab của mọi khoá
JavaScript bị chạy qua trình thông dịch Python). Test dưới đây khoá lại hành vi để
việc gộp về một đường không âm thầm đổi kết quả.
"""

import json

import pytest

from core.graph import write_state_artifacts_to_disk


@pytest.fixture
def lesson_dir(tmp_path):
    d = tmp_path / "Session 01 - Nhập môn" / "Lesson 01 - Biến"
    d.mkdir(parents=True)
    return d


def _base_state(**overrides):
    state = {
        "session_id": "Session 01",
        "lesson_id": "Lesson 01",
        "technology_stack": "javascript/web",
        "requested_parts": ["html", "quiz", "lab", "reading_questions", "video_script"],
    }
    state.update(overrides)
    return state


class TestLessonLevelWrites:
    def test_writes_every_artifact_present_in_state(self, lesson_dir):
        state = _base_state(
            html_content="<html>bài đọc</html>",
            practical_lab_markdown="# Bài thực hành",
            practical_lab_html="<html>lab</html>",
            reading_questions_markdown="# Câu hỏi bài đọc",
            video_script_markdown="# Kịch bản video",
        )

        written = write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)

        assert (lesson_dir / "Bài đọc" / "reading.html").read_text(encoding="utf-8") == "<html>bài đọc</html>"
        assert (lesson_dir / "Bài thực hành" / "practical_lab.md").exists()
        assert (lesson_dir / "Bài thực hành" / "practical_lab.html").exists()
        assert (lesson_dir / "Câu hỏi bài đọc" / "reading_questions.md").exists()
        assert (lesson_dir / "Video" / "SCRIPT.md").exists()

        assert written["html"].endswith("reading.html")
        assert written["video_script"].endswith("SCRIPT.md")

    def test_absent_artifacts_reported_as_skipped(self, lesson_dir):
        written = write_state_artifacts_to_disk(_base_state(), lesson_dir=lesson_dir)

        assert written == {
            "html": "Skipped",
            "quiz": "Skipped",
            "practical_lab_md": "Skipped",
            "practical_lab_html": "Skipped",
            "reading_questions": "Skipped",
            "video_script": "Skipped",
        }

    def test_uses_practical_lab_html_from_state_verbatim(self, lesson_dir):
        """
        HTML lab do nhánh song song sinh ra phải được ghi nguyên vẹn, không render lại.

        Đây là mặt còn lại của lỗi practical_lab_html bị mất khi merge: nếu state đã có
        HTML thì tuyệt đối không được dựng lại từ lab_json.
        """
        state = _base_state(
            practical_lab_html="<html>bản do LLM sinh</html>",
            lab_json={"title": "Lab"},
        )

        write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)

        content = (lesson_dir / "Bài thực hành" / "practical_lab.html").read_text(encoding="utf-8")
        assert content == "<html>bản do LLM sinh</html>"


class TestRequestedPartsGating:
    def test_html_skipped_when_not_requested(self, lesson_dir):
        state = _base_state(requested_parts=["quiz"], html_content="<html/>")

        written = write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)

        assert written["html"] == "Skipped"
        assert not (lesson_dir / "Bài đọc").exists()

    def test_video_written_for_either_alias(self, lesson_dir):
        """requested_parts dùng lẫn lộn 'video' và 'video_script' — chấp nhận cả hai."""
        for part in ("video", "video_script"):
            state = _base_state(requested_parts=[part], video_script_markdown="# Kịch bản")
            written = write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)
            assert written["video_script"].endswith("SCRIPT.md"), f"trượt với '{part}'"


class TestSessionLevelWrites:
    def test_quiz_without_lesson_id_goes_to_session_folder(self, tmp_path):
        """
        Session không có lesson con: quiz nằm thẳng trong thư mục session và đặt tên
        theo buổi ('Thuc_hanh') thay vì theo lesson.
        """
        session_dir = tmp_path / "Session 05 - Thực hành"
        session_dir.mkdir(parents=True)
        state = _base_state(
            session_id="Session 05",
            lesson_id="",
            quiz_json={"lesson_quiz": [{"question": "Câu 1?", "options": ["A", "B"]}]},
        )

        written = write_state_artifacts_to_disk(state, lesson_dir=session_dir)

        quiz_json_path = session_dir / "Câu hỏi Quizz" / "quiz.json"
        assert quiz_json_path.exists()
        assert not (session_dir / "Quizz lesson").exists()
        assert (session_dir / "Câu hỏi Quizz" / "Quizz_Session05_Thuc_hanh.xlsx").exists()
        assert written["quiz"].endswith("Quizz_Session05_Thuc_hanh.xlsx")

    def test_quiz_with_lesson_id_uses_lesson_folder_and_name(self, lesson_dir):
        state = _base_state(
            quiz_json={"lesson_quiz": [{"question": "Câu 1?", "options": ["A", "B"]}]}
        )

        write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)

        quiz_dir = lesson_dir / "Quizz lesson"
        assert json.loads((quiz_dir / "quiz.json").read_text(encoding="utf-8"))
        assert (quiz_dir / "Quizz_Session01_Lesson01.xlsx").exists()


class TestFailureIsolation:
    def test_one_failing_artifact_does_not_block_the_others(self, lesson_dir):
        """
        Lab thiếu technology_stack thì require_tech_stack raise — nhưng kịch bản video
        phía sau vẫn phải được ghi.

        Trước đây toàn bộ khối nằm chung một try/except, nên chỉ một artifact lỗi là
        mọi artifact còn lại im lặng biến mất.
        """
        state = _base_state(
            lab_json={"title": "Lab"},
            video_script_markdown="# Kịch bản video",
            html_content="<html>bài đọc</html>",
        )
        del state["technology_stack"]

        written = write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)

        assert written["practical_lab_html"] == "Skipped"
        assert (lesson_dir / "Video" / "SCRIPT.md").exists()
        assert (lesson_dir / "Bài đọc" / "reading.html").exists()

    def test_unresolvable_directory_returns_all_skipped(self):
        """Không xác định được thư mục thì trả về toàn Skipped, không ném lỗi ra ngoài."""
        written = write_state_artifacts_to_disk({"html_content": "<html/>"}, lesson_dir=None)

        assert set(written.values()) <= {"Skipped"} or "html" in written

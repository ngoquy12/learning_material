"""
Khóa các lỗi quy trình liên quan đến phạm vi kiến thức, chạy tiếp (resume), batch
song song và ngữ cảnh cho tài nguyên cấp session.
"""

import unittest

from core.batch_runner import execute_lessons_batch_parallel
from core.graph import ensure_dynamic_scope_calculated
from core.lesson_summary import build_lesson_summary
from core.resume import merge_resume_state
from core.scope_calculator import validate_text_against_scope


class TestScopeNotRecomputedFromWindow(unittest.TestCase):
    def test_pham_vi_tinh_tren_toan_khoa_khong_bi_ghi_de(self):
        state = {
            "session_id": "Session 01",
            "lesson_id": "Lesson 01",
            "scope_source": "full_course",
            "allowed_scope": ["bien"],
            "forbidden_scope": ["decorator", "metaclass"],
            # cửa sổ 3 session: nếu tính lại, 'metaclass' ở buổi xa sẽ biến mất
            "full_curriculum": '[{"session_id": "Session 01", "lessons": [{"lesson_id": "Lesson 01", "title": "bien"}]}]',
        }
        out = ensure_dynamic_scope_calculated(state)
        self.assertEqual(out["forbidden_scope"], ["decorator", "metaclass"])
        self.assertIn("metaclass", out["core_ssot"]["forbidden_scope"])


class TestDisclaimerStripping(unittest.TestCase):
    def test_tu_chua_note_trong_tu_khac_khong_xoa_phan_con_lai(self):
        # 'annotation' chứa 'note' nhưng không phải từ 'note'
        self.assertEqual(
            validate_text_against_scope("Dùng annotation và decorator ở đây.", {"decorator"}),
            ["decorator"],
        )

    def test_cau_cam_van_duoc_bo_qua(self):
        self.assertEqual(
            validate_text_against_scope("Lưu ý: không dùng decorator. Bài này ổn.", {"decorator"}),
            [],
        )


class TestResumeMerge(unittest.TestCase):
    def test_cau_hinh_moi_thang_ket_qua_cu_duoc_giu(self):
        cached = {
            "requested_parts": ["html"],
            "html_content": "<html>da sinh</html>",
            "artifacts_status": {"html": "Approved", "quiz": "Skipped"},
        }
        fresh = {
            "requested_parts": ["quiz"],
            "forbidden_scope": ["x"],
            "artifacts_status": {"html": "Pending", "quiz": "Pending"},
        }
        merged = merge_resume_state(cached, fresh)
        self.assertEqual(merged["requested_parts"], ["quiz"])
        self.assertEqual(merged["forbidden_scope"], ["x"])
        self.assertEqual(merged["html_content"], "<html>da sinh</html>")
        self.assertEqual(merged["artifacts_status"]["html"], "Approved")
        self.assertEqual(merged["artifacts_status"]["quiz"], "Pending")


class TestBatchFailureVisible(unittest.TestCase):
    def test_lesson_loi_duoc_danh_dau_failed(self):
        def workflow(state):
            if state["lesson_id"] == "L2":
                raise RuntimeError("hong")
            state["artifacts_status"] = {"session": "PUBLISHED"}
            return state

        states = [{"lesson_id": f"L{i}", "artifacts_status": {}} for i in (1, 2)]
        out = execute_lessons_batch_parallel(states, workflow, max_workers=2)
        self.assertEqual(out[0]["artifacts_status"]["session"], "PUBLISHED")
        self.assertEqual(out[1]["artifacts_status"]["session"], "FAILED")
        self.assertIn("hong", out[1]["review_logs"][-1]["feedback"])


class TestLessonSummary(unittest.TestCase):
    def test_tom_tat_lay_de_muc_tu_bai_doc_that(self):
        html = "<h2>Biến là gì</h2><p>Biến lưu giá trị.</p><h3>Kiểu dữ liệu</h3><p>Số và chuỗi.</p>"
        text = build_lesson_summary("Bài 1", {"html_content": html})
        self.assertIn("Biến là gì", text)
        self.assertIn("Kiểu dữ liệu", text)
        self.assertNotIn("```python", text)

    def test_bai_dang_la_placeholder_khong_duoc_dung(self):
        text = build_lesson_summary("Bài 1", {"html_content": "<!-- Empty outline -->"})
        self.assertEqual(text.strip(), "Bài học: Bài 1")


if __name__ == "__main__":
    unittest.main()

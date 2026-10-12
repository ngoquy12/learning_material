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




class TestReadingBudgetValidator(unittest.TestCase):
    def _page(self, words):
        body = " ".join(["từ"] * words)
        sections = "".join(
            f'<section id="section-{i}"><span id="sec-2-4"></span><h2>{i}. Mục</h2><p>{body if i == 1 else "ý"}</p>'
            + ('<h3>a</h3><h3>b</h3><h3>c</h3><pre><code>x = 1</code></pre>' if i == 3 else "")
            + "</section>"
            for i in range(1, 6)
        )
        return f"<!doctype html><html><body><h1>Bài</h1>{sections}</body></html>"

    def _errors(self, words, **meta):
        from core.validators.reading_validator import validate_reading_material

        meta.setdefault("enforce_word_budget", True)
        meta.setdefault("tech_stack", "javascript")
        meta.setdefault("skip_size_check", True)
        return validate_reading_material(self._page(words), meta)[1]

    def test_bai_qua_dai_bi_tu_choi(self):
        self.assertTrue(any("quá dài" in e for e in self._errors(3000)))

    def test_bai_trong_gioi_han_khong_bi_tu_choi_vi_do_dai(self):
        self.assertFalse(any("quá dài" in e or "quá ngắn" in e for e in self._errors(1700)))

    def test_khong_bat_khi_khong_bat_co(self):
        self.assertFalse(any("quá dài" in e for e in self._errors(3000, enforce_word_budget=False)))

    def test_mon_khong_viet_ma_khong_bat_buoc_khoi_ma(self):
        from core.validators.reading_validator import validate_reading_material

        html = self._page(1700).replace("<pre><code>x = 1</code></pre>", "")
        errs = validate_reading_material(html, {"tech_stack": "Agile Scrum"})[1]
        self.assertFalse(any("khối mã nguồn" in e for e in errs))
        errs_code = validate_reading_material(html, {"tech_stack": "javascript"})[1]
        self.assertTrue(any("khối mã nguồn" in e for e in errs_code))


if __name__ == "__main__":
    unittest.main()

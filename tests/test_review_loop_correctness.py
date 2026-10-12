"""
Khóa các lỗi quy trình khiến kết quả sai mà không ai biết:
- reviewer không từ chối được (trạng thái APPROVED đặt sớm),
- phản hồi reviewer không tới lần sinh lại, bộ nhớ đệm trả lại bản đã bị từ chối,
- reviewer tự duyệt khi không đọc được phán quyết,
- nội dung giả (quiz/lab/video) được ghi như thật,
- session luôn PUBLISHED dù có tài nguyên hỏng.
"""

import unittest
from unittest import mock

from core import graph
from core.artifact_status import ArtifactStatus
from core.exceptions import GenerationError
from core.retry_feedback import (
    clear_retry_feedback,
    get_retry_feedback,
    retry_feedback_block,
    set_retry_feedback,
)
from core.semantic_cache import _make_hash


class _Clean:
    is_clean = True


def _base_state():
    return {
        "session_id": "Session 01",
        "lesson_id": "Lesson 01",
        "artifacts_status": {},
        "review_logs": [],
    }


class TestHtmlReviewLoop(unittest.TestCase):
    def _run(self, reviews):
        """Chạy vòng HTML với dãy phán quyết `reviews`; trả về (state, số lần sinh, feedback thấy được)."""
        seen_feedback = []
        calls = {"writer": 0}

        def fake_writer(state):
            calls["writer"] += 1
            seen_feedback.append(get_retry_feedback(state, "html"))
            state["html_content"] = f"<html>v{calls['writer']}</html>"
            # Mô phỏng creator thật: không được tự đặt APPROVED.
            state["artifacts_status"]["html"] = ArtifactStatus.PENDING
            return state

        it = iter(reviews)
        with mock.patch.object(graph, "html_writer_agent", fake_writer), \
             mock.patch.object(graph, "html_ux_reviewer", lambda s: next(it)), \
             mock.patch.object(graph, "audit_artifact_scope", lambda *a, **k: _Clean()), \
             mock.patch.object(graph, "write_state_artifacts_to_disk", lambda s: None), \
             mock.patch.object(graph, "save_state_checkpoint", lambda s: None):
            fn = graph.pipeline_html_production
            fn = getattr(fn, "func", fn)
            state = fn(_base_state())
        return state, calls["writer"], seen_feedback

    def test_ban_bi_tu_choi_khong_duoc_coi_la_da_duyet(self):
        rejected = {"status": "REJECTED", "feedback": "Thiếu sơ đồ"}
        state, writes, _ = self._run([rejected, rejected, rejected])
        self.assertEqual(writes, 3)
        self.assertEqual(state["artifacts_status"]["html"], ArtifactStatus.PENDING_HUMAN_REVIEW)

    def test_phan_hoi_reviewer_toi_lan_sinh_lai(self):
        rejected = {"status": "REJECTED", "feedback": "Thiếu sơ đồ"}
        approved = {"status": "APPROVED", "feedback": ""}
        state, writes, seen = self._run([rejected, approved])
        self.assertEqual(writes, 2)
        self.assertEqual(seen[0], "")
        self.assertIn("Thiếu sơ đồ", seen[1])
        self.assertEqual(state["artifacts_status"]["html"], ArtifactStatus.APPROVED)
        self.assertEqual(get_retry_feedback(state, "html"), "")


class TestRetryFeedback(unittest.TestCase):
    def test_khoi_phan_hoi_rong_o_lan_dau(self):
        self.assertEqual(retry_feedback_block({}, "html"), "")

    def test_dat_va_xoa(self):
        state = {}
        set_retry_feedback(state, "quiz", "  Thiếu câu 5 ")
        self.assertIn("Thiếu câu 5", retry_feedback_block(state, "quiz"))
        clear_retry_feedback(state, "quiz")
        self.assertEqual(retry_feedback_block(state, "quiz"), "")


class TestSemanticCacheKey(unittest.TestCase):
    def test_hash_phan_biet_prompt_khac_nhau_o_phan_duoi(self):
        head = "x" * 1500
        self.assertNotEqual(_make_hash("s", head + "A"), _make_hash("s", head + "B"))


class TestReviewersNeverAutoApprove(unittest.TestCase):
    def test_khong_doc_duoc_phan_quyet_thi_tu_choi(self):
        from agents.reviewer_agents import _normalize_review, _unreadable_review

        self.assertEqual(_unreadable_review("X")["status"], "REJECTED")
        self.assertEqual(_normalize_review("rác", "X")["status"], "REJECTED")
        self.assertEqual(_normalize_review({"status": "maybe"}, "X")["status"], "REJECTED")

    def test_status_viet_thuong_duoc_chuan_hoa(self):
        from agents.reviewer_agents import _normalize_review

        out = _normalize_review({"status": "approved"}, "X")
        self.assertEqual(out["status"], "APPROVED")
        self.assertIsInstance(out["feedback"], str)

    def test_reject_thieu_feedback_van_co_ly_do(self):
        from agents.reviewer_agents import _normalize_review

        out = _normalize_review({"status": "REJECTED"}, "X")
        self.assertTrue(out["feedback"])


class TestNoFakeContent(unittest.TestCase):
    def _state(self):
        state = _base_state()
        state.update(
            {
                "technology_stack": "Python",
                "core_ssot": {"session_title": "T"},
                "html_content": "<p>noi dung</p>",
                "lesson_content": {"problem": "p"},
            }
        )
        return state

    def test_quiz_khong_du_5_cau_thi_nem_loi(self):
        from agents.creators import quiz_creator

        state = self._state()
        with mock.patch.object(quiz_creator, "call_llm", return_value="[]"):
            with self.assertRaises(GenerationError):
                quiz_creator.quiz_agent(state)
        self.assertNotIn("quiz_json", state)
        self.assertNotIn("lab_json", state)

    def test_video_rong_thi_nem_loi(self):
        from agents.creators import video_script_creator as v

        state = self._state()
        with mock.patch.object(v, "call_llm", return_value="   "):
            with self.assertRaises(GenerationError):
                v.video_script_creator_agent(state)
        self.assertNotIn("video_script_markdown", state)

    def test_lab_khong_hop_le_thi_nem_loi(self):
        from agents.creators import practical_lab_creator as p

        state = self._state()
        with mock.patch.object(p, "call_llm", return_value="{}"):
            with self.assertRaises(GenerationError):
                p.practical_lab_creator_agent(state)
        self.assertNotIn("lab_json", state)


class TestSessionCompiler(unittest.TestCase):
    def _compile(self, statuses):
        from agents.creators.session_compiler_creator import session_compiler_agent

        state = _base_state()
        state["artifacts_status"] = dict(statuses)
        return session_compiler_agent(state)["artifacts_status"]["session"]

    def test_chi_published_khi_moi_tai_nguyen_dat(self):
        self.assertEqual(
            self._compile({"html": ArtifactStatus.APPROVED, "quiz": ArtifactStatus.APPROVED}),
            ArtifactStatus.PUBLISHED,
        )

    def test_co_tai_nguyen_hong_thi_khong_published(self):
        self.assertEqual(
            self._compile({"html": ArtifactStatus.APPROVED, "quiz": ArtifactStatus.FAILED}),
            ArtifactStatus.FAILED,
        )

    def test_can_nguoi_ra_lai_thi_khong_published(self):
        self.assertEqual(
            self._compile({"html": ArtifactStatus.PENDING_HUMAN_REVIEW}),
            ArtifactStatus.PENDING_HUMAN_REVIEW,
        )


if __name__ == "__main__":
    unittest.main()

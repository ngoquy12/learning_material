import unittest
from unittest import mock

from core import graph
from core.lesson_summary import approved_reading_text


def _fake_branches(seen):
    def make(name):
        def run(state):
            seen[name] = state.get("html_content", "")
            if name == "HTML":
                state["html_content"] = "<h2>BÀI ĐỌC CUỐI</h2>" + "x" * 1200
            return state
        return graph.DerivedPipeline(name, name.lower(), run)

    return tuple(make(n) for n in ("HTML", "Quiz", "PracticalLab", "ReadingQuestions", "VideoScript"))


class TestStagePlan(unittest.TestCase):
    def test_nhanh_phu_thuoc_bai_doc_chay_sau(self):
        stages = graph.plan_pipeline_stages(_fake_branches({}))
        self.assertEqual([b.name for b in stages[0]], ["HTML", "PracticalLab"])
        self.assertEqual({b.name for b in stages[1]}, {"Quiz", "ReadingQuestions", "VideoScript"})

    def test_nhanh_phu_thuoc_thay_bai_doc_da_sinh(self):
        seen = {}
        state = {"session_id": "S1", "lesson_id": "L1", "artifacts_status": {}, "review_logs": [], "html_content": ""}
        with mock.patch.object(graph, "DERIVED_PIPELINES", _fake_branches(seen)), \
             mock.patch.object(graph, "save_state_checkpoint", lambda s: None):
            out = graph.node_parallel_derived_production.func(state) \
                if hasattr(graph.node_parallel_derived_production, "func") \
                else graph.node_parallel_derived_production(state)
        self.assertEqual(seen["Quiz"][:21], "<h2>BÀI ĐỌC CUỐI</h2>"[:21])
        self.assertTrue(seen["VideoScript"].startswith("<h2>BÀI ĐỌC CUỐI"))
        self.assertTrue(seen["ReadingQuestions"].startswith("<h2>BÀI ĐỌC CUỐI"))
        self.assertEqual(seen["HTML"], "")
        self.assertTrue(out["html_content"].startswith("<h2>BÀI ĐỌC CUỐI"))


class TestApprovedReadingText(unittest.TestCase):
    def test_placeholder_khong_duoc_dung(self):
        self.assertEqual(approved_reading_text({"html_content": "<!-- Empty outline -->" + "x" * 2000}), "")
        self.assertEqual(approved_reading_text({}), "")

    def test_lay_van_ban_hien_thi(self):
        html = "<script>var a=1</script><h2>Tiêu đề</h2><p>" + "nội dung " * 200 + "</p>"
        text = approved_reading_text({"html_content": html})
        self.assertIn("Tiêu đề", text)
        self.assertNotIn("var a", text)


if __name__ == "__main__":
    unittest.main()


class TestDomainDrift(unittest.TestCase):
    def test_bai_viet_nhac_ten_domain_khong_bi_bao_troi(self):
        from core.scope_gate import audit_artifact_scope

        state = {"chosen_domain": "SHOPEE_FOOD", "technology_stack": "Python"}
        text = "Hệ thống ShopeeFood tính phí giao hàng cho đơn đặt món."
        self.assertFalse(audit_artifact_scope(text, state, "html").domain_drift)

    def test_bai_viet_nhac_thuc_the_van_hop_le(self):
        from core.scope_gate import audit_artifact_scope

        state = {"chosen_domain": "SHOPEE_FOOD", "technology_stack": "Python"}
        self.assertFalse(audit_artifact_scope("class FoodOrder: pass", state, "html").domain_drift)

    def test_bai_viet_domain_khac_bi_bao_troi(self):
        from core.scope_gate import audit_artifact_scope

        state = {"chosen_domain": "SHOPEE_FOOD", "technology_stack": "Python"}
        self.assertTrue(audit_artifact_scope("Hệ thống quản lý thư viện mượn sách.", state, "html").domain_drift)

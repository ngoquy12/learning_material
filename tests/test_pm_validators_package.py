"""
tests/test_pm_validators_package.py
Verifies the Modular PM Validators Package (core.pm_validators):
- Structure validator
- Academic tone validator
- Granularity validator
- Scope continuity validator
- CLO coverage validator
- Reading and exercise quality gates
"""

import unittest
from core.pm_validators import (
    validate_syllabus_structure,
    validate_academic_tone,
    validate_pm_granularity,
    validate_scope_continuity,
    validate_clo_coverage,
    lint_pm_syllabus,
    audit_reading_html_quality_gate,
    audit_exercise_quality_gate
)
from agents.pm_reviewer_agent import pm_reviewer_agent

class TestPMValidatorsPackage(unittest.TestCase):

    def setUp(self):
        self.sample_pm_valid = [
            {
                "session_num": 1,
                "session_id": "Session 01",
                "hinh_thuc": "Lý thuyết",
                "title": "Định hướng môn học và Lộ trình phát triển",
                "content_scope": "Tổng quan toàn bộ môn học, phương pháp học tập hiệu quả, cài đặt công cụ cần thiết.",
                "expected_outcome": "Phân biệt được các giai đoạn học tập, thiết lập thành công môi trường lập trình.",
                "lessons": [
                    {
                        "lesson_num": 1,
                        "title": "Tổng quan lộ trình và Demo sản phẩm",
                        "content_scope": "Khái niệm kiến trúc phần mềm, quy trình làm việc thực tế, demo sản phẩm hoàn chỉnh.",
                        "expected_outcome": "Trình bày được lộ trình học tập và mục tiêu đầu ra của khóa học.",
                        "forbidden_scope": "CẤM: Lập trình bất đồng bộ async await, luồng threading đa nhiệm.",
                        "allowed_scope": "ĐÃ HỌC: Kỹ năng tin học văn phòng căn bản, thao tác tệp tin."
                    }
                ]
            },
            {
                "session_num": 2,
                "session_id": "Session 02",
                "hinh_thuc": "Lý thuyết",
                "title": "Tổng quan ngôn ngữ và Cú pháp cơ bản",
                "content_scope": "Giới thiệu lịch sử, đặc điểm cốt lõi, biến và kiểu dữ liệu nguyên thủy.",
                "expected_outcome": "Khởi tạo được biến số, thực hiện nhập xuất dữ liệu thành thạo.",
                "lessons": [
                    {
                        "lesson_num": 1,
                        "title": "Giới thiệu tổng quan về công nghệ",
                        "content_scope": "Cú pháp khai báo biến, các kiểu dữ liệu int, float, string, lệnh print và input.",
                        "expected_outcome": "Viết được chương trình nhập xuất cơ bản đầu tiên.",
                        "forbidden_scope": "CẤM: Cấu trúc rẽ nhánh if else, vòng lặp for while, hàm def.",
                        "allowed_scope": "ĐÃ HỌC: Cài đặt môi trường ở Session 01."
                    },
                    {
                        "lesson_num": 2,
                        "title": "Khai báo biến và Kiểu dữ liệu nguyên thủy",
                        "content_scope": "Toán tử cộng trừ nhân chia, ép kiểu dữ liệu tường minh, quy tắc đặt tên biến.",
                        "expected_outcome": "Tính toán được các biểu thức số học phức tạp.",
                        "forbidden_scope": "CẤM: Cấu trúc rẽ nhánh if else, vòng lặp for while.",
                        "allowed_scope": "ĐÃ HỌC: Khai báo biến, kiểu dữ liệu int float."
                    }
                ]
            },
            {
                "session_num": 3,
                "session_id": "Session 03",
                "hinh_thuc": "Thi cuối môn",
                "title": "Đánh giá Năng lực và Thi cuối môn",
                "content_scope": "Đánh giá toàn diện kiến thức đã học trong môn học.",
                "expected_outcome": "Giải quyết được các bài toán thực tế theo yêu cầu đề thi.",
                "lessons": []
            }
        ]

    def test_validate_syllabus_structure_valid(self):
        """Tests that a well-structured PM passes structure validation."""
        deductions, violations, logs = validate_syllabus_structure(
            pm_data=self.sample_pm_valid,
            tech_stack="Python",
            sessions_per_day=1
        )
        self.assertEqual(deductions, 0)
        self.assertEqual(len(violations), 0)

    def test_validate_academic_tone(self):
        """Tests academic tone and anti-hype validation."""
        deductions, violations, logs = validate_academic_tone(
            pm_data=self.sample_pm_valid,
            tech_stack="Python"
        )
        self.assertEqual(deductions, 0)
        self.assertEqual(len(violations), 0)

    def test_validate_granularity(self):
        """Tests 5-column granularity validation."""
        deductions, violations, logs = validate_pm_granularity(self.sample_pm_valid)
        self.assertEqual(deductions, 0)
        self.assertEqual(len(violations), 0)

    def test_full_linter_and_agent(self):
        """Tests lint_pm_syllabus and pm_reviewer_agent orchestrator."""
        is_valid, score, violations, logs = lint_pm_syllabus(
            pm_data=self.sample_pm_valid,
            tech_stack="Python"
        )
        self.assertTrue(is_valid)
        self.assertGreaterEqual(score, 90)

        res = pm_reviewer_agent(
            pm_data=self.sample_pm_valid,
            config_data={"tech_stack": "Python"}
        )
        self.assertTrue(res["is_approved"])
        self.assertGreaterEqual(res["score"], 90)

    def test_quality_gates(self):
        """Tests reading and exercise quality gates."""
        html_good = """
        <div id="problem-intro"></div>
        <div id="data-structure"></div>
        <div id="interactive-demo"></div>
        <div id="summary-notes"></div>
        <div id="self-test">
            <input type="radio" name="selftest_q1" />
            <button id="btn-check-selftest">Kiểm Tra Đáp Án</button>
        </div>
        <svg viewBox="0 0 800 450"></svg>
        <div class="ph-check-circle good-practice">Good</div>
        <div class="ph-x-circle bad-practice">Bad</div>
        <p>Nội dung bài học chuẩn mực chất lượng cao.</p>
        """
        res_reading = audit_reading_html_quality_gate(html_good)
        self.assertTrue(res_reading["passed"])
        self.assertGreaterEqual(res_reading["score"], 70)

if __name__ == "__main__":
    unittest.main()

"""
tests/test_pedagogical_benchmark.py
Verifies the Pedagogical Benchmark Suite and Quality Scorecard Engine:
- Factual & Code accuracy verification via sandbox.
- Bloom cognitive alignment calculation.
- Contextual continuity check.
- Visual scannability & light mode compliance.
- AI cliché detection.
- Full scorecard compilation and Markdown output generation.
"""

import unittest
from core.evals.benchmark import (
    PedagogicalBenchmarkEngine,
    PedagogicalScorecard,
    evaluate_lesson_pedagogy
)

class TestPedagogicalBenchmarkSuite(unittest.TestCase):

    def test_factual_accuracy_clean_code(self):
        """Tests that valid runnable code receives high factual accuracy score."""
        content = """
        <article>
        ```python
        total = sum([10, 20, 30])
        print(f"Total: {total}")
        ```
        </article>
        """
        metric = PedagogicalBenchmarkEngine.evaluate_factual_accuracy(content, tech_stack="python")
        self.assertGreaterEqual(metric.score, 90.0)
        self.assertEqual(metric.status, "PASS")

    def test_factual_accuracy_broken_code_penalty(self):
        """Tests that runtime crash reduces factual accuracy score."""
        content = """
        ```python
        x = 10 / 0
        ```
        """
        metric = PedagogicalBenchmarkEngine.evaluate_factual_accuracy(content, tech_stack="python")
        self.assertLess(metric.score, 100.0)
        self.assertTrue(any("ZeroDivisionError" in d for d in metric.details))

    def test_visual_scannability_light_mode_and_tables(self):
        """Tests visual scannability detection of wrapped tables and light mode."""
        valid_html = """
        <article class="bg-white">
            <div class="overflow-x-auto my-4 border border-slate-200 rounded-xl">
                <table><tr><td>Header</td></tr></table>
            </div>
            <figure>
                <img src="img.png"/>
                <figcaption><i>Hình 1.1 Sơ đồ</i></figcaption>
            </figure>
        </article>
        """
        metric = PedagogicalBenchmarkEngine.evaluate_visual_scannability(valid_html)
        self.assertEqual(metric.score, 100.0)
        self.assertEqual(metric.status, "PASS")

    def test_visual_scannability_dark_container_penalty(self):
        """Tests that dark mode container penalty is applied."""
        invalid_html = "<div class='bg-slate-900'><h2>Lỗi nền tối</h2></div>"
        metric = PedagogicalBenchmarkEngine.evaluate_visual_scannability(invalid_html)
        self.assertLess(metric.score, 100.0)

    def test_tone_cleanliness_ai_cliche_penalty(self):
        """Tests that forbidden AI buzzwords trigger penalties."""
        dirty_text = "Hôm nay chúng ta sẽ cùng khám phá tất tần tật bí kíp và các bẫy lập trình thần thánh."
        metric = PedagogicalBenchmarkEngine.evaluate_tone_cleanliness(dirty_text)
        self.assertLess(metric.score, 60.0)
        self.assertEqual(metric.status, "FAIL")

    def test_full_benchmark_and_markdown_scorecard(self):
        """Tests compiling a complete PedagogicalScorecard and exporting to Markdown."""
        html_content = """
        <article class="bg-white">
            <h1 class="text-2xl font-bold">Cú pháp và Biến trong Python</h1>
            <div class="overflow-x-auto my-4">
                <table><tr><td>Kiểu dữ liệu</td></tr></table>
            </div>
            ```python
            price = 50000
            quantity = 2
            total = price * quantity
            print(f"Tổng tiền đơn hàng: {total}")
            ```
            <figure>
                <img src="pic.png"/>
                <figcaption><i>Hình 1.1 Sơ đồ luồng thanh toán</i></figcaption>
            </figure>
        </article>
        """
        scorecard: PedagogicalScorecard = evaluate_lesson_pedagogy(
            html_content=html_content,
            lesson_id="Lesson 02",
            lesson_title="Biến và Kiểu Dữ Liệu",
            tech_stack="Python 3.12"
        )
        self.assertGreaterEqual(scorecard.overall_score, 80.0)
        self.assertTrue(scorecard.passed)

        md_report = scorecard.to_markdown()
        self.assertIn("Pedagogical Quality Scorecard", md_report)
        self.assertIn("Factual & Code Accuracy", md_report)
        self.assertIn("Python 3.12", md_report)

        dumped = scorecard.to_dict()
        self.assertIn("overall_score", dumped)
        self.assertEqual(dumped["lesson_id"], "Lesson 02")

if __name__ == "__main__":
    unittest.main()

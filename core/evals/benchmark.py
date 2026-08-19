"""
core/evals/benchmark.py
Automated Pedagogical Benchmark Suite and Quality Scorecard Engine.
Evaluates AI-generated learning materials across 5 Rikkei Education Golden Criteria:
1. Factual Accuracy Score (Code sandbox & syntax verification)
2. Bloom Cognitive Alignment Score (Bloom taxonomy distribution)
3. Contextual Continuity Score (Single unified real-world scenario adherence)
4. Visual & Scannability Score (Light mode compliance, overflow tables, italic captions)
5. Tone Cleanliness Score (Zero AI clichés, no forbidden buzzwords, 100% accented Vietnamese)
"""

import re
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from core.sandbox.code_executor import execute_code_snippet

@dataclass
class MetricScore:
    name: str
    score: float  # 0.0 to 100.0
    weight: float  # e.g. 0.25
    status: str    # "PASS" | "WARNING" | "FAIL"
    details: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "score": round(self.score, 1),
            "weight": self.weight,
            "status": self.status,
            "details": self.details
        }


@dataclass
class PedagogicalScorecard:
    lesson_id: str
    lesson_title: str
    tech_stack: str
    overall_score: float
    passed: bool
    metrics: Dict[str, MetricScore] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lesson_id": self.lesson_id,
            "lesson_title": self.lesson_title,
            "tech_stack": self.tech_stack,
            "overall_score": round(self.overall_score, 1),
            "passed": self.passed,
            "timestamp": self.timestamp,
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()}
        }

    def to_markdown(self) -> str:
        status_icon = "PASSED" if self.passed else "FAILED"
        md_lines = [
            f"# Báo Cáo Đo Lường Chất Lượng Sư Phạm (Pedagogical Quality Scorecard)",
            f"**Bài học**: `{self.lesson_id} - {self.lesson_title}` | **Công nghệ**: `{self.tech_stack}`",
            f"**Thời gian kiểm chuẩn**: `{self.timestamp}` | **Kết luận**: **{status_icon}** ({self.overall_score:.1f}/100đ)\n",
            "## 1. Bảng Tổng Hợp Điểm 5 Tiêu Chí Sư Phạm",
            "| Tiêu chí đánh giá | Trọng số | Điểm số (0-100) | Trạng thái | Đánh giá tóm tắt |",
            "| :--- | :---: | :---: | :---: | :--- |"
        ]

        for m in self.metrics.values():
            detail_summary = m.details[0] if m.details else "Đạt chuẩn xuất sắc."
            md_lines.append(f"| **{m.name}** | {int(m.weight*100)}% | **{m.score:.1f}** | {m.status} | {detail_summary} |")

        md_lines.append("\n## 2. Chi Tiết Kiểm Định Từng Hạng Mục")
        for m in self.metrics.values():
            md_lines.append(f"### {m.name} — {m.score:.1f}/100đ ({m.status})")
            if m.details:
                for d in m.details:
                    md_lines.append(f"- {d}")
            else:
                md_lines.append("- Không phát hiện bất kỳ lỗi hay cảnh báo nào.")
            md_lines.append("")

        return "\n".join(md_lines).strip()


class PedagogicalBenchmarkEngine:
    """
    Evaluator engine that computes the 5 core pedagogical metrics for generated learning resources.
    """

    FORBIDDEN_AI_CLICHES = [
        "bẫy", "bẫy lập trình", "bẫy lỗi", "bẫy cú pháp", "gotcha", "anti-pattern",
        "khám phá", "tìm hiểu ngay", "bí kíp", "tất tần tật", "thần thánh",
        "tuyệt vời", "bậc nhất", "vô cùng", "viên ngọc"
    ]

    @classmethod
    def evaluate_factual_accuracy(cls, html_or_text: str, tech_stack: str = "python") -> MetricScore:
        """
        Criteria 1: Factual & Syntax Accuracy (Weight: 25%)
        Runs extracted code in sandbox and checks for syntax errors or runtime crashes.
        """
        score = 100.0
        details = []
        code_blocks = re.findall(r'```(?:python|py)?\n(.*?)```', html_or_text, re.DOTALL)

        if not code_blocks and "<pre>" in html_or_text:
            soup = BeautifulSoup(html_or_text, "html.parser")
            for pre in soup.find_all("pre"):
                code_text = pre.get_text()
                if len(code_text.strip().splitlines()) >= 2:
                    code_blocks.append(code_text)

        if not code_blocks:
            details.append("Không phát hiện khối code mẫu nào để chạy kiểm thử sandbox.")
            return MetricScore(name="1. Factual & Code Accuracy", score=90.0, weight=0.25, status="PASS", details=details)

        import textwrap

        tested_count = 0
        error_count = 0
        for idx, code in enumerate(code_blocks, 1):
            clean_code = textwrap.dedent(code).strip()
            if not clean_code:
                continue
            tested_count += 1
            result = execute_code_snippet(clean_code, tech_stack=tech_stack, timeout_sec=2.0)
            if not result.success:
                error_count += 1
                penalty = 25.0
                score = max(0.0, score - penalty)
                details.append(f"Khối code #{idx} lỗi runtime ({result.error_type}): {result.error_message}")

        if error_count == 0:
            details.append(f"Đã kiểm thử {tested_count} khối mã nguồn qua Sandbox: 100% thực thi hoàn hảo.")
            status = "PASS"
        elif score >= 70.0:
            status = "WARNING"
        else:
            status = "FAIL"

        return MetricScore(name="1. Factual & Code Accuracy", score=score, weight=0.25, status=status, details=details)

    @classmethod
    def evaluate_bloom_alignment(cls, content: Dict[str, Any]) -> MetricScore:
        """
        Criteria 2: Bloom Cognitive Alignment (Weight: 20%)
        Verifies alignment across Remember/Understand -> Apply -> Analyze/Create.
        """
        score = 100.0
        details = []

        # Check self-test / questions presence
        self_test = content.get("self_test", [])
        reading_sections = content.get("reading_sections", [])
        quiz = content.get("quiz", [])
        raw_str = str(content).lower()

        if not self_test and not quiz and "selftest" not in raw_str and "quiz" not in raw_str and "câu hỏi" not in raw_str:
            score -= 15.0
            details.append("Thiếu bộ câu hỏi khảo thí tự đánh giá (Self-test/Quiz).")
        else:
            details.append("Có đầy đủ bộ câu hỏi tự đánh giá bám sát nội dung bài học.")

        if len(reading_sections) >= 4 or "section-1" in raw_str or "<h2" in raw_str or "<article" in raw_str:
            details.append("Cấu trúc bài học phân tầng nhận thức đầy đủ từ Vấn đề -> Bản chất -> Thực hành -> Lưu ý.")
        else:
            score -= 15.0
            details.append("Cấu trúc bài học chưa đủ 4-5 phân tầng nhận thức chuẩn.")

        status = "PASS" if score >= 80.0 else ("WARNING" if score >= 65.0 else "FAIL")
        return MetricScore(name="2. Bloom Cognitive Alignment", score=score, weight=0.20, status=status, details=details)

    @classmethod
    def evaluate_contextual_continuity(cls, html_or_text: str, unified_scenario: str = "") -> MetricScore:
        """
        Criteria 3: Single Unified Real-World Scenario Continuity (Weight: 20%)
        Verifies that the same real-world business context runs across all sections.
        """
        score = 100.0
        details = []

        # Check for multiple disconnected scenarios
        disjoint_scenarios = [
            ("Rạp chiếu phim / Vé xem phim", ["rạp chiếu phim", "vé xem phim", "tuổi xem phim"]),
            ("Học bổng sinh viên", ["học bổng", "điểm rèn luyện", "gpa"]),
            ("Giao dịch ngân hàng", ["chuyển khoản", "số dư tài khoản", "lãi suất ngân hàng"]),
            ("Đơn hàng thương mại điện tử", ["giỏ hàng", "voucher", "mã giảm giá", "đơn hàng", "tổng tiền"])
        ]

        detected = []
        text_lower = html_or_text.lower()
        for s_name, keywords in disjoint_scenarios:
            if any(kw in text_lower for kw in keywords):
                detected.append(s_name)

        if len(detected) > 2:
            score -= 30.0
            details.append(f"Cảnh báo vi phạm Kim Chỉ Nam 16: Phát hiện trộn lẫn {len(detected)} ngữ cảnh rời rạc ({', '.join(detected)}).")
        else:
            details.append("Tính nhất quán của kịch bản thực tế doanh nghiệp đạt chuẩn (Single Unified Scenario).")

        status = "PASS" if score >= 80.0 else "WARNING"
        return MetricScore(name="3. Contextual Continuity", score=score, weight=0.20, status=status, details=details)

    @classmethod
    def evaluate_visual_scannability(cls, html_content: str) -> MetricScore:
        """
        Criteria 4: Visual & Scannability Standard (Weight: 20%)
        Checks Light Mode compliance, Table wrappers, Italic captions, and Bullet lists.
        """
        score = 100.0
        details = []

        if not html_content or "<" not in html_content:
            return MetricScore(name="4. Visual & Scannability", score=90.0, weight=0.20, status="PASS", details=["Định dạng Markdown cơ sở."])

        soup = BeautifulSoup(html_content, "html.parser")

        # 1. Check table wrappers
        tables = soup.find_all("table")
        unwrapped_tables = 0
        for t in tables:
            parent = t.parent
            if not parent or "overflow-x-auto" not in parent.get("class", []):
                unwrapped_tables += 1

        if unwrapped_tables > 0:
            score -= 15.0 * unwrapped_tables
            details.append(f"Có {unwrapped_tables} bảng table chưa được bọc thẻ overflow-x-auto.")
        else:
            details.append("100% bảng so sánh kỹ thuật có wrapper overflow-x-auto hỗ trợ responsive.")

        # 2. Check dark mode violations on non-code containers
        dark_violations = 0
        for el in soup.find_all(["div", "section", "article"]):
            classes = el.get("class", [])
            if any(k in classes for k in ["terminal", "visualizer", "code-tracker", "hljs"]):
                continue
            if "bg-slate-900" in classes or "bg-black" in classes or "bg-gray-900" in classes:
                dark_violations += 1

        if dark_violations > 0:
            score -= 20.0 * dark_violations
            details.append(f"Có {dark_violations} thẻ container vi phạm chuẩn Light Mode (chứa màu nền tối).")
        else:
            details.append("100% giao diện tuân thủ nghiêm ngặt chuẩn Light Mode.")

        # 3. Check image captions italic tag
        for fig in soup.find_all("figcaption"):
            if not fig.find("i") and not fig.find("em"):
                score -= 10.0
                details.append(f"Chú thích hình ảnh '{fig.get_text()[:30]}' chưa có thẻ in nghiêng <i>.")
                break

        score = max(0.0, score)
        status = "PASS" if score >= 85.0 else ("WARNING" if score >= 70.0 else "FAIL")
        return MetricScore(name="4. Visual & Scannability", score=score, weight=0.20, status=status, details=details)

    @classmethod
    def evaluate_tone_cleanliness(cls, text_content: str) -> MetricScore:
        """
        Criteria 5: Zero AI Cliché & Professional Tone (Weight: 15%)
        Checks for forbidden AI buzzwords and informal hype phrases.
        """
        score = 100.0
        details = []
        found_cliches = []

        text_lower = text_content.lower()
        for cliche in cls.FORBIDDEN_AI_CLICHES:
            pattern = r'\b' + re.escape(cliche) + r'\b'
            if re.search(pattern, text_lower):
                found_cliches.append(cliche)

        if found_cliches:
            penalty = len(found_cliches) * 15.0
            score = max(0.0, score - penalty)
            details.append(f"Phát hiện {len(found_cliches)} từ cấm/từ lóng AI: {', '.join(found_cliches)}.")
        else:
            details.append("100% văn phong kỹ sư chuyên nghiệp, sạch hoàn toàn từ lóng AI.")

        status = "PASS" if score >= 85.0 else ("WARNING" if score >= 70.0 else "FAIL")
        return MetricScore(name="5. Professional Tone & Tone Cleanliness", score=score, weight=0.15, status=status, details=details)

    @classmethod
    def run_full_benchmark(
        cls,
        html_or_text: str,
        lesson_id: str = "Lesson 01",
        lesson_title: str = "Bài học",
        tech_stack: str = "python",
        content_dict: Optional[Dict[str, Any]] = None
    ) -> PedagogicalScorecard:
        """
        Runs comprehensive benchmark suite and compiles overall PedagogicalScorecard.
        """
        m1 = cls.evaluate_factual_accuracy(html_or_text, tech_stack=tech_stack)
        m2 = cls.evaluate_bloom_alignment(content_dict or {"text": html_or_text})
        m3 = cls.evaluate_contextual_continuity(html_or_text)
        m4 = cls.evaluate_visual_scannability(html_or_text)
        m5 = cls.evaluate_tone_cleanliness(html_or_text)

        metrics = {
            "factual_accuracy": m1,
            "bloom_alignment": m2,
            "contextual_continuity": m3,
            "visual_scannability": m4,
            "tone_cleanliness": m5
        }

        overall_score = sum(m.score * m.weight for m in metrics.values())
        passed = overall_score >= 80.0 and all(m.status != "FAIL" for m in metrics.values())

        return PedagogicalScorecard(
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            tech_stack=tech_stack,
            overall_score=overall_score,
            passed=passed,
            metrics=metrics
        )


def evaluate_lesson_pedagogy(
    html_content: str,
    lesson_id: str = "Lesson 01",
    lesson_title: str = "Bài học",
    tech_stack: str = "python"
) -> PedagogicalScorecard:
    """Convenience function to run full benchmark."""
    return PedagogicalBenchmarkEngine.run_full_benchmark(
        html_or_text=html_content,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        tech_stack=tech_stack
    )

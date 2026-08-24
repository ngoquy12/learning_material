"""
tests/test_pedagogy_trend.py — Theo dõi xu hướng chất lượng sư phạm (G3).

PedagogicalBenchmarkEngine đã chấm được điểm một bài học, nhưng điểm đó chỉ tồn tại
trong một lần chạy rồi biến mất. Hệ quả: không trả lời được câu hỏi quan trọng nhất
với một hệ thống sinh nội dung bằng LLM — "bản refactor hôm nay có làm học liệu tệ
đi so với tuần trước không?".

Một điểm 82/100 tự nó chẳng nói lên gì. 82 sau khi tuần trước là 91 là một sự cố;
82 sau khi tuần trước là 74 là một tiến bộ.
"""

import pytest

from core import paths
from core.evals import trend_store


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
    paths.reset_path_cache()
    yield
    paths.reset_path_cache()


def _card(score: float, passed: bool = True) -> dict:
    return {
        "overall_score": score,
        "passed": passed,
        "tech_stack": "Python 3.12",
        "metrics": {"bloom": {"score": score, "status": "PASS"}},
    }


class TestRecording:
    def test_ghi_va_doc_lai_duoc(self, store):
        trend_store.record_scorecard(_card(88.5), subject="bai_A", commit_sha="abc123")
        history = trend_store.get_history("bai_A")

        assert len(history) == 1
        assert history[0].overall_score == 88.5
        assert history[0].commit_sha == "abc123"

    def test_lich_su_moi_nhat_truoc(self, store):
        for score in (70.0, 80.0, 90.0):
            trend_store.record_scorecard(_card(score), subject="bai_A", commit_sha=str(score))

        scores = [p.overall_score for p in trend_store.get_history("bai_A")]
        assert scores == [90.0, 80.0, 70.0]

    def test_nhan_ca_doi_tuong_scorecard_that(self, store):
        from core.evals.benchmark import evaluate_lesson_pedagogy

        card = evaluate_lesson_pedagogy(
            html_content="<section id='section-1'><h2>Đặt vấn đề</h2><p>Nội dung.</p></section>",
            lesson_id="L1",
            tech_stack="python",
        )
        point = trend_store.record_scorecard(card, subject="bai_that")
        assert point.overall_score == pytest.approx(card.overall_score)

    def test_cac_doi_tuong_doc_lap_voi_nhau(self, store):
        trend_store.record_scorecard(_card(90.0), subject="bai_A")
        trend_store.record_scorecard(_card(50.0), subject="bai_B")

        assert trend_store.get_history("bai_A")[0].overall_score == 90.0
        assert trend_store.get_history("bai_B")[0].overall_score == 50.0


class TestRegressionDetection:
    def test_phat_hien_tut_diem(self, store):
        trend_store.record_scorecard(_card(93.0), subject="bai_A", commit_sha="cu")
        trend_store.record_scorecard(_card(71.0, passed=False), subject="bai_A", commit_sha="moi")

        regressions = trend_store.detect_regressions(["bai_A"])

        assert len(regressions) == 1
        assert regressions[0].delta == pytest.approx(-22.0)
        assert "tụt 22.0 điểm" in regressions[0].message()

    def test_dao_dong_nho_khong_bao_dong(self, store):
        """
        Bộ chấm có tiêu chí dựa trên heuristic văn bản, dao động vài điểm là bình
        thường. Báo động vì nhiễu sẽ khiến người ta bỏ qua cả những lần tụt thật.
        """
        trend_store.record_scorecard(_card(90.0), subject="bai_A")
        trend_store.record_scorecard(_card(87.0), subject="bai_A")

        assert trend_store.detect_regressions(["bai_A"]) == []

    def test_tang_diem_khong_bi_bao_la_tut(self, store):
        trend_store.record_scorecard(_card(70.0), subject="bai_A")
        trend_store.record_scorecard(_card(95.0), subject="bai_A")
        assert trend_store.detect_regressions(["bai_A"]) == []

    def test_chi_moi_co_mot_moc_thi_chua_so_duoc(self, store):
        trend_store.record_scorecard(_card(50.0), subject="bai_A")
        assert trend_store.detect_regressions(["bai_A"]) == []

    def test_so_voi_lan_LIEN_TRUOC_khong_phai_diem_cao_nhat(self, store):
        """
        Mục tiêu là phát hiện thay đổi VỪA gây hại, không phải kể lể một lần tụt đã
        biết và đã chấp nhận từ trước.
        """
        trend_store.record_scorecard(_card(95.0), subject="bai_A")  # đỉnh cũ
        trend_store.record_scorecard(_card(75.0), subject="bai_A")  # đã tụt, đã biết
        trend_store.record_scorecard(_card(76.0), subject="bai_A")  # nhích lên chút

        assert trend_store.detect_regressions(["bai_A"]) == [], (
            "Không được báo lại một lần tụt đã xảy ra ở mốc trước"
        )

    def test_nguong_tuy_chinh_duoc(self, store):
        trend_store.record_scorecard(_card(90.0), subject="bai_A")
        trend_store.record_scorecard(_card(87.0), subject="bai_A")

        assert trend_store.detect_regressions(["bai_A"], threshold=2.0)
        assert not trend_store.detect_regressions(["bai_A"], threshold=10.0)

    def test_quet_moi_doi_tuong_khi_khong_chi_dinh(self, store):
        trend_store.record_scorecard(_card(90.0), subject="bai_A")
        trend_store.record_scorecard(_card(60.0), subject="bai_A")
        trend_store.record_scorecard(_card(90.0), subject="bai_B")
        trend_store.record_scorecard(_card(89.0), subject="bai_B")

        subjects = {r.subject for r in trend_store.detect_regressions()}
        assert subjects == {"bai_A"}


class TestReport:
    def test_bao_cao_hien_duong_di_cua_diem(self, store):
        for score in (70.0, 80.0, 90.0):
            trend_store.record_scorecard(_card(score), subject="bai_A")

        report = trend_store.format_trend_report(["bai_A"])
        assert "90 <- 80 <- 70" in report

    def test_bao_cao_neu_ro_tut_diem(self, store):
        trend_store.record_scorecard(_card(93.0), subject="bai_A")
        trend_store.record_scorecard(_card(71.0, passed=False), subject="bai_A")

        report = trend_store.format_trend_report(["bai_A"])
        assert "TỤT ĐIỂM" in report
        assert "CHƯA ĐẠT" in report

    def test_khong_co_du_lieu_thi_noi_ro(self, store):
        assert "chưa có dữ liệu" in trend_store.format_trend_report(["bai_moi"])


class TestEvalScript:
    def test_cham_tren_ban_golden(self, store, tmp_path, monkeypatch):
        """
        Chấm trên bản golden đã commit chứ không phải nội dung sinh mới mỗi lần:
        nếu chấm trên nội dung mới, không phân biệt được "code tệ đi" với "LLM hôm
        nay trả lời kém may".
        """
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "scripts/run_pedagogical_eval.py", "--no-record"],
            cwd=str(paths.BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
            check=False,
        )

        assert result.returncode == 0, result.stderr
        assert "reading_python_full" in result.stdout
        assert "reading_sql_minimal" in result.stdout

    def test_script_dung_dung_bo_golden(self):
        from pathlib import Path

        source = Path("scripts/run_pedagogical_eval.py").read_text(encoding="utf-8")
        assert 'tests" / "golden"' in source
        assert 'fixture.get("renderer") != "reading"' in source, (
            "Phải bỏ qua bài thực hành: bộ chấm này dành cho bài đọc"
        )


class TestNightlyWorkflow:
    def test_workflow_hop_le_va_giu_lai_kho_xu_huong(self):
        from pathlib import Path

        import yaml

        wf = yaml.safe_load(Path(".github/workflows/nightly-evals.yml").read_text(encoding="utf-8"))
        job = wf["jobs"]["pedagogy-trend"]
        steps = job["steps"]

        assert any("cache" in str(s.get("uses", "")) for s in steps), (
            "Kho xu hướng phải sống qua các lần chạy, nếu không mỗi đêm lại là mốc "
            "đầu tiên và không bao giờ so sánh được với gì"
        )
        assert any("--check" in str(s.get("run", "")) for s in steps)
        assert any("STORAGE_DIR" in str(s.get("env", {})) for s in steps), (
            "Phải trỏ STORAGE_DIR vào thư mục cache, không để rơi vào cây mã nguồn"
        )

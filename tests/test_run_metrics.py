"""
tests/test_run_metrics.py — Sổ đo chi phí lượt chạy (D3).

Hệ thống đã ghi trace từng lượt gọi LLM ra JSONL và đã đếm cache theo agent, nhưng
không nơi nào trả lời được câu hỏi người vận hành thực sự hỏi sau mỗi lần chạy:
"buổi này tốn bao nhiêu token, cache đỡ được mấy phần, tiền đi vào khâu nào".

Trace JSONL trả lời được nhưng phải tự cộng hàng nghìn dòng; còn get_cache_stats()
thì cộng dồn của MỌI lượt chạy trong 30 ngày qua, không phải lượt vừa rồi.
"""

import threading

import pytest

from core import run_metrics


@pytest.fixture
def metrics():
    """Sổ đo sạch cho mỗi test — nó là singleton cấp tiến trình."""
    run_metrics.start_run("test")
    yield run_metrics
    run_metrics.start_run("")


class TestAccumulation:
    def test_cong_don_token_theo_agent(self, metrics):
        metrics.record_llm_call("Reading Creator", {"prompt_tokens": 100, "completion_tokens": 40, "total_tokens": 140}, 1.5)
        metrics.record_llm_call("Reading Creator", {"prompt_tokens": 60, "completion_tokens": 20, "total_tokens": 80}, 0.5)
        metrics.record_llm_call("Quiz Creator", {"prompt_tokens": 30, "completion_tokens": 10, "total_tokens": 40}, 0.2)

        snap = metrics.get_run_metrics().snapshot()

        assert snap["llm_calls"] == 3
        assert snap["total_tokens"] == 260
        assert snap["prompt_tokens"] == 190
        assert snap["completion_tokens"] == 70

    def test_xep_hang_theo_token_giam_dan(self, metrics):
        """Câu hỏi thực dụng là "tiền đi vào đâu", nên agent tốn nhất phải đứng đầu."""
        metrics.record_llm_call("Nho", {"total_tokens": 10})
        metrics.record_llm_call("To", {"total_tokens": 900})
        metrics.record_llm_call("Vua", {"total_tokens": 200})

        names = [r["agent_name"] for r in metrics.get_run_metrics().snapshot()["by_agent"]]
        assert names == ["To", "Vua", "Nho"]

    def test_thieu_so_lieu_token_khong_lam_hong_so_do(self, metrics):
        """Đường fallback trong llm.py truyền token rỗng — vẫn phải đếm được lượt gọi."""
        metrics.record_llm_call("Agent", None)
        metrics.record_llm_call("Agent", {})

        snap = metrics.get_run_metrics().snapshot()
        assert snap["llm_calls"] == 2
        assert snap["total_tokens"] == 0


class TestCacheHitRate:
    def test_ty_le_cache_tinh_tren_luot_chay_nay(self, metrics):
        for _ in range(3):
            metrics.record_llm_call("A", {"total_tokens": 100})
        for _ in range(7):
            metrics.record_cache_hit("A")

        snap = metrics.get_run_metrics().snapshot()
        assert snap["llm_calls"] == 3
        assert snap["cache_hits"] == 7
        assert snap["cache_hit_rate"] == pytest.approx(0.7)

    def test_cache_hit_khong_cong_them_token(self, metrics):
        """Lượt được cache phục vụ là lượt KHÔNG tốn tiền — cộng token vào là báo cáo sai."""
        metrics.record_cache_hit("A")
        metrics.record_cache_hit("A")

        snap = metrics.get_run_metrics().snapshot()
        assert snap["total_tokens"] == 0
        assert snap["cache_hits"] == 2

    def test_khong_chia_cho_khong_khi_chua_co_gi(self, metrics):
        assert metrics.get_run_metrics().snapshot()["cache_hit_rate"] == 0.0


class TestThreadSafety:
    def test_nam_nhanh_song_song_khong_mat_so_lieu(self, metrics):
        """5 nhánh sản xuất chạy song song và cùng ghi vào sổ đo này."""

        def worker(idx):
            for _ in range(50):
                metrics.record_llm_call(f"Agent{idx}", {"total_tokens": 10})
                metrics.record_cache_hit(f"Agent{idx}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        snap = metrics.get_run_metrics().snapshot()
        assert snap["llm_calls"] == 250
        assert snap["cache_hits"] == 250
        assert snap["total_tokens"] == 2500


class TestNeverBreaksTheRun:
    """Đo đạc hỏng không đáng để mất cả buổi sinh học liệu."""

    def test_ham_module_nuot_loi(self, monkeypatch):
        class Boom:
            def record_llm_call(self, *a, **k):
                raise RuntimeError("sổ đo hỏng")

            def record_cache_hit(self, *a, **k):
                raise RuntimeError("sổ đo hỏng")

            def start_run(self, *a, **k):
                raise RuntimeError("sổ đo hỏng")

        monkeypatch.setattr(run_metrics, "_RUN_METRICS", Boom())
        run_metrics.start_run("x")
        run_metrics.record_llm_call("A", {"total_tokens": 1})
        run_metrics.record_cache_hit("A")

    def test_bao_cao_rong_khi_chua_co_so_lieu(self, metrics):
        assert run_metrics.format_run_report() == ""

    def test_khong_ghi_db_khi_chua_co_so_lieu(self, metrics):
        assert run_metrics.persist_run_metrics() is False


class TestReport:
    def test_bao_cao_neu_du_con_so_can_thiet(self, metrics):
        metrics.record_llm_call("Reading Creator", {"prompt_tokens": 1000, "completion_tokens": 500, "total_tokens": 1500}, 3.2)
        metrics.record_cache_hit("Quiz Creator")

        report = run_metrics.format_run_report()

        assert "Reading Creator" in report
        assert "1,500" in report, "Token phải có dấu phân cách nghìn để đọc được"
        assert "50.0%" in report, "Phải nêu tỷ lệ cache của chính lượt chạy này"

    def test_bao_cao_cat_bot_khi_qua_nhieu_agent(self, metrics):
        for i in range(20):
            metrics.record_llm_call(f"Agent{i:02d}", {"total_tokens": i * 10})

        report = run_metrics.format_run_report(top_n=5)
        assert "và 15 agent khác" in report


class TestPersistence:
    def test_ghi_va_doc_lai_duoc_tu_kho_tri_thuc(self, tmp_path, monkeypatch, metrics):
        monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
        from core import paths

        paths.reset_path_cache()
        try:
            metrics.record_llm_call("Reading Creator", {"total_tokens": 4242}, 1.0)
            assert run_metrics.persist_run_metrics() is True

            import sqlite3

            conn = sqlite3.connect(str(paths.get_knowledge_db_path()))
            row = conn.execute(
                "SELECT label, llm_calls, total_tokens FROM run_cost_metrics"
            ).fetchone()
            conn.close()

            assert row == ("test", 1, 4242)
        finally:
            paths.reset_path_cache()


class TestWiring:
    """Sổ đo phải được nối vào chỗ thắt cổ chai, không rải rác từng agent."""

    def test_moi_luot_goi_llm_that_deu_di_qua_log_agent_call(self):
        from pathlib import Path

        source = Path("core/observability.py").read_text(encoding="utf-8")
        assert "record_llm_call" in source, (
            "log_agent_call là chỗ mọi lượt gọi LLM thật đi qua — phải cộng dồn tại đây"
        )

    def test_ca_hai_duong_cache_hit_deu_duoc_dem(self):
        from pathlib import Path

        source = Path("core/semantic_cache.py").read_text(encoding="utf-8")
        assert source.count("_record_cache_hit(agent_name)") == 2, (
            "Phải đếm cả EXACT HIT lẫn FUZZY HIT, thiếu một đường là tỷ lệ cache sai"
        )

    def test_cli_in_bao_cao_cuoi_luot_chay(self):
        from pathlib import Path

        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert "start_run(" in source
        assert "print_run_cost_report()" in source

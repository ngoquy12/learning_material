"""
tests/test_learning_analytics.py — Vòng phản hồi từ người học (F2).

Trước module này, vòng phản hồi của hệ thống chỉ có MỘT chiều và chỉ nghe được
chính nó: LLM sinh → reviewer chấm → lessons_learned → LLM sinh lần sau.

Reviewer là một mô hình ngôn ngữ đọc học liệu, nên nó chỉ thấy được lỗi hiện trên
trang giấy. Có một loại vấn đề nó KHÔNG BAO GIỜ thấy, vì chỉ người học mới biết:
bài viết đúng hết nhưng 70% bỏ giữa chừng; một câu quiz cả lớp cùng sai; một bài
thiết kế cho 10 phút nhưng thực tế mất 40 phút.
"""

import json

import pytest

from core import paths
from core.learning_analytics import (
    MIN_COHORT_SIZE,
    aggregate_statements,
    derive_signals,
    format_analytics_report,
    ingest_xapi_export,
    load_statements,
)

LESSON = "http://x.vn/xapi/C/Session_05/Lesson_03"
QUESTION = LESSON + "/q/3"


def _stmt(learner, verb, obj_id=LESSON, name="Đệ quy", result=None, obj_type="lesson"):
    s = {
        "actor": {"objectType": "Agent", "mbox": f"mailto:{learner}@x.vn"},
        "verb": {"id": f"http://adlnet.gov/expapi/verbs/{verb}"},
        "object": {
            "objectType": "Activity",
            "id": obj_id,
            "definition": {
                "name": {"vi-VN": name},
                "type": f"http://adlnet.gov/expapi/activities/{obj_type}",
            },
        },
    }
    if result:
        s["result"] = result
    return s


def _cohort(n=20, completed=6, duration_s=600):
    """n người học mở bài, `completed` người hoàn thành."""
    out = []
    for i in range(n):
        learner = f"sv{i:02d}"
        out.append(_stmt(learner, "initialized"))
        if i < completed:
            out.append(_stmt(learner, "completed", result={"completion": True,
                                                           "duration": f"PT{duration_s}S"}))
        else:
            out.append(_stmt(learner, "terminated", result={"duration": f"PT{duration_s}S"}))
    return out


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
    paths.reset_path_cache()
    yield tmp_path
    paths.reset_path_cache()


class TestAggregation:
    def test_dem_dung_so_nguoi_hoc_khong_dem_so_phat_bieu(self):
        """Một người học mở lại bài 5 lần vẫn là MỘT người, không phải 5."""
        statements = [_stmt("sv01", "initialized") for _ in range(5)]
        stats = aggregate_statements(statements)

        assert stats[LESSON].cohort_size == 1
        assert stats[LESSON].initialized == 5

    def test_tach_rieng_tung_hoat_dong(self):
        stats = aggregate_statements(
            [_stmt("sv01", "initialized"), _stmt("sv01", "answered", QUESTION, obj_type="question")]
        )
        assert set(stats) == {LESSON, QUESTION}

    def test_tinh_ty_le_bo_giua_chung(self):
        stats = aggregate_statements(_cohort(n=20, completed=6))
        assert stats[LESSON].abandonment_rate == pytest.approx(0.7)

    def test_tinh_ty_le_tra_loi_sai(self):
        statements = [
            _stmt(f"sv{i:02d}", "answered", QUESTION, result={"success": i < 5}, obj_type="question")
            for i in range(20)
        ]
        stats = aggregate_statements(statements)
        assert stats[QUESTION].error_rate == pytest.approx(0.75)

    def test_trung_vi_thoi_luong(self):
        stats = aggregate_statements(_cohort(n=20, completed=20, duration_s=600))
        assert stats[LESSON].median_duration == pytest.approx(600.0)

    def test_phat_bieu_hong_khong_lam_chet_bo_gom(self):
        stats = aggregate_statements(
            [None, "chuoi", {}, {"object": {}}, _stmt("sv01", "initialized")]
        )
        assert stats[LESSON].initialized == 1

    def test_chi_doc_thoi_luong_dang_minh_phat_ra(self):
        """
        Cố ý không cài bộ đọc ISO-8601 đầy đủ: đoán sai đơn vị thời gian sẽ tạo ra
        tín hiệu "quá giờ" hoàn toàn bịa.
        """
        stats = aggregate_statements(
            [_stmt("sv01", "completed", result={"duration": "P1DT2H30M"})]
        )
        assert stats[LESSON].median_duration is None


class TestCohortGuard:
    """Nhóm bảo vệ quan trọng nhất: không biến nhiễu thống kê thành quy định."""

    def test_khong_sinh_luat_tu_co_mau_qua_nho(self):
        """
        Một luật sinh ra từ vài người học sẽ ràng buộc MỌI bài sinh về sau. Sai ở
        đây tệ hơn hẳn việc không có luật nào.
        """
        stats = aggregate_statements(_cohort(n=3, completed=0))
        assert derive_signals(stats) == []

    def test_du_co_mau_thi_sinh_luat(self):
        stats = aggregate_statements(_cohort(n=MIN_COHORT_SIZE, completed=0))
        assert derive_signals(stats)

    def test_nguong_co_mau_dieu_chinh_duoc_cho_thu_nghiem(self):
        stats = aggregate_statements(_cohort(n=3, completed=0))
        assert derive_signals(stats, min_cohort=2)


class TestSignals:
    def test_bat_duoc_bai_bi_bo_giua_chung(self):
        stats = aggregate_statements(_cohort(n=20, completed=6))
        signals = derive_signals(stats)

        abandonment = [s for s in signals if s.kind == "abandonment"]
        assert len(abandonment) == 1
        assert abandonment[0].value == pytest.approx(0.7)
        assert abandonment[0].severity == "CRITICAL"

    def test_bai_binh_thuong_khong_bi_bao(self):
        """18/20 hoàn thành trong đúng thời lượng thiết kế là bài tốt."""
        stats = aggregate_statements(_cohort(n=20, completed=18, duration_s=560))
        assert derive_signals(stats) == []

    def test_bat_duoc_cau_hoi_ca_lop_cung_sai(self):
        statements = [
            _stmt(f"sv{i:02d}", "answered", QUESTION, "Câu hỏi khó",
                  result={"success": i < 4}, obj_type="question")
            for i in range(20)
        ]
        signals = derive_signals(aggregate_statements(statements))

        hard = [s for s in signals if s.kind == "hard_question"]
        assert len(hard) == 1
        assert "80%" in hard[0].rule_text

    def test_bat_duoc_bai_vuot_thoi_luong_thiet_ke(self):
        stats = aggregate_statements(_cohort(n=20, completed=20, duration_s=1800))
        signals = derive_signals(stats, expected_minutes=10.0)

        overrun = [s for s in signals if s.kind == "duration_overrun"]
        assert len(overrun) == 1
        assert overrun[0].value == pytest.approx(3.0)

    def test_luat_sinh_ra_phai_HANH_DONG_DUOC(self):
        """
        Một luật chỉ mô tả hiện tượng ("bài này bị bỏ nhiều") thì lần sinh sau không
        biết phải làm gì khác đi. Luật phải nói rõ hành động cụ thể.
        """
        stats = aggregate_statements(_cohort(n=20, completed=4))
        signal = next(s for s in derive_signals(stats) if s.kind == "abandonment")

        assert "hãy" in signal.rule_text.lower()
        assert any(kw in signal.rule_text for kw in ("rút ngắn", "chia nhỏ", "sớm hơn"))


class TestLoadStatements:
    def test_doc_duoc_mang_json(self, tmp_path):
        f = tmp_path / "a.json"
        f.write_text(json.dumps([_stmt("sv01", "initialized")]), encoding="utf-8")
        assert len(load_statements(str(f))) == 1

    def test_doc_duoc_object_boc_statements(self, tmp_path):
        """Nhiều LRS xuất ra dạng {"statements": [...], "more": "..."}."""
        f = tmp_path / "a.json"
        f.write_text(json.dumps({"statements": [_stmt("sv01", "initialized")], "more": ""}),
                     encoding="utf-8")
        assert len(load_statements(str(f))) == 1

    def test_doc_duoc_jsonl(self, tmp_path):
        f = tmp_path / "a.jsonl"
        f.write_text("\n".join(json.dumps(_stmt(f"sv{i}", "initialized")) for i in range(3)),
                     encoding="utf-8")
        assert len(load_statements(str(f))) == 3

    def test_dong_hong_trong_jsonl_bi_bo_qua(self, tmp_path):
        f = tmp_path / "a.jsonl"
        f.write_text(json.dumps(_stmt("sv01", "initialized")) + "\n{hong\n", encoding="utf-8")
        assert len(load_statements(str(f))) == 1

    def test_file_rong(self, tmp_path):
        f = tmp_path / "a.json"
        f.write_text("", encoding="utf-8")
        assert load_statements(str(f)) == []

    def test_file_khong_ton_tai_bao_loi_ro_rang(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="xAPI"):
            load_statements(str(tmp_path / "khong_co.json"))


class TestReport:
    def test_noi_ro_phan_chua_du_co_mau(self):
        """
        Im lặng bỏ qua khiến người đọc tưởng những bài đó không có vấn đề gì.
        """
        stats = aggregate_statements(_cohort(n=3, completed=0))
        report = format_analytics_report(stats, [])

        assert "Chưa đủ cỡ mẫu" in report

    def test_khong_co_du_lieu_thi_noi_ro(self):
        assert "Không có phát biểu" in format_analytics_report({}, [])


class TestFullLoop:
    def test_vong_khep_kin_tu_hanh_vi_den_prompt_lan_sau(self, store, tmp_path):
        """
        Test quan trọng nhất của F2: hành vi người học phải đi được hết vòng và
        quay lại prompt của lần sinh sau. Đứt ở bất kỳ mắt xích nào thì toàn bộ
        tính năng chỉ là một báo cáo đẹp mà không ai dùng.
        """
        statements = _cohort(n=20, completed=4)
        source = tmp_path / "xapi.json"
        source.write_text(json.dumps(statements), encoding="utf-8")

        result = ingest_xapi_export(str(source), tech_stack="Python 3.12")

        assert result["stored_rules"] >= 1

        from agents.knowledge_memory_agent import get_relevant_memories_for_creator

        context = get_relevant_memories_for_creator(
            tech_stack="Python 3.12", scope="all", query="Đệ quy", limit=5
        )
        assert "bỏ giữa chừng" in context, (
            "Tín hiệu từ người học không tới được prompt của lần sinh sau — vòng đứt"
        )

    def test_dry_run_khong_ghi_gi(self, store, tmp_path):
        """
        Luật trong kho kinh nghiệm ảnh hưởng tới MỌI lần sinh về sau, nên xem trước
        là bước đáng có.
        """
        source = tmp_path / "xapi.json"
        source.write_text(json.dumps(_cohort(n=20, completed=4)), encoding="utf-8")

        result = ingest_xapi_export(str(source), dry_run=True)

        assert result["signals"], "Vẫn phải rút ra tín hiệu để xem trước"
        assert result["stored_rules"] == 0

    def test_nap_lai_cung_du_lieu_khong_nhan_doi_luat(self, store, tmp_path):
        source = tmp_path / "xapi.json"
        source.write_text(json.dumps(_cohort(n=20, completed=4)), encoding="utf-8")

        first = ingest_xapi_export(str(source))
        second = ingest_xapi_export(str(source))

        assert first["stored_rules"] >= 1
        assert second["stored_rules"] == 0


class TestCliWiring:
    def test_co_dong_lenh_nap_du_lieu(self):
        import sys

        from cli.args import parse_cli_arguments

        argv = sys.argv
        try:
            sys.argv = ["main.py", "--ingest-xapi", "data.json", "--ingest-dry-run"]
            args = parse_cli_arguments()
            assert args.ingest_xapi == "data.json"
            assert args.ingest_dry_run is True
        finally:
            sys.argv = argv

    def test_workflow_goi_bo_nap(self):
        from pathlib import Path

        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert "handle_xapi_ingest(args)" in source

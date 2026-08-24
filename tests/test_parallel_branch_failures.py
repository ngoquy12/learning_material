"""
tests/test_parallel_branch_failures.py — Nhánh sản xuất song song chết phải HIỆN RA (B4),
và các node giai đoạn phải kiểm được độc lập (B3).

Lỗi được sửa: `node_parallel_derived_production` chạy 5 nhánh song song, nhưng khi
một nhánh ném ngoại lệ thì chỉ có một dòng `print` rồi đi tiếp. Hậu quả:

  - Artifact của nhánh đó giữ nguyên trạng thái "Pending" từ lúc khởi tạo, không
    phân biệt được với "chưa chạy tới".
  - Báo cáo cuối in "✅ Tất cả tài nguyên đã hoàn tất" — sai sự thật.
  - Ở nhánh async, `asyncio.gather(return_exceptions=True)` trả về đối tượng
    exception thô, mất luôn thông tin nhánh nào đã chết.

Người vận hành chỉ phát hiện ra khi mở thư mục học liệu và thấy thiếu file.
"""

import asyncio

import pytest

from core import graph
from core.artifact_status import ArtifactStatus, is_failed


def _base_state() -> dict:
    return {
        "session_id": "Session 07",
        "lesson_id": "Lesson 02",
        "technology_stack": "Python 3.12",
        "artifacts_status": {
            "html": ArtifactStatus.PENDING,
            "quiz": ArtifactStatus.PENDING,
            "practical_lab": ArtifactStatus.PENDING,
            "reading_questions": ArtifactStatus.PENDING,
            "video_script": ArtifactStatus.PENDING,
        },
    }


class TestPipelineDeclaration:
    """B4: danh sách nhánh và ánh xạ artifact phải nằm trong MỘT khai báo."""

    def test_moi_nhanh_deu_khai_bao_artifact_key(self):
        for branch in graph.DERIVED_PIPELINES:
            assert branch.artifact_key, f"Nhánh {branch.name} thiếu artifact_key"
            assert callable(branch.run), f"Nhánh {branch.name} không có hàm chạy"

    def test_khong_trung_ten_va_khong_trung_artifact(self):
        names = [b.name for b in graph.DERIVED_PIPELINES]
        keys = [b.artifact_key for b in graph.DERIVED_PIPELINES]
        assert len(set(names)) == len(names), "Trùng tên nhánh"
        assert len(set(keys)) == len(keys), "Hai nhánh cùng ghi vào một artifact"

    def test_artifact_key_khop_voi_trang_thai_khoi_tao(self):
        """Sai khoá thì trạng thái FAILED ghi vào một ô không ai đọc."""
        known = set(_base_state()["artifacts_status"])
        for branch in graph.DERIVED_PIPELINES:
            assert branch.artifact_key in known, (
                f"Nhánh {branch.name} khai báo artifact_key='{branch.artifact_key}' "
                f"không nằm trong tập artifact cấp lesson"
            )


class TestRecordBranchFailures:
    def test_danh_dau_failed_dung_artifact(self):
        state = _base_state()
        graph.record_branch_failures(state, {"Quiz": RuntimeError("LLM trả JSON hỏng")})

        assert is_failed(state["artifacts_status"]["quiz"])
        # Các nhánh khác không được đụng tới.
        assert state["artifacts_status"]["html"] == ArtifactStatus.PENDING

    def test_giu_lai_traceback_trong_review_logs(self):
        """Console cuộn mất sau vài phút chạy; người sửa cần dấu vết ở lại trong state."""
        state = _base_state()
        graph.record_branch_failures(state, {"HTML": ValueError("thiếu tech_stack")})

        logs = state["review_logs"]
        assert len(logs) == 1
        assert "HTML" in logs[0]["source"]
        assert "ValueError" in logs[0]["feedback"]
        assert "thiếu tech_stack" in logs[0]["feedback"]

    def test_nhieu_nhanh_chet_cung_luc(self):
        state = _base_state()
        graph.record_branch_failures(
            state,
            {"Quiz": RuntimeError("a"), "VideoScript": RuntimeError("b")},
        )
        assert is_failed(state["artifacts_status"]["quiz"])
        assert is_failed(state["artifacts_status"]["video_script"])
        assert len(state["review_logs"]) == 2

    def test_ten_nhanh_la_bi_bo_qua_khong_lam_chet_pipeline(self):
        state = _base_state()
        graph.record_branch_failures(state, {"KhongTonTai": RuntimeError("x")})
        assert state["artifacts_status"]["html"] == ArtifactStatus.PENDING
        assert not state.get("review_logs")


class TestParallelNodeEndToEnd:
    """Chạy thật node song song với một nhánh được ép cho chết."""

    @pytest.fixture
    def failing_quiz(self, monkeypatch):
        def _ok(state):
            return state

        def _boom(state):
            raise RuntimeError("Quiz agent hỏng giữa chừng")

        patched = tuple(
            graph.DerivedPipeline(b.name, b.artifact_key, _boom if b.name == "Quiz" else _ok)
            for b in graph.DERIVED_PIPELINES
        )
        monkeypatch.setattr(graph, "DERIVED_PIPELINES", patched)
        monkeypatch.setattr(graph, "save_state_checkpoint", lambda state: None)

    def test_nhanh_chet_duoc_danh_dau_failed(self, failing_quiz):
        result = graph.node_parallel_derived_production(_base_state())

        assert is_failed(result["artifacts_status"]["quiz"]), (
            "Nhánh Quiz đã ném ngoại lệ nhưng trạng thái artifact không phản ánh điều đó"
        )

    def test_cac_nhanh_con_lai_van_hoan_tat(self, failing_quiz):
        """Một nhánh hỏng không được kéo theo bốn nhánh còn lại."""
        result = graph.node_parallel_derived_production(_base_state())

        for key in ("html", "practical_lab", "reading_questions", "video_script"):
            assert not is_failed(result["artifacts_status"][key]), (
                f"Nhánh '{key}' bị đánh dấu hỏng lây dù nó chạy bình thường"
            )

    def test_bao_cao_khong_noi_doi_la_hoan_tat_het(self, failing_quiz, capsys):
        graph.node_parallel_derived_production(_base_state())
        out = capsys.readouterr().out

        assert "Tất cả tài nguyên đã hoàn tất" not in out, (
            "Có nhánh hỏng mà báo cáo vẫn tuyên bố hoàn tất toàn bộ"
        )
        assert "Quiz" in out

    def test_duong_chay_threadpool_cung_ghi_nhan_loi(self, failing_quiz):
        """
        Node chọn ThreadPool khi đã có event loop đang chạy. Hai đường chạy phải
        cho cùng kết quả — trước đây chỉ đường ThreadPool có tên nhánh, còn đường
        async thì mất.
        """

        async def _drive():
            return graph.node_parallel_derived_production(_base_state())

        result = asyncio.run(_drive())
        assert is_failed(result["artifacts_status"]["quiz"])


class TestGraphStructure:
    """B3: node ở module level và đồ thị không còn node chết."""

    @pytest.mark.parametrize(
        "node_name",
        [
            "node_pm_review",
            "node_prerequisite_check",
            "node_init_objectives",
            "node_allocate_schedule",
            "node_lock_ssot",
            "node_generate_master_content",
            "node_generate_blueprint",
            "node_parallel_derived_production",
        ],
    )
    def test_node_kiem_duoc_doc_lap(self, node_name):
        """
        Ba node từng là closure bên trong compile_learning_content_workflow() nên
        không thể import ra để kiểm riêng. Test này khoá lại việc đó.
        """
        assert callable(getattr(graph, node_name, None)), (
            f"{node_name} không truy cập được ở cấp module — không unit-test được"
        )

    def test_da_go_node_chet_html_first_production(self):
        workflow = graph.compile_learning_content_workflow()
        assert "html_first_production" not in workflow.nodes
        assert not hasattr(graph, "node_html_first_production")

    def test_do_thi_van_lien_mach_sau_khi_go_node(self):
        workflow = graph.compile_learning_content_workflow()
        for name in (
            "pm_review",
            "generate_master_content",
            "generate_blueprint",
            "parallel_derived_production",
            "final_compiler_and_publish",
        ):
            assert name in workflow.nodes

    def test_ham_ghi_dia_van_import_duoc_tu_graph(self):
        """Đã chuyển sang core/artifact_writer.py nhưng phải giữ tương thích ngược."""
        from core.artifact_writer import write_state_artifacts_to_disk as canonical

        assert graph.write_state_artifacts_to_disk is canonical


class TestBranchIsolation:
    """
    Mỗi nhánh song song phải nhận một bản state có container mutable RIÊNG.

    Đây là bất biến mà mọi ý định "tối ưu" copy.deepcopy thành shallow copy sẽ phá.
    Đo thực tế cho thấy deepcopy 5 nhánh của một state ~1 MB chỉ tốn 0,7 ms và
    0,05 MB — vì deepcopy trả về chính đối tượng cũ cho chuỗi bất biến, nên nội
    dung lớn vốn đã được chia sẻ sẵn. Đổi sang shallow copy là đánh đổi 0,7 ms lấy
    nguy cơ nhánh này ghi đè trạng thái của nhánh kia.
    """

    def test_moi_nhanh_ghi_trang_thai_doc_lap(self, monkeypatch):
        seen = {}

        def _make(name):
            def _run(state):
                # Mỗi nhánh ghi trạng thái của riêng nó rồi giữ lại tham chiếu dict.
                state.setdefault("artifacts_status", {})[name] = "DONE_" + name
                seen[name] = state["artifacts_status"]
                return state

            return _run

        patched = tuple(
            graph.DerivedPipeline(b.name, b.artifact_key, _make(b.artifact_key))
            for b in graph.DERIVED_PIPELINES
        )
        monkeypatch.setattr(graph, "DERIVED_PIPELINES", patched)
        monkeypatch.setattr(graph, "save_state_checkpoint", lambda state: None)

        graph.node_parallel_derived_production(_base_state())

        dict_ids = {id(d) for d in seen.values()}
        assert len(dict_ids) == len(seen), (
            "Hai nhánh dùng chung một dict artifacts_status — nhánh này sẽ ghi đè nhánh kia"
        )

    def test_nhanh_khong_lam_ban_state_goc(self, monkeypatch):
        def _run(state):
            state.setdefault("review_logs", []).append({"source": "nhanh", "feedback": "x"})
            return state

        patched = tuple(
            graph.DerivedPipeline(b.name, b.artifact_key, _run) for b in graph.DERIVED_PIPELINES
        )
        monkeypatch.setattr(graph, "DERIVED_PIPELINES", patched)
        monkeypatch.setattr(graph, "save_state_checkpoint", lambda state: None)

        original = _base_state()
        original["review_logs"] = []
        graph.node_parallel_derived_production(original)

        # Kết quả đi qua reducer append_unique, nên bản gốc không được bị 5 nhánh
        # cùng ghi thẳng vào.
        assert len(original["review_logs"]) <= 1, (
            f"State gốc bị các nhánh ghi trực tiếp: {len(original['review_logs'])} bản ghi"
        )

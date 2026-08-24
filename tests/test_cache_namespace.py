"""
tests/test_cache_namespace.py — Semantic cache phải cô lập theo phạm vi bài học (C2).

Lỗi được sửa: `cache_lookup` đối sánh mờ bằng TF-IDF với ngưỡng 0.88 trên TOÀN BỘ
bảng cache, không lọc theo bài học. Trong khi đó `with_semantic_cache` VỐN ĐÃ NHẬN
`session_id` và `lesson_id` nhưng không hề truyền xuống.

Hậu quả là lỗi sư phạm chứ không phải lỗi kỹ thuật: hai bài học liền kề cùng chủ đề
có prompt gần trùng nhau về từ vựng, nên bài sau có thể nhận lại nguyên nội dung của
bài trước — đúng ngữ pháp, đúng công nghệ, nhưng SAI PHẠM VI KIẾN THỨC (dùng khái
niệm chưa dạy, hoặc lặp lại đúng thứ vừa dạy). Không có gì báo lỗi vì kết quả trông
hoàn toàn hợp lệ.
"""

import pytest

from core import paths


@pytest.fixture
def cache(tmp_path, monkeypatch):
    """Cache sạch trong thư mục tạm, bật sẵn, prefix khoá học rỗng."""
    monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
    monkeypatch.setenv("SEMANTIC_CACHE_ENABLED", "true")
    paths.reset_path_cache()

    import importlib

    from core import persistence, semantic_cache

    importlib.reload(persistence)
    importlib.reload(semantic_cache)
    semantic_cache.CACHE_ENABLED = True
    semantic_cache.set_cache_namespace_prefix("")
    yield semantic_cache

    semantic_cache.set_cache_namespace_prefix("")
    paths.reset_path_cache()
    importlib.reload(persistence)
    importlib.reload(semantic_cache)


# Hai prompt cố tình gần như trùng nhau — đúng kịch bản hai bài học liền kề cùng chủ đề.
SYS = "Bạn là chuyên gia biên soạn học liệu Python. Hãy viết bài đọc về danh sách."
USER_L02 = "Viết bài đọc Lesson 02 về thao tác thêm phần tử trong danh sách List."
USER_L03 = "Viết bài đọc Lesson 03 về thao tác xoá phần tử trong danh sách List."


class TestCrossLessonIsolation:
    def test_hai_prompt_nay_that_su_du_giong_de_khop_mo(self, cache):
        """
        Nếu hai prompt mẫu KHÔNG đủ giống thì mọi test dưới đây trở nên vô nghĩa
        (chúng sẽ xanh vì lý do sai). Khẳng định tiền đề trước.
        """
        sim = cache._tf_idf_similarity(f"{SYS[:400]} {USER_L02[:800]}", f"{SYS[:400]} {USER_L03[:800]}")
        assert sim >= cache.SIMILARITY_THRESHOLD, (
            f"Độ tương đồng chỉ {sim:.3f} < ngưỡng {cache.SIMILARITY_THRESHOLD}; "
            f"hãy chỉnh lại cặp prompt mẫu cho sát kịch bản thật"
        )

    def test_bai_sau_khong_an_cache_cua_bai_truoc(self, cache):
        ns_l02 = cache.build_namespace("Reading Creator", "Session 05", "Lesson 02")
        ns_l03 = cache.build_namespace("Reading Creator", "Session 05", "Lesson 03")
        assert ns_l02 != ns_l03

        cache.cache_store(SYS, USER_L02, "NỘI DUNG CỦA LESSON 02", namespace=ns_l02)

        hit = cache.cache_lookup(SYS, USER_L03, namespace=ns_l03)
        assert hit is None, (
            "Lesson 03 đã nhận lại nội dung của Lesson 02 qua đối sánh mờ — "
            "đây chính là nội dung sai phạm vi kiến thức"
        )

    def test_dung_bai_do_thi_van_hit_binh_thuong(self, cache):
        """Cô lập không được làm cache mất tác dụng: cùng phạm vi vẫn phải hit."""
        ns = cache.build_namespace("Reading Creator", "Session 05", "Lesson 02")
        cache.cache_store(SYS, USER_L02, "NỘI DUNG CỦA LESSON 02", namespace=ns)

        assert cache.cache_lookup(SYS, USER_L02, namespace=ns) == "NỘI DUNG CỦA LESSON 02"

    def test_khop_mo_van_hoat_dong_trong_cung_pham_vi(self, cache):
        """
        Đối sánh mờ là tính năng có ích khi ở đúng phạm vi (prompt sinh lại lần 2
        khác vài ký tự). Chỉ chặn khớp CHÉO phạm vi, không giết luôn tính năng.
        """
        ns = cache.build_namespace("Reading Creator", "Session 05", "Lesson 02")
        cache.cache_store(SYS, USER_L02, "NỘI DUNG CỦA LESSON 02", namespace=ns)

        variant = USER_L02 + " "
        assert cache.cache_lookup(SYS, variant, namespace=ns) == "NỘI DUNG CỦA LESSON 02"


class TestAgentIsolation:
    def test_quiz_khong_an_cache_cua_reading(self, cache):
        """Prompt của Reading Creator và Quiz Creator cho cùng một bài chia sẻ rất nhiều từ vựng."""
        ns_reading = cache.build_namespace("Reading Creator", "Session 05", "Lesson 02")
        ns_quiz = cache.build_namespace("Quiz Creator", "Session 05", "Lesson 02")
        assert ns_reading != ns_quiz

        cache.cache_store(SYS, USER_L02, "BÀI ĐỌC HTML", namespace=ns_reading)
        assert cache.cache_lookup(SYS, USER_L02, namespace=ns_quiz) is None


class TestCourseIsolation:
    def test_hai_khoa_hoc_khac_nhau_khong_dung_chung_cache(self, cache):
        """Khoá nào cũng có 'Session 01 / Lesson 01' — thiếu prefix là lẫn nội dung giữa các khoá."""
        cache.set_cache_namespace_prefix("Lap_trinh_Python")
        ns_python = cache.build_namespace("Reading Creator", "Session 01", "Lesson 01")
        cache.cache_store(SYS, USER_L02, "NỘI DUNG KHOÁ PYTHON", namespace=ns_python)

        cache.set_cache_namespace_prefix("Lap_trinh_Java")
        ns_java = cache.build_namespace("Reading Creator", "Session 01", "Lesson 01")

        assert ns_python != ns_java
        assert cache.cache_lookup(SYS, USER_L02, namespace=ns_java) is None

    def test_cli_dat_prefix_khoa_hoc(self):
        """Hàm đặt prefix phải được CLI gọi, nếu không cô lập cấp khoá học chỉ là lý thuyết."""
        from pathlib import Path

        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert "set_cache_namespace_prefix(" in source, (
            "cli/commands/workflow_cmd.py không gọi set_cache_namespace_prefix — "
            "cache sẽ dùng chung giữa các khoá học"
        )


class TestPrimaryKeyCollision:
    def test_prompt_trung_nhau_o_hai_pham_vi_deu_luu_duoc(self, cache):
        """
        id của entry lấy từ hash prompt. Nếu namespace không nằm trong hash, hai
        phạm vi có prompt trùng nhau sẽ đụng khoá chính và INSERT OR IGNORE lặng lẽ
        vứt bản ghi thứ hai — phạm vi thứ hai vĩnh viễn không bao giờ cache được.
        """
        ns_a = cache.build_namespace("Reading Creator", "Session 01", "Lesson 01")
        ns_b = cache.build_namespace("Reading Creator", "Session 09", "Lesson 01")

        cache.cache_store(SYS, USER_L02, "NỘI DUNG A", namespace=ns_a)
        cache.cache_store(SYS, USER_L02, "NỘI DUNG B", namespace=ns_b)

        assert cache.cache_lookup(SYS, USER_L02, namespace=ns_a) == "NỘI DUNG A"
        assert cache.cache_lookup(SYS, USER_L02, namespace=ns_b) == "NỘI DUNG B"

    def test_hash_khac_nhau_theo_namespace(self, cache):
        h1 = cache._make_hash(SYS, USER_L02, "ns-mot")
        h2 = cache._make_hash(SYS, USER_L02, "ns-hai")
        assert h1 != h2


class TestLegacyEntries:
    def test_entry_cu_khong_namespace_khong_duoc_tai_su_dung(self, cache):
        """
        Entry sinh ra trước khi có cô lập được lưu với namespace rỗng. Chúng không
        thể tin là đúng phạm vi kiến thức nào, nên tuyệt đối không được phục vụ cho
        truy vấn mới. Mất một ít hiệu năng cache là cái giá đúng phải trả.
        """
        cache.cache_store(SYS, USER_L02, "NỘI DUNG CŨ KHÔNG RÕ PHẠM VI", namespace="")

        ns = cache.build_namespace("Reading Creator", "Session 05", "Lesson 02")
        assert cache.cache_lookup(SYS, USER_L02, namespace=ns) is None


class TestWrapperWiring:
    def test_wrapper_truyen_session_lesson_xuong_cache(self, cache, monkeypatch):
        """
        Hồi quy trực tiếp: wrapper đã nhận session_id/lesson_id từ trước nhưng không
        dùng. Test này khẳng định namespace thực sự đi tới tầng cache.
        """
        seen = {}

        def fake_lookup(system_prompt, user_prompt, agent_name="", fuzzy=True, namespace=""):
            seen["namespace"] = namespace
            return None

        monkeypatch.setattr(cache, "cache_lookup", fake_lookup)
        monkeypatch.setattr(cache, "cache_store", lambda *a, **k: None)

        wrapped = cache.with_semantic_cache(
            lambda system_prompt, user_prompt, **kwargs: "ket qua"
        )
        wrapped(SYS, USER_L02, agent_name="Reading Creator",
                session_id="Session 05", lesson_id="Lesson 02")

        assert "Session 05" in seen["namespace"]
        assert "Lesson 02" in seen["namespace"]
        assert "Reading Creator" in seen["namespace"]

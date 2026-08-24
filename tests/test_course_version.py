"""
tests/test_course_version.py — Phiên bản học liệu và nhật ký thay đổi (F3).

Một khoá học được sinh lại nhiều lần: sửa PM, đổi tech stack, nâng prompt, chạy lại
sau khi giảng viên rà soát. Hệ thống không lưu gì giữa các lần, nên ba câu hỏi vận
hành cơ bản đều không trả lời được:

    - "Lớp K18 học bản nào, lớp K19 học bản nào?"
    - "Lần chạy hôm nay đổi những gì so với hôm qua?"
    - "Bài tôi rà tuần trước, giờ còn nguyên như lúc tôi duyệt không?"

Câu thứ ba là câu đắt nhất: không có công cụ thì giảng viên phải mở từng file đọc
lại mới biết — với 20 buổi × 3 bài × 5 tài nguyên thì không ai làm.
"""

import time
from pathlib import Path

import pytest

from core import paths
from core.course_version import (
    IGNORED_NAMES,
    Changelog,
    compare_digests,
    find_changed_since_approval,
    get_latest_snapshot,
    next_version,
    scan_course_digests,
    snapshot_course,
)


@pytest.fixture
def course(tmp_path, monkeypatch):
    """Khoá học tối thiểu trong thư mục tạm, kho tri thức cũng tạm."""
    monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
    paths.reset_path_cache()

    root = tmp_path / "Lap_trinh_Python"
    lesson = root / "Session 02 - Bien" / "Lesson 01 - Khai bao"
    (lesson / "Bài đọc").mkdir(parents=True)
    (lesson / "Bài đọc" / "reading.html").write_text("<h1>Bản 1</h1>", encoding="utf-8")
    (lesson / "quiz.json").write_text('{"quiz": []}', encoding="utf-8")

    yield root
    paths.reset_path_cache()


class TestScanning:
    def test_chi_theo_doi_file_hoc_lieu(self, course):
        (course / "anh_minh_hoa.png").write_bytes(b"\x89PNG")
        (course / "ghi_chu.txt").write_text("tạm", encoding="utf-8")

        digests = scan_course_digests(str(course))

        assert not any(k.endswith((".png", ".txt")) for k in digests), (
            "Ảnh và tệp tạm đổi vì lý do kỹ thuật chứ không phải vì nội dung dạy học "
            "đổi — đưa vào sẽ khiến mọi lần sinh đều báo có thay đổi"
        )

    def test_bo_qua_san_pham_phu_cua_he_thong(self, course):
        for name in IGNORED_NAMES:
            (course / name).write_text("x", encoding="utf-8")

        digests = scan_course_digests(str(course))
        assert not any(name in digests for name in IGNORED_NAMES)

    def test_changelog_khong_tu_theo_doi_chinh_no(self, course):
        """
        Chính module này ghi ra CHANGELOG.md. Không loại trừ thì mỗi lần sinh, nội
        dung nhật ký đổi, nên lần sinh KẾ TIẾP luôn thấy "có 1 sửa đổi" và tăng số
        phiên bản dù học liệu không đổi gì.
        """
        assert "CHANGELOG.md" in IGNORED_NAMES

    def test_chuan_hoa_ky_tu_xuong_dong(self, course, tmp_path):
        """
        Không chuẩn hoá thì cùng nội dung sinh trên Windows và Linux cho hai mã băm
        khác nhau, và mọi lần chạy đổi máy đều báo "toàn bộ học liệu đã thay đổi".
        """
        a = tmp_path / "a"
        b = tmp_path / "b"
        a.mkdir()
        b.mkdir()
        (a / "x.md").write_bytes(b"dong 1\ndong 2")
        (b / "x.md").write_bytes(b"dong 1\r\ndong 2")

        assert scan_course_digests(str(a))["x.md"] == scan_course_digests(str(b))["x.md"]

    def test_thu_muc_khong_ton_tai_tra_ve_rong(self, tmp_path):
        assert scan_course_digests(str(tmp_path / "khong_co")) == {}


class TestComparison:
    def test_phan_loai_dung_ba_nhom_thay_doi(self):
        old = {"a": "1", "b": "2", "c": "3"}
        new = {"a": "1", "b": "SUA", "d": "4"}

        added, modified, removed = compare_digests(old, new)

        assert added == ["d"]
        assert modified == ["b"]
        assert removed == ["c"]

    def test_khong_doi_thi_khong_co_gi(self):
        d = {"a": "1"}
        assert compare_digests(d, dict(d)) == ([], [], [])


class TestVersionNumbering:
    def test_lan_dau_la_v1(self):
        assert next_version(None, ([], [], [])) == "v1.0.0"

    def test_them_hoac_go_tai_nguyen_tang_minor(self):
        """Thêm/gỡ tài nguyên nghĩa là CẤU TRÚC khoá học đã đổi."""
        assert next_version("v1.2.3", (["moi"], [], [])) == "v1.3.0"
        assert next_version("v1.2.3", ([], [], ["cu"])) == "v1.3.0"

    def test_chi_sua_noi_dung_tang_patch(self):
        assert next_version("v1.2.3", ([], ["sua"], [])) == "v1.2.4"

    def test_khong_doi_gi_thi_giu_nguyen_phien_ban(self):
        """
        Sinh ra phiên bản mới mà nội dung y hệt sẽ làm số phiên bản mất hết ý nghĩa.
        """
        assert next_version("v1.2.3", ([], [], [])) == "v1.2.3"

    def test_phien_ban_hong_thi_quay_ve_v1(self):
        assert next_version("khong-phai-phien-ban", ([], ["x"], [])) == "v1.0.0"


class TestSnapshotFlow:
    def test_lan_dau_ghi_v1_va_sinh_changelog(self, course):
        result = snapshot_course("Lap_trinh_Python", str(course))

        assert result["version"] == "v1.0.0"
        assert not result["changelog"].is_empty
        assert (course / "CHANGELOG.md").exists()

    def test_sinh_lai_khong_sua_gi_thi_khong_tang_phien_ban(self, course):
        first = snapshot_course("Lap_trinh_Python", str(course))
        second = snapshot_course("Lap_trinh_Python", str(course))

        assert second["version"] == first["version"]
        assert second["changelog"].is_empty

    def test_sua_noi_dung_thi_tang_patch(self, course):
        snapshot_course("Lap_trinh_Python", str(course))
        reading = course / "Session 02 - Bien" / "Lesson 01 - Khai bao" / "Bài đọc" / "reading.html"
        reading.write_text("<h1>Bản 2 khác hẳn</h1>", encoding="utf-8")

        result = snapshot_course("Lap_trinh_Python", str(course))

        assert result["version"] == "v1.0.1"
        assert len(result["changelog"].modified) == 1

    def test_them_tai_nguyen_thi_tang_minor(self, course):
        snapshot_course("Lap_trinh_Python", str(course))
        lab = course / "Session 02 - Bien" / "Lesson 01 - Khai bao" / "Bài thực hành"
        lab.mkdir()
        (lab / "practical_lab.md").write_text("# Lab", encoding="utf-8")

        result = snapshot_course("Lap_trinh_Python", str(course))
        assert result["version"] == "v1.1.0"

    def test_khong_ghi_anh_chup_trung_lap(self, course):
        """Lịch sử phiên bản đầy những mốc y hệt nhau sẽ không tra cứu được."""
        from core.course_version import list_snapshots

        snapshot_course("Lap_trinh_Python", str(course))
        snapshot_course("Lap_trinh_Python", str(course))
        snapshot_course("Lap_trinh_Python", str(course))

        assert len(list_snapshots("Lap_trinh_Python")) == 1

    def test_anh_chup_luu_lai_duoc(self, course):
        snapshot_course("Lap_trinh_Python", str(course))
        latest = get_latest_snapshot("Lap_trinh_Python")

        assert latest is not None
        assert latest.version == "v1.0.0"
        assert latest.artifact_count == 2


class TestStaleApprovals:
    """Câu hỏi đắt nhất mà module này trả lời."""

    def test_phat_hien_ban_da_duyet_bi_doi(self, course):
        from core.approvals import record_approval

        snapshot_course("Lap_trinh_Python", str(course))
        time.sleep(0.02)
        record_approval(
            artifact="html", reviewer="Nguyen Van A", course="Lap_trinh_Python",
            session_id="Session 02", lesson_id="Lesson 01",
        )
        time.sleep(0.02)

        reading = course / "Session 02 - Bien" / "Lesson 01 - Khai bao" / "Bài đọc" / "reading.html"
        reading.write_text("<h1>Bản sinh lại, KHÁC bản đã duyệt</h1>", encoding="utf-8")

        result = snapshot_course("Lap_trinh_Python", str(course))
        stale = result["stale_approvals"]

        assert len(stale) == 1
        assert stale[0]["reviewer"] == "Nguyen Van A"
        assert "reading.html" in stale[0]["path"]

    def test_ban_da_duyet_con_nguyen_thi_khong_bao(self, course):
        from core.approvals import record_approval

        snapshot_course("Lap_trinh_Python", str(course))
        time.sleep(0.02)
        record_approval(
            artifact="html", reviewer="A", course="Lap_trinh_Python",
            session_id="Session 02", lesson_id="Lesson 01",
        )

        digests = scan_course_digests(str(course))
        assert find_changed_since_approval("Lap_trinh_Python", digests) == []

    def test_chua_ai_duyet_thi_khong_co_gi_de_bao(self, course):
        digests = scan_course_digests(str(course))
        assert find_changed_since_approval("Lap_trinh_Python", digests) == []


class TestChangelogMarkdown:
    def test_liet_ke_du_ba_nhom(self):
        cl = Changelog(
            course="C", from_version="v1.0.0", to_version="v1.1.0",
            added=["a.html"], modified=["b.md"], removed=["c.json"],
        )
        md = cl.to_markdown()

        assert "v1.0.0" in md and "v1.1.0" in md
        assert "Thêm mới (1)" in md
        assert "Sửa đổi (1)" in md
        assert "Gỡ bỏ (1)" in md
        assert "3" in md

    def test_khong_thay_doi_thi_noi_ro(self):
        cl = Changelog(course="C", from_version="v1.0.0", to_version="v1.0.0")
        assert "Không có thay đổi" in cl.to_markdown()


class TestCliWiring:
    def test_workflow_danh_so_phien_ban_cuoi_luot_chay(self):
        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert "stamp_course_version(" in source

    def test_danh_so_truoc_khi_dung_trang_ra_soat(self):
        """
        Trang rà soát là công cụ quản trị, không phải học liệu, nên không được tính
        vào ảnh chụp phiên bản.
        """
        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert source.index("stamp_course_version(") < source.index("write_review_dashboard(course_dir.name")


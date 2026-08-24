"""
tests/test_xapi_export.py — Phát biểu xAPI / cmi5 trong gói xuất bản (F1).

SCORM 1.2 chỉ báo về LMS được vài trường nghèo nàn (lesson_status, score.raw,
session_time). Với chúng, câu hỏi duy nhất trả lời được là "sinh viên đã xong chưa
và mấy điểm". Những câu hỏi thực sự dùng để cải tiến học liệu thì không: bài nào bị
bỏ giữa chừng, câu quiz nào cả lớp cùng sai, phần nào tốn thời gian bất thường.

RÀNG BUỘC QUAN TRỌNG NHẤT của tính năng này: mã theo dõi tuyệt đối không được lọt
vào reading.html. Thiết kế bài đọc là vùng đóng băng. Nhóm test cuối cùng ở đây
kiểm chính điều đó trên gói .zip thật.
"""

import json
import zipfile
from pathlib import Path

import pytest

from core.xapi import (
    ACTIVITY_TYPE_QUESTION,
    VERB_COMPLETED,
    build_activity_id,
    build_cmi5_course_structure,
    build_statement,
    build_wrapper_tracking_snippet,
    build_xapi_client_js,
)

READING_HTML = (
    "<!DOCTYPE html>\n<html lang='vi'><head><title>Bài đọc</title></head>"
    "<body><h1>Biến và phép gán</h1><p>Nội dung bài học.</p></body></html>"
)


@pytest.fixture
def course_tree(tmp_path):
    """Cây thư mục học liệu tối thiểu đủ để bộ xuất bản quét ra một bài."""
    lesson_dir = tmp_path / "Session 02 - Bien va phep gan" / "Lesson 01 - Khai bao bien"
    lesson_dir.mkdir(parents=True)
    (lesson_dir / "reading.html").write_text(READING_HTML, encoding="utf-8")
    (lesson_dir / "quiz.json").write_text('{"quiz": []}', encoding="utf-8")
    return tmp_path


class TestActivityId:
    def test_iri_on_dinh_giua_cac_lan_xuat_ban(self):
        """
        IRI đổi giữa hai lần xuất là dữ liệu học tập của cùng một bài nằm rải rác
        thành nhiều hoạt động rời rạc trong LRS, không cộng lại được.
        """
        a = build_activity_id("http://x.vn/xapi", "Python", "Session 02", "Lesson 01")
        b = build_activity_id("http://x.vn/xapi", "Python", "Session 02", "Lesson 01")
        assert a == b

    def test_bai_khac_nhau_co_iri_khac_nhau(self):
        a = build_activity_id("http://x.vn", "Python", "Session 02", "Lesson 01")
        b = build_activity_id("http://x.vn", "Python", "Session 02", "Lesson 02")
        assert a != b

    def test_bo_qua_thanh_phan_rong(self):
        assert build_activity_id("http://x.vn", "Python", "Session 02", "") == (
            "http://x.vn/Python/Session_02"
        )


class TestStatement:
    def test_phat_bieu_dung_cau_truc_xapi(self):
        st = build_statement(
            "Nguyen Van A", "a@x.vn", VERB_COMPLETED,
            "http://x.vn/l1", "Bài 1", result={"completion": True},
        )
        assert st["actor"]["mbox"] == "mailto:a@x.vn"
        assert st["verb"]["id"] == VERB_COMPLETED
        assert st["object"]["id"] == "http://x.vn/l1"
        assert st["result"]["completion"] is True

    def test_khong_bia_danh_tinh_khi_thieu_email(self):
        st = build_statement("", "", VERB_COMPLETED, "http://x.vn/l1", "Bài 1")
        assert st["actor"]["mbox"] == "mailto:unknown@example.org"


class TestCmi5Structure:
    def test_liet_ke_moi_bai_hoc(self):
        lessons = [
            {"session_id": "Session 01", "lesson_id": "Lesson 01", "title": "Bài A", "rel_path": "s1/l1"},
            {"session_id": "Session 01", "lesson_id": "Lesson 02", "title": "Bài B", "rel_path": "s1/l2"},
        ]
        xml = build_cmi5_course_structure("Python", lessons)

        assert xml.count("<au ") == 2
        assert "Bài A" in xml and "Bài B" in xml
        assert "course/s1/l1/lesson.html" in xml

    def test_thoat_ky_tu_xml(self):
        lessons = [{"session_id": "S1", "lesson_id": "L1", "title": "A & B <script>", "rel_path": "p"}]
        xml = build_cmi5_course_structure("Khoá & Học", lessons)

        assert "<script>" not in xml
        assert "&amp;" in xml

    def test_xml_phan_tich_duoc(self):
        from xml.etree import ElementTree

        lessons = [{"session_id": "S1", "lesson_id": "L1", "title": "Bài A", "rel_path": "p"}]
        ElementTree.fromstring(build_cmi5_course_structure("Python", lessons))


class TestClientJs:
    def test_khong_co_endpoint_thi_chay_che_do_ghi_log(self):
        """Gói học liệu vẫn dùng được bình thường thay vì hỏng vì thiếu cấu hình."""
        js = build_xapi_client_js("")
        assert 'var ENDPOINT = "";' in js
        assert "console.debug" in js

    def test_endpoint_duoc_nhung_an_toan(self):
        """Endpoint là dữ liệu người dùng nhập; nhúng thô vào JS là lỗ chèn mã."""
        hostile = 'http://lrs.x.vn/"; alert(1); //'
        js = build_xapi_client_js(hostile)

        endpoint_line = next(
            ln for ln in js.split("\n") if ln.strip().startswith("var ENDPOINT")
        )

        # Toàn bộ giá trị phải nằm gọn trong MỘT literal chuỗi JSON hợp lệ. Nếu dấu
        # nháy không được thoát, chuỗi sẽ đóng sớm và phần sau thoát ra thành mã —
        # phép giải mã ngược dưới đây bắt đúng tình huống đó.
        literal = endpoint_line.strip()[len("var ENDPOINT = ") : -1]
        assert json.loads(literal) == hostile.rstrip("/"), (
            "Endpoint không được mã hoá an toàn: có thể thoát khỏi chuỗi để chèn mã"
        )

    def test_dung_sendbeacon_khi_roi_trang(self):
        """
        fetch thường bị huỷ giữa chừng lúc trang đóng — mà đó đúng là lúc gửi
        'terminated' kèm thời lượng học.
        """
        js = build_xapi_client_js("http://lrs.x.vn")
        assert "sendBeacon" in js
        assert "terminated" in js

    def test_lay_danh_tinh_tu_lms_khong_tu_bia(self):
        js = build_xapi_client_js("http://lrs.x.vn")
        assert 'queryParam("actor")' in js

    def test_mo_api_cho_noi_dung_tu_nguyen_goi(self):
        js = build_xapi_client_js("")
        assert "answered:" in js
        assert ACTIVITY_TYPE_QUESTION in js


class TestPackageExport:
    def _export(self, course_tree, tmp_path, **kwargs):
        from core.scorm_exporter import export_scorm_package

        out = tmp_path / "package.zip"
        export_scorm_package(
            output_course_dir=str(course_tree),
            course_name="Lap trinh Python",
            scorm_output_path=str(out),
            **kwargs,
        )
        return out

    def test_goi_chua_ca_scorm_lan_cmi5(self, course_tree, tmp_path):
        """
        Bổ sung BÊN CẠNH SCORM chứ không thay thế, để gói nạp được vào cả LMS đời cũ
        lẫn LMS hỗ trợ xAPI mà không phải chọn một bỏ một.
        """
        out = self._export(course_tree, tmp_path)
        with zipfile.ZipFile(out) as zf:
            names = zf.namelist()

        assert "imsmanifest.xml" in names
        assert "cmi5.xml" in names
        assert "shared/scorm_api.js" in names
        assert "shared/xapi.js" in names

    def test_lop_boc_co_ma_theo_doi(self, course_tree, tmp_path):
        out = self._export(course_tree, tmp_path, xapi_endpoint="http://lrs.x.vn")
        with zipfile.ZipFile(out) as zf:
            wrapper = next(n for n in zf.namelist() if n.endswith("lesson.html"))
            content = zf.read(wrapper).decode("utf-8")

        assert "shared/xapi.js" in content
        assert "XAPI.initialized()" in content
        assert "XAPI.terminated()" in content

    def test_endpoint_di_vao_goi(self, course_tree, tmp_path):
        out = self._export(course_tree, tmp_path, xapi_endpoint="http://lrs.x.vn")
        with zipfile.ZipFile(out) as zf:
            js = zf.read("shared/xapi.js").decode("utf-8")
        assert "http://lrs.x.vn" in js


class TestFrozenDesignUntouched:
    """
    Nhóm test quan trọng nhất của F1.

    Thiết kế bài đọc là vùng đóng băng. Cách duy nhất thêm được theo dõi mà không
    phạm vào đó là đặt toàn bộ mã ở LỚP BỌC và nhúng bài đọc nguyên vẹn trong iframe.
    """

    def test_reading_html_trong_goi_giong_nguyen_ban_tung_byte(self, course_tree, tmp_path):
        from core.scorm_exporter import export_scorm_package

        out = tmp_path / "package.zip"
        export_scorm_package(
            output_course_dir=str(course_tree),
            course_name="Lap trinh Python",
            scorm_output_path=str(out),
            xapi_endpoint="http://lrs.x.vn",
        )

        source_bytes = next(course_tree.rglob("reading.html")).read_bytes()

        with zipfile.ZipFile(out) as zf:
            name = next(n for n in zf.namelist() if n.endswith("reading.html"))
            packaged_bytes = zf.read(name)

        # So sánh với bản TRÊN ĐĨA chứ không phải chuỗi trong bộ nhớ: Windows ghi
        # file bằng CRLF, nên so với chuỗi gốc sẽ đỏ vì lý do chẳng liên quan gì tới
        # việc mã theo dõi có lọt vào hay không.
        assert packaged_bytes == source_bytes, (
            "reading.html trong gói đã khác bản gốc — mã theo dõi đã lọt vào vùng "
            "thiết kế đóng băng"
        )

    def test_khong_co_ma_xapi_nao_trong_reading_html(self, course_tree, tmp_path):
        from core.scorm_exporter import export_scorm_package

        out = tmp_path / "package.zip"
        export_scorm_package(
            output_course_dir=str(course_tree),
            course_name="C",
            scorm_output_path=str(out),
            xapi_endpoint="http://lrs.x.vn",
        )

        with zipfile.ZipFile(out) as zf:
            name = next(n for n in zf.namelist() if n.endswith("reading.html"))
            packaged = zf.read(name).decode("utf-8")

        for marker in ("XAPI", "xapi.js", "sendBeacon", "lrs.x.vn"):
            assert marker not in packaged, f"'{marker}' đã lọt vào bài đọc"

    def test_template_bai_doc_khong_he_biet_den_xapi(self):
        """Chặn ở tầng mã nguồn, không chỉ ở tầng gói xuất bản."""
        for path in ("templates/html/reading.html", "templates/html/reading_master.html.j2"):
            source = Path(path).read_text(encoding="utf-8")
            assert "xapi" not in source.lower(), f"{path} đã bị chèn mã xAPI"

    def test_ma_theo_doi_chi_o_lop_boc(self):
        source = Path("core/xapi.py").read_text(encoding="utf-8")
        assert "reading_master" not in source
        assert "templates/html" not in source


class TestCliFlags:
    def test_co_co_dong_lenh_xapi(self):
        import sys

        from cli.args import parse_cli_arguments

        argv = sys.argv
        try:
            sys.argv = ["main.py", "--scorm", "--xapi-endpoint", "http://lrs.x.vn"]
            args = parse_cli_arguments()
            assert args.xapi_endpoint == "http://lrs.x.vn"
        finally:
            sys.argv = argv

    def test_workflow_truyen_co_xuong_bo_xuat_ban(self):
        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert "xapi_endpoint=getattr(args" in source

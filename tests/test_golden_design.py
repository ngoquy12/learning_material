"""
tests/test_golden_design.py — HÀNG RÀO BẢO VỆ THIẾT KẾ HỌC LIỆU (G2).

Thiết kế bài đọc và bài thực hành hiện tại ĐÃ ĐẠT YÊU CẦU và được chốt là không
sửa nữa. Nhưng "không sửa nữa" nếu chỉ là thoả thuận miệng thì mọi refactor phía
sau (tách renderer, thêm tracking xAPI, dọn dead code) đều có thể làm lệch diện
mạo mà không ai nhận ra — HTML sinh ra dài hàng nghìn dòng, không ai diff bằng mắt.

File này biến thoả thuận đó thành ràng buộc kỹ thuật, gồm HAI lớp:

  Lớp 1 — Ảnh chụp nguyên văn (golden file).
      Render payload cố định rồi so từng byte với bản đã chốt trong
      tests/golden/expected/. Bắt được MỌI thay đổi, kể cả một khoảng trắng.

  Lớp 2 — Bất biến thiết kế.
      Lớp 1 có một điểm yếu chí mạng: khi ai đó chạy lệnh cập nhật golden để
      "cho nó xanh lại", bản lệch lập tức trở thành chuẩn mới và hàng rào tự vô
      hiệu hoá trong im lặng. Lớp 2 kiểm tra các dấu hiệu nhận diện bắt buộc
      (bảng màu Rikkei, bộ font, đủ 5 section, engine sandbox đúng công nghệ)
      TRỰC TIẾP trên bản golden — nên một lần regenerate cẩu thả vẫn bị chặn.

Cách cập nhật golden khi thay đổi thiết kế là CÓ CHỦ ĐÍCH:

    UPDATE_GOLDEN=1 python -m pytest tests/test_golden_design.py

Sau đó BẮT BUỘC đọc `git diff tests/golden/expected/` trước khi commit. Nếu diff
chứa thứ bạn không cố ý đổi, đó chính là hồi quy mà hàng rào này sinh ra để bắt.
"""

from __future__ import annotations

import difflib
import json
import os
import re
from pathlib import Path
from typing import Any

import pytest

GOLDEN_DIR = Path(__file__).parent / "golden"
FIXTURES_DIR = GOLDEN_DIR / "fixtures"
EXPECTED_DIR = GOLDEN_DIR / "expected"

UPDATE_MODE = os.getenv("UPDATE_GOLDEN", "").strip().lower() in ("1", "true", "yes")

# Bản render ngắn hơn ngưỡng này chắc chắn là hỏng (template lỗi, biến rỗng).
# Chặn ngay tại đây để một bản hỏng không bao giờ được ghi đè thành golden mới.
_MIN_PLAUSIBLE_HTML_LEN = 3000


def _load_fixtures() -> list[dict[str, Any]]:
    fixtures = []
    for path in sorted(FIXTURES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["name"] = path.stem
        fixtures.append(data)
    return fixtures


FIXTURES = _load_fixtures()
FIXTURE_IDS = [f["name"] for f in FIXTURES]


def _render(fixture: dict[str, Any]) -> str:
    """Dựng HTML từ fixture qua đúng hàm render mà pipeline thật sử dụng."""
    kind = fixture["renderer"]
    payload = fixture["payload"]
    metadata = fixture.get("metadata", {})

    if kind == "reading":
        from core.renderers.reading_renderer import assemble_reading_html

        return assemble_reading_html(payload, metadata)
    if kind == "lab":
        from agents.creators.practical_lab_creator import format_lab_to_html

        return format_lab_to_html(payload, metadata.get("tech_stack", ""))

    raise ValueError(f"Fixture '{fixture['name']}' khai báo renderer lạ: {kind!r}")


def _normalize(text: str) -> str:
    """
    Chuẩn hoá xuống dòng trước khi so sánh.

    Repo bật autocrlf nên cùng một file golden sẽ là CRLF khi checkout trên
    Windows và LF trên runner Linux. Không chuẩn hoá thì test đỏ toàn bộ trên
    một trong hai nền tảng vì lý do chẳng liên quan gì tới thiết kế.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _diff_report(name: str, expected: str, actual: str, max_lines: int = 60) -> str:
    diff = list(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile=f"golden/{name}.html (bản đã chốt)",
            tofile=f"{name} (bản vừa render)",
            lineterm="",
            n=2,
        )
    )
    shown = diff[:max_lines]
    tail = "" if len(diff) <= max_lines else f"\n... (còn {len(diff) - max_lines} dòng khác)"
    return (
        f"\n\nTHIẾT KẾ HỌC LIỆU ĐÃ LỆCH so với bản đã chốt: {name}\n"
        f"Thiết kế bài đọc/bài thực hành là vùng đóng băng — nếu thay đổi này KHÔNG\n"
        f"cố ý, hãy sửa lại code thay vì cập nhật golden.\n"
        f"Nếu ĐÚNG là bạn cố ý đổi thiết kế:\n"
        f"    UPDATE_GOLDEN=1 python -m pytest tests/test_golden_design.py\n"
        f"rồi đọc kỹ `git diff tests/golden/expected/` trước khi commit.\n\n"
        + "\n".join(shown)
        + tail
    )


class TestGoldenSnapshot:
    """Lớp 1: ảnh chụp nguyên văn."""

    def test_co_fixture_de_kiem(self):
        """Thư mục fixture rỗng nghĩa là hàng rào không bảo vệ gì cả."""
        assert FIXTURES, "Không tìm thấy fixture nào trong tests/golden/fixtures/"

    @pytest.mark.parametrize("fixture", FIXTURES, ids=FIXTURE_IDS)
    def test_render_khop_ban_da_chot(self, fixture):
        name = fixture["name"]
        actual = _normalize(_render(fixture))

        assert len(actual) >= _MIN_PLAUSIBLE_HTML_LEN, (
            f"Bản render của '{name}' chỉ dài {len(actual)} ký tự — quá ngắn so với một "
            f"trang học liệu hoàn chỉnh. Nhiều khả năng template hỏng hoặc context rỗng; "
            f"tuyệt đối không ghi đè bản này thành golden."
        )

        expected_path = EXPECTED_DIR / f"{name}.html"

        if UPDATE_MODE:
            EXPECTED_DIR.mkdir(parents=True, exist_ok=True)
            expected_path.write_text(actual, encoding="utf-8", newline="\n")
            pytest.skip(f"UPDATE_GOLDEN: đã ghi lại bản chốt cho '{name}'")

        assert expected_path.exists(), (
            f"Chưa có bản chốt cho '{name}'. Sinh lần đầu bằng:\n"
            f"    UPDATE_GOLDEN=1 python -m pytest tests/test_golden_design.py"
        )

        expected = _normalize(expected_path.read_text(encoding="utf-8"))
        assert actual == expected, _diff_report(name, expected, actual)


class TestDesignInvariants:
    """
    Lớp 2: các dấu hiệu nhận diện bắt buộc, kiểm TRỰC TIẾP trên bản golden.

    Mục đích không phải kiểm lại lớp 1, mà là chặn kịch bản ai đó chạy
    UPDATE_GOLDEN để làm CI xanh trở lại và vô hiệu hoá hàng rào trong im lặng.
    """

    @pytest.fixture(scope="class")
    def golden_texts(self) -> dict[str, str]:
        if UPDATE_MODE:
            pytest.skip("Đang ở chế độ cập nhật golden")
        texts = {}
        for fixture in FIXTURES:
            path = EXPECTED_DIR / f"{fixture['name']}.html"
            if path.exists():
                texts[fixture["name"]] = _normalize(path.read_text(encoding="utf-8"))
        if not texts:
            pytest.skip("Chưa có bản golden nào để kiểm bất biến")
        return texts

    def test_giu_nguyen_bang_mau_thuong_hieu(self, golden_texts):
        """Đỏ Rikkei #be111c là nhận diện thương hiệu, mất nó là mất bộ nhận diện."""
        for name, html in golden_texts.items():
            assert "#be111c" in html, f"{name}: thiếu mã màu đỏ Rikkei #be111c"
            assert "rikkei" in html.lower(), f"{name}: thiếu token màu 'rikkei'"

    def test_giu_nguyen_bo_font(self, golden_texts):
        for name, html in golden_texts.items():
            for font in ("Montserrat", "JetBrains Mono"):
                assert font in html, f"{name}: thiếu font bắt buộc '{font}'"

    def test_bai_doc_giu_du_5_section(self, golden_texts):
        """Kiến trúc 5 phần cố định là chỉ thị sư phạm số 1 của AGENTS.md."""
        for fixture in FIXTURES:
            if fixture["renderer"] != "reading":
                continue
            html = golden_texts.get(fixture["name"])
            if html is None:
                continue
            for idx in range(1, 6):
                assert f'id="section-{idx}"' in html, (
                    f"{fixture['name']}: thiếu Section {idx} — kiến trúc 5 phần cố định "
                    f"của bài đọc đã bị phá vỡ"
                )

    # Thẻ script thật sự TẢI VỀ runtime Python WASM (~10MB). Đây mới là thứ phải
    # chặn, chứ không phải mọi lần chuỗi "pyodide" xuất hiện trong trang: bản thân
    # hàm trợ giúp JS có nhắc tên engine nhưng bị cờ isPython vô hiệu hoá.
    _PYODIDE_RUNTIME = re.compile(r"<script[^>]+pyodide[^>]*\.js", re.IGNORECASE)

    def test_khong_tai_runtime_python_cho_mon_khac(self, golden_texts):
        """
        Rò rỉ engine sai công nghệ là lỗi thật đã từng xảy ra: bài SQL/Git bị nhúng
        runtime Python. resolve_domain_engine() chặn ở tầng chọn engine, còn đây chặn
        ở tầng HTML thành phẩm — nơi hậu quả là học viên tải về ~10MB WASM vô dụng.
        """
        expectations = {
            "reading_python_full": True,
            "reading_javascript_visual": False,
            "reading_sql_minimal": False,
            "reading_concept_static": False,
            "lab_python": True,
            "lab_sql": False,
        }
        for name, should_load in expectations.items():
            html = golden_texts.get(name)
            if html is None:
                continue
            loads_runtime = bool(self._PYODIDE_RUNTIME.search(html))
            if should_load:
                assert loads_runtime, f"{name}: bài học Python phải nạp runtime Pyodide"
            else:
                assert not loads_runtime, (
                    f"{name}: KHÔNG được nạp runtime Pyodide — đây là rò rỉ engine Python "
                    f"sang môn học khác công nghệ, bắt học viên tải ~10MB WASM vô ích"
                )

    def test_co_sandbox_bat_dung_theo_cong_nghe(self, golden_texts):
        """
        Cờ quyết định có chạy code Python hay không phải khớp với công nghệ bài học.
        Bài lab non-Python phải rơi vào nhánh kiểm cú pháp tĩnh.
        """
        cases = {"lab_python": '"true" === "true"', "lab_sql": '"false" === "true"'}
        for name, expected_flag in cases.items():
            html = golden_texts.get(name)
            if html is None:
                continue
            assert expected_flag in html, (
                f"{name}: cờ bật sandbox Python không khớp công nghệ bài học "
                f"(mong đợi {expected_flag!r})"
            )

    def test_khong_lot_cu_phap_jinja_chua_render(self, golden_texts):
        """Còn '{{' hoặc '{%' trong thành phẩm nghĩa là template render dở dang."""
        leftover = re.compile(r"\{\{[^}]*\}\}|\{%[^%]*%\}")
        for name, html in golden_texts.items():
            found = leftover.findall(html)
            assert not found, f"{name}: còn cú pháp Jinja chưa render: {found[:3]}"


class TestFixtureCoverage:
    """Bộ fixture phải phủ hết các nhánh điều kiện của template, nếu không hàng rào có lỗ."""

    def test_phu_du_cac_loai_engine(self):
        stacks = {f["metadata"].get("tech_stack", "").lower() for f in FIXTURES}
        for keyword in ("python", "javascript", "sql", "git"):
            assert any(keyword in s for s in stacks), (
                f"Thiếu fixture cho nhóm công nghệ '{keyword}' — nhánh engine tương ứng "
                f"trong template không được bảo vệ"
            )

    def test_phu_ca_nhanh_co_va_khong_co_thanh_phan_tuy_chon(self):
        readings = [f for f in FIXTURES if f["renderer"] == "reading"]
        for key in ("self_test_questions", "visualizer_component_html", "context_image_url"):
            has = [f for f in readings if f["payload"].get(key)]
            lacks = [f for f in readings if not f["payload"].get(key)]
            assert has, f"Không fixture nào CÓ '{key}' — nhánh khẳng định không được phủ"
            assert lacks, f"Không fixture nào THIẾU '{key}' — nhánh phủ định không được phủ"

    def test_moi_fixture_deu_co_mo_ta(self):
        """Mô tả là thứ giải thích fixture này bảo vệ điều gì — thiếu nó thì vô nghĩa."""
        for fixture in FIXTURES:
            assert fixture.get("description", "").strip(), (
                f"Fixture '{fixture['name']}' thiếu trường 'description'"
            )

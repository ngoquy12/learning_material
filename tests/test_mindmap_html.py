import re

from core.renderers.mindmap_exporter import parse_markmap_tree, validate_mindmap_structure
from core.renderers.mindmap_html import build_mindmap_html

SAMPLE = """# Cấu trúc <điều kiện>

## Lesson 01 — Câu lệnh if
### Khái niệm
- Rẽ nhánh theo điều kiện
### Cú pháp
- Khai báo: `if (a < b) {}`
  - Điều kiện: boolean
### Ví dụ
- Kịch bản: xếp loại
  ```javascript
  const x = "<script>alert(1)</script>";
  ```
### Lưu ý
- **Dùng `=` thay `===`**: gán nhầm

## Lesson 02 — Vòng lặp
### A
- a1
### B
- b1
### C
- c1
### D
- d1

## Liên kết hệ thống
- Lesson 01 là tiền đề của Lesson 02
"""


def _render(tmp_path):
    tree = parse_markmap_tree(SAMPLE)
    out = tmp_path / "mindmap.html"
    assert build_mindmap_html(tree, out, "Cấu trúc <điều kiện>")
    return tree, out.read_text(encoding="utf-8")


def test_html_contains_all_nodes_and_structure(tmp_path):
    tree, html = _render(tmp_path)
    assert validate_mindmap_structure(tree) == []
    for text in ["Câu lệnh if", "Vòng lặp", "Liên kết hệ thống", "Rẽ nhánh theo điều kiện",
                 "Khái niệm", "Lưu ý", "tiền đề"]:
        assert text in html
    # 1 root + 3 H2 + 8 H3 branches => 12 heading nodes carry class l0/l1/l2
    assert html.count('class="n l0') == 1
    assert html.count('class="n l1') == 3
    assert html.count('class="n l2') == 8


def test_html_escapes_content(tmp_path):
    _, html = _render(tmp_path)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<điều kiện>" not in html
    assert "<pre>" in html and "<code>" in html


def test_html_is_self_contained_light(tmp_path):
    _, html = _render(tmp_path)
    assert not re.search(r'(src|href)\s*=\s*["\']?https?://', html)
    assert "cdn" not in html.lower()
    assert "prefers-color-scheme" not in html
    assert "Thu gọn tất cả" in html and "Mở rộng tất cả" in html


def test_html_missing_root_returns_false(tmp_path):
    assert build_mindmap_html({"children": []}, tmp_path / "x.html") is False

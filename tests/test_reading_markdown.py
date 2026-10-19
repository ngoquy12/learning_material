import tempfile
import unittest
from pathlib import Path

from core.renderers.reading_markdown import convert_html_to_markdown

HTML = """<!doctype html><html><body>
<aside id="toc">MUC LUC BEN TRAI</aside>
<h1>Bài đọc thử</h1>
<section id="section-1"><h2>1. Đặt vấn đề</h2><p>Cửa hàng cần tính tiền.</p></section>
<section id="section-2"><h2>2. Cú pháp</h2><pre><code>total = 1 + 2</code></pre></section>
</body></html>"""


class TestReadingMarkdown(unittest.TestCase):
    def _convert(self, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "reading.html"
            p.write_text(HTML, encoding="utf-8")
            return convert_html_to_markdown(str(p), **kw)

    def test_giu_noi_dung_bo_giao_dien(self):
        md = self._convert(default_lang="python")
        self.assertIn("Bài đọc thử", md)
        self.assertIn("Cửa hàng cần tính tiền.", md)
        self.assertNotIn("MUC LUC BEN TRAI", md)

    def test_ngon_ngu_mac_dinh_lay_tu_tham_so_khong_doan_theo_duong_dan(self):
        self.assertIn("```python", self._convert(default_lang="python"))
        # Đường dẫn tạm chứa chữ "py"/"js"/"c" không được ảnh hưởng.
        self.assertNotIn("```c\n", self._convert(default_lang="python"))

    def test_artifact_writer_sinh_reading_md_dung_ngon_ngu(self):
        from core.artifact_writer import write_state_artifacts_to_disk

        with tempfile.TemporaryDirectory() as tmp:
            state = {"session_id": "Session 01", "lesson_id": "Lesson 01", "technology_stack": "Python",
                     "html_content": HTML, "requested_parts": ["html"], "artifacts_status": {}}
            written = write_state_artifacts_to_disk(state, lesson_dir=Path(tmp))
            md = Path(written["markdown"]).read_text(encoding="utf-8")
            self.assertIn("```python", md)


if __name__ == "__main__":
    unittest.main()

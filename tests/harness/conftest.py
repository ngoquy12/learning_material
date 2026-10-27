"""Fixture dùng chung cho test harness."""
from __future__ import annotations

from pathlib import Path

import pytest

SESSION = "Session 01 - Ly thuyet"


def write_tree(root: Path, files: dict[str, str | bytes]) -> Path:
    """Ghi các tệp từ dict {đường dẫn tương đối: nội dung}; tạo thư mục cha."""
    for rel, content in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
    return root


def course_files() -> dict[str, str | bytes]:
    """Cấu trúc môn giả đủ 7 loại (nội dung chỉ là chỗ giữ chỗ)."""
    s = SESSION
    ex = f"{s}/Bai tap/1_co_ban_1_demo"
    return {
        "README.md": "# Mon hoc\n",
        f"{s}/Lesson 01 - Mo dau/Bai doc/reading.html": "<html></html>",
        f"{s}/Lesson 01 - Mo dau/Bai doc/reading.md": "# doc\n",
        f"{s}/Lesson 01 - Mo dau/Quizz lesson/quiz.md": "# quiz\n",
        f"{s}/Lesson 01 - Mo dau/Quizz lesson/Quizz_Session01_Lesson01.xlsx": b"PK",
        f"{s}/Lesson 01 - Mo dau/Cau hoi bai doc/reading_questions.md": "# cau hoi\n",
        f"{s}/Quizz session/quizz_cuoi_gio.md": "# quiz cuoi gio\n",
        f"{s}/Quizz session/Quizz_Session01.xlsx": b"PK",
        f"{s}/Bai giang tren lop/slides.html": "<html></html>",
        f"{s}/Slide bài giảng/deck.pptx": b"PK",
        f"{s}/Bai thuc hanh/lab_guide.md": "# Lab\n",
        f"{ex}/de_bai_bai_tap.md": "# de\n",
        f"{ex}/tieu_chi_cham_diem_ai.md": "# tieu chi\n",
        f"{ex}/starter/package.json": "{}",
        f"{s}/Bai tap/HOP_DONG_CHUNG.md": "# hop dong\n",
        f"{s}/Bai tap/tai_lieu_giang_vien/dap_an_mau/bai_1/solution.js": "//\n",
        "node_modules/x/reading.html": "<html></html>",
    }


@pytest.fixture
def course_tree(tmp_path: Path) -> Path:
    return write_tree(tmp_path / "course", course_files())

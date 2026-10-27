"""Mẫu hợp lệ dùng chung, tái dùng các builder của test cổng."""
from __future__ import annotations

from pathlib import Path

from tests.harness.test_gate_exercise import de_bai
from tests.harness.test_gate_lab import lab_md
from tests.harness.test_gate_quiz import lesson_md, lesson_xlsx, session_md, session_xlsx
from tests.harness.test_gate_slide_pptx import make_deck

READING_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "harness" / "reading_ok.html"
SLIDE_HTML = "<html><body><div class='slide active'><h2>Biến và kiểu dữ liệu</h2><p>Nội dung</p></div></body></html>"
SESSION = "Session 01 - Ly thuyet"


def build_valid_course(root: Path) -> Path:
    """Cây môn nhỏ đủ 7 loại, mỗi tài nguyên hợp lệ với cổng tĩnh tương ứng."""
    s = root / SESSION
    reading = s / "Lesson 01 - Mo dau" / "Bai doc"
    reading.mkdir(parents=True)
    (reading / "reading.html").write_text(READING_FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    ql = s / "Lesson 01 - Mo dau" / "Quizz lesson"
    ql.mkdir(parents=True)
    (ql / "quiz.md").write_text(lesson_md(), encoding="utf-8")
    lesson_xlsx(ql / "Quizz_S01_L01.xlsx")
    qs = s / "Quizz session"
    qs.mkdir(parents=True)
    (qs / "quizz_cuoi_gio.md").write_text(session_md(), encoding="utf-8")
    session_xlsx(qs / "Session01.xlsx")
    (s / "Bai giang tren lop").mkdir(parents=True)
    (s / "Bai giang tren lop" / "slides.html").write_text(SLIDE_HTML, encoding="utf-8")
    (s / "Slide bai giang").mkdir(parents=True)
    make_deck(s / "Slide bai giang" / "deck.pptx")
    (s / "Bai thuc hanh").mkdir(parents=True)
    (s / "Bai thuc hanh" / "lab_guide.md").write_text(lab_md(), encoding="utf-8")
    base = s / "Bai tap"
    ex = base / "1_tong_hop_demo"
    (ex / "starter").mkdir(parents=True)
    (ex / "de_bai_bai_tap.md").write_text(de_bai(), encoding="utf-8")
    (ex / "tieu_chi_cham_diem_ai.md").write_text("tiêu chí", encoding="utf-8")
    (ex / "starter" / "index.js").write_text("x", encoding="utf-8")
    sol = base / "tai_lieu_giang_vien" / "dap_an_mau" / "bai_1"
    sol.mkdir(parents=True)
    (sol / "index.js").write_text("y", encoding="utf-8")
    (base / "tai_lieu_giang_vien" / "huong_dan_bai_1.md").write_text("hd", encoding="utf-8")
    return root

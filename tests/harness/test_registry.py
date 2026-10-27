from core.harness.registry import detect_kind, discover, normalize_name


def test_normalize():
    assert normalize_name("Slide bài giảng") == "slide bai giang"
    assert normalize_name("Bài Đọc") == "bai doc"


def test_discover(course_tree):
    found, unknown = discover(course_tree)
    kinds = sorted(k for k, _ in found)
    assert kinds == ["exercise", "lab", "quiz_lesson", "quiz_session", "reading", "slide_html", "slide_pptx"]
    assert not any("node_modules" in str(p) or "tai_lieu_giang_vien" in str(p) for _, p in found)
    assert any(p.name == "README.md" for p in unknown)


def test_discover_targets_and_unknown_details(course_tree):
    found, unknown = discover(course_tree)
    by_kind = dict(found)
    assert by_kind["quiz_lesson"].is_dir() and by_kind["quiz_lesson"].name == "Quizz lesson"
    assert by_kind["quiz_session"].is_dir()
    assert by_kind["exercise"].is_dir() and by_kind["exercise"].name.startswith("1_")
    assert by_kind["slide_pptx"].name == "deck.pptx"
    names = {p.name for p in unknown}
    assert {"README.md", "reading_questions.md", "HOP_DONG_CHUNG.md"} <= names
    assert "reading.md" not in names
    assert all(p.is_file() for p in unknown)
    inside = ("starter", "quiz.md", "quizz_cuoi_gio.md", "node_modules", "tai_lieu_giang_vien", ".xlsx")
    assert not any(any(s in str(p) for s in inside) for p in unknown)


def test_detect_kind_on_single_file(course_tree):
    html = next(course_tree.rglob("reading.html"))
    assert detect_kind(html) == "reading"


def test_detect_kind_quiz_folder_and_files(course_tree):
    qdir = next(course_tree.rglob("Quizz lesson"))
    assert detect_kind(qdir) == "quiz_lesson"
    assert detect_kind(qdir / "quiz.md") == "quiz_lesson"
    assert detect_kind(next(qdir.glob("*.xlsx"))) == "quiz_lesson"
    sdir = next(course_tree.rglob("Quizz session"))
    assert detect_kind(sdir) == "quiz_session"
    assert detect_kind(sdir / "quizz_cuoi_gio.md") == "quiz_session"


def test_detect_kind_none_cases(course_tree):
    assert detect_kind(course_tree / "README.md") is None
    assert detect_kind(next(course_tree.rglob("reading_questions.md"))) is None
    assert detect_kind(next(course_tree.rglob("package.json"))) is None
    assert detect_kind(next(course_tree.rglob("HOP_DONG_CHUNG.md"))) is None

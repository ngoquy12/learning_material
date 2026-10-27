import copy
import shutil

from core.harness.course_spec import load_spec
from core.harness.planner import build_tasks, resolve_target
from tests.harness._course_spec_samples import VALID, make_course_tree, write_yaml


def _spec(tmp_path, data):
    course = make_course_tree(tmp_path, data)
    return load_spec(write_yaml(course, data)), course


def _by_id(tasks):
    return {t.id: t for t in tasks}


def _theory_only(exercises=2):
    data = copy.deepcopy(VALID)
    data["sessions"] = data["sessions"][:1]
    data["sessions"][0]["exercises"] = exercises
    return data


def test_ids_and_waves(tmp_path):
    spec, course = _spec(tmp_path, _theory_only())
    tasks = _by_id(build_tasks(spec, course))
    assert set(tasks) == {
        "s01/l01/reading", "s01/l02/reading",
        "s01/l01/reading_questions", "s01/l02/reading_questions",
        "s01/l01/quiz_lesson", "s01/l02/quiz_lesson",
        "s01/quiz_session", "s01/exercise_1", "s01/exercise_2", "s01/slide_html",
    }
    for tid, task in tasks.items():
        assert task.wave == (1 if tid.endswith("/reading") else 2)
    assert tasks["s01/quiz_session"].depends_on == ["s01/l01/reading", "s01/l02/reading"]
    assert tasks["s01/quiz_session"].skill == "quizz_session"
    assert tasks["s01/l01/reading_questions"].gate is None
    assert tasks["s01/l01/reading"].gate == "reading"
    built = build_tasks(spec, course)
    assert built == sorted(built, key=lambda t: (t.wave, t.id))


def test_practice_depends_on_previous_theory(tmp_path):
    data = copy.deepcopy(VALID)
    data["sessions"][1]["resources"] = ["lab"]
    data["sessions"][1]["exercises"] = 0
    spec, course = _spec(tmp_path, data)
    lab = _by_id(build_tasks(spec, course))["s02/lab"]
    assert lab.depends_on == ["s01/l01/reading", "s01/l02/reading"]
    assert lab.wave == 2


def test_practice_exercises_depend_on_dep_sessions(tmp_path):
    spec, course = _spec(tmp_path, copy.deepcopy(VALID))
    ex = _by_id(build_tasks(spec, course))["s02/exercise_1"]
    assert ex.depends_on == ["s01/l01/reading", "s01/l02/reading"]


def test_resolve_accented_folders(tmp_path):
    spec, course = _spec(tmp_path, copy.deepcopy(VALID))
    d = course / "Session 01 - Ly thuyet" / "Lesson 01 - Tong quan" / "Bài đọc"
    d.mkdir()
    (d / "reading.html").write_text("x", encoding="utf-8")
    t = _by_id(build_tasks(spec, course))["s01/l01/reading"]
    assert t.target == (d / "reading.html").resolve()


def test_missing_session_on_disk(tmp_path):
    data = copy.deepcopy(VALID)
    data["sessions"].append({"folder": "Session 09 - Y", "lessons": [{"folder": "Lesson 01 - Z"}]})
    spec, course = _spec(tmp_path, data)
    shutil.rmtree(course / "Session 09 - Y")
    t = _by_id(build_tasks(spec, course))["s03/l01/reading"]
    assert t.target is None
    assert t.target_hint == "Session 09 - Y/Lesson 01 - Z/Bai doc/reading.html"


def test_exercise_folder_match(tmp_path):
    spec, course = _spec(tmp_path, _theory_only(exercises=3))
    base = course / "Session 01 - Ly thuyet" / "Bai tap"
    for n in ("1_a", "2_b", "tai_lieu_giang_vien"):
        (base / n).mkdir(parents=True)
    tasks = _by_id(build_tasks(spec, course))
    assert tasks["s01/exercise_1"].target == (base / "1_a").resolve()
    assert tasks["s01/exercise_3"].target is None
    assert tasks["s01/exercise_3"].target_hint == "Session 01 - Ly thuyet/Bai tap/3_..."


def test_pptx_first_file(tmp_path):
    d = tmp_path / "Slide bai giang"
    d.mkdir()
    for n in ("b.pptx", "a.pptx", "~$a.pptx"):
        (d / n).write_text("x")
    assert resolve_target(tmp_path, ["Slide bai giang"], "*.pptx") == d / "a.pptx"


def test_hint_uses_accented_folder_on_disk(tmp_path):
    spec, course = _spec(tmp_path, copy.deepcopy(VALID))
    (course / "Session 01 - Ly thuyet" / "Lesson 01 - Tong quan" / "Bài đọc").mkdir()
    t = _by_id(build_tasks(spec, course))["s01/l01/reading"]
    assert t.target is None
    assert t.target_hint == "Session 01 - Ly thuyet/Lesson 01 - Tong quan/Bài đọc/reading.html"

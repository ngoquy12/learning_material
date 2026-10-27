import copy

import pytest

from core.harness.course_spec import SpecError, load_spec
from tests.harness._course_spec_samples import VALID, write_yaml


def test_load_valid(tmp_path):
    spec = load_spec(write_yaml(tmp_path, VALID))
    assert spec.course_id == "demo" and len(spec.sessions) == 2
    assert spec.sessions[1].kind == "practice" and spec.sessions[1].exercises == 2
    assert spec.lesson_resources(spec.sessions[0].lessons[0]) == ["reading", "reading_questions", "quiz_lesson"]


def test_lesson_override(tmp_path):
    d = copy.deepcopy(VALID)
    d["sessions"][0]["lessons"][0]["resources"] = ["reading"]
    spec = load_spec(write_yaml(tmp_path, d))
    assert spec.lesson_resources(spec.sessions[0].lessons[0]) == ["reading"]


@pytest.mark.parametrize("mutate, needle", [
    (lambda d: d.pop("course_id"), "course_id"),
    (lambda d: d.update(course_id=" "), "course_id"),
    (lambda d: d["sessions"][0]["resources"].append("video"), "sessions[0].resources"),
    (lambda d: d["sessions"][0]["lessons"][0].update(resources=["slide_html"]), "sessions[0].lessons[0].resources"),
    (lambda d: d["sessions"][0].update(resources=["exercises"], exercises=0), "exercises"),
    (lambda d: d["sessions"][0].update(depends_on_sessions=[1]), "depends_on_sessions"),
    (lambda d: d["sessions"][1].update(folder=d["sessions"][0]["folder"]), "trùng"),
    (lambda d: d["sessions"][0]["lessons"][1].update(folder="lesson 01 - tong quan"), "trùng"),
    (lambda d: d["sessions"][0].update(kind="other"), "sessions[0].kind"),
])
def test_invalid(tmp_path, mutate, needle):
    d = copy.deepcopy(VALID)
    mutate(d)
    with pytest.raises(SpecError) as e:
        load_spec(write_yaml(tmp_path, d))
    assert any(needle in m for m in e.value.messages)


@pytest.mark.parametrize("content", ["", "- a\n- b\n", "a: [unclosed"])
def test_not_yaml_mapping(tmp_path, content):
    p = tmp_path / "course_spec.yaml"
    p.write_text(content, encoding="utf-8")
    with pytest.raises(SpecError):
        load_spec(p)


def test_missing_file(tmp_path):
    with pytest.raises(SpecError):
        load_spec(tmp_path / "none.yaml")


def test_non_utf8(tmp_path):
    p = tmp_path / "course_spec.yaml"
    p.write_bytes(b"course_id: " + bytes([0xFF, 0xFE]))
    with pytest.raises(SpecError) as e:
        load_spec(p)
    assert any("UTF-8" in m for m in e.value.messages)


def test_malformed_yaml_message_vietnamese(tmp_path):
    p = tmp_path / "course_spec.yaml"
    p.write_text("a: [unclosed\n", encoding="utf-8")
    with pytest.raises(SpecError) as e:
        load_spec(p)
    text = " ".join(e.value.messages)
    assert "dòng" in text and "while parsing" not in text


@pytest.mark.parametrize("mutate, needle", [
    (lambda d: d["sessions"][0].update(resourcs=["lab"]), "sessions[0].resourcs"),
    (lambda d: d.update(sessions=["x"]), "sessions[0]"),
    (lambda d: d["sessions"][0].update(exercises=-1), "không được âm"),
])
def test_strict_and_vietnamese(tmp_path, mutate, needle):
    d = copy.deepcopy(VALID)
    mutate(d)
    with pytest.raises(SpecError) as e:
        load_spec(write_yaml(tmp_path, d))
    assert any(needle in m for m in e.value.messages)
    assert not any("Input should" in m or "Extra inputs" in m for m in e.value.messages)

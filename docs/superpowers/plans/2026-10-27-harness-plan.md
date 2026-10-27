# Harness Plan (đặc tả môn và bộ lập lịch) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `course_spec.yaml` + các lệnh `python -m core.harness init|plan|status|next` suy ra nhiệm vụ, đợt và trạng thái của một môn từ đặc tả và kết quả `verify`.

**Architecture:** Bốn module mới trong `core/harness/` (`course_spec`, `planner`, `state`, `spec_init`) và một `cli.py` gom lệnh con; `state` gọi `verify_path` có sẵn làm cổng; trạng thái lưu ở `storage/harness/<course_id>/state.json`.

**Tech Stack:** Python 3.10, pydantic 2, PyYAML 6, pytest.

**Spec:** `docs/superpowers/specs/2026-10-27-harness-plan-design.md`

## Global Constraints

- Không hardcode tên môn, session, công nghệ; mọi thứ đến từ đặc tả hoặc đĩa.
- Khớp tên thư mục bằng `core.harness.registry.normalize_name` (bỏ dấu, không phân biệt hoa thường).
- `init` chỉ ghi `course_spec.yaml` trong thư mục môn; mọi trạng thái và báo cáo khác chỉ ghi vào `storage/`.
- Trạng thái: `missing`, `failed`, `blocked_tool`, `done`; `blocked_tool` không tính là `done` cho phụ thuộc.
- Mã thoát `status`: 0 mọi nhiệm vụ `done`; 1 có `failed`; 3 còn `missing` và không có `failed`; 2 chỉ còn `blocked_tool`.
- Thông báo tiếng Việt có dấu, không emoji. `yaml.safe_load`/`safe_dump`. Không gọi LLM.
- Test kín: môn giả trong `tmp_path`, không đọc `output/`; cổng được giả lập khi cần.
- Hành vi `verify` hiện có không đổi; toàn bộ test hiện có (918 passed, 3 skipped) phải đạt.

## Review Focus

1. Môn cũ có thư mục tên có dấu (`Bài đọc`, `Slide bài giảng`) phải được nhận đích đúng như tên không dấu trong đặc tả.
2. Đặc tả trỏ tới session hay lesson không có trên đĩa: các nhiệm vụ của nó là `missing`, không ném lỗi.
3. `exercises: 6` nhưng đĩa chỉ có bài 1–4: bài 5, 6 là `missing`; thư mục `tai_lieu_giang_vien` không bị nhận là bài tập.
4. `state.json` hỏng hoặc của đặc tả khác (`course_id` khác): `next` tự tính lại, không ném lỗi.
5. YAML sai (thiếu `course_id`, tài nguyên lạ, `depends_on_sessions` trỏ về sau): lỗi tiếng Việt có vị trí, mã thoát 1, không traceback.

---

## File structure

```
core/harness/course_spec.py   # CourseSpec, SessionSpec, LessonSpec; load_spec; SpecError
core/harness/planner.py       # Task; build_tasks; resolve_target
core/harness/state.py         # TaskState, StateSnapshot; compute_status; load_state; save_state; ready_tasks; status_exit_code
core/harness/spec_init.py     # draft_spec; write_spec
core/harness/cli.py           # main(argv): verify | init | plan | status | next
core/harness/__main__.py      # gọi cli.main
tests/harness/test_course_spec.py  test_planner.py  test_state.py  test_spec_init.py  test_cli_plan.py
```

---

### Task 1: Mô hình đặc tả

**Files:** Create `core/harness/course_spec.py`; Test `tests/harness/test_course_spec.py`

**Interfaces:**
- Produces:
  - `LESSON_RESOURCES = ("reading", "reading_questions", "quiz_lesson")`, `SESSION_RESOURCES = ("quiz_session", "exercises", "slide_html", "slide_pptx", "mindmap", "lab")`.
  - `LessonSpec(folder: str, title: str = "", allowed: list[str] = [], forbidden: list[str] = [], resources: list[str] | None = None)`.
  - `SessionSpec(folder: str, kind: Literal["theory","practice"] = "theory", resources: list[str] = [], exercises: int = 0, lessons: list[LessonSpec] = [], depends_on_sessions: list[int] | None = None)`.
  - `CourseSpec(course_id: str, title: str = "", tech_stack: str = "", notes: str = "", defaults: Defaults = Defaults(), sessions: list[SessionSpec])`, `Defaults(lesson_resources: list[str] = list(LESSON_RESOURCES))`. Method `lesson_resources(lesson) -> list[str]` trả `lesson.resources` hoặc mặc định.
  - `class SpecError(Exception)` với thuộc tính `messages: list[str]`.
  - `load_spec(path: Path) -> CourseSpec`: đọc YAML, kiểm, ném `SpecError` với thông báo tiếng Việt có vị trí.

- [ ] **Step 1: Test thất bại**

```python
def test_load_valid(tmp_path):
    p = write_yaml(tmp_path, VALID)            # VALID: 2 session, session 2 practice với lab + exercises: 2
    spec = load_spec(p)
    assert spec.course_id == "demo" and len(spec.sessions) == 2
    assert spec.lesson_resources(spec.sessions[0].lessons[0]) == ["reading", "reading_questions", "quiz_lesson"]

@pytest.mark.parametrize("mutate, needle", [
    (lambda d: d.pop("course_id"), "course_id"),
    (lambda d: d["sessions"][0]["resources"].append("video"), "sessions[0].resources"),
    (lambda d: d["sessions"][0]["lessons"][0].update(resources=["slide_html"]), "sessions[0].lessons[0].resources"),
    (lambda d: d["sessions"][0].update(resources=["exercises"], exercises=0), "exercises"),
    (lambda d: d["sessions"][0].update(depends_on_sessions=[1]), "depends_on_sessions"),
    (lambda d: d["sessions"][1].update(folder=d["sessions"][0]["folder"]), "trùng"),
])
def test_invalid(tmp_path, mutate, needle):
    d = copy.deepcopy(VALID); mutate(d)
    with pytest.raises(SpecError) as e:
        load_spec(write_yaml(tmp_path, d))
    assert any(needle in m for m in e.value.messages)

def test_not_yaml_mapping(tmp_path):  # tệp rỗng hoặc YAML là danh sách → SpecError
```

- [ ] **Step 2:** `python -m pytest tests/harness/test_course_spec.py -q` → FAIL (ImportError).
- [ ] **Step 3:** Cài đặt. Lỗi pydantic chuyển sang tiếng Việt, vị trí dạng `sessions[0].lessons[0].resources`; trùng tên thư mục so sau `normalize_name`.
- [ ] **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(harness): mo hinh dac ta mon course_spec`.

---

### Task 2: Bộ lập kế hoạch

**Files:** Create `core/harness/planner.py`; Test `tests/harness/test_planner.py`

**Interfaces:**
- Consumes: `CourseSpec` (Task 1), `normalize_name`.
- Produces:
  - `Task(id: str, kind: str, gate: str | None, skill: str, target: Path | None, target_hint: str, depends_on: list[str], wave: int, session_index: int, lesson_index: int | None, allowed: list[str], forbidden: list[str])` (dataclass). `kind` là tên tài nguyên (`reading`, `exercise`, ...); `gate` là kind của `GATES` hoặc `None` cho cổng "tồn tại"; `target` là đường dẫn tuyệt đối đã tìm thấy trên đĩa hoặc `None`; `target_hint` là đường dẫn mong đợi (tương đối thư mục môn) để in khi chưa có.
  - `build_tasks(spec: CourseSpec, course_dir: Path) -> list[Task]` theo bảng 4.2 của spec, id `sNN/lNN/<kind>`, `sNN/<kind>`, `sNN/exercise_<i>`; sắp theo (wave, id).
  - `resolve_target(course_dir: Path, parts: list[str], pattern: str | None = None) -> Path | None`: đi từng phần theo `normalize_name`; phần cuối có thể là mẫu (`*.pptx`, `^3_`).
- Quy tắc phụ thuộc và đợt: đúng bảng 4.2; session practice không có `depends_on_sessions` phụ thuộc session theory gần nhất đứng trước (nếu không có, không phụ thuộc). Đợt = 1 + max đợt phụ thuộc.

- [ ] **Step 1: Test thất bại** (môn giả trong `tmp_path` dựng bằng helper):
  - `test_ids_and_waves`: 1 session theory 2 lesson với mặc định + `quiz_session, exercises: 2, slide_html` → id đúng; reading đợt 1; reading_questions, quiz_lesson, quiz_session, exercise_1/2, slide_html đợt 2; `quiz_session.depends_on == ["s01/l01/reading", "s01/l02/reading"]`.
  - `test_practice_depends_on_previous_theory`: session 2 practice `lab` phụ thuộc mọi reading của session 1.
  - `test_resolve_accented_folders`: đĩa có `Lesson 01 - X/Bài đọc/reading.html` → target tìm thấy.
  - `test_missing_session_on_disk`: target `None`, `target_hint` = `Session 09 - Y/Lesson 01 - Z/Bai doc/reading.html`.
  - `test_exercise_folder_match`: đĩa có `Bai tap/1_a`, `Bai tap/2_b`, `Bai tap/tai_lieu_giang_vien` với `exercises: 3` → exercise_3 target `None`, exercise_1 target `.../1_a`.
  - `test_pptx_first_file`: `Slide bai giang/b.pptx`, `a.pptx` → `a.pptx`; bỏ qua `~$a.pptx`.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(harness): lap ke hoach nhiem vu theo dot tu dac ta mon`.

---

### Task 3: Trạng thái

**Files:** Create `core/harness/state.py`; Test `tests/harness/test_state.py`

**Interfaces:**
- Consumes: `load_spec`, `build_tasks`, `verify_path(target, VerifyOptions)` (`core/harness/verify.py`), `Report.exit_code`, `GateResult.findings`.
- Produces:
  - `TaskState(id, kind, status: Literal["missing","failed","blocked_tool","done"], target: str, target_hint: str, wave: int, depends_on: list[str], errors: int, warnings: int, first_error: str, checked_at: str)`.
  - `StateSnapshot(course_id: str, spec_path: str, updated_at: str, runtime: bool, tasks: dict[str, TaskState])` với `to_json()/from_json()`.
  - `STATE_ROOT = <repo>/storage/harness`; `state_path(course_id) -> Path` = `STATE_ROOT / course_id / "state.json"`.
  - `compute_status(spec_path: Path, runtime: bool = False, verify=verify_path) -> StateSnapshot` (tham số `verify` để test giả lập): target `None` hoặc tệp rỗng → `missing`; gate `None` → `done` nếu tồn tại và không rỗng; ngược lại gọi `verify(target, VerifyOptions(kind=gate, runtime=runtime and gate in {"exercise", "slide_html"}))` và ánh xạ exit 0/1/2 → done/failed/blocked_tool; `first_error` = message của finding error đầu tiên. Ngoại lệ trong `verify` → `failed` với message.
  - `save_state(snap) -> Path`, `load_state(course_id) -> StateSnapshot | None` (tệp hỏng → None).
  - `ready_tasks(snap) -> list[TaskState]`: không `done` và mọi phụ thuộc `done`, sắp (wave, id).
  - `status_exit_code(snap) -> int` theo Global Constraints.
  - `TASK_SKILL` lấy từ `Task.skill` (đã có ở Task 2), lưu thêm vào `TaskState` dưới trường `skill: str`.

- [ ] **Step 1: Test thất bại** (verify giả lập trả `Report` có exit code chỉ định theo id):
  - ánh xạ 4 trạng thái; `blocked_tool` không mở khóa phụ thuộc; `ready_tasks` thứ tự đúng.
  - `status_exit_code`: mọi done → 0; một failed → 1; chỉ missing → 3; chỉ blocked_tool (còn lại done) → 2; missing + blocked_tool → 3.
  - `save_state`/`load_state` khứ hồi (monkeypatch `STATE_ROOT` vào `tmp_path`); tệp hỏng → None.
  - verify ném `RuntimeError` → `failed`, `first_error` chứa thông điệp.
  - `runtime=True` chỉ bật runtime cho exercise và slide_html (kiểm `VerifyOptions` mà verify giả nhận).
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(harness): tinh trang thai nhiem vu tu ket qua verify`.

---

### Task 4: Dựng đặc tả nháp

**Files:** Create `core/harness/spec_init.py`; Test `tests/harness/test_spec_init.py`

**Interfaces:**
- Consumes: `normalize_name`, `CourseSpec`, `load_spec`, `build_tasks`.
- Produces: `draft_spec(course_dir: Path) -> dict` theo quy tắc `init` ở spec 4.4; `write_spec(course_dir: Path, force: bool = False) -> Path` (ghi `course_dir / "course_spec.yaml"`, `allow_unicode=True`, `sort_keys=False`; tồn tại mà không `force` → `FileExistsError`).
- Suy ra tài nguyên: lesson có `Bai doc/` → `reading`; `Cau hoi bai doc/` → `reading_questions`; `Quizz lesson/` → `quiz_lesson`; nếu tập của lesson khác mặc định thì ghi `resources` cho lesson đó. Session: `Quizz session/` → `quiz_session`; `Bai tap/` có thư mục `^\d+_` → `exercises` với `exercises` = số lớn nhất; `Bai giang tren lop/slides.html` → `slide_html`; `Slide bai giang/*.pptx` → `slide_pptx`; `So do tu duy/mindmap.md` → `mindmap`; `Bai thuc hanh/lab_guide.md` → `lab` và `kind: practice`.
- Session sắp theo tên đã chuẩn hóa; lesson cũng vậy.

- [ ] **Step 1: Test thất bại**: dựng môn giả 2 session (một theory đủ loại, một practice có lab và 2 bài tập, một lesson thiếu quiz) → `draft_spec` đúng từng trường; `write_spec` rồi `load_spec` không lỗi và `build_tasks` mọi target khác `None`; ghi lần hai không `force` → `FileExistsError`; tên có dấu (`Bài đọc`) vẫn nhận.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(harness): dung dac ta mon nhap tu thu muc co san`.

---

### Task 5: CLI và tài liệu

**Files:** Create `core/harness/cli.py`; Modify `core/harness/__main__.py`, `core/harness/verify.py` (chuyển phần phân tích tham số sang cli, giữ `verify.main` là alias gọi `cli.main(["verify", ...])` để test cũ đạt), `docs/harness.md`, `.agents/AGENTS.md` (mục 9: thêm 3 dòng về `init/status/next`); Test `tests/harness/test_cli_plan.py`

**Interfaces:**
- Consumes: Task 1–4, `verify.verify_path`, `report_io`.
- Produces: `cli.main(argv: list[str] | None = None) -> int` với lệnh con `verify` (y nguyên hành vi cũ), `init <dir> [--force]`, `plan <spec> [--json]`, `status <spec> [--runtime] [--json]`, `next <spec> [--limit N] [--json]` theo spec 4.4. `next` chạy `compute_status` khi `load_state` trả None, `course_id` khác, hoặc mtime đặc tả mới hơn `updated_at`. `SpecError` → in từng thông báo ra stderr, mã 1, không traceback. stdout UTF-8 như `verify`.

- [ ] **Step 1: Test thất bại** (môn giả + verify giả lập qua monkeypatch `state.verify_path` hoặc tham số):
  - `init` ghi tệp, in đường dẫn, mã 0; lần hai mã 1 với thông báo dùng `--force`.
  - `plan --json` trả danh sách có `id`, `wave`, `depends_on`.
  - `status` mã 3 khi còn missing; `--json` có `counts`.
  - `next --limit 1 --json` trả đúng 1 khối có `skill` = `skills/<tên>/SKILL.md`, `verify_command` chứa `--kind`.
  - Đặc tả hỏng → mã 1, stderr có vị trí, không `Traceback`.
  - Toàn bộ `tests/harness/test_cli.py` cũ vẫn đạt.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt; cập nhật `docs/harness.md` (mục mới "Đặc tả môn và lập lịch": định dạng YAML, bảng tài nguyên, bốn lệnh, mã thoát của `status`) và `.agents/AGENTS.md`.
- [ ] **Step 4:** PASS; `python -m pytest -q` toàn bộ.
- [ ] **Step 5 (kiểm thủ công):** `init` trên bản sao của `output/pms/nodejs_ai_driven` và `reactjs_ai_driven` — KHÔNG ghi vào `output/`: chép thư mục môn sang thư mục tạm ngoài repo (bỏ `node_modules`), chạy `init`, `status`, `next` trên bản sao; mong đợi mọi nhiệm vụ có cổng `done`, mã thoát 0. Ghi số nhiệm vụ và thời gian vào thân commit.
- [ ] **Step 6:** Commit `feat(harness): lenh init, plan, status, next cho dac ta mon`.

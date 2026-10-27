# Harness Verify (cổng kiểm chứng) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Một lệnh `python -m core.harness verify <path>` nhận diện từng tài nguyên học liệu, chạy đúng cổng kiểm chứng, ghi báo cáo JSON/Markdown và trả mã thoát 0/1/2, dùng chung cho agent trong IDE và pipeline.

**Architecture:** Gói mới `core/harness/` gồm mô hình kết quả, bộ nhận diện loại, các cổng (mỗi loại một module trong `gates/`) và các bộ chạy thật (`runners/`). Cổng gọi lại validator và script đã có (`core/validators/reading_validator.py`, `skills/*/scripts/*.py`) thay vì viết lại; quy tắc văn bản gom về `text_rules.py`. Phần chạy thật chỉ bật khi có `--runtime`/`--render`.

**Tech Stack:** Python 3.10, pytest, BeautifulSoup, openpyxl, python-pptx, Playwright (tùy chọn, có Chrome hệ thống làm dự phòng), Node + Vitest (tùy chọn), mysqld 8 (tùy chọn).

**Spec:** `docs/superpowers/specs/2026-10-27-harness-design.md`

## Global Constraints

- Không hardcode tên môn, tên session hay công nghệ; mọi nhận diện dựa vào cấu trúc thư mục và nội dung tệp.
- So khớp tên thư mục sau khi bỏ dấu tiếng Việt và `casefold()`.
- Mã thoát: `0` không lỗi; `1` có lỗi; `2` không lỗi nhưng có cổng `skipped` vì thiếu công cụ.
- Báo cáo mặc định ghi vào `storage/harness_reports/<YYYYmmdd-HHMMSS>_<tên đích bỏ dấu>/report.json` và `report.md`. Không ghi gì vào thư mục tài nguyên được kiểm.
- MySQL tạm: `mysqld --initialize-insecure`, `--bind-address=127.0.0.1`, cổng trống khác 3306, không tạo user, xóa thư mục dữ liệu sau khi chạy.
- Không gọi LLM. Không đổi `core/validators/*` hay `quality_gates.py`.
- Thông điệp `Finding.message` bằng tiếng Việt có dấu; không emoji.
- Test không mở mạng, không cần Node/mysqld/Chrome: phần chạy thật được test bằng cách giả lập `subprocess`/Playwright; một test tích hợp đánh dấu `@pytest.mark.integration`.

## Review Focus

1. Thư mục môn cũ có tên có dấu (`Slide bài giảng/`, `Bài đọc/`) phải được nhận diện như tên không dấu.
2. Thiếu Playwright/Chrome/Node/mysqld phải ra `skipped` + mã 2, không bao giờ ra `pass`.
3. Thư mục `Bai tap/tai_lieu_giang_vien/` và `node_modules/` không được nhận nhầm là bài tập hay bị duyệt vào.
4. Quiz xlsx có tiêu đề cột đúng nhưng số dòng câu hoặc đáp án lệch với `.md` phải là lỗi, không phải cảnh báo.
5. Starter bài tập chạy pass 100% test là lỗi (đề không còn gì để làm); starter không chạy được (lỗi cú pháp, thiếu module) cũng là lỗi.

---

## File structure

```
core/harness/
  __init__.py          # xuất verify_path, Report
  __main__.py          # CLI
  findings.py          # Finding, GateResult, Report
  text_rules.py        # từ cấm, emoji, thẻ ngoặc vuông, chữ in hoa
  registry.py          # normalize_name, detect_kind, discover
  report_io.py         # write_report
  verify.py            # verify_path: discover -> gate -> Report
  gates/__init__.py    # GATES: dict[str, Callable[[Path, VerifyOptions], GateResult]]
  gates/reading.py
  gates/quiz.py        # quiz_lesson, quiz_session
  gates/exercise.py
  gates/lab.py
  gates/slide_pptx.py
  gates/slide_html.py
  runners/__init__.py
  runners/tooling.py   # find_chrome, which_node, find_mysqld
  runners/browser.py   # launch_browser, run_tests_html, measure_slides
  runners/vitest.py    # NodeWorkspace, run_vitest
  runners/mysql_sandbox.py  # MySQLSandbox (context manager)
tests/harness/
  conftest.py          # fixture course_tree (dựng cây thư mục nhỏ trong tmp_path)
  test_findings.py  test_text_rules.py  test_registry.py
  test_gate_reading.py  test_gate_quiz.py  test_gate_exercise.py  test_gate_lab.py
  test_gate_slide_pptx.py  test_gate_slide_html.py
  test_runners.py  test_cli.py
```

`VerifyOptions` (dataclass trong `verify.py`): `runtime: bool = False`, `render: bool = False`, `kind: str | None = None`.

---

### Task 1: Mô hình kết quả và quy tắc văn bản

**Files:**
- Create: `core/harness/__init__.py`, `core/harness/findings.py`, `core/harness/text_rules.py`
- Test: `tests/harness/test_findings.py`, `tests/harness/test_text_rules.py`

**Interfaces:**
- Produces:
  - `Finding(severity: Literal["error","warning","info"], gate: str, message: str, location: str = "")` (dataclass, frozen).
  - `GateResult(kind: str, path: str, gate: str, findings: list[Finding], skipped_reason: str = "", duration_s: float = 0.0, detail: dict = {})` với property `status -> "pass"|"fail"|"skipped"` (`fail` nếu có error; ngược lại `skipped` nếu `skipped_reason`; ngược lại `pass`).
  - `Report(target: str, results: list[GateResult], started_at: str)` với `exit_code -> int`, `to_dict() -> dict`, `to_json() -> str`, `to_markdown() -> str`, `counts() -> dict[str, int]` (khóa `pass`, `fail`, `skipped`).
  - `text_rules.BANNED_WORDS: tuple[str, ...]` (hợp của danh sách trong `check_slides_html.py` và `check_reading.py`), `EMOJI_RE`, `BRACKET_TAG_RE` (lấy từ `deck_lint.BRACKET_TAG`), `find_banned_words(text) -> list[str]`, `find_emoji(text) -> list[str]`, `find_bracket_tags(text) -> list[str]`, `find_all_caps(text, min_letters=10) -> list[str]`.

- [ ] **Step 1: Viết test thất bại**

```python
def test_status_and_exit_code():
    ok = GateResult("reading", "a.html", "reading", [])
    warn = GateResult("reading", "b.html", "reading", [Finding("warning", "reading", "x")])
    bad = GateResult("quiz_lesson", "q.md", "quiz", [Finding("error", "quiz", "thiếu đáp án")])
    skip = GateResult("slide_html", "s.html", "slide_html", [], skipped_reason="Thiếu Playwright")
    assert (ok.status, warn.status, bad.status, skip.status) == ("pass", "pass", "fail", "skipped")
    assert Report("t", [ok, warn], "2026-10-27T00:00:00").exit_code == 0
    assert Report("t", [ok, skip], "…").exit_code == 2
    assert Report("t", [skip, bad], "…").exit_code == 1
    assert Report("t", [], "…").exit_code == 0

def test_markdown_lists_failures_first():
    md = Report("t", [ok_result(), fail_result()], "…").to_markdown()
    assert md.index("fail") < md.index("pass")

def test_text_rules():
    assert set(find_banned_words("Bí kíp thực chiến nhé")) == {"nhé", "thực chiến", "bí kíp"}
    assert find_emoji("Xong ✅") == ["✅"]
    assert find_bracket_tags("[NOTE] và [userId]") == ["[NOTE]"]
    assert find_all_caps("API CRUD là gì") == []
    assert find_all_caps("CẢNH BÁO QUAN TRỌNG") != []
```

(`find_banned_words` không phân biệt hoa thường.)

- [ ] **Step 2:** `pytest tests/harness/test_findings.py tests/harness/test_text_rules.py -v` → FAIL (ImportError).
- [ ] **Step 3:** Cài đặt hai module. `to_markdown` có tiêu đề, bảng đếm, rồi từng kết quả (fail trước, skipped, pass), mỗi finding một dòng `- [error] message (location)`.
- [ ] **Step 4:** Chạy lại → PASS.
- [ ] **Step 5:** Commit `feat(harness): mo hinh ket qua va quy tac van ban dung chung`.

---

### Task 2: Nhận diện loại tài nguyên

**Files:**
- Create: `core/harness/registry.py`, `tests/harness/conftest.py`
- Test: `tests/harness/test_registry.py`

**Interfaces:**
- Produces:
  - `normalize_name(name: str) -> str`: bỏ dấu (NFD, bỏ dấu kết hợp, `đ`→`d`), `casefold()`.
  - `detect_kind(path: Path) -> str | None` trả một trong `reading, slide_pptx, slide_html, quiz_lesson, quiz_session, exercise, lab` theo bảng ở spec 4.2. Bài tập là **thư mục** khớp `^\d+_` nằm trong `Bai tap/`; các loại khác là **tệp**.
  - `discover(root: Path) -> tuple[list[tuple[str, Path]], list[Path]]`: (đích có kind, tệp không nhận diện được). Bỏ qua `node_modules`, `.git`, `screenshots`, `tai_lieu_giang_vien`, và mọi thứ bên trong một thư mục bài tập (bài tập được kiểm như một đơn vị). Quiz lesson và quiz session: mỗi thư mục quiz là **một** đích (đường dẫn thư mục), không phải từng tệp. `reading.md` cạnh `reading.html` không phải đích riêng.
  - Fixture `course_tree(tmp_path) -> Path`: dựng một môn giả nhỏ có đủ 7 loại, một thư mục tên có dấu `Slide bài giảng/`, một `node_modules/x/reading.html` và `Bai tap/tai_lieu_giang_vien/dap_an_mau/bai_1/`.

- [ ] **Step 1: Viết test thất bại**

```python
def test_normalize():
    assert normalize_name("Slide bài giảng") == "slide bai giang"
    assert normalize_name("Bài Đọc") == "bai doc"

def test_discover(course_tree):
    found, unknown = discover(course_tree)
    kinds = sorted(k for k, _ in found)
    assert kinds == ["exercise", "lab", "quiz_lesson", "quiz_session", "reading", "slide_html", "slide_pptx"]
    assert not any("node_modules" in str(p) or "tai_lieu_giang_vien" in str(p) for _, p in found)
    assert any(p.name == "README.md" for p in unknown)

def test_detect_kind_on_single_file(course_tree):
    html = next(course_tree.rglob("reading.html"))
    assert detect_kind(html) == "reading"
```

- [ ] **Step 2:** Chạy → FAIL. **Step 3:** Cài đặt. **Step 4:** Chạy → PASS.
- [ ] **Step 5:** Commit `feat(harness): nhan dien loai tai nguyen theo cau truc thu muc`.

---

### Task 3: Cổng bài đọc

**Files:**
- Create: `core/harness/gates/__init__.py`, `core/harness/gates/reading.py`
- Modify: `skills/reading_generator/scripts/check_reading.py` (chuyển `extra_checks` sang dùng `text_rules`, giữ nguyên CLI)
- Test: `tests/harness/test_gate_reading.py`

**Interfaces:**
- Consumes: `validate_reading_material(content, metadata)` từ `core/validators/reading_validator.py`; `extra_checks(html) -> (errors, warnings)` từ `skills/reading_generator/scripts/check_reading.py` (nạp bằng `importlib.util.spec_from_file_location`, không thêm `skills/` vào `sys.path`).
- Produces: `check_reading(path: Path, opts) -> GateResult`; `GATES["reading"] = check_reading`.

Cổng gọi validator với cùng metadata mà `check_reading.py main()` đang dùng (`enforce_word_budget=True`). Lỗi validator → `error`; `extra_checks` errors → `error`, warnings → `warning`. `detail["word_count"] = count_visible_words(html)`.

- [ ] **Step 1: Test thất bại**: một bài đọc mẫu đạt chuẩn (lấy nhỏ nhất có thể từ fixture, hoặc dựng HTML đủ `section-1..5` và 1.500–2.000 từ) → `status == "pass"`; cùng bài thêm `<a href="#">` và `✅` → `fail`, có finding chứa `href="#"` và một finding emoji; tệp rỗng → `fail`.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt, rồi sửa `check_reading.py` để dùng `text_rules`. **Step 4:** PASS, và `python skills/reading_generator/scripts/check_reading.py <một reading.html của nodejs_ai_driven>` vẫn trả mã 0 như trước.
- [ ] **Step 5:** Commit `feat(harness): cong bai doc`.

---

### Task 4: Cổng quiz lesson và quiz session

**Files:**
- Create: `core/harness/gates/quiz.py`
- Test: `tests/harness/test_gate_quiz.py`

**Interfaces:**
- Produces:
  - `parse_quiz_md(text: str) -> list[QuizQuestion]` với `QuizQuestion(number: int, tag: str, options: dict[str, str], answer: str, has_explanation: bool, has_feedback: bool)`. Câu bắt đầu bằng `### Câu N (TAG)`; phương án là dòng `A. `…`D. `; đáp án từ `**Đáp án đúng:** X`.
  - `check_quiz_lesson(path: Path, opts) -> GateResult`, `check_quiz_session(path: Path, opts) -> GateResult`; đăng ký trong `GATES`.
- Giá trị pin từ spec:
  - Lesson: đúng 5 câu; `tag ∈ {SYNTAX, EXECUTION_FLOW, CODE_TRACE, COMPARISON, TRAP_PREDICTION}`; 4 phương án; có `**Giải thích:**` và `**Phản hồi khi chọn sai:**`. xlsx: sheet `Template Import Quiz`, hàng 1 đúng 16 tiêu đề `question_content, type, points, answer_1..answer_6, right_1..right_6, isCorrect`; số hàng dữ liệu = số câu md; phương án đúng trong xlsx khớp đáp án md theo thứ tự.
  - Session: đúng 45 câu; tag tự do (tên lesson); 4 phương án; có đáp án. xlsx: sheet `Quiz Bank`, 13 tiêu đề `STT, question_content, answer_1, explanation_answer, answer_2, explanation_answer, answer_3, explanation_answer, answer_4, explanation_answer, isCorrect, difficulty, category`; 45 hàng dữ liệu; `isCorrect` khớp đáp án md.
  - Thiếu tệp md hoặc xlsx trong thư mục quiz → `error`.
- Trước khi cài đặt, mở một xlsx thật của `nodejs_ai_driven` để xác định cách `isCorrect` / `right_N` biểu diễn đáp án đúng; ghi cách đó vào docstring và test.

- [ ] **Step 1: Test thất bại** (dựng md/xlsx nhỏ bằng openpyxl trong `tmp_path`): bộ lesson đúng → pass; thiếu `**Phản hồi khi chọn sai:**` ở câu 3 → error có `Câu 3`; tag `SYNTAXX` → error; xlsx 4 hàng khi md 5 câu → error; xlsx đáp án câu 2 khác md → error có `Câu 2`; session 44 câu → error có `45`.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS; chạy cổng trên mọi thư mục quiz của `output/pms/nodejs_ai_driven` và `reactjs_ai_driven` bằng một lệnh Python ngắn → không có lỗi (đây là dữ liệu đã duyệt; nếu có lỗi, sửa cổng trừ khi lỗi là thật thì báo lại).
- [ ] **Step 5:** Commit `feat(harness): cong quiz lesson va quiz session`.

---

### Task 5: Cổng lab và cổng bài tập (tĩnh)

**Files:**
- Create: `core/harness/gates/lab.py`, `core/harness/gates/exercise.py`
- Test: `tests/harness/test_gate_lab.py`, `tests/harness/test_gate_exercise.py`

**Interfaces:**
- Produces: `check_lab(path, opts) -> GateResult`; `check_exercise(path, opts) -> GateResult` (tĩnh khi `opts.runtime` là False); `exercise_number(path: Path) -> int` (số đầu tên thư mục); `solution_dir(path: Path) -> Path` = `path.parent / "tai_lieu_giang_vien" / "dap_an_mau" / f"bai_{n}"`.
- Lab: có ít nhất một `## Lab N - … (K phút)`; có `## Tổng kết` và `## Rubric` (so khớp bỏ dấu, tiền tố); mỗi mục Lab có ít nhất một "Kết quả mong đợi" → thiếu là `error`; tổng phút các Lab ghi vào `detail["minutes"]`.
- Bài tập tĩnh: có `de_bai_bai_tap.md`, `tieu_chi_cham_diem_ai.md`, `starter/` không rỗng; `de_bai_bai_tap.md` có đúng 5 tiêu đề `### ` và 350–700 từ (đếm từ ngoài khối mã; ngoài khoảng là `warning`); `solution_dir` tồn tại và không rỗng; `tai_lieu_giang_vien/huong_dan_bai_{n}.md` tồn tại; `text_rules` trên đề bài (từ cấm, emoji → `error`).

- [ ] **Step 1: Test thất bại**: lab đủ → pass; lab có Lab 2 thiếu "Kết quả mong đợi" → error có `Lab 2`; bài tập đủ → pass; thiếu `tieu_chi_cham_diem_ai.md` → error; thiếu `dap_an_mau/bai_3` → error; đề 4 tiêu đề H3 → error; đề 900 từ → warning.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS; chạy trên 12 bài tập và 2 lab của hai môn đã duyệt → không lỗi.
- [ ] **Step 5:** Commit `feat(harness): cong lab va cong bai tap tinh`.

---

### Task 6: Cổng slide pptx và slide html (tĩnh)

**Files:**
- Create: `core/harness/gates/slide_pptx.py`, `core/harness/gates/slide_html.py`
- Modify: `skills/slide_html/scripts/check_slides_html.py` (lấy `BANNED_WORDS`, `EMOJI` từ `text_rules`)
- Test: `tests/harness/test_gate_slide_pptx.py`, `tests/harness/test_gate_slide_html.py`

**Interfaces:**
- Consumes: `deck_lint.lint_slides`, `deck_lint.load_slides`, `check_deck.static_checks(pptx_path) -> dict`, `check_deck.render_with_powerpoint`, `check_deck.measured_checks` (nạp bằng `spec_from_file_location`). Đọc trả về của `static_checks` trước khi ánh xạ; các khóa lỗi → `error`, cảnh báo → `warning`.
- Produces: `check_slide_pptx(path, opts) -> GateResult`, `check_slide_html(path, opts) -> GateResult`, `static_html_findings(html: str) -> list[Finding]`.
- slide_pptx: nếu có `slides.json` cùng thư mục thì chạy `lint_slides`. `opts.render` trên máy không phải Windows hoặc không có PowerPoint → thêm `skipped_reason` (không xóa lỗi tĩnh).
- slide_html tĩnh: token phong cách cấm (`BANNED_STYLE` của `check_slides_html.py`), emoji, `{{ name }}` ngoài `<pre>/<code>`, `href="#"`, từ cấm → `error`. Phần đo vừa khung để Task 7.

- [ ] **Step 1: Test thất bại**: pptx dựng bằng python-pptx 2 slide sạch → pass; `slides.json` có 6 bullet ở một slide → error (giới hạn 5 của engine); html có `backdrop-filter` → error; html có `style={{ color }}` trong `<pre>` → không lỗi; `opts.render=True` khi `sys.platform != "win32"` (monkeypatch) → `skipped_reason` khác rỗng.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS; `check_slides_html.py` vẫn chạy được như cũ.
- [ ] **Step 5:** Commit `feat(harness): cong slide pptx va slide html tinh`.

---

### Task 7: Bộ chạy thật

**Files:**
- Create: `core/harness/runners/__init__.py`, `tooling.py`, `browser.py`, `vitest.py`, `mysql_sandbox.py`
- Modify: `core/harness/gates/slide_html.py`, `core/harness/gates/exercise.py`
- Test: `tests/harness/test_runners.py`

**Interfaces:**
- Produces:
  - `tooling.find_chrome() -> str | None` (danh sách đường dẫn như `_SYSTEM_CHROME_PATHS` trong `agents/lecture_ui_reviewer_agent.py`), `tooling.which(name) -> str | None`, `tooling.find_mysqld() -> str | None` (PATH, rồi `C:\Program Files\MySQL\MySQL Server *\bin\mysqld.exe`), `tooling.free_port(exclude={3306}) -> int`.
  - `browser.launch_browser(playwright)` (Chromium của Playwright, dự phòng Chrome hệ thống), `browser.measure_slides(html: Path, viewports=[(1366,768),(1920,1080),(1280,720)]) -> dict` với khóa `slide_overflow: list[{slide, viewport, over_px, state}]`, `console_errors: list[str]`; `browser.run_tests_html(html: Path) -> dict` `{passed, total, results}` (gọi `window.report()` rồi đợi `window.__results.done`, quá 30 s là lỗi). Thiếu Playwright/Chrome → `raise ToolUnavailable(reason)`.
  - `vitest.NodeWorkspace(cache_root: Path)` với `prepare(package_json: Path) -> Path` (thư mục có `node_modules`, khóa bằng sha1 của `dependencies`+`devDependencies` đã sắp xếp; `npm install` một lần), `vitest.run_vitest(project: Path, workspace: Path, env: dict | None = None) -> dict` `{passed, failed, total, ok}` (chép dự án sang thư mục tạm cạnh workspace, chạy `npx vitest run --reporter=json`, đọc JSON).
  - `mysql_sandbox.MySQLSandbox()` context manager: `__enter__` trả `{"host": "127.0.0.1", "port": p, "user": "root", "password": ""}`; `__exit__` tắt tiến trình và xóa datadir.
  - `ToolUnavailable(Exception)` trong `runners/__init__.py`.
- Nối vào cổng:
  - slide_html với `opts.runtime`: `measure_slides`; mỗi overflow > 2 px → `error` có số slide và viewport; lỗi console → `error`; `ToolUnavailable` → `skipped_reason`.
  - exercise với `opts.runtime`: chọn runner theo spec 4.2 (`package.json` có `vitest` → Vitest; có `db/*.sql` hoặc `DB_` trong `.env.example` → bọc trong `MySQLSandbox` và truyền `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD`; có `tests.html` + `harness.js` → `run_tests_html`). Đáp án mẫu phải `passed == total > 0`; starter phải chạy được (`total > 0`) và `passed < total`. Không runner nào khớp → `skipped_reason="Không có bộ test chạy được"`.
  - Cache workspace Node: `storage/harness_cache/node_ws/`.

- [ ] **Step 1: Test thất bại** (giả lập, không cần công cụ thật):
  - `free_port()` không bao giờ trả 3306 (monkeypatch socket để cổng đầu tiên là 3306).
  - `NodeWorkspace` hai `package.json` cùng dependency khác thứ tự → cùng khóa; `subprocess.run` bị monkeypatch, `npm install` chỉ gọi một lần.
  - `run_vitest` đọc một JSON Vitest mẫu (`numPassedTests`, `numFailedTests`, `numTotalTests`) → đúng dict.
  - Cổng exercise `runtime=True` với runner giả: đáp án 10/10, starter 10/10 → error "starter đã đạt hết"; starter 0 test (crash) → error; đáp án 9/10 → error; `ToolUnavailable` → `status == "skipped"`.
  - Cổng slide_html `runtime=True` với `measure_slides` giả trả một overflow → error có `slide 4` và `1366x768`.
  - Một test `@pytest.mark.integration`: chạy cổng exercise `runtime=True` trên bài 1 của `nodejs_ai_driven` Session 01 (skip nếu thiếu node hoặc mysqld hoặc thư mục output).
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS; chạy thủ công test integration một lần trên máy này và ghi kết quả vào mô tả commit.
- [ ] **Step 5:** Commit `feat(harness): bo chay that vitest, mysql tam va trinh duyet`.

---

### Task 8: verify_path, ghi báo cáo, CLI

**Files:**
- Create: `core/harness/verify.py`, `core/harness/report_io.py`, `core/harness/__main__.py`
- Modify: `core/harness/__init__.py`
- Test: `tests/harness/test_cli.py`

**Interfaces:**
- Consumes: `discover`, `detect_kind`, `GATES`, `Report`.
- Produces:
  - `verify_path(target: Path, opts: VerifyOptions) -> Report`: tệp/thư mục một tài nguyên → một kết quả (dùng `opts.kind` nếu có, ngược lại `detect_kind`; không nhận diện được → một `GateResult` kind `unknown` có `error` "Không nhận diện được loại tài nguyên, dùng --kind"); thư mục lớn hơn → `discover` rồi chạy từng đích; tệp không nhận diện → một `GateResult` kind `unknown` chỉ có `info`. Ngoại lệ trong một cổng → `error` "Cổng lỗi: <ngoại lệ>" cho đích đó, không dừng cả lần chạy. Đo `duration_s` cho từng cổng.
  - `write_report(report: Report, report_dir: Path | None = None) -> Path` (trả thư mục đã ghi).
  - `main(argv: list[str] | None = None) -> int` cho `python -m core.harness verify …` với cờ ở spec 4.1. Mặc định in bảng tóm tắt (số pass/fail/skipped và các finding error) và đường dẫn báo cáo; `--json` in `report.to_json()`.
- `--report-dir` cho phép test ghi vào `tmp_path`.

- [ ] **Step 1: Test thất bại**:
  - `main(["verify", str(course_tree), "--report-dir", str(tmp)])` → trả 0 với cây mẫu sạch; `tmp/report.json` có `results` đủ 7 kind và `report.md` tồn tại.
  - Làm hỏng quiz lesson trong cây → trả 1.
  - `--kind reading` trên một tệp `.txt` → dùng cổng reading.
  - Cổng giả ném `RuntimeError` → trả 1, các đích khác vẫn có kết quả.
  - Đường dẫn không tồn tại → trả 1 và thông báo rõ, không traceback.
- [ ] **Step 2:** FAIL. **Step 3:** Cài đặt. **Step 4:** PASS. Chạy `python -m core.harness verify "output/pms/nodejs_ai_driven"` và `…/reactjs_ai_driven` (tĩnh) → mã 0; ghi số đích và thời gian vào commit.
- [ ] **Step 5:** Commit `feat(harness): lenh verify va bao cao`.

---

### Task 9: Nối vào quy trình agent

**Files:**
- Modify: `AGENTS.md`, `skills/reading_generator/SKILL.md`, `skills/slide_html/SKILL.md`, `skills/slide_deck/SKILL.md`, `skills/quiz_generator/SKILL.md`, `skills/lab_generator/SKILL.md`, `skills/exercise_generator/SKILL.md`
- Create: `docs/harness.md`
- Test: `pytest tests/harness -q` và toàn bộ `pytest -q`

- [ ] **Step 1:** `AGENTS.md`: thêm mục "Cổng kiểm chứng": một tài nguyên chỉ được báo xong khi `python -m core.harness verify <thư mục>` trả 0; mã 2 phải nêu công cụ thiếu; bài tập cần thêm `--runtime`.
- [ ] **Step 2:** Mỗi SKILL.md liệt kê ở trên: thêm một dòng vào mục kiểm tra cuối, trỏ đến lệnh `verify` với `--kind` tương ứng (giữ nguyên các lệnh script cũ).
- [ ] **Step 3:** `docs/harness.md`: cách dùng, bảng kind, mã thoát, chỗ ghi báo cáo, công cụ tùy chọn và cách cài.
- [ ] **Step 4:** `pytest -q` toàn bộ: số test cũ (khoảng 684) vẫn đạt, cộng test mới.
- [ ] **Step 5:** Commit `docs(harness): bat buoc cong kiem chung trong AGENTS va cac skill`.

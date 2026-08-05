---
name: lessons_learned
description: System Reflection Memory Store containing consolidated technical guardrails, gotchas, and error-prevention directives derived from prior AI Agent iterations and Reviewer feedback logs. Target output language is 100% Accented Vietnamese.
---

# Lessons Learned & Technical Guardrails Memory Store — Rikkei Education Standards

This file serves as the system's **Long-Term Reflection Memory Store**. All AI Agents MUST read these accumulated technical guardrails before generating or reviewing learning materials to prevent regression and avoid repeating past technical mistakes.

---

## 1. Operating System & Environment Guardrails

- **[WINDOWS UTF-8 ENCODING]**:
  - Always reconfigure standard I/O encoding when processing Vietnamese text on Windows:
    ```python
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    ```
  - Prevents `UnicodeEncodeError` crashes caused by default Windows `CP1252` encoding.
  - Set `PYTHONIOENCODING=utf-8` environment variable for subprocess executions.

- **[VIRTUAL ENVIRONMENT DETECTION]**:
  - Use `sys.prefix != sys.base_prefix` to detect active virtual environment (`venv`) status accurately.

---

## 2. Python Core & Language Gotchas

- **[MUTABLE DEFAULT ARGUMENTS]**:
  - FORBIDDEN to define functions with mutable default arguments (`def func(lst=[])`). Use `def func(lst=None)` with `if lst is None: lst = []`.

- **[MULTILINE STRING LITERALS]**:
  - Always use triple quotes (`"""` or `'''`) for multiline strings instead of trailing backslashes `\` to avoid `SyntaxError: unterminated string literal`.

- **[JSON CODE EXTRACTION & PARSING]**:
  - When extracting Python code snippets from JSON fields, ALWAYS use proper JSON parsers (`json.loads`) or regex filters to strip trailing delimiters (e.g. `",` at end of lines) that cause `SyntaxError: unterminated string literal`.

- **[SHORT-CIRCUIT EVALUATION TRAPS]**:
  - In boolean expression quizzes (`and`, `or`), ensure zero-division risk expressions (`10 / x`) are guarded properly (`x != 0 and (10 / x > 1)`).

---

## 3. Web Frameworks & Database ORM (Backend APIs & Data Persistence)

- **[TRANSACTION ROLLBACK ON INTEGRITY ERROR]**:
  - When catching database exceptions in Web APIs, ALWAYS execute `db.rollback()` inside database `IntegrityError` / transaction exception handlers before returning error responses to release failed transactions.

- **[DEPENDENCY INJECTION & ASYNC SESSIONS]**:
  - In web frameworks, always inject database sessions properly using dependencies or context managers (`db: AsyncSession = Depends(get_db)`).

- **[PYDANTIC SCHEMA VALIDATION]**:
  - Input schema fields representing lists MUST declare validation bounds (e.g. `Field(..., min_items=1)` for quiz items).
  - Practical lab schemas MUST define explicit sub-schemas for `objectives`, `steps`, and `checklist`.

- **[STRICT SCOPE BOUNDARY CONTROL]**:
  - FORBIDDEN to introduce future framework/ORM concepts (`APIRouter`, `SQLAlchemy`, `FastAPI`, `Pydantic`) inside foundational `python/core` lessons.

---

## 4. Interactive DOM Visualizers & Wasm Sandbox

- **[NON-BLOCKING WASM EXECUTIONS]**:
  - CLI lessons containing `input()` MUST use mock datasets or input stubs (`unittest.mock.patch`) in testing environments to prevent `TimeoutExpired` sandbox freezes.

- **[DOM ELEMENT ID SYNCHRONIZATION]**:
  - HTML container IDs (`id="custom-input"`) MUST strictly match JavaScript dereferencing selectors (`document.getElementById("custom-input")`).

- **[RAW OPERATORS IN CONSOLE LOGS]**:
  - When logging to terminal visualizers via `innerText`, pass raw boolean string operators (e.g. `&&`) rather than HTML entities (`&amp;&amp;`).

- **[COPY BUTTON EVENT BINDING]**:
  - Sync function signature `copyCode(button, codeId)` 1-to-1 with element attributes `onclick="copyCode(this, 'id')"` to prevent `TypeError`.

---

## 5. HyperFrames Video & GSAP Animations

- **[INITIAL GSAP TIMELINE INITIALIZATION]**:
  - Every GSAP scene timeline MUST initialize visibility at timestamp 0:
    ```javascript
    tl.set(".clip", { autoAlpha: 1 }, 0);
    ```

- **[MINIMUM 3-STEP ANIMATION SEQUENCE]**:
  - Each scene animation timeline MUST include at least 3 sequential steps:
    1. Clip visibility initialization (`autoAlpha: 1`)
    2. Intro title reveal
    3. Main content breakdown & highlights

- **[SCENE & TTS SCRIPT SYNCHRONIZATION]**:
  - `scene_id` array keys MUST match 1-to-1 between visual `scenes` and audio `tts_scripts`.
  - Cumulative `start_at_root` timestamps MUST equal the sum of durations of all preceding scenes.

---

## 6. Markmap Mindmaps & Design Formatting

- **[BILINGUAL HEADING TRANSLATION]**:
  - Convert internal snake_case keys into natural Accented Vietnamese for all Markdown H2/H3 mindmap headings.

- **[STRICT TEXT EMOJI PROHIBITION]**:
  - 100% FORBIDDEN to render text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶).
  - Use vector Phosphor Icons `<i class="ph-bold ph-*"></i>` or standardized text badges (`[NOTE]`, `[TIP]`, `[WARNING]`).

- **[SYNTAX FENCE INTEGRITY]**:
  - Ensure all Markmap Markdown codeblocks (` ```markmap `) close cleanly without dangling backticks.

- **[COLLAPSIBLE HTML DETAILS]**:
  - Wrap extended supplementary code snippets inside `<details><summary>...</summary>...</details>` blocks with custom WCAG accessible styling.
* **[PYTHON/CORE]**: Khi thiết kế bài học thực hành cấu trúc điều khiển (Is Theory/Diagram Only Lesson = False), luôn sử dụng các động từ Bloom đo lường được (như giải thích được, trình bày được, sử dụng được) trong chuẩn đầu ra, loại bỏ rác hệ thống và tích hợp đầy đủ visualizer-canvas mô phỏng trạng thái biến lặp, bảng điều khiển từng bước (Start, Pause, Step, Reset) cùng Code Tracker có highlight lớp active-line đồng bộ. | Source: [[Lesson 01 - Khái niệm vòng lặp và câu lệnh for]]
* **[PYTHON/CORE]**: Khi thiết kế ví dụ mã nguồn cho bài học vòng lặp while cơ bản, chỉ điều khiển chu kỳ lặp bằng cách cập nhật biến kiểm soát trong thân vòng lặp và không sử dụng các câu lệnh ngắt lặp vượt cấp như break hoặc continue. | Source: [[Lesson 02 - Vòng lặp while và lặp theo điều kiện]]

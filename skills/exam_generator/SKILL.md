---
name: exam_generator
description: Generate midterm and final practical/MCQ/oral examinations that adapt their exam format to the course's underlying architecture pattern (CLI console app, Web Backend REST API, Web Frontend UI, Mobile App, Database SQL, DevOps/Cloud) — exported as Markdown (Đề thi thực hành, Câu hỏi vấn đáp) and JSON (Đề thi trắc nghiệm) inside the exam session folder. Target output language is 100% Accented Vietnamese.
---

# Exam Generator Skill — Rikkei Education Standards

This document defines the technical standard for the **`exam_generator`** skill, responsible for
authoring Midterm (`Thi Giữa Môn`) and Final (`Thi Cuối Môn`) examinations. It governs 3 exam
artifacts per exam session: **Đề thi thực hành** (Practical Exam), **Đề thi trắc nghiệm** (MCQ
Exam), and **Câu hỏi vấn đáp** (Oral Defense Questions).

---

## 0. PEDAGOGICAL FOUNDATION

1. **Exam Format MUST Match Course Architecture, Not Be Hardcoded Per-Course**:
   - Exam design MUST NOT assume any specific technology. The practical exam's deliverable shape
     is derived dynamically from the SAME `resolve_course_architecture()` engine that already
     governs Mini Project generation (`core/course_architecture.py`), which classifies the course
     into one of: `CLI_CORE`, `WEB_BACKEND`, `WEB_FRONTEND`, `MOBILE_APP`, `DATABASE_SQL`,
     `DEVOPS_CLOUD`.
   - Concretely:
     * `CLI_CORE` (e.g. Python Core, Java Core, C fundamentals): the practical exam is a
       **menu-driven terminal/console application** (numbered menu loop, functions triggered by
       user input, native exceptions, console I/O only).
     * `WEB_BACKEND` (e.g. FastAPI, Express, Spring Boot): the practical exam is **building REST
       API endpoints** (routes, request/response schemas, HTTP status codes, unified JSON error
       envelope).
     * `WEB_FRONTEND` (e.g. HTML/CSS, React, Vue): the practical exam is **building a UI screen /
       component** matching a given spec (layout, form validation, inline error states, DOM
       interactivity where taught).
     * `MOBILE_APP`, `DATABASE_SQL`, `DEVOPS_CLOUD`: the practical exam mirrors the equivalent
       real deliverable of that discipline (a mobile screen/flow, a schema+query set, a
       pipeline/deployment script respectively).
   - ABSOLUTELY FORBIDDEN to author a CLI menu exam for a course whose architecture is
     `WEB_FRONTEND`, or vice-versa — the exam type must be re-derived per course/session, never
     copy-pasted from a template written for a different architecture.

2. **Zero Out-of-Scope / Future-Concept Leakage (Hard Contract)**:
   - Every exam question, practical requirement, MCQ option, and oral question MUST use ONLY
     concepts explicitly present in the CUMULATIVE `allowed_scope` (everything taught in the
     course UP TO the exam's position) — Midterm = everything before the midterm session; Final =
     everything in the entire course.
   - ABSOLUTELY FORBIDDEN to reference anything in `forbidden_scope` (concepts taught in later
     sessions, for Midterm; there normally is none left to forbid for Final since it is the last
     content checkpoint).
   - This is enforced both at generation time (the scope contract is injected into every prompt,
     exactly like Mini Project generation) and at review time via
     `lint_document_architecture()` (the same systemic linter Mini Project already uses).

3. **Midterm vs Final — Scope and Weight Differ, Format Logic Does Not**:
   - **Midterm (Thi Giữa Môn)**: covers the first half of the course. Practical exam requests a
     FOCUSED deliverable (4-6 functions/endpoints/screen-elements). Duration guidance: 90-120
     minutes. MCQ: exactly 20 questions. Oral: 6-8 questions.
   - **Final (Thi Cuối Môn)**: covers the ENTIRE course cumulatively. Practical exam requests a
     BROADER, integrative deliverable (6-10 functions/endpoints/screen-elements, may combine
     multiple modules taught across the course). Duration guidance: 120-180 minutes. MCQ: exactly
     30 questions. Oral: 8-10 questions.
   - Both reuse the exact same architecture-adaptive logic from directive #1 — only the scope
     window and quantity/duration change.

---

## 1. ARTIFACT 1 — ĐỀ THI THỰC HÀNH (Practical Exam)

**Output**: `Đề thi thực hành/de_thi_thuc_hanh.md`

**Mandatory Document Structure** (mirrors the Mini Project entry-test/assignment convention for
consistency across the platform):
- Title: `## <center>[Đề thi Giữa Môn | Đề thi Cuối Môn] — [Tên nghiệp vụ] ([English Name])</center>`
- `### **1. Mục tiêu bài thi**` — what competencies this exam verifies.
- `### **2. Đề bài và Yêu cầu**` — contains a 100%-width HTML spec table (function/endpoint/screen
  name in Vietnamese + English `<code>` identifier | Input | Processing Logic | Output), following
  the SAME naming-convention/error-model contract `resolve_course_architecture()` returns for the
  detected pattern.
- `### **3. Ràng buộc kỹ thuật**` — explicitly restates the allowed/forbidden knowledge boundary
  in plain language so a student self-audits before submitting.
- `### **4. Tiêu chí chấm điểm**` — 100-point rubric, same 5-group structure as Mini Project
  (Thiết lập & Khởi tạo, Logic nghiệp vụ cốt lõi, Kiểm chuẩn dữ liệu & Xử lý ngoại lệ, Chức năng
  nâng cao/Kiểm thử, Chất lượng mã nguồn) plus Bonus.
- `### **5. Yêu cầu nộp bài**` — submission instructions (GitHub link or equivalent per course
  convention).

**Content Rules**:
- Single unified business domain per exam (reuse `get_domain_for_session`/`chosen_domain`, same
  as every other resource in this session) — the practical exam is a concrete module of that
  domain, not a generic disconnected toy problem.
- Progressive-difficulty-aware: within the spec table, order requirements from simplest
  (data setup / basic CRUD) to most complex (validation, aggregation, edge-case handling) so
  students can build up their solution incrementally under time pressure.
- 100% English identifiers, 100% Accented Vietnamese prose — same contract as every other
  resource in this platform.
- No AI/assistant mentions, no informal tone, no student-ability tiering labels (reuses the exact
  banned-word list `project_reviewer_agent` already enforces).

---

## 2. ARTIFACT 2 — ĐỀ THI TRẮC NGHIỆM (MCQ Exam)

**Output**: `Đề thi trắc nghiệm/de_thi_trac_nghiem.json` (+ Excel export via the existing
`core/quiz_excel.export_lesson_quiz_to_excel` pipeline, matching lesson-quiz conventions already
in use).

**Schema** (array of question objects, same shape as the existing lesson `quiz_agent` schema so
downstream tooling — Excel export, review scripts — is reusable without modification):
```json
[
  {
    "stt": 1,
    "question_type": "SYNTAX | EXECUTION_FLOW | CODE_TRACE | COMPARISON | TRAP_PREDICTION",
    "question": "Câu hỏi trắc nghiệm tiếng Việt, có thể chứa `inline_code` hoặc khối ```lang ...```.",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "correct_option_index": 0,
    "explanation": "Giải thích đáp án đúng.",
    "instant_feedback": "Gợi ý ôn lại phần kiến thức liên quan nếu chọn sai.",
    "time_limit_sec": 45
  }
]
```

**Content Rules**:
- Exactly 20 questions for Midterm, exactly 30 for Final.
- Questions MUST be distributed proportionally across ALL sessions/topics covered in the exam's
  scope window — never concentrate all questions on only the most recent 1-2 sessions.
  Distribute roughly evenly across the 5 `question_type` categories.
- Zero forbidden-scope leakage — every question is checked against the same `forbidden_scope`
  contract as every other resource.
- No duplicate questions (same concept + same code snippet tested twice).

---

## 3. ARTIFACT 3 — CÂU HỎI VẤN ĐÁP (Oral Defense Questions)

**Output**: `Câu hỏi vấn đáp/cau_hoi_van_dap.md`

**Purpose**: A short, individually-administered oral checklist the instructor uses immediately
after the practical exam submission, specifically designed to verify the student personally
understands what they submitted (anti-plagiarism / anti-"AI wrote it for me" safeguard) — NOT a
repeat of the MCQ theory exam.

**Content Rules**:
- 6-8 questions for Midterm, 8-10 for Final.
- Every question MUST reference a concrete design decision or code element that would plausibly
  appear in a correct solution to THIS exam's own practical exam artifact (e.g. "Giải thích lý do
  bạn chọn cấu trúc dữ liệu X cho tính năng Y trong bài làm của mình", "Nếu yêu cầu Z đổi thành
  ..., bạn sẽ sửa đoạn code nào và vì sao?") — never generic textbook questions unrelated to the
  student's own submission.
- Include a short "Định hướng đáp án đạt" note per question (what a competent, genuine answer
  sounds like) to help the instructor calibrate scoring consistently.
- Same scope boundary and banned-word contract as every other artifact.

**Output Format**:
```markdown
# Bộ câu hỏi vấn đáp — [Đề thi Giữa Môn | Đề thi Cuối Môn]

### Câu 1: [Câu hỏi vấn đáp cụ thể, gắn với bài làm thực hành của thí sinh]
> **Định hướng đáp án đạt:** [Mô tả ngắn gọn câu trả lời hợp lệ]

---
```

---

## 4. REVIEW GATE (MANDATORY BEFORE PUBLISH)

Every exam session's 3 artifacts MUST pass `exam_reviewer_agent` before being written to their
final disk location (same generate→review→retry-up-to-3x→publish loop as
`generate_mini_project_session`). The reviewer checks, in order:
1. Architecture/scope linting via `lint_document_architecture()` (reused verbatim from the
   Mini Project governance engine) — catches forbidden-scope leakage and architecture-pattern
   mismatches (e.g. a REST API artifact appearing in a CLI_CORE course).
2. Banned casual/AI-mention words and student-ability-tiering labels (reused verbatim from
   `project_reviewer_agent`'s list).
3. Structural completeness: all mandatory H3 headers present in the practical exam; MCQ count
   exactly matches the Midterm/Final quota with 5 valid `question_type` values and 4 options each;
   oral question count within the mandated range and each item has a "Định hướng đáp án đạt" note.
4. 100%-width HTML table check (reused verbatim) wherever a spec table is used.
5. Domain consistency: the practical exam's business scenario matches the session's
   `chosen_domain`.

If REJECTED, regenerate with the reviewer's feedback appended as additional context (same retry
pattern as Mini Project, capped at 3 attempts, then publish the last draft with a console warning
for human follow-up rather than blocking the pipeline indefinitely).

---

## 5. LESSON FOLDER STRUCTURE LOCATION

```text
📁 Session XX - [Thi Giữa Môn | Thi Cuối Môn]/
├── 📂 Đề thi thực hành/
│   └── 📄 de_thi_thuc_hanh.md
├── 📂 Đề thi trắc nghiệm/
│   ├── 📄 de_thi_trac_nghiem.json
│   └── 📄 De_Thi_Trac_Nghiem_SessionXX.xlsx
└── 📂 Câu hỏi vấn đáp/
    └── 📄 cau_hoi_van_dap.md
```

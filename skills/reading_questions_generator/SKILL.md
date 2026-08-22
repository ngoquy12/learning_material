---
name: reading_questions_generator
description: Generate exactly 3 practical scenario questions (3 difficulty levels — Thông hiểu/Vận dụng/Phân tích) anchored on reading.html code snippets to verify actual reading comprehension, exported as Markdown (reading_questions.md) inside the 'Câu hỏi bài đọc' folder. Target output language is 100% Accented Vietnamese.
---

# Multi-Case Practical Reading Check Generator Skill — Rikkei Education Standards

This document defines the technical standards for the **`reading_questions_generator`** skill, responsible for generating practical multi-case reading comprehension check questions anchored directly on code snippets and scenario data from `reading.html`.

---

## 0. PEDAGOGICAL OBJECTIVE & MULTI-CASE CODE TRACING MANDATE

1. **Primary Evaluation Objective**:
   - The Reading Comprehension Question Suite (`reading_questions.md`) is specifically designed to **verify that students have ACTUALLY READ, TRACED, and DEEPLY UNDERSTOOD the lesson article (`reading.html`)**.
   - Questions MUST NOT be long, text-heavy, or abstract theoretical essays. Questions MUST be **practical, concise, and structured around multi-case execution tracing**.

2. **Zero Fabrication — Anchor on the REAL `reading.html`, Not a Blueprint**:
   - Every question MUST be built from code/data that is **verbatim, actually present in the
     lesson's finished `reading.html`** (extracted programmatically from the real sandbox code
     blocks and section text — NOT from an intermediate content blueprint, which may drift in
     domain/scenario from the finished article).
   - ABSOLUTELY FORBIDDEN to invent a new business scenario or new code that does not literally
     appear in the article. If the question set's scenario does not match the article a student is
     looking at, the entire assessment is broken — the student cannot answer by having read it.
   - There is **NO separate upfront "code snippet" section**. Each question is self-contained: it
     quotes its own relevant real code excerpt directly inside the question text (inline `code`
     span or short fenced block), then asks about it directly.

3. **Exactly 3 Questions, 3 Difficulty Levels (Quy tắc 3 Câu — 3 Mức Độ) — internal design guidance only**:
   - **Question 1 — Mức Thông hiểu (Comprehension)**: Quote a real code excerpt from the article and ask directly what it does / its core mechanism. (e.g. *"Trong đoạn code sau: `for i in items:` dòng lệnh này có chức năng gì?"*)
   - **Question 2 — Mức Vận dụng (Application)**: Change ONE concrete value in that SAME real code ➔ Student predicts the new result. (e.g. *"Nếu đổi giá trị của `a` từ 3 thành 4 thì kết quả in ra là gì?"*)
   - **Question 3 — Mức Phân tích (Analysis)**: A boundary/invalid input or common mistake on that SAME real code ➔ Student pinpoints the logic flaw/error and states the fix.
   - **These 3 level names are an internal authoring guide ONLY — they must NEVER appear as visible
     labels/prefixes in the question text itself** (see Section 2 of this document, "FORBIDDEN
     META-LABELS", for the exact wording ban). Exactly 3 questions total — never 4 or more.

4. **FORBIDDEN META-LABELS**:
   - ABSOLUTELY FORBIDDEN to prefix any question with case-naming jargon such as
     `(Xung hướng - Tính toán kết quả với dữ liệu X)`, `(Nghịch hướng - Suy luận dữ liệu đầu vào từ
     kết quả Z)`, `(Forward Tracing ...)`, `(Reverse Deduction ...)`, or any similar meta-label.
   - Questions MUST read as plain, direct, straight-to-the-point comprehension checks with no
     artificial framing — the question text itself starts directly with the real content/code.

5. **Domain-Agnostic Contract (Cấm Hardcode theo Môn)**:
   - **Executable Programming (Python, JS, Java, C++, SQL...)**: Trace variables, branching execution paths, boundary values, and console outputs.
   - **Tooling & Process (Git, Docker, VS Code, Agile...)**: Trace CLI command parameters, file config options, repository states, and terminal error outputs.

---

## 1. QUESTION MATRIX & SPECIFICATIONS

| # | Difficulty Level | Pedagogical Objective | Expected Answer Format |
| :-: | :--- | :--- | :--- |
| **1** | **Thông hiểu (Comprehension)** | Test understanding of what a real code excerpt does / its core mechanism. | Explanation of the mechanism, anchored on the real code. |
| **2** | **Vận dụng (Application)** | Test ability to predict execution outcome after changing one concrete value. | Branch/flow decision + new predicted output value. |
| **3** | **Phân tích (Analysis)** | Test detection of boundary errors, common mistakes, or invalid inputs. | Root cause analysis + corrected code/input logic. |

---

## 2. OUTPUT FORMAT STANDARDS (`reading_questions.md`)

The reading comprehension questions MUST be formatted as a clean Markdown document saved at
`Câu hỏi bài đọc/reading_questions.md`. There is **NO shared upfront "code snippet" section** —
each question embeds its own real code excerpt directly, and question titles carry **NO meta-label
prefix** (plain "Câu N:" only, followed directly by the real question content):

```markdown
# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

### Câu 1: Trong đoạn code sau trích từ bài đọc: `for i in items:` — dòng lệnh này có chức năng gì?
> **Gợi ý trả lời & Định hướng đáp án:**
> - [Giải thích cơ chế của dòng lệnh, bám sát đúng code thật đã trích...]

---

### Câu 2: Vẫn với đoạn code trên, nếu đổi giá trị của `a` từ 3 thành 4 thì kết quả in ra là gì?
> **Gợi ý trả lời & Định hướng đáp án:**
> - [Phân tích sự thay đổi và kết quả mới, dựa trên code thật...]

---

### Câu 3: Nếu truyền vào giá trị biên/không hợp lệ cho đoạn code trên, hiện tượng gì xảy ra và cách sửa là gì?
> **Gợi ý trả lời & Định hướng đáp án:**
> - [Phân tích nguyên nhân lỗi / Unreachable code...]
> - [Giải pháp khắc phục đúng quy chuẩn...]
```

---

## 3. WORKED EXEMPLARS (FEW-SHOT)

The two exemplars below are the **only** place in this document showing a complete
input ➔ output pair. Follow their SHAPE exactly; ignore their subject matter.

> **Two exemplars in two different stacks, on purpose.** A single-stack exemplar makes the
> model anchor on that stack's idioms and quietly reshape questions for unrelated subjects.
> Whatever the lesson's `tech_stack` is, the output must mirror the STRUCTURE below, never
> the language.

### 3.1 Exemplar A — executable programming stack

**Input — real excerpt actually present in `reading.html`:**

```python
gio_da_dat = 3
if gio_da_dat > 2:
    phi_giu_xe = 20000
else:
    phi_giu_xe = 10000
print(phi_giu_xe)
```

**Correct output:**

```markdown
# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

### Câu 1: Trong đoạn code sau trích từ bài đọc: `if gio_da_dat > 2:` — điều kiện này quyết định điều gì trong cách tính phí giữ xe?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Điều kiện so sánh số giờ đã đặt với mốc 2 giờ để chọn một trong hai mức phí.
> - Với `gio_da_dat = 3`, điều kiện đúng nên nhánh đầu tiên chạy, `phi_giu_xe` nhận giá trị 20000.

---

### Câu 2: Vẫn với đoạn code trên, nếu đổi `gio_da_dat` từ 3 thành 2 thì chương trình in ra bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - `2 > 2` là sai, nên chương trình rẽ sang nhánh `else`.
> - Kết quả in ra là 10000.

---

### Câu 3: Nếu `gio_da_dat` nhận giá trị âm, đoạn code trên xử lý ra sao và cần sửa thế nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Code vẫn chạy và rơi vào nhánh `else`, tính phí 10000 cho một số giờ vô nghĩa — sai về nghiệp vụ chứ không báo lỗi.
> - Cần kiểm tra `gio_da_dat` không âm trước khi tính phí, hoặc dừng lại và báo dữ liệu không hợp lệ.
```

### 3.2 Exemplar B — tooling / process stack (same shape, no code execution)

**Input — real excerpt actually present in `reading.html`:**

```bash
git commit -m "them man hinh dat phong"
```

**Correct output (question titles only, hint blocks follow the same format as above):**

```markdown
### Câu 1: Trong câu lệnh sau trích từ bài đọc: `git commit -m "them man hinh dat phong"` — tham số `-m` có tác dụng gì?

### Câu 2: Vẫn với câu lệnh trên, nếu bỏ hẳn phần `-m "..."` thì Git sẽ phản ứng thế nào?

### Câu 3: Nếu chạy câu lệnh trên khi chưa có tệp nào được đưa vào vùng staging, Git báo gì và cần làm gì trước đó?
```

### 3.3 What these exemplars demonstrate

| Rule | How the exemplars satisfy it |
| :-- | :-- |
| Zero fabrication | Every question quotes the excerpt verbatim; no new scenario invented. |
| Exactly 3 questions | Three `### Câu N:` headings, never four. |
| No meta-labels | Titles start with the real content — no `(Xung hướng - ...)` prefixes, and the level names Thông hiểu/Vận dụng/Phân tích appear nowhere in the output. |
| Same code across all 3 | Q2 and Q3 say "Vẫn với đoạn code trên" instead of introducing new code. |
| Progressive difficulty | Q1 explains the mechanism ➔ Q2 changes one value ➔ Q3 probes a boundary and asks for the fix. |
| Domain-agnostic | Exemplar B carries the identical structure with no executable code at all. |

---

## 4. LESSON FOLDER STRUCTURE LOCATION

```text
📁 Lesson XX - [Tên Bài Học]/
├── 📂 Bài đọc/
│   └── 📄 reading.html
├── 📂 Bài thực hành/
│   ├── 📄 practical_lab.md
│   └── 📄 practical_lab.html
├── 📂 Câu hỏi bài đọc/
│   └── 📄 reading_questions.md
├── 📂 Câu hỏi Quizz/
│   └── 📄 quiz.json
└── 📂 Video/
    └── 📄 SCRIPT.md
```

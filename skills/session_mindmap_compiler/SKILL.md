---
name: session_mindmap_compiler
description: Synthesize and generate Session-Level Markmap mindmaps (.md format) for 1.5-hour sessions according to Rikkei Education standards, compatible with VS Code Markmap and XMind. Target output language is 100% Accented Vietnamese.
---

# Session Mindmap Compiler Skill — Rikkei Education Standards

## 0. Context & Purpose

This skill generates **1 single Markmap file** (`session_XX_mindmap.md`) encompassing the entire 1.5-hour learning session.

**Mindmap Scope Distinction**:

- `mindmap_generator` — **Lesson-level** Mindmap (individual lesson technical details)
- `session_mindmap_compiler` ← **This Skill** — **Session-level** Mindmap (overall architecture, cross-lesson synthesis)

**Tool Compatibility**:

- VS Code Markmap extension (live preview)
- XMind: File → Import → Markdown
- Browser: Markmap Live (markmap.netlify.app)
- Obsidian: Markmap plugin inside Obsidian vault

---

## 1. Fixed Mandatory Hierarchy

```markmap
# Session XX: [Tên Session — ngắn gọn, mô tả kỹ năng đầu ra]

## Bối cảnh buổi học
- Bài toán nghiệp vụ tổng thể session
- Mục tiêu kỹ năng đầu ra

## Lesson 01 — [Tên Lesson]
### [Vấn đề] Tại sao cần học?
### [Khái niệm] Kiến thức cốt lõi
### [Cú pháp] Mã nguồn & Cấu trúc
### [Thực chiến] Lưu ý & Bẫy lỗi
### [Áp dụng] Câu hỏi tình huống

## Lesson 02 — [Tên Lesson]
...

## Kết nối liên bài
- [Kiến thức Lesson 01] → nền tảng cho [Lesson 02]
- Bài toán tổng hợp xuyên suốt session
```

**Heading Hierarchy Rules**:

- `#` — Session Root Node (Exactly 1 root node)
- `##` — Session Context + Each Lesson + Cross-Lesson Connections
- `###` — 5 Fixed Branch Sub-headings per Lesson
- `-` (bullet) — Details ≤ 6 words/line, max 3 bullet levels

---

## 2. 5 Fixed Branch Specifications per Lesson

Every `## Lesson` MUST contain exactly 5 `###` branches in the following order:

### Branch 1: `[Vấn đề] Tại sao cần học?` (Directive 3 — Problem-First)

**Objective**: Trigger "Why?" thinking before teaching concepts.
**Mandatory Content**:

- Real-world business problem (1 bullet — ≤ 8 words)
- Legacy approach drawbacks (2-3 short bullets)
- Key benefits of new approach (1 bullet)

**Exemplar**:

```markmap
### [Vấn đề] Tại sao cần học?
- Bài toán: Tính lương 500 nhân viên tự động
- Cách cũ: Viết lặp code 500 lần — lỗi nhất quán
- Cách cũ: Sửa một chỗ → phải sửa 500 chỗ
- Hàm: Đóng gói logic — thay đổi 1 nơi, áp dụng ngay
```

### Branch 2: `[Khái niệm] Kiến thức cốt lõi` (Directive 2 — Micro-Learning)

**Rules**:

- Maximum 5 bullets — each bullet ≤ 6 words
- Core concepts only; no long explanations
- Keep EN technical keywords; provide concise VI explanations

**Exemplar**:

```markmap
### [Khái niệm] Kiến thức cốt lõi
- `function` — khối code tái sử dụng
- Parameter — đầu vào, Return — đầu ra
- Scope: Local vs Global
- `def` keyword (Python) / `function` (JS)
```

### Branch 3: `[Cú pháp] Mã nguồn & Cấu trúc` (Directive 4 — Visual-Rich)

**Rules**:

- MUST include 1 runnable short code snippet (≤ 8 lines) inside ` ```language ` block
- Executable snippet with Vietnamese inline comments
- Case convention: `snake_case` (Python/C), `camelCase` (JS/Java/C++)
- NO toy variable names (`a`, `b`, `x`, `temp`)

**Exemplar (Python)**:

````markmap
### [Cú pháp] Mã nguồn & Cấu trúc
- Khai báo hàm Python:
  ```python
  def tinh_thue_vat(gia_ban: float, thue_suat: float = 0.1) -> float:
      """Tính thuế VAT cho sản phẩm."""
      return gia_ban * thue_suat
````

- Gọi hàm: `tien_thue = tinh_thue_vat(500_000)`
- Default parameter: `thue_suat=0.1`
- Type hint: `-> float` chỉ kiểu trả về

````

### Branch 4: `[Thực chiến] Lưu ý & Bẫy lỗi` (Directive 4 — Gotchas)
**Rules**:
- 3-4 bullets — each bullet: **Bold Bug Name** + short impact summary
- Gotchas MUST represent real-world traps students encounter
- Include "Best practice vs Anti-pattern" where applicable

**Exemplar**:
```markmap
### [Thực chiến] Lưu ý & Bẫy lỗi
- **Mutable default arg**: `def f(lst=[])` → bug khó tìm
- **Global scope leak**: dùng `global x` → phá vỡ encapsulation
- **Side effect**: hàm vừa tính vừa print → khó test
- Thực hành tốt: 1 hàm = 1 nhiệm vụ duy nhất
````

### Branch 5: `[Áp dụng] Câu hỏi tình huống` (Directives 5+6 — Scenario-Based)

**Rules**:

- 2-3 scenario-based questions (NO rote theory recall)
- Each question starts with "Nếu..." / "Bạn đang..." / "Hãy chọn..."
- Include citation note "Đáp án: Phần X bài đọc" for Anti-AI verification
- FORBIDDEN: "Hàm là gì?", "Liệt kê cú pháp của..."

**Exemplar**:

```markmap
### [Áp dụng] Câu hỏi tình huống
- Nếu hàm `tinh_thue()` vừa tính vừa in ra màn hình — vấn đề?
  - Đáp án: Phần 4 bài đọc — vi phạm Single Responsibility
- Bạn cần tính thuế cho 3 loại thuế suất khác nhau — làm thế nào?
  - Đáp án: Phần 3 — Default parameter + function call 3 lần
- Hãy chọn: dùng global variable hay parameter để truyền giá trị?
  - Đáp án: Phần 4 — Gotcha: Global scope leak
```

---

## 3. Special Nodes: Session Context & Cross-Lesson Connections

### `## Bối cảnh buổi học` (Placed first, under Session Root)

```markmap
## Bối cảnh buổi học
- Dự án thực tế: [Tên dự án xuyên suốt session]
- Bài toán: [Mô tả 1 câu — ≤ 10 từ]
- Kỹ năng đầu ra: [Liệt kê 2-3 kỹ năng cụ thể]
- Ngôn ngữ: [Python / JavaScript / Java / C / C++]
```

### `## Kết nối liên bài` (Placed last)

```markmap
## Kết nối liên bài
- Lesson 01 → Lesson 02: [Kiến thức nào làm nền tảng]
- Bài toán tổng hợp: [Mô tả bài tập áp dụng xuyên session]
- Bài học tiếp theo: [Preview kiến thức sẽ học]
```

---

## 4. Mandatory Technical Rules

### Content Rules (10 Directives Applied to Mindmap)

|  #  | Directive         | Mindmap Branch Application                               |
| :-: | :---------------- | :------------------------------------------------------- |
|  1  | Fixed Hierarchy   | Session → Lesson → 5 fixed sub-branches                  |
|  2  | Micro-learning    | Each bullet ≤ 6 words — NO paragraph blocks inside nodes |
|  3  | Problem-First     | Branch 1 per Lesson = Business Problem                   |
|  4  | Visual-Rich       | Branch 3 = Runnable code snippet with VI comments        |
|  5  | Scenario-Based    | Branch 5 = Scenario questions; NO rote theory recall     |
|  6  | Anti-AI Shortcut  | Branch 5 includes "Đáp án: Phần X bài đọc" citations     |
|  7  | Single Page       | Link anchor to original reading material if cited        |
|  8  | Human Quality     | EN keywords preserved; concise VI explanation            |
|  9  | Code Conventions  | `snake_case` (Python/C), `camelCase` (JS/Java/C++)       |
| 10  | Emoji Prohibition | STRICTLY NO emojis in any node. NO ALL CAPS text.        |

### Anti-Scope-Leakage Directives

- **STRICTLY FORBIDDEN** to reference unlearned syntax/concepts outside session boundary.
- Respect each lesson's `forbidden_scope` parameter.

### Bilingual Conventions

- **English**: Technical keywords, function names, variable names, error types (`IndentationError`, `None`, `undefined`).
- **Accented Vietnamese**: Branch titles, explanations, scenario questions.
- FORBIDDEN non-standard abbreviations ("ko", "vs", "đk", "bt").

---

## 5. Technology Matrix

| Language       | Syntax Branch                           | Gotchas Branch (Language-Specific Traps)                |
| :------------- | :-------------------------------------- | :------------------------------------------------------ |
| **Python**     | `def`, type hint `->`, docstring `"""`  | Mutable default arg, Global scope, IndentationError     |
| **JavaScript** | `function` / arrow `=>`, `const/let`    | `undefined` vs `null`, hoisting, `this` context         |
| **Java**       | `returnType methodName(params)`, `void` | NullPointerException, pass-by-value of reference        |
| **C**          | `returnType funcName(params)`, `void*`  | Dangling pointer, no return value check, stack overflow |
| **C++**        | function overloading, default params    | Undefined behavior, double free, slicing problem        |

---

## 6. Execution Workflow

```
Step 1: Receive SSOT Session metadata from PM
  → Lesson IDs + titles + forbidden_scope per lesson

Step 2: Generate Session Root Structure
  → # Session XX: [Title] + ## Bối cảnh buổi học

Step 3: For each Lesson — generate 5 mandatory branches ###
  → [Vấn đề] → [Khái niệm] → [Cú pháp] → [Thực chiến] → [Áp dụng]
  → Verify forbidden_scope before outputting Syntax branch

Step 4: Generate ## Kết nối liên bài
  → Analyze cross-lesson dependencies

Step 5: Run Quality Gate Check (Section 7)
  → Pass → output file session_XX_mindmap.md
  → Fail → remediate violating branches
```

---

## 7. Quality Gate Checklist — 6 Audit Points

Mindmap is approved ONLY when passing all 6 audit points:

|  #  | Criterion                                    | Verification Method                    |
| :-: | :------------------------------------------- | :------------------------------------- |
|  1  | Exactly 5 `###` sub-branches per Lesson      | Count `###` headings under `##` groups |
|  2  | Zero forbidden_scope leaks                   | Grep forbidden scope terms             |
|  3  | Runnable snippet in `[Cú pháp]` branch       | Grep ` ```language ` block             |
|  4  | `[Vấn đề]` starts with business problem      | Validate first bullet content          |
|  5  | `[Áp dụng]` contains "Nếu/Bạn/Hãy" scenarios | Match scenario pattern                 |
|  6  | No text emojis, no ALL CAPS text in nodes    | Regex inspection                       |

---

## 8. Output Format & Tool Compatibility

### Output File Schema

```text
session_XX_mindmap.md
```

All content wrapped in Markmap block:

```markmap
# Session XX: [Session Title]
...
```

### Tool Usage Reference

| Tool                | Usage Mode                              | Notes                   |
| :------------------ | :-------------------------------------- | :---------------------- |
| **VS Code Markmap** | Install extension → live preview        | Real-time SVG rendering |
| **XMind**           | File → Import → Markdown → select `.md` | Structure preserved     |
| **Markmap Live**    | markmap.netlify.app → paste content     | Browser native          |
| **Obsidian**        | Markmap plugin → render in vault        | Integrated with notes   |

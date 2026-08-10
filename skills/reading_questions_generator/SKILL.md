---
name: reading_questions_generator
description: Generate a 3 to 4 open-ended essay question Reading Check set adhering to Anti-AI pedagogical standards directly based on reading.html content, exported as Markdown (reading_questions.md) inside the 'Câu hỏi bài đọc' folder. Target output language is 100% Accented Vietnamese.
---

# Open-ended Reading Check Generator Skill — Rikkei Education Standards

This document defines the technical standards for the **`reading_questions_generator`** skill, responsible for generating open-ended essay reading comprehension check questions directly from `reading.html`.

---

## 0. PEDAGOGICAL OBJECTIVE & ANTI-SHORTCUT MANDATE

1. **Primary Evaluation Objective**:
   - The Reading Comprehension Question Suite (`reading_questions.md`) is specifically designed to **verify that students have ACTUALLY READ and DEEPLY UNDERSTOOD the specific lesson article (`reading.html`)**.
   - 100% of reading check questions MUST be presented in open-ended essay format (Dạng Tự Luận). NO multiple-choice options (A/B/C/D).

2. **Strict Anti-AI & Anti-Search Shortcut Contract**:
   - **ABSOLUTELY FORBIDDEN**: High-level generic textbook questions (e.g. "What is Git?", "Explain why virtual environments are important", "Present syntax of loop", "List PEP 8 rules").
   - **MANDATORY DATA BINDING**: EVERY question MUST be tightly bound to **specific concrete data, code snippets, file/variable names, error messages, step sequences, or Gotcha traps** present within THAT SPECIFIC lesson article (`reading.html`).
   - External search engines (Google) or generic AI queries MUST NOT be able to solve the question without analyzing the exact scenario data given in the reading text.

---

## 1. ESSAY QUESTION MATRIX (3-4 DATA-BOUND QUESTIONS)

|   #   | Question Type | Content & Evaluation Objective | Mandatory Data Source in `reading.html` |
| :---: | :--- | :--- | :--- |
| **1** | **Scenario Data & Business Rationale** | Force student to analyze the specific enterprise pain point, file/variable names, or numerical constraints. | Section 1 (`#problem-intro`) |
| **2** | **Mechanism Trace & State Change** | Force student to trace underlying execution steps, memory allocations, or RAM/state transforms. | Section 2 (`#data-structure`) |
| **3** | **Code Bug & Execution Line Analysis** | Quote specific code snippet or CLI sequence from article; student pinpoints exact error line or output. | Section 3 (`#interactive-demo`) |
| **4** | **Gotcha Trap & Anti-Pattern Fix** | Analyze specific anti-pattern or error trap from Section 4; student details PEP 8/Best Practice resolution. | Section 4 (`#summary-notes`) |

---

## 2. OUTPUT FORMAT STANDARDS (`reading_questions.md`)

The reading comprehension essay questions MUST be formatted as a clean Markdown document saved at `Câu hỏi bài đọc/reading_questions.md`:

```markdown
# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: [Nội dung câu hỏi tự luận phân tích bối cảnh/tình huống nghiệp vụ...]
> **Gợi ý trả lời & Định hướng đáp án:** [Phân tích chi tiết câu trả lời tự luận dựa trên kiến thức và sơ đồ trong bài đọc...]

---

### Câu 2: [Nội dung câu hỏi tự luận phân tích cơ chế vận hành hoặc Gotcha...]
> **Gợi ý trả lời & Định hướng đáp án:** [Giải thích chi tiết nguyên lý vận hành, quy chuẩn thụt lề hoặc bẫy lỗi hệ thống...]

---

### Câu 3: [Nội dung câu hỏi tự luận phân tích đoạn mã nguồn và khắc phục lỗi...]
> **Gợi ý trả lời & Định hướng đáp án:** [Giải thích từng dòng lệnh, ép kiểu dữ liệu tường minh và cách sửa lỗi mã nguồn theo chuẩn PEP 8...]
```

---

## 3. LESSON FOLDER STRUCTURE LOCATION

```text
📁 Lesson XX - [Tên Bài Học]/
├── 📂 Bài đọc/
│   └── 📄 reading.html
├── 📂 Câu hỏi bài đọc/
│   └── 📄 reading_questions.md
├── 📂 Câu hỏi Quizz/
│   └── 📄 quiz.json
└── 📂 Video/
    └── 📄 SCRIPT.md
```


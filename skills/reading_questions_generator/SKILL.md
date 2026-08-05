---
name: reading_questions_generator
description: Generate a 3-question Reading Check set adhering to Anti-AI pedagogical standards directly based on reading.html content, exported as JSON and Excel (.xlsx) inside the 'Câu hỏi bài đọc' folder. Target output language is 100% Accented Vietnamese.
---

# 3-Question Reading Check Generator Skill — Rikkei Education Standards

This document defines the technical standards for the **`reading_questions_generator`** skill, responsible for generating **3 reading comprehension check questions** directly from `reading.html`.

---

## 0. PEDAGOGICAL PHILOSOPHY (ANTI-AI SHORTCUT QUESTIONING)

1. **Must-Read Mandatory Requirement (Anti-AI Rule)**:
   - 100% of questions and options MUST link directly to specific examples, syntax, data values, or Gotchas presented in `reading.html`.
   - Students CANNOT answer using generic AI shortcuts without reading the document.

2. **Decoupled Architecture from Lesson Quizzes**:
   - `Reading Check Questions`: 3 multiple-choice check questions evaluating comprehension immediately post-reading (`reading_questions.json` & `Cau_hoi_bai_doc.xlsx` saved in `Câu hỏi bài đọc/`).
   - `Lesson Quiz`: Comprehensive assessment quiz evaluating overall lesson competency (saved in `Câu hỏi Quizz/`).

---

## 1. 3-QUESTION MATRIX

|   #   | Question Type           | Content & Evaluation Objective                          | Data Source in `reading.html`                                 |
| :---: | :---------------------- | :------------------------------------------------------ | :------------------------------------------------------------ |
| **1** | **Concept & Syntax**    | Evaluate core concept or syntax introduced in lesson    | Section 1 (`#problem-intro`) or Section 2 (`#data-structure`) |
| **2** | **Mechanism & Gotchas** | Evaluate underlying mechanism or common gotchas         | Section 2 (`#data-structure`) or Section 4 (`#summary-notes`) |
| **3** | **Code Reading & I/O**  | Evaluate code output prediction based on sample snippet | Section 3 (`#interactive-demo`)                               |

---

## 2. OUTPUT FORMAT STANDARDS

### 2.1 JSON Schema (`reading_questions.json`)

```json
[
  {
    "question_num": 1,
    "question": "Scenario question content based on reading...",
    "options": {
      "A": "Distractor option 1",
      "B": "Correct answer option",
      "C": "Distractor option 2",
      "D": "Distractor option 3"
    },
    "correct_answer": "B",
    "explanation": "Detailed explanation citing reading section..."
  },
  {
    "question_num": 2,
    "question": "Mechanism / Gotchas question content...",
    "options": {
      "A": "Correct answer option",
      "B": "Distractor option 1",
      "C": "Distractor option 2",
      "D": "Distractor option 3"
    },
    "correct_answer": "A",
    "explanation": "Detailed explanation..."
  },
  {
    "question_num": 3,
    "question": "Given the following Python code... What is the output?",
    "options": {
      "A": "Distractor option 1",
      "B": "Distractor option 2",
      "C": "Correct answer option",
      "D": "Distractor option 3"
    },
    "correct_answer": "C",
    "explanation": "Detailed step-by-step execution explanation..."
  }
]
```

### 2.2 Excel Export Schema (`Cau_hoi_bai_doc.xlsx`)

- Columns: `STT` (Index), `Nội dung câu hỏi` (Question Content), `Đáp án A` (Option A), `Đáp án B` (Option B), `Đáp án C` (Option C), `Đáp án D` (Option D), `Đáp án đúng` (Correct Answer), `Giải thích chi tiết` (Detailed Explanation).
- Header styling: `#1E293B` (Dark Slate) fill, white bold centered text.

---

## 3. LESSON FOLDER STRUCTURE LOCATION

```text
📁 Lesson XX - [Tên Bài Học]/
├── 📂 Bài đọc/
│   └── 📄 reading.html
├── 📂 Câu hỏi bài đọc/
│   ├── 📄 Cau_hoi_bai_doc.xlsx
│   └── 📄 reading_questions.json
├── 📂 Câu hỏi Quizz/
│   └── 📄 quiz.json
└── 📂 Video/
    └── 📄 SCRIPT.md
```

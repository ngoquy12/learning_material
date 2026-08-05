# E-learning Quiz & Session Assessment Design Skill — Rikkei Education Standards

This skill guides the AI Agent to design, standardize, and generate multiple-choice quiz question banks (including 5-question Lesson Quizzes and 45-question Session Entrance/Exit Quizzes) for E-learning platforms, strictly adhering to pedagogical standards and export schema requirements. Target output language is 100% Accented Vietnamese.

---

## 🎯 1. Core Pedagogical Principles for Quiz Design

When generating any multiple-choice question, the Agent MUST strictly adhere to these 7 pedagogical principles:

1. **Single Concept Principle:** Each question MUST evaluate exactly one technical concept or skill. Ensure code snippets or context do not contain unrelated syntax bugs so students focus solely on the tested issue.
2. **Context-Driven Principle:** Avoid dry theoretical definitions ("What does the break keyword do?"). Instead, place the student in a concrete technical scenario.
3. **Plausible Distractors Principle:** Incorrect options MUST be plausible and based on real student misconceptions (e.g. infinite loops, off-by-one errors). FORBIDDEN to use trivial distractors or "All of the above are correct/incorrect".
4. **Homogeneity Principle:** All 4 answer choices (A, B, C, D) MUST be homogeneous in length, grammatical structure, and scope. Prevent students from guessing the correct answer based on length.
5. **No Clues Principle:** Eliminate keyword matching clues between question text and correct answer.
6. **Objectivity & Contextual Integrity:** Questions MUST be stated objectively like a standardized national exam. FORBIDDEN vague references ("in the video", "instructor said", "slide mentions").
7. **Dynamic Progressive Scope Boundary:** 100% of questions MUST be strictly within the scope of currently taught and previous lessons. FORBIDDEN to include future topics, unlearned frameworks, or out-of-scope concepts.

---

## 📚 2. Exam Structure & Bloom Difficulty Matrix

The system supports 2 levels of multiple-choice assessment:

### 2.1. Lesson Quiz - 5 Questions
Every theoretical lesson quiz deck MUST contain exactly 5 questions following this Bloom matrix:
1. **Q1: Definition / Syntax (Remember)**: Check declaration syntax, library names, basic parameters.
2. **Q2: Mechanism / Flow (Understand)**: Check execution order of server, middleware, router, or DB query.
3. **Q3: Code Reading (Apply)**: Provide short code snippet and ask for return value or syntax error.
4. **Q4: Comparison (Analyze)**: Compare two approaches (e.g. Path params vs Query params, Async vs Sync).
5. **Q5: Edge Case Trap Prediction (Evaluate)**: Complex code snippet containing subtle logic traps to evaluate deep understanding.

### 2.2. Session Quiz - 45 Questions
Divided into 2 exam types:

#### A. Entrance Quiz
*Evaluates previous lesson retention (practical problem-solving focus) combined with new lesson warm-up.*
* **45-Question Distribution**: **30 Old Lesson questions** and **15 New Lesson questions** (2:1 ratio).
* **30 Old Lesson Questions**:
  1. *Q1 - 12 (12 questions): Advanced Application*: category: `"BÀI CŨ"`, difficulty: `4`.
  2. *Q13 - 21 (9 questions): Deep Analysis (Debug)*: category: `"BÀI CŨ"`, difficulty: `6`.
  3. *Q22 - 30 (9 questions): Creation (Optimization & Security)*: category: `"BÀI CŨ"`, difficulty: `8`.
* **15 New Lesson Questions**:
  4. *Q31 - 36 (6 questions): Understanding*: category: `"BÀI MỚI"`, difficulty: `5`.
  5. *Q37 - 42 (6 questions): Basic Application*: category: `"BÀI MỚI"`, difficulty: `7`.
  6. *Q43 - 45 (3 questions): Basic Analysis*: category: `"BÀI MỚI"`, difficulty: `9`.

#### B. Exit Quiz
*Measures immediate knowledge absorption and practical application durability at the end of class.*
* **45-Question Distribution**: All 45 questions belong to **New Lesson** (Category: `BÀI MỚI`).
  1. *Q1 - 18 (18 questions): Advanced Application*: difficulty: `6`.
  2. *Q19 - 33 (15 questions): Deep Analysis (Debug)*: difficulty: `10`.
  3. *Q34 - 45 (12 questions): Creation (Create)*: difficulty: `11`.

---

## 📊 3. Export Excel Template Format

### 3.1. Export Naming Convention
Exported Excel files MUST strictly follow this naming convention:
* **Entrance Quiz:** `SessionXX._Quizz_Dau_Gio_<New_Lesson_Slide_Title>.xlsx`
* **Exit Quiz:** `SessionXX._Quizz_Cuoi_Gio_<New_Lesson_Slide_Title>.xlsx`

### 3.2. Flat Data Table Structure (13 Columns)

| # | Column Name in Excel   | Data Type | Description                                                             |
| :- | :--------------------- | :-------- | :---------------------------------------------------------------------- |
| 1  | `STT`                  | Number    | Sequential number 1 to 45.                                              |
| 2  | `question_content`     | Text      | Concise, real-world question text.                                      |
| 3  | `answer_1`             | Text      | Option 1 text (strip A., B. prefixes if present).                       |
| 4  | `explanation_answer_1` | Text      | Explanation why option 1 is correct or incorrect.                       |
| 5  | `answer_2`             | Text      | Option 2 text.                                                          |
| 6  | `explanation_answer_2` | Text      | Explanation why option 2 is correct or incorrect.                       |
| 7  | `answer_3`             | Text      | Option 3 text.                                                          |
| 8  | `explanation_answer_3` | Text      | Explanation why option 3 is correct or incorrect.                       |
| 9  | `answer_4`             | Text      | Option 4 text.                                                          |
| 10 | `explanation_answer_4` | Text      | Explanation why option 4 is correct or incorrect.                       |
| 11 | `isCorrect`            | Number    | Index of correct answer (`1` for A, `2` for B, `3` for C, `4` for D).   |
| 12 | `difficulty`           | Number    | Question difficulty on a scale from `1` to `11`.                       |
| 13 | `category`             | Text      | Source classification: `"BÀI CŨ"` or `"BÀI MỚI"`.                       |

---

## 💻 4. Code Styling Guidelines in Questions

When generating code snippets inside `question_content`, options, or explanations:
1. **Source Code Identifiers:** 100% of variable, function, class, and attribute names MUST be in **English**.
2. **Naming Conventions:**
   * Use **`snake_case`** for Python/Database variables and functions (`user_id`, `get_active_users`).
   * Use **`camelCase`** or **`PascalCase`** for JavaScript/TypeScript/Java (`userId`, `fetchData`).
3. **Indentation:**
   * Maintain consistent 4-space indentation for block structures. Never concatenate multi-line code into a single line. Use explicit `\n` linebreaks.



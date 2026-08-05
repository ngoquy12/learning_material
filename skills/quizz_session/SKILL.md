---
name: quizz_session
description: Generate comprehensive session-level entrance and exit quizzes based on current and previous lesson topics, formatted as 13-column flat structures. Target output language is 100% Accented Vietnamese.
---

# Session Quiz Generator Skill — Rikkei Education Standards

## 1. Objective
Design and structure 2 flat-structured multiple-choice exam decks (Entrance Quiz - 45 questions and Exit Quiz - 45 questions). Ensure proper Bloom's taxonomy difficulty distribution and new/old lesson question allocation ratios.

## 2. Content & Question Allocation Standards (45 Questions)

### 2.1. Entrance Quiz
Evaluates previous lesson knowledge retention (2/3 ratio) combined with new lesson warm-up (1/3 ratio) to control self-study discipline.
* **30 Old Lesson Questions**:
  - `STT 1-12 (12 questions)`: Advanced Application | difficulty: `4`.
  - `STT 13-21 (9 questions)`: Debug & Error Analysis | difficulty: `6`.
  - `STT 22-30 (9 questions)`: Optimization & Security | difficulty: `8`.
* **15 New Lesson Questions**:
  - `STT 31-36 (6 questions)`: Mechanical Understanding | difficulty: `5`.
  - `STT 37-42 (6 questions)`: Basic Application | difficulty: `7`.
  - `STT 43-45 (3 questions)`: Basic Analysis | difficulty: `9`.

### 2.2. Exit Quiz
Measures immediate in-class knowledge absorption and application for the new lesson.
* **45 New Lesson Questions**:
  - `STT 1-18 (18 questions)`: Enterprise Application | difficulty: `6`.
  - `STT 19-33 (15 questions)`: Debug & Code Fixes | difficulty: `10`.
  - `STT 34-45 (12 questions)`: Creation & Optimization | difficulty: `11`.

## 3. Distractor Standards & Language Tone
* **Homogeneous Options**: All 4 options (A, B, C, D) MUST have comparable lengths and structures.
* **Plausible Distractors**: Incorrect options MUST reflect real-world developer errors (e.g., bad import path, missing await, decorator syntax error).
* **Tone**: Objective and neutral. FORBIDDEN vague references ("in the video", "in this lesson").
* **Output**: JSON question array matching 13-column Excel template.

---

## 4. Code Styling Guidelines in Questions
When generating code snippets inside `question_content`, options, or explanations:
* **Identifiers**: 100% of variable, function, class, and property names MUST be in **English**.
* **Naming Conventions**:
  - Use **`snake_case`** for Python/Database (`user_id`, `get_active_users`).
  - Use **`camelCase`** or **`PascalCase`** for JavaScript/TypeScript/Java (`userId`, `fetchData`).
* **Indentation**:
  - Ensure consistent 4-space indentation. Never concatenate multi-line code into a single line. Use explicit `\n` linebreaks.



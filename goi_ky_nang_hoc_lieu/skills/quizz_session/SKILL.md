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

- **30 Old Lesson Questions**:
  - `STT 1-12 (12 questions)`: Advanced Application | difficulty: `4`.
  - `STT 13-21 (9 questions)`: Debug & Error Analysis | difficulty: `6`.
  - `STT 22-30 (9 questions)`: Optimization & Security | difficulty: `8`.
- **15 New Lesson Questions**:
  - `STT 31-36 (6 questions)`: Mechanical Understanding | difficulty: `5`.
  - `STT 37-42 (6 questions)`: Basic Application | difficulty: `7`.
  - `STT 43-45 (3 questions)`: Basic Analysis | difficulty: `9`.

### 2.2. Exit Quiz

Measures immediate in-class knowledge absorption and application for the new lesson.

- **45 New Lesson Questions**:
  - `STT 1-18 (18 questions)`: Enterprise Application | difficulty: `6`.
  - `STT 19-33 (15 questions)`: Debug & Code Fixes | difficulty: `10`.
  - `STT 34-45 (12 questions)`: Creation & Optimization | difficulty: `11`.

### 2.3. 15-Question Student Exam Extractor Standard

While the system generates a full 45-question bank for archiving and randomized testing, the **actual student exam paper administered in class consists of EXACTLY 15 questions** extracted according to fixed pedagogical ratios:

1. **Entrance Exam (15 Questions)**:
   - **10 Old Lesson Questions**: 4 Deep Application (from STT 1-12) + 3 Deep Analysis/Debug (from STT 13-21) + 3 Optimization/Security (from STT 22-30).
   - **5 New Lesson Questions**: 2 Mechanical Understanding (from STT 31-36) + 2 Basic Application (from STT 37-42) + 1 Basic Analysis (from STT 43-45).
2. **Exit Exam (15 Questions)**:
   - **15 New Lesson Questions**: 6 Application (from STT 1-18) + 5 Analysis/Debug (from STT 19-33) + 4 Creation/Optimization (from STT 34-45).

### 2.4. Student Capability Classification Matrices

#### A. Entrance Quiz 5-Group Classification Matrix (Total 15 Questions):
- **Gương mẫu (Model Student)**: Score $\ge 13/15$ AND New Lesson $= 5/5$ $\rightarrow$ Outstanding! Assign as Team Leader or assign hard Creative tasks.
- **Nỗ lực (Diligent but Gap)**: Score $7-9/15$ AND New Lesson $\ge 3/5$ $\rightarrow$ Hardworking but gaps in old foundation $\rightarrow$ Remediate old knowledge in class.
- **Tư duy tốt (High Logic, Lazy)**: Score $10-12/15$ AND New Lesson $< 3/5$ $\rightarrow$ Good logic but lazy $\rightarrow$ Warning on self-study discipline.
- **Nguy cơ (At-Risk)**: Score $< 7/15$ $\rightarrow$ Weak in both $\rightarrow$ Require 1:1 Mentoring or TA support.
- **Ổn định (Stable/Average)**: Score $10-12/15$ AND New Lesson $\ge 3/5$ $\rightarrow$ Average group $\rightarrow$ Push to Model group.
- **Ẩn mình (Hidden Potential)**: Score $7-9/15$ AND New Lesson $< 3/5$ $\rightarrow$ Smart but lacks discipline $\rightarrow$ Re-read materials in class.

#### B. Exit Quiz 4-Group Classification Matrix (Total 15 Questions):
- **Làm chủ (Mastery)**: Score $13-15/15$ $\rightarrow$ Assign project-based homework, assign as TA mentor for weak group.
- **Đạt (Proficient)**: Score $10-12/15$ $\rightarrow$ Require writing code comments/documentation, assign advanced homework.
- **Cơ bản (Basic)**: Score $7-9/15$ $\rightarrow$ Require re-doing lab from scratch without sample code.
- **Cần kèm (Needs Mentoring)**: Score $< 7/15$ $\rightarrow$ 1:1 mentoring by TA/Instructor immediately after class.

## 3. Mandatory Quiz Directives & Tone

When generating any question for entrance or exit quizzes, the AI MUST strictly obey these 9 requirements:

1. **Professional Significance:** 100% of question content MUST target core technical concepts and practical developer scenarios.
2. **Anti-Generic (Non-Googleable):** NO generic outside knowledge that students can Google without taking the course.
3. **Concrete Scenarios:** Questions revolve around real-world technical problems and concrete code/configuration examples.
4. **STRICT PROHIBITION OF CONTEXT/SOURCE REFERRAL PHRASES (CRITICAL):**
   - ABSOLUTELY FORBIDDEN to use intermediate context or source referral phrases in question stems, answer choices, or explanations, such as: `"in the slide"`, `"on slide"`, `"lecture slide"`, `"slide mentions"`, `"in the lecture"`, `"according to the lecture"`, `"according to the video"`, `"in the video"`, `"from the instructor"`, `"instructor said"`, `"According to Section ..."`, `"in enterprise scenario ..."`, `"in the scenario"`, `"from an unknown source"`, etc.
   - All questions, options, and explanations MUST be stated 100% objectively, independently, and professionally.
5. **Plausible Distractors:** Incorrect options MUST reflect real-world developer errors or syntax traps. FORBIDDEN: `"All of the above are correct"` or `"All of the above are incorrect"`.
6. **Option Homogeneity (Equal Length):** All 4 choices (A, B, C, D) MUST have comparable text length and structure.
7. **No Clues:** Remove keyword matching clues between question stem and options.
8. **Random Correct Answer Placement:** Randomly assign the correct choice across options A, B, C, D (or `answer_1` through `answer_4` shuffled at post-processing).
9. **Output:** Clean JSON array adhering to 13-column Excel export structure.

---

## 4. Code Styling Guidelines in Questions

When generating code snippets inside `question_content`, options, or explanations:

- **Identifiers**: 100% of variable, function, class, and property names MUST be in **English**.
- **Naming Conventions**:
  - Use **`snake_case`** for Python/Database (`user_id`, `get_active_users`).
  - Use **`camelCase`** or **`PascalCase`** for JavaScript/TypeScript/Java (`userId`, `fetchData`).
- **Indentation**:
  - Ensure consistent 4-space indentation. Never concatenate multi-line code into a single line. Use explicit `\n` linebreaks.


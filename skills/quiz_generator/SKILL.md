# E-learning Quiz & Session Assessment Design Skill — Rikkei Education Standards

This skill guides the AI Agent to design, standardize, and generate multiple-choice quiz question banks (including 5-question Lesson Quizzes and 45-question Session Entrance/Exit Quizzes) for E-learning platforms, strictly adhering to pedagogical standards (`RE_Tiêu chuẩn quizz.pdf`) and export schema requirements. Target output language is 100% Accented Vietnamese.

---

## 🎯 1. Core Pedagogical & Quality Directives for Quiz Design

When generating any multiple-choice question (Lesson Quiz or Session Entrance/Exit Quiz), the Agent MUST strictly enforce these 9 mandatory requirements from `RE_Tiêu chuẩn quizz.pdf`:

1. **Single Concept (Nguyên tắc đơn nhiệm):** Each question MUST evaluate EXACTLY ONE technical concept or skill. Do not combine multiple unrelated bugs or concepts into a single question.
2. **Context-Driven (Ngữ cảnh hóa):** Frame questions inside concrete real-world developer scenarios (Scenario-based). ABSOLUTELY FORBIDDEN to ask dry textbook definitions (e.g., FORBIDDEN: *"What is the break statement used for?"*; REQUIRED: *"You are iterating through a list of 1M users to find the first user with spending > 10M. Which statement immediately stops the loop to optimize performance?"*).
3. **Plausible Distractors (Phương án nhiễu thông minh):** Incorrect choices MUST be plausible and based on real student misconceptions or common syntax/logic traps (e.g., infinite loop, off-by-one errors). ABSOLUTELY FORBIDDEN options: _"All of the above"_, _"None of the above"_, _"Cả 3 đáp án trên đều sai"_, _"Tất cả đều đúng"_.
4. **Homogeneity (Đồng nhất):** All 4 choices (A, B, C, D) MUST have comparable text length, grammatical structure, and detail level. Prevent guessing correct choices based on length.
5. **No Clues (Không mách nước):** Eliminate keyword matching clues between question stem and correct answer choice. Avoid grammar clues.
6. **Instant Feedback (Phản hồi tức thì):** Include a short, punchy explanation for why the correct choice is right and how to fix common misconceptions.
7. **30-Second Rule (Nguyên tắc 30 giây/câu):** Questions must be concise and straight to the point so students who studied the lesson can answer within 30 seconds.
8. **NO CONTEXT REFERRAL PHRASES:**
   - ABSOLUTELY FORBIDDEN to use intermediate context or source referral phrases in question stems, answer choices, or explanations: `"in the slide"`, `"on slide"`, `"lecture slide"`, `"slide mentions"`, `"in the lecture"`, `"according to the lecture"`, `"according to the video"`, `"in the video"`, `"from the instructor"`, `"instructor said"`, `"According to Section ..."`, `"in enterprise scenario ..."`, `"in the scenario"`, `"from an unknown source"`, etc.
   - All questions, choices, and explanations MUST be stated 100% objectively, independently, and professionally as standard domain knowledge.
9. **Domain-Agnostic Standard (Cấm Hardcode theo Môn):**
   - MUST be 100% domain-agnostic and dynamically adapt to `tech_stack` (Python, JS, Java, C++, SQL, Git, Docker, HTML/CSS, etc.).
   - NEVER hardcode a specific technology in generic prompts or skill files.

---

---

## 📚 2. Lesson Quiz Standard — 5 Questions Matrix & Enhanced Schema

Every theoretical lesson quiz deck MUST contain **EXACTLY 5 questions** strictly adhering to the 5 STT structure defined in `RE_Tiêu chuẩn quizz.pdf`:

| STT | Dạng câu (question_type) | Mục tiêu đánh giá (Pedagogical Goal) | Ví dụ minh họa (Domain-Agnostic Example) |
| :-: | :--- | :--- | :--- |
| **1** | `SYNTAX` | Nhận diện thành phần bắt buộc, cú pháp chuẩn của ngôn ngữ / công nghệ. | "Đâu là cú pháp khởi tạo đúng của [Công nghệ X]?" |
| **2** | `EXECUTION_FLOW` | Hiểu cơ chế hoạt động cơ bản và luồng chạy (Execution flow) của mã nguồn / quy trình. | "Trong cấu trúc X, khối lệnh Y được thực thi mấy lần / khi nào nếu điều kiện Z?" |
| **3** | `CODE_TRACE` | Đọc hiểu code cơ bản, trace biến và xác định giá trị đầu ra của đoạn code mẫu. | "Cho đoạn code `int i=0; while(i<3){ i++; }`. Giá trị của `i` sau khi kết thúc là bao nhiêu?" |
| **4** | `COMPARISON` | Tránh nhầm lẫn giữa các cấu trúc, lệnh hoặc tính ứng dụng. | "Điểm khác biệt lớn nhất giữa A và B khi giải quyết bài toán Y là gì?" |
| **5** | `TRAP_PREDICTION` | Kiểm tra sự tỉ mỉ, phát hiện bẫy logic / bẫy cú pháp / lỗi lặp vô tận / biến không thay đổi. | "Chuyện gì xảy ra nếu các biến tham gia điều kiện vòng lặp không thay đổi giá trị trong thân vòng lặp?" |

### 2.1. Required JSON Schema Fields for Each Question

1. `stt`: Integer from `1` to `5`.
2. `question_type`: Enum string (`SYNTAX`, `EXECUTION_FLOW`, `CODE_TRACE`, `COMPARISON`, `TRAP_PREDICTION`).
3. `question`: String containing scenario-based question stem with Markdown code fences/backticks.
4. `options`: List of 4 homogeneous string options.
5. `correct_option_index`: Integer `0`, `1`, `2`, or `3`.
6. `explanation`: Detailed technical explanation of why the correct option is right.
7. `instant_feedback`: Short, punchy pedagogical guidance when a student picks an incorrect option, explicitly pointing them back to the relevant section or concept in the lesson reading text (e.g., *"Chưa chính xác! Bạn hãy tham khảo lại Mục 2.1 trong bài đọc để hiểu rõ hơn về cú pháp khai báo..."*).
8. `time_limit_sec`: Fixed integer `30` (30 seconds per question rule).

---

## 💻 3. Code Styling & Markdown Formatting Guidelines in Questions

When generating code snippets or code symbols inside `question`, `options`, `explanation`, or `instant_feedback`:

1. **Fenced Multi-Line Code Blocks (` ```{lang}\n ... \n``` `)**:
   - All multi-line code snippets MUST be formatted inside Markdown fenced code blocks specifying the exact target language tag `{lang}` (dynamically derived from `tech_stack`, e.g., ````python ... ``` `, ````javascript ... ``` `, ````java ... ``` `, ````sql ... ``` `, ````bash ... ``` `).
   - Multi-line code statements MUST use explicit linebreaks (`\n`) and consistent 4-space indentation for block structures. Never flatten multi-line code into a single line.

2. **Inline Code Symbols (`` `code` ``)**:
   - All inline variable names, function names, keywords, parameter names, and syntax tokens MUST be wrapped in single backticks (e.g. `` `order_amount` ``, `` `is_vip` ``, `` `if-else` ``, `` `SELECT * FROM users` ``).

3. **Source Code Identifiers:** 100% of variable, function, class, and attribute names MUST be in **English**.
4. **Naming Conventions:**
   - Use **`snake_case`** for Python/Database variables and functions (`user_id`, `order_amount`).
   - Use **`camelCase`** or **`PascalCase`** for JavaScript/TypeScript/Java (`userId`, `fetchData`).


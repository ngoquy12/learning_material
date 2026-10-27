---
name: lab_generator
description: Structure practical hands-on labs with clear objectives, sequential execution tasks, dynamic stack adaptation, and quantitative evaluation checklists, exported as Markdown (practical_lab.md) inside the 'Bài thực hành' folder. Target output language is 100% Accented Vietnamese.
---

# Hands-on Lab Generator Skill — Rikkei Education Standards

## 1. Overview & Pedagogical Vision
Hands-on Labs serve as the practical backbone for students to develop real-world coding skills and build modular components for enterprise projects. Every Lab MUST adapt strictly to the lesson's target `tech_stack`, featuring clear objectives and step-by-step executable instructions.

### 1.1 Progressive Difficulty Contract (Beginner-First, Simple -> Advanced)
- The task's overall difficulty MUST be calibrated to what the student has ACTUALLY learned up to and including the current lesson (`allowed_scope`) — never assume mastery of concepts from later lessons.
- The step sequence (`steps`) MUST itself escalate gradually: early steps cover the simplest possible setup/single-value handling of the scenario, later steps layer in the lesson's new concept, and only the final step(s) may approach a fuller, more complete business scenario. Never open Step 1 with the full multi-field/multi-branch complexity that belongs at the end.
- `code_demo` MUST mirror this same step progression — the reference solution should read as an incremental build-up (simple -> complete), not a monolithic advanced solution dropped all at once.
- Avoid stacking every business rule/edge case into a single task for early sessions of a course; edge cases and advanced rules are appropriate once the course has progressed and students have more foundation.

### 1.2 Session-Wide Domain Persistence Contract
- The unified business domain (`chosen_domain`) is fixed for the ENTIRE SESSION, not just the current lesson — every lab inside the same session MUST reuse the exact same domain/business scenario family (see the `UNIFIED SESSION BUSINESS DOMAIN CONTRACT` block in the prompt) so the practical work across a session reads as one continuous project instead of disconnected, unrelated exercises.

## 2. Output File Standard (`practical_lab.md`)
The hands-on practical lab MUST be formatted as a clean Markdown document saved at `Bài thực hành/practical_lab.md`.

```markdown
# Bài thực hành: [Tên kịch bản doanh nghiệp thực tế]

## 1. Mục tiêu
- [Mục tiêu 1: Kỹ năng đạt được...]
- [Mục tiêu 2: Vận dụng công nghệ...]
- [Mục tiêu 3: Kiểm chuẩn kết quả...]

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: [Mô tả môi trường, cấu hình và dữ liệu đầu vào...]

### Các bước thực hiện:
1. **Bước 1: Khởi tạo và thiết lập**: [Hướng dẫn bước 1...]
2. **Bước 2: Xây dựng logic nghiệp vụ**: [Hướng dẫn bước 2...]
3. **Bước 3: Định dạng & Kiểm lỗi**: [Hướng dẫn bước 3...]

## 3. Checklist đánh giá
- [ ] [Tiêu chí kiểm định 1...]
- [ ] [Tiêu chí kiểm định 2...]
- [ ] [Tiêu chí kiểm định 3...]
```

## 3. Worked Exemplar (Few-Shot)

The template in Section 2 shows the skeleton; this section shows one fully written lab so the
Progressive Difficulty Contract is visible in practice rather than only described in prose.

> Follow the SHAPE, not the subject. The stack and domain below are illustrative — the same
> structure must hold for any `tech_stack` and any `chosen_domain`.

**Input contract given to the agent:**

- `chosen_domain`: Hotel Booking
- `tech_stack`: python/core
- `allowed_scope`: biến, kiểu dữ liệu, toán tử, câu lệnh `if/else`
- `forbidden_scope`: vòng lặp, hàm, danh sách, từ điển

**Correct output:**

```markdown
# Bài thực hành: Tính phí đặt phòng cho một lượt khách

## 1. Mục tiêu
- Khai báo và gán giá trị cho biến mô tả một lượt đặt phòng.
- Vận dụng câu lệnh `if/else` để chọn mức giá theo số đêm nghỉ.
- Kiểm chuẩn kết quả in ra khớp với bảng giá đã cho.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Một lượt đặt phòng gồm số đêm nghỉ và giá phòng mỗi đêm là 500000 đồng. Khách nghỉ từ 3 đêm trở lên được giảm 10% trên tổng tiền.

### Các bước thực hiện:
1. **Bước 1: Khởi tạo và thiết lập**: Khai báo biến `nights` với giá trị 2 và biến `price_per_night` với giá trị 500000. In ra tổng tiền chưa giảm giá.
2. **Bước 2: Xây dựng logic nghiệp vụ**: Dùng `if/else` kiểm tra `nights` có từ 3 trở lên hay không để tính `total_price` tương ứng có giảm giá hoặc không.
3. **Bước 3: Định dạng & Kiểm lỗi**: Đổi `nights` lần lượt thành 3 rồi thành 0, chạy lại và đối chiếu kết quả với bảng giá.

## 3. Checklist đánh giá
- [ ] Chương trình chạy không lỗi cú pháp với cả ba giá trị `nights` là 2, 3 và 0.
- [ ] Với `nights` bằng 2, kết quả in ra đúng 1000000.
- [ ] Với `nights` bằng 3, kết quả in ra đúng 1350000 (đã giảm 10%).
- [ ] Toàn bộ tên biến viết bằng tiếng Anh theo `snake_case`.
```

### 3.1 What this exemplar demonstrates

| Rule | How the exemplar satisfies it |
| :-- | :-- |
| Progressive difficulty | Bước 1 chỉ gán biến và in ra -> Bước 2 mới thêm rẽ nhánh -> Bước 3 mới thử giá trị biên. Bước 1 không mở màn bằng toàn bộ nghiệp vụ. |
| Scope boundary | Chỉ dùng biến, toán tử và `if/else`. Không có vòng lặp, hàm, danh sách — dù chúng sẽ khiến bài "đẹp" hơn, đó là kiến thức CHƯA dạy. |
| Domain persistence | Toàn bộ bài nằm trong đúng bối cảnh Hotel Booking, không nhảy sang bối cảnh khác giữa chừng. |
| Checklist đo được | Mỗi mục kiểm định nêu giá trị đầu vào và kết quả mong đợi cụ thể, chấm được đúng/sai — không phải nhận xét cảm tính như "code sạch sẽ". |

> **Ca sai thường gặp:** một lab đúng chủ đề nhưng Bước 1 đã yêu cầu xử lý danh sách nhiều
> lượt đặt phòng. Bài trông chuyên nghiệp hơn, nhưng học viên chưa học danh sách nên tắc
> ngay bước đầu. Vi phạm phạm vi kiến thức luôn nặng hơn việc bài tập trông quá đơn giản.

---

## 4. Code Styling Guidelines in Labs
When providing code snippets or step-by-step code guidance:
* **Identifiers**: 100% of variable, function, class, and property names MUST be in **English**.
* **Naming Conventions**:
  - Use **`snake_case`** for Python / C / SQL (`database_connection`, `get_user_by_email`).
  - Use **`camelCase`** or **`PascalCase`** for JavaScript / TypeScript / Java (`databaseConnection`, `getUserByEmail`).
* **Indentation**:
  - Ensure consistent 4-space indentation for block structures (2 spaces for JS/HTML). Use explicit linebreaks.

## 5. Multi-Step Lab Guide (long form, for a practice session)

When a session is built around several chained labs (for example six labs that match six exercises), write ONE guide `Bai thuc hanh/lab_guide.md` instead of several small files:

1. **Opening**: goal of the session, prerequisites (tools, accounts, versions), and a mapping table lab -> exercise.
2. **One section per lab**, each with: duration, objective, numbered steps (commands and files exactly as run), a block "Kết quả mong đợi" (screen text, server log lines, JSON bodies, table rows) and a short list of common errors with fixes. Labs build on each other and reuse the same files and names.
3. **Closing**: a wrap-up (about 5 minutes), a 10-point rubric, a short "Tự học thêm" line for out-of-scope topics, and an appendix table of files per lab.
4. Every "Kết quả mong đợi" block comes from a REAL run of the exact code in the step. Environment-specific values (database name, port) are replaced with the names the student is told to use.
5. Durations add up to the session length; lab 1 is the simplest and the last lab is the most complete.

## 6. Pre-Delivery Verification Gate (MANDATORY for programming courses)

Root causes of past defects were process gaps, not individual labs: labs written before the readings drifted from them, steps used constructs the course had not taught, expected outputs were guessed.

1. **Order of work**: finish the Lesson readings FIRST. Write labs afterwards, reusing the exact function names, Vietnamese labels, fixed messages and data conventions the readings introduced. Never author a lab from the syllabus alone.
2. **Run it**: execute every step of the lab in a clean copy of the starter, in order, and compare the output with the "Kết quả mong đợi" block. Fix the text, not the output.
3. **Scope**: declare the not-yet-taught constructs for the course (from `forbidden_scope` / the course spec) and run the scope checker over the code the student writes: `python scripts/check_exercise_scope.py <course folder> --forbid <constructs> --language javascript` (it scans `script.js` and `src/**/*.js(x)`). Fix until it reports 0 problems, or state the intentional change in the lab.
4. **Shared base code** is copied verbatim from the earlier lab's solution (same names, same parameter shapes); never re-author helpers per lab.
5. If the checker flags a construct that is genuinely needed, do NOT quietly keep it: teach it in a reading first, or redesign the lab so students never write it.

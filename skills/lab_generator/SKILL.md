---
name: lab_generator
description: Structure practical hands-on labs with clear objectives, sequential execution tasks, dynamic stack adaptation, and quantitative evaluation checklists, exported as Markdown (practical_lab.md) inside the 'Bài thực hành' folder. Target output language is 100% Accented Vietnamese.
---

# Hands-on Lab Generator Skill — Rikkei Education Standards

## 1. Overview & Pedagogical Vision
Hands-on Labs serve as the practical backbone for students to develop real-world coding skills and build modular components for enterprise projects. Every Lab MUST adapt strictly to the lesson's target `tech_stack`, featuring clear objectives and step-by-step executable instructions.

### 1.1 Progressive Difficulty Contract (Beginner-First, Simple ➔ Advanced)
- The task's overall difficulty MUST be calibrated to what the student has ACTUALLY learned up to and including the current lesson (`allowed_scope`) — never assume mastery of concepts from later lessons.
- The step sequence (`steps`) MUST itself escalate gradually: early steps cover the simplest possible setup/single-value handling of the scenario, later steps layer in the lesson's new concept, and only the final step(s) may approach a fuller, more complete business scenario. Never open Step 1 with the full multi-field/multi-branch complexity that belongs at the end.
- `code_demo` MUST mirror this same step progression — the reference solution should read as an incremental build-up (simple ➔ complete), not a monolithic advanced solution dropped all at once.
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

## 💻 3. Code Styling Guidelines in Labs
When providing code snippets or step-by-step code guidance:
* **Identifiers**: 100% of variable, function, class, and property names MUST be in **English**.
* **Naming Conventions**:
  - Use **`snake_case`** for Python / C / SQL (`database_connection`, `get_user_by_email`).
  - Use **`camelCase`** or **`PascalCase`** for JavaScript / TypeScript / Java (`databaseConnection`, `getUserByEmail`).
* **Indentation**:
  - Ensure consistent 4-space indentation for block structures (2 spaces for JS/HTML). Use explicit linebreaks.


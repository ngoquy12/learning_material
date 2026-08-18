---
name: session_mindmap_compiler
description: Synthesize and generate Session-Level Markmap mindmaps (.md format) for 1.5-hour sessions according to Rikkei Education standards, compatible with VS Code Markmap and XMind. Target output language is 100% Accented Vietnamese.
---

# Session Mindmap Compiler Skill — Rikkei Education Standards

## 1. Fixed Mandatory Hierarchy

Every generated session-level mindmap MUST strictly follow this hierarchy in Markdown format for Markmap rendering:

```markmap
# [Clean Session Title - Topic Only]

## Lesson 01 — [Tên Lesson 01]
### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: [Bản chất khái niệm, max 10 từ]
- Vai trò: [Giải quyết vấn đề gì?]
### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
  ```language
  # Cú pháp chuẩn của ngôn ngữ/công nghệ
  ```
- Giải thích thành phần:
  - [Tên thành phần 1]: [Ý nghĩa, kiểu dữ liệu]
  - [Tên thành phần 2]: [Ý nghĩa]
### Ví dụ thực hành
- Kịch bản áp dụng: [Mô tả bối cảnh nghiệp vụ thực tế nhỏ]
  ```language
  # Mã nguồn ví dụ thực tế chạy được (5-8 dòng)
  ```
- Giải thích ví dụ: [Phân tích nhanh luồng chạy]
### Lưu ý triển khai
- **[Tên lỗi phổ biến]**: Tác động/cách khắc phục (cấm dùng từ "thực chiến", "gotcha", "bẫy lỗi").
- **Lưu ý định dạng**: Quy chuẩn đặt tên và thụt lề theo style guide của công nghệ.

## Lesson 02 — [Tên Lesson 02]
...

## Liên kết hệ thống
- Mối quan hệ logic: [Lesson 01] đóng vai trò gì (tiền đề / bổ trợ) cho [Lesson 02]?
- Luồng dữ liệu xuyên suốt: [Đầu ra của Lesson 01] -> làm [Đầu vào của Lesson 02]
- Ứng dụng tổng hợp: [Cách kết hợp cả hai bài học để giải quyết bài toán nghiệp vụ lớn]
```

---

## 2. Heading Hierarchy Rules

- `#` — Session Root Node (Exactly 1 root node containing only clean session topic name).
- `##` — Lesson Nodes + final "Liên kết hệ thống" connection node.
- `###` — 4 Fixed Branch Sub-headings per Lesson.
- `-` (bullet) — Details ≤ 15 words/line, max 3 bullet levels.

---

## 3. Mandatory Structuring & Content Rules

1. **Clean Root Topic Title (`#`)**:
   - MUST contain ONLY the content topic of the session.
   - ABSOLUTELY FORBIDDEN to include prefixes like "Session XX - ", "Session XX: ", or session numbers.
   - Example: `# Cấu trúc điều kiện` (CORRECT) vs `# Session 06 - Cấu trúc điều kiện` (INCORRECT).

2. **No Metadata & Problem Branches**:
   - ABSOLUTELY FORBIDDEN to include "Mục tiêu bài học", "Bài toán", or "Bối cảnh buổi học" branches at the top of the session.
   - For each lesson branch, ABSOLUTELY FORBIDDEN to include "Vấn đề" or "Tại sao cần học" branches. Start directly with the lessons' technical content.

3. **Strict Coding & Naming Conventions**:
   - 100% of code syntax in mindmaps MUST comply with the target `tech_stack` coding rules.
   - For Python: Use `snake_case` for variables/functions, `PascalCase` for classes.
   - For Java/JS: Use `camelCase` for variables/methods, `PascalCase` for classes.
   - ABSOLUTELY FORBIDDEN to use arbitrary variable names like `a`, `b`, `x`, `y`, `temp`. Variable names must represent real business context.

4. **AI Cliché & Academic Jargon Ban**:
   - ABSOLUTELY FORBIDDEN to use informal words ("nhé", "nha", "nhé các bạn") or AI assistant clichés ("thực chiến", "thần thánh", "gotcha", "anti-pattern", "bẫy lập trình"). Use formal, neutral technical language.
   - Keep technical keywords in English, and write explanations in 100% Accented Vietnamese.

5. **Cross-Lesson Integration (`## Liên kết hệ thống`)**:
   - MUST include a final `## Liên kết hệ thống` branch summarizing the dependency flow, input-process-output data mapping, and how the lessons fit together to solve a larger business problem.

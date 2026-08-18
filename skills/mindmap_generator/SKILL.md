---
name: mindmap_generator
description: Generate Lesson-Level Markmap mindmaps synthesizing all lesson knowledge according to Rikkei Education standards. Target output language is 100% Accented Vietnamese.
---

# Lesson-Level Mindmap Generator Skill — Rikkei Education Standards

## 1. Fixed Mindmap Heading & Branching Hierarchy

Every generated mindmap MUST strictly follow this 2-Level hierarchy in Markdown format for Markmap rendering:

```markmap
# [Clean Topic/Content Title]

## Khái niệm & Vai trò
- Định nghĩa ngắn gọn: [Bản chất khái niệm, max 10 từ]
- Vai trò: [Giải quyết vấn đề gì?]

## Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
  ```language
  # Cú pháp chuẩn của ngôn ngữ/công nghệ
  ```
- Giải thích thành phần:
  - [Tên thành phần 1]: [Ý nghĩa, kiểu dữ liệu]
  - [Tên thành phần 2]: [Ý nghĩa]

## Ví dụ thực hành
- Kịch bản áp dụng: [Mô tả bối cảnh nghiệp vụ thực tế nhỏ]
  ```language
  # Mã nguồn ví dụ thực tế chạy được (5-8 dòng)
  ```
- Giải thích ví dụ: [Phân tích nhanh luồng chạy]

## Lưu ý triển khai
- **[Tên lỗi phổ biến]**: Tác động/cách khắc phục (cấm dùng từ "thực chiến", "gotcha", "bẫy lỗi").
- **Lưu ý định dạng**: Quy chuẩn đặt tên và thụt lề theo style guide của công nghệ.

## Liên kết hệ thống
- Mối quan hệ logic: [Nội dung này kế thừa hay bổ trợ cho nội dung nào?]
- Luồng chạy thực tế: [Cách kết hợp các thành phần để hoàn thành luồng dữ liệu]
```

---

## 2. Mandatory Structuring Rules

1. **Level 1 Heading (`#`) — Clean Content Title**:
   - MUST contain ONLY the content topic of the lesson.
   - ABSOLUTELY FORBIDDEN to include prefixes like "Lesson YY - ", "Session XX - ", or codes.
   - Example: `# Vòng lặp for` (CORRECT) vs `# Lesson 02 - Vòng lặp for` (INCORRECT).

2. **Level 2 Headings (`##`) — Structural Branches**:
   - MUST contain exactly the 5 structural branches: `## Khái niệm & Vai trò`, `## Cú pháp & Giải nghĩa`, `## Ví dụ thực hành`, `## Lưu ý triển khai`, and `## Liên kết hệ thống`.
   - ABSOLUTELY FORBIDDEN to include "Mục tiêu bài học", "Bài toán", or "Đặt tình huống" branches.

3. **Leaf Nodes & Content Density**:
   - Nodes MUST be highly condensed and scannable. Keep sentences short (maximum 15 words per leaf node). No long paragraphs.
   - Code blocks must be kept to minimal 5-8 lines of syntax/examples. Never include large, bloated code snippets.

4. **Strict Technology Stack Isolation & Naming Conventions**:
   - 100% of code syntax in mindmaps MUST comply with the target `tech_stack` coding rules.
   - For Python: Use `snake_case` for variables/functions, `PascalCase` for classes.
   - For Java/JS: Use `camelCase` for variables/methods, `PascalCase` for classes.
   - ABSOLUTELY FORBIDDEN to use arbitrary variable names like `a`, `b`, `x`, `y`, `temp`. Variable names must represent real business context.

5. **AI Cliché & Academic Jargon Ban**:
   - ABSOLUTELY FORBIDDEN to use informal words ("nhé", "nha", "nhé các bạn") or AI assistant clichés ("thực chiến", "thần thánh", "gotcha", "anti-pattern", "bẫy lập trình"). Use formal, neutral technical language.
   - Keep technical keywords in English (e.g. `function`, `parameter`, `IndentationError`), and write explanations in 100% Accented Vietnamese.

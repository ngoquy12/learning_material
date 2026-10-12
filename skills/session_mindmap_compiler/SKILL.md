---
name: session_mindmap_compiler
description: Synthesize Session-Level Markmap mindmaps (.md) for 1.5-hour sessions per Rikkei Education standards. Nodes are SHORT keyword phrases (visual-first, little text); the same tree is rendered to Markmap .md, XMind and a self-contained interactive HTML. Target output language is 100% Accented Vietnamese.
---

# Session Mindmap Compiler Skill — Rikkei Education Standards

A mindmap is a visual map, not a summary document. Each node is a short keyword phrase that the
learner scans in one glance. Knowledge coverage stays the same as before; it is expressed in
fewer words, split across more small nodes instead of long sentences.

## 1. Fixed Mandatory Hierarchy

Output ONE Markmap tree (Markdown headings + bullets). Illustrative shape (names and wording are
examples, adapt them to the real content):

```markmap
# Cấu trúc điều kiện

## Lesson 01 — Câu lệnh if
### Khái niệm & vai trò
- Rẽ nhánh theo điều kiện
- Chạy đúng một nhánh
### Cú pháp
- Khai báo: `if (điều kiện) { ... }`
  - Điều kiện: kiểu boolean
  - Khối lệnh: trong dấu `{ }`
### Ví dụ minh họa
- Kịch bản: xếp loại điểm học viên
  ```javascript
  if (studentScore >= 8) grade = "Giỏi";
  ```
- Luồng chạy: kiểm tra từ trên xuống
### Lưu ý triển khai
- **Dùng `=` thay `===`**: gán thay vì so sánh
- Thụt lề 4 khoảng trắng

## Lesson 02 — ...

## Liên kết hệ thống
- Quan hệ: Lesson 01 là tiền đề của Lesson 02
- Luồng dữ liệu: đầu ra bài 1 -> đầu vào bài 2
- Ứng dụng tổng hợp: bài toán nghiệp vụ lớn
```

## 2. Heading Hierarchy Rules (unchanged)

- `#` — Session root (exactly 1; clean topic only).
- `##` — one per Lesson (`Lesson NN — Tên`), then the final `## Liên kết hệ thống`.
- `###` — EXACTLY 4 branches per Lesson. Names (2-4 words) are chosen to fit the lesson; count is fixed.
  Together the 4 branches MUST still cover: (1) concept/purpose, (2) syntax or process mechanics,
  (3) a concrete example, (4) pitfalls/implementation notes.
- `-` bullets — at most 3 bullet levels under a `###`.

## 3. Node Length and Visual Rules (visual-first)

1. **Short nodes**: each node (heading or bullet) is a keyword phrase of at most 8-10 words, no
   full sentences, no trailing explanations, no paragraphs. If an idea needs more words, split it
   into a parent node plus 2-3 child nodes.
2. **Depth**: at most 3 bullet levels below a `###`. Prefer 3-6 sibling nodes per branch; avoid a
   wall of 10+ siblings.
3. **Code is minimal**: code lives ONLY in the example branch (or as an inline `code` span in a
   syntax node). Use either a single inline code span, or one fenced block of 1 line (at most 2-3
   short lines). NEVER a long listing. Inline code spans may be used inside any short node for
   keywords, operators and identifiers.
4. **Labels instead of sentences**: start a node with a short label (1-3 words) followed by a
   colon, then a fragment, e.g. `Khai báo: ...`, `Kịch bản: ...`, `Kết quả: ...`, `Lỗi: ...`,
   `Cách sửa: ...`, `Quy tắc: ...`, `Đầu vào: ...`, `Đầu ra: ...`. The renderer turns such labels
   into coloured tag chips and colours each Lesson branch automatically. Labels are plain text:
   NEVER emojis, icons, symbols or unicode pictograms.
5. **Bold** (`**...**`) only for the name of a common mistake or a key term, at most one per bullet.
6. **Same coverage**: shortening must not drop knowledge. Keep every key concept, rule, syntax
   element, example and pitfall that the lessons teach; only remove filler words.

## 4. Mandatory Structuring & Content Rules (unchanged)

1. **Clean Root Topic Title (`#`)**: ONLY the topic. FORBIDDEN prefixes such as "Session XX - ",
   "Session XX: " or session numbers. Correct: `# Cấu trúc điều kiện`.
2. **No Metadata & Problem Branches**: FORBIDDEN "Mục tiêu bài học", "Bài toán", "Bối cảnh buổi
   học" at session level; FORBIDDEN "Vấn đề" or "Tại sao cần học" branches per lesson. Start
   directly with technical content.
3. **Coding & Naming Conventions**: code follows the target `tech_stack` rules (Python:
   `snake_case` / `PascalCase` classes; Java/JS: `camelCase` / `PascalCase` classes). FORBIDDEN
   arbitrary names like `a`, `b`, `x`, `y`, `temp`; names reflect real business context (and the
   unified business domain when one is given).
4. **No emojis, no clichés**: FORBIDDEN any emoji or pictogram character (including check/cross
   marks and arrows such as ❌ ✅ ⚠️ 🔴 🟢 ▶). FORBIDDEN informal words ("nhé", "nha") and AI
   clichés ("thực chiến", "thần thánh", "gotcha", "anti-pattern", "bẫy lập trình"). Use formal,
   neutral technical Vietnamese; keep technical keywords in English.
5. **Knowledge scope**: only concepts within the allowed taught scope; never leak topics that are
   not yet taught.
6. **Cross-Lesson Integration (`## Liên kết hệ thống`)**: final node covering the dependency flow
   between lessons, input-process-output mapping, and the combined business application, written
   as short nodes.
7. **Language**: all node text in 100% Accented Vietnamese.

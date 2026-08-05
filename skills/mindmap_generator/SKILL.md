---
name: mindmap_generator
description: Generate Session-Level Markmap mindmaps synthesizing all lesson knowledge across the entire session according to Rikkei Education standards. Target output language is 100% Accented Vietnamese.
---

# Session-Level Mindmap Generator Skill — Rikkei Education Standards

## 1. Fixed Mindmap Heading & Branching Hierarchy

Every generated mindmap MUST strictly follow this 3-Level hierarchy in Markdown format for Markmap rendering:

```markmap
# [Clean Topic/Content Title]

## Mục tiêu bài học
- [Objective 1: Measurable outcome]
- [Objective 2: Measurable outcome]
- [Objective 3: Measurable outcome]
- [Objective 4: Measurable outcome]

## Đặt tình huống
- [Real-world business problem or motivation]

## [Lesson 01 Title]
### [Short Dynamic Title 1]
- [Short description/mechanics, max 15 words]
### [Short Dynamic Title 2]
- [Short description or syntax]
  ```python
  # Core syntax template (1-3 lines max)
  ```
### [Short Dynamic Title 3]
*Prompt tạo ảnh: A clean 2D flat vector technical illustration of [Detailed logic/business workflow description here]. Main title in meaningful concise Vietnamese. Strictly NO text emojis. 16:9 aspect ratio, spacious layout with at least 32px safe outer margin on all sides. Minimalist infographics style, clean white background, muted corporate color palette.*
### [Short Dynamic Title 4]
- [Gotcha or best practice, max 15 words]

## [Lesson 02 Title]
...
```

---

## 2. Mandatory Structuring Rules

1. **Level 1 Heading (`#`) — Clean Content Title**:
   - MUST contain ONLY the content topic of the session/lesson.
   - ABSOLUTELY FORBIDDEN to include prefixes like "Session XX - ", "Lesson YY - ", or codes.
   - Example: `# Vòng lặp` (CORRECT) vs `# Session 05 - Vòng lặp` (INCORRECT).

2. **Level 2 Headings (`##`) — Structural Milestones**:
   - Branch 1: `## Mục tiêu bài học` (MUST always be first, outlining 3-4 clear objectives).
   - Branch 2: `## Đặt tình huống` (MUST outline the real-world business context/problem statement).
   - Remaining branches: Each lesson/major topic in the session MUST form a Level 2 branch.

3. **Level 3 Headings (`###`) — Dynamic & Ultra-Concise**:
   - FORBIDDEN to hardcode static titles (e.g. avoid rigidly repeating "Khái niệm thực chiến", "Lưu ý thực chiến" everywhere).
   - Titles MUST be dynamic, flexible, and as short as possible while ensuring correctness and proper spelling (e.g. `Khái niệm`, `Cú pháp`, `Cơ chế`, `Lưu ý`, `So sánh`).

4. **Leaf Nodes & Content Density**:
   - Nodes MUST be highly condensed and scannable. Keep sentences short (maximum 15 words per leaf node). No long paragraphs.
   - Code blocks must be kept to minimal 1-3 lines of syntax patterns. Never include large, bloated code snippets.

5. **2D Flat Vector Visualizations**:
   - For difficult concepts or workflow control, embed standard English image prompts matching `image_prompt_standard`:
     `*Prompt tạo ảnh: A clean 2D flat vector technical illustration of [detailed logic]. Main title in concise Accented Vietnamese. Strictly NO text emojis. 16:9 aspect ratio, spacious layout...*`

6. **Strict Emoji-Free Directive**:
   - 100% FORBIDDEN to use text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶) anywhere in the mindmap text. Only use standard Markdown formatting.

````

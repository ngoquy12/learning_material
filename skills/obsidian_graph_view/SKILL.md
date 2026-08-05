---
name: obsidian_graph_view
description: Establish cross-linked Markdown note structure (WikiLinks) compatible with Obsidian Graph View for full course curriculum visualization. Target output language is 100% Accented Vietnamese.
---

# Obsidian Graph View Generator Skill — Rikkei Education Standards

## 1. Objective & Architecture Vision
When managing large academic curricula, visualizing relationships between Sessions, Lessons, and core learning materials (Readings, Slides, Quizzes, Video Scripts, Mindmaps) is essential.

Obsidian is a powerful local knowledge management engine leveraging cross-linked Markdown notes via `[[Note Title]]` WikiLink syntax. By generating a standardized Obsidian Vault, users can launch Obsidian's **Graph View** to dynamically inspect the course knowledge map.

---

## 2. Cross-Linking Rules (WikiLink Architecture)
Every Markdown file in the Obsidian Vault MUST strictly comply with these naming and cross-linking rules:

### A. Course Homepage (`index.md`)
- Central Hub anchor node for the entire curriculum graph.
- Contains general course metadata and introduction.
- Links to all Sessions: `[[Session 01 - Tên Session]]`, `[[Session 02 - Tên Session]]`,...

### B. Session Note (`Session XX - Tên Session.md`)
- Backlink to homepage: `[[index|🏠 Trang chủ môn học]]`.
- Links to child lessons: `[[Lesson XX.Y - Tên Lesson]]`.
- Links to session quizzes: `[[Session XX - Entrance Quiz]]` and `[[Session XX - Exit Quiz]]`.

### C. Lesson Note (`Lesson XX.Y - Tên Lesson.md`)
- Backlink to parent session: `[[Session XX - Tên Session|⬅️ Session XX]]`.
- Links to 4 core lesson resources:
  - Reading Material: `[[Lesson XX.Y - Reading]]`
  - Lecture Deck: `[[Lesson XX.Y - Slides]]`
  - Mindmap: `[[Lesson XX.Y - Mindmap]]`
  - Video Script: `[[Lesson XX.Y - Video Script]]`

### D. Component Resource Note
- Backlink to parent lesson: `[[Lesson XX.Y - Tên Lesson|↩️ Bài học chính]]`.

---

## 3. Vault Folder Hierarchy

```text
obsidian_vault/
├── index.md (Course Homepage Hub)
├── Session 01 - Tên Session/
│   ├── Session 01 - Tên Session.md
│   ├── Session 01 - Entrance Quiz.md
│   ├── Session 01 - Exit Quiz.md
│   ├── Lesson 01.1 - Tên Lesson/
│   │   ├── Lesson 01.1 - Tên Lesson.md
│   │   ├── Lesson 01.1 - Reading.md
│   │   ├── Lesson 01.1 - Slides.md
│   │   ├── Lesson 01.1 - Mindmap.md
│   │   └── Lesson 01.1 - Video Script.md
```

---

## 4. Metadata Standard (YAML Frontmatter)
Every Markdown file MUST include YAML frontmatter:
```markdown
---
type: [course | session | lesson | reading | slide | quiz | mindmap | video]
id: [Corresponding Identifier]
title: [Full Title]
tags:
  - learning-material
  - obsidian-graph
---
```

This structure enables users to filter and color-code graph nodes in Obsidian Graph View by resource type (e.g. purple for Slides, red for Quizzes, green for Readings).


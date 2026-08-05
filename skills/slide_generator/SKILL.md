---
name: slide_generator
description: Generate rich, interactive master HTML slide decks adhering to the 8 Golden Rules, 8 dynamic layouts, Action Headlines, Mermaid diagrams, VS Code dark code boxes, clean typography, SVG icons, and Rikkei Education brand identity. Target output language is 100% Accented Vietnamese.
---

# Master HTML Slide Generator Skill — Rikkei Education Standards

## 1. Pedagogical Vision & 8 Golden Rules for Lecture Slides

Lecture slides serve as a **Visual Facilitation Tool** for instructors during a 1.5-hour session. Slides are NOT a text-heavy textbook; they must be concise, crisp, and high-impact.

> [!IMPORTANT]
> **8 MANDATORY GOLDEN RULES FOR SLIDE GENERATION:**
>
> 1. **Cognitive Load Control (Slide Count Limit - 15 to 20 Slides/Session)**:
>    - ABSOLUTELY FORBIDDEN to create bloated 50-70 slide decks causing cognitive overload.
>    - A 1.5-hour Session MUST contain **maximum 15 - 20 focus slides**. Each Lesson consists of **3 - 4 high-quality slides**:
>      - _Slide 1: Problem & Hook (Real-world enterprise scenario)_.
>      - _Slide 2: Core Concept & Visual Diagram (Concepts & flowcharts)_.
>      - _Slide 3: Code Demo Explainer / Live Playground (Production code)_.
>      - _Slide 4: Pitfalls & Summary (Gotchas & Summary)_.
> 2. **Cover Slide (Slide 1)**:
>    - **Red Tag**: Display Session Name (e.g. `Session 01` in red `#be111c`, Montserrat/Inter font).
>    - **Main Title**: Remove the word "Session" from title (e.g. `Giới thiệu Python và Thiết lập môi trường` in dark `#0f172a`).
>    - **Course Name**: Actual course title (e.g., `Môn học: Lập trình Python`). FORBIDDEN uppercase or wrong branding.
> 3. **Session Agenda Slide (Slide 2)**:
>    - List all lessons in numbered sequence (`01. Lesson 01 - ...`, `02. Lesson 02 - ...`).
>    - Agenda Title: **`NỘI DUNG BÀI HỌC`** (Montserrat Bold 36px, red `#be111c`). Lesson titles in large font (24px - 28px).
> 4. **Lesson Content Large Title (From Slide 3 Onward)**:
>    - Main title on content slides MUST be **Lesson Name hyphenated with Slide Index** (e.g. `Lesson 01 - Giới thiệu ngôn ngữ Python - 1`).
>    - Font: Brand red `#be111c`, size **28px** (Montserrat Bold).
> 5. **Subtitle / Sub-heading (Content Slide Subtitle)**:
>    - Subtitle directly below main title specifies slide topic (e.g. `Đặt vấn đề & Bối cảnh thực tế doanh nghiệp`).
>    - Font: **BLACK (`#0f172a`)**, size **20px** (Inter Bold). FORBIDDEN repeating main title or redundant prefixes.
> 6. **Typography Scaling (3-30-300 Rule)**:
>    - **Body Text**: Size **18px** (Inter Medium/Regular).
>    - **Sub-bullets**: Size **MINIMUM 16px** (Never use text smaller than 16px).
>    - **3-30-300 Rule**: Max 3 main points per slide, max 30 words per point. Auto-bold technical keywords (`<b>snake_case</b>`, `<b>PEP 8</b>`).
> 7. **Card Color Coding System**:
>    - ⚪ **Default Card**: Light gray background (`#f8fafc`), Border `#e2e8f0`.
>    - 🟠 **Warning Card**: Light amber background (`#fffbeb`), Border `#f59e0b`, Text `#92400e`.
>    - 🔴 **Error / Gotcha Card**: Light red background (`#fef2f2`), Border `#ef4444`, Text `#991b1b`.
>    - 🟢 **Success / Best Practice Card**: Light green background (`#f0fdf4`), Border `#22c55e`, Text `#166534`.
>    - 🔵 **Tip / Info Card**: Light blue background (`#eff6ff`), Border `#3b82f6`, Text `#1e40af`.
> 8. **Graphics, Markdown Rendering & Language Standards**:
>    - **100% Visualized**: Prioritize Mermaid flowcharts, SVG diagrams, or infographics over plain text.
>    - **100% Markdown Rendered**: All Markdown formatting (`**bold**`, `` `code` ``) rendered to clean HTML.
>    - **Academic & Professional Tone**: Production-grade academic tone. ABSOLUTELY FORBIDDEN informal words ("nhé", "thân mến", "nha").
>    - **STRICT NO EMOJI**: ABSOLUTELY FORBIDDEN to use text emojis. Use Phosphor SVG icons or CSS badges.

---

## 2. Advanced Interactive Slide Features

1. **Bento Grid Layout**: Rounded card corners (16px - 20px), soft shadows `box-shadow: 0 20px 40px rgba(0,0,0,0.06)`, Gradient highlights.
2. **Dual-Theme Engine (1-Click Dark 🌙 / Light ☀️ Switcher)**: Toggle between Dark/Light mode depending on classroom lighting.
3. **Interactive In-Slide Tabs & Accordions**: Combine sub-topics into interactive tabs within a single slide instead of creating multiple cluttered slides.
4. **Split Screen Code Comparison**: Side-by-side anti-pattern code ❌ vs PEP 8 standard code ✅.
5. **Presenter View Mode (P Key / Button 🎤)**: Toggle Speaker Notes & Timer for instructors.

---

## 3. Dynamic Slide Layout Archetypes (8 Layouts)

| Layout Code (`layout_type`) | Purpose & Description                              | Presentation Structure                                         |
| :-------------------------- | :-------------------------------------------------- | :------------------------------------------------------------- |
| `COVER_LAYOUT`              | Lecture Deck Cover Page                             | Rikkei Red Logo, Session Red Tag, Dark Main Title, Course Code |
| `AGENDA_LAYOUT`             | Table of Contents Progress Page                     | List of Lessons with prominent red badges (24px)               |
| `SINGLE_COLUMN_FOCUS`       | Single Core Principle / Definition                  | 1 Large Centered Card, Typography 20px-24px, Callout Note      |
| `TWO_COLUMN_COMPARE`        | Problem vs Solution, Good vs Bad Code               | 2 Contrasting Side-by-Side Cards (Green vs Red)                |
| `THREE_COLUMN_CARDS`        | 3 Components / 3 Rules / 3 Steps                    | 3 Parallel Column Cards Grid                                   |
| `CODE_DEMO_EXPLAINER`       | Production Code Snippet with Detailed Explanations  | Left: Overview & Bullets 18px; Right: VS Dark Code Panel       |
| `MERMAID_DIAGRAM`           | Visual Architecture Flowchart occupying 80% area    | Mermaid Flowchart/Sequence/ClassDiagram rendered smoothly      |
| `TABLE_COMPARISON`          | 4-Column Full-width Comparison Table                | 4-Column Markdown Table (Criteria, Method A, Method B, Impact) |
| `WARNING_GOTCHAS`           | Highlight Critical Pitfalls / Syntax Gotchas        | Light Red Warning Card (`#fef2f2`, border `#ef4444`)           |
| `TIMELINE_RECAP`            | Session Milestone Summary                           | 4-Step Connected Timeline Component                            |

---

## 4. Code & Mermaid Standards in Slides

1. **Code Snippet Boxes**:
   - Use `Fira Code` or `JetBrains Mono` font.
   - Dark background matching VS Code Dark (`#0f172a`), border `#334155`.
   - Variable names and keywords MUST be standard English.

2. **Mermaid Diagram Boxes**:
   - Wrap in `<div class="mermaid"> ... </div>`.
   - Use Mermaid v10+ syntax: `flowchart TD`, `sequenceDiagram`, `classDiagram`.
   - Node step labels in ACCENTED VIETNAMESE.

> [!IMPORTANT]
> The single output file for each Lesson Slide Deck is **`slides.html`** (located at `Bài giảng/slides.html`). FORBIDDEN to output as `slides.md`.


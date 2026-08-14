---
name: classroom_lecture_generator
description: Generate premium classroom lecture HTML/PPTX slide presentations (Bài giảng trên lớp) for Rikkei Education programming, database, and system courses. Applies the 8 Golden Slide Rules, tech-stack adaptability (Python, Java, JS/TS, SQL, DevOps, Architecture), cover slide, agenda, bento grids, and code-theory 2-column layouts. Target output language is 100% Accented Vietnamese.
---

# Classroom Lecture Generator Skill (Bài giảng trên lớp) — Rikkei Education Standards

This skill governs the generation of premium, interactive HTML Slide Presentations used by instructors for classroom lectures. Slides must be highly visual, structured, concise, and professional.

---

## 1. PEDAGOGICAL SLIDE PRESENTATION STANDARDS (8 GOLDEN RULES)

Every classroom lecture slide deck (Bài giảng trên lớp) MUST satisfy these 8 rules:

1. **Slide Count Limits (15-20 Slides/Session)**:
   - A standard slide deck for a 1.5-hour classroom session MUST contain exactly 15 to 20 slides.
   - For single-lesson sessions, keep slides focused and high impact.

2. **Cover Slide (Slide 1)**:
   - Must feature a clean, professional cover design.
   - Session ID badge in red color fill (`Session XX`), main session title in bold dark text (`#0f172a`), and the official course header.

3. **Agenda Slide (Slide 2)**:
   - Titled **`LESSON AGENDA`** or **`NỘI DUNG BÀI HỌC`**.
   - Lists the sequential sub-lessons or core concepts of the session in format `01. Lesson 01 - ...`.

4. **Typography & Constraint Rules (3-30-300 Rule)**:
   - Body text minimum `18px`, sub-bullets minimum `16px`.
   - Max 3 main key points per slide, max 30 words per key point.
   - Absolute maximum of 300 words total on any single slide.

5. **No Emojis Standard**:
   - STRICT NO EMOJI (❌, ✅, ⚠️, 🟢) inside slide headings, bullets, or text content.
   - Use clean Phosphor vector SVG icons or Tailwind CSS badges for visual accents.

6. **Unified Slide Header & Navigation**:
   - Every content slide must display the Session ID, Lesson ID, and Slide Title clearly at the top.
   - Active scroll indicator / slide number at the bottom-right corner.

7. **Bento Grid & Grid Cards Layouts**:
   - Use multi-column grid layouts (2-column, 3-column, or Bento Grid cards) to display parallel details.
   - Avoid flat list layouts for complex comparisons. Use side-by-side "Good vs Bad" or comparison tables.

8. **Accented Vietnamese Output Contract**:
   - All text, diagrams, labels, and explanations inside the slides must be written in 100% Accented Vietnamese.
   - Standard programming syntax (variable names, functions) remains in standard English code format.

---

## 2. DYNAMIC TECH-STACK ADAPTABILITY CONTRACT

Slides must dynamically adapt to the specific course subject and `tech_stack`:

1. **Syntax & Style Compliance**:
   - **Python**: Use `snake_case`, `#` comments, Pyodide WASM console-friendly structure.
   - **Java / Spring Boot**: Use `camelCase`/`PascalCase`, `//` comments, standard strong typing.
   - **JavaScript / TypeScript / React / Node.js**: Use `camelCase`/`PascalCase`, `//` comments, modern ES6+ import/export syntax.
   - **SQL**: Use `UPPERCASE` for SQL keywords (`SELECT`, `JOIN`, `WHERE`), snake_case for fields/tables, `--` comments.
   - **Linux / DevOps / Git CLI**: Use standard terminal prompt signs (`$ ` or `# `), clean command flags, and bash output mockups.
   - **Methodology (Agile/Scrum, UML, Architecture)**: Avoid code blocks. Use SVG process flowcharts, tables, and comparison cards instead.

2. **Accented Vietnamese Code Comments**:
   - Every comment inside code blocks (`# ...`, `// ...`, `-- ...`) MUST be written in 100% Accented Vietnamese explaining the logic steps.

3. **No Future Leakage**:
   - Ensure the slide contents stay strictly within the session's taught bounds. Do not leak future syntax or methods.

4. **Plain Developer Language**:
   - Forbid AI/academic buzzwords (`"thách thức kỹ thuật"`, `"anti-pattern"`, `"gotcha"`).
   - Use neutral, clean terms (`"Lỗi thường gặp"`, `"Sai sót phổ biến"`, `"Ngoại lệ cần lưu ý"`).

5. **Closing Period Directive**:
   - Ensure all bullet points, explanation text, and slide subtitles end with a closing period (`.`).

---

## 3. LAYOUT ARCHE-TYPES BY SUBJECT Nature

- **Programming Courses (Python, Java, JS/TS)**:
  - **Slide 1**: Image Explainer (project real-world domain context).
  - **Slide 2**: Code Explainer (left: bullets on mechanism, right: clean syntax block).
  - **Slide 3**: Good vs Bad Practice Comparison (side-by-side code blocks showing incorrect vs correct approach).

- **Database / SQL Courses**:
  - **Slide 1**: Image Explainer (relational ERD or query plan).
  - **Slide 2**: Code Explainer (left: bullets on query logic, right: `SELECT` query block).
  - **Slide 3**: Good vs Bad Practice Comparison (inefficient query vs optimized query with index).

- **Tooling / CLI / Process Courses (Git, Docker, Linux, Agile)**:
  - **Slide 1**: Image Explainer (workflow state diagram or Git tree visual).
  - **Slide 2**: Command Explainer (left: flags breakdown, right: Terminal block with commands).
  - **Slide 3**: Bento Grid / Comparison Card (comparing command outcomes or configuration formats).

---

## 4. TEMPLATE DYNAMIC LOADING & LOOK-AND-FEEL COMPLIANCE (CẤM HARD CODE)

To ensure high-quality design consistency, flexibility, and easy maintainability, all presentation generation processes MUST strictly satisfy the following implementation standards:

1. **Dynamic Template Loading (Cấm Hard Code HTML/CSS/JS):**
   - The agent MUST load the slide skeleton structure dynamically from [`templates/slide_template.html`](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/templates/slide_template.html).
   - ABSOLUTELY FORBIDDEN to hardcode the page layout, standard CSS stylesheets, or navigation JavaScript logic directly inside Python scripts/f-strings.
   - Use standardized placeholders (`{{SESSION_TITLE}}`, `{{MODULE_NAME}}`, `{{NAV_LINKS}}`, `{{SLIDES_CONTENT}}`) inside the template file to insert dynamic contents.

2. **Fixed Header & Rikkei Academy Branding:**
   - Include a fixed header at the top (`fixed top-0 left-0 right-0 h-16 bg-white/95 backdrop-blur-md border-b z-50`) featuring the official Rikkei Academy Logo and module name.
   - All slide content sections must clear the header by using a top spacer or padding (`pt-16` or `padding-top: 4rem`) to prevent overlapping.

3. **Dynamic Tab Scrollspy Highlighting:**
   - The header must feature navigation tabs for each lesson, dynamically generated by the agent.
   - Implement JavaScript `IntersectionObserver` scrollspy logic to detect the active lesson slide and highlight the corresponding nav link in the primary red color (`text-rikkei-red`) and underline style (`border-rikkei-red`).

4. **Student Readability & Font Scaling:**
   - Set the minimum font size for all slide text, list bullets, code cards, inputs, and console elements to at least **`16px` (`text-base`)** to ensure excellent legibility and engagement.
   - Titles, headings, and input labels must scale up proportionally (e.g. `20px` to `30px`) to establish a clear visual hierarchy.

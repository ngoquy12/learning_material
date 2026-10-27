---
name: classroom_lecture_generator
description: Generate the interactive lecture dashboard (Visualizer, file Visualizer/index.html) for a session: per lesson, a few theory cards on the left and a live code or process demo with runtime trace on the right, on one real business scenario, flat light style. This is a dashboard, NOT slides: for projected slides (slides.html) use slide_html and for the PowerPoint deck use slide_deck. Target output language is 100% accented Vietnamese.
---

# Classroom Lecture Dashboard Skill (Visualizer) — Rikkei Education

## 0. Scope

1. **This skill makes a dashboard page**, an interactive companion for a live lecture and for review: concise theory cards plus a demo students can operate. It is one scrolling page with a sidebar, not a deck of slides.
2. **It does not make slides.** Projected slides (`Bai giang tren lop/slides.html`) follow `slide_html`; the PowerPoint file follows `slide_deck`. Never reuse the dashboard layout for slides.
3. **Known pipeline limitation.** `agents/classroom_lecture_generator_agent.py::generate_lecture` also writes the dashboard HTML to `Bai giang tren lop/slides.html` when no `outline_bai_giang.md` exists, so the pipeline's default `slides.html` is this dashboard. Treat that file as a placeholder and replace it with a deck made by `slide_html`.

## 1. Layout

- One page, content width up to about 1680 px, centered; fixed header with the logo; left sidebar of contents (sticky, one link per section, numbered, active link highlighted).
- Per lesson, a two-column block on wide screens (12-column grid):
  - **Left (5 columns): 2 to 3 theory cards**, scannable from a projector. Card 1 "Khái niệm và cú pháp" (2-3 bullets on the core mechanism and syntax), card 2 "Lưu ý thực hành" (real mistakes, edge cases, pitfalls from homework), optional card 3 "Quy chuẩn kỹ thuật" (conventions, naming, productivity tips).
  - **Right (7 columns, sticky): the live demo.** Input controls, a code card with a file name matching the language (`main.py`, `script.js`, `App.java`, `query.sql`), and a runtime trace card with the result.
- Footer: `@{year} Rikkei Education — @copyright All Rights Reserved.`

## 2. Visual style (flat light)

- White and slate surfaces with slate borders, brand red `#be111c` for the active link, buttons and chips. Code cards and the trace console may be dark (`#0f172a`) with high-contrast syntax colors.
- **Forbidden:** glass or blur effects (`backdrop-filter`, `backdrop-blur`), gradients (including gradient text and gradient headers), pulsing or bouncing animation, hover lift effects, colored decorative icons, emoji, ALL CAPS labels or badges. Mark the running step with a static outline or background tint.
- The CSS class `glass-card` is a legacy name kept for compatibility; in the template it is a flat card. Do not add blur or gradients back to it.
- Icons: Phosphor (`ph-bold ph-*`), neutral slate or brand red, at most one per card header, never decorative.
- Fonts: Montserrat for headings, Inter for body, JetBrains Mono for code and trace. Labels and badges use sentence case.
- All text is accented Vietnamese; code identifiers are English.

## 3. Pedagogical directives

- **A. Scope boundary.** Use only concepts taught up to this session. The allowed and forbidden concept lists come from the course data (`allowed_scope`, `forbidden_scope`); nothing about the lesson order is hardcoded here. Never use a forbidden concept in cards, code, comments, identifiers or trace text.
- **B. One scenario.** One concrete business scenario for the whole session dashboard; every snippet, parameter and trace across all lessons builds on that same scenario. Never jump between unrelated example topics.
- **C. Full curriculum coverage.** Every sub-concept listed for each lesson in the course syllabus is covered by a theory card and shown in the demo.
- **D. One control per parameter.** Each input of the demo is its own labeled control (`input` or `select`) with a unique id, in a responsive grid. Never pack several parameters into one text field. A scenario selector auto-fills every control; changing any control re-evaluates the trace and the result immediately.
- **E. Short titles.** Section titles are short (a few words), simulator headers under about 8 words, sidebar links short and numbered. No long repeated titles that wrap onto several lines.
- **F. Micro-steps.** Split code into 2-3 labeled sequential steps with comment dividers (`// --- Bước 1: ... ---`), not one monolithic listing. Each trace line maps one-to-one to one micro-step.

## 4. Technology neutrality

The skill works for any stack: web frontend, Python, Java or C++, SQL, command line and DevOps, backend APIs. Choose the snippet file name and code idiom from `tech_stack`. Do not assume a language; examples in this file are illustrative only.

## 5. Data contract with the pipeline

The generator asks the model for a JSON payload that the template renders:

- `knowledge_cards`: 2-3 theory cards (title, bullets).
- `sim_title`: short demo title.
- `snippet_filename`: language-appropriate file name.
- `controllers_html`: the separate input controls (ids unique and prefixed by lesson).
- `code_box_html`: the 2-3 step code with comment dividers.
- `scenarios`: three test cases: standard, edge, exception, each mapping to every control value.
- `js_code`: plain JavaScript that syncs the controls, evaluates and writes the trace.

Rules for the payload: no external libraries, no `eval`, no leftover `{{ ... }}`, ids match their selectors one to one, every control has a Vietnamese label, and the result is correct for all three scenarios. Without a model (offline), the agent falls back to a heuristic that still produces 2 cards, split steps and separate controls.

## 6. Verification

1. Open the page and operate every control and every scenario; the trace and result must update and the browser console must stay free of errors.
2. No horizontal overflow at 1366 and 1920 px width; no unrendered `{{`, `undefined`, `NaN` or `[object Object]`.
3. No glass, blur, gradient, pulse animation, emoji or ALL CAPS labels (search the HTML for `backdrop`, `gradient`, `animate-pulse`).
4. Cross-check the snippet outputs by running them for real; the trace text must match.
5. Run the lecture UI review (`skills/lecture_ui_reviewer`).

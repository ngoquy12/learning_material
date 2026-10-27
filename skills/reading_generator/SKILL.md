---
name: reading_generator
description: Generate or revise the interactive HTML reading material (reading.html, a 15-minute lesson reading) for a programming, database, tooling or concept lesson at Rikkei Education. Fixed 5-section structure (section-1 to section-5), single business scenario, progressive examples, syntax-first explanations, live sandbox or static code cards by technology, step-by-step simulator, self-test. Includes a checker that runs the project's reading validator. Target output language is 100% accented Vietnamese.
---

# Reading Material Skill (reading.html) — Rikkei Education

This is the technical standard for every reading. Component markup lives in `reference/html_snippets.md`; the map from the former 25 numbered directives to the rules below and the list of what the code really enforces live in `reference/directive_map.md`.

## 0. How to work

1. **Never redesign the approved look.** Copy the page frame (head, styles, sidebar, scripts) from an approved reading of the same project (or `templates/html/reading.html`) and change only content and simulator. This skill governs content and rules, not new visuals.
2. **Write the reading before anything that depends on it** (reading questions, quiz, lab, slides, exercises). They reuse its names, data and messages.
3. **Verify, do not assume.** Run every code example and every number for real, then run `scripts/check_reading.py` (section 6). Do not report done on a failing check.
4. `tech_stack` and, when given, `chosen_domain`, `allowed_scope`, `forbidden_scope` always come from the course data. Never invent a default stack.

## 1. Rules (all mandatory)

### Structure and size
- **R1. Five sections** with ids `section-1` to `section-5` (this is what the validator checks): 1 Problem, 2 Syntax and mechanism, 3 Practical examples, 4 Common mistakes and decision table, 5 Self-test. The legacy anchors `problem-intro`, `data-structure`, `interactive-demo`, `summary-notes`, `self-test` are only read by `core/pm_validators/quality_gates.py`; add them on an inner element only when that gate matters.
- **R2. Fifteen-minute cap.** 1,500-2,000 words counted on visible text (code and UI labels included, scripts and styles excluded; constants in `core/reading_budget.py`). One main problem per lesson; cut secondary ideas. Allocation guide: Section 1 about 100, Section 2 about 550, Section 3 about 650, Section 4 about 250, Section 5 about 250.
- **R3. One scenario.** One real business scenario runs through the whole lesson and, when `chosen_domain` is set, through every lesson of the session. Never switch to an unrelated example topic.
- **R4. Progressive difficulty.** Section 1 uses the simplest instance (one field, one value). Sub-sections 2.1, 2.2, 2.3 add exactly one increment each. 3.1 is minimal (1-2 lines, no branching), 3.2 adds one layer, 3.3 alone may reach full enterprise complexity. Never invert the order or open with a loaded dataset.
- **R5. Scope boundary.** Use only concepts taught up to this lesson. Any `forbidden_scope` term must not appear anywhere: code, comments, identifiers, headings, prose. A reviewer rejects the reading on a leak.

### Content
- **R6. Section 1 story.** At most 3 short paragraphs (scenario, conflict, need for the new concept), about 100 words, plain language, no academic jargon, a general section title, one hero illustration (R18). Show why the old or manual way fails with two concrete risks (money lost, users lost, time lost), then introduce the lesson concept as the answer.
- **R7. Section 2 order in each sub-section:** (1) syntax card, (2) component-by-component bullet list that uses the exact identifiers of the card in bold code badges, (3) a short example or sandbox. Sub-section 2.4 is the step-by-step simulator (see variants). Include one GOOD versus BAD comparison with complete code in both columns.
- **R8. Section 3** has at least three `h3` examples `3.1`, `3.2`, `3.3`, each with a code block (or a command block, table or diagram for non-code subjects). Clean headings: no prefixes like "Ví dụ cơ bản:". Above every sandbox put a requirement box "Yêu cầu bài toán" with context, constraints and expected output.
- **R9. Section 4:** at most 2 common mistakes ("Lỗi thường gặp"), a decision table, nothing else.
- **R10. Section 5:** scenario-based multiple-choice self-test of 3 questions on concrete data from the reading (names, values, results), one check button, feedback inline. Answers must not be guessable without reading.

### Runtime
- **R11. Executable sandbox only where an engine exists:** Python with Pyodide, browser JavaScript with a worker, SQL with AlaSQL. For CLI, Git, Docker, architecture, process and non-code subjects use static terminal blocks, tables, Mermaid or diagrams, never an empty sandbox or a run button. Never load Pyodide for a non-Python subject. For stacks without an in-browser runtime (React, Node/Express/MySQL) use static code cards plus a plain-JavaScript simulation fed with results from real runs.
- **R12. Orientation lesson (Session 01):** one consolidated lesson with three parts (course overview and roadmap, learning method and prerequisites, demo of the final product); no code demo and no sandbox; its outputs are reading, slides and video script only.

### Language and style
- **R13. Vietnamese.** Accented Vietnamese for all prose, labels, code comments and console strings. Code identifiers in English, following the language convention (`snake_case` for Python, C and SQL; `camelCase` for JavaScript and Java). Code card titles are descriptive Title Case, never ALL CAPS.
- **R14. Plain engineering tone.** Banned words: nhé, bẫy lập trình, bẫy cú pháp, bẫy lỗi, thần thánh, bí kíp, tất tần tật, bảo bối, thân mến, thực chiến, gotcha, anti-pattern, khám phá, tuyệt vời, chinh phục, bứt phá, làm chủ, giải mã, hành trình. Banned fluff: "hãy cùng", "như vậy chúng ta thấy", "thú vị là". Use "Lỗi thường gặp", "Lưu ý thực tế", "Mô hình sai cần tránh". An English term is followed by its Vietnamese gloss on first use.
- **R15. Typography.** No emoji or pictograms; the only glyphs are Phosphor icons (`ph-bold ph-*`). No square-bracket tags such as `[NOTE]`. No ALL CAPS headings, buttons or badges. Italics only for captions under images or diagrams. The article `h1` is the clean topic, never "Lesson 01 -" or "Bài 01 -".

### Visual and technical
- **R16. Light page.** White and slate surfaces, brand red `#be111c` for accents, no `dark:` variants and no dark section or card backgrounds. The only dark surfaces are code cards and the console output (high-contrast tokens, console text `#4ade80`, font JetBrains Mono). The simulator panel is light; inactive code lines use dark slate text, never faint gray.
- **R17. Callouts** use role colors on light tints with dark text: amber for notes and warnings, rose for errors, emerald for good practice, sky for tips and requirement boxes. Never nest a code block inside a callout.
- **R18. Illustrations.** Section 1 has one hero: a 2D flat vector image (`<img>`, made with `image_prompt_standard`) or an inline 16:9 SVG (`viewBox="0 0 800 450"`). Sections 2-4 use inline SVG or Mermaid diagrams only. Every image has a caption right below it. No title banner baked into an image, no code inside images, labels 100% Vietnamese.
- **R19. Technical hygiene.** `type="button"` on every button; `event.preventDefault()` on form handlers; no `<script>` tags inside JSON payload strings; code blocks keep their newlines and encode `<` and `>`; tables sit in `div.overflow-x-auto`; `hljs.highlightAll()` after load; Mermaid v10 syntax; no `display:none` on iframes that hold Mermaid; no unrendered `{...}` placeholders; ids match their JavaScript selectors one to one.

### Truth
- **R20. Run everything.** Every code snippet, command, query, status code and printed value is executed for real and copied exactly. Simulations and quiz answers use those real results. Reading questions, quiz and self-test must be answerable from the reading's own concrete data.

## 2. Section blueprint

1. **Problem (`section-1`).** Hero illustration, 3-paragraph story, general title (R6).
2. **Syntax and mechanism (`section-2`).** 2.1, 2.2, 2.3: syntax card, bullet breakdown, short example (R7). 2.4: the step-by-step simulator with Play, Pause, Previous, Next, Reset, speed selector, code tracker (active line highlighted), state table and console, all labels in Vietnamese. GOOD versus BAD cards.
3. **Examples (`section-3`).** 3.1, 3.2, 3.3 with requirement boxes (R8).
4. **Mistakes (`section-4`).** Up to 2 mistakes and a decision table (R9).
5. **Self-test (`section-5`).** 3 scenario questions, one check button (R10); then references (real URLs only) and one "Tự học thêm" line naming topics left out.

## 3. Variants

- **Simulator at the end of Section 3.** The ReactJS and NodeJS courses place one "Mô phỏng tương tác" block after 3.3 instead of 2.4. This is an accepted course-level variant when the course spec says so; `core/validators/visual_linter.py` looks for a "Section 2.4" marker (`sec-2-4`, "mô phỏng cơ chế vận hành", `viz-line-`, `mech-line-`), so such readings report that one error. Do not mix the two placements inside one course.
- **Non-code subjects** (analysis and design, Agile, architecture): no source code, no sandbox; use Mermaid or UML diagrams, rule tables and scenarios (Gherkin, user stories).

## 4. Rewriting an existing reading

Keep its images and figure captions. Keep Section 1 title general. Touch layout only where needed, one small change at a time. Stay within the 15-minute budget. After the rewrite, re-check the reading questions, quiz and self-test against the new text and fix every mismatch.

## 5. Procedure

1. Read the lesson data (`tech_stack`, scenario, `allowed_scope`, `forbidden_scope`, outcomes) and the previous lesson's reading for names and data.
2. Outline the five sections and the word allocation. Write the code first and run it.
3. Write the page from the frame; add simulator data from real runs.
4. Run `python skills/reading_generator/scripts/check_reading.py <reading.html> --tech-stack <stack>`; fix and repeat.
5. Open the page in a browser, operate every button, check the console for errors and a 390 px width for horizontal scroll.

## 6. Checker

`scripts/check_reading.py` runs the project's `validate_reading_material` (section ids, 3 examples in Section 3, emoji, banned words, requirement box, Pyodide compatibility for Python, word budget) and adds checks the validator lacks: `href="#"`, buttons without `type`, images without caption, `dark:` classes, ALL CAPS headings and buttons, square-bracket tags. It does not execute your code and does not judge whether the content teaches well; both remain your job (R20 and the browser check).

Before reporting the reading done, also run the verification gate: `python -m core.harness verify <reading.html> --kind reading` (exit 0 required; exit 2 means a tool was missing, so name it and do not claim verified).

## 7. Reference files

- `reference/html_snippets.md` — component markup: callouts, code cards, sandbox, comparison cards, simulator, self-test, decision table.
- `reference/directive_map.md` — old directive numbers mapped to these rules, and what the code enforces.

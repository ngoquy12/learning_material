---
name: reading_generator
description: Generate enterprise interactive HTML reading materials for programming courses — applying the 10 Mandatory Directives of AGENTS.md, fixed 5-section architecture, live sandbox, code tracker, Good/Bad comparison cards, and Anti-AI scenario questions. Target output language is 100% Accented Vietnamese.
---

# Programming Reading Material Skill — Rikkei Education Standards

This document serves as the **Supreme Technical Directive** governing all agents generating HTML reading materials. Every generated reading material MUST satisfy 100% of the standards below without exception.

---

## 0. PEDAGOGICAL FOUNDATION (MANDATORY DIRECTIVES)

All Agents MUST strictly implement all 25 core directives below.

> Numbering note: this table previously repeated the numbers 10, 11 and 12 and then jumped
> to 37-46, so several directives shared an id and cross-references could not be resolved.
> It is now numbered sequentially 1-25. Cite directives by NUMBER **and** NAME when
> referring to them elsewhere, so a future renumbering cannot silently break the reference.

|  #  | Directive                                                                                                                                                                                                                                                                                                                                                                                  | Status    |
| :-: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| 1 | **Fixed 5-Section Architecture** (Problem Statement ➔ Syntax & Mechanism ➔ Practical Examples ➔ Gotchas ➔ Self-Test)                                                                                                                                                                                                                                                                       | MANDATORY |
| 2 | **10-Minute Micro-Learning** — Bullet Lists & Sublists instead of monolithic text                                                                                                                                                                                                                                                                                                          | MANDATORY |
| 3 | **Ultra-Simple Conversational Storytelling for Section 1** — Friendly real-world story (max 3 short paragraphs: Scenario ➔ Conflict ➔ Need for new concept) with ZERO academic jargon ("Xung đột kỹ thuật", "chạy tuyến tính", "loại trừ độc quyền"), accompanied by a 2D Flat Vector Image                                                                                                | MANDATORY |
| 4 | **2D Flat Vector Image Integration (No HTML/CSS SVG Manual Code)** — 2D Flat Vector Technical Scene Image (via `image_prompt_standard` skill) auto-cropped around visual bounding box (`w-full max-w-3xl h-auto mx-auto rounded-xl shadow-sm`) with NO border, NO background box, NO text clipping, ZERO blank margins, Code Sandboxes per sub-section (2.1, 2.2...), Step Code Visualizer | MANDATORY |
| 5 | **Plain Developer Language & Banned Jargon** — Plain engineering Vietnamese, NO juvenile/AI cliché words ("bẫy lập trình", "mẹo", "bí kíp", "tất tần tật", "bảo bối"). Use "Các lỗi thường gặp", "Lưu ý thực tế", "Kinh nghiệm xử lý"                                                                                                                                                      | MANDATORY |
| 6 | **100% English Code Identifiers (`snake_case`)** — Variables/placeholders MUST be English (`order_amount`, etc.)                                                                                                                                                                                                                                                                           | MANDATORY |
| 7 | **Progressive Syntax Code Sandbox per Sub-section** — Every sub-section (2.1, 2.2, 2.3...) includes a concrete Live Code Sandbox demonstrating that specific syntax variation expanding on the unified scenario                                                                                                                                                                            | MANDATORY |
| 8 | **Human-Like Quality Standard & Domain Agnostic** — 100% Accented Vietnamese, no AI markers, zero hardcoding for any specific tech stack                                                                                                                                                                                                                                                   | MANDATORY |
| 9 | **JSON Payload Output & Jinja2 Template Engine** — Output structured JSON payload (`LessonReadingContent`), while `templates/reading_master.html.j2` renders 100% gold-standard HTML matching `templates/reading.html`                                                                                                                                                                     | MANDATORY |
| 10 | **Domain-Adaptive Component Registry** — Python WASM / JS Worker for coding, AlaSQL for SQL, Terminal Simulator for CLI, SVG Process Cards for Theory/Architecture                                                                                                                                                                                                                         | MANDATORY |
| 11 | **Problem Requirement Box Above Every Demo & Single Unified Scenario** — Insert a clear "Yêu cầu bài toán" callout box directly above every Code Demo Sandbox. ALL demos in Section 2 and Section 3 MUST build on the EXACT SAME UNIFIED REAL-WORLD SCENARIO                                                                                                                               | MANDATORY |
| 12 | **100% Accented Vietnamese Code Comments** — 100% of code comments (`# ...`, `// ...`) and console output strings inside ALL code demos MUST be written in friendly, clear Accented Vietnamese                                                                                                                                                                                             | MANDATORY |
| 13 | **Interactive Step Visualizer UX Standard** — Section 2.4 step visualizers MUST use clean Light Theme, NO line numbers in code display, Live Range Slider for value inputs, dynamic True/False condition badges (`🟢 True - KHỚP!`, `❌ False - Bỏ qua`), and Speed Selectors (`1.5s`, `1.0s`, `0.5s`)                                                                                     | MANDATORY |
| 14 | **Dark Terminal Output** — Console output wrapped in JetBrains Mono font with `#4ade80` text                                                                                                                                                                                                                                                                                               | MANDATORY |
| 15 | **Minimal Italic Text** — Only use italics for captions directly below images/diagrams                                                                                                                                                                                                                                                                                                     | MANDATORY |
| 16 | **STRICT DOMAIN ISOLATION & ZERO HARDCODED FALLBACK CONTRACT** — `tech_stack` MUST ALWAYS be dynamically passed from PM/State. ABSOLUTELY FORBIDDEN to hardcode fallback defaults (no default to Python, Java, etc.) or leak Python Pyodide AST/WASM checks into non-Python subjects (Java, JavaScript, SQL, DevOps)                                                                       | MANDATORY |
| 17 | **100% LIVE EXECUTABLE CODE SANDBOXES** — All code examples in Section 2 and Section 3 MUST use Live Executable Code Sandboxes (`runPythonCode` / Pyodide WASM / JS Worker) with Play, Reset, Copy buttons and Output Console                                                                                                                                                              | MANDATORY |
| 18 | **PEDAGOGICAL ORDER: SYNTAX ➔ BREAKDOWN ➔ EXAMPLE** — Section 2 sub-sections MUST present: (1) Syntax Card FIRST, (2) Component Explanation List SECOND, (3) Live Executable Sandbox THIRD                                                                                                                                                                                                 | MANDATORY |
| 19 | **VIETNAMESE TECHNICAL TERMINOLOGY (NO UNEXPLAINED JARGON)** — Banned unexplained English jargon like "Gotcha", "Anti-pattern". Use "Bẫy lỗi thường gặp", "Mô hình sai cần tránh". Always append Vietnamese translations in parentheses                                                                                                                                                    | MANDATORY |
| 20 | **CLEAN SUB-HEADINGS (NO PREFIX FLUFF)** — ABSOLUTELY FORBIDDEN to use prefixes `Ví dụ cơ bản:`, `Ví dụ nghiệp vụ:`, `Ví dụ doanh nghiệp:` in Section 3 sub-headings. Use clean, direct titles                                                                                                                                                                                             | MANDATORY |
| 21 | **2D FLAT VECTOR INFOGRAPHIC ASSETS** — Section 1 context illustrations MUST use clean 2D Flat Vector Infographics or SVG process diagrams matching lesson topics                                                                                                                                                                                                                          | MANDATORY |
| 22 | **SINGLE UNIFIED REAL-WORLD DEMO SCENARIO CONTRACT** — 100% of code snippets, sandboxes, and visualizers across Section 2 and Section 3 MUST progressively expand on the EXACT SAME UNIFIED SCENARIO established in Section 1. ABSOLUTELY FORBIDDEN to switch to unrelated example topics within the same lesson                                                                           | MANDATORY |
| 23 | **STRICT BANNED AI BUZZWORDS CONTRACT** — ABSOLUTELY FORBIDDEN to use AI cliché words `"bẫy"`, `"bẫy lập trình"`, `"bẫy lỗi"`, `"gotcha"`, `"khám phá"`, `"bí kíp"`, `"tất tần tật"`, `"thần thánh"`. ALWAYS use formal technical terms: `"Lỗi thường gặp"`, `"Sai sót phổ biến"`, `"Ngoại lệ cần lưu ý"`                                                                                  | MANDATORY |
| 24 | **PROGRESSIVE DIFFICULTY CONTRACT (BEGINNER-FIRST, SIMPLE ➔ ADVANCED)** — Complexity MUST be introduced gradually: Section 1's opening scenario uses the SIMPLEST possible concrete instance of the domain (1 field/1 variable, not a full multi-field enterprise object); Section 2 sub-sections (`2.1` ➔ `2.2` ➔ `2.3`) each add exactly ONE new increment of complexity on top of the previous one; Section 3's `3.1` MUST be genuinely minimal (1-2 lines, no branching, no extra fields) even though it stays in the same domain — enterprise-level complexity is reserved for `3.3` only. ABSOLUTELY FORBIDDEN to open with a fully-loaded enterprise dataset before the student has seen a basic version | MANDATORY |
| 25 | **SESSION-WIDE DOMAIN PERSISTENCE CONTRACT** — The unified business domain (`chosen_domain`) is fixed for the ENTIRE SESSION, not just the current lesson — every lesson inside the same session MUST reuse the exact same domain/business scenario family so students experience one continuous storyline across the whole session instead of a new unrelated scenario each lesson | MANDATORY |

---

## 0.15 CODE-LEVEL ENFORCEMENT STATUS

An investigation found that several directives below were, until this refactor, **prompt-only
promises with zero code-level enforcement** — the LLM was asked nicely but nothing in the
rendering pipeline actually guaranteed the outcome, and real generated lessons confirmed the
directives were being violated in practice. The items below are now genuinely enforced in code
(`agents/creators/reading_creator.py`, `core/renderers/reading_renderer.py`,
`core/renderers/reading/*.py`) — cite the exact function when relying on a rule so this list
stays honest as the pipeline evolves:

| Directive | Enforced by | Notes |
| :-- | :-- | :-- |
| #16 "Strict Domain Isolation & Zero Hardcoded Fallback" | `resolve_domain_engine()` (reading_renderer.py) | Raises `ValueError` for an unrecognized `tech_stack` instead of silently defaulting to Python — previously it silently fell back to Python/Pyodide for ANY unmapped stack. |
| Runtime script isolation per stack | `templates/html/reading_master.html.j2` (`{% if engine_type == ... %}`) | `runPythonCode`/Pyodide and `runJsCode` are now conditionally rendered — previously EVERY generated `reading.html` (including non-Python courses) always shipped the Pyodide boilerplate regardless of `engine_type`. |
| §7 Strict Knowledge Scope Boundary | `cli/commands/workflow_cmd.py` computing `forbidden_scope`/`allowed_scope` via `core.scope_calculator.calculate_lesson_scope_contract()`, consumed by `generate_reading_html()` | Previously `state["forbidden_scope"]` was never populated for reading generation at all (quiz generation had this; reading did not) — the prompt fell back to a generic static placeholder string with no real per-lesson boundary. |
| #4 "2D Flat Vector Image Integration" — prioritise 2D image over inline SVG (Sections 2-4) | `_strip_stray_images()` / `_guard_inline_svgs()` (reading_creator.py) | Section 1 already had image governance; Sections 2-4 previously had NONE — the LLM could insert unlimited `<img>`/raw `<svg>` there. Now: `<img>` is stripped from Sections 2-4 entirely (2D images are Section-1-only), and any inline `<svg>` diagram is passed through `guard_svg_syntax()` individually. |
| Section 2/3 sandbox vs static code block | `convert_code_to_live_sandbox()` (`code_sandbox_renderer.py`) | Decision is now made PER CODE BLOCK, not once for the whole lesson's `tech_stack` — a Windows `cmd`/SQL/YAML snippet embedded in a Python or JS lesson is force-static (no "Chạy chương trình" button) even though the lesson's overall stack is executable. |
| #15 "Minimal Italic Text" | `convert_inline_markdown()` (markdown_parser.py) + `sanitize_html_tags_and_italics()` (html_sanitizer.py) | `*text*`/`_text_` now actually convert to `<em>` (previously there was no conversion at all — the ban on italics was the only defense, and once an LLM ignored it, the raw characters leaked straight into rendered prose). The unclosed-`<i class="...">` cleanup regex is also now length-capped so it can never delete an entire real paragraph — it used to be able to. |
| #23 "Strict Banned AI Buzzwords Contract" | `strip_ai_cliches_from_title()` + `FORBIDDEN_AI_CLICHES` (html_sanitizer.py), applied to `section1_title`/`section2_title` | Titles previously skipped ALL sanitizers, including this one — the buzzword ban only ever applied to body prose. List also extended with "chinh phục", "bứt phá", "làm chủ", "giải mã", "hành trình" + English equivalents. |

Everything else in this document (5-section architecture, visual/UX conventions, design tokens,
Section 1 storytelling structure, etc.) remains prompt-level guidance the LLM is expected to
follow — it is not independently validated by a code-level gate today. Treat those as
best-effort unless/until a corresponding enforcement mechanism is added and listed above.

---

## 0.2 SESSION 01 ORIENTATION LESSON SPECIAL DIRECTIVE

For **Session 01 (Orientation & Course Overview)**:

1. **Consolidated Single Lesson**: Session 01 is structured into **1 consolidated lesson** titled `Tổng quan lộ trình và Demo sản phẩm`.
2. **3 Core Sub-sections**:
   - **Part 1: `1. Tổng quan nội dung & Lộ trình môn học`**: Summarize course modules and roadmap using a visual connected Timeline component (`<div class="timeline-track">...</div>`) or a clean structured List.
   - **Part 2: `2. Phương pháp học tập hiệu quả & Kiến thức tiền đề`**: Detail proactive learning methodologies, AI Pair-Programming workflow (Cursor/Windsurf), and prerequisite skills required.
   - **Part 3: `3. Demo sản phẩm dự án đầu ra`**: Present specifications, features, and outcomes of the capstone project / product students will complete by course end.
3. **STRICT NO CODE DEMO / NO EMPTY SANDBOX RULE**:
   - **ABSOLUTELY FORBIDDEN** to generate code demo snippets, executable sandboxes, or empty code blocks for Session 01.
4. **Flexible Bố cục & Tiêu đề**:
   - Do NOT force rigid 5-section IDs (`#problem-intro`, `#data-structure`, etc.) on orientation lessons. Flexible titles matching the 3 main parts are encouraged.
5. **Artifact Scope**:
   - Session 01 produces ONLY **Reading Material** (`reading.html`), **Presentation Slides** (`slides.html`), and **Video Studio Script** (`SCRIPT.md` / `video_script.html`). Quizzes, Homework, and Practical Labs are automatically skipped.

---

## 0.1 CALLOUT BOX & CODE BLOCK ISOLATION STANDARD

1. **CALLOUT BOX COLOR SYSTEM**:
   All text note blocks, warnings, and alerts MUST follow role-based color standards:
   - 🟠 **Warning / Note**: `<div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">`
   - 🔴 **Error / Gotcha**: `<div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">`
   - 🟢 **Success / Best Practice**: `<div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50/60 text-slate-800 my-4">`
   - 🔵 **Tip / Info**: `<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">`

2. **STRICT STANDALONE CODE BLOCK RULE (NO CALLOUT NESTING)**:
   - Callout boxes are strictly reserved for short text alerts and warnings.
   - **ABSOLUTELY FORBIDDEN** to wrap `<pre><code>` or code cards inside a callout box container (`<div class="p-4 rounded-xl border...">`).
   - Place all syntax templates and code examples directly as standalone `<pre><code class="language-LANG">...</code></pre>` blocks.

3. **100% ENGLISH CODE IDENTIFIERS & 100% VIETNAMESE CODE COMMENTS**:
   - Variables, function names, class names, and syntax keywords inside code blocks MUST use clean English `snake_case` / `camelCase` (e.g. `order_amount`, `discount_rate`).
   - 🚨 **100% ACCENTED VIETNAMESE CODE COMMENTS & PRINT STRINGS** 🚨: All code comments (`# ...`, `// ...`) and console output strings inside ALL code demos MUST be written in friendly, clear Accented Vietnamese (e.g., `# 1. Kiểm tra đơn hàng từ 500k trở lên`, `print(f"Phí giao hàng: {shipping_fee} VNĐ")`).
   - Explanations outside code blocks must also be in 100% Accented Vietnamese.

4. **MACBOOK DOTS & SPECIFIC CODE CARD TITLES (NO UPPER CASE)**:
   - Code card headers MUST feature 3 macOS traffic light dots: Red (`#ff5f56`), Yellow (`#ffbd2e`), Green (`#27c93f`).
   - Code card titles MUST be specific and descriptive in Title Case (e.g., `Cú pháp khai báo câu lệnh for trong Python`).
   - **ABSOLUTELY FORBIDDEN** to use generic UPPERCASE titles like `PYTHON CÚ PHÁP` or `PYTHON CODE`.

5. **SYNCHRONIZED SYNTAX EXPLANATION DERIVATION CONTRACT**:
   - Every bullet item explaining code syntax MUST use the EXACT SAME identifier/parameter names as used in the code block.
   - Example: If code uses `for item in iterable_object: statement_1`, bullet items MUST explain `item`, `iterable_object`, and `statement_1` verbatim. NEVER use mismatched terms.

6. **STRICT LIGHT MODE ONLY (NO DARK PANELS / OVERRIDES)**:
   - All generated reading materials MUST strictly use Light Mode.
   - **ABSOLUTELY FORBIDDEN** to use dark background panels (`bg-slate-900`, `bg-black`), dark cards, or dark mode toggle logic.
   - Maintain a balanced, professional corporate palette (`bg-white`, `bg-slate-50`, `border-slate-200`, `text-slate-900`, `text-slate-700`).

7. **STRICT KNOWLEDGE SCOPE BOUNDARY CONTRACT (NO UNLEARNED CONCEPTS)**:
   - The generated reading content, examples, code blocks, and diagrams MUST strictly stay within the knowledge taught up to the current session/lesson.
   - **ABSOLUTELY FORBIDDEN** to leak future unlearned data structures (e.g. using `List` / `[1, 2, 3]` / `.append()` / `range(len(list))` in an introductory `for`/`range` loop session before `List` is introduced), unlearned libraries, or advanced methods not introduced in previous sessions.
   - **REVIEWER AUDIT CONTRACT**: Reviewer agents MUST audit generated HTML against current lesson details and previous session sequence. If ANY unlearned concept or future data structure is detected, the Reviewer MUST REJECT the document immediately.

8. **CLEAN ARTICLE TITLE CONTRACT (NO LESSON PREFIX)**:
   - Main article `<h1>` title MUST ONLY display the clean topic title (e.g., `Khái niệm vòng lặp và câu lệnh for`).
   - **ABSOLUTELY FORBIDDEN** to include `Lesson 01 -`, `Lesson 02 -`, `Bài 01 -` prefix in the main article `<h1>` title.

9. **SYNTAX FIRST, EXPLANATION SECOND PEDAGOGICAL ORDER**:
   - ALWAYS present the **Syntax Card Component** FIRST, followed immediately by the **Component Explanation Bullet List**.
   - Each keyword or placeholder in the explanation list MUST be highlighted with code badges (`<code>...</code>`) and bold font.

10. **INTERACTIVE STEP-BY-STEP MECHANISM VISUALIZER & CODE CARD SEPARATION**:
    - Section 2 MUST embed an **Interactive Step-by-Step Mechanism Visualizer** (HTML/CSS/JS) with Play/Pause/Prev/Next controls, active step line highlights, and step state updates.
    - General syntax templates in Section 2 MUST use **Static Code Cards** (macOS dots, copy button, no run button). Executable practical code in Section 3 MUST use **Live Pyodide Sandboxes** (with run and console output buttons).

11. **INTERACTIVE VISUALIZER COLOR & VIETNAMESE UI CONTRACT**:
    - All visualizer component UI labels, headers, and buttons MUST be in clear Accented Vietnamese (Title: `Mô phỏng cơ chế vận hành từng bước`, Buttons: `Tiếp theo`, `Lùi lại`, `Thử lại`, `Tự động chạy`, Memory Panel: `Bảng bộ nhớ & Trạng thái biến`).
    - Inactive code lines MUST use high-contrast dark slate text (`color: #475569 !important; font-weight: 500`).
    - **ABSOLUTELY FORBIDDEN** to use faint gray, white, or low-contrast text on light backgrounds in visualizers.

12. **VISUALIZER CODE SYNTAX HIGHLIGHTING & NO LINE NUMBERS CONTRACT**:
    - Code lines displayed inside the Step-by-Step Visualizer panel MUST use syntax highlighting matching the language (e.g., `<span class="kw">for</span>`, `<span class="fn">print</span>`, `<span class="num">10</span>`, `<span class="str">"text"</span>`).
    - **ABSOLUTELY FORBIDDEN** to include line numbers (such as `1. `, `2. `, `Dòng 1:`) inside visualizer code lines. Keep code lines clean, accurately highlighted, and syntactically correct.

13. **NO INLINE SCRIPT TAGS & PRESERVE CODE NEWLINES CONTRACT**:
    - **ABSOLUTELY FORBIDDEN** to generate raw inline `<script>...</script>` tags inside JSON response strings. Use standard button event attributes (`onclick="runVizStep(1)"`) calling framework helpers instead.
    - Code blocks inside `<pre><code>...</code></pre>` MUST preserve literal line breaks (`\n`) for proper code indentation.

14. **ENTERPRISE IT IMAGE GENERATION SKILL STANDARD (5 GOLDEN RULES FOR IT LEARNING GRAPHICS)**:
    - 🚨 **RULE 1: ZERO BIG TITLE BANNERS & ZERO DETAILED CODE SNIPPETS** 🚨:
      - **NO BIG TITLE OVERLAYS**: ABSOLUTELY FORBIDDEN to render large title headers (e.g. `HỆ THỐNG XỬ LÝ ĐƠN HÀNG`, `PYTHON COURSE`) at the top of generated images. Headers occupy prime space and duplicate the HTML section title.
      - **NO DETAILED CODE BLOCKS**: ABSOLUTELY FORBIDDEN to show long code snippets (`for order_number in range(5): process_order()`) inside pixel graphics! Code inside images causes spelling artifacts (e.g. `teraton`, `stem`) and clutter. Code belongs exclusively inside HTML code sandboxes.
    - 🎯 **RULE 2: FOCUS ON BUSINESS PROBLEM & WORKFLOW SCENARIO (PROBLEM-FIRST VISUAL)** 🎯:
      - Graphics MUST illustrate the **Real-World Business Context / Problem Scenario** (e.g. Supermarket Checkout Conveyor ➔ Scanner ➔ Invoice Payment ➔ Delivery) or **Input ➔ Process ➔ Output (I-P-O)** workflow.
      - Use clean visual icons, numbered step badges (`1`, `2`, `3`), and short labels instead of code lines.
    - 🛠️ **RULE 3: TECH-STACK ADAPTIVE ILLUSTRATION DESIGN PATTERNS** 🛠️:
      - _Programming & Algorithms (Python, JS, Java, C++)_: 2D real-world business object workflow (Orders, Accounts, Inventory, Tax Engine).
      - _Databases & Data (SQL, NoSQL)_: 2D Data Pipelines, Schema Tables, B-Tree Indexing, Query Flow.
      - _DevOps & Cloud (Git, Docker, CI/CD)_: 2D Container Docks, Git Branch Trees, Pipeline Stages (Build ➔ Test ➔ Deploy).
      - _Web / Mobile / APIs (REST, Microservices)_: 2D Request-Response Flow between Client App, API Gateway, and Backend Services.
      - _Architecture & Security (Redis, Auth, Load Balancer)_: 2D Traffic Distribution, Cache Hit/Miss, Authentication Handshake.
    - 🎨 **RULE 4: HARMONIOUS 2D FLAT VECTOR PALETTE & TYPOGRAPHY** 🎨:
      - 100% Clean 2D Flat Vector Corporate Infographic style.
      - Palette: Corporate Navy `#0f172a`, Slate Gray `#64748b`, Soft Emerald `#059669`, Accent Red `#be111c` on a clean light background (`#f8fafc`).
      - ABSOLUTELY FORBIDDEN to use 3D sci-fi, dark neon backgrounds, or cluttered text overlays.
    - 🔤 **RULE 5: BILINGUAL BALANCE CONTRACT** 🔤:
      - Step descriptions & UI labels inside graphics: **100% Accented Vietnamese** (`QUÉT MÃ SẢN PHẨM`, `KIỂM TRA HÀNG TỒN`, `IN HÓA ĐƠN`, `GIỜ GIAO HÀNG`).
      - Technical terms & keywords only: **Standard English** (`Python`, `range()`, `RAM`, `CPU`, `SQL`, `Docker`, `API`).

## 1. STRICT 5-SECTION ARCHITECTURE

Every reading material document MUST contain exactly 5 sections with fixed Anchor IDs. `<h2>` titles adapt dynamically to the lesson topic while maintaining strict pedagogical order.

### Section 1: `#problem-intro` — Real-World Problem Statement

**Pedagogical Objective**: Trigger "Why do I need to learn this?" before presenting theory by analyzing concrete business impact.

**Mandatory Content Structure**:

1. **Real-world Business Scenario** — Place student in a developer role solving a concrete system problem (e.g. ShopeeFood order checkout engine, banking loan interest calculation, VAT billing).
2. **Sequential Line-by-Line Execution Drawbacks & Financial/Business Risk**:
   - Detail why running code statically line-by-line fails for different inputs.
   - Highlight 2 concrete business risks: _Financial Loss_ (e.g., granting freeship to small 20k orders, causing negative revenue) and _User Churn_ (e.g., overcharging shipping on 100k+ orders).
3. **Conditional Branching Solution (`if`, `elif`, `else`)** — Introduce current lesson concept as an automated cashier decision engine evaluating runtime parameters (`order_amount`).
4. **16:9 Context SVG Diagram** — Visualize input order flow ➔ decision diamond ➔ TRUE vs FALSE execution branches.

**SVG 16:9 Widescreen Technical Standard**:

```html
<div class="my-6">
  <div
    class="w-full max-w-200 mx-auto overflow-hidden rounded-xl border border-slate-200 dark:border-rikkei-borderDark shadow-md rikkei-diagram"
  >
    <svg viewBox="0 0 800 450" class="w-full h-auto">
      <!-- Light/Dark adaptive SVG content using rikkei-diagram-* classes -->
    </svg>
  </div>
  <p class="text-center text-sm text-slate-500 dark:text-slate-400 italic mt-3">
    Problem context diagram caption...
  </p>
</div>
```

---

### Section 2: `#data-structure` — Syntax & Mechanism Breakdown

**Pedagogical Objective**: Dissect keyword syntax + visualize underlying mechanisms so students master concepts immediately.

**Context-Aware Content Structure**:

1. **Context-Aware Visual Block at Subsections 2.1, 2.2, 2.3**:
   - **For Syntax / Programming Lessons**: EVERY subsection (`2.1`, `2.2`...) embeds a **Live Code Sandbox / Syntax Illustration Block** (`<div class="my-4 rounded-xl overflow-hidden border border-slate-700 bg-slate-900"><pre><code class="hljs language-LANG">...</code></pre></div>`) for instant execution.
   - **For Concept / Setup / Tool Lessons (Git, VS Code, Agile, Architecture)**: Do NOT force empty code sandboxes. Instead, embed **Terminal Command Blocks, Configuration Parameter Tables, or Setup Workflow Diagrams**.
2. **Mechanism Illustration Diagrams & Full-Width Interactive Step-by-Step Visualizer**:
   - **Mandatory 100% Full-Width Interactive Mechanism Visualizer Component**: For any technology syntax or algorithm explaining step-by-step execution mechanics, embed a **100% Full-Width Interactive Visualizer (`w-full my-8 rounded-2xl bg-slate-900 border border-slate-700 overflow-hidden shadow-xl`)**.
   - **Required Controls & Sub-Panels**:
     - ⏯️ **Play/Pause Button** (`visualizerTogglePlay('{ID}')`) to auto-advance steps.
     - ⏭️ **Step Prev / Step Next Buttons** (`visualizerPrev('{ID}')` / `visualizerNext('{ID}')`).
     - 🔄 **Reset Button** (`visualizerReset('{ID}')`).
     - ⏱️ **Timer / Speed Selector** (`1.5s`, `1.0s`, `0.5s`).
     - 📌 **Code Tracker Panel**: Highlights active code line being executed with high-contrast badge (`bg-emerald-500/20 border-l-4 border-emerald-500 text-white`).
     - 🖥️ **Data/Memory State Canvas Panel**: Displays variable state transforms, RAM allocations, or array pointer updates in real time.
     - 📟 **Console Output Panel**: Displays real-time output printed or returned at each step.

3. **Component-by-Component Explanation** — Bulleted list, bold technical terms, max 1-2 sentences per point.
4. **Code Comparison Component — GOOD vs BAD Practice**:

```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
  <!-- BAD PRACTICE -->
  <div
    class="bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800/50 rounded-xl p-4"
  >
    <div
      class="flex items-center gap-2 text-rose-700 dark:text-rose-400 font-bold text-sm mb-3"
    >
      <i class="ph-bold ph-x-circle text-base"></i>
      <span>Anti-Pattern (Avoid)</span>
    </div>
    <pre><code class="language-python"># BAD: Redundant tax logic duplication...</code></pre>
    <p class="text-xs text-rose-600 dark:text-rose-400 mt-2 italic">
      Drawback: Code duplication, hard to maintain when tax rates change.
    </p>
  </div>
  <!-- GOOD PRACTICE -->
  <div
    class="bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/50 rounded-xl p-4"
  >
    <div
      class="flex items-center gap-2 text-emerald-700 dark:text-emerald-400 font-bold text-sm mb-3"
    >
      <i class="ph-bold ph-check-circle text-base"></i>
      <span>Best Practice (Recommended)</span>
    </div>
    <pre><code class="language-python"># GOOD: Encapsulated inside reusable function...</code></pre>
    <p class="text-xs text-emerald-600 dark:text-emerald-400 mt-2 italic">
      Benefit: Reusable, maintainable, adheres to DRY principle.
    </p>
  </div>
</div>
```

---

### Section 3: `#interactive-demo` — Practical Application Examples & Adaptive Code Block Standard

**Pedagogical Objective**: Hands-on practical application. Students inspect, analyze, or execute code/commands to master real-world usage.

**SUBJECT NATURE ANALYSIS CONTRACT (EXECUTABLE PROGRAMMING VS PURE CONCEPT / TOOLING / CLI / ARCHITECTURE)**:

- **For Executable Programming Courses (Python, JavaScript, Java, C++, SQL...)**: Embed Pyodide Wasm Sandbox / Live JS Runner with "Run Code" button and live console output.
- **For Pure Concept / Tooling / Process / CLI / Architecture Courses (Git, VS Code, Linux/Bash CLI, Docker CLI, Agile/Scrum, Software Architecture, System Design, UML Analysis & Design...)**: ABSOLUTELY FORBIDDEN to force live Pyodide Wasm sandboxes or run buttons. Section 3 MUST use static Terminal Command Blocks (`<pre><code class="language-bash">...</code></pre>`), Command Flow Comparison Cards, or Config/Diagram Parameter Cards.

**Mandatory Content Structure**:

1. **Hierarchical Sub-heading Numbering (`3.1`, `3.2`, `3.3...`)**: All `<h3>` sub-headings MUST follow parent section hierarchy (Section 2 ➔ `2.1`, `2.2`; Section 3 ➔ `3.1`, `3.2`; Section 4 ➔ `4.1`, `4.2`). FORBIDDEN independent `1.`, `2.`, `3.` numbering.
2. **Code Snippets for Every Example (`3.1`, `3.2`, `3.3`)**: EVERY EXAMPLE MUST include a code block directly below it (`<pre><code class="hljs language-LANG">`). Replace `LANG` with appropriate language (e.g. `bash` for Git/CLI, `python` for Python, `sql` for SQL).
3. **Progressive Example Complexity (1 to 3 Examples from Simple ➔ Complex / Enterprise)**:
   - **Example 3.1 (Ultra-Simple / Syntax Minimalist)**: Minimal syntax/command graspable in 30 seconds (e.g. 1 variable declaration, or basic `git status` command). MUST use only 1-2 concrete values from the domain — NOT the full multi-field object used later in 3.3. A true beginner seeing 3.1 for the first time must be able to follow it without having mastered 3.2/3.3 yet.
   - **Example 3.2 (Moderate / Business Scenario)**: Applied to a small business task (e.g. discounted order total, or feature branching workflow). Adds exactly ONE new layer of complexity on top of 3.1 (one extra condition/field/step), never a full jump to enterprise scale.
   - **Example 3.3 (Enterprise Practical / Advanced)**: Full business scenario (e.g. HR payroll processing or production release merge conflict resolution). This is the ONLY sub-section allowed to reach full enterprise complexity.
   - ⛔ **FORBIDDEN SINGLE ULTRA-COMPLEX EXAMPLE**: Never present a single overly complex or non-practical example.
   - ⛔ **FORBIDDEN DIFFICULTY INVERSION**: 3.1 must always be strictly simpler than 3.2, and 3.2 strictly simpler than 3.3 — never let an "easy" example secretly carry enterprise-level field counts or nested logic.
4. **Pyodide Live Wasm Sandbox & Terminal Console (Only for Runnable Programming Languages)**: Embedded `<script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>` with **Run Code** button for browser execution. (Skipped for Git/CLI/Theory subjects).

**Template Pyodide Interactive Editor Sandbox chuẩn (theo `functions.html` — Style 1 Sáng/Tối Linh hoạt)**:

```html
<div
  class="border border-slate-200 dark:border-rikkei-borderDark rounded-xl overflow-hidden shadow-sm my-6"
>
  <div
    class="relative bg-slate-50/50 dark:bg-slate-900/60 text-slate-800 dark:text-slate-100 font-mono text-sm border-b border-slate-200 dark:border-rikkei-borderDark"
  >
    <!-- Floating Toolbar Top-Right -->
    <div
      class="absolute top-3 right-3 flex items-center gap-1.5 z-10 bg-white/90 dark:bg-slate-800/90 backdrop-blur px-2 py-1 rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm"
    >
      <button
        onclick="clearSandbox('code-1', 'output-1', 'container-1')"
        class="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-400 dark:text-slate-500 hover:text-rikkei-red transition-all"
        title="Khôi phục code gốc"
      >
        <i class="ph-bold ph-x text-sm"></i>
      </button>
      <button
        onclick="runPythonCode('code-1', 'output-1', 'container-1')"
        class="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-400 dark:text-slate-500 hover:text-rikkei-red transition-all"
        title="Chạy chương trình"
      >
        <i class="ph-bold ph-play text-sm"></i>
      </button>
      <button
        onclick="copySandboxCode('code-1', this)"
        class="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-400 dark:text-slate-500 hover:text-rikkei-red transition-all"
        title="Sao chép"
      >
        <i class="ph-bold ph-copy text-sm"></i>
      </button>
    </div>
    <!-- Code area -->
    <pre
      id="code-1"
      contenteditable="true"
      spellcheck="false"
      data-original="# Code demo..."
      class="w-full min-h-24 bg-transparent p-4 font-mono text-sm leading-relaxed outline-none pt-4 pr-28 select-text whitespace-pre-wrap break-all"
    >
# Code demo...</pre
    >
  </div>
  <!-- Output Container -->
  <div
    id="container-1"
    class="hidden bg-slate-100/80 dark:bg-slate-950/60 border-t border-slate-200 dark:border-slate-800/60 p-4"
  >
    <div
      class="flex items-center justify-between text-xs text-slate-400 font-mono mb-1"
    >
      <span>CONSOLE OUTPUT:</span>
    </div>
    <pre
      id="output-1"
      class="font-mono text-sm text-slate-700 dark:text-slate-300 select-text whitespace-pre-wrap m-0"
    ></pre>
  </div>
</div>
```

        class="p-1.5 text-slate-400 hover:text-rikkei-red rounded transition-all"
        title="Xem mô phỏng luồng thực thi"
      >
        <i class="ph-bold ph-eye text-sm"></i>
      </button>
      <button
        type="button"
        onclick="copySandboxCode('code-{ID}', this)"
        class="p-1.5 text-slate-400 hover:text-rikkei-red rounded transition-all"
        title="Sao chép mã nguồn"
      >
        <i class="ph-bold ph-copy text-sm"></i>
      </button>
    </div>

  </div>
  <!-- Code Editable Area -->
  <pre
    id="code-{ID}"
    contenteditable="true"
    spellcheck="false"
    class="p-4 font-mono text-sm leading-relaxed outline-none whitespace-pre-wrap text-slate-800 dark:text-slate-200 min-h-30"
    data-original="{ESCAPED_CODE_CONTENT}"
  >
{CODE_CONTENT_HERE}
  </pre>
  <!-- Output Panel (hidden by default) -->
  <div
    id="output-{ID}"
    class="hidden border-t border-slate-200 dark:border-rikkei-borderDark p-4 bg-slate-900 font-mono text-sm text-emerald-400"
  >
    <div class="flex items-center gap-2 text-slate-400 text-xs mb-2">
      <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
      <span>Console Output</span>
    </div>
    <pre class="output-content"></pre>
  </div>
</div>

<!-- Interactive Code Tracker (toggle với Eye button) -->
<div
  id="tracker-{ID}"
  class="hidden my-4 rounded-xl border border-slate-200 dark:border-rikkei-borderDark overflow-hidden"
>
  <div
    class="bg-slate-800 px-4 py-2 flex items-center gap-2 text-slate-300 text-xs font-semibold"
  >
    <i class="ph-bold ph-play-circle text-rikkei-red"></i>
    <span>Mô phỏng luồng thực thi từng bước</span>
  </div>
  <div
    class="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200 dark:divide-rikkei-borderDark"
  >
    <!-- Left: Code Line Highlight -->
    <div
      class="p-4 bg-slate-900 font-mono text-xs space-y-1"
      id="tracker-code-{ID}"
    >
      <!-- JS sẽ inject các .tracker-line div tại đây -->
    </div>
    <!-- Right: Variable Inspector -->
    <div class="p-4 bg-white dark:bg-rikkei-cardDark">
      <p
        class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2"
      >
        Trạng thái biến (RAM)
      </p>
      <table class="w-full text-xs">
        <thead>
          <tr
            class="text-slate-500 border-b border-slate-200 dark:border-rikkei-borderDark"
          >
            <th class="text-left pb-1">Biến</th>
            <th class="text-left pb-1">Kiểu</th>
            <th class="text-left pb-1">Giá trị</th>
          </tr>
        </thead>
        <tbody id="tracker-vars-{ID}" class="font-mono"></tbody>
      </table>
    </div>
  </div>
  <!-- Step Controls -->
  <div
    class="bg-slate-100 dark:bg-slate-800 px-4 py-2 flex items-center gap-3 border-t border-slate-200 dark:border-rikkei-borderDark"
  >
    <button
      type="button"
      onclick="trackerPrev('{ID}')"
      class="px-2 py-1 text-xs bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 rounded font-mono"
    >
      ⏮ Trước
    </button>
    <button
      type="button"
      onclick="trackerNext('{ID}')"
      class="px-2 py-1 text-xs bg-rikkei-red hover:bg-rikkei-darkred text-white rounded font-mono font-bold"
    >
      Sau ⏭
    </button>
    <span id="tracker-step-{ID}" class="text-xs text-slate-500 font-mono"
      >Bước 1 / ?</span
    >
    <span
      id="tracker-msg-{ID}"
      class="text-xs text-amber-600 dark:text-amber-400 italic ml-auto"
    ></span>
  </div>
</div>
```

**CSS quy chuẩn Code Tracker Highlight**:

```css
/* Dòng code đang thực thi */
.tracker-line {
  transition: all 0.2s ease;
  color: #94a3b8;
  padding: 2px 4px;
  border-radius: 4px;
  border-left: 3px solid transparent;
}
.tracker-line.active-step {
  background-color: rgba(190, 17, 28, 0.18);
  border-left-color: #be111c;
  color: #ffffff !important;
  font-weight: 700;
}
/* Biến vừa cập nhật */
.var-updated {
  animation: pulse-var 1s ease;
}
@keyframes pulse-var {
  0% {
    background-color: rgba(16, 185, 129, 0.35);
  }
  100% {
    background-color: transparent;
  }
}
```

---

### Section 4: `#summary-notes` — Production Gotchas & Best Practices

**Pedagogical Objective**: Prevent common bugs before students proceed to independent practice.

**Mandatory Content Structure**:

1. **Common Pitfalls & Gotchas List** — Bulleted list with bold error names:
   - Python: Mutable default argument, Scope LEGB, IndentationError
   - C/C++: Dangling pointer, Memory leak, Undefined behavior
   - Java: NullPointerException, Pass-by-value of reference
   - JavaScript: `undefined` vs `null`, Type coercion, Closure leak

2. **Decision Matrix Table** — When to use A vs B:

```html
<div class="overflow-x-auto my-6">
  <table class="w-full text-sm border-collapse">
    <thead class="bg-rikkei-red text-white">
      <tr>
        <th class="px-4 py-3 text-left font-semibold">Scenario</th>
        <th class="px-4 py-3 text-left font-semibold">Recommended Choice</th>
        <th class="px-4 py-3 text-left font-semibold">Rationale</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-200 dark:divide-rikkei-borderDark">
      <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50">
        <td class="px-4 py-3 text-slate-700 dark:text-slate-300">...</td>
        <td
          class="px-4 py-3 font-mono text-emerald-700 dark:text-emerald-400 font-semibold"
        >
          ...
        </td>
        <td class="px-4 py-3 text-slate-600 dark:text-slate-400">...</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

### Section 5: `#self-test` — 1-Page Interactive Self-Test Assessment

**Pedagogical Objective**: Enable immediate self-evaluation directly on the reading page. Scenario-based questions enforce thorough reading of the material.

**3 Immutable Directives**:

1. **Scenario-Based**: Place student in a concrete context, querying data directly presented in reading material.
2. **Anti-AI Shortcut**: Answers MUST cite specific sections in `reading.html`.
3. **1-Page**: Single Check Answers button — inline feedback rendered directly below each question.

**Self-Test Form Component Template**:

```html
<section id="self-test" class="mb-10 scroll-mt-24">
  <h2
    class="font-montserrat font-bold text-2xl text-slate-900 dark:text-white mb-6"
  >
    5. Khảo thí tự đánh giá
  </h2>

  <!-- Câu 1: Radio Choice -->
  <div
    class="border border-slate-200 dark:border-rikkei-borderDark rounded-xl p-5 mb-4 bg-slate-50 dark:bg-rikkei-cardDark/50"
  >
    <div class="flex items-start gap-3">
      <span
        class="w-7 h-7 rounded-full bg-rikkei-red text-white text-xs flex items-center justify-center font-bold shrink-0 mt-0.5"
        >1</span
      >
      <div class="flex-1">
        <p
          class="font-semibold text-slate-900 dark:text-white text-sm leading-relaxed mb-3"
        >
          {SITUATION_SCENARIO_QUESTION — phải dựa trên dữ kiện cụ thể trong bài
          đọc}
        </p>
        <div class="space-y-2">
          <label
            class="flex items-center gap-3 p-3 rounded-lg border border-slate-200 dark:border-rikkei-borderDark hover:border-rikkei-red cursor-pointer transition-all"
          >
            <input type="radio" name="q1" value="A" class="accent-rikkei-red" />
            <span class="text-sm text-slate-700 dark:text-slate-300"
              >A. {OPTION_A}</span
            >
          </label>
          <label
            class="flex items-center gap-3 p-3 rounded-lg border border-slate-200 dark:border-rikkei-borderDark hover:border-rikkei-red cursor-pointer transition-all"
          >
            <input type="radio" name="q1" value="B" class="accent-rikkei-red" />
            <span class="text-sm text-slate-700 dark:text-slate-300"
              >B. {OPTION_B}</span
            >
          </label>
          <label
            class="flex items-center gap-3 p-3 rounded-lg border border-slate-200 dark:border-rikkei-borderDark hover:border-rikkei-red cursor-pointer transition-all"
          >
            <input type="radio" name="q1" value="C" class="accent-rikkei-red" />
            <span class="text-sm text-slate-700 dark:text-slate-300"
              >C. {OPTION_C}</span
            >
          </label>
          <label
            class="flex items-center gap-3 p-3 rounded-lg border border-slate-200 dark:border-rikkei-borderDark hover:border-rikkei-red cursor-pointer transition-all"
          >
            <input type="radio" name="q1" value="D" class="accent-rikkei-red" />
            <span class="text-sm text-slate-700 dark:text-slate-300"
              >D. {OPTION_D}</span
            >
          </label>
        </div>
        <!-- Feedback (hidden by default) -->
        <div
          id="feedback-q1"
          class="hidden mt-3 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/50 text-sm text-emerald-800 dark:text-emerald-300"
        >
          <i class="ph-bold ph-check-circle mr-1"></i>
          <strong>Đáp án: {CORRECT_OPTION}</strong> —
          {DETAILED_EXPLANATION_REFERENCING_READING_CONTENT}
        </div>
      </div>
    </div>
  </div>

  <!-- Nút Submit duy nhất -->
  <button
    type="button"
    id="btn-check-answers"
    onclick="checkSelfTest()"
    class="w-full py-3 bg-rikkei-red hover:bg-rikkei-darkred text-white font-bold text-sm rounded-xl transition-all shadow-lg flex items-center justify-center gap-2 mt-6"
  >
    <i class="ph-bold ph-check-square"></i>
    Kiểm Tra Đáp Án
  </button>
  <div
    id="selftest-result"
    class="hidden mt-4 p-4 rounded-xl border border-slate-200 dark:border-rikkei-borderDark text-sm font-semibold text-center"
  ></div>
</section>
```

---

## 2. DESIGN TOKENS & STYLE GUIDE (IMMUTABLE DESIGN TOKENS)

| Token            | Light Mode                   | Dark Mode                            | Target Element Application                 |
| :--------------- | :--------------------------- | :----------------------------------- | :----------------------------------------- |
| Primary Accent   | `#be111c`                    | `#be111c`                            | Button, Active Link, Badge, Section border |
| Page Background  | `bg-slate-50` (#f8fafc)      | `bg-rikkei-bgDark` (#0b0f19)         | Body container                             |
| Card Background  | `bg-white`                   | `bg-rikkei-cardDark` (#151d30)       | Article, Section cards                     |
| Border           | `border-slate-200` (#e2e8f0) | `border-rikkei-borderDark` (#1e293b) | Dividers, Card borders                     |
| Text Main        | `text-slate-900` (#0f172a)   | `text-white` (#ffffff)               | Headings                                   |
| Text Body        | `text-slate-600` (#475569)   | `text-slate-300` (#cbd5e1)           | Paragraphs                                 |
| Text Muted       | `text-slate-500` (#64748b)   | `text-slate-400` (#94a3b8)           | Captions, Labels                           |
| Code Font        | JetBrains Mono               | JetBrains Mono                       | All code blocks                            |
| Console Output   | `#4ade80` on `#0f172a`       | `#4ade80` on `#0f172a`               | Dark Terminal                              |
| Good Practice BG | `bg-emerald-50`              | `bg-emerald-950/30`                  | GOOD code card                             |
| Bad Practice BG  | `bg-rose-50`                 | `bg-rose-950/30`                     | BAD code card                              |

---

## 3. PROGRAMMING LANGUAGE MATRIX REFERENCE

| Language       | Naming Convention          | Memory Anatomy Diagram (Section 2)                    | Sandbox & Tracker                                        | Language Gotchas                                             |
| :------------- | :------------------------- | :---------------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------- |
| **Python**     | `snake_case`               | PyObject reference, Mutable vs Immutable, Stack frame | **Pyodide Wasm** (Real browser execution) + Code Tracker | Mutable default args, Global scope leak, IndentationError    |
| **JavaScript** | `camelCase`                | Call Stack, Scope Chain, Event Loop, Closure          | JS Console Emulator + Scope Tracker                      | `undefined` vs `null`, Type coercion, `this` context         |
| **Java**       | `camelCase` / `PascalCase` | Stack (Primitive) vs Heap (Reference), GC             | Java Execution Flow Tracker                              | NullPointerException, Pass-by-value of reference, Autoboxing |
| **C**          | `snake_case`               | Stack address (0x...), Heap malloc/free, Pointer      | Memory Pointer Tracker, Address Inspector                | Dangling pointer, Memory leak, Buffer overflow               |
| **C++**        | `camelCase` / `snake_case` | Stack vs Heap, Constructor/Destructor lifecycle       | Object Lifecycle Tracker                                 | Undefined behavior, Double free, Dangling reference          |

---

## 4. TECHNICAL MANDATORY RULES

1. **100% `type="button"`** on all `<button>` elements in reading material to prevent accidental form submission.
2. **`event.preventDefault()`** on click handlers in input forms.
3. **Strictly NO ALL CAPS** on headings, buttons, or badges. Use Sentence case.
4. **Phosphor Icons** (`ph-bold ph-*`) replacing text emojis (❌, ✅, ⚠️).
5. **100% Accented Vietnamese** in body text, self-test questions, SVG labels, and code comments.
6. **No AI Clichés** — FORBIDDEN fluff phrases ("hãy cùng", "như vậy chúng ta thấy", "thú vị là").
7. **Highlight.js** auto-initialized post DOM load (`hljs.highlightAll()`).
8. **Mermaid v10+ Syntax** — Arrow with label syntax `A -->|Label| B`, special character labels enclosed in `["label"]`.
9. **SVG Adaptive Colors** — Use `rikkei-diagram-*` CSS utility classes instead of inline fill for Dark Mode support.
10. **Scroll Progress Bar** — Header reading progress indicator.
11. **No Embedded Title Banner in Images** — 100% FORBIDDEN to render text title banners inside the image canvas graphic. Image canvas focuses 100% on pure visual flow cards and state graphics.
12. **100% Unified Accented Vietnamese Labels in Images** — Zero mixed English/Vietnamese jargon inside visual graphics (`INPUT ORDER` ➔ `Đầu vào đơn hàng`, `NET TOTAL` ➔ `Tổng thanh toán`).
13. **At Least 3 Progressive Examples in Section 3** — Section 3 MUST contain at least 3 progressive sub-sections (`3.1`, `3.2`, `3.3`) with title, problem requirement box, and sample code sandbox.
14. **Mandatory Requirement Callout Before Sandboxes** — BEFORE EVERY live code sandbox, embed a clean Requirement Callout Component (`p-4 rounded-xl border border-sky-200 bg-sky-50/60...`) stating the concise problem description.
15. **Prioritize 2D Flat Vector Image Assets** — Prioritize 2D Flat Vector Image assets (`.png` / `.webp` / referenced `.svg` inside `<img>` tags) over raw inline SVG code blocks.

---

## 5. QUALITY GATE APPROVAL RUBRIC (6-POINT CHECKLIST)

Reading material is approved ONLY when passing all 6 audit points:

|  #  | Criterion                           | Verification Method                                                               |
| :-: | :---------------------------------- | :-------------------------------------------------------------------------------- |
|  1  | Exactly 5 fixed Anchor IDs          | Grep `#problem-intro #data-structure #interactive-demo #summary-notes #self-test` |
|  2  | Zero future concept leaks           | Verify `forbidden_scope` terms do not appear in content                           |
|  3  | Executable code, zero syntax errors | Linter / Pyodide test verification                                                |
|  4  | 16:9 Widescreen SVG in Section 1    | Grep `viewBox="0 0 800 450"` or `viewBox="0 120 800 210"`                         |
|  5  | GOOD vs BAD Practice cards present  | Grep `ph-check-circle` and `ph-x-circle`                                          |
|  6  | Self-Test Form with Submit button   | Grep `id="btn-check-answers"` or `checkSelfTest`                                  |

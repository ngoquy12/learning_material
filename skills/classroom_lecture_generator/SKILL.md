---
name: classroom_lecture_generator
description: Generate premium interactive visual classroom lecture dashboards (Bài giảng trên lớp / Interactive Visualizer) for Rikkei Education sessions. Adheres to the 2-column layout (Left: Concise 2-Hour Review Theory Cards, Right: Interactive Live Code Demo & Runtime Trace). Enforces Strict Knowledge Scope Boundaries (no future unlearned functions/if-else), Single Unified Real-World Business Scenario per session, Dedicated Multi-Input Parameter Separation, Concise & Punchy Titles, Modular Micro-Content Sub-Step Demo Splitting, and Full Curriculum Completeness. Works universally across ANY subject/tech stack (Web JS, Python, Java, C++, SQL, Git, Linux, Docker, React, etc.) without hardcoding. Target output language is 100% Accented Vietnamese.
---

# Interactive Classroom Visual Lecture Dashboard Skill (Bài giảng trên lớp) — Rikkei Education Standards

This skill governs the generation of the **Interactive Classroom Visual Lecture Dashboard (`slides.html` / `index.html`)** used by instructors for 2-hour live classroom lectures and student review.

---

## 1. 2-HOUR CLASSROOM REVIEW PHILOSOPHY & 2-COLUMN LAYOUT

Instructors have a **2-hour (120-minute) lecture window** to review key concepts and conduct live coding demonstrations. Therefore, the dashboard MUST remain concise, focused, practical, and avoid overwhelming students with excessive theoretical minutiae.

### 1.1. Standard 2-Column Split Grid per Lesson (`grid grid-cols-1 xl:grid-cols-12 gap-6 items-start`)

1. **Left Panel: Core Concise Theory Cards (`xl:col-span-5 space-y-4`)**:
   - Exactly **2 to 3 concise, scannable Glass-Cards** per lesson:
     - **Card 1: Khái niệm & Cú pháp Cốt lõi** (`badge: "KHÁI NIỆM & CÚ PHÁP"`, `icon: "ph-bold ph-lightbulb text-amber-500"`): 2-3 bullet points defining the core mechanism and standard syntax for the lesson's target technology.
     - **Card 2: Lưu ý & Bẫy lỗi Thường gặp** (`badge: "LƯU Ý THỰC HÀNH"`, `icon: "ph-bold ph-warning-octagon text-rose-600"`): Common real-world mistakes, edge cases, and pitfalls students encounter during homework and project tasks (e.g. Type coercion with `==`, floating-point precision `0.1 + 0.2`, prefix vs postfix increment `++x` vs `x++`, short-circuiting pitfalls).
     - **Card 3 (Optional): Quy chuẩn Kỹ thuật / Pro Tip** (`badge: "QUY CHUẨN KỸ THUẬT"`, `icon: "ph-bold ph-check-square-offset text-blue-600"`): Best practice conventions, naming rules, or productivity tips.
   - **Conciseness Directive**: Keep bullet points punchy and easy to scan from a projector or laptop.

2. **Right Panel: Live Code Demo & Runtime Trace (`xl:col-span-7 sticky top-24 space-y-6`)**:
   - **Interactive Controllers**: Dedicated separate input fields, select dropdowns, or testcase buttons enabling instructors and students to adjust individual parameters live.
   - **IDE Window Code Card**: Clean macOS-style code box displaying the active code snippet with syntax highlighting and language-appropriate filename (e.g. `main.py`, `script.js`, `App.java`, `query.sql`, `main.cpp`).
   - **Runtime Trace & Visual Evaluation Card**: Real-time console log / compiler trace explaining execution steps in 100% Accented Vietnamese and output result badge.

---

## 2. STRICT PEDAGOGICAL & ARCHITECTURAL DIRECTIVES

### 2.1. Directive A: Strict Knowledge Scope Boundary & Zero Concept Leakage (Directive 12)

- All generated lecture cards and code demo snippets MUST strictly adhere to the knowledge scope taught up to the current session.
- **Introductory & Syntax Operator Sessions (e.g. Sessions 1 to 5)**:
  - ⛔ **ABSOLUTELY FORBIDDEN**: Using function declarations (`function calculateTotal(...)`, `def foo(...)`), branching statements (`if-else`, `switch-case`), loops (`for`, `while`), classes/OOP, DOM manipulation, async/await, or advanced standard library helper methods (`Math.round`, `Number.isNaN`) before their dedicated introduction sessions!
  - ✅ **MANDATORY APPROACH**: All code snippets MUST use direct sequential variable declarations (`const`, `let`), direct arithmetic/comparison/logic expressions, and standard output logging (`console.log`, `print`).

### 2.2. Directive B: Mandatory Single Unified Real-World Scenario Contract (Directive 16)

- Every generated session dashboard MUST establish exactly **ONE unified concrete real-world business scenario** across all lessons in that session (e.g., _Hệ thống Giỏ hàng & Thanh toán Đơn hàng E-Commerce (Shopee/Tiki Checkout)_, _Hệ thống Phân loại Khách hàng & Xét duyệt Đơn vay Ngân hàng_, or _Hệ thống Quản lý Đặt khám Bệnh viện_).
- 100% of code snippets, variables, parameter inputs, and runtime traces across all sections (Section 1, Section 2, Section 3...) MUST progressively build on and expand THAT EXACT SAME UNIFIED SCENARIO.
- ⛔ **ABSOLUTELY FORBIDDEN**: Switching to disjointed, random example topics (e.g., Shopping cart in Lesson 1 ➔ Cinema age check in Lesson 2 ➔ Admin auth in Lesson 3) within the same session dashboard!

### 2.3. Directive C: Full Curriculum Topic Completeness

- Every sub-concept specified in the Course Syllabus (PM Matrix) for each lesson MUST be explicitly covered in the theory cards and illustrated in the live demo:
  - _Toán tử Số học_: `+`, `-`, `*`, `/`, `%` (chia lấy dư), `**` (lũy thừa), `+=`, `-=`, `*=`, `/=`, `++`, `--` (tiền tố vs hậu tố).
  - _Toán tử So sánh_: `===` (bằng nghiêm ngặt) vs `==` (bằng lỏng lẻo/ép kiểu), `!==` vs `!=`, và so sánh quan hệ `>`, `<`, `>=`, `<=`.
  - _Toán tử Logic & Ngắn mạch_: `&&` (AND), `||` (OR), `!` (NOT), cơ chế Ngắn mạch (Short-circuit evaluation), và 6 giá trị Falsy (`false`, `0`, `""`, `null`, `undefined`, `NaN`).

### 2.4. Directive D: Multi-Input Parameter Separation & Dedicated Controllers

- When an interactive code demo involves multiple parameters (e.g. `Đơn giá`, `Số lượng`, `Mã giảm giá`, `Phí vận chuyển`, `Mã Voucher`, `Hạng thành viên`, `Đã đăng nhập`):
  - ⛔ **ABSOLUTELY FORBIDDEN**: Bundling or concatenating multiple parameters into a single large text string input field (e.g., `value="itemPrice = 200000, quantity = 2, shipping = 30000"`).
  - ✅ **MANDATORY APPROACH**: Break down parameters into **separate, dedicated `<input>` or `<select>` controls** within a responsive grid (`grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3`).
  - Each input field MUST have a clear Vietnamese label (`Đơn giá (VNĐ)`, `Số lượng (món)`, `Mã giảm giá (VNĐ)`, `Phí ship (VNĐ)`) with distinct HTML IDs (e.g., `id="s1-price"`, `id="s1-qty"`, `id="s1-discount"`, `id="s1-shipping"`).
  - When the instructor or student changes the Scenario Dropdown, JavaScript MUST auto-fill all individual input fields.
  - When the user types or modifies ANY individual input field, the simulator MUST dynamically re-evaluate the calculation, runtime trace, and result card in real-time.

### 2.5. Directive E: Concise, Punchy & Meaningful Titles (Strict No-Bloat Directive)

- Section Titles (`<h2>`), Sidebar Navigation pills, and Simulator Demo Headers (`<h3>`) MUST be **concise, punchy, meaningful, and strictly avoid text bloating**.
- ⛔ **ABSOLUTELY FORBIDDEN**: Long repetitive verbose titles like `Trình diễn trực quan: Toán tử So sánh Bằng nghiêm ngặt (===) và Khác (!==) — Hệ thống Giỏ hàng & Thanh toán Đơn hàng E-Commerce (Shopee/Tiki Checkout)` (over 15-20 words, multi-line wrapping).
- ✅ **MANDATORY APPROACH**:
  - Section Title (`<h2>`): Concise & focused (e.g. `1. Toán tử Số học & Gán gộp`, `2. So sánh Nghiêm ngặt (===, !==)`, `3. Logic & Ngắn mạch (&&, ||)`).
  - Simulator Header (`<h3>`): Short & punchy under 6-8 words (e.g. `Trực quan: Tính toán Giỏ hàng`, `Trực quan: So sánh Voucher & VIP`, `Trực quan: Điều kiện Freeship`).
  - Sidebar links: Concise pills (e.g. `1. Số học & Gán gộp`, `2. So sánh Nghiêm ngặt`, `3. Logic & Ngắn mạch`).

### 2.6. Directive F: Modular Micro-Content & Progressive Sub-Step Demo Splitting

- ⛔ **ABSOLUTELY FORBIDDEN**: Writing monolithic 30-line code blocks that bundle 10 distinct concepts together into 1 giant uninterrupted script, making it difficult for instructors to explain during classroom demos.
- ✅ **MANDATORY APPROACH**:
  - **Theory Cards**: Divide theoretical analysis into distinct, granular micro-cards (Cú pháp cốt lõi, Cơ chế hoạt động, Bẫy lỗi thường gặp).
  - **Code Demo Structure**: Structure code snippets into **2-3 clearly labeled, sequential micro-steps** using comment dividers (e.g., `// --- Bước 1: Tính tạm tính (Số học *, +) ---`, `// --- Bước 2: Áp dụng giảm giá (Gán gộp -=, ++) ---`, `// --- Bước 3: Đánh giá kết quả ---`).
  - **Runtime Trace Alignment**: Each line in the runtime trace MUST map 1-to-1 with a discrete micro-step in the demo snippet, allowing progressive line-by-line tracing.

---

## 3. MULTI-STACK UNIVERSAL BASE CONTRACT (ABSOLUTELY ZERO HARDCODING)

The generator agent MUST operate as a **Universal Generic Base Engine** applicable across ANY subject and technology stack:

- **Web Frontend (JavaScript / TypeScript / React / HTML5 / CSS3)**: DOM API, event handling, ES6+ features, state mutation, Async/Fetch.
- **Python**: Control flows, slicing, list/dict comprehensions, functions, OOP, Pandas/Data science.
- **Backend / OOP (Java / C# / C++ / PHP / Go)**: OOP principles, static typing, data structures, algorithm flow.
- **Database / SQL**: Table schemas, queries (`SELECT`, `JOIN`, `GROUP BY`), data filtering.
- **System / CLI / DevOps (Git, Linux, Docker, CI/CD)**: Command builders, pipeline workflows, file system changes.

### 3.1. LLM-Driven Dynamic Generation Contract

1. The agent extracts ground-truth curriculum metadata (Syllabus details, goals, allowed/forbidden scope boundaries) and reading knowledge.
2. The agent establishes a Unified Session Scenario and feeds the unified context to the LLM.
3. The LLM produces a structured JSON payload containing:
   - `knowledge_cards`: 2-3 concise theory cards.
   - `sim_title`: Short punchy title of the live demo (under 6-8 words).
   - `snippet_filename`: Language-appropriate source file name (`main.py`, `script.js`, `App.java`, `main.cpp`, `query.sql`).
   - `controllers_html`: Interactive input controls with separate dedicated fields for each parameter.
   - `code_box_html`: Sequential sample demo code split into 2-3 modular steps with comment dividers.
   - `scenarios`: 3 realistic testcase scenarios (1: Chuẩn/Standard, 2: Biên/Edge case, 3: Ngoại lệ/Gotcha case) mapping to individual parameter values.
   - `js_code`: Vanilla JS function for interactive browser binding that syncs individual input fields and triggers real-time evaluation.

### 3.2. Robust Generic Heuristic Base Fallback

When running offline or without an active LLM, the agent MUST employ a domain-aware parser that:

- Generates clean 2-card theory summaries matching syllabus topics.
- Constructs scope-safe sequential code demos split into 2-3 modular steps (`Bước 1`, `Bước 2`, `Bước 3`).
- Renders separate dedicated input fields for each parameter in `controllers_html`.
- Binds interactive controllers with real-time step-by-step trace explanations (no dummy math multiplications).

---

## 4. UI/UX & STYLING SPECIFICATIONS

- **Container Breadth**: Max container width `max-w-[1680px]` with balanced 2-column grid (`xl:col-span-5` and `xl:col-span-7`).
- **Typography**: `Montserrat` (Headings), `Inter` (Body text), `JetBrains Mono` (Code & Traces).
- **Branding**: Official Rikkei Education logo, Rikkei Red (`#be111c`), High-contrast dark syntax panels (`#0f172a`), Clean light containers (`bg-white`, `bg-slate-50`).
- **Footer Copyright Contract**: `<p>@{{ current_year | default('2026') }} Rikkei Education — @copyright All Rights Reserved.</p>`.
- **Accented Vietnamese**: 100% of labels, cards, traces, and explanations MUST be written in standard Accented Vietnamese.

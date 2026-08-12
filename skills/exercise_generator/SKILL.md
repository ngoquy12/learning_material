---
name: exercise_generator
description: Instructs AI agent to generate a 15-exercise suite adhering to Rikkei Education pedagogical standards (Enterprise Context, Real-world Pain Points, Anti-Scope-Leakage, Dynamic Multi-Stack Adaptation, Stack Isolation, Language-Specific Code Formatting). Target output language is 100% Accented Vietnamese.
---

# Exercise Generator Skill — Rikkei Education Standards

## 1. Overview & Architectural Vision

This skill instructs the AI agent to act as a **Senior Computer Science Professor and Academic Director** designing a standardized set of **15 exercises** for a single course learning session.

The exercise standard of Rikkei Education adheres to 6 core pedagogical principles:

1. **CLOSED HOW - OPEN WHAT & WHY (Golden Rule)**:
   - ABSOLUTELY FORBIDDEN to provide step-by-step algorithmic execution hints in exercise prompts (e.g., forbid writing "Step 1: use for loop, Step 2: check condition with if/else").
   - Prompts MUST ONLY state the destination business outcome (**What**) and why the business/user needs this feature (**Why**). Students MUST autonomously choose programming constructs and design the solution logic themselves.
2. **Thinking First, Coding Second**:
   - Code is merely the implementation of logical thinking. Every exercise (from Basic to Creative) MUST require students to submit a Solution Analysis & Logic Design report (I/O specification, Test Cases, Pseudocode, or Flowchart) alongside source code.
3. **Direct & Concise Presentation**:
   - Go straight to the business scenario and technical core. ABSOLUTELY FORBIDDEN long-winded academic fluff or confusing convoluted descriptions. Keep exercise statements crisp, professional, and easy for students to grasp instantly.
4. **Real-World Enterprise Scenario & Roleplay**:
   - ABSOLUTELY FORBIDDEN dry mathematical puzzle problems (e.g., finding GCD, printing star pyramids, array element sum). 100% of exercises MUST use roleplay scenarios solving real enterprise subsystem modules (Logistics, E-commerce, Inventory WMS, CRM, Finance, Education Management).
5. **Always Embed Edge-Case Traps**:
   - Every exercise MUST embed 1-2 edge-case failure scenarios (duplicate check, capacity bound overflow, unverified state) to train proactive risk mitigation.
6. **Strict Scope Boundary & Technology Stack Isolation**:
   - 100% of concepts in exercises MUST be strictly confined to what was taught up to the current session (`allowed_scope`). ABSOLUTELY FORBIDDEN to introduce future concepts (`forbidden_scope`) or alien web frameworks unless `tech_stack` explicitly requires it.

---

## 2. Cognitive Bloom Taxonomy & I/O Rules (15-Exercise Suite)

The 15 exercises are distributed across 4 Bloom taxonomy cognitive levels:

- **I. BASIC APPLICATION (Exercises 1 to 6 - 6 Basic Application Exercises)**
  - **Objective**: Read and understand legacy code, trace execution flow, detect business logic bugs or edge-case gaps.
  - **Exercise Prompt Structure**:
    - *Business Context*: State the correct system rules.
    - *Current Problem (Customer Complaint)*: State ONLY observed symptoms/complaints from users. **ABSOLUTELY FORBIDDEN to explain technical causes or point out broken code lines**.
    - *Flawed Legacy Code*: Provide runnable, syntactically valid legacy code with subtle logic flaws. **ABSOLUTELY FORBIDDEN to put bug-spoiler comments in code** (e.g. FORBIDDEN: `# LOGIC ERROR: ...`, `# BROKEN HERE`). Code comments MUST be neutral developer notes.
    - *Output Deliverables*: (1) Test Case Report (minimum 3 test cases) pinpointing flawed logic, (2) Corrected source code.
    - *Test Case Table Format Rule*: The HTML Test Case table MUST contain EXACTLY 1 fully filled sample test case in Row 1 (STT 1) as a reference example. Row 2, Row 3, and subsequent rows MUST be left incomplete with `...` placeholders for students to trace and fill out themselves. ABSOLUTELY FORBIDDEN to complete all test case rows for the student!

- **II. ADVANCED APPLICATION (Exercises 7 to 9 - 3 Advanced Application Exercises)**
  - **Objective**: Provide 1 realistic enterprise problem statement. **Students MUST autonomously propose 1 technical solution**, design sequential processing steps, and write implementation code.
  - **Exercise Prompt Structure**:
    - *Business Context & Problem*: Business need and rationale.
    - *Business Rules & System Constraints*: Detailed formulas, rules, and calculations.
    - *Edge Cases & Constraints*: Exceptional data scenarios.
    - *Mandatory Output Deliverables*:
      - **Part 1: Analysis & Solution Design Report**:
        - *I/O Analysis*: Specify Input/Output parameters and data types.
        - *Autonomous Solution Proposal*: Student presents logic idea (FORBIDDEN to hint algorithms in prompt).
        - *Step-by-Step Design*: Sequential processing steps (bullet points or flowchart).
      - **Part 2: Implementation & Error Guards (Coding)**: Source code strictly matching designed steps and catching edge cases.

- **III. ANALYSIS (Exercises 10 to 12 - 3 Analysis Exercises)**
  - **Objective**: Analyze a problem from multiple technical perspectives, evaluate Trade-offs, and select the optimal solution.
  - **Exercise Prompt Structure**:
    - *Business Context & Rules*: System rules and calculation requirements.
    - *Constraints & Edge Cases*: Exceptional data scenarios. **ABSOLUTELY FORBIDDEN to pre-package or suggest Option A / Option B in prompt. Prompt only states the business problem; student MUST autonomously discover and propose solutions.**
    - *Mandatory Output Deliverables*:
      - **Part 1: Multi-Solution Proposal & Analysis**: Specify I/O, autonomously propose **at least 2 distinct technical solutions** within allowed scope.
      - **Part 2: Trade-off Comparison & Selection**: 5-criterion comparison table (Speed, Memory, Readability, Maintainability, Suitability) ➔ Select optimal solution.
      - **Part 3: Design & Implementation**: Pseudocode/flowchart design ➔ Complete source code catching edge cases.

- **IV. CREATIVE SYNTHESIS (Exercises 13 to 15 - 3 Creative Exercises)**
  - **Objective**: Master full feature lifecycle from an open-ended customer requirement: define requirements, design architecture, and implement feature.
  - **Exercise Prompt Structure**:
    - *Open Customer Need*: High-level unrefined pain point.
    - *Technical Constraints*: Technology stack bounds, runtime limits, Clean Code standards.
    - *Mandatory Output Deliverables*:
      - **Architecture Design**: Autonomously define modules and draw Mermaid Data Flow diagram.
      - **Complete Product**: Robust source code handling all exceptions gracefully with friendly user interaction.

---

## 3. Multi-Technology Stack Adaptation Standard

Exercise problems, sample code, and grading rubrics MUST adapt dynamically to the specified target `tech_stack`:

| Tech Stack Category | In-Memory Data Storage & Operations | Sample Code & Debugging (Ex 1 & 2) | Technical Requirements (Ex 3-6) |
| :--- | :--- | :--- | :--- |
| **Python Core** (`python/core`) | `list`, `dict`, `set`, `tuple`, `class`, `def` | `snake_case`, native `ValueError`/`KeyError`, PEP 8 | In-memory data structures, CLI functions, module imports. **NO FastAPI / NO HTTP status codes.** |
| **C / C++** (`c/cpp`) | `struct`, pointer, array, `std::vector` | `snake_case` / `camelCase`, check memory leaks | `malloc`/`free`, `struct`, pointer safety, Standard I/O. |
| **Java Core** (`java/core`) | Class, Interface, `ArrayList`, Exception | `camelCase` / `PascalCase`, OOP design | Custom exceptions, Collections framework, Clean OOP. |
| **JavaScript / Web** (`javascript/web`) | Object, Array, ES6 functions, DOM | `camelCase`, `const`/`let`, ES6 Modules | Event handling, array methods, JSON manipulation. |
| **Web Framework** (`typescript/nestjs`, `java/springboot`, `python/webapi`) | API Route, Controller, DTO/Schema, RAM DB | RESTful naming, HTTP Status Codes | Response DTOs, request validation, route parameters. |

---

## 4. Language-Specific Code Formatting Matrix

When presenting code snippets in exercises (especially Debug Exercises 1 & 2), the AI agent MUST strictly adhere to the target language's formatting standards:

| Tech Stack | Code Fence Tag | Naming Convention | Indentation | Style Guide & Standard Characteristics |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | ` ```python ` | `snake_case` (functions/vars), `PascalCase` (classes) | 4 spaces | **PEP 8**: Type hints (`def fn(x: int) -> str:`), Vietnamese explanatory comments for bugs. |
| **C** | ` ```c ` | `snake_case` (functions/vars/structs), `UPPER` (macros) | 4 spaces | **ANSI C / C99**: `#include <stdio.h>`, pointer `int *ptr`, `struct` definition. |
| **C++** | ` ```cpp ` | `camelCase` / `snake_case`, `PascalCase` (classes) | 4 spaces | **C++11/17**: `std::`, `#include <iostream>`, `#include <vector>`. |
| **Java** | ` ```java ` | `camelCase` (methods/vars), `PascalCase` (classes) | 4 spaces | **Java Code Conventions**: Packages, imports, braces on same line `{`. |
| **JavaScript** | ` ```javascript ` | `camelCase` (methods/vars), `const`/`let` | 2 spaces | **ES6+ Standard**: Arrow functions `const fn = () => {}`, strict equality `===`. |
| **TypeScript** | ` ```typescript ` | `camelCase` (methods/vars), `PascalCase` (interfaces) | 2 spaces | **Strict TypeScript**: Explicit interfaces `interface Item { id: number; }`, no implicit `any`. |
| **HTML / CSS** | ` ```html ` / ` ```css ` | `kebab-case` (classes, ids) | 2 spaces | **W3C Semantic HTML5 & BEM CSS**: `.card__title--active`, `<main>`, `<article>`. |
| **SQL** | ` ```sql ` | `UPPERCASE` (keywords), `snake_case` (tables/cols) | 4 spaces | **ANSI SQL**: `SELECT`, `FROM`, `WHERE`, `JOIN` capitalized. |

### Source Code Writing Directives:
1. **100% English Identifiers**: All variable names, function names, class names, and attributes MUST be in standard English (e.g., `inventory_list`, `check_stock_balance`).
2. **Vietnamese Comments**: Comments explaining logic or bug traps MUST be in 100% Accented Vietnamese.
3. **Consistent Indentation**: Use exact standard indentation (4 spaces for Python/C/Java, 2 spaces for JS/TS/HTML).

---

## 5. Exercise Student Document Format (5 H3 Sections in 100% Accented Vietnamese)

The generated student exercise document MUST be formatted in clean Markdown with exactly **5 H3 headers in 100% Accented Vietnamese** (ABSOLUTELY NO GRADING RUBRIC TABLE HERE):

```markdown
## <center>[Exercise Type] Specific Exercise Title in Vietnamese</center>

### **1. Mục tiêu**
- Specify concrete CLO skills mastered from session SSOT in Accented Vietnamese.

### **2. Bối cảnh & Vấn đề** (or ### **2. Vấn đề**)
- Business story and customer complaint in Accented Vietnamese.
- Automatic image placement tag or Mermaid flowchart.

### **Mermaid Flowchart Shape Standardization Contract**:
All generated Mermaid flowcharts MUST strictly use the standardized 5 shapes according to their technical function:
1. **Terminator (Start / End)**: Oval / Stadium shape `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
2. **Input / Output**: Parallelogram `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
3. **Decision (Condition Check)**: Diamond `{"Kiểm tra điều kiện?"}` with `-->|Đúng|` / `-->|Sai|` branches.
4. **Process (Action / Calculation)**: Rectangle `["Thực hiện hành động / Tính toán"]`.
5. **Flowline**: Arrow `-->` or labelled arrow `-->|Đúng|`.

**ABSOLUTELY FORBIDDEN**: Using Parallelogram `[/ /]` for Process actions/calculations! Use Rectangle `[" "]` for Process actions, and Parallelogram `[/ /]` ONLY for Input/Output.

### **3. Quy tắc nghiệp vụ** (or ### **3. Mã nguồn hiện tại** for Debug Ex 1 to 6)
- State business rules, validation constraints, or provide flawed legacy code with neutral Vietnamese comments.

### **4. Yêu cầu bài toán** (or ### **4. Yêu cầu đầu ra**)
- Explicit numbered requirement list in Accented Vietnamese (Analysis vs Implementation).

### **5. Yêu cầu nộp bài**
- Submission guidelines and GitHub repository directory naming standard (`[Tên Lớp]_[Môn Học]_SessionXX_Ex0Y`).
```

---

## 6. Grading Criteria & Rubric Standard (Separated Document in 100% Accented Vietnamese)

The grading rubric MUST be **SEPARATED INTO AN INDEPENDENT MARKDOWN DOCUMENT** (`tieu_chi_cham_diem_ai.md`) written in **100% Accented Vietnamese**:

```markdown
### **Tiêu chí chấm điểm (AI / Mentor)**

**[Exercise Title] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Thiết kế / Báo cáo Test Case — 20-30 điểm**
#### **2. Hiện thực hóa logic nghiệp vụ cốt lõi — 30-40 điểm**
#### **3. Kiểm chuẩn dữ liệu & Chặn bẫy biên Edge Cases — 20-30 điểm**
#### **4. Chất lượng mã nguồn, Clean Code & Xử lý ngoại lệ — 10 điểm**
#### **5. Quy chuẩn nộp bài GitHub & Lịch sử Commit — 10 điểm**
#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
```

---

## 7. Strict Directives & Violation Penalties

1. **TARGET OUTPUT CONTRACT**: 100% of final user-facing exercise deliverables (markdown text, titles, problem statements, business descriptions, student requirements, GitHub submission rules, and rubric criteria) MUST ALWAYS be generated in **100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất)**.
2. **STRICT NO HARDCODED STACK ASSUMPTIONS**: Never assume `FastAPI`, `HTTP status codes`, `REST API`, `Express`, or `Spring Boot` unless the session's `tech_stack` explicitly demands it.
3. **STRICT NO EMOJI**: 100% forbidden to use text emojis (❌, ✅, ⚠️, 🚀). Use text badges `[NOTE]`, `[TIP]`, `[WARNING]`.
4. **NO SCOPE LEAKAGE**: 100% forbidden to introduce concepts from `forbidden_scope`.
5. **NO ALL CAPS**: Diagram labels and headings MUST use Sentence Case or Title Case.

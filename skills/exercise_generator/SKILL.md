---
name: exercise_generator
description: Generate a suite of 6 role-based, enterprise scenario coding exercises adhering to Rikkei Education pedagogical standards (Enterprise Context, Real-world Pain Points, Anti-Scope-Leakage, Dynamic Multi-Stack Adaptation, Stack Isolation, Language-Specific Code Formatting). Target output language is 100% Accented Vietnamese.
---

# Exercise Generator Skill — Rikkei Education Standards

## 1. Overview & Architectural Vision

This skill instructs the AI agent to act as a **Senior Computer Science Professor and Academic Director** designing a standardized set of **6 exercises** for a single course learning session.

The exercise standard of Rikkei Education adheres to 5 core pedagogical principles:

1. **Real-World Enterprise Scenario**: NEVER use dry algorithmic puzzle problems (e.g., printing star pyramids, calculating factorials). Every exercise must model a concrete enterprise subsystem module (Logistics, E-commerce, Inventory WMS, CRM, Finance, Education Management).
2. **Strict Scope Boundary & SSOT Alignment**: 100% of concepts in exercises MUST be strictly confined to what was taught up to the current session (`allowed_scope`). ABSOLUTELY FORBIDDEN to introduce future concepts (`forbidden_scope`).
3. **Strict Technology Stack Isolation (No Unrequested Framework Injection)**:
   - For **Core / CLI Courses** (e.g., `python/core`, `c/cpp`, `java/core`): Use ONLY standard language features, native data structures (List, Dict, Array, Struct, Class), and native exceptions (`raise ValueError`, `raise KeyError`). ABSOLUTELY FORBIDDEN to inject web frameworks, HTTP status codes (400, 409, 500), DTO schemas, or REST API decorators unless explicitly requested in `tech_stack`.
   - For **Web Framework Courses** (e.g., `typescript/nestjs`, `java/springboot`, `python/webapi`): Include RESTful endpoints, DTO validation schemas, and HTTP status codes as appropriate.
4. **Language-Specific Code Formatting**: Source code snippets MUST adhere strictly to the target stack's style guide and syntax conventions.
5. **Clean Markdown Format & Separated Rubrics**: Exercise prompt output is clean Markdown for students (5 H3 sections), while **Grading Criteria (Rubrics) are SEPARATED INTO INDEPENDENT DOCUMENTS** for Mentors / Automated AI Evaluators.

---

## 2. Cognitive Bloom Taxonomy & I/O Rules (6-Exercise Suite)

The 6 exercises are distributed across 4 Bloom taxonomy cognitive levels:

- **I. BASIC APPLICATION (Exercise 1 & Exercise 2)**
  - Provide buggy legacy source code properly formatted in target language syntax, containing a specific business logic flaw or missing validation.
  - Student traces code, identifies the flaw, creates a Test Case report table (minimum 3 test cases: Input, actual buggy Output, expected Output), and fixes the code.
  - _Core Stack Directive_: Use native language error handling (`raise ValueError`, `raise KeyError`, error codes). Forbid `HTTPException` / `HTTP 400` unless `tech_stack` is a web framework.

- **II. ADVANCED APPLICATION (Exercise 3 & Exercise 4)**
  - Student acts as a Software Engineer taking on a new feature task.
  - Must implement complex Business Rules, Edge Cases, and data integrity checks.
  - _I/O Policy_: Provide sample I/O data (JSON payloads, CLI parameters, or function argument specs) to clarify requirements.

- **III. ANALYSIS (Exercise 5)**
  - Optimize legacy processes (slow, redundant, or memory-heavy code).
  - Student proposes **at least 2 distinct technical solutions**, builds a 5-criterion Trade-off comparison table (Speed, Memory, Maintainability, Readability, Suitability), and selects the optimal solution before coding.

- **IV. CREATIVE SYNTHESIS (Exercise 6 / Tiered Exercise 5)**
  - **MAXIMUM STUDENT AUTONOMY**: Open-ended feature expansion request.
  - ⛔ **ABSOLUTELY FORBIDDEN**: Do NOT provide pre-made I/O samples, skeleton code, or pre-listed error traps.
  - ✅ **STUDENT AUTONOMY MANDATE**:
    1. **Autonomously Design I/O Schema**: Define input/output structures from scratch.
    2. **Autonomously Discover Edge Cases**: List potential edge-case failure scenarios.
    3. **Design System Architecture**: Draw a Mermaid Data Flow / Architecture diagram.
    4. **Implementation**: Write clean, modular source code based on personal blueprint design.

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

## 5. Exercise Student Document Format (5 H3 Sections)

The student exercise problem statement MUST be formatted in clean Markdown with exactly **5 bold H3 headers** (ABSOLUTELY NO GRADING RUBRIC TABLE HERE):

```markdown
## <center>[Exercise Type] Specific Exercise Title</center>

### **1. Mục tiêu**
- Specify concrete CLO skills mastered from session SSOT.

### **2. Bối cảnh & Vấn đề** (or ### **2. Vấn đề**)
- Enterprise scenario context and business pain point.
- **MANDATORY MERMAID DIAGRAM**: Highly detailed, correctly spelled Mermaid flowchart visualizing data flow or logic process. Use standard flowchart shapes correctly: `[]` (rectangle) for process/action, `{}` (diamond) for condition/decision, `[/ /]` (parallelogram) for Input/Output.

### **3. Quy tắc nghiệp vụ** (or ### **3. Mã nguồn hiện tại** for Debug Ex 1 & 2)
- State business rules, validation constraints, or provide flawed legacy code.

### **4. Yêu cầu bài toán** (or ### **4. Yêu cầu đầu ra**)
- Explicit numbered requirement list (Analysis vs Implementation).

### **5. Yêu cầu nộp bài**
- Submission guidelines and GitHub repository directory naming standard (`[Tên Lớp]_[Môn Học]_SessionXX_Ex0Y`).
```

---

## 6. Grading Criteria & Rubric Standard (Separated Document)

The grading rubric MUST be **SEPARATED INTO AN INDEPENDENT MARKDOWN DOCUMENT** (`tieu_chi_cham_diem_ai.md`) for Mentors and AI Evaluation Agents:

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

1. **TARGET OUTPUT CONTRACT**: All student text, titles, problem statements, business descriptions, and rubric criteria MUST be produced in **100% Accented Vietnamese**.
2. **STRICT NO HARDCODED STACK ASSUMPTIONS**: Never assume `FastAPI`, `HTTP status codes`, `REST API`, `Express`, or `Spring Boot` unless the session's `tech_stack` explicitly demands it.
3. **STRICT NO EMOJI**: 100% forbidden to use text emojis (❌, ✅, ⚠️, 🚀). Use text badges `[NOTE]`, `[TIP]`, `[WARNING]`.
4. **NO SCOPE LEAKAGE**: 100% forbidden to introduce concepts from `forbidden_scope`.
5. **NO ALL CAPS**: Diagram labels and headings MUST use Sentence Case or Title Case.

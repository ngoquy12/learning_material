---
name: lab_generator
description: Structure practical hands-on labs with clear objectives, sequential execution tasks, dynamic stack adaptation, and quantitative evaluation checklists. Target output language is 100% Accented Vietnamese.
---

# Hands-on Lab Generator Skill — Rikkei Education Standards

## 1. Overview & Pedagogical Vision
Hands-on Labs serve as the practical backbone for students to develop real-world coding skills and build modular components for enterprise projects. Every Lab MUST adapt strictly to the lesson's target `tech_stack`, featuring clear objectives and step-by-step executable instructions.

## 2. Standardized 3-Part Architecture
Every Lab exercise MUST strictly follow this 3-part layout:
1. **Objectives (Mục tiêu)**:
   - State 2-3 specific technical skills the student will master matching the target `tech_stack` (e.g. For `python/core`: "Modularize data validation using Functions"; For Web Frameworks: "Establish DTO Schemas and Route Handlers").
   - State expected output benchmark: *"Expected outcome: runs stably without logic or execution errors."*
2. **Description & Step-by-Step Instructions (Mô tả & Các bước thực hiện)**:
   - State input resources matching the course stack (e.g., *"Configured project environment and sample dataset in RAM"* for Core CLI courses; *"Existing project workspace and database config"* for Web Framework courses).
   - List execution steps in progressive order (Step 1, Step 2, Step 3...) clearly and explicitly. Avoid vague, non-actionable instructions.
3. **Evaluation Checklist (Checklist Đánh giá)**:
   - Provide a quantitative checklist for students to self-verify before submission.
   - Examples (Core CLI):
     - `[ ] Function `process_inventory_batch()` correctly validates item quantities.`
     - `[ ] Raises ValueError when encountering negative quantities.`
     - `[ ] Returns complete processed item summary list.`
   - Examples (Web Framework):
     - `[ ] GET endpoint returns complete data roster.`
     - `[ ] Request DTO schema correctly validates incoming JSON fields.`
     - `[ ] Raises HTTP 404 Exception when entity is not found.`

## 💻 3. Code Styling Guidelines in Labs
When providing code snippets or step-by-step code guidance:
* **Identifiers**: 100% of variable, function, class, and property names MUST be in **English**.
* **Naming Conventions**:
  - Use **`snake_case`** for Python / C / SQL (`database_connection`, `get_user_by_email`).
  - Use **`camelCase`** or **`PascalCase`** for JavaScript / TypeScript / Java (`databaseConnection`, `getUserByEmail`).
* **Indentation**:
  - Ensure consistent 4-space indentation for block structures (2 spaces for JS/HTML). Use explicit linebreaks.

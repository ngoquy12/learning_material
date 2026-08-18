# agents/homework_agents.py
"""
Homework Agents Module for Elearning Content Factory.
Generates and audits a suite of 6 role-based, enterprise scenario coding exercises 
adhering to Rikkei Education pedagogical standards (Bloom Taxonomy, Dynamic Multi-Stack Adaptation,
Technology Stack Isolation, Strict No-Emoji, 100% Accented Vietnamese Output Contract).
"""

import json
import re
import os
import random
import xml.etree.ElementTree as ET
from typing import Dict, Any, List
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from core.llm import call_llm
from core.domain_adapters import get_domain_rules
from core.domain_knowledge import (
    BUSINESS_DOMAINS,
    get_domain_blueprint,
    select_random_domain,
    format_domain_rules_for_prompt
)
from agents.practice_agents import sanitize_vietnamese_filename, generate_and_link_diagram
from agents.reviewer_agents import check_forbidden_keywords

def homework_creator_agent(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str,
    idx: int,
    level_name: str,
    chosen_domain: str,
    forbidden_scope: str = ""
) -> Dict[str, Any]:
    """
    Homework Creator Agent:
    Generates a single homework assignment XML block (de_bai_content and tieu_chi_content)
    tailored specifically to the target tech_stack and Bloom cognitive taxonomy level.
    Supports a 15-exercise suite per session (6 Basic, 3 Advanced, 3 Analysis, 3 Creative).
    """
    print(f"    -> [LLM Generation] Creating exercise {idx}/15 ({level_name}) for domain: {chosen_domain.upper()}...")
    
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise ValueError("API Key configuration (GEMINI_API_KEY or OPENAI_API_KEY) is required to generate homework exercises.")

    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] homework_creator_agent: Yêu cầu tham số tech_stack hợp lệ.")

    # Determine stack category & technology boundaries
    from agents.practice_agents import is_cli_or_tooling_tech
    stack_lower = tech_stack.lower().strip()
    is_web_framework = any(kw in stack_lower for kw in ["fastapi", "express", "spring", "flask", "django", "nest", "web api", "rest api"])
    is_tooling = is_cli_or_tooling_tech(tech_stack)
    domain_adapter_rules = get_domain_rules(tech_stack)

    # Technology isolation instructions
    if is_web_framework:
        stack_tech_directives = """
- TECHNOLOGY DIRECTIVES (WEB FRAMEWORK COURSE):
  + Model entity endpoints, Request/Response DTO schemas, and controller route handlers.
  + Use framework-appropriate validation and HTTP status codes (e.g. 400 Bad Request, 409 Conflict, 500 Internal Error).
"""
        example_repo_prefix = f"HNKS25CNTT1_WebAPI_Session"
    elif is_tooling:
        stack_tech_directives = f"""
- TECHNOLOGY DIRECTIVES (CLI / TOOLING / PROCESS / ARCHITECTURE COURSE):
  + This course is a CLI / Tooling / Version Control / Process / Architecture subject ({tech_stack}), NOT a programming language class writing OOP application code.
  + ABSOLUTELY FORBIDDEN to force students to write complex OOP programming code (e.g., Python classes, exception handling like ValueError/KeyError, API endpoints in Python/Java/JS) unless the lesson explicitly asks for simple automation scripts.
  + Focus on real-world operational scenarios, CLI command workflows, repository/branch/config setup, system state validation, and troubleshooting/conflict resolution.
"""
        example_repo_prefix = f"HNKS25CNTT1_Tooling_Session"
    else:
        stack_tech_directives = """
- TECHNOLOGY ISOLATION DIRECTIVES (CORE PROGRAMMING COURSE):
  + ABSOLUTELY FORBIDDEN to use any web frameworks, external database libraries, HTTP status codes, routing decorators, or REST API concepts.
  + MUST use native language features only: CLI input/output, in-memory data structures (lists, dicts, arrays, structs, objects), native exception handling (e.g. `raise ValueError`, `raise KeyError` in Python; native Exception classes in Java; error return codes in C/C++).
"""
        example_repo_prefix = f"HNKS25CNTT1_Core_Session"

    # Define level specific guidelines for 15-exercise suite (1..6 Basic, 7..9 Advanced, 10..12 Analysis, 13..15 Creative)
    level_guidelines = ""
    rubric_guidelines = ""
    
    if 1 <= idx <= 6:
        if is_tooling:
            level_guidelines = f"""
- Difficulty Level: 'Basic Application {idx}'.
- PRINCIPLE: CLOSED HOW - OPEN WHAT & WHY. Keep description crisp, concise, and direct to the point.
- MUST provide a realistic buggy CLI script, broken configuration file, or flawed repository scenario in section '### **3. Mã nguồn hiện tại**' (or '### **3. Mô tả kịch bản hiện tại**').
- Legacy scenario MUST contain a specific operational flaw (e.g. broken configuration, missing tracked files, wrong branch checkout, merge conflict, flawed CLI flow).
- DO NOT list step-by-step algorithm resolution instructions. Keep hints minimal.
- Student Execution Directives:
  + Part 1: Diagnostic report table (minimum 3 test cases specifying Input CLI operations, actual buggy behavior, and expected correct result).
  + Part 2: Fix the operational flaw using standard '{tech_stack}' CLI commands and tool operations.
"""
            rubric_guidelines = f"""
Mandatory 5 Rubric Criteria Groups:
#### **1. Phân tích & Phát hiện lỗi vận hành (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác lỗi:** Correctly pinpoint the operational or configuration flaw.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Provide minimum 3 concrete test cases (Input, buggy Output, and expected Output).

#### **2. Thao tác khắc phục sự cố & Lệnh thực thi — 40 điểm**
*   **[20 điểm] Thao tác đúng lệnh nghiệp vụ:** Successfully resolve operational flaws using correct '{tech_stack}' commands.
*   **[20 điểm] Xử lý tình huống hệ thống:** Execute proper workflow commands and maintain clean system state.

#### **3. Kiểm chuẩn quy trình & Trạng thái hệ thống — 20 điểm**
*   **[10 điểm] Validate cấu hình cơ bản:** Block invalid configurations or unsafe operations.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ensure repository and workflow state remain consistent without data loss.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Explain why this operational flaw occurs in production and how to prevent it.

#### **5. Chất lượng quy trình và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Nhật ký thao tác sạch:** Clear command history, standard workflow formatting.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Push repository to GitHub following required directory structure.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tự động hóa quy trình:** Write automated script testing or validating the fix.
"""
        else:
            level_guidelines = f"""
- Difficulty Level: 'Basic Application {idx}'.
- PRINCIPLE: STRICT NO SPOILER & CLOSED HOW - OPEN WHAT & WHY (MANDATORY RE_STANDARDS).
- Section 2 ('Bối cảnh & Vấn đề'):
  + State the CORRECT business rules of the system clearly.
  + State ONLY the customer's complaint or observed symptom (e.g. "Khách hàng phàn nàn rằng tổng tiền thanh toán bị sai khi chọn vị trí ghế VIP", "Người dùng phản ánh tài khoản dưới 18 tuổi vẫn mua được vé").
  + ABSOLUTELY FORBIDDEN to explain the technical cause of the bug, reveal why it happens, or point out which line/operator is broken!
- Section 3 ('Mã nguồn hiện tại'):
  + MUST provide 100% syntactically valid and runnable legacy source code in '{tech_stack}' that contains a subtle logic/validation flaw.
  + ABSOLUTELY FORBIDDEN to put spoiler comments in code pointing out bugs (FORBIDDEN: `# LỖI LOGIC 1: ...`, `# LỖI Ở ĐÂY`, `# TRỪ SAI PHÍ...`). All comments in code MUST be standard neutral developer comments (e.g. `# Tính tổng tiền thanh toán`, `# Kiểm tra điều kiện`).
- Student Execution Directives (MANDATORY 2 PARTS):
  + Part 1 - Code Tracing & Bug Discovery (Test Case Report Table):
    * Student MUST trace code, pinpoint the exact bug line, and complete a 3-testcase table with columns: STT, Input, Buggy Output, Expected Output, Failing Line of Code (Dòng code gây lỗi), and Logic Note (Giải thích nguyên nhân) proving where and why the code fails.
    * MANDATORY TEST CASE TABLE STRUCTURE CONTRACT: The HTML Test Case table in Section 4 MUST contain EXACTLY 1 FULLY FILLED SAMPLE TEST CASE in Row 1 (STT 1) as a guide/reference example. Row 2, Row 3, and subsequent rows MUST BE LEFT INCOMPLETE (using `...` placeholders) for the student to trace and fill out! ABSOLUTELY FORBIDDEN to complete all test case rows for the student!
  + Part 2 - Source Code Correction: Student MUST fix the legacy source code to enforce correct business logic.
"""
            rubric_guidelines = f"""
Mandatory 5 Rubric Criteria Groups:
#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Correctly pinpoint the exact line in sample code handling flawed logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Provide minimum 3 concrete test cases (Input, buggy Output, and expected Output).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Successfully fix legacy code to enforce in-memory business constraints.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Implement proper native exception handling and informative error messages.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Block empty inputs or invalid data types.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ensure program handles malformed parameters gracefully without crashing.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Explain why this logic flaw occurs in production and how to prevent it.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Clean code, meaningful variable names, standard language formatting.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Push source code to GitHub repository following required directory structure.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Write automated unit test script testing the error scenarios.
"""
    elif 7 <= idx <= 9:
        level_guidelines = f"""
- Difficulty Level: 'Advanced Application {idx-6}'.
- PRINCIPLE: CLOSED HOW - OPEN WHAT & WHY (MANDATORY RE_STANDARDS).
- Present 1 realistic enterprise business scenario with detailed rules and edge-case constraints so student fully understands the context.
- ABSOLUTELY FORBIDDEN to provide step-by-step algorithm solution instructions (e.g. forbid writing "Bước 1: dùng vòng lặp for, Bước 2: dùng câu lệnh if...").
- NO-CODE HINTING POLICY: ABSOLUTELY FORBIDDEN to provide skeleton code, empty function signatures, or hint code blocks.
- Student Execution Directives (MANDATORY 2 PARTS):
  + Part 1 - Solution Analysis & Design Report:
    * Autonomously specify Input/Output parameters & data types (Phân tích I/O).
    * Autonomously propose a technical logic solution (Tự sinh viên đề xuất giải pháp).
    * Autonomously design sequential processing steps (Lập các bước thực hiện / sơ đồ luồng).
  + Part 2 - Implementation & Error Guards (Coding): Write clean modular code strictly matching designed steps and catching edge cases.
"""
        rubric_guidelines = f"""
Mandatory 5 Rubric Criteria Groups:
#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Specify complete data types and structures for Input/Output parameters.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Autonomously present logic solution and sequential processing steps (pseudocode/flowchart).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Define entity models/structures and maintain in-memory state.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Implement core business operations matching designed steps.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Enforce business constraints and raise exceptions on duplicate/limit violations.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Perform strict input format validation.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Return unified error reporting with clear descriptive messages.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** English identifiers, clear modular structure.
*   **[5 điểm] Nộp bài GitHub:** Push repository to GitHub using standard naming format.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Propose optimized memory management or conflict handling.
"""
    elif 10 <= idx <= 12:
        level_guidelines = f"""
- Difficulty Level: 'Analysis {idx-9}'.
- PRINCIPLE: STRICT NO-SPOILER & NO PRE-PACKAGED SOLUTIONS (MANDATORY RE_STANDARDS).
- Requirements: Present a clear business scenario, rules, and edge-case constraints in the {chosen_domain.upper()} domain.
- ABSOLUTELY FORBIDDEN to pre-write, suggest, or describe the 2 technical solutions in the prompt (e.g. FORBIDDEN to write 'Phương án A: ...', 'Phương án B: ...'). The student MUST autonomously discover, propose, and describe at least 2 distinct technical solutions themselves!
- STRICT SCOPE BOUNDARY MANDATE: ABSOLUTELY FORBIDDEN to mention or use unlearned advanced concepts (such as lists, dicts, classes, databases, ORM, web frameworks, FastAPI) if they are not yet taught!
- Student Execution Directives (MANDATORY 3 PARTS):
  + Part 1 - Multi-Solution Proposal & Analysis Report: Student MUST independently discover and propose at least 2 distinct technical solutions from scratch & build a Trade-off comparison report table (Speed, Memory, Maintainability, Readability, Suitability).
  + Part 2 - Trade-off Justification & Flowchart Design: Student MUST justify their choice of the optimal solution and design sequential logic steps (flowchart/pseudocode).
  + Part 3 - Implementation & Bug Prevention: Implement source code for the chosen optimal solution catching edge cases.
"""
        rubric_guidelines = f"""
Mandatory 5 Rubric Criteria Groups:
#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Detail structural and algorithmic differences between the 2 solutions.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Create 5-criterion trade-off comparison table (Time complexity, Memory, Maintainability, Readability, Use case).

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Explain rationale for chosen solution under hypothetical load.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Present detailed pseudocode/flowchart for chosen optimal solution.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Implement chosen optimal solution matching designed architecture.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Block edge-case logic errors during data processing.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Data output strictly matches specification without redundant fields.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Standard English identifiers, clean modular code.
*   **[5 điểm] Nộp bài GitHub:** Valid GitHub repository link with clean commit history.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Write benchmark script measuring runtime of both solutions on large dataset.
"""
    else:
        level_guidelines = f"""
- Difficulty Level: 'Creative Synthesis {idx-12}'.
- PRINCIPLE: CLOSED HOW - OPEN WHAT & WHY.
- Open-ended business pain point request strictly within allowed scope ({previous_lessons_text}).
- STRICT SCOPE BOUNDARY MANDATE: ABSOLUTELY FORBIDDEN to introduce unlearned future concepts or frameworks!
- CREATIVE PROACTIVITY DIRECTIVE:
  + ABSOLUTELY FORBIDDEN to provide sample Input/Output data or pre-made parameter lists.
  + ABSOLUTELY FORBIDDEN to list detailed edge cases for the student.
  + ABSOLUTELY FORBIDDEN to provide skeleton code or empty function signatures.
- Student Proactive Execution Requirements:
  + Part 1 - Self-Designed I/O Schema: Define Input/Output structures from scratch.
  + Part 2 - Self-Discovered Edge Cases: List potential edge cases and state conflicts.
  + Part 3 - Data Flow Diagram: Draw Mermaid Data Flow / Architecture diagram.
  + Part 4 - Implementation: Write clean source code from scratch based on personal design.
"""
        rubric_guidelines = f"""
Mandatory 5 Rubric Criteria Groups:
#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Autonomously define Request/Response data structures matching business expansion.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Discover minimum 3 business edge cases.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Draw detailed Mermaid diagram illustrating data lifecycle through processing layers.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Explain feature state transition mechanisms.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Implement custom expansion features matching personal design.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Ensure custom query/filter operations handle hidden or updated state records.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Implement code guards for self-discovered edge cases with descriptive messages.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Modular, extensible code with English identifiers.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Clear commits, README instructions for running creative project.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Add data recovery or audit logging module.
"""

    domain_blueprint = get_domain_blueprint(chosen_domain)
    domain_prompt_block = format_domain_rules_for_prompt(domain_blueprint)

    forbidden_scope_instruction = ""
    if forbidden_scope:
        forbidden_scope_instruction = f"\nPHẠM VI CẤM DÙNG (FORBIDDEN SCOPE): {forbidden_scope}.\nTUYỆT ĐỐI CẤM SỬ DỤNG CÁC KIẾN THỨC/TỪ KHÓA BỊ CẤM NÀY VÀO BÀI TẬP (BAO GỒM CẢ CÁC BÀI PHÂN TÍCH VÀ SÁNG TẠO).\n"

    system_prompt = f"""You are a Senior Computer Science Professor specializing in designing standardized college-level essay & code homework assignments.
Your task is to generate EXACTLY 1 homework exercise formatted in clean XML complying with strict pedagogical and domain standards.

COURSE & SESSION CONTEXT:
- Session: {session_id} - {session_title}
- Target Technology Stack: {tech_stack}
- Allowed Knowledge Boundary: {previous_lessons_text}{forbidden_scope_instruction}

{domain_prompt_block}

INDUSTRY CODING RULES FOR THIS STACK:
{domain_adapter_rules}

{stack_tech_directives}

EXERCISE REQUIREMENTS:
- Exercise Index in Session: Exercise #{idx} / 15.
- Cognitive Bloom Taxonomy Level: {level_name}
- Required Enterprise Subsystem Domain: {domain_blueprint.get('name_vi', chosen_domain.upper())} ({chosen_domain.upper()}).
- UNIFIED DOMAIN ECOSYSTEM DIRECTIVE (MANDATORY): All 15 exercises in this session MUST be set in the SAME '{domain_blueprint.get('name_vi', chosen_domain.upper())}' ({chosen_domain.upper()}) domain. Exercise #{idx} is a progressive module in this system. Lower-level exercises (Exercises 1-6) serve as building blocks/premises for higher-level exercises (Exercises 7-15).
- SIMPLICITY & RELATABILITY DIRECTIVE: Present the business scenario using practical, intuitive rules that students can relate to immediately (e.g. food delivery order, ride booking, cinema ticketing, coffee POS). Avoid overly complex mathematical formulas or dense academic jargon.

DIFFICULTY LEVEL GUIDELINES ({level_name.upper()}):
{level_guidelines}

MANDATORY FORMATTING & LANGUAGE DIRECTIVES:
0. STRICT NO EMOJI DIRECTIVE: ABSOLUTELY FORBIDDEN to use text emojis in title, body, or source code. Use text labels [NOTE], [TIP], [WARNING], [REQUIREMENT] instead.
0.1 DYNAMIC PROGRESSIVE KNOWLEDGE BOUNDARY:
- You MUST ONLY use concepts taught up to the current Session ({session_id} - {session_title}) and prior lessons: {previous_lessons_text}.
- ABSOLUTELY FORBIDDEN to introduce concepts, syntax, functions, libraries, or structures from future lessons or forbidden scope: {forbidden_scope_instruction}!
- FORBIDDEN KEYWORDS BAN FOR CORE/CLI COURSES ({tech_stack}): ABSOLUTELY FORBIDDEN to mention or write any of the following terms anywhere in exercise body, titles, or rubric: fastapi, uvicorn, pydantic, sqlalchemy, express, springboot, rest api, database, orm!
0.3 MERMAID FLOWCHART SHAPE STANDARDIZATION CONTRACT:
- Whenever generating a Mermaid flowchart, you MUST strictly use the 5 standardized shapes according to technical function:
  1. Terminator (Start / End): Oval / Stadium shape `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
  2. Input / Output: Parallelogram `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
  3. Decision (Condition Check): Diamond `{"Kiểm tra điều kiện?"}` with `-->|Đúng|` / `-->|Sai|` branches.
  4. Process (Action / Calculation): Rectangle `["Thực hiện hành động / Tính toán"]`.
  5. Flowline: Arrow `-->` or labelled arrow `-->|Đúng|`.
- ABSOLUTELY FORBIDDEN to use Parallelogram `[/ /]` for Process actions/calculations! Use Rectangle `[" "]` for Process actions, and Parallelogram `[/ /]` ONLY for Input/Output.
0.2 CODE FORMATTING & SYNTAX DIRECTIVE ({tech_stack}):
- All code snippets MUST strictly follow syntax, naming, indentation, and code fence standards of '{tech_stack}'.
- Specify proper code fence tag (e.g. ```python, ```c, ```cpp, ```java, ```javascript, ```typescript, ```sql, ```html).
- Source code identifiers (variables, functions, classes) MUST be 100% in ENGLISH. Comments explaining logic MUST be in Vietnamese with full diacritics.
1. REQUIRED EXERCISE HEADINGS STRUCTURE: Must contain exactly 5 bold H3 section headers in Accented Vietnamese:
   ### **1. Mục tiêu**
   ### **2. Vấn đề** (or ### **2. Bối cảnh & Vấn đề**)
   ### **3. Quy tắc nghiệp vụ** (or ### **3. Mã nguồn hiện tại** for debug exercises 1 & 2)
   ### **4. Yêu cầu bài toán** (or ### **4. Yêu cầu đầu ra**)
   ### **5. Yêu cầu nộp bài**
2. CENTERED H2 MAIN TITLE:
   - Use tag: ## <center>[Exercise Type] Specific Exercise Title</center>. Main title MUST be in ACCENTED VIETNAMESE.
   - FORBIDDEN to write exercise index numbers in this main title (e.g. forbid '## <center>Bài 1: ...</center>').
3. ACADEMIC TONE & TARGET OUTPUT CONTRACT:
   - Target Output Language: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất) for exercise text, descriptions, problem statements, and rubric items.
   - FORBIDDEN informal words (nhé, nha, nhé các bạn).
   - FORBIDDEN AI assistant mentions (AI, ChatGPT, Copilot).
   - FORBIDDEN difficulty labels like "sinh viên yếu", "độ khó:" in exercise body.
4. INDIVIDUAL SUBMISSION REQUIREMENTS:
   Section 5 MUST describe submission guidelines in Accented Vietnamese following this format:
   ### **5. Yêu cầu nộp bài**
   Học viên cần nộp:
   *   Phần phân tích/báo cáo và mã nguồn triển khai.
   *   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_Session{session_id}_Ex{idx}.
       Ví dụ: {example_repo_prefix}_{session_id}_Ex{idx}
5. IMAGE PROMPT SPECIFICATION (Clean 2D Flat Vector & NO ALL CAPS):
   - MUST include in section '### **2. Vấn đề**' (directly below scenario description) in EVERY exercise:
     Prompt tạo ảnh: A clean 2D flat vector technical illustration of [detailed business logic/flow description here]. Minimalist infographics style, elegant layout, muted corporate color palette (navy blue, slate gray, soft emerald accents). Clear lines, no 3D elements, no glowing neon effects. All text labels must be in Sentence Case or Title Case (NEVER ALL CAPS), keeping key technical terms in English while using Vietnamese for annotations.
6. HTML TABLE STYLING REQUIREMENT:
   - Any HTML table MUST include attribute: style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%".
7. DYNAMIC KNOWLEDGE BOUNDARY SCOPING (MANDATORY):
   All required knowledge in the exercise MUST be strictly scoped within taught lessons. ABSOLUTELY FORBIDDEN to request unlearned technologies or frameworks outside taught scope.

MANDATORY OUTPUT FORMAT — SINGLE VALID XML BLOCK ENCLOSED IN <exercise>...</exercise>:
- <folder_name>: Lowercase folder name without spaces (e.g. '1_debug_trung_ma', '3_create_phieu_dang_ky').
- <title>: Concise exercise title in ACCENTED VIETNAMESE (e.g. '[Vận dụng cơ bản 1] Sửa lỗi kiểm tra lô hàng kho').
- <de_bai_content>: Markdown exercise body content wrapped inside CDATA block (sections 1. Mục tiêu through 5. Yêu cầu nộp bài, ABSOLUTELY NO grading rubric here).
- <tieu_chi_content>: Detailed Markdown grading rubric wrapped inside CDATA block following guidelines:
  + Start with H3 header: ### **Tiêu chí chấm điểm (AI)**
  + Followed by: **[Exercise Title] — Tổng điểm: 100 điểm**
  + Implement 5 rubric groups according to difficulty level:
{rubric_guidelines}

EXPECTED OUTPUT XML PATTERN:
<exercise>
  <folder_name>1_debug_trung_ma</folder_name>
  <title>[Vận dụng cơ bản 1] Sửa lỗi kiểm tra lô hàng kho</title>
  <de_bai_content><![CDATA[
Markdown exercise body content here...
  ]]></de_bai_content>
  <tieu_chi_content><![CDATA[
### **Tiêu chí chấm điểm (AI)**
**[Exercise Title] — Tổng điểm: 100 điểm**
...
  ]]></tieu_chi_content>
</exercise>
"""
    user_prompt = f"Generate exercise prompt and grading rubric XML for Exercise #{idx} ({level_name}) in subsystem domain {chosen_domain.upper()} for session {session_id}."
    
    ex_data = None
    for attempt in range(3):
        response = None
        try:
            response = call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                json_mode=False,
                agent_name=f"Homework Creator ({level_name})",
                session_id=session_id
            )
            if not response:
                continue
            
            # Parse exercise XML
            xml_clean = response.strip()
            if xml_clean.startswith("```xml"):
                xml_clean = xml_clean[6:]
            if xml_clean.startswith("```"):
                xml_clean = xml_clean[3:]
            if xml_clean.endswith("```"):
                xml_clean = xml_clean[:-3]
            xml_clean = xml_clean.strip()
            
            start_idx = xml_clean.find("<exercise>")
            end_idx = xml_clean.rfind("</exercise>")
            if start_idx != -1 and end_idx != -1:
                xml_clean = xml_clean[start_idx:end_idx + 11]
                
            root = ET.fromstring(xml_clean)
            folder_name_node = root.find("folder_name")
            title_node = root.find("title")
            de_bai_node = root.find("de_bai_content")
            tieu_chi_node = root.find("tieu_chi_content")
            
            folder_name = folder_name_node.text.strip() if folder_name_node is not None and folder_name_node.text else f"{idx}_exercise"
            title = title_node.text.strip() if title_node is not None and title_node.text else f"Bài tập {idx}"
            de_bai_content = de_bai_node.text.strip() if de_bai_node is not None and de_bai_node.text else ""
            tieu_chi_content = tieu_chi_node.text.strip() if tieu_chi_node is not None and tieu_chi_node.text else ""
            
            if de_bai_content and tieu_chi_content:
                ex_data = {
                    "index": idx,
                    "level": level_name,
                    "folder_name": folder_name,
                    "title": title,
                    "content": de_bai_content,
                    "rubric": tieu_chi_content
                }
                break
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to parse XML for homework level {level_name}: {e}")
            if response:
                print(f"      [Debug] Response length: {len(response)} chars")
                print(f"      [Debug] Response start:\n{response[:200]}")
                print(f"      [Debug] Response end:\n{response[-200:]}")
                
    if not ex_data:
        raise ValueError(f"Failed to generate homework exercise for level {level_name} after 3 attempts.")
        
    return ex_data

def homework_reviewer_agent(
    exercises: List[Dict[str, Any]],
    tech_stack: str,
    chosen_domain: str,
    previous_lessons_text: str,
    session_id: str,
    forbidden_scope: str = ""
) -> Dict[str, Any]:
    """
    Homework Reviewer Agent:
    Audits the generated 6-exercise batch for pedagogical quality, structural compliance,
    and STRICT TECHNOLOGY BOUNDARY ISOLATION (preventing unrequested web framework leakage into core CLI courses).
    """
    print("  [Homework Reviewer] Auditing generated theoretical homework session exercises...")
    
    # 1. Check quantity must be exactly 6
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] homework_reviewer_agent: Yêu cầu tham số tech_stack hợp lệ.")
        
    stack_lower = tech_stack.lower().strip()
    is_core_cli = "core" in stack_lower or "cli" in stack_lower or not any(kw in stack_lower for kw in ["fastapi", "express", "spring", "flask", "django", "nest", "web api", "rest api"])

    for idx, ex in enumerate(exercises):
        content = ex.get("content", "")
        rubric = ex.get("rubric", "")
        title = ex.get("title", "")
        folder_name = ex.get("folder_name", "")
        level = ex.get("level", "")
        
        combined_text = content + "\n" + rubric
        
        # 1.1 Forbidden Scope Contract Check
        if forbidden_scope:
            raw_forb = str(forbidden_scope).replace("CẤM:", "").strip()
            forb_set = set(item.strip().lower() for item in raw_forb.split(",") if item.strip())
            forbidden_feedback = check_forbidden_keywords(combined_text, tech_stack, forb_set)
            if forbidden_feedback:
                feedback_msg = f"Exercise #{idx+1} '{title}' vi phạm FORBIDDEN SCOPE: {forbidden_feedback} Yêu cầu sinh lại không dùng các từ khóa này."
                print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}
        
        # 2. Technology Stack Boundary Isolation Guard: Block unrequested web frameworks in Core/CLI courses
        if is_core_cli:
            forbidden_web_kws = ["fastapi", "httpexception", "basemodel", "uvicorn", "status_code=", "@app.", "rest api endpoint"]
            found_forbidden = [kw for kw in forbidden_web_kws if kw in combined_text.lower()]
            if found_forbidden:
                feedback_msg = (
                    f"Exercise #{idx+1} '{title}' contains unrequested web framework concept(s) ({', '.join(found_forbidden)}) "
                    f"for a Core/CLI technology stack ({tech_stack}). Re-generate using pure native language features without web APIs."
                )
                print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

        # 3. Check forbidden informal words (case-insensitive)
        forbidden_words = ["nhé", "thân mến", "nhé các bạn", "nhe", "nha", "assistant", "chatgpt", "openai", "gemini", "llm", "copilot"]
        for word in forbidden_words:
            pattern = rf"\b{word}\b"
            if re.search(pattern, combined_text, re.IGNORECASE):
                print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' contains forbidden AI/informal word: '{word}'. Bypassing minor warning.")
                
        # 4. Check case-sensitive "AI" (exempting "Tiêu chí chấm điểm (AI)" header in rubric)
        combined_text_for_ai_check = combined_text
        for header_exempt in ["Tiêu chí chấm điểm (AI)", "Tiêu chí chấm điểm (ai)", "tiêu chí chấm điểm (AI)", "tiêu chí chấm điểm (ai)"]:
            combined_text_for_ai_check = combined_text_for_ai_check.replace(header_exempt, "")
        if re.search(r"\bAI\b", combined_text_for_ai_check):
            print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' contains standalone acronym 'AI'. Bypassing minor warning.")
            
        # 5. Check student discriminatory categorization labels
        discriminatory_labels = ["học viên yếu", "học sinh giỏi", "học lực", "dành cho học viên", "dành cho sinh viên", "mức độ:", "độ khó:"]
        for fl in discriminatory_labels:
            if fl in combined_text.lower():
                print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' contains difficulty label '{fl}'. Bypassing minor warning.")
                
        # 6. Verify H3 section headings in content (MANDATORY GATE)
        required_headers = [
            r"###\s*(\*\*|\*|)?1\.\s*Mục tiêu(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?2\.\s*(Bối cảnh & )?Vấn đề(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?3\.\s*(Quy tắc nghiệp vụ|Mã nguồn hiện tại|Quy tắc xử lý)(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?4\.\s*(Yêu cầu bài toán|Yêu cầu đầu ra)(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?5\.\s*Yêu cầu nộp bài(\*\*|\*|)?[\s:]*"
        ]
        for header in required_headers:
            if not re.search(header, content):
                feedback_msg = f"Exercise #{idx+1} '{title}' lacks mandatory H3 section header matching pattern '{header}'."
                print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

        # 7. Verify Rubric format in tieu_chi_cham_diem_ai.md (MANDATORY GATE)
        if not rubric or not rubric.startswith("### **Tiêu chí chấm điểm (AI)**"):
            feedback_msg = f"Exercise #{idx+1} '{title}' missing grading rubric or rubric does not start with '### **Tiêu chí chấm điểm (AI)**'!"
            print(f"  [Homework Reviewer REJECT] {feedback_msg}")
            return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

        # 8. Check Mermaid Flowchart shape standard compliance (MANDATORY GATE)
        if "```mermaid" in content:
            mermaid_blocks = re.findall(r"```mermaid\n?(.*?)```", content, re.DOTALL)
            for m_block in mermaid_blocks:
                if re.search(r"\[/\s*(?:tính|gán|thực hiện|xử lý|khởi tạo|cập nhật)\b", m_block, re.IGNORECASE):
                    feedback_msg = f"Exercise #{idx+1} '{title}' uses Parallelogram [/ /] for calculation/action in Mermaid flowchart. Parallelogram is ONLY for Input/Output; use Rectangle [' '] for Process actions!"
                    print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                    return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

        # Determine global exercise number (1 to 15) correctly even during retry subsets
        ex_level_num = ex.get("level_num")
        if not ex_level_num:
            match_num = re.search(r"^(\d+)_", folder_name)
            if match_num:
                ex_level_num = int(match_num.group(1))
            else:
                ex_level_num = idx + 1

        # 9. ENFORCE STRICT NO-SPOILER POLICY PER LEVEL
        if ex_level_num in range(1, 7):
            if "```" not in content:
                feedback_msg = f"Debug Exercise #{ex_level_num} '{title}' missing legacy code snippet in Section 3!"
                print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

            # Check for spoiler comments in legacy code
            code_blocks = re.findall(r"```(?:[a-zA-Z0-9_+#-]+)?\n?(.*?)```", content, re.DOTALL)
            for block in code_blocks:
                if re.search(r"#\s*(lỗi|bug|sai ở đây|lỗi logic|bị lỗi)", block, re.IGNORECASE):
                    feedback_msg = f"Exercise #{ex_level_num} '{title}' contains spoiler comment in legacy code (e.g. '# LỖI LOGIC'). Legacy code comments must be neutral and not reveal the bug!"
                    print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                    return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

            # Verify Test Case table structure for Basic Application exercises (1-6)
            if "<table" in content:
                tr_list = re.findall(r"<tr[^>]*>(.*?)</tr>", content, re.DOTALL | re.IGNORECASE)
                table_has_placeholders = any("..." in tr for tr in tr_list[1:]) if len(tr_list) > 1 else False
                if not table_has_placeholders and len(tr_list) >= 3:
                    feedback_msg = f"Exercise #{ex_level_num} '{title}' has all test case rows fully completed in prompt table. Row 1 MUST be a sample testcase, while Row 2 & 3 MUST be left incomplete ('...') for students!"
                    print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                    return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}
        else:
            # For Analysis exercises (10-12), forbid pre-packaged solution option descriptions in prompt (e.g. 'Phương án A:', 'Phương án B:')
            if 10 <= ex_level_num <= 12:
                if re.search(r"(phương án a:|phương án b:|giải pháp a:|giải pháp b:)", content, re.IGNORECASE):
                    feedback_msg = f"Exercise #{ex_level_num} '{title}' contains pre-packaged solution hints (e.g. 'Phương án A: / Phương án B:'). Prompt must not spoil solution options! Let students propose solutions."
                    print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                    return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

            # For levels 7-15, forbid full solution code skeletons
            all_code_blocks = re.findall(r"```(?:[a-zA-Z0-9_+#-]+)?\n?(.*?)```", content, re.DOTALL)
            for block in all_code_blocks:
                if any(kw in block for kw in ["def ", "class ", "function ", "public class ", "struct ", "interface "]):
                    if len(block.strip().split("\n")) > 10:
                        feedback_msg = f"Exercise #{ex_level_num} '{title}' contains pre-made solution code implementation (>10 lines) in prompt! Prompt must not spoil implementation code for students."
                        print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                        return {"status": "REJECTED", "feedback": feedback_msg, "failed_idx": idx}

    return {"status": "APPROVED", "feedback": "All session exercises successfully passed pedagogical and technology scope review."}

def sanitize_homework_markdown(content: str, level_name: str = "") -> str:
    if not content:
        return content
        
    import re
    # 1. Clean JSON artifacts/noise from code block fence closures
    content = re.sub(r'```",\s*$', '```', content, flags=re.MULTILINE)
    content = re.sub(r'```",\s*\n\s*\.', '```', content, flags=re.MULTILINE)
    
    from agents.creators.common_utils import normalize_markdown_headers
    content = normalize_markdown_headers(content)

    # Split content by markdown code blocks to avoid corrupting code segments
    parts = content.split("```")
    for i in range(len(parts)):
        # Even indices (0, 2, 4...) are non-code markdown text segments
        if i % 2 == 0:
            parts[i] = parts[i].replace('",\n  "example_good": "Thực hành tốt:', '\n\n#### **Thực hành tốt:**\n')
            parts[i] = parts[i].replace('",\n  "example_good": "Thực hành tốt: ', '\n\n#### **Thực hành tốt:**\n')
            parts[i] = parts[i].replace('",\n  "example_bad": "Thực hành sai:', '\n\n#### **Thực hành sai:**\n')
            parts[i] = parts[i].replace('",\n  "example_bad": "Thực hành sai: ', '\n\n#### **Thực hành sai:**\n')
            parts[i] = parts[i].replace('",\n  "resolve_title": "Quản trị rủi ro và Nguyên tắc thực hành tốt nhất khi thao tác List', '\n\n#### **Cách phòng ngừa & Xử lý:**\n')
            parts[i] = parts[i].replace('",\n  "resolve_title": "Quản trị rủi ro', '\n\n#### **Cách phòng ngừa & Xử lý:**\n')
            parts[i] = parts[i].replace('",\n  ', '\n\n')
            parts[i] = parts[i].replace('",', '')
            
            # Sửa lỗi rác của resolve_title trong bài 16/17
            parts[i] = parts[i].replace('#### **Cách phòng ngừa & Xử lý:**\n\n```\n\n.\n\n### **4. Yêu cầu bài toán**', '### **4. Yêu cầu bài toán**')
            parts[i] = parts[i].replace('#### **Cách phòng ngừa & Xử lý:**\n\n```\n\n.', '')

    content = "```".join(parts)
    
    # 2. Restore broken python print statements
    content = re.sub(
        r'print\("# Danh sách sau khi xử lý thành công:\s*([\w_]+)\)', 
        r'print("# Danh sách sau khi xử lý thành công:", \1)', 
        content
    )
    content = re.sub(
        r'print\("# Số lượng phần tử còn lại:\s*(len\([\w_]+\))\)', 
        r'print("# Số lượng phần tử còn lại:", \1)', 
        content
    )
    
    # 3. Standardize H3 Headers & Ensure clean linebreaks
    content = normalize_markdown_headers(content)
    
    # 4. Standardize H3 Headers
    content = re.sub(r'### \*\*2\. Vấn đề\*\*|### \*\*2\. Bối cảnh & Yêu cầu tổng hợp\*\*|### \*\*2\. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)\*\*', '### **2. Bối cảnh & Vấn đề**', content)
    if level_name and "cơ bản" in level_name.lower():
        content = re.sub(r'### \*\*3\. Quy tắc nghiệp vụ\*\*|### \*\*3\. Quy tắc nghiệp vụ & Luồng xử lý tích hợp\*\*|### \*\*3\. Quy tắc nghiệp vụ & Từ khóa trọng tâm\*\*', '### **3. Mã nguồn hiện tại**', content)
    else:
        content = re.sub(r'### \*\*3\. Mã nguồn hiện tại\*\*|### \*\*3\. Quy tắc nghiệp vụ & Luồng xử lý tích hợp\*\*|### \*\*3\. Quy tắc nghiệp vụ & Từ khóa trọng tâm\*\*', '### **3. Quy tắc nghiệp vụ**', content)
        
    content = re.sub(r'### \*\*4\. Yêu cầu đầu ra\*\*|### \*\*4\. Hướng dẫn Giảng viên Live-Demo & Mã nguồn Mẫu\*\*|### \*\*4\. Yêu cầu bài toán (Sản phẩm nộp)\*\*', '### **4. Yêu cầu bài toán**', content)
    content = re.sub(r'### \*\*5\. Hướng dẫn nộp bài\*\*', '### **5. Yêu cầu nộp bài**', content)
    
    # 5. Standardize H1 Header prefix
    if level_name:
        h1_match = re.search(r'## <center>(.*?)</center>', content)
        if h1_match:
            h1_text = h1_match.group(1).strip()
            if level_name not in h1_text:
                new_h1_text = f"[{level_name}] {h1_text}"
                new_h1_text = re.sub(r'\[.*?\]\s*\[.*?\]', f"[{level_name}]", new_h1_text)
                content = content.replace(h1_match.group(0), f"## <center>{new_h1_text}</center>")
                
    # 6. Remove banned emojis/symbols
    content = content.replace("➔", "->")
    content = content.replace("▶", "")
    content = content.replace("❌", "[LỖI]")
    content = content.replace("✅", "[ĐÚNG]")
    content = content.replace("⚠️", "[CẢNH BÁO]")
    
    # Sửa lỗi rác của resolve_title trong bài 16/17
    content = content.replace('#### **Cách phòng ngừa & Xử lý:**\n\n```\n\n.\n\n### **4. Yêu cầu bài toán**', '### **4. Yêu cầu bài toán**')
    content = content.replace('#### **Cách phòng ngừa & Xử lý:**\n\n```\n\n.', '')
    
    return normalize_markdown_headers(content)

def session_homework_pipeline(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str,
    output_dir: Path = None,
    session_dir_path: str = None,
    forbidden_scope: str = ""
) -> List[Dict[str, Any]]:
    """
    Session Homework Pipeline:
    Coordinates the 15-exercise creation and review loop for a single session,
    saving the resulting Markdown files and diagram prompts into session output directory.
    (6 Basic Application, 3 Advanced Application, 3 Analysis, 3 Creative Synthesis).
    Features per-exercise resilience (retrying only failed individual exercises).
    """
    print(f"\n==================================================")
    print(f" 📝 [SESSION HOMEWORK FACTORY] Generating 15 Exercises for Session: {session_id} - {session_title}")
    print(f"    - Target Tech Stack: {tech_stack}")
    print(f"==================================================")
    
    if session_dir_path:
        session_dir = Path(session_dir_path)
    elif output_dir:
        session_dir = Path(output_dir) / session_id
    else:
        session_dir = Path("output") / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    homework_dir = session_dir / "Bài tập"
    homework_dir.mkdir(exist_ok=True)
    
    # Select a relatable open-ended enterprise business domain from our rich registry
    domain_info = select_random_domain()
    chosen_domain = domain_info["domain_id"]
    print(f"  [Homework Pipeline] Selected Unified Relatable Domain Context: {domain_info['name_vi']} ({chosen_domain})")
    
    levels = [
        ("Vận dụng cơ bản 1", 1),
        ("Vận dụng cơ bản 2", 2),
        ("Vận dụng cơ bản 3", 3),
        ("Vận dụng cơ bản 4", 4),
        ("Vận dụng cơ bản 5", 5),
        ("Vận dụng cơ bản 6", 6),
        ("Vận dụng nâng cao 1", 7),
        ("Vận dụng nâng cao 2", 8),
        ("Vận dụng nâng cao 3", 9),
        ("Phân tích 1", 10),
        ("Phân tích 2", 11),
        ("Phân tích 3", 12),
        ("Sáng tạo 1", 13),
        ("Sáng tạo 2", 14),
        ("Sáng tạo 3", 15)
    ]
    
    candidate_exercises = [None] * len(levels)
    pending_indices = list(range(len(levels)))

    # Per-exercise resilient retry loop (up to 10 rounds)
    for round_num in range(10):
        if not pending_indices:
            break
        print(f"  [Homework Pipeline] Round {round_num+1}: Generating {len(pending_indices)} exercises (Indices: {[i+1 for i in pending_indices]})...")
        with ThreadPoolExecutor(max_workers=min(len(pending_indices), 10)) as executor:
            futures = {
                executor.submit(
                    homework_creator_agent,
                    session_id=session_id,
                    session_title=session_title,
                    tech_stack=tech_stack,
                    previous_lessons_text=previous_lessons_text,
                    idx=levels[i][1],
                    level_name=levels[i][0],
                    chosen_domain=chosen_domain,
                    forbidden_scope=forbidden_scope
                ): i
                for i in pending_indices
            }
            for fut in futures:
                i = futures[fut]
                try:
                    candidate_exercises[i] = fut.result()
                except Exception as e:
                    print(f"  [Homework Warning] Exercise #{i+1} generation exception: {e}")

        # Review candidate exercises individually
        new_pending = []
        for i in range(len(levels)):
            ex = candidate_exercises[i]
            if not ex:
                new_pending.append(i)
                continue
            review_res = homework_reviewer_agent(
                [ex], 
                tech_stack, 
                chosen_domain, 
                previous_lessons_text,
                session_id,
                forbidden_scope
            )
            if review_res["status"] != "APPROVED":
                print(f"  [Homework Reviewer] Exercise #{i+1} REJECTED: {review_res['feedback']}. Scheduling re-generation...")
                candidate_exercises[i] = None
                new_pending.append(i)

        pending_indices = new_pending

    exercises_data = [ex for ex in candidate_exercises if ex is not None]
    if len(exercises_data) < len(levels):
        raise ValueError(f"Unable to generate all 15 exercises for session {session_id}. Only generated {len(exercises_data)}/15.")
        
    print(f"  [Homework Reviewer] ALL {len(exercises_data)} EXERCISES APPROVED SUCCESSFULLY!")
        
    # Clean legacy artifacts in homework_dir
    if homework_dir.exists():
        import shutil
        for item in homework_dir.glob("*"):
            if item.name == "images":
                continue
            if item.is_dir():
                try:
                    shutil.rmtree(item)
                except Exception:
                    pass
            elif item.is_file() and item.name.startswith("bai_"):
                try:
                    item.unlink()
                except Exception:
                    pass

    # Save the 6 exercises in their respective subfolders
    for idx, ex in enumerate(exercises_data):
        title = ex.get("title", "Bài tập")
        clean_name = sanitize_vietnamese_filename(title).replace(".md", "")[:45].rstrip("_")
        ex_folder = homework_dir / f"{idx+1}_{clean_name}"
        ex_folder.mkdir(parents=True, exist_ok=True)
        
        filename_no_ext = f"bai_{idx+1:02d}_{clean_name}"
        content = ex.get("content", "")
        rubric = ex.get("rubric", "")
        
        # Post-process content to link/generate diagram image and sanitize math formulas
        from agents.creators.common_utils import clean_markdown_formulas
        processed_content = clean_markdown_formulas(generate_and_link_diagram(content, homework_dir, filename_no_ext))
        processed_content = sanitize_homework_markdown(processed_content, level_name=levels[idx][0])
        
        # Save de_bai_bai_tap.md
        desc_file_path = ex_folder / "de_bai_bai_tap.md"
        with open(desc_file_path, "w", encoding="utf-8") as f:
            f.write(processed_content)
            
        # Save direct bai_tap_{idx+1}.md in homework_dir
        direct_file_path = homework_dir / f"bai_tap_{idx+1}.md"
        with open(direct_file_path, "w", encoding="utf-8") as f:
            f.write(processed_content)
            
        # Save tieu_chi_cham_diem_ai.md
        rubric_file_path = ex_folder / "tieu_chi_cham_diem_ai.md"
        with open(rubric_file_path, "w", encoding="utf-8") as f:
            f.write(rubric)
            
        print(f"  [Success] Saved homework folder: {ex_folder}")

    # -------------------------------------------------------------------------
    # 1. Tự động sinh Bài tập Tổng hợp Session (Giảng viên Demo trên lớp)
    # -------------------------------------------------------------------------
    demo_synthesis_folder = homework_dir / "16_tong_hop_demo_giang_vien_tren_lop"
    demo_synthesis_folder.mkdir(exist_ok=True, parents=True)
    
    print(f"  [Homework Pipeline] Generating Instructor Demo Synthesis Assignment for {session_id}...")
    demo_prompt = f"""You are a Master Technical Trainer and Lead Curriculum Architect at Rikkei Education.
Generate a COMPLETE, Standardized Instructor Live-Demo Synthesis Assignment for Session: {session_id} - {session_title}.
Target System Domain: {chosen_domain.upper()}
Target Technology Stack: {tech_stack}
Session Scope: {previous_lessons_text}
Forbidden Scope: {forbidden_scope}

This synthesis assignment is designed FOR THE INSTRUCTOR TO LIVE-DEMO IN CLASS, synthesizing ALL core concepts taught in Session {session_id} at a basic level (approx. 30 minutes execution time). It must NOT contain any solution code, skeleton code, or code snippets in the description.

Return your response in EXACTLY the following XML schema (no conversational text outside XML):
<exercise>
<de_bai_content>
## <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp ({chosen_domain.upper()})</center>

### **1. Mục tiêu**
- **Kiến thức**: [Objectives for integration of all session concepts]
- **Kỹ năng**: [Skills to trace execution and handle basic logic]
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
- Describe a realistic business scenario in {chosen_domain.upper()} system that integrates all core session lessons.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**
- Design exactly 3 simple functions representing the workflow.
- Format EACH function using exactly these 3 lines:
  - **Nghiệp vụ**: [Clear business logic description]
  - **Đầu vào (Input)**: [What inputs are required]
  - **Đầu ra (Output)**: [What is the printed status/output]

### **4. Yêu cầu nộp bài**
Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_{session_id.replace(' ', '')}_Demo`.
Ví dụ: `HNKS25CNTT1_Core_{session_id.replace(' ', '')}_Demo`
</de_bai_content>
<tieu_chi_content>
### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
</tieu_chi_content>
</exercise>

CRITICAL RULES:
- ABSOLUTELY NO Python/C/Java code samples, skeleton code, or solutions in the output. The student must write all code from scratch.
- The 3 functions in Section 3 must strictly have the bold titles **Nghiệp vụ**, **Đầu vào (Input)**, **Đầu ra (Output)**.
- All text in de_bai_content must be in 100% Accented Vietnamese.
"""
    demo_response = call_llm(
        system_prompt="Bạn là Chuyên gia thiết kế bài tập Demo tổng hợp cho Giảng viên Rikkei Education.",
        user_prompt=demo_prompt,
        json_mode=False,
        agent_name="Demo_Synthesis_Exercise_Agent",
        session_id=session_id
    )
    
    demo_de_bai = ""
    demo_rubric = ""
    if demo_response:
        xml_clean = demo_response.strip()
        if xml_clean.startswith("```xml"):
            xml_clean = xml_clean[6:]
        if xml_clean.startswith("```"):
            xml_clean = xml_clean[3:]
        if xml_clean.endswith("```"):
            xml_clean = xml_clean[:-3]
        xml_clean = xml_clean.strip()
        
        import re
        # Extract de_bai_content using robust regex
        de_bai_match = re.search(r"<de_bai_content>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</de_bai_content>", xml_clean, re.DOTALL | re.IGNORECASE)
        if de_bai_match:
            demo_de_bai = de_bai_match.group(1).strip()
            
        # Extract tieu_chi_content using robust regex
        rubric_match = re.search(r"<tieu_chi_content>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</tieu_chi_content>", xml_clean, re.DOTALL | re.IGNORECASE)
        if rubric_match:
            demo_rubric = rubric_match.group(1).strip()

    if not demo_de_bai:
        demo_de_bai = f"""## <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp ({chosen_domain.upper()})</center>

### **1. Mục tiêu**
- **Kiến thức**: Tổng hợp toàn bộ kiến thức cốt lõi của {session_id} trong 1 bài toán thực tế thuộc hệ thống {chosen_domain.upper()}.
- **Kỹ năng**: Áp dụng các cấu trúc rẽ nhánh, vòng lặp và thao tác tập hợp dữ liệu động mức cơ bản.
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding demo trực tiếp trên lớp.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
Hệ thống {chosen_domain.upper()} yêu cầu triển khai một phân hệ tổng hợp tích hợp toàn bộ các quy tắc nghiệp vụ của bài học {session_title}.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**
#### **Chức năng 1: Khởi tạo và Thiết lập phân hệ**
- **Nghiệp vụ**: Thiết lập các giá trị ban đầu và tham số quét cho hệ thống.
- **Đầu vào (Input)**: Các tham số thiết lập từ bàn phím.
- **Đầu ra (Output)**: Thông điệp khởi tạo lô dữ liệu thành công.

#### **Chức năng 2: Xử lý lô dữ liệu và Rà soát điều kiện**
- **Nghiệp vụ**: Duyệt qua danh sách, kiểm tra điều kiện an toàn, lọc bỏ các bản ghi không hợp lệ hoặc kích hoạt lệnh dừng khẩn cấp.
- **Đầu vào (Input)**: Giá trị của các bản ghi dữ liệu.
- **Đầu ra (Output)**: Các thông điệp trạng thái xử lý cho từng bản ghi.

#### **Chức năng 3: Báo cáo kết quả**
- **Nghiệp vụ**: Tổng hợp kết quả, đếm số bản ghi hợp lệ và tính tổng các khoản tiền phát sinh nếu hoàn thành trọn vẹn.
- **Đầu vào (Input)**: Kết quả tích lũy từ tiến trình xử lý.
- **Đầu ra (Output)**: Bảng báo cáo kết quả an toàn hoặc cảnh báo niêm phong hệ thống.

### **4. Yêu cầu nộp bài**
Đẩy lên GitHub Repository: `[Tên Lớp]_[Môn Học]_{session_id.replace(' ', '')}_Demo`.
"""
    if not demo_rubric:
        demo_rubric = """### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sò đồ thuật toán — 20 điểm**
#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
"""

    from agents.creators.common_utils import clean_markdown_formulas
    processed_demo_de_bai = clean_markdown_formulas(generate_and_link_diagram(demo_de_bai, homework_dir, "bai_16_tong_hop_demo_giang_vien"))
    processed_demo_de_bai = sanitize_homework_markdown(processed_demo_de_bai, level_name="Tổng hợp Demo")

    demo_file_path = demo_synthesis_folder / "de_bai_bai_tap.md"
    with open(demo_file_path, "w", encoding="utf-8") as f:
        f.write(processed_demo_de_bai)
        
    direct_demo_path = homework_dir / "bai_tap_tong_hop.md"
    with open(direct_demo_path, "w", encoding="utf-8") as f:
        f.write(processed_demo_de_bai)

    demo_rubric_path = demo_synthesis_folder / "tieu_chi_cham_diem_ai.md"
    with open(demo_rubric_path, "w", encoding="utf-8") as f:
        f.write(demo_rubric)
        
    print(f"  [Success] Saved instructor demo synthesis homework folder: {demo_synthesis_folder}")

    # -------------------------------------------------------------------------
    # 2. Tự động sinh Bài tập Hệ thống hóa Mindmap (Cho Sinh viên)
    # -------------------------------------------------------------------------
    mindmap_folder = homework_dir / "17_tong_hop_he_thong_kien_thuc_mindmap"
    mindmap_folder.mkdir(exist_ok=True, parents=True)
    
    print(f"  [Homework Pipeline] Generating Student Mindmap Assignment for {session_id}...")
    mindmap_prompt = f"""Bạn là Chuyên gia Đào tạo Lập trình. Hãy tạo 1 Bài tập Tổng hợp Kiến thức (Mindmap & System Synthesis Assignment) hoàn chỉnh cho Buổi học: {session_id} - {session_title}.
Lĩnh vực áp dụng: {chosen_domain.upper()}
Phạm vi kiến thức buổi học: {previous_lessons_text}

Yêu cầu trả về đúng cấu trúc XML sau:
<exercise>
<de_bai_content>
## <center>[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) - Session {session_id}</center>

### **1. Mục tiêu**
- Hệ thống hóa toàn bộ kiến thức cốt lõi và các bẫy lỗi nghiệp vụ trong {session_id}.
- Trực quan hóa cấu trúc dữ liệu và luồng thực thi bằng Sơ đồ Tư duy (Mindmap).
- Rèn luyện kỹ năng phân tầng logic và kết nối tri thức hệ thống một cách khoa học.

### **2. Bối cảnh & Yêu cầu tổng hợp**
- Describe the student's role (Software Engineer) mapping out technical knowledge mindmap diagram for {session_title} to onboard new members in {chosen_domain.upper()} project.

### **3. Quy tắc nghiệp vụ & Từ khóa trọng tâm**
Sơ đồ tư duy BẮT BUỘC bao phủ các từ khóa trọng tâm của buổi học này:
{previous_lessons_text}

### **4. Yêu cầu bài toán (Sản phẩm nộp)**
1. File ảnh Sơ đồ tư duy (.png hoặc .jpg).
2. File thiết kế gốc (.xmind hoặc .pdf).
3. Bản tóm tắt tóm lược Markdown (summary.md) giải thích các nhánh liên kết chính trong sơ đồ.

### **5. Yêu cầu nộp bài**
Học viên nộp bài theo quy chuẩn GitHub:
* Đẩy mã nguồn và sơ đồ lên GitHub Repository theo cấu trúc: `[Tên Lớp]_[Môn Học]_{session_id.replace(' ', '')}_Mindmap`.
  Ví dụ: `HNKS25CNTT1_Core_{session_id.replace(' ', '')}_Mindmap`
</de_bai_content>
<tieu_chi_content>
### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
#### **2. Phân tầng logic & Mối liên kết — 30 điểm**
#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
#### **4. Bản tóm tắt giải trình (summary.md) — 10 điểm**
#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
</tieu_chi_content>
</exercise>
"""
    mindmap_response = call_llm(
        system_prompt="Bạn là Chuyên gia thiết kế bài tập Lập trình chuẩn hóa của Rikkei Education.",
        user_prompt=mindmap_prompt,
        json_mode=False,
        agent_name="Mindmap_Exercise_Agent",
        session_id=session_id
    )
    
    mindmap_de_bai = ""
    mindmap_rubric = ""
    if mindmap_response:
        xml_clean = mindmap_response.strip()
        if xml_clean.startswith("```xml"):
            xml_clean = xml_clean[6:]
        if xml_clean.startswith("```"):
            xml_clean = xml_clean[3:]
        if xml_clean.endswith("```"):
            xml_clean = xml_clean[:-3]
        xml_clean = xml_clean.strip()
        
        import re
        # Extract de_bai_content using robust regex
        de_bai_match = re.search(r"<de_bai_content>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</de_bai_content>", xml_clean, re.DOTALL | re.IGNORECASE)
        if de_bai_match:
            mindmap_de_bai = de_bai_match.group(1).strip()
            
        # Extract tieu_chi_content using robust regex
        rubric_match = re.search(r"<tieu_chi_content>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</tieu_chi_content>", xml_clean, re.DOTALL | re.IGNORECASE)
        if rubric_match:
            mindmap_rubric = rubric_match.group(1).strip()

    if not mindmap_de_bai:
        mindmap_de_bai = f"""## <center>[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) - {session_title}</center>

### **1. Mục tiêu**
* Hệ thống hóa toàn bộ kiến thức cốt lõi và các bẫy lỗi nghiệp vụ trong {session_id}.
* Trực quan hóa cấu trúc dữ liệu và luồng thực thi bằng Sơ đồ Tư duy.

### **2. Bối cảnh & Yêu cầu tổng hợp**
Học viên đóng vai trò Kỹ sư Lập trình chính, thực hiện xây dựng Sơ đồ Tư duy (Mindmap) tổng hợp kiến thức đã học.

Prompt tạo ảnh: A clean 2D flat vector technical illustration of a developer mapping out technical knowledge mindmap diagram for {session_title}. Minimalist infographics style, corporate Navy and Emerald palette.

### **3. Quy tắc nghiệp vụ & Từ khóa trọng tâm**
Sơ đồ tư duy BẮT BUỘC bao phủ các từ khóa: {previous_lessons_text}.

### **4. Yêu cầu bài toán (Sản phẩm nộp)**
1. File ảnh Sơ đồ tư duy (.png hoặc .jpg).
2. File thiết kế gốc (.xmind hoặc .pdf).
3. Bản tóm tắt tóm lược Markdown (summary.md).

### **5. Yêu cầu nộp bài**
Đẩy lên GitHub Repository theo chuẩn: `[Tên Lớp]_[Môn Học]_{session_id.replace(' ', '')}_Mindmap`.
"""
    if not mindmap_rubric:
        mindmap_rubric = """### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
#### **2. Phân tầng logic & Mối liên kết — 30 điểm**
#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
#### **4. Bản tóm tắt giải trình (summary.md) — 10 điểm**
#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
"""

    processed_mindmap_de_bai = clean_markdown_formulas(generate_and_link_diagram(mindmap_de_bai, homework_dir, "bai_17_tong_hop_mindmap"))
    processed_mindmap_de_bai = sanitize_homework_markdown(processed_mindmap_de_bai, level_name="Tổng hợp Mindmap")

    mindmap_file_path = mindmap_folder / "de_bai_bai_tap.md"
    with open(mindmap_file_path, "w", encoding="utf-8") as f:
        f.write(processed_mindmap_de_bai)
        
    direct_mindmap_path = homework_dir / "bai_tap_mindmap.md"
    with open(direct_mindmap_path, "w", encoding="utf-8") as f:
        f.write(processed_mindmap_de_bai)

    mindmap_rubric_path = mindmap_folder / "tieu_chi_cham_diem_ai.md"
    with open(mindmap_rubric_path, "w", encoding="utf-8") as f:
        f.write(mindmap_rubric)
        
    print(f"  [Success] Saved mindmap homework folder: {mindmap_folder}")

    # Compile all rubrics into tieu_chi_danh_gia.md
    all_rubrics = []
    for idx, ex in enumerate(exercises_data):
        clean_title = ex.get("title", f"Bài tập {idx+1}")
        all_rubrics.append(f"## {clean_title}\n\n" + ex.get("rubric", "") + "\n\n---\n")
    all_rubrics.append("## [Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session\n\n" + demo_rubric + "\n\n---\n")
    all_rubrics.append("## [Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap)\n\n" + mindmap_rubric + "\n\n---\n")
    with open(homework_dir / "tieu_chi_danh_gia.md", "w", encoding="utf-8") as f:
        f.write("\n".join(all_rubrics))
    
    print(f"  [Homework Pipeline] Successfully completed all 15 homework assignments + 1 Demo Synthesis + 1 Mindmap Synthesis for Session {session_id}!")
    return exercises_data

# Alias for backwards compatibility
generate_session_homework = session_homework_pipeline

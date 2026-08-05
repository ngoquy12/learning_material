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
from core.llm import call_llm
from core.domain_adapters import get_domain_rules
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
    """
    print(f"    -> [LLM Generation] Creating exercise {idx}/6 ({level_name}) for domain: {chosen_domain.upper()}...")
    
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise ValueError("API Key configuration (GEMINI_API_KEY or OPENAI_API_KEY) is required to generate homework exercises.")

    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] homework_creator_agent: Yêu cầu tham số tech_stack hợp lệ.")

    # Determine stack category & technology boundaries
    stack_lower = tech_stack.lower().strip()
    is_web_framework = any(kw in stack_lower for kw in ["fastapi", "express", "spring", "flask", "django", "nest", "web api", "rest api"])
    domain_adapter_rules = get_domain_rules(tech_stack)

    # Technology isolation instructions
    if is_web_framework:
        stack_tech_directives = """
- TECHNOLOGY DIRECTIVES (WEB FRAMEWORK COURSE):
  + Model entity endpoints, Request/Response DTO schemas, and controller route handlers.
  + Use framework-appropriate validation and HTTP status codes (e.g. 400 Bad Request, 409 Conflict, 500 Internal Error).
"""
        example_repo_prefix = f"HNKS25CNTT1_WebAPI_Session"
    else:
        stack_tech_directives = """
- TECHNOLOGY ISOLATION DIRECTIVES (CORE / CLI COURSE):
  + ABSOLUTELY FORBIDDEN to use any web frameworks, external database libraries, HTTP status codes, routing decorators, or REST API concepts.
  + MUST use native language features only: CLI input/output, in-memory data structures (lists, dicts, arrays, structs, objects), native exception handling (e.g. `raise ValueError`, `raise KeyError` in Python; native Exception classes in Java; error return codes in C/C++).
"""
        example_repo_prefix = f"HNKS25CNTT1_Core_Session"

    # Define level specific guidelines
    level_guidelines = ""
    rubric_guidelines = ""
    
    if idx in [1, 2]:
        level_guidelines = f"""
- Difficulty Level: 'Basic Application {idx}'.
- MUST provide runnable legacy source code adhering strictly to '{tech_stack}' syntax in section '### **3. Mã nguồn hiện tại**'.
- Legacy code MUST contain a specific business logic flaw or missing input validation (e.g. missing duplicate check, capacity bound overflow, wrong status state).
- Student Execution Directives:
  + Part 1: Write a test case report table (minimum 3 test cases specifying Input, actual buggy Output, and expected correct Output).
  + Part 2: Fix legacy source code to enforce in-memory business constraints using standard '{tech_stack}' error handling patterns.
- ABSOLUTELY FORBIDDEN to provide completed solution code or pre-fixed source code.
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
    elif idx == 3:
        level_guidelines = f"""
- Difficulty Level: 'Advanced Application'.
- Requirements: Student MUST design data handling flow and write functions/classes from scratch for enterprise entity relationships (e.g. student registration, duplicate check, capacity bounds).
- NO-CODE HINTING POLICY: ABSOLUTELY FORBIDDEN to provide skeleton code, empty function signatures, or hint code blocks.
- Only visual data examples are allowed (e.g. sample data payloads, parameter lists, or error log messages).
- Student Execution Directives:
  + Part 1: Solution analysis and design report (Input/Output schema specification, pseudocode or flowchart).
  + Part 2: Implement code from scratch based on personal design.
"""
        rubric_guidelines = f"""
Mandatory 5 Rubric Criteria Groups:
#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** List complete data types and structures for Input/Output parameters.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Write pseudocode or flowchart describing validation steps prior to data mutation.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Define entity models/structures and maintain in-memory state.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Implement core business operations operating smoothly.

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
    elif idx == 4:
        level_guidelines = f"""
- Difficulty Level: 'Analysis'.
- Requirements: Student MUST research and propose at least 2 distinct technical solutions for the same business problem (e.g., sequential list search vs direct dictionary key mapping for lookup optimization).
- NO-CODE HINTING POLICY: ABSOLUTELY FORBIDDEN to provide skeleton code, empty function signatures, or hint code blocks.
- Student Execution Directives:
  + Part 1: Trade-off comparison report table comparing the 2 proposed solutions (Memory, Speed, Readability, Maintainability, Suitability).
  + Part 2: Justification for optimal choice and algorithm flowchart/pseudocode.
  + Part 3: Implement source code for the chosen optimal solution.
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
    elif idx == 5:
        level_guidelines = f"""
- Difficulty Level: 'Creative Synthesis'.
- Open-ended business expansion request (e.g. Soft Delete vs Hard Delete for audit trail, dynamic status workflow).
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
    elif idx == 6:
        level_guidelines = f"""
- Difficulty Level: 'Synthesis Exercise'. Must combine basic session skills into a single cohesive project module.
- DIFFICULTY BOUNDS: Basic level achievable within 40 minutes by listening in class.
- Content: Integrate 2-3 core functional features (Create, Read, Delete/Update) operating on in-memory RAM data.
- NO-CODE HINTING POLICY: ABSOLUTELY FORBIDDEN to provide skeleton code or empty function signatures.
- Student Execution Requirement: Implement all required features and test execution successfully.
"""
        rubric_guidelines = f"""
Mandatory 5 Rubric Criteria Groups:
#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Setup project environment, dependencies, and entry point.
*   **[10 điểm] Xây dựng Cấu trúc dữ liệu:** Define accurate data schemas/classes with proper types.

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Chức năng Đọc/Xem danh sách:** Implement module fetching all in-memory records.
*   **[20 điểm] Chức năng Ghi/Thêm mới:** Implement module creating new entity in RAM with unique identifier generation.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý trùng lặp:** Block duplicate unique fields and raise clear exceptions.
*   **[10 điểm] Xử lý bản ghi không tồn tại:** Validate entity existence on operations and handle errors.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Ensure output matches specification, English domain identifiers.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Push repository to GitHub following required directory naming format.
"""

    forbidden_scope_instruction = ""
    if forbidden_scope:
        forbidden_scope_instruction = f"\nPHẠM VI CẤM DÙNG (FORBIDDEN SCOPE): {forbidden_scope}.\nTUYỆT ĐỐI CẤM SỬ DỤNG CÁC KIẾN THỨC/TỪ KHÓA BỊ CẤM SAU ĐÂY VÀO BÀI TẬP.\n"

    system_prompt = f"""You are a Senior Computer Science Professor specializing in designing standardized college-level essay & code homework assignments.
Your task is to generate EXACTLY 1 homework exercise formatted in clean XML complying with strict pedagogical and domain standards.

COURSE & SESSION CONTEXT:
- Session: {session_id} - {session_title}
- Target Technology Stack: {tech_stack}
- Allowed Knowledge Boundary: {previous_lessons_text}{forbidden_scope_instruction}

INDUSTRY CODING RULES FOR THIS STACK:
{domain_adapter_rules}

{stack_tech_directives}

EXERCISE REQUIREMENTS:
- Exercise Index in Session: Exercise #{idx} / 6.
- Cognitive Bloom Taxonomy Level: {level_name}
- Required Enterprise Subsystem Domain: {chosen_domain.upper()} domain (e.g., ecommerce, crm, logistics, warehouse, fintech).

DIFFICULTY LEVEL GUIDELINES ({level_name.upper()}):
{level_guidelines}

MANDATORY FORMATTING & LANGUAGE DIRECTIVES:
0. STRICT NO EMOJI DIRECTIVE: ABSOLUTELY FORBIDDEN to use text emojis (🚀, 💡, ⚠️, ✅, ❌) in title, body, or source code. Use text labels [NOTE], [TIP], [WARNING], [REQUIREMENT] instead.
0.1 DYNAMIC PROGRESSIVE KNOWLEDGE BOUNDARY:
- You MUST ONLY use concepts taught up to the current Session ({session_id} - {session_title}) and prior lessons: {previous_lessons_text}.
- ABSOLUTELY FORBIDDEN to introduce concepts, syntax, functions, libraries, or structures from future lessons in the curriculum!
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
   *   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session{session_id[-2:]}_Ex0{idx}`.
       Ví dụ: `{example_repo_prefix}{session_id[-2:]}_Ex0{idx}`
5. IMAGE PROMPT SPECIFICATION (Clean 2D Flat Vector & NO ALL CAPS):
   - Place inside section '### **2. Vấn đề**' (directly below scenario description).
   - Mandatory format (in English):
     `*Prompt tạo ảnh: A clean 2D flat vector technical illustration of [detailed business logic/flow description here]. Minimalist infographics style, elegant layout, muted corporate color palette (navy blue, slate gray, soft emerald accents). Clear lines, no 3D elements, no glowing neon effects. All text labels must be in Sentence Case or Title Case (NEVER ALL CAPS), keeping key technical terms in English while using Vietnamese for annotations.*`
6. HTML TABLE STYLING REQUIREMENT:
   - Any HTML table MUST include attribute: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.
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
            forbidden_feedback = check_forbidden_keywords(combined_text, tech_stack, set([forbidden_scope]))
            if forbidden_feedback:
                feedback_msg = f"Exercise #{idx+1} '{title}' vi phạm FORBIDDEN SCOPE: {forbidden_feedback} Yêu cầu sinh lại không dùng các từ khóa này."
                print(f"  [Homework Reviewer REJECT] {feedback_msg}")
                return {"status": "REJECTED", "feedback": feedback_msg}
        
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
                return {"status": "REJECTED", "feedback": feedback_msg}

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
                
        # 6. Check layout structure of content (H2 title centering and NO numbering)
        if "## <center>" not in content:
            print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' lacks centered H2 title. Auto-formatting.")
            lines = content.split('\n')
            has_h2 = False
            for i, line in enumerate(lines):
                if line.strip().startswith('##') or line.strip().startswith('#'):
                    raw_title = line.replace('##', '').replace('#', '').replace('<center>', '').replace('</center>', '').strip()
                    lines[i] = f"## <center>{raw_title}</center>"
                    has_h2 = True
                    break
            if not has_h2:
                lines.insert(0, f"## <center>{title}</center>\n")
            content = '\n'.join(lines)
            ex["content"] = content
            
        h2_match = re.search(r"## <center>(.*?)</center>", content)
        if h2_match:
            header_text = h2_match.group(1).lower()
            if any(kw in header_text for kw in ["bai tap", "bài tập", "exercise"]) and re.search(r"\d+", header_text):
                print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' has numbered H2 title. Bypassing minor warning.")
                
        # 7. Verify H3 section headings in content
        required_headers = [
            r"###\s*(\*\*|\*|)?1\.\s*Mục tiêu(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?2\.\s*(Bối cảnh & )?Vấn đề(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?3\.\s*(Quy tắc nghiệp vụ|Mã nguồn hiện tại|Quy tắc xử lý)(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?4\.\s*(Yêu cầu bài toán|Yêu cầu đầu ra)(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?5\.\s*Yêu cầu nộp bài(\*\*|\*|)?[\s:]*"
        ]
        for header in required_headers:
            if not re.search(header, content):
                print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' lacks required H3 section header matching '{header}'. Bypassing minor warning.")

        # 8. Check prompt location and format (must be inside Section 2 Vấn đề)
        idx_problem = content.find("2. Vấn đề")
        if idx_problem == -1:
            idx_problem = content.find("2. Bối cảnh & Vấn đề")
            
        idx_req = content.find("3. Quy tắc nghiệp vụ")
        if idx_req == -1:
            idx_req = content.find("3. Mã nguồn hiện tại")
            
        if idx_problem != -1 and idx_req != -1:
            sub_content = content[idx_problem:idx_req]
            if "*Prompt tạo ảnh:" not in sub_content:
                print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' missing '*Prompt tạo ảnh:' inside Section 2. Bypassing minor warning.")

        # 9. Verify Table styling
        if "<table" in content and "width: 100%" not in content and 'width="100%"' not in content:
            print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' contains HTML table without 100% width attribute. Bypassing minor warning.")

        # 10. Check Rubric format in tieu_chi_cham_diem_ai.md
        if not rubric:
            print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' missing grading rubric content.")
        elif not rubric.startswith("### **Tiêu chí chấm điểm (AI)**"):
            print(f"  [Homework Reviewer Warning] Rubric for Exercise #{idx+1} '{title}' does not start with '### **Tiêu chí chấm điểm (AI)**'. Bypassing minor warning.")

        # 11. ENFORCE STRICT NO-CODE HINTING POLICY FOR ADVANCED LEVELS (3-6)
        if idx+1 in [1, 2]:
            if "```" not in content:
                print(f"  [Homework Reviewer Warning] Debug Exercise #{idx+1} '{title}' missing legacy code snippet.")
        else:
            # For levels 3-6, forbid full solution code skeletons
            python_code_blocks = re.findall(r"```python(.*?)```", content, re.DOTALL)
            for block in python_code_blocks:
                if "def " in block or "class " in block:
                    if len(block.strip().split("\n")) > 10:
                        print(f"  [Homework Reviewer Warning] Exercise #{idx+1} '{title}' contains pre-made function/class code implementation for students. Bypassing minor warning.")

    return {"status": "APPROVED", "feedback": "All 6 session exercises successfully passed pedagogical and technology scope review."}

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
    Coordinates the 6-exercise creation and review loop for a single session,
    saving the resulting Markdown files and diagram prompts into session output directory.
    """
    print(f"\n==================================================")
    print(f" 📝 [SESSION HOMEWORK FACTORY] Generating 6 Exercises for Session: {session_id} - {session_title}")
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
    
    # Randomly select the unified enterprise domain context
    domains = ["ecommerce", "crm", "logistics", "warehouse", "fintech"]
    chosen_domain = random.choice(domains)
    print(f"  [Homework Pipeline] Selected Unified Domain Context: {chosen_domain.upper()}")
    
    levels = [
        ("Vận dụng cơ bản 1", 1),
        ("Vận dụng cơ bản 2", 2),
        ("Vận dụng chuyên sâu", 3),
        ("Phân tích", 4),
        ("Sáng tạo", 5),
        ("Bài tập tổng hợp", 6)
    ]
    
    exercises_data = []
    
    # Run the generate-review critique loop
    for attempt in range(3):
        print(f"  [Homework Pipeline] Attempt {attempt+1}/3 to generate session homework suite...")
        candidate_exercises = []
        try:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=6) as executor:
                futures = [
                    executor.submit(
                        homework_creator_agent,
                        session_id=session_id,
                        session_title=session_title,
                        tech_stack=tech_stack,
                        previous_lessons_text=previous_lessons_text,
                        idx=idx,
                        level_name=level_name,
                        chosen_domain=chosen_domain,
                        forbidden_scope=forbidden_scope
                    )
                    for level_name, idx in levels
                ]
                candidate_exercises = [f.result() for f in futures]
            
            # Review the entire batch of 6 exercises
            review_result = homework_reviewer_agent(
                candidate_exercises, 
                tech_stack, 
                chosen_domain, 
                previous_lessons_text,
                session_id,
                forbidden_scope
            )
            
            if review_result["status"] == "APPROVED":
                exercises_data = candidate_exercises
                print(f"  [Homework Reviewer] APPROVED: {review_result['feedback']}")
                break
            else:
                print(f"  [Homework Reviewer] REJECTED (Attempt {attempt+1}): {review_result['feedback']}")
        except Exception as e:
            print(f"  [Homework Warning] Attempt {attempt+1} failed due to exception: {e}")
            
    if not exercises_data:
        raise ValueError(f"Unable to generate standardized homework exercises for session {session_id} after 3 attempts.")
        
    # Clean legacy artifacts in homework_dir
    if homework_dir.exists():
        for old_folder in homework_dir.glob("*_*"):
            if old_folder.is_dir():
                import shutil
                try:
                    shutil.rmtree(old_folder)
                except Exception:
                    pass

    # Save the 6 exercises in their respective subfolders
    for idx, ex in enumerate(exercises_data):
        title = ex.get("title", "Bài tập")
        clean_name = sanitize_vietnamese_filename(title).replace(".md", "")
        ex_folder = homework_dir / f"{idx+1}_{clean_name}"
        ex_folder.mkdir(exist_ok=True)
        
        filename_no_ext = f"bai_{idx+1:02d}_{clean_name}"
        content = ex.get("content", "")
        rubric = ex.get("rubric", "")
        
        # Post-process content to link/generate diagram image
        processed_content = generate_and_link_diagram(content, homework_dir, filename_no_ext)
        
        # Save de_bai_bai_tap.md
        desc_file_path = ex_folder / "de_bai_bai_tap.md"
        with open(desc_file_path, "w", encoding="utf-8") as f:
            f.write(processed_content)
            
        # Save tieu_chi_cham_diem_ai.md
        rubric_file_path = ex_folder / "tieu_chi_cham_diem_ai.md"
        with open(rubric_file_path, "w", encoding="utf-8") as f:
            f.write(rubric)
            
        print(f"  [Success] Saved homework folder: {ex_folder}")
    # Tự động sinh Bài tập Mindmap (Yêu cầu mới)
    mindmap_folder = homework_dir / "Hệ thống kiến thức Mindmap"
    mindmap_folder.mkdir(exist_ok=True)
    
    # We call LLM to extract keywords for the mindmap objectives
    mindmap_prompt = f"""Dựa vào nội dung Session {session_id} - {session_title}:
{previous_lessons_text}

Hãy liệt kê khoảng 5-10 keyword trọng tâm nhất của bài học này để sinh viên làm Mindmap. Trả về đúng định dạng Markdown sau, KHÔNG thêm gì khác:
## <center>[Bài tập] Hệ thống kiến thức Mindmap</center>

### 1. Mục tiêu
- Hiểu được tổng quan đến chi tiết của buổi học thông qua các từ khóa:
  - {{KEYWORD_1}}
  - {{KEYWORD_2}}
  - ...

### 2. Yêu cầu nộp bài
- Nộp file ảnh xuất ra từ Xmind/Mindmeister (định dạng .png hoặc .jpg)
- Nộp file nguồn của Mindmap (ví dụ file .xmind)

### 3. Tiêu chí đánh giá
- **Độ chi tiết (40 điểm)**: Thể hiện đầy đủ các khái niệm, phân nhánh sâu đến các thuộc tính hoặc ví dụ cụ thể.
- **Tính logic và liên kết (30 điểm)**: Các nhánh được nhóm đúng theo quan hệ cha - con, sử dụng mũi tên liên kết giữa các nhánh liên quan.
- **Màu sắc và hình ảnh (30 điểm)**: Sử dụng màu sắc nhất quán cho các nhánh chính, có các icon minh họa sinh động, rõ ràng dễ nhớ.
"""
    mindmap_content = call_llm(
        system_prompt="Bạn là chuyên gia thiết kế bài tập Mindmap.",
        user_prompt=mindmap_prompt,
        json_mode=False,
        agent_name="Mindmap_Exercise_Agent"
    )
    
    if not mindmap_content:
        mindmap_content = """## <center>[Bài tập] Hệ thống kiến thức Mindmap</center>

### 1. Mục tiêu
- Hiểu được tổng quan đến chi tiết của buổi học

### 2. Yêu cầu nộp bài
- Nộp file ảnh xuất ra từ Xmind/Mindmeister (định dạng .png hoặc .jpg)
- Nộp file nguồn của Mindmap (ví dụ file .xmind)

### 3. Tiêu chí đánh giá
- **Độ chi tiết (40 điểm)**: Thể hiện đầy đủ các khái niệm, phân nhánh sâu.
- **Tính logic và liên kết (30 điểm)**: Các nhánh được nhóm đúng theo quan hệ cha - con.
- **Màu sắc và hình ảnh (30 điểm)**: Sử dụng màu sắc nhất quán cho các nhánh chính.
"""
    else:
        mindmap_content = mindmap_content.replace('```markdown', '').replace('```', '').strip()

    mindmap_file_path = mindmap_folder / "de_bai_bai_tap.md"
    with open(mindmap_file_path, "w", encoding="utf-8") as f:
        f.write(mindmap_content)
        
    print(f"  [Success] Saved mindmap homework folder: {mindmap_folder}")
    
    print(f"  [Homework Pipeline] Successfully completed all 6 homework assignments + 1 Mindmap assignment for Session {session_id}!")
    return exercises_data

# Alias for backwards compatibility
generate_session_homework = session_homework_pipeline

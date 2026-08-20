from pathlib import Path
# agents/practice_agents.py
import json
import re
import os
from typing import Dict, Any, List
from core.llm import call_llm
from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt


def _build_domain_prompt_block(session_id: str, session_title: str, chosen_domain: str) -> str:
    """Builds the UNIFIED SESSION BUSINESS DOMAIN CONTRACT block shared by all Practice-track prompts."""
    if not chosen_domain:
        return ""
    session_domain_data = get_domain_for_session(session_id, session_title, chosen_domain)
    domain_rules = format_domain_rules_for_prompt(session_domain_data)
    active_domain = session_domain_data.get("name_vi", chosen_domain)
    return f"""
=== UNIFIED SESSION BUSINESS DOMAIN CONTRACT ===
{domain_rules}
CRITICAL DOMAIN CONSISTENCY MANDATE:
- This Session has ONE unified business domain: {active_domain}. Each exercise's subsystem below
  is a different FUNCTIONAL ANGLE of this SAME domain — do NOT invent an unrelated business.
=================================================
"""

def sanitize_vietnamese_filename(text: str) -> str:
    # Chuyển sang chữ thường
    text = text.lower()
    # Loại bỏ dấu tiếng Việt
    text = re.sub(r'[áàảãạăắằẳẵặâấầẩẫậ]', 'a', text)
    text = re.sub(r'[éèẻẽẹêếềểễệ]', 'e', text)
    text = re.sub(r'[íìỉĩị]', 'i', text)
    text = re.sub(r'[óòỏõọôốồổỗộơớờởỡợ]', 'o', text)
    text = re.sub(r'[úùủũụưứừửữự]', 'u', text)
    text = re.sub(r'[ýỳỷỹỵ]', 'y', text)
    text = re.sub(r'đ', 'd', text)
    
    # Loại bỏ ký tự đặc biệt
    text = re.sub(r'[^a-z0-9\s_]', '', text)
    text = re.sub(r'\s+', '_', text)
    return text.strip('_') + ".md"

def clean_exercise_content(content: str) -> str:
    if not content:
        return ""
    from agents.creators.common_utils import normalize_markdown_headers
    content = normalize_markdown_headers(content)
    # 1. Remove bracket tags like [NOTE], [WARNING], [TIP], [REQUIREMENT], [ERROR], [INFO], [CAUTION]
    content = re.sub(r'\[(NOTE|WARNING|TIP|REQUIREMENT|ERROR|INFO|CAUTION)\]\s*', '', content, flags=re.IGNORECASE)
    # 2. Ensure all HTML <table> tags enforce 100% full width
    def fix_table_tag(match):
        tag = match.group(0)
        if 'style=' in tag:
            if 'width:' not in tag and 'width :' not in tag:
                tag = re.sub(r'style=["\']', 'style="width: 100%; ', tag, count=1)
        else:
            tag = tag.replace('<table', '<table style="width: 100%; border-collapse: collapse;"')
        return tag
    content = re.sub(r'<table[^>]*>', fix_table_tag, content, flags=re.IGNORECASE)
    return normalize_markdown_headers(content)

def is_cli_or_tooling_tech(tech_stack: str) -> bool:
    """Check if the tech stack is a CLI, Version Control, Container, Shell, OS, DevOps, Agile/Scrum, or System Architecture subject."""
    tech_lower = (tech_stack or "").lower().strip()
    tooling_keywords = [
        "git", "vcs", "github", "gitlab", "terminal", "bash", "shell", "cli", "cmd",
        "powershell", "docker", "kubernetes", "devops", "linux", "unix",
        "agile", "scrum", "diagram", "uml", "design", "system analysis",
        "software architecture", "kiến trúc", "process", "quy trình"
    ]
    return any(kw in tech_lower for kw in tooling_keywords)

def practice_creator_agent(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str,
    only_index: int | None = None,
    latest_theory_session: str = "",
    forbidden_scope: str = "",
    allowed_scope: str = "",
    chosen_domain: str = ""
) -> Dict[str, Any]:
    print(f"  [Practice Creator] Designing exercises for {session_id} - {session_title}...")
    
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise ValueError("Cần cấu hình API key (GEMINI_API_KEY hoặc OPENAI_API_KEY) để sinh nội dung bài tập thực hành. Chế độ offline fallback đã bị loại bỏ.")
        
    levels = [
        ("Dễ", "yếu/trung bình"),
        ("Trung bình", "trung bình"),
        ("Khá", "khá"),
        ("Giỏi", "giỏi"),
        ("Xuất sắc", "xuất sắc")
    ]
    
    domains = ["ecommerce", "crm", "logistics", "warehouse", "fintech"]
    exercises = []

    scope_rules = ""
    if forbidden_scope:
        scope_rules += f"\nPHẠM VI CẤM DÙNG (FORBIDDEN SCOPE): {forbidden_scope}.\nTUYỆT ĐỐI CẤM SỬ DỤNG CÁC KIẾN THỨC BỊ CẤM NÀY.\n"
    if allowed_scope:
        scope_rules += f"\nPHẠM VI ĐÃ HỌC (ALLOWED SCOPE): {allowed_scope}.\n"

    domain_prompt_block = _build_domain_prompt_block(session_id, session_title, chosen_domain)

    is_tooling = is_cli_or_tooling_tech(tech_stack)
    
    if is_tooling:
        subject_directive = f"""SUBJECT NATURE DIRECTIVE (CLI / TOOLING / PROCESS / ARCHITECTURE SUBJECT):
This course is a CLI / Tooling / Version Control / Process / Architecture subject ({tech_stack}), NOT a programming language class writing OOP application code.
- ABSOLUTELY FORBIDDEN to force students to write complex OOP programming code (e.g., Python classes, exception handling classes like ValueError/KeyError, API endpoints in Python/Java/JS) unless the lesson explicitly asks for simple automation scripts.
- The exercise MUST focus on: Real-world operational scenarios, CLI command workflows, Repository/Branch/Config setup, Git/CLI status verification, System State transitions, and Troubleshooting / Conflict resolution.
- Input & Output: Present 'Đầu vào (Input)' as initial system state / scenario context / CLI operations, and 'Đầu ra (Output)' as expected system state, CLI log/graph output, or repository status.
"""
        rubric_group_3 = "#### **3. Thao tác lệnh & Xử lý sự cố (30 điểm)**"
        example_title = "Thực hành Thao tác Quản lý Kho lưu trữ và Phân nhánh Dự án (Tên bài tập bằng tiếng Việt có dấu)"
    else:
        subject_directive = f"""SUBJECT NATURE DIRECTIVE (PROGRAMMING / CODING SUBJECT):
This course is a programming language / backend engineering subject ({tech_stack}).
- Focus on business logic, data validation, algorithms, error handling, and clean code principles.
- Input & Output: Strictly respect the current Session's knowledge boundary! ABSOLUTELY FORBIDDEN to use JSON, Dict, List, or complex objects if those data structures have NOT been taught yet in prior lessons. For early sessions (e.g. Session 01 to 07 before List/Dict topics), Input & Output MUST use standard primitive variables (int, float, str, bool) and formatted text console lines.
"""
        rubric_group_3 = "#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**"
        example_title = "Xây dựng Module Quản lý Đơn hàng Ecommerce (Tên bài tập bằng tiếng Việt có dấu)"
    
    for idx, (level_name, target_student) in enumerate(levels):
        if only_index is not None and (idx + 1) != only_index:
            continue
        domain = domains[idx % len(domains)]
        print(f"    -> Generating exercise {idx+1}/5 (Mức độ: {level_name})...")
        
        system_prompt = f"""You are a Senior Computer Science Professor designing practical hands-on IT lab exercises.
Your task is to generate EXACTLY 1 practical exercise for:
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}
Latest Preceding Theory Session: {latest_theory_session or session_title}
{domain_prompt_block}
{scope_rules}
REQUIRED DIFFICULTY LEVEL:
- Level: {level_name} (Targeted for {target_student} students)
- Domain Subsystem: {domain.upper()} Management Subsystem

{subject_directive}

MANDATORY EXERCISE DIRECTIVES:
0. STRICT NO EMOJI & NO BRACKET TAGS DIRECTIVE: ABSOLUTELY FORBIDDEN to use text emojis (🚀, 💡, ⚠️, ✅, ❌) OR bracket tags like [NOTE], [TIP], [WARNING], [REQUIREMENT], [ERROR] in titles, notes, body, or source code. For notes/warnings, use clean bold labels like '**Lưu ý:**', '**Ghi chú:**', or '**Cảnh báo:**'. For rules under 'Quy tắc xử lý', use 'Yêu cầu 1:', 'Yêu cầu 2:', etc. instead of bracket tags.
0.1 DYNAMIC PROGRESSIVE KNOWLEDGE BOUNDARY & PEDAGOGICAL WEIGHTING (70% NEW + 30% CUMULATIVE):
   - 70-80% CORE FOCUS (LATEST THEORY TOPIC):
     * The main problem statement, algorithms, and core requirements MUST focus directly and deeply on the immediately preceding Theory Session: {latest_theory_session or session_title}.
   - 20-30% CUMULATIVE INTEGRATION (PRIOR FOUNDATIONS):
     * Seamlessly integrate foundational concepts and tools from prior sessions ({previous_lessons_text}) to form realistic, cohesive business problems.
   - STRICT NO SCOPE LEAKAGE:
     * ABSOLUTELY FORBIDDEN to leak future unlearned topics, unlearned data structures (e.g., Dict/List/Set/Classes/Async before their respective dedicated sessions), or unlearned execution commands for any technology stack ({tech_stack}).
     * Strictly comply with Forbidden Scope ({forbidden_scope or 'None'}) listed above — this includes ALL future session/lesson topics not yet taught.

0.2 MERMAID DATA FLOW DIAGRAM:
   - In Section 2 (Problem Context), MUST include 1 highly detailed, correctly spelled Mermaid diagram (````mermaid ... ````) visualizing data flow (Inputs -> Process Logic -> Expected Output).
   - MANDATORY FLOWCHART SHAPE STANDARDS (STRICT FUNCTIONAL MATCHING):
     * Terminator (Start / End): Oval / Stadium shape `([Bắt đầu quy trình])` or `([Kết thúc: Dừng chương trình])`.
     * Input / Output: Parallelogram `[/Đầu vào: .../]` or `[/Đầu ra: .../]`.
     * Decision (Condition check): Diamond `{"Kiểm tra điều kiện?"}`.
     * Process (Action / Calculation): Rectangle `["Thực hiện tính toán / Xử lý dữ liệu"]`.
     * Flowline: Arrow `-->` or `-->|Đúng|` / `-->|Sai|`.
     * ABSOLUTELY FORBIDDEN to use Parallelogram `[/ /]` for actions or calculations! Use Rectangle `[" "]` for actions/calculations, and Parallelogram `[/ /]` ONLY for Input/Output.
   - ALWAYS double-quote node labels containing parens, slashes, or Vietnamese text: e.g., `A["Input: Data (v1)"] -->|Success| B["Process / Build"]`.
   - FORBIDDEN syntax: NEVER use `-- label -->` or `-- label -- >` with spaces before `>`. ALWAYS use `-->|label|`.
   - Diagram Labels: Technical identifiers (variables, functions, git commands) MUST remain in English (`git commit`, `git checkout`); Step labels MUST be in Vietnamese with correct spelling.
0.4 MANDATORY MATHEMATICAL & FINANCIAL FORMULA FORMATTING DIRECTIVE:
   - ABSOLUTELY FORBIDDEN to use LaTeX syntax (`\\frac`, `\\text`, `\\times`), double dollar signs (`$$...$$`), or single dollar signs (`$var_name$`) for math or financial formulas. Single dollars containing variable names with underscores (e.g. `$Total_Payable$`) collide with Markdown italic syntax (`_..._`) and cause broken rendering artifacts.
   - ALL mathematical, financial, or calculation formulas MUST be formatted as clean programming expressions wrapped in Markdown code badges (`code` / `` `code` ``):
     * GOOD: `- Lãi suất tháng (r): r = annual_rate / (100 * 12)`
     * GOOD: `- Số tiền trả hàng tháng (PMT): PMT = P * (r * (1 + r)^n) / ((1 + r)^n - 1)`
     * BAD: `- Lãi suất tháng ($r$): $$r = \\frac{{\\text{{annual_rate}}}}{{{{100 \\times 12}}}}$$`
0.5 MANDATORY 100% FULL-WIDTH HTML TABLE DIRECTIVE:
   - ALL HTML tables (e.g., parameter tables, command tables, input/output specifications) MUST be 100% full-width using '<table border="1" style="width: 100%; border-collapse: collapse;">' (or '<table class="w-full" style="width: 100%; border-collapse: collapse;">'). ABSOLUTELY FORBIDDEN to omit width 100% or use narrow tables.
0.3 EVALUATION RUBRIC TABLE (100 POINTS):
   - At the bottom of each exercise rubric, include '### **Tiêu chí chấm điểm (AI)**'.
   - You MUST EXACTLY use these 6 criteria headers (include the asterisks and numbering):
     #### **1. Thiết lập & Khởi tạo (10 điểm)**
     #### **2. Logic nghiệp vụ (30 điểm)**
     {rubric_group_3}
     #### **4. Tối ưu hoá hiệu suất (20 điểm)**
     #### **5. Chất lượng mã nguồn (10 điểm)**
     #### **Điểm cộng (5-10 điểm)**
1. BLOOM TAXONOMY DIFFICULTY ({level_name}):
   - Easy: Focus on basic syntax/commands and environment config. FORBIDDEN complex search/filter/sort/pagination.
   - Medium: Basic operations and simple inputs/workflows. FORBIDDEN complex search/filter/pagination.
   - Hard/Advanced: Real-world workflows, strict validation, specific edge case handling (e.g., merge conflicts, complex branching). Include concrete Input/Output examples.
2. SCOPE GUARANTEE: Based strictly on current context ({previous_lessons_text}). FORBIDDEN unlearned topics.
3. EXERCISE FORMATTING: Academic Markdown style. NO informal words (nhé, nha, nhé các bạn). NO AI assistant mentions (AI, ChatGPT, Copilot).
4. EXERCISE STRUCTURE & HEADINGS:
   - Centered H2 Title: `## <center>[Exercise Title]</center>` in ACCENTED VIETNAMESE. FORBIDDEN exercise numbers in H2 title.
   - Section Headings: `### **1. Mục tiêu**`, `### **2. Vấn đề**`, `### **3. Yêu cầu bài toán**`, `### **4. Quy tắc xử lý**`, `### **5. Yêu cầu nộp bài**`.
   - Function/Command Tables: Present complex commands or parameters in HTML `<table style="width: 100%; border-collapse: collapse;">` formatted according to `{tech_stack}` conventions.
   - Input/Output Examples: Show concrete Input and Output scenarios using markdown code fences. Filter inputs must match filtered outputs.
   - Submission Section: Standard GitHub submission format.

OUTPUT XML FORMAT CONTRACT:
Return ONLY a valid XML string wrapped in `<exercise>...</exercise>`:
- <title>: Exercise title in ACCENTED VIETNAMESE (No '&' symbol, replace with 'and' or 'và').
- <filename>: Lowercase filename without spaces.
- <content>: Markdown exercise body in CDATA (Sections 1 to 5).
- <rubric>: 100-point grading rubric in CDATA.

<exercise>
  <title>{example_title}</title>
  <filename>xay_dung_lab_thuc_hanh_chuyen_nghiep</filename>
  <content><![CDATA[
Markdown exercise body here...
  ]]></content>
  <rubric><![CDATA[
### **Tiêu chí chấm điểm (AI)**
**[Tên Bài Tập] — Tổng điểm: 100 điểm**
...
  ]]></rubric>
</exercise>
"""
        user_prompt = f"Generate practical hands-on IT lab exercise prompt and rubric XML for level {level_name} in session {session_id}."
        
        ex_data = None
        for attempt in range(3):
            response = None
            try:
                response = call_llm(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    json_mode=False,
                    agent_name=f"Practice Creator ({level_name})",
                    session_id=session_id
                )
                if not response:
                    continue
                
                # Parse single exercise XML
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
                    
                import xml.etree.ElementTree as ET
                root = ET.fromstring(xml_clean)
                title_node = root.find("title")
                filename_node = root.find("filename")
                content_node = root.find("content")
                rubric_node = root.find("rubric")
                
                title = title_node.text.strip() if title_node is not None and title_node.text else ""
                filename = filename_node.text.strip() if filename_node is not None and filename_node.text else ""
                content = content_node.text.strip() if content_node is not None and content_node.text else ""
                rubric = rubric_node.text.strip() if rubric_node is not None and rubric_node.text else ""
                
                if title and filename and content and rubric:
                    from agents.creators.reading_creator import guard_mermaid_syntax
                    content = guard_mermaid_syntax(content)
                    ex_data = {
                        "title": title,
                        "filename": filename,
                        "content": content,
                        "rubric": rubric
                    }
                    break
            except Exception as e:
                print(f"      [Warning] Attempt {attempt+1} failed to parse XML for level {level_name}: {e}")
                if response:
                    print(f"      [Debug] Response length: {len(response)} chars")
                    print(f"      [Debug] Response start:\n{response[:200]}")
                    print(f"      [Debug] Response end:\n{response[-200:]}")
                    
        if not ex_data:
            raise ValueError(f"Không thể sinh được bài tập mức độ {level_name} cho {session_id} sau 3 lần thử.")
            
        exercises.append(ex_data)
        
    return {"exercises": exercises}

def practice_reviewer_agent(exercises_json: Dict[str, Any], tech_stack: str) -> Dict[str, Any]:
    print("  [Practice Reviewer] Verifying practice exercises...")
    
    exercises = exercises_json.get("exercises", [])
    is_tooling = is_cli_or_tooling_tech(tech_stack)
    
    # 1. Check quantity must be exactly 5
    if len(exercises) != 5:
        return {"status": "REJECTED", "feedback": f"Số lượng bài tập là {len(exercises)}, không khớp yêu cầu bắt buộc là đúng 5 bài."}
        
    for idx, ex in enumerate(exercises):
        content = ex.get("content", "")
        rubric = ex.get("rubric", "")
        title = ex.get("title", "")
        
        combined_text = content + "\n" + rubric
        
        forbidden_words = ["nhé", "thân mến", "nhé các bạn", "nhe", "nha", "assistant", "chatgpt", "openai", "gemini", "llm", "copilot"]
        vn_boundary = r"(?<![a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđĐ])"
        vn_boundary_end = r"(?![a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđĐ])"
        for word in forbidden_words:
            pattern = rf"{vn_boundary}{re.escape(word)}{vn_boundary_end}"
            if re.search(pattern, combined_text, re.IGNORECASE):
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' chứa từ cấm suồng sã hoặc liên quan đến AI: '{word}'."}
                
        # Check case-sensitive "AI" (exempting "Tiêu chí chấm điểm (AI)" header in rubric)
        combined_text_for_ai_check = combined_text
        if "Tiêu chí chấm điểm (AI)" in combined_text_for_ai_check:
            combined_text_for_ai_check = combined_text_for_ai_check.replace("Tiêu chí chấm điểm (AI)", "")
        if "Tiêu chí chấm điểm (ai)" in combined_text_for_ai_check:
            combined_text_for_ai_check = combined_text_for_ai_check.replace("Tiêu chí chấm điểm (ai)", "")
        if re.search(r"\bAI\b", combined_text_for_ai_check):
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' chứa từ viết tắt 'AI'. Hãy tránh nhắc đến AI hoặc trợ lý ảo."}
                
        # 3. Check layout structure of content
        if "## <center>" not in content:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' không có tiêu đề H2 căn giữa sử dụng ## <center>."}
            
        # 4. Enforce NO numbering in H2 header
        h2_match = re.search(r"## <center>(.*?)</center>", content)
        if h2_match:
            header_text = h2_match.group(1).lower()
            if any(kw in header_text for kw in ["bai tap", "bài tập", "exercise"]) and re.search(r"\d+", header_text):
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' vi phạm quy định về tiêu đề: Không được đánh số thứ tự trong H2."}

        required_headers = [
            r"###\s*(\*\*|\*|)?1\.\s*Mục tiêu(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?2\.\s*Vấn đề(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?3\.\s*Yêu cầu bài toán(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?4\.\s*(Quy tắc xử lý|Quy tắc nghiệp vụ)(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?5\.\s*Yêu cầu nộp bài(\*\*|\*|)?[\s:]*"
        ]
        for header in required_headers:
            if not re.search(header, content):
                header_clean = header.replace('\\', '')
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' thiếu tiêu đề bắt buộc hoặc không đúng định dạng H3 bôi đậm: '{header_clean}'."}

        # Check rubric headers
        if not rubric:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' thiếu nội dung Tiêu chí chấm điểm (Rubric)."}
        if not re.search(r"### \*\*Tiêu chí chấm điểm \(AI\)\*\*", rubric, re.IGNORECASE):
            return {"status": "REJECTED", "feedback": f"Tiêu chí chấm điểm của Bài tập {idx+1} '{title}' phải bắt đầu bằng tiêu đề H3 bôi đậm '### **Tiêu chí chấm điểm (AI)**'."}

        rubric_required = [
            r"#### \*\*1\.\s+Thiết lập",
            r"#### \*\*2\.\s+Logic nghiệp vụ",
            r"#### \*\*3\.\s+(Kiểm chuẩn dữ liệu|Thao tác lệnh|Kiểm chuẩn quy trình|Xử lý sự cố)",
            r"#### \*\*4\.\s+",
            r"#### \*\*5\.\s+Chất lượng mã nguồn",
            r"#### \*\*Điểm cộng"
        ]
        for r_hdr in rubric_required:
            if not re.search(r_hdr, rubric, re.IGNORECASE):
                r_hdr_clean = r_hdr.replace('\\', '')
                return {"status": "REJECTED", "feedback": f"Tiêu chí chấm điểm Bài tập {idx+1} '{title}' thiếu nhóm tiêu chí bắt buộc: '{r_hdr_clean}'."}

        # 5. Check input/output details in Yêu cầu bài toán
        if not is_tooling:
            if "đầu vào" not in content.lower() or "đầu ra" not in content.lower():
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' vi phạm quy định Yêu cầu bài toán: Phải mô tả rõ Đầu vào (Input) và Đầu ra (Output) cho từng yêu cầu."}
        else:
            has_in = any(kw in content.lower() for kw in ["đầu vào", "kịch bản", "trạng thái ban đầu", "yêu cầu thao tác", "input"])
            has_out = any(kw in content.lower() for kw in ["đầu ra", "kết quả kỳ vọng", "trạng thái kết quả", "output"])
            if not (has_in and has_out):
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' vi phạm quy định Yêu cầu bài toán: Phải mô tả rõ Đầu vào / Kịch bản thao tác và Đầu ra / Kết quả kỳ vọng."}

        # 6. Check single requirement formatting: Cấm dùng "Yêu cầu 1:" nếu chỉ có 1 yêu cầu trong bài
        if "yêu cầu 1:" in content.lower() and "yêu cầu 2:" not in content.lower():
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' chỉ có 1 yêu cầu nhưng lại ghi nhãn 'Yêu cầu 1:'. Hãy bỏ nhãn đánh số này."}

        # 7. Check code format in output/input: JSON outputs should have fenced code block
        if not is_tooling and "đầu ra" in content.lower() and "{" in content and "```" not in content:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' mô tả cấu trúc JSON nhưng chưa định dạng trong block code."}

        # 8. Check that if there is a table, it has style width 100%
        if "<table" in content and "width: 100%" not in content and 'width="100%"' not in content:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' sử dụng bảng HTML nhưng chưa cấu hình chiều rộng 100% màn hình."}

        # 9. Verify logical consistency of mock parameters & JSON output values
        if not is_tooling and idx >= 2 and ("lọc" in content.lower() or "tìm kiếm" in content.lower() or "search" in content.lower()):
            has_example = any(kw in content.lower() for kw in ["ví dụ", "vi du", "query", "tham số", "parameter", "?", "url", "uri", "get /"])
            if not has_example:
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' lọc dữ liệu nhưng thiếu ví dụ truy vấn cụ thể ở phần Đầu vào để sinh viên dễ hình dung."}

        # 10. Check submission text format
        if "đưa mã nguồn lên github" not in content.lower() or "dán link của repository" not in content.lower():
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' vi phạm định dạng phần nộp bài. Phải dùng đúng mẫu yêu cầu nộp bài."}

        # 12. Enforce strict check to prevent discriminatory level labels or student categorization text
        forbidden_labels = ["dành cho sinh viên", "dành cho học viên", "mức độ:", "độ khó:", "yếu/trung bình", "học lực"]
        for fl in forbidden_labels:
            if fl in combined_text.lower():
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' chứa nhãn phân loại học lực hoặc mức độ '{fl}'. Hãy loại bỏ nhãn này để tránh gây sự phân biệt cho sinh viên."}

    return {"status": "APPROVED", "feedback": "Đề bài tập thực hành đạt tất cả tiêu chuẩn về sư phạm và cấu trúc mới."}

def parse_diagram_info(prompt_text: str, content: str = ""):
    endpoints = []
    storage = "In-Memory RAM"
    
    text_to_search = (prompt_text + " " + content)
    
    # Match patterns like GET /categories, POST /api/v1/bins, DELETE /api/v1/bins/{bin_code}
    matches = re.findall(r"\b(GET|POST|PUT|DELETE|PATCH)\s+([`*'_]*)(/[a-zA-Z0-9_{}/-]+)([`*'_]*)", text_to_search, re.IGNORECASE)
    seen = set()
    for method, prefix_quote, path, suffix_quote in matches:
        m_upper = method.upper()
        p_clean = path.strip().rstrip(".,()[]{}*`'")
        if (m_upper, p_clean) not in seen and len(p_clean) > 1:
            seen.add((m_upper, p_clean))
            endpoints.append((m_upper, p_clean))
            
    if not endpoints:
        table_matches = re.findall(r"\|\s*(GET|POST|PUT|DELETE|PATCH)\s*\|\s*([`*'_]*)(/[a-zA-Z0-9_{}/-]+)", text_to_search, re.IGNORECASE)
        for method, _, path in table_matches:
            m_upper = method.upper()
            p_clean = path.strip().rstrip(".,()[]{}*`'")
            if (m_upper, p_clean) not in seen and len(p_clean) > 1:
                seen.add((m_upper, p_clean))
                endpoints.append((m_upper, p_clean))

    if not endpoints:
        endpoints = [("GET", "/api/v1/resource"), ("POST", "/api/v1/resource")]
        
    if any(k in text_to_search.lower() for k in ["database", "db", "postgresql", "mysql", "sqlite", "csdl"]):
        storage = "Database (SQL)"
    elif any(k in text_to_search.lower() for k in ["ram", "in-memory", "list", "dict", "temporary", "bộ nhớ"]):
        storage = "In-Memory (RAM)"
        
    return endpoints[:4], storage

_IMAGE_GENERATION_DISABLED = False

def generate_and_link_diagram(content: str, practice_dir, filename_no_ext: str) -> str:
    global _IMAGE_GENERATION_DISABLED
    from pathlib import Path
    images_dir = Path(practice_dir) / "images"
    images_dir.mkdir(exist_ok=True)
    
    prompt_match = re.search(r"\*?\s*Prompt tạo ảnh:\s*(.*?)(?:\*|\n\n|\n(?=###)|$)", content, re.IGNORECASE | re.DOTALL)
    if not prompt_match:
        return content
        
    prompt_text = prompt_match.group(1).strip()
    image_name = f"{filename_no_ext}_diagram.png"
    image_path = images_dir / image_name
    
    # Circuit breaker: skip generating if previous calls timed out or failed
    if _IMAGE_GENERATION_DISABLED:
        new_content = re.sub(r"\*?\s*Prompt tạo ảnh:\s*(.*?)(?:\*|\n\n|\n(?=###)|$)", "", content, flags=re.IGNORECASE | re.DOTALL)
        return new_content
        
    # Extract title from content
    title_text = "API WORKFLOW DIAGRAM"
    title_match = re.search(r"##\s*<center>(.*?)</center>", content, re.IGNORECASE)
    if title_match:
        title_text = title_match.group(1).strip()
    else:
        title_match = re.search(r"###\s*.*?(?:Bài tập|Bài thực hành)\s*\d+:\s*(.*)", content, re.IGNORECASE)
        if title_match:
            title_text = title_match.group(1).strip()
        else:
            title_text = filename_no_ext.replace("bai_", "").replace("_", " ").title()
            
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not image_path.exists() and api_key:
        print(f"  [Image Generator] Generating 2D diagram for '{filename_no_ext}'...")
        import requests
        import base64
        import time
        base_url = os.getenv("GEMINI_BASE_URL")
        
        success = False
        last_error = None
        for attempt in range(1, 4):
            try:
                if base_url:
                    url = f"{base_url.rstrip('/')}/v1/images/generations"
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "prompt": prompt_text,
                        "n": 1,
                        "size": "1024x576"
                    }
                    # Lowered timeout to 10s for fast circuit breaker action
                    response = requests.post(url, headers=headers, json=data, timeout=10)
                    if response.status_code == 200:
                        resp_json = response.json()
                        img_data = resp_json.get("data", [])
                        if img_data and "b64_json" in img_data[0]:
                            img_b64 = img_data[0]["b64_json"]
                            with open(image_path, "wb") as f:
                                f.write(base64.b64decode(img_b64))
                            print(f"  [Image Generator] Successfully saved generated diagram to: {image_path}")
                            success = True
                            break
                        elif img_data and "url" in img_data[0]:
                            img_url = img_data[0]["url"]
                            img_resp = requests.get(img_url, timeout=15)
                            if img_resp.status_code == 200:
                                with open(image_path, "wb") as f:
                                    f.write(img_resp.content)
                                print(f"  [Image Generator] Successfully saved downloaded diagram to: {image_path}")
                                success = True
                                break
                            else:
                                raise RuntimeError(f"Failed to download generated image from URL: {img_url}")
                        else:
                            raise RuntimeError(f"API response did not contain image data: {resp_json}")
                    else:
                        raise RuntimeError(f"Image Generation API returned error status {response.status_code}: {response.text}")
                else:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
                    headers = {"Content-Type": "application/json"}
                    data = {
                        "instances": [{"prompt": prompt_text}],
                        "parameters": {
                            "sampleCount": 1,
                            "aspectRatio": "16:9",
                            "outputMimeType": "image/png"
                        }
                    }
                    # Lowered timeout to 10s for fast circuit breaker action
                    response = requests.post(url, headers=headers, json=data, timeout=10)
                    if response.status_code == 200:
                        resp_json = response.json()
                        if "predictions" in resp_json and len(resp_json["predictions"]) > 0:
                            img_b64 = resp_json["predictions"][0]["bytesBase64Encoded"]
                            with open(image_path, "wb") as f:
                                f.write(base64.b64decode(img_b64))
                            print(f"  [Image Generator] Successfully saved generated diagram to: {image_path}")
                            success = True
                            break
                        else:
                            raise RuntimeError(f"GenerativeAI API response did not contain predictions: {resp_json}")
                    else:
                        raise RuntimeError(f"GenerativeAI API returned error status {response.status_code}: {response.text}")
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                print(f"  [Image Generator Warning] Attempt {attempt}/3 failed for '{filename_no_ext}': {e}")
                
                # Check for network error/timeout to activate circuit breaker immediately
                if "timeout" in err_str or "connection" in err_str or "connect" in err_str or "read time out" in err_str or "unreachable" in err_str:
                    print("  [Image Generator Circuit Breaker] Connection error or timeout detected. Disabling image generation for this run to avoid hangs.")
                    _IMAGE_GENERATION_DISABLED = True
                    break
                    
                if attempt < 3:
                    time.sleep(1)
                    
        if not success:
            print(f"  [Image Generator Warning] Could not generate image via API for '{filename_no_ext}': {last_error}. Bypassing image file creation.")
            
    markdown_image_tag = ""
    if image_path.exists():
        markdown_image_tag = f"\n\n<p align=\"center\">\n  <img src=\"../images/{image_name}\" alt=\"Sơ đồ luồng nghiệp vụ\" width=\"80%\">\n</p>\n\n"
    
    new_content = re.sub(r"\*?\s*Prompt tạo ảnh:\s*(.*?)(?:\*|\n\n|\n(?=###)|$)", markdown_image_tag, content, flags=re.IGNORECASE | re.DOTALL)
    return new_content

def generate_practice_session_exercises(session_id: str, session_title: str, session_dir_path: str, tech_stack: str, previous_lessons_text: str, latest_theory_session: str = "", forbidden_scope: str = "", allowed_scope: str = "", chosen_domain: str = ""):
    import pathlib
    session_dir = pathlib.Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    practice_dir = session_dir / "Bài tập"
    practice_dir.mkdir(exist_ok=True)
    
    # Run the generate-review loop
    exercises_data = None
    last_candidate = None
    for attempt in range(3):
        candidate_exercises = practice_creator_agent(
            session_id=session_id,
            session_title=session_title,
            tech_stack=tech_stack,
            previous_lessons_text=previous_lessons_text,
            latest_theory_session=latest_theory_session,
            forbidden_scope=forbidden_scope,
            allowed_scope=allowed_scope,
            chosen_domain=chosen_domain
        )
        last_candidate = candidate_exercises
        review_result = practice_reviewer_agent(candidate_exercises, tech_stack)
        
        if review_result["status"] == "APPROVED":
            exercises_data = candidate_exercises
            print(f"  [Practice Reviewer] APPROVED: {review_result['feedback']}")
            break
        else:
            print(f"  [Practice Reviewer] REJECTED (Attempt {attempt+1}): {review_result['feedback']}")
            
    if not exercises_data:
        print(f"  [CẢNH BÁO TỪ PM] Không thể tạo được bộ bài tập thực hành đạt tiêu chuẩn 100% cho {session_id} sau nhiều lượt duyệt. BỎ QUA LỖI và dùng bản nháp cuối cùng (Pending Human Review).")
        exercises_data = last_candidate
        
    # Clean up all legacy exercise subfolders (e.g. 1_*, 2_*, etc.) and legacy files in practice_dir
    if practice_dir.exists():
        import shutil
        for item in practice_dir.glob("*"):
            if item.name == "images":
                continue
            if item.is_dir():
                try:
                    shutil.rmtree(item)
                except Exception as e:
                    print(f"  [Warning] Could not remove old practice folder {item}: {e}")
            elif item.is_file() and item.name.startswith("bai_"):
                try:
                    item.unlink()
                except Exception:
                    pass

    levels = ["Dễ", "Trung bình", "Khá", "Giỏi", "Xuất sắc"]
    # Save files in subfolders
    for idx, ex in enumerate(exercises_data["exercises"]):
        title = ex.get("title", "Bài tập")
        clean_name = sanitize_vietnamese_filename(title).replace(".md", "")
        # Folder name: {idx+1}_{clean_name}
        ex_folder = practice_dir / f"{idx+1}_{clean_name}"
        ex_folder.mkdir(exist_ok=True)
        
        filename_no_ext = f"bai_{idx+1:02d}_{clean_name}"
        content = ex.get("content", "")
        rubric = ex.get("rubric", "")
        
        # Post-process content to link/generate diagram image and sanitize math formulas, bracket tags & table width
        from agents.creators.common_utils import clean_markdown_formulas
        processed_content = clean_exercise_content(clean_markdown_formulas(generate_and_link_diagram(content, practice_dir, filename_no_ext)))
        
        # Write exercise description file
        desc_file_path = ex_folder / "de_bai_thuc_hanh.md"
        with open(desc_file_path, "w", encoding="utf-8") as f:
            f.write(processed_content)
            
        # Write grading criteria file
        rubric_file_path = ex_folder / "tieu_chi_cham_diem_ai.md"
        with open(rubric_file_path, "w", encoding="utf-8") as f:
            f.write(rubric)
            
        # Update keys for frontend compatibility
        ex["index"] = idx + 1
        ex["level"] = levels[idx] if idx < len(levels) else "Nâng cao"
        ex["folder_name"] = f"{idx+1}_{clean_name}"
        ex["content"] = processed_content
            
        print(f"  [Success] Saved practice assignment folder: {ex_folder}")
        
    return exercises_data

def regenerate_single_practice_exercise(session_id: str, session_title: str, session_dir_path: str, tech_stack: str, previous_lessons_text: str, exercise_index: int) -> Dict[str, Any]:
    import pathlib
    session_dir = pathlib.Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    practice_dir = session_dir / "Bài tập"
    practice_dir.mkdir(exist_ok=True)
    
    # Generate single exercise data using Creator and Reviewer loop
    ex_data = None
    for attempt in range(3):
        candidate_exercises = practice_creator_agent(session_id, session_title, tech_stack, previous_lessons_text, only_index=exercise_index)
        review_result = practice_reviewer_agent(candidate_exercises, tech_stack)
        
        if review_result["status"] == "APPROVED":
            ex_data = candidate_exercises["exercises"][0]
            print(f"  [Practice Reviewer] APPROVED: {review_result['feedback']}")
            break
        else:
            print(f"  [Practice Reviewer] REJECTED (Attempt {attempt+1}): {review_result['feedback']}")
            
    if not ex_data:
        raise ValueError(f"Không thể tạo lại bài tập thực hành số {exercise_index} đạt tiêu chuẩn.")
        
    levels = ["Dễ", "Trung bình", "Khá", "Giỏi", "Xuất sắc"]
    idx = exercise_index - 1
    
    title = ex_data.get("title", "Bài tập")
    clean_name = sanitize_vietnamese_filename(title).replace(".md", "")
    
    # Remove any existing folder for this specific exercise index (e.g. 1_*) to prevent stale duplicate folders
    for old_item in practice_dir.glob(f"{exercise_index}_*"):
        if old_item.is_dir():
            import shutil
            try:
                shutil.rmtree(old_item)
            except Exception:
                pass

    # Folder name: {idx+1}_{clean_name}
    ex_folder = practice_dir / f"{idx+1}_{clean_name}"
    ex_folder.mkdir(parents=True, exist_ok=True)
    
    filename_no_ext = f"bai_{idx+1:02d}_{clean_name}"
    content = ex_data.get("content", "")
    rubric = ex_data.get("rubric", "")
    
    from agents.creators.common_utils import clean_markdown_formulas
    processed_content = clean_exercise_content(clean_markdown_formulas(generate_and_link_diagram(content, practice_dir, filename_no_ext)))
    
    # Write exercise description file
    desc_file_path = ex_folder / "de_bai_thuc_hanh.md"
    with open(desc_file_path, "w", encoding="utf-8") as f:
        f.write(processed_content)
        
    # Write grading criteria file
    rubric_file_path = ex_folder / "tieu_chi_cham_diem_ai.md"
    with open(rubric_file_path, "w", encoding="utf-8") as f:
        f.write(rubric)
        
    # Update keys for frontend compatibility
    ex_data["index"] = exercise_index
    ex_data["level"] = levels[idx] if idx < len(levels) else "Nâng cao"
    ex_data["folder_name"] = f"{idx+1}_{clean_name}"
    ex_data["content"] = processed_content
    
    print(f"  [Success] Regenerated and saved single practice assignment: {ex_folder}")
    return ex_data

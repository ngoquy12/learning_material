# agents/project_agents.py
import json
import re
import os
from typing import Dict, Any, List
from pathlib import Path
from core.llm import call_llm
from core.course_architecture import (
    resolve_course_architecture,
    lint_document_architecture,
    ARCH_CLI_CORE
)

def sanitize_vietnamese_filename(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[áàảãạăắằẳẵặâấầẩẫậ]', 'a', text)
    text = re.sub(r'[éèẻẽẹêếềểễệ]', 'e', text)
    text = re.sub(r'[íìỉĩị]', 'i', text)
    text = re.sub(r'[óòỏõọôốồổỗộơớờởỡợ]', 'o', text)
    text = re.sub(r'[úùủũụưứừửữự]', 'u', text)
    text = re.sub(r'[ýỳỷỹỵ]', 'y', text)
    text = re.sub(r'đ', 'd', text)
    text = re.sub(r'[^a-z0-9\s_]', '', text)
    text = re.sub(r'\s+', '_', text)
    return text.strip('_') + ".md"

def parse_xml_robust(response: str, tags: List[str]) -> Dict[str, str]:
    res = {}
    for tag in tags:
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        
        val = ""
        if start_tag in response and end_tag in response:
            val = response.split(start_tag, 1)[1].split(end_tag, 1)[0].strip()
        else:
            match = re.search(rf"<{tag}>(.*?)</{tag}>", response, re.DOTALL | re.IGNORECASE)
            val = match.group(1).strip() if match else ""
            
        if val.startswith("<![CDATA["):
            val = val[9:]
            if val.endswith("]]>"):
                val = val[:-3]
            else:
                idx = val.rfind("]]>")
                if idx != -1:
                    val = val[:idx]
        res[tag] = val.strip()
    return res

def project_entry_test_creator(session_id: str, session_title: str, tech_stack: str, previous_lessons_text: str, test_idx: int, forbidden_scope: str = "", allowed_scope: str = "") -> Dict[str, Any]:
    print(f"    -> [Project Creator] Generating Dynamic Entry Test {test_idx+1}/4...")
    
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise ValueError("Cần cấu hình API key để sinh nội dung học liệu. Chế độ offline fallback đã bị loại bỏ.")
        
    arch_info = resolve_course_architecture(session_title, tech_stack, forbidden_scope, allowed_scope)
    
    domain_archetypes = [
        "Quản lý danh mục & Thực thể hệ thống (Resource & Entity Management)",
        "Xử lý giao dịch & Tính toán luồng nghiệp vụ (Transaction & Workflow Processing)",
        "Tìm kiếm nâng cao, Lọc dữ liệu & Thống kê (Search, Filtering & Analytics)",
        "Điều hướng quy trình & Quản lý trạng thái tác vụ (Task & State Navigation)"
    ]
    archetype = domain_archetypes[test_idx % len(domain_archetypes)]

    scope_rules = ""
    if forbidden_scope:
        scope_rules += f"\nPHẠM VI CẤM DÙNG (FORBIDDEN SCOPE): {forbidden_scope}.\nTUYỆT ĐỐI CẤM SỬ DỤNG CÁC KIẾN THỨC BỊ CẤM NÀY.\n"
    if allowed_scope:
        scope_rules += f"\nPHẠM VI ĐÃ HỌC (ALLOWED SCOPE): {allowed_scope}.\n"
    
    naming_convention = arch_info["naming_guidelines"]
    error_model = arch_info["error_model"]
    
    system_prompt = f"""You are a Senior Computer Science Professor and Technical Lead specializing in {tech_stack}.
Your task is to generate EXACTLY 1 concise Entry Test complying with:
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}
Architecture Model: {arch_info["arch_name"]}
Business Scenario Archetype #{test_idx+1}/4: {archetype}
Target Difficulty: Warm-up level (15-20 minutes completion time)
{scope_rules}

{naming_convention}

{error_model}

MANDATORY EXECUTION DIRECTIVES:
1. Scenario Diversity & 100% Subject Flexibility:
   - Create 1 independent real-world scenario matching business archetype '{archetype}', architecture '{arch_info["arch_name"]}', tech stack '{tech_stack}', and lesson topic '{session_title}'.
   - Test #{test_idx+1} scenario MUST be completely distinct from other entry tests in the same Session.
2. Concise Warm-up (15-20 Minutes):
   - Only request students to complete 2 to 3 core functions / components / operational steps. FORBIDDEN to request verbose system setups exceeding 20 minutes.
3. Strict Knowledge Scope Protection:
   - Only test previously taught knowledge: {previous_lessons_text or 'Prior lessons'}. Strictly comply with Forbidden Scope ({forbidden_scope or 'None'}).
4. Academic & Professional Tone:
   - FORBIDDEN informal words. NO AI assistant mentions. FORBIDDEN student capability labels.
5. 100% Full-Width HTML Specification Table:
   - Specify 2-3 functions/components in a 100% width HTML table:
   `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`
   Column 1: Function/Component Name (Bold Vietnamese Title + English Function Name inside `<code>`).
   Column 2: Input / Parameters (100% English variables).
   Column 3: Processing Logic & Rules.
   Column 4: Output / Expected Return Value.
6. Mandatory Exercise Structure:
   - Main Title: Centered tag `## <center>[Vietnamese Title] ([English Title])</center>`. FORBIDDEN exercise numbers in H2 title.
   - Required Bold H3 Sections:
     ### **1. Mục tiêu**
     ### **2. Yêu cầu** (Contains 100% width HTML specification table)
     ### **3. Tiêu chí đánh giá** (10-point rubric allocation)
     ### **4. Yêu cầu nộp bài** (Standard GitHub submission instructions)

MANDATORY OUTPUT FORMAT — SINGLE VALID XML BLOCK ENCLOSED IN <entry_test>...</entry_test>:
<entry_test>
  <title>Title of Entry Test in Accented Vietnamese</title>
  <filename>bai_kiem_tra_01_tieu_de</filename>
  <content><![CDATA[
Full Markdown content of the entry test here...
  ]]></content>
</entry_test>
"""
    user_prompt = f"Author entry test prompt #{test_idx+1} for {session_id} in technology stack {tech_stack}."
    
    test_data = None
    for attempt in range(3):
        response = None
        try:
            response = call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                json_mode=False,
                agent_name=f"Entry Test Creator {test_idx+1}",
                session_id=session_id
            )
            if not response:
                continue
            
            parsed = parse_xml_robust(response, ["title", "filename", "content"])
            title = parsed.get("title", "")
            filename = parsed.get("filename", "")
            content = parsed.get("content", "")
            
            if title and filename and content:
                test_data = {
                    "title": title,
                    "filename": filename,
                    "content": content
                }
                break
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to parse Entry Test {test_idx+1} XML: {e}")
            
    if not test_data:
        raise ValueError(f"Không thể tạo được đề kiểm tra {test_idx+1} cho session {session_id} sau 3 lần thử. Đã vô hiệu hóa fallback offline.")
    return test_data

def project_srs_creator(session_id: str, session_title: str, tech_stack: str, forbidden_scope: str = "", allowed_scope: str = "") -> Dict[str, Any]:
    print(f"    -> [Project Creator] Generating Dynamic SRS Document for '{session_title}' ({tech_stack})...")
    
    arch_info = resolve_course_architecture(session_title, tech_stack, forbidden_scope, allowed_scope)
    srs_headers_formatted = "\n   - ".join(arch_info["srs_headers"])
    
    scope_rules = ""
    if forbidden_scope:
        scope_rules += f"\nPHẠM VI CẤM DÙNG (FORBIDDEN SCOPE): {forbidden_scope}.\nTUYỆT ĐỐI CẤM SỬ DỤNG CÁC KIẾN THỨC/CÚ PHÁP/THƯ VIỆN BỊ CẤM NÀY.\n"
    if allowed_scope:
        scope_rules += f"\nPHẠM VI ĐÃ HỌC (ALLOWED SCOPE): {allowed_scope}.\nChỉ thiết kế yêu cầu dựa trên các kiến thức đã học tới session hiện tại.\n"

    naming_convention = arch_info["naming_guidelines"]
    error_model = arch_info["error_model"]

    system_prompt = f"""You are a Lead Solution Architect authoring Software Requirements Specification (SRS) documents for Enterprise Mini Projects.
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}
Designated Architecture Model: {arch_info["arch_name"]}
{scope_rules}

{naming_convention}

{error_model}

MANDATORY SPECIFICATION DIRECTIVES:
1. Strict Architecture Model Alignment: Requirements MUST align 100% with '{tech_stack}' and '{session_title}'. FORBIDDEN to introduce alien architecture concepts (e.g. if CLI model, forbid REST endpoints, HTTP status codes, Swagger UI, Controllers).
2. Professional Academic Tone: FORBIDDEN informal words, AI mentions, or academic tiering labels.
3. 100% Table Width: `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`
4. Minimalist 2D Vector Diagram Prompt: Include 1 image prompt inside '### **1. Tổng quan hệ thống**' or '### **2. Đặc tả chức năng**'.
   Format (ENGLISH): `*Prompt tạo ảnh: A clean 2D flat vector technical illustration of [detailed system data flow description]. Minimalist infographics style, elegant layout, muted corporate color palette (navy blue, slate gray, soft emerald accents). Clear lines, no 3D elements, no glowing neon effects. All text labels must be in Sentence Case or Title Case (NEVER ALL CAPS), keeping key technical terms in English while using Vietnamese for annotations.*`
5. NO FULL CODE: Describe business logic via narrative, math formulas, pseudocode, or sample JSON schemas.
6. Mandatory SRS Document Structure (7 H3 headers):
   - Document Title: '## <center>Tài liệu đặc tả Hệ thống [Tên nghiệp vụ] ([English Name])</center>' (centered).
   - {srs_headers_formatted}

MANDATORY OUTPUT FORMAT — SINGLE VALID XML BLOCK ENCLOSED IN <srs_doc>...</srs_doc>:
<srs_doc>
  <title>SRS Specification Title in Accented Vietnamese</title>
  <content><![CDATA[
Full Markdown SRS document content in Accented Vietnamese...
  ]]></content>
</srs_doc>
"""
    user_prompt = f"Author a comprehensive, concise SRS specification document for Mini Project in Session {session_id} ({session_title}) using technology stack {tech_stack}."
    
    srs_data = None
    for attempt in range(3):
        response = None
        try:
            response = call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                json_mode=False,
                agent_name="SRS Creator",
                session_id=session_id
            )
            if not response:
                continue
            
            parsed = parse_xml_robust(response, ["title", "content"])
            title = parsed.get("title", "")
            content = parsed.get("content", "")
            
            if title and content:
                srs_data = {
                    "title": title,
                    "content": content
                }
                break
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to parse SRS XML: {e}")
            
    if not srs_data:
        raise ValueError(f"Không thể sinh được tài liệu SRS cho session {session_id} sau 3 lần thử. Đã vô hiệu hóa fallback offline.")
    return srs_data

def project_mini_project_creator(session_id: str, session_title: str, tech_stack: str, srs_title: str, forbidden_scope: str = "", allowed_scope: str = "") -> Dict[str, Any]:
    print(f"    -> [Project Creator] Generating Dynamic Mini Project Prompt for '{session_title}'...")
    
    arch_info = resolve_course_architecture(session_title, tech_stack, forbidden_scope, allowed_scope)
    
    scope_rules = ""
    if forbidden_scope:
        scope_rules += f"\nPHẠM VI CẤM DÙNG (FORBIDDEN SCOPE): {forbidden_scope}.\nTUYỆT ĐỐI CẤM YÊU CẦU HOẶC ĐƯA VÀO CÁC KIẾN THỨC BỊ CẤM NÀY.\n"

    naming_convention = arch_info["naming_guidelines"]
    error_model = arch_info["error_model"]

    system_prompt = f"""You are a Senior Computer Science Instructor designing concise Enterprise Mini Project assignments for technology stack '{tech_stack}'.
Your task is to author a Mini Project assignment prompt for:
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}
Designated Architecture Model: {arch_info["arch_name"]}
SRS Context: {srs_title}
{scope_rules}

{naming_convention}

{error_model}

MANDATORY SPECIFICATION DIRECTIVES:
0. STRICT NO EMOJI DIRECTIVE: FORBIDDEN to use text emojis. Use labels [NOTE], [TIP], [WARNING], [REQUIREMENT] instead.
1. 100% Architecture Alignment: Assignment must strictly match technology stack '{tech_stack}' and '{session_title}'.
2. SRS Document Link: Must explicitly include link reference to SRS document:
   *Example: "Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md)."*
3. Professional Academic Tone: FORBIDDEN informal words, AI mentions, or tiering labels.
4. 100% Table Width: `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`
5. Mandatory Assignment Structure:
   - Assignment Title: '## <center>[Mini project] [Tên nghiệp vụ] ([English Name])</center>' (centered).
   - Must contain 3 bold H3 section headers:
     ### **1. Mục tiêu dự án**
     ### **2. Đề bài và Yêu cầu** (Tasks matching tech stack '{tech_stack}', strictly adhering to Forbidden Scope).
     ### **3. Yêu cầu nộp bài** (GitHub repository link format).

MANDATORY OUTPUT FORMAT — SINGLE VALID XML BLOCK ENCLOSED IN <mini_project>...</mini_project>:
- <title>: Concise project title in Accented Vietnamese.
- <content>: Markdown project prompt content wrapped in CDATA block.
- <rubric>: Detailed 100-point Markdown grading rubric wrapped in CDATA block following 5 criteria groups:
    #### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
    #### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
    #### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
    #### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
    #### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
    #### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**

<mini_project>
  <title>Mini Project Title in Accented Vietnamese</title>
  <content><![CDATA[
Markdown assignment content here...
  ]]></content>
  <rubric><![CDATA[
### **Tiêu chí chấm điểm (AI)**
**[Project Title] — Tổng điểm: 100 điểm**
...
  ]]></rubric>
</mini_project>
"""
    user_prompt = f"Author Mini Project prompt and grading rubric XML for Session {session_id} ({session_title}) in technology stack {tech_stack} based on SRS '{srs_title}'."
    
    project_data = None
    for attempt in range(3):
        response = None
        try:
            response = call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                json_mode=False,
                agent_name="Mini Project Creator",
                session_id=session_id
            )
            if not response:
                continue
            
            parsed = parse_xml_robust(response, ["title", "content", "rubric"])
            title = parsed.get("title", "")
            content = parsed.get("content", "")
            rubric = parsed.get("rubric", "")
            
            if title and content and rubric:
                project_data = {
                    "title": title,
                    "content": content,
                    "rubric": rubric
                }
                break
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to parse Mini Project XML: {e}")
            
    if not project_data:
        raise ValueError(f"Không thể sinh được đề bài Mini Project cho session {session_id} sau 3 lần thử. Đã vô hiệu hóa fallback offline.")
    return project_data

def project_reviewer_agent(entry_tests: List[Dict[str, Any]], srs_doc: Dict[str, Any], mini_project: Dict[str, Any], tech_stack: str, forbidden_scope: str = "") -> Dict[str, Any]:
    print("  [Project Reviewer] Verifying project templates and specs via Systemic Architecture Governance Engine...")
    
    if len(entry_tests) != 4:
        return {"status": "REJECTED", "feedback": f"Số lượng bài kiểm tra đầu giờ là {len(entry_tests)}, không đúng quy định bắt buộc phải là đúng 4 đề song song."}
        
    seen_entry_titles = set()
    for idx, test in enumerate(entry_tests):
        t_title = test.get("title", "").strip().lower()
        if t_title in seen_entry_titles:
            return {"status": "REJECTED", "feedback": f"Bài kiểm tra đầu giờ số {idx+1} bị trùng lặp tiêu đề '{test.get('title')}' với một đề kiểm tra khác."}
        seen_entry_titles.add(t_title)
        
    mp_content = mini_project.get("content", "")
    mp_rubric = mini_project.get("rubric", "")
    
    all_files = entry_tests + [
        srs_doc,
        {"title": "Mini Project Content", "content": mp_content},
        {"title": "Mini Project Rubric", "content": mp_rubric}
    ]
    
    forbidden_words = ["nhé", "thân mến", "nhé các bạn", "nhe", "nha", "assistant", "chatgpt", "openai", "gemini", "llm", "copilot"]
    discriminatory_labels = ["dành cho sinh viên", "dành cho học viên", "mức độ:", "độ khó:", "yếu/trung bình", "học lực"]
    
    for doc in all_files:
        content = doc.get("content", "")
        title = doc.get("title", "")
        
        for word in forbidden_words:
            pattern = rf"\b{word}\b"
            if re.search(pattern, content, re.IGNORECASE):
                return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa từ cấm suồng sã hoặc liên quan đến AI: '{word}'."}
                
        content_for_ai_check = content
        if "Tiêu chí chấm điểm (AI)" in content_for_ai_check:
            content_for_ai_check = content_for_ai_check.replace("Tiêu chí chấm điểm (AI)", "")
        if "Tiêu chí chấm điểm (ai)" in content_for_ai_check:
            content_for_ai_check = content_for_ai_check.replace("Tiêu chí chấm điểm (ai)", "")
        if re.search(r"\bAI\b", content_for_ai_check):
            return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa từ viết tắt 'AI'. Hãy tránh nhắc đến AI hoặc trợ lý ảo."}
                
        for fl in discriminatory_labels:
            if fl in content.lower():
                return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa nhãn phân loại học lực hoặc mức độ '{fl}'."}
                
        if "<table" in content and "width: 100%" not in content and 'width="100%"' not in content:
            return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' sử dụng bảng HTML nhưng chưa cấu hình chiều rộng 100% màn hình."}

    # 5. Systemic Architecture & Pedagogy Linter
    arch_info = resolve_course_architecture(srs_doc.get("title", ""), tech_stack, forbidden_scope)
    for doc in all_files:
        doc_title = doc.get("title", "")
        content = doc.get("content", "")
        violations = lint_document_architecture(doc_title, content, arch_info, forbidden_scope)
        if violations:
            return {"status": "REJECTED", "feedback": "; ".join(violations)}

    # Mini Project headers check
    mp_required = [
        r"### \*\*1\.\s+Mục tiêu dự án",
        r"### \*\*2\.\s+Đề bài và Yêu cầu",
        r"### \*\*3\.\s+Yêu cầu nộp bài"
    ]
    for r_hdr in mp_required:
        if not re.search(r_hdr, mp_content, re.IGNORECASE):
            r_hdr_clean = r_hdr.replace('\\', '')
            return {"status": "REJECTED", "feedback": f"Đề bài Mini Project thiếu tiêu đề bắt buộc hoặc không đúng định dạng H3 bôi đậm: '{r_hdr_clean}'."}

    if not mp_rubric:
        return {"status": "REJECTED", "feedback": "Mini Project thiếu nội dung Tiêu chí chấm điểm (Rubric)."}
    if not re.search(r"### \*\*Tiêu chí chấm điểm \(AI\)\*\*", mp_rubric, re.IGNORECASE):
        return {"status": "REJECTED", "feedback": "Tiêu chí chấm điểm của Mini Project phải bắt đầu bằng tiêu đề H3 bôi đậm '### **Tiêu chí chấm điểm (AI)**'."}
    
    rubric_required = [
        (r"1\..*?Thiết lập cấu trúc", "Nhóm 1: Thiết lập cấu trúc"),
        (r"2\..*?Logic nghiệp vụ", "Nhóm 2: Logic nghiệp vụ"),
        (r"3\..*?Kiểm chuẩn dữ liệu", "Nhóm 3: Kiểm chuẩn dữ liệu"),
        (r"4\..*?(Chức năng nâng cao|Kiểm thử|Kiểm chuẩn)", "Nhóm 4: Chức năng nâng cao hoặc Kiểm thử"),
        (r"5\..*?Chất lượng mã nguồn", "Nhóm 5: Chất lượng mã nguồn"),
        (r"(Điểm cộng|Bonus)", "Điểm cộng khuyến khích (Bonus)")
    ]
    for r_hdr, group_name in rubric_required:
        if not re.search(r_hdr, mp_rubric, re.IGNORECASE):
            return {"status": "REJECTED", "feedback": f"Tiêu chí chấm điểm Mini Project thiếu nhóm tiêu chí bắt buộc: {group_name}."}

    if "tai_lieu_dac_ta_yeu_cau_srs.md" not in mp_content:
        return {"status": "REJECTED", "feedback": "Đề bài Mini Project chưa chứa đường dẫn liên kết tham chiếu tương đối chính xác đến tài liệu đặc tả SRS."}

    if "*Prompt tạo ảnh:" not in srs_doc.get("content", "") and "<div class=\"mermaid" not in srs_doc.get("content", ""):
        return {"status": "REJECTED", "feedback": "Tài liệu đặc tả SRS không chứa '*Prompt tạo ảnh:' hoặc sơ đồ nghiệp vụ."}

    return {"status": "APPROVED", "feedback": "Bộ học liệu Mini Project đạt tất cả tiêu chuẩn chất lượng tinh gọn."}

def generate_and_link_srs_diagram(content: str, srs_dir, filename_no_ext: str, session_title: str = "", tech_stack: str = "", forbidden_scope: str = "") -> str:
    images_dir = Path(srs_dir) / "images"
    images_dir.mkdir(exist_ok=True)
    
    prompt_match = re.search(r"\*Prompt tạo ảnh:\s*(.*?)\*", content, re.IGNORECASE)
    prompt_text = prompt_match.group(1).strip() if prompt_match else f"Architecture and workflow diagram for {session_title}"
    image_name = f"{filename_no_ext}_diagram.png"
    image_path = images_dir / image_name
    
    title_text = "WORKFLOW DIAGRAM"
    title_match = re.search(r"##\s*<center>(.*?)</center>", content, re.IGNORECASE)
    if title_match:
        title_text = title_match.group(1).strip()
    else:
        title_text = filename_no_ext.replace("bai_", "").replace("_", " ").title()
        
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    image_generated = False
    
    if api_key and not image_path.exists():
        print(f"  [Image Generator] Generating business diagram using Imagen 3 AI...")
        try:
            import requests
            import base64
            base_url = os.getenv("GEMINI_BASE_URL")
            if base_url:
                base_host = base_url.rstrip('/')
                url = f"{base_host}/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
            else:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "instances": [{"prompt": prompt_text}],
                "parameters": {"sampleCount": 1, "aspectRatio": "16:9", "outputMimeType": "image/png"}
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                resp_json = response.json()
                if "predictions" in resp_json and len(resp_json["predictions"]) > 0:
                    img_b64 = resp_json["predictions"][0]["bytesBase64Encoded"]
                    with open(image_path, "wb") as f:
                        f.write(base64.b64decode(img_b64))
                    print(f"  [Image Generator] Successfully generated & saved Imagen 3 diagram to: {image_path}")
                    image_generated = True
        except Exception as e:
            print(f"  [Image Generator Warning] Imagen 3 image API call skipped/unavailable ({e}). Switching to AI Mermaid Diagram generation...")
            
    if image_generated and image_path.exists():
        markdown_image_tag = f"\n\n<p align=\"center\">\n  <img src=\"./images/{image_name}\" alt=\"Sơ đồ nghiệp vụ\" width=\"80%\">\n</p>\n\n"
        new_content = re.sub(r"\*Prompt tạo ảnh:\s*.*?\*", lambda m: markdown_image_tag, content, flags=re.IGNORECASE)
    else:
        # 100% AI GENERATED MERMAID DIAGRAM (Zero local fallback code!)
        print(f"  [AI Diagram Agent] Generating 100% AI Mermaid Architecture Diagram for '{title_text}'...")
        
        scope_warning = ""
        if forbidden_scope:
            scope_warning = f"FORBIDDEN IN DIAGRAM: {forbidden_scope}. ABSOLUTELY FORBIDDEN to draw File I/O, JSON/CSV files, or external Database nodes if forbidden!"
            
        ai_diagram_prompt = f"""You are a Lead AI Diagram Architect. Author EXACTLY ONE monolithic Mermaid flowchart (flowchart TD) reflecting business workflow and data lifecycle:
Title: {title_text}
Topic: {session_title}
Technology Stack: {tech_stack}
Context: {prompt_text}
{scope_warning}

MANDATORY MERMAID SYNTAX RULES TO PREVENT PARSE ERRORS:
1. Enclose ALL Node text labels in double quotes `""`.
   - CORRECT: `Start(["Khởi động ứng dụng Console"]):::startEnd`
   - INCORRECT: `Start([Khởi động ứng dụng Console]) :::startEnd`
2. FORBIDDEN spaces before `:::` when assigning class styles:
   - CORRECT: `NodeA["Nhãn văn bản"]:::className`
   - INCORRECT: `NodeA["Nhãn văn bản"] :::className`
3. If forbidden scope includes File I/O or Database, strictly restrict state to in-memory RAM storage (`In-memory RAM Storage`).

Return ONLY the HTML wrapper container with raw Mermaid code inside:
<div class="mermaid-diagram-container" style="background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin: 20px 0; overflow-x: auto;">
  <div class="mermaid" style="display: flex; justify-content: center; color: #f8fafc;">
flowchart TD
  ...
</div>
</div>
Return only the HTML wrapper with Mermaid code inside. Do not wrap in markdown code blocks.
"""
        ai_mermaid_code = call_llm(
            system_prompt="You are a Senior AI Business Flow Diagram Architect specializing in valid syntax Mermaid JS.",
            user_prompt=ai_diagram_prompt,
            json_mode=False,
            agent_name="AI Diagram Generator"
        )
        if ai_mermaid_code:
            ai_mermaid_code = ai_mermaid_code.strip().lstrip("```html").lstrip("```xml").lstrip("```mermaid").lstrip("```").rstrip("```").strip()
        else:
            raise ValueError(f"AI Diagram Generator failed to generate Mermaid diagram for session {session_title}. Offline fallbacks are completely disabled.")
        
        new_content = re.sub(r"\*Prompt tạo ảnh:\s*.*?\*", lambda m: ai_mermaid_code, content, flags=re.IGNORECASE)
        
    return new_content

def generate_mini_project_session(session_id: str, session_title: str, session_dir_path: str, tech_stack: str, previous_lessons_text: str, session_info: Dict[str, Any] = None):
    session_dir = Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    test_dir = session_dir / "Bài kiểm tra đầu giờ"
    srs_dir = session_dir / "Tài liệu đặc tả SRS"
    mp_dir = session_dir / "Mini project"
    
    test_dir.mkdir(exist_ok=True)
    srs_dir.mkdir(exist_ok=True)
    mp_dir.mkdir(exist_ok=True)
    
    forbidden_scope = session_info.get("forbidden_scope", "") if session_info else ""
    allowed_scope = session_info.get("allowed_scope", "") if session_info else ""
    
    # Generation & review loop
    final_entry_tests = []
    final_srs_doc = None
    final_mini_project = None
    
    for attempt in range(3):
        # 1. Generate 4 Entry Tests sequentially
        entry_tests = []
        for idx in range(4):
            test = project_entry_test_creator(session_id, session_title, tech_stack, previous_lessons_text, idx, forbidden_scope, allowed_scope)
            entry_tests.append(test)
            
        # 2. Generate SRS
        srs_doc = project_srs_creator(session_id, session_title, tech_stack, forbidden_scope, allowed_scope)
        
        # 3. Generate Mini Project
        mini_project = project_mini_project_creator(session_id, session_title, tech_stack, srs_doc["title"], forbidden_scope, allowed_scope)
        
        # 4. Review
        review_result = project_reviewer_agent(entry_tests, srs_doc, mini_project, tech_stack, forbidden_scope)
        if review_result["status"] == "APPROVED":
            final_entry_tests = entry_tests
            final_srs_doc = srs_doc
            final_mini_project = mini_project
            print(f"  [Project Reviewer] APPROVED: {review_result['feedback']}")
            break
        else:
            print(f"  [Project Reviewer] REJECTED (Attempt {attempt+1}): {review_result['feedback']}")
            
    if not (final_entry_tests and final_srs_doc and final_mini_project):
        raise ValueError(f"Không thể sinh được bộ học liệu Mini Project đạt tiêu chuẩn cho session {session_id} sau nhiều lượt tạo/đánh giá.")
        
    # Save files
    if test_dir.exists():
        for old_file in test_dir.glob("bai_kiem_tra_*"):
            try:
                old_file.unlink()
            except Exception:
                pass
                
    for idx, test in enumerate(final_entry_tests):
        clean_name = sanitize_vietnamese_filename(test["title"])
        filename = f"bai_kiem_tra_{idx+1:02d}_{clean_name}"
        file_path = test_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test["content"])
        print(f"  [Success] Saved Entry Test: {file_path}")
        
    # SRS doc
    srs_filename = "tai_lieu_dac_ta_yeu_cau_srs.md"
    srs_file_path = srs_dir / srs_filename
    processed_srs_content = generate_and_link_srs_diagram(final_srs_doc["content"], srs_dir, "so_do_dac_ta_nghiep_vu", session_title, tech_stack, forbidden_scope)
    with open(srs_file_path, "w", encoding="utf-8") as f:
        f.write(processed_srs_content)
    print(f"  [Success] Saved SRS Document: {srs_file_path}")
    
    # Mini Project
    mp_filename = "de_bai_mini_project.md"
    mp_file_path = mp_dir / mp_filename
    with open(mp_file_path, "w", encoding="utf-8") as f:
        f.write(final_mini_project["content"])
        
    rubric_filename = "tieu_chi_cham_diem_ai.md"
    rubric_file_path = mp_dir / rubric_filename
    with open(rubric_file_path, "w", encoding="utf-8") as f:
        f.write(final_mini_project["rubric"])
        
    print(f"  [Success] Saved Mini Project prompt and rubric to: {mp_dir}")
    
    return {
        "entry_tests": final_entry_tests,
        "srs": final_srs_doc,
        "mini_project": final_mini_project
    }

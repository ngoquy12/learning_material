from pathlib import Path
# agents/practice_agents.py
import json
import re
import os
from typing import Dict, Any, List
from core.llm import call_llm

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

def practice_creator_agent(session_id: str, session_title: str, tech_stack: str, previous_lessons_text: str, only_index: int | None = None) -> Dict[str, Any]:
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
    
    for idx, (level_name, target_student) in enumerate(levels):
        if only_index is not None and (idx + 1) != only_index:
            continue
        domain = domains[idx % len(domains)]
        print(f"    -> Generating exercise {idx+1}/5 (Mức độ: {level_name})...")
        
        system_prompt = f"""You are a Senior Computer Science Professor designing practical hands-on IT lab exercises.
Your task is to generate EXACTLY 1 practical exercise for:
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}

REQUIRED DIFFICULTY LEVEL:
- Level: {level_name} (Targeted for {target_student} students)
- Domain Subsystem: {domain.upper()} Management Subsystem

MANDATORY EXERCISE DIRECTIVES:
0. STRICT NO EMOJI DIRECTIVE: ABSOLUTELY FORBIDDEN to use text emojis (🚀, 💡, ⚠️, ✅, ❌) in title, body, or source code. Use text labels [NOTE], [TIP], [WARNING] instead. For rules under 'Quy tắc xử lý', use 'Yêu cầu 1:', 'Yêu cầu 2:', etc. instead of [REQUIREMENT 1].
0.1 DYNAMIC PROGRESSIVE KNOWLEDGE BOUNDARY:
   - You MUST ONLY use concepts taught up to the current Session ({session_id} - {session_title}) and prior lessons. FORBIDDEN to use future topics.
0.2 MERMAID DATA FLOW DIAGRAM:
   - In Section 2 (Problem Context), MUST include 1 highly detailed, correctly spelled Mermaid diagram (````mermaid ... ````) visualizing data flow (Inputs -> Process Logic -> Expected Output).
   - Use standard flowchart shapes correctly: `[]` (rectangle) for process/action, `{{}}` (diamond) for condition/decision, `[/ /]` (parallelogram) for Input/Output.
   - Diagram Labels: Technical identifiers (variables, functions) MUST remain in English (`user_id`, `calculate()`); Step labels MUST be in Vietnamese with correct spelling.
0.3 EVALUATION RUBRIC TABLE (100 POINTS):
   - At the bottom of each exercise rubric, include '### **Tiêu chí chấm điểm (AI)**'.
   - You MUST EXACTLY use these 6 criteria headers (include the asterisks and numbering):
     #### **1. Thiết lập & Khởi tạo (10 điểm)**
     #### **2. Logic nghiệp vụ (30 điểm)**
     #### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
     #### **4. Tối ưu hoá hiệu suất (20 điểm)**
     #### **5. Chất lượng mã nguồn (10 điểm)**
     #### **Điểm cộng (5-10 điểm)**
1. BLOOM TAXONOMY DIFFICULTY ({level_name}):
   - Easy: Focus on basic syntax and environment config. FORBIDDEN search/filter/sort/pagination.
   - Medium: Basic functions and simple inputs. FORBIDDEN complex search/filter/pagination.
   - Hard/Advanced: Real-world workflows, strict validation, specific edge case handling. Include concrete Input/Output examples.
2. SCOPE GUARANTEE: Based strictly on current context ({previous_lessons_text}). FORBIDDEN unlearned topics.
3. EXERCISE FORMATTING: Academic Markdown style. NO informal words (nhé, nha, nhé các bạn). NO AI assistant mentions (AI, ChatGPT, Copilot).
4. EXERCISE STRUCTURE & HEADINGS:
   - Centered H2 Title: `## <center>[Exercise Title]</center>` in ACCENTED VIETNAMESE. FORBIDDEN exercise numbers in H2 title.
   - Section Headings: `### **1. Mục tiêu**`, `### **2. Vấn đề**`, `### **3. Yêu cầu bài toán**`, `### **4. Quy tắc xử lý**`, `### **5. Yêu cầu nộp bài**`.
   - Function/API Tables: Present complex APIs in HTML `<table>` (width 100%) formatted according to `{tech_stack}` conventions.
   - Input/Output Examples: Show concrete Input and Output data structures (JSON, XML) using markdown code fences. Filter inputs must match filtered outputs.
   - Submission Section: Standard GitHub submission format.

OUTPUT XML FORMAT CONTRACT:
Return ONLY a valid XML string wrapped in `<exercise>...</exercise>`:
- <title>: Exercise title in ACCENTED VIETNAMESE (No '&' symbol, replace with 'and' or 'và').
- <filename>: Lowercase filename without spaces.
- <content>: Markdown exercise body in CDATA (Sections 1 to 5).
- <rubric>: 100-point grading rubric in CDATA.

<exercise>
  <title>Xây dựng API Quản lý Đơn hàng Ecommerce (Tên bài tập bằng tiếng Việt có dấu)</title>
  <filename>xay_dung_api_quan_ly_san_pham</filename>
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
    
    # 1. Check quantity must be exactly 5
    if len(exercises) != 5:
        return {"status": "REJECTED", "feedback": f"Số lượng bài tập là {len(exercises)}, không khớp yêu cầu bắt buộc là đúng 5 bài."}
        
    for idx, ex in enumerate(exercises):
        content = ex.get("content", "")
        rubric = ex.get("rubric", "")
        title = ex.get("title", "")
        
        combined_text = content + "\n" + rubric
        
        # 2. Check forbidden words in content and rubric
        forbidden_words = ["nhé", "thân mến", "nhé các bạn", "nhe", "nha", "assistant", "chatgpt", "openai", "gemini", "llm", "copilot"]
        for word in forbidden_words:
            pattern = rf"\b{word}\b"
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
            r"#### \*\*3\.\s+Kiểm chuẩn dữ liệu",
            r"#### \*\*4\.\s+",
            r"#### \*\*5\.\s+Chất lượng mã nguồn",
            r"#### \*\*Điểm cộng"
        ]
        for r_hdr in rubric_required:
            if not re.search(r_hdr, rubric, re.IGNORECASE):
                r_hdr_clean = r_hdr.replace('\\', '')
                return {"status": "REJECTED", "feedback": f"Tiêu chí chấm điểm Bài tập {idx+1} '{title}' thiếu nhóm tiêu chí bắt buộc: '{r_hdr_clean}'."}

        # 5. Check input/output details in Yêu cầu bài toán
        if "đầu vào" not in content.lower() or "đầu ra" not in content.lower():
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' vi phạm quy định Yêu cầu bài toán: Phải mô tả rõ Đầu vào (Input) và Đầu ra (Output) cho từng yêu cầu."}

        # 6. Check single requirement formatting: Cấm dùng "Yêu cầu 1:" nếu chỉ có 1 yêu cầu trong bài
        if "yêu cầu 1:" in content.lower() and "yêu cầu 2:" not in content.lower():
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' chỉ có 1 yêu cầu nhưng lại ghi nhãn 'Yêu cầu 1:'. Hãy bỏ nhãn đánh số này."}

        # 7. Check code format in output/input: JSON outputs should have fenced code block
        if "đầu ra" in content.lower() and "{" in content and "```" not in content:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' mô tả cấu trúc JSON nhưng chưa định dạng trong block code."}

        # 8. Check that if there is a table, it has style width 100%
        if "<table" in content and "width: 100%" not in content and 'width="100%"' not in content:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' sử dụng bảng HTML nhưng chưa cấu hình chiều rộng 100% màn hình."}

        # 9. Verify logical consistency of mock parameters & JSON output values
        if idx >= 2 and ("lọc" in content.lower() or "tìm kiếm" in content.lower() or "search" in content.lower()):
            has_example = any(kw in content.lower() for kw in ["ví dụ", "vi du", "query", "tham số", "parameter", "?", "url", "uri", "get /"])
            if not has_example:
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' lọc dữ liệu nhưng thiếu ví dụ truy vấn cụ thể ở phần Đầu vào để sinh viên dễ hình dung."}

        # 10. Check submission text format
        if "đưa mã nguồn lên github" not in content.lower() or "dán link của repository" not in content.lower():
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' vi phạm định dạng phần nộp bài. Phải dùng đúng mẫu yêu cầu nộp bài."}

        # 11. (Removed Image Prompt check)

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

def draw_fallback_diagram(prompt_text: str, content: str, title_text: str, image_path):
    print("  [Image Generator Info] AI Image generation skipped due to API quota. Proceeding without optional diagram.")
    return

def generate_and_link_diagram(content: str, practice_dir, filename_no_ext: str) -> str:
    from pathlib import Path
    images_dir = Path(practice_dir) / "images"
    images_dir.mkdir(exist_ok=True)
    
    prompt_match = re.search(r"\*Prompt tạo ảnh:\s*(.*?)\*", content, re.IGNORECASE)
    if not prompt_match:
        return content
        
    prompt_text = prompt_match.group(1).strip()
    image_name = f"{filename_no_ext}_diagram.png"
    image_path = images_dir / image_name
    
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
    if api_key and not image_path.exists():
        print(f"  [Image Generator] Generating diagram for '{filename_no_ext}' using Imagen 3...")
        try:
            import requests
            import base64
            base_url = os.getenv("GEMINI_BASE_URL")
            if base_url:
                # Use OpenAI image generation format through proxy
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
                response = requests.post(url, headers=headers, json=data, timeout=40)
                if response.status_code == 200:
                    resp_json = response.json()
                    img_data = resp_json.get("data", [])
                    if img_data and "b64_json" in img_data[0]:
                        img_b64 = img_data[0]["b64_json"]
                        with open(image_path, "wb") as f:
                            f.write(base64.b64decode(img_b64))
                        print(f"  [Image Generator] Successfully saved generated diagram to: {image_path}")
                    elif img_data and "url" in img_data[0]:
                        img_url = img_data[0]["url"]
                        img_resp = requests.get(img_url, timeout=20)
                        if img_resp.status_code == 200:
                            with open(image_path, "wb") as f:
                                f.write(img_resp.content)
                            print(f"  [Image Generator] Successfully saved downloaded diagram to: {image_path}")
                        else:
                            print(f"  [Image Generator Warning] Failed to download image from url: {img_url}")
                            draw_fallback_diagram(prompt_text, content, title_text, image_path)
                    else:
                        print(f"  [Image Generator Warning] Response did not contain images: {resp_json}")
                        draw_fallback_diagram(prompt_text, content, title_text, image_path)
                else:
                    print(f"  [Image Generator Warning] API returned status {response.status_code}: {response.text}")
                    draw_fallback_diagram(prompt_text, content, title_text, image_path)
            else:
                # Fallback to direct Google GenerativeAI API
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
                response = requests.post(url, headers=headers, json=data, timeout=30)
                if response.status_code == 200:
                    resp_json = response.json()
                    if "predictions" in resp_json and len(resp_json["predictions"]) > 0:
                        img_b64 = resp_json["predictions"][0]["bytesBase64Encoded"]
                        with open(image_path, "wb") as f:
                            f.write(base64.b64decode(img_b64))
                        print(f"  [Image Generator] Successfully saved generated diagram to: {image_path}")
                    else:
                        print(f"  [Image Generator Warning] Response did not contain predictions: {resp_json}")
                        draw_fallback_diagram(prompt_text, content, title_text, image_path)
                else:
                    print(f"  [Image Generator Warning] API returned status {response.status_code}: {response.text}")
                    draw_fallback_diagram(prompt_text, content, title_text, image_path)
        except Exception as e:
            print(f"  [Image Generator Warning] Failed to dynamically generate diagram: {e}")
            draw_fallback_diagram(prompt_text, content, title_text, image_path)
            
    markdown_image_tag = ""
    if image_path.exists():
        markdown_image_tag = f"\n\n<p align=\"center\">\n  <img src=\"../images/{image_name}\" alt=\"Sơ đồ luồng nghiệp vụ\" width=\"80%\">\n</p>\n\n"
    
    new_content = re.sub(r"\*Prompt tạo ảnh:\s*.*?\*", markdown_image_tag, content, flags=re.IGNORECASE)
    return new_content

def generate_practice_session_exercises(session_id: str, session_title: str, session_dir_path: str, tech_stack: str, previous_lessons_text: str):
    import pathlib
    session_dir = pathlib.Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    practice_dir = session_dir / "Bài tập"
    practice_dir.mkdir(exist_ok=True)
    
    # Run the generate-review loop
    exercises_data = None
    last_candidate = None
    for attempt in range(3):
        candidate_exercises = practice_creator_agent(session_id, session_title, tech_stack, previous_lessons_text)
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
        
    # Clean legacy single-file artifacts in parent practice_dir
    if practice_dir.exists():
        for old_file in practice_dir.glob("bai_*"):
            if old_file.is_file():
                try:
                    old_file.unlink()
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
        
        # Post-process content to link/generate diagram image
        processed_content = generate_and_link_diagram(content, practice_dir, filename_no_ext)
        
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
    
    # Folder name: {idx+1}_{clean_name}
    ex_folder = practice_dir / f"{idx+1}_{clean_name}"
    ex_folder.mkdir(exist_ok=True)
    
    filename_no_ext = f"bai_{idx+1:02d}_{clean_name}"
    content = ex_data.get("content", "")
    rubric = ex_data.get("rubric", "")
    
    processed_content = generate_and_link_diagram(content, practice_dir, filename_no_ext)
    
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

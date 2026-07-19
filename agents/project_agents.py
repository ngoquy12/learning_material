# agents/project_agents.py
import json
import re
import os
from typing import Dict, Any, List
from pathlib import Path
from core.llm import call_llm

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

def project_entry_test_creator(session_id: str, session_title: str, tech_stack: str, previous_lessons_text: str, test_idx: int) -> Dict[str, Any]:
    print(f"    -> [Project Creator] Generating Entry Test {test_idx+1}/4...")
    
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise ValueError("Cần cấu hình API key để sinh nội dung học liệu. Chế độ offline fallback đã bị loại bỏ.")
        
    domains = ["cinema_booking", "library_catalog", "hotel_room_booking", "courier_shipping"]
    domain = domains[test_idx % len(domains)]
    
    system_prompt = f"""Bạn là giảng viên cao cấp thiết kế đề kiểm tra bài cũ cho sinh viên ngành Công nghệ thông tin.
Nhiệm vụ của bạn là sinh ĐÚNG 1 đề bài kiểm tra đầu giờ (Entry Test) ngắn gọn dựa trên thông tin sau:
Session: {session_id} - {session_title}
Môn học công nghệ: {tech_stack}
Độ khó: Cơ bản (Entry level, làm trong 30-40 phút)
Chủ đề nghiệp vụ kiểm tra: {domain.upper()} (Quản lý {domain})

CÁC QUY TẮC BẮT BUỘC:
1. Cấm rò rỉ kiến thức chưa học (No Concept Leakage): Chỉ kiểm tra các kiến thức đã học trước đó: {previous_lessons_text}. Tuyệt đối cấm đưa vào các khái niệm, thư viện, hoặc cú pháp nâng cao thuộc các session sau.
2. Ngôn từ chuyên nghiệp, học thuật: Cấm tuyệt đối các từ ngữ thân mật, suồng sã hoặc sến súa như "nhé", "nhé các bạn", "thân mến", "nhe", "nha". Không được nhắc đến các từ khóa chỉ hệ thống tự động/AI ("AI", "Assistant", "ChatGPT").
3. Cấm nhãn phân biệt học lực: Cấm tuyệt đối ghi các dòng chữ phân loại học lực (yếu/trung bình/khá/giỏi) hoặc mức độ khó trong tiêu đề hay nội dung bài học.
4. Cấu trúc đề bài bắt buộc:
   - Tên bài: Dùng thẻ '## <center>[Tên đề bài tiếng Việt] ([Tên đề bài tiếng Anh])</center>' (căn giữa). Cấm đánh số thứ tự trong H2 này.
   - Các phần bắt buộc:
     ### **1. Mục tiêu**
     ### **2. Yêu cầu**
     ### **3. Tiêu chí đánh giá**
     ### **4. Yêu cầu nộp bài**
   - Mục Yêu cầu:
     + Khai báo một mảng dữ liệu mô phỏng trong bộ nhớ (In-memory Database) chứa ít nhất 2 bản ghi mẫu ban đầu.
     + Đặc tả đúng 3 API cơ bản (CRUD rút gọn), ghi rõ Phương thức & Endpoint, Input (Request body JSON hoặc Path/Query parameters), Logic xử lý, và Ví dụ phản hồi JSON (thành công & lỗi) bọc qua cấu trúc Unified Envelope chuẩn 6 trường: statusCode, message, data, error, timestamp (hoặc tương tự), path.
   - Mục Tiêu chí đánh giá: Phân bổ trọng số điểm rõ ràng (Tổng 10 điểm) cho các tiêu chí kỹ thuật cụ thể.
   - Mục Yêu cầu nộp bài: Định dạng bắt buộc:
     Để hoàn thành bài tập, sinh viên cần:
     - Đưa mã nguồn lên GitHub.
     - Dán link của repository lên phần nộp bài trên hệ thống.

Đầu ra bắt buộc phải là duy nhất chuỗi XML hợp lệ bọc trong thẻ <entry_test>...</entry_test>:
- <title>: Tên đề kiểm tra ngắn gọn (cấm dùng ký tự '&', nếu cần hãy thay bằng 'and' hoặc 'và').
- <filename>: Tên file viết thường không dấu cách (vd: bai_kiem_tra_01_dat_ve_xem_phim).
- <content>: Nội dung markdown bọc trong khối CDATA.
<entry_test>
  <title>Tên đề kiểm tra</title>
  <filename>bai_kiem_tra_01_dat_ve_xem_phim</filename>
  <content><![CDATA[
Nội dung Markdown đầy đủ của bài kiểm tra ở đây...
  ]]></content>
</entry_test>
"""
    user_prompt = f"Hãy tạo đề bài kiểm tra đầu giờ số {test_idx+1} cho {session_id} thuộc chủ đề {domain}."
    
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
            title = parsed["title"]
            filename = parsed["filename"]
            content = parsed["content"]
            
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
        raise ValueError(f"Không thể tạo được đề kiểm tra {test_idx+1} cho session {session_id} sau 3 lần thử.")
    return test_data

def project_srs_creator(session_id: str, session_title: str, tech_stack: str) -> Dict[str, Any]:
    print(f"    -> [Project Creator] Generating SRS Document...")
    
    system_prompt = f"""Bạn là giảng viên cao cấp kiêm Solution Architect trong dự án doanh nghiệp.
Nhiệm vụ của bạn là sinh 1 tài liệu đặc tả yêu cầu phần mềm SRS (Software Requirements Specification) chi tiết phục vụ cho Mini Project của buổi học:
Session: {session_id} - {session_title}
Môn học công nghệ: {tech_stack}

CÁC QUY TẮC BẮT BUỘC:
1. Độ khó doanh nghiệp: Thiết kế nghiệp vụ thực tế, có tính liên kết chặt chẽ (ví dụ: Quản lý công việc nhóm, Đặt hàng trực tuyến, Sổ cái giao dịch).
2. Ngôn từ chuyên nghiệp, học thuật: Cấm tuyệt đối các từ ngữ thân mật, suồng sã hoặc sến súa như "nhé", "nhé các bạn", "thân mến", "nhe", "nha". Không được nhắc đến "AI", "Assistant". Cấm mọi nhãn phân loại học lực sinh viên.
3. Bảng HTML rộng 100%: Toàn bộ bảng mô tả API, danh mục lỗi, và các bảng dữ liệu phải sử dụng cấu trúc rộng 100% màn hình:
   `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`
4. DTO Pattern & Bảo mật: Đặc tả rõ nét việc lọc dữ liệu nhạy cảm (như mật khẩu băm, internal_notes) bằng các Schemas khác nhau (Internal Model vs Public Response Schema).
5. Global Exception Handler: Đặc tả rõ việc bắt lỗi tập trung (an toàn hệ thống, che giấu Stack Trace thô) và trả về HTTP 500 JSON Envelope.
6. Sơ đồ nghiệp vụ (Prompt tạo ảnh bối cảnh/sự cố nghiệp vụ):
   - Chứa đúng 1 Prompt tạo ảnh.
   - Vị trí: Đặt ở BÊN TRONG phần '### **1. Tổng quan hệ thống**' hoặc '### **2. Đặc tả chức năng**'.
   - Phải viết bằng TIẾNG ANH, định dạng mẫu:
     `*Prompt tạo ảnh: A realistic 16:9 cinematic photo of [mô tả chi tiết bối cảnh sự cố nghiệp vụ/kỹ thuật kịch tính cụ thể ở đây]. [Mô tả trạng thái con người hoặc thiết bị cụ thể thể hiện sự căng thẳng hoặc lỗi hệ thống ở đây]. Cinematic lighting, detailed environment, professional photography, dramatic corporate lighting.*`
   - Yêu cầu phong cách: Bắt buộc ảnh chụp chân thực, sáng tạo, mang tính chất điện ảnh (realistic cinematic photo) thể hiện trực quan và sinh động bối cảnh sự cố hệ thống/nghiệp vụ. Cấm dùng các nét vẽ phẳng tối giản hay sơ đồ đường truyền kỹ thuật nhàm chán đơn điệu.
7. KHÔNG ĐƯỢC TỰ Ý CUNG CẤP CODE: Cấm tuyệt đối việc viết code mẫu hoặc cài đặt logic lập trình thực tế cho sinh viên trong tài liệu SRS (như hàm Python, Java class, TypeScript decorators). SRS chỉ mô tả quy tắc nghiệp vụ bằng lời, công thức toán học, bảng quyết định hoặc mã giả, cấm chứa code block của ngôn ngữ lập trình thực thi thực tế.
8. Cấu trúc tài liệu SRS bắt buộc:
   - Tên tài liệu: Dùng thẻ '## <center>Tài liệu đặc tả Hệ thống API [Tên nghiệp vụ] ([Tên nghiệp vụ tiếng Anh])</center>' (căn giữa).
   - Phải chứa đầy đủ 7 tiêu đề sau đây (dùng thẻ H3 bôi đậm):
     ### **1. Tổng quan hệ thống** (Gồm Mục đích, Đối tượng sử dụng)
     ### **2. Đặc tả chức năng (Functional Requirements)** (Mô tả chi tiết 4-5 API endpoints nghiệp vụ cốt lõi, bao gồm chức năng tìm kiếm nâng cao với logic regex và quy tắc thuật toán nghiệp vụ tính toán nội bộ để trả về kết quả).
     ### **3. Đặc tả phi chức năng (Non-Functional Requirements)** (Gồm bảo mật, tính toàn vẹn dữ liệu, che giấu stack trace).
     ### **4. Đặc tả dữ liệu (Data Model / Schemas)** (Chi tiết các trường dữ liệu Internal Model, Schema thêm mới, Schema phản hồi công khai dưới dạng JSON đại diện cấu trúc).
     ### **5. Danh mục lỗi và Mã thông báo (Error Codes & Unified Envelope)** (Cấu trúc Response Envelope 6 trường và bảng danh mục lỗi ERR-TASK-xx).
     ### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)** (Bảng HTML liệt kê Vị trí phát sinh, Tình huống lỗi, Mã lỗi, Hành động xử lý bắt buộc).
     ### **7. Giao diện kiểm thử và Phản hồi hệ thống (API Specifications & Interface)** (Swagger UI và ReDoc, các bước Try it out, Response mẫu dưới dạng JSON).

Đầu ra bắt buộc phải là duy nhất chuỗi XML hợp lệ bọc trong thẻ <srs_doc>...</srs_doc>:
- <title>: Tên tài liệu đặc tả ngắn gọn.
- <content>: Nội dung markdown bọc trong khối CDATA.
<srs_doc>
  <title>Tài liệu đặc tả yêu cầu SRS</title>
  <content><![CDATA[
Nội dung Markdown đầy đủ của tài liệu SRS ở đây...
  ]]></content>
</srs_doc>
"""
    user_prompt = f"Hãy tạo tài liệu đặc tả SRS chi tiết nhưng cực kỳ cô đọng, súc tích cho Mini Project của {session_id}. Lưu ý: Viết ngắn gọn, tập trung vào cấu trúc kỹ thuật và API, tránh giải thích dông dài lê thê để đảm bảo tài liệu đầy đủ các phần và kết thúc bằng thẻ đóng </content> và </srs_doc> mà không bị cắt cụt giữa chừng."
    
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
            else:
                ends_with_srs_doc = "</srs_doc>" in response
                ends_with_content = "</content>" in response
                print(f"      [Warning] Attempt {attempt+1} failed to parse title/content. Length: {len(response)}. Contains </content>: {ends_with_content}, </srs_doc>: {ends_with_srs_doc}")
                print(f"      [Debug] First 100: {response[:100]}")
                print(f"      [Debug] Last 300: {response[-300:] if len(response) > 300 else response}")
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to parse SRS XML: {e}")
            if response:
                print(f"      [Debug] Response length: {len(response)}. Suffix: {response[-300:] if len(response) > 300 else response}")
            
    if not srs_data:
        raise ValueError(f"Không thể sinh được tài liệu SRS cho session {session_id} sau 3 lần thử.")
    return srs_data

def project_mini_project_creator(session_id: str, session_title: str, tech_stack: str, srs_title: str) -> Dict[str, Any]:
    print(f"    -> [Project Creator] Generating Mini Project Prompt...")
    
    system_prompt = f"""Bạn là giảng viên cao cấp thiết kế đề bài Mini Project tinh gọn cho sinh viên ngành Công nghệ thông tin.
Nhiệm vụ của bạn là sinh 1 đề bài Mini Project ngắn gọn cho:
Session: {session_id} - {session_title}
Môn học công nghệ: {tech_stack}

CÁC QUY TẮC BẮT BUỘC:
1. Tinh gọn cực độ: Đề bài Mini Project đóng vai trò như các thẻ nhiệm vụ tóm tắt. TUYỆT ĐỐI CẤM định nghĩa chi tiết Pydantic Schema, bảng mã lỗi, hay ví dụ JSON response dài dòng tại đây. Hãy lược bỏ các phần này để sinh viên có trải nghiệm tinh gọn, không bị quá tải thông tin.
2. Dẫn link liên kết đến SRS: Bắt buộc ghi rõ chú thích dẫn link đến file đặc tả SRS để sinh viên tự tra cứu cấu trúc kỹ thuật:
   *Ví dụ chú thích: "Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, Pydantic validation, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md)."*
3. Ngôn từ chuyên nghiệp, học thuật: Cấm tuyệt đối các từ ngữ thân mật, suồng sã như "nhé", "nhé các bạn", "thân mến". Không được nhắc đến "AI", "Assistant". Cấm mọi nhãn phân loại học lực sinh viên.
4. Bảng HTML rộng 100%: Bảng chấm điểm phải rộng 100% màn hình:
   `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`
5. Cấu trúc đề bài bắt buộc:
   - Tên bài: Dùng thẻ '## <center>[Mini project] Hệ thống API [Tên nghiệp vụ] ([Tên nghiệp vụ tiếng Anh])</center>' (căn giữa).
   - Phải chứa đầy đủ 3 tiêu đề sau đây trong content (dùng thẻ H3 bôi đậm):
     ### **1. Mục tiêu dự án**
     ### **2. Đề bài và Yêu cầu** (Liệt kê các đầu việc lớn dưới dạng Task 1: Khởi tạo database RAM; Task 2: Viết CRUD APIs; Task 3: Viết API Dashboard. Chỉ rõ đường dẫn tương đối tới SRS).
     ### **3. Yêu cầu nộp bài** (Định dạng bắt buộc y hệt 4 dòng chuẩn).

Đầu ra bắt buộc phải là duy nhất chuỗi XML hợp lệ bọc trong thẻ <mini_project>...</mini_project>:
- <title>: Tên đề bài ngắn gọn.
- <content>: Nội dung markdown mô tả đề bài bọc trong khối CDATA (bao gồm các phần 1. Mục tiêu dự án đến 3. Yêu cầu nộp bài, tuyệt đối KHÔNG chứa Tiêu chí chấm điểm ở đây).
- <rubric>: Nội dung markdown chi tiết về Tiêu chí chấm điểm (AI) bọc trong khối CDATA, thiết kế thang điểm chi tiết tổng 100 điểm + bonus theo 5 nhóm tiêu chí từ mẫu báo cáo tiêu chí chấm điểm:
  + Cấu trúc tiêu đề của rubric phải bắt đầu bằng: ### **Tiêu chí chấm điểm (AI)**
  + Theo sau là: **[Tên Dự Án] — Tổng điểm: 100 điểm**
  + Tiếp theo là 5 nhóm tiêu chí cụ thể:
    #### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
    #### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
    #### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
    #### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
    #### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
    #### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**

<mini_project>
  <title>Đề bài Mini Project</title>
  <content><![CDATA[
Nội dung Markdown đề bài Mini Project ở đây...
  ]]></content>
  <rubric><![CDATA[
### **Tiêu chí chấm điểm (AI)**
**[Tên Dự Án] — Tổng điểm: 100 điểm**
...
  ]]></rubric>
</mini_project>
"""
    user_prompt = f"Hãy tạo đề bài Mini Project tinh gọn cho {session_id}."
    
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
        raise ValueError(f"Không thể sinh được đề bài Mini Project cho session {session_id} sau 3 lần thử.")
    return project_data

def project_reviewer_agent(entry_tests: List[Dict[str, Any]], srs_doc: Dict[str, Any], mini_project: Dict[str, Any], tech_stack: str) -> Dict[str, Any]:
    print("  [Project Reviewer] Verifying project templates and specs...")
    
    # 1. Verify Entry Tests quantity
    if len(entry_tests) != 4:
        return {"status": "REJECTED", "feedback": f"Số lượng bài kiểm tra đầu giờ là {len(entry_tests)}, không đúng quy định bắt buộc phải là đúng 4 đề song song."}
        
    mp_content = mini_project.get("content", "")
    mp_rubric = mini_project.get("rubric", "")
    
    # Prepare all files to scan
    all_files = entry_tests + [
        srs_doc,
        {"title": "Mini Project Content", "content": mp_content},
        {"title": "Mini Project Rubric", "content": mp_rubric}
    ]
    
    forbidden_words = ["nhé", "thân mến", "nhé các bạn", "nhe", "nha", "assistant", "chatgpt", "openai", "gemini", "llm", "copilot"]
    discriminatory_labels = ["dành cho sinh viên", "dành cho học viên", "mức độ:", "độ khó:", "yếu/trung bình", "học lực"]
    
    for idx, doc in enumerate(all_files):
        content = doc.get("content", "")
        title = doc.get("title", "")
        
        # 2. Check forbidden suồng sã/AI words
        for word in forbidden_words:
            pattern = rf"\b{word}\b"
            if re.search(pattern, content, re.IGNORECASE):
                return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa từ cấm suồng sã hoặc liên quan đến AI: '{word}'."}
                
        # Check case-sensitive "AI" (exempting "Tiêu chí chấm điểm (AI)" header in rubric)
        content_for_ai_check = content
        if "Tiêu chí chấm điểm (AI)" in content_for_ai_check:
            content_for_ai_check = content_for_ai_check.replace("Tiêu chí chấm điểm (AI)", "")
        if "Tiêu chí chấm điểm (ai)" in content_for_ai_check:
            content_for_ai_check = content_for_ai_check.replace("Tiêu chí chấm điểm (ai)", "")
        if re.search(r"\bAI\b", content_for_ai_check):
            return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa từ viết tắt 'AI'. Hãy tránh nhắc đến AI hoặc trợ lý ảo."}
                
        # 3. Check discriminatory student categorization labels
        for fl in discriminatory_labels:
            if fl in content.lower():
                return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa nhãn phân loại học lực hoặc mức độ '{fl}'. Hãy loại bỏ nhãn này để tránh gây sự phân biệt cho sinh viên."}
                
        # 4. Check that HTML tables have style width 100%
        if "<table" in content and "width: 100%" not in content and 'width="100%"' not in content:
            return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' sử dụng bảng HTML nhưng chưa cấu hình chiều rộng 100% màn hình."}

    # 5. Check SRS specific headers
    srs_content = srs_doc.get("content", "")
    srs_required = [
        r"### \*\*1\.\s+Tổng quan",
        r"### \*\*2\.\s+Đặc tả chức năng",
        r"### \*\*3\.\s+Đặc tả phi chức năng",
        r"### \*\*4\.\s+Đặc tả dữ liệu",
        r"### \*\*5\.\s+Danh mục lỗi",
        r"### \*\*6\.\s+Bảng tổng hợp tình huống lỗi",
        r"### \*\*7\.\s+Giao diện kiểm thử"
    ]
    for r_hdr in srs_required:
        if not re.search(r_hdr, srs_content, re.IGNORECASE):
            return {"status": "REJECTED", "feedback": f"Tài liệu đặc tả SRS thiếu tiêu đề bắt buộc hoặc không đúng định dạng H3 bôi đậm: '{r_hdr.replace('\\', '')}'."}

    # 6. Check Mini Project specific headers inside content
    mp_required = [
        r"### \*\*1\.\s+Mục tiêu dự án",
        r"### \*\*2\.\s+Đề bài và Yêu cầu",
        r"### \*\*3\.\s+Yêu cầu nộp bài"
    ]
    for r_hdr in mp_required:
        if not re.search(r_hdr, mp_content, re.IGNORECASE):
            return {"status": "REJECTED", "feedback": f"Đề bài Mini Project thiếu tiêu đề bắt buộc hoặc không đúng định dạng H3 bôi đậm: '{r_hdr.replace('\\', '')}'."}

    # Check Mini Project rubric headers
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

    # 7. Check relative link to SRS inside Mini Project content
    if "tai_lieu_dac_ta_yeu_cau_srs.md" not in mp_content:
        return {"status": "REJECTED", "feedback": "Đề bài Mini Project chưa chứa đường dẫn liên kết tham chiếu tương đối chính xác đến tài liệu đặc tả SRS."}

    # 8. Check that diagram prompt is in English and has correct design description
    if "*Prompt tạo ảnh:" not in srs_content:
        return {"status": "REJECTED", "feedback": "Tài liệu đặc tả SRS không chứa hoặc đặt sai vị trí '*Prompt tạo ảnh:'."}
        
    prompt_match = re.search(r"\*Prompt tạo ảnh:\s*(.*?)\*", srs_content, re.IGNORECASE)
    if prompt_match:
        prompt_text = prompt_match.group(1).lower()
        cinematic_keywords = ["cinematic", "photo", "lighting", "photography", "realistic"]
        if not any(kw in prompt_text for kw in cinematic_keywords):
            return {"status": "REJECTED", "feedback": "Prompt tạo ảnh trong SRS thiếu mô tả phong cách ảnh điện ảnh chân thực (realistic cinematic photo)."}

    # 9. Check that SRS does not contain project implementation code blocks
    code_blocks = re.findall(r"```[a-zA-Z]*\n(.*?)\n```", srs_doc.get("content", ""), re.DOTALL)
    for block in code_blocks:
        block_lower = block.lower()
        # Avoid detecting JSON schemas/responses as code blocks
        if any(kw in block_lower for kw in ["def ", "class ", "public class", "private ", "function ", "@injectable", "@controller", "import ", "from "]) and not "{" in block_lower:
            return {"status": "REJECTED", "feedback": "Tài liệu đặc tả SRS tự ý cài đặt code mẫu/logic lập trình cho sinh viên. SRS chỉ được phép mô tả nghiệp vụ và cấu trúc API, cấm gợi ý code triển khai."}

    return {"status": "APPROVED", "feedback": "Bộ học liệu Mini Project đạt tất cả tiêu chuẩn chất lượng tinh gọn."}

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

def draw_fallback_diagram(prompt_text: str, content: str, title_text: str, image_path: Path):
    try:
        from PIL import Image, ImageDraw, ImageFont
        endpoints, storage = parse_diagram_info(prompt_text, content)
        
        # 16:9 Aspect Ratio
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), "#0F172A") # Deep slate blue-gray
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 28)
            font_header = ImageFont.truetype("arial.ttf", 20)
            font_body = ImageFont.truetype("arial.ttf", 16)
            font_code = ImageFont.truetype("consolas.ttf", 15)
            font_label = ImageFont.truetype("arial.ttf", 14)
        except Exception:
            font_title = ImageFont.load_default()
            font_header = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_code = ImageFont.load_default()
            font_label = ImageFont.load_default()
            
        # Draw tech grid
        grid_size = 40
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill="#1E293B", width=1)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill="#1E293B", width=1)
            
        # Incident Title Panel (Bright Red Warning Border)
        draw.rounded_rectangle([40, 30, width-40, 95], radius=8, fill="#1E1E2F", outline="#EF4444", width=3)
        draw.text((width//2, 62), f"CRITICAL INCIDENT ALERT: {title_text.upper()}", fill="#F87171", font=font_title, anchor="mm")
        
        # LEFT PANEL: SYSTEM METRICS (Status: DEGRADED)
        metrics_box = [60, 140, 380, 660]
        draw.rounded_rectangle(metrics_box, radius=10, fill="#1E293B", outline="#F59E0B", width=2)
        draw.text((220, 175), "INCIDENT STATE", fill="#F59E0B", font=font_header, anchor="mm")
        draw.line([(80, 200), (360, 200)], fill="#334155", width=2)
        
        metrics = [
            ("STATUS:", "DEGRADED", "#F87171"),
            ("CPU LOAD:", "99.4% (CRITICAL)", "#F87171"),
            ("LATENCY:", "4850 ms", "#FBBF24"),
            ("STORAGE:", storage.upper(), "#E2E8F0"),
            ("LEAK TYPE:", "RESOURCE LOCK", "#F87171"),
        ]
        
        y_offset = 230
        for label, val, val_color in metrics:
            draw.text((90, y_offset), label, fill="#94A3B8", font=font_body)
            draw.text((210, y_offset), val, fill=val_color, font=font_body)
            y_offset += 45
            
        # Urgent notice footer inside metrics
        draw.rounded_rectangle([80, 480, 360, 630], radius=6, fill="#0F172A", outline="#EF4444", width=1)
        draw.text((220, 510), "ACTION REQUIRED:", fill="#F87171", font=font_header, anchor="mm")
        notice_text = "Optimize algorithms &\nresolve critical leaks\nin FastAPI endpoint\nto restore operations."
        y_n = 535
        for line in notice_text.split("\n"):
            draw.text((220, y_n), line, fill="#E2E8F0", font=font_label, anchor="mm")
            y_n += 22

        # CENTER PANEL: JAGGED CRITICAL WAVEFORM (Performance Bottleneck)
        wave_box = [420, 140, 860, 660]
        draw.rounded_rectangle(wave_box, radius=10, fill="#1E293B", outline="#475569", width=2)
        draw.text((640, 175), "LATENCY ANOMALY CHART (SPIKE)", fill="#E2E8F0", font=font_header, anchor="mm")
        draw.line([(440, 200), (840, 200)], fill="#334155", width=2)
        
        # Draw waveform coordinate system
        draw.line([(460, 240), (460, 620)], fill="#475569", width=2)
        draw.line([(460, 620), (830, 620)], fill="#475569", width=2)
        
        # Waveform points (simulating a dramatic lag spike)
        points = [
            (460, 580), (500, 570), (540, 590), (580, 520), (620, 540),
            (660, 260), # HUGE CRITICAL SPIKE
            (700, 320), (740, 450), (780, 540), (820, 560)
        ]
        draw.line(points, fill="#EF4444", width=4)
        
        # Draw flashing critical alert point at the top of the spike
        draw.ellipse([650, 250, 670, 270], fill="#EF4444", outline="#FCA5A5", width=2)
        draw.text((680, 245), "BOTTLENECK DETECTED", fill="#F87171", font=font_label)
        
        # Add labels to chart
        draw.text((435, 260), "5s", fill="#94A3B8", font=font_label, anchor="rm")
        draw.text((435, 450), "2.5s", fill="#94A3B8", font=font_label, anchor="rm")
        draw.text((435, 620), "0s", fill="#94A3B8", font=font_label, anchor="rm")

        # RIGHT PANEL: FLAGGED API ENDPOINTS
        api_box = [900, 140, 1220, 660]
        draw.rounded_rectangle(api_box, radius=10, fill="#1E293B", outline="#A855F7", width=2)
        draw.text((1060, 175), "AFFECTED ROUTERS", fill="#A855F7", font=font_header, anchor="mm")
        draw.line([(920, 200), (1200, 200)], fill="#334155", width=2)
        
        draw.text((925, 220), "Active endpoint targets:", fill="#E2E8F0", font=font_body)
        
        y_offset = 260
        for method, path in endpoints:
            m_color = "#34D399" # Green for GET
            if method == "POST":
                m_color = "#FBBF24" # Yellow/Orange for POST
            elif method in ["DELETE", "REMOVE"]:
                m_color = "#F87171" # Red for DELETE
            elif method in ["PUT", "PATCH"]:
                m_color = "#60A5FA" # Blue for PUT/PATCH
                
            draw.rounded_rectangle([925, y_offset-2, 1005, y_offset+22], radius=4, fill="#0F172A", outline=m_color, width=1)
            draw.text((965, y_offset+10), method, fill=m_color, font=font_code, anchor="mm")
            draw.text((1015, y_offset+10), path, fill="#E2E8F0", font=font_code, anchor="lm")
            y_offset += 55
            
        draw.text((925, 520), "Host: localhost:8000", fill="#94A3B8", font=font_body)
        draw.text((925, 555), "Protocol: HTTP/1.1 JSON", fill="#94A3B8", font=font_body)
        draw.text((925, 590), "Status: 503 Service Temp", fill="#F87171", font=font_body)

        draw.rectangle([5, 5, width-5, height-5], outline="#EF4444", width=3)
        
        image_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(image_path)
        print(f"  [Image Incident Visualizer Fallback] Programmatically drew incident report dashboard to: {image_path}")
    except Exception as e:
        print(f"  [Image Incident Visualizer Error] Failed to draw incident: {e}")

def generate_and_link_srs_diagram(content: str, srs_dir, filename_no_ext: str) -> str:
    images_dir = Path(srs_dir) / "images"
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
        title_text = filename_no_ext.replace("bai_", "").replace("_", " ").title()
        
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key and not image_path.exists():
        print(f"  [Image Generator] Generating business diagram using Imagen 3...")
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
                "instances": [
                    {
                        "prompt": prompt_text
                    }
                ],
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
                    print(f"  [Image Generator] Saved diagram to: {image_path}")
                else:
                    print(f"  [Image Generator Warning] Response did not contain images: {resp_json}")
                    draw_fallback_diagram(prompt_text, content, title_text, image_path)
            else:
                print(f"  [Image Generator Warning] API status {response.status_code}: {response.text}")
                draw_fallback_diagram(prompt_text, content, title_text, image_path)
        except Exception as e:
            print(f"  [Image Generator Warning] Dynamic image generation error: {e}")
            draw_fallback_diagram(prompt_text, content, title_text, image_path)
    elif not image_path.exists():
        # Draw fallback if no API key
        draw_fallback_diagram(prompt_text, content, title_text, image_path)
            
    markdown_image_tag = f"\n\n<p align=\"center\">\n  <img src=\"./images/{image_name}\" alt=\"Sơ đồ nghiệp vụ\" width=\"80%\">\n</p>\n\n"
    new_content = re.sub(r"\*Prompt tạo ảnh:\s*.*?\*", markdown_image_tag, content, flags=re.IGNORECASE)
    return new_content

def generate_mini_project_session(session_id: str, session_title: str, session_dir_path: str, tech_stack: str, previous_lessons_text: str):
    import pathlib
    session_dir = pathlib.Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    test_dir = session_dir / "Bài kiểm tra đầu giờ"
    srs_dir = session_dir / "Tài liệu đặc tả SRS"
    mp_dir = session_dir / "Mini project"
    
    test_dir.mkdir(exist_ok=True)
    srs_dir.mkdir(exist_ok=True)
    mp_dir.mkdir(exist_ok=True)
    
    # Generation & review loop
    final_entry_tests = []
    final_srs_doc = None
    final_mini_project = None
    
    for attempt in range(3):
        # 1. Generate 4 Entry Tests sequentially
        entry_tests = []
        for idx in range(4):
            test = project_entry_test_creator(session_id, session_title, tech_stack, previous_lessons_text, idx)
            entry_tests.append(test)
            
        # 2. Generate SRS
        srs_doc = project_srs_creator(session_id, session_title, tech_stack)
        
        # 3. Generate Mini Project
        mini_project = project_mini_project_creator(session_id, session_title, tech_stack, srs_doc["title"])
        
        # 4. Review
        review_result = project_reviewer_agent(entry_tests, srs_doc, mini_project, tech_stack)
        if review_result["status"] == "APPROVED":
            final_entry_tests = entry_tests
            final_srs_doc = srs_doc
            final_mini_project = mini_project
            print(f"  [Project Reviewer] APPROVED: {review_result['feedback']}")
            break
        else:
            print(f"  [Project Reviewer] REJECTED (Attempt {attempt+1}): {review_result['feedback']}")
            
    if not final_entry_tests:
        raise ValueError(f"Không thể sinh được bộ học liệu Mini Project đạt tiêu chuẩn cho session {session_id} sau nhiều lượt tạo/đánh giá.")
        
    # Save files
    # 1. Entry tests (clean old tests first)
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
        
    # 2. SRS doc
    srs_filename = "tai_lieu_dac_ta_yeu_cau_srs.md"
    srs_file_path = srs_dir / srs_filename
    processed_srs_content = generate_and_link_srs_diagram(final_srs_doc["content"], srs_dir, "so_do_dac_ta_nghiep_vu")
    with open(srs_file_path, "w", encoding="utf-8") as f:
        f.write(processed_srs_content)
    print(f"  [Success] Saved SRS Document: {srs_file_path}")
    
    # 3. Mini Project
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

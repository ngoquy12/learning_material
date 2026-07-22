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
        
        system_prompt = f"""Bạn là giảng viên cao cấp thiết kế bài thực hành thực tế cho sinh viên ngành Công nghệ thông tin.
Nhiệm vụ của bạn là sinh ĐÚNG 1 bài tập thực hành dành cho:
Session: {session_id} - {session_title}
Môn học công nghệ: {tech_stack}

ĐỘ KHÓ YÊU CẦU:
- Mức độ: {level_name} (Dành cho sinh viên {target_student})
- Chủ đề nghiệp vụ: Phân hệ {domain.upper()} (Quản lý {domain})

CÁC QUY TẮC BẮT BUỘC CHO BÀI TẬP:
0. QUY TẮC CẤM EMOJI: TUYỆT ĐỐI KHÔNG sử dụng bất kỳ biểu tượng cảm xúc/emoji (như 🚀, 💡, ⚠️, ✅, ❌,...) trong toàn bộ đề bài, tiêu đề hay mã nguồn. Thay bằng các nhãn văn bản thuần túy [NOTE], [TIP], [WARNING], [YÊU CẦU].
0.1 QUY TẮC GIỚI HẠN KIẾN THỨC ĐỘNG BẮT BUỘC (DYNAMIC PROGRESSIVE SCOPE):
   - Bạn BẮT BUỘC CHỈ ĐƯỢC PHÉP sử dụng các kiến thức thuộc Session hiện tại ({session_id} - {session_title}) và các bài học trước đó.
   - TUYỆT ĐỐI CẤM đưa vào bất kỳ khái niệm, cú pháp, hàm hay thư viện thuộc các bài học SAU ĐÓ trong chương trình đào tạo!
1. Độ khó tương ứng với mức {level_name}:
   - Nếu là Dễ: Tập trung làm quen cú pháp, cấu hình ban đầu, xây dựng các cấu trúc/chức năng đơn giản nhất. CẤM TUYỆT ĐỐI các chức năng lọc, tìm kiếm, sắp xếp hay phân trang ở mức độ này.
   - Nếu là Trung bình: Xây dựng các chức năng cơ bản, tiếp nhận tham số đầu vào đơn giản. CẤM TUYỆT ĐỐI các chức năng lọc, tìm kiếm, sắp xếp hay phân trang phức tạp ở mức độ này.
   - Nếu là Khá: Giải quyết luồng nghiệp vụ thực tế trung bình, yêu cầu validation đầu vào chặt chẽ, xử lý ngoại lệ nghiệp vụ cụ thể. Nếu có tìm kiếm/lọc, bắt buộc phải có ví dụ cụ thể ở phần Đầu vào (Input).
   - Nếu là Giỏi: Xây dựng bài toán tổng hợp, kết hợp nhiều cấu trúc/module, lọc/tìm kiếm nâng cao (kết hợp phân trang, sắp xếp, lọc đa tham số) hoặc xử lý dữ liệu phức tạp. Bắt buộc phải có ví dụ cụ thể ở phần Đầu vào (Input).
   - Nếu là Xuất sắc: Thách thức cao về tư duy logic nghiệp vụ doanh nghiệp, tối ưu hóa xử lý lỗi, bảo mật hoặc xử lý logic nghiệp vụ chéo phức tạp. Nếu có lọc/tìm kiếm, bắt buộc phải có ví dụ cụ thể ở phần Đầu vào (Input).
2. Trọng tâm kiến thức: Chỉ dựa vào kiến thức gần nhất trước đó ({previous_lessons_text}) và các buổi học lý thuyết trước đó để làm chủ đề kiến thức. CẤM đưa các khái niệm, cú pháp hoặc thư viện nâng cao mà sinh viên chưa từng được học vào đề bài.
3. Định dạng bài tập:
   - Trình bày dạng Markdown học thuật chỉnh chu theo chuẩn trường đại học, khoa học, dễ hiểu.
   - Không được dùng các cụm từ như "AI", "Assistant". CẤM TUYỆT ĐỐI các từ ngữ suồng sã, thân mật hoặc sến súa như "nhé", "nhé các bạn", "thân mến", "nhe", "nha".
4. Cấu trúc bài tập:
   - Tên bài tập: Dùng thẻ '## <center>[Tên bài tập]</center>' (căn giữa). Tên bài tập BẮT BUỘC phải viết bằng TIẾNG VIỆT CÓ DẤU CHUẨN XÁC (Ví dụ: '## <center>Tính Toán Hóa Đơn và Phân Hạng Khách Hàng Ecommerce</center>'). CẤM TUYỆT ĐỐI viết không dấu, cấm ghi số thứ tự bài tập ở tiêu đề chính này.
   - Tên các tiêu đề phần trong bài tập: Dùng thẻ '### **1. Mục tiêu**', '### **2. Vấn đề**', '### **3. Yêu cầu bài toán**', '### **4. Quy tắc xử lý**', '### **5. Yêu cầu nộp bài**' (căn trái, bôi đậm).
   - Mục tiêu: Viết sâu sắc, nêu bật sau khi học xong sinh viên áp dụng/ứng dụng được gì về mặt kỹ thuật/lý thuyết chung. CẤM TUYỆT ĐỐI ghi các từ khoá chỉ mức độ khó (Dễ/Trung bình/Khá/Giỏi/Xuất sắc) hay phân nhóm học lực (yếu/trung bình/khá/giỏi/xuất sắc) trong phần này hoặc bất kỳ phần nào khác của đề bài nhằm tránh gây sự tự ti hay phân biệt cho học viên.
   - Vấn đề: Phải mô tả sâu sắc, thuyết phục các khó khăn thực tế của doanh nghiệp để làm nổi bật lý do phải dùng giải pháp này.
   - Tùy biến cách trình bày các chức năng/API/thành phần ở đầu phần Yêu cầu bài toán:
     - Nếu bài tập chỉ chứa 1 hoặc ít chức năng/thành phần đơn giản: Hãy trình bày dạng danh sách gạch đầu dòng ngắn gọn.
     - Nếu bài tập có nhiều chức năng/API/thành phần phức tạp (từ 2 trở lên): Hãy trình bày dưới dạng bảng HTML sử dụng thẻ `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">` (đặt thuộc tính style để bảng rộng 100% màn hình, không bị co hẹp). Các cột trong bảng phải được thiết kế phù hợp với đặc thù môn học công nghệ hiện tại ({tech_stack}):
       + Với Web API (FastAPI, NestJS, Spring Boot...): Phương thức, Endpoint, Mô tả chức năng.
       + Với Lập trình cơ bản/OOP/Thuật toán: Tên lớp/Hàm, Tham số đầu vào, Đầu ra, Mô tả xử lý.
       + Với Cơ sở dữ liệu: Bảng/Collection, Tên trường, Kiểu dữ liệu, Ràng buộc nghiệp vụ.
       + Với DevOps/Hệ thống/Git: Lệnh/File cấu hình, Tham số, Chức năng xử lý.
       + Với các môn học khác: Thiết kế cột linh hoạt và logic nhất đại diện cho cấu trúc của bài học.
   - Chi tiết Yêu cầu bài toán:
      - NẾU bài toán chỉ có DUY NHẤT 1 yêu cầu (1 API/1 chức năng), bạn CẤM TUYỆT ĐỐI ghi nhãn là "Yêu cầu 1:". Hãy viết thẳng nội dung yêu cầu đó bằng một câu mô tả cụ thể.
      - NẾU bài toán có từ 2 yêu cầu trở lên, bạn mới sử dụng các ký tự đầu dòng như `- Yêu cầu 1:`, `- Yêu cầu 2:`.
      - Với mỗi yêu cầu con, bạn BẮT BUỘC phải chỉ rõ thông tin Đầu vào (Input) và Đầu ra (Output) cụ thể ở phía cuối dưới dạng thụt lề:
        - Đầu vào (Input): ...
        - Đầu ra (Output): ...
        - QUY TẮC CỐT LÕI VỀ CODE/DATA & TÍNH NHẤT QUÁN LOGIC:
          - Nếu Đầu ra (Output) hay Đầu vào (Input) có cấu trúc dữ liệu dạng mã (ví dụ như JSON payload, XML body, Code Block), bạn BẮT BUỘC phải viết trực tiếp cấu trúc mã/JSON cụ thể tương ứng đặt trong block code markdown tương ứng (ví dụ: ```json ... ```) và căn chỉnh thụt dòng thật chuẩn xác.
          - Đặc biệt, với các chức năng tìm kiếm/lọc: Ở phần Đầu vào (Input), bạn phải chỉ rõ một ví dụ giá trị tham số truyền vào cụ thể (Ví dụ: `q=Ha Noi`, `min_price=100000.0`). Ở phần Đầu ra (Output) ví dụ, dữ liệu mẫu trả về BẮT BUỘC phải khớp hoàn toàn với giá trị đã giả định lọc đó (ví dụ: các bản ghi trả về phải thực sự thỏa mãn logic của tham số lọc giả định). CẤM TUYỆT ĐỐI trả về các đối tượng không thỏa mãn logic của tham số lọc giả định.
    - Quy tắc xử lý: Chứa các quy tắc nghiệp vụ, ràng buộc dữ liệu (ví dụ: validations, giá trị tối thiểu/tối đa) hoặc ràng buộc cấu trúc tập tin/thư mục bắt buộc cho bài thực hành.
    - Yêu cầu nộp bài: Định dạng BẮT BUỘC phải là:
      Để hoàn thành bài tập, sinh viên cần:
      - Đưa mã nguồn lên GitHub.
      - Dán link của repository lên phần nộp bài trên hệ thống.
 5. Quy tắc sinh Prompt tạo ảnh (Ảnh minh họa bối cảnh/sơ đồ nghiệp vụ kỹ thuật thực tế):
    - Chuỗi Prompt tạo ảnh bắt buộc phải được viết bằng TIẾNG ANH để các mô hình tạo ảnh (như DALL-E, Stable Diffusion, Imagen 3) hiểu chính xác nhất.
    - Phong cách thiết kế của ảnh: Bắt buộc yêu cầu ảnh chụp thực tế hoặc sơ đồ luồng dữ liệu 3D sinh động (realistic system dashboard mockup, 3D data-flow diagram overlay, or detailed software interface mockup). Ảnh phải thể hiện rõ các thành phần nghiệp vụ đan xen liên quan trực tiếp đến bài toán (ví dụ: giao diện phần mềm quản trị có các thông số nghiệp vụ cụ thể, API endpoints, dữ liệu cấu trúc JSON dạng khối đan xen, hoặc bản đồ theo dõi đơn hàng thời gian thực). Tránh các hình ảnh chụp chung chung khó hiểu.
    - Vị trí: Đặt ở BÊN TRONG phần '### **2. Vấn đề**' (ở ngay phía dưới mô tả vấn đề bối cảnh ban đầu, không được để cuối bài học hay trước Vấn đề).
    - Định dạng và mẫu bắt buộc của prompt: Bạn bắt buộc phải ghi đúng cấu trúc mẫu sau (chỉ thay đổi phần mô tả chi tiết trong ngoặc vuông, giữ nguyên các phần còn lại):
      `*Prompt tạo ảnh: A realistic 16:9 cinematic photo of [mô tả chi tiết các thành phần nghiệp vụ, giao diện phần mềm, API endpoints, hoặc sơ đồ luồng dữ liệu 3D đan xen liên quan trực tiếp đến bài toán ở đây]. [Mô tả cụ thể các chi tiết kỹ thuật hiển thị trên màn hình hoặc giao diện hệ thống ở đây]. Cinematic lighting, detailed software environment, professional visualization, high tech aesthetics.*`

Đầu ra bắt buộc phải là duy nhất chuỗi XML hợp lệ bọc trong thẻ <exercise>...</exercise>:
- <title>: Tên bài tập ngắn gọn bằng TIẾNG VIỆT CÓ DẤU CHUẨN XÁC (CẤM TUYỆT ĐỐI viết không dấu, cấm dùng ký tự '&', nếu cần hãy thay bằng 'and' hoặc 'và').
- <filename>: Tên file viết thường không dấu cách.
- <content>: Nội dung markdown mô tả đề bài bọc trong khối CDATA (bao gồm các phần 1. Mục tiêu đến 5. Yêu cầu nộp bài, tuyệt đối KHÔNG chứa Tiêu chí chấm điểm ở đây).
- <rubric>: Nội dung markdown chi tiết về Tiêu chí chấm điểm (AI) bọc trong khối CDATA, thiết kế thang điểm chi tiết tổng 100 điểm + bonus theo 5 nhóm tiêu chí từ mẫu báo cáo tiêu chí chấm điểm:
  + Cấu trúc tiêu đề của rubric phải bắt đầu bằng: ### **Tiêu chí chấm điểm (AI)**
  + Theo sau là: **[Tên Bài Tập] — Tổng điểm: 100 điểm**
  + Tiếp theo là 5 nhóm tiêu chí cụ thể:
    #### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
    #### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
    #### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
    #### **4. Kiểm thử hoặc câu hỏi lý thuyết bổ sung — 10 điểm**
    #### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
    #### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**

<exercise>
  <title>Xây dựng API Quản lý Đơn hàng Ecommerce (Tên bài tập bằng tiếng Việt có dấu)</title>
  <filename>xay_dung_api_quan_ly_san_pham</filename>
  <content><![CDATA[
Nội dung Markdown đề bài bài tập ở đây...
  ]]></content>
  <rubric><![CDATA[
### **Tiêu chí chấm điểm (AI)**
**[Tên Bài Tập] — Tổng điểm: 100 điểm**
...
  ]]></rubric>
</exercise>
"""
        user_prompt = f"Hãy tạo đề bài thực hành mức độ {level_name} cho {session_id}."
        
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

        # 11. Check prompt location and English-language verification
        idx_problem = content.find("2. Vấn đề")
        idx_req = content.find("3. Yêu cầu bài toán")
        
        if idx_problem == -1 or idx_req == -1:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' không định nghĩa đúng cấu trúc phần Vấn đề hoặc Yêu cầu bài toán."}
            
        sub_content = content[idx_problem:idx_req]
        if "*Prompt tạo ảnh:" not in sub_content:
            return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' không chứa hoặc đặt sai vị trí '*Prompt tạo ảnh:' (yêu cầu đặt nằm bên trong phần Vấn đề)."}
        
        # Check if the prompt inside contains cinematic photo keywords
        prompt_match = re.search(r"\*Prompt tạo ảnh:\s*(.*?)\*", sub_content, re.IGNORECASE)
        if prompt_match:
            prompt_text = prompt_match.group(1).lower()
            cinematic_keywords = ["cinematic", "photo", "lighting", "photography", "realistic"]
            if not any(kw in prompt_text for kw in cinematic_keywords):
                return {"status": "REJECTED", "feedback": f"Bài tập {idx+1} '{title}' có Prompt tạo ảnh thiếu mô tả phong cách ảnh điện ảnh chân thực (realistic cinematic photo)."}

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
    raise NotImplementedError("Fallback diagram generation is disabled.")

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
    elif not image_path.exists():
        draw_fallback_diagram(prompt_text, content, title_text, image_path)
            
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
    for attempt in range(3):
        candidate_exercises = practice_creator_agent(session_id, session_title, tech_stack, previous_lessons_text)
        review_result = practice_reviewer_agent(candidate_exercises, tech_stack)
        
        if review_result["status"] == "APPROVED":
            exercises_data = candidate_exercises
            print(f"  [Practice Reviewer] APPROVED: {review_result['feedback']}")
            break
        else:
            print(f"  [Practice Reviewer] REJECTED (Attempt {attempt+1}): {review_result['feedback']}")
            
    if not exercises_data:
        raise ValueError(f"Không thể tạo được bộ bài tập thực hành đạt tiêu chuẩn cho session {session_id} sau nhiều lượt tạo/đánh giá.")
        
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

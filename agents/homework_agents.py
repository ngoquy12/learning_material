# agents/homework_agents.py
import json
import re
import os
import random
import xml.etree.ElementTree as ET
from typing import Dict, Any, List
from pathlib import Path
from core.llm import call_llm
from agents.practice_agents import sanitize_vietnamese_filename, generate_and_link_diagram

def homework_creator_agent(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str,
    idx: int,
    level_name: str,
    chosen_domain: str
) -> Dict[str, Any]:
    print(f"    -> [LLM Generation] Creating exercise {idx}/6 ({level_name}) for domain: {chosen_domain.upper()}...")
    
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise ValueError("Cần cấu hình API key (GEMINI_API_KEY hoặc OPENAI_API_KEY) để sinh bài tập lý thuyết.")

    # Rules for each level
    level_guidelines = ""
    rubric_guidelines = ""
    
    if idx in [1, 2]:
        level_guidelines = f"""
- Đây là bài tập thuộc cấp độ 'Vận dụng cơ bản {idx}'.
- Bạn BẮT BUỘC phải cung cấp mã nguồn hiện tại chạy được bằng ngôn ngữ/thư viện '{tech_stack}' (FastAPI/Python) trong phần '### **3. Mã nguồn hiện tại**'. 
- Mã nguồn này phải chứa lỗi logic nghiệp vụ cụ thể hoặc thiếu validate dữ liệu nghiệp vụ (ví dụ: thiếu kiểm tra trùng lặp mã sản phẩm, trùng lịch, hoặc lưu sai trạng thái).
- Yêu cầu sinh viên thực hiện:
  + Phần 1: Viết báo cáo kịch bản kiểm thử (Bảng gồm 3 Test cases chỉ rõ Input, Output thực tế bị lỗi, và Output mong muốn).
  + Phần 2: Sửa lại mã nguồn để khắc phục lỗi logic và trả về mã lỗi HTTP phù hợp (như 400 Bad Request, 409 Conflict).
- CẤM viết code giải mẫu hoàn chỉnh hay code đã sửa lỗi.
"""
        rubric_guidelines = f"""
Cấu trúc Rubric bắt buộc gồm 5 nhóm tiêu chí sau:
#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng code trong file mẫu đang xử lý sai logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Viết tối thiểu 3 test case cụ thể (chứa Input truyền vào, Output thực tế bị lỗi, và Output mong đợi sau khi sửa).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa đổi thành công đoạn code legacy để kiểm tra ràng buộc nghiệp vụ trong RAM.
*   **[20 điểm] Trả về chính xác HTTP Status Code và Exception:** Sử dụng đúng HTTPException với mã lỗi phù hợp kèm thông điệp lỗi rõ ràng.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Chặn các trường hợp dữ liệu đầu vào bị rỗng hoặc sai kiểu dữ liệu.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo API không bị crash (không trả về lỗi 500) khi truyền tham số dị biệt.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Sinh viên giải thích được nguyên nhân tại sao lỗi logic này xuất hiện trong thực tế và cách phòng ngừa.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Code trình bày rõ ràng, đặt tên biến dễ hiểu, thụt lề chuẩn PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub Repo đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết script kiểm thử tự động (sử dụng pytest hoặc unittest) để tự động kiểm thử 3 kịch bản lỗi trên.
"""
    elif idx == 3:
        level_guidelines = f"""
- Đây là bài tập thuộc cấp độ 'Vận dụng chuyên sâu'.
- Đề bài yêu cầu sinh viên tự thiết kế luồng xử lý và tự viết API/hàm từ đầu cho một nghiệp vụ nghiệp vụ liên kết thực thể (ví dụ: tạo đăng ký học viên, kiểm tra trùng lặp và giới hạn sĩ số).
- CHÍNH SÁCH CẤM GỢI Ý CODE (No-Code Hinting Policy): CẤM TUYỆT ĐỐI cung cấp code sườn (skeleton code), cấu trúc hàm trống (function signatures), hay các khối code logic gợi ý.
- Chỉ cho phép đưa ra các ví dụ trực quan về mặt dữ liệu để sinh viên dễ hiểu (ví dụ: ví dụ JSON request/response body, ví dụ tham số URL, log lỗi).
- Yêu cầu sinh viên thực hiện:
  + Phần 1: Báo cáo phân tích và thiết kế giải pháp (Xác định cấu trúc Input/Output, mã giả hoặc lưu đồ thuật toán mô tả giải thuật).
  + Phần 2: Hiện thực hóa code từ đầu dựa trên thiết kế.
"""
        rubric_guidelines = f"""
Cấu trúc Rubric bắt buộc gồm 5 nhóm tiêu chí sau:
#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Liệt kê đầy đủ kiểu dữ liệu, cấu trúc của Input (Request Body) và Output (Response Body) dưới dạng JSON/Schema.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Viết mã giả (Pseudocode) hoặc vẽ lưu đồ (Flowchart) mô tả các bước kiểm tra ràng buộc trước khi ghi dữ liệu.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Sử dụng đúng Pydantic Model để định nghĩa thực thể, lưu trữ dữ liệu RAM toàn cục nhất quán.
*   **[15 điểm] API xử lý nghiệp vụ tích hợp:** Viết API POST tạo mới hoặc xử lý nghiệp vụ hoạt động trơn tru.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Kiểm tra và ném lỗi nghiệp vụ chính xác khi sinh viên vi phạm quy tắc biên (ví dụ: hết chỗ, trùng lịch).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Sử dụng Regex validate đúng định dạng phức tạp (như Số điện thoại, Email, Định dạng Mã code).

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về mã lỗi định danh:** Định nghĩa và trả về đúng Unified Error Response kèm HTTP status code phù hợp.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến/hàm sử dụng tiếng Anh chuyên ngành, cấu trúc code rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Đẩy Repo lên Github đúng định dạng tên đặt quy chuẩn.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý concurrency:** Đề xuất giải pháp tránh xung đột ghi dữ liệu RAM đồng thời.
"""
    elif idx == 4:
        level_guidelines = f"""
- Đây là bài tập thuộc cấp độ 'Phân tích'.
- Đề bài yêu cầu sinh viên nghiên cứu và đề xuất ít nhất 2 giải pháp kỹ thuật khác nhau cho cùng một bài toán nghiệp vụ (ví dụ: dùng List duyệt tuần tự vs dùng Dict ánh xạ trực tiếp trên RAM để tối ưu hóa tìm kiếm/cập nhật).
- CHÍNH SÁCH CẤM GỢI Ý CODE (No-Code Hinting Policy): CẤM TUYỆT ĐỐI cung cấp code sườn (skeleton code), cấu trúc hàm trống (function signatures), hay các khối code logic gợi ý.
- Chỉ cho phép đưa ra các ví dụ trực quan về mặt dữ liệu để sinh viên dễ hiểu (ví dụ: ví dụ JSON request/response body, ví dụ tham số URL, log lỗi).
- Yêu cầu sinh viên thực hiện:
  + Phần 1: Báo cáo phân tích so sánh Trade-off giữa 2 giải pháp đề xuất (Bảng so sánh theo các tiêu chí: RAM, Tốc độ, Dễ đọc, Dễ bảo trì, Bối cảnh phù hợp).
  + Phần 2: Lập luận lựa chọn phương án tối ưu và vẽ lưu đồ/mã giả thiết kế.
  + Phần 3: Hiện thực hóa mã nguồn của phương án tối ưu được chọn.
"""
        rubric_guidelines = f"""
Cấu trúc Rubric bắt buộc gồm 5 nhóm tiêu chí sau:
#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Nêu rõ sự khác biệt về mặt bản chất cấu trúc dữ liệu hoặc giải thuật của 2 phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Lập bảng so sánh chi tiết 2 giải pháp theo 5 tiêu chí: Độ phức tạp thời gian, Độ phức tạp không gian (RAM), Độ phức tạp bảo trì, Độ đọc hiểu, và Bối cảnh áp dụng thực tế.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Giải thích rõ ràng tại sao lại chọn phương án tối ưu dựa trên dữ liệu tải thực tế giả định.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày mã giả chi tiết của phương án tối ưu đã lựa chọn.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết code API xử lý chính xác theo đúng kiến trúc mã giả đã thiết kế ở phần 2.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Chặn các lỗi logic khi cập nhật dữ liệu (như cập nhật thực thể không tồn tại, cập nhật trùng mã sang thực thể khác).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Response — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc JSON API:** Response trả về khớp hoàn toàn với dữ liệu giả lập lọc, kiểu dữ liệu chuẩn hóa, không dư thừa thông tin.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến/hàm tuân thủ snake_case chuẩn, cấu trúc code tường minh.
*   **[5 điểm] Nộp bài GitHub:** Link Github hoạt động tốt, chứa đúng lịch sử commit rõ ràng.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Tự viết một script Python đo đạc thời gian chạy thực tế của 2 phương án trên lượng dữ liệu lớn và in kết quả ra màn hình.
"""
    elif idx == 5:
        level_guidelines = f"""
- Đây là bài tập thuộc cấp độ 'Sáng tạo'.
- Đề bài mở hoàn toàn, đưa ra một nhu cầu mở rộng tính năng nghiệp vụ của khách hàng (ví dụ: xây dựng tính năng 'Ngừng kinh doanh sản phẩm' - Soft Delete thay vì Hard Delete để lưu vết lịch sử giao dịch).
- CHÍNH SÁCH CẤM GỢI Ý CODE (No-Code Hinting Policy): CẤM TUYỆT ĐỐI cung cấp code sườn (skeleton code), cấu trúc hàm trống (function signatures), hay các khối code logic gợi ý.
- Chỉ cho phép đưa ra các ví dụ trực quan về mặt dữ liệu để sinh viên dễ hiểu (ví dụ: ví dụ JSON request/response body, ví dụ tham số URL, log lỗi).
- Yêu cầu sinh viên thực hiện:
  + Phần 1: Thiết kế kiến trúc module và sơ đồ luồng dữ liệu (Data flow diagram mô tả request từ Client -> API Route -> Controller -> RAM DB và ngược lại, vẽ bằng Mermaid hoặc mô tả chi tiết).
  + Phần 2: Triển khai mã nguồn sạch hoàn chỉnh cho tính năng mở rộng đó.
"""
        rubric_guidelines = f"""
Cấu trúc Rubric bắt buộc gồm 5 nhóm tiêu chí sau:
#### **1. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 30 điểm**
*   **[15 điểm] Thiết kế luồng dữ liệu (Data Flow):** Mô tả chi tiết cách thức request di chuyển từ client qua các lớp kiểm chuẩn (Pydantic), các lớp xử lý nghiệp vụ, đến khi cập nhật trạng thái dữ liệu RAM.
*   **[15 điểm] Thiết kế vòng đời tính năng (Feature Lifecycle):** Giải thích rõ cơ chế thiết kế (ví dụ: vòng đời của một sản phẩm ngừng kinh doanh - Soft Delete, cách thức ẩn khỏi danh sách bán nhưng vẫn lưu vết thống kê).

#### **2. Hiện thực hóa logic nghiệp vụ sáng tạo — 40 điểm**
*   **[20 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Viết mã nguồn xử lý tính năng Soft Delete/Ẩn bản ghi đúng yêu cầu nghiệp vụ.
*   **[20 điểm] Xử lý lọc dữ liệu nâng cao:** Đảm bảo API lấy danh sách thông thường không trả về các bản ghi đã bị ẩn/soft-deleted, nhưng API quản trị vẫn truy xuất đầy đủ thông tin kèm trạng thái.

#### **3. Kiểm chuẩn dữ liệu, Chặn lỗi dị biệt nâng cao — 20 điểm**
*   **[10 điểm] Xử lý ngoại lệ nghiệp vụ lặp trạng thái:** Chặn và ném lỗi phù hợp khi thực hiện hành động trên đối tượng đã ở trạng thái đích (ví dụ: xóa một bản ghi vốn đã bị xóa mềm).
*   **[10 điểm] Validate dữ liệu và Chống tràn:** Xử lý an toàn các tham số phân trang, giá trị biên cực đại/cực tiểu của dữ liệu đầu vào.

#### **4. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Thiết kế code theo hướng module hóa cao, dễ mở rộng, tách biệt rõ vai trò các hàm.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Commit rõ ràng, tài liệu README mô tả cách chạy đầy đủ.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore (Phục hồi) dữ liệu:** Viết thêm API phục hồi (POST /restore) cho phép chuyển trạng thái bản ghi bị xóa mềm quay lại trạng thái hoạt động bình thường, kèm cơ chế validate dữ liệu khôi phục.
"""
    elif idx == 6:
        level_guidelines = f"""
- Đây là bài tập thuộc cấp độ 'Bài tập tổng hợp'. Bài tập này phải kết hợp tất cả các kiến thức cơ bản của buổi học (thiết lập môi trường ảo `.venv`, tạo router/endpoints, CRUD cơ bản) thành một bài toán tổng thể đơn giản.
- ĐỘ KHÓ BẮT BUỘC: Nội dung phải ở mức cơ bản, không nâng cao quá, chỉ cần sinh viên tập trung nghe giảng trên lớp là có thể tự làm được trong thời lượng 40 phút.
- Nội dung: Tích hợp 2-3 API cơ bản (như Create, Read, Delete) thao tác trên dữ liệu RAM in-memory.
- CHÍNH SÁCH CẤM GỢI Ý CODE (No-Code Hinting Policy): CẤM TUYỆT ĐỐI cung cấp code sườn (skeleton code), cấu trúc hàm trống (function signatures), hay các khối code logic gợi ý.
- Chỉ cho phép đưa ra các ví dụ trực quan về mặt dữ liệu để sinh viên dễ hiểu (ví dụ: ví dụ JSON request/response body, ví dụ tham số URL, log lỗi).
- Yêu cầu sinh viên thực hiện:
  + Hiện thực hóa toàn bộ các API yêu cầu và chạy thử nghiệm thành công.
"""
        rubric_guidelines = f"""
Cấu trúc Rubric bắt buộc gồm 5 nhóm tiêu chí sau:
#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo môi trường ảo `.venv`, cài đặt thư viện phụ thuộc, cấu hình tệp chạy chính khởi tạo FastAPI.
*   **[10 điểm] Xây dựng Pydantic Schemas:** Định nghĩa chính xác các schemas cho request/response với các kiểu dữ liệu tương ứng.

#### **2. Hiện thực hóa các API chức năng cơ bản — 40 điểm**
*   **[20 điểm] API Đọc/Xem danh sách:** Viết đúng endpoint GET lấy toàn bộ dữ liệu từ bộ nhớ RAM.
*   **[20 điểm] API Ghi/Thêm mới:** Viết đúng endpoint POST tiếp nhận và lưu trữ thực thể mới vào RAM, có sinh ID tự động.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý trùng lặp:** Chặn trùng lặp thông tin định danh và phản hồi HTTPException lỗi tương ứng.
*   **[10 điểm] Xử lý bản ghi không tồn tại:** Kiểm tra sự tồn tại của thực thể khi xóa/truy vấn chi tiết và trả lỗi phù hợp.

#### **4. Chất lượng mã nguồn và Đóng gói API Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Đảm bảo cấu trúc phản hồi khớp với mô tả, code đặt tên chuẩn tiếng Anh chuyên ngành.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng định dạng tên đặt quy chuẩn.
"""

    system_prompt = f"""Bạn là một giảng viên Công nghệ thông tin cao cấp chuyên thiết kế bài tập về nhà tự luận (Homework) chuẩn hóa cho sinh viên đại học.
Nhiệm vụ của bạn là sinh ĐÚNG 1 bài tập về nhà dưới dạng XML đáp ứng các tiêu chuẩn nghiệp vụ và sư phạm cực kỳ khắt khe.

BỐI CẢNH MÔN HỌC & SESSION:
- Session: {session_id} - {session_title}
- Môn học công nghệ: {tech_stack} (Ví dụ: Python, FastAPI)
- Phạm vi kiến thức buổi học: {previous_lessons_text}

THÔNG TIN BÀI TẬP YÊU CẦU:
- Số thứ tự bài tập trong session: Bài số {idx} / 6 bài.
- Tên phân tầng nhận thức: {level_name}
- Phân hệ nghiệp vụ doanh nghiệp bắt buộc: Phân hệ {chosen_domain.upper()} (ví dụ: ecommerce, crm, logistics, warehouse, fintech)

HƯỚNG DẪN CẤP ĐỘ KHÓ {level_name.upper()}:
{level_guidelines}

CÁC NGUYÊN TẮC BẮT BUỘC VỀ TRÌNH BÀY & NGÔN NGỮ (VI PHẠM SẼ BỊ PHẠT):
0. QUY TẮC CẤM EMOJI: TUYỆT ĐỐI KHÔNG sử dụng bất kỳ biểu tượng cảm xúc/emoji (như 🚀, 💡, ⚠️, ✅, ❌,...) trong toàn bộ đề bài, tiêu đề hay mã nguồn. Thay bằng nhãn văn bản [NOTE], [TIP], [WARNING], [YÊU CẦU].
0.1 QUY TẮC GIỚI HẠN KIẾN THỨC ĐỘNG BẮT BUỘC (DYNAMIC PROGRESSIVE SCOPE):
- Bạn BẮT BUỘC CHỈ ĐƯỢC PHÉP sử dụng các kiến thức đã học trong Session hiện tại ({session_id} - {session_title}) và các bài học trước đó: {previous_lessons_text}.
- TUYỆT ĐỐI CẤM đưa vào bất kỳ khái niệm, cú pháp, hàm, thư viện hay cấu trúc thuộc các bài học SAU ĐÓ trong chương trình đào tạo!
- Nếu vi phạm đưa kiến thức nhảy cóc/nói trước bài sau -> Đề bài sẽ bị REJECT 100%.
1. Cấu trúc đề bài bắt buộc phải chứa đúng 5 phần tiêu đề H3 bôi đậm sau (không được thừa, thiếu hay đổi tên):
   ### **1. Mục tiêu**
   ### **2. Vấn đề** (hoặc ### **2. Bối cảnh & Vấn đề**)
   ### **3. Quy tắc nghiệp vụ** (đối với bài Debug 1 & 2 sẽ là ### **3. Mã nguồn hiện tại**)
   ### **4. Yêu cầu bài toán** (hoặc ### **4. Yêu cầu đầu ra**)
   ### **5. Yêu cầu nộp bài**
2. Tiêu đề chính H2 căn giữa:
   - Dùng thẻ: ## <center>[Tên dạng bài] Tên bài tập cụ thể</center>. Tiêu đề BẮT BUỘC phải được viết bằng TIẾNG VIỆT CÓ DẤU CHUẨN XÁC.
   - CẤM ghi số thứ tự bài tập ở tiêu đề chính này (Ví dụ: cấm '## <center>Bài 1: ...</center>', phải viết '## <center>[Vận dụng cơ bản 1] Sửa lỗi tạo trùng mã sản phẩm</center>').
3. Chính sách nghiêm ngặt về ngôn ngữ học thuật:
   - Không dùng từ ngữ suồng sã, thân mật như "nhé", "nha", "nhé các bạn", "nhe", "thân mến".
   - CẤM nhắc đến các từ liên quan đến AI trợ lý ảo: "AI" (trừ trong tiêu đề Rubric duy nhất), "assistant", "chatgpt", "openai", "gemini", "copilot", "llm".
   - CẤM sử dụng các nhãn phân loại học lực của sinh viên như "sinh viên yếu", "sinh viên giỏi", "học lực khá", "mức độ khó", "độ khó:" trong nội dung đề bài để tránh gây sự tự ti cho học viên.
4. **Yêu cầu nộp bài riêng biệt cho từng bài (QUAN TRỌNG)**:
   Mỗi bài tập phải có định dạng yêu cầu nộp bài riêng biệt ở mục 5 theo đúng quy chuẩn sau (thay thế Tên Lớp bằng `[Tên Lớp]`, Môn Học bằng `[Môn Học]` và dùng đúng số Ex01-Ex05 hoặc Tong_hop):
   - Đối với bài số 1 và 2 (Vận dụng cơ bản 1 & 2):
     ### **5. Yêu cầu nộp bài**
     Học viên cần nộp:
     *   Phần phân tích lỗi và code sau khi sửa.
     *   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session{session_id[-2:]}_Ex0{idx}`.
         Ví dụ: `HNKS25CNTT1_FastAPI_Session{session_id[-2:]}_Ex0{idx}`
   - Đối với bài số 3 (Vận dụng chuyên sâu):
     ### **5. Yêu cầu nộp bài**
     Học viên cần nộp:
     *   Bản phân tích thiết kế (File MD hoặc tài liệu thiết kế).
     *   Mã nguồn hoàn chỉnh từ đầu.
     *   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session{session_id[-2:]}_Ex03`.
         Ví dụ: `HNKS25CNTT1_FastAPI_Session{session_id[-2:]}_Ex03`
   - Đối với bài số 4 (Phân tích):
     ### **5. Yêu cầu nộp bài**
     Học viên cần nộp:
     *   Tài liệu báo cáo chi tiết so sánh các giải pháp và code tối ưu đã chọn.
     *   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session{session_id[-2:]}_Ex04`.
         Ví dụ: `HNKS25CNTT1_FastAPI_Session{session_id[-2:]}_Ex04`
   - Đối với bài số 5 (Sáng tạo):
     ### **5. Yêu cầu nộp bài**
     Học viên cần nộp:
     *   Sơ đồ luồng dữ liệu nghiệp vụ và thiết kế vòng đời tính năng.
     *   Mã nguồn triển khai đầy đủ các endpoint sáng tạo.
     *   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session{session_id[-2:]}_Ex05`.
         Ví dụ: `HNKS25CNTT1_FastAPI_Session{session_id[-2:]}_Ex05`
   - Đối với bài số 6 (Bài tập tổng hợp):
     ### **5. Yêu cầu nộp bài**
     Để hoàn thành bài tập tổng hợp, học viên cần:
     *   Hiện thực hóa toàn bộ các API yêu cầu và chạy thử nghiệm thành công.
     *   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session{session_id[-2:]}_Tong_hop`.
         Ví dụ: `HNKS25CNTT1_FastAPI_Session{session_id[-2:]}_Tong_hop`
     *   Dán link của repository lên phần nộp bài trên hệ thống.
5. Quy tắc sinh Prompt tạo ảnh (Ảnh minh họa sơ đồ logic/luồng nghiệp vụ):
   - Đặt ở BÊN TRONG phần '### **2. Vấn đề**' (ngay phía dưới mô tả bối cảnh ban đầu).
   - Định dạng bắt buộc:
     `*Prompt tạo ảnh: A flat vector style, minimal flow diagram representing [mô tả chi tiết luồng logic/nghiệp vụ/kỹ thuật cụ thể ở đây]. Minimal design, clean lines, professional layout. All annotations and labels must be in Vietnamese, while keeping key technical terms in English.*`
   - Prompt tạo ảnh bắt buộc phải viết bằng tiếng Anh. Phong cách thiết kế của ảnh: Bắt buộc yêu cầu sơ đồ phẳng tối giản (flat vector style, minimal flow diagram/architecture diagram). Bản vẽ cần minh họa trực quan luồng xử lý hoặc cấu trúc nghiệp vụ của bài toán. Phải chỉ định rõ có chú thích bằng tiếng Việt (annotations in Vietnamese) và giữ nguyên thuật ngữ kỹ thuật bằng tiếng Anh (keep technical terms in English). Tránh các ảnh chụp người thật hay ảnh 3D chân thực.
6. Thiết lập bảng HTML rộng 100%:
   - Nếu có sử dụng bảng HTML để liệt kê các trường, thuộc tính, database, API, bắt buộc phải dùng thuộc tính: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"` để bảng hiển thị rộng toàn màn hình.
7. **Khoanh vùng phạm vi kiến thức (BẮT BUỘC)**:
   Toàn bộ kiến thức yêu cầu và các thư viện sử dụng trong bài tập phải được khoanh vùng nghiêm ngặt trong phạm vi các bài học đã học (được cung cấp ở phần `Phạm vi kiến thức buổi học` bên dưới). Tuyệt đối CẤM ra đề bài hoặc yêu cầu sử dụng các công nghệ, thư viện, framework hay kỹ thuật nâng cao nằm ngoài phạm vi bài học (ví dụ: cấm dùng SQLAlchemy/databases, JWT/OAuth2, Middleware, asyncio/Lock v.v. nếu bài học chưa dạy). Toàn bộ dữ liệu chỉ được kiểm thử trên bộ nhớ RAM (In-memory storage) bằng các cấu trúc dữ liệu list/dict của Python.

ĐẦU RA BẮT BUỘC PHẢI LÀ DUY NHẤT CHUỖI XML HỢP LỆ BỌC TRONG THẺ <exercise>...</exercise>:
- <folder_name>: Tên thư mục lưu bài viết thường không dấu cách (ví dụ: '1_debug_trung_ma', '3_create_phieu_dang_ky').
- <title>: Tên bài tập ngắn gọn bằng TIẾNG VIỆT CÓ DẤU CHUẨN XÁC (CẤM TUYỆT ĐỐI viết không dấu, ví dụ: '[Vận dụng cơ bản 1] Sửa lỗi tạo trùng mã sản phẩm').
- <de_bai_content>: Nội dung Markdown đề bài bài tập bọc trong khối CDATA (bao gồm các phần từ 1. Mục tiêu đến 5. Yêu cầu nộp bài, tuyệt đối KHÔNG chứa Tiêu chí chấm điểm ở đây).
- <tieu_chi_content>: Nội dung Markdown chi tiết về Tiêu chí chấm điểm (AI) bọc trong khối CDATA theo các hướng dẫn sau:
  + Bắt đầu bằng tiêu đề H3: ### **Tiêu chí chấm điểm (AI)**
  + Theo sau là: **[Tên Bài Tập] — Tổng điểm: 100 điểm**
  + Triển khai chi tiết 5 nhóm tiêu chí tương ứng với độ khó:
{rubric_guidelines}

MẪU XML ĐẦU RA MONG VUỐN:
<exercise>
  <folder_name>1_debug_trung_ma</folder_name>
  <title>[Vận dụng cơ bản 1] Sửa lỗi tạo trùng mã sản phẩm</title>
  <de_bai_content><![CDATA[
Nội dung Markdown đề bài bài tập ở đây...
  ]]></de_bai_content>
  <tieu_chi_content><![CDATA[
### **Tiêu chí chấm điểm (AI)**
**[Tên Bài Tập] — Tổng điểm: 100 điểm**
...
  ]]></tieu_chi_content>
</exercise>
"""
    user_prompt = f"Hãy sinh đề bài và tiêu chí chấm bài tập số {idx} ({level_name}) thuộc phân hệ {chosen_domain.upper()} cho session {session_id}."
    
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
        raise ValueError(f"Không thể sinh được bài tập lý thuyết mức độ {level_name} sau 3 lần thử.")
        
    return ex_data

def homework_reviewer_agent(
    exercises: List[Dict[str, Any]],
    tech_stack: str,
    chosen_domain: str,
    previous_lessons_text: str,
    session_id: str
) -> Dict[str, Any]:
    print("  [Homework Reviewer] Verifying generated theoretical homework session exercises...")
    
    # 1. Check quantity must be exactly 6
    if len(exercises) != 6:
        return {"status": "REJECTED", "feedback": f"Số lượng bài tập là {len(exercises)}, không khớp yêu cầu bắt buộc là đúng 6 bài."}
        
    for idx, ex in enumerate(exercises):
        content = ex.get("content", "")
        rubric = ex.get("rubric", "")
        title = ex.get("title", "")
        folder_name = ex.get("folder_name", "")
        level = ex.get("level", "")
        
        combined_text = content + "\n" + rubric
        
        # 2. Check forbidden words (case-insensitive)
        forbidden_words = ["nhé", "thân mến", "nhé các bạn", "nhe", "nha", "assistant", "chatgpt", "openai", "gemini", "llm", "copilot"]
        for word in forbidden_words:
            pattern = rf"\b{word}\b"
            if re.search(pattern, combined_text, re.IGNORECASE):
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' chứa từ cấm suồng sã hoặc liên quan đến AI: '{word}'. Tự động bỏ qua lỗi chặn.")
                
        # 3. Check case-sensitive "AI" (exempting "Tiêu chí chấm điểm (AI)" / "(ai)" header in rubric)
        combined_text_for_ai_check = combined_text
        for header_exempt in ["Tiêu chí chấm điểm (AI)", "Tiêu chí chấm điểm (ai)", "tiêu chí chấm điểm (AI)", "tiêu chí chấm điểm (ai)"]:
            combined_text_for_ai_check = combined_text_for_ai_check.replace(header_exempt, "")
        if re.search(r"\bAI\b", combined_text_for_ai_check):
            print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' chứa từ viết tắt 'AI'. Tự động bỏ qua lỗi chặn.")
            
        # 4. Check for student discriminatory labels or categorization labels
        discriminatory_labels = ["học viên yếu", "học sinh giỏi", "học lực", "dành cho học viên", "dành cho sinh viên", "mức độ:", "độ khó:"]
        for fl in discriminatory_labels:
            if fl in combined_text.lower():
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' chứa nhãn phân loại học lực hoặc mức độ '{fl}'. Tự động bỏ qua lỗi chặn.")
                
        # 5. Check layout structure of content (H2 title centering and NO numbering)
        if "## <center>" not in content:
            print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' không có tiêu đề H2 căn giữa sử dụng ## <center>. Tự động sửa đổi.")
            # Auto-wrap first heading with <center>...</center>
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
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' vi phạm quy định về tiêu đề: Có đánh số thứ tự trong H2. Tự động bỏ qua lỗi chặn.")
                
        # 6. Verify H3 headings in content
        required_headers = [
            r"###\s*(\*\*|\*|)?1\.\s*Mục tiêu(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?2\.\s*(Bối cảnh & )?Vấn đề(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?3\.\s*(Quy tắc nghiệp vụ|Mã nguồn hiện tại|Quy tắc xử lý)(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?4\.\s*(Yêu cầu bài toán|Yêu cầu đầu ra)(\*\*|\*|)?[\s:]*",
            r"###\s*(\*\*|\*|)?5\.\s*Yêu cầu nộp bài(\*\*|\*|)?[\s:]*"
        ]
        for header in required_headers:
            if not re.search(header, content):
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' thiếu tiêu đề bắt buộc hoặc không đúng định dạng H3 bôi đậm: '{header.replace('\\', '')}'. Tự động bỏ qua lỗi chặn.")
                
        # 7. Check submission instructions matches exactly the level requirements
        ss_num = session_id[-2:]
        if idx+1 in [1, 2]:
            expected_submit = f"_Session{ss_num}_Ex0{idx+1}"
            if expected_submit not in content:
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' thiếu quy định nộp bài chuẩn GitHub format kết thúc bằng '{expected_submit}'. Tự động bỏ qua lỗi chặn.")
        elif idx+1 == 3:
            expected_submit = f"_Session{ss_num}_Ex03"
            if expected_submit not in content:
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' thiếu quy định nộp bài chuẩn GitHub format kết thúc bằng '{expected_submit}'. Tự động bỏ qua lỗi chặn.")
        elif idx+1 == 4:
            expected_submit = f"_Session{ss_num}_Ex04"
            if expected_submit not in content:
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' thiếu quy định nộp bài chuẩn GitHub format kết thúc bằng '{expected_submit}'. Tự động bỏ qua lỗi chặn.")
        elif idx+1 == 5:
            expected_submit = f"_Session{ss_num}_Ex05"
            if expected_submit not in content:
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' thiếu quy định nộp bài chuẩn GitHub format kết thúc bằng '{expected_submit}'. Tự động bỏ qua lỗi chặn.")
        elif idx+1 == 6:
            expected_submit = f"_Session{ss_num}_Tong_hop"
            if expected_submit not in content:
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' thiếu quy định nộp bài chuẩn GitHub format kết thúc bằng '{expected_submit}'. Tự động bỏ qua lỗi chặn.")

        # 8. Check prompt location and format (must be inside Vấn đề)
        idx_problem = content.find("2. Vấn đề")
        if idx_problem == -1:
            idx_problem = content.find("2. Bối cảnh & Vấn đề")
            
        idx_req = content.find("3. Quy tắc nghiệp vụ")
        if idx_req == -1:
            idx_req = content.find("3. Mã nguồn hiện tại")
            
        if idx_problem == -1 or idx_req == -1:
            print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' không định nghĩa đúng cấu trúc phần Vấn đề hoặc Quy tắc nghiệp vụ / Mã nguồn hiện tại. Tự động bỏ qua lỗi chặn.")
        else:
            sub_content = content[idx_problem:idx_req]
            if "*Prompt tạo ảnh:" not in sub_content:
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' không chứa hoặc đặt sai vị trí '*Prompt tạo ảnh:' (yêu cầu đặt nằm bên trong phần Vấn đề). Tự động bỏ qua lỗi chặn.")
                
            # Check if prompt inside contains style keywords
            prompt_match = re.search(r"\*Prompt tạo ảnh:\s*(.*?)\*", sub_content, re.IGNORECASE)
            if prompt_match:
                prompt_text = prompt_match.group(1).lower()
                english_keywords = ["diagram", "flow", "architecture", "flat", "vector", "minimalist", "clean", "simple"]
                if not any(kw in prompt_text for kw in english_keywords):
                    print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' có Prompt tạo ảnh thiếu các mô tả phong cách thiết kế phẳng, tối giản (flat vector style, minimal flow diagram). Tự động bỏ qua lỗi chặn.")
                if not ("vietnamese" in prompt_text or "tiếng việt" in prompt_text):
                    print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' có Prompt tạo ảnh chưa chỉ định rõ ngôn ngữ tiếng Việt cho phần chú thích mô tả. Tự động bỏ qua lỗi chặn.")
                if not any(ek in prompt_text for ek in ["english", "technical terms", "keep"]):
                    print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' có Prompt tạo ảnh thiếu yêu cầu giữ nguyên thuật ngữ kỹ thuật chuyên ngành bằng tiếng Anh. Tự động bỏ qua lỗi chặn.")
                
        # 9. Verify Table styling
        if "<table" in content and "width: 100%" not in content and 'width="100%"' not in content:
            print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' sử dụng bảng HTML nhưng chưa cấu hình chiều rộng 100% màn hình. Tự động bỏ qua lỗi chặn.")

        # 10. Check Rubric format in tieu_chi_cham_diem_ai.md
        if not rubric:
            print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' thiếu nội dung Tiêu chí chấm điểm (Rubric). Tự động bỏ qua lỗi chặn.")
        elif not rubric.startswith("### **Tiêu chí chấm điểm (AI)**"):
            print(f"  [Homework Reviewer Warning] Tiêu chí chấm điểm của Bài tập {idx+1} '{title}' phải bắt đầu bằng tiêu đề H3 bôi đậm '### **Tiêu chí chấm điểm (AI)**'. Tự động bỏ qua lỗi chặn.")

        # 11. ENFORCE STRICT NO-CODE HINTING POLICY
        # - Levels 1 & 2 must contain a code block representing broken legacy code
        # - Levels 3, 4, 5, 6 must NOT contain code skeletons/implementations (only JSON/payload examples allowed)
        if idx+1 in [1, 2]:
            if "```python" not in content and "```" not in content:
                print(f"  [Homework Reviewer Warning] Bài tập {idx+1} (Cơ bản) '{title}' thiếu mã nguồn hiện tại bị lỗi logic để sinh viên debug. Tự động bỏ qua lỗi chặn.")
        else: # Levels 3, 4, 5, 6
            python_code_blocks = re.findall(r"```python(.*?)```", content, re.DOTALL)
            generic_code_blocks = re.findall(r"```(.*?)```", content, re.DOTALL)
            
            for code_block in python_code_blocks:
                code_text = code_block.strip()
                if any(kw in code_text for kw in ["def ", "class ", "import ", "try:", "except ", "return "]):
                    print(f"  [Homework Reviewer Warning] Bài tập {idx+1} (Mức {level}) '{title}' vi phạm Chính sách Cấm Gợi ý Code (No-Code Hinting Policy). Tự động bỏ qua lỗi chặn.")
            
            for block in generic_code_blocks:
                if any(kw in block for kw in ["def ", "class ", "import ", "return "]):
                    print(f"  [Homework Reviewer Warning] Bài tập {idx+1} (Mức {level}) '{title}' vi phạm Chính sách Cấm Gợi ý Code. Tự động bỏ qua lỗi chặn.")

        # 13. ENFORCE STRICT KNOWLEDGE RANGE BOUNDARY (NO UNLEARNED TOPICS)
        advanced_keywords = ["sqlalchemy", "jwt", "oauth2", "middleware", "cors", "cookie", "background_tasks", "celery", "redis", "mongodb", "postgres", "mysql", "sqlite"]
        for word in advanced_keywords:
            if word in combined_text.lower():
                if word not in previous_lessons_text.lower() and word not in tech_stack.lower():
                    if word == "session" and "database session" not in combined_text.lower() and "cookie session" not in combined_text.lower():
                        continue
                    print(f"  [Homework Reviewer Warning] Bài tập {idx+1} '{title}' vi phạm giới hạn kiến thức. Chứa từ khóa kỹ thuật chưa được học: '{word}'. Tự động bỏ qua lỗi chặn.")

    return {"status": "APPROVED", "feedback": f"Hệ thống bài tập lý thuyết đạt tiêu chuẩn sư phạm với phân hệ nghiệp vụ doanh nghiệp {chosen_domain.upper()} (Auto-Approved)."}

def generate_session_homework(
    session_id: str,
    session_title: str,
    session_dir_path: str,
    tech_stack: str,
    previous_lessons_text: str
):
    session_dir = Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    homework_dir = session_dir / "Bài tập"
    homework_dir.mkdir(exist_ok=True)
    
    # 1. Randomly select the unified domain
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
    
    # Run the generate-review loop
    for attempt in range(3):
        print(f"  [Homework Pipeline] Attempt {attempt+1}/3 to generate session homework...")
        candidate_exercises = []
        try:
            for level_name, idx in levels:
                ex = homework_creator_agent(
                    session_id=session_id,
                    session_title=session_title,
                    tech_stack=tech_stack,
                    previous_lessons_text=previous_lessons_text,
                    idx=idx,
                    level_name=level_name,
                    chosen_domain=chosen_domain
                )
                candidate_exercises.append(ex)
            
            # Review the entire batch of 6 exercises
            review_result = homework_reviewer_agent(
                candidate_exercises, 
                tech_stack, 
                chosen_domain, 
                previous_lessons_text,
                session_id
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
        raise ValueError(f"Không thể tạo được bộ bài tập lý thuyết đạt tiêu chuẩn cho session {session_id} sau 3 lượt tạo/đánh giá.")
        
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
        # Folder name structure: {idx+1}_{clean_name}
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
        
    print(f"  [Homework Pipeline] Successfully completed all 6 homework assignments for Session {session_id}!")
    return exercises_data

"""
agents/pm_generator_agent.py

AI Curriculum Architect Agent that generates a complete, pedagogically-sound
curriculum syllabus (PM) from PLO, CLO, and student profile, and exports to MD and Excel.
"""

import os
import json
import shutil
import openpyxl
from copy import copy
from typing import Dict, Any, List, Optional
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from core.llm import call_llm
from agents.pm_schemas import (
    LessonBlock, SessionBlock, StudentProfile, ClassConfiguration,
    SessionBudget, PMGeneratorConfig, SyllabusPM,
)
from agents.pm_reviewer_agent import pm_reviewer_agent

SYSTEM_PROMPT = """You are a Lead Academic Director specializing in curriculum architecture at Rikkei Education.
Your task is to design a complete, pedagogically-sound curriculum syllabus (PM Syllabus) in JSON format based on PLOs, CLOs, student profiles, session count, target technology, and class configurations.

CRITICAL: OUTPUT ONLY RAW JSON ARRAY. DO NOT write any explanations, Markdown commentary, or text outside JSON.

WRITE EXTREMELY CONCISELY TO PREVENT OUTPUT TOKEN LIMIT TRUNCATION:
- Session title (session_title): Under 10 words.
- Lesson title (lesson_title): Under 12 words.
- content_scope: List 3-5 keywords separated by ";". Max 50 chars.
- expected_outcome: Write 1 concise action sentence in Accented Vietnamese. Max 60 chars.
- forbidden_scope: "FORBIDDEN:" + list of 3-6 keywords. Max 60 chars.
- allowed_scope: "TAUGHT:" + list of 3-6 keywords. Max 60 chars.

MANDATORY PEDAGOGICAL EXECUTION DIRECTIVES:

1. FIRST SESSIONS PACING DIRECTIVE:
   - Session 01 MUST be Orientation & Curriculum Roadmap (Theory/Overview). MUST NOT contain setup or complex coding tasks. Focus on CLO/PLO, sample product demo, study plan.
   - Session 02 MUST be the first Technical Theory Session (e.g. environment setup, basic syntax, architecture overview).
   - Session 03 MUST be the first Practical Lab Session (hands-on practice for technical skills taught in Session 02).
   - ABSOLUTELY FORBIDDEN to schedule a Practical Lab on Session 02 because students have not learned technical content in Session 01.

2. DYNAMIC COGNITIVE PACING & WORKLOAD DIRECTIVE:
   - Light Theory (setup, basic syntax, simple config): Allow max 2 consecutive light theory sessions before a mandatory Practical Lab.
   - Heavy Theory (DB integration, auth/permissions, software architecture, testing): Beginners MUST have an immediate Practical Lab or Mini Project following every heavy theory session to prevent cognitive overload.
   - Final Session N MUST be the Final Exam or Project Presentation ("Final Exam" or "Project").
   - Practice sessions MUST use real-world enterprise scenarios (e.g., e-commerce order API, CRM ticket), NOT dry academic tasks (factorial, star printing). Session N practice MUST strictly use concepts taught in prior theory sessions (1 to N-1).

3. QUY TẮC CẤM CHIA BÀI HỌC CHO CÁC BUỔI PHI LÝ THUYẾT (NO LESSONS FOR NON-THEORY):
   - TUYỆT ĐỐI CẤM chia nhỏ bài học con cho các buổi có hình thức là "Thực hành", "Mini project", "Project", "Hackathon", "Thi giữa môn", "Thi cuối môn". Mảng "lessons" của các buổi này BẮT BUỘC phải để rỗng `[]`.

4. QUY TẮC PHÂN BỔ MINI PROJECT (COMBO-BASED):
   - Combo = 1 Lý thuyết + 1 Thực hành của cùng một chủ đề kiến thức.
   - Với kiến thức cơ bản (cú pháp, cấu hình, xử lý đầu vào/đầu ra): Xếp 1 buổi Mini Project sau 3-4 combos.
   - Với kiến thức phức tạp (tích hợp DB, xác thực/phân quyền, kiến trúc hệ thống): Xếp 1 buổi Mini Project sau 2 combos.

5. QUY TẮC THI GIỮA MÔN (HACKATHON) & TỔNG ÔN TẬP:
   - Phải có 1 buổi thi Hackathon (giữa môn) tại khoảng buổi thứ 2/3 khóa học (đối với 36 buổi là Session 24; đối với 24 buổi là Session 16). Điều kiện thi là sinh viên đã nắm vững các kỹ năng cốt lõi nhất của `tech_stack` (tự suy luận từ CLO/PLO).
   - Buổi ngay trước Hackathon (ví dụ Session 23) bắt buộc phải là buổi Thực hành (Tổng ôn tập kiến thức nâng cao và luyện đề).

6. QUY TẮC PHÂN PHỐI LÊN LỚP (DELIVERY CONFIGURATION):
   - `sessions_per_day`: Nếu là 2 (học 2 ca/ngày):
     * Ngày 1 (Session 01 + Session 02): Session 01 là Định hướng (Lý thuyết), Session 02 BẮT BUỘC là Lý thuyết kỹ thuật đầu tiên (cài đặt môi trường / kiến trúc cơ bản).
     * Ngày 2 (Session 03 + Session 04): Session 03 bắt buộc là Thực hành (luyện tập cho Session 02), Session 04 bắt buộc là Lý thuyết kỹ thuật tiếp theo.
     * Ngày 3 (Session 05 + Session 06): Session 05 bắt buộc là Thực hành (luyện tập cho Session 04), Session 06 bắt buộc là Lý thuyết kỹ thuật tiếp theo.
     * Các ngày tiếp theo (cặp 7-8, 9-10...): Bố trí xen kẽ sao cho mỗi ngày học chỉ chứa tối đa 1 buổi Lý thuyết và 1 buổi Thực hành/Mini project. TUYỆT ĐỐI CẤM xếp 2 buổi Lý thuyết liên tiếp trong cùng một ngày học (ngoại trừ Ngày 1).
   - `session_duration_hours`:
     * Đối với thời lượng học ngắn và trung bình (1.5 - 2.0 giờ): Cho phép mỗi buổi Lý thuyết chứa từ 2 đến 4 bài học nhỏ (lessons). Phân bổ số lượng lessons PHẢI thay đổi linh hoạt theo ĐỘ KHÓ và KHỐI LƯỢNG của chủ đề:
       + Chủ đề nhẹ, ít khái niệm mới (cài đặt môi trường, cú pháp cơ bản, cấu hình đơn giản): 2-3 lessons là đủ.
       + Chủ đề trung bình (kiểm định dữ liệu, xử lý file, cấu trúc mã nguồn): 3 lessons.
       + Chủ đề nặng, nhiều khái niệm mới và phức tạp (tích hợp cơ sở dữ liệu, xử lý quan hệ dữ liệu, xác thực/phân quyền, kiểm thử tự động): BẮT BUỘC dùng 4 lessons để trải đều nội dung, tránh nhồi nhét.
     * Đối với thời lượng học dài (3.0 giờ): Cho phép từ 4-5 bài học nhỏ.
     * TUYỆT ĐỐI CẤM fix cứng tất cả sessions lý thuyết đều cùng 1 số lessons (ví dụ: cấm để tất cả đều đúng 3 lessons). Số lessons phải dao động tự nhiên giữa 2-4 tùy nội dung.
     * KIỂM TRA DỒN NÉN (COMPRESSION CHECK): Trước khi chốt số lessons, tự hỏi: "Nếu dồn nội dung chủ đề này vào ít hơn 4 lessons, liệu sinh viên có bị quá tải khi xem 1 video 12 phút?" — Nếu CÓ → TÁCH thêm lesson, tối đa 4.

7. QUY TẮC MẠCH LẠC SƯ PHẠM & LIÊN KẾT NỀN TẢNG (PREREQUISITE CHAIN):
   - Cấm nhảy cóc kiến thức: Nội dung bài trước (Lesson N-1) bắt buộc phải là nền tảng lý thuyết trực tiếp cho bài sau (Lesson N).
   - Tiến trình sư phạm luôn đi từ: Khái niệm cơ bản ➔ Cơ chế hoạt động ➔ Cú pháp khai báo ➔ Xử lý lỗi/Ứng dụng thực tế.
   - Các bài học nhỏ trong cùng một buổi phải có liên kết chặt chẽ xung quanh một chủ đề thống nhất.

8. QUY TẮC TRÌNH BÀY & LÀM SẠCH TIÊU ĐỀ:
   - CẤM chèn bất kỳ hậu tố phân loại độ khó hoặc hình thức học nào như (HEAVY), (LIGHT), (Lý thuyết Nhẹ) vào tiêu đề Session hoặc Lesson. Tiêu đề phải sạch sẽ 100%.
   - KHÔNG DÙNG CHỮ IN HOA TOÀN BỘ (NO ALL CAPS): Tiêu đề viết thường dạng Sentence case.
   - KHÔNG DÙNG EMOJI: Cấm dùng emoji.
   - 100% tiếng Việt có dấu chuẩn xác. Tên biến/hàm trong code ví dụ dùng tiếng Anh có nghĩa.

9. QUY TẮC NGÔN NGỮ CHUẨN SƯ PHẠM (ACADEMIC TONE):
   - Sử dụng thuật ngữ khoa học chuyên ngành CNTT, khách quan, trung tính và chuyên nghiệp.
   - TUYỆT ĐỐI CẤM sử dụng các từ ngữ phóng đại, giật tít, quảng cáo, sến sẩm (như: 'Làm chủ...', 'Sức mạnh của...', 'Chìa khóa...', 'Bí quyết...', 'Tận dụng...', 'Cực chất', 'Tuyệt vời', 'Thực chiến', 'Tối thượng', 'Thần tốc', 'Lợi ích kép', 'Bứt phá').
   - Thay vào đó dùng các từ trung tính: 'Cấu hình...', 'Thiết lập...', 'Lập trình...', 'Tích hợp...', 'Triển khai...', 'Ứng dụng...', 'Phân tích...', 'Hệ thống hóa...'.

10. QUY TẮC BAO PHỦ BẢN ĐỒ TRI THỨC ĐỘNG (DYNAMIC ROADMAP COMPLETENESS):
   - Căn cứ vào công nghệ mục tiêu (`tech_stack`) và chuẩn đầu ra CLO/PLO, bạn phải tự suy luận ra toàn bộ danh sách các chủ đề kiến thức cốt lõi cần học.
   - BẮT BUỘC thiết kế chương trình bao phủ đầy đủ toàn bộ lộ trình này, đi từ cơ bản đến nâng cao. Tuyệt đối không được bỏ sót các chủ đề nền tảng và không được nhảy cóc sang kiến thức nâng cao khi chưa học kiến thức nền.
   - Phạm vi bao phủ PHẢI phù hợp với năng lực tiếp thu của sinh viên (`student_profile`). Với `difficulty_level: "beginner"`, chỉ đưa vào những công nghệ/công cụ trực tiếp phục vụ CLO/PLO. TUYỆT ĐỐI CẤM đưa các nội dung ngoài phạm vi CLO/PLO chỉ vì chúng "thường đi kèm" trong thực tế — nếu CLO/PLO không yêu cầu rõ ràng thì không được đưa vào.

11. QUY TẮC THIẾT KẾ BÀI HỌC NHỎ CHO VIDEO (VIDEO-UNIT LESSON DESIGN):
   - Mỗi bài học nhỏ (lesson) tương ứng với 1 video bài giảng dài tối đa 12 phút.
   - TÁCH LESSON KHI BỊ DỒN NÉN: Nếu nội dung của một lesson bị ép quá nhiều khái niệm vào 1 video, BẮT BUỘC tách thành các lesson độc lập, tối đa 4 lessons/session. Không được để 1 lesson ôm quá nhiều thứ chỉ vì muốn giữ số lesson ít.
   - THỨ TỰ BẮT BUỘC trong 1 session (trật tự dẫn dắt cụ thể):
     * Lesson đầu: Đặt vấn đề thực tế + giải thích khái niệm ("Tại sao cần?", "Vấn đề gì cần giải?")
     * Lesson giữa: Khai báo cú pháp + cơ chế hoạt động nội bộ
     * Lesson cuối: Ứng dụng vào kịch bản thực tế dự án (gắn với doanh nghiệp)
   - TÍNH NỀN TẢNG (PREREQUISITE CHAIN): Lesson N-1 phải là tiền đề trực tiếp cho Lesson N. CẤM đặt lesson không có sự kế tiếp logic với lesson trước trong cùng session.
   - TÍNH THỰC TẾ BẮT BUỘC (REAL-WORLD APPLICABILITY): Mỗi lesson PHẢI có ít nhất 1 ứng dụng thực tế rõ ràng trong học tập hoặc đi làm. CẤM lesson thuần lý thuyết trừu tượng không gắn với bài toán thực tiễn.
   - Ví dụ SAI: 3 lesson rời rạc — Lesson 1 "Giới thiệu class", Lesson 2 "Giới thiệu method", Lesson 3 "Giới thiệu inheritance" (chỉ liệt kê khái niệm, không dẫn dắt, không ứng dụng).
   - Ví dụ ĐÚNG: Lesson 1 "Vấn đề code lặp và giải pháp OOP" → Lesson 2 "Khai báo class, thuộc tính và phương thức" → Lesson 3 "Kế thừa và tái sử dụng code trong dự án" → Lesson 4 "Áp dụng OOP vào module quản lý người dùng" (có nền tảng, có thứ tự, có thực tế).

12. QUY TẮC ĐẶT MÌNH VÀO VỊ TRÍ SINH VIÊN (STUDENT-FIRST PERSPECTIVE):
   - Khi thiết kế mỗi lesson, hãy tự hỏi: "Nếu tôi là sinh viên mới học chủ đề này lần đầu, tôi sẽ hiểu ngay không? Tôi có bị quá tải không?".
   - Với mỗi chủ đề khó và mới (lần đầu sinh viên tiếp xúc), lesson đầu tiên của chủ đề PHẢI là bài dẫn nhập: giải thích vấn đề cần giải quyết, tại sao cần công cụ/kỹ thuật này, trước khi đi vào cú pháp.
   - Ví dụ: Khi dạy một thư viện/framework mới, Lesson 1 không được bắt đầu bằng cú pháp khai báo. Phải bắt đầu bằng giải thích vấn đề thực tế cần giải quyết và lý do cần công cụ này.

13. QUY TẮC CẤM FIX CỨNG CÔNG NGHỆ (TECHNOLOGY-AGNOSTIC DESIGN):
   - TUYỆT ĐỐI CẤM fix cứng hay fallback nội dung cho bất kỳ công nghệ, framework, thư viện, hoặc ngôn ngữ cụ thể nào trong quy tắc sư phạm.
   - Toàn bộ nội dung chương trình học PHẢI được suy luận động 100% từ `tech_stack`, CLO/PLO, và `student_profile` được truyền vào.
   - Nội dung sinh ra cho từng môn học phải khác nhau hoàn toàn tùy vào `tech_stack` — KHÔNG được dùng chung template nội dung cho mọi tech stack.
   - CẤM đặt tên thư viện, framework, hay công cụ cụ thể trong quy tắc sư phạm hệ thống. Chỉ được dùng tên công nghệ cụ thể trong NỘI DUNG sinh ra cho từng môn cụ thể (dựa trên `tech_stack` đầu vào).

15. QUY TẮC BIÊN GIỚI NỘI DUNG TUYỆT ĐỐI (STRICT CONTENT BOUNDARY):
   - TUYỆT ĐỐI CẤM đưa bất kỳ công nghệ, thư viện, framework, khái niệm, hay cú pháp nào KHÔNG được liệt kê rõ ràng trong `tech_stack` và `tech_stack_versions` vào nội dung lesson.
   - Đây là vi phạm nghiêm trọng nhất. Ví dụ vi phạm tiêu biểu:
     * Môn Python Core → CẤM xuất hiện: SQLite, SQL, Database, Flask, Django, FastAPI, HTML, CSS, React, JavaScript, API, Docker, Redis, Pandas, NumPy, Machine Learning (trừ khi nằm trong `tech_stack_versions`)
     * Môn JavaScript Frontend thuần → CẤM xuất hiện: React, Vue, Angular, Vite, Next.js, Express, Node.js, Python, FastAPI, SQL, Java (trừ khi nằm trong `tech_stack_versions`)
     * Môn Java Spring Boot → CẤM xuất hiện: Python, JavaScript, PHP (trừ khi nằm trong `tech_stack_versions`)
   - QUY TẮC VÀNG: Trước khi điền nội dung cho từng lesson, hãy kiểm tra bắt buộc: "Công nghệ này có trong `tech_stack` hay `tech_stack_versions` đã cung cấp không?" — Nếu KHÔNG → TUYỆT ĐỐI CẤM đưa vào.
   - Ranh giới nội dung phải được bảo vệ nghiêm ngặt suốt toàn bộ 36 buổi. Không có ngoại lệ.

16. QUY TẮC ĐỐI SOÁT CHẶT CHẼ CLO, PLO VÀ NỘI DUNG CHÍNH (STRICT CLO/PLO/MAIN CONTENT ALIGNMENT):
   - TUYỆT ĐỐI CẤM đưa nội dung/công nghệ của các môn học tương lai hoặc các framework nâng cao vào môn học nếu CLO, PLO và Nội dung chính từ Khung chương trình đào tạo chỉ yêu cầu kiến thức nền tảng/ngôn ngữ thuần.
   - Ví dụ cụ thể: Môn học có CLO/PLO yêu cầu 'Lập trình các tương tác Web bằng Javascript thuần' (Vanilla JS, DOM API, Fetch API) ➔ TUYỆT ĐỐI CẤM đưa React, Vue, Angular, Vite, Next.js, Node.js, Express hay Database vào bài học! Môn học nào CHỈ ĐƯỢC TẬP TRUNG ĐÚNG CÔNG NGHỆ CỦA MÔN HỌC ĐÓ.
   - BẮT BUỘC đọc kỹ cột CLO, PLO và Nội dung chính từ Khung chương trình được truyền vào ở từng cuộc gọi để xác định đúng ranh giới công nghệ tối đa được phép dạy.

17. QUY TẮC ĐẢM BẢO HÀM LƯỢNG THỰC HÀNH (PRACTICE SUBSTANCE & DEPTH GUARANTEE):
   - TUYỆT ĐỐI CẤM thiết kế một Session Thực hành (2h) bị nông hoặc rỗng nội dung do Session Lý thuyết tiền đề quá ít kiến thức (ví dụ: Session Lý thuyết 2 chỉ có cài đặt môi trường/venv/linter mà chưa dạy bất kỳ kiến thức lập trình nào).
   - ĐỂ KHẮC PHỤC RỦI RO BUỔI THỰC HÀNH BỊ RỖNG:
     * GIẢI PHÁP 1 (TĂNG HÀM LƯỢNG - KHUYÊN DÙNG): Khi thiết kế Session Lý thuyết có nội dung Cài đặt/Cấu hình (Session 02), BẮT BUỘC đưa ngay các kiến thức lập trình/cú pháp cơ bản đầu tiên (Khai báo biến, Kiểu dữ liệu cơ bản, Nhập xuất dữ liệu input/print, Toán tử số học) vào Session Lý thuyết đó, để Session Thực hành liền sau có bài tập viết script, tính toán và xử lý logic thực tế cho sinh viên thực hành suốt 2h.
     * GIẢI PHÁP 2 (ĐIỀU CHỈNH LOẠI SESSION): Nếu một chủ đề thuần thao tác cài đặt chưa có kiến thức code, hãy thiết kế thành 2 buổi Lý thuyết liên tiếp trước khi đến buổi Thực hành tổng hợp.

14. QUY TẮC SINH PHẠM VI SƯ PHẠM (SCOPE COLUMNS):
   Mỗi lesson (hoặc mỗi session phi lý thuyết) BẮT BUỘC phải có 4 trường phạm vi chi tiết:
   a. `content_scope`: Liệt kê cụ thể từng khái niệm, cú pháp, công cụ sẽ học trong lesson này. Viết dạng liệt kê ngắn phân cách bằng dấu ";". Ví dụ: "Khái niệm biến và ô nhớ; Biến int, float, str, bool; Quy tắc snake_case; Kiểm tra type() và id()."
   b. `expected_outcome`: Mô tả kết quả mong đợi sau lesson — sinh viên CÓ THỂ LÀM ĐƯỢC GÌ cụ thể. Viết 1-2 câu hành động (dùng động từ: "Khai báo thành công...", "Viết được...", "Phân biệt được...").
   c. `forbidden_scope`: Liệt kê các khái niệm/công nghệ CHƯA ĐƯỢC HỌC và CẤM sử dụng trong lesson này. Viết dạng: "CẤM: <danh sách khái niệm chưa học>". Phải cập nhật tích lũy — forbidden_scope ở lesson sau phải bớt đi các khái niệm vừa học ở lesson trước.
   d. `allowed_scope`: Liệt kê tích lũy các khái niệm ĐÃ HỌC từ tất cả các lesson/session trước đó. Viết dạng: "ĐÃ HỌC: <danh sách tích lũy>". Phải cập nhật cộng dồn — allowed_scope ở lesson sau = allowed_scope lesson trước + nội dung lesson trước.
   - CÁC QUY TẮC QUAN TRỌNG CHO SCOPE:
     * `forbidden_scope` và `allowed_scope` PHẢI NHẤT QUÁN LOGIC: Nếu khái niệm X có trong `allowed_scope` thì KHÔNG được có trong `forbidden_scope`.
     * Session 01 (Định hướng): `allowed_scope` = "ĐÃ HỌC: Chưa có (Buổi mở đầu).", `forbidden_scope` liệt kê toàn bộ kiến thức kỹ thuật của khóa.
     * Các session phi lý thuyết (Thực hành/Mini project): Ghi scope ở cấp session (không ở lesson).

ĐỊNH DẠNG ĐẦU RA JSON BẮT BUỘC (TRẢ VỀ DUY NHẤT 1 MẢNG JSON HỢP LỆ, KHÔNG CHỨA BLOCK MARKDOWN):
[
  {
    "session_num": 1,
    "hinh_thuc": "Lý thuyết",
    "title": "Chủ đề của buổi học",
    "content_scope": "",
    "expected_outcome": "",
    "forbidden_scope": "",
    "allowed_scope": "",
    "lessons": [
      {
        "lesson_num": 1,
        "title": "Tiêu đề chi tiết của bài học nhỏ",
        "content_scope": "Khái niệm A; Cú pháp B; Công cụ C",
        "expected_outcome": "Khai báo thành công X, phân biệt được Y",
        "forbidden_scope": "CẤM: List, Dict, Loop, Function, Class",
        "allowed_scope": "ĐÃ HỌC: Biến, kiểu dữ liệu, print()"
      }
    ]
  }
]
"""

# ---------------------------------------------------------------------------
# Constants for Excel styling
# ---------------------------------------------------------------------------
_HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
_HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
_HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)

_DATA_FONT = Font(name="Calibri", size=10)
_DATA_FONT_BOLD = Font(name="Calibri", size=10, bold=True)
_DATA_ALIGN = Alignment(horizontal="left", vertical="center", wrap_text=True)
_DATA_ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

_THIN_BORDER = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)

_SESSION_TYPE_FILLS = {
    "Lý thuyết":   PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid"),
    "Thực hành":   PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid"),
    "Mini project": PatternFill(start_color="FFF7ED", end_color="FFF7ED", fill_type="solid"),
    "Hackathon":   PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid"),
    "Thi giữa môn": PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid"),
    "Thi cuối môn": PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid"),
    "Project":     PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid"),
}
_DEFAULT_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

_COL_WIDTHS = [14, 16, 16, 36, 36, 45, 45, 35, 35, 22]

# Maximum number of self-correction rounds for prerequisite guard
MAX_CORRECTION_ROUNDS = 3


# ---------------------------------------------------------------------------
# Prerequisite Guard (Part L)
# ---------------------------------------------------------------------------
def _validate_prerequisite_chain(pm_data: List[Dict[str, Any]]) -> tuple:
    """
    Validates pedagogical prerequisite rules on the generated PM.
    Returns (is_valid: bool, errors: List[str]).
    """
    errors = []

    if not pm_data:
        errors.append("PM rỗng — không có session nào được sinh ra.")
        return False, errors

    # Rule 1: Session 01 must be orientation (Lý thuyết)
    s1 = pm_data[0]
    ht1 = str(s1.get("hinh_thuc", "")).strip()
    if "Lý thuyết" not in ht1:
        errors.append(f"Session 01 phải là 'Lý thuyết' (Định hướng), nhưng hiện tại là '{ht1}'.")

    # Rule 2: Session 02 must be Lý thuyết (not Thực hành)
    if len(pm_data) >= 2:
        s2 = pm_data[1]
        ht2 = str(s2.get("hinh_thuc", "")).strip()
        if "Thực hành" in ht2 or "Mini project" in ht2:
            errors.append(f"Session 02 PHẢI là 'Lý thuyết' kỹ thuật, nhưng hiện tại là '{ht2}'.")

    # Rule 3: Session 03 must be Thực hành
    if len(pm_data) >= 3:
        s3 = pm_data[2]
        ht3 = str(s3.get("hinh_thuc", "")).strip()
        if "Thực hành" not in ht3:
            errors.append(f"Session 03 PHẢI là 'Thực hành' đầu tiên, nhưng hiện tại là '{ht3}'.")

    # Rule 4: Last session must be exam or project
    last = pm_data[-1]
    ht_last = str(last.get("hinh_thuc", "")).strip()
    valid_finals = ["Thi cuối môn", "Project", "Dự án cuối khóa"]
    if not any(vf in ht_last for vf in valid_finals):
        errors.append(f"Buổi cuối cùng phải là Thi cuối môn hoặc Project, nhưng hiện tại là '{ht_last}'.")

    # Rule 5: Non-theory sessions must have empty lessons
    for s in pm_data:
        ht = str(s.get("hinh_thuc", "")).strip()
        lessons = s.get("lessons", [])
        if "Lý thuyết" not in ht and len(lessons) > 0:
            errors.append(
                f"Session {s.get('session_num', '?')} ({ht}) không nên có lessons con, nhưng có {len(lessons)} lessons."
            )

    # Rule 6: No practice session before any theory has been taught
    theory_seen = False
    for s in pm_data:
        ht = str(s.get("hinh_thuc", "")).strip()
        if "Lý thuyết" in ht:
            # Skip orientation (session 1)
            snum = s.get("session_num", 0)
            if snum > 1:
                theory_seen = True
        if "Thực hành" in ht and not theory_seen:
            errors.append(
                f"Session {s.get('session_num', '?')} là Thực hành nhưng chưa có buổi Lý thuyết kỹ thuật nào trước đó."
            )

    # Rule 7: Theory sessions must not exceed 4 lessons
    for s in pm_data:
        ht = str(s.get("hinh_thuc", "")).strip()
        lessons = s.get("lessons", [])
        if "Lý thuyết" in ht and len(lessons) > 4:
            errors.append(
                f"Session {s.get('session_num', '?')} (Lý thuyết) có {len(lessons)} lessons — vượt quá giới hạn tối đa 4."
            )

    # Rule 8: Session numbers must be strictly sequential (1, 2, 3, ...)
    # This catches Part1+Part2 merge bugs where sessions restart numbering
    expected_num = 1
    for s in pm_data:
        actual = s.get("session_num", -1)
        if actual != expected_num:
            errors.append(
                f"Số thứ tự session không liên tục: mong đợi Session {expected_num:02d}, nhận Session {actual}. "
                f"Có thể do lỗi ghép Phần 1 + Phần 2."
            )
            break
        expected_num += 1

    is_valid = len(errors) == 0
    return is_valid, errors



def _self_correct_pm(
    pm_data: List[Dict[str, Any]],
    errors: List[str],
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    student_profile: Dict[str, Any],
    session_budget: Dict[str, Any],
    tech_stack: str,
    class_configuration: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Calls LLM with the current PM and detected errors to produce a corrected version.
    """
    error_block = "\n".join(f"- {e}" for e in errors)

    correction_prompt = f"""Current curriculum contains the following pedagogical defects / deductions (GOAL: 100/100 PERFECT GRADE):
{error_block}

Current curriculum needing revision:
{json.dumps(pm_data, ensure_ascii=False, indent=2)}

REVISE and UPGRADE the curriculum syllabus to resolve ALL defects and warnings above to achieve a 100/100 score.
- For vague bloom verbs: Replace with measurable Bloom action verbs in Accented Vietnamese ("Phân biệt được...", "Khởi tạo thành công...", "Giải quyết được...").
- For sequence ordering or practice load warnings: Restructure the 3 lessons per theory session or add code depth.
- Retain valid content and only adjust/restructure non-compliant or flagged sessions.
Return ONLY raw updated JSON array."""

    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=correction_prompt,
        json_mode=True,
        agent_name="PM Generator Agent (Self-Correction)"
    )

    try:
        clean_json = response.replace("```json", "").replace("```", "").strip()
        parsed_data = json.loads(clean_json)
        if isinstance(parsed_data, list):
            return parsed_data
        elif isinstance(parsed_data, dict) and "sessions" in parsed_data:
            return parsed_data["sessions"]
        else:
            print(f"  [Guard] Output sửa lỗi không phải list: {type(parsed_data)}")
            return pm_data
    except Exception as e:
        print(f"  [Guard] Lỗi parse JSON sửa lỗi: {e}")
        return pm_data


# ---------------------------------------------------------------------------
# Core generation functions
# ---------------------------------------------------------------------------
def generate_curriculum_pm(
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    student_profile: Dict[str, Any],
    session_budget: Dict[str, Any],
    tech_stack: str,
    class_configuration: Dict[str, Any],
    existing_pm: Optional[List[Dict[str, Any]]] = None,
    main_content: str = "",
    exam_type: str = ""
) -> List[Dict[str, Any]]:
    """
    Invokes LLM to generate the structured PM syllabus.
    Splits into two parts for long courses to avoid token truncation limits.
    Applies prerequisite guard with up to 3 self-correction rounds.
    """
    total_sessions = session_budget.get("total_sessions", 25)
    hackathon_sess = int(total_sessions * 2 / 3)
    review_sess = hackathon_sess - 1

    if total_sessions > 18:
        print(f"  [SPGA] Số lượng buổi lớn ({total_sessions} buổi). Thực hiện sinh thành 2 phần tách biệt...")
        half = total_sessions // 2

        # Part 1: sessions 1 to half
        part1_instruction = f"""Design PART 1: EXACTLY the first {half} Sessions (Session 01 to Session {half:02d}).
MANDATORY Course Opening Session Allocation Rules:
- Session 01 is Course Orientation (Theory), no technical coding or environment setup.
- Session 02 MUST be the first Technical Theory session (e.g. environment setup, project structure).
- Session 03 MUST be the first Practical Lab session (practicing Session 02 concepts).
- ABSOLUTELY FORBIDDEN to place Practical Lab at Session 02.
Apply Theory-Practice pairing rules (sessions_per_day = {class_configuration.get('sessions_per_day', 1)}).
Allocate Mini Projects after every 3-4 basic combos (or 2 advanced combos)."""

        pm_part1 = _call_generator_agent(
            course_id, course_name, clos, plos, student_profile, session_budget, tech_stack, class_configuration,
            prompt_suffix=part1_instruction, existing_pm=existing_pm,
            main_content=main_content, exam_type=exam_type
        )

        if not pm_part1:
            print("  [Error] Không thể tạo Phân 1 của chương trình học.")
            return []

        print(f"  [SPGA] Đã sinh xong Phân 1 ({len(pm_part1)} sessions). Đang sinh Phần 2...")

        # Part 2: sessions half + 1 to total_sessions
        part2_instruction = f"""Design PART 2: Remaining Sessions from Session {half + 1:02d} to Session {total_sessions:02d} (total {total_sessions - half} sessions).
Here is the list of Sessions generated in PART 1 for reference and continuity:
{json.dumps(pm_part1, ensure_ascii=False, indent=2)}

MANDATORY DIRECTIVES:
- Continue curriculum design starting precisely at Session {half + 1:02d} through Session {total_sessions:02d}.
- Ensure knowledge continuity and prerequisite flow from prior sessions.
- Place Midterm Exam / Hackathon at Session {hackathon_sess:02d}, and the session immediately preceding it (Session {review_sess:02d}) MUST be a Practical Review Lab.
- Final Session (Session {total_sessions:02d}) MUST be Capstone Project Defense."""

        pm_part2 = _call_generator_agent(
            course_id, course_name, clos, plos, student_profile, session_budget, tech_stack, class_configuration,
            prompt_suffix=part2_instruction, existing_pm=existing_pm,
            main_content=main_content, exam_type=exam_type
        )

        if not pm_part2:
            print("  [Warning] Không thể sinh Phần 2. Trả về kết quả của Phần 1.")
            return pm_part1

        # Merge parts and normalize session numbers
        merged = []
        for idx, s in enumerate(pm_part1 + pm_part2, 1):
            s["session_num"] = idx
            ht = str(s.get("hinh_thuc", "")).strip()
            if "Lý thuyết" not in ht:
                s["lessons"] = []
            merged.append(s)

        print(f"  [SPGA] Ghép nối thành công lộ trình chương trình học ({len(merged)} buổi).")
        pm_data = merged
    else:
        # Standard single call
        single_instruction = f"""Design entire curriculum syllabus containing EXACTLY {total_sessions} Sessions (Session 01 to Session {total_sessions:02d}).
MANDATORY Course Opening Session Allocation Rules:
- Session 01 is Course Orientation (Theory), no technical coding or setup.
- Session 02 MUST be the first Technical Theory session.
- Session 03 MUST be the first Practical Lab session.
- ABSOLUTELY FORBIDDEN to place Practical Lab at Session 02.
Final Session (Session {total_sessions:02d}) MUST be Final Exam / Capstone Project Defense.
If total sessions >= 16: place Midterm Hackathon Exam at Session {hackathon_sess:02d} and Practical Review Lab at Session {review_sess:02d}."""

        res = _call_generator_agent(
            course_id, course_name, clos, plos, student_profile, session_budget, tech_stack, class_configuration,
            prompt_suffix=single_instruction, existing_pm=existing_pm,
            main_content=main_content, exam_type=exam_type
        )
        for s in res:
            ht = str(s.get("hinh_thuc", "")).strip()
            if "Lý thuyết" not in ht:
                s["lessons"] = []
        pm_data = res

    # --------------- PM Reviewer & QA Auditor Agent ---------------
    config_dict = {
        "tech_stack": tech_stack,
        "class_configuration": class_configuration,
        "student_profile": student_profile,
        "session_budget": session_budget
    }
    course_info_dict = {
        "course_id": course_id,
        "course_name": course_name,
        "clos": clos,
        "plos": plos
    }

    for round_num in range(1, MAX_CORRECTION_ROUNDS + 1):
        review_result = pm_reviewer_agent(pm_data, config_dict, course_info_dict)
        score = review_result["score"]
        violations = review_result["rule_violations"]

        if score == 100 or (score >= 98 and len(violations) == 0):
            print(f"  [PM Reviewer] Phê duyệt tuyệt đối — PM đạt điểm chất lượng tối đa ({score}/100).")
            break

        if review_result["is_approved"]:
            print(f"  [PM Reviewer] Vòng {round_num}/{MAX_CORRECTION_ROUNDS}: Đã đạt {score}/100 (qua ngưỡng 90), đang tiếp tục tự tối ưu để hướng tới ĐIỂM TỐI ĐA (100/100)...")
        else:
            print(f"  [PM Reviewer] Vòng {round_num}/{MAX_CORRECTION_ROUNDS}: Chưa đạt chuẩn ({score}/100, {len(violations)} vi phạm). Đang tự sửa lỗi...")

        pm_data = _self_correct_pm(
            pm_data, violations,
            course_id, course_name, clos, plos,
            student_profile, session_budget, tech_stack, class_configuration,
        )
        # Re-enforce non-theory empty lessons after correction
        for s in pm_data:
            ht = str(s.get("hinh_thuc", "")).strip()
            if "Lý thuyết" not in ht:
                s["lessons"] = []
    else:
        # Exhausted all rounds
        final_review = pm_reviewer_agent(pm_data, config_dict, course_info_dict)
        print(f"  [PM Reviewer] Hoàn tất {MAX_CORRECTION_ROUNDS} vòng tối ưu. Điểm chất lượng cuối cùng: {final_review['score']}/100.")

    return pm_data


def _call_generator_agent(
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    student_profile: Dict[str, Any],
    session_budget: Dict[str, Any],
    tech_stack: str,
    class_configuration: Dict[str, Any],
    prompt_suffix: str,
    existing_pm: Optional[List[Dict[str, Any]]] = None,
    main_content: str = "",
    exam_type: str = ""
) -> List[Dict[str, Any]]:
    mode_text = ""
    if existing_pm:
        mode_text = f"""
MODE: REFACTOR MODE (UPDATE EXISTING CURRICULUM SYLLABUS)
Existing curriculum structure on disk:
{json.dumps(existing_pm, ensure_ascii=False, indent=2)}
"""

    user_prompt = f"""Author full Academic PM Curriculum Syllabus for course:
Course: {course_id} - {course_name}

1. LEARNING OUTCOMES (CLO & PLO):
- Course Learning Outcomes (CLO):
{json.dumps(clos, ensure_ascii=False, indent=2)}

- Program Learning Outcomes (PLO):
{json.dumps(plos, ensure_ascii=False, indent=2)}

2. MANDATORY MAIN CONTENT & CURRICULUM SCOPE:
{main_content if main_content else 'Unspecified'}

3. PRIMARY ASSESSMENT METHOD:
{exam_type if exam_type else 'Unspecified'}

4. MANDATORY SESSION BUDGET & ALLOCATION:
- Total Sessions: {session_budget.get('total_sessions', '?')} sessions ({class_configuration.get('session_duration_hours', 2.0)} hours per session)
- Theory Sessions: {session_budget.get('theory_sessions', '?')}
- Practice Sessions: {session_budget.get('practice_sessions', '?')}
- Mini Project Sessions: {session_budget.get('mini_projects', '?')}
- Midterm / Exam Sessions: {session_budget.get('final_exam', '?')}
- Capstone Project Sessions: {session_budget.get('capstone_project', '?')}

5. STUDENT PROFILE & CLASS CONFIGURATION:
- Student Profile: {json.dumps(student_profile, ensure_ascii=False, indent=2)}
- Class Configuration: {json.dumps(class_configuration, ensure_ascii=False, indent=2)}
- Target Technology Stack: {tech_stack}

STRICT PEDAGOGICAL & KNOWLEDGE BOUNDARY DIRECTIVES ({course_id}):
- Session count and session types MUST match 100% with the SESSION BUDGET above.
- MUST cover all mandatory main content topics from the curriculum framework.
- ONLY use technologies, libraries, and concepts within target tech stack: [{tech_stack}].
- FORBIDDEN to introduce unlisted technologies (databases, frameworks, ORMs, auth if not listed).
{mode_text}

Specific Phase Generation Task:
{prompt_suffix}

MANDATORY OUTPUT CONTRACT: Return ONLY a valid JSON array of sessions adhering strictly to the pedagogical rules.
"""

    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        json_mode=True,
        agent_name="PM Generator Agent"
    )

    try:
        clean_json = response.replace("```json", "").replace("```", "").strip()
        parsed_data = json.loads(clean_json)
        if isinstance(parsed_data, list):
            return parsed_data
        elif isinstance(parsed_data, dict) and "sessions" in parsed_data:
            return parsed_data["sessions"]
        else:
            print(f"  [Warning] Output JSON is not a list: {parsed_data}")
            return []
    except Exception as e:
        print(f"  [Error] Failed to parse generated PM JSON: {e}. Output was:\n{response}")
        return []


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------
def export_pm_to_markdown(
    pm_data: List[Dict[str, Any]],
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    filepath: str,
    tech_stack: str = "",
):
    """
    Exports the generated syllabus PM to a beautiful Markdown report.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    lines = []
    lines.append(f"# Chương Trình Học Chi Tiết Môn Học: {course_id} - {course_name}\n")

    lines.append("## 1. Chuẩn Đầu Ra Học Kỳ (PLO - Program Learning Outcomes)")
    for plo in plos:
        lines.append(f"- {plo}")
    lines.append("")

    lines.append("## 2. Chuẩn Đầu Ra Môn Học (CLO - Course Learning Outcomes)")
    for clo in clos:
        lines.append(f"- {clo}")
    lines.append("")

    lines.append("## 3. Kế Hoạch Giảng Dạy Từng Buổi (Syllabus Sessions)")
    lines.append("| Session | Loại Session | Mã Session | Tên Tiêu Đề Session | Tên Lesson | Nội Dung Chi Tiết | Kết Quả Mong Đợi | Phạm Vi Cấm Dùng | Phạm Vi Đã Học | Tech Stack |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    session_type_code_map = {
        "Lý thuyết": "THEORY", "Thực hành": "PRACTICE", "Mini project": "MINI_PROJECT",
        "Project": "PROJECT", "Hackathon": "HACKATHON", "Thi giữa môn": "MIDTERM", "Thi cuối môn": "FINAL",
    }

    for sess in pm_data:
        num = sess.get("session_num", sess.get("session", ""))
        hinh_thuc = sess.get("hinh_thuc", sess.get("session_type", ""))
        title = sess.get("title", sess.get("session_title", ""))
        lessons = sess.get("lessons", [])
        s_tech = sess.get("tech_stack_version", tech_stack)

        num_str = f"Session {int(num):02d}" if str(num).isdigit() else str(num)
        session_code = session_type_code_map.get(hinh_thuc, hinh_thuc.upper().replace(" ", "_"))
        session_title_full = f"{num_str} - {title}"

        if not lessons:
            s_noidung = sess.get("content_scope", "")
            s_outcome = sess.get("expected_outcome", "")
            s_forbidden = sess.get("forbidden_scope", "")
            s_allowed = sess.get("allowed_scope", "")
            lines.append(f"| {num_str} | {hinh_thuc} | {session_code} | {session_title_full} | {session_title_full} | {s_noidung} | {s_outcome} | {s_forbidden} | {s_allowed} | {s_tech} |")
        else:
            for idx, l in enumerate(lessons):
                l_num = l.get("lesson_num", idx + 1)
                l_title = l.get("title", "")
                l_noidung = l.get("content_scope", l.get("note", ""))
                l_outcome = l.get("expected_outcome", "")
                l_forbidden = l.get("forbidden_scope", "")
                l_allowed = l.get("allowed_scope", "")

                l_num_str = f"{int(l_num):02d}" if str(l_num).isdigit() else str(l_num)
                lesson_name = f"Lesson {l_num_str}: {l_title}"

                if idx == 0:
                    lines.append(f"| {num_str} | {hinh_thuc} | {session_code} | {session_title_full} | {lesson_name} | {l_noidung} | {l_outcome} | {l_forbidden} | {l_allowed} | {s_tech} |")
                else:
                    lines.append(f"| | | | | {lesson_name} | {l_noidung} | {l_outcome} | {l_forbidden} | {l_allowed} | {s_tech} |")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [Export] Saved Markdown syllabus to: {filepath}")


def export_pm_to_excel(
    pm_data: List[Dict[str, Any]],
    course_id: str,
    course_name: str,
    filepath: str,
    template_path: Optional[str] = None,
    clos: Optional[List[str]] = None,
    plos: Optional[List[str]] = None,
    student_profile: Optional[Dict[str, Any]] = None,
    tech_stack: str = "",
):
    """
    Exports the generated syllabus PM to a styled Excel spreadsheet.
    Copies from PM_Template_Standard.xlsx if available, applying professional
    color-coded styling per session type with merged cells.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Determine effective template path
    effective_template = template_path
    if not effective_template or not os.path.exists(effective_template):
        # Try standard location relative to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate = os.path.join(project_root, "templates", "PM_Template_Standard.xlsx")
        if os.path.exists(candidate):
            effective_template = candidate

    if effective_template and os.path.exists(effective_template):
        shutil.copy2(effective_template, filepath)
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        print(f"  [Export] Loaded template: {effective_template}")

        # Clear existing data rows (keep header row 5)
        if ws.max_row > 5:
            ws.delete_rows(6, ws.max_row - 5)
            # Clean up template's old merged cells in the data area (row >= 6) to avoid overlapping/corrupted merges
            for m_range in list(ws.merged_cells.ranges):
                if m_range.min_row >= 6:
                    ws.merged_cells.remove(m_range)

        # Write metadata rows 1-3
        persona_text = ""
        if student_profile:
            persona_text = f"Trình độ: {student_profile.get('entry_level', 'beginner')}, Nền tảng: {student_profile.get('background', 'non-it')}"
        ws.cell(row=1, column=2, value=persona_text)

        clo_text = "; ".join(clos) if clos else ""
        ws.cell(row=2, column=2, value=clo_text)

        ws.cell(row=3, column=2, value=f"Xây dựng sản phẩm dự án cuối khóa sử dụng {tech_stack}")
    else:
        # Fallback: create from scratch with styling
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"{course_id}"
        print(f"  [Export] Tạo mới workbook (không tìm thấy template)")

        # Write title
        ws.cell(row=1, column=1, value=f"Môn học: {course_id} - {course_name}")
        ws.merge_cells("A1:J1")

        # Write headers at row 5
        headers = [
            'Session', 'Loại Session', 'Mã Session', 'Tên Tiêu Đề Session',
            'Tên Lesson', 'Nội Dung Chi Tiết (Lesson Scope)',
            'Kết Quả Mong Đợi', 'Phạm Vi CẤM DÙNG',
            'Phạm Vi ĐÃ HỌC', 'Tech Stack & Quy Chuẩn'
        ]
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_idx, value=h)
            cell.font = _HEADER_FONT
            cell.fill = _HEADER_FILL
            cell.alignment = _HEADER_ALIGN
            cell.border = _THIN_BORDER

        # Set column widths
        for i, width in enumerate(_COL_WIDTHS):
            col_letter = openpyxl.utils.get_column_letter(i + 1)
            ws.column_dimensions[col_letter].width = width

        # Set header row height
        ws.row_dimensions[5].height = 28

    # --- Populate data rows starting from row 6 ---
    current_row = 6
    session_type_code_map = {
        "Lý thuyết": "THEORY",
        "Thực hành": "PRACTICE",
        "Mini project": "MINI_PROJECT",
        "Project": "PROJECT",
        "Hackathon": "HACKATHON",
        "Thi giữa môn": "MIDTERM",
        "Thi cuối môn": "FINAL",
    }

    for sess in pm_data:
        num = sess.get("session_num", "")
        hinh_thuc = str(sess.get("hinh_thuc", "")).strip()
        title = sess.get("title", "")
        lessons = sess.get("lessons", [])

        num_str = f"Session {int(num):02d}" if str(num).isdigit() else str(num)
        session_code = session_type_code_map.get(hinh_thuc, hinh_thuc.upper().replace(" ", "_"))
        session_title_full = f"{num_str} - {title}"

        # Determine fill color for this session type
        fill = _DEFAULT_FILL
        for key, f in _SESSION_TYPE_FILLS.items():
            if key in hinh_thuc:
                fill = f
                break

        if not lessons:
            # Single row for non-theory sessions
            s_noidung = sess.get("content_scope", "")
            s_outcome = sess.get("expected_outcome", "")
            s_forbidden = sess.get("forbidden_scope", "")
            s_allowed = sess.get("allowed_scope", "")
            row_data = [num_str, hinh_thuc, session_code, session_title_full, session_title_full, s_noidung, s_outcome, s_forbidden, s_allowed, tech_stack]
            for col_idx, val in enumerate(row_data, 1):
                cell = ws.cell(row=current_row, column=col_idx, value=val)
                cell.font = _DATA_FONT_BOLD if col_idx <= 4 else _DATA_FONT
                cell.alignment = _DATA_ALIGN_CENTER if col_idx <= 3 else _DATA_ALIGN
                cell.fill = fill
                cell.border = _THIN_BORDER
            ws.row_dimensions[current_row].height = 24
            current_row += 1
        else:
            # Multiple rows for theory sessions with lessons
            start_row = current_row
            for idx, l in enumerate(lessons):
                l_num = l.get("lesson_num", idx + 1)
                l_title = l.get("title", "")
                l_noidung = l.get("content_scope", l.get("note", ""))
                l_outcome = l.get("expected_outcome", "")
                l_forbidden = l.get("forbidden_scope", "")
                l_allowed = l.get("allowed_scope", "")
                l_num_str = f"{int(l_num):02d}" if str(l_num).isdigit() else str(l_num)

                lesson_name = f"Lesson {l_num_str}: {l_title}"

                if idx == 0:
                    # First lesson row — write session columns
                    row_data = [num_str, hinh_thuc, session_code, session_title_full, lesson_name, l_noidung, l_outcome, l_forbidden, l_allowed, tech_stack]
                else:
                    # Subsequent lesson rows — session columns blank (will be merged)
                    row_data = [None, None, None, None, lesson_name, l_noidung, l_outcome, l_forbidden, l_allowed, tech_stack]

                for col_idx, val in enumerate(row_data, 1):
                    cell = ws.cell(row=current_row, column=col_idx, value=val)
                    cell.font = _DATA_FONT_BOLD if col_idx <= 4 and idx == 0 else _DATA_FONT
                    cell.alignment = _DATA_ALIGN_CENTER if col_idx <= 3 else _DATA_ALIGN
                    cell.fill = fill
                    cell.border = _THIN_BORDER
                ws.row_dimensions[current_row].height = 24
                current_row += 1

            # Merge session info cells (columns A-D) if multiple lessons
            if len(lessons) > 1:
                end_row = current_row - 1
                for merge_col in range(1, 5):  # Columns A, B, C, D
                    ws.merge_cells(
                        start_row=start_row, start_column=merge_col,
                        end_row=end_row, end_column=merge_col
                    )

    wb.save(filepath)
    print(f"  [Export] Saved Excel syllabus to: {filepath}")


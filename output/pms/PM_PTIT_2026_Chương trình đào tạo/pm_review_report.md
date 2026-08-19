# 📑 BÁO CÁO THẨM ĐỊNH CHƯƠNG TRÌNH HỌC (PM REVIEW)
**Công nghệ mục tiêu:** `general/software_engineering`

## 1. 📊 Tổng Quan & Điểm Đánh Giá
- **Điểm sẵn sàng (Readiness Score):** 2/10
- **Nhận định chung:** Về mặt ý tưởng vĩ mô (Macro-level), lộ trình đào tạo rất hiện đại, có sự kết hợp xuất sắc giữa tư duy lập trình và ứng dụng AI (Prompting) ngay từ giai đoạn đầu. Tuy nhiên, về mặt vi mô (Micro-level) và cấu trúc dữ liệu đầu vào, bản thảo này đang vi phạm nghiêm trọng các nguyên tắc sư phạm về phân bổ tải trọng nhận thức (Cognitive Load) và sai lệch hoàn toàn cấu trúc JSON dành cho hệ thống sinh nội dung tự động (Automated Pipeline). Hệ thống AI sẽ thất bại toàn tập nếu sử dụng đầu vào này.

## 2. 🧠 Phân Tích Dòng Chảy Nhận Thức & Kế Thừa
- **Điểm sáng:** 
  - Tính kế thừa dự án (Project-based learning) được thiết kế rất tốt. Việc lấy đầu ra của IT-103 (Bản vẽ Figma) làm đầu vào cho IT-104 (Code HTML/CSS), sau đó đẩy lên Git (IT-105) và tiếp tục phát triển logic (IT-106) tạo ra một luồng học tập thực tế, sát với quy trình làm việc tại doanh nghiệp.
  - Đưa AI Prompting (IT-102) vào ngay từ đầu để sinh viên dùng AI như một trợ giảng/công cụ gỡ lỗi cho các module sau là một quyết định sư phạm mang tính đột phá.
- **Lỗ hổng "Nhảy cóc" (Missing Prerequisites) & Quá tải nhận thức:** 
  - **Nhầm lẫn khái niệm Session (Buổi học) và Module (Môn học):** PM đang nhồi nhét khối lượng kiến thức của một *môn học* (kéo dài nhiều tuần) vào một *buổi học* (Session). 
  - Ví dụ tại `Session 06`: Việc yêu cầu sinh viên học từ "JS Variables, Loops" nhảy thẳng đến "ES6, DOM Manipulation", và vươn tới cả "Promises/Async-Await" trong cùng một Session là một bước nhảy cóc phi lý. Một người mới không thể tiêu hóa kiến thức từ biến số cơ bản đến bất đồng bộ chỉ trong một buổi.

## 3. ⚠️ Các Điểm Yếu Cần Khắc Phục Khẩn Cấp (Critical Issues)
- **Cấu trúc Lesson phi lý & Thiếu độ phân giải (Granularity):**
  - *Vị trí:* Tất cả các Session (Từ 01 đến 06).
  - *Mô tả:* PM đang gộp toàn bộ nội dung của một khóa học thành một chuỗi (string) duy nhất và đặt vào trường `lesson_id` (VD: `"lesson_id": "Lesson JS Variables, Loops, ES6... DOM... Promises"`).
  - *Hậu quả sư phạm:* Hệ thống AI Pipeline không thể sinh ra bài giảng chi tiết khi không có sự bóc tách. Mỗi `lesson` phải là một khái niệm đơn lẻ (VD: Lesson 1: Biến trong JS; Lesson 2: Vòng lặp).
- **Vi phạm quy tắc cấu trúc phiên Thực hành/Dự án (Practice/Project Constraints):**
  - *Vị trí:* Trường `title` của các bài học bên trong Session 01 đến 05 đều ghi "Thi thực hành", và Session 06 ghi "Project".
  - *Mô tả:* Theo quy định, nếu đây là các bài kiểm tra thực hành hoặc dự án, chúng KHÔNG ĐƯỢC PHÉP chứa các `lessons` con mang tính lý thuyết bên trong. Ngược lại, nếu đây là các buổi học lý thuyết kết hợp thực hành, việc đặt tên bài học là "Thi thực hành" trong khi nội dung (lesson_id) lại chứa lý thuyết (Token, Zero-shot, Flexbox...) là sự mâu thuẫn hoàn toàn về mặt siêu dữ liệu (metadata).
  - *Hậu quả sư phạm:* Hệ thống sẽ bị lỗi logic: Hoặc bỏ qua việc tạo tài liệu (vì tưởng là bài thi), hoặc tạo ra một bài thi chứa toàn lý thuyết hỗn lốn.
- **Trường `expected_output` bị bỏ trống:**
  - *Vị trí:* Toàn bộ các mảng `lessons`.
  - *Hậu quả sư phạm:* AI generator không có tiêu chí (Rubric) để xác định học viên cần đạt được gì sau từng bài học nhỏ, dẫn đến nội dung sinh ra sẽ lan man, thiếu trọng tâm.

## 4. 🛠 Đề Xuất Chỉnh Sửa Cụ Thể Gửi PM
- **Yêu cầu 1 (Tái cấu trúc Session vs Module):** PM cần đập đi xây lại cấu trúc Session. Các mã như `IT-104`, `IT-106` nên được hiểu là các Module. Mỗi Module này phải được chia thành nhiều `Session` nhỏ. VD: Module IT-104 cần chia thành Session 4.1 (HTML5 Semantic), Session 4.2 (CSS3 Core & Flexbox), Session 4.3 (Tailwind CSS).
- **Yêu cầu 2 (Độ phân giải Lesson):** Bên trong mỗi Session mới được chia nhỏ, phải tách biệt từng `lesson`. Không gộp chung chuỗi. VD: 
  - `{"lesson_id": "L1", "title": "Cơ bản về Flexbox", "expected_output": "Sinh viên căn giữa được các phần tử..."}`
  - `{"lesson_id": "L2", "title": "CSS Grid", "expected_output": "Sinh viên tạo được layout 12 cột..."}`
- **Yêu cầu 3 (Xử lý các bài Thực hành/Project):** Nếu PM muốn có các bài thi thực hành hoặc làm Project, hãy tách chúng ra thành một `Session` riêng biệt, đặt tên Session có chứa từ khóa "Thực hành" hoặc "Project", và **XÓA TOÀN BỘ** mảng `lessons` bên trong Session đó theo đúng quy định số 4 của hệ thống.
- **Yêu cầu 4 (Bổ sung Output):** Viết rõ `expected_output` cho từng bài học nhỏ để định hướng cho AI Generator.

## 5. 🛑 Kết Luận (Verdict)
- **[REJECTED]** - Cấu trúc JSON và sự phân bổ tải trọng nhận thức (Cognitive Load) đang vi phạm nghiêm trọng các tiêu chuẩn sư phạm và kỹ thuật của hệ thống. Yêu cầu PM đập đi xây lại cấu trúc mảng `lessons` và phân bổ lại thời lượng học tập trước khi đưa vào Automated Pipeline.
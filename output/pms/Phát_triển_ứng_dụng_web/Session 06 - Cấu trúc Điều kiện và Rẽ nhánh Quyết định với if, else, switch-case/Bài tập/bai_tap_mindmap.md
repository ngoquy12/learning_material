# <center>[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) - Session 06</center>

### **1. Mục tiêu**
- Hệ thống hóa toàn bộ kiến thức cốt lõi về cấu trúc điều kiện (`if`, `else if`, `else`), câu lệnh rẽ nhánh nhiều trường hợp (`switch-case`), và toán tử điều kiện ba ngôi (Ternary Operator) trong JavaScript.
- Trực quan hóa cấu trúc dữ liệu, luồng rẽ nhánh quyết định và các lỗi chống mẫu (Anti-patterns) thường gặp bằng Sơ đồ Tư duy (Mindmap).
- Vận dụng tư duy phân tầng logic vào lĩnh vực Quản lý Check-in Hàng không (**AIRLINE_CHECKIN**), rèn luyện khả năng thiết kế hệ thống xử lý logic chuyên nghiệp và chuẩn hóa quy trình đào tạo nhân sự mới (Onboarding).

### **2. Bối cảnh & Vấn đề**
Bạn đang đảm nhận vai trò **Kỹ sư Lập trình Hệ thống Hàng không (Airline System Software Engineer)** tại một hãng hàng không quốc tế. Hệ thống làm thủ tục chuyến bay (**AIRLINE_CHECKIN**) đang chuẩn bị nâng cấp module xử lý logic quyết định: tính phí hành lý quá cước, định tuyến trạng thái check-in của hành khách và phân loại luồng ưu tiên lên tàu bay (Boarding Gate Priority).

Để đào tạo cho các lập trình viên mới gia nhập dự án (Onboarding), bạn được giao nhiệm vụ thiết kế một **Sơ đồ Tư duy (Mindmap)** tổng hợp toàn bộ kiến thức điều kiện rẽ nhánh của Session 06, kết hợp với tài liệu giải trình **`summary.md`** mô phỏng kiến trúc xử lý logic cho hệ thống AIRLINE_CHECKIN.

---

### **3. Quy tắc nghiệp vụ**

Sơ đồ tư duy và tài liệu tổng hợp BẮT BUỘC phải thể hiện rõ 3 khối kiến thức trọng tâm cùng với các kịch bản nghiệp vụ thuộc lĩnh vực **AIRLINE_CHECKIN**:

```                                SESSION 06: CẤU TRÚC ĐIỀU KIỆN & RẼ NHÁNH QUYẾT ĐỊNH
                                                         │
         ┌───────────────────────────────────────────────┼───────────────────────────────────────────────┐
         ▼                                               ▼                                               ▼
  [LESSON 01: IF / ELSE IF / ELSE]               [LESSON 02: SWITCH - CASE]                 [LESSON 03: TERNARY OPERATOR]
  - Tính phí hành lý ký gửi quá cước              - Mã trạng thái vé / Cửa ra tàu bay        - Gán nhãn ưu đãi & Lối đi ưu tiên
  - Bẫy thứ tự điều kiện (Khoảng giá trị)        - Bẫy trôi lệnh (Fall-through / Missing break) - Bẫy lồng ghép toán tử (Nested Ternary)
  - Khối lệnh Scope {} & Thụt lề Clean Code      - Giá trị mặc định (default case)          - Biểu thức gán trực tiếp 1 dòng
```

# **Nhánh 1: Cấu trúc Điều kiện `if`, `else if`, `else` (Lesson 01)**
- **Kiến thức cốt lõi:**
  - Cú pháp và luồng thực thi từ trên xuống dưới của khối `if ... else if ... else`.
  - Quy tắc sắp xếp thứ tự điều kiện: Kiểm tra từ khoảng điều kiện chi tiết / hẹp nhất đến khoảng điều kiện bao quát / rộng hơn.
  - Tầm quan trọng của khối ngoặc nhọn `{}` để giới hạn phạm vi khối lệnh (Scope) và quy chuẩn căn lề 2 spaces.
- **Áp dụng nghiệp vụ AIRLINE_CHECKIN:**
  - *Bài toán tính phí hành lý quá cước:* 
    - Nếu hành lý `> 30kg`: Áp dụng phí 400.000 VNĐ + Yêu cầu xác nhận của Quản lý ca (Supervisor Approval).
    - Nếu hành lý `> 20kg` (và `<= 30kg`): Áp dụng phí 150.000 VNĐ tiêu chuẩn.
    - Còn lại (`<= 20kg`): Miễn phí hành lý ký gửi (Phí = 0 VNĐ).
- **Các bẫy lỗi cần làm nổi bật (Anti-patterns):**
  - **Bẫy 1 (Sai thứ tự điều kiện):** Đặt điều kiện bao quát `weight > 20` lên trước `weight > 30` khiến cho khối `weight > 30` không bao giờ được chạm tới.
  - **Bẫy 2 (Thiếu khối ngoặc nhọn `{}`):** Viết lệnh không có `{}` khiến câu lệnh thứ 2 bị văng ra khỏi khối điều kiện và luôn thực thi ngoài ý muốn.

#### **Nhánh 2: Câu lệnh Rẽ nhánh Nhiều Trường hợp `switch-case` (Lesson 02)**
- **Kiến thức cốt lõi:**
  - Cú pháp `switch (expression)` và So sánh bằng nghiêm ngặt (`===`).
  - Vai trò bắt buộc của từ khóa `break` để thoát khỏi khối lệnh rẽ nhánh.
  - Khối xử lý mặc định `default` khi giá trị không khớp với bất kỳ `case` nào.
- **Áp dụng nghiệp vụ AIRLINE_CHECKIN:**
  - *Bài toán xử lý Mã trạng thái Check-in của hành khách (`checkInStatusCode`):*
    - `Case 1`: "Đã đặt chỗ - Chưa Check-in"
    - `Case 2`: "Đã Check-in Trực tuyến (Online Check-in Completed)"
    - `Case 3`: "Đã Xử lý Hành lý tại Quầy (Baggage Dropped)"
    - `Case 4`: "Đã Qua Cửa An ninh (Security Cleared)"
    - `Case 5`: "Đã lên máy bay (Boarded)"
    - `Default`: "Trạng thái không hợp lệ - Cần kiểm tra lại hệ thống"
- **Các bẫy lỗi cần làm nổi bật (Anti-patterns):**
  - **Lỗi trôi lệnh (Fall-through Bug):** Quên từ khóa `break;` ở các `case` khiến chương trình tự động chạy tiếp tục xuống câu lệnh của `case` phía dưới.
  - So sánh không đồng nhất kiểu dữ liệu (vd: so sánh String `"1"` với Number `1`).

#### **Nhánh 3: Biểu thức Điều kiện Ba ngôi - Ternary Operator (Lesson 03)**
- **Kiến thức cốt lõi:**
  - Cú pháp toán tử 3 ngôi: `condition ? expressionIfTrue : expressionIfFalse`.
  - Mục đích sử dụng: Gán giá trị biểu thức trực tiếp cho hằng số/biến trên một dòng lệnh ngắn gọn và sạch sẽ.
- **Áp dụng nghiệp vụ AIRLINE_CHECKIN:**
  - Gán thẻ lối đi ưu tiên qua Cửa An ninh dựa trên hạng vé VIP hoặc Thương gia: 
    - `const boardingLane = (isVipPassenger || isBusinessClass) ? "Lối đi Ưu tiên Fast-Track" : "Lối đi Phổ thông";`
- **Các bẫy lỗi cần làm nổi bật (Anti-patterns):**
  - **Bẫy lồng ghép ba ngôi (Nested Ternary Operator):** Lồng 3-4 tầng ba ngôi liên tiếp `a ? b : c ? d : e ? f : g` gây rối mắt, vi phạm tiêu chuẩn Clean Code, gây khó khăn cho việc bảo trì và bảo mật ứng dụng.

---

### **4. Yêu cầu bài toán (Sản phẩm nộp)**

Học viên phải hoàn thiện và đóng gói bài nộp gồm **3 thành phần chính**:

1. **File sơ đồ tư duy dạng hình ảnh (`.png` hoặc `.jpg`):**
   - Đảm bảo độ phân giải cao, rõ nét, dễ đọc.
   - Thể hiện đầy đủ 3 nhánh kiến thức tương ứng 3 bài học và áp dụng đúng ngữ cảnh `AIRLINE_CHECKIN`.
2. **File thiết kế sơ đồ gốc (`.xmind`, `.drawio`, `.pdf` hoặc link Canva/EdrawMind công khai):**
   - Lưu trữ bản chỉnh sửa kỹ thuật để Mentor kiểm tra cấu trúc phân cấp (Nodes hierarchy).
3. **Bản tóm tắt giải trình hệ thống `summary.md` (Định dạng Markdown):**
   - Trình bày tóm lược luồng tư duy kiến trúc rẽ nhánh trong hệ thống Check-in Hàng không.
   - Phân tích chi tiết 3 ví dụ minh họa bằng mã nguồn JavaScript (Good practice vs Bad practice) áp dụng trực tiếp bài toán AIRLINE_CHECKIN theo đúng nội dung học trong tuần.

---

### **5. Yêu cầu nộp bài**

Học viên nộp bài theo quy chuẩn Git / GitHub chuyên nghiệp:
* Tạo GitHub Repository với cấu trúc tên chuẩn: `[Tên Lớp]_[Môn Học]_Session06_Mindmap`
  *(Ví dụ: `HN_JV240304_Core_Session06_Mindmap` hoặc `HNKS25CNTT1_Core_Session06_Mindmap`)*
* Thư mục bài nộp trên GitHub bao gồm:

```text
  ├── mindmap.png (hoặc mindmap.jpg)
  ├── mindmap_source.xmind (hoặc file gốc tương đương)
  └── summary.md (Bản thuyết minh tổng hợp kiến thức & ví dụ mã nguồn JavaScript)
```

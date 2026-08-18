### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
- **Sơ đồ tư duy / Luồng xử lý (10 điểm)**: Vẽ hoặc diễn giải đúng luồng rẽ nhánh điều kiện cho cả 3 chức năng trước khi viết mã.
- **Xác định điều kiện biên (10 điểm)**: Xác định chính xác các điểm ranh giới điều kiện (ví dụ: đúng 20kg, 30kg, 40kg; trường hợp mã hạng vé không nằm từ 1-4).

#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
- **Chức năng 1 - Cấu trúc if/else-if/else (15 điểm)**:
  - Viết chuẩn xác thứ tự so sánh từ nhỏ đến lớn hoặc từ lớn đến nhỏ.
  - Sử dụng đầy đủ khối ngoặc nhọn `{}` cho các nhánh lệnh.
- **Chức năng 2 - Cấu trúc switch-case (15 điểm)**:
  - Áp dụng chuẩn xác cú pháp `switch (ticketClassCode)`.
  - Có đầy đủ từ khóa `break;` ở cuối mỗi nhánh `case`, không bị lỗi trôi lệnh.
  - Khai báo và xử lý trường hợp ngoại lệ với khối `default`.
- **Chức năng 3 - Toán tử Ba ngôi (10 điểm)**:
  - Đặt đúng cú pháp `dieu_kien ? gia_tri_1 : gia_tri_2`.
  - Gán trực tiếp biểu thức vào hằng số/biến trên 1 dòng đơn giản, không lồng ghép ba ngôi phức tạp gây khó đọc.

#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
- **Bẫy trôi lệnh switch-case (10 điểm)**: Đảm bảo kiểm thử tất cả các trường hợp hạng vé đều dừng đúng case mong muốn, không nhảy tràn sang case phía dưới.
- **Bẫy thứ tự logic trong if-else (10 điểm)**: Không đảo ngược điều kiện dẫn đến việc câu lệnh bị bỏ qua vô lý (ví dụ: kiểm tra `>= 20` trước `>= 40` khiến nhánh `>= 40` không bao giờ chạy tới được).

#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
- **Đặt tên biến & Căn lề chuẩn (10 điểm)**: Sử dụng kiểu `camelCase` đúng ngữ nghĩa tiếng Anh (`baggageWeight`, `ticketClassCode`, `isVipMember`), căn lề thụt lề chuẩn 2 spaces.
- **Đóng gói & Cấu trúc thư mục (10 điểm)**: Đặt tên thư mục nộp bài chuẩn quy định `[Tên Lớp]_[Môn Học]_Session06_Demo`, mã nguồn chạy thành công không có lỗi cú pháp trên Console.
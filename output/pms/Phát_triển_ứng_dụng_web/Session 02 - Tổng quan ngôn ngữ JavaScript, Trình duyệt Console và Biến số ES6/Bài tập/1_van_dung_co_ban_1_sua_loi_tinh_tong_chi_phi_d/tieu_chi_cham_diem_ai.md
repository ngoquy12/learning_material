# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng mã nguồn thực hiện phép cộng chuỗi `baseFeeInput + specialistFeeInput` chưa ép kiểu trong file `app.js`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ các dòng còn thiếu trong bảng Test Case chứng minh kết quả bị nối chuỗi sai so với thực tế kỳ vọng.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng hàm `Number()` để ép kiểu dữ liệu từ `prompt()` sang kiểu số, giúp phép tính tổng tiền khám bệnh chính xác.
*   **[20 điểm] Sử dụng Template Literals chuẩn ES6:** Chuyển đổi mã nguồn ghép chuỗi bằng toán tử `+` sang cú pháp Template Literals `${...}` minh bạch, dễ bảo trì.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Thực hiện chuyển đổi kiểu dữ liệu một cách minh bạch ngay tại bước nhập liệu hoặc bước tính toán số học.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo chương trình chạy mượt mà trên môi trường trình duyệt console mà không xảy ra lỗi runtime hay đứt gãy luồng thực thi.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được lý do hàm `prompt()` trong JavaScript luôn trả về giá trị kiểu String và cơ chế ép kiểu ngầm định (implicit coercion) của toán tử `+`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến chuẩn camelCase, mã nguồn tuân thủ tiêu chuẩn ES6 (`let`/`const`), thụt lề nhất quán.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex1`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu định dạng hiển thị:** Định dạng lại hiển thị số tiền có dấu phân cách hàng nghìn hoặc kiểm tra tính hợp lệ của dữ liệu đầu vào.

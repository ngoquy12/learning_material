# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi ưu tiên tính toán tổng hóa đơn phòng khách sạn — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng biểu thức bị lỗi thứ tự ưu tiên toán tử trong hàm `calculate_booking_invoice`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành chính xác 2 hàng còn thiếu trong bảng Test Case (tính đúng kết quả mã lỗi Buggy Output, Expected Output và giải thích rõ nguyên nhân sai do ưu tiên phép nhân `*` trước phép cộng `+`).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa biểu thức tính toán sử dụng đúng cặp dấu ngoặc đơn `()` để nhân tỉ lệ thuế trên toàn bộ tổng tiền phòng và phụ thu check-in sớm.
*   **[20 điểm] Kiểm chuẩn giá trị tính toán:** Kết quả trả về từ hàm khớp chính xác 100% với công thức tài chính chuẩn: `(room_rate * num_nights + early_checkin_fee) * (1.0 + tax_rate)`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra kiểu dữ liệu của số đêm (`int`), giá phòng và phụ phí (`float`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo không xảy ra lỗi tràn số hoặc tính toán số âm khi nhập các thông số hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao toán tử `*` có độ ưu tiên cao hơn toán tử `+` trong Python và tác dụng bắt buộc của dấu ngoặc `()` trong việc thay đổi thứ tự thực hiện biểu thức.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ chuẩn PEP 8 (indentation 4 space, snake_case cho tên biến/hàm, type hints đầy đủ).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub theo đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết đoạn mã kiểm thử đơn giản sử dụng từ khóa `assert` để tự động kiểm tra tính đúng đắn của hàm `calculate_booking_invoice` với 3 bộ dữ liệu test case.

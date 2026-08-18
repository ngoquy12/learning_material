### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính tổng tiền hóa đơn order tại quầy Highlands POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác các dòng lệnh nhận dữ liệu từ `input()` thiếu ép kiểu `int()` và dòng thực hiện phép cộng số học bị biến thành phép nối chuỗi.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác thông tin cho các hàng Test Case 2 và 3 trong bảng (bao gồm Input, Buggy Output, Expected Output, Dòng lỗi và Giải thích).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Thực hiện chuyển đổi kiểu dữ liệu thành công (`int(input(...))`) giúp chương trình thực hiện đúng phép cộng số học thay vì nối chuỗi.
*   **[20 điểm] Xử lý xuất dữ liệu chuẩn định dạng:** Hiển thị kết quả hóa đơn ra màn hình console trực quan, đúng số tiền và kèm đơn vị "VNĐ".

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng dữ liệu đầu vào:** Đảm bảo mã nguồn chuyển đổi đúng các số nguyên dương nhập vào từ bàn phím.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Mã nguồn ngắn gọn, cấu trúc mạch lạc, tránh xung đột về kiểu dữ liệu khi thực hiện xuất chuỗi kết hợp biến số (`print("...", final_amount, "VNĐ")` hoặc f-string).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được sự khác biệt giữa kiểu `str` và kiểu `int` trong Python, giải thích tại sao hàm `input()` luôn trả về `str` và rủi ro của việc nối chuỗi ngoài ý muốn trong ứng dụng thực tế.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng theo tiêu chuẩn Python (`base_price`, `topping_total_price`, `final_amount`), có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub theo đúng cấu trúc tên thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết mã kiểm thử tự động:** Viết thêm đoạn script kiểm thử đơn giản sử dụng các giá trị đầu vào cố định để xác minh tính đúng đắn của phép tính mà không cần nhập tay nhiều lần.
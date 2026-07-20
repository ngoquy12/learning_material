### **Tiêu chí chấm điểm (AI)**
**[Khắc phục lỗi logic tính phí Fintech] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:**
    *   Chỉ ra được lỗi sai độ ưu tiên toán tử tại câu lệnh điều kiện `if tx.balance < tx.amount + fee or not tx.is_active and tx.amount > 100:` (Giải thích được do toán tử `and` có mức độ ưu tiên cao hơn `or`).
    *   Chỉ ra được lỗi bỏ qua kiểm tra hạn mức do so sánh chuỗi phân biệt hoa thường (`tx.card_type == "Standard"`) trong khi đầu vào chuẩn hóa chưa được áp dụng đồng bộ.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:**
    *   Cung cấp đủ và đúng 3 Test Cases theo mẫu bảng HTML.
    *   Mô tả chi tiết các giá trị Input (ví dụ: giao dịch 50 USD, `is_active=False` nhưng hệ thống vẫn duyệt) và làm rõ sự khác biệt giữa kết quả đầu ra thực tế lỗi và đầu ra mong muốn.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:**
    *   Sửa lỗi độ ưu tiên toán tử bằng cách sử dụng dấu ngoặc đơn `()` hợp lý hoặc tách cấu trúc điều kiện để chặn ngay tài khoản không hoạt động trước khi thực hiện các so sánh khác.
    *   Đồng bộ hóa việc so khớp và kiểm tra hạn mức thẻ không phân biệt chữ hoa, chữ thường bằng phương thức xử lý chuỗi (ví dụ: `.upper()` hoặc `.capitalize()`).
*   **[20 điểm] Trả về chính xác HTTP Status Code và Exception:**
    *   Ném ra `HTTPException` với mã lỗi `400 Bad Request` khi hạng thẻ không hợp lệ hoặc giao dịch vượt quá hạn mức thẻ.
    *   Ném ra đúng lỗi `400 Bad Request` khi tài khoản bị khóa hoặc số dư không đủ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:**
    *   Chặn các trường hợp số tiền giao dịch (`amount`) nhỏ hơn hoặc bằng 0 và trả về lỗi phù hợp.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:**
    *   Xử lý trường hợp chuỗi gửi lên rỗng hoặc chứa ký tự khoảng trắng dư thừa (sử dụng phương thức `.strip()`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:**
    *   Sinh viên giải thích được quy tắc độ ưu tiên giữa các toán tử logic (`not`, `and`, `or`) trong Python và viết được biểu thức rút gọn hoặc tối ưu cho các cấu trúc điều kiện phức tạp.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:**
    *   Code viết rõ ràng, sạch sẽ, tuân thủ đúng quy tắc PEP 8 (sử dụng khoảng trắng thụt lề chuẩn, đặt tên biến theo định dạng snake_case).
*   **[5 điểm] Tuân thủ nộp bài GitHub:**
    *   Tạo repository và đẩy mã nguồn lên đúng cấu trúc thư mục quy định: `[Tên Lớp]_PythonCore_Session02_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:**
    *   Học viên viết kèm một file kiểm thử tự động sử dụng `pytest` hoặc `TestClient` của FastAPI đại diện cho 3 test case đã liệt kê ở phần báo cáo để kiểm tra tính đúng đắn của mã nguồn mới.
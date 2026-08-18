### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi tính phụ phí và xác thực ưu đãi đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng mã khai báo biểu thức `is_discount_approved` bị sai thiếu dấu ngoặc đơn gây hiểu sai độ ưu tiên toán tử logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ các dòng còn thiếu trong bảng Test Case (tối thiểu 3 test cases) phân tích rõ Buggy Output vs Expected Output và giải thích nguyên nhân do độ ưu tiên của toán tử `and` cao hơn `or`.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng cặp dấu ngoặc đơn `(loyalty_points >= 500 or is_promo_event) and num_nights >= 2` để đảm bảo nhóm điều kiện ưu đãi được đánh giá đúng trước khi kết hợp với số đêm.
*   **[20 điểm] Tính toán chính xác phụ phí và tổng tiền:** Giữ nguyên các phép tính phụ thu số học `is_early_checkin * room_rate * 0.3` và tổng thanh toán đúng chuẩn nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate kiểu dữ liệu đúng chuẩn:** Đảm bảo các biến kiểu `int`, `float`, `bool` được khởi tạo và ép kiểu/tính toán an toàn không gây ra lỗi `TypeError`.
*   **[10 điểm] Bắt lỗi giá trị không hợp lệ:** Đảm bảo biểu thức tính toán không bị treo/lỗi khi giá trị số đêm hoặc giá phòng bằng 0 hoặc số âm.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn trong comment hoặc báo cáo về quy tắc độ ưu tiên toán tử trong Python: Toán tử số học (`*`, `/`) -> Toán tử so sánh (`>=`, `<`) -> Toán tử `and` -> Toán tử `or`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến tuân thủ snake_case, có type hints rõ ràng, trình bày code chuẩn PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository theo đúng tên thư mục yêu cầu: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Script kiểm thử tự động:** Viết các câu lệnh `assert` hoặc mã kiểm thử tự động xác nhận tính đúng đắn của biểu thức sau khi sửa lỗi cho toàn bộ 3 test cases.
### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi tính tổng tiền hóa đơn POS Highlands Coffee — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng mã nguồn tính `subtotal` gặp sự cố do ưu tiên toán tử phép nhân `*` thực hiện trước phép cộng `+`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ và chính xác 2 dòng Test Case còn trống (STT 2 và STT 3) với thông số Buggy Output, Expected Output và giải thích nguyên nhân rõ ràng.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh công thức tính toán sử dụng cặp ngoặc đơn `()` chính xác: `subtotal = (BASE_PRICE_SIZE_S + is_size_l * SIZE_L_EXTRA + topping_count * TOPPING_PRICE) * quantity`.
*   **[20 điểm] Đảm bảo giới hạn kiến thức bài học:** Tính toán chính xác số tiền giảm giá và tổng tiền cuối cùng dựa hoàn toàn vào toán tử số học/logic, tuyệt đối không dùng câu lệnh rẽ nhánh `if/else` hoặc các cấu trúc bị cấm.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Ép kiểu đầu vào an toàn:** Ép kiểu từ `input()` sang `int` đúng quy chuẩn cho tất cả các biến số lượng và cờ lựa chọn.
*   **[10 điểm] Định dạng hiển thị kết quả:** In rõ ràng các thành phần thông tin hóa đơn (Tổng tiền gốc, Tiền giảm giá, Thành tiền thanh toán) kèm đơn vị "VNĐ".

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn cơ chế ưu tiên toán tử trong Python (Operator Precedence) và lý do tại sao biểu thức chứa toán tử nhân số học với biến kiểu boolean/số nguyên (`is_gold * DISCOUNT_RATE_GOLD`) giúp thay thế câu lệnh điều kiện `if/else` trong bài tập này.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng bằng tiếng Anh (snake_case), viết ghi chú thích bằng tiếng Việt có dấu chuẩn sản xuất, tuân thủ PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session04_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản kiểm thử tự động:** Viết thêm file mã nguồn Python độc lập thực hiện tự động hóa các bộ test case để kiểm tra tính đúng đắn của công thức hóa đơn.
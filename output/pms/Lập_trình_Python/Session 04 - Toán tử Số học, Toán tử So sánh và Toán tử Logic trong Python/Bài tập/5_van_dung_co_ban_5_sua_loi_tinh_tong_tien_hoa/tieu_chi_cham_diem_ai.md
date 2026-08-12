### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính tổng tiền hóa đơn POS Highlands Coffee — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng tính toán `raw_total = (base_price + 10000) * is_size_l + topping_count * 8000` bị lỗi thứ tự toán tử và đóng mở ngoặc sai.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ các dòng Test Case 2 và Test Case 3 trong bảng báo cáo kiểm thử với các giá trị Buggy Output và Expected Output chính xác.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa biểu thức số học thành `raw_total = base_price + is_size_l * 10000 + topping_count * 8000` hoặc biểu thức tương đương đúng về mặt toán học.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng đúng các kiểu dữ liệu `float` cho giá tiền, `int` cho số lượng/cờ nhị phân (0 hoặc 1), tính toán chính xác số tiền giảm giá và tiền thanh toán cuối cùng.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ép kiểu dữ liệu `float()` và `int()` hợp lệ từ bàn phím cho các biến `base_price`, `is_size_l`, `topping_count`, `is_gold_member`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Chương trình không bị ngắt đột ngột khi nhập đúng định dạng số, tính toán đúng khi `is_size_l = 0` hoặc `is_gold_member = 0`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được vì sao biểu thức ban đầu lại nhân cả `base_price` với `is_size_l` và cách ưu tiên toán tử trong Python (phép nhân `*` có độ ưu tiên cao hơn phép cộng `+`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến theo chuẩn `snake_case`, có bình luận giải thích dòng mã sạch sẽ, không chứa câu lệnh bị cấm như `if/else`.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm đoạn mã kiểm thử tự động so sánh kết quả tính toán với giá trị mong đợi bằng biểu thức so sánh `==` hiển thị `True`/`False` mà không dùng `if`.
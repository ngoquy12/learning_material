### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính tổng tiền hóa đơn đơn hàng Highlands POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng mã tính toán `final_total` vi phạm thứ tự ưu tiên toán tử số học (`*` thực hiện trước `+`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền chính xác 100% dữ liệu cho Test Case 2 và Test Case 3 trong bảng báo cáo (tính đúng cả Buggy Output và Expected Output).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa biểu thức tính toán thành công bằng cách sử dụng dấu ngoặc đơn `(base_price + topping_count * topping_price)` để nhóm tổng tiền hàng trước khi nhân với hệ số giảm giá `(1 - is_gold_member * discount_rate)`.
*   **[20 điểm] Tuân thủ giới hạn kiến thức (Phạm vi Session 04):** Không sử dụng `if/else`, không dùng hàm `def`, không sử dụng cấu trúc dữ liệu phức tạp. Chỉ dùng toán tử số học và biểu thức logic cơ bản.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Thực hiện ép kiểu dữ liệu từ chuỗi nhập vào (`input()`) sang `float` và `int` an toàn, không bị lỗi cú pháp.
*   **[10 điểm] Xử lý cờ boolean chính xác:** Xử lý chuỗi nhập cho `is_gold_member_str` chính xác bằng phép so sánh logic để thu được giá trị kiểu `bool` (`True`/`False`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế ép kiểu ngầm định của Python khi thực hiện phép nhân giữa số thực/số nguyên với biến kiểu `bool` (`True` tương đương 1, `False` tương đương 0).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết đúng chuẩn PEP 8 (thụt lề 4 dấu cách, tên biến dạng `snake_case`, chú thích bằng tiếng Việt rõ ràng).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session04_Ex1`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu hóa biểu thức ngắn gọn:** Viết biểu thức tính toán hiển thị chi tiết số tiền giảm giá riêng biệt (`discount_amount`) và số tiền tổng thanh toán (`final_total`) mà vẫn không cần dùng `if/else`.
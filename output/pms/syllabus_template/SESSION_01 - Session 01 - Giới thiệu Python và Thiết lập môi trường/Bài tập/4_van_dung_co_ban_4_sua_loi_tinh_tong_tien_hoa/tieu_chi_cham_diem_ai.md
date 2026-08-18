### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính tổng tiền hóa đơn POS khi xử lý kiểu dữ liệu đầu vào — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code gán biến `topping_count` thiếu hàm ép kiểu số `int()` hoặc `float()` và dòng code tính toán thực hiện phép cộng giữa kiểu dữ liệu `float` với `str`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ thông tin cho các hàng 2 và 3 trong bảng Test Case với đầy đủ 6 cột thông tin (Input, Buggy Output, Expected Output, Failing Line, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công việc ép kiểu `int(input(...))` hoặc `float(input(...))` cho `topping_count`, tính toán đúng tiền đồ uống, tiền topping và tổng tiền hóa đơn.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Định dạng dữ liệu đầu ra rõ ràng, in đúng cấu trúc hóa đơn thanh toán không phát sinh lỗi crash `TypeError` khi thực thi.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ép kiểu thích hợp cho tất cả dữ liệu đầu vào từ bàn phím (`unit_price`, `quantity`, `size_extra`, `topping_count`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo toàn bộ các phép toán nhân/cộng chi phí diễn ra chính xác giữa các kiểu dữ liệu số (`int`, `float`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được bản chất hàm `input()` trong Python luôn trả về dữ liệu kiểu `str` và hệ quả của phép toán nhân chuỗi (`str * int`) cũng như phép cộng giữa `str` và số.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến đặt chuẩn snake_case tiếng Anh (`drink_subtotal`, `topping_subtotal`, `total_amount`), có nhận xét/chú thích mã nguồn bằng tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub theo đúng cấu trúc thư mục đã quy định (`[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex4`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết kịch bản kiểm thử tự động với nhiều trường hợp dữ liệu (ví dụ: số topping = 0, size extra = 0) để kiểm tra tính đúng đắn của công thức tính tiền.
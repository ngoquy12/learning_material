### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính toán hóa đơn đơn hàng E-Commerce — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng 9 (`total_goods_cost = raw_price * int(raw_quantity)`) làm nhân bản chuỗi và dòng 10 (`final_payment = total_goods_cost + raw_shipping_fee`) gây ghép chuỗi thay vì cộng số học.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp đủ bảng báo cáo với ít nhất 3 kịch bản kiểm thử làm rõ sự khác biệt giữa Buggy Output và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Ép kiểu thành công `float(raw_price)`, `int(raw_quantity)`, `float(raw_shipping_fee)` và tính toán chính xác giá trị hóa đơn tài chính.
*   **[20 điểm] Định dạng console chuyên nghiệp:** Xuất dữ liệu console chuẩn xác với tham số `sep=" - "` ở dòng tiêu đề và `sep=": "`, `end=" VND\n"` ở dòng kết quả.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ngăn chặn ứng dụng dừng đột ngột khi người dùng nhập chuỗi trống hoặc ký tự không hợp lệ.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Triển khai khối `try - except ValueError` bắt lỗi chuyển đổi kiểu dữ liệu và in thông báo hướng dẫn nhập số hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao hàm `input()` trong Python mặc định luôn trả về kiểu `str` và rủi ro tài chính của việc ghép chuỗi âm thầm trong các hệ thống E-Commerce thương mại.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết sạch sẽ, tuân thủ chuẩn PEP 8 (thụt lùi 4 khoảng trắng, đặt tên biến dạng `snake_case`, comment làm rõ logic bằng tiếng Việt).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn đúng cấu trúc tên thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex01`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm đoạn mã tự động kiểm thử nhiều giá trị đầu vào mà không cần người dùng nhập tay liên tục từ bàn phím.
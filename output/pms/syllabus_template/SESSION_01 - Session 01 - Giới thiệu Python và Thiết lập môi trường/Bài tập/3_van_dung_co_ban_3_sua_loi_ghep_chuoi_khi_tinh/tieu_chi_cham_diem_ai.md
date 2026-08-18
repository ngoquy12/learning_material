### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi ghép chuỗi khi tính hóa đơn bán hàng POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
* **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã nguồn `total_payment = str(drink_subtotal) + str(topping_subtotal)` là nguyên nhân gây ra hiện tượng ghép chuỗi ngoài ý muốn.
* **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác thông tin cho các hàng STT 2 và STT 3 (bao gồm Buggy Output, Expected Output, Failing Line và Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
* **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa lại phép tính tổng tiền thanh toán theo đúng quy tắc số học `total_payment = drink_subtotal + topping_subtotal`.
* **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Thực hiện chuyển đổi kiểu dữ liệu từ `input()` thành số nguyên (`int`) một cách hợp lệ trước khi thực hiện các phép tính nhân/cộng.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
* **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo mã nguồn nhận dữ liệu từ `input()` mà không gây ra lỗi ngắt chương trình đột ngột khi nhập đúng định dạng số.
* **[10 điểm] Bắt lỗi an toàn hệ thống:** Hiển thị hóa đơn thanh toán đầy đủ các thông tin gồm tiền nước, tiền topping và tổng tiền một cách rõ ràng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
* **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được sự khác nhau của toán tử `+` khi áp dụng với kiểu dữ liệu `str` (ghép chuỗi) và kiểu dữ liệu `int`/`float` (cộng số học) trong Python.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng, tuân thủ chuẩn snake_case của Python, viết comment bằng tiếng Việt có dấu đúng ngữ cảnh.
* **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng theo cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
* **[10 điểm] Viết Unit Test tự động:** Định dạng hiển thị kết quả số tiền thanh toán có dấu phân cách hàng nghìn (ví dụ: `106,000 VNĐ`) để tăng tính chuyên nghiệp cho giao diện POS.
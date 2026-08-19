# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi tính hóa đơn thanh toán tại quầy POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
* **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng mã nguồn nhận dữ liệu từ `input()` nhưng không thực hiện ép kiểu, dẫn đến dòng tính `unit_price` và `total_payment` bị xử lý dạng chuỗi.
* **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu 2 trường hợp Test Case còn thiếu (STT 2 và STT 3), thể hiện rõ kết quả lỗi hiện tại và kết quả kỳ vọng đúng.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
* **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng hàm `int()` hoặc `float()` để chuyển đổi `base_price`, `size_fee`, và `quantity` sang kiểu số trước khi thực hiện tính toán.
* **[20 điểm] Tính toán chính xác đơn giá và tổng tiền:** Đơn giá 1 ly và Tổng tiền thanh toán được tính toán chính xác tuyệt đối theo đúng công thức số học: $\text{unit\_price} = \text{base\_price} + \text{size\_fee}$ và $\text{total\_payment} = \text{unit\_price} \times \text{quantity}$.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
* **[10 điểm] Ép kiểu an toàn dữ liệu số:** Chuyển đổi dữ liệu từ `input()` sang số nguyên (`int`) một cách hợp lý cho đơn giá và số lượng ly.
* **[10 điểm] Định dạng đầu ra thông tin rõ ràng:** Xuất kết quả thanh toán trên CLI theo đúng yêu cầu bài toán, có kèm đơn vị tính "VNĐ" rõ ràng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
* **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao hàm `input()` trong Python 3 luôn trả về kiểu `str` và sự khác biệt giữa phép toán `+`, `*` trên kiểu `str` so với kiểu `int`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết rõ ràng, đặt tên biến chuẩn tiếng Anh (`base_price`, `size_fee`, `quantity`), chú thích bằng tiếng Việt có dấu.
* **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
* **[10 điểm] Định dạng tiền tệ đẹp mắt:** Sử dụng định dạng chuỗi Python (f-string) để hiển thị số tiền có dấu phân cách hàng nghìn (ví dụ: `102,000 VNĐ` hoặc `102.000 VNĐ`).

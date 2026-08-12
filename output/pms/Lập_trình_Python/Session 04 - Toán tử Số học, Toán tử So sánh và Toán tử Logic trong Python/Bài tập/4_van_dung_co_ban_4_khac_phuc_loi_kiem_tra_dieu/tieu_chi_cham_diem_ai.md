### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Khắc phục lỗi kiểm tra điều kiện ưu đãi hóa đơn POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng mã nguồn kiểm tra điều kiện `is_eligible_discount = is_gold and (gross_total >= 100000)` sử dụng sai toán tử logic `and` thay vì `or`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành chính xác dữ liệu chạy vết cho STT 2 và STT 3 trong bảng HTML Test Case, thể hiện rõ sự khác biệt giữa Buggy Output và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công biểu thức kiểm tra thành `is_gold or (gross_total >= 100000)`. Kết quả tính toán tổng tiền gốc, số tiền giảm giá và số tiền thực thanh toán đạt chính xác 100% cho mọi trường hợp.
*   **[20 điểm] Tuân thủ ràng buộc kiến thức:** Tính toán thành công số tiền giảm giá bằng cách nhân trực tiếp giá trị Boolean với biểu thức số học (`gross_total * 0.10 * is_eligible_discount`), tuyệt đối không sử dụng câu lệnh `if/else`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ép kiểu chính xác cho dữ liệu đầu vào `float()` cho giá tiền và `int()` cho số lượng topping.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý chuỗi nhập vào `is_gold_input` sang Boolean an toàn (`is_gold_input == "True"` hoặc so sánh không phân biệt hoa thường đơn giản).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ cơ chế chuyển đổi ngầm định của kiểu `bool` thành `int` (`True` tương đương 1, `False` tương đương 0) khi thực hiện phép nhân toán tử số học trong Python.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến chuẩn Tiếng Anh (`base_price`, `size_upcharge`, `topping_count`, `gross_total`, `net_total`), mã nguồn có chú thích logic rõ ràng bằng Tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`HNKS25CNTT1_Core_Session04_Ex4`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Giải pháp tối ưu:** Viết mã nguồn ngắn gọn, tối ưu biểu thức tính toán không bị dư thừa dấu ngoặc và có định dạng hiển thị tiền tệ đẹp mắt (`:.0f` VNĐ).
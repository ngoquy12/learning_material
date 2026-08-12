### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế Mô đun Khai báo và Tính toán Hóa đơn Bán hàng Tự động trên Hệ thống POS — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:**
    *   Định nghĩa đầy đủ, rõ ràng danh sách tham số đầu vào và đầu ra cho bài toán POS.
    *   Xác định chính xác kiểu dữ liệu (`int`, `float`, `str`, `bool`) và đơn vị tính cho từng biến.
    *   Bảng Schema minh bạch, chuyên nghiệp, thể hiện được các cờ logic (flags) phục vụ tính toán không cần `if`.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):**
    *   Phát hiện tối thiểu 3 bẫy dữ liệu nghiệp vụ thực tế (ví dụ: Khách đưa thiếu tiền, số lượng topping âm, cờ chọn size bất hợp lệ).
    *   Giải thích cơ chế dùng toán tử so sánh/logic để tạo biến kiểm định trạng thái bẫy dữ liệu (`is_valid_payment`, `is_valid_topping`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):**
    *   Cung cấp sơ đồ Mermaid minh họa chính xác luồng xử lý từ Input -> Phụ thu -> Chiết khấu -> VAT -> Output.
    *   Tuân thủ tuyệt đối quy ước 5 hình dạng chuẩn: Oval cho Start/End, Hình bình hành cho Input/Output, Hình chữ nhật cho Phép tính/Xử lý dữ liệu, Hình thoi cho Kiểm tra logic điều kiện.
*   **[10 điểm] Thiết kế vòng đời tính năng:**
    *   Mô tả rõ ràng thứ tự ưu tiên toán tử trong việc áp dụng mã giảm giá và thuế VAT (Chiết khấu phần trăm -> Chiết khấu cố định -> Thuế VAT).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:**
    *   Tính chính xác tiền phụ thu size (Size M +6k, Size L +10k) bằng biểu thức số học kết hợp Boolean (ví dụ: `is_size_m * 6000 + is_size_l * 10000`).
    *   Tính chính xác chiết khấu Thẻ Vàng 10% và Mega Voucher 15.000 VNĐ bằng toán tử logic `and`, `or`, `not` thuần túy.
*   **[15 điểm] Xử lý lọc và tính toán nâng cao:**
    *   Tính chính xác thuế VAT 8% và số tiền thừa trả lại cho khách hàng (`cash_given - final_total`).
    *   Không vi phạm bất kỳ phạm vi cấm nào (không dùng `if/else`, `for/while`, `def`, `class`, `list`, `dict`).

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:**
    *   Tạo các cờ kiểm định Boolean (`is_order_valid`) xác nhận toàn bộ đơn hàng hợp lệ dựa trên kết hợp các điều kiện biên.
    *   Xuất thông điệp trạng thái kiểm tra (Hợp lệ: True/False) trực tiếp ra giao diện console hóa đơn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Quy chuẩn Python:**
    *   Mã nguồn tuân thủ PEP 8: Đặt tên biến snake_case bằng Tiếng Anh có ý nghĩa (`base_price`, `is_gold_member`, `topping_count`).
    *   Viết chú thích code (comments) bằng Tiếng Việt rõ ràng, giải thích công thức toán học/logic được sử dụng.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:**
    *   Cấu trúc thư mục nộp bài chính xác theo định dạng yêu cầu.
    *   Có file hướng dẫn hoặc giải thích tóm tắt thiết kế trong phần báo cáo/nộp bài.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế In Hóa đơn & Auditing tự động:**
    *   Định dạng hóa đơn đầu ra đẹp mắt bằng chuỗi nhiều dòng (`f-string` hoặc căn lề) hiển thị chi tiết từng khoản tiền (Tiền gốc, Tiền phụ thu, Tiền giảm giá, VAT, Tiền khách đưa, Tiền thừa) mà chỉ dùng duy nhất các hàm `print()` nối tiếp.
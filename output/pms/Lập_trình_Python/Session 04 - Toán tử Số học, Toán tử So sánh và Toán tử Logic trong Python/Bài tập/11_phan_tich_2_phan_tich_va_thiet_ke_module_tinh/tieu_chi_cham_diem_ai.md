### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Phân tích và Thiết kế Module Tính Tiền Hóa Đơn Trà Sữa POS Không Dùng Câu Lệnh Rẽ Nhánh — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Đề xuất đầy đủ 2 phương án xử lý logic tính toán theo điều kiện mà không dùng lệnh `if/else`.
    *   *Phương án 1*: Tận dụng tính chất Boolean trong Python (`True` tương đương 1, `False` tương đương 0 khi thực hiện phép tính số học) để nhân trực tiếp hệ số phụ thu và giảm giá.
    *   *Phương án 2*: Sử dụng các phép toán so sánh trả về kết quả `bool` kết hợp ép kiểu `int()` hoặc toán tử logic `and`/`or` để bật/tắt các giá trị cộng thêm.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Tạo bảng so sánh HTML/Markdown đầy đủ 5 tiêu chí (Tốc độ, Bộ nhớ, Độ bảo trì, Độ đọc, Ngữ cảnh áp dụng).
    *   Đánh giá chính xác ưu/nhược điểm từng phương án. Thấu hiểu tác động của việc không dùng `if/else` đến tính dễ đọc của mã nguồn.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Lý giải thuyết phục lý do chọn phương án tối ưu dựa trên tiêu chuẩn mã nguồn sạch (Clean Code), tính đơn giản và hiệu năng tính toán tuyến tính trong Python core.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu (Mermaid):**
    *   Vẽ lưu đồ Mermaid đúng cú pháp, áp dụng chuẩn 5 hình khối:
        *   Terminator: `([Bắt đầu])` / `([Kết thúc])`
        *   Input/Output: `[/Nhập base_price, is_size_m, is_size_l, topping_count, is_gold_member/]`
        *   Process: `["Tính surcharge_size = is_size_m * 6000 + is_size_l * 10000"]`, `["Tính subtotal = base_price + surcharge_size + topping_count * 8000"]`, `["Tính discount = subtotal * 0.10 * is_gold_member"]`, `["Tính final_total = subtotal - discount"]`
        *   Decision: `Kiểm tra (subtotal >= 30000) and (topping_count <= 5)?`
        *   Flowline: các mũi tên liên kết logic rõ ràng.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Viết code Python hoàn chỉnh, sử dụng đúng kiến thức Session 04 (toán tử số học, so sánh, logic, ép kiểu).
    *   Không vi phạm phạm vi cấm: Tuyệt đối không dùng `if`, `else`, `elif`, `for`, `while`, `list`, `dict`, `def`, `class`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Tính chính xác phụ thu size (ví dụ: `size_surcharges = is_size_m * 6000 + is_size_l * 10000`).
    *   Tính chính xác phụ thu topping (`topping_count * 8000`).
    *   Tính chính xác mức giảm giá (`discount_amount = subtotal * 0.10 * is_gold_member`).
    *   Tính cờ hợp lệ chính xác: `is_valid_order = (subtotal >= 30000) and (topping_count <= 5)`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu POS Receipt:**
    *   In kết quả rõ ràng, chuyên nghiệp dưới dạng hóa đơn POS gồm: Giá đồ uống gốc, Phụ thu Size, Tiền Topping, Tổng tiền hàng (Subtotal), Tiền giảm giá (Discount), Tổng tiền thanh toán (Final Total), và Trạng thái hợp lệ (Is Valid Order).
    *   Chuyển đổi kiểu dữ liệu chính xác khi in (ví dụ: định dạng float/int hợp lý).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến 100% bằng Tiếng Anh chuẩn PEP 8 (snake_case) (ví dụ: `base_price`, `is_size_m`, `topping_count`, `subtotal`, `final_price`).
    *   Chú thích giải thích bằng Tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub hợp lệ, đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Phân tích mở rộng nâng cao:**
    *   Biểu diễn thêm phương án tự động kiểm tra xem khách chọn đồng thời cả 2 Size M và L (dữ liệu sai lệch `is_size_m == 1 and is_size_l == 1`) và gắn cờ cảnh báo lỗi nhập liệu `has_input_error` chỉ bằng toán tử logic `and`/`or`/`==` mà không dùng `if`.
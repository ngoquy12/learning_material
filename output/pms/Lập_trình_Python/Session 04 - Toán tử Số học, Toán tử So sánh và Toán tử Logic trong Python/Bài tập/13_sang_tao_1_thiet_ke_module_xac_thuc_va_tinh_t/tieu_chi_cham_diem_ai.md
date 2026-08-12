### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế Module Xác thực và Tính toán Hóa đơn POS Trà sữa — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, rõ ràng danh sách tham số đầu vào (tối thiểu 5 thông số: đơn giá, số lượng, chọn size M/L, số topping, trạng thái thẻ Vàng) và kết quả đầu ra (tổng phụ thu, giảm giá, tổng thanh toán, cờ hợp lệ) với đúng kiểu dữ liệu (`int`, `float`, `bool`).
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê đúng và chi tiết tối thiểu 03 trường hợp biên nghiệp vụ (ví dụ: số lượng <= 0 hoặc > 50; số lượng topping < 0; tổng tiền < 100.000 VNĐ nhưng khách cố tình áp mã giảm giá). Giải thích được cơ chế chặn lỗi bằng toán tử logic/số học.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện đầy đủ chu trình dữ liệu từ lúc nhập dữ liệu từ quầy POS đến khi tính toán và in kết quả.
*   **[10 điểm] Tuân thủ quy chuẩn sơ đồ Mermaid:** Sử dụng chính xác 100% các ký hiệu hình khối (Stadium cho Start/End, Parallelogram cho Input/Output, Rectangle cho Process/Calculation, Diamond cho Decision). Không vi phạm lỗi dùng sai hình chữ nhật hoặc hình bình hành.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chính xác phụ thu size (Size M +6.000, Size L +10.000), phụ thu topping (+8.000/phần) và tổng chi phí đơn hàng trước giảm giá bằng các toán tử số học và logic.
*   **[15 điểm] Tính toán giảm giá không dùng lệnh điều khiển:** Áp dụng sáng tạo biểu thức ép kiểu ép giá trị Boole hoặc nhân trực tiếp cờ logic (`is_gold_member and reaches_threshold`) để tính tiền giảm giá 10% mà KHÔNG sử dụng câu lệnh `if/else`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng cờ logic `is_valid_order` kết hợp đầy đủ các điều kiện hợp lệ thông qua toán tử `and`, `or`, `not` và in ra kết quả xác thực hợp lệ (`True`/`False`) rõ ràng cho thu ngân.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn Python:** Tên biến 100% bằng tiếng Anh (`base_price`, `is_gold_member`, `topping_count`), tuân thủ chuẩn `snake_case`. Có chú thích tiếng Việt rõ ràng. KHÔNG sử dụng bất kỳ từ khóa hoặc cấu trúc thuộc phạm vi cấm (`if`, `else`, `for`, `while`, `def`, `list`, `dict`).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session04_Ex13`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Tính toán thêm thông số phân tích hiệu quả đơn hàng (ví dụ: tính tỷ lệ % tiền giảm giá trên tổng hóa đơn, hoặc tính số điểm tích lũy quy đổi từ hóa đơn hợp lệ bằng toán tử `//`) mà hoàn toàn tuân thủ giới hạn kiến thức đã học.
### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế module kiểm định và tính hóa đơn phức hợp cho hệ thống Highlands POS — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự chủ thiết kế danh sách các biến Input/Output rõ ràng, có chỉ định kiểu dữ liệu (`int`, `float`, `bool`, `str`) và đơn vị đo lường phù hợp với bài toán POS.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Nhận diện xuất sắc ít nhất 3 kịch bản lỗi/biên nghiệp vụ trong thực tế (nhập số topping âm, đưa thiếu tiền thối, chọn sai mã size, áp dụng giảm giá khi không đủ hạn mức).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid minh họa chính xác luồng xử lý từ dữ liệu đầu vào đến đầu ra. Tuân thủ 100% quy chuẩn 5 dạng hình (Oval cho Terminator, Hình bình hành cho I/O, Hình chữ nhật cho Process, Hình thoi cho Decision, Mũi tên cho Flowline).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày mạch lạc logic tính tiền và cơ chế chuyển đổi các trạng thái kiểm định dạng Boolean.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chính xác tổng tiền đồ uống (giá gốc + phụ thu size + phụ thu topping), tính tiền giảm giá thành viên Vàng và tiền thừa trả khách mà hoàn toàn KHÔNG dùng câu lệnh rẽ nhánh `if/else`.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Xây dựng thành công các biểu thức logic phức hợp kết hợp các toán tử so sánh (`>=`, `==`, `!=`) và toán tử logic (`and`, `or`, `not`) để tạo ra các cờ trạng thái (vd: `is_order_valid`, `is_sufficient_cash`).

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng các toán tử số học/logic thông minh để vô hiệu hóa chiết khấu sai quy định hoặc gắn cờ cảnh báo đơn hàng bất hợp lệ khi dữ liệu đầu vào vi phạm kịch bản biên đã nêu.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn Python:** Mã nguồn viết theo chuẩn PEP 8, biến số bằng tiếng Anh dạng `snake_case` minh bạch, ghi chú tiếng Việt có dấu rõ ràng, không vi phạm giới hạn kiến thức (không dùng `def`, `class`, `if`, `for`, `while`, `list`, `dict`).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy mã nguồn và báo cáo thiết kế lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng thêm chỉ số cảnh báo rủi ro gian lận (Audit Flag) dựa trên biểu thức logic đa điều kiện (ví dụ: phát hiện đơn hàng có tiền thừa vượt quá 500.000 VNĐ hoặc số lượng topping bất thường).
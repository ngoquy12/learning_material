### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Phân hạng và Phân bổ Chăm sóc Khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Khai báo đầy đủ Type Hints cho Input và Output Data Schemas (sử dụng cú pháp modern Python 3.10+ như `dict[str, Any]`, `list[dict]`, `str | int | float`).
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Trình bày mã giả (Pseudocode) hoặc sơ đồ luồng (Flowchart) thể hiện chính xác các bước kiểm chuẩn dữ liệu, phân hạng và xử lý tràn bộ nhớ VIP trước khi lưu trữ.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Tổ chức dữ liệu đầu ra dạng Dictionary chứa các nhóm danh sách rõ ràng (`vip_customers`, `gold_customers`, `standard_customers`, `vip_overflow_queue`, `error_logs`).
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Xây dựng hàm phân hạng xử lý đúng các điều kiện logic phức tạp (kết hợp `AND`, `OR` giữa chi tiêu và điểm tương tác) để xếp hạng thành viên chính xác.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Phát hiện chính xác trùng lặp `customer_id` hoặc `email`; kiểm soát đúng hạn mức tối đa 3 khách hàng VIP và đẩy khách hàng thứ 4 trở đi vào danh sách chờ `vip_overflow_queue`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kiểm tra đầy đủ 5 tiêu chí hợp lệ dữ liệu (tiền tố `CUST_`, cấu trúc email, độ dài và số 0 đầu câu của số điện thoại, chi tiêu >= 0, điểm tương tác 0-100).

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Bắt các trường hợp lỗi dữ liệu không hợp lệ bằng `raise ValueError` và bắt lỗi trùng lặp/thiếu trường bằng ngoại lệ thích hợp mà không làm sập chương trình, ghi nhận đầy đủ vào `error_logs`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Định danh hoàn toàn bằng Tiếng Anh, tuân thủ PEP 8 (snake_case cho hàm/biến), comment giải thích bằng Tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub theo đúng định dạng tên thư mục được quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Triển khai hàm thống kê tổng quan (tổng doanh thu theo từng hạng thành viên VIP/Gold/Standard) với độ phức tạp tối ưu O(N) trong một lượt duyệt (single pass).
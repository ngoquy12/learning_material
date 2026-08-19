# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Mô hình Kiểm tra và Xử lý Chuỗi Mượn Trả Sách Tự động — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản lỗi thường gặp — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự xây dựng kịch bản kiểm duyệt chuỗi giao dịch mượn trả logic, định nghĩa rõ ràng dải đầu vào `range()`, các điều kiện kích hoạt `continue` (lỗi nhẹ) và `break` (lỗi nghiêm trọng).
*   **[15 điểm] Chủ động phát hiện sai sót dữ liệu (Edge Cases):** Phát hiện và mô tả phương án xử lý cho tối thiểu 3 trường hợp biên nghiệp vụ (như dải mã không hợp lệ, lỗi dừng xảy ra ngay vị trí đầu tiên, toàn bộ dải mã đều bị bỏ qua).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện đầy đủ vòng đời kiểm duyệt giao dịch mượn trả sách, tuân thủ đúng 100% chuẩn hình dạng (Oval cho Start/End, Parallelogram cho Input/Output, Diamond cho Điều kiện, Rectangle cho Xử lý).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày rõ ràng cơ chế chuyển đổi trạng thái khi gặp câu lệnh `continue`, `break` và luồng chạy vào khối `else` của vòng lặp `for`.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Viết mã nguồn Python thực hiện chính xác kịch bản đã tự thiết kế, kết hợp chuẩn xác vòng lặp `for`, `range()`, `if/elif/else`, `break`, `continue`, `else`.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Xử lý chính xác việc phân loại và in thông báo rõ ràng tương ứng với từng trạng thái giao dịch (thành công, bỏ qua do lỗi nhẹ, ngắt khẩn cấp do vi phạm an toàn). Tuyệt đối tuân thủ phạm vi kiến thức đã học, không vi phạm các từ khóa/kiến thức bị cấm (`while`, `list`, `dict`, `def`, `class`).

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các câu lệnh điều kiện kiểm tra (guards/validation) để xử lý an toàn các trường hợp biên dữ liệu đã đề xuất ở Phần 2 trước khi đưa vào vòng lặp kiểm duyệt.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Đặt tên biến hoàn toàn bằng tiếng Anh đúng chuẩn PEP 8 (`snake_case`), viết comment giải thích bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo đúng thư mục theo cấu trúc mẫu, mã nguồn chạy mượt mà không phát sinh lỗi cú pháp.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Tự tích hợp thêm biến đếm tổng số giao dịch xử lý thành công, tổng số giao dịch bị bỏ qua và xuất báo cáo tổng kết chi tiết trong khối `else` của vòng lặp `for`.

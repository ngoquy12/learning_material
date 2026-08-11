### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế Hệ thống Console Điều hướng và Quản lý Đơn hàng E-commerce — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa rõ ràng, hợp lý cấu trúc dữ liệu lưu trữ đơn hàng và kịch bản đầu vào/đầu ra cho các chức năng trong Console Menu.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 03 trường hợp biên hoặc xung đột trạng thái nghiệp vụ (ví dụ: nhập sai định dạng phím menu, vi phạm luồng chuyển trạng thái đơn hàng, áp dụng voucher không đủ điều kiện).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Cung cấp sơ đồ Mermaid minh họa chính xác luồng di chuyển dữ liệu từ thao tác Console người dùng đến các hàm xử lý logic.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Mô tả rõ ràng cơ chế quản lý trạng thái đơn hàng và nguyên lý điều phối luồng menu không sử dụng vòng lặp bị cấm (`while`, `break`, `continue`).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Viết mã nguồn Python chạy hoàn chỉnh giao diện Console tương tác, thực hiện đầy đủ các chức năng quản lý đơn hàng đã đề xuất.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Triển khai các thao tác truy vấn, tính toán tổng doanh thu, áp dụng giảm giá và cập nhật trạng thái đơn hàng chuẩn xác.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xử lý triệt để các tình huống dữ liệu sai hoặc thao tác menu không hợp lệ với thông báo lỗi rõ ràng, chuyên nghiệp trên giao diện Console.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn chia hàm rõ ràng, sử dụng Type Hints (Python 3.10+), tên hàm/biến bằng tiếng Anh chuẩn PEP 8. Không vi phạm các từ khóa lặp bị cấm.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định, có file `README.md` hướng dẫn chạy dự án chi tiết.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung chức năng ghi nhật ký thao tác (Audit Log) lưu lại thông tin thời gian và trạng thái thay đổi của từng đơn hàng.
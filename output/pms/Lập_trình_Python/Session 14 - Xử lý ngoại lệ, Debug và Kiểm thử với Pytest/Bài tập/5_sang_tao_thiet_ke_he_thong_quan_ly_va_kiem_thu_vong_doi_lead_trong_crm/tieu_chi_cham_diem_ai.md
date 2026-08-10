### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế Hệ thống Quản lý và Kiểm thử Vòng đời Lead trong CRM — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự chủ định nghĩa cấu trúc dữ liệu `Lead` đầy đủ các trường thông tin cần thiết (ID, Name, Email, Phone, Budget, Status, is_deleted, ...), thể hiện rõ kiểu dữ liệu sử dụng Type Hints hiện đại của Python 3.12.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện và mô tả rõ ràng tối thiểu 4 kịch bản lỗi biên (ví dụ: chuyển trạng thái từ LOST sang CONVERTED, nhập budget âm, trùng ID Lead, thao tác trên Lead đã bị Soft Delete).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác luồng di chuyển của dữ liệu qua các bước: nhận vào, kiểm tra hợp lệ, xử lý ngoại lệ, lưu trữ và Soft Delete.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ ràng cơ chế chuyển đổi giữa các trạng thái (State Machine) và logic quản lý xóa mềm / khôi phục dữ liệu.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Xây dựng hoàn chỉnh lớp `LeadManager` với các phương thức thêm mới, cập nhật trạng thái, xóa mềm và khôi phục Lead. Áp dụng chuẩn xác khối lệnh `try-except-else-finally`.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Đảm bảo các hàm truy vấn/tìm kiếm tự động loại bỏ các bản ghi đã xóa mềm (`is_deleted = True`) trừ khi có yêu cầu truy vấn lịch sử kiểm toán đặc biệt.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Khai báo và kích hoạt (`raise`) chính xác các Custom Exception (`LeadValidationError`, `InvalidStateTransitionError`, `LeadNotFoundError`) kèm thông báo lỗi chi tiết khi gặp kịch bản bất hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn tuân thủ PEP 8, đặt tên tiếng Anh chuẩn mực, chú thích tiếng Việt đầy đủ dấu.
*   **[5 điểm] Quy chuẩn nộp bài & Test Suite Pytest:** Tổ chức mã nguồn chuẩn xác, có file `test_crm_system.py` chạy qua 100% các test case của `pytest 8.3` (bao gồm kiểm tra `pytest.raises`). Đẩy bài lên GitHub đúng cấu trúc thư mục yêu cầu.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng thêm nhật ký ghi vết (Audit Log) theo dõi thời gian và người thực hiện thao tác khôi phục dữ liệu hoặc thay đổi trạng thái Lead.
### **Tiêu chí chấm điểm (AI)**
**[Thiết kế dòng lệnh tính toán diện tích và Soft Lock vị trí kho hàng] — Tổng điểm: 100 điểm**

#### **1. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 30 điểm**
*   **[15 điểm] Thiết kế luồng dữ liệu (Data Flow):** Mô tả chuẩn xác bằng Mermaid hoặc tài liệu các bước chuyển dịch dữ liệu từ chuỗi ký tự nhận từ `input()`, đi qua cổng ép kiểu dữ liệu đích (float, int, bool) đến khi tính toán ra các giá trị đo lường và trả về `print()`.
*   **[15 điểm] Thiết kế vòng đời tính năng (Feature Lifecycle):** Mô tả được cơ chế thiết lập trạng thái đóng/mở vị trí (Soft Lock) thông qua việc kết hợp các biểu thức logic so sánh thể tích và trạng thái bảo trì, làm rõ được việc ẩn/khóa cơ chế tiếp nhận mà không cần xóa vật lý bản ghi.

#### **2. Hiện thực hóa logic nghiệp vụ sáng tạo — 40 điểm**
*   **[20 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chính xác thể tích đơn chiếc, thể tích thuần và thể tích yêu cầu thực tế có cộng thêm tỷ lệ dự phòng theo đúng công thức nghiệp vụ được đề ra.
*   **[20 điểm] Xử lý lọc dữ liệu nâng cao (Toán tử logic không rẽ nhánh):** Xây dựng thành công biểu thức logic kết hợp (`and`, `not`, so sánh `<=`) để quyết định giá trị boolean cho biến phê duyệt nhập kho, thay thế hoàn toàn được cấu trúc điều kiện `if-else`.

#### **3. Kiểm chuẩn dữ liệu, Chặn lỗi dị biệt nâng cao — 20 điểm**
*   **[10 điểm] Xử lý ngoại lệ nghiệp vụ lặp trạng thái:** Ép kiểu bảo trì tối ưu, chuyển đổi thành công đầu vào chuỗi "1" hoặc các ký tự khác thành kiểu boolean đúng bản chất logic.
*   **[10 điểm] Validate dữ liệu và Chống tràn:** Định dạng chuẩn chỉ số thập phân (lấy đúng 2 chữ số sau dấu phẩy bằng cú pháp `:.2f` trong f-string) ngăn chặn việc hiển thị chuỗi float vô hạn gây tràn dòng hiển thị trên Terminal.

#### **4. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Biến số đặt tên tiếng Anh hoặc tiếng Việt rõ nghĩa theo chuẩn snake_case (ví dụ: `chieu_dai`, `ty_le_du_phong`, `is_approved`), mã nguồn có ghi chú (comment) phân tách rõ ràng các bước: Nhập liệu - Xử lý tính toán - Xuất báo cáo.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc đúng thư mục quy định `[Tên Lớp]_[Môn Học]_Session01_Ex05`, có file README.md hướng dẫn chi tiết cách chạy chương trình.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore (Phục hồi) dữ liệu:** Bổ sung tính năng mô phỏng việc khôi phục trạng thái vị trí bị đầy bằng cách thiết lập công thức tính toán thể tích trống còn lại sau khi trừ đi thể tích lô hàng hiện tại, kiểm tra xem vị trí đó có thể khôi phục trạng thái trống (trực quan hóa bằng một cờ boolean phụ `is_restorable` hiển thị ra màn hình).
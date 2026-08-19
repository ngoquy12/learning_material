# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Động cơ Phân loại và Tự động hóa Check-in Hàng không — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Khai báo đầy đủ các biến đầu vào (`ticketClass`, `baggageWeight`, `bookingStatusCode`, `isVip`) và biến tổng hợp đầu ra có cấu trúc mạch lạc, đúng kiểu dữ liệu.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê chính xác tối thiểu 3 trường hợp biên (Ví dụ: `baggageWeight < 0`, `bookingStatusCode` nằm ngoài dải 1-4, `ticketClass` không thuộc Eco/Deluxe/Business) và nêu rõ hướng xử lý.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid hoàn chỉnh thể hiện chính xác các bước kiểm tra từ tiếp nhận dữ liệu -> phân loại trạng thái -> tính phí hành lý -> gán nhãn ưu tiên -> xuất kết quả.
*   **[10 điểm] Chuẩn hóa hình khối Mermaid:** Tuân thủ 100% quy chuẩn hình khối (Oval cho Bắt đầu/Kết thúc, Bình hành cho I/O, Hình thoi cho Điều kiện, Chữ nhật cho Thao tác/Tính toán).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** 
    *   Sử dụng `switch-case` chính xác cho mã trạng thái đặt chỗ (có từ khóa `break` và trường hợp `default`).
    *   Sử dụng `if...else` phân cấp tính chính xác phí quá cước hành lý theo từng hạng vé.
    *   Sử dụng toán tử ba ngôi `?:` ngắn gọn, chuẩn mực để gán nhãn ưu tiên `boardingZone` và phí chọn ghế.
*   **[15 điểm] Xử lý tổng hợp chi phí:** Tính đúng tổng chi phí phụ thu `totalExtraFee = extraBaggageFee + seatSelectionFee` và hiển thị kết quả phân loại chi tiết ra màn hình CLI qua `console.log`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các khối điều kiện bảo vệ (Guard Clauses) ở đầu chương trình để phát hiện dữ liệu sai (như trọng lượng âm hoặc mã trạng thái hủy) và in thông báo lỗi rõ ràng trước khi tính toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Tên biến/hằng số 100% bằng Tiếng Anh (camelCase chuẩn ES6+), ghi chú giải thích logic bằng Tiếng Việt có dấu, căn lề chuẩn 2 spaces.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo đúng thư mục bài tập theo định dạng `[Tên Lớp]_[Môn Học]_Session06_Ex14` trên GitHub.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung biến lưu vết lịch sử kiểm duyệt (`auditLogMessage`) tổng hợp tóm tắt nguyên nhân chấp nhận hoặc từ chối lượt check-in để phục vụ công tác truy vết sau chuyến bay.

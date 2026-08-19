# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Hệ thống Quét và Kiểm định Luồng Mượn Trả Sách Thư viện — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản lỗi thường gặp — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự xây dựng bộ tham số đầu vào (dải mã `start_id`, `end_id`, quy tắc xác định lỗi nhẹ và lỗi an ninh) và đầu ra console trực quan, đáp ứng đúng yêu cầu nghiệp vụ LIBRARY_WMS.
*   **[15 điểm] Chủ động phát hiện sai sót dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 trường hợp lỗi biên hợp lý (ví dụ: dải quét rỗng, số ngày mượn nhập vào không hợp lệ, sự cố an ninh xảy ra ngay tại mã đầu tiên).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác tiến trình duyệt `range()`, xử lý `continue`, `break` và khối `else`. Tuân thủ đúng 5 dạng hình tiêu chuẩn (Oval, Parallelogram, Rectangle, Diamond, Arrow).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ ràng cơ chế hoạt động của khối `else` đi kèm vòng lặp `for` và lý do `else` không chạy khi gặp `break`.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chuẩn xác tiền phạt quá hạn 5.000 VNĐ/ngày cho các trường hợp mượn trên 14 ngày bằng câu lệnh rẽ nhánh và các phép toán cơ bản.
*   **[15 điểm] Điều khiển luồng lặp sáng tạo:** Áp dụng đúng cú pháp `break`, `continue` và khối `else` của vòng lặp `for` để thể hiện trọn vẹn kịch bản quét kiểm định thư viện.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các điều kiện validate kiểm tra dữ liệu đầu vào (ví dụ: `start_id <= end_id`), in thông báo cảnh báo phù hợp mà không làm ứng dụng sập đột ngột.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn phạm vi:** Đặt tên biến tiếng Anh dạng `snake_case`, ghi chú thích logic đầy đủ bằng Tiếng Việt có dấu. TUYỆT ĐỐI KHÔNG dùng `while`, `def`, `list`, `dict`, `tuple`, `set`, `class`.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session08_Ex15`, các commit rõ ràng, trình bày báo cáo sạch đẹp.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Tích hợp thành công biến đếm độc lập để thống kê tổng số phiếu hợp lệ đã xử lý, tổng tiền phạt thu được trong ca quét và số phiếu bị bỏ qua mà chỉ sử dụng biến đơn giản.

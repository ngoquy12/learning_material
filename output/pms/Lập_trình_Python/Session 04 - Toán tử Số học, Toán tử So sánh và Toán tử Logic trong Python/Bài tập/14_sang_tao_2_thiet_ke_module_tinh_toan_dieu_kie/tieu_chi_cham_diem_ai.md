# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết Kế Module Tính Toán Điều Kiện Đặt Phòng Khách Sạn — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, hợp lý danh sách các biến Input/Output phù hợp với nghiệp vụ hệ thống đặt phòng khách sạn, có gán kiểu dữ liệu chuẩn (`int`, `float`, `bool`).
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 trường hợp biên nghiệp vụ (như giờ check-in ngoài khoảng 0-24, số lượng khách nhỏ hơn hoặc bằng 0, số ngày hủy cọc là số âm) và giải thích nguyên nhân xung đột dữ liệu.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid minh họa chính xác vòng đời dữ liệu. Tuân thủ 100% quy tắc sử dụng hình dạng chuẩn (Oval cho Start/End, Parallelogram cho I/O, Rectangle cho Process).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày rõ ràng cơ chế tính toán phụ phí và cờ logic thông qua thứ tự ưu tiên của toán tử.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chính xác các cờ Boolean (`is_early_checkin`, `is_full_refund_eligible`, `is_child_free`, `is_over_capacity`) bằng toán tử so sánh và toán tử logic.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Tính toán chính xác số tiền phụ phí (check-in sớm, phụ phí người phát sinh) dựa hoàn toàn vào công thức toán tử số học đại số kết hợp giá trị Boolean mà không dùng lệnh `if/else`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng cờ kiểm tra tính hợp lệ dữ liệu tổng hợp `is_valid_booking_data` để xác nhận toàn bộ tham số đầu vào nằm trong phạm vi cho phép.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn trình bày sạch sẻ, tuân thủ PEP 8, đặt tên biến tiếng Anh chuẩn xác, ghi chú bằng tiếng Việt có dấu đầy đủ.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session04_Ex14`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Thiết kế thêm các chỉ số đánh giá doanh thu dự kiến hoặc tỷ lệ phạt hủy phòng tính theo phần trăm cọc một cách sáng tạo và tối ưu.

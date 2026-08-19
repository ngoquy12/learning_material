# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế phân hệ tính phụ phí và xác thực điều kiện đặt phòng khách sạn — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Khai báo đầy đủ, hợp lý các biến đầu vào và đầu ra cho phân hệ đặt phòng khách sạn với kiểu dữ liệu chuẩn (`int`, `float`, `str`, `bool`) và Type Hints chính xác.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích và chỉ ra tối thiểu 3 trường hợp biên hoặc dữ liệu bất hợp lệ thực tế (giờ check-in sai, đơn giá không hợp lệ, số tuổi âm...), có đề xuất hướng biểu diễn kiểm tra bằng toán tử so sánh.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid chính xác, mô tả chi tiết luồng xử lý từ dữ liệu đầu vào đến kết quả tính toán. Tuân thủ 100% quy chuẩn 5 hình dạng chuẩn (Oval, Parallelogram, Rectangle, Diamond, Arrow).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày rõ ràng trình tự tính toán phụ phí, kiểm tra điều kiện hoàn tiền và hợp lệ hóa dữ liệu đặt phòng.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chính xác phụ thu check-in sớm (30%), chi phí người phát sinh và kiểm tra hoàn tiền cọc (hủy trước >= 3 ngày) bằng toán tử số học và toán tử so sánh.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Biểu diễn các điều kiện kiểm tra dữ liệu dưới dạng các biến cờ Boolean (`bool`) nguyên bản mà không vi phạm phạm vi cấm (không dùng `if/else`, không dùng `and/or/not`, không dùng `list/dict`).

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng các biểu thức so sánh kiểm tra tính hợp lệ của dữ liệu đầu vào (ví dụ: `is_valid_checkin_time = checkin_hour >= 0`, `is_valid_price = room_price > 0`) và in ra màn hình trạng thái xác thực.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Đặt tên biến/hàm 100% bằng Tiếng Anh chuẩn snake_case, mã nguồn sạch đẹp, có Type Hints đầy đủ, tuân thủ chuẩn PEP 8.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục đúng định dạng quy định `[Tên Lớp]_[Môn Học]_Session04_Ex13`, có tệp README mô tả giải pháp thiết kế.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Đề xuất hoặc cài đặt thêm biểu thức tính toán chỉ số tài chính mở rộng (ví dụ: tính toán tỷ lệ phần trăm tiền cọc được hoàn lại, mã hóa trạng thái đơn đặt phòng dưới dạng mã số kiểm toán).

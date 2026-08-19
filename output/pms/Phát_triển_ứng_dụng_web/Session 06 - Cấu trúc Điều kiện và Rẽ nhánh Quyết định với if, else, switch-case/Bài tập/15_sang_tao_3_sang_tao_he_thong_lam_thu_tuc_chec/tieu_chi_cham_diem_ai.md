# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Sáng tạo hệ thống làm thủ tục check-in và tính phí hành lý hàng không — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ các biến Input/Output mô tả chi tiết thông tin hành khách (PassengerProfile), vé (FlightTicket), hành lý (BaggageInfo) và kết quả phụ thu.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện và mô tả rõ ràng giải pháp xử lý cho ít nhất 3 kịch bản lỗi biên nghiệp vụ (ví dụ: trọng lượng âm, mã trạng thái vé bất hợp lệ, mã vị trí ghế không tồn tại).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác vòng đời xử lý làm thủ tục.
*   **[10 điểm] Thiết kế hình khối chuẩn Mermaid:** Tuân thủ 100% quy tắc hình khối (Stadium cho Bắt đầu/Kết thúc, Parallelogram cho Input/Output, Diamond cho Decision, Rectangle cho Process).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Kết hợp chính xác `if-else`, `switch-case` và toán tử ba ngôi để tính toán phí cước hành lý (50.000 VNĐ/kg quá cước) và phí chọn vị trí ghế.
*   **[15 điểm] Tối ưu hóa cấu trúc rẽ nhánh:** Mã nguồn được tổ chức mạch lạc, thứ tự kiểm tra điều kiện hợp lý, không bị lỗi lặp logic hoặc lọt điều kiện.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết mã nguồn kiểm tra dữ liệu đầu vào (Guard Clauses) để ngắt chương trình hoặc đưa ra thông báo lỗi thích đáng khi gặp dữ liệu không hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn ES6+:** Sử dụng `const`/`let`, đặt tên biến/hằng số bằng tiếng Anh theo quy chuẩn CamelCase, comment bằng Tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đặt tên thư mục nộp bài đúng mẫu `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex15`, mã nguồn chạy thành công không có lỗi cú pháp.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung logic ghi nhật ký (Audit Log) theo dõi lịch sử thay đổi trạng thái check-in và tính tổng doanh thu thu thêm từ phí dịch vụ của chuyến bay.

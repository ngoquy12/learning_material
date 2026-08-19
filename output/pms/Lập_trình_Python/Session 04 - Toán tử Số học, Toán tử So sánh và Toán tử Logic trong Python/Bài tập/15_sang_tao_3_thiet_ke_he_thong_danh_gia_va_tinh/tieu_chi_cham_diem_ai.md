# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế Hệ thống Đánh giá và Tính Phụ phí Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, rõ ràng danh sách biến đầu vào và đầu ra kèm Type Hints chính xác phản ánh đúng nghiệp vụ đặt phòng homestay/khách sạn.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê tối thiểu 3 kịch bản dữ liệu biên (Edge Cases) thực tế trong ngành du lịch/khách sạn và nêu giải pháp xử lý phù hợp với giới hạn kiến thức bài học.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện rõ ràng luồng xử lý từ dữ liệu thô đến kết quả tổng hóa đơn thanh toán. Tuân thủ 100% quy chuẩn 5 dạng hình (Terminator, Input/Output, Decision, Process, Flowline).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày được tiến trình tính toán logic nguyên tử từ tính tiền gốc, phụ thu đến cờ xác nhận phê duyệt đặt phòng.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chính xác tổng tiền phòng, phụ thu nhận phòng sớm và phụ thu khách vượt chuẩn theo đúng quy tắc nghiệp vụ đã đưa ra.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Xây dựng biểu thức đại số và so sánh để xác định cờ phê duyệt đặt phòng (`is_booking_approved`) và cờ đạt tiêu chuẩn cọc mà không dùng lệnh rẽ nhánh `if/else`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xử lý thành công các bẫy dữ liệu đã nêu ở Phần 1 bằng toán tử số học/so sánh trực tiếp, đảm bảo chương trình không bị tính toán sai lầm hoặc ra kết quả vô lý.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết bằng Python 3.12, định danh hoàn toàn bằng tiếng Anh, ghi chú giải thích logic bằng tiếng Việt có dấu, tuân thủ chuẩn PEP 8.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đóng gói mã nguồn đúng cấu trúc thư mục quy định, kèm file README mô tả thiết kế và hướng dẫn chạy chương trình.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng thêm biểu thức đại số xuất ra chỉ số phân tích hiệu suất phòng (ví dụ: tỷ lệ tiền phụ thu / tổng chi phí hóa đơn dạng %, chỉ số cảnh báo rủi ro bồi thường cọc) chỉ bằng các toán tử đã học.

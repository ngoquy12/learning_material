### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Phân hệ Quản lý Đặt phòng Động và Chuẩn hóa JSON Payload — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc dữ liệu Object đặt phòng đầy đủ các trường thông tin tiêu chuẩn, trường phụ thu động và trường nhạy cảm; thể hiện rõ cấu trúc trước và sau khi làm sạch/đóng gói JSON.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Nhận diện ít nhất 3 bẫy dữ liệu thực tế (như sai cú pháp khi dùng Dot Notation cho key có ký tự đặc biệt, lỗi lãng phí bộ nhớ do dùng `undefined` thay cho `delete`, lỗi thao tác thuộc tính trực tiếp trên chuỗi JSON chưa được parse).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác vòng đời dữ liệu từ khởi tạo đối tượng, cập nhật dynamic property, xóa dữ liệu nhạy cảm, đến serialization và deserialization JSON.
*   **[10 điểm] Thiết kế quy chuẩn Mermaid:** Tuân thủ 100% quy chuẩn hình dạng node trong sơ đồ Mermaid (Oval cho Bắt đầu/Kết thúc, Chữ nhật cho Xử lý, Bình hành cho Đầu vào/Đầu ra, Hình thoi cho Điều kiện).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Thực hiện chính xác thao tác thêm/cập nhật phụ phí đặt phòng (`early-checkin-fee`, phụ thu người phát sinh) bằng Bracket Notation và Dynamic Key Access.
*   **[15 điểm] Chuẩn hóa và Đóng gói JSON Payload:** Sử dụng đúng từ khóa `delete` để loại bỏ hoàn toàn các trường nhạy cảm (`tempToken`, `paymentGatewayPin`) trước khi chuyển đổi bằng `JSON.stringify` và giải mã phục hồi chính xác bằng `JSON.parse`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng câu lệnh kiểm tra (guards) hoặc logic an toàn để ngăn chặn các bẫy dữ liệu đã liệt kê ở Phần 2 trong mã nguồn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết sạch sẻ, định danh biến/hàm bằng tiếng Anh rõ nghĩa (`bookingReservation`, `earlyCheckinFee`, `sanitizeBookingPayload`), chú thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session12_Ex14` kèm tệp Readme giải thích luồng hoạt động.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Viết thêm hàm mô phỏng việc kiểm thử tự động (Audit Log) so sánh dung lượng/danh sách key của Object trước và sau khi sanitize để chứng minh các trường nhạy cảm đã bị xoá hoàn toàn khỏi bộ nhớ.
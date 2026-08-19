# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế mô-đun nhập liệu và xuất hóa đơn POS linh hoạt cho chuỗi Highlands POS — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Đề xuất được sơ đồ dữ liệu Đầu vào / Đầu ra chi tiết, xác định chính xác kiểu dữ liệu (`str`, `int`, `float`) cho từng trường thông tin nghiệp vụ hóa đơn POS.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Xác định đủ và chính xác ít nhất 3 kịch bản bẫy dữ liệu (nhập số âm, sai kiểu dữ liệu, giảm giá quá 100%...) kèm phân tích rủi ro tương ứng.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ đúng sơ đồ Mermaid thể hiện luồng xử lý hóa đơn. Tuân thủ nghiêm ngặt 5 dạng hình khối tiêu chuẩn (Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Process, Diamond cho Decision).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày rõ ràng các bước chuyển đổi dữ liệu từ chuỗi nhập thô `input()` sang số học và định dạng thành tiền tệ xuất hóa đơn.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Lập trình mã nguồn Python thực thi chính xác các công thức tính đơn giá ly, tổng tiền hàng, tiền chiết khấu và tổng thanh toán.
*   **[15 điểm] Trình bày kết quả hóa đơn chuyên nghiệp:** Căn chỉnh giao diện xuất console dạng biên lai bán hàng đẹp mắt, dễ nhìn, sử dụng hợp lý các ký tự kẻ bảng/đường phân cách.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các câu lệnh ép kiểu an toàn hoặc thông báo hướng dẫn rõ ràng khi người dùng nhập dữ liệu không mong muốn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Đặt tên biến hoàn toàn bằng tiếng Anh theo chuẩn Clean Code, viết chú thích mã nguồn bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định và kèm tệp README mô tả chi tiết bài làm.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Auditing / Mã tra cứu hóa đơn:** Tự nghĩ ra thuật toán tạo mã tra cứu hóa đơn độc bản (Order Reference Code) dựa trên tên thu ngân, số tiền và thời gian/số thứ tự giao dịch.

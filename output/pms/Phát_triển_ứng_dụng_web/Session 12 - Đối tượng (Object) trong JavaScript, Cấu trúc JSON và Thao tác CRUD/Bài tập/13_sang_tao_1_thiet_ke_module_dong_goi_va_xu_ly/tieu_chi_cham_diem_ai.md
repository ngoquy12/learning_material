### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế Module Đóng gói và Xử lý Payload Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc đối tượng `BookingReservation` sáng tạo, hợp lý, đầy đủ thuộc tính cơ bản (id, customerName, basePrice) và thuộc tính có tên key chứa ký tự đặc biệt (ví dụ: `early-checkin-fee`, `extra-services`). Định nghĩa chuỗi JSON đầu ra minh bạch.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện và mô tả rõ ràng tối thiểu 3 bẫy lỗi kỹ thuật liên quan đến Object & JSON (Lỗi ReferenceError do truyền biến chưa khai báo vào Bracket Notation, lỗi SyntaxError do dùng Dot Notation cho key gạch ngang, lỗi giữ lại key ẩn do gán `undefined` thay vì dùng `delete`, hoặc lỗi khi parse JSON không đúng cú pháp).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid đúng cú pháp. Sử dụng chính xác 100% quy chuẩn hình dạng:
    *   Hình Stadium/Oval `([ ])` cho Start/End.
    *   Hình Bình hành `[/ /]` cho Input/Output.
    *   Hình Chữ nhật `[" "]` cho Process/Action (Tuyệt đối không dùng bình hành cho hành động xử lý).
    *   Hình Thoi `?` cho Decision.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày mạch lạc logic từng giai đoạn chuyển đổi dữ liệu từ đối tượng gốc -> đối tượng sau làm sạch -> chuỗi JSON đóng gói -> đối tượng phục hồi.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Mã nguồn JavaScript vận dụng linh hoạt Dot Notation cho key chuẩn và Bracket Notation cho key chứa ký tự đặc biệt. Thực hiện tính toán phụ thu check-in sớm hoặc phụ thu người ở thêm chính xác.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Sử dụng chuẩn xác từ khóa `delete` để xóa bỏ hoàn toàn các trường dữ liệu tạm thời/nhạy cảm (như `temp-token`, `secret-code`) trước khi thực hiện `JSON.stringify()`. Đảm bảo chuỗi JSON thu được hoàn toàn sạch sẽ.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các đoạn mã kiểm tra (Guard Clauses) hoặc xử lý an toàn nhằm ngăn ngừa các lỗi biên đã mô tả ở Phần 2 (ví dụ: kiểm tra sự tồn tại của thuộc tính trước khi parse hoặc truy cập dynamic key).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết bằng JavaScript ES6+, đặt tên biến/hàm 100% bằng Tiếng Anh (camelCase), chú thích giải thích logic bằng Tiếng Việt có dấu, mã nguồn phân chia hàm rõ ràng ngăn ngắn.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đóng gói thư mục đúng tên theo yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex13`, có file README.md mô tả dự án và hướng dẫn chạy file script.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng thêm hàm hỗ trợ sao lưu (Backup snapshot) đối tượng ban đầu trước khi xóa key nhạy cảm hoặc kiểm tra tính toàn vẹn của dữ liệu sau khi `JSON.parse()`.
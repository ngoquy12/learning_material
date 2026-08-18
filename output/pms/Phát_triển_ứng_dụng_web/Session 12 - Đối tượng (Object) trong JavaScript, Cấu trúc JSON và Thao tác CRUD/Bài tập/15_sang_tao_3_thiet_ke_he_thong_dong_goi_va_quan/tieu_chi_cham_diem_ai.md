### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết Kế Hệ Thống Đóng Gói Và Quản Lý Hóa Đơn Đặt Phòng Khách Sạn — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc dữ liệu Object đầy đủ các trường nghiệp vụ (mã đặt phòng, giá phòng, thông tin khách, thuộc tính tạm thời) và chuỗi JSON kết xuất chuẩn xác.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 bẫy lỗi nghiệp vụ/kỹ thuật (ví dụ: dùng sai Dot notation cho key có gạch ngang, nhầm lẫn giữa gán `undefined` và dùng `delete`, cố truy xuất thuộc tính trên chuỗi JSON chưa được `JSON.parse`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác vòng đời dữ liệu từ Object -> Thao tác CRUD -> Stringify -> Parse. Tuân thủ 100% quy chuẩn hình dạng Mermaid (Rectangle cho Process, Parallelogram CHỈ cho Input/Output, Diamond cho Decision, Oval cho Start/End).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích cơ chế biến đổi trạng thái của Object và quá trình đóng gói JSON minh bạch, logic.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Áp dụng chính xác quy tắc phụ thu check-in sớm, chính sách trẻ em và cập nhật thành công các thuộc tính bằng cả Dot Notation và Bracket Notation (truy cập dynamic key).
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Sử dụng từ khóa `delete` để loại bỏ hoàn toàn các trường dữ liệu tạm thời/nhạy cảm trước khi đóng gói bằng `JSON.stringify()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết mã nguồn kiểm tra hoặc truy xuất an toàn, tránh bị ngắt chương trình do ReferenceError hoặc SyntaxError khi xử lý Object và JSON.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Tên biến/hàm đặt bằng Tiếng Anh chuẩn camelCase (`roomPrice`, `earlyCheckInSurcharge`, `serializeInvoice`), giải thích logic bằng Tiếng Việt chuẩn.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo đúng thư mục bài tập theo cú pháp `[Tên Lớp]_[Môn Học]_Session12_Ex15` với file mã nguồn chạy độc lập thành công trên Node.js hoặc Browser Console.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Viết thêm mô-đun đối soát dữ liệu So sánh Object ban đầu và Object sau khi Parse từ JSON để phát hiện các thuộc tính đã bị loại bỏ (Audit log).
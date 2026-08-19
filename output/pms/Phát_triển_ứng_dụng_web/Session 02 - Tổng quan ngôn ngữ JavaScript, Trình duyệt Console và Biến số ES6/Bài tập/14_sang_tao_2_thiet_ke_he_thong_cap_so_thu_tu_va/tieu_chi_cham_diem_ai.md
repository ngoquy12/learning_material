# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế hệ thống cấp số thứ tự và tính chi phí khám bệnh — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ danh mục dữ liệu đầu vào (tên bệnh nhân, tuổi, phí khám ban đầu, phí xét nghiệm, phần trăm giảm giá BHYT, ...) và dữ liệu đầu ra hiển thị trên phiếu khám bệnh.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 bẫy thực tế (nhập dữ liệu rỗng, nhập chuỗi ký tự vào ô số gây `NaN`, cộng chuỗi ngoài ý muốn nếu quên `Number()`, hoặc lỗi khai báo hằng số `const` khi cần gán lại).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid chính xác mô tả chi tiết từ lúc trình duyệt tải HTML, nạp `app.js`, tương tác `prompt()`, xử lý ép kiểu `Number()`, tính toán tài chính và xuất bằng Template Literals.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Sử dụng chính xác 100% các ký hiệu chuẩn Mermaid: Oval cho Bắt đầu/Kết thúc, Hình bình hành `[/ /]` cho Input/Output, Hình chữ nhật `[" "]` cho Process, Hình thoi cho Decision. Tuyệt đối không dùng hình bình hành cho phép tính toán.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Xây dựng hoàn chỉnh tính năng nhập liệu, tính toán tiền khám chính xác, áp dụng giảm giá BHYT hoặc phụ phí cấp sổ khám đúng theo logic tự thiết kế.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Đóng gói thông tin phiếu khám bằng chuỗi Template Literals (`` `${}` ``) định dạng đẹp mắt, rõ ràng, hiển thị chuẩn xác qua `console.log()` và `alert()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Mã nguồn triển khai việc ép kiểu minh bạch `Number()`, kiểm tra giá trị hợp lệ cơ bản trước khi tính toán để tránh lỗi phép tính ra `NaN` hoặc sai lệch chuỗi.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn ES6:** Phân định rõ ràng `const` và `let`, tuyệt đối không dùng `var`. Tên biến đặt 100% bằng tiếng Anh theo chuẩn `camelCase`. Đặt thẻ `<script>` ở cuối thẻ `<body>` của file HTML.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc tệp sạch sẽ (`index.html`, `app.js`), commit rõ ràng, README mô tả đầy đủ các bước thực thi dự án.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung việc xuất log chi tiết ở các cấp độ `console.info()`, `console.warn()`, `console.error()` để mô phỏng hệ thống Auditing quá trình tiếp đón bệnh nhân.

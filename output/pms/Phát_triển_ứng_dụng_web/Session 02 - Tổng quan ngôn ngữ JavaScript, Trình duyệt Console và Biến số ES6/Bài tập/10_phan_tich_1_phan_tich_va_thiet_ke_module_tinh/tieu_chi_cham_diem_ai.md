# **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân tích và Thiết kế Module Tính Chi phí Khám bệnh Ban đầu — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Đề xuất được 2 phương án có sự khác biệt rõ ràng về cấu trúc quản lý biến (`const`/`let` độc lập vs gộp biến xử lý), thời điểm ép kiểu dữ liệu `Number()` (ngay khi nhập vs khi tính toán) và vị trí gắn file mã nguồn JS.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Lập bảng so sánh 5 tiêu chí (Hiệu năng V8, Bộ nhớ, Tính bảo trì, Khả năng chống bẫy nối chuỗi, Bối cảnh phù hợp). Bảng HTML được định dạng đúng thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Trình bày lý do chọn phương án tối ưu dựa trên khả năng bảo vệ phạm vi biến (Block Scope), tối ưu hóa bộ nhớ RAM và tuân thủ nguyên tắc Clean Code.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày sơ đồ luồng Mermaid đầy đủ. Ký hiệu đúng 100% chuẩn hình dạng (Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Process/Calculation).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết tệp `index.html` và `app.js` chuẩn HTML5 và ES6+. Liên kết script chính xác ở cuối thẻ `<body>`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Sử dụng `Number()` ép kiểu rõ ràng ngay từ đầu vào thu thập từ `prompt()`, tính đúng tuổi bệnh nhân theo năm 2026 và tính chính xác chi phí khám thực tế với phép nhân tỷ lệ miễn giảm `baseFee * (1 - insuranceDiscountRate)`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Sử dụng đúng chuỗi Template Literals (dấu backticks `` ` ``) để nhúng biến số. Hiển thị thông báo phiếu khám bệnh đồng nhất trên cả `console.log` và `alert`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến bằng tiếng Anh chuẩn `camelCase` (ví dụ: `patientName`, `birthYear`, `baseFee`, `insuranceDiscountRate`), tuyệt đối không dùng `var`, chú thích mã nguồn bằng tiếng Việt rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn repository công khai, đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session02_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script / Phân tích V8 Engine:** Viết mã phân tích hoặc giải thích chi tiết cơ chế V8 Engine xử lý Variable Hoisting với `var` so với Temporal Dead Zone (TDZ) của `let`/`const` ảnh hưởng thế nào đến độ an toàn của ứng dụng phòng khám.

# **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Phân tích và thiết kế module tính toán phiếu đặt lịch khám bệnh — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Tự đề xuất và trình bày rõ ràng ít nhất 2 phương án thiết kế kiến trúc mã nguồn khác nhau (ví dụ: phân tích sự khác biệt giữa việc tách tệp `app.js` độc lập kết nối cuối `body` so với nhúng mã trực tiếp; hoặc so sánh việc ép kiểu `Number()` ngay khi nhận đầu vào từ `prompt()` so với việc giữ chuỗi thô rồi ép kiểu trong biểu thức tính toán).
    *   Nêu rõ ưu/nhược điểm cấu trúc của từng giải pháp dựa trên phạm vi kiến thức đã học (V8 Engine, ES6 Variables).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Xây dựng bảng ma trận so sánh đầy đủ 5 tiêu chí (Tốc độ thực thi, Bộ nhớ RAM, Khả năng bảo trì, Độ rõ ràng, Mức độ phù hợp).
    *   Bảng HTML có thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lý giải thuyết phục dựa trên cơ chế hoạt động của V8 Engine (tách tệp `.js` giúp V8 Engine cache Bytecode tối ưu) và quy chuẩn tránh ô nhiễm scope/tránh biến toàn cục.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ sơ đồ Mermaid thể hiện chính xác luồng xử lý của phương án chọn.
    *   Tuân thủ nghiêm ngặt chuẩn 5 hình khối: Stadium `([ ])` cho Start/End, Parallelogram `[/ /]` cho I/O (`prompt`, `console`/DOM), Rectangle `[" "]` cho tính toán toán học/gán biến, Diamond cho bước kiểm tra (nếu có), Mũi tên `-->` kết nối.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Tạo file `index.html` và `app.js` liên kết chuẩn xác ở cuối thẻ `body`.
    *   Khai báo biến chuẩn ES6 (`const` cho hằng số không đổi, `let` cho biến tính toán/thay đổi, tuyệt đối không dùng `var`).
    *   Thực hiện ép kiểu dữ liệu đầu vào bằng `Number()` chính xác.
    *   Tính toán đúng chi phí khám sau BHYT và tổng chi phí thanh toán theo công thức nghiệp vụ.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Ngăn chặn triệt để lỗi cộng chuỗi (`"200000" + "30000"`).
    *   Không xảy ra lỗi gán lại hằng số (`TypeError`).
    *   Không gây lỗi truy cập phần tử DOM null (do đặt script đúng vị trí sau khi HTML render).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Sử dụng chuỗi Template Literals để tạo thông điệp phiếu khám đầy đủ thông tin: Tên bệnh nhân, Chuyên khoa, Chi phí gốc, Số tiền giảm BHYT, Phí dịch vụ, và Tổng thanh toán thực tế.
    *   Xuất kết quả đồng thời ra `console.log()` và hiển thị thành công lên giao diện HTML bằng thuộc tính DOM `textContent`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến sử dụng chuẩn `camelCase` bằng tiếng Anh rõ nghĩa (`patientName`, `baseExamFee`, `insuranceDiscountRate`, `bookingServiceFee`, `totalPayment`).
    *   Chú thích mã nguồn bằng tiếng Việt có dấu chuẩn sản xuất.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn kho chứa GitHub hợp lệ, cấu trúc thư mục đúng quy chuẩn: `[Tên Lớp]_[Môn Học]_SessionSession 02_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Đoạn mã Đo kiểm Hiệu năng (Benchmark Script):**
    *   Sử dụng `console.time()` và `console.timeEnd()` trong môi trường Node.js / Browser Console để đo đạc và so sánh thời gian xử lý việc tạo chuỗi thông điệp phiếu khám giữa phương pháp nối chuỗi toán tử `+` cổ điển và phương pháp dùng Template Literals ES6.

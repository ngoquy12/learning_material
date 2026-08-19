# **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân tích và Triển khai Module Tính Phụ phí Check-in Máy bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự phát hiện và trình bày rõ ràng ít nhất 2 cấu trúc rẽ nhánh khác nhau (ví dụ: chuỗi `if...else if` lồng nhau đa tầng vs `switch-case` phân tầng kết hợp `ternary operator`), phân tích sự khác biệt về mặt cấu trúc điều kiện.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Xây dựng bảng so sánh HTML đầy đủ 5 tiêu chí (Tốc độ thực thi, Bộ nhớ, Độ bảo trì, Độ sạch mã nguồn, Ngữ cảnh áp dụng). Thẻ `<table>` tuân thủ đúng thuộc tính CSS `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Đưa ra lập luận rõ ràng, hợp lý lý giải tại sao phương án được chọn là tối ưu nhất trong bối cảnh ứng dụng thực tế.
*   **[10 điểm] Lưu đồ luồng Mermaid chuẩn hóa:** Vẽ thành công sơ đồ luồng Mermaid mô tả chính xác logic rẽ nhánh. Sử dụng đúng 5 hình dạng quy chuẩn (Stadium cho Start/End, Parallelogram cho Input/Output, Diamond cho Condition, Rectangle cho Process/Action, Arrow cho luồng nối). tuyệt đối không dùng sai hình dạng cho bước tính toán hay điều kiện.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Triển khai mã nguồn JavaScript ES6+ chạy chính xác tất cả các quy tắc nghiệp vụ (tính đúng mức miễn cước theo hạng vé, tính đúng đơn giá quá cước 50k/kg, áp dụng đúng phí làm thủ tục quầy 100k cho ECO không VIP, giảm 20% cho VIP).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Có logic kiểm tra dữ liệu đầu vào (Validation) chặn triệt để trường hợp `baggageWeight < 0` hoặc `ticketClass` không hợp lệ trước khi thực hiện tính toán.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Định dạng hiển thị Console rõ ràng:** In đầy đủ thông số báo cáo phụ phí (Số kg quá cước, Phí quá cước, Tiền giảm giá VIP, Phí in thẻ quầy, Tổng phụ phí) rõ ràng, dễ đọc, chính xác theo số liệu thực tế.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Sử dụng hằng số `const` và `let` đúng mục đích, tên biến bằng tiếng Anh đúng ngữ nghĩa (`ticketClass`, `baggageWeight`, `overweightFee`, `totalFee`), comment bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo repository và đẩy bài làm lên cấu trúc thư mục đúng mẫu: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Viết đoạn mã đo thời gian thực thi (sử dụng `console.time()` / `console.timeEnd()`) so sánh hiệu năng chạy 100.000 lần của cả 2 phương án đề xuất.

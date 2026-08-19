# **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Phân tích và thiết kế mô-đun tính chi phí và tạo phiếu xác nhận khám bệnh — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự đề xuất và mô tả rõ ràng sự khác biệt về cấu trúc logic giữa 2 phương án (ví dụ: Phương án ép kiểu trực tiếp tại đầu vào vs Phương án lưu chuỗi thô rồi ép kiểu khi tính toán; hoặc Phương án quản lý biến đơn lẻ vs Phương án gộp bước).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Thiết lập bảng so sánh HTML đầy đủ 5 tiêu chí (Tốc độ xử lý, Bộ nhớ, Bảo trì, Độ đọc hiểu, Tuân thủ ES6) có định dạng bảng đúng chuẩn quy định (`style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`).

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Trình bày lập luận kỹ thuật thuyết phục cho phương án được chọn (tại sao chọn ép kiểu minh bạch `Number()` ngay từ đầu, tại sao dùng `const` thay vì `let` cho các hằng số tính toán).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày lưu đồ Mermaid đúng cú pháp và đúng 5 hình khối tiêu chuẩn (Terminator, Parallelogram cho IO, Rectangle cho Process, Diamond cho Decision).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết đầy đủ mã nguồn JavaScript trong tệp `app.js`, liên kết đúng cách với `index.html`. Áp dụng chính xác cú pháp ES6 (`let`, `const`, Template Literals).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Kiểm tra và xử lý thỏa đáng trường hợp dữ liệu đầu vào bị `NaN`, âm, hoặc chuỗi rỗng trước khi tính toán.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Kết quả xuất ra Developer Console và Alert hiển thị đầy đủ thông tin phiếu xác nhận (Mã bệnh nhân, Tên, Chi phí gốc, Tiền miễn giảm BHYT, Phí ưu tiên, Tổng thanh toán) dạng chuỗi nhiều dòng minh bạch.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến bằng tiếng Anh theo quy tắc `camelCase` (ví dụ: `patientId`, `baseExamFee`, `totalPayment`), mã nguồn sạch đẹp, có ghi chú giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn repository GitHub hợp lệ, đúng cấu trúc thư mục yêu cầu và lịch sử commit rõ ràng.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản kiểm thử hiệu năng/Validation:** Đóng gói đoạn mã kiểm thử tính chính xác của phép tính với nhiều trường hợp dữ liệu đầu vào khác nhau (BHYT 0%, BHYT 80%, có/không có phí ưu tiên).

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Thiết kế và tối ưu logic tính phí dịch vụ làm thủ tục chuyến bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    - Mô tả chi tiết cấu trúc logic của ít nhất 2 phương án lập trình rẽ nhánh khác nhau trong JavaScript ES6+ (ví dụ: Cấu trúc Nested `if-else` truyền thống vs Cấu trúc Guard Clauses kết hợp `switch-case`).
    - Nêu rõ điểm khác biệt về mặt tổ chức luồng điều khiển và thứ tự đánh giá điều kiện.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    - Tạo bảng so sánh trực quan chứa đầy đủ 5 tiêu chí bắt buộc: Độ phức tạp thời gian, Dung lượng bộ nhớ, Tính bảo trì, Độ đọc hiểu, Bối cảnh phù hợp.
    - Phân tích có chiều sâu chuyên môn, thể hiện rõ ưu/nhược điểm của từng phương án.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    - Đưa ra lập luận thuyết phục chọn phương án tối ưu dựa trên tiêu chuẩn Clean Code và khả năng mở rộng khi hãng bổ sung hạng vé hoặc điều chỉnh mức phí.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    - Xây dựng mã giả hoặc lưu đồ Mermaid đúng quy định chuẩn hóa (Khối bắt đầu/kết thúc `([ ])`, Khối điều kiện `{ }`, Khối tính toán `[" "]`, Khối đầu vào/đầu ra `[/ /]`).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    - Triển khai thành công mã nguồn JavaScript (ES6+) phản ánh đúng phương án tối ưu đã chọn.
    - Tính toán chính xác phí hành lý quá cước theo từng mức miễn cước của 3 hạng vé (`1`, `2`, `3`) và áp dụng đúng ưu đãi giảm 10% phí hành lý cho `isVipMember === true`.
    - Tính toán đúng phí chọn chỗ ngồi theo khu vực ghế và hạng vé tương ứng.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    - Bắt và xử lý triệt để các trường hợp dữ liệu đầu vào vi phạm (`ticketClass` ngoài 1-3, `seatZone` ngoài 1-3, `baggageWeight < 0`).
    - Trả về tổng phí `-1` và hiển thị thông điệp cảnh báo phù hợp khi phát hiện lỗi dữ liệu.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    - Kết quả xuất ra màn hình console rõ ràng, đầy đủ các thông tin: Hạng vé, Khối lượng quá cước, Phí hành lý quá cước (sau giảm giá nếu có), Phí chọn chỗ ngồi, và Tổng phí làm thủ tục.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    - Đặt tên hằng số và biến bằng tiếng Anh, chuẩn `camelCase` (`ticketClass`, `baggageWeight`, `seatZone`, `isVipMember`, `excessBaggageFee`, `seatFee`, `totalFee`).
    - Sử dụng đúng `const`/`let`, không dùng `var`. Thụt lề chuẩn 2 spaces.
*   **[5 điểm] Nộp bài GitHub:**
    - Cung cấp link repository GitHub hợp lệ, đúng cấu trúc tên thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    - Viết đoạn mã kiểm thử hiệu năng (sử dụng `console.time` / `console.timeEnd`) so sánh tốc độ thực thi của 2 giải pháp qua 100.000 lượt giả lập dữ liệu check-in.
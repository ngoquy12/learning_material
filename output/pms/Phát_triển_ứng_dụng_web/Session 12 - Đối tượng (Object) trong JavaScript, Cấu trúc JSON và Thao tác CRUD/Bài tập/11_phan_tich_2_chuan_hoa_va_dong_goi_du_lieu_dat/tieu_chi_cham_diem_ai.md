### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Chuẩn hóa và Đóng gói Dữ liệu Đặt phòng Khách sạn Agoda — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự đề xuất độc lập tối thiểu 2 phương án xử lý đối tượng (ví dụ: Biến đổi trực tiếp trên đối tượng gốc bằng toán tử `delete` vs Khởi tạo đối tượng mới và trích xuất các thuộc tính hợp lệ). Phân tích rõ sự khác biệt về cấu trúc logic của từng phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Thiết lập đầy đủ bảng so sánh HTML chuẩn theo 5 tiêu chí: Tốc độ xử lý, Bộ nhớ tiêu tốn, Khả năng bảo trì, Độ rõ ràng mã nguồn và Mức độ phù hợp hệ thống. Phân tích sắc bén, logic.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Đưa ra lập luận thuyết phục về việc chọn giải pháp tối ưu phù hợp với quy mô ứng dụng đặt phòng Agoda.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Sử dụng Mermaid Flowchart biểu diễn quy trình xử lý. Tuân thủ 100% quy chuẩn hình học (Oval `([ ])` cho Bắt đầu/Kết thúc, Bình hành `[/ /]` cho I/O, Chữ nhật `[" "]` cho Tiến trình/Tính toán, Hình thoi `?` cho Rẽ nhánh điều kiện).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Xây dựng mã nguồn JavaScript Vanilla ES6+ thực thi chính xác các bước: tính phụ thu `earlyCheckInFee` (30% khi `checkInHour < 12`), tính `totalAmount`, sử dụng `delete` để xóa `tempToken` và `draftSessionId`, truy xuất đúng key gạch ngang bằng Bracket Notation `["special-request"]`, và thực hiện chuyển đổi JSON qua lại.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Tránh bẫy lỗi gán `undefined` làm phình bộ nhớ đối tượng.
    *   Tránh bẫy lỗi cú pháp SyntaxError khi đọc key có ký tự đặc biệt.
    *   Kiểm tra tính hợp lệ của dữ liệu trước và sau khi `JSON.parse()`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Kết quả in ra console và chuỗi JSON đầu ra phải loại bỏ hoàn toàn các key rác, tính đúng tổng tiền thanh toán, hiển thị đầy đủ thông tin phòng đặt theo đúng yêu cầu nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến/hàm/thuộc tính chuẩn Tiếng Anh (camelCase), chú thích logic bằng Tiếng Việt có dấu. Tuyệt đối không dùng các từ cấm (frameworks, ORM, REST API, HTTP codes).
*   **[5 điểm] Nộp bài GitHub:** Nộp đúng đường dẫn repository GitHub theo định dạng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session12_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Xây dựng đoạn mã JavaScript sử dụng `console.time()` và `console.timeEnd()` để đo đạc thời gian thực thi của cả 2 giải pháp trên tập mẫu 10,000 lượt đặt phòng thô, rút ra kết luận thực nghiệm về hiệu năng.
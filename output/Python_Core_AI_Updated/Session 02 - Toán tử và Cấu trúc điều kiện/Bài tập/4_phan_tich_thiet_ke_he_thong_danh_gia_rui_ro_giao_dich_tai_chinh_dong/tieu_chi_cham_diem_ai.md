### **Tiêu chí chấm điểm (AI)**
**[Thiết kế hệ thống đánh giá rủi ro giao dịch tài chính động] — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Trình bày chi tiết cách thiết lập logic bằng `nested if-else` truyền thống (Giải pháp 1) so với phương pháp phân tách các điều kiện thành một trạng thái tuple hóa rồi truyền qua cơ chế pattern matching `match-case` (Giải pháp 2).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Lập bảng so sánh chi tiết 2 giải pháp theo 5 tiêu chí: Độ phức tạp thời gian, Độ phức tạp không gian (RAM), Độ phức tạp bảo trì, Độ đọc hiểu, và Bối cảnh áp dụng thực tế.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Giải thích rõ ràng tại sao lại chọn phương án tối ưu dựa trên nhu cầu nâng cấp nghiệp vụ bảo mật thanh toán liên tục của Fintech; phân tích ưu điểm/nhược điểm cụ thể.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày mã giả (Pseudocode) rõ ràng, thể hiện chính xác thứ tự ưu tiên kiểm tra dữ liệu đầu vào (Validation) trước rồi mới đến phân lớp rủi ro giao dịch.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết code Python thực thi phân loại rủi ro chuẩn xác với các test case đề ra từ nghiệp vụ mà không có lỗi chạy chương trình.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Hiện thực hóa đầy đủ bước kiểm chuẩn định dạng của các tham số (ví dụ: `amount <= 0`, `score < 300` hoặc `score > 850`, `failed < 0`) trước khi đưa vào luồng kiểm tra rủi ro chính để bảo vệ phần mềm khỏi lỗi runtime.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Response — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Định dạng đầu ra của mỗi giao dịch chính xác theo kiểu số thực (float) đối với phí bảo hiểm và được làm tròn chính xác 2 chữ số sau dấu phẩy.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến/hàm tuân thủ chuẩn `snake_case`, giải quyết bài toán mạch lạc, không lặp code vô nghĩa, có chú thích code chi tiết ở các khối nghiệp vụ phức tạp.
*   **[5 điểm] Nộp bài GitHub:** Link Github hoạt động tốt, cấu trúc thư mục đặt đúng quy chuẩn `[Tên Lớp]_[Môn Học]_Session02_Ex04`, có mô tả ngắn tại file README.md.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Tự thiết kế một hàm tạo ngẫu nhiên 10,000 giao dịch giả lập (không dùng thư viện ngoài ngoại trừ thư viện `time` có sẵn của Python) để đo thời gian chạy của cả hai phương án (Nested-if vs Match-case) và in kết quả so sánh tốc độ thực tế ra màn hình log.
# **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Phân tích và Thiết kế Tiến trình Kiểm soát Mã Sách Mượn Tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Mô tả rõ ràng cấu trúc điều khiển của ít nhất 2 giải pháp khác nhau (ví dụ: Giải pháp 1 dùng `for...else` với `break`/`continue` trực tiếp; Giải pháp 2 dùng biến cờ cờ hiệu `flag` kết hợp các câu lệnh điều kiện `if`).
    *   Phân tích được cơ chế hoạt động của khối `else` trong vòng lặp Python khi có và không có câu lệnh `break`.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng so sánh HTML đầy đủ 5 tiêu chí theo đúng cấu trúc yêu cầu (Time complexity, Memory overhead, Maintainability, Readability, Use case).
    *   Đánh giá chính xác và thuyết phục ưu/nhược điểm của từng phương án trong bối cảnh ứng dụng thực tế.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lý do lựa chọn phương án tối ưu dựa trên tiêu chuẩn mã nguồn sạch (Clean Code), độ mạch lạc của luồng điều khiển và hiệu năng xử lý.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ lưu đồ Mermaid hoặc mã giả chính xác luồng dữ liệu.
    *   Tuân thủ 100% quy chuẩn hình dạng Mermaid: Oval `([ ])` cho Start/End, Song song `[/ /]` cho Input/Output, Hình thoi `{ }` cho Điều kiện, Hình chữ nhật `[" "]` cho Tiến trình.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Triển khai đúng vòng lặp `for` với `range(start_id, end_id + 1)`.
    *   Sử dụng đúng `continue` để bỏ qua mã lỗi nhẹ và `break` để ngắt khẩn cấp khi gặp `critical_id`.
    *   Áp dụng đúng khối `else` của vòng lặp `for` (hoặc logic kiểm soát tương đương đã đề xuất) để xác nhận khi tiến trình hoàn tất an toàn.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Kiểm tra và xử lý trường hợp `start_id > end_id` trước khi lặp.
    *   Đảm bảo các mã bị bỏ qua (`continue`) không bị tính vào tổng số lượng sách mượn thành công.
    *   Đảm bảo khi gặp `break`, khối `else` của vòng lặp không được thực thi.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Đầu ra hiển thị rõ ràng thông báo trạng thái từng mã sách, cảnh báo an ninh hoặc thông báo xác nhận thành công trọn vẹn theo đúng quy tắc nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến chuẩn tiếng Anh (`start_id`, `end_id`, `critical_id`, `success_count`).
    *   Không vi phạm vùng kiến thức bị cấm (KHÔNG dùng `while`, `list`, `dict`, `def`, `class`).
    *   Chú thích mã nguồn bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn repository GitHub hợp lệ, cấu trúc thư mục đúng quy định `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Script kiểm thử toàn diện kịch bản biên:**
    *   Viết mã nguồn thử nghiệm đầy đủ 3 kịch bản: (1) Quét thành công không có lỗi an ninh; (2) Quét bị ngắt giữa chừng do gặp `critical_id`; (3) Dải mã đầu vào bị lỗi (`start_id > end_id`).

# **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Thiết kế Luồng Xử lý và Quét Nhật ký Mượn Trả Sách Thư viện Hàng ngày — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Mô tả rõ ràng cơ chế hoạt động của ít nhất 2 phương án (ví dụ: Phương án 1 dùng cấu trúc nguyên bản `for...else` với `break`/`continue`; Phương án 2 dùng biến cờ hiệu `is_aborted` theo kiểu lập trình cờ lệnh).
    *   Phân tích được ưu/nhược điểm mặt cấu trúc của từng giải pháp.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Tạo bảng so sánh HTML đầy đủ 5 tiêu chí: Tốc độ, Bộ nhớ, Khả năng bảo trì, Độ đọc hiểu, Mức độ phù hợp.
    *   Sử dụng đúng thẻ HTML có thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Lập luận ngắn gọn, thuyết phục lý do chọn phương án tối ưu dựa trên tiêu chuẩn Pythonic (`for...else`) giúp tối ưu tài nguyên bộ nhớ và mã nguồn gọn gàng.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Cung cấp sơ đồ Mermaid minh họa đúng luồng xử lý bài toán.
    *   Tuân thủ đúng 5 ký hiệu hình học tiêu chuẩn (Oval cho Start/End, Parallelogram cho In/Out, Rectangle cho Thao tác/Tính toán, Diamond cho Điều kiện, Mũi tên cho Luồng).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Viết mã nguồn Python chạy đúng các trường hợp nghiệp vụ: bỏ qua mã chia hết cho 5 (`continue`), dừng khẩn cấp mã chia hết cho 13 (`break`), tính tiền phạt cho mã chia hết cho 3, xuất thông báo hoàn thành trong khối `else` của `for`.
    *   Tuân thủ nghiêm ngặt pham vi kiến thức: Không dùng `while`, `def`, `class`, `list`, `dict`, `set`, `tuple`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Kiểm tra đầu vào: Thông báo lỗi và dừng chương trình khi `start_id <= 0` hoặc `end_id < start_id`.
    *   Cộng dồn chính xác tổng số giao dịch thành công và tổng tiền phạt.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   In kết quả đầu ra rõ ràng, đúng các thông tin nghiệp vụ yêu cầu (số giao dịch thành công, tổng tiền phạt thu được, trạng thái ca trực).
    *   Không dư thừa thông tin hoặc vi phạm định dạng hiển thị.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến bằng tiếng Anh chuẩn PEP 8 (ví dụ: `start_id`, `end_id`, `total_fine`, `success_count`, `tx_id`).
    *   Mã nguồn có chú thích bằng tiếng Việt có dấu rõ ràng, mạch lạc.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn repo GitHub hợp lệ, đúng cấu trúc thư mục yêu cầu: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Thống kê báo cáo mở rộng:**
    *   Viết kịch bản kiểm thử các dải mã biên khác nhau (ví dụ: dải mã chứa cả mã chia hết cho 5 và 13, dải mã hoàn toàn sạch) và xuất báo cáo tỷ lệ giao dịch thành công/bỏ qua chi tiết.

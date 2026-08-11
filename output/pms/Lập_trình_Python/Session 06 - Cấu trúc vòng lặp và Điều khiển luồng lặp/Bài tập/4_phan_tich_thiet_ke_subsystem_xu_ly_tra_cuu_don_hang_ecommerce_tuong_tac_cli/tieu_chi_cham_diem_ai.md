### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Thiết kế Subsystem Xử lý & Tra cứu Đơn hàng E-Commerce Tương tác CLI — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Mô tả chi tiết, chính xác bản chất cấu trúc dữ liệu và giải thuật của Phương án A (Sequential Search qua List) và Phương án B (Direct Lookup qua Dictionary Key).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Trình bày đầy đủ bảng HTML theo yêu cầu với 5 tiêu chí: Độ phức tạp thời gian ($O(n)$ vs $O(1)$), Bộ nhớ, Tính dễ đọc, Khả năng mở rộng và Ngữ cảnh áp dụng. Thẻ HTML `<table>` chứa đúng thuộc tính CSS quy định.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Đưa ra lập luận thuyết phục, dựa trên kết quả so sánh Trade-off để chọn Phương án B cho hệ thống E-Commerce thực tế.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Mã giả thể hiện rõ ràng các bước duyệt danh sách sản phẩm/voucher, kiểm tra điều kiện và tính toán hóa đơn. Tuyệt đối không chứa cú pháp `while`, `break`, `continue`.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết code Python thực thi đúng logic tra cứu, áp mã giảm giá và tính toán chiết khấu chính xác theo quy tắc nghiệp vụ.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Bắt các ngoại lệ biên bằng `ValueError` hoặc `KeyError` khi sản phẩm không tồn tại, mua vượt tồn kho, voucher hết hạn hoặc đơn hàng không đủ giá trị tối thiểu (`min_order_value`). Không vi phạm phạm vi cấm (`while`, `break`, `continue`).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Giao diện Menu Console và Hóa đơn hiển thị rõ ràng, chuyên nghiệp, đúng định dạng số liệu (tổng tiền gốc, tiền giảm, tiền thanh toán).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Mã nguồn tuân thủ PEP 8, sử dụng danh xưng biến/hàm bằng tiếng Anh chuẩn, có chú thích logic bằng tiếng Việt có dấu, sử dụng Type Hints chuẩn Python 3.10+ (`str | float`).
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn nộp bài đúng chuẩn thư mục `[Tên Lớp]_[Môn Học]_Session06_Ex04`, commit history rõ ràng.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Viết script đo thời gian thực thi (dùng thư viện `time`) so sánh hiệu năng trực tiếp giữa 2 giải pháp trên tập dữ liệu giả lập $100,000$ sản phẩm.
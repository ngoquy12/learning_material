# **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Phân tích và Triển khai Module Tính tiền Hóa đơn Quầy POS — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Mô tả rõ ràng 2 hướng tiếp cận mã nguồn khác nhau (ví dụ: Phương án 1 - Biểu thức gộp trực tiếp tính toán trong lệnh print; Phương án 2 - Biến trung gian tuần tự lưu trữ từng chi phí thành phần).
    *   Phân tích ưu/nhược điểm cấu trúc của từng giải pháp trong phạm vi kiến thức đã học.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng HTML chứa đầy đủ 5 tiêu chí: Tốc độ xử lý, Dung lượng bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Trường hợp sử dụng.
    *   Bảng HTML sử dụng đúng thuộc tính bắt buộc: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Giải trình lý do chọn phương án tối ưu dựa trên bài toán thực tế của phần mềm POS (tính minh bạch tài chính, dễ debug lỗi tính toán, dễ cập nhật thuế VAT hoặc phí topping).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ lưu đồ Mermaid hoặc mã giả thể hiện chính xác trình tự xử lý: Nhập dữ liệu -> Ép kiểu -> Tính phụ thu -> Tính Subtotal -> Tính Discount -> Tính VAT -> Làm tròn Final Total -> In Hóa đơn.
    *   Sử dụng đúng các hình dạng quy chuẩn Mermaid: `([Start/End])`, `[/Input/Output/]`, `["Process"]`.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Mã nguồn Python thực thi chính xác tất cả các công thức nghiệp vụ: phụ thu size, topping (8.000 VNĐ/cái), giảm giá %, VAT (8%), tổng tiền.
    *   Chương trình chạy không lỗi cú pháp, thực thi mượt mà trên môi trường CLI.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Thực hiện ép kiểu dữ liệu từ `input()` chính xác (`int` cho số lượng, `float` cho phần trăm giảm giá).
    *   Xử lý đúng phép chia tỷ lệ phần trăm (`discount_rate / 100`) và ép kiểu số nguyên `int()` cho số tiền thanh toán cuối cùng mà không làm lệch kết quả.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Đầu ra màn hình console thể hiện hóa đơn đầy đủ các dòng: Tên món, Đơn giá, Kích thước phụ thu, Tiền topping, Tổng tiền hàng, Giảm giá, VAT 8%, Tổng thanh toán.
    *   Định dạng văn bản căn lề đẹp mắt, sử dụng các đường kẻ ngang phân cách (ví dụ: `=` hoặc `-`) chuyên nghiệp.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến viết bằng Tiếng Anh chuẩn `snake_case` (ví dụ: `drink_name`, `unit_price`, `size_upcharge`, `topping_count`, `discount_rate`, `final_total`).
    *   Có chú thích mã nguồn bằng Tiếng Việt có dấu rõ ràng. không chứa từ ngữ không trang trọng hay emojis.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub repository hợp lệ, cấu trúc thư mục đúng chuẩn `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Viết kịch bản kiểm thử đo lường thời gian thực thi (sử dụng thư viện `time`) để so sánh tốc độ xử lý giữa 2 phương án khi thực hiện hàng triệu phép tính hóa đơn giả lập.

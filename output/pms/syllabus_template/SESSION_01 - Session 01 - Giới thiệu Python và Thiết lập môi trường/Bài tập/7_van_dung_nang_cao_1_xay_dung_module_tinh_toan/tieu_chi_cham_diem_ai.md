# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Xây dựng Module Tính toán và Xuất Hóa đơn Bán hàng POS — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ tên biến, kiểu dữ liệu (`str`, `int`, `float`), miền giá trị và ý nghĩa nghiệp vụ cho tất cả tham số Input/Output của hệ thống POS.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Mô tả đúng chuỗi các bước tính toán và trình bày sơ đồ luồng dữ liệu (Flowchart Mermaid hoặc Pseudocode) đầy đủ từ nhập liệu đến xuất hóa đơn.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu và Chuyển đổi kiểu:** Thực hiện `input()` dữ liệu và ép kiểu dữ liệu (`int()`, `float()`) chính xác, không phát sinh lỗi kiểu dữ liệu trong quá trình tính toán.
*   **[15 điểm] Logic tính toán hóa đơn chính xác:** Tính chính xác phụ thu size, topping, Subtotal, giảm giá hội viên, thuế VAT 8% và Tổng tiền thanh toán theo đúng công thức nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Kiểm soát dữ liệu số hợp lệ:** Đảm bảo số lượng ly, phụ thu, số topping không bị giá trị âm; giá trị tỷ lệ giảm giá nằm trong khoảng cho phép (0% - 100%).
*   **[15 điểm] Định dạng số tiền và hiển thị phiếu thu:** Sử dụng làm tròn số tiền (`round()` hoặc ép kiểu `int()`) và trình bày hóa đơn dạng văn bản CLI trực quan, chuyên nghiệp.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xử lý và hiển thị thông báo lỗi rõ ràng bằng tiếng Việt khi người dùng nhập dữ liệu không hợp lệ (như nhập chuỗi cho trường số nguyên).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Sử dụng tên biến tiếng Anh chuẩn (`base_price`, `topping_count`, `subtotal`, `final_total`), có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu định dạng hóa đơn:** Sử dụng kỹ thuật căn chỉnh chuỗi (string format / f-string formatting với dấu phân cách hàng nghìn) giúp hóa đơn hiển thị đẹp như máy in POS thực tế.

# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Tính toán Hóa đơn Bán hàng Tích hợp Chiết khấu và Thuế POS Highlands — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ các danh mục đầu vào (Input) và đầu ra (Output) kèm theo kiểu dữ liệu chính xác (`str` cho tên món, `int` cho đơn giá và số lượng, `float` cho tỷ lệ phần trăm và tổng tiền).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày tuần tự công thức toán học và xây dựng sơ đồ luồng dữ liệu (Mermaid) chuẩn quy chuẩn hệ thống POS (sử dụng đúng hình khối quy định: Parallelogram cho Input/Output, Rectangle cho Process/Calculation).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Chuyển đổi kiểu dữ liệu & Khai báo biến:** Thực hiện ép kiểu `int()`, `float()`, `str()` chính xác từ dữ liệu nhập vào qua hàm `input()`; sử dụng danh xưng biến chuẩn tiếng Anh readable.
*   **[15 điểm] Tính toán tài chính hóa đơn:** Tính chính xác phụ thu Size M (6.000 VNĐ), Size L (10.000 VNĐ), Topping (8.000 VNĐ), Tổng gộp (`gross_subtotal`), Tiền giảm giá (`discount_amount`), Tiền thuế VAT (`vat_amount`), Tổng thanh toán (`final_total`) và Tiền thừa trả lại (`change_due`).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Đảm bảo thứ tự ưu tiên tính toán:** Thực hiện đúng quy tắc chiết khấu được trừ trên tiền hàng trước khi nhân tỷ lệ thuế VAT.
*   **[15 điểm] Tính toán chia trung bình & Làm tròn:** Tính đúng giá trị trung bình mỗi ly trà/cà phê (`avg_price_per_cup`) và đảm bảo các phép chia không bị lỗi logic số học.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trình bày Hóa đơn POS chuẩn mực:** Trình bày kết quả đầu ra trực quan bằng chuỗi ký tự định dạng (f-string) căn lề đẹp mắt, hiển thị phân tách rõ ràng giữa các phần itemized bill, giảm giá, VAT và thanh toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Đặt tên biến hoàn toàn bằng tiếng Anh chuẩn định danh software engineering (`base_price`, `cash_given`, `vat_rate`), chú thích giải thích logic bằng Tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Tạo đúng cấu trúc thư mục và đặt tên repository theo chuẩn hướng dẫn `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex9`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Định dạng số tiền chuyên nghiệp:** Sử dụng định dạng hàng nghìn phân cách dấu phẩy/dấu chấm (ví dụ: `150,000 VNĐ`) trong hiển thị kết quả bằng kỹ thuật định dạng chuỗi nâng cao của Python.

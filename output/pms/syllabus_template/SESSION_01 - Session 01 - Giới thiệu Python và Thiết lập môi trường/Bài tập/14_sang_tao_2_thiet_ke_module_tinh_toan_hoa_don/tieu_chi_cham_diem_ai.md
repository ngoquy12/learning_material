# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Module Tính toán Hóa đơn và Phân tích Doanh thu POS Linh hoạt — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, hợp lý danh sách tham số đầu vào và kết quả đầu ra với kiểu dữ liệu chuẩn xác (`int`, `float`, `str`) đáp ứng toàn bộ bài toán nghiệp vụ POS.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích rõ ràng tối thiểu 3 kịch bản biên hoặc dữ liệu đầu vào bất hợp lý kèm theo định hướng xử lý tài chính phù hợp.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid đúng cú pháp và đúng quy định 5 hình dạng (Stadium `([ ])`, Parallelogram `[/ /]`, Rectangle `[" "]`), thể hiện mạch lạc các bước xử lý thông tin.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Diễn giải chính xác các bước chuyển đổi dữ liệu từ chuỗi nhập vào (`str`) sang dữ liệu số (`int`/`float`) và các bước tính toán tài chính nối tiếp nhau.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Mã nguồn Python chạy không lỗi, thực hiện chính xác 100% các công thức tính toán đơn giá, subtotal, chiết khấu, VAT, tổng tiền và tiền thừa.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Định dạng kết quả xuất hóa đơn chuyên nghiệp, phân tách các mục rõ ràng bằng kỹ thuật f-string, căn lề và trình bày đẹp mắt.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Áp dụng các phương pháp tính toán an toàn (như làm tròn số tiền `round()` hoặc ép kiểu dữ liệu chặt chẽ) cho các trường hợp số lẻ/thập phân trong giao dịch tài chính.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Đặt tên biến chuẩn tiếng Anh (ví dụ: `base_price`, `topping_fee`, `quantity`, `discount_rate`, `tax_rate`, `total_amount`), có ghi chú (comments) tiếng Việt giải thích từng khối tính toán.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục quy định, có tệp README mô tả chi tiết kịch bản thiết kế cá nhân.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung đoạn mã tạo chuỗi nhật ký kiểm toán giao dịch (Transaction Audit Log) dạng chuỗi mã hóa đơn tự tạo (Transaction ID) kết hợp thời gian giả lập và dấu vết dữ liệu thô.

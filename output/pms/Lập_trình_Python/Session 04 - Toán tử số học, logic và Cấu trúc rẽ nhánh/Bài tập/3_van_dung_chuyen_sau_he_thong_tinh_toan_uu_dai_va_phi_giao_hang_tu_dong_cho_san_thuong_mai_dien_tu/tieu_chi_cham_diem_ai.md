### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Hệ thống tính toán ưu đãi và phí giao hàng tự động cho sàn Thương mại điện tử — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Liệt kê đầy đủ các tham số đầu vào (kèm kiểu dữ liệu Python tương ứng) và cấu trúc dữ liệu đầu ra để hiển thị chi tiết hóa đơn.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Vẽ sơ đồ luồng (Flowchart) hoặc viết giả mã (Pseudocode) phân định rõ các bước kiểm tra tính hợp lệ dữ liệu (Guard Clauses) trước khi thực hiện phép tính toán tiền.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Áp dụng chiết khấu hạng hội viên và voucher:** Lập trình đúng logic tính chiết khấu theo từng hạng (`DIAMOND`, `GOLD`, `SILVER`, `BRONZE`) và kiểm tra điều kiện áp dụng mã `SUMMER2025` / `FREESHIP`.
*   **[15 điểm] Tính toán phí giao hàng và ưu đãi thanh toán:** Triển khai chính xác logic phân tầng phí giao hàng theo khoảng cách, cơ chế miễn phí giao hàng và tính phụ phí COD / chiết khấu Ví điện tử.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Phẳng hóa điều kiện (PEP 8 Flattening):** Loại bỏ triệt để cấu trúc conditional lồng nhau quá sâu (Arrow Anti-Pattern); kết hợp hiệu quả toán tử logic `and`, `or` và câu lệnh `elif` phẳng.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Chặn chính xác các trường hợp đầu vào âm, bằng 0, hạng hội viên không tồn tại hoặc phương thức thanh toán không hợp lệ ngay tại đầu chương trình.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xử lý và hiển thị thông báo lỗi rõ ràng, mang tính định danh cho người dùng khi dữ liệu đầu vào vi phạm quy tắc nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Định danh tiếng Anh (`subtotal`, `calculate_order_total`, `membership_tier`), có Type Hinting rõ ràng và chú thích Tiếng Việt có dấu giải thích logic.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub theo đúng cấu trúc tên thư mục quy định `[Tên Lớp]_[Môn Học]_Session04_Ex03`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Thiết kế hàm tính toán độc lập, trả về dữ liệu cấu trúc sạch (như dictionary hoặc tuple) giúp mã nguồn dễ dàng mở rộng và tái sử dụng mà không tạo các biến dư thừa trong bộ nhớ.
### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Hệ thống tính toán hóa đơn và xác thực ưu đãi Highlands POS — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đúng và đủ tất cả tên biến, kiểu dữ liệu chuẩn (`int`, `float`, `bool`) cho cả đầu vào (các tham số đơn hàng, cờ cấu hình) và đầu ra (đơn giá, thành tiền, tổng giảm giá, số tiền thanh toán, cờ kiểm định).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** 
    *   Trình bày được giải pháp đại số Boolean để nhân trực tiếp giá trị cờ logic (`0` hoặc `1`) với giá trị số tiền mà không cần dùng `if/else`.
    *   Vẽ sơ đồ luồng Mermaid đầy đủ, chính xác theo 5 dạng hình quy chuẩn (Terminator, Input/Output, Process, Decision, Flowline).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Tính toán chi phí đơn vị và thành tiền:** Tính đúng giá 1 ly (kèm phụ thu Size M/L và topping) và tính đúng Thành tiền gốc của đơn hàng dựa trên số lượng ly.
*   **[15 điểm] Xử lý logic chiết khấu và tổng thanh toán:** Áp dụng đúng toán tử tính chiết khấu cho Hội viên Vàng (10%) và Khung giờ vàng (5%) dựa trên biểu thức số học; tính chính xác số tiền phải thanh toán cuối cùng.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Đánh giá điều kiện nhận Voucher VIP:** Xây dựng chính xác biểu thức Boolean kết hợp các toán tử so sánh (`>=`) và logic (`and`, `or`) để xác định đúng trạng thái cờ `is_vip_voucher_eligible`.
*   **[15 điểm] Kiểm tra tính hợp lệ của đơn hàng:** Xây dựng biểu thức Boolean kiểm tra toàn bộ điều kiện dữ liệu đầu vào (giá > 0, số lượng > 0, topping >= 0, không trùng chọn cả size M và L) cho cờ `is_valid_order`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Hiển thị kết quả rõ ràng và chính xác:** Định dạng đầu ra trên màn hình CLI chuyên nghiệp, thể hiện đầy đủ các thông tin hóa đơn, số tiền chi tiết và các cờ kiểm tra dưới dạng giá trị `True`/`False` minh bạch.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tuân thủ quy chuẩn đặt tên biến tiếng Anh (snake_case), viết chú thích rõ ràng bằng tiếng Việt có dấu, code mạch lạc, tuân thủ đúng phạm vi kiến thức cho phép (không dùng `if/else`, vòng lặp, hàm hay thư viện cấm).
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đẩy bài làm lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session 04_Ex8`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu biểu thức toán học:** Triển khai biểu thức rút gọn thông minh cho việc tính phụ thu size và giảm giá chiết khấu, tối ưu hóa số phép tính logic và đảm bảo ép kiểu chuẩn xác.
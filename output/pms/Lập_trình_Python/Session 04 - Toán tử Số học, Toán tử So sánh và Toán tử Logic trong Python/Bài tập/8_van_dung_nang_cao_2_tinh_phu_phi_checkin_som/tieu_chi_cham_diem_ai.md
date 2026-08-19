# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Tính phụ phí check-in sớm và xác nhận hóa đơn đặt phòng — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đầy đủ và chính xác kiểu dữ liệu cho 4 tham số đầu vào (`room_price: float`, `num_nights: int`, `checkin_hour: int`, `vip_points: int`) và các kết quả đầu ra (`total_invoice: float`, `is_priority_approved: bool`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày giải thuật biểu diễn logic phụ phí và cờ phê duyệt bằng toán tử so sánh/số học; xây dựng sơ đồ Mermaid tuân thủ đúng 5 dạng hình chuẩn.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Định nghĩa đúng hàm xử lý với Type Hints đầy đủ (`float`, `int`, `bool`), khởi tạo các biến lưu trữ trung gian sạch và rõ ràng.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán đúng tiền phòng gốc, phụ phí check-in sớm (30%), miễn trừ VIP (>= 1000 điểm), tổng hóa đơn và cờ duyệt ưu tiên mà tuyệt đối không dùng `if/else`, `for/while`, `list/dict`, `and/or/not`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Xử lý chính xác các trường hợp biên như giờ check-in bằng đúng 12h (không tính phụ thu), điểm VIP bằng đúng 1000 (được miễn phụ thu), hoặc hóa đơn đúng 15,000,000 VNĐ.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Đảm bảo biểu thức tính toán hoạt động chính xác với các giá trị đầu vào là số nguyên và số thực hợp lệ trong miền giá trị thực tế của khách sạn.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất ra màn hình console thông tin hóa đơn chi tiết, rõ ràng, không bị lỗi định dạng số thực.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn viết bằng tiếng Anh chuẩn PEP 8 (snake_case), có ghi chú thích giải thích bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Nộp đúng cấu trúc thư mục trên GitHub theo yêu cầu.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Tối ưu hóa các biểu thức logic số học thành dạng rút gọn ngắn gọn, đạt hiệu năng tính toán cao nhất.

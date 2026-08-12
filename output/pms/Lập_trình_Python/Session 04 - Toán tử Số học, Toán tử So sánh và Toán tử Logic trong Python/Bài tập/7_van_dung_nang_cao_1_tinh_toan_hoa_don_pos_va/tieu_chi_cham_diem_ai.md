### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Tính toán hóa đơn POS và kiểm định điều kiện ưu đãi Highlands — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đúng và đầy đủ kiểu dữ liệu, ý nghĩa nghiệp vụ của 5 tham số đầu vào (`base_price_s`, `size_code`, `topping_count`, `quantity`, `member_code`) và các giá trị đầu ra (đơn giá, tạm tính, giảm giá, tổng thanh toán, 4 cờ kiểm định).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Giải thích rõ ràng nguyên lý chuyển đổi giá trị Boolean (`True`/`False` thành `1`/`0`) để tính toán đại số không dùng `if/else`; thiết kế trình tự các bước tính toán logic theo đúng thứ tự ưu tiên toán tử.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Đọc dữ liệu đầu vào từ bàn phím bằng `input()`, thực hiện ép kiểu chính xác (`float`, `int`, `str`).
*   **[15 điểm] Xử lý nghiệp vụ tính toán đơn hàng:** Xây dựng công thức tính phụ thu size (`(size_code == "M") * 6000 + (size_code == "L") * 10000`), tiền topping, tiền subtotal, tiền chiết khấu GOLD (`subtotal * 0.10 * (member_code == "GOLD")`) và tổng tiền thanh toán chính xác.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Xử lý các cờ kiểm định nghiệp vụ:** Biểu diễn chính xác 4 cờ logic Boolean (`is_valid_topping`, `is_eligible_freeship`, `is_vip_promotion`, `is_valid_order`) bằng các toán tử so sánh và toán tử logic (`and`, `or`, `not`).
*   **[15 điểm] Validate dữ liệu và giới hạn nghiệp vụ:** Đảm bảo bẫy biên topping được giới hạn trong dải `[0, 5]` và kiểm tra điều kiện đơn hàng hợp lệ khi giá gốc > 0 và số lượng ly > 0.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất thông tin hóa đơn minh bạch kèm trạng thái cờ hợp lệ đơn hàng `is_valid_order`, đảm bảo chương trình tính toán trơn tru không phát sinh lỗi Runtime khi xử lý toán tử.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến sử dụng tiếng Anh chuẩn snake_case (PEP 8), ghi chú giải thích logic bằng tiếng Việt có dấu, tuân thủ tuyệt đối quy định **không dùng từ khóa bị cấm** (`if`, `else`, `def`, `list`, `dict`...).
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đẩy bài nộp lên GitHub đúng định dạng thư mục `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & biểu thức:** Tối ưu số lượng biến trung gian, viết biểu thức logic gọn gàng, linh hoạt xử lý chuỗi nhập vào (ví dụ xử lý viết hoa/viết thường mã size hoặc mã thẻ bằng `.upper()`).
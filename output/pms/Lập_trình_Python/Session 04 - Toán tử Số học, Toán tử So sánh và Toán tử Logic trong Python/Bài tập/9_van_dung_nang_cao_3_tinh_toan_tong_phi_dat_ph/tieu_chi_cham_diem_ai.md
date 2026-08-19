# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Tính toán Tổng Phí Đặt Phòng và Kiểm Soát Điều Kiện Đặt Cọc Homestay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đầy đủ danh sách biến đầu vào (`price_per_night: float/int`, `num_nights: int`, `num_guests: int`, `is_early_checkin: bool`, `days_before_cancel: int`) và biến đầu ra (`room_cost`, `early_fee`, `extra_guest_fee`, `total_amount`, `deposit_required`, `is_valid_booking`, `is_full_refund_eligible`) kèm kiểu dữ liệu chuẩn xác.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Đề xuất logic tính toán thuần toán tử số học/so sánh (không dùng `if/else`, không dùng `and`/`or`/`not`) và vẽ sơ đồ Mermaid đúng 5 dạng hình chuẩn kỹ thuật (Oval, Parallelogram, Rectangle, Diamond, Flowline).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo chính xác các biến đầu vào với kiểu dữ liệu chuẩn (Type Hints), giá trị khởi tạo đúng ngữ cảnh nghiệp vụ homestay.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Triển khai công thức tính toán phụ thu check-in sớm, phụ thu người phát sinh, tổng chi phí thanh toán và số tiền cọc 50% chính xác 100%.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Áp dụng đúng công thức số học tính toán số khách vượt quá `(num_guests - 2) * (num_guests > 2)` để xử lý trường hợp số khách `<= 2` không bị phụ thu âm hoặc sai lệch.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kết hợp đúng toán tử so sánh để kiểm tra tính hợp lệ của booking trong phạm vi ngày `(1..30)` và số khách `(1..6)` cũng như điều kiện hoàn cọc `(days_before_cancel >= 3)`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Hiển thị báo cáo kết quả trên giao diện CLI rõ ràng, định dạng tiền tệ và các cờ trạng thái `True/False` dễ hiểu cho người dùng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tuân thủ nghiêm ngặt PEP 8, đặt tên biến tiếng Anh chuẩn `snake_case`, comment logic bằng tiếng Việt có dấu đầy đủ.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex9`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Đề xuất giải pháp biểu diễn cờ điều kiện logic kết hợp hoàn toàn bằng tính toán số học boolean (ví dụ: nhân các biểu thức so sánh dạng số nguyên) không phụ thuộc vào từ khóa rẽ nhánh hay hàm thư viện bên ngoài.

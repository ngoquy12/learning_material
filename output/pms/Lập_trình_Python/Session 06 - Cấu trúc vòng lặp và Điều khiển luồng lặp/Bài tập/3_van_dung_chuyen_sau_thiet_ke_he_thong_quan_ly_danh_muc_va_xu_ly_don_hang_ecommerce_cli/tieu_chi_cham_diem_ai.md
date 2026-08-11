### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Thiết kế hệ thống quản lý danh mục và xử lý đơn hàng E-Commerce CLI — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Xác định đầy đủ và chính xác kiểu dữ liệu Input/Output cho từng hàm (sử dụng đúng syntax Python 3.10+ type hints như `dict[str, dict]`, `list[dict]`, `tuple[bool, float, str]`).
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Vẽ sơ đồ khối hoặc viết mã giả mô tả rõ luồng kiểm tra dữ liệu trước khi trừ kho. Giải thích được giải pháp thay thế việc dùng `break`/`continue`/`while` bằng cờ hiệu (boolean flag) hợp lý.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Tổ chức đúng cấu trúc dữ liệu cho danh mục tồn kho và danh sách đơn hàng theo yêu cầu.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác giá trị chiết khấu cho cả hạng VIP và Regular theo đúng hạn mức giá trị đơn hàng.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Bắt chính xác lỗi số lượng đặt vượt quá tồn kho hiện có (`stock`) hoặc mã sản phẩm không tồn tại trong catalog. Tuân thủ tính nguyên tố (Atomicity): Không trừ kho bất kỳ mặt hàng nào nếu đơn hàng bị lỗi.
*   **[15 điểm] Tuân thủ giới hạn cú pháp bài học:** Không chứa bất kỳ từ khóa cấm nào (`while`, `break`, `continue`). Tất cả vòng lặp được triển khai bằng `for` hợp lệ.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xử lý và báo lỗi tường minh sử dụng `raise ValueError` hoặc `KeyError` với thông điệp tiếng Việt rõ ràng, trả ra thông báo lỗi tương ứng với từng trường hợp thất bại.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến/hàm bằng tiếng Anh theo chuẩn `snake_case`, chú thích code bằng tiếng Việt có dấu, định dạng 4 spaces chuẩn PEP 8.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session06_Ex03`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Thiết kế hàm báo cáo tổng hợp hiển thị dạng bảng Console chuyên nghiệp, tự động tính tỷ lệ đơn thành công (%) và tổng doanh thu thu về sau chiết khấu.
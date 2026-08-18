### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Điều chỉnh và Cập nhật Nhật ký Chuyến đi GrabRide — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Trình bày đầy đủ các biến đầu vào (danh sách khoảng cách `list[float]`, chỉ số cần cập nhật/xóa `int`, trạng thái giờ cao điểm `bool`) và đầu ra (danh sách mới, tổng số chuyến `int`, tổng quãng đường `float`, tổng doanh thu `float`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Thiết kế rõ ràng các bước thực hiện hoặc vẽ sơ đồ luồng Mermaid tuân thủ đúng 5 hình khối chuẩn (Oval, Hình bình hành, Hình chữ nhật, Hình thoi, Mũi tên). Thể hiện được chiến lược kiểm tra biên trước khi thao tác trên chỉ số danh sách.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Cập nhật/Xóa chính xác:**
    *   Khởi tạo đúng danh sách số thực `khoang_cach_chuyen`.
    *   Sử dụng đúng cú pháp cập nhật theo chỉ số: `khoang_cach_chuyen[1] = 3.5`.
    *   Sử dụng đúng cú pháp xóa phần tử theo chỉ số: `del khoang_cach_chuyen[3]`.
    *   Tuyệt đối không dùng `append()`, `pop()`, `insert()`, `remove()`.
*   **[15 điểm] Thuật toán tính toán cước phí và tổng hợp ca:**
    *   Sử dụng vòng lặp duyệt qua danh sách sau khi đã xóa phần tử lỗi.
    *   Áp dụng đúng công thức tính giá 2 km đầu (12.000 VNĐ) và các km tiếp theo (4.500 VNĐ/km).
    *   Tính đúng phụ phí hệ số `1.2` khi `is_gio_cao_diem = True`.
    *   Dùng `len()` để xác định chính xác số lượng chuyến đi còn lại.

#### **3. Kiểm chuẩn dữ liệu và Chặn sai sót biên (Edge Cases) — 30 điểm**
*   **[15 điểm] lỗi thường gặp phạm vi chỉ số (Index Out of Bounds Guard):** Có câu lệnh `if` kiểm tra điều kiện chỉ số hợp lệ `0 <= index < len(khoang_cach_chuyen)` trước khi tiến hành cập nhật hoặc xóa, tránh hiện tượng sập chương trình do `IndexError`.
*   **[15 điểm] Validation dữ liệu khoảng cách cập nhật:** Kiểm tra giá trị khoảng cách mới phải thỏa mãn điều kiện lớn hơn `0`. Trường hợp giá trị cập nhật không hợp lệ phải bỏ qua hoặc thông báo lỗi rõ ràng.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Thông điệp đầu ra định danh rõ ràng:** In ra màn hình các thông điệp báo trạng thái nghiệp vụ minh bạch (ví dụ: thông báo cập nhật chuyến đi thành công, thông báo xóa chuyến đi bị hủy, in kết quả tổng quãng đường và tổng doanh thu định dạng rõ ràng).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch chuẩn PEP 8:** Đặt tên biến dạng `snake_case` chuẩn tiếng Anh (ví dụ: `trip_distances`, `total_fare`, `peak_hour_surcharge`), viết chú thích logic bằng tiếng Việt có dấu, có sử dụng Type Hints (`list[float]`, `bool`, `float`, `int`).
*   **[5 điểm] Nộp bài GitHub:** Cấu trúc bài nộp đúng tên thư mục quy định `[Tên Lớp]_[Môn Học]_Session10_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Đề xuất được giải pháp quản lý chỉ số linh hoạt khi cần xóa nhiều phần tử liên tiếp mà không làm lệch chỉ số vòng lặp (duyệt ngược từ cuối danh sách lên đầu hoặc tính toán lại chỉ số động).
### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Điều chỉnh và Lọc dữ liệu Cước phí Chuyến xe GrabRide — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đúng kiểu dữ liệu Input (`trip_fares: list[int]`, `update_index: int`, `new_fare: int`, `delete_index: int`) và Output (danh sách đã cập nhật/xóa, tổng số chuyến xe `remaining_trips: int`, thông điệp cảnh báo).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày sơ đồ luồng Mermaid đầy đủ logic kiểm tra biên chỉ số và cập nhật/xóa. Sử dụng đúng 5 hình dạng chuẩn (Oval cho Bắt đầu/Kết thúc, Hình bình hành cho I/O, Hình thoi cho Điều kiện, Hình chữ nhật cho Tiến trình).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo danh sách cước phí `trip_fares` đúng kiểu dữ liệu với Type Hints chuẩn Python 3.12 (`list[int]`).
*   **[15 điểm] Thao tác Cập nhật và Xóa trên List:** Thực hiện cập nhật phần tử thành công qua cú pháp gán chỉ số `trip_fares[update_index] = new_fare` và xóa phần tử bằng `del trip_fares[delete_index]` đúng vị trí.

#### **3. Kiểm chuẩn dữ liệu và Chặn sai sót biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn sai sót chỉ số ngoài phạm vi (Index Out of Range Guard):** Kiểm tra chính xác chỉ số hợp lệ `0 <= index < len(trip_fares)` trước khi truy cập hoặc xóa. Không để phát sinh lỗi dừng chương trình (`IndexError`).
*   **[15 điểm] Validate dữ liệu cước phí tối thiểu:** Rào chắn điều kiện cước phí mới phải >= 12.000 VNĐ trước khi gán cập nhật.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** In thông báo lỗi rõ ràng, chuyên nghiệp bằng tiếng Việt khi chỉ số không hợp lệ hoặc giá cước vi phạm quy tắc tối thiểu.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Định danh biến 100% bằng tiếng Anh (`trip_fares`, `update_index`, `new_fare`, `remaining_trips`), tuân thủ chuẩn PEP 8, chú thích code bằng tiếng Việt có dấu. Tuân thủ tuyệt đối phạm vi kiến thức (không dùng `def`, `class`, `append`, `pop`, `dict`).
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session10_Ex8`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu hóa xử lý chuỗi thao tác:** Kiểm tra động độ dài danh sách `len()` ngay sau mỗi thao tác xóa để đảm bảo các thao tác kế tiếp sử dụng chỉ số chính xác mà không làm lệch danh sách.
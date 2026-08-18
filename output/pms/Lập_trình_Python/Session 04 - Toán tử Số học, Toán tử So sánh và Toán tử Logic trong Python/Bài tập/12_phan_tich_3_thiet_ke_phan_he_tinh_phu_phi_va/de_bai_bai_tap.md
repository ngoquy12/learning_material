## <center>[Phân tích 3] Thiết Kế Phân Hệ Tính Phụ Phí Và Phê Duyệt Hoàn Tiền Đặt Phòng Khách Sạn</center>

### **1. Mục tiêu**
*   **Phân tích nghiệp vụ**: Nắm vững cơ chế tính toán chi phí lưu trú, phụ thu check-in sớm, phụ thu người đi kèm và cờ phê duyệt hoàn tiền cọc trong phân hệ giao dịch của nền tảng đặt phòng khách sạn (Agoda / Traveloka).
*   **Tư duy giải thuật giới hạn**: Đề xuất ít nhất 2 phương án kỹ thuật để xử lý logic phụ phí và cờ phê duyệt chỉ bằng toán tử số học và toán tử so sánh (tuyệt đối không sử dụng câu lệnh rẽ nhánh `if/else`, không dùng toán tử logic `and/or/not`, không dùng vòng lặp hay cấu trúc dữ liệu nâng cao).
*   **Đánh giá & Thiết kế**: Xây dựng bảng so sánh trade-off 5 tiêu chí, vẽ lưu đồ thuật toán Mermaid đúng chuẩn và cài đặt mã nguồn Python 3.12 đạt chuẩn PEP 8.

---

### **2. Bối cảnh & Vấn đề**
Trong phân hệ xử lý tính toán giao dịch tốc độ cao của hệ thống Agoda / Traveloka, mỗi yêu cầu đặt phòng cần được tính toán tổng số tiền thanh toán thực tế và xác định cờ phê duyệt hoàn tiền cọc khi hủy phòng.

Do phân hệ tính toán này nằm trong core-engine xử lý hàng triệu giao dịch mỗi giây, nhóm kiến trúc phần mềm yêu cầu biểu diễn các cờ quy tắc nghiệp vụ và các khoản phụ thu trực tiếp bằng biểu thức số học và biểu thức so sánh logic nguyên bản (trả về `True`/`False` hoặc `1`/`0`), hoàn toàn không phụ thuộc vào câu lệnh rẽ nhánh điều khiển để tối ưu hóa hiệu năng tính toán.---

### **3. Quy tắc nghiệp vụ**

Hệ thống cần tiếp nhận các tham số đầu vào và tính toán các chỉ số tài chính theo quy tắc sau:

1.  **Tiền phòng cơ bản (`base_room_cost`)**:
    `base_room_cost = nightly_rate * num_nights`
2.  **Phụ thu Check-in sớm (`early_surcharge`)**:
    *   Nếu khách check-in sớm trước 12h trưa (`check_in_hour < 12`), tính phụ thu 30% giá phòng của 1 đêm (`nightly_rate * 0.3`).
    *   Nếu khách check-in từ 12h trưa trở đi (`check_in_hour >= 12`), phụ thu check-in sớm bằng `0.0`.
3.  **Phụ thu khách đi kèm (`guest_surcharge`)**:
    *   Trẻ em dưới 6 tuổi (`guest_age < 6`) được miễn phí phụ thu (`0.0`).
    *   Khách từ 6 tuổi trở lên (`guest_age >= 6`) chịu phụ thu cố định 200,000 VND cho mỗi đêm lưu trú (`200000 * num_nights`).
4.  **Tổng chi phí thanh toán (`total_payment`)**:
    `total_payment = base_room_cost + early_surcharge + guest_surcharge`
5.  **Phê duyệt hoàn 100% tiền cọc (`is_full_refund_approved`)**:
    *   Khách hủy phòng trước thời điểm check-in từ 3 ngày trở lên (`cancellation_days >= 3`) sẽ nhận cờ phê duyệt hoàn tiền cọc là `True`. Ngược lại nhận giá trị `False`.

[WARNING] **Phạm vi kiến thức bắt buộc (Scope Boundary)**:
*   Chỉ được phép sử dụng: Khai báo biến, kiểu dữ liệu cơ bản (`int`, `float`, `bool`), toán tử số học (`+`, `-`, `*`, `/`, `//`, `%`), toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`), Type Hints và hàm `print()`.
*   TUYỆT ĐỐI CẤM SỬ DỤNG: Câu lệnh rẽ nhánh (`if`, `else`, `elif`), toán tử logic (`and`, `or`, `not`), vòng lặp (`for`, `while`), List, Dict, Tuples, Class hoặc các thư viện bên ngoài.

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Kỹ sư Phần mềm tại Agoda / Traveloka, thực hiện báo cáo và mã nguồn nộp lại theo 3 phần bắt buộc:

#### **Phần 1: Báo cáo Đề xuất Đa giải pháp & So sánh Trade-off**
*   Tự nghiên cứu và đề xuất **ít nhất 2 phương án kỹ thuật** để biểu diễn các quy tắc phụ thu và cờ phê duyệt chỉ bằng toán tử số học và so sánh (không dùng `if/else`, không dùng `and/or/not`).
*   Xây dựng bảng so sánh Trade-off trực quan giữa 2 phương án theo đúng 5 tiêu chí: *Tốc độ thực thi (Speed)*, *Tiêu tốn bộ nhớ (Memory)*, *Khả năng bảo trì (Maintainability)*, *Độ rõ ràng mã nguồn (Readability)*, *Ngữ cảnh áp dụng phù hợp (Suitability)*.

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Lưu đồ Thuật toán**
*   Đưa ra lý giải kỹ thuật ngắn gọn giải thích lý do lựa chọn phương án tối ưu nhất cho hệ thống đặt phòng.
*   Vẽ lưu đồ thuật toán (Flowchart) bằng định dạng Mermaid minh họa luồng xử lý của phương án tối ưu.
    *   [REQUIREMENT] Lưu đồ Mermaid phải tuân thủ nghiêm ngặt 5 hình dạng tiêu chuẩn:
        1. Terminator (Bắt đầu/Kết thúc): `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`
        2. Input/Output (Đầu vào/Đầu ra): `[/Nhập thông tin đặt phòng/]` / `[/In hóa đơn thanh toán/]`
        3. Decision (Kiểm tra điều kiện): `Kiểm tra giờ check-in < 12?`
        4. Process (Tính toán/Hành động): `["Tính phụ thu check-in sớm"]`
        5. Flowline (Luồng thực hiện): mũi tên `-->` hoặc label `-->|Đúng|`

#### **Phần 3: Triển khai Mã nguồn Python & Xử lý Biên**
*   Cài đặt mã nguồn Python 3.12 hoàn chỉnh thực thi phương án tối ưu đã chọn.
*   Chương trình cần có các biến đầu vào mẫu để kiểm thử logic:
    *   `nightly_rate: float = 1500000.0`
    *   `num_nights: int = 3`
    *   `check_in_hour: int = 10`
    *   `guest_age: int = 25`
    *   `cancellation_days: int = 4`
*   In kết quả rõ ràng ra màn hình CLI bao gồm: Tiền phòng cơ bản, Phụ thu check-in sớm, Phụ thu khách đi kèm, Tổng thanh toán và Trạng thái hoàn tiền cọc.

---

### **5. Yêu cầu nộp bài**

Học viên cần nộp bài theo cấu trúc chuẩn:
*   Phần 1 & Phần 2: Trình bày chi tiết trong tệp báo cáo Markdown `REPORT.md`.
*   Phần 3: Đẩy mã nguồn chương trình Python lên kho chứa GitHub.
*   Cấu trúc thư mục nộp bài trên GitHub: `[Tên Lớp]_[Môn Học]_Session04_Ex12`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session04_Ex12`
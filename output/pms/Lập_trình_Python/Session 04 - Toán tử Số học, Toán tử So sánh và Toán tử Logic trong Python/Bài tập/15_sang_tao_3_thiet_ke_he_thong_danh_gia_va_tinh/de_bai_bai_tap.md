## <center>[Sáng tạo 3] Thiết kế Hệ thống Đánh giá và Tính Phụ phí Đặt phòng Khách sạn</center>

### **1. Mục tiêu**
*   **Tự thiết kế & Triển khai:** Tự đề xuất cấu trúc dữ liệu đầu vào/đầu ra (I/O Schema) và xây dựng thuật toán tính toán tổng chi phí đặt phòng (BookingReservation) trên hệ thống Agoda / Traveloka mà không phụ thuộc vào mã bộ khung có sẵn.
*   **Vận dụng toán tử cơ bản:** Áp dụng sáng tạo toán tử số học (`+`, `-`, `*`, `/`, `//`, `%`) và toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`) để tính phụ thu check-in sớm, phụ phí người vượt chuẩn và kiểm tra cờ phê duyệt đặt phòng.
*   **Trực quan hóa luồng dữ liệu:** Vẽ sơ đồ Mermaid Flowchart chuẩn hóa biểu diễn trọn vẹn vòng đời xử lý thông tin từ dữ liệu thô đến kết quả quyết toán hóa đơn (ServiceInvoice).
*   **Tuân thủ chuẩn công nghiệp:** Viết mã nguồn Python 3.12 đáp ứng chuẩn Clean Code (PEP 8, Type Hints, tên biến tiếng Anh, ghi chú tiếng Việt).

### **2. Bối cảnh & Vấn đề**
Nền tảng đặt phòng trực tuyến Agoda / Traveloka đang mở rộng dòng sản phẩm Homestay & Khách sạn cao cấp với cơ chế tính phí linh hoạt. Khi người dùng thực hiện giao dịch đặt phòng (`BookingReservation`), hệ thống cần tính toán chính xác tổng hóa đơn thanh toán (`ServiceInvoice`) dựa trên nhiều thông số nghiệp vụ thực tế: giá phòng theo ngày, thời gian check-in thực tế, số lượng khách phát sinh và số tiền đã đặt cọc.

Hiện tại, bộ phận kỹ thuật cần một module tính toán nguyên tử (atomic calculation module) có tốc độ phản hồi cao. Module này nhận thông tin từ yêu cầu đặt phòng, tự động tính toán tiền phòng cơ bản, tính các khoản phụ thu (check-in sớm trước 12h trưa, khách vượt sức chứa tiêu chuẩn) và xác minh cờ điều kiện duyệt phòng (`is_approved`). Do yêu cầu tối ưu hiệu năng tính toán ở tầng lõi, thuật toán phải được biểu diễn bằng các phép toán số học và so sánh đại số, loại bỏ hoàn toàn các cấu trúc rẽ nhánh phức tạp.### **3. Quy tắc nghiệp vụ**
Hệ thống tính toán cần tuân thủ nghiêm ngặt các quy định nghiệp vụ sau:
1. **Giá phòng cơ bản:** Tổng tiền phòng gốc = Số đêm lưu trú * Giá phòng mỗi đêm.
2. **Phụ thu Check-in sớm:** Khách nhận phòng trước 12:00 trưa chịu phụ thu 30% tiền phòng của 1 đêm (`EARLY_CHECKIN_SURCHARGE_RATE = 0.30`).
3. **Phụ thu khách vượt chuẩn:** Mỗi phòng có số lượng khách tiêu chuẩn (`standard_capacity`). Nếu tổng số khách thực tế vượt quá sức chứa tiêu chuẩn, mỗi khách vượt chuẩn chịu phụ phí cố định mỗi đêm (`EXTRA_GUEST_FEE = 150000` VNĐ/đêm/người). Trẻ em dưới 6 tuổi không bị tính vào số khách vượt chuẩn.
4. **Xác minh điều kiện phê duyệt đặt phòng (`is_booking_approved`):** Đơn đặt phòng chỉ đủ điều kiện phê duyệt khi đồng thời thỏa mãn:
   * Số tiền cọc đã thanh toán (`deposit_amount`) đạt tối thiểu 50% tổng giá trị tiền phòng gốc.
   * Tổng số khách thực tế không vượt quá sức chứa tối đa (`max_capacity`) của phòng.
5. **Ràng buộc phạm vi kỹ thuật:** Tuyệt đối KHÔNG sử dụng câu lệnh rẽ nhánh (`if/else`), vòng lặp (`for/while`), danh sách (`list`), từ điển (`dict`) hoặc các thư viện ngoài.

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phần mềm tại Agoda / Traveloka, tự thiết kế và hoàn thiện giải pháp theo 4 phần bắt buộc sau:

*   **Phần 1 — Tự thiết kế I/O Schema:**
    *   Tự xác định danh sách các biến đầu vào (`Input variables`) mô tả thông tin đặt phòng khách sạn (ví dụ: số đêm, giá phòng, giờ check-in, số khách, tiền cọc, ...) kèm theo kiểu dữ liệu `Type Hints`.
    *   Tự xác định danh sách các biến đầu ra (`Output variables`) thể hiện chi tiết chi phí và các trạng thái phê duyệt (phụ thu check-in, phụ thu người vượt chuẩn, tổng hóa đơn, cờ duyệt phòng).

*   **Phần 2 — Phân tích kịch bản bẫy dữ liệu (Edge Cases):**
    *   Chủ động phát hiện ít nhất 3 kịch bản bẫy dữ liệu hoặc tranh chấp nghiệp vụ có thể xảy ra trong thực tế (ví dụ: tiền cọc bị âm, giờ check-in vượt quá 24h, số khách vượt tối đa sức chứa phòng, ...).
    *   Đề xuất phương án xử lý đại số cho các bẫy dữ liệu này trong phạm vi toán tử cho phép.

*   **Phần 3 — Thiết kế Sơ đồ luồng dữ liệu (Mermaid Flowchart):**
    *   Vẽ sơ đồ luồng dữ liệu minh họa toàn bộ quá trình tiếp nhận dữ liệu đầu vào -> tính tiền phòng -> tính phụ thu -> xác minh cờ phê duyệt -> xuất hóa đơn.
    *   Sơ đồ phải tuân thủ nghiêm ngặt 5 dạng hình chuẩn:
        1. Terminator: `([Bắt đầu ...])` / `([Kết thúc ...])`
        2. Input / Output: `[/Đầu vào: .../]` / `[/Đầu ra: .../]`
        3. Decision: `Kiểm tra điều kiện?` với các nhánh `-->|Đúng|` và `-->|Sai|`
        4. Process: `["Thực hiện hành động / Tính toán"]`
        5. Flowline: Mũi tên kết nối `-->`

*   **Phần 4 — Triển khai mã nguồn Python:**
    *   Viết chương trình Python 3.12 hoàn chỉnh thực thi toàn bộ thiết kế đã lập.
    *   Mã nguồn tuân thủ chuẩn PEP 8: Đặt tên biến/hàm bằng tiếng Anh theo chuẩn `snake_case`, ghi chú giải thích logic bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex15`
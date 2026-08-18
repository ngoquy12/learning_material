### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Xử lý cập nhật phụ phí đặt phòng và đóng gói dữ liệu JSON — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** 
    * Xác định chính xác kiểu dữ liệu của đối tượng đầu vào `BookingReservation` (chứa `bookingId`: string, `roomPrice`: number, `checkInHour`: number, `tempToken`: string, `internalNote`: string).
    * Xác định chính xác kiểu dữ liệu của đầu ra (đối tượng JavaScript sau khi làm sạch và chuỗi `jsonPayload`: string).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:**
    * Trình bày logic kiểm tra đầu vào, áp dụng công thức tính phụ phí check-in sớm, cập nhật thuộc tính động qua Bracket Notation và xóa dữ liệu nhạy cảm bằng `delete`.
    * Vẽ sơ đồ luồng Mermaid Flowchart đúng quy chuẩn 5 hình (Oval, Parallelogram, Diamond, Rectangle, Flowline) không vi phạm lỗi cú pháp.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và thao tác thuộc tính:**
    * Tạo đối tượng `bookingReservation` lưu trữ đầy đủ các thuộc tính ban đầu.
    * Sử dụng Bracket Notation với biến động để thêm thành công thuộc tính `"emergency-contact"`.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:**
    * Tính đúng phụ thu 30% khi `checkInHour < 12.0` và gán chính xác thuộc tính `totalAmount`.
    * Sử dụng từ khóa `delete` để xóa bỏ hoàn toàn 2 thuộc tính `tempToken` và `internalNote`.
    * Thực hiện đúng chuyển đổi `JSON.stringify()` và `JSON.parse()`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:**
    * Kiểm tra tính hợp lệ của `checkInHour` (nằm ngoài khoảng `0.0` - `24.0` sẽ báo lỗi).
    * Kiểm tra tính hợp lệ của `roomPrice` (nhỏ hơn hoặc bằng 0 sẽ báo lỗi).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:**
    * Kiểm tra `bookingId` rỗng hoặc không phải dạng chuỗi ký tự hợp lệ.
    * Đảm bảo đối tượng JSON giải mã (`JSON.parse`) trùng khớp cấu trúc và không còn chứa các thuộc tính bị xóa.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    * Hiển thị thông điệp lỗi rõ ràng bằng Tiếng Việt khi dữ liệu đầu vào không hợp lệ (ví dụ: `[LỖI] Giá phòng không hợp lệ`, `[LỖI] Giờ check-in vượt quá phạm vi cho phép`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:**
    * Tên biến, hàm viết bằng Tiếng Anh chuẩn `camelCase`. Comment giải thích rõ ràng bằng Tiếng Việt có dấu. Không chứa emoji hoặc cú pháp bị cấm.
*   **[5 điểm] Nộp bài GitHub:**
    * Tạo cấu trúc thư mục nộp bài chuẩn quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:**
    * Đóng gói logic cập nhật và làm sạch vào một hàm xử lý tái sử dụng (reusable function), kiểm tra kỹ lưỡng đối tượng trước và sau khi `JSON.stringify()` để khẳng định không dư thừa dữ liệu trong bộ nhớ.
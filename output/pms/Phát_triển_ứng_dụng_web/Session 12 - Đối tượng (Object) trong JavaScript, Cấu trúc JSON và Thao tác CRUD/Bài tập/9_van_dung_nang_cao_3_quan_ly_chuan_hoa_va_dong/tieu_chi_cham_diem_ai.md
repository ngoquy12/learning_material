# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Quản Lý Chuẩn Hóa và Đóng Gói Dữ Liệu Đặt Phòng Khách Sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:**
    *   Liệt kê đầy đủ các thuộc tính của Object thô đầu vào (các thuộc tính số, chuỗi, boolean, key động có dấu gạch ngang như `"check-in-hour"`).
    *   Mô tả chính xác kiểu dữ liệu và cấu trúc của chuỗi JSON đầu ra.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:**
    *   Giải thích đúng sự khác biệt giữa `delete` và gán `undefined` đối với dung lượng bộ nhớ và kết quả `JSON.stringify()`.
    *   Vẽ sơ đồ Mermaid đáp ứng đúng chuẩn 5 hình dạng (Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Action/Process, Diamond cho Condition). Tuyệt đối không dùng Parallelogram cho bước tính toán.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và thao tác thuộc tính:**
    *   Khai báo Object thô chuẩn xác, minh họa truy cập đúng bằng Bracket Notation cho tên key có dấu gạch ngang (`"check-in-hour"`).
    *   Thêm mới và cập nhật thành công các thuộc tính `earlyCheckInFee`, `extraGuestFee`, `totalPayment`, `isPaid`.
*   **[15 điểm] Lập trình tính toán phụ phí nghiệp vụ:**
    *   Tính đúng 30% phụ thu check-in sớm nếu `"check-in-hour"` < 12.
    *   Tính đúng phụ thu khách phát sinh khi `adultsCount` > `standardCapacity` (miễn phí `childrenUnder6`).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Làm sạch dữ liệu nhạy cảm (Sanitization):**
    *   Sử dụng chính xác toán tử `delete` để xóa bỏ hoàn toàn 3 thuộc tính: `securityCode`, `tempToken`, `internalNote`.
    *   Đảm bảo đối tượng sau khi làm sạch không còn tồn tại các key này trong bộ nhớ.
*   **[15 điểm] Đóng gói và Giải mã JSON an toàn:**
    *   Chuyển đổi thành công đối tượng sang chuỗi JSON hợp lệ bằng `JSON.stringify()`.
    *   Xây dựng hàm `restoreAndValidateBooking(jsonString)` giải mã thành công bằng `JSON.parse()` và thực hiện validate các key bắt buộc (`bookingId`, `roomCode`, `totalPayment`).

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    *   Xử lý ngoại lệ khi truyền vào chuỗi JSON sai cú pháp hoặc chuỗi rỗng bằng khối `try...catch`.
    *   Báo lỗi rõ ràng bằng tiếng Việt khi thiếu một trong các thuộc tính bắt buộc sau khi giải mã.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:**
    *   Tên biến, tên hàm 100% bằng Tiếng Anh chuẩn (camelCase).
    *   Ghi chú giải thích logic bằng Tiếng Việt có dấu đầy đủ, rõ ràng.
*   **[5 điểm] Nộp bài GitHub:**
    *   Tạo repository và đặt tên thư mục theo đúng cú pháp hướng dẫn `[Tên Lớp]_[Môn Học]_Session12_Ex9`.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:**
    *   Viết hàm tiện ích reusable (ví dụ: `sanitizeObject(obj, keysToRemove)`) nhận vào danh sách các key cần xóa và trả về object sạch một cách linh hoạt, dễ bảo trì cho các thực thể khác trong hệ thống.

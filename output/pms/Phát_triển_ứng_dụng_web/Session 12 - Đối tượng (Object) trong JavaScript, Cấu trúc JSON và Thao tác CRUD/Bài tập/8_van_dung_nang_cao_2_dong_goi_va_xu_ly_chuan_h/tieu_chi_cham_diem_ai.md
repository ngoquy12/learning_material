### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Đóng gói và Xử lý Chuẩn hóa Dữ liệu Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** 
    *   Xác định chính xác kiểu dữ liệu và cấu trúc đối tượng `BookingReservation` (String, Number, Boolean, Key có ký tự đặc biệt).
    *   Xác định rõ ràng kết quả đầu ra bao gồm chuỗi JSON sạch và đối tượng được phục hồi từ JSON.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế sơ đồ luồng (Flowchart):**
    *   Đề xuất logic giải pháp rõ ràng, mạch lạc, giải thích lý do phải dùng `delete` thay vì gán `undefined`.
    *   Vẽ sơ đồ luồng Mermaid tuân thủ chính xác 5 dạng hình tiêu chuẩn: Oval `([Start/End])`, Bình hành `[/Input/Output/]`, Thoi `Condition?`, Chữ nhật `["Process"]`. Không dùng hình Bình hành cho các thao tác tính toán hay xóa thuộc tính.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:**
    *   Khai báo đối tượng Object Literal lưu trữ đầy đủ thông tin đặt phòng khách sạn.
    *   Định danh chính xác các key chứa ký tự đặc biệt như `early-checkin-fee`, `late-checkout-fee` và các trường nhạy cảm `tempSessionToken`, `internalCardCVV`.
*   **[15 điểm] Thao tác thuộc tính Đối tượng & Đóng gói JSON:**
    *   Sử dụng đúng Bracket Notation để truy cập và cộng dồn các thuộc tính phụ phí dynamic.
    *   Thêm/cập nhật thành công các thuộc tính mới (`totalAmount`, `isProcessed`, `exportTimestamp`) vào đối tượng.
    *   Sử dụng thành thạo toán tử `delete` để xóa bỏ hoàn toàn các trường dữ liệu tạm thời và nhạy cảm.
    *   Mã hóa thành công đối tượng thành chuỗi JSON bằng `JSON.stringify()`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng / Thiếu trường bắt buộc:**
    *   Kiểm tra sự tồn tại của các trường bắt buộc (`reservationId`, `guestName`, `roomCode`).
    *   Phát hiện và ngăn chặn quy trình nếu đối tượng thiếu dữ liệu quan trọng hoặc chứa giá trị không hợp lệ (ví dụ: giá phòng âm).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao & Phục hồi JSON:**
    *   Giải mã chuỗi JSON an toàn bằng `JSON.parse()`.
    *   Kiểm tra tính toàn vẹn của đối tượng sau khi parse, đảm bảo các trường đã bị `delete` không còn xuất hiện trong chuỗi JSON cũng như đối tượng mới.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    *   Bắt lỗi và ném ra ngoại lệ/thông điệp lỗi rõ ràng bằng tiếng Việt khi dữ liệu đầu vào thiếu trường bắt buộc hoặc khi thao tác parse chuỗi JSON thất bại.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** 
    *   Đặt tên biến, hàm 100% bằng tiếng Anh theo quy chuẩn `camelCase` (ví dụ: `sanitizeBookingData`, `parseReservationJson`).
    *   Viết ghi chú giải thích logic bằng tiếng Việt có dấu rõ ràng. Không sử dụng các từ khóa hoặc thư viện bị cấm.
*   **[5 điểm] Nộp bài GitHub:** 
    *   Tạo repository và đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex8`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & Dynamic Key Mapping:**
    *   Xây dựng hàm làm sạch dữ liệu nhận vào danh sách mảng các key cần xóa một cách linh hoạt (Dynamic Keys Deletion) thay vì hard-code tên key, giúp tái sử dụng module cho nhiều loại phiếu dịch vụ khác nhau trong hệ thống HOTEL_BOOKING.
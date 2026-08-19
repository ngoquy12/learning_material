# <center>[Vận dụng nâng cao 1] Xử lý cập nhật phụ phí đặt phòng và đóng gói dữ liệu JSON</center>

### **1. Mục tiêu**
*   **Kiến thức:** Thao tác thành thạo với đối tượng (Object Literal) trong JavaScript ES6+, truy cập thuộc tính qua Dot Notation và Bracket Notation (Dynamic Key Access), quản lý thuộc tính đối tượng bằng câu lệnh `delete`, và thực hiện chuyển đổi dữ liệu hai chiều với JSON (`JSON.stringify`, `JSON.parse`).
*   **Kỹ năng:** Phân tích dữ liệu đầu vào/đầu ra, thiết kế luồng xử lý bằng sơ đồ thuật toán (Flowchart), thực hiện cập nhật thông tin nghiệp vụ động và kiểm soát dữ liệu nhạy cảm trước khi đóng gói dữ liệu.
*   **Thái độ:** Rèn luyện tư duy lập trình cẩn trọng, chú trọng bảo mật thông tin và tối ưu dung lượng bộ nhớ khi truyền nhận dữ liệu.

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Đặt phòng Khách sạn & Homestay (HOTEL_BOOKING), khi một khách hàng đến nhận phòng (`BookingReservation`), nhân viên lễ tân cần thực hiện các thao tác kiểm tra và cập nhật đơn đặt phòng trên giao diện quản lý. Đơn đặt phòng khi được khởi tạo ban đầu lưu trữ các thuộc tính cơ bản như mã đặt phòng, tên khách hàng, giá phòng mỗi đêm, giờ nhận phòng dự kiến, cùng với các dữ liệu tạm thời để xác thực giao dịch (`tempToken`) và ghi chú nội bộ của nhân viên (`internalNote`).

Trong quá trình làm thủ tục check-in, nhân viên cần bổ sung thông tin liên hệ khẩn cấp (có tên key chứa ký tự đặc biệt `emergency-contact`), tính toán phụ phí nếu khách check-in sớm, loại bỏ các thuộc tính tạm thời và thông tin nội bộ nhạy cảm trước khi đóng gói dữ liệu đối tượng thành chuỗi JSON chuẩn để lưu trữ vào bộ nhớ hệ thống hoặc gửi đến cổng thanh toán.

### **3. Quy tắc nghiệp vụ**
1. **Quy tắc tính phụ phí check-in sớm:**
   * Giờ check-in tiêu chuẩn của khách sạn là từ `12.0` (12:00 PM) trở đi.
   * Nếu giờ check-in thực tế của khách nhỏ hơn `12.0` (ví dụ: `9.5` tức 9h30 sáng), hệ thống sẽ tính phụ phí check-in sớm bằng 30% giá phòng gốc.
   * Tổng tiền thanh toán `totalAmount` được thêm vào đối tượng đơn đặt phòng theo công thức: `totalAmount = roomPrice + earlyCheckInSurcharge`. Nếu không check-in sớm, `totalAmount = roomPrice`.
2. **Quy tắc cập nhật thuộc tính động:**
   * Cập nhật thông tin liên hệ khẩn cấp với tên key là `"emergency-contact"` (bắt buộc dùng Bracket Notation).
   * Giá trị liên hệ khẩn cấp có thể được truyền vào thông qua một biến động đại diện cho tên thuộc tính.
3. **Quy tắc làm sạch dữ liệu (Data Sanitization):**
   * Trước khi lưu trữ hoặc đóng gói JSON, hệ thống bắt buộc phải xóa hoàn toàn hai thuộc tính `tempToken` và `internalNote` khỏi đối tượng bằng từ khóa `delete` để đảm bảo an toàn thông tin.
4. **Quy tắc đóng gói và giải mã JSON:**
   * Chuyển đổi đối tượng sau khi làm sạch thành chuỗi JSON hợp lệ bằng `JSON.stringify()`.
   * Thực hiện parse chuỗi JSON vừa tạo về đối tượng JavaScript bằng `JSON.parse()` để xác nhận tính toàn vẹn dữ liệu.
5. **Quy tắc kiểm chuẩn đầu vào (Validation & Edge Cases):**
   * Mã đặt phòng (`bookingId`) không được để trống hoặc rỗng.
   * Giá phòng (`roomPrice`) phải là một số dương lớn hơn 0.
   * Giờ check-in (`checkInHour`) phải nằm trong khoảng từ `0.0` đến `24.0`.
   * Trường hợp dữ liệu đầu vào không hợp lệ, chương trình phải đưa ra thông điệp báo lỗi rõ ràng và dừng tiến trình xử lý.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Nộp dạng văn bản/Markdown)**
1. **Phân tích I/O (Input / Output):**
   * Liệt kê chi tiết các thông tin đầu vào (Input) cần cung cấp cho đối tượng đơn đặt phòng và các biến động.
   * Xác định rõ định dạng và kiểu dữ liệu đầu ra (Output) sau khi hoàn tất tính toán, xóa dữ liệu nhạy cảm và đóng gói JSON.
2. **Đề xuất giải pháp kỹ thuật:**
   * Trình bày hướng tiếp cận mã nguồn sử dụng các kiến thức đã học trong Session 12 (Dot Notation, Bracket Notation, Dynamic Key Access, `delete`, `JSON.stringify`, `JSON.parse`).
3. **Sơ đồ luồng xử lý (Mermaid Flowchart):**
   * Vẽ sơ đồ thuật toán thể hiện đầy đủ quy trình kiểm tra dữ liệu, tính phụ phí, cập nhật thuộc tính động, xóa thuộc tính tạm và đóng gói JSON.
   * Quy chuẩn ký hiệu Mermaid:
     * Hình Oval `([Bắt đầu/Kết thúc])` dùng cho điểm khởi đầu và kết thúc.
     * Hình Bình hành `[/Đầu vào: .../]` hoặc `[/Đầu ra: .../]` dùng cho Input/Output.
     * Hình Thoi `Kiểm tra điều kiện?` dùng cho câu lệnh rẽ nhánh.
     * Hình Chữ nhật `["Hành động/Tính toán"]` dùng cho các thao tác xử lý logic hoặc tính toán.

#### **Phần 2: Triển khai Mã nguồn (Coding)**
* Viết chương trình bằng JavaScript Vanilla (ES6+) thực hiện trọn vẹn nghiệp vụ nêu trên.
* Mã nguồn cần được tổ chức sạch sẽ, đặt tên biến/hàm bằng tiếng Anh theo chuẩn `camelCase`, comment giải thích logic bằng tiếng Việt có dấu đầy đủ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
* Phần phân tích/báo cáo và mã nguồn triển khai.
* Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex7`.
  * Ví dụ: `HNKS25CNTT1_Core_Session12_Ex7`

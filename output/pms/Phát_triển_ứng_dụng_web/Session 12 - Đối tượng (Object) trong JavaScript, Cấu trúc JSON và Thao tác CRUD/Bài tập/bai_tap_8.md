# <center>[Vận dụng nâng cao 2] Đóng gói và Xử lý Chuẩn hóa Dữ liệu Đặt phòng Khách sạn</center>

### **1. Mục tiêu**
*   **Thao tác nâng cao với Đối tượng (Object Literal)**: Thực hiện khai báo, truy xuất, cập nhật thuộc tính động (Dynamic Key Access), sử dụng thành thạo Dot Notation và Bracket Notation trong các bối cảnh dữ liệu phức tạp.
*   **Quản lý thuộc tính và Bảo mật dữ liệu**: Sử dụng toán tử `delete` để loại bỏ chính xác các trường dữ liệu tạm thời, dữ liệu nhạy cảm của khách hàng trước khi đồng bộ hệ thống.
*   **Chuyển đổi và Đóng gói JSON**: Thành thạo việc mã hóa đối tượng JavaScript thành chuỗi JSON (`JSON.stringify()`) và giải mã chuỗi JSON thành đối tượng (`JSON.parse()`) phục vụ việc truyền nhận dữ liệu đặt phòng.
*   **Tư duy Phân tích & Lập trình phòng thủ**: Tự xây dựng báo cáo phân tích thiết kế, kiểm tra dữ liệu đầu vào và xử lý các lỗi bẫy biên phát sinh trong quy trình nghiệp vụ thực tế.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng khách sạn và homestay trực tuyến (tương tự Agoda/Traveloka), khi khách hàng hoàn tất quy trình chọn phòng và thanh toán, hệ thống sẽ khởi tạo một đối tượng lưu giữ toàn bộ thông tin đơn đặt phòng (`BookingReservation`). Dữ liệu này chứa thông tin khách hàng (`GuestInfo`), thông tin phòng (`HotelRoom`), các loại phụ phí phát sinh dynamic (như `early-checkin-fee`, `late-checkout-fee`, `extra-adult-fee`), cùng với các token phiên làm việc tạm thời (`tempSessionToken`, `internalCardCVV`) được sinh ra trong quá trình giao dịch.

Trước khi lưu trữ thông tin xuống bộ nhớ hoặc gửi chuỗi dữ liệu sang hệ thống đối soát tài chính của đối tác, phần mềm yêu cầu:
1. Tính toán lại tổng chi phí lưu trú dựa trên giá phòng cơ bản và các trường phụ phí dynamic chứa ký tự đặc biệt.
2. Cập nhật các trường thông tin trạng thái đặt phòng và thời gian đóng gói dữ liệu.
3. Loại bỏ triệt để các thuộc tính nhạy cảm và dữ liệu tạm thời để đảm bảo an toàn thông tin và tránh lãng phí dung lượng lưu trữ.
4. Chuyển đổi đối tượng đã làm sạch thành chuỗi JSON chuẩn hóa và hỗ trợ phục hồi chuỗi JSON đó trở lại đối tượng JavaScript để truy xuất thông tin chi tiết.

### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý thông tin phiếu đặt phòng phải tuân thủ nghiêm ngặt các quy tắc sau:

1.  **Quy tắc truy cập và cập nhật thuộc tính dynamic**:
    *   Các trường phụ phí có tên chứa dấu gạch ngang (ví dụ: `early-checkin-fee`, `late-checkout-fee`) bắt buộc phải được truy cập và thao tác thông qua Bracket Notation (`obj["key-name"]`).
    *   Tổng tiền thanh toán của đơn đặt phòng phải được cập nhật động vào đối tượng thông qua thuộc tính `totalAmount`.
2.  **Quy tắc làm sạch dữ liệu (Data Sanitization)**:
    *   Bắt buộc loại bỏ hoàn toàn các trường dữ liệu nhạy cảm hoặc tạm thời gồm: `tempSessionToken`, `internalCardCVV`, `checkoutStep` ra khỏi đối tượng bằng toán tử `delete`.
    *   [WARNING] Việc gán giá trị `undefined` hoặc `null` cho trường dữ liệu không được chấp nhận vì thuộc tính vẫn sẽ tồn tại trong bộ nhớ đối tượng và gây nguy cơ lộ thông tin.
3.  **Quy tắc đóng gói và phục hồi JSON**:
    *   Đối tượng sau khi làm sạch phải được chuyển đổi thành chuỗi JSON chuẩn thông qua `JSON.stringify()`.
    *   Hệ thống phải có khả năng giải mã chuỗi JSON ngược lại thành đối tượng JavaScript thông qua `JSON.parse()` và truy xuất chính xác các thông tin đã cập nhật.
4.  **Quy tắc kiểm chuẩn và bảo vệ biên (Validation & Edge Cases)**:
    *   Nếu dữ liệu đối tượng đầu vào bị thiếu một trong các trường cốt lõi (`reservationId`, `guestName`, `roomCode`), hệ thống phải ngăn chặn xử lý và phát tín hiệu lỗi cụ thể.
    *   Nếu chuỗi JSON truyền vào hàm giải mã bị sai cú pháp, hệ thống phải xử lý an toàn, tránh để ứng dụng bị dừng đột ngột.

### **4. Yêu cầu bài toán**

[REQUIREMENT] Bài tập được chia thành 2 phần bắt buộc:

#### **Phần 1: Báo cáo Phân tích I/O & Thiết kế Giải pháp (Thực hiện trước khi viết code)**
1.  **Phân tích Đầu vào / Đầu ra (Input/Output)**:
    *   Xác định cấu trúc dữ liệu của đối tượng đặt phòng ban đầu (kiểu dữ liệu của các thuộc tính, tên key chuẩn và key chứa ký tự đặc biệt).
    *   Xác định kết quả đầu ra (chuỗi JSON chuẩn và đối tượng đã phục hồi).
2.  **Đề xuất giải pháp kỹ thuật & Luồng xử lý**:
    *   Mô tả các bước thực hiện để bổ sung thuộc tính dynamic, tính toán dữ liệu, xóa trường nhạy cảm và đóng gói JSON.
    *   Vẽ sơ đồ luồng dữ liệu (Flowchart) minh họa quy trình từ khi tiếp nhận đối tượng thô đến khi tạo ra chuỗi JSON sạch.
    *   *Yêu cầu sơ đồ Mermaid*: Bắt buộc tuân thủ 5 dạng hình chuẩn:
        *   Hình Oval `([Bắt đầu / Kết thúc])`
        *   Hình Bình hành `[/Đầu vào / Đầu ra/]`
        *   Hình Thoi `Kiểm tra điều kiện?`
        *   Hình Chữ nhật `["Thực hiện xử lý / Tính toán"]`
        *   Mũi tên luồng `-->`

#### **Phần 2: Triển khai Mã nguồn (Implementation & Error Guards)**
Sinh viên tự xây dựng mã nguồn bằng JavaScript (ES6+) thực hiện trọn vẹn các yêu cầu sau:
1.  Khai báo đối tượng phiếu đặt phòng (`BookingReservation`) ban đầu chứa đầy đủ các trường thông tin theo mô tả nghiệp vụ.
2.  Xây dựng module/hàm thực hiện làm sạch dữ liệu, cập nhật tổng chi phí và đóng gói thành chuỗi JSON.
3.  Xây dựng module/hàm thực hiện nhận chuỗi JSON, giải mã về đối tượng và kiểm tra truy xuất thuộc tính dynamic.
4.  Viết mã kiểm thử cho các trường hợp dữ liệu hợp lệ và các trường hợp bẫy biên (thiếu thông tin bắt buộc, chuỗi JSON lỗi).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (Phần 1) và mã nguồn triển khai (Phần 2) trong cùng một file bài làm hoặc thư mục dự án.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex8`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session12_Ex8`

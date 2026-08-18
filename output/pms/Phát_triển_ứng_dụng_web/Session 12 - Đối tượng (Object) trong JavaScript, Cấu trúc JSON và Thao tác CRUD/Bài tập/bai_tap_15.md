#

# <center>[Sáng tạo 3] Thiết Kế Hệ Thống Đóng Gói Và Quản Lý Hóa Đơn Đặt Phòng Khách Sạn</center>

### **1. Mục tiêu**
*   Tự thiết kế cấu trúc Object Literal đại diện cho các thực thể dữ liệu nghiệp vụ `BookingReservation` và `ServiceInvoice` trong ứng dụng đặt phòng khách sạn.
*   Thực hiện nhuần nhuyễn các thao tác CRUD trên Object bằng JavaScript Vanilla (sử dụng Dot Notation, Bracket Notation, Dynamic Key Access và từ khóa `delete`).
*   Thao tác đóng gói và phục hồi dữ liệu hai chiều qua định dạng JSON (`JSON.stringify()` và `JSON.parse()`) trước khi truyền tải hoặc lưu trữ.
*   Phát triển tư duy thiết kế phần mềm độc lập: tự xác định I/O Schema, tự phân tích bẫy lỗi bối cảnh (Edge Cases), vẽ sơ đồ luồng dữ liệu Mermaid và triển khai mã nguồn hoàn chỉnh.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng khách sạn trực tuyến (tương tự Agoda hoặc Traveloka), việc quản lý dữ liệu đặt phòng và tính toán hóa đơn thanh toán đòi hỏi tính chính xác cao. Khi một giao dịch đặt phòng (`BookingReservation`) chuyển sang giai đoạn quyết toán hóa đơn (`ServiceInvoice`), thông tin dữ liệu không cố định mà liên tục biến động:
1.  **Cập nhật dữ liệu phụ phí**: Hệ thống cần bổ sung các trường dữ liệu mới vào Object (ví dụ: phụ phí check-in sớm, dịch vụ ăn uống phát sinh, giảm giá chính sách trẻ em).
2.  **Làm sạch dữ liệu nhạy cảm**: Trước khi đóng gói hóa đơn thành chuỗi JSON để lưu trữ hoặc gửi sang đối tác thanh toán, các thông tin tạm thời hoặc thông tin nhạy cảm (như `tempAuthToken`, `internalPasskey`, `debugSessionId`) phải được xóa bỏ hoàn toàn khỏi Object nhằm đảm bảo an toàn bộ nhớ và an ninh dữ liệu.
3.  **Đóng gói và Giải mã JSON**: Chuyển đổi dữ liệu Object sang chuỗi JSON và phục hồi lại Object từ JSON khi người dùng tra cứu lịch sử đơn hàng, đồng thời đảm bảo xử lý chính xác các thuộc tính có tên key chứa ký tự đặc biệt (ví dụ: `service-charge`, `early-discount`).

### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý hóa đơn cần tuân thủ các quy tắc nghiệp vụ thực tế sau:
*   **Phụ thu Check-in sớm**: Nếu khách nhận phòng trước 12:00 trưa, bổ sung thuộc tính phụ thu check-in sớm (`earlyCheckInSurcharge`) bằng 30% giá phòng một đêm vào Object hóa đơn.
*   **Chính sách trẻ em**: Trẻ em dưới 6 tuổi đi cùng được miễn phí hoàn toàn tiền lưu trú phát sinh.
*   **Hủy phòng & Hoàn cọc**: Hủy phòng trước 3 ngày được hoàn 100% tiền cọc (xóa bỏ hoặc cập nhật thuộc tính phí hủy phòng `cancellationFee`).
*   **Làm sạch thông tin an toàn**: Sử dụng từ khóa `delete` để xóa triệt để các thuộc tính tạm thời trước khi đóng gói dữ liệu với `JSON.stringify()`. Không gán giá trị `undefined` vì việc gán `undefined` vẫn giữ lại tên key trong bộ nhớ Object.
*   **Truy xuất Dynamic Key & Key đặc biệt**: Truy cập các thuộc tính có ký tự đặc biệt (như dấu gạch ngang `-`) hoặc truy cập qua biến số bằng Bracket Notation `object[key]`.

### **4. Yêu cầu bài toán**
Bài tập yêu cầu học viên tự chủ hoàn toàn trong việc thiết kế và triển khai giải pháp kỹ thuật qua 4 phần:

*   **Phần 1: Thiết kế I/O Schema (Cấu trúc dữ liệu)**
    *   Tự xây dựng cấu trúc Object ban đầu cho đơn đặt phòng (`BookingReservation` hoặc `ServiceInvoice`).
    *   Tự thiết kế cấu trúc Object sau khi qua luồng biến đổi CRUD (thêm phụ phí, xóa trường nhạy cảm).
    *   Tự định nghĩa định dạng chuỗi JSON kết xuất và Object khôi phục sau khi `JSON.parse()`.

*   **Phần 2: Phân tích bẫy dữ liệu (Edge Cases)**
    *   Liệt kê ít nhất 3 tình huống bẫy lỗi hoặc xung đột dữ liệu thực tế (Ví dụ: Lỗi cú pháp khi dùng Dot Notation cho key chứa gạch ngang, việc gán `undefined` gây lãng phí bộ nhớ so với `delete`, hoặc cố gắng truy cập thuộc tính trực tiếp trên chuỗi JSON chưa qua `JSON.parse()`).
    *   Đề xuất giải pháp xử lý bằng mã nguồn JS cho các bẫy lỗi đã kê khai.

*   **Phần 3: Sơ đồ luồng dữ liệu (Mermaid Flowchart)**
    *   Vẽ sơ đồ luồng mô tả toàn bộ vòng đời của hóa đơn: Khởi tạo Object -> Tính toán & Thêm/Sửa thuộc tính CRUD -> Xóa trường tạm thời bằng `delete` -> Đóng gói JSON (`JSON.stringify`) -> Giải mã JSON (`JSON.parse`) -> Truy xuất dynamic key.
    *   *Yêu cầu chuẩn hóa hình dạng Mermaid*:
        *   Hình Oval/Stadium `([Bắt đầu...])` / `([Kết thúc...])` cho điểm khởi đầu và kết thúc.
        *   Hình Chữ nhật `["Thực hiện tính toán / CRUD"]` cho tất cả các thao tác xử lý logic, tính phụ thu, xóa key.
        *   Hình Thoi `Kiểm tra điều kiện?` cho luồng rẽ nhánh quyết định.
        *   Hình Bình hành `[/Đầu vào dữ liệu/]` và `[/Đầu ra JSON/]` CHỈ dùng cho dữ liệu vào/ra.

*   **Phần 4: Triển khai mã nguồn (JavaScript ES6+)**
    *   Viết mã nguồn JS Vanilla hoàn chỉnh thực hiện từ đầu đến cuối luồng xử lý trên.
    *   Sử dụng mã sạch (Clean Code), tên biến bằng tiếng Anh, chú thích logic rõ ràng bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session12_Ex15`
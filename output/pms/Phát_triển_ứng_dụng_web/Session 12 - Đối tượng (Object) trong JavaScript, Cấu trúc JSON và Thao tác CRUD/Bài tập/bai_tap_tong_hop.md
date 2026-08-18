#

# <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp (HOTEL_BOOKING)</center>

### **1. Mục tiêu**
- **Kiến thức**: Hiểu và vận dụng thành thạo cú pháp khai báo Object Literal (Key-Value), 3 phương thức truy cập thuộc tính (Dot Notation, Bracket Notation, Dynamic Key Access); làm chủ các thao tác CRUD thuộc tính đối tượng (Thêm, Sửa, Xóa thuộc tính bằng toán tử delete); đóng gói và giải mã dữ liệu cấu trúc JSON bằng `JSON.stringify()` và `JSON.parse()`.
- **Kỹ năng**: Rèn luyện kỹ năng phân tích cấu trúc dữ liệu đối tượng thực tế trong hệ thống quản lý khách sạn, xử lý linh hoạt các tên key đặc biệt, tránh các bẫy lỗi phổ biến như gán `undefined` thay vì xóa thuộc tính, truy cập nhầm key chưa parse JSON hoặc thiếu nháy trong ngoặc vuông.
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu trong thời gian khoảng 30 phút.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
Trong phân hệ Quản lý Đặt phòng Khách sạn (HOTEL_BOOKING), mỗi giao dịch đặt phòng của khách hàng được đại diện bởi một đối tượng thông tin phiếu đặt phòng (`bookingData`). Đối tượng này chứa các thuộc tính đa dạng như mã phiếu, tên khách hàng, loại phòng, đơn giá, trạng thái và một số thuộc tính chứa ký tự đặc biệt đại diện cho thông tin cấu hình phòng (ví dụ: `room-number`).

Trong quá trình vận hành, nhân viên thu ngân có thể cần cập nhật lại giá tiền, thêm dịch vụ đi kèm, điều chỉnh số phòng, hoặc loại bỏ các thuộc tính nhạy cảm/tạm thời (như mã OTP xác thực giao dịch) trước khi lưu trữ. Cuối cùng, dữ liệu phiếu đặt phòng hoàn chỉnh cần được đóng gói thành chuỗi chuẩn JSON để lưu xuống cơ sở dữ liệu hoặc gửi qua API, đồng thời mô phỏng quá trình nhận lại chuỗi JSON và chuyển đổi ngược về đối tượng JavaScript để hiển thị cho người dùng.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**

- Chức năng 1: Khởi tạo phiếu đặt phòng và truy xuất dữ liệu đa phương thức
  - **Nghiệp vụ**: Khai báo một đối tượng phiếu đặt phòng khách sạn ban đầu gồm các thông tin chính (Mã đặt phòng, Tên khách hàng, Loại phòng, Đơn giá mỗi đêm, Trạng thái thanh toán, và một key có ký tự đặc biệt chứa gạch ngang là `room-number`). Thực hiện truy cập và in thông tin ra màn hình bằng 3 phương thức khác nhau: sử dụng Dot Notation cho key tiêu chuẩn, sử dụng Bracket Notation cho key chứa ký tự đặc biệt, và sử dụng biến lưu tên thuộc tính động (Dynamic Key Access) để truy xuất dữ liệu loại phòng.
  - **Đầu vào (Input)**: Đối tượng thông tin đặt phòng ban đầu và tên thuộc tính động cần truy vấn.
  - **Đầu ra (Output)**: Kết quả truy xuất dữ liệu phiếu đặt phòng hiển thị tương ứng với 3 phương thức truy cập.

- Chức năng 2: Cập nhật thông tin phiếu và làm sạch thuộc tính thừa (CRUD Object)
  - **Nghiệp vụ**: Thực hiện thêm thuộc tính mới ghi nhận dịch vụ bổ sung (ăn sáng, đưa đón sân bay), cập nhật lại đơn giá phòng theo khung giờ ưu đãi, thêm thông tin địa chỉ khách hàng bằng key đặc biệt (dùng dấu gạch ngang), và loại bỏ hoàn toàn thuộc tính mã xác thực tạm thời khỏi đối tượng bằng toán tử `delete` để đảm bảo an toàn thông tin (không gán giá trị `undefined`).
  - **Đầu vào (Input)**: Đối tượng đặt phòng hiện tại, dữ liệu điều chỉnh giá, dịch vụ bổ sung, địa chỉ mới và mã tạm thời cần xóa.
  - **Đầu ra (Output)**: Đối tượng phiếu đặt phòng hoàn chỉnh đã được cập nhật đầy đủ thông tin mới và loại bỏ triệt để thuộc tính tạm thời.

- Chức năng 3: Đóng gói dữ liệu JSON và khôi phục đối tượng JS
  - **Nghiệp vụ**: Đóng gói toàn bộ đối tượng phiếu đặt phòng đã làm sạch thành chuỗi dữ liệu định dạng JSON để chuẩn bị truyền qua hệ thống. Sau đó, tiến hành giải mã chuỗi JSON này trở lại thành một đối tượng JavaScript độc lập và kiểm tra tính hợp lệ của dữ liệu sau khi khôi phục bằng cách truy xuất lại tên khách hàng và số phòng.
  - **Đầu vào (Input)**: Đối tượng phiếu đặt phòng đã qua xử lý ở Chức năng 2.
  - **Đầu ra (Output)**: Chuỗi JSON chuẩn được đóng gói và dữ liệu thuộc tính của đối tượng sau khi giải mã khôi phục thành công.

### **4. Yêu cầu nộp bài**
Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_Session12_Demo`.
Ví dụ: `HNKS25CNTT1_Core_Session12_Demo`
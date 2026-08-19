# <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp (CLINIC_APPOINTMENT)</center>

### **1. Mục tiêu**
- **Kiến thức**: 
  - Thấu hiểu cơ chế V8 Engine biên dịch và thực thi mã nguồn JavaScript tách biệt trong tệp `script.js` ngoài, đặt thẻ script tối ưu trước thẻ đóng `</body>`.
  - Phân biệt và ứng dụng chính xác phạm vi hoạt động (scope) cùng tính chất thay đổi (mutability) của `const` và `let` theo đúng quy chuẩn ES6 và quy tắc đặt tên `camelCase`.
  - Thành thạo kỹ thuật ép kiểu dữ liệu minh bạch (`Number()`) để tránh lỗi nối chuỗi ngoài ý muốn từ dữ liệu đầu vào của trình duyệt.
  - Sử dụng thành thạo chuỗi nội suy Template Literals (dấu backticks `` `${}` ``) để đóng gói thông tin xuất ra Console và Alert.
- **Kỹ năng**: 
  - Khởi tạo và cấu hình cấu trúc dự án Web tiêu chuẩn trong môi trường Cursor AI / VS Code kết hợp chạy Live Server.
  - Kiểm tra và thực thi mã nguồn JS trực tiếp trên DevTools Console và Terminal Node.js.
  - Kiểm tra kiểu dữ liệu biến bằng `typeof` và phát hiện sớm các lỗi cú pháp gán lại giá trị cho hằng số (`const`).
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
Hệ thống quản lý phòng khám y tế Rikkeicare (`CLINIC_APPOINTMENT`) đang vận hành quy trình tiếp đón và lập phiếu thu phí khám sơ bộ cho bệnh nhân tại quầy lễ tân. Hiện tại, dữ liệu nhập từ người dùng thông qua trình duyệt luôn trả về dạng chuỗi văn bản, gây ra nguy cơ sai lệch tính toán số học tiền khám nếu không được ép kiểu chuẩn xác. 

Giảng viên sẽ minh họa trực tiếp (Live-Demo) việc thiết lập cấu trúc tệp HTML5/JS chuẩn V8 Engine, khai báo hệ thống thông tin phòng khám bằng hằng số `const`, thu thập thông tin bệnh nhân và chi phí dịch vụ bằng `let` kết hợp `prompt()`, ép kiểu dữ liệu an toàn và xuất hóa đơn tiếp đón chi tiết qua `console.log()` và `alert()`.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**

- **Chức năng 1: Khởi tạo thông tin hệ thống phòng khám và tiếp nhận bệnh nhân**
  - **Nghiệp vụ**: Khai báo các thông tin cố định của hệ thống phòng khám (Tên phòng khám, Mã định danh phân hệ tiếp đón, Phí dịch vụ cố định) bằng hằng số `const` với quy tắc `camelCase`. Tiếp nhận họ tên bệnh nhân và số điện thoại từ bàn phím.
  - **Đầu vào (Input)**: Chuỗi nhập họ tên bệnh nhân và chuỗi nhập số điện thoại từ cửa sổ `prompt()`.
  - **Đầu ra (Output)**: Hiển thị dòng trạng thái khởi tạo phiếu khám thành công cùng tên phòng khám lên DevTools Console.

- **Chức năng 2: Thu thập chi phí dịch vụ khám và ép kiểu dữ liệu số học**
  - **Nghiệp vụ**: Thu thập giá tiền khám chuyên khoa và giá tiền xét nghiệm sơ bộ từ người dùng. Thực hiện ép kiểu dữ liệu minh bạch từ String sang Number để tránh lỗi toán tử cộng chuỗi. Tính tổng chi phí khám bệnh nhân cần thanh toán.
  - **Đầu vào (Input)**: Giá tiền khám chuyên khoa (dạng chuỗi) và giá tiền xét nghiệm (dạng chuỗi) nhập vào qua `prompt()`.
  - **Đầu ra (Output)**: Kết quả tổng chi phí khám (kiểu Number) và kiểm tra xác minh kiểu dữ liệu của biến số sau khi ép kiểu ra Console qua toán tử `typeof`.

- **Chức năng 3: Đóng gói và xuất thông tin phiếu hẹn thu phí qua Template Literals**
  - **Nghiệp vụ**: Đóng gói toàn bộ các thông tin đã xử lý (Tên phòng khám, Mã tiếp đón, Họ tên bệnh nhân, Số điện thoại, Chi tiết chi phí và Tổng tiền) thành một thông điệp hóa đơn hoàn chỉnh bằng kỹ thuật Template Literals.
  - **Đầu vào (Input)**: Tập hợp các biến số `const` và `let` đã được thu thập và tính toán từ Chức năng 1 và Chức năng 2.
  - **Đầu ra (Output)**: In phiếu thu tiền chi tiết dạng dòng văn bản chuẩn hóa ra DevTools Console (`console.log()`) và bật cửa sổ thông báo kết quả giao dịch cho lễ tân (`alert()`).

### **4. Yêu cầu nộp bài**
Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_Session02_Demo`.
Ví dụ: `HNKS25CNTT1_Core_Session02_Demo`

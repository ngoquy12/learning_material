# <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp (GRAB_RIDE)</center>

### **1. Mục tiêu**
- **Kiến thức**: Tích hợp các kiến thức cốt lõi về danh sách động (Mutable List) trong Python 3.12, bao gồm: khởi tạo danh sách, truy xuất và cập nhật phần tử qua chỉ số (index), xóa phần tử bằng câu lệnh `del` và đo độ dài danh sách bằng hàm `len()`.
- **Kỹ năng**: Rèn luyện kỹ năng theo dõi luồng biến đổi dữ liệu của danh sách, thao tác chính xác trên các chỉ số index và tổ chức mã nguồn chuẩn PEP 8 kết hợp Type Hints trong môi trường Cursor/Windsurf AI IDE.
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
Hệ thống GrabRide cần quản lý danh sách giá cước (đơn vị: nghìn VNĐ) của các chuyến xe được ghi nhận trong một ca trực của tài xế. Trong quá trình vận hành thực tế, một số chuyến xe bị thay đổi cước phí do phụ phí thời tiết/kẹt xe, hoặc một số chuyến xe bị hủy do khách đổi ý. Giảng viên sẽ thực hiện demo trực tiếp quy trình quản lý dữ liệu ca trực bao gồm: khởi tạo danh sách cước phí ban đầu, cập nhật lại cước phí của một chuyến xe tại vị trí chỉ số xác định, xóa bỏ chuyến xe bị hủy ra khỏi danh sách và đếm số lượng chuyến xe hoàn tất còn lại.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**
- **Chức năng 1: Cập nhật cước phí chuyến xe theo vị trí chỉ số**
  - **Nghiệp vụ**: Hệ thống nhận thông tin thay đổi cước phí của một chuyến xe cụ thể. Giảng viên thao tác ghi đè giá trị mới vào đúng vị trí chỉ số (index) của chuyến xe đó trong danh sách cước phí ca trực.
  - **Đầu vào (Input)**: Danh sách cước phí ban đầu, vị trí chỉ số chuyến xe cần chỉnh sửa (số nguyên), giá trị cước phí mới (số nguyên).
  - **Đầu ra (Output)**: In ra màn hình danh sách cước phí trước và sau khi được cập nhật thành công.

- **Chức năng 2: Xóa chuyến xe bị hủy khỏi ca trực**
  - **Nghiệp vụ**: Khi có chuyến xe bị hủy, sử dụng câu lệnh xóa phần tử tại vị trí chỉ số tương ứng để loại bỏ cước phí chuyến xe đó khỏi danh sách, làm thay đổi trực tiếp cấu trúc danh sách ban đầu.
  - **Đầu vào (Input)**: Danh sách cước phí hiện tại, vị trí chỉ số chuyến xe bị hủy (số nguyên).
  - **Đầu ra (Output)**: In ra màn hình thông báo xóa thành công và danh sách cước phí cập nhật mới nhất.

- **Chức năng 3: Thống kê số lượng chuyến xe còn lại trong ca**
  - **Nghiệp vụ**: Truy xuất tổng số lượng chuyến xe hợp lệ còn tồn tại trong danh sách ca trực sau khi đã thực hiện xong các thao tác cập nhật và xóa.
  - **Đầu vào (Input)**: Danh sách cước phí sau khi xử lý.
  - **Đầu ra (Output)**: In ra màn hình thông báo tổng số lượng chuyến xe thực tế còn lại.

### **4. Yêu cầu nộp bài**
Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_Session10_Demo`.
Ví dụ: `HNKS25CNTT1_Core_Session10_Demo`

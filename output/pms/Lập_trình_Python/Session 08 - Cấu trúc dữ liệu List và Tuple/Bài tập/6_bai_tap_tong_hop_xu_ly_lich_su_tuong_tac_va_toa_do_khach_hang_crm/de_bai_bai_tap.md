## <center>[Bài tập tổng hợp] Xử lý Lịch sử Tương tác và Tọa độ Khách hàng CRM</center>

### **1. Mục tiêu**
* Áp dụng cấu trúc dữ liệu `List` và `Tuple` trong Python 3.12 để xử lý thông tin và lịch sử tương tác khách hàng trong hệ thống CRM.
* Thực hiện kỹ thuật giải nén Tuple (Tuple Unpacking) và hoán đổi giá trị biến (Variable Swap) trực tiếp không sử dụng biến trung gian.
* Cập nhật phần tử trong `List` thông qua chỉ số (Index) và trích xuất danh sách con bằng kỹ thuật cắt lát (Slicing).
* Tuân thủ quy chuẩn mã nguồn Python PEP 8 và định kiểu Type Hints theo tiêu chuẩn phát triển ứng dụng doanh nghiệp.

### **2. Vấn đề**
Trong phân hệ quản lý khách hàng (CRM) của một doanh nghiệp bán lẻ, dữ liệu khách hàng trích xuất từ bộ nhớ tạm (RAM) bao gồm hai thành phần chính: thông tin cố định hệ thống (mã khách hàng, số điện thoại, tọa độ địa lý) được lưu dưới dạng `Tuple`, và danh sách mã số các phiên hỗ trợ tương tác gần nhất được lưu dưới dạng `List`.

Do sự cố ghi nhận dữ liệu từ thiết bị đầu cuối:
1. Tọa độ địa lý trong Tuple thông tin khách hàng bị đảo ngược vị trí giữa kinh độ (Longitude) và vĩ độ (Latitude).
2. Mã phiên tương tác đầu tiên trong List lịch sử bị ghi nhầm mã hệ thống cũ và cần được cập nhật mã mới.
3. Chuyên viên CRM cần trích xuất một phân đoạn gồm 3 mã phiên tương tác ở giữa danh sách để lập báo cáo nhanh mà không làm thay đổi danh sách gốc.



### **3. Quy tắc nghiệp vụ**
* **Dữ liệu đầu vào:**
  - Metadata thông tin khách hàng gốc (Tuple): `customer_info = ("CUST-8892", "0908123456", 106.66017, 10.76262)` (Trong đó vị trí index 2 là kinh độ `106.66017`, index 3 là vĩ độ `10.76262`).
  - Danh sách mã phiên tương tác (List): `session_history = [1000, 7002, 7003, 7004, 7005]`
  - Mã phiên mới cần sửa cho index 0: `9999`

* **Quy trình xử lý nghiệp vụ:**
  1. Giải nén Tuple `customer_info` thành 4 biến riêng biệt: `customer_id`, `phone_number`, `latitude`, `longitude`.
  2. Áp dụng kỹ thuật Swap trực tiếp trong Python (`a, b = b, a`) để hoán đổi lại giá trị hai biến `latitude` và `longitude` sao cho `latitude` mang giá trị `10.76262` và `longitude` mang giá trị `106.66017`.
  3. Tái đóng gói dữ liệu đã chuẩn hóa thành một Tuple mới có tên `updated_customer_info`.
  4. Cập nhật mã phiên đầu tiên (index 0) của `session_history` thành mã phiên mới `9999` bằng phép gán qua index.
  5. Sử dụng kỹ thuật Slicing `[1:4]` trên `session_history` để lấy ra phân đoạn 3 phiên tương tác trung gian (tại index 1, 2, 3) và gán vào biến `recent_sessions`.
  6. In toàn bộ kết quả sau xử lý ra màn hình theo đúng định dạng đầu ra.

### **4. Yêu cầu bài toán**
* Tạo file mã nguồn `main.py` và triển khai chương trình bằng Python 3.12.
* Mã nguồn phải tuân thủ chuẩn PEP 8 (sử dụng 4 khoảng trắng để thụt lề, tên biến theo chuẩn `snake_case`).
* Kết quả hiển thị trên màn hình CLI phải tuân thủ chính xác cấu trúc mẫu sau:

```text
=== HỆ THỐNG QUẢN LÝ KHÁCH HÀNG CRM ===
Mã khách hàng: CUST-8892
Số điện thoại: 0908123456
Tọa độ gốc (Lat, Lng): (10.76262, 106.66017)
Lịch sử phiên gốc: [1000, 7002, 7003, 7004, 7005]
Lịch sử phiên sau cập nhật Index 0: [9999, 7002, 7003, 7004, 7005]
Phân đoạn phiên tương tác gần đây (Slicing [1:4]): [7002, 7003, 7004]
Tuple thông tin khách hàng đã chuẩn hóa: ('CUST-8892', '0908123456', 10.76262, 106.66017)
```

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
* Phần phân tích/báo cáo và mã nguồn triển khai.
* Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex06`.
  Ví dụ: `HNKS25CNTT1_Core_Session08_Ex06`
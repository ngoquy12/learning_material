#

# <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp (AIRLINE_CHECKIN)</center>

### **1. Mục tiêu**
- **Kiến thức**: Tích hợp toàn diện câu lệnh điều kiện `if / else-if / else`, cấu trúc rẽ nhánh đa trường hợp `switch-case`, và biểu thức điều kiện ba ngôi (ternary operator) trong việc giải quyết bài toán nghiệp vụ quy trình check-in hàng không.
- **Kỹ năng**: Rèn luyện kỹ năng phân tích luồng điều kiện, kiểm soát thứ tự logic, tránh các lỗi phổ biến như quên lệnh `break` gây trôi lệnh (fall-through) hay lồng ghép biểu thức phức tạp, viết mã nguồn sạch (Clean Code) theo quy chuẩn ES6+.
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
Hệ thống làm thủ tục tự động của hãng hàng không **AIRLINE_CHECKIN** cần xử lý thông tin hành khách ngay tại quầy check-in tự động trước khi ra cửa khởi hành. Hệ thống cần thực hiện chuỗi 3 thao tác tính toán và rẽ nhánh điều kiện logic:
1. Xác định mức phí phạt hành lý ký gửi quá cước dựa trên trọng lượng.
2. Tra cứu quyền lợi phòng chờ và thứ tự nhóm lên máy bay (Boarding Group) dựa trên Mã hạng vé.
3. Phân loại nhanh làn kiểm tra an ninh (Làn ưu tiên Fast-Track hay Làn thông thường) dựa trên tiêu chí đối tượng ưu tiên.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**

#### **Chức năng 1: Tính phí hành lý ký gửi quá cước (Áp dụng cấu trúc `if / else-if / else`)**
- **Nghiệp vụ**: Phân loại trọng lượng hành lý ký gửi (`baggageWeight` tính bằng kg) để xác định phí xử lý:
  - Dưới hoặc bằng 20kg: Miễn phí hành lý ký gửi (0 VNĐ).
  - Từ trên 20kg đến 30kg: Phụ thu 200.000 VNĐ.
  - Từ trên 30kg đến 40kg: Phụ thu 500.000 VNĐ.
  - Trên 40kg: Phí phạt hành lý quá trọng lượng là 1.000.000 VNĐ và in thông báo yêu cầu làm thủ tục tại quầy hàng hóa đặc biệt.
- **Đầu vào (Input)**: Biến số thực `baggageWeight` đại diện cho trọng lượng cân được (ví dụ: `25.5`).
- **Đầu ra (Output)**: In thông báo rõ ràng mức phí phụ thu hành lý phải trả và hướng dẫn đi kèm trên Console.

#### **Chức năng 2: Phân loại phòng chờ và nhóm ưu tiên lên máy bay (Áp dụng cấu trúc `switch-case`)**
- **Nghiệp vụ**: Tra cứu thông tin dịch vụ dựa trên mã hạng vé (`ticketClassCode` dạng số nguyên) theo bảng quy định:
  - Mã `1`: Hạng Nhất (First Class) -> Sử dụng "Phòng chờ VIP Lotus lên máy bay "Nhóm 1 (Ưu tiên đặc biệt)".
  - Mã `2`: Hạng Thương gia (Business Class) -> Sử dụng "Phòng chờ Thương gia lên máy bay "Nhóm 2 (Ưu tiên)".
  - Mã `3`: Hạng Phổ thông Đặc biệt (Premium Economy) -> Sử dụng "Khu vực chờ tiêu chuẩn lên máy bay "Nhóm 3".
  - Mã `4`: Hạng Phổ thông (Economy) -> Sử dụng "Khu vực chờ tiêu chuẩn lên máy bay "Nhóm 4".
  - Các mã khác: Thông báo "Mã hạng vé không hợp lệ trong hệ thống". (Bắt buộc dùng `break` và nhánh `default`).
- **Đầu vào (Input)**: Biến số nguyên `ticketClassCode` (ví dụ: `2`).
- **Đầu ra (Output)**: In tên phòng chờ dịch vụ và thứ tự nhóm lên máy bay tương ứng.

#### **Chức năng 3: Phân loại làn kiểm tra an ninh Fast-Track (Áp dụng Toán tử Ba ngôi Ternary Operator)**
- **Nghiệp vụ**: Sử dụng toán tử ba ngôi để gán trực tiếp thông điệp phân làn kiểm tra an ninh:
  - Nếu hành khách sở hữu thẻ VIP (`isVipMember = true`) HOẶC có số tuổi `passengerAge >= 60` (người cao tuổi), gán nhãn thông báo: `"Đi vào Làn ưu tiên Fast-Track (Cửa A1)"`.
  - Ngược lại, gán nhãn thông báo: `"Đi vào Làn kiểm tra an ninh thông thường (Cửa B1-B4)"`.
- **Đầu vào (Input)**: Biến boolean `isVipMember` và biến số nguyên `passengerAge`.
- **Đầu ra (Output)**: In trực tiếp nhãn hướng dẫn luồng di chuyển an ninh sau khi gán bằng toán tử ba ngôi.

### **4. Yêu cầu nộp bài**
Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_Session06_Demo`.
Ví dụ: `HNKS25CNTT1_Core_Session06_Demo`
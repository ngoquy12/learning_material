## <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp (HOTEL_BOOKING)</center>

### **1. Mục tiêu**
- **Kiến thức**: Tích hợp toàn bộ kiến thức về các phép toán số học (cộng, trừ, nhân, chia, chia lấy nguyên, chia lấy dư, lũy thừa) và các phép toán so sánh trong Python để tính toán chỉ số tài chính, xác thực điều kiện đặt phòng và quy đổi ưu đãi dịch vụ.
- **Kỹ năng**: Rèn luyện kỹ năng thực thi mã nguồn từng bước (trace execution), khai báo biến chuẩn quy cách PEP 8 có Type Hints, xử lý chính xác biểu thức toán học và biểu thức logic để kiểm tra trạng thái nghiệp vụ mà không cần dùng câu lệnh rẽ nhánh.
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
Hệ thống quản lý khách sạn thông minh `HOTEL_BOOKING` cần xây dựng phân hệ xử lý nghiệp vụ đặt phòng tự động cho khách hàng. Phân hệ này chịu trách nhiệm tính toán tổng chi phí lưu trú kèm phụ phí dịch vụ, kiểm tra tính hợp lệ về độ tuổi và khả năng tài chính của khách hàng, đồng thời tự động quy đổi đêm nghỉ miễn phí dựa trên chính sách tích điểm thành viên.

Giảng viên sẽ thực hiện minh họa trực tiếp (Live-Demo) việc xây dựng luồng xử lý này từ việc nhận dữ liệu thô, thực hiện biểu thức tính toán số học, so sánh giá trị và in ra kết quả trạng thái phê duyệt của hệ thống.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**

- **Chức năng 1: Tính toán chi phí lưu trú và tổng hóa đơn**
  - **Nghiệp vụ**: Tính toán tổng tiền phòng cơ bản dựa trên đơn giá một đêm và số đêm ở; sau đó cộng thêm chi phí dịch vụ cố định và trừ đi số tiền giảm giá từ mã khuyến mãi để ra tổng hóa đơn thanh toán cuối cùng.
  - **Đầu vào (Input)**: Đơn giá phòng một đêm (kiểu số thực hoặc số nguyên), Số đêm lưu trú (kiểu số nguyên), Chi phí dịch vụ phụ trợ (kiểu số thực hoặc số nguyên), Số tiền giảm giá khuyến mãi (kiểu số thực hoặc số nguyên).
  - **Đầu ra (Output)**: In ra màn hình giá trị tổng chi phí lưu trú nguyên bản và tổng tiền hóa đơn thực tế khách hàng phải trả.

- **Chức năng 2: Kiểm tra điều kiện độ tuổi và năng lực tài chính**
  - **Nghiệp vụ**: Kiểm tra xem khách hàng có đủ từ 18 tuổi trở lên hay không, đồng thời so sánh số dư tài khoản của khách hàng với tổng tiền hóa đơn để kiểm tra xem tài khoản có đủ tiền thanh toán hay không.
  - **Đầu vào (Input)**: Tuổi của khách hàng (kiểu số nguyên), Số dư tài khoản khả dụng (kiểu số thực hoặc số nguyên), Tổng tiền hóa đơn cần thanh toán (kiểu số thực hoặc số nguyên).
  - **Đầu ra (Output)**: In ra màn hình kết quả dạng luận lý thể hiện việc khách hàng có đủ tuổi hay không và có đủ tiền trong tài khoản hay không.

- **Chức năng 3: Quy đổi đêm nghỉ thưởng và kiểm tra giờ nhận phòng**
  - **Nghiệp vụ**: Sử dụng toán tử chia lấy nguyên để xác định số đêm nghỉ miễn phí khách hàng được nhận (mỗi 5 đêm lưu trú trong lịch sử sẽ đổi được 1 đêm miễn phí), dùng toán tử chia lấy dư để tìm số đêm tích lũy dư còn lại, và so sánh giờ nhận phòng thực tế với mốc giờ tiêu chuẩn để xác định khách hàng có đến trễ hay không.
  - **Đầu vào (Input)**: Tổng số đêm khách đã ở trong lịch sử (kiểu số nguyên), Giờ nhận phòng thực tế (kiểu số nguyên từ 0 đến 23), Giờ nhận phòng tiêu chuẩn của khách sạn (kiểu số nguyên).
  - **Đầu ra (Output)**: In ra số đêm thưởng quy đổi được, số đêm tích lũy chưa đủ điều kiện đổi, và kết quả kiểm tra trạng thái nhận phòng trễ.

### **4. Yêu cầu nộp bài**
Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_Session04_Demo`.
Ví dụ: `HNKS25CNTT1_Core_Session04_Demo`
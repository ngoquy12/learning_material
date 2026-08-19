# <center>[Tổng hợp Demo] Phân hệ Tổng hợp Kiểm soát và Xử lý Lô Sách Thư viện (LIBRARY_WMS)</center>

### **1. Mục tiêu**

- **Kiến thức:** Minh họa trực quan cách kết hợp vòng lặp và câu lệnh rẽ nhánh trong một bài toán nghiệp vụ tích hợp.
- **Kỹ năng:** Trình diễn cách kiểm soát luồng chương trình khi xử lý dữ liệu hàng loạt trên bộ nhớ RAM, xử lý các sự cố bỏ qua phần tử lỗi hoặc dừng khẩn cấp khi gặp rủi ro an ninh.
- **Vai trò:** Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**

Trong Hệ thống Quản lý Mượn trả Sách Thư viện (LIBRARY_WMS), giảng viên sẽ hướng dẫn học viên xây dựng phân hệ kiểm soát hàng loạt bản ghi sách mượn quá hạn. Phân hệ này chạy tự động trên RAM nhằm quét qua dải mã sách liên tiếp, tính tiền phạt quá hạn và kiểm tra chất lượng nhãn vạch cũng như mức độ an ninh của sách.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**

Chương trình Demo trên lớp yêu cầu thực hiện đầy đủ 3 chức năng sau:

#### **Chức năng 1: Thiết lập phạm vi quét kiểm kê**

- **Nghiệp vụ**: Cán bộ vận hành thiết lập một khoảng quét sách dựa trên mã số bản ghi bắt đầu và mã số kết thúc. Hệ thống sẽ lần lượt kiểm tra tất cả các mã sách nằm trong khoảng này.
- **Đầu vào (Input)**:
  - Mã bắt đầu (Số nguyên dương, ví dụ: `101`)
  - Mã kết thúc (Số nguyên dương, ví dụ: `110`)
- **Đầu ra (Output)**: In thông điệp thông báo bắt đầu quét toàn bộ lô sách.

#### **Chức năng 2: Kiểm soát chất lượng sách & Cảnh báo an ninh**

- **Nghiệp vụ**: Trong quá trình kiểm tra từng mã sách:
  - **Nhận diện sách lỗi tem nhãn**: Các sách có mã số chia hết cho 5 được quy ước là lỗi nhãn vạch nhẹ. Hệ thống cần bỏ qua sách này, không tính tiền phạt hay ghi nhận xử lý thành công, và chuyển ngay sang mã sách tiếp theo.
  - **Phát hiện vi phạm an ninh nghiêm trọng**: Các sách có mã số chia hết cho 13 được quy ước là sách cấm lưu hành hoặc có dấu hiệu gian lận. Hệ thống cần đưa ra cảnh báo khẩn cấp và dừng ngay lập tức toàn bộ tiến trình kiểm tra (không tiếp tục kiểm tra các quyển sách còn lại).
  - **Xử lý bản ghi hợp lệ**: Với các sách bình thường, thủ thư nhập số ngày quá hạn từ bàn phím. Nếu sách quá hạn (ngày quá hạn lớn hơn 0), phí phạt quá hạn được tính với đơn giá cố định `5.000 VNĐ/ngày`. Hệ thống ghi nhận thêm 1 bản ghi xử lý thành công và cộng dồn phí phạt vào tổng tiền phạt của lô.
- **Đầu vào (Input)**:
  - Số ngày quá hạn (Số nguyên nhập từ bàn phím cho mỗi quyển sách hợp lệ).
- **Đầu ra (Output)**:
  - Thông báo bỏ qua đối với sách lỗi tem nhãn.
  - Thông báo dừng khẩn cấp kèm cảnh báo an ninh đối với sách vi phạm.
  - Thông báo ghi nhận xử lý thành công mã sách kèm số tiền phạt phát sinh.

#### **Chức năng 3: Báo cáo kết quả kiểm kê tự động**

- **Nghiệp vụ**:
  - **Trường hợp hoàn thành trọn vẹn**: Nếu tiến trình quét hết toàn bộ danh sách sách thiết lập mà không gặp bất kỳ sự cố an ninh nghiêm trọng nào (không kích hoạt lệnh dừng khẩn cấp), hệ thống tự động xuất báo cáo tổng kết an toàn (Hiển thị tổng số sách đã kiểm kê thành công và tổng tiền phạt thu được).
  - **Trường hợp bị dừng khẩn cấp**: Nếu tiến trình bị dừng đột ngột do gặp sách vi phạm an ninh, hệ thống không được phép in báo cáo tổng kết an toàn mà chỉ in thông điệp hệ thống bị niêm phong và trạng thái dừng.
- **Đầu ra (Output)**:
  - Báo cáo tổng kết lô sách an toàn (nếu hoàn thành trọn vẹn).
  - Thông điệp niêm phong hệ thống (nếu bị dừng khẩn cấp).

### **4. Yêu cầu nộp bài**

Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_Session08_Demo`.
Ví dụ: `HNKS25CNTT1_Core_Session08_Demo`

## <center>[Vận dụng nâng cao 3] Rà soát và Tổng hợp Đợt mượn trả Sách Thư viện LIBRARY_WMS</center>

### **1. Mục tiêu**
*   **Vận dụng nâng cao kiến thức lặp:** Sử dụng thành thạo cấu trúc vòng lặp `for` kết hợp với hàm `range()` để duyệt và kiểm soát dải mã bản ghi lượt mượn sách (`borrow_id`) trong hệ thống quản lý thư viện LIBRARY_WMS.
*   **Kỹ năng điều khiển luồng nâng cao:** Phối hợp chính xác câu lệnh `break` để ngắt khẩn cấp tiến trình khi gặp sự cố vi phạm nghiêm trọng và câu lệnh `continue` để bỏ qua các lượt mượn gặp lỗi dữ liệu nhẹ.
*   **Khai thác khối lệnh `else` của vòng lặp:** Ứng dụng khối `else` liên kết trực tiếp với vòng lặp `for` để xác nhận đợt rà soát hoàn tất thành công và an toàn khi không có sự cố ngắt giữa chừng.
*   **Báo cáo thiết kế giải pháp:** Rèn luyện năng lực độc lập phân tích I/O, thiết kế luồng xử lý bằng sơ đồ Mermaid đạt quy chuẩn trước khi cài đặt mã nguồn Python.

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS), cuối mỗi ca làm việc, hệ thống cần tự động chạy tiến trình rà soát một dải mã giao dịch mượn sách liên tiếp từ `start_id` tới `end_id`. 

Trong quá trình tiến hành quét từng giao dịch, hệ thống phải phân tích các dấu hiệu bất thường để xử lý kịp thời. Một số mã giao dịch có thể bị thiếu thông tin vị trí lưu kho của tài liệu (lỗi nhẹ), hệ thống cần bỏ qua để kiểm tra mã tiếp theo. Tuy nhiên, nếu phát hiện mã giao dịch thuộc danh mục vi phạm quy chế nghiêm trọng (như thẻ sinh viên bị khóa do gian lận hoặc sách bị báo mất), hệ thống phải ngắt toàn bộ tiến trình rà soát ngay lập tức để tránh phát sinh lỗi dây chuyền. Ngược lại, nếu dải mã được rà soát từ đầu đến cuối mà không xảy ra bất kỳ lệnh ngắt khẩn cấp nào, hệ thống phải phát thông báo xác nhận tiến trình an toàn thông qua khối `else`.

### **3. Quy tắc nghiệp vụ**
Tiến trình rà soát dữ liệu mượn trả được thực hiện trong dải mã từ `start_id` đến `end_id` (bao gồm cả `end_id`) dựa trên các quy định sau:

1. **Khởi tạo tham số kiểm tra:**
   - Nhập vào hai số nguyên dương `start_id` và `end_id` biểu diễn dải mã giao dịch cần rà soát (yêu cầu `start_id` phải nhỏ hơn hoặc bằng `end_id`).

2. **Phân loại và xử lý từng giao dịch trong vòng lặp:**
   - **Trường hợp 1 (Sự cố nghiêm trọng - Dừng khẩn cấp):** Nếu `borrow_id` chia hết cho cả 3 và 7 (tức chia hết cho 21) -> Phát hiện giao dịch nghi ngờ gian lận thẻ mượn. Hệ thống in thông báo cảnh báo dừng khẩn cấp và gọi `break` để thoát khỏi vòng lặp ngay lập tức.
   - **Trường hợp 2 (Lỗi dữ liệu nhẹ - Bỏ qua):** Nếu `borrow_id` chia hết cho 5 (và không thuộc Trường hợp 1) -> Bản ghi bị thiếu thông tin vị trí lưu trữ sách. Hệ thống in thông báo bỏ qua mã này, cập nhật số lượng mã bị bỏ qua và gọi `continue` để chuyển sang mã tiếp theo.
   - **Trường hợp 3 (Mã hợp lệ - Xử lý thành công):** Mã giao dịch bình thường. Hệ thống thực hiện:
     - Tăng biến đếm số giao dịch hợp lệ.
     - Tính tích lũy phí phạt quá hạn (`OverdueFine`): Nếu `borrow_id` là số lẻ, tính phí phạt quá hạn phát sinh là 5.000 VNĐ; nếu `borrow_id` là số chẵn, phí phạt phát sinh là 0 VNĐ.

3. **Xác nhận hoàn thành với khối `else` của vòng lặp `for`:**
   - Nếu tiến trình rà soát duyệt hết toàn bộ các mã trong dải `[start_id, end_id]` mà **không bị ngắt** bởi câu lệnh `break`, khối `else` tương ứng của `for` sẽ thực thi và in ra thông báo: `"XÁC NHẬN: TOÀN BỘ ĐỢT RÀ SOÁT ĐÃ HOÀN THÀNH AN TOÀN!"`.

4. **Tổng hợp kết quả:**
   - Sau khi kết thúc tiến trình (dù dừng do `break` hay hoàn tất an toàn), hệ thống hiển thị báo cáo gồm: Tổng số giao dịch xử lý thành công, tổng số giao dịch bị bỏ qua, và tổng tiền phạt quá hạn tích lũy được trong đợt quét.

### **4. Yêu cầu bài toán**

Bài tập bao gồm 2 phần bắt buộc:

#### **Phần 1: Báo cáo Phân tích I/O & Thiết kế Giải pháp**
1. **Phân tích I/O:**
   - Trình bày rõ ràng danh sách tham số đầu vào (Input) và đầu ra (Output) kèm theo kiểu dữ liệu tương ứng trong Python.
2. **Đề xuất Giải pháp & Thiết kế Luồng xử lý:**
   - Đề xuất phương án lập trình sử dụng cấu trúc lặp `for`, `range()`, các câu lệnh điều khiển `break`, `continue` và khối lệnh `else`.
   - Xây dựng sơ đồ luồng (Mermaid Flowchart) biểu diễn tiến trình xử lý rà soát. Sơ đồ Mermaid phải tuân thủ đúng các dạng hình chuẩn:
     - Hình oval `([Bắt đầu/Kết thúc])`
     - Hình bình hành `[/Nhập/Xuất dữ liệu/]`
     - Hình thoi `Kiểm tra điều kiện?`
     - Hình chữ nhật `["Thực hiện hành động / Tính toán"]`
     - Tuyệt đối không dùng hình bình hành cho các bước tính toán hoặc gán giá trị biến.

#### **Phần 2: Triển khai Mã nguồn Python (Implementation)**
1. Viết chương trình Python thực thi chính xác các quy tắc nghiệp vụ đã phân tích.
2. Ràng buộc kỹ thuật nghiêm ngặt:
   - **TUYỆT ĐỐI CẤM SỬ DỤNG:** Vòng lặp `while`, kiểu dữ liệu danh sách `list`, từ điển `dict`, `tuple`, `set`, định nghĩa hàm `def`, hoặc lớp `class`.
   - Đặt tên biến hoàn toàn bằng tiếng Anh theo đúng quy chuẩn `snake_case` (ví dụ: `start_id`, `end_id`, `valid_count`, `skipped_count`, `total_fine`).
   - Chú thích giải thích logic code 100% bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex9`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 08_Ex9`
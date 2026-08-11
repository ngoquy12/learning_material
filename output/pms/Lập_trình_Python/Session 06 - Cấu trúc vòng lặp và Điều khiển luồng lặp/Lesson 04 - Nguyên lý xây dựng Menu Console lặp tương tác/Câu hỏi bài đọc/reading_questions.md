# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Dựa vào phần bối cảnh doanh nghiệp và điểm đau vận hành được mô tả trong bài đọc, khi nhân viên sử dụng ứng dụng dòng lệnh truyền thống thực hiện lệnh 'python main.py' để in số dư tài khoản, họ gặp phải 3 bất cập lớn nào liên quan đến thời gian thao tác, bộ nhớ RAM và trải nghiệm người dùng? Hãy phân tích lý do kiến trúc vòng lặp 'while True' có thể giải quyết dứt điểm các bất cập này.
> **Gợi ý trả lời & Định hướng đáp án:** Thí sinh cần nêu đủ 3 điểm đau vận hành được trích dẫn chính xác trong bài đọc:
1. Lãng phí thời gian thao tác: Mất thêm từ 3 đến 5 giây cho mỗi lần gõ lại lệnh khởi tạo ('python main.py').
2. Mất ngữ cảnh dữ liệu tạm: Mọi biến và trạng thái làm việc trong bộ nhớ RAM bị giải phóng hoàn toàn ngay sau khi chương trình đóng.
3. Trải nghiệm người dùng kém: Luồng làm việc bị ngắt quãng liên tục, gia tăng nguy cơ gõ sai lệnh hệ thống Terminal.
Giải pháp kiến trúc: Mô hình Menu Console lặp tương tác dựa trên vòng lặp 'while True' duy trì ứng dụng ở trạng thái chờ lệnh liên tục, lưu giữ phiên làm việc và trạng thái dữ liệu trong RAM, tự động hiển thị lại bảng chọn menu sau mỗi lần hoàn thành tác vụ, chỉ kết thúc khi nhận tín hiệu điều khiển chủ động từ người dùng.

---

### Câu 2: Theo sơ đồ luồng điều khiển Mermaid và bảng thông số kỹ thuật trong bài đọc, hãy mô tả chi tiết từng bước xử lý của hệ thống trong hai kịch bản người dùng sau:
- Kịch bản A: Người dùng nhập vào một giá trị lựa chọn không hợp lệ (không có trong danh sách menu).
- Kịch bản B: Người dùng nhập vào lựa chọn phím '0'.
Trong từng kịch bản, câu lệnh nào ('continue' hay 'break') được kích hoạt và câu lệnh đó tác động như thế nào đến luồng chạy của vòng lặp 'while True'?
> **Gợi ý trả lời & Định hướng đáp án:** Thí sinh cần phân tích chuẩn xác luồng chạy theo đúng bài đọc:
- Kịch bản A (Giá trị không hợp lệ):
  + Hệ thống kiểm tra giá trị lựa chọn, đưa ra cảnh báo lỗi và kích hoạt câu lệnh 'continue'.
  + Tác động của 'continue': Bỏ qua phần mã bên dưới và tái hiển thị ngay bảng chọn menu bằng cách quay lại đầu vòng lặp 'while True'.
- Kịch bản B (Nhập phím '0'):
  + Hệ thống xác định đây là tín hiệu thoát an toàn (Exit Strategy), in lời chào/thực hiện dọn dẹp tài nguyên và kích hoạt câu lệnh 'break'.
  + Tác động của 'break': Ngắt hoàn toàn vòng lặp vô hạn 'while True', giải phóng tài nguyên và kết thúc chương trình một cách an toàn.

---

### Câu 3: Bài đọc liệt kê 3 trụ cột cơ bản để xây dựng ứng dụng dòng lệnh tương tác enterprise bao gồm: Vòng lặp vô hạn điều kiện, Cấu trúc rẽ nhánh đa luồng và Cơ chế ngắt luồng an toàn. Hãy chỉ ra vai trò kỹ thuật cụ thể của khối 'if-elif-else' trong mô hình này, và giải thích tại sao ứng dụng lặp tương tác bắt buộc phải thiết kế một cơ chế thoát an toàn (Exit Strategy) chủ động thay vì kết thúc đột ngột.
> **Gợi ý trả lời & Định hướng đáp án:** Thí sinh cần trình bày đủ 2 ý kỹ thuật từ bài đọc:
1. Vai trò của khối rẽ nhánh 'if-elif-else': Đóng vai trò là bộ định tuyến (router), có nhiệm vụ phân tích giá trị chuỗi nhập vào từ bàn phím (input) để điều hướng và gọi đúng khối lệnh chức năng tương ứng.
2. Sự cần thiết của cơ chế thoát an toàn (Exit Strategy): Vì vòng lặp 'while True' duy trì ứng dụng ở trạng thái lắng nghe liên tục, nếu không có cơ chế thoát chủ động (như nhập phím '0'), người dùng sẽ không thể thoát chương trình một cách chuẩn chỉnh. Cơ chế thoát an toàn cho phép chương trình chủ động thực hiện các tác vụ dọn dẹp tài nguyên trước khi gọi lệnh 'break' để giải phóng bộ nhớ và kết thúc phiên làm việc an toàn.

---
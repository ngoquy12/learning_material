# <center>[Sáng tạo 1] Thiết kế phân hệ tính phụ phí và xác thực điều kiện đặt phòng khách sạn</center>

### **1. Mục tiêu**

- **Tư duy thiết kế hệ thống:** Tự chủ đề xuất cấu trúc dữ liệu, luồng xử lý và phát hiện các kịch bản lỗi phát sinh trong phân hệ tài chính đặt phòng khách sạn (HOTEL_BOOKING).
- **Vận dụng kỹ thuật nâng cao:** Sử dụng thành thạo các toán tử số học và toán tử so sánh trong Python 3.12 để biểu diễn công thức tính phụ phí check-in sớm, phụ thu người phát sinh và kiểm tra điều kiện hoàn tiền cọc.
- **Chuẩn hóa mã nguồn:** Viết mã nguồn Python sạch, tuân thủ nghiêm ngặt quy chuẩn PEP 8, có type hints rõ ràng và không sử dụng các cấu trúc rẽ nhánh hay vòng lặp chưa được học.

### **2. Bối cảnh & Vấn đề**

Trong các nền tảng đặt phòng trực tuyến như Agoda hoặc Traveloka, phân hệ tính toán chi phí lưu trú (Booking Financial Service) đóng vai trò nòng cốt. Khi khách hàng tiến hành đặt phòng (`BookingReservation`), hệ thống phải xử lý nhiều biến số tài chính bao gồm: đơn giá phòng gốc, giờ check-in thực tế, số lượng trẻ em đi kèm, và thời gian hủy phòng so với ngày nhận phòng.

Hiện tại, bộ phận nghiệp vụ yêu cầu phát triển một module tự động tính toán tổng hóa đơn thanh toán và xác minh tính hợp lệ của đơn đặt phòng dựa trên các chỉ số định lượng. Với vai trò là Kỹ sư phần mềm backend, bạn cần tự thiết kế mô hình xử lý, dự báo rủi ro dữ liệu xấu và cài đặt chương trình bằng mã nguồn Python 3.12.

### **3. Quy tắc nghiệp vụ**

1.  **Phụ thu nhận phòng sớm (Early Check-in Surcharge):** Nếu khách hàng nhận phòng trước 12:00 trưa (giờ check-in chuẩn), hệ thống tính phụ phí bằng 30% giá phòng gốc một đêm.
2.  **Miễn phí lưu trú cho trẻ em:** Trẻ em dưới 6 tuổi (tuổi < 6) được miễn phí hoàn toàn chi phí ở ghép.
3.  **Điều kiện hoàn tiền cọc (Deposit Refund Eligibility):** Khách hàng hủy phòng trước thời điểm nhận phòng tối thiểu 3 ngày (số ngày hủy >= 3) sẽ đạt điều kiện hoàn lại 100% tiền đặt cọc.
4.  **Ràng buộc phạm vi kiến thức:** Chỉ áp dụng toán tử số học và toán tử so sánh để tính toán giá trị biểu thức. Tuyệt đối không sử dụng câu lệnh rẽ nhánh (`if`/`else`), vòng lặp (`for`/`while`), toán tử logic (`and`/`or`/`not`) hoặc cấu trúc dữ liệu phức tạp (`list`/`dict`).

### **4. Yêu cầu bài toán**

[REQUIREMENT] Học viên chủ động thực hiện bài tập theo 4 phần chi tiết dưới đây:

- **Phần 1 - Tự thiết kế Schema I/O (Input/Output Schema):**
  - Tự khai báo danh sách các biến đầu vào (Request Parameters) bao gồm tên biến, kiểu dữ liệu (`int`, `float`, `bool`, `str`) và đơn vị đo lường liên quan đến nghiệp vụ đặt phòng.
  - Tự xác định danh sách các kết quả đầu ra (Response Metrics) mô tả đầy đủ tổng tiền, phụ phí và trạng thái cờ so sánh (`bool`).

- **Phần 2 - Tự phát hiện kịch bản lỗi & Trường hợp biên (Edge Cases):**
  - Liệt kê tối thiểu 3 trường hợp dữ liệu biên hoặc dữ liệu bất thường có thể xảy ra trong thực tế (ví dụ: giờ check-in là số âm, số ngày hủy phòng không hợp lệ, đơn giá phòng bằng 0).
  - Đề xuất phương án xử lý hoặc biểu diễn bằng biểu thức toán học/so sánh để phát hiện các bẫy dữ liệu này.

- **Phần 3 - Thiết kế Sơ đồ luồng dữ liệu (Data Flow Diagram):**
  - Vẽ sơ đồ Mermaid biểu diễn luồng dữ liệu từ lúc tiếp nhận thông tin đơn đặt phòng, trải qua các bước tính toán toán học và kiểm tra điều kiện so sánh, cho đến khi trả về kết quả cuối cùng.
  - Yêu cầu tuân thủ đúng 5 hình dạng chuẩn: Oval `([Bắt đầu/Kết thúc])`, Hình bình hành `[/Đầu vào/Đầu ra/]`, Hình chữ nhật `["Tính toán/Xử lý"]`, Hình thoi `Kiểm tra condition?`.

- **Phần 4 - Hiện thực hóa mã nguồn (Implementation):**
  - Xây dựng file chương trình Python 3.12 hoàn chỉnh.
  - Khai báo hàm xử lý có Type Hints và Docstring mô tả rõ ràng.
  - Viết các câu lệnh tính toán phụ phí, tổng chi phí và kết quả xác thực điều kiện bằng toán tử số học và toán tử so sánh.
  - In kết quả đầu ra rõ ràng ra màn hình CLI.

### **5. Yêu cầu nộp bài**

Học viên cần nộp:

- Phần phân tích/báo cáo và mã nguồn triển khai.
- Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]\_[Môn Học]\_Session04_Ex13.
  Ví dụ: HNKS25CNTT1_Core_Session04_Ex13

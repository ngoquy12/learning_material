## <center>[Sáng tạo 1] Thiết kế Tiến trình Kiểm duyệt Danh mục Sách Trả Tự động</center>

### **1. Mục tiêu**

- **Vận dụng sáng tạo** cấu trúc vòng lặp `for`, hàm `range()`, kết hợp các câu lệnh điều khiển luồng `break`, `continue` và khối `else` gắn liền với vòng lặp.
- **Tự phân tích và thiết kế** lược đồ dữ liệu đầu vào/đầu ra (I/O Schema) cho phân hệ kiểm duyệt lô tài liệu trả về trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS).
- **Chủ động phát hiện sai sót dữ liệu (Edge Cases)**, vẽ sơ đồ luồng dữ liệu (Mermaid Flowchart) và lập trình giải pháp phần mềm bằng ngôn ngữ Python tuân thủ quy chuẩn Clean Code.

### **2. Bối cảnh & Vấn đề**

Trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS), phân hệ trả sách tự động cuối ngày chịu trách nhiệm xử lý hàng loạt tài liệu được sinh viên trả về qua hộp nhận sách thông minh. Các tài liệu được gắn mã định danh dạng số nguyên (`book_id`) nằm trong một dải số liên tục.

Trong tiến trình quét kiểm kê lô sách:

1.  Một số tài liệu có nhãn mờ, bị rách barcode hoặc lỗi định dạng nhẹ: Hệ thống cần ghi nhận cảnh báo và ngay lập tức bỏ qua tài liệu này để chuyển sang xử lý cuốn tiếp theo mà không làm gián đoạn toàn bộ tiến trình.
2.  Một số tài liệu bị báo mất, thuộc danh mục cấm lưu hành hoặc có dấu hiệu gian lận thẻ mượn ở mức nghiêm trọng: Hệ thống phải lập tức kích hoạt cơ chế ngắt khẩn cấp để phong tỏa thiết bị và báo động cho thủ thư.
3.  Nếu toàn bộ lô sách trong phạm vi kiểm tra được duyệt thành công mà không gặp bất kỳ vi phạm nghiêm trọng nào ngắt giữa chừng, hệ thống sẽ xác nhận hoàn tất kiểm duyệt toàn bộ lô an toàn.

Nhà trường yêu cầu bạn thiết kế và cài đặt chương trình kiểm duyệt lô tài liệu này dựa trên dải mã số tài liệu chạy theo chu kỳ `range()`.

### **3. Quy tắc nghiệp vụ**

1.  **Duyệt danh mục tài liệu**: Hệ thống quét qua dải mã sách nguyên `book_id` từ `start_id` đến `end_id` (sử dụng hàm `range()`).
2.  **Phân loại và điều khiển luồng**:
    - **Tài liệu hợp lệ**: Tiến trình ghi nhận thông tin xử lý thành công, tính toán tổng số sách hợp lệ hoặc tổng tiền phạt chậm trả (nếu có).
    - **Tài liệu lỗi nhẹ (Skip)**: Sử dụng câu lệnh `continue` để bỏ qua các công đoạn tính toán tiếp theo của mã sách hiện tại và chuyển sang mã sách kế tiếp.
    - **Tài liệu vi phạm nghiêm trọng (Halt)**: Sử dụng câu lệnh `break` để ngắt lập toàn bộ tiến trình kiểm duyệt lô sách.
    - **Hoàn tất lô an toàn (Success)**: Sử dụng khối `else` của vòng lặp `for` để in báo cáo nghiệm thu khi vòng lặp kết thúc tự nhiên mà không bị ngắt bởi `break`.
3.  **Giới hạn kĩ thuật**:
    - [WARNING] TUYỆT ĐỐI KHÔNG sử dụng: vòng lặp `while`, danh sách (`list`), từ điển (`dict`), tập hợp (`set`), chuỗi đa chiều (`tuple`), định nghĩa hàm (`def`) hoặc lớp (`class`).
    - Chỉ sử dụng kiến thức đã học: biến đơn, câu lệnh điều kiện `if/elif/else`, vòng lặp `for`, hàm `range()`, `break`, `continue`, khối `else` của vòng lặp và câu lệnh `print()`, `input()`.

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Kĩ sư Kiến trúc Phần mềm, thực hiện bài nộp gồm 4 phần chi tiết:

#### **Phần 1: Tự thiết kế I/O Schema & Kịch bản nghiệp vụ**

- Đề xuất bảng tham số đầu vào (ví dụ: `start_id`, `end_id`, quy tắc nhận diện mã lỗi nhẹ, mã lỗi nghiêm trọng) và kết quả đầu ra mong muốn.
- Mô tả rõ công thức hoặc quy tắc logic để phân loại một mã sách là "hợp lệ", "lỗi nhẹ" hay "vi phạm nghiêm trọng".

#### **Phần 2: Phân tích sai sót dữ liệu (Edge Cases)**

- Liệt kê ít nhất 3 kịch bản sai sót dữ liệu biên (ví dụ: `start_id >= end_id`, toàn bộ lô sách đều là mã lỗi nhẹ, mã vi phạm xuất hiện ngay vị trí đầu tiên,...).
- Trình bày giải pháp xử lý cho từng kịch bản.

#### **Phần 3: Vẽ sơ đồ luồng dữ liệu (Mermaid Flowchart)**

- Vẽ sơ đồ luồng thể hiện trọn vẹn tiến trình kiểm duyệt bằng cú pháp Mermaid.
- Yêu cầu tuân thủ đúng 5 dạng hình khối tiêu chuẩn:
  1.  Terminator (Bắt đầu / Kết thúc): Hình bo góc `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
  2.  Input / Output (Đầu vào / Đầu ra): Hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
  3.  Decision (Kiểm tra điều kiện): Hình thoi `Kiểm tra điều kiện?` kèm nhánh `-->|Đúng|` / `-->|Sai|`.
  4.  Process (Thực thi / Tính toán): Hình chữ nhật `["Thực hiện hành động / Tính toán"]`.
  5.  Flowline (Đường luồng): Mũi tên `-->`.

#### **Phần 4: Triển khai mã nguồn Python**

- Viết chương trình Python hoàn chỉnh giải quyết bài toán theo đúng thiết kế đã đề ra.
- Mã nguồn phải có chú thích bằng Tiếng Việt có dấu giải thích tư duy logic.
- Đặt tên biến hoàn toàn bằng tiếng Anh theo quy chuẩn PEP 8 (ví dụ: `total_valid_books`, `skipped_count`, `is_system_halted`).

### **5. Yêu cầu nộp bài**

Học viên cần nộp:

- Phần phân tích/báo cáo (Phần 1, 2, 3) và mã nguồn triển khai (Phần 4) vào file báo cáo bài tập.
- Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex13`.
  Ví dụ: `HNKS25CNTT1_Core_Session_Session 08_Ex13`

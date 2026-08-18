## <center>[Vận dụng nâng cao 2] Tự động hóa kiểm soát đợt mượn sách bằng luồng vòng lặp</center>

### **1. Mục tiêu**
*   **Kiến thức & Kỹ năng:** Nắm vững và áp dụng thành thạo cấu trúc vòng lặp `for` phối hợp với hàm `range()`, các câu lệnh điều khiển luồng `break`, `continue` và khối `else` gắn kèm vòng lặp trong ngôn ngữ lập trình Python.
*   **Tư duy phân tích bài toán:** Tự phân tích bài toán nghiệp vụ kiểm soát dữ liệu mượn sách thư viện thực tế, thiết kế cấu trúc dữ liệu và xây dựng sơ đồ luồng thuật toán độc lập mà không dựa vào mã mồi (skeleton code).
*   **Năng lực triển khai:** Hoàn thiện báo cáo phân tích kĩ thuật (I/O, Mermaid Flowchart) và lập trình chương trình thực thi chính xác, xử lý triệt để các tình huống dừng dừng đột ngột hoặc bỏ qua dữ liệu rác.

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS), vào cuối mỗi ca trực, cán bộ thư viện cần tiến hành kiểm soát đột xuất một đợt bản ghi mượn sách có mã số định danh dạng số nguyên liên tiếp (ví dụ kiểm tra từ mã `start_id` đến `end_id`). 

Trong quá trình duyệt qua từng mã bản ghi mượn sách, hệ thống có thể gặp phải các tình huống đặc biệt:
1.  **Bản ghi lỗi nhẹ (Thiếu dữ liệu/Lỗi định dạng):** Cần được bỏ qua để tiếp tục kiểm tra các bản ghi tiếp theo mà không làm gián đoạn tiến trình.
2.  **Bản ghi vi phạm nghiêm trọng (Cảnh báo gian lận/Mất sách khẩn cấp):** Hệ thống phải phát tín hiệu báo động và dừng ngay lập tức toàn bộ quá trình kiểm soát đợt mượn để tiến hành phong tỏa tài khoản sinh viên.
3.  **Hoàn thành toàn bộ đợt kiểm tra:** Nếu toàn bộ dãy bản ghi được duyệt qua an toàn không gặp sự cố nghiêm trọng nào, hệ thống cần tự động xuất báo cáo tổng kết hoàn thành kiểm tra an toàn.

### **3. Quy tắc nghiệp vụ**
Hệ thống yêu cầu xử lý đợt mượn sách theo các quy định sau:

1.  **Thiết lập khoảng kiểm tra:**
    *   Người dùng nhập hai số nguyên: `start_id` (mã bản ghi bắt đầu) và `end_id` (mã bản ghi kết thúc).
    *   Hệ thống sẽ thực hiện vòng lặp duyệt qua tất cả các mã bản ghi trong phạm vi từ `start_id` đến `end_id` (bao gồm cả `end_id`).

2.  **Quy tắc điều khiển luồng trong vòng lặp:**
    *   **Bỏ qua bản ghi lỗi (`continue`):** Mã bản ghi mượn sách là số chia hết cho 5 được quy ước là bản ghi tạm thời thiếu thông tin vị trí lưu kho. Hệ thống in thông báo bỏ qua bản ghi này và dùng lệnh `continue` để lập tức chuyển sang kiểm tra mã bản ghi tiếp theo (không tính phí phạt hay cộng dồn chi phí cho bản ghi này).
    *   **Dừng khẩn cấp (`break`):** Mã bản ghi mượn sách là số chia hết cho 13 được quy ước là mã sách bị cảnh báo mất trộm hoặc vi phạm an ninh thư viện nghiêm trọng. Hệ thống ngay lập tức in thông báo cảnh báo nguy hiểm, hiển thị lý do dừng khẩn cấp và dùng lệnh `break` để thoát khỏi vòng lặp kiểm tra ngay lập tức.
    *   **Xử lý bản ghi hợp lệ:** Đối với các mã bản ghi bình thường:
        *   Nhập số ngày mượn quá hạn (`overdue_days`) của bản ghi đó từ bàn phím.
        *   Nếu `overdue_days > 0`: Tính tiền phạt với đơn giá 5.000 VNĐ/ngày. Nếu `overdue_days <= 0`: Tiền phạt bằng 0 VNĐ.
        *   Cộng dồn tiền phạt vào tổng số tiền phạt của cả đợt kiểm tra và in thông báo xử lý thành công mã bản ghi kèm tiền phạt phát sinh.

3.  **Quy tắc khối `else` của vòng lặp:**
    *   Sử dụng khối `else` kết hợp trực tiếp với vòng lặp `for`.
    *   Nếu vòng lặp kết thúc tự nhiên (tất cả các bản ghi trong khoảng đều được kiểm tra mà không bị ngắt bởi `break`), khối `else` sẽ chạy và hiển thị thông điệp xác nhận toàn bộ đợt kiểm tra đã hoàn thành thành công cùng tổng tiền phạt thu được.
    *   Nếu vòng lặp bị ngắt mid-way do gặp câu lệnh `break`, khối `else` tuyệt đối không được thực thi.

4.  **Giới hạn kỹ thuật bắt buộc (Phạm vi kiến thức):**
    *   **ĐƯỢC PHÉP DÙNG:** Cấu trúc vòng lặp `for`, hàm `range()`, các câu lệnh `break`, `continue`, khối `else` của vòng lặp, các câu lệnh rẽ nhánh `if/elif/else`, các phép toán cơ bản, hàm `print()`, `input()`.
    *   **TUYỆT ĐỐI CẤM:** Vòng lặp `while`, các cấu trúc dữ liệu danh sách/tập hợp (`list`, `dict`, `tuple`, `set`), tự định nghĩa hàm (`def`), định nghĩa lớp (`class`), import bất kỳ thư viện ngoài nào.

### **4. Yêu cầu bài toán**

Học viên thực hiện bài nộp gồm 2 phần chính:

#### **Phần 1: Báo cáo Phân tích I/O & Thiết kế Giải pháp (Nộp dạng văn bản Markdown)**
1.  **Phân tích Đầu vào / Đầu ra (Input / Output Analysis):**
    *   Liệt kê đầy đủ các biến đầu vào (tên biến, kiểu dữ liệu, ý nghĩa nghiệp vụ).
    *   Liệt kê đầy đủ các biến đầu ra và thông tin cần hiển thị.
2.  **Đề xuất Giải pháp & Sơ đồ luồng (Flowchart):**
    *   Mô tả giải pháp logic tổng quan.
    *   Vẽ sơ đồ luồng thuật toán bằng cú pháp Mermaid syntax. 
    *   *Quy chuẩn hình dạng Mermaid bắt buộc:*
        *   Start/End: Hình bo tròn `([Bắt đầu])`, `([Kết thúc])`.
        *   Input/Output: Hình bình hành `[/Nhập start_id, end_id/]` hoặc `[/In thông báo/].`
        *   Điều kiện kiểm tra: Hình thoi `Kiểm tra điều kiện?`.
        *   Thao tác tính toán/Gán biến: Hình chữ nhật `["Tính tiền phạt"]`.
3.  **Giải thích luồng điều khiển:**
    *   Nêu rõ tại sao lại đặt `continue` tại vị trí kiểm tra bản ghi lỗi nhẹ.
    *   Nêu rõ cơ chế ngắt của `break` khi gặp sự cố an ninh và vai trò kích hoạt/không kích hoạt của khối `else`.

#### **Phần 2: Triển khai Mã nguồn Python (Nộp file `.py`)**
1.  Viết chương trình Python độc lập thực thi chính xác toàn bộ quy tắc nghiệp vụ đã mô tả.
2.  Tuân thủ chuẩn PEP 8: Đặt tên biến rõ ràng bằng tiếng Anh (`snake_case`), thụt lề 4 khoảng trắng.
3.  Chú thích mã nguồn bằng tiếng Việt có dấu để giải thích ý nghĩa logic từng đoạn.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex8`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 08_Ex8`
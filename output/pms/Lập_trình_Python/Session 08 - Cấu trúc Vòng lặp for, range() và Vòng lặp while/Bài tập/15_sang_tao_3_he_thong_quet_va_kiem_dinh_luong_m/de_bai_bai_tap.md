## <center>[Sáng tạo 3] Hệ thống Quét và Kiểm định Luồng Mượn Trả Sách Thư viện</center>

### **1. Mục tiêu**
*   Vận dụng sáng tạo cấu trúc vòng lặp `for` kết hợp hàm `range()` để quét dữ liệu theo chuỗi mã danh mục.
*   Thành thạo kỹ thuật điều khiển luồng lặp bằng `continue` để bỏ qua dữ liệu ngoại lệ nhẹ và `break` để xử lý sự cố an ninh nghiêm trọng.
*   Khai thác hiệu quả khối `else` kết hợp với vòng lặp `for` nhằm xác minh tiến trình quét hoàn tất thành công.
*   Tự thiết kế cấu trúc luồng xử lý, phân tích lỗi biên nghiệp vụ và vẽ sơ đồ luồng dữ liệu (Data Flow Diagram) chuẩn hóa.

### **2. Bối cảnh & Vấn đề**
Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS) đang triển khai mô-đun tự động quét kiểm định hàng loạt giao dịch mượn trả sách trong ca làm việc. Mỗi phiếu mượn được cấp một mã số nguyên định danh tăng dần liên tục (ví dụ từ mã `start_id` đến `end_id`).

Trong ca trực, thủ thư khởi chạy tiến trình quét tự động dải phiếu mượn này để tính toán ngày mượn, phát hiện tiền phạt quá hạn (`OverdueFine`), đồng thời phát hiện các nguy cơ gian lận hoặc lỗi dữ liệu.
*   Nếu gặp phiếu mượn bị lỗi dữ liệu nhẹ (ví dụ: thông tin sách đang được bảo trì hệ thống), hệ thống cần bỏ qua phiếu mượn này để tiếp tục kiểm tra các phiếu kế tiếp.
*   Nếu phát hiện phiếu mượn có nguy cơ rủi ro bảo mật hoặc gian lận (ví dụ: tài khoản sinh viên bị khóa khẩn cấp hoặc mã sách bị cảnh báo mất trộm), hệ thống phải lập tức dừng toàn bộ tiến trình quét để niêm phong dữ liệu.
*   Nếu toàn bộ dải phiếu mượn được kiểm định thành công mà không phát hiện bất kỳ sự cố an ninh nghiêm trọng nào, hệ thống sẽ đưa ra thông báo xác nhận tiến trình hoàn tất an toàn.

### **3. Quy tắc nghiệp vụ**
1.  **Duyệt dải mã phiếu mượn**: Sử dụng vòng lặp `for` và `range(start_id, end_id + 1)` để quét danh sách các phiếu mượn.
2.  **Định mức mượn sách & Phạt quá hạn**:
    *   Thời hạn mượn sách quy định tối đa là 14 ngày.
    *   Nếu số ngày mượn thực tế lớn hơn 14 ngày, tiền phạt quá hạn được tính theo công thức: `Phí phạt = (Số ngày mượn - 14) * 5.000 VNĐ`.
3.  **Điều khiển luồng lặp**:
    *   **Bỏ qua (continue)**: Khi gặp mã phiếu mượn thuộc danh sách sự cố nhẹ (do học viên tự định nghĩa điều kiện logic, ví dụ: mã chia hết cho một giá trị đặc biệt hoặc mã thuộc dải bảo trì).
    *   **Dừng khẩn cấp (break)**: Khi gặp mã phiếu mượn có cảnh báo gian lận/rủi ro an ninh nghiêm trọng (do học viên tự định nghĩa điều kiện logic).
4.  **Xác nhận hoàn tất (khối else của loop)**:
    *   Sử dụng khối `else` của vòng lặp `for` để in thông báo tổng kết: tất cả phiếu mượn đã được quét an toàn (chỉ chạy khi vòng lặp không bị ngắt bởi `break`).
5.  **Ràng buộc công nghệ**:
    *   [REQUIREMENT] CHỈ được phép dùng các biến đơn, cấu trúc điều kiện `if/elif/else`, vòng lặp `for`, hàm `range()`, các câu lệnh `break`, `continue` và khối `else` của vòng lặp.
    *   [WARNING] TUYỆT ĐỐI CẤM sử dụng: vòng lặp `while`, danh sách/tập hợp (`list`, `dict`, `tuple`, `set`), định nghĩa hàm (`def`), hoặc lớp (`class`).

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phát triển Hệ thống, thực hiện các yêu cầu sau:

*   **Phần 1: Tự thiết kế I/O Schema & Kịch bản dữ liệu**
    *   Tự xác định dải mã phiếu mượn đầu vào (`start_id`, `end_id`) và định nghĩa logic phát hiện mã bị bỏ qua (`continue`), mã bị ngắt khẩn cấp (`break`), cũng như số ngày mượn cho từng lượt kiểm tra.
*   **Phần 2: Chủ động phát hiện và Phân tích Lỗi biên (Edge Cases)**
    *   Liệt kê ít nhất 3 kịch bản lỗi biên hoặc xung đột dữ liệu mượn sách (ví dụ: `start_id` lớn hơn `end_id`, mã ngắt xuất hiện ngay ở phần tử đầu tiên, số ngày mượn bị âm...).
*   **Phần 3: Vẽ Sơ đồ Luồng Dữ liệu (Data Flow Diagram)**
    *   Vẽ sơ đồ Mermaid minh họa luồng xử lý của hệ thống. Luồng vẽ phải tuân thủ nghiêm ngặt chuẩn 5 dạng hình:
        1. Hình bầu dục `([Bắt đầu/Kết thúc])`
        2. Hình bình hành `[/Đầu vào/Đầu ra/]`
        3. Hình thoi `Kiểm tra điều kiện?`
        4. Hình chữ nhật `["Thực hiện tính toán/hành động"]`
        5. Mũi tên luồng `-->`
*   **Phần 4: Triển khai Mã nguồn Python**
    *   Viết mã nguồn Python từ đầu hoàn chỉnh, tuân thủ 100% phạm vi kiến thức đã học, có chú thích logic chi tiết bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, sơ đồ Mermaid) và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session08_Ex15`
## <center>[Phân tích 2] Phân tích và Thiết kế Tiến trình Kiểm soát Mã Sách Mượn Tự động</center>

### **1. Mục tiêu**
*   **Kỹ năng phân tích thuật toán**: Đánh giá và so sánh các phương án thiết kế luồng điều khiển vòng lặp khi xử lý các tình huống bất ngờ (bỏ qua phần tử lỗi nhẹ, ngắt khẩn cấp khi gặp sự cố an ninh nghiêm trọng).
*   **Tối ưu hóa luồng xử lý dữ liệu**: Vận dụng hiệu quả cấu trúc vòng lặp `for`, kết hợp hàm `range()`, các câu lệnh điều hướng `break`, `continue` và khối `else` trong Python để xây dựng hệ thống chạy ổn định, an toàn.
*   **Tư duy phòng ngừa rủi ro logic**: Xử lý triệt để các trường hợp biên và đảm bảo tính nhất quán của dữ liệu thống kê trong Hệ thống Quản lý Mượn trả Sách Thư viện (LIBRARY_WMS).

### **2. Vấn đề**
Trong phân hệ trạm mượn sách tự phục vụ (Self-service Checkout Kiosk) thuộc hệ thống LIBRARY_WMS, khi sinh viên tiến hành mượn một lô sách, trạm mượn sẽ tự động quét dải mã định danh sách (Book ID) chạy liên tiếp từ `start_id` đến `end_id`.

Tuy nhiên, quá trình quét mã sách trong thực tế thường gặp phải hai dạng sự cố nghiệp vụ:
1.  **Sự cố nhẹ (Lỗi nhãn/mã mờ)**: Một số mã sách bị mờ hoặc nhòe nhãn mã vạch (ví dụ: mã sách thỏa mãn điều kiện cảnh báo nhẹ). Hệ thống cần tạm thời bỏ qua mã này, không ghi nhận vào danh sách mượn thành công, đồng thời tiếp tục kiểm tra các quyển sách tiếp theo trong dải mà không dừng chương trình.
2.  **Sự cố an ninh nghiêm trọng (Sách bị báo mất/khóa lưu hành)**: Phát hiện mã sách nằm trong danh mục vi phạm an ninh nghiêm trọng (ví dụ: mã sách trùng với mã kích hoạt còi báo động `critical_id`). Hệ thống phải ngay lập tức hủy bỏ tiến trình quét, ngắt vòng lặp khẩn cấp và kích hoạt chế độ phong tỏa thiết bị.

Nếu toàn bộ dải mã sách từ `start_id` tới `end_id` được kiểm tra an toàn mà không kích hoạt bất kỳ cảnh báo an ninh nghiêm trọng nào, hệ thống phải tự động đưa ra xác nhận hoàn thành trọn vẹn tiến trình kiểm duyệt đơn mượn.

### **3. Quy tắc nghiệp vụ**
Hệ thống nhận dữ liệu đầu vào gồm dải mã sách từ `start_id` đến `end_id` (giá trị nguyên dương) và mã cảnh báo an ninh nghiêm trọng `critical_id`. Tiến trình duyệt từng `book_id` tuân thủ các quy tắc sau:

1.  **Kiểm tra dải dữ liệu**: Dải mã sách được duyệt từ `start_id` đến `end_id` (bao gồm cả `end_id`). Nếu `start_id > end_id`, hệ thống thông báo dữ liệu dải mã không hợp lệ và kết thúc.
2.  **Phân loại sự cố và xử lý luồng**:
    *   **Phát hiện sự cố nghiêm trọng**: Nếu `book_id == critical_id`, in thông báo: `"CẢNH BÁO AN NINH: Phát hiện sách vi phạm mã {book_id} -> DỪNG TOÀN BỘ TIẾN TRÌNH!"` và lập tức dừng vòng lặp (`break`).
    *   **Phát hiện sự cố nhẹ**: Nếu `book_id` là mã lỗi nhẹ (ví dụ: `book_id` chia hết cho 7), in thông báo: `"Bỏ qua mã sách {book_id} do lỗi nhãn mờ"` và chuyển ngay sang mã tiếp theo (`continue`), không tính mã này vào số lượng mượn thành công.
    *   **Xử lý mã hợp lệ**: Nếu mã sách an toàn và hợp lệ, in thông báo `"Đã xác nhận mượn thành công sách mã: {book_id}"` và tăng biến đếm số lượng mượn thành công lên 1.
3.  **Xác thực hoàn tất tiến trình (Khối `else` của vòng lặp)**:
    *   Nếu dải mã được quét hết mà KHÔNG bị ngắt bởi `break`, khối `else` liên kết với vòng lặp `for` sẽ được kích hoạt để xuất thông báo: `"XÁC NHẬN: Toàn bộ danh mục mượn đã được kiểm duyệt an toàn!"`.
    *   In ra tổng số lượng sách mượn thành công.

### **4. Yêu cầu bài toán**

Học viên đóng vai trò là Kiến trúc sư phần mềm Backend, thực hiện đầy đủ 3 phần công việc sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Tự thiết kế và đề xuất ít nhất **02 phương án kỹ thuật** khác nhau để giải quyết luồng xử lý kiểm duyệt mã sách (Ví dụ: Phương án 1 sử dụng cấu trúc `for...else` kết hợp trực tiếp `break`/`continue`; Phương án 2 sử dụng biến cờ hiệu `flag` để theo dõi trạng thái dừng thay cho khối `else` của vòng lặp).
*   Lập bảng so sánh Trade-off chi tiết giữa 2 phương án theo 5 tiêu chí bắt buộc bên dưới:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Tiêu chí so sánh</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án 1</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">1. Độ phức tạp thời gian (Time Complexity)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">2. Tiêu tốn bộ nhớ (Memory Overhead)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">3. Khả năng bảo trì (Maintainability)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">4. Độ rõ ràng mã nguồn (Readability)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">5. Bối cảnh áp dụng phù hợp (Use Case)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Giải trình Lựa chọn và Thiết kế Lưu đồ Luồng**
*   Đưa ra lập luận kỹ thuật để chọn 01 phương án tối ưu nhất cho trạm mượn tự phục vụ LIBRARY_WMS.
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) hoặc viết Mã giả (Pseudocode) thể hiện chi tiết luồng xử lý của phương án tối ưu đã chọn.
*   *Quy chuẩn Mermaid (bắt buộc)*:
    *   Bắt đầu/Kết thúc: Hình Oval `([Bắt đầu])`, `([Kết thúc])`.
    *   Đầu vào/Đầu ra: Hình Song song `[/Nhập start_id, end_id, critical_id/]` hoặc `[/In thông báo/]` (CẤM dùng hình chữ nhật cho Input/Output).
    *   Kiểm tra điều kiện: Hình Thoi `{book_id == critical_id?}`.
    *   Thực hiện hành động/Tính toán: Hình Chữ nhật `["Tăng biến đếm mượn thành công"]`.

#### **Phần 3: Triển khai Mã nguồn & Kiểm thử Biên**
*   Viết chương trình Python hoàn chỉnh thực thi phương án tối ưu đã chọn.
*   Mã nguồn tuân thủ nghiêm ngặt chuẩn PEP 8 (tên biến dạng `snake_case`, chú thích logic bằng tiếng Việt có dấu).
*   Chỉ sử dụng các cú pháp đã học (`for`, `range()`, `if/elif/else`, `break`, `continue`, khối `else` của vòng lặp). **TUYỆT ĐỐI CẤM**: Sử dụng `while`, danh sách (`list`), từ điển (`dict`), định nghĩa hàm (`def`), lớp (`class`).
*   Xử lý đầy đủ các trường hợp biên: dải mã bị ngược (`start_id > end_id`), dải mã không có lỗi, mã an ninh nằm ngay vị trí đầu tiên `start_id`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai trong file bài làm.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 08_Ex11`
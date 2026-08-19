# <center>[Phân tích 1] Thiết kế luồng kiểm tra nhật ký mượn trả và tự động xử lý ngoại lệ trong LIBRARY_WMS</center>

### **1. Mục tiêu**
*   **Tư duy phân tích luồng**: Phân tích, so sánh và đánh giá ưu/nhược điểm giữa các giải pháp điều khiển vòng lặp trong bài toán duyệt nhật ký dữ liệu mượn trả tài liệu thư viện.
*   **Kỹ năng kỹ thuật**: Ứng dụng thành thạo cấu trúc vòng lặp `for`, hàm tạo chuỗi số `range()`, các câu lệnh điều hướng luồng `break`, `continue` và khối điều kiện kết thúc an toàn `else` trong Python.
*   **Trực quan hóa thuật toán**: Thiết kế lưu đồ Mermaid chuẩn hóa biểu diễn luồng xử lý ngoại lệ tự động mà không làm treo hệ thống hoặc ngốn tài nguyên xử lý.

---

### **2. Bối cảnh & Vấn đề**
Trong **Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS)**, phân hệ *Audit Record Checker* đảm nhận nhiệm vụ quét và đối soát tự động tập hợp các bản ghi mượn sách theo ngày. Mỗi lượt mượn trong ca làm việc được cấp một mã số định danh dạng số nguyên `borrow_id` chạy liên tục từ $1$ đến `N`.

Khi quét danh sách bản ghi, hệ thống gặp phải hai thách thức lớn về xử lý dữ liệu:
1.  **Dữ liệu chưa hoàn thiện nhẹ**: Một số lượt mượn thiếu thông tin liên hệ của sinh viên hoặc chưa cập nhật ngày hẹn trả. Tiến trình cần đưa ra cảnh báo bỏ qua bản ghi này để tiếp tục kiểm tra bản ghi kế tiếp mà không được dừng toàn bộ chương trình.
2.  **Rủi ro vi phạm an ninh nghiêm trọng**: Nếu phát hiện một mã lượt mượn gắn liền với tài khoản sinh viên đang bị khóa do nợ phạt quá hạn hoặc có dấu hiệu mượn sách trái phép, hệ thống phải ngay lập tức phát cảnh báo đỏ và kích hoạt cơ chế ngắt khẩn cấp để phong tỏa dữ liệu.

Nếu toàn bộ `N` bản ghi được quét qua an toàn mà không có sự cố vi phạm nghiêm trọng nào kích hoạt dừng khẩn cấp, hệ thống cần đưa ra thông điệp xác nhận tiến trình hoàn tất an toàn.

Hệ thống yêu cầu Kỹ sư phần mềm phân tích bài toán, đề xuất các phương án cấu trúc điều khiển luồng lặp, chọn ra giải pháp tối ưu và triển khai mã nguồn đáp ứng chính xác các quy tắc nghiệp vụ.---

### **3. Quy tắc nghiệp vụ**
Hệ thống nhận các thông số đầu vào từ giao diện điều khiển (CLI):
*   `total_records`: Tổng số bản ghi lượt mượn cần kiểm tra trong ngày (`N`).
*   `critical_flag_id`: Mã lượt mượn bị đánh dấu vi phạm an ninh nghiêm trọng cần ngắt hệ thống.
*   `overdue_days_unit`: Số ngày mượn quá hạn chuẩn áp dụng tính tiền phạt cho từng bản ghi hợp lệ.

Quy tắc xử lý trong vòng lặp duyệt `borrow_id` từ $1$ đến `total_records` (sử dụng `range(1, total_records + 1)`):
1.  **Trường hợp Bỏ qua (Lỗi nhẹ)**: Bản ghi có `borrow_id` là số chia hết cho 4 (ví dụ: 4, 8, 12...) được xác định là dữ liệu chưa hoàn thiện. Hệ thống in thông báo bỏ qua lượt mượn này và dùng `continue` chuyển ngay sang bản ghi tiếp theo.
2.  **Trường hợp Dừng khẩn cấp (Rủi ro an ninh)**: Nếu `borrow_id` trùng khớp với `critical_flag_id`, hệ thống in thông báo cảnh báo vi phạm an ninh nghiêm trọng, dừng lập tức tiến trình quét bằng lệnh `break`.
3.  **Trường hợp Bản ghi Hợp lệ**:
    *   Hệ thống tính tiền phạt mượn quá hạn phát sinh: Phí phạt = `overdue_days_unit` * 5.000 VNĐ (chỉ tính nếu `overdue_days_unit > 0`).
    *   Cộng dồn phí phạt vào biến tổng tiền phạt tích lũy `total_fine`.
    *   In thông báo xử lý thành công lượt mượn `borrow_id`.
4.  **Trường hợp Hoàn thành An toàn**: Nếu vòng lặp duyệt hết toàn bộ `total_records` mà không bị ngắt giữa chừng bởi `break`, khối `else` của vòng lặp sẽ thực thi để xuất thông báo xác nhận tiến trình hoàn thành an toàn kèm tổng tiền phạt tích lũy.

---

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Học viên độc lập nghiên cứu và đề xuất ít nhất **02 phương án kỹ thuật khác nhau** để thiết kế cấu trúc luồng điều hướng vòng lặp cho bài toán trên (Ví dụ: Phương án 1 ứng dụng cấu trúc `for...else` kết hợp trực tiếp `break` và `continue`; Phương án 2 ứng dụng biến cờ hiệu trạng thái `is_compromised` kết hợp các câu lệnh rẽ nhánh `if-else` truyền thống).
*   Xây dựng bảng so sánh Trade-off trực quan giữa 2 phương án đề xuất theo đúng mẫu bảng HTML dưới đây (tuân thủ 5 tiêu chí: *Thời gian thực thi, Dung lượng bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Mức độ phù hợp với LIBRARY_WMS*):

```html
<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Tiêu chí đánh giá</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án 1 (Mô tả ngắn)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án 2 (Mô tả ngắn)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>1. Thời gian thực thi (Time Complexity)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>2. Dung lượng bộ nhớ (Space Complexity)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>3. Khả năng bảo trì (Maintainability)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>4. Độ dễ đọc của mã (Readability)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>5. Mức độ phù hợp quy mô</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>
```

# **Phần 2: Giải trình Lựa chọn & Thiết kế Lưu đồ luồng (Mermaid Flowchart)**
*   Đưa ra lý giải khoa học thuyết phục về lý do lựa chọn phương án tối ưu nhất dựa trên kết quả phân tích bảng Trade-off.
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) cho phương án tối ưu đã chọn.
*   **Quy chuẩn bắt buộc về 5 hình dạng Mermaid**:
    1.  Thẻ bắt đầu / kết thúc: Oval `([Bắt đầu tiến trình])`, `([Kết thúc tiến trình])`.
    2.  Thẻ nhập / xuất dữ liệu: Hình bình hành `[/Nhập total_records, critical_flag_id/]` hoặc `[/In thông báo/].`
    3.  Thẻ kiểm tra điều kiện: Hình thoi `{borrow_id == critical_flag_id?}` kèm nhánh `-->|Đúng|` và `-->|Sai|`.
    4.  Thẻ thực hiện hành động / tính toán: Hình chữ nhật `["Tính phí phạt OverdueFine = ..."]` (TUYỆT ĐỐI KHÔNG dùng hình bình hành cho câu lệnh tính toán/gán biến).
    5.  Đường luồng kết nối: Mũi tên `-->`.

#### **Phần 3: Triển khai Mã nguồn Python & Chặn lỗi biên**
*   Triển khai mã nguồn Python cho phương án tối ưu đã chọn.
*   **Ràng buộc kiến thức nghiêm ngặt**: Chỉ được phép dùng các kiến thức đã học trong bài (`for`, `range()`, `break`, `continue`, khối `else`, điều kiện `if/elif/else`, các biến nguyên/thực/chuỗi). TUYỆT ĐỐI CẤM sử dụng: vòng lặp `while`, danh sách (`list`), từ điển (`dict`), mảng, tập hợp, hàm (`def`), hoặc lớp (`class`).
*   **Chặn lỗi biên (Edge-case prevention)**:
    *   Kiểm tra nếu `total_records <= 0`, lập tức báo lỗi dữ liệu nhập không hợp lệ và không chạy vòng lặp.
    *   Kiểm tra nếu `overdue_days_unit < 0`, tự động đưa về 0 để tránh tiền phạt bị âm.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex10`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 08_Ex10`

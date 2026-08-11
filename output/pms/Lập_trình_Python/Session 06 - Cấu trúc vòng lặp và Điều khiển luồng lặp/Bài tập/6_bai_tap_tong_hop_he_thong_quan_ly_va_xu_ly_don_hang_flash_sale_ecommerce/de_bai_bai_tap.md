## <center>[Bài tập tổng hợp] Hệ thống Quản lý và Xử lý Đơn hàng Flash Sale E-Commerce</center>

### **1. Mục tiêu**
*   Vận dụng kiến thức về cấu trúc vòng lặp `for`, các câu lệnh điều khiển luồng rẽ nhánh `if/elif/else`, và cấu trúc dữ liệu lưu trữ trong bộ nhớ RAM (`list`, `dict`) để xây dựng module console quản lý giao dịch Flash Sale.
*   Rèn luyện kỹ năng viết mã nguồn Python chuẩn PEP 8, tích hợp Type Hints hiện đại (`int | str`), xử lý ngoại lệ nghiệp vụ và định dạng dữ liệu đầu ra chuyên nghiệp theo tiêu chuẩn hệ thống E-Commerce.

### **2. Bối cảnh & Vấn đề**
Sàn thương mại điện tử E-Shop chuẩn bị vận hành chiến dịch Flash Sale khung giờ vàng. Để đảm bảo tính ổn định của hệ thống và tránh quá tải, bộ phận vận hành cần một ứng dụng Console CLI xử lý giao dịch theo đợt (`batch processing`). Quản trị viên hệ thống sẽ duyệt qua một số lượng lượt thao tác được thiết lập trước trong phiên làm việc để kiểm tra tồn kho, tiếp nhận đơn đặt hàng của khách, cập nhật bổ sung kho hàng và xuất báo cáo tổng kết doanh thu.



### **3. Quy tắc nghiệp vụ**
Hệ thống cần tuân thủ các quy tắc quản lý nghiệp vụ E-Commerce sau:
1. **Khởi tạo dữ liệu kho hàng (RAM):**
   Kho hàng Flash Sale được lưu dưới dạng danh sách các từ điển (`list[dict]`), chứa các thông tin:
   *   Mã sản phẩm (`product_id`: `str`) - Định danh duy nhất (ví dụ: `"PROD01"`, `"PROD02"`).
   *   Tên sản phẩm (`name`: `str`).
   *   Đơn giá (`price`: `int` hoặc `float`).
   *   Số lượng tồn kho (`stock`: `int`).

2. **Giới hạn luồng lặp phiên làm việc:**
   *   Chương trình thực hiện duyệt qua một số lượng lượt giao dịch cố định `N` (với `N` do người dùng nhập vào đầu phiên) bằng vòng lặp `for`.
   *   TUYỆT ĐỐI KHÔNG sử dụng vòng lặp `while`, câu lệnh `break`, hoặc `continue` trong toàn bộ chương trình.

3. **Nghị định xử lý chức năng:**
   *   **Chức năng 1 (Xem danh sách sản phẩm):** In bảng danh sách sản phẩm gồm Mã sản phẩm, Tên sản phẩm, Đơn giá và Số lượng tồn kho.
   *   **Chức năng 2 (Tạo đơn hàng mới):** Người dùng nhập `product_id` và số lượng mua (`quantity`).
     *   Nếu `product_id` không có trong danh sách kho -> Báo lỗi `[LỖI] Mã sản phẩm không tồn tại trên hệ thống!`.
     *   Nếu `quantity` > `stock` -> Báo lỗi `[LỖI] Số lượng tồn kho không đủ để đáp ứng đơn hàng!`.
     *   Nếu hợp lệ -> Trừ số lượng tồn kho tương ứng, cộng dồn vào doanh thu và tổng số đơn hàng thành công, hiển thị tổng tiền thanh toán.
   *   **Chức năng 3 (Bổ sung tồn kho):** Người dùng nhập `product_id` và số lượng nhập thêm (`added_stock`).
     *   Kiểm tra tính hợp lệ của mã sản phẩm và cộng dồn số lượng vào `stock`.
   *   **Chức năng 4 (Báo cáo tổng kết phiên):** Hiển thị tổng doanh thu tích lũy và số lượng đơn hàng giao dịch thành công.
   *   **Lựa chọn không hợp lệ:** Khi nhập phím ngoài chuỗi chức năng (1 - 4), hiển thị thông báo `[LỖI] Lựa chọn không hợp lệ! Vui lòng chọn từ 1 đến 4.`.

### **4. Yêu cầu đầu ra**
*   Viết chương trình Python thực thi đầy đủ các quy tắc nghiệp vụ trên.
*   Sử dụng vòng lặp `for` để quản lý số lượt tương tác trong phiên làm việc.
*   Tuân thủ nghiêm ngặt các tiêu chuẩn mã nguồn: PEP 8, Type Hints, sử dụng cú pháp `int | str` nếu có hợp nhất kiểu dữ liệu.
*   Chỉ sử dụng tính năng gốc của ngôn ngữ Python, không dùng thư viện ngoài.

Ví dụ giao diện xuất dữ liệu Terminal:
```text
==================================================
      HỆ THỐNG QUẢN LÝ FLASH SALE E-COMMERCE
==================================================
1. Xem danh sách sản phẩm Flash Sale
2. Tiếp nhận đơn hàng mới
3. Bổ sung tồn kho sản phẩm
4. Xem báo cáo doanh thu phiên làm việc
==================================================
```

Bảng mô tả cấu trúc menu và phản hồi hệ thống:
<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Mã chức năng</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Tên chức năng</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Mô tả phản hồi kết quả</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">1</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Xem danh sách sản phẩm</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Hiển thị định dạng danh sách chi tiết các mặt hàng Flash Sale trong kho RAM.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">2</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tạo đơn hàng mới</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Xác nhận bán hàng, trừ kho, tính tiền và ghi nhận doanh thu phiên.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">3</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Bổ sung tồn kho</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Cộng dồn số lượng tồn kho cho sản phẩm chỉ định.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">4</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Báo cáo tổng kết</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">In tổng doanh thu tích lũy và số lượng đơn hàng thành công trong phiên.</td>
    </tr>
  </tbody>
</table>

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex06`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex06`
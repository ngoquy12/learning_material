## <center>Hệ thống Quản lý Thiết bị Công nghệ (IT Device Management System)</center>

### **1. Mục tiêu**
Đánh giá khả năng vận dụng các kiến thức cốt lõi của ngôn ngữ Python bao gồm: cấu trúc dữ liệu (List, Dictionary), vòng lặp, câu lệnh rẽ nhánh, định nghĩa hàm cùng cơ chế xử lý lỗi/ngoại lệ cơ bản. Sinh viên cần hoàn thành các chức năng quản lý danh mục và thực thể thiết bị mà không sử dụng Class hoặc các thư viện ngoài.

### **2. Yêu cầu**

Thiết kế cấu trúc dữ liệu lưu trữ danh sách thiết bị dưới dạng một List chứa các Dictionary. Mỗi thiết bị (Dictionary) có các thuộc tính:
* `device_id` (chuỗi ký tự, mã duy nhất)
* `device_name` (chuỗi ký tự, tên thiết bị)
* `category` (chuỗi ký tự, danh mục thiết bị)
* `status` (chuỗi ký tự, trạng thái: chỉ nhận một trong ba giá trị `"Available"`, `"Assigned"`, hoặc `"Maintenance"`)

Sinh viên viết mã nguồn phát triển 2 hàm chức năng cốt lõi theo đặc tả sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse; border: 1px solid #ccc;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="padding: 10px; border: 1px solid #ccc; width: 25%;">Tên chức năng/Hàm</th>
      <th style="padding: 10px; border: 1px solid #ccc; width: 20%;">Tham số/Input</th>
      <th style="padding: 10px; border: 1px solid #ccc; width: 35%;">Logic xử lý</th>
      <th style="padding: 10px; border: 1px solid #ccc; width: 20%;">Output / Kết quả trả về</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #ccc;">
        <b>[Thêm thiết bị mới]</b><br><code>add_device()</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ccc;">
        - <code>devices</code>: list (danh sách thiết bị hiện tại)<br>
        - <code>device_id</code>: str<br>
        - <code>device_name</code>: str<br>
        - <code>category</code>: str<br>
        - <code>status</code>: str (mặc định là "Available")
      </td>
      <td style="padding: 10px; border: 1px solid #ccc;">
        1. Kiểm tra <code>device_id</code> có bị trùng lặp trong <code>devices</code> hay không. Nếu trùng, phát sinh ngoại lệ <code>ValueError</code>.<br>
        2. Kiểm tra tham số <code>status</code> đầu vào có nằm trong tập giá trị hợp lệ <code>{"Available", "Assigned", "Maintenance"}</code> hay không. Nếu không hợp lệ, phát sinh ngoại lệ <code>ValueError</code>.<br>
        3. Tạo mới dictionary thiết bị và thêm vào <code>devices</code>.
      </td>
      <td style="padding: 10px; border: 1px solid #ccc;">
        Trả về <code>devices</code> sau khi đã thêm thiết bị mới thành công.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ccc;">
        <b>[Cập nhật trạng thái]</b><br><code>update_device_status()</code>
      </td>
      <td style="padding: 10px; border: 1px solid #ccc;">
        - <code>devices</code>: list<br>
        - <code>device_id</code>: str<br>
        - <code>new_status</code>: str
      </td>
      <td style="padding: 10px; border: 1px solid #ccc;">
        1. Kiểm tra giá trị của <code>new_status</code> xem có hợp lệ hay không. Nếu không hợp lệ, phát sinh ngoại lệ <code>ValueError</code>.<br>
        2. Tìm kiếm thiết bị theo dữ liệu <code>device_id</code>.<br>
        3. Nếu tìm thấy, thực hiện cập nhật <code>status</code> của thiết bị đó thành <code>new_status</code>.<br>
        4. Nếu không tìm thấy thiết bị, phát sinh ngoại lệ <code>KeyError</code>.
      </td>
      <td style="padding: 10px; border: 1px solid #ccc;">
        Trả về <code>devices</code> sau khi đã cập nhật thành công.
      </td>
    </tr>
  </tbody>
</table>

*Yêu cầu kiểm soát lỗi bằng khối lệnh `try-except` khi thực thi gọi hàm trong chương trình chính để đảm bảo ứng dụng không bị dừng đột ngột.*

### **3. Tiêu chí đánh giá**
*   **Cơ chế Validation & Kiểm soát lỗi (3.0 điểm):** Định nghĩa và phát sinh ngoại lệ chính xác (ValueError, KeyError), bọc khối lệnh gọi chức năng đúng cách trong `try-except`.
*   **Logic Hàm add_device (3.5 điểm):** Kiểm tra trùng lặp khóa chính xác, xác thực danh mục trạng thái hợp lệ, cập nhật và trả về cấu trúc dữ liệu theo đúng mô tả.
*   **Logic Hàm update_device_status (3.5 điểm):** Duyệt cấu trúc dữ liệu tìm kiếm phần tử, cập nhật trạng thái mới và báo lỗi tường minh khi không tìm thấy mã thiết bị.

### **4. Yêu cầu nộp bài**
*   Đường dẫn tới GitHub Repository chứa dự án cá nhân (được thiết lập ở chế độ Public).
*   Đường dẫn trực tiếp đến file mã nguồn Python (`main.py` hoặc `device_manager.py`) của bài làm.
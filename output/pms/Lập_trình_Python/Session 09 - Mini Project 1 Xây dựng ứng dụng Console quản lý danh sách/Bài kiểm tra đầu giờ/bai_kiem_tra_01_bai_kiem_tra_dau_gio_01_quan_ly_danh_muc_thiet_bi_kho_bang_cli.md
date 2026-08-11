## <center>Ứng Dụng Console Quản Lý Danh Mục Thiết Bị Kho (CLI Equipment Inventory Management)</center>

### **1. Mục tiêu**
- Kiểm tra và củng cố kiến thức sử dụng các cấu trúc dữ liệu cơ bản (`list`, `tuple`), vòng lặp (`while`, `for`), câu lệnh điều kiện (`if-elif-else`) và xử lý ngoại lệ cơ bản trong Python 3.12.
- Xây dựng chương trình điều khiển dạng dòng lệnh (CLI Menu) đơn giản phục vụ quản lý danh mục và thực thể hệ thống mà không sử dụng hàm tùy chỉnh (`def`), `dict`, `set` hay Lập trình hướng đối tượng (`OOP`).

### **2. Yêu cầu**

Xây dựng ứng dụng Console cho phép người quản lý kho theo dõi và quản lý danh mục các thiết bị công nghệ. Mỗi thiết bị trong kho được đại diện bởi một `tuple` gồm 4 thông tin: `(device_id, device_name, category, quantity)`.

Danh sách các thiết bị (`device_list`) được khởi tạo sẵn dữ liệu ban đầu như sau:
```python
device_list = [
    ("DEV001", "Laptop Dell XPS 13", "Electronics", 5),
    ("DEV002", "Monitor LG 27 inch", "Display", 10),
    ("DEV003", "Keyboard Mechanical", "Accessories", 15)
]
```

Ứng dụng chạy trên vòng lặp dòng lệnh `while True` hiển thị bảng chọn (Menu) gồm 4 lựa chọn:
1. Hiển thị danh sách thiết bị
2. Thêm thiết bị mới
3. Tìm kiếm thiết bị theo danh mục
0. Thoát chương trình

Đặc tả chi tiết các khối chức năng xử lý trong ứng dụng:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Tên chức năng / Thành phần</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Quy trình xử lý & Quy tắc (Logic)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Kết quả đầu ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Hiển thị danh sách thiết bị]</b><br><code>display_device_list</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Biến danh sách <code>device_list</code>.</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">- Sử dụng vòng lặp <code>for</code> để duyệt qua từng phần tử <code>tuple</code> trong <code>device_list</code>.<br>- In ra từng cột: Mã thiết bị, Tên thiết bị, Danh mục, Số lượng.<br>- Kiểm tra nếu <code>device_list</code> trống thì in thông báo "Danh sách thiết bị đang rỗng."</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Bảng danh sách các thiết bị ra màn hình Console kèm tổng số thiết bị hiện có.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Thêm thiết bị mới]</b><br><code>add_device_entry</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Các giá trị nhập từ bàn phím:<br><code>device_id</code>, <code>device_name</code>, <code>category</code>, <code>quantity</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">- Yêu cầu nhập lần lượt 4 thông tin qua <code>input()</code>.<br>- Ép kiểu <code>quantity</code> sang số nguyên <code>int</code>. Sử dụng <code>try-except ValueError</code> để xử lý trường hợp người dùng nhập số lượng không phải số nguyên.<br>- Kiểm tra tính duy nhất: Duyệt danh sách để đảm bảo <code>device_id</code> chưa từng tồn tại (không phân biệt hoa thường). Nếu đã tồn tại, hủy thao tác và in thông báo lỗi.<br>- Nếu thông tin hợp lệ, tạo tuple <code>(device_id, device_name, category, quantity)</code> và dùng <code>append()</code> để thêm vào <code>device_list</code>.</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Thông báo "Thêm thiết bị mới thành công!" hoặc thông báo lỗi tương ứng khi trùng mã / nhập sai kiểu số lượng.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Tìm kiếm theo danh mục]</b><br><code>search_by_category</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Chuỗi nhập từ bàn phím:<br><code>search_category</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">- Nhập tên danh mục cần tìm từ bàn phím.<br>- Duyệt qua <code>device_list</code>, so sánh <code>category</code> của từng thiết bị với <code>search_category</code> (dùng <code>lower()</code> để so sánh không phân biệt chữ hoa/thường).<br>- Nếu khớp, in chi tiết thiết bị đó.<br>- Đếm số lượng thiết bị tìm thấy, nếu bằng 0 thì thông báo "Không tìm thấy thiết bị thuộc danh mục này."</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Danh sách kết quả các thiết bị thuộc danh mục cần tìm.</td>
    </tr>
  </tbody>
</table>

> **Lưu ý phạm vi kiến thức:** 
> - **KHÔNG** định nghĩa hàm custom (`def`). Toàn bộ mã nguồn viết trực tiếp trong tệp chương trình chính theo luồng tuần tự và vòng lặp `while True`.
> - **KHÔNG** sử dụng `dict`, `set`, Lớp (`class`), hoặc các thư viện ngoài.

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Điểm tối đa |
|---|---|---|
| 1 | Khởi tạo đúng cấu trúc dữ liệu mẫu (`list` chứa `tuple`) và thiết lập vòng lặp Menu chính (`while True`) | 2.0 điểm |
| 2 | Hiện thực đúng khối chức năng hiển thị danh sách (`display_device_list`) | 2.0 điểm |
| 3 | Hiện thực đúng khối chức năng thêm mới (`add_device_entry`), kiểm tra trùng lặp `device_id` và bắt lỗi `ValueError` khi nhập số lượng | 3.0 điểm |
| 4 | Hiện thực đúng khối chức năng tìm kiếm (`search_by_category`) không phân biệt chữ hoa chữ thường | 1.5 điểm |
| 5 | Đặt tên biến 100% bằng Tiếng Anh chuẩn `snake_case`, định dạng đầu ra màn hình CLI sạch sẽ, chuyên nghiệp | 1.5 điểm |
| **Tổng điểm** | | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**
- Tạo tệp mã nguồn duy nhất có tên `device_management.py`.
- Thực hiện lưu mã nguồn và đẩy lên kho lưu trữ GitHub cá nhân (Git commit & push).
- Cú pháp câu lệnh commit gợi ý:
  ```bash
  git add device_management.py
  git commit -m "feat: complete entry test session 09 device management CLI"
  git push origin main
  ```
## <center>HỆ THỐNG QUẢN LÝ THIẾT BỊ PHÒNG MÁY TÍNH CLI (IT ASSET MANAGEMENT CLI SYSTEM)</center>

### **1. Mục tiêu**
- Đánh giá khả năng áp dụng kiến thức cốt lõi Python để lập trình một ứng dụng Console (CLI) hoàn chỉnh theo luồng điều hướng Menu.
- Thành thạo thao tác với kiểu dữ liệu danh sách (`list`) kết hợp bộ dữ liệu không thay đổi (`tuple`) để lưu trữ dữ liệu thực thể.
- Áp dụng các cấu trúc điều khiển vòng lặp (`while`, `for`), câu lệnh điều kiện (`if-elif-else`) và xử lý ngoại lệ cơ bản (`try-except`) để kiểm soát dữ liệu đầu vào.
- Tuân thủ quy chuẩn đặt tên PEP 8 với 100% tên biến bằng tiếng Anh chuẩn `snake_case`.

---

### **2. Yêu cầu**

Xây dựng ứng dụng Console bằng Python 3.12 để quản lý danh mục thiết bị CNTT tại một trung tâm máy tính (bao gồm: Tên thiết bị, Số lượng, Mã phòng học). Chương trình chạy trên giao diện dòng lệnh tương tác thông qua Menu lựa chọn.

#### **Bảng mô tả chi tiết chức năng hệ thống**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 25%;">Tên chức năng / Thao tác</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 20%;">Dữ liệu đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 35%;">Luồng xử lý & Quy tắc (Processing Logic & Rules)</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 20%;">Kết quả đầu ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Chức năng 1] Nhập và Lưu trữ Thiết bị</b><br>
        <code>add_asset_flow</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - <code>asset_name</code> (str)<br>
        - <code>quantity</code> (int)<br>
        - <code>room_code</code> (str)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Nhận dữ liệu từ bàn phím bằng <code>input()</code>.<br>
        2. Dùng <code>try-except</code> để ép kiểu <code>quantity</code> về <code>int</code>. Nếu số lượng &le; 0 hoặc không phải số integer hợp lệ, xuất thông báo lỗi và bỏ qua.<br>
        3. Tạo một <code>tuple</code> chứa thông tin <code>(asset_name, quantity, room_code)</code> và thêm (append) vào <code>list</code> lưu trữ danh sách thiết bị.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        In thông báo xác nhận thành công hoặc thông báo lỗi dữ liệu đầu vào.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Chức năng 2] Hiển thị Danh mục Thiết bị</b><br>
        <code>display_asset_list</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Không có (Đọc từ danh sách hiện có)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Kiểm tra nếu danh sách rỗng, in thông báo "Danh sách thiết bị trống".<br>
        2. Nếu có dữ liệu, dùng vòng lặp <code>for</code> duyệt qua danh sách và hiển thị từng dòng kèm chỉ số STT (tăng từ 1).
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Bảng danh sách thiết bị rõ ràng theo định dạng dòng: STT, Tên thiết bị, Số lượng, Mã phòng.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Chức năng 3] Cập nhật Số lượng Thiết bị</b><br>
        <code>update_asset_quantity</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - <code>asset_index</code> (int)<br>
        - <code>new_quantity</code> (int)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Cho người dùng nhập STT của thiết bị cần cập nhật.<br>
        2. Kiểm tra tính hợp lệ của vị trí trong danh sách. Sử dụng <code>try-except</code> để bắt lỗi nhập sai kiểu dữ liệu.<br>
        3. Thay thế <code>tuple</code> cũ bằng <code>tuple</code> mới chứa <code>new_quantity</code> giữ nguyên <code>asset_name</code> và <code>room_code</code>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Thông báo cập nhật thành công hoặc lỗi "Chỉ số thiết bị không tồn tại".
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

Đánh giá bài làm dựa trên thang điểm 10 với các chỉ tiêu sau:

1. **Khởi tạo môi trường và Cấu trúc dự án (1.5 điểm)**
   - Khai báo đúng môi trường ảo Python (`.venv`).
   - Đặt tên biến 100% bằng tiếng Anh chuẩn `snake_case` (Ví dụ: `asset_list`, `asset_name`, `quantity`, `room_code`).

2. **Giao diện điều hướng Console CLI Menu (2.0 điểm)**
   - Xây dựng vòng lặp `while True` hiển thị Menu gồm 4 lựa chọn: (1) Thêm thiết bị, (2) Xem danh sách, (3) Cập nhật số lượng, (4) Thoát.
   - Nhận lựa chọn từ người dùng và điều hướng đúng nhánh bằng `if-elif-else`.

3. **Chức năng Thêm và Xem danh sách (4.5 điểm)**
   - Thêm thiết bị mới đúng dạng cấu trúc dữ liệu `list` chứa các `tuple` (2.5 điểm).
   - Duyệt và hiển thị định dạng danh sách chính xác bằng vòng lặp `for` (2.0 điểm).

4. **Chức năng Cập nhật và Xử lý ngoại lệ (2.0 điểm)**
   - Xử lý thành công việc tạo lại `tuple` mới để thay thế trong `list` khi cập nhật số lượng (1.0 điểm).
   - Sử dụng khối `try-except` để xử lý ngoại lệ `ValueError` và bắt lỗi chỉ số vượt quá phạm vi danh sách (1.0 điểm).

---

### **4. Yêu cầu nộp bài**

- **Cấu trúc thư mục nộp bài**:
  ```text
  session_09_entry_test/
  ├── .venv/
  ├── main.py
  └── README.md
  ```
- **Hướng dẫn thực hiện**:
  1. Tạo thư mục làm việc và kích hoạt môi trường ảo `venv`.
  2. Viết mã nguồn toàn bộ luồng chương trình trên file `main.py` (Lưu ý: Không định nghĩa hàm `def` hoặc Class OOP, viết trực tiếp luồng điều khiển trong khối chương trình chính).
  3. Thực hiện commit và push bài làm lên Git repository cá nhân theo cú pháp:
     - `git commit -m "feat: complete session 09 entry test hardware asset cli"`
     - `git push origin main`
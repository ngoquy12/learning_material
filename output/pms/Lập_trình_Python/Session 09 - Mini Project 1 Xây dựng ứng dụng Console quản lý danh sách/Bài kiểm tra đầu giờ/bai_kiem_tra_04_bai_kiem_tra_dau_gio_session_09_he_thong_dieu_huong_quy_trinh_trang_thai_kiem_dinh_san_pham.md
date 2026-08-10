## <center>HỆ THỐNG ĐIỀU HƯỚNG QUY TRÌNH & TRẠNG THÁI KIỂM ĐỊNH SẢN PHẨM (Product Inspection Workflow & Task State Navigation System)</center>

### **1. Mục tiêu**
- Luyện tập kỹ năng sử dụng vòng lặp (`while`, `for`), cấu trúc rẽ nhánh (`if-elif-else`), và các thao tác trên danh sách (`list`).
- Xây dựng ứng dụng Console thực hiện cơ chế điều hướng quy trình làm việc (Task Navigation) và quản lý trạng thái từng công đoạn kiểm định sản phẩm.
- Tuân thủ quy chuẩn đặt tên biến tiếng Anh `snake_case` (PEP 8) và làm việc trực tiếp trên cấu trúc script cơ bản mà không dùng hàm custom (`def`) hay kiểu dữ liệu nâng cao (`dict`, `set`, `class`).

### **2. Yêu cầu**

Một nhà máy sản xuất cần một chương trình Console đơn giản để kỹ thuật viên điều hướng qua các bước trong quy trình kiểm định chất lượng sản phẩm và cập nhật trạng thái của từng bước. Hệ thống sử dụng 2 danh sách song song:
- `task_list`: Lưu tên các công đoạn (VD: `["Kiểm tra ngoại quan", "Thử nghiệm điện áp", "Đóng tem chất lượng"]`).
- `status_list`: Lưu trạng thái tương ứng của từng công đoạn (VD: `["Hoàn thành", "Đang thực hiện", "Chờ xử lý"]`).

Sinh viên thực hiện chương trình chạy trên Terminal theo các yêu cầu chi tiết trong bảng dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left; width: 25%;">Chức năng / Tác vụ</th>
      <th style="padding: 8px; text-align: left; width: 20%;">Đầu vào / Biến khởi tạo</th>
      <th style="padding: 8px; text-align: left; width: 35%;">Quy tắc & Logic xử lý</th>
      <th style="padding: 8px; text-align: left; width: 20%;">Đầu ra / Hiển thị CLI</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><b>1. Xem quy trình & Điều hướng bước</b><br><code>view_and_navigate_steps</code></td>
      <td style="padding: 8px;">
        - <code>task_list</code> (list)<br>
        - <code>status_list</code> (list)<br>
        - <code>current_index</code> (int)
      </td>
      <td style="padding: 8px;">
        - Hiển thị danh sách các bước kèm trạng thái.<br>
        - Đánh dấu ký tự <code>[->]</code> tại bước đang được chọn (vị trí <code>current_index</code>).<br>
        - Cho phép người dùng nhập lệnh:<br>
          + <code>N</code> (Next): Chuyển tới bước tiếp theo (nếu <code>current_index < len(task_list) - 1</code>).<br>
          + <code>P</code> (Previous): Quay lại bước trước (nếu <code>current_index > 0</code>).
      </td>
      <td style="padding: 8px;">In ra bảng danh sách công đoạn và con trỏ đánh dấu bước đang chọn thành công.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>2. Cập nhật trạng thái bước</b><br><code>update_current_step_status</code></td>
      <td style="padding: 8px;">
        - <code>status_choice</code> (int)<br>
        - <code>status_list</code> (list)
      </td>
      <td style="padding: 8px;">
        - Cho phép cập nhật trạng thái của công đoạn tại vị trí <code>current_index</code>.<br>
        - Nhập lựa chọn số:<br>
          + <code>1</code>: "Chờ xử lý"<br>
          + <code>2</code>: "Đang thực hiện"<br>
          + <code>3</code>: "Hoàn thành"<br>
        - Nếu nhập sai lựa chọn số, thông báo lỗi và giữ nguyên trạng thái cũ.
      </td>
      <td style="padding: 8px;">Ghi đè giá trị mới vào <code>status_list[current_index]</code> và thông báo kết quả.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>3. Bổ sung bước kiểm định mới</b><br><code>append_new_workflow_step</code></td>
      <td style="padding: 8px;">
        - <code>new_task_name</code> (str)<br>
        - <code>task_list</code> (list)<br>
        - <code>status_list</code> (list)
      </td>
      <td style="padding: 8px;">
        - Nhập tên bước kiểm định mới từ bàn phím.<br>
        - Nếu tên không được để rỗng, dùng <code>append()</code> để thêm <code>new_task_name</code> vào <code>task_list</code> và thêm giá trị mặc định <code>"Chờ xử lý"</code> vào <code>status_list</code>.
      </td>
      <td style="padding: 8px;">Thêm thành công vào cuối hai danh sách và thông báo tổng số lượng công đoạn hiện tại.</td>
    </tr>
  </tbody>
</table>

> **Phạm vi CẤM sử dụng**: Tuân thủ tuyệt đối không dùng `def` (viết hàm custom), không dùng `dict`, `set`, không định nghĩa `class` OOP. Tất cả logic xử lý được thực hiện trực tiếp trong vòng lặp chính của script.

---

### **3. Tiêu chí đánh giá**

- **Khởi tạo và Cấu trúc dữ liệu (2.0 điểm)**:
  - Khởi tạo đúng hai danh sách song song `task_list` và `status_list` với ít nhất 3 dữ liệu mẫu ban đầu.
  - Quản lý chính xác chỉ số vị trí hiện tại `current_index` (khởi tạo bằng `0`).

- **Tính năng 1: Điều hướng quy trình (3.0 điểm)**:
  - Hiển thị danh sách công đoạn rõ ràng, có ký tự đánh dấu bước đang chọn.
  - Xử lý lệnh `N` (Next) và `P` (Previous) chính xác, ngăn chặn lỗi chỉ số vượt giới hạn (IndexError/Out of bounds).

- **Tính năng 2: Cập nhật trạng thái (2.5 điểm)**:
  - Cập nhật đúng phần tử trong `status_list` dựa trên `current_index`.
  - Kiểm tra hợp lệ lựa chọn trạng thái đầu vào.

- **Tính năng 3: Bổ sung bước mới (1.5 điểm)**:
  - Thêm tên bước mới và trạng thái mặc định vào hai danh sách tương ứng bằng `append()`.
  - Kiểm tra điều kiện đầu vào không được là chuỗi rỗng.

- **Chuẩn Mã Nguồn & Quy Định Cấm (1.0 điểm)**:
  - Đặt tên biến 100% Tiếng Anh chuẩn `snake_case` (VD: `task_list`, `current_index`, `user_choice`).
  - Không vi phạm phạm vi cấm (không sử dụng `def`, `dict`, `set`, `class`).

---

### **4. Yêu cầu nộp bài**

1. Tạo file script Python đặt tên là `task_navigation.py` trong môi trường ảo (`venv`).
2. Kiểm thử toàn bộ các chức năng (Xem danh sách, Điều hướng `N`/`P`, Cập nhật trạng thái, Thêm bước mới, Thoát chương trình).
3. Commit mã nguồn và push bài làm lên kho lưu trữ GitHub cá nhân.
4. Gửi đường dẫn (URL) GitHub repository lên hệ thống quản lý học tập đúng thời hạn quy định.
## <center>XÂY DỰNG HỆ THỐNG QUẢN LÝ TIẾN TRÌNH VÉ HỖ TRỢ KỸ THUẬT (IT Support Ticket Navigation System)</center>

### **1. Mục tiêu**
- Đánh giá khả năng thao tác với danh sách (List) và bộ dữ liệu không thay đổi (Tuple) trong Python 3.12 để quản lý trạng thái luồng công việc (workflow).
- Luyện tập kỹ năng xây dựng menu điều hướng CLI cơ bản sử dụng vòng lặp `while`, câu lệnh điều kiện `if-elif-else`, xử lý chuỗi và chỉ số (index).
- Đảm bảo tuân thủ nguyên tắc lập trình sạch, chuẩn đặt tên biến tiếng Anh `snake_case` và không sử dụng các cấu trúc nâng cao chưa học (như Dictionary, Set, custom `def`, Class).

---

### **2. Yêu cầu**

Xây dựng chương trình dạng Console Script cho phép nhân viên vận hành quản lý quy trình chuyển đổi trạng thái của các vé hỗ trợ kỹ thuật (IT Tickets). Hệ thống sử dụng một Tuple cố định để định nghĩa các bước trong quy trình:
`STATUS_PIPELINE = ("NEW", "IN_PROGRESS", "RESOLVED", "CLOSED")`

Dữ liệu vé hỗ trợ được lưu trữ dưới dạng một `list` chứa các `tuple` thông tin: `(ticket_id, ticket_title, current_status_index)`.

Yêu cầu chi tiết về các chức năng xử lý được mô tả trong bảng sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%;">Tên chức năng / Thành phần</th>
      <th style="width: 20%;">Dữ liệu đầu vào</th>
      <th style="width: 35%;">Lô-gích xử lý & Quy tắc</th>
      <th style="width: 20%;">Đầu ra mong đợi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>[Tạo mới vé hỗ trợ]</b><br><code>add_new_ticket</code></td>
      <td>
        - <code>ticket_id</code> (str)<br>
        - <code>ticket_title</code> (str)
      </td>
      <td>
        1. Yêu cầu nhập Mã vé (<code>ticket_id</code>) và Tiêu đề (<code>ticket_title</code>).<br>
        2. Duyệt danh sách kiểm tra xem <code>ticket_id</code> đã tồn tại hay chưa. Nếu đã tồn tại, hiển thị thông báo lỗi và hủy thao tác.<br>
        3. Nếu mã chưa tồn tại, khởi tạo vé với chỉ số trạng thái mặc định là <code>0</code> (tương ứng với <code>"NEW"</code>).<br>
        4. Thêm tuple <code>(ticket_id, ticket_title, 0)</code> vào danh sách lưu trữ.
      </td>
      <td>Thông báo thành công hoặc thông báo mã vé bị trùng lặp trên Console.</td>
    </tr>
    <tr>
      <td><b>[Chuyển trạng thái vé]</b><br><code>advance_ticket_status</code></td>
      <td>
        - <code>target_ticket_id</code> (str)
      </td>
      <td>
        1. Nhập Mã vé cần chuyển trạng thái.<br>
        2. Tìm kiếm vị trí của vé trong danh sách.<br>
        3. Nếu tìm thấy vé:<br>
        &nbsp;&nbsp;- Kiểm tra xem <code>current_status_index</code> đã đạt trạng thái cuối (<code>len(STATUS_PIPELINE) - 1</code>) hay chưa.<br>
        &nbsp;&nbsp;- Nếu chưa phải trạng thái cuối, cập nhật chỉ số trạng thái lên 1 đơn vị bằng cách tạo tuple mới thay thế tuple cũ tại vị trí tương ứng trong danh sách.<br>
        &nbsp;&nbsp;- Nếu đã là <code>"CLOSED"</code>, thông báo vé đã đóng không thể chuyển tiếp.<br>
        4. Nếu không tìm thấy vé, hiển thị thông báo lỗi.
      </td>
      <td>Thông báo cập nhật trạng thái thành công kèm tên trạng thái mới hoặc thông báo lỗi phù hợp.</td>
    </tr>
    <tr>
      <td><b>[Hiển thị danh sách tiến trình]</b><br><code>display_ticket_pipeline</code></td>
      <td>Không có dữ liệu đầu vào.</td>
      <td>
        1. Kiểm tra nếu danh sách vé đang rỗng, in thông báo chưa có dữ liệu.<br>
        2. Duyệt qua từng phần tử trong danh sách vé.<br>
        3. Sử dụng <code>current_status_index</code> để tra cứu tên trạng thái hiển thị từ Tuple <code>STATUS_PIPELINE</code>.<br>
        4. In ra thông tin chi tiết từng vé theo định dạng chuẩn.
      </td>
      <td>Danh sách vé được trình bày rõ ràng với ID, Tiêu đề và Trạng thái hiện tại.</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

- **Cấu trúc dữ liệu và Tuân thủ Phạm vi (2.0 điểm):**
  - Khai báo đúng `STATUS_PIPELINE` dạng Tuple.
  - Khai báo danh sách `ticket_records` dạng List để chứa các phần tử Tuple.
  - Tuyệt đối KHÔNG dùng Dictionary, Set, custom `def`, Class OOP.
- **Chức năng Tạo mới vé hỗ trợ (2.5 điểm):**
  - Nhập dữ liệu chính xác, kiểm tra trùng lặp `ticket_id` bằng vòng lặp.
  - Thêm đúng cấu trúc tuple với chỉ số trạng thái ban đầu bằng `0`.
- **Chức năng Chuyển trạng thái vé (3.0 điểm):**
  - Tìm kiếm và cập nhật đúng phần tử trong danh sách.
  - Kiểm tra điều kiện biên chính xác (không vượt quá chỉ số cuối của Tuple trạng thái).
- **Chức năng Hiển thị danh sách tiến trình (1.5 điểm):**
  - Duyệt danh sách và ánh xạ đúng chỉ số trạng thái sang tên chuỗi tương ứng.
  - Trình bày thông tin rõ ràng, xử lý trường hợp danh sách rỗng.
- **Chuẩn Mã Nguồn và Giao diện Console (1.0 điểm):**
  - Đặt tên biến 100% bằng tiếng Anh chuẩn `snake_case` (VD: `ticket_id`, `ticket_records`, `target_ticket_id`).
  - Giao diện menu CLI rõ ràng, có luồng thoát chương trình an toàn.

---

### **4. Yêu cầu nộp bài**

- Học viên chuẩn bị mã nguồn trong một tệp Python duy nhất đặt tên là `main.py`.
- Cam kết mã nguồn chạy hoàn chỉnh trên môi trường **Python 3.12**.
- Đẩy mã nguồn lên kho lưu trữ GitHub cá nhân và nộp liên kết (URL) của commit hoặc Pull Request theo hướng dẫn của giảng viên.
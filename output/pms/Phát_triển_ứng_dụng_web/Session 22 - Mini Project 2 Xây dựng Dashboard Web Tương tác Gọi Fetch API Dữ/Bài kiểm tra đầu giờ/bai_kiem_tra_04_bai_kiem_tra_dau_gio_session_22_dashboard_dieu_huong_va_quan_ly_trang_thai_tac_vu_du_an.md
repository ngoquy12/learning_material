## <center>BÀI KIỂM TRA ĐẦU GIỜ: XÂY DỰNG DASHBOARD ĐIỀU HƯỚNG VÀ QUẢN LÝ TRẠNG THÁI TÁC VỤ DỰ ÁN (PROJECT TASK & STATE NAVIGATION DASHBOARD)</center>

### **1. Mục tiêu**
- **Kiến thức**: Đánh giá năng lực tích hợp Fetch API bất đồng bộ (`async/await`), truy xuất và thao tác DOM Tree, cùng kỹ năng quản lý trạng thái dữ liệu tác vụ trên bộ nhớ (In-memory State Management) theo mô hình Single Page Application (SPA).
- **Kỹ năng**: Thực thi quy trình gọi API dữ liệu động, xử lý các trạng thái lọc dữ liệu (Filter Tabs), rẽ nhánh render giao diện linh hoạt và xử lý các sự kiện tương ứng với từng tác vụ mà không làm tải lại trang (No Page Reload).
- **Thời gian hoàn thành**: 15 - 20 phút.

---

### **2. Yêu cầu**

Thực hiện bài tập lập trình xây dựng một giao diện Dashboard đơn giản cho phép điều hướng và quản lý trạng thái các tác vụ công việc của dự án. Giao diện bao gồm thanh điều hướng bộ lọc (Filter Tabs: Tất cả / Đang xử lý / Hoàn thành), vùng hiển thị danh sách tác vụ động và cơ chế chuyển đổi trạng thái làm việc trực tiếp.

Chi tiết các chức năng cần hoàn thiện theo bảng mô tả bên dưới:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 10px; text-align: left; width: 25%;">Tên Chức năng / Thành phần</th>
      <th style="padding: 10px; text-align: left; width: 20%;">Đầu vào (Parameters / Inputs)</th>
      <th style="padding: 10px; text-align: left; width: 35%;">Xử lý Logic & Quy tắc</th>
      <th style="padding: 10px; text-align: left; width: 20%;">Đầu ra (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><b>[Tải danh sách tác vụ bất đồng bộ]</b><br><code>fetchTaskList()</code></td>
      <td style="padding: 8px;"><code>statusFilter</code> (string: <code>'all'</code>, <code>'in_progress'</code>, <code>'completed'</code>)</td>
      <td style="padding: 8px;">
        - Sử dụng cú pháp <code>async/await</code> kết hợp <code>fetch()</code> để gửi truy vấn đến Rest API giả lập (ví dụ: <code>https://jsonplaceholder.typicode.com/todos?_limit=8</code>).<br>
        - Chuyển đổi dữ liệu nhận được thành JSON.<br>
        - Lọc mảng kết quả dựa theo tham số <code>statusFilter</code> (nếu <code>statusFilter === 'completed'</code> lấy các task có <code>completed === true</code>, ngược lại nếu <code>statusFilter === 'in_progress'</code> lấy các task có <code>completed === false</code>).<br>
        - Sử dụng khối <code>try...catch</code> để bắt lỗi mạng và hiển thị thông báo lỗi lên màn hình nếu thất bại.
      </td>
      <td style="padding: 8px;">Trả về mảng các đối tượng tác vụ <code>taskList</code> tương ứng với bộ lọc được chọn.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>[Hiển thị danh sách tác vụ lên DOM UI]</b><br><code>renderTaskDashboard()</code></td>
      <td style="padding: 8px;"><code>taskList</code> (Array of Task Objects: <code>[{ id, title, completed }]</code>)</td>
      <td style="padding: 8px;">
        - Xóa sạch nội dung cũ trong thẻ chứa HTML (<code>taskContainer.innerHTML = ''</code>).<br>
        - Nếu mảng <code>taskList</code> rỗng, hiển thị thông báo "Không có tác vụ nào thuộc trạng thái này".<br>
        - Duyệt qua từng phần tử tác vụ để tạo phần tử HTML tương ứng.<br>
        - Hiển thị nhãn trạng thái (Badge): "Hoàn thành" (màu xanh) hoặc "Đang xử lý" (màu vàng).<br>
        - Gắn nút hành động "Đổi trạng thái" (Toggle Status) cho từng thẻ tác vụ và đăng ký sự kiện <code>click</code> cho từng nút để gọi hàm <code>switchTaskStatus(taskId)</code>.
      </td>
      <td style="padding: 8px;">Cập nhật giao diện danh sách tác vụ trên DOM trực quan và chính xác.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>[Điều chuyển trạng thái tác vụ]</b><br><code>switchTaskStatus()</code></td>
      <td style="padding: 8px;"><code>taskId</code> (number / string)</td>
      <td style="padding: 8px;">
        - Tìm kiếm tác vụ tương ứng với <code>taskId</code> trong mảng biến trạng thái toàn cục trong bộ nhớ.<br>
        - Đảo ngược giá trị thuộc tính <code>completed</code> (từ <code>true</code> sang <code>false</code> hoặc ngược lại).<br>
        - Gọi lại hàm <code>renderTaskDashboard()</code> với dữ liệu mảng đã được cập nhật để cập nhật trạng thái UI hiển thị mới nhất mà không reload trang.
      </td>
      <td style="padding: 8px;">Trạng thái tác vụ được đổi thành công cả trên biến bộ nhớ lẫn UI hiển thị.</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

- **Cấu trúc & Cú pháp JavaScript ES6+ (2.0 điểm)**:
  - Khai báo đúng các dạng hàm `async/await`, `arrow functions`, phân rã mảng/đối tượng và đặt tên biến 100% bằng Tiếng Anh theo chuẩn `camelCase`.
- **Tích hợp API & Bất đồng bộ (3.0 điểm)**:
  - Sử dụng `fetch()` và `async/await` lấy dữ liệu chính xác từ endpoint, xử lý đúng cơ chế lọc dữ liệu theo trạng thái tác vụ, bắt lỗi đầy đủ bằng `try...catch`.
- **Thao tác DOM & Quản lý Sự kiện (3.0 điểm)**:
  - Render thẻ HTML động đúng cấu trúc, gắn sự kiện điều hướng Tab Filter mượt mà, xử lý sự kiện nút chuyển trạng thái `switchTaskStatus()` chính xác.
- **UI/UX & Trải nghiệm Người dùng (2.0 điểm)**:
  - Hiển thị rõ ràng các thẻ tác vụ, có màu sắc phân biệt trạng thái công việc (badge), thông báo danh sách rỗng hợp lý khi không có dữ liệu.

---

### **4. Yêu cầu nộp bài**

1. Tạo thư mục bài làm đặt tên theo chuẩn: `ho_ten_bkt_session_22` (Ví dụ: `nguyen_van_a_bkt_session_22`).
2. Mã nguồn phải tách biệt rõ ràng các tệp: `index.html`, `style.css`, và `script.js`.
3. Đẩy mã nguồn lên kho lưu trữ **GitHub Personal** và đính kèm đường link repository vào hệ thống nộp bài theo thời hạn quy định.
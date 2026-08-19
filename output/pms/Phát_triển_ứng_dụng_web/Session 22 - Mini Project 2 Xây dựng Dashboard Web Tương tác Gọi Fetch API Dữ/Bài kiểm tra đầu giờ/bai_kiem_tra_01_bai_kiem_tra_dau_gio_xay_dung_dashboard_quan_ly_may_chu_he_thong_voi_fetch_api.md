# <center>Bảng Điều Khiển Quản Lý Máy Chủ Hệ Thống (System Server Node Dashboard)</center>

### **1. Mục tiêu**
- Đánh giá khả năng vận dụng cú pháp **Async/Await** và **Fetch API** để lấy dữ liệu bất đồng bộ từ REST API.
- Đánh giá kỹ năng thao tác **DOM API** (truy xuất phần tử, thay đổi nội dung HTML, gắn CSS class linh hoạt bằng toán tử ba ngôi).
- Kiểm tra tư duy xử lý sự kiện tương tác người dùng (Event Handling với `<select>`) để lọc dữ liệu hiển thị trên giao diện SPA (Single Page Application).

---

### **2. Yêu cầu**

Thực sinh viên triển khai ứng dụng Single Page Web Dashboard hiển thị và quản lý trạng thái các máy chủ hệ thống. Chi tiết các chức năng được mô tả trong bảng quy định kỹ thuật dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 25%;">Tên chức năng / Hàm</th>
      <th style="width: 20%;">Tham số đầu vào (Input)</th>
      <th style="width: 35%;">Logic xử lý & Quy tắc</th>
      <th style="width: 20%;">Đầu ra dự kiến (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>[Lấy danh sách máy chủ từ API]</b><br><code>fetchServerNodes()</code></td>
      <td>Không có (<code>None</code>)</td>
      <td>
        - Sử dụng cú pháp <code>async/await</code> gọi <code>fetch()</code> tới đường dẫn API giả lập <code>https://jsonplaceholder.typicode.com/users</code>.<br>
        - Kiểm tra tính hợp lệ của phản hồi bằng <code>response.ok</code>. Nếu phản hồi lỗi, hiển thị thông báo lỗi trên UI dạng cảnh báo (Inline Error Banner).<br>
        - Chuyển đổi dữ liệu nhận được sang định dạng JSON và gán vào mảng dữ liệu <code>serverList</code>.<br>
        - Gọi hàm <code>renderServerList()</code> để hiển thị dữ liệu ban đầu.
      </td>
      <td>Mảng đối tượng <code>serverList</code> chứa thông tin máy chủ và tự động kích hoạt hiển thị DOM.</td>
    </tr>
    <tr>
      <td><b>[Hiển thị danh sách máy chủ lên DOM]</b><br><code>renderServerList()</code></td>
      <td><code>nodes</code> (<code>Array&lt;Object&gt;</code>)</td>
      <td>
        - Xóa sạch nội dung cũ trong vùng hiển thị (<code>#serverListContainer</code>).<br>
        - Duyệt qua từng phần tử trong mảng <code>nodes</code> bằng vòng lặp <code>forEach</code> hoặc <code>for...of</code>.<br>
        - Sử dụng Template Literals để tạo các thẻ đại diện cho máy chủ (dòng <code>&lt;tr&gt;</code> hoặc thẻ <code>&lt;div class="card"&gt;</code>).<br>
        - Sử dụng toán tử ba ngôi (Ternary Operator) để định dạng trạng thái (ví dụ: gán nhãn "Hoạt động" kèm class <code>badge-success</code> hoặc "Bảo trì" kèm class <code>badge-danger</code> dựa trên ID máy chủ).
      </td>
      <td>Cập nhật trực tiếp cây DOM hiển thị danh sách máy chủ với giao diện chuẩn UI/UX.</td>
    </tr>
    <tr>
      <td><b>[Lọc máy chủ theo trạng thái]</b><br><code>filterServersByStatus()</code></td>
      <td><code>selectedStatus</code> (<code>string</code>)</td>
      <td>
        - Đăng ký sự kiện <code>change</code> trên thanh chọn trạng thái (<code>#statusFilter</code>).<br>
        - Nếu <code>selectedStatus === 'all'</code>, hiển thị toàn bộ danh sách máy chủ.<br>
        - Nếu <code>selectedStatus === 'active'</code> hoặc <code>'maintenance'</code>, lọc danh sách <code>serverList</code> tương ứng bằng phương thức lọc mảng.<br>
        - Gọi lại <code>renderServerList()</code> với mảng đã qua xử lý lọc.
      </td>
      <td>Giao diện tự động cập nhật hiển thị đúng danh sách máy chủ theo tiêu chí lọc được chọn.</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

- **[3.0 Điểm] Gọi API và Xử lý Bất đồng bộ:** Sử dụng chính xác `async/await`, `fetch()` và kiểm tra lỗi khi gọi API.
- **[3.0 Điểm] Thao tác DOM & Render Dữ liệu:** Sử dụng đúng Template Literals, toán tử ba ngôi để tạo thẻ HTML động và hiển thị dữ liệu chính xác lên UI.
- **[2.0 Điểm] Xử lý Sự kiện & Lọc Dữ liệu:** Bắt sự kiện `change` trên ô `<select>` và lọc mảng đúng theo yêu cầu logic.
- **[2.0 Điểm] Mã nguồn Sạch & Đặt tên Chuẩn:** Đặt tên biến, tên hàm 100% bằng Tiếng Anh có nghĩa, định dạng mã nguồn rõ ràng theo chuẩn ES6+.

---

### **4. Yêu cầu nộp bài**

1. Tạo thư mục bài làm đặt tên theo cú pháp: `HoVaTen_MaSinhVien_Session22`.
2. Tạo các tệp tin `index.html`, `styles.css`, và `script.js` trong thư mục bài làm.
3. Tiến hành đẩy mã nguồn (Push) lên kho lưu trữ GitHub cá nhân.
4. Nộp liên kết (URL) repository chứa bài làm lên hệ thống quản lý học tập trước khi hết thời gian làm bài.

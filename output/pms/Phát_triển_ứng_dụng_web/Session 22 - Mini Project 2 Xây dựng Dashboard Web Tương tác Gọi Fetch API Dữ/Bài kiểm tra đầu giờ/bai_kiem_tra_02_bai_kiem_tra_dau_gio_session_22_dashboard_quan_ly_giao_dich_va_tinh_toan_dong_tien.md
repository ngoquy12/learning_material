# <center>BÀI KIỂM TRA ĐẦU GIỜ: XÂY DỰNG DASHBOARD XỬ LÝ GIAO DỊCH VÀ TÍNH TOÁN DÒNG TIỀN (FINANCIAL TRANSACTION DASHBOARD)</center>

### **1. Mục tiêu**
Đánh giá năng lực vận dụng kiến thức lập trình JavaScript ES6+, thao tác DOM API, câu lệnh bất đồng bộ `async/await` kết hợp `fetch()` API để xây dựng màn hình Dashboard quản lý và tính toán giao dịch dòng tiền cho hệ thống thanh toán trực tuyến.

---

### **2. Yêu cầu**

Sinh viên khởi tạo ứng dụng Web Single Page với file `index.html` và `script.js` để hoàn thành các chức năng theo bảng mô tả kỹ thuật dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 22%;">Tên Chức Năng / Hàm</th>
      <th style="width: 20%;">Đầu Vào (Input)</th>
      <th style="width: 38%;">Logic Xử Lý & Quy Tắc Nghiệp Vụ</th>
      <th style="width: 20%;">Đầu Ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Lấy danh sách giao dịch từ API</b><br><code>fetchTransactionData()</code></td>
      <td><code>apiUrl</code> (string): Đường dẫn API chứa dữ liệu giao dịch giả định.</td>
      <td>
        - Gọi Fetch API bất đồng bộ với cú pháp <code>async/await</code>.<br>
        - Trong lúc chờ dữ liệu, hiển thị trạng thái thông báo <i>"Đang tải dữ liệu giao dịch..."</i> trên giao diện DOM.<br>
        - Chuyển đổi dữ liệu JSON thu được (chứa các thuộc tính: <code>transactionId</code>, <code>customerName</code>, <code>amount</code>, <code>processingFee</code>, <code>status</code>).<br>
        - Xử lý lỗi với <code>try...catch</code>, nếu thất bại hiển thị thẻ thông báo lỗi trên UI.
      </td>
      <td>Trả về mảng <code>transactions</code> và hiển thị danh sách ban đầu lên bảng DOM table.</td>
    </tr>
    <tr>
      <td><b>Tính toán chỉ số dòng tiền</b><br><code>calculateMetrics()</code></td>
      <td><code>transactionsList</code> (Array): Mảng chứa các đối tượng giao dịch.</td>
      <td>
        - Duyệt mảng giao dịch để tính toán các chỉ số nghiệp vụ:<br>
        + <b>Tổng doanh thu hoàn tất</b>: Tổng <code>amount</code> của các giao dịch có <code>status === 'COMPLETED'</code>.<br>
        + <b>Tổng phí xử lý</b>: Tổng <code>processingFee</code> của tất cả giao dịch.<br>
        + <b>Số lượng giao dịch thành công</b>: Số lượng phần tử có <code>status === 'COMPLETED'</code>.<br>
        - Cập nhật giá trị tính toán vào các phần tử HTML tương ứng trên Dashboard UI qua DOM API.
      </td>
      <td>Cập nhật hiển thị số liệu nghiệp vụ real-time lên các thẻ chỉ số trên giao diện.</td>
    </tr>
    <tr>
      <td><b>Lọc giao dịch theo trạng thái</b><br><code>filterTransactionsByStatus()</code></td>
      <td>
        - <code>selectedStatus</code> (string): Trạng thái chọn từ thẻ <code>&lt;select&gt;</code> (<code>'ALL'</code>, <code>'COMPLETED'</code>, <code>'PENDING'</code>, <code>'FAILED'</code>).<br>
        - <code>originalTransactions</code> (Array).
      </td>
      <td>
        - Lắng nghe sự kiện <code>change</code> trên thanh lọc <code>&lt;select id="statusFilter"&gt;</code>.<br>
        - Nếu <code>selectedStatus === 'ALL'</code>, lấy toàn bộ danh sách.<br>
        - Ngược lại, lọc mảng theo điều kiện <code>item.status === selectedStatus</code>.<br>
        - Đổ lại mảng đã lọc ra giao diện bảng HTML DOM và gọi hàm <code>calculateMetrics()</code> để cập nhật chỉ số dòng tiền tương ứng với mảng đã lọc.
      </td>
      <td>Bảng dữ liệu DOM và các con số thống kê được làm mới theo đúng bộ lọc được chọn.</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

- **3.5 Điểm**: Lấy dữ liệu bất đồng bộ từ Fetch API thành công với `async/await`, xử lý trạng thái Loading và Render dữ liệu bảng HTML chuẩn xác.
- **3.0 Điểm**: Thực hiện chính xác thuật toán tính toán dòng tiền (doanh thu thành công, tổng phí, số lượng) và hiển thị lên UI.
- **2.5 Điểm**: Tương tác sự kiện lọc trạng thái (`filter`) mượt mà, render lại bảng và cập nhật chỉ số thống kê chính xác.
- **1.0 Điểm**: Mã nguồn sạch (Clean Code), đặt tên biến/hàm 100% bằng Tiếng Anh chuẩn ngữ nghĩa (`camelCase`), giao diện UI có thông báo lỗi rõ ràng.

---

### **4. Yêu cầu nộp bài**

- Sinh viên hoàn thiện bài làm trực tiếp trên thư mục dự án Cursor AI IDE.
- Đẩy mã nguồn lên kho lưu trữ GitHub cá nhân và nộp liên kết Repository kèm bản chụp màn hình kết quả chạy ứng dụng lên hệ thống quản lý học tập.

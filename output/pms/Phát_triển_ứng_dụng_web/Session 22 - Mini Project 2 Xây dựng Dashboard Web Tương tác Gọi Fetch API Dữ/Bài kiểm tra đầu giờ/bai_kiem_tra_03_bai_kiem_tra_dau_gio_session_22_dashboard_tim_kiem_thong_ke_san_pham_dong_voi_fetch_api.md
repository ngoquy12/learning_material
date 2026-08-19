# <center>BÀI KIỂM TRA ĐẦU GIỜ: XÂY DỰNG DASHBOARD TÌM KIẾM VÀ THỐNG KÊ SẢN PHẨM DÙNG FETCH API (FETCH API & DOM DASHBOARD SEARCH/ANALYTICS)</center>

### **1. Mục tiêu**
* **Đánh giá kiến thức:** Kiểm tra khả năng ứng dụng cú pháp `async/await` kết hợp `fetch API` để tải dữ liệu JSON bất đồng bộ, thao tác xử lý mảng dữ liệu (lọc, tìm kiếm, tính toán thống kê) và cập nhật giao diện người dùng động (Single Page Application UI) thông qua DOM API.
* **Thời gian hoàn thành dự kiến:** 15 - 20 phút.

---

### **2. Yêu cầu**

Thực hiện xây dựng các chức năng chính cho ứng dụng **Dashboard Tìm Kiếm & Thống Kê Sản Phẩm Công Nghệ (Tech Product Analytics Dashboard)** sử dụng JavaScript Vanilla ES6+, Fetch API và HTML5/CSS3 theo quy tả trong bảng dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Tên Chức Năng / Thành Phần</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Đầu Vào (Input / Parameters)</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Luồng Xử Lý & Quy Tắc Logic</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Đầu Ra (Output / Expected Return Value)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <b>[Tải dữ liệu Sản phẩm]</b><br>
        <code>fetchProductData()</code>
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <code>apiUrl</code> (String - Đường dẫn API lấy danh sách sản phẩm)
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        - Sử dụng cú pháp <code>async/await</code> và <code>fetch()</code> để gửi request lấy dữ liệu sản phẩm.<br>
        - Hiển thị phần tử báo trạng thái đang tải (Loading indicator) lên giao diện trước khi gọi API.<br>
        - Khi nhận phản hồi thành công, chuyển đổi dữ liệu dạng JSON, ẩn Loading indicator và lưu mảng sản phẩm thu được vào mảng toàn cục <code>productsList</code>.<br>
        - Nếu gặp lỗi mạng hoặc HTTP status thất bại, hiển thị thông báo lỗi inline trực tiếp lên giao diện (ví dụ: thẻ <code>#errorMessage</code>).<br>
        - Gọi hàm <code>renderProductList()</code> và <code>calculateProductStats()</code> để cập nhật UI lần đầu.
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <code>Promise<void></code> (Dữ liệu mảng <code>productsList</code> được cập nhật và hiển thị trực tiếp lên bảng DOM UI).
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <b>[Lọc & Tìm kiếm Nâng cao]</b><br>
        <code>filterAndSearchProducts()</code>
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <code>keyword</code> (String), <code>selectedCategory</code> (String), <code>productsList</code> (Array)
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        - Lắng nghe sự kiện <code>input</code> từ ô tìm kiếm (<code>#searchInput</code>) và sự kiện <code>change</code> từ dropdown danh mục (<code>#categorySelect</code>).<br>
        - Lọc danh sách <code>productsList</code> thỏa mãn đồng thời 2 điều kiện:<br>
          1. Thuộc tính <code>title</code> của sản phẩm chứa chuỗi <code>keyword</code> (không phân biệt chữ hoa / chữ thường).<br>
          2. Thuộc tính <code>category</code> của sản phẩm trùng khớp với <code>selectedCategory</code> (Nếu <code>selectedCategory === "all"</code> thì bỏ qua điều kiện lọc danh mục).<br>
        - Gọi hàm hiển thị giao diện <code>renderProductList()</code> với mảng kết quả đã lọc và tính toán lại thống kê qua <code>calculateProductStats()</code>.
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <code>filteredProducts</code> (Array - Mảng các đối tượng sản phẩm sau khi lọc).
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <b>[Thống kê Chỉ số Dashboard]</b><br>
        <code>calculateProductStats()</code>
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <code>currentProducts</code> (Array - Danh sách sản phẩm đang hiển thị trên giao diện)
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        - Duyệt mảng <code>currentProducts</code> để tính toán 3 số liệu thống kê tổng hợp:<br>
          1. <code>totalCount</code>: Tổng số lượng dòng sản phẩm trong mảng.<br>
          2. <code>totalStockQuantity</code>: Tổng số lượng tồn kho của tất cả sản phẩm (cộng dồn trường <code>stock</code>).<br>
          3. <code>averagePrice</code>: Giá trung bình của các sản phẩm hiển thị (Tổng giá / tổng số dòng sản phẩm, làm tròn 2 chữ số thập phân bằng <code>toFixed(2)</code>). Trường hợp mảng rỗng thì gán bằng 0.<br>
        - Cập nhật các thông số tính toán được vào các thẻ hiển thị Metric Card tương ứng trên cây DOM qua thuộc tính <code>textContent</code>.
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <code>Object</code> chứa <code>{ totalCount, totalStockQuantity, averagePrice }</code> và cập nhật UI.
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

Chấm điểm trên thang điểm 10 theo các tiêu chí sau:

* **3.0 điểm:** Thực thi thành công hàm `fetchProductData()` sử dụng đúng cú pháp `async/await`, gửi request `fetch()`, xử lý trạng thái Loading indicator và hiển thị thông báo lỗi trên UI khi có phát sinh lỗi.
* **3.5 điểm:** Lập trình chính xác logic hàm `filterAndSearchProducts()`, xử lý được sự kiện `input` và `change` để lọc kết quả kết hợp theo từ khóa và danh mục.
* **2.5 điểm:** Hoàn thành logic tính toán chỉ số thống kê `calculateProductStats()` và cập nhật chính xác các giá trị này vào thẻ DOM Dashboard Metrics.
* **1.0 điểm:** Đặt tên biến và hàm chuẩn mực Tiếng Anh camelCase, tổ chức mã nguồn mô-đun rõ ràng, tuân thủ quy chuẩn mã sạch ES6+.

---

### **4. Yêu cầu nộp bài**
* Học viên tạo thư mục dự án và thực hiện commit mã nguồn đầy đủ gồm các file `index.html`, `style.css`, `app.js` lên kho lưu trữ GitHub cá nhân.
* Đẩy toàn bộ mã nguồn lên branch `main` và nộp liên kết Repository lên hệ thống học tập trước khi hết thời gian làm bài.

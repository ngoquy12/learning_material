## <center>Bài Kiểm Tra Đầu Giờ: Hệ Thống Thống Kê & Lọc Danh Mục Phụ Kiện Công Nghệ Console (Tech Catalog Analytics CLI)</center>

### **1. Mục tiêu**
- Assessment kỹ năng thao tác với mảng đối tượng (Array of Objects), vòng lặp lồng logic kiểm tra điều kiện phức hợp trong JavaScript ES6+.
- Đánh giá khả năng thực thi thuật toán lọc dữ liệu đa điều kiện và tính toán thống kê tích lũy (tổng giá trị tồn kho, số lượng sản phẩm hết hàng).
- Đánh giá kỹ năng định dạng dữ liệu đầu ra console bằng Template Literals và chuyển đổi dữ liệu qua cấu trúc JSON (`JSON.stringify`).
- Rèn luyện tư duy lập trình mã nguồn chuẩn mực: đặt tên biến 100% Tiếng Anh, tuân thủ `camelCase` và không sử dụng các tính năng nâng cao chưa học.

### **2. Yêu cầu**

Cho mảng dữ liệu mẫu ban đầu lưu trữ danh sách các phụ kiện công nghệ trong hệ thống:
```javascript
const products = [
  { productId: "P01", productName: "Wireless Mouse", category: "Accessories", price: 25, stockQuantity: 50, isAvailable: true },
  { productId: "P02", productName: "Mechanical Keyboard", category: "Accessories", price: 120, stockQuantity: 0, isAvailable: false },
  { productId: "P03", productName: "Gaming Monitor", category: "Display", price: 350, stockQuantity: 15, isAvailable: true },
  { productId: "P04", productName: "USB-C Hub", category: "Accessories", price: 45, stockQuantity: 25, isAvailable: true },
  { productId: "P05", productName: "4K Web Camera", category: "Display", price: 95, stockQuantity: 0, isAvailable: false }
];
```

Thực hiện viết đoạn mã JavaScript (Node.js Console CLI) xử lý 3 chức năng chính theo bảng mô tả chi tiết dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 25%;">Tên chức năng / Khối xử lý</th>
      <th style="width: 20%;">Dữ liệu đầu vào</th>
      <th style="width: 35%;">Xử lý & Quy tắc nghiệp vụ</th>
      <th style="width: 20%;">Kết quả đầu ra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Lọc sản phẩm theo danh mục và khoảng giá</b><br><code>filterProductsByPriceAndCategory</code></td>
      <td>
        - Mảng <code>products</code><br>
        - Biến <code>targetCategory</code> = "Accessories"<br>
        - Biến <code>minPrice</code> = 20<br>
        - Biến <code>maxPrice</code> = 100
      </td>
      <td>
        - Duyệt mảng <code>products</code> bằng vòng lặp (<code>for</code> hoặc <code>for...of</code>).<br>
        - Sử dụng toán tử so sánh nghiêm ngặt (<code>===</code>) và logic (<code>&&</code>) để lọc ra các sản phẩm thỏa mãn đồng thời: thuộc danh mục <code>targetCategory</code> VÀ có mức giá nằm trong khoảng [<code>minPrice</code>, <code>maxPrice</code>].<br>
        - Thêm các sản phẩm thỏa mãn vào mảng kết quả <code>filteredProducts</code> bằng phương thức <code>.push()</code>.
      </td>
      <td>
        Mảng <code>filteredProducts</code> chứa danh sách đối tượng các sản phẩm thỏa mãn điều kiện lọc.
      </td>
    </tr>
    <tr>
      <td><b>Thống kê tổng quan giá trị tồn kho theo danh mục</b><br><code>calculateCategoryAnalytics</code></td>
      <td>
        - Mảng <code>products</code><br>
        - Biến <code>analyticsCategory</code> = "Accessories"
      </td>
      <td>
        - Khởi tạo các biến tích lũy: <code>totalStockQuantity = 0</code>, <code>totalInventoryValue = 0</code>, <code>outOfStockItemCount = 0</code>.<br>
        - Duyệt qua mảng <code>products</code>, kiểm tra nếu thuộc <code>analyticsCategory</code>:<br>
          + Cộng dồn <code>stockQuantity</code> vào <code>totalStockQuantity</code>.<br>
          + Cộng dồn giá trị tồn kho bằng biểu thức toán tử <code>price * stockQuantity</code> vào <code>totalInventoryValue</code>.<br>
          + Nếu <code>stockQuantity === 0</code> hoặc <code>isAvailable === false</code> thì tăng <code>outOfStockItemCount</code> lên 1 đơn vị.<br>
        - Tổng hợp thành đối tượng <code>analyticsSummary</code>.
      </td>
      <td>
        Đối tượng <code>analyticsSummary</code> chứa các thuộc tính: <code>categoryName</code>, <code>totalStockQuantity</code>, <code>totalInventoryValue</code>, <code>outOfStockItemCount</code>.
      </td>
    </tr>
    <tr>
      <td><b>Xuất báo cáo định dạng JSON & Console</b><br><code>exportAnalyticsReport</code></td>
      <td>
        - Đối tượng <code>analyticsSummary</code><br>
        - Mảng <code>filteredProducts</code>
      </td>
      <td>
        - Chuyển đổi đối tượng <code>analyticsSummary</code> thành chuỗi JSON dạng chuẩn bằng <code>JSON.stringify(analyticsSummary, null, 2)</code>.<br>
        - Sử dụng chuỗi Template Literals (dấu backticks `` ` ``) để in định dạng báo cáo tiêu đề và danh sách kết quả ra màn hình Console.<br>
        - In số lượng sản phẩm lọc được và nội dung chuỗi JSON báo cáo chi tiết.
      </td>
      <td>
        Hiển thị chuỗi thông báo kết quả báo cáo rõ ràng, chuyên nghiệp trên màn hình Console.
      </td>
    </tr>
  </tbody>
</table>

### **3. Tiêu chí đánh giá**

- **Cấu trúc & Khai báo dữ liệu (2.0 điểm):**
  - Khai báo đúng mảng đối tượng mẫu ban đầu với tên biến 100% Tiếng Anh, chuẩn `camelCase` (`productId`, `productName`, `category`, `price`, `stockQuantity`, `isAvailable`).
  - Phân biệt và sử dụng đúng từ khóa `const` và `let`.

- **Xử lý Thuật toán Lọc nâng cao (3.0 điểm):**
  - Duyệt mảng chính xác bằng vòng lặp `for` hoặc `for...of`.
  - Áp dụng chuẩn xác toán tử so sánh bằng nghiêm ngặt `===`, toán tử so sánh số học và toán tử logic `&&`.
  - Đưa phần tử thỏa mãn vào mảng kết quả bằng `.push()`.

- **Xử lý Logic Thống kê Tích lũy (3.0 điểm):**
  - Khởi tạo và tính toán đúng các biến tích lũy (tổng số lượng tồn, tổng giá trị tồn kho `price * stockQuantity`).
  - Đếm chính xác số lượng sản phẩm hết hàng thỏa mãn điều kiện.
  - Tổng hợp thành công đối tượng thống kê kết quả (`analyticsSummary`).

- **Xuất Báo Báo & Format Dữ liệu (2.0 điểm):**
  - Sử dụng thành thạo `JSON.stringify()` với tham số thụt lề để định dạng cấu trúc JSON.
  - Trình bày thông điệp đầu ra bằng Template Literals chuyên nghiệp, sạch đẹp trên màn hình Console.

### **4. Yêu cầu nộp bài**

- Học viên thực hiện trực tiếp đoạn mã xử lý trong tệp `script.js` (hoặc `index.js`) trong môi trường Cursor AI IDE / VS Code.
- Mở Terminal tích hợp và chạy lệnh kiểm tra kết quả bằng Node.js: `node script.js`.
- Chụp ảnh màn hình kết quả chạy Console thành công và thực hiện đẩy mã nguồn lên kho lưu trữ GitHub (GitHub Repository) cá nhân.
- Nộp liên kết (URL) của commit hoặc repository lên hệ thống quản lý học tập đúng thời hạn quy định.
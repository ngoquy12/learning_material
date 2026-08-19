# <center>[Mini project] Xây dựng Ứng dụng Quản lý Danh mục Bán hàng Console (Phần 1)<br>(Sales Catalog Management Console Application - Part 1)</center>

### **1. Mục tiêu dự án**
[REQUIREMENT] Mini Project 1 là bài tập tổng hợp giai đoạn 1, tập trung vào việc áp dụng các kiến thức JavaScript ES6+ cốt lõi (biến `let`/`const`, kiểu dữ liệu nguyên thủy và dữ liệu phức hợp, toán tử, cấu trúc rẽ nhánh `if-else`/`switch-case`, vòng lặp `for`/`while`, mảng `Array`, đối tượng `Object`, định dạng chuỗi `Template Literals` và cấu trúc dữ liệu `JSON`).

Dự án giúp học viên:
* Định hình và thiết kế cấu trúc dữ liệu cho mô hình quản lý bán hàng thực tế trên môi trường Console / CLI Application.
* Thành thạo thao tác CRUD (Create, Read, Update, Delete) trên mảng và đối tượng trong JavaScript Vanilla.
* Áp dụng tư duy kiểm chuẩn dữ liệu đầu vào (Validation) và xử lý ngoại lệ nghiệp vụ trực tiếp bằng màn hình Console mà không phụ thuộc vào giao diện trang web.
* Tối ưu hóa quy trình phát triển mã nguồn với Cursor AI IDE, áp dụng chuẩn mã sạch Clean Code ES6+ và quản lý mã nguồn bằng Git/GitHub.

---

### **2. Đề bài và Yêu cầu**

Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md).

#### **Cấu trúc Thư mục Dự án Gợi ý (Project Skeleton Tree)**

```text
sales-catalog-console/
├── data/
│   └── initialCatalog.json

# File JSON lưu trữ danh mục sản phẩm ban đầu
├── src/
│   ├── config.js

# Định nghĩa các hằng số hệ thống và mã lỗi
│   └── catalogManager.js

# Logic xử lý dữ liệu danh mục sản phẩm (Array & Object)
├── index.js

# File chạy chính của ứng dụng Console
├── package.json

# Khai báo dự án Node.js runtime
└── README.md

# Tài liệu hướng dẫn cài đặt và vận hành
```

# **Danh sách Chức năng Nghiệp vụ Chi tiết**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: center; width: 5%;">STT</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 25%;">Tên chức năng/hàm</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 35%;">Mô tả nghiệp vụ chi tiết</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 17%;">Đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 18%;">Đầu ra mong đợi (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Khởi tạo Danh mục]</b><br><code>initializeCatalog()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Đọc và nạp dữ liệu từ chuỗi JSON mẫu. Đọc dữ liệu mảng các đối tượng sản phẩm bao gồm: <code>productId</code>, <code>productName</code>, <code>category</code>, <code>price</code>, <code>quantity</code>, <code>isAvailable</code>. Nếu chuỗi JSON sai định dạng, catch lỗi và trả về mảng rỗng kèm thông báo.</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Chuỗi JSON <code>initialCatalog.json</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Mảng <code>products</code> chứa các Object sản phẩm</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Thêm Sản phẩm Mới]</b><br><code>addProduct()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Thêm sản phẩm vào mảng. Kiểm tra dữ liệu: <code>productId</code> không trùng, <code>productName</code> không được để trống, <code>price</code> > 0, <code>quantity</code> >= 0. Đẩy sản phẩm hợp lệ vào mảng bằng phương thức <code>.push()</code>.</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Đối tượng <code>newProduct</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">In ra thông báo thành công hoặc mã lỗi chi tiết</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Cập nhật Sản phẩm]</b><br><code>updateProduct()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tìm kiếm sản phẩm theo <code>productId</code>. Cập nhật các thông tin được phép thay đổi: <code>price</code>, <code>quantity</code>, <code>isAvailable</code>. Nếu không tìm thấy sản phẩm, báo lỗi <code>ERR_PRODUCT_NOT_FOUND</code>.</td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><code>productId</code>, Object <code>updateFields</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Cập nhật thuộc tính của Object trong mảng</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">4</td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Xóa Sản phẩm]</b><br><code>removeProduct()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Xác định chỉ số (index) của sản phẩm dựa trên <code>productId</code>. Sử dụng <code>.splice()</code> để loại bỏ sản phẩm khỏi mảng. Nếu sản phẩm có <code>quantity > 0</code>, đưa ra cảnh báo tồn kho trước khi xóa.</td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><code>productId</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Thông báo xóa thành công và kích thước mảng mới</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">5</td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Xuất Báo cáo Danh mục]</b><br><code>displayCatalogReport()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Duyệt qua danh sách sản phẩm bằng vòng lặp, định dạng dữ liệu từng hàng sử dụng Template Literals backticks. Tính toán tổng số lượng sản phẩm, tổng giá trị tồn kho (<code>price * quantity</code>), và đếm số lượng mặt hàng hết hàng.</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Mảng <code>products</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Bảng văn bản định dạng đẹp mắt trên Console</td>
    </tr>
  </tbody>
</table>

#### **Kịch bản Chạy Thử nghiệm (Mock Input / Output Case)**

*Ví dụ dữ liệu đầu vào chạy ứng dụng (`index.js`):*

```javascript
// Dữ liệu sản phẩm mới truyền vào ứng dụng
const sampleProduct = {
  productId: "PROD-004",
  productName: "Bàn phím cơ Không dây",
  category: "Linh kiện",
  price: 1250000,
  quantity: 15,
  isAvailable: true
};

// Gọi thao tác thêm sản phẩm
addProduct(sampleProduct);

// Gọi hiển thị báo cáo danh mục
displayCatalogReport();
```

*Ví dụ kết quả mong đợi hiển thị tại Console/Terminal:*

```text
[SUCCESS] Đã thêm thành công sản phẩm: PROD-004 - Bàn phím cơ Không dây

================================================================================
                    BÁO CÁO DANH MỤC SẢN PHẨM BÁN HÀNG
================================================================================
STT | Mã SP    | Tên Sản Phẩm              | Danh Mục   | Đơn Giá (VND) | Tồn Kho | Trạng Thái
--------------------------------------------------------------------------------
1   | PROD-001 | Chuột Không dây Gaming    | Phụ kiện   |   450,000     |    20   | Đang bán
2   | PROD-002 | Tai nghe Bluetooth Pro    | Âm thanh   | 1,200,000     |     0   | Hết hàng
3   | PROD-003 | Màn hình 27 inch 4K       | Hiển thị   | 8,900,000     |     5   | Đang bán
4   | PROD-004 | Bàn phím cơ Không dây     | Linh kiện  | 1,250,000     |    15   | Đang bán
--------------------------------------------------------------------------------
Tổng số lượng mặt hàng: 4
Tổng giá trị tồn kho: 98,000,000 VND
Số lượng mặt hàng hết hàng: 1
================================================================================
```

---

### **3. Yêu cầu nộp bài**
[NOTE] Học viên chuẩn bị mã nguồn và nộp bài theo đúng các bước quy định sau:
1. Tạo một Repository mới trên GitHub ở chế độ **Public** với tên: `sales-catalog-console`.
2. Commit toàn bộ mã nguồn bài làm lên nhánh `main` (hoặc `master`). Viết thông điệp commit (commit message) rõ ràng, thể hiện các bước phát triển chức năng.
3. Cập nhật file `README.md` giới thiệu dự án, mô tả cấu trúc dữ liệu và hướng dẫn câu lệnh thực thi file `node index.js`.
4. Nộp liên kết (URL) của GitHub Repository lên hệ thống quản lý học tập (LMS).
   *Dạng URL hợp lệ: `https://github.com/username/sales-catalog-console`*

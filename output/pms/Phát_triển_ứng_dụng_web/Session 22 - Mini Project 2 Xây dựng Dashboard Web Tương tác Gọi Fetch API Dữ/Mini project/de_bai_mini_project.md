## <center>[Mini project] Bảng điều khiển Quản lý & Phân tích Sản phẩm Dữ liệu Động (Dynamic Product Analytics Dashboard)</center>

[NOTE]: Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md).

### **1. Mục tiêu dự án**
- **Vận dụng Async/Await & Fetch API:** Thực hành kết nối, truyền nhận dữ liệu bất đồng bộ từ RESTful API (sử dụng DummyJSON API hoặc Mock REST API) bằng cú pháp `async/await` và hàm `fetch()`.
- **Thao tác DOM API Nâng cao:** Xây dựng giao diện Single Page Application (SPA) phản hồi nhanh, render danh sách sản phẩm động và cập nhật chỉ số báo cáo tổng quan (Metrics Dynamic Cards) mà không làm tải lại trang web.
- **Xử lý Dữ liệu Mảng ES6+:** Áp dụng các phương thức làm việc với mảng nâng cao như `map()`, `filter()`, `reduce()`, `sort()` để thực hiện phân lọc dữ liệu, tìm kiếm từ khóa và tính toán chỉ số thống kê kinh doanh.
- **Quản lý Trạng thái UI & Lỗi:** Thiết kế trạng thái tải dữ liệu (Loading Spinner / Skeleton), xử lý ngoại lệ kết nối mạng (Network Error / HTTP Status Errors) bằng khối `try...catch` và thông báo lỗi trực quan cho người dùng.
- **Tương tác Công cụ AI IDE:** Sử dụng Cursor AI IDE để hỗ trợ sinh mã giao diện HTML5/CSS3 chuẩn mực, kiểm thử các trường hợp dữ liệu biên và tối ưu hóa hiệu năng DOM Rendering.

---

### **2. Đề bài và Yêu cầu**

#### **A. Bối cảnh nghiệp vụ**
Doanh nghiệp bán lẻ trực tuyến cần một trang **Dynamic Product Analytics Dashboard** giúp bộ phận vận hành theo dõi trực quan danh mục sản phẩm, tính toán giá trị tồn kho, lọc sản phẩm theo ngành hàng và phân tích các chỉ số đánh giá trung bình. Toàn bộ dữ liệu sản phẩm được lấy động từ máy chủ API từ xa.

#### **B. Khung cấu trúc thư mục gợi ý (Project Skeleton)**
```text
dynamic-product-dashboard/
├── index.html
├── css/
│   └── styles.css
└── js/
    ├── api.js
    ├── utils.js
    └── app.js
```

#### **C. Cấu trúc Mô hình Dữ liệu Mock I/O mẫu**
- **Đầu vào (API Dynamic JSON Payload từ API Endpoint):**
```json
{
  "products": [
    {
      "id": 1,
      "title": "Essence Mascara Lash Princess",
      "category": "beauty",
      "price": 9.99,
      "rating": 4.94,
      "stock": 85,
      "brand": "Essence",
      "thumbnail": "https://cdn.dummyjson.com/products/images/beauty/Essence%20Mascara%20Lash%20Princess/thumbnail.png"
    },
    {
      "id": 2,
      "title": "Eyeshadow Palette with Mirror",
      "category": "beauty",
      "price": 19.99,
      "rating": 3.25,
      "stock": 0,
      "brand": "Glamour",
      "thumbnail": "https://cdn.dummyjson.com/products/images/beauty/Eyeshadow%20Palette%20with%20Mirror/thumbnail.png"
    }
  ]
}
```

- **Kết quả Xử lý Nghiệp vụ & Hiển thị UI:**
  - **Metrics Dashboard:** 
    - Tổng số lượng sản phẩm: `2`
    - Tổng giá trị tồn kho: `$849.15` (Tính bằng `85 * 9.99 + 0 * 19.99`)
    - Điểm đánh giá trung bình: `4.10` (Tính bằng `(4.94 + 3.25) / 2`)
    - Hàng hết tồn kho (Out of Stock): `1` sản phẩm
  - **Bảng dữ liệu / Lưới danh sách sản phẩm (DOM Render):** Hiển thị danh sách card gồm ảnh thumbnail, tên sản phẩm, danh mục, giá tiền, điểm đánh giá và badge trạng thái tồn kho ("Còn hàng" / "Hết hàng").

---

#### **D. Chi tiết Yêu cầu Chức năng (Requirements Breakdown)**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 25%;">Tên chức năng / Hàm</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 45%;">Mô tả Yêu cầu Kỹ thuật</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 30%;">Đầu ra Yêu cầu (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>Tải dữ liệu API bất đồng bộ</b><br>
        <code>fetchProducts()</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Sử dụng <code>async/await</code> gọi hàm <code>fetch()</code> tới Endpoint API (ví dụ: <code>https://dummyjson.com/products</code>). Bọc khối lệnh trong <code>try...catch</code> để kiểm soát HTTP Status Code và lỗi kết nối mạng.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Trả về mảng danh sách sản phẩm chuẩn hóa dữ liệu hoặc ném ngoại lệ nếu thất bại.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>Tính toán Chỉ số Tổng quan</b><br>
        <code>calculateMetrics()</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Duyệt qua mảng dữ liệu bằng <code>reduce()</code> hoặc <code>filter()</code> để tính toán: Tổng số sản phẩm, Tổng giá trị kho (<code>price * stock</code>), Đánh giá trung bình (<code>rating</code>), và Số lượng sản phẩm có <code>stock === 0</code>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Object chứa các chỉ số: <code>{ totalProducts, totalInventoryValue, averageRating, outOfStockCount }</code>.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>Hiển thị Dashboard UI</b><br>
        <code>renderMetrics()</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Cập nhật dữ liệu từ <code>calculateMetrics()</code> lên các thẻ KPI Metric Cards trên giao diện bằng <code>textContent</code>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Giao diện hiển thị các chỉ số được định dạng số thực chuẩn (VD: <code>$1,250.00</code>, <code>4.8 / 5</code>).
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>Render Danh sách Sản phẩm</b><br>
        <code>renderProductList()</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Tạo động các phần tử HTML (Product Cards/Table rows) bằng DOM API (<code>innerHTML</code> hoặc <code>document.createElement</code>) và gắn vào vùng hiển thị danh sách.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Hiển thị danh sách sản phẩm động với badge phân biệt "Còn hàng" (xanh) / "Hết hàng" (đỏ).
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>Bộ lọc & Tìm kiếm Tương tác</b><br>
        <code>filterProducts()</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Đăng ký sự kiện <code>input</code> trên ô tìm kiếm tên và sự kiện <code>change</code> trên dropdown chọn danh mục/sắp xếp giá. Sử dụng <code>filter()</code> và <code>sort()</code> để cập nhật danh sách.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Danh sách hiển thị lập tức lọc chính xác theo từ khóa và tiêu chí được chọn.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>Xem Chi tiết Sản phẩm</b><br>
        <code>showProductDetails()</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Đăng ký sự kiện <code>click</code> vào từng sản phẩm, truy xuất thông tin chi tiết bằng <code>find()</code> theo <code>productId</code> và hiển thị cửa sổ Modal popup.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Modal hiển thị đầy đủ thông số sản phẩm, thương hiệu, số lượng tồn chi tiết và nút đóng Modal.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>Quản lý Trạng thái UI & Lỗi</b><br>
        <code>showLoadingSpinner()</code><br><code>renderErrorMessage()</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Bật Spinner/Skeleton khi bắt đầu <code>fetch</code> và ẩn khi kết thúc. Hiển thị Banner cảnh báo màu đỏ kèm thông tin lỗi chi tiết nếu quá trình gọi API gặp lỗi.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Trải nghiệm người dùng mượt mà, không bị treo giao diện và thông báo lỗi rõ ràng.
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Yêu cầu nộp bài**
- **Đóng gói mã nguồn:** Tạo kho lưu trữ (Repository) công khai trên GitHub với tên theo định dạng: `javascript-session22-mini-project-2-[Ho-Va-Ten]`.
- **Cấu trúc lưu trữ:** Cam kết mã nguồn đẩy lên tuân thủ đúng cấu trúc cây thư mục đã mô tả ở phần 2.B.
- **Tệp tài liệu đính kèm:** Đính kèm tệp `README.md` tại thư mục gốc mô tả ngắn gọn:
  - Hướng dẫn khởi chạy ứng dụng (Mở `index.html` với Live Server).
  - Mô tả các Endpoint API đã sử dụng.
  - Ảnh chụp màn hình giao diện Dashboard khi tải thành công và khi gặp sự cố mạng (Network Error).
- **Đường link nộp bài:** Nộp đường link GitHub Repository trực tiếp lên hệ thống quản lý học tập (LMS).

---
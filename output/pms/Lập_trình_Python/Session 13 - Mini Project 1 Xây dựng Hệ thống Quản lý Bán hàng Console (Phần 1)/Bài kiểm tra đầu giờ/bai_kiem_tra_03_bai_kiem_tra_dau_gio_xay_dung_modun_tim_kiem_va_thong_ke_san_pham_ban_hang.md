## <center>BÀI KIỂM TRA ĐẦU GIỜ: XÂY DỰNG MÔ-ĐUN TÌM KIẾM VÀ THỐNG KÊ SẢN PHẨM BÁN HÀNG (ADVANCED SEARCH & ANALYTICS MODULE)</center>

### **1. Mục tiêu**
- Kiểm tra khả năng ứng dụng các kiểu dữ liệu nâng cao (`list`, `dict`, `tuple`, `set`) và hàm (Function) trong Python 3.12 để xử lý dữ liệu bán hàng.
- Đánh giá kỹ năng viết mã chuẩn **PEP 8**, khai báo **Type Hints** đầy đủ và xử lý ngoại lệ nguyên bản (**Native Exception Handling**).
- Rèn luyện tư duy thực hiện các bài toán tìm kiếm, lọc dữ liệu và thống kê số liệu kinh doanh trên ứng dụng Console CLI mà không sử dụng Lập trình hướng đối tượng (OOP) hay Database.

---

### **2. Yêu cầu**

Bạn được giao nhiệm vụ phát triển mô-đun tìm kiếm nâng cao và thống kê dữ liệu cho **Hệ thống Quản lý Bán hàng Console**. Dữ liệu sản phẩm được lưu trữ dưới dạng danh sách các Dictionary (`list[dict]`) với cấu trúc mẫu như sau:

```python
productList: list[dict] = [
    {
        "productId": "P01",
        "productName": "Laptop Dell XPS 13",
        "category": "Electronics",
        "price": 28000000.0,
        "stockQuantity": 15
    },
    {
        "productId": "P02",
        "productName": "Chuột Không Dây Logitech",
        "category": "Electronics",
        "price": 450000.0,
        "stockQuantity": 50
    },
    {
        "productId": "P03",
        "productName": "Áo Thun Nam Cotton",
        "category": "Fashion",
        "price": 250000.0,
        "stockQuantity": 100
    }
]
```

Sinh viên cần hoàn thành 3 hàm chức năng cốt lõi theo đúng đặc tả dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%;">Tên chức năng / Hàm</th>
      <th style="width: 25%;">Tham số đầu vào (Input)</th>
      <th style="width: 30%;">Luồng xử lý & Quy tắc</th>
      <th style="width: 20%;">Kết quả đầu ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Lọc sản phẩm theo danh mục & khoảng giá</b><br><code>filterProductsByCategoryAndPrice()</code></td>
      <td>
        <code>productList: list[dict]</code><br>
        <code>categoryName: str</code><br>
        <code>minPrice: float</code><br>
        <code>maxPrice: float</code>
      </td>
      <td>
        - Kiểm tra nếu <code>minPrice > maxPrice</code> hoặc <code>minPrice < 0</code>: Bắn lỗi <code>ValueError("Khoảng giá tìm kiếm không hợp lệ.")</code>.<br>
        - Lọc các sản phẩm thuộc danh mục <code>categoryName</code> (không phân biệt hoa thường) có mức giá nằm trong khoảng <code>[minPrice, maxPrice]</code>.
      </td>
      <td><code>list[dict]</code> danh sách sản phẩm thỏa mãn điều kiện lọc.</td>
    </tr>
    <tr>
      <td><b>Tìm kiếm sản phẩm theo từ khóa</b><br><code>searchProductsByName()</code></td>
      <td>
        <code>productList: list[dict]</code><br>
        <code>keyword: str</code>
      </td>
      <td>
        - Loại bỏ khoảng trắng thừa đầu/cuối của <code>keyword</code>.<br>
        - Nếu <code>keyword</code> rỗng sau khi loại bỏ khoảng trắng: Bắn lỗi <code>ValueError("Từ khóa tìm kiếm không được để trống.")</code>.<br>
        - Tìm kiếm tất cả sản phẩm có tên (<code>productName</code>) chứa <code>keyword</code> (không phân biệt chữ hoa/chữ thường).
      </td>
      <td><code>list[dict]</code> danh sách các sản phẩm khớp từ khóa.</td>
    </tr>
    <tr>
      <td><b>Thống kê tồn kho & giá trị theo danh mục</b><br><code>calculateCategoryAnalytics()</code></td>
      <td>
        <code>productList: list[dict]</code>
      </td>
      <td>
        - Duyệt qua toàn bộ danh sách sản phẩm.<br>
        - Gom nhóm theo từng danh mục (<code>category</code>) và tính toán:<br>
          + <code>totalStock</code>: Tổng số lượng tồn kho.<br>
          + <code>totalValue</code>: Tổng giá trị hàng tồn kho (bằng <code>price * stockQuantity</code>).
      </td>
      <td>
        <code>dict[str, dict]</code> dạng:<br>
        <code>{</code><br>
        &nbsp;&nbsp;<code>"Electronics": {"totalStock": 65, "totalValue": 442500000.0},</code><br>
        &nbsp;&nbsp;<code>"Fashion": {"totalStock": 100, "totalValue": 25000000.0}</code><br>
        <code>}</code>
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Điểm tối đa |
| :-: | :--- | :-: |
| 1 | Cài đặt chính xác 3 hàm xử lý theo đúng yêu cầu logic và có **Type Hints** chuẩn Python 3.12 | 6.0 điểm |
| 2 | Xử lý ngoại lệ nguyên bản (**Native Exception Handling**: `ValueError`, `TypeError`...) đúng quy tắc, không sử dụng envelope API | 2.0 điểm |
| 3 | Tuân thủ quy chuẩn đặt tên Tiếng Anh (camelCase cho biến/hàm, dict keys), chuẩn **PEP 8**, không dùng Class/OOP hay SQL | 2.0 điểm |
| **Tổng** | **Tổng điểm bài kiểm tra** | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**
- Tạo file mã nguồn Python theo tên: `sales_analytics.py`.
- Đảm bảo môi trường chạy trên Python 3.12 (đã kích hoạt `virtualenv`).
- Đẩy mã nguồn lên kho lưu trữ GitHub cá nhân và nộp đường dẫn (link repository) trước khi hết giờ làm bài.
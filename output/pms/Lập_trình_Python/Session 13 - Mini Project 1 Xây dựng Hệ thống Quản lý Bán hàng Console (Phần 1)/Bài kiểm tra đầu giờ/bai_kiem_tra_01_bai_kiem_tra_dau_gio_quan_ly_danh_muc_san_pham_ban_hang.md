## <center>Bài Kiểm Tra Đầu Giờ: Quản Lý Danh Mục Sản Phẩm Bán Hàng (Product Catalog Management)</center>

### **1. Mục tiêu**
- Đánh giá khả năng thao tác dữ liệu cấu trúc danh sách kết hợp với Dictionary (`list[dict[str, Any]]`) trong Python 3.12.
- Áp dụng đầy đủ Type Hints tiêu chuẩn và tuân thủ quy tắc đặt tên PEP 8 trên môi trường IDE Cursor / Windsurf.
- Thực hành kiểm soát logic nghiệp vụ và xử lý ngoại lệ nguyên bản (Native Exceptions) trong ứng dụng Console CLI mà không sử dụng Lập trình hướng đối tượng (OOP Class) hay Cơ sở dữ liệu SQL.

### **2. Yêu cầu**
Bạn được giao nhiệm vụ khởi tạo phân hệ quản lý danh mục sản phẩm cho hệ thống bán hàng trên giao diện dòng lệnh (Console CLI). Danh mục sản phẩm được lưu trữ dưới dạng một danh sách chứa các Dictionary với cấu trúc mỗi sản phẩm bao gồm các thuộc tính: `productId` (mã sản phẩm), `productName` (tên sản phẩm), `category` (danh mục), `unitPrice` (đơn giá), và `stockQuantity` (số lượng tồn kho).

Hãy viết mã nguồn Python 3.12 để triển khai các hàm theo bảng quy chuẩn dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">Tên chức năng / Hàm</th>
      <th style="padding: 8px; text-align: left;">Đầu vào (Parameters)</th>
      <th style="padding: 8px; text-align: left;">Quy tắc & Logic xử lý</th>
      <th style="padding: 8px; text-align: left;">Đầu ra (Return Value)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><b>[Thêm sản phẩm mới]</b><br><code>addProduct()</code></td>
      <td style="padding: 8px;">
        <code>catalog: list[dict[str, Any]]</code><br>
        <code>productId: str</code><br>
        <code>productName: str</code><br>
        <code>category: str</code><br>
        <code>unitPrice: float</code><br>
        <code>stockQuantity: int</code>
      </td>
      <td style="padding: 8px;">
        - Kiểm tra <code>productId</code> không được rỗng và không được trùng với sản phẩm đã có trong <code>catalog</code>.<br>
        - Đảm bảo <code>unitPrice > 0</code> và <code>stockQuantity >= 0</code>.<br>
        - Nếu vi phạm dữ liệu, nảy ra ngoại lệ <code>ValueError</code> kèm thông báo rõ ràng.<br>
        - Nếu hợp lệ, thêm sản phẩm mới dưới dạng Dictionary vào <code>catalog</code>.
      </td>
      <td style="padding: 8px;"><code>bool</code> (Trả về <code>True</code> khi thêm thành công)</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>[Tìm kiếm sản phẩm theo mã]</b><br><code>findProductById()</code></td>
      <td style="padding: 8px;">
        <code>catalog: list[dict[str, Any]]</code><br>
        <code>productId: str</code>
      </td>
      <td style="padding: 8px;">
        - Duyệt qua danh sách <code>catalog</code> để tìm sản phẩm có <code>productId</code> khớp chính xác với mã cần tìm.<br>
        - Không phân biệt hoa thường khi so sánh mã.
      </td>
      <td style="padding: 8px;"><code>dict[str, Any] | None</code> (Trả về Dictionary chứa sản phẩm hoặc <code>None</code> nếu không tìm thấy)</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>[Cập nhật số lượng tồn kho]</b><br><code>updateStockQuantity()</code></td>
      <td style="padding: 8px;">
        <code>catalog: list[dict[str, Any]]</code><br>
        <code>productId: str</code><br>
        <code>addedQuantity: int</code>
      </td>
      <td style="padding: 8px;">
        - Sử dụng <code>findProductById()</code> để tra cứu sản phẩm.<br>
        - Nếu không tìm thấy sản phẩm, nảy ra <code>KeyError</code>.<br>
        - Nếu số lượng tồn kho mới sau khi cộng <code>addedQuantity</code> nhỏ hơn 0, nảy ra <code>ValueError</code>.<br>
        - Cập nhật trực tiếp số lượng tồn kho vào sản phẩm.
      </td>
      <td style="padding: 8px;"><code>bool</code> (Trả về <code>True</code> khi cập nhật thành công)</td>
    </tr>
  </tbody>
</table>

*Lưu ý phạm vi:* Tuyệt đối **KHÔNG** sử dụng từ khóa `class` (OOP) và **KHÔNG** sử dụng thư viện kết nối Cơ sở dữ liệu SQL (như `sqlite3`). Chỉ sử dụng cấu trúc dữ liệu thuần (List, Dict, Tuple) và các hàm thủ tục.

---

### **3. Tiêu chí đánh giá**

- **Chức năng `addProduct()` (3.0 điểm):**
  - Xử lý kiểm tra trùng mã sản phẩm và validate đơn giá, tồn kho chính xác (1.5 điểm).
  - Thêm dữ liệu vào danh sách đúng cấu trúc Dictionary và nảy ngoại lệ `ValueError` khi vi phạm (1.5 điểm).

- **Chức năng `findProductById()` (2.0 điểm):**
  - Tìm kiếm chính xác, trả về đúng định dạng Dictionary hoặc `None` (2.0 điểm).

- **Chức năng `updateStockQuantity()` (2.5 điểm):**
  - Cập nhật chính số lượng tồn kho và tận dụng lại hàm `findProductById()` (1.0 điểm).
  - Xử lý ngoại lệ `KeyError` khi mã không tồn tại và `ValueError` khi tổng số lượng âm (1.5 điểm).

- **Chuẩn kỹ thuật & Chất lượng Mã nguồn (2.5 điểm):**
  - 100% tên biến, tên hàm, khóa của dictionary dùng tiếng Anh chuẩn camelCase (0.5 điểm).
  - Khai báo Type Hints đầy đủ theo chuẩn Python 3.12 (0.5 điểm).
  - Tuân thủ PEP 8 và không vi phạm Phạm vi Cấm (Không dùng Class / OOP, không dùng SQL) (1.5 điểm).

---

### **4. Yêu cầu nộp bài**
1. Khởi tạo môi trường ảo `virtualenv` trong thư mục dự án và kích hoạt trước khi lập trình trên Cursor / Windsurf IDE.
2. Viết toàn bộ mã nguồn vào tệp tin `product_management.py`. Tệp tin phải bao gồm khối kiểm thử `if __name__ == "__main__":` để chạy thử nghiệm các hàm trên Console CLI với các trường hợp dữ liệu hợp lệ và không hợp lệ (dùng khối `try-except`).
3. Commit mã nguồn và đẩy (push) lên repository GitHub cá nhân theo cú pháp commit: `feat(catalog): implement console product management functions`.
4. Dán đường dẫn URL repository GitHub vào hệ thống nộp bài.
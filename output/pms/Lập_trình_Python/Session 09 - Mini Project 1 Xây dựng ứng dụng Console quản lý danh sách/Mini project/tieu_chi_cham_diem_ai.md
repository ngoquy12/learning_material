### **Tiêu chí chấm điểm (AI)**
**Console Product Inventory Management System — Tổng điểm: 100 điểm**

---

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
* **Dữ liệu khởi tạo mặc định (10 điểm)**:
  * Khởi tạo thành công ít nhất 3 sản phẩm mẫu đúng cấu trúc (danh sách đa chiều hoặc các danh sách song song `product_ids`, `product_names`, `product_categories`, `product_prices`, `product_quantities`) ngay khi chương trình bắt đầu.
* **Vòng lặp menu điều khiển (10 điểm)**:
  * Xây dựng vòng lặp menu chính (`while True`) hiển thị rõ ràng 7 tùy chọn.
  * Tiếp nhận lựa chọn người dùng và điều hướng chính xác đến từng khối xử lý logic.

---

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
* **Hiển thị danh sách sản phẩm (5 điểm)**:
  * In danh sách dữ liệu kho dạng cột phẳng hàng ngay ngắn, tính đúng Thành tiền (`unit_price * quantity`) cho mỗi item.
* **Thêm sản phẩm mới (5 điểm)**:
  * Thêm thành công sản phẩm mới vào danh sách kho hàng. Kiểm tra và chặn trường hợp nhập trùng `product_id`.
* **Cập nhật thông tin sản phẩm (5 điểm)**:
  * Tìm đúng sản phẩm theo ID và cập nhật thành công đơn giá/số lượng. Giữ nguyên giá trị cũ nếu người dùng bỏ qua (bấm Enter).
* **Xóa sản phẩm (5 điểm)**:
  * Tìm và xóa chính xác phần tử tại chỉ số (index) tương ứng trong toàn bộ các danh sách lưu trữ sau khi xác nhận thành công.
* **Tìm kiếm & Lọc sản phẩm (5 điểm)**:
  * Tìm kiếm chính xác tên sản phẩm chứa từ khóa (không phân biệt hoa/thường) hoặc lọc chuẩn xác theo danh mục.
* **Thống kê kho hàng (5 điểm)**:
  * Tính toán chính xác Tổng giá trị kho hàng, tìm sản phẩm đắt nhất và lọc danh sách sản phẩm sắp hết hàng (tồn kho < 5).

---

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
* **Bắt lỗi ép kiểu dữ liệu đầu vào (15 điểm)**:
  * Sử dụng khối `try-except ValueError` tại tất cả các điểm nhận dữ liệu đầu vào là số (`int`, `float`) như Menu option, Product ID, Price, Quantity. Chương trình không bị ngắt đột ngột (crash) khi nhập chữ thay vì số.
* **Ràng buộc giá trị hợp lệ (15 điểm)**:
  * Đơn giá phải lớn hơn 0 (`unit_price > 0`).
  * Số lượng tồn kho phải lớn hơn hoặc bằng 0 (`quantity >= 0`).
  * Thông báo lỗi rõ ràng ra màn hình Console và cho phép người dùng thực hiện lại thao tác mà không bị thoát ứng dụng.

---

#### **4. Kịch bản kiểm thử thủ công và Chức năng nâng cao — 10 điểm**
* **Căn chỉnh định dạng Console (5 điểm)**:
  * Màn hình in ra được định dạng dạng bảng sử dụng F-string formatting (VD: `f"{id:<5} | {name:<20} | {price:>12,.0f}"`).
* **Trải nghiệm người dùng (UX Console) (5 điểm)**:
  * Có các thông báo phản hồi rõ ràng sau mỗi hành động (thêm thành công, xóa thành công, không tìm thấy ID sản phẩm). Khôi phục trạng thái menu mượt mà.

---

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **Quy chuẩn đặt tên (Clean Code) (5 điểm)**:
  * 100% tên biến sử dụng Tiếng Anh có nghĩa, tuân thủ nguyên tắc `snake_case` (VD: `product_ids`, `inventory_list`, `total_inventory_value`).
* **Tuân thủ Phạm vi cấm (Forbidden Scope) & Cấu trúc nộp bài (5 điểm)**:
  * Tuyệt đối **KHÔNG** sử dụng `dict`, `set`, `def`, `class`, `pytest`. Toàn bộ mã nguồn nằm gọn trong tệp `main.py`.
  * Nộp đúng đường dẫn GitHub Repository công khai có tệp `main.py` và `README.md`.

---

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
* **+5 điểm**: Thêm chức năng Sắp xếp danh sách kho hàng theo Đơn giá (Tăng dần / Giảm dần) hoặc theo Số lượng tồn kho mà chỉ dùng thuật toán sắp xếp trên danh sách (Bubble Sort / Selection Sort) hoặc hàm `sort()` bản địa mà không dùng Lambda/Custom Functions.
* **+5 điểm**: Hỗ trợ phân trang danh sách kho hàng (hiển thị 5 sản phẩm/trang) khi số lượng sản phẩm lớn.
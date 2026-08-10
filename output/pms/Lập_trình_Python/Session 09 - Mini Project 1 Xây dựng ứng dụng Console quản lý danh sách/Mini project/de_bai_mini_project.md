## <center>[Mini project] Xây dựng ứng dụng Console quản lý danh sách kho hàng bán lẻ (Retail Inventory Console App)</center>

### **1. Mục tiêu dự án**
Dự án Mini Project này giúp học viên củng cố và vận dụng tổng hợp các kiến thức nền tảng của ngôn ngữ Python (`python/core`) đã được học trong 9 buổi đầu tiên, tập trung vào mô hình ứng dụng Console CLI.

Sau khi hoàn thành dự án, học viên có khả năng:
* Cấu trúc và quản lý tập hợp dữ liệu động bằng danh sách (List) trong Python (sử dụng danh sách đa chiều List of Lists hoặc danh sách song song Parallel Lists).
* Thiết kế luồng điều khiển chương trình tương tác liên tục qua Menu Console bằng vòng lặp `while` và câu lệnh điều kiện `if-elif-else`.
* Thực hiện thành thạo các thao tác cơ bản trên danh sách: Thêm (Append), Hiển thị (Read/Traversal), Cập nhật (Update), Xóa (Delete/Pop/Remove), Tìm kiếm (Search) và Tính toán thống kê (Aggregation).
* Xử lý ngoại lệ chuẩn nét bằng `try-except` để khôi phục luồng chương trình khi người dùng nhập sai kiểu dữ liệu mà không làm sập ứng dụng CLI.
* Tuân thủ quy chuẩn đặt tên mã nguồn bằng Tiếng Anh (`snake_case`) và tư duy tổ chức mã sạch đẹp.

---

### **2. Đề bài và Yêu cầu**

Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md).

[WARNING] **GIỚI HẠN PHẠM VI KỸ THUẬT (FORBIDDEN SCOPE):**
* **CẤM TUYỆT ĐỐI**: Không sử dụng `Dictionary` (`{}`), không dùng `Set` (`set()`), không viết hàm tự định nghĩa (`def`), không tạo Lớp/Đối tượng OOP (`class`), không sử dụng thư viện kiểm thử như `pytest`.
* TOÀN BỘ chương trình được viết dưới dạng luồng kịch bản chính (Main Execution Script Body) điều khiển bằng vòng lặp `while True` và cấu trúc rẽ nhánh `if-elif-else`.

#### **Cấu trúc lưu trữ dữ liệu khuyến nghị:**
Mỗi mặt hàng trong kho sẽ bao gồm 5 thông tin cơ bản:
1. `item_id`: Mã sản phẩm (chuỗi, ví dụ: `"PROD001"`)
2. `item_name`: Tên sản phẩm (chuỗi, ví dụ: `"Sữa tươi tiệt trùng"`)
3. `category`: Danh mục hàng (chuỗi, ví dụ: `"Thực phẩm"`)
4. `quantity`: Số lượng tồn kho (số nguyên, ví dụ: `50`)
5. `unit_price`: Đơn giá (số thực float, ví dụ: `25000.0`)

Học viên lưu trữ danh sách mặt hàng bằng dạng Danh sách đa chiều `inventory_list = []` (trong đó mỗi phần tử là 1 danh sách con đại diện cho 1 sản phẩm: `[item_id, item_name, category, quantity, unit_price]`).

---

#### **Danh sách chức năng nghiệp vụ cần triển khai:**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 5%;">STT</th>
      <th style="width: 25%;">Tên chức năng</th>
      <th style="width: 45%;">Mô tả chi tiết nghiệp vụ</th>
      <th style="width: 25%;">Ràng buộc & Kiểm chuẩn dữ liệu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td><b>Xem danh sách mặt hàng</b><br><code>display_inventory_list</code></td>
      <td>Hiển thị toàn bộ các sản phẩm hiện có trong kho hàng dưới dạng bảng Console có định dạng cột ngay ngắn. Nếu danh sách rỗng, in thông báo cho người dùng.</td>
      <td>Cần căn chỉnh khoảng cách các cột (format string). Hiển thị rõ tổng số lượng mặt hàng hiện có.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td><b>Thêm mới mặt hàng vào kho</b><br><code>add_inventory_item</code></td>
      <td>Cho phép người dùng nhập đầy đủ 5 thông tin của mặt hàng mới và thêm vào danh sách kho hàng.</td>
      <td>
        - Mã sản phẩm không được trùng với mã đã tồn tại trong kho.<br>
        - Số lượng phải là số nguyên <code>int >= 0</code>.<br>
        - Đơn giá phải là số thực <code>float > 0</code>.<br>
        - Bắt ngoại lệ <code>ValueError</code> nếu nhập sai kiểu số.
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td><b>Cập nhật thông tin mặt hàng</b><br><code>update_inventory_item</code></td>
      <td>Nhập `item_id` cần chỉnh sửa. Nếu tìm thấy, cho phép nhập lại số lượng tồn kho mới và đơn giá mới.</td>
      <td>
        - Nếu `item_id` không tồn tại, thông báo lỗi.<br>
        - Kiểm tra tính hợp lệ của số lượng mới (<code>>= 0</code>) và đơn giá mới (<code>> 0</code>).
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">4</td>
      <td><b>Xóa mặt hàng khỏi kho</b><br><code>delete_inventory_item</code></td>
      <td>Nhập `item_id` cần xóa. Yêu cầu xác nhận (Y/N) trước khi thực hiện xóa khỏi danh sách.</td>
      <td>
        - Nếu `item_id` không tồn tại, báo lỗi tương ứng.<br>
        - Nếu chọn 'Y'/'y' thì thực hiện xóa, ngược lại hủy thao tác xóa.
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">5</td>
      <td><b>Tìm kiếm mặt hàng theo tên</b><br><code>search_inventory_item</code></td>
      <td>Nhập từ khóa tìm kiếm tên sản phẩm (không phân biệt hoa thường). In ra danh sách các sản phẩm khớp với từ khóa.</td>
      <td>Dùng phương thức chuỗi `.lower()` và toán tử `in` để tìm kiếm tương đối.</td>
    </tr>
    <tr>
      <td style="text-align: center;">6</td>
      <td><b>Thống kê tổng quan kho hàng</b><br><code>calculate_inventory_stats</code></td>
      <td>Tính và in ra màn hình các chỉ số thống kê:<br>- Tổng giá trị kho hàng (= sum of quantity * unit_price).<br>- Sản phẩm có giá trị cao nhất.<br>- Danh sách các mặt hàng có số lượng tồn kho sắp hết (quantity < 10).</td>
      <td>Xử lý chính xác khi danh sách rỗng (tránh lỗi tính toán trên danh sách trống).</td>
    </tr>
    <tr>
      <td style="text-align: center;">7</td>
      <td><b>Thoát chương trình</b><br><code>exit_console_app</code></td>
      <td>In lời chào tạm biệt và dừng vòng lặp thực thi chương trình Menu.</td>
      <td>Thoát ứng dụng an toàn.</td>
    </tr>
  </tbody>
</table>

---

### **3. Yêu cầu nộp bài**

1. **Hình thức nộp bài:**
   * Học viên khởi tạo một kho lưu trữ công khai (Public Repository) trên **GitHub**.
   * Đặt tên repository theo cú pháp: `python-core-mini-project-1-[ho_va_ten]`.
   * Commit và push mã nguồn lên nhánh chính (`main` hoặc `master`).
   * Nộp liên kết (URL) của GitHub Repository lên hệ thống học tập theo đúng thời hạn.

2. **Cấu trúc thư mục Repository bắt buộc:**
   ```text
   python-core-mini-project-1-[ho_va_ten]/
   ├── main.py              # File mã nguồn duy nhất chứa toàn bộ ứng dụng Console
   └── README.md            # File mô tả dự án, hướng dẫn chạy ứng dụng và danh sách thành viên/học viên
   ```

3. **Yêu cầu về Commit:**
   * Đảm bảo lịch sử commit phản ánh quá trình làm bài thực tế (tối thiểu 4-5 commit có ý nghĩa với thông điệp rõ ràng bằng tiếng Anh hoặc tiếng Việt có dấu).
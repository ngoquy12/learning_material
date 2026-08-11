## <center>[Mini project] HỆ THỐNG QUẢN LÝ KHO SẢN PHẨM CONSOLE (Console Product Inventory Management System)</center>

### **1. Mục tiêu dự án**

Dự án Mini Project 1 hướng tới việc củng cố tư duy lập trình căn bản, kỹ năng điều khiển luồng thực thi và quản lý dữ liệu trong bộ nhớ (In-memory Data Structure) sử dụng ngôn ngữ **Python 3.12**. Sau khi hoàn thành dự án này, học viên có khả năng:
* Cấu trúc và quản lý dữ liệu danh sách dạng 1D/2D (`List`) hoặc các danh sách song song (Parallel Lists) để lưu trữ thông tin đối tượng kho hàng.
* Làm chủ các vòng lặp (`while`, `for`) và cấu trúc rẽ nhánh (`if-elif-else`) trong việc xây dựng ứng dụng tương tác giao diện dòng lệnh (CLI).
* Áp dụng quy trình kiểm chuẩn dữ liệu đầu vào (Input Validation) và khôi phục lỗi runtime bằng cơ chế ngoại lệ bản địa (`try-except` với `ValueError`, `IndexError`...).
* Xây dựng báo cáo thống kê, tìm kiếm và lọc dữ liệu kho hàng theo kịch bản nghiệp vụ thực tế.

Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md).

**PHẠM VI CẤM DÙNG (FORBIDDEN SCOPE):**
Để đảm bảo mục tiêu đánh giá năng lực lập trình cốt lõi của Session 09, chương trình **TUYỆT ĐỐI CẤM** sử dụng các kiến thức thuộc phạm vi sau:
1. Không sử dụng Từ điển (`dict`) hoặc Tập hợp (`set`).
2. Không viết hàm tự định nghĩa (`def`) hoặc khai báo Lớp/Đối tượng (`class` - OOP).
3. Không sử dụng thư viện bên thứ ba hoặc thư viện kiểm thử tự động (`pytest`, `unittest`...).
4. Không sử dụng các khái niệm Web APIs (HTTP Status Codes, REST Envelope, DTO, Controller...).
Toàn bộ ứng dụng phải được viết theo mô hình lập trình tuần tự (Procedural Scripting) trên một tệp mã nguồn duy nhất (`main.py`).

---

### **2. Đề bài và Yêu cầu**

#### **2.1. Ngữ cảnh nghiệp vụ**
Doanh nghiệp thương mại bán lẻ cần một ứng dụng Console chạy trên thiết bị đầu cuối để nhân viên quản lý kho thực hiện các thao tác: kiểm kê hàng hóa, nhập sản phẩm mới, điều chỉnh đơn giá/số lượng tồn kho, xóa mã hàng lỗi thời, tìm kiếm sản phẩm và xuất báo cáo tổng quan kho hàng.

Dữ liệu sản phẩm trong kho được quản lý thông qua danh sách 2 chiều `inventory_list` (mỗi phần tử là một danh sách dạng `[product_id, product_name, category, unit_price, quantity]`) hoặc các danh sách song song:
* `product_ids`: Danh sách mã sản phẩm (Số nguyên `int`, Duy nhất).
* `product_names`: Danh sách tên sản phẩm (Chuỗi `str`).
* `product_categories`: Danh sách danh mục sản phẩm (Chuỗi `str`).
* `product_prices`: Danh sách đơn giá (Số thực `float`, > 0).
* `product_quantities`: Danh sách số lượng tồn kho (Số nguyên `int`, >= 0).

---

#### **2.2. Danh sách chức năng chi tiết**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #ddd; padding: 8px; text-align: center; width: 5%;">STT</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left; width: 25%;">Tên chức năng/Hàm</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left; width: 45%;">Mô tả chi tiết nghiệp vụ</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left; width: 25%;">Ràng buộc & Xử lý ngoại lệ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">1</td>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>[Hiển thị danh sách kho]</b><br><code>display_inventory</code></td>
      <td style="border: 1px solid #ddd; padding: 8px;">In toàn bộ danh sách sản phẩm dạng bảng có căn chỉnh cột đẹp mắt (ID, Tên, Danh mục, Đơn giá, Số lượng, Thành tiền = Đơn giá * Số lượng). Nếu kho rỗng, hiển thị thông báo phù hợp.</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Báo lỗi nếu danh sách trống. Căn chỉnh chuỗi chuẩn định dạng.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">2</td>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>[Thêm sản phẩm mới]</b><br><code>add_product</code></td>
      <td style="border: 1px solid #ddd; padding: 8px;">Yêu cầu người dùng nhập Mã sản phẩm, Tên, Danh mục, Đơn giá, Số lượng. Kiểm tra logic và thêm vào kho hàng nếu hợp lệ.</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Báo lỗi `ValueError` nếu nhập sai kiểu dữ liệu số. Kiểm tra trùng `product_id`. Đơn giá > 0, Số lượng >= 0.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">3</td>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>[Cập nhật sản phẩm]</b><br><code>update_product</code></td>
      <td style="border: 1px solid #ddd; padding: 8px;">Tìm kiếm sản phẩm theo `product_id`. Cho phép người dùng cập nhật Đơn giá mới và Số lượng tồn kho mới. Nếu nhấn Enter mà không nhập, giữ nguyên giá trị cũ.</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Thông báo lỗi nếu không tìm thấy `product_id`. Kiểm chuẩn giá trị số mới nhập vào.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">4</td>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>[Xóa sản phẩm]</b><br><code>delete_product</code></td>
      <td style="border: 1px solid #ddd; padding: 8px;">Tìm kiếm sản phẩm theo `product_id`. Hiển thị thông tin xác nhận (Y/N). Nếu chọn Y, tiến hành xóa sản phẩm khỏi các danh sách quản lý.</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Báo lỗi nếu không tìm thấy `product_id`. Yêu cầu nhập đúng ký tự xác nhận (`y`/`n`).</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">5</td>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>[Tìm kiếm & Lọc]</b><br><code>search_and_filter</code></td>
      <td style="border: 1px solid #ddd; padding: 8px;">Cho phép chọn: (1) Tìm theo tên sản phẩm (chứa từ khóa, không phân biệt hoa thường); (2) Lọc sản phẩm theo danh mục chính xác. Hiển thị kết quả dạng bảng.</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Xử lý trường hợp không tìm thấy kết quả phù hợp nào. Chuyển đổi chuỗi chữ thường (`lower()`).</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">6</td>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>[Thống kê báo cáo]</b><br><code>generate_analytics</code></td>
      <td style="border: 1px solid #ddd; padding: 8px;">Tính toán và in báo cáo: Tổng giá trị toàn bộ kho hàng, Sản phẩm có giá đắt nhất, Sản phẩm có số lượng tồn kho thấp nhất (dưới 5 units), Tổng số chủng loại mặt hàng.</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Xử lý an toàn khi kho trống. Sử dụng các hàm dựng sẵn `max()`, `min()`, `sum()` trên danh sách thích hợp.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">7</td>
      <td style="border: 1px solid #ddd; padding: 8px;"><b>[Thoát ứng dụng]</b><br><code>exit_application</code></td>
      <td style="border: 1px solid #ddd; padding: 8px;">Kết thúc vòng lặp ứng dụng menu, in lời cảm ơn và dừng chương trình an toàn.</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Bắt sự kiện thoát vòng lặp bằng `break`.</td>
    </tr>
  </tbody>
</table>

---

#### **2.3. Quy trình thực thi ứng dụng Menu Console**

Chương trình chính trong `main.py` phải duy trì một vòng lặp liên tục (`while True`) để hiển thị giao diện menu dạng sau:

```text
==================================================
   HỆ THỐNG QUẢN LÝ KHO SẢN PHẨM (PYTHON 3.12 CLI)
==================================================
1. Hiển thị danh sách kho hàng
2. Thêm sản phẩm mới vào kho
3. Cập nhật thông tin sản phẩm (Giá/Số lượng)
4. Xóa sản phẩm khỏi kho
5. Tìm kiếm & Lọc sản phẩm
6. Báo cáo thống kê kho hàng
7. Thoát chương trình
==================================================
Vui lòng chọn chức năng (1-7): 
```

**Dữ liệu khởi tạo mặc định (Initial Sample Data):**
Khi chương trình khởi chạy, ứng dụng phải chứa sẵn ít nhất **3 sản phẩm mẫu** để kiểm thử ngay mà không bắt buộc người dùng nhập từ đầu:
1. ID: `101` | Tên: `Laptop Dell XPS` | Danh mục: `Electronics` | Đơn giá: `25000000.0` | Số lượng: `8`
2. ID: `102` | Tên: `Mouse Logitech MX` | Danh mục: `Accessories` | Đơn giá: `1200000.0` | Số lượng: `25`
3. ID: `103` | Tên: `Keyboard Keychron K2` | Danh mục: `Accessories` | Đơn giá: `2100000.0` | Số lượng: `3`

---

### **3. Yêu cầu nộp bài**

1. **Cấu trúc lưu trữ mã nguồn**:
   Học viên khởi tạo Repository trên GitHub với cấu trúc chuẩn như sau:
   ```text
   console_inventory_management/
   ├── main.py
   └── README.md
   ```
   * `main.py`: Chứa toàn bộ mã nguồn chương trình (đảm bảo chạy thành công trên Python 3.12, tuân thủ Phạm vi cấm).
   * `README.md`: Hướng dẫn cách chạy chương trình và tóm tắt các chức năng cơ bản.

2. **Hình thức nộp bài**:
   * Nộp liên kết (URL) của GitHub Repository công khai lên hệ thống học tập.
   * Ví dụ định dạng link nộp bài: `https://github.com/username/console_inventory_management`.
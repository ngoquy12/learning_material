## <center>[Vận dụng nâng cao 2] Thiết kế Module Tính toán và Xuất Hóa đơn POS Phức hợp tại Highlands Coffee</center>

### **1. Mục tiêu**
*   **Vận dụng nâng cao kỹ năng xử lý dữ liệu CLI:** Nhập dữ liệu chuỗi/số, chuyển đổi kiểu dữ liệu chính xác (`str`, `int`, `float`), thực hiện chuỗi tính toán tài chính đa bước trong Python.
*   **Tư duy phân tích và thiết kế hệ thống:** Tự phân tích bảng tham số Đầu vào/Đầu ra (Input/Output), đề xuất thuật toán tính toán hóa đơn bán hàng và vẽ sơ đồ luồng dữ liệu (Flowchart) chuẩn kỹ thuật.
*   **Kỹ năng định dạng dữ liệu đầu ra chuyên nghiệp:** Thiết kế và xuất hóa đơn POS dạng văn bản (ASCII Receipt) căn chỉnh lề, sử dụng f-string nâng cao để hiển thị thông tin tài chính rõ ràng, minh bạch cho khách hàng.

---

### **2. Bối cảnh & Vấn đề**

Hệ thống Phần mềm Quản lý Bán hàng (Highlands POS) đang được nâng cấp module tính toán thanh toán tại quầy. Khi nhân viên order nhập các thông tin món uống, phụ thu size, topping, mã giảm giá thành viên và số tiền khách đưa, hệ thống cần tính toán chính xác tuyệt đối từng chi nhánh tài chính bao gồm: phụ thu, tổng tiền hàng, số tiền giảm giá, tiền thuế VAT, tổng tiền cần thanh toán và tiền thừa phải trả lại cho khách.

Bộ phận kỹ thuật yêu cầu xây dựng một module xử lý độc lập chạy trên giao diện dòng lệnh (CLI). Module này nhận toàn bộ tham số đầu vào của đơn hàng, thực hiện chuỗi công thức nghiệp vụ tài chính và in ra một hóa đơn bán hàng (POS Receipt) có cấu trúc đẹp mắt, căn chỉnh chuẩn xác để in ra máy in nhiệt tại quầy.---

### **3. Quy tắc nghiệp vụ**

Hệ thống tính toán hóa đơn áp dụng các quy tắc nghiệp vụ tài chính chuẩn như sau:

1. **Đơn giá 1 ly hoàn chỉnh (Unit Price):**
   `Unit Price = Base Price + Size Surcharge + (Topping Count * Topping Price)`
2. **Tổng tiền hàng trước giảm giá (Subtotal):**
   `Subtotal = Unit Price * Quantity`
3. **Số tiền giảm giá thành viên (Discount Amount):**
   `Discount Amount = Subtotal * Discount Rate`
4. **Tổng tiền sau giảm giá (Subtotal After Discount):**
   `Subtotal After Discount = Subtotal - Discount Amount`
5. **Tiền thuế giá trị gia tăng VAT (VAT Amount):**
   `VAT Amount = Subtotal After Discount * VAT Rate`
6. **Tổng tiền hóa đơn thanh toán (Final Total):**
   `Final Total = Subtotal After Discount + VAT Amount`
7. **Tiền thừa trả lại khách (Change Amount):**
   `Change Amount = Customer Cash - Final Total`

#### **Bảng tham số mô phỏng dữ liệu đơn hàng:**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: left;">Tên thông số nghiệp vụ</th>
      <th style="text-align: left;">Kiểu dữ liệu mong muốn</th>
      <th style="text-align: left;">Mô tả & Dữ liệu thử nghiệm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tên món uống (Item Name)</td>
      <td>Chuỗi ký tự (`str`)</td>
      <td>Trà Thạch Đào (Peach Jelly Tea)</td>
    </tr>
    <tr>
      <td>Giá gốc Size S (Base Price)</td>
      <td>Số thực (`float`)</td>
      <td>45000.0 (VNĐ)</td>
    </tr>
    <tr>
      <td>Phụ thu Size M/L (Size Surcharge)</td>
      <td>Số thực (`float`)</td>
      <td>10000.0 (VNĐ cho Size L)</td>
    </tr>
    <tr>
      <td>Số lượng Topping (Topping Count)</td>
      <td>Số nguyên (`int`)</td>
      <td>2 (phần topping)</td>
    </tr>
    <tr>
      <td>Đơn giá 1 Topping (Topping Price)</td>
      <td>Số thực (`float`)</td>
      <td>8000.0 (VNĐ/topping)</td>
    </tr>
    <tr>
      <td>Số lượng ly đặt (Quantity)</td>
      <td>Số nguyên (`int`)</td>
      <td>3 (ly)</td>
    </tr>
    <tr>
      <td>Tỷ lệ giảm giá Vàng (Discount Rate)</td>
      <td>Số thực (`float`)</td>
      <td>0.10 (tương đương giảm 10%)</td>
    </tr>
    <tr>
      <td>Tỷ lệ thuế VAT (VAT Rate)</td>
      <td>Số thực (`float`)</td>
      <td>0.08 (tương đương thuế 8%)</td>
    </tr>
    <tr>
      <td>Tiền khách đưa (Customer Cash)</td>
      <td>Số thực (`float`)</td>
      <td>300000.0 (VNĐ)</td>
    </tr>
  </tbody>
</table>

---

### **4. Yêu cầu bài toán**

Học viên thực hiện đầy đủ **2 phần nội dung bắt buộc** sau:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Analysis & Design Report)**
1. **Phân tích I/O (Input/Output Analysis):** 
   * Liệt kê danh sách tất cả các biến đầu vào và đầu ra. Khai báo rõ tên biến bằng tiếng Anh (ví dụ: `item_name`, `base_price`, `quantity`, `vat_rate`, `final_total`), kiểu dữ liệu Python tương ứng và vai trò nghiệp vụ.
2. **Thiết kế Thuật toán & Sơ đồ luồng (Flowchart Design):**
   * Trình bày các bước thực hiện thứ tự toán học để từ dữ liệu thô ra được kết quả tiền thừa trả khách.
   * Vẽ sơ đồ luồng dữ liệu (Flowchart) bằng cú pháp Mermaid. Sơ đồ phải tuân thủ nghiêm ngặt 5 dạng hình chuẩn kỹ thuật:
     * Hình ovan `([Bắt đầu])` / `([Kết thúc])` đại diện cho điểm đầu/cuối.
     * Hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]` cho thao tác Nhập/Xuất dữ liệu.
     * Hình chữ nhật `["Tính toán / Xử lý logic"]` cho các phép toán tài chính.
     * Hình thoi `Kiểm tra điều kiện?` cho các điểm rẽ nhánh.

#### **Phần 2: Cài đặt Mã nguồn & Định dạng Xuất Hóa đơn (Implementation & Formatting)**
1. Viết chương trình Python thuần (không dùng thư viện ngoài) thực thi qua CLI.
2. Thực hiện nhập đầy đủ các thông số từ bàn phím bằng hàm `input()`, ép kiểu dữ liệu đầu vào chính xác (`int`, `float`).
3. Thực hiện chuỗi phép toán theo đúng Quy tắc nghiệp vụ tài chính đã nêu tại Mục 3.
4. Xuất ra màn hình khung Hóa đơn Bán hàng (POS Receipt) được căn chỉnh cân đối bằng các kỹ thuật f-string (như căn lề trái/phải, kẻ đường phân cách `=`, `-`, định dạng số thực hiển thị 1 chữ số thập phân hoặc dạng số nguyên).

---

### **5. Yêu cầu nộp bài**

Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex8`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex8`
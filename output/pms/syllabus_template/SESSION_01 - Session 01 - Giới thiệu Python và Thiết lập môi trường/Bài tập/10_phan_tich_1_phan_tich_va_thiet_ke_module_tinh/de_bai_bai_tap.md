## <center>[Phân tích 1] Phân tích và Thiết kế Module Tính Tiền Hóa đơn POS Trà Sữa Highlands</center>

### **1. Mục tiêu**
*   **Phân tích nghiệp vụ & Kiểu dữ liệu**: Hiểu rõ luồng tính toán chi tiết một hóa đơn bán hàng tại quầy POS, phân tích đúng các kiểu dữ liệu đầu vào và áp dụng chính xác ép kiểu (Type Casting) trong Python (`str`, `int`, `float`).
*   **Tư duy Đa giải pháp (Trade-off Analysis)**: Đề xuất các phương án cấu trúc mã nguồn khác nhau (quản lý qua biến trung gian vs biểu thức tính toán gộp), phân tích ưu nhược điểm dựa trên các tiêu chí kỹ thuật.
*   **Thiết kế & Triển khai**: Vẽ lưu đồ thuật toán (Flowchart) chuẩn hóa và hiện thực hóa mã nguồn Python thực thi tính tiền, xử lý an toàn các phép toán tài chính cơ bản mà không gây lỗi logic hệ thống.

### **2. Vấn đề**
Tại các chi nhánh Highlands Coffee, hệ thống máy tính tiền quầy (POS) cần xử lý dữ liệu gọi món (Order) từ nhân viên thu ngân để tính toán hóa đơn chính xác. Mỗi đơn hàng bao gồm tên thức uống, đơn giá cơ bản (Size S), khoản phụ thu nâng size (Size M hoặc Size L), số lượng topping chọn thêm, số lượng ly và tỷ lệ chiết khấu thẻ thành viên (Membership Discount).

Thu ngân sẽ nhập các thông số này từ bàn phím thông qua giao diện dòng lệnh (CLI). Do dữ liệu nhận từ hàm `input()` trong Python mặc định luôn là kiểu chuỗi (`str`), nếu không phân tích và chuyển đổi kiểu dữ liệu một cách chặt chẽ, chương trình sẽ gặp lỗi phép toán (ví dụ: nhân chuỗi hoặc cộng chuỗi thay vì tính toán đại số) hoặc tính sai tiền hóa đơn của khách hàng.

Nhiệm vụ của bạn là phân tích bài toán, đề xuất các hướng kiến trúc xử lý mã nguồn, lựa chọn giải pháp tối ưu và triển khai chương trình Python tính toán chính xác hóa đơn bán hàng POS.### **3. Quy tắc nghiệp vụ**
1.  **Đơn giá cơ bản (`base_price`)**: Áp dụng cho Size S tiêu chuẩn (kiểu số nguyên `int`, đơn vị VNĐ).
2.  **Phụ thu Size (`size_upgrade_fee`)**: 
    *   Size S: `0` VNĐ.
    *   Size M: `6,000` VNĐ.
    *   Size L: `10,000` VNĐ.
    *(Giá trị phụ thu nâng size được thu ngân nhập trực tiếp tương ứng với size khách chọn).*
3.  **Phụ thu Topping (`topping_fee`)**:
    *   Mỗi loại topping thêm có đơn giá cố định `8,000` VNĐ/topping (`TOPPING_PRICE = 8000`).
    *   Tổng phí topping trên 1 ly = `num_toppings * 8000`.
4.  **Đơn giá 1 ly hoàn chỉnh (`unit_price`)**:
    `unit_price = base_price + size_upgrade_fee + (num_toppings * 8000)`
5.  **Tổng tiền hàng (`subtotal`)**:
    `subtotal = unit_price * quantity`
6.  **Tiền giảm giá thành viên (`discount_amount`)**:
    *   Thành viên Vàng (Gold Member) được giảm `10%` (`discount_rate = 0.10`). Khách thường `discount_rate = 0.0`.
    *   `discount_amount = subtotal * discount_rate`
7.  **Tổng tiền thanh toán (`final_amount`)**:
    `final_amount = subtotal - discount_amount`
    *(Giá trị cuối cùng được ép kiểu về số nguyên `int` để hiển thị đúng định dạng tiền tệ VNĐ).*

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Kỹ sư Phần mềm phụ trách module POS, thực hiện đầy đủ 3 phần sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Tự nghiên cứu, đề xuất ít nhất **2 giải pháp kỹ thuật khác nhau** để thực hiện tính toán và xuất hóa đơn POS (Ví dụ: Khác biệt về việc sử dụng các biến trung gian từng bước để minh bạch dữ liệu tài chính so với việc rút gọn biểu thức tính toán gộp trực tiếp trong lệnh `print`; hoặc khác biệt trong cách quản lý các hằng số nghiệp vụ).
*   Lập bảng so sánh Trade-off giữa các giải pháp dựa trên 5 tiêu chí bắt buộc theo mẫu HTML sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">Tiêu chí So sánh</th>
      <th style="padding: 8px; text-align: left;">Giải pháp 1 (Mô tả tên phương án)</th>
      <th style="padding: 8px; text-align: left;">Giải pháp 2 (Mô tả tên phương án)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><strong>Execution Speed (Tốc độ)</strong></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Memory Usage (Bộ nhớ)</strong></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Maintainability (Bảo trì)</strong></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Readability (Độ dễ đọc)</strong></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Suitability (Độ phù hợp)</strong></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Giải trình Lựa chọn và Thiết kế Lưu đồ Thuật toán (Flowchart)**
*   Đưa ra lý do chọn phương án tối ưu nhất dựa trên phân tích từ Phần 1 (đặc biệt trong bối cảnh phần mềm POS quầy cần độ chính xác cao và dễ bảo trì logic giá).
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) cho phương án tối ưu đã chọn.
    *   *Yêu cầu hình dạng Mermaid strictly:* 
        *   Bắt đầu/Kết thúc: Hình Oval `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
        *   Nhập/Xuất dữ liệu: Hình Parallelogram `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
        *   Xử lý/Tính toán: Hình Rectangle `["Thực hiện tính toán..."]`.

#### **Phần 3: Triển khai Mã nguồn Python & Xử lý Lỗi logic biên**
*   Hiện thực hóa mã nguồn bằng ngôn ngữ Python theo đúng kiến thức đã học (Session 01 - Biến, Kiểu dữ liệu, Nhập xuất `input`/`print`, Phép toán đại số, Ép kiểu `int`/`float`).
*   Tên biến đặt bằng tiếng Anh tiêu chuẩn (ví dụ: `drink_name`, `base_price`, `quantity`, `size_upgrade_fee`, `num_toppings`, `discount_rate`, `subtotal`, `final_amount`).
*   Chú thích mã nguồn bằng tiếng Việt có dấu mô tả logic chi tiết.
*   Xử lý an toàn các rủi ro biên: ép kiểu dữ liệu từ `input()` chính xác, không gây ra lỗi ghép chuỗi (string concatenation bug).

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex10`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex10`
## <center>[Vận dụng nâng cao 3] Tính toán Hóa đơn Bán hàng Tích hợp Chiết khấu và Thuế POS Highlands</center>

### **1. Mục tiêu**
*   **Kiến thức:** Vận dụng thành thạo kỹ thuật khai báo biến, chuyển đổi kiểu dữ liệu (`int`, `float`, `str`) và các toán tử số học cơ bản trong ngôn ngữ Python.
*   **Kỹ năng:** Phân tích yêu cầu nghiệp vụ thực tế của hệ thống POS điểm bán hàng, xác định tham số Input/Output, lập quy trình dòng chảy dữ liệu và triển khai chương trình CLI tính toán hóa đơn tài chính chính xác.
*   **Thái độ:** Rèn luyện tư duy lập trình chỉn chu, tính toán tỉ mỉ các chỉ số chiết khấu - thuế VAT, và trình bày hóa đơn bán hàng chuyên nghiệp theo tiêu chuẩn phần mềm doanh nghiệp.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống Quản lý Bán hàng Quán Cà phê / Trà sữa Highlands POS (`COFFEE_POS`), quy trình tính tiền tại quầy thu ngân đòi hỏi sự chính xác tuyệt đối khi xử lý các đơn hàng phức hợp. Mỗi đơn hàng bao gồm món nước chính (với đơn giá niêm yết theo Size S cơ bản), các khoản phụ thu nâng cấp dung tích (Size M, Size L), số lượng Topping gọi thêm, cùng các chính sách giảm giá dành cho khách hàng hội viên Vàng (Gold) và nghĩa vụ thuế giá trị gia tăng (VAT).

Bộ phận kỹ thuật POS cần phát triển một module dòng lệnh (CLI) giúp thu ngân nhập thông tin đơn hàng khách chọn và tự động tính toán tổng tiền, chiết khấu, thuế, tiền khách đưa và tiền thừa trả lại một cách chính xác.### **3. Quy tắc nghiệp vụ**
Hệ thống tính toán hóa đơn POS áp dụng các quy tắc tài chính và phụ thu chuẩn hóa sau:

1.  **Đơn giá và Nâng cấp Size:**
    *   Giá niêm yết ban đầu áp dụng cho Size S (`base_price`).
    *   Nâng cấp lên **Size M**: Phụ thu thêm **6.000 VNĐ/ly**.
    *   Nâng cấp lên **Size L**: Phụ thu thêm **10.000 VNĐ/ly**.
2.  **Topping kèm theo:**
    *   Mỗi phần Topping thêm (`topping_count`) tính đồng giá **8.000 VNĐ/phần**.
3.  **Chiết khấu & Thuế VAT:**
    *   Tổng tiền hàng gộp (`gross_subtotal`) = Tổng tiền nước cơ bản + Tổng phụ thu Size M + Tổng phụ thu Size L + Tổng phụ thu Topping.
    *   Tiền chiết khấu Hội viên Gold (`discount_amount`) = Tổng tiền hàng gộp $*$ (Tỷ lệ chiết khấu % / 100).
    *   Tiền trước thuế (`net_before_vat`) = Tổng tiền hàng gộp - Tiền chiết khấu.
    *   Tiền thuế VAT (`vat_amount`) = Tiền trước thuế $*$ (Tỷ lệ thuế VAT % / 100).
    *   Tổng thanh toán cuối cùng (`final_total`) = Tiền trước thuế + Tiền thuế VAT.
4.  **Thanh toán & Tiền thừa:**
    *   Tiền thừa trả lại khách (`change_due`) = Tiền khách đưa (`cash_given`) - Tổng thanh toán cuối cùng (`final_total`).
    *   Giá trị trung bình mỗi ly (`avg_price_per_cup`) = Tổng thanh toán cuối cùng / Tổng số lượng ly.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Hạng mục nghiệp vụ</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Giá trị / Tỷ lệ cố định</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Ghi chú áp dụng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">Phụ thu Size M</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">6.000 VNĐ / ly</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Cộng dồn trên số ly nâng Size M</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">Phụ thu Size L</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">10.000 VNĐ / ly</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Cộng dồn trên số ly nâng Size L</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">Đồng giá Topping</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">8.000 VNĐ / phần</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tính trên tổng số phần topping gọi thêm</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">Hội viên Vàng (Gold)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tỷ lệ nhập vào (ví dụ: 10%)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Trừ trực tiếp trước khi tính thuế VAT</td>
    </tr>
  </tbody>
</table>

### **4. Yêu cầu bài toán**

Học viên bắt buộc phải thực hiện đầy đủ **2 phần** sau:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Bắt buộc)**
1.  **Phân tích Input/Output:**
    *   Xác định rõ ràng tất cả dữ liệu đầu vào (tên món, giá cơ bản, số lượng ly, số ly size M, số ly size L, số topping, % giảm giá, % VAT, tiền khách đưa) và dữ liệu đầu ra cần in.
    *   Khai báo rõ kiểu dữ liệu tương ứng của từng biến (`int`, `float`, `str`).
2.  **Thiết kế sơ đồ quy trình tính toán:**
    *   Vẽ sơ đồ luồng dữ liệu (Sử dụng biểu đồ Mermaid) hoặc trình bày các bước toán học tuần tự thể hiện logic chuyển đổi dữ liệu và công thức tính tiền.

#### **Phần 2: Cài đặt Mã nguồn Python (Coding)**
*   Triển khai mã nguồn Python thực thi trên màn hình dòng lệnh (CLI).
*   Chương trình lần lượt nhập các dữ liệu đơn hàng từ bàn phím, thực hiện ép kiểu chính xác.
*   Tính toán toàn bộ các chỉ số tài chính theo đúng quy tắc nghiệp vụ.
*   In ra màn hình thông tin **Hóa đơn Bán hàng (PosReceipt)** chuyên nghiệp với các cột thông tin rõ ràng, minh bạch tiền hàng, giảm giá, VAT, tổng tiền và tiền thừa trả lại.

[REQUIREMENT] Mã nguồn phải đặt tên biến bằng tiếng Anh chuẩn ngành (`drink_name`, `base_price`, `total_qty`, `gross_subtotal`, `final_total`, v.v.), phần chú thích và thông điệp hiển thị cho người dùng bằng Tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex9`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex9`
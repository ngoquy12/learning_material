## <center>[Phân tích] Thiết kế Subsystem Xử lý & Tra cứu Đơn hàng E-Commerce Tương tác CLI</center>

### **1. Mục tiêu**
*   **Phân tích & Đánh giá Kiến trúc:** Nâng cao tư duy phân tích giải pháp kỹ thuật bằng cách so sánh hiệu năng, độ phức tạp và khả năng mở rộng giữa hai phương pháp tra cứu dữ liệu (Sequential Search vs. Direct Hash Key Mapping) trong hệ thống E-Commerce.
*   **Vận dụng Cấu trúc Lặp & Kiểu dữ liệu:** Áp dụng thành thạo vòng lặp `for` kết hợp với các cấu trúc dữ liệu `list` và `dict` tuân thủ phạm vi kiến thức Session 06.
*   **Tuân thủ Quy chuẩn Lập trình:** Thực hành chuẩn mã nguồn PEP 8, sử dụng Type Hints chuẩn Python 3.10+ và xử lý ngoại lệ nghiệp vụ minh bạch.

---

### **2. Bối cảnh & Vấn đề**
Sàn thương mại điện tử VietMart đang nâng cấp hệ thống máy POS tra cứu thông tin sản phẩm và tính toán giá trị hóa đơn cho nhân viên tư vấn khách hàng. Khi xử lý một giỏ hàng gồm nhiều mặt hàng và mã giảm giá (voucher), hệ thống phải thực hiện hiển thị bảng menu tương tác CLI để thực thi chuỗi thao tác: kiểm tra tồn kho sản phẩm, xác minh tính hợp lệ của mã giảm giá, áp dụng chiết khấu và tính tổng tiền thanh toán.

Đội ngũ kỹ thuật cần tìm ra phương án tối ưu nhất để hệ thống xử lý tra cứu nhanh chóng ngay cả khi danh mục hàng hóa (Catalog) mở rộng lên hàng trăm nghìn sản phẩm.



---

### **3. Quy tắc nghiệp vụ**
1.  **Dữ liệu Danh mục Sản phẩm (Catalog Data):**
    *   Mỗi sản phẩm gồm: `product_id` (chuỗi mã duy nhất), `name` (tên sản phẩm), `price` (đơn giá, số thực > 0), `stock` (số lượng tồn kho, số nguyên >= 0).

2.  **Dữ liệu Mã giảm giá (Voucher Data):**
    *   Mỗi voucher gồm: `voucher_code` (chuỗi mã duy nhất), `discount_rate` (tỉ lệ giảm giá từ 0.05 đến 0.30), `min_order_value` (giá trị đơn hàng tối thiểu áp dụng).

3.  **Tính toán Đơn hàng & Áp dụng Chiết khấu:**
    *   `Tổng tiền gốc` = Tổng (Số lượng mua * Đơn giá sản phẩm).
    *   Voucher chỉ hợp lệ khi: Có tồn tại trong hệ thống VÀ `Tổng tiền gốc` >= `min_order_value`.
    *   Nếu voucher hợp lệ: `Tiền giảm` = `Tổng tiền gốc` * `discount_rate`. Nếu không hợp lệ hoặc không có voucher: `Tiền giảm` = 0.
    *   `Tổng tiền thanh toán` = `Tổng tiền gốc` - `Tiền giảm`.

4.  **Ràng buộc Kỹ thuật Nghiêm ngặt:**
    *   [TUYỆT ĐỐI CẤM]: Không sử dụng vòng lặp `while`, không sử dụng các từ khóa điều khiển `break` và `continue`.
    *   Phải sử dụng cấu trúc lặp `for` để xử lý danh sách thao tác hoặc tập hợp dữ liệu.
    *   Toàn bộ hàm xử lý phải có Type Hints theo tiêu chuẩn Python 3.10+ (ví dụ: `int | float`, `list[dict[str, Any]]`).
    *   Bắt ngoại lệ dữ liệu không hợp lệ bằng các class lỗi native như `ValueError`, `KeyError`.

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Kỹ sư Phần mềm thực hiện phân tích và triển khai bài tập theo 3 phần bắt buộc:

#### **Phần 1: Báo cáo So sánh Trade-off (Đề xuất 2 Phương án)**
Hãy đề xuất và phân tích 2 phương án kỹ thuật cho bài toán tra cứu sản phẩm và voucher trong giỏ hàng:
*   **Phương án A (Sequential Search List):** Lưu trữ danh mục dưới dạng danh sách `list[dict]` và sử dụng vòng lặp `for` để duyệt tìm sản phẩm/voucher theo mã.
*   **Phương án B (Direct Hash/Key Mapping Dict):** Chuyển đổi danh mục sang dạng từ điển `dict[str, dict]` lấy mã làm khóa (key) để truy cập trực tiếp kết hợp vòng lặp `for` duyệt giỏ hàng.

Yêu cầu lập bảng so sánh Trade-off theo mẫu HTML bên dưới (đảm bảo thuộc tính CSS bắt buộc):

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr>
      <th style="padding: 8px; text-align: left;">Tiêu chí So sánh</th>
      <th style="padding: 8px; text-align: left;">Phương án A (Sequential List Search)</th>
      <th style="padding: 8px; text-align: left;">Phương án B (Direct Dict Key Mapping)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;">Độ phức tạp thời gian (Time Complexity)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Tiêu tốn bộ nhớ (Memory Consumption)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Tính dễ đọc &amp; Bảo trì (Readability &amp; Maintainability)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Khả năng mở rộng quy mô (Scalability)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Ngữ cảnh áp dụng phù hợp (Suitability)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Mã giả (Pseudocode)**
1.  Đưa ra lập luận kỹ thuật rõ ràng để chọn ra phương án tối ưu cho hệ thống E-Commerce quy mô lớn.
2.  Viết mã giả (Pseudocode) hoặc mô tả lưu đồ thuật toán cho luồng xử lý đơn hàng tương tác CLI của phương án đã chọn. Mã giả phải thể hiện cách xử lý lặp menu/danh sách mà không dùng `while`, `break`, `continue`.

#### **Phần 3: Triển khai Mã nguồn Python (Implementation)**
Triển khai chương trình Python hoàn chỉnh thực hiện giải pháp tối ưu đã chọn:
*   Định nghĩa các hàm có Type Hints đầy đủ.
*   Thiết kế giao diện Console tương tác duyệt qua danh sách các lệnh thực thi (Menu Actions) hiển thị thông tin sản phẩm, áp mã voucher, tính tổng tiền hóa đơn và in ra kết quả.
*   Xử lý chặn các lỗi biên: mã sản phẩm không tồn tại, số lượng vượt tồn kho, voucher không hợp lệ hoặc chưa đủ điều kiện chiết khấu.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex04`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex04`
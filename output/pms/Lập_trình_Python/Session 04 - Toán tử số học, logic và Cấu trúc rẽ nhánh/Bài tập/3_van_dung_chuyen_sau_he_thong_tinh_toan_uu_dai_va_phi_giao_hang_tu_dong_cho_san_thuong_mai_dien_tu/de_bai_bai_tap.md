## <center>[Vận dụng chuyên sâu] Hệ thống tính toán ưu đãi và phí giao hàng tự động cho sàn Thương mại điện tử</center>

### **1. Mục tiêu**
*   **Kiến thức:** Nắm vững và vận dụng chuyên sâu cấu trúc rẽ nhánh (`if-elif-else`), các toán tử số học (`+`, `-`, `*`, `/`) và toán tử logic (`and`, `or`, `not`) trong bài toán thực tế.
*   **Kỹ năng chuẩn hóa PEP 8:** Thực hành kỹ thuật "phẳng hóa" điều kiện (Flattening Conditionals), loại bỏ Anti-pattern lồng nhau quá sâu (Arrow Anti-Pattern) để nâng cao tính bảo trì và đọc hiểu mã nguồn.
*   **Tư duy thiết kế nghiệp vụ:** Phân tích, xây dựng sơ đồ xử lý dữ liệu và thiết kế quy trình kiểm định điều kiện kinh doanh cho hệ thống Thương mại điện tử (E-Commerce).
*   **Chuẩn mực mã nguồn:** Áp dụng định danh tiếng Anh, chú thích Tiếng Việt có dấu, bổ sung Type Hinting theo đúng chuẩn PEP 8 cho ngôn ngữ Python.

### **2. Bối cảnh & Vấn đề**
Hệ thống xử lý thanh toán của sàn thương mại điện tử E-Commerce đang gặp tình trạng mã nguồn bị "rác" nghiêm trọng do đội ngũ cũ viết các câu lệnh `if` lồng nhau tới 5-6 cấp để tính toán chiết khấu và phí giao hàng. Điều này dẫn tới việc phát sinh lỗi ẩn khi tính tiền, cực kỳ khó đọc và vi phạm nghiêm trọng quy chuẩn lập trình PEP 8.

Ban công nghệ yêu cầu bạn xây dựng lại module tính toán hóa đơn tự động. Module mới phải xử lý toàn bộ logic tính tiền, giảm giá theo hạng hội viên, áp dụng mã voucher, tính phí giao hàng và phụ phí thanh toán. Đặc biệt, mã nguồn bắt buộc phải được "phẳng hóa" bằng toán tử logic, sử dụng Guard Clauses để chặn dữ liệu không hợp lệ ngay từ đầu.



### **3. Quy tắc nghiệp vụ**

Hệ thống tính toán chi phí hóa đơn dựa trên các thông số đầu vào:
*   `subtotal` (float): Tổng giá trị hàng hóa gốc (VNĐ).
*   `distance_km` (float): Khoảng cách giao hàng (km).
*   `membership_tier` (str): Hạng hội viên (`"BRONZE"`, `"SILVER"`, `"GOLD"`, `"DIAMOND"`).
*   `voucher_code` (str): Mã giảm giá nhập vào (`"SUMMER2025"`, `"FREESHIP"`, hoặc chuỗi rỗng `""`).
*   `payment_method` (str): Phương thức thanh toán (`"COD"`, `"E_WALLET"`, `"CREDIT_CARD"`).

Các quy tắc tính toán và kiểm tra dữ liệu được chi tiết trong bảng sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%;">Hạng mục nghiệp vụ</th>
      <th style="width: 75%;">Quy tắc áp dụng & Điều kiện xử lý</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Kiểm tra hợp lệ (Guard Clauses)</strong></td>
      <td>
        - Nếu <code>subtotal <= 0</code> hoặc <code>distance_km <= 0</code>: Báo lỗi dữ liệu không hợp lệ.<br>
        - Nếu <code>membership_tier</code> không nằm trong 4 hạng quy định: Báo lỗi hạng hội viên không tồn tại.<br>
        - Nếu <code>payment_method</code> không nằm trong 3 phương thức quy định: Báo lỗi phương thức thanh toán không hỗ trợ.
      </td>
    </tr>
    <tr>
      <td><strong>2. Chiết khấu Hạng hội viên (Tier Discount)</strong></td>
      <td>
        - Hạng <code>DIAMOND</code>: Giảm 15% nếu <code>subtotal >= 2.000.000</code>; ngược lại giảm 10%.<br>
        - Hạng <code>GOLD</code>: Giảm 10% nếu <code>subtotal >= 1.000.000</code>; ngược lại giảm 5%.<br>
        - Hạng <code>SILVER</code>: Giảm 5% nếu <code>subtotal >= 500.000</code>; ngược lại giảm 2%.<br>
        - Hạng <code>BRONZE</code>: Chiết khấu 0%.
      </td>
    </tr>
    <tr>
      <td><strong>3. Ưu đãi Mã giảm giá (Voucher)</strong></td>
      <td>
        - Mã <code>SUMMER2025</code>: Giảm thêm 50.000 VNĐ nếu tổng tiền sau khi giảm hạng hội viên <code>>= 500.000</code> VNĐ.<br>
        - Mã <code>FREESHIP</code>: Miễn phí giao hàng (Phí giao hàng = 0 VNĐ) nếu <code>subtotal</code> gốc <code>>= 300.000</code> VNĐ.<br>
        - Các mã khác hoặc không thỏa điều kiện: Giảm 0 VNĐ cho voucher.
      </td>
    </tr>
    <tr>
      <td><strong>4. Phí giao hàng (Shipping Fee)</strong></td>
      <td>
        - Khoảng cách <code>distance_km <= 5</code>: Phí gốc 15.000 VNĐ.<br>
        - Khoảng cách <code>5 < distance_km <= 20</code>: Phí gốc 30.000 VNĐ.<br>
        - Khoảng cách <code>distance_km > 20</code>: Phí gốc 50.000 VNĐ.<br>
        - <em>Miễn phí giao hàng (Phí = 0 VNĐ)</em> nếu tiền sau giảm hạng hội viên <code>>= 1.500.000</code> VNĐ HOẶC áp dụng thành công mã <code>FREESHIP</code>.
      </td>
    </tr>
    <tr>
      <td><strong>5. Phụ phí & Ưu đãi Thanh toán</strong></td>
      <td>
        - Thanh toán <code>COD</code>: Cộng thêm phụ phí 10.000 VNĐ nếu <code>subtotal</code> gốc <code>< 200.000</code> VNĐ.<br>
        - Thanh toán <code>E_WALLET</code>: Giảm thêm 2% trên tổng số tiền cần trả hiện tại nếu <code>subtotal</code> gốc <code>>= 300.000</code> VNĐ.<br>
        - Thanh toán <code>CREDIT_CARD</code>: Không phụ phí, không chiết khấu thêm.
      </td>
    </tr>
  </tbody>
</table>

### **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Thiết kế giải pháp (Báo cáo)**
1. Lập sơ đồ tư duy hoặc giải thuật (Pseudocode/Flowchart) thể hiện luồng kiểm tra dữ liệu và tính toán hóa đơn.
2. Phân tích chi tiết phương pháp loại bỏ các câu lệnh `if` lồng nhau (Arrow Anti-Pattern) thành cấu trúc điều kiện phẳng sử dụng toán tử `and`, `or` và kỹ thuật trả về sớm (Guard Clauses).

#### **Phần 2: Cài đặt chương trình Python**
Thực hiện viết mã nguồn Python hoàn chỉnh từ đầu để xử lý bài toán trên. Chương trình cần:
1. Nhận đầy đủ 5 thông số đầu vào của đơn hàng.
2. Tiến hành kiểm tra và tính toán giá trị cuối cùng bao gồm các thành phần:
   *   Giá trị chiết khấu hội viên.
   *   Giá trị giảm giá voucher.
   *   Phí giao hàng thực tế.
   *   Phụ phí / Giảm giá thanh toán.
   *   Tổng số tiền thanh toán cuối cùng (Final Payable Amount).
3. Tuân thủ 100% quy chuẩn mã nguồn PEP 8 (Thụt lề 4 space, tên biến/hàm `snake_case`, bổ sung Type Hinting).

[NOTE] **Ví dụ dữ liệu mô phỏng để kiểm thử chương trình:**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th>Mã Kịch Bản</th>
      <th>Dữ liệu đầu vào (Input Payload)</th>
      <th>Kết quả kỳ vọng (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>TestCase_01</strong></td>
      <td>
        subtotal = 1.200.000<br>
        distance_km = 8.5<br>
        membership_tier = "GOLD"<br>
        voucher_code = "SUMMER2025"<br>
        payment_method = "E_WALLET"
      </td>
      <td>
        - Chiết khấu hội viên: 120.000 VNĐ (10%)<br>
        - Tiền sau giảm hạng: 1.080.000 VNĐ<br>
        - Giảm giá Voucher: 50.000 VNĐ<br>
        - Phí giao hàng: 30.000 VNĐ<br>
        - Giảm giá E-Wallet (2%): 21.200 VNĐ<br>
        - <strong>Tổng thanh toán: 1.038.800 VNĐ</strong>
      </td>
    </tr>
    <tr>
      <td><strong>TestCase_02</strong></td>
      <td>
        subtotal = 2.500.000<br>
        distance_km = 12.0<br>
        membership_tier = "DIAMOND"<br>
        voucher_code = "FREESHIP"<br>
        payment_method = "CREDIT_CARD"
      </td>
      <td>
        - Chiết khấu hội viên: 375.000 VNĐ (15%)<br>
        - Tiền sau giảm hạng: 2.125.000 VNĐ<br>
        - Giảm giá Voucher: 0 VNĐ<br>
        - Phí giao hàng: 0 VNĐ (Miễn phí do tiền > 1.5M)<br>
        - Phụ phí/Ưu đãi thanh toán: 0 VNĐ<br>
        - <strong>Tổng thanh toán: 2.125.000 VNĐ</strong>
      </td>
    </tr>
    <tr>
      <td><strong>TestCase_03</strong></td>
      <td>
        subtotal = -50.000<br>
        distance_km = 3.0<br>
        membership_tier = "BRONZE"<br>
        voucher_code = ""<br>
        payment_method = "COD"
      </td>
      <td>
        - Trả về thông điệp lỗi: "Lỗi: Giá trị đơn hàng và khoảng cách phải lớn hơn 0."
      </td>
    </tr>
  </tbody>
</table>

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex03`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex03`
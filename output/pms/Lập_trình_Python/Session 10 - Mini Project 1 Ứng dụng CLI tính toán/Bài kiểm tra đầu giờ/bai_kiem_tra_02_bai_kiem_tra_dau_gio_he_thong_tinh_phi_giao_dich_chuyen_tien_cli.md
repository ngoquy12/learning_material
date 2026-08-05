## <center>Bài Kiểm Tra Đầu Giờ: Hệ Thống Tính Phí Giao Dịch Chuyển Tiền CLI (Quick Money Transfer Billing CLI)</center>

### **1. Mục tiêu**
* Đánh giá kỹ năng vận dụng các kiến thức cốt lõi: cấu trúc điều kiện (`if-elif-else`), vòng lặp (`while`), xử lý ngoại lệ đầu vào (`try-except`) và định dạng chuỗi trong Python.
* Xây dựng luồng tính toán phí giao dịch tài chính cho ứng dụng Console CLI tuân thủ chính xác logic nghiệp vụ.
* Đảm bảo mã nguồn tuân thủ nghiêm ngặt quy chuẩn đặt tên biến bằng Tiếng Anh (`snake_case`) và không sử dụng các kiến thức thuộc phạm vi cấm.

---

### **2. Yêu cầu**

Xây dựng một chương trình Console CLI cho phép người dùng nhập thông tin một giao dịch chuyển tiền, kiểm tra tính hợp lệ của dữ liệu đầu vào, tính toán phí giao dịch dựa trên loại tài khoản và phương thức chuyển tiền, sau đó hiển thị hóa đơn thanh toán chi tiết.

**LƯU Ý QUAN TRỌNG:**
* **PHẠM VI CẤM:** KHÔNG được sử dụng Hàm (`def`), Danh sách (`list`), Hướng đối tượng (`OOP`), hoặc Tập tin (`file`). Tất cả xử lý được viết dưới dạng luồng mã tuyến tính trong tập tin chính.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 25%;">Tên chức năng/Thành phần</th>
      <th style="width: 20%;">Đầu vào / Tham số</th>
      <th style="width: 35%;">Logic xử lý & Quy tắc</th>
      <th style="width: 20%;">Đầu ra / Giá trị kỳ vọng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>[Nhập và kiểm tra dữ liệu giao dịch]</b><br><code>input_transaction_data</code></td>
      <td>
        <code>transfer_amount</code><br>
        <code>account_type</code><br>
        <code>is_express</code>
      </td>
      <td>
        - Sử dụng vòng lặp <code>while</code> và <code>try-except</code> để yêu cầu người dùng nhập:<br>
        1. <code>transfer_amount</code>: Số tiền chuyển (kiểu <code>float</code>). Bắt lỗi <code>ValueError</code> nếu nhập chữ hoặc số tiền &le; 0. Hiển thị thông báo và yêu cầu nhập lại.<br>
        2. <code>account_type</code>: Loại tài khoản, chỉ chấp nhận <code>"standard"</code> hoặc <code>"vip"</code> (không phân biệt hoa/thường).<br>
        3. <code>is_express</code>: Có chọn chuyển hỏa tốc không, chỉ chấp nhận <code>"yes"</code> hoặc <code>"no"</code> (không phân biệt hoa/thường).
      </td>
      <td>Các biến <code>transfer_amount</code>, <code>account_type</code>, <code>is_express</code> mang giá trị hợp lệ.</td>
    </tr>
    <tr>
      <td><b>[Tính toán phí giao dịch và ưu đãi]</b><br><code>calculate_transfer_fee</code></td>
      <td>
        <code>transfer_amount</code><br>
        <code>account_type</code><br>
        <code>is_express</code>
      </td>
      <td>
        - Phí gốc (<code>base_fee</code>):<br>
        + Nếu <code>transfer_amount</code> &lt; 10,000,000 VNĐ: Phí gốc = 1.0% số tiền chuyển.<br>
        + Nếu <code>transfer_amount</code> &ge; 10,000,000 VNĐ: Phí gốc = 0.8% số tiền chuyển.<br>
        - Mức giảm giá tài khoản (<code>discount_amount</code>):<br>
        + Nếu <code>account_type == "vip"</code>: Giảm 50% trên <code>base_fee</code>.<br>
        + Nếu <code>account_type == "standard"</code>: Giảm 0%.<br>
        - Phụ phí hỏa tốc (<code>express_surcharge</code>):<br>
        + Nếu <code>is_express == "yes"</code>: Phụ phí = 10,000 VNĐ.<br>
        + Ngược lại: Phụ phí = 0 VNĐ.<br>
        - Phí thực tế (<code>final_fee</code>) = <code>base_fee</code> - <code>discount_amount</code> + <code>express_surcharge</code>.<br>
        - Tổng thanh toán (<code>total_payment</code>) = <code>transfer_amount</code> + <code>final_fee</code>.
      </td>
      <td>Các biến kết quả: <code>base_fee</code>, <code>discount_amount</code>, <code>express_surcharge</code>, <code>final_fee</code>, <code>total_payment</code>.</td>
    </tr>
    <tr>
      <td><b>[Hiển thị hóa đơn giao dịch]</b><br><code>display_transaction_receipt</code></td>
      <td>
        <code>transfer_amount</code><br>
        <code>account_type</code><br>
        <code>is_express</code><br>
        <code>base_fee</code><br>
        <code>discount_amount</code><br>
        <code>express_surcharge</code><br>
        <code>final_fee</code><br>
        <code>total_payment</code>
      </td>
      <td>
        - Định dạng các số tiền dạng số thực ra màn hình Console rõ ràng.<br>
        - Hiển thị giao diện chi tiết hóa đơn bao gồm:<br>
        + Số tiền chuyển gốc.<br>
        + Phí dịch vụ ban đầu.<br>
        + Số tiền được giảm giá (nếu có).<br>
        + Phụ phí chuyển hỏa tốc (nếu có).<br>
        + Phí dịch vụ thực tế phải trả.<br>
        + Tổng số tiền trừ khỏi tài khoản người dùng.
      </td>
      <td>In ra màn hình giao diện Console hóa đơn thanh toán giao dịch hoàn chỉnh.</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

* **Kiểm soát dữ liệu đầu vào (3.0 điểm):** Xử lý ngoại lệ `try-except` chính xác cho kiểu số, dùng vòng lặp `while` bắt buộc nhập đúng loại tài khoản và lựa chọn chuyển hỏa tốc.
* **Tính toán luồng nghiệp vụ (3.5 điểm):** Tính đúng phí gốc, giảm giá cho tài khoản VIP, phụ phí chuyển hỏa tốc và tổng tiền thanh toán.
* **Hiển thị hóa đơn Console (2.5 điểm):** Trình bày hóa đơn mạch lạc, rõ ràng, định dạng đúng các thông số.
* **Quy chuẩn mã nguồn (1.0 điểm):** Tên biến 100% tiếng Anh chuẩn `snake_case`, mã nguồn sạch đẹp, không vi phạm phạm vi cấm (List, Hàm, OOP, File).

---

### **4. Yêu cầu nộp bài**

* Viết toàn bộ mã nguồn xử lý vào tập tin `main.py`.
* Thực hiện commit mã nguồn lên tài khoản GitHub cá nhân với thông điệp ghi chú rõ ràng (`Git commit message`).
* Nộp liên kết (URL) của GitHub repository lên hệ thống trước khi hết thời gian quy định (15-20 phút).
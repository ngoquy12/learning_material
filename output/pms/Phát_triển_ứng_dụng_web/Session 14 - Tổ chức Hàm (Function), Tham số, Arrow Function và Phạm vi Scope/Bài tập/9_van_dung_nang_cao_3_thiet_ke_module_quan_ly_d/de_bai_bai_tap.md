# <center>[Vận dụng nâng cao 3] Thiết kế Module Quản lý Đặt vé và Hạn ngạch Sự kiện bằng Closure & Arrow Function</center>

### **1. Mục tiêu**
*   Vận dụng sáng tạo các kiến thức về **Arrow Function**, **Tham số mặc định (Default Parameters)**, **Lexical Scope** và **Closure** trong JavaScript ES6+ để thiết kế module đóng gói trạng thái giao dịch bán vé.
*   Tự phân tích luồng dữ liệu, xác định kiểu dữ liệu đầu vào/đầu ra và xây dựng hệ thống quản lý hạn ngạch mua vé (tối đa 4 vé/tài khoản cho 1 sự kiện), tính toán tiền chiết khấu đợt vé mở bán sớm (Early Bird) và phí phát hành.
*   Đảm bảo nguyên lý đóng gói dữ liệu (Encapsulation), bảo vệ biến cục bộ trong bộ nhớ RAM, tránh hoàn toàn rủi ro ghi đè biến toàn cục (Global Variable Mutation).

---

### **2. Bối cảnh & Vấn đề**
Ban tổ chức đại nhạc hội ca nhạc "Summer Music Fest 2025" triển khai cổng bán vé trực tuyến trên hệ thống **Ticketbox**. Với các đêm diễn thu hút lượng lớn người hâm mộ, hệ thống gặp phải hai thách thức kỹ thuật lớn:
1.  **Hiện tượng đầu cơ vé (Phe vé):** Một số người dùng tìm cách mua số lượng lớn vé trong một hoặc nhiều lượt đặt liên tiếp trên cùng một tài khoản. Ban tổ chức đã ban hành quy định cứng: **Một tài khoản chỉ được phép mua tối đa 4 vé cho một đêm diễn**.
2.  **Rò rỉ và can thiệp dữ liệu kho vé:** Mã nguồn cũ lưu trữ tổng số vé còn lại và lịch sử mua hàng của khách trong các biến toàn cục (Global Variables). Điều này khiến dữ liệu dễ bị các đoạn script bên ngoài can thiệp và làm lệch tồn kho thực tế.

Ban công nghệ yêu cầu bạn thiết kế lại **Module Quản lý Đặt vé Sự kiện (Ticket Booking Session Manager)** bằng cách áp dụng **Closure** và **Arrow Function**. Module phải đóng gói hoàn toàn số lượng vé còn lại trong kho và số lượng vé mà khách hàng đã tích lũy mua, đồng thời tính toán chính xác tổng tiền thanh toán sau khi áp dụng chiết khấu vé sớm (Early Bird) và phí dịch vụ phát hành vé.---

### **3. Quy tắc nghiệp vụ**

Hệ thống đặt vé cần tuân thủ nghiêm ngặt các quy tắc tính toán và hạn ngạch sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Quy tắc nghiệp vụ</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Mô tả chi tiết &amp; Công thức áp dụng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>1. Đóng gói trạng thái (State Encapsulation)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Toàn bộ dữ liệu về số lượng vé tồn kho (<code>availableStock</code>) và tổng số vé đã mua của khách hàng (<code>userPurchasedCount</code>) phải nằm trong Lexical Scope của hàm khởi tạo session. Mã bên ngoài không thể truy cập hoặc sửa đổi trực tiếp các biến này.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>2. Giới hạn hạn ngạch (Purchase Limit)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Mỗi tài khoản được mua <strong>tối đa 4 vé</strong>. Nếu giao dịch mới khiến tổng số vé tích lũy của khách vượt quá 4 vé, hệ thống phải từ chối giao dịch và giữ nguyên tồn kho.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>3. Chiết khấu mặc định (Early Bird Discount)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Mặc định áp dụng tỷ lệ chiết khấu bán sớm là <strong>15% (0.15)</strong> nếu không truyền tham số chiết khấu khác.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>4. Phí dịch vụ mặc định (Issuance Fee)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Mỗi vé phát hành chịu phí cố định mặc định là <strong>20,000 VNĐ / vé</strong> nếu không truyền tham số phí khác.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>5. Công thức tính tổng thanh toán</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>Tiền vé sau chiết khấu = Số lượng mua * Giá niêm yết * (1 - Tỷ lệ chiết khấu)</code><br>
        <code>Tổng phí dịch vụ = Số lượng mua * Phí dịch vụ mỗi vé</code><br>
        <code>Tổng thanh toán = Tiền vé sau chiết khấu + Tổng phí dịch vụ</code>
      </td>
    </tr>
  </tbody>
</table>

---

### **4. Yêu cầu bài toán**

Học viên thực hiện bài tập theo **2 phần bắt buộc** sau:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Viết trong file BÁO_CÁO.md hoặc phần Comment ở đầu file code)**
1.  **Phân tích I/O:** Xác định chi tiết danh sách tham số đầu vào (Input), dữ liệu trả về (Output) và kiểu dữ liệu (Data types) cho các hàm cần xây dựng.
2.  **Đề xuất Giải pháp kỹ thuật:** Giải thích cách ứng dụng Closure và Arrow Function để bảo vệ dữ liệu private (`availableStock`, `userPurchasedCount`) không bị can thiệp từ Global scope.
3.  **Sơ đồ luồng xử lý (Flowchart/Pseudocode):** Lập sơ đồ các bước thực hiện khi khách hàng yêu cầu đặt mua số lượng vé `N`. Tuân thủ đúng các quy tắc kiểm tra hạn ngạch 4 vé và kiểm tra tồn kho.

#### **Phần 2: Cài đặt Mã nguồn & Kiểm chuẩn (Implementation & Edge-case Guards)**
Viết chương trình bằng **JavaScript ES6+** đáp ứng các yêu cầu kỹ thuật:
1.  Sử dụng cú pháp **Arrow Function** và **Tham số mặc định (Default Parameters)** cho các hàm tính toán và khởi tạo.
2.  Đóng gói toàn bộ logic quản lý session đặt vé vào một hàm tạo (ví dụ: `createTicketBookingSession`), trả về một object chứa các phương thức tương tác với state thông qua Closure.
3.  Bắt chặt các trường hợp lỗi dữ liệu biên (Edge cases):
    *   Số lượng vé mua không phải là số nguyên dương ($N \le 0$ hoặc không phải kiểu integer).
    *   Số lượng vé mua vượt quá tồn kho còn lại của sự kiện.
    *   Số lượng vé mua làm tổng số vé tài khoản sở hữu vượt quá hạn ngạch 4 vé.
    *   Giá vé niêm yết âm hoặc không hợp lệ.
4.  Viết các kịch bản kiểm thử (Test cases) giả định cuộc gọi hàm consoleLog để minh họa:
    *   Kịch bản 1: Mua hợp lệ lần 1 (dùng chiết khấu mặc định).
    *   Kịch bản 2: Mua tiếp lần 2 thành công nhưng tiệm cận hạn ngạch.
    *   Kịch bản 3: Mua lần 3 thất bại do vượt tổng hạn ngạch 4 vé.
    *   Kịch bản 4: Truyền dữ liệu lỗi (số lượng âm hoặc vượt quá tồn kho còn lại).

---

### **5. Yêu cầu nộp bài**

Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai đầy đủ logic trên 1 file script JS (hoặc đính kèm file báo cáo `.md`).
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex9`.
    *   *Ví dụ:* `HNKS25CNTT1_Core_Session14_Ex9`

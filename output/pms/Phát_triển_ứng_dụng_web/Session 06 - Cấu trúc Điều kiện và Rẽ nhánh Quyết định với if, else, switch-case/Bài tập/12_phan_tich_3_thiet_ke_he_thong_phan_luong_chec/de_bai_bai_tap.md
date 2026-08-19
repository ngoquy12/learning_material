# <center>[Phân tích 3] Thiết kế Hệ thống Phân luồng Check-in và Tính phí Phụ thu Hành lý Máy bay</center>

### **1. Mục tiêu**
*   **Phân tích kiến trúc điều kiện phức tạp:** Đánh giá và so sánh các phương án thiết kế luồng rẽ nhánh (`if-else if-else`, `switch-case`, toán tử ba ngôi ternary) khi xử lý logic nghiệp vụ có nhiều tiêu chí đầu vào phối hợp.
*   **Tối ưu hóa khả năng bảo trì mã nguồn:** Áp dụng kỹ thuật phẳng hóa điều kiện (Guard Clauses) hoặc phân tách nhóm quyết định để giảm độ phức tạp nhận thức (Cognitive Complexity) của chương trình.
*   **Triển khai logic phân luồng và phụ thu check-in:** Lập trình hoàn chỉnh module tính phí hành lý quá cước, phí trễ giờ làm thủ tục và chỉ định quầy làm thủ tục (Counter Lane) cho hành khách hàng không theo chuẩn Clean Code.

### **2. Bối cảnh & Vấn đề**
Hệ thống quầy làm thủ tục tự động (Kiosk & Staff Check-in Desk) của hãng hàng không Vietjet / Vietnam Airlines cần xử lý hàng triệu lượt hành khách mỗi ngày tại các sân bay lớn. Khi hành khách tới làm thủ tục check-in, hệ thống phải xác định ngay lập tức hai thông tin quan trọng:
1.  **Tổng chi phí phụ thu phát sinh** (bao gồm phí hành lý ký gửi quá kg quy định và phí xử lý check-in sát giờ bay).
2.  **Làn quầy ưu tiên (Counter Lane)** dành riêng cho hành khách thực hiện thủ tục.

Hiện tại, mã nguồn của hệ thống gặp tình trạng lồng ghép nhiều câu lệnh `if-else` quá sâu, dẫn đến việc tính sai phụ thu đối với hành khách hạng Deluxe/Business và phân nhầm làn phục vụ trong các khung giờ cao điểm. Nhiệm vụ của bạn là phân tích các giải pháp kiến trúc rẽ nhánh, lựa chọn phương án tối ưu và cài đặt lại logic nghiệp vụ này bằng JavaScript (ES6+).

### **3. Quy tắc nghiệp vụ**
Hệ thống nhận vào 4 biến thông tin hành khách cơ bản:
*   `ticketClass` (số nguyên): Hạng vé (`1`: Eco, `2`: Deluxe, `3`: Business).
*   `baggageWeight` (số thực/số nguyên): Trọng lượng hành lý thực tế (đơn vị: kg).
*   `isVipPassenger` (boolean): Trạng thái hành khách thân thiết VIP (`true` / `false`).
*   `isLateCheckin` (boolean): Trạng thái làm thủ tục sát giờ bay dưới 45 phút (`true` / `false`).

Các quy tắc tính toán và phân luồng áp dụng như sau:

1.  **Quy định Miễn cước & Phí hành lý quá cân:**
    *   **Hạng Eco (`ticketClass === 1`):** Mức hành lý miễn phí tối đa là 7 kg. Mỗi kg vượt cước tính 50.000 VNĐ/kg.
    *   **Hạng Deluxe (`ticketClass === 2`):** Mức hành lý miễn phí tối đa là 20 kg. Mỗi kg vượt cước tính 40.000 VNĐ/kg.
    *   **Hạng Business (`ticketClass === 3`):** Mức hành lý miễn phí tối đa là 40 kg. Mỗi kg vượt cước tính 30.000 VNĐ/kg.
    *   *Lưu ý:* Nếu trọng lượng hành lý thực tế nhỏ hơn hoặc bằng mức miễn cước thì phí quá cân bằng 0 VNĐ.

2.  **Quy định Phí làm thủ tục trễ sát giờ (`isLateCheckin === true`):**
    *   **Hạng Eco (`ticketClass === 1`):** Thu thêm phí xử lý nhanh 200.000 VNĐ.
    *   **Hạng Deluxe (`ticketClass === 2`):** Thu thêm phí xử lý nhanh 100.000 VNĐ.
    *   **Hạng Business (`ticketClass === 3`):** Miễn phí xử lý nhanh (0 VNĐ).
    *   *Lưu ý:* Nếu `isLateCheckin === false` thì phí trễ bằng 0 VNĐ cho tất cả các hạng vé.

3.  **Quy định Phân bổ Làn check-in (`counterLane`):**
    *   Nếu hành khách là khách VIP (`isVipPassenger === true`) HOẶC bay hạng Business (`ticketClass === 3`): Phân bổ vào `"Làn Ưu Tiên (Priority Counter)"`.
    *   Ngược lại, nếu bay hạng Deluxe (`ticketClass === 2`): Phân bổ vào `"Làn Nhanh (Fast-track Counter)"`.
    *   Ngược lại (bay hạng Eco `ticketClass === 1` và không phải VIP): Phân bổ vào `"Làn Tiêu Chuẩn (Standard Counter)"`.

4.  **Kiểm tra Dữ liệu Hợp lệ (Data Validation Edge Cases):**
    *   Nếu `ticketClass` không thuộc tập {1, 2, 3} hoặc `baggageWeight < 0`, chương trình phải dừng tính toán và thông báo dữ liệu không hợp lệ.

### **4. Yêu cầu bài toán**

Học viên thực hiện đầy đủ 3 phần công việc sau:

#### **Phần 1: Đề xuất Đa giải pháp & Báo cáo So sánh Trade-off**
*   Tự thiết kế và đề xuất ít nhất **02 phương án kỹ thuật rẽ nhánh** khác nhau để giải quyết bài toán trên (Ví dụ: Phương án 1 dùng lồng ghép `switch-case` kiểm tra hạng vé và các mệnh đề `if-else` bên trong; Phương án 2 áp dụng kỹ thuật Kiểm tra dữ liệu biên sớm Guard Clauses combined với các hằng số cấu hình rẽ nhánh phẳng).
*   Lập bảng so sánh chi tiết giữa 2 phương án theo 5 tiêu chí bắt buộc sử dụng định dạng HTML table:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Tiêu chí So sánh</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án A</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">1. Tốc độ xử lý (Time Complexity)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">2. Bộ nhớ sử dụng (Memory Space)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">3. Khả năng bảo trì (Maintainability)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">4. Độ dễ đọc mã nguồn (Readability)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">5. Mức độ phù hợp với quy mô nghiệp vụ</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Giải trình Lựa chọn và Thiết kế Mã giả / Lưu đồ**
*   Đưa ra lập luận kỹ thuật ngắn gọn giải thích lý do chọn phương án tối ưu nhất cho hệ thống sân bay thực tế.
*   Biểu diễn luồng thuật toán tối ưu bằng **Mã giả (Pseudocode)** hoặc **Lưu đồ Mermaid (Mermaid Flowchart)**. Tuân thủ nghiêm ngặt quy chuẩn hình dạng Mermaid:
    *   Bắt đầu/Kết thúc: Hình Oval `([Bắt đầu])`, `([Kết thúc])`.
    *   Nhập/Xuất dữ liệu: Hình Biểu tượng Đầu vào/Đầu ra `[/Đầu vào: .../]`.
    *   Kiểm tra điều kiện: Hình Thoi `Kiểm tra điều kiện?`.
    *   Thực hiện tính toán / gán biến: Hình Chữ nhật `["Tính toán / Thực thi"]`.

#### **Phần 3: Triển khai Mã nguồn & Kiểm chuẩn Biên**
*   Viết chương trình JavaScript Vanilla (ES6+) thực thi phương án đã chọn.
*   Khai báo bộ dữ liệu kiểm thử (Test Cases) phủ đủ các trường hợp:
    1.  Hành khách Eco đi quá cước + sát giờ bay (`ticketClass = 1`, `baggageWeight = 12`, `isVipPassenger = false`, `isLateCheckin = true`).
    2.  Hành khách Deluxe VIP không sát giờ bay (`ticketClass = 2`, `baggageWeight = 25`, `isVipPassenger = true`, `isLateCheckin = false`).
    3.  Hành khách Business quá cước sát giờ bay (`ticketClass = 3`, `baggageWeight = 45`, `isVipPassenger = false`, `isLateCheckin = true`).
    4.  Trường hợp lỗi dữ liệu biên: `ticketClass = 99` hoặc `baggageWeight = -5`.
*   Hiển thị báo cáo kết quả chi tiết ra `console.log` rõ ràng từng khoản mục tiền và làn check-in tương ứng.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo so sánh và mã nguồn triển khai trong một tập tin duy nhất hoặc theo cấu trúc dự án.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex12`.
    *   *Ví dụ:* `HNKS25CNTT1_Core_Session06_Ex12`

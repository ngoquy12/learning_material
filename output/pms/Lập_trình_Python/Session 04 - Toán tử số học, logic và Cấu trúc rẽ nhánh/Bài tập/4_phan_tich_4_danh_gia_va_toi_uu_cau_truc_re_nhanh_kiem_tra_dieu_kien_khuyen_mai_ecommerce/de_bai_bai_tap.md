## <center>[Phân tích] Tối ưu hóa logic duyệt ưu đãi đơn hàng E-Commerce</center>

### **1. Mục tiêu**
*   **Phân tích và đánh giá**: So sánh chi tiết sự khác biệt giữa cấu trúc rẽ nhánh lồng nhau nhiều tầng (Arrow Anti-Pattern) và cấu trúc điều kiện phẳng hóa kết hợp toán tử logic (`and`, `or`, `not`) tuân thủ chuẩn PEP 8.
*   **Đề xuất giải pháp**: Xây dựng 2 phương án kiến trúc xử lý điều kiện khuyến mãi đơn hàng trong hệ thống Thương mại Điện tử (E-Commerce).
*   **Đánh giá Trade-off**: Lập bảng phân tích đánh giá ưu/nhược điểm của từng phương án dựa trên các tiêu chí kỹ thuật: Thời gian xử lý, Dung lượng bộ nhớ, Độ đọc hiểu, Khả năng mở rộng và Duy trì mã nguồn.
*   **Triển khai mã nguồn**: Hiện thực hóa giải pháp tối ưu bằng ngôn ngữ Python với đầy đủ chú giải kiểu dữ liệu (Type Hints) và kiểm soát các trường hợp dữ liệu biên.

### **2. Bối cảnh & Vấn đề**
Trong các chiến dịch mua sắm lớn (Flash Sale), hệ thống E-Commerce phải xử lý hàng trăm nghìn yêu cầu kiểm tra điều kiện áp dụng mã giảm giá mỗi phút. Đoạn mã hiện tại của hệ thống đang gặp phải hiện tượng "mũi tên lồng nhau" (Arrow Anti-Pattern) do các kỹ sư tiền nhiệm viết nhiều câu lệnh `if-else` lồng sâu vào nhau để kiểm tra độ tuổi, hạng thành viên, giá trị đơn hàng và khoảng cách giao hàng.

Hệ quả là mã nguồn trở nên vô cùng rối rắm, khó đọc, dễ phát sinh lỗi khi bổ sung quy tắc mới và làm giảm tốc độ phản hồi của hệ thống. Đội ngũ Kiến trúc sư Phần mềm yêu cầu bạn thực hiện một báo cáo phân tích phản biện kỹ thuật, so sánh giữa giải pháp mã lồng nhau truyền thống và giải pháp phẳng hóa điều kiện theo chuẩn PEP 8, sau đó triển khai mã nguồn chuẩn hóa hoàn chỉnh.



### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý ưu đãi đơn hàng tuân theo các quy tắc kiểm tra nghiêm ngặt sau:

1.  **Kiểm tra tính hợp lệ của dữ liệu đầu vào**:
    *   Giá trị đơn hàng (`cart_value`): phải lớn hơn 0.
    *   Độ tuổi khách hàng (`customer_age`): phải từ 0 trở lên.
    *   Khoảng cách giao hàng (`shipping_distance`): phải từ 0 km trở lên.
    *   Số đơn hàng đã mua trong tháng (`total_past_orders`): phải từ 0 trở lên.
    *   *Nếu bất kỳ chỉ số nào vi phạm, hệ thống dừng xử lý và thông báo lỗi dữ liệu không hợp lệ.*

2.  **Hạng mức ưu đãi áp dụng**:
    *   **Mức 1 (Ưu đãi VIP - Giảm 20% và Miễn phí vận chuyển)**:
        Khách hàng là thành viên VIP (`is_vip = True`) HOẶC Đơn hàng có giá trị từ 5,000,000 VNĐ trở lên. Đồng thời, khách hàng phải từ 18 tuổi trở lên VÀ khoảng cách giao hàng không quá 20 km.
    *   **Mức 2 (Ưu đãi Thân thiết - Giảm 10%)**:
        Nếu không đạt Mức 1, đơn hàng được giảm 10% nếu khách hàng đã mua từ 5 đơn hàng trở lên trong tháng HOẶC giá trị đơn hàng từ 2,000,000 VNĐ trở lên.
    *   **Mức 3 (Không áp dụng ưu đãi - Giảm 0%)**:
        Tất cả các trường hợp còn lại.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất & So sánh Trade-off**
*   Mô tả ngắn gọn 2 phương án kỹ thuật triển khai cho bài toán trên:
    *   **Phương án A**: Triển khai bằng cấu trúc `if-else` lồng nhau nhiều cấp (Nested Branching).
    *   **Phương án B**: Phẳng hóa điều kiện bằng toán tử logic (`and`, `or`, `not`) kết hợp quy tắc thoát sớm (Guard Clauses / Early Exit) chuẩn PEP 8.
*   Xây dựng bảng so sánh Trade-off trực quan giữa 2 phương án theo bảng mẫu HTML dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr>
      <th style="padding: 8px; text-align: left;">Tiêu chí đánh giá</th>
      <th style="padding: 8px; text-align: left;">Phương án A (Nested if-else)</th>
      <th style="padding: 8px; text-align: left;">Phương án B (Phẳng hóa PEP 8)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;">Thời gian xử lý (Speed)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Bộ nhớ sử dụng (Memory)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Độ đọc hiểu (Readability)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Bảo trì & Mở rộng (Maintainability)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Mức độ phù hợp thực tế (Suitability)</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Lý giải Chọn lựa & Biểu diễn Mã giả**
*   Đưa ra lập luận kỹ thuật giải thích lý do vì sao chọn Phương án B cho hệ thống E-Commerce quy mô lớn.
*   Biểu diễn mã giả (Pseudocode) hoặc Lưu đồ thuật toán (Flowchart bằng text/ASCII) mô tả chi tiết luồng xử lý của Phương án B.

#### **Phần 3: Triển khai Mã nguồn Python Tối ưu**
*   Viết hàm xử lý chính `evaluate_order_promotion` nhận vào các tham số: `cart_value: float`, `customer_age: int`, `is_vip: bool`, `total_past_orders: int`, `shipping_distance: float` và trả về kết quả dưới dạng chuỗi thông báo kết quả chi tiết.
*   Mã nguồn phải tuân thủ chuẩn PEP 8 (thụt lề 4 space, đặt tên biến theo chuẩn `snake_case`, sử dụng Type Hints đầy đủ).
*   Chương trình bao gồm các câu lệnh thử nghiệm kiểm chứng cho cả 3 trường hợp ưu đãi và 1 trường hợp dữ liệu biên không hợp lệ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex04`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex04`
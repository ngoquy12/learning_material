## <center>[Vận dụng nâng cao 1] Tính toán chi phí đặt phòng phức hợp và Đánh giá điều kiện xác thực giao dịch</center>

### **1. Mục tiêu**
*   **Kiến thức:** Vận dụng thành thạo các toán tử số học (`+`, `-`, `*`, `/`, `//`, `%`, `**`) và toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`) trong ngôn ngữ lập trình Python 3.12 để giải quyết bài toán tài chính phức hợp.
*   **Kỹ năng:** Nâng cao tư duy phân tích nghiệp vụ độc lập (Closed How - Open What & Why), biết cách tự định nghĩa mô hình dữ liệu đầu vào/đầu ra, thiết kế luồng xử lý bằng sơ đồ thuật toán và cài đặt mã nguồn tuân thủ nghiêm ngặt chuẩn PEP 8 cùng Type Hints.
*   **Thực tiễn:** Giải quyết bài toán tính toán chi phí lưu trú, phụ phí dịch vụ phát sinh và kiểm tra điều kiện giao dịch tài chính cho hệ thống đặt phòng trực tuyến Agoda / Traveloka.

---

### **2. Bối cảnh & Vấn đề**
Trong phân hệ xử lý giao dịch của nền tảng đặt phòng khách sạn và homestay trực tuyến (HOTEL_BOOKING), khi khách hàng thực hiện đặt phòng, hệ thống cần tự động tính toán tổng hóa đơn lưu trú. Chi phí này không chỉ bao gồm tiền phòng theo đêm mà còn bao gồm các khoản phụ thu nghiệp vụ như: phụ thu nhận phòng sớm (early check-in), phí phát sinh cho khách vượt số lượng tiêu chuẩn, và tiền thuế giá trị gia tăng (VAT).

Sau khi tổng hợp chi phí, hệ thống cần thực hiện các phép đánh giá tài chính tự động thông qua toán tử so sánh để trả về các trạng thái logic kiểu `bool`:
1.  Xác nhận tiền đặt cọc thực tế của khách đã đạt mức cọc tối thiểu theo quy định hay chưa.
2.  Xác định đơn hàng có đạt hạn mức tổng tiền để tự động kích hoạt chế độ nâng hạng phòng VIP hay không.
3.  Kiểm tra ngân sách bình quân mỗi khách lưu trú có nằm trong hạn mức tiêu chuẩn của nền tảng hay không.

Sinh viên đóng vai trò là Lập trình viên Backend chịu trách nhiệm phân tích I/O, thiết kế luồng tính toán và viết mã nguồn thực thi logic trên mà không được sử dụng các cấu trúc rẽ nhánh hay vòng lặp nâng cao.---

### **3. Quy tắc nghiệp vụ**
Hệ thống áp dụng các quy tắc số học và điều kiện hạn mức tài chính sau:

1.  **Tiền phòng cơ bản (`base_room_cost`):**
    `base_room_cost = base_price_per_night * nights_count`
2.  **Phụ thu check-in sớm (`early_checkin_fee`):**
    Nếu khách check-in sớm (nhận giá trị đánh dấu `1` cho biến `early_checkin_flag`, ngược lại là `0`), tính phụ thu 30% giá phòng của 1 đêm:
    `early_checkin_fee = base_price_per_night * 0.3 * early_checkin_flag`
3.  **Phụ thu khách phát sinh (`extra_guest_fee`):**
    Số khách tiêu chuẩn cho mỗi phòng là 2 người. Phụ thu cho mỗi khách vượt tiêu chuẩn (`extra_guest_count`) là 200,000 VND/người/đêm:
    `extra_guest_fee = extra_guest_count * 200000 * nights_count`
4.  **Tổng chi phí trước thuế (`total_before_tax`) & Thuế VAT (`vat_amount`):**
    `total_before_tax = base_room_cost + early_checkin_fee + extra_guest_fee`
    `vat_amount = total_before_tax * 0.10`
5.  **Tổng hóa đơn thanh toán (`total_amount`):**
    `total_amount = total_before_tax + vat_amount`
6.  **Hạn mức đặt cọc tối thiểu (`required_deposit`):**
    Quy định đặt cọc tối thiểu bằng 50% tổng hóa đơn thanh toán:
    `required_deposit = total_amount * 0.5`
7.  **Các chỉ số đánh giá điều kiện giao dịch (Kết quả So sánh `bool`):**
    *   `is_deposit_sufficient`: Kiểm tra số tiền cọc thực tế khách đã trả (`paid_deposit`) có lớn hơn hoặc bằng tiền cọc tối thiểu (`required_deposit`) hay không.
    *   `is_vip_upgrade_eligible`: Kiểm tra tổng hóa đơn thanh toán (`total_amount`) có đạt từ 15,000,000 VND trở lên hay không.
    *   `is_budget_per_guest_valid`: Tính chi phí bình quân mỗi khách (sử dụng phép chia lấy phần nguyên `total_amount // total_guests` với `total_guests = standard_guests + extra_guest_count`) và kiểm tra xem có nhỏ hơn hoặc bằng 2,500,000 VND hay không.

---

### **4. Yêu cầu bài toán**
Bài tập bao gồm 2 phần bắt buộc học viên phải thực hiện:

#### **Phần 1: Báo cáo Phân tích & Thiết kế (Analysis & Design Report)**
1.  **Phân tích I/O (Input / Output):**
    *   Tự xác định và lập bảng danh sách toàn bộ các tham số đầu vào (`Input`) và đầu ra (`Output`).
    *   Ghi rõ tên biến (bằng Tiếng Anh), mô tả ý nghĩa nghiệp vụ và kiểu dữ liệu tương ứng trong Python (`int`, `float`, `bool`).
2.  **Đề xuất giải pháp & Thiết kế quy trình (Flowchart):**
    *   Mô tả các bước thực hiện tuần tự để tính toán và đánh giá điều kiện.
    *   Vẽ sơ đồ quy trình Mermaid Flowchart thể hiện toàn bộ luồng xử lý từ lúc nhận dữ liệu đến khi xuất kết quả.
    *   *Quy định bắt buộc về hình khối Mermaid:*
        *   Hình Oval `([Bắt đầu / Kết thúc])`: Điểm bắt đầu và kết thúc luồng.
        *   Hình Bình hành `[/Đầu vào / Đầu ra/]`: Nhập thông số booking và Xuất kết quả tài chính.
        *   Hình Chữ nhật `["Tính toán / Xử lý"]`: Phép tính số học (tổng tiền, phụ thu, thuế, cọc).
        *   Hình Thoi `Kiểm tra điều kiện?`: Thực hiện các phép so sánh kiểm tra hạn mức tài chính.

#### **Phần 2: Cài đặt Mã nguồn (Implementation)**
1.  Khai báo các biến đầu vào mô phỏng một giao dịch thực tế trên Agoda / Traveloka với đầy đủ Type Hints theo chuẩn PEP 8.
2.  Thực hiện các tính toán số học và so sánh logic đúng theo các Quy tắc nghiệp vụ ở Mục 3.
3.  In báo cáo tài chính đặt phòng và kết quả đánh giá điều kiện giao dịch ra màn hình console bằng hàm `print()`.
4.  **HẠN MỨC KIẾN THỨC CẤM:**
    *   TUYỆT ĐỐI KHÔNG sử dụng câu lệnh rẽ nhánh (`if`, `elif`, `else`).
    *   TUYỆT ĐỐI KHÔNG sử dụng vòng lặp (`for`, `while`).
    *   TUYỆT ĐỐI KHÔNG sử dụng các cấu trúc dữ liệu nâng cao (`list`, `dict`, `set`, `tuple`).
    *   TUYỆT ĐỐI KHÔNG sử dụng các toán tử logic (`and`, `or`, `not`). Chỉ sử dụng toán tử số học và toán tử so sánh.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex7`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex7`
# <center>[Vận dụng nâng cao 1] Hệ thống tính phí cước hành lý sân bay tự động</center>

### **1. Mục tiêu**
Vận dụng kết hợp các cấu trúc điều kiện `if...else`, rẽ nhánh `switch-case` và toán tử ba ngôi (ternary operator) trong JavaScript (ES6+) để xây dựng module tính toán hạn mức hành lý miễn cước và tổng phí phạt quá cước hành lý tại quầy check-in sân bay cho hệ thống quản lý bay **AIRLINE_CHECKIN**.

### **2. Bối cảnh & Vấn đề**
Trong quy trình làm thủ tục làm vé (check-in) của các hãng hàng không, việc xác định hạn mức hành lý miễn phí và tính tiền phạt cước khi vượt trọng lượng đòi hỏi độ chính xác tuyệt đối. Hệ thống cần tự động tính toán dựa trên hạng vé (Business, Deluxe, Eco), loại hành khách (Người lớn, Trẻ em, Em bé) và chính sách ưu đãi cho thẻ hội viên VIP. Ngoài ra, với những kiện hàng quá nặng vượt quá 15 kg so với quy định miễn cước, hệ thống cần áp dụng thêm phụ phí xếp dỡ đặc biệt.

### **3. Quy tắc nghiệp vụ**
Chương trình cần xử lý các dữ liệu đầu vào gồm: `ticketClass` (mã hạng vé), `baggageWeight` (trọng lượng hành lý thực tế tính theo kg), `passengerType` (loại hành khách), và `isVipMember` (trạng thái hội viên VIP).

1. **Hạn mức hành lý miễn cước cơ bản (Free Baggage Allowance):**
   * Hạng vé `"BUSINESS"`: 30 kg miễn cước.
   * Hạng vé `"DELUXE"`: 20 kg miễn cước.
   * Hạng vé `"ECO"`: 7 kg miễn cước.
   * Nếu `ticketClass` không thuộc 3 hạng trên: Cảnh báo hạng vé không hợp lệ và không tiến hành tính toán.

2. **Cộng thêm hạn mức ưu đãi:**
   * Nếu `passengerType === "INFANT"` (Em bé dưới 2 tuổi): Được cộng thêm 5 kg vào hạn mức miễn cước cơ bản.
   * Nếu `isVipMember === true`: Được cộng thêm 10 kg vào hạn mức miễn cước cơ bản.
   * Hai ưu đãi này có thể tích lũy đồng thời nếu khách hàng thỏa mãn cả hai điều kiện.

3. **Tính trọng lượng quá cước (Excess Weight):**
   * Trọng lượng quá cước = `baggageWeight` - `tổng hạn mức miễn cước`.
   * Nếu trọng lượng quá cước <= 0: Không phát sinh phí phạt quá cước (Phí phạt = 0 VNĐ).

4. **Đơn giá cước phạt theo kg (Overweight Rate):**
   * Hạng `"BUSINESS"`: 40.000 VNĐ / kg quá cước.
   * Hạng `"DELUXE"`: 50.000 VNĐ / kg quá cước.
   * Hạng `"ECO"`: 60.000 VNĐ / kg quá cước.

5. **Phụ phí kiện cồng kềnh/quá tải (Surcharge Fee):**
   * Áp dụng toán tử ba ngôi: Nếu trọng lượng quá cước lớn hơn 15 kg (`excessWeight > 15`), áp dụng mức phụ phí xếp dỡ là 200.000 VNĐ; ngược lại phụ phí bằng 0 VNĐ.

6. **Tính tổng tiền & Kiểm tra dữ liệu hợp lệ (Input Validation):**
   * Tổng phí phạt = (Trọng lượng quá cước * Đơn giá cước) + Phụ phí.
   * Nếu `baggageWeight < 0`: Thông báo lỗi dữ liệu cân nặng không hợp lệ.

### **4. Yêu cầu bài toán**
Học viên thực hiện bài tập theo 2 phần bắt buộc:

*   **Phần 1: Báo cáo Phân tích & Thiết kế giải pháp (Solution Analysis & Design Report)**
    *   **Phân tích I/O:** Xác định rõ các biến đầu vào, đầu ra và kiểu dữ liệu tương ứng (string, number, boolean).
    *   **Đề xuất giải pháp & Sơ đồ luồng (Flowchart):** Thiết kế sơ đồ tiến trình xử lý nghiệp vụ bằng định dạng Mermaid Flowchart tuân thủ đúng 5 dạng hình chuẩn:
        1. Oval `([Bắt đầu / Kết thúc])`
        2. Parallelogram `[/Đầu vào: .../]` và `[/Đầu ra: .../]`
        3. Diamond `Kiểm tra điều kiện?` với các nhánh `-->|Đúng|` / `-->|Sai|`
        4. Rectangle `["Thực hiện tính toán / Gán giá trị"]`
        5. Quy tắc bắt buộc: Tuyệt đối không dùng hình Parallelogram cho các bước tính toán xử lý!

*   **Phần 2: Cài đặt Mã nguồn & Chặn lỗi biên (Implementation & Error Guards)**
    *   Viết mã nguồn bằng JavaScript (ES6+) thực thi kịch bản xử lý nghiệp vụ trên.
    *   Sử dụng cấu trúc `switch-case` để phân loại đơn giá cước phạt theo từng hạng vé.
    *   Sử dụng cấu trúc `if...else` để kiểm tra điều kiện ưu đãi và tính toán hạn mức hành lý miễn cước.
    *   Sử dụng toán tử ba ngôi (`? :`) để xác định phụ phí xếp dỡ cho kiện cồng kềnh.
    *   Xử lý các bẫy dữ liệu đầu vào vi phạm quy tắc (cân nặng âm, hạng vé không hợp lệ).
    *   In kết quả tính toán chi tiết ra màn hình console minh bạch và rõ ràng.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex7`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex7`

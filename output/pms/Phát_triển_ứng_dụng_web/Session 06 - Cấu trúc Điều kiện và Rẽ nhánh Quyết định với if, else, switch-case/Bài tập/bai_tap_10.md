# <center>[Phân tích 1] Phân tích và Triển khai Module Tính Phụ phí Check-in Máy bay</center>

### **1. Mục tiêu**
*   **Tư duy Phân tích & Thiết kế**: Học viên có khả năng phân tích một bài toán rẽ nhánh đa điều kiện thực tế trong hệ thống quản lý bay, tự đề xuất ít nhất 2 phương án kiến trúc lập trình khác nhau (kết hợp `if...else`, `switch-case`, và toán tử ba ngôi `ternary operator`).
*   **Đánh giá Trade-off**: Đánh giá ưu/nhược điểm của các phương án dựa trên 5 tiêu chí kỹ thuật (Hiệu năng, Bộ nhớ, Khả năng bảo trì, Độ sạch của mã nguồn, Tính phù hợp nghiệp vụ).
*   **Chuẩn hóa Lưu đồ thuật toán**: Vẽ sơ đồ luồng (Flowchart) bằng Mermaid tuân thủ đúng 5 quy chuẩn hình dạng kỹ thuật.
*   **Kỹ năng Lập trình**: Triển khai mã nguồn JavaScript (ES6+) tối ưu, xử lý triệt để các trường hợp dữ liệu biên (edge cases) và kiểm soát lỗi dữ liệu đầu vào.

---

### **2. Bối cảnh & Vấn đề**
Hệ thống Ban Vé & Làm thủ tục check-in của hãng hàng không (AIRLINE_CHECKIN) đang phát triển module tự động tính toán phụ phí hành lý ký gửi và phí dịch vụ check-in tại sân bay. 

Khi hành khách làm thủ tục tại quầy hoặc trên ứng dụng trực tuyến, hệ thống cần tính toán chính xác tổng chi phí phát sinh dựa trên:
1. Hạng vé mà hành khách sở hữu (Business, Deluxe, Eco).
2. Trọng lượng hành lý ký gửi thực tế mang theo.
3. Kênh thực hiện làm thủ tục (Tại quầy sân bay hay Trực tuyến qua Web/App).
4. Trạng thái thẻ VIP của khách hàng.

Nếu cấu trúc rẽ nhánh điều kiện được thiết kế không hợp lý, mã nguồn sẽ trở nên rườm rà, dễ bỏ sót trường hợp biên (như nhập trọng lượng âm hoặc sai mã hạng vé), hoặc dẫn đến việc tính sai phụ phí làm ảnh hưởng trực tiếp đến doanh thu hãng và trải nghiệm khách hàng.---

### **3. Quy tắc nghiệp vụ**
Hệ thống tiếp nhận 4 tham số đầu vào cho mỗi lượt check-in:
*   `ticketClass` (chuỗi): Mã hạng vé (`"BUSINESS"`, `"DELUXE"`, `"ECO"`).
*   `baggageWeight` (số): Trọng lượng hành lý ký gửi thực tế (đơn vị: kg).
*   `checkinChannel` (chuỗi): Kênh làm thủ tục (`"WEB"` hoặc `"COUNTER"`).
*   `isVipPassenger` (boolean): Trạng thái khách hàng VIP (`true` hoặc `false`).

Các quy tắc tính toán phụ phí được quy định chi tiết như sau:

1.  **Mức hành lý ký gửi miễn phí theo hạng vé**:
    *   `"BUSINESS"`: Miễn phí tối đa **30 kg**.
    *   `"DELUXE"`: Miễn phí tối đa **20 kg**.
    *   `"ECO"`: **Không** có suất miễn phí (0 kg).

2.  **Đơn giá phụ thu hành lý quá cước**:
    *   Số kg vượt quá cước miễn phí sẽ chịu phụ thu với đơn giá chuẩn: **50.000 VNĐ / kg**.
    *   Nếu trọng lượng hành lý nhỏ hơn hoặc bằng mức miễn phí áp dụng cho hạng vé đó, phí quá cước bằng **0 VNĐ**.

3.  **Phí làm thủ tục tại quầy (Counter Fee)**:
    *   Nếu `checkinChannel === "COUNTER"` đồng thời `ticketClass === "ECO"` và `isVipPassenger === false`: Phụ thu phí in thẻ lên tàu bay tại quầy là **100.000 VNĐ**.
    *   Các trường hợp còn lại (làm qua WEB/App, hoặc vé BUSINESS/DELUXE, hoặc là khách VIP): Phí này bằng **0 VNĐ**.

4.  **Chính sách ưu đãi dành cho Khách hàng VIP**:
    *   Nếu `isVipPassenger === true`: Hành khách được **giảm 20%** trực tiếp trên tổng phí hành lý quá cước (`overweightFee * 0.2`). Phí in thẻ làm thủ tục tại quầy (nếu có) không áp dụng mức giảm giá này.

5.  **Kiểm tra tính hợp lệ dữ liệu (Validation)**:
    *   Nếu `baggageWeight < 0` hoặc `ticketClass` không phải là một trong các giá trị (`"BUSINESS"`, `"DELUXE"`, `"ECO"`), hệ thống phải thông báo lỗi dữ liệu không hợp lệ và hủy quá trình tính toán.

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò là Lập trình viên Senior phụ trách module này, hãy thực hiện bài báo cáo và triển khai theo đúng 3 phần sau:

#### **Phần 1: Đề xuất & Báo cáo So sánh Trade-off (Độc lập đề xuất 2 giải pháp)**
*   Độc lập đề xuất ít nhất **2 giải pháp kỹ thuật khác nhau** về mặt cấu trúc mã nguồn để giải quyết logic nghiệp vụ trên (Tuyệt đối không sao chép gợi ý hay đáp án có sẵn).
    *   *Ví dụ định hướng*: Một phương án dùng chuỗi `if...else if...else` lồng ghép; một phương án kết hợp `switch-case` rẽ nhánh hạng vé chính với toán tử ba ngôi `ternary operator` xử lý logic phụ.
*   Xây dựng **Bảng so sánh Trade-off** chi tiết giữa 2 giải pháp dựa trên 5 tiêu chí bắt buộc:
    1. Tốc độ thực thi (Time Complexity)
    2. Dung lượng bộ nhớ (Memory Footprint)
    3. Khả năng bảo trì khi thêm hạng vé mới (Maintainability)
    4. Độ dễ đọc và Clean Code (Readability)
    5. Ngữ cảnh áp dụng tối ưu (Suitability)

[NOTE] Bảng so sánh phải trình bày bằng thẻ HTML `<table>` chứa thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **Phần 2: Lý giải Chọn lựa & Thiết kế Lưu đồ Thuật toán (Flowchart)**
*   Trình bày lý do khoa học và thuyết phục để chọn ra 1 phương án tối ưu nhất trong 2 giải pháp đã đề xuất.
*   Thiết kế lưu đồ thuật toán (Flowchart) mô tả chi tiết từng bước rẽ nhánh điều kiện của phương án tối ưu bằng cú pháp **Mermaid**.
*   **Quy chuẩn bắt buộc về 5 hình dạng Mermaid**:
    1. Stadium/Oval `([Bắt đầu])`, `([Kết thúc])`: Điểm bắt đầu và kết thúc quy trình.
    2. Parallelogram `[/Đầu vào: .../]`, `[/Đầu ra: .../]`: Nhận dữ liệu tham số vào hoặc xuất kết quả.
    3. Diamond `Kiểm tra điều kiện?`: Kiểm tra rẽ nhánh với các nhãn `-->|Đúng|` và `-->|Sai|`.
    4. Rectangle `["Tính toán / Gán giá trị"]`: Thực hiện phép tính hoặc gán biến.
    5. Arrow `-->`: Mũi tên chỉ hướng luồng thực thi.

#### **Phần 3: Triển khai Mã nguồn JavaScript ES6+ & Xử lý Trường hợp Biên**
*   Hiện thực hóa phương án tối ưu bằng mã nguồn **JavaScript (ES6+)**.
*   Đặt tên biến bằng tiếng Anh, viết comment giải thích logic bằng tiếng Việt có dấu.
*   Xử lý triệt để các trường hợp dữ liệu biên (hành lý âm, hạng vé sai định dạng).
*   In kết quả tính toán chi tiết ra `console.log()` với format rõ ràng bao gồm:
    - Mã hạng vé & Kênh làm thủ tục
    - Trạng thái VIP
    - Số kg hành lý quá cước
    - Phí hành lý quá cước ban đầu
    - Tiền giảm giá VIP (nếu có)
    - Phí làm thủ tục tại quầy
    - **Tổng phụ phí cuối cùng phải thanh toán**

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (Phần 1 & Phần 2) và mã nguồn triển khai (Phần 3).
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex10`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 06_Ex10`

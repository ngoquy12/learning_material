# <center>[Phân tích 2] Phân tích và thiết kế module tính toán phiếu đặt lịch khám bệnh</center>

### **1. Mục tiêu**
*   **Phân tích & Đề xuất kiến trúc:** Đánh giá và so sánh các phương án tổ chức mã nguồn JavaScript (tệp độc lập `.js` so với mã nhúng trực tiếp) và chiến lược quản lý biến số ES6 (`const`/`let`) trong phân hệ xử lý phiếu đặt lịch khám bệnh.
*   **Tối ưu hóa cơ chế thực thi V8 Engine:** Hiểu rõ cách V8 Engine nạp HTML, phân tích (Parser) và biên dịch Bytecode (Ignition) để đưa ra thiết kế mã nguồn tối ưu tốc độ và bộ nhớ.
*   **Xử lý kiểu dữ liệu An toàn:** Kiểm soát và loại bỏ triệt để lỗi sai lệch kiểu dữ liệu (nối chuỗi ngoài ý muốn từ dữ liệu đầu vào `prompt()`) thông qua ép kiểu minh bạch với `Number()`.
*   **Đóng gói Chuỗi & Tương tác DOM:** Áp dụng chuẩn Template Literals để tạo thông điệp xác nhận lịch khám chuyên nghiệp và hiển thị lên giao diện web thông qua thuộc tính `textContent` của DOM.

---

### **2. Bối cảnh & Vấn đề**
Phòng khám Đa khoa Quốc tế Rikkei Care đang triển khai nâng cấp hệ thống đặt lịch khám bệnh tự động (`CLINIC_APPOINTMENT`). Phân hệ hiện tại cần tiếp nhận thông tin đăng ký từ bệnh nhân, tính toán chi phí khám bệnh thực tế sau khi áp dụng tỷ lệ miễn giảm bảo hiểm y tế (BHYT), cộng phí dịch vụ đặt lịch trực tuyến, và hiển thị phiếu xác nhận ra màn hình console cũng như giao diện HTML.

Tuy nhiên, đội ngũ phát triển đang gặp bế tắc trong việc lựa chọn kiến trúc mã nguồn và chiến lược quản lý biến số:
1. Một số lập trình viên sử dụng cách nhúng mã lệnh trực tiếp vào các sự kiện HTML và dùng biến `var` toàn cục, dẫn đến tình trạng ô nhiễm scope, lỗi gán đè biến và khiến V8 Engine không thể tái sử dụng Bytecode đã biên dịch.
2. Dữ liệu nhận từ hàm `prompt()` trả về dạng chuỗi (`String`), nếu không xử lý ép kiểu đúng lúc sẽ dẫn đến lỗi logic cộng chuỗi (ví dụ: giá khám `200000` cộng phí ship `30000` thành `"20000030000"`).

Hệ thống yêu cầu bạn - trong vai trò Lập trình viên Frontend Chuyên nghiệp - phải tự nghiên cứu, đề xuất các giải pháp kỹ thuật khả thi, lập bảng phân tích so sánh các điểm đánh đổi (Trade-offs), lựa chọn phương án tối ưu nhất và triển khai mã nguồn hoàn chỉnh.---

### **3. Quy tắc nghiệp vụ**
Dữ liệu đầu vào và các quy tắc tính toán của phân hệ đặt lịch khám (`CLINIC_APPOINTMENT`) được quy định cụ thể như sau:

*   **Quy tắc 1 (Tiếp nhận thông tin):** Tiếp nhận 5 thông tin cơ bản từ người dùng:
    *   Tên bệnh nhân (`patientName`): Chuỗi ký tự đại diện cho họ tên.
    *   Tên chuyên khoa (`specialtyName`): Chuỗi ký tự (ví dụ: `"Nội khoa"`, `"Nhi khoa"`).
    *   Chi phí khám gốc (`baseExamFee`): Số tiền khám ban đầu (đơn vị: VNĐ).
    *   Tỷ lệ giảm giá BHYT (`insuranceDiscountRate`): Số thập phân thể hiện tỷ lệ miễn giảm (ví dụ: `0.8` tương ứng giảm 80% tiền khám ban đầu).
    *   Phí dịch vụ đặt lịch (`bookingServiceFee`): Phí cố định cho mỗi lượt đặt lịch trực tuyến (đơn vị: VNĐ).
*   **Quy tắc 2 (Ép kiểu dữ liệu minh bạch):** Tất cả các giá trị số nhận về từ hàm `prompt()` đều ở dạng chuỗi, bắt buộc phải được chuyển đổi sang kiểu `Number` trước khi thực hiện các phép tính số học.
*   **Quy tắc 3 (Công thức tính toán):**
    *   Chi phí khám sau khi giảm giá BHYT: `discountedFee = baseExamFee * (1 - insuranceDiscountRate)`
    *   Tổng chi phí thanh toán thực tế: `totalPayment = discountedFee + bookingServiceFee`
*   **Quy tắc 4 (Quy chuẩn khai báo biến ES6):**
    *   Tuyệt đối không sử dụng từ khóa `var`.
    *   Sử dụng `const` cho các giá trị hằng số không thay đổi (tên phòng khám, định danh tiền tệ `"VNĐ"`, thông tin định danh bệnh nhân).
    *   Sử dụng `let` cho các biến có giá trị thay đổi hoặc biến tính toán trung gian.
    *   Tên biến phải tuân thủ chuẩn `camelCase` bằng tiếng Anh.
*   **Quy tắc 5 (Hiển thị kết quả):**
    *   Sử dụng chuỗi Template Literals (

``` `...${var}...`
```

) để đóng gói toàn bộ phiếu xác nhận lịch khám.
    *   Ghi kết quả ra Developer Console bằng `console.log()`.
    *   Cập nhật nội dung hiển thị trên giao diện trang web HTML bằng thuộc tính DOM `document.getElementById(...).textContent`.

---

### **4. Yêu cầu bài toán**

Học viên thực hiện bài nộp theo đúng 3 phần phân tích và triển khai chi tiết:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & Ma trận So sánh Trade-off**
*   Tự độc lập nghiên cứu và đề xuất ít nhất **2 phương án kỹ thuật khác nhau** để giải quyết bài toán trên (về cấu trúc mã nguồn HTML/JS, vị trí đặt thẻ `<script>`, chiến lược ép kiểu dữ liệu `Number()` và quản lý biến `let`/`const`).
*   [REQUIREMENT] Không viết sẵn hoặc liệt kê trước tên phương án trong đề bài; học viên phải tự định nghĩa và mô tả điểm khác biệt bản chất giữa các phương án.
*   Lập bảng ma trận so sánh các điểm đánh đổi (Trade-off Matrix) giữa các phương án theo 5 tiêu chí:
    1. Tốc độ thực thi & Tối ưu V8 Engine (Speed & V8 Bytecode Optimization)
    2. Dung lượng & Quản lý bộ nhớ RAM (Memory Usage)
    3. Khả năng bảo trì & Mở rộng mã nguồn (Maintainability)
    4. Độ rõ ràng & Dễ đọc của mã nguồn (Readability)
    5. Mức độ phù hợp với quy chuẩn Doanh nghiệp (Enterprise Suitability)
*   [REQUIREMENT] Bảng so sánh HTML phải tuân thủ thuộc tính định dạng: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Sơ đồ Luồng (Flowchart)**
*   Đưa ra lập luận kỹ thuật khoa học để giải thích lý do lựa chọn phương án tối ưu nhất (dựa trên cơ chế V8 Engine Parser/Ignition và quy tắc Clean Code ES6).
*   Xây dựng sơ đồ luồng tiến trình (Mermaid Flowchart) biểu diễn quy trình từ khi trang web được tải, nạp tệp JS, nhận dữ liệu `prompt()`, ép kiểu `Number()`, tính toán chi phí, đến khi hiển thị kết quả lên DOM và Console.
*   [REQUIREMENT] Sơ đồ Mermaid phải tuân thủ nghiêm ngặt 5 hình khối chuẩn:
    1. Hình Stadium `([Bắt đầu / Kết thúc])` cho điểm khởi chạy và kết thúc.
    2. Hình Parallelogram `[/Đầu vào / Đầu ra/]` cho thao tác `prompt()` và xuất `console.log()` / `textContent`.
    3. Hình Diamond `Kiểm tra điều kiện?` với các nhánh `-->|Đúng|` / `-->|Sai|` nếu có bước kiểm tra.
    4. Hình Rectangle `["Thực hiện hành động / Tính toán"]` cho các phép tính toán số học và gán biến.
    5. Đường nối mũi tên `-->` thể hiện luồng thực thi tuyến tính.

#### **Phần 3: Triển khai Mã nguồn & Phòng ngừa Lỗi**
*   Tạo cấu trúc dự án gồm 2 tệp: `index.html` và `app.js`.
*   Viết mã HTML5 chuẩn semantic, liên kết tệp `app.js` bên ngoài ở trước thẻ đóng `</body>`.
*   Viết mã JavaScript trong `app.js` thực thi phương án tối ưu đã chọn:
    *   Nhập đầy đủ thông tin bệnh nhân qua `prompt()`.
    *   Ép kiểu dữ liệu an toàn bằng `Number()`.
    *   Tính toán đúng theo Quy tắc 3.
    *   Đóng gói thông điệp phiếu khám bằng Template Literals.
    *   Cập nhật thông điệp lên DOM qua `textContent` và in ra `console.log()`.
*   Đảm bảo mã nguồn phòng ngừa triệt để các lỗi logic biên: lỗi ô nhiễm scope (`var`), lỗi gán lại hằng số (`TypeError`), lỗi nối chuỗi ngoài ý muốn.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 02_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 02_Ex11`

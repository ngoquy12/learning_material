# [Vận dụng cơ bản 1] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng mã nguồn thực hiện phép cộng chuỗi `baseFeeInput + specialistFeeInput` chưa ép kiểu trong file `app.js`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ các dòng còn thiếu trong bảng Test Case chứng minh kết quả bị nối chuỗi sai so với thực tế kỳ vọng.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng hàm `Number()` để ép kiểu dữ liệu từ `prompt()` sang kiểu số, giúp phép tính tổng tiền khám bệnh chính xác.
*   **[20 điểm] Sử dụng Template Literals chuẩn ES6:** Chuyển đổi mã nguồn ghép chuỗi bằng toán tử `+` sang cú pháp Template Literals `${...}` minh bạch, dễ bảo trì.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Thực hiện chuyển đổi kiểu dữ liệu một cách minh bạch ngay tại bước nhập liệu hoặc bước tính toán số học.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo chương trình chạy mượt mà trên môi trường trình duyệt console mà không xảy ra lỗi runtime hay đứt gãy luồng thực thi.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được lý do hàm `prompt()` trong JavaScript luôn trả về giá trị kiểu String và cơ chế ép kiểu ngầm định (implicit coercion) của toán tử `+`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến chuẩn camelCase, mã nguồn tuân thủ tiêu chuẩn ES6 (`let`/`const`), thụt lề nhất quán.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex1`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu định dạng hiển thị:** Định dạng lại hiển thị số tiền có dấu phân cách hàng nghìn hoặc kiểm tra tính hợp lệ của dữ liệu đầu vào.

---

## [Vận dụng cơ bản 2] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng code thực hiện phép cộng biến chưa qua ép kiểu dữ liệu làm sai lệch logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành chính xác các ô còn trống (`...`) trong bảng Test Case với dữ liệu thực tế và kỳ vọng chính xác.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Tính chính xác tổng tiền thanh toán là phép cộng số học của phí khám và phí sổ khám (`consultationFee + cardFee`).
*   **[20 điểm] Ép kiểu dữ liệu an toàn:** Áp dụng đúng hàm `Number()` ngay sau khi nhận dữ liệu từ `prompt()` hoặc trước khi tính toán.

#### **3. Kiểm chuẩn dữ liệu & Xử lý xuất kết quả — 20 điểm**
*   **[10 điểm] Sử dụng Template Literals:** Định dạng câu thông báo kết quả bằng cú pháp `` `${...}` `` sạch đẹp, dễ đọc, không dùng nối chuỗi rườm rà.
*   **[10 điểm] Hiển thị kết quả đa kênh:** Xuất thông báo đầy đủ ra Developer Console (`console.log`) và cửa sổ thông báo (`alert`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ lý do hàm `prompt()` luôn trả về kiểu dữ liệu String và lý do từ khóa `var` không còn được khuyến khích trong ES6.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Áp dụng đúng quy tắc đặt tên `camelCase`, khai báo chuẩn `const`/`let`, có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tải mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex2`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý giá trị mặc định:** Bổ sung logic gán giá trị mặc định bằng `0` nếu người dùng bấm Cancel hoặc để trống ô nhập phí sổ khám.

---

## [Vận dụng cơ bản 3] Sửa lỗi tính tổng tiền khám bệnh và xuất phiếu thông báo

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi tính tổng tiền khám bệnh và xuất phiếu thông báo — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code `var totalFee = consultationFee + testingFee;` thực hiện phép cộng trên hai chuỗi chưa ép kiểu.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ thông tin dòng 2 và dòng 3 trong bảng Test Case (đầu ra bị lỗi, đầu ra mong đợi, vị trí dòng lỗi và nguyên nhân logic về kiểu dữ liệu String).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Ép kiểu dữ liệu chính xác:** Áp dụng `Number()` ép kiểu thành công cho hai tham số chi phí đầu vào, tính toán chính xác tổng chi phí thanh toán (ví dụ: `200000 + 50000 = 250000`).
*   **[20 điểm] Chuẩn hóa biến ES6 và Naming Convention:**
    *   Loại bỏ 100% từ khóa `var`.
    *   Sử dụng đúng `const` cho các giá trị không bị gán lại và `let` cho các biến thay đổi.
    *   Đổi tên biến `Patient_Name` thành `patientName` chuẩn `camelCase`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Sử dụng Template Literals:** Đóng gói chuỗi thông báo kết quả sạch đẹp, dễ đọc bằng dấu backticks `` `...${}...` ``.
*   **[10 điểm] Hiển thị kết quả ra DOM & Console:** Xuất đúng thông tin thông báo phiếu khám ra Developer Console và gán thành công vào thuộc tính `textContent` của thẻ HTML có id `appointment-summary`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế trả về dữ liệu của hàm `prompt()` trong trình duyệt luôn là kiểu `String` và sự khác biệt giữa phép toán `+` khi thao tác với String (nối chuỗi) so với Number (cộng số học).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn Javascript trình bày rõ ràng, thụt lùi dòng chuẩn, có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tạo đúng cấu trúc tệp `index.html` và `app.js`, đẩy lên GitHub repository theo định dạng thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu hóa nhập liệu:** Thực hiện ép kiểu trực tiếp `Number(prompt(...))` gọn gàng ngay tại thời điểm khai báo biến.

---

## [Vận dụng cơ bản 4] Sửa lỗi tính tổng chi phí đăng ký khám bệnh tự động

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính tổng chi phí đăng ký khám bệnh tự động — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng vị trí dòng khai báo/gán biến `specialistSurcharge` chưa được chuyển đổi kiểu dữ liệu từ Chuỗi sang Số.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện chính xác 100% các ô thông tin còn thiếu (`...`) trong dòng STT 2 và STT 3 của bảng báo cáo kiểm thử.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công phép cộng số học, đảm bảo tổng chi phí khám bệnh tính toán chính xác tuyệt đối.
*   **[20 điểm] Ép kiểu dữ liệu minh bạch:** Áp dụng đúng hàm `Number()` cho toàn bộ dữ liệu số nhập từ `prompt()`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Định dạng chuỗi kết quả chuẩn xác:** Sử dụng cú pháp Template Literals `${...}` để ghép chuỗi hóa đơn đầy đủ thông tin bệnh nhân, tiền khám, phụ phí và tổng tiền.
*   **[10 điểm] Xuất dữ liệu đa kênh:** Thực thi đúng việc xuất dữ liệu đồng thời ra cả `console.log()` và `alert()`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế ép kiểu ngầm định (implicit type coercion) của toán tử `+` trong JavaScript khi có ít nhất một toán hạng là kiểu `String`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn camelCase (`patientName`, `baseFee`, `specialistSurcharge`, `totalFee`), sử dụng `const`/`let` đúng phạm vi và đúng mục đích.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc tên thư mục quy định `[Tên Lớp]_[Môn Học]_Session02_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý dữ liệu không hợp lệ:** Thêm đoạn mã kiểm tra nếu giá trị chuyển đổi bằng `NaN` (ví dụ bệnh nhân nhập chữ thay vì số) thì thông báo cảnh báo nhập sai dữ liệu.

---

## [Vận dụng cơ bản 5] Sửa lỗi tính tổng chi phí dịch vụ đặt lịch khám bệnh

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính tổng chi phí dịch vụ đặt lịch khám bệnh — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng code thực hiện phép tính `totalPayment` thiếu ép kiểu số từ `prompt()`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác các giá trị bị lỗi (Buggy Output), giá trị mong đợi (Expected Output) và giải thích nguyên nhân cho 2 trường hợp Test Case còn lại trong bảng.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi chính xác dữ liệu đầu vào bằng `Number()` giúp tính tổng chi phí khám bệnh chính xác trong mọi tình huống.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Tách biệt rõ ràng biến nhận dữ liệu chuỗi từ `prompt()` và biến lưu giá trị số sau khi ép kiểu (hoặc ép kiểu ngay tại câu lệnh nhập).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo dữ liệu nhập từ `prompt()` được xử lý an toàn, tránh lỗi tính toán ra `NaN` khi dữ liệu rỗng.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Định dạng thông điệp xuất ra bằng Template Literals đúng cú pháp ES6, không gây lỗi cú pháp hiển thị.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ cơ chế ép kiểu ngầm định (Implicit Type Coercion) trong JavaScript khi kết hợp toán tử số học `+` giữa các kiểu dữ liệu `Number` và `String`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết sạch đẹp, đặt tên biến theo chuẩn `camelCase`, tuyệt đối không dùng từ khóa cũ `var`.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub theo đúng cấu trúc thư mục được yêu cầu: `[Tên Lớp]_[Môn Học]_Session02_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Bổ sung kiểm tra hợp lệ:** Viết thêm câu lệnh kiểm tra giá trị nhập vào nếu không phải là số hợp lệ (`isNaN`) thì cảnh báo người dùng nhập lại.

---

## [Vận dụng cơ bản 6] Sửa lỗi tính tổng chi phí đăng ký khám bệnh

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính tổng chi phí đăng ký khám bệnh — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng thực hiện phép cộng hai biến kiểu String trả về từ `prompt()` mà chưa qua ép kiểu `Number()`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ 2 trường hợp kiểm thử còn thiếu (STT 2 và STT 3) trong bảng HTML với đầy đủ các cột Input, Buggy Output, Expected Output, Dòng code lỗi và Giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa tệp mã nguồn để thực hiện chính xác phép cộng số học giữa phí khám và phí dịch vụ bổ sung, cho ra tổng tiền thanh toán chuẩn xác.
*   **[20 điểm] Ép kiểu dữ liệu minh bạch:** Sử dụng hàm `Number()` đúng vị trí khi đọc giá trị từ `prompt()` để chuyển đổi từ dạng chuỗi sang dạng số.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Tối ưu hóa luồng nhập dữ liệu:** Đảm bảo mã nguồn ngắn gọn, dễ đọc, ép kiểu trực tiếp hoặc gián tiếp một cách nhất quán.
*   **[10 điểm] Sử dụng chuỗi Template Literals chuẩn xác:** Sử dụng cú pháp dấu backtick (`` ` ``) và biểu thức `${}` để đóng gói chuỗi thông báo kết quả hóa đơn chuyên nghiệp.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Giải thích nguyên nhân lỗi toán tử `+`:** Trả lời rõ ràng cơ chế ép kiểu tự động (implicit type coercion) của JavaScript khi gặp toán tử `+` với dữ liệu kiểu String.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến theo chuẩn `camelCase`, mã nguồn trình bày ngắn gọn, thụt lùi dòng nhất quán, comment giải thích rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex6`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Kiểm tra trường hợp nhập NaN:** Bổ sung logic kiểm tra giá trị người dùng nhập vào nếu không phải là số hợp lệ thì cảnh báo hoặc gán giá trị mặc định là 0.

---

## [Vận dụng nâng cao 1] Tính Toán Chi Phí Khám Bệnh Và Xác Nhận Đặt Lịch Phòng Khám

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Tính Toán Chi Phí Khám Bệnh Và Xác Nhận Đặt Lịch Phòng Khám — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định chính xác các tham số đầu vào (`patientName`, `patientAge`, `baseExamFee`, `insuranceDiscountRate`), hằng số (`serviceFee`) và đầu ra (`totalPayment`, phiếu xác nhận) cùng kiểu dữ liệu tương ứng (`String`, `Number`, `Boolean`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày giải pháp logic mạch lạc và vẽ sơ đồ Mermaid tuân thủ đúng 5 dạng hình tiêu chuẩn (Terminator, Input/Output, Decision, Process, Flowline).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo đúng phạm vi biến ES6 (`const` cho hằng số cố định như phí dịch vụ, `let` cho giá trị tính toán), đặt tên biến chuẩn `camelCase` bằng tiếng Anh rõ nghĩa.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác số tiền BHYT chi trả, giá khám thực tế và tổng chi phí thanh toán theo quy tắc nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Thực hiện ép kiểu minh bạch với `Number()` cho các dữ liệu số từ `prompt()`, phòng ngừa tuyệt đối lỗi cộng chuỗi ngoài ý muốn (ví dụ: `"150000" + "30000"` thành `"15000030000"`).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Xử lý dữ liệu nhập vào hợp lý, tránh các trường hợp tính toán sai lệch khi giá trị BHYT hoặc chi phí khám không phải số hợp lệ.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Định dạng chuỗi Template Literals đa dòng đầy đủ thông tin hóa đơn xác nhận và xuất đồng thời ra cả `console.log()` lẫn `alert()`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn sạch đẹp, định dạng thụt lề chuẩn xác, tách biệt HTML và JavaScript (`<script src="app.js"></script>`), có chú thích Tiếng Việt rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Đẩy toàn bộ mã nguồn lên thư mục GitHub theo đúng cấu trúc tên bài tập quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Trình bày thông tin xác nhận hóa đơn dưới dạng bảng kết quả chuyên nghiệp trong Developer Console bằng `console.table()` bên cạnh dạng chuỗi văn bản thông thường.

---

## [Vận dụng nâng cao 2] Tính toán Chi phí và Xuất Phiếu Đăng ký Khám bệnh Tự động

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Tính toán Chi phí và Xuất Phiếu Đăng ký Khám bệnh Tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ các tham số đầu vào (`patientId`, `patientName`, `patientAge`, `baseFee`, `labFee`, `insuranceDiscountRate`) cùng kiểu dữ liệu ban đầu (`string`) và kiểu dữ liệu sau ép kiểu (`number`), đầu ra xuất ra Console & Alert.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày rõ phương án ép kiểu dữ liệu bằng `Number()`, quy tắc dùng `const`/`let` và sơ đồ luồng Mermaid đầy đủ các bước thực hiện.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo chính xác các biến và hằng số theo chuẩn ES6 `camelCase`, phân định hợp lý giữa `const` (đơn giá cố định, kết quả tính toán) và `let` (biến có thể thay đổi).
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác tổng chi phí dịch vụ, số tiền BHYT chi trả, tổng thanh toán thực tế và biểu thức kiểm tra ưu tiên cao tuổi.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Ép kiểu minh bạch toàn bộ các tham số tài chính số (`Number(...)`), triệt tiêu hoàn toàn lỗi nối chuỗi `string + string` của `prompt()`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Đảm bảo thứ tự nhận dữ liệu logic, xử lý dữ liệu đầu vào an toàn, đúng kiểu dữ liệu mục tiêu trước khi thực hiện phép tính số học.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất dữ liệu phiếu tiếp nhận bằng Template Literals với định dạng đẹp mắt, bố cục rõ ràng trên Console và thông báo Alert súc tích.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn viết hoàn toàn bằng tên Tiếng Anh (`camelCase`), ghi chú giải thích bằng Tiếng Việt có dấu, cấu trúc HTML/JS tách biệt chuẩn V8 Engine (`script` đặt trước `</body>`).
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đẩy mã nguồn lên GitHub đúng định dạng tên thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex8`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Trình bày sơ đồ luồng Mermaid minh họa chính xác 5 dạng hình khối tiêu chuẩn (Oval, Parallelogram, Rectangle, Diamond, Arrow) và giải thích được cơ chế V8 Engine biên dịch Bytecode tối ưu khi tách riêng file `.js`.

---

## [Vận dụng nâng cao 3] Tính toán Chi phí và Xuất Phiếu Khám Bệnh Tự động

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Tính toán Chi phí và Xuất Phiếu Khám Bệnh Tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Phân tích đầy đủ tất cả các tham số đầu vào (`patientName`, `birthYear`, `baseFee`, `hasInsurance`, `serviceFee`) và đầu ra (`patientAge`, `insuranceDiscount`, `totalPayment`, `isPriority`), xác định đúng kiểu dữ liệu nguyên thủy cho từng biến.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ sơ đồ Mermaid Flowchart thể hiện chính xác luồng xử lý từ nhập liệu, ép kiểu `Number`, tính toán tài chính đến đóng gói chuỗi Template Literals. Tuân thủ 100% quy tắc 5 hình dạng chuẩn (không dùng sai hình bình hành cho bước tính toán).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo hằng số hệ thống (`currentYear = 2026`, `insuranceDiscountRate = 0.8`, `priorityAgeThreshold = 70`) bằng từ khóa `const`. Khai báo biến lưu giữ kết quả tính toán bằng `let`. Đặt tên biến 100% chuẩn `camelCase` bằng tiếng Anh.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác tuổi bệnh nhân, tiền giảm trừ BHYT (80% nếu `hasInsurance = 1`, 0% nếu `hasInsurance = 0`), phụ phí và tổng chi phí thanh toán cuối cùng.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Thực hiện ép kiểu dữ liệu đầu vào minh bạch ngay khi nhận dữ liệu từ `prompt()` bằng `Number()`, ngăn ngừa tuyệt đối lỗi cộng nối chuỗi ngầm định (ví dụ: `"150000" + "30000" = "15000030000"`).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Xử lý chính xác trường hợp năm sinh hoặc chi phí bị nhập sai định dạng thành `NaN`, đảm bảo kết quả phép tính toán học không bị sai lệch dữ liệu.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất báo cáo phiếu xác nhận khám đầy đủ, chuyên nghiệp thông qua chuỗi Template Literals với định dạng rõ ràng, hiển thị đồng thời ở `console.log()` và `alert()`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn viết sạch sẻ, có chú thích giải thích logic bằng tiếng Việt có dấu, nhúng tệp script ngoài ở trước thẻ đóng `</body>` trong file `index.html`.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên kho lưu trữ GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex9`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Trình bày mã nguồn tối ưu, đóng gói biểu thức logic kiểm tra điều kiện ưu tiên trực tiếp trong chuỗi nội dung xuất mà không tạo thêm các biến trung gian thừa thải.

---

## [Phân tích 1] Phân tích và Thiết kế Module Tính Chi phí Khám bệnh Ban đầu

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân tích và Thiết kế Module Tính Chi phí Khám bệnh Ban đầu — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Đề xuất được 2 phương án có sự khác biệt rõ ràng về cấu trúc quản lý biến (`const`/`let` độc lập vs gộp biến xử lý), thời điểm ép kiểu dữ liệu `Number()` (ngay khi nhập vs khi tính toán) và vị trí gắn file mã nguồn JS.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Lập bảng so sánh 5 tiêu chí (Hiệu năng V8, Bộ nhớ, Tính bảo trì, Khả năng chống bẫy nối chuỗi, Bối cảnh phù hợp). Bảng HTML được định dạng đúng thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Trình bày lý do chọn phương án tối ưu dựa trên khả năng bảo vệ phạm vi biến (Block Scope), tối ưu hóa bộ nhớ RAM và tuân thủ nguyên tắc Clean Code.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày sơ đồ luồng Mermaid đầy đủ. Ký hiệu đúng 100% chuẩn hình dạng (Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Process/Calculation).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết tệp `index.html` và `app.js` chuẩn HTML5 và ES6+. Liên kết script chính xác ở cuối thẻ `<body>`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Sử dụng `Number()` ép kiểu rõ ràng ngay từ đầu vào thu thập từ `prompt()`, tính đúng tuổi bệnh nhân theo năm 2026 và tính chính xác chi phí khám thực tế với phép nhân tỷ lệ miễn giảm `baseFee * (1 - insuranceDiscountRate)`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Sử dụng đúng chuỗi Template Literals (dấu backticks `` ` ``) để nhúng biến số. Hiển thị thông báo phiếu khám bệnh đồng nhất trên cả `console.log` và `alert`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến bằng tiếng Anh chuẩn `camelCase` (ví dụ: `patientName`, `birthYear`, `baseFee`, `insuranceDiscountRate`), tuyệt đối không dùng `var`, chú thích mã nguồn bằng tiếng Việt rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn repository công khai, đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session02_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script / Phân tích V8 Engine:** Viết mã phân tích hoặc giải thích chi tiết cơ chế V8 Engine xử lý Variable Hoisting với `var` so với Temporal Dead Zone (TDZ) của `let`/`const` ảnh hưởng thế nào đến độ an toàn của ứng dụng phòng khám.

---

## [Phân tích 2] Phân tích và thiết kế module tính toán phiếu đặt lịch khám bệnh

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Phân tích và thiết kế module tính toán phiếu đặt lịch khám bệnh — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Tự đề xuất và trình bày rõ ràng ít nhất 2 phương án thiết kế kiến trúc mã nguồn khác nhau (ví dụ: phân tích sự khác biệt giữa việc tách tệp `app.js` độc lập kết nối cuối `body` so với nhúng mã trực tiếp; hoặc so sánh việc ép kiểu `Number()` ngay khi nhận đầu vào từ `prompt()` so với việc giữ chuỗi thô rồi ép kiểu trong biểu thức tính toán).
    *   Nêu rõ ưu/nhược điểm cấu trúc của từng giải pháp dựa trên phạm vi kiến thức đã học (V8 Engine, ES6 Variables).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Xây dựng bảng ma trận so sánh đầy đủ 5 tiêu chí (Tốc độ thực thi, Bộ nhớ RAM, Khả năng bảo trì, Độ rõ ràng, Mức độ phù hợp).
    *   Bảng HTML có thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lý giải thuyết phục dựa trên cơ chế hoạt động của V8 Engine (tách tệp `.js` giúp V8 Engine cache Bytecode tối ưu) và quy chuẩn tránh ô nhiễm scope/tránh biến toàn cục.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ sơ đồ Mermaid thể hiện chính xác luồng xử lý của phương án chọn.
    *   Tuân thủ nghiêm ngặt chuẩn 5 hình khối: Stadium `([ ])` cho Start/End, Parallelogram `[/ /]` cho I/O (`prompt`, `console`/DOM), Rectangle `[" "]` cho tính toán toán học/gán biến, Diamond cho bước kiểm tra (nếu có), Mũi tên `-->` kết nối.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Tạo file `index.html` và `app.js` liên kết chuẩn xác ở cuối thẻ `body`.
    *   Khai báo biến chuẩn ES6 (`const` cho hằng số không đổi, `let` cho biến tính toán/thay đổi, tuyệt đối không dùng `var`).
    *   Thực hiện ép kiểu dữ liệu đầu vào bằng `Number()` chính xác.
    *   Tính toán đúng chi phí khám sau BHYT và tổng chi phí thanh toán theo công thức nghiệp vụ.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Ngăn chặn triệt để lỗi cộng chuỗi (`"200000" + "30000"`).
    *   Không xảy ra lỗi gán lại hằng số (`TypeError`).
    *   Không gây lỗi truy cập phần tử DOM null (do đặt script đúng vị trí sau khi HTML render).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Sử dụng chuỗi Template Literals để tạo thông điệp phiếu khám đầy đủ thông tin: Tên bệnh nhân, Chuyên khoa, Chi phí gốc, Số tiền giảm BHYT, Phí dịch vụ, và Tổng thanh toán thực tế.
    *   Xuất kết quả đồng thời ra `console.log()` và hiển thị thành công lên giao diện HTML bằng thuộc tính DOM `textContent`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến sử dụng chuẩn `camelCase` bằng tiếng Anh rõ nghĩa (`patientName`, `baseExamFee`, `insuranceDiscountRate`, `bookingServiceFee`, `totalPayment`).
    *   Chú thích mã nguồn bằng tiếng Việt có dấu chuẩn sản xuất.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn kho chứa GitHub hợp lệ, cấu trúc thư mục đúng quy chuẩn: `[Tên Lớp]_[Môn Học]_SessionSession 02_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Đoạn mã Đo kiểm Hiệu năng (Benchmark Script):**
    *   Sử dụng `console.time()` và `console.timeEnd()` trong môi trường Node.js / Browser Console để đo đạc và so sánh thời gian xử lý việc tạo chuỗi thông điệp phiếu khám giữa phương pháp nối chuỗi toán tử `+` cổ điển và phương pháp dùng Template Literals ES6.

---

## [Phân tích 3] Phân tích và thiết kế mô-đun tính chi phí và tạo phiếu xác nhận khám bệnh

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Phân tích và thiết kế mô-đun tính chi phí và tạo phiếu xác nhận khám bệnh — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự đề xuất và mô tả rõ ràng sự khác biệt về cấu trúc logic giữa 2 phương án (ví dụ: Phương án ép kiểu trực tiếp tại đầu vào vs Phương án lưu chuỗi thô rồi ép kiểu khi tính toán; hoặc Phương án quản lý biến đơn lẻ vs Phương án gộp bước).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Thiết lập bảng so sánh HTML đầy đủ 5 tiêu chí (Tốc độ xử lý, Bộ nhớ, Bảo trì, Độ đọc hiểu, Tuân thủ ES6) có định dạng bảng đúng chuẩn quy định (`style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`).

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Trình bày lập luận kỹ thuật thuyết phục cho phương án được chọn (tại sao chọn ép kiểu minh bạch `Number()` ngay từ đầu, tại sao dùng `const` thay vì `let` cho các hằng số tính toán).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày lưu đồ Mermaid đúng cú pháp và đúng 5 hình khối tiêu chuẩn (Terminator, Parallelogram cho IO, Rectangle cho Process, Diamond cho Decision).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết đầy đủ mã nguồn JavaScript trong tệp `app.js`, liên kết đúng cách với `index.html`. Áp dụng chính xác cú pháp ES6 (`let`, `const`, Template Literals).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Kiểm tra và xử lý thỏa đáng trường hợp dữ liệu đầu vào bị `NaN`, âm, hoặc chuỗi rỗng trước khi tính toán.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Kết quả xuất ra Developer Console và Alert hiển thị đầy đủ thông tin phiếu xác nhận (Mã bệnh nhân, Tên, Chi phí gốc, Tiền miễn giảm BHYT, Phí ưu tiên, Tổng thanh toán) dạng chuỗi nhiều dòng minh bạch.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến bằng tiếng Anh theo quy tắc `camelCase` (ví dụ: `patientId`, `baseExamFee`, `totalPayment`), mã nguồn sạch đẹp, có ghi chú giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn repository GitHub hợp lệ, đúng cấu trúc thư mục yêu cầu và lịch sử commit rõ ràng.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản kiểm thử hiệu năng/Validation:** Đóng gói đoạn mã kiểm thử tính chính xác của phép tính với nhiều trường hợp dữ liệu đầu vào khác nhau (BHYT 0%, BHYT 80%, có/không có phí ưu tiên).

---

## [Sáng tạo 1] Thiết kế mô-đun tiếp nhận bệnh nhân và dự tính chi phí khám

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế mô-đun tiếp nhận bệnh nhân và dự tính chi phí khám — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ bảng biến Input/Output chuẩn ES6 (`camelCase`), xác định rõ kiểu dữ liệu (`String`, `Number`) và mô tả mục đích nghiệp vụ.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê ít nhất 3 bẫy dữ liệu thực tế (nhập chuỗi không hợp lệ vào prompt số, bấm hủy prompt trả về null, cộng chuỗi do quên ép kiểu `Number()`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid đúng chuẩn kỹ thuật 5 hình khối (Oval `([ ])`, Bình hành `[/ /]`, Thoi `?`, Chữ nhật `[" "]`), thể hiện đúng luồng dữ liệu từ Kiosk nhập vào đến khi xuất thông báo.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ ràng các bước chuyển đổi dữ liệu từ dạng Chuỗi (`String`) sang Số (`Number`) và đóng gói thành Chuỗi kết quả (`Template Literals`).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Khai báo biến `const`/`let` chuẩn xác, thực hiện các phép tính số học (tổng phí, giảm trừ BHYT, tiền thanh toán) đúng công thức nghiệp vụ.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Đóng gói thông tin phiếu đăng ký chuyên nghiệp bằng Template Literals (`${}`), hiển thị chính xác kết quả qua `console.log()` và `alert()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xử lý ép kiểu an toàn với `Number()`, có lời nhắn hướng dẫn rõ ràng trên giao diện prompt/alert khi dữ liệu chưa hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết bằng ES6+, phân tách HTML và JS chuyên nghiệp qua thẻ `<script src="app.js"></script>`, tên biến tiếng Anh rõ nghĩa (`patientName`, `baseFee`, `totalPayment`).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy đủ file `index.html`, `app.js` và báo cáo thiết kế lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Trình bày chi tiết log kiểm toán (audit log) định dạng đẹp mắt trong `console.log` sử dụng định dạng chuỗi nhiều dòng bằng Template Literals.

---

## [Sáng tạo 2] Thiết kế hệ thống cấp số thứ tự và tính chi phí khám bệnh

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế hệ thống cấp số thứ tự và tính chi phí khám bệnh — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ danh mục dữ liệu đầu vào (tên bệnh nhân, tuổi, phí khám ban đầu, phí xét nghiệm, phần trăm giảm giá BHYT, ...) và dữ liệu đầu ra hiển thị trên phiếu khám bệnh.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 bẫy thực tế (nhập dữ liệu rỗng, nhập chuỗi ký tự vào ô số gây `NaN`, cộng chuỗi ngoài ý muốn nếu quên `Number()`, hoặc lỗi khai báo hằng số `const` khi cần gán lại).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid chính xác mô tả chi tiết từ lúc trình duyệt tải HTML, nạp `app.js`, tương tác `prompt()`, xử lý ép kiểu `Number()`, tính toán tài chính và xuất bằng Template Literals.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Sử dụng chính xác 100% các ký hiệu chuẩn Mermaid: Oval cho Bắt đầu/Kết thúc, Hình bình hành `[/ /]` cho Input/Output, Hình chữ nhật `[" "]` cho Process, Hình thoi cho Decision. Tuyệt đối không dùng hình bình hành cho phép tính toán.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Xây dựng hoàn chỉnh tính năng nhập liệu, tính toán tiền khám chính xác, áp dụng giảm giá BHYT hoặc phụ phí cấp sổ khám đúng theo logic tự thiết kế.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Đóng gói thông tin phiếu khám bằng chuỗi Template Literals (`` `${}` ``) định dạng đẹp mắt, rõ ràng, hiển thị chuẩn xác qua `console.log()` và `alert()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Mã nguồn triển khai việc ép kiểu minh bạch `Number()`, kiểm tra giá trị hợp lệ cơ bản trước khi tính toán để tránh lỗi phép tính ra `NaN` hoặc sai lệch chuỗi.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn ES6:** Phân định rõ ràng `const` và `let`, tuyệt đối không dùng `var`. Tên biến đặt 100% bằng tiếng Anh theo chuẩn `camelCase`. Đặt thẻ `<script>` ở cuối thẻ `<body>` của file HTML.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc tệp sạch sẽ (`index.html`, `app.js`), commit rõ ràng, README mô tả đầy đủ các bước thực thi dự án.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung việc xuất log chi tiết ở các cấp độ `console.info()`, `console.warn()`, `console.error()` để mô phỏng hệ thống Auditing quá trình tiếp đón bệnh nhân.

---

## [Sáng tạo 3] Thiết kế mô-đun tổng hợp phiếu đăng ký khám và tính chi phí phòng khám tự động

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế mô-đun tổng hợp phiếu đăng ký khám và tính chi phí phòng khám tự động — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự xây dựng bảng I/O Schema đầy đủ các trường thông tin (tên bệnh nhân, mã BHYT, tiền khám gốc, phí phụ thu, tỷ lệ giảm trừ BHYT, tổng tiền) với kiểu dữ liệu chính xác, phân định biến `const`/`let` và tên biến chuẩn `camelCase`.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích và chỉ ra ít nhất 3 bẫy lỗi tiềm ẩn (lỗi nối chuỗi do thiếu `Number()`, lỗi `TypeError` khi reassign `const`, lỗi dữ liệu `NaN` khi tính toán số học, hoặc lỗi script chặn DOM loading nếu đặt sai vị trí thẻ `<script>`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện đầy đủ vòng đời xử lý từ khi trình duyệt tải HTML, V8 Engine nạp `app.js`, thu thập `prompt()`, ép kiểu dữ liệu, tính toán chi phí, và xuất báo cáo.
*   **[10 điểm] Thiết kế chuẩn hình khối Mermaid:** Đảm bảo tuân thủ nghiêm ngặt quy tắc hình khối (Terminator `([ ])`, Input/Output `[/ /]`, Process `[" "]`, Decision `?`).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Viết mã lệnh thu thập thông tin qua `prompt()`, ép kiểu `Number()`, tính toán đúng logic chi phí khám (áp dụng giảm giá 80% BHYT cho tiền khám gốc + cộng phí dịch vụ).
*   **[15 điểm] Định dạng báo cáo chuyên nghiệp:** Đóng gói toàn bộ kết quả bằng Chuỗi mẫu (Template Literals) hiển thị thông tin phiếu khám sạch đẹp, trực quan ra `console.log()` và `alert()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xử lý ép kiểu an toàn và quản lý phạm vi biến chính xác, tránh các cạm bẫy ô nhiễm phạm vi toàn cục hoặc tính toán sai lệch do nối chuỗi `String`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn ES6:** Tách biệt rõ ràng tệp `index.html` và `app.js`. Đặt tên biến hoàn toàn bằng Tiếng Anh (`camelCase`), có chú thích bằng Tiếng Việt có dấu. Không dùng từ khóa `var`.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo repository theo đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex15`), commit mã nguồn rõ ràng và kèm tệp README hướng dẫn chạy ứng dụng qua Live Server.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung đoạn mã ghi vết nhật ký kiểm toán (Audit Log) trên Console hiển thị thời gian khởi chạy phiếu khám và kiểm tra trạng thái bộ nhớ/phiên bản Node runtime.

---

## [Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
- **Sơ đồ tiến trình thực thi (10 điểm)**: Vẽ/mô tả đầy đủ luồng tải tệp của trình duyệt và V8 Engine (Tải HTML -> Đọc thẻ script -> Nạp vào RAM -> Parser -> Ignition Bytecode).
- **Phân tích biến số & Scope (10 điểm)**: Bảng liệt kê chính xác các biến cần dùng, phân định rõ ràng biến nào dùng `const` (hằng số hệ thống), biến nào dùng `let` (dữ liệu nhập/thay đổi) và lý do không dùng `var`.

#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
- **Cấu trúc tệp & Tách biệt Logic (10 điểm)**: Tạo tệp `index.html` và `app.js` riêng biệt; nhúng script chính xác ngay trước thẻ đóng `</body>`; khởi chạy thành công qua Live Server HTTP (không chạy bằng protocol `file:///`).
- **Khai báo biến ES6 & Naming Convention (10 điểm)**: Đặt tên biến đúng chuẩn `camelCase` (ví dụ: `clinicName`, `patientName`, `consultationFee`), khai báo đúng `const`/`let`, không xảy ra lỗi Re-assignment hay Ô nhiễm Scope.
- **Xử lý Nhập/Xuất Dữ liệu (10 điểm)**: Nhận dữ liệu thành công qua `prompt()`, bật thông báo hoàn tất qua `alert()` đúng quy trình nghiệp vụ.
- **Định dạng Template Literals (10 điểm)**: Sử dụng chính xác cặp dấu backticks (`` ` ``) và cú pháp `${variable}` để đóng gói chuỗi kết quả rõ ràng, chuyên nghiệp.

#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
- **Ép kiểu dữ liệu minh bạch (10 điểm)**: Bắt buộc dùng `Number()` để chuyển đổi chuỗi số từ `prompt()` trước khi thực hiện phép tính toán học; giải thích và chứng minh được hậu quả nếu quên ép kiểu (lỗi cộng chuỗi).
- **Kiểm tra kiểu dữ liệu (10 điểm)**: Thực hiện in kết quả kiểm tra `typeof` của các biến số quan trọng ra Console để xác minh dữ liệu đã ở đúng dạng Số (`number`).

#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
- **Chú thích mã nguồn (10 điểm)**: Có comment ghi chú rõ ràng các bước thực hiện trong tệp `app.js`, giải thích logic xử lý cho từng phân đoạn nghiệp vụ.
- **Quy chuẩn cấu trúc thư mục (10 điểm)**: Đặt tên thư mục dự án đúng theo mẫu quy định `[Tên Lớp]_[Môn Học]_Session02_Demo`, mã nguồn không chứa câu lệnh thừa hoặc biến không sử dụng.

---

## [Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap)

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm (30 điểm)**
- **Phản ánh đủ 4 nhánh kiến thức cốt lõi (15 điểm)**:
  - [3.75đ] Nhánh 1: Cơ chế V8 Engine (HTML Parser -> RAM -> Ignition Bytecode), vị trí đặt thẻ `<script>`.
  - [3.75đ] Nhánh 2: Runtime Environment (Browser Console vs Node.js), Live Server HTTP vs `file:///`.
  - [3.75đ] Nhánh 3: Biến ES6 (`const`, `let`, `var`), Scope, Hoisting, Quy chuẩn đặt tên camelCase.
  - [3.75đ] Nhánh 4: Nhập/xuất dữ liệu (`prompt`, `alert`, `console.log`), ép kiểu `Number()`, Template Literals.
- **Tích hợp ngữ cảnh thực tế CLINIC_APPOINTMENT (15 điểm)**:
  - Các khái niệm và ví dụ trên sơ đồ được lồng ghép chuẩn xác vào bài toán Đặt lịch khám (ví dụ: `patientName`, `consultationFee`, `appointmentId`, tính tổng phí dịch vụ y tế).

---

#### **2. Phân tầng logic & Mối liên kết (30 điểm)**
- **Cấu trúc phân cấp mạch lạc (15 điểm)**:
  - Sơ đồ tư duy chia rõ từ Root Node (Session 02 JS Core) -> Main Branches (4 bài học) -> Sub-branches (Kiến thức chi tiết) -> Leaf Nodes (Ví dụ mã nguồn/Lỗi thường gặp).
- **Phân tích bẫy lập trình & Giải pháp (15 điểm)**:
  - Chỉ rõ các anti-patterns: Dùng `var` làm ô nhiễm scope, đặt thẻ script chặn DOM render, lỗi cộng chuỗi do quên dùng `Number()` khi đọc dữ liệu từ `prompt()`.
  - Đưa ra giải pháp chuẩn ES6 khắc phục hoàn toàn các lỗi trên.

---

#### **3. Trực quan hóa & Định dạng xuất file (20 điểm)**
- **Tính thẩm mỹ và dễ đọc (10 điểm)**:
  - Sử dụng màu sắc phân biệt giữa các nhánh logic, icon minh họa trực quan, chữ viết rõ ràng, không đè vạch liên kết.
- **Định dạng và đầy đủ file (10 điểm)**:
  - Có đủ file ảnh (`.png`/`.jpg`) chất lượng cao và file thiết kế gốc (`.xmind`/`.pdf`) trong thư mục `docs/`.

---

#### **4. Bản tóm tắt giải trình (summary.md) (10 điểm)**
- **Trình bày chuẩn Markdown (5 điểm)**:
  - Đầy đủ tiêu đề, bảng biểu so sánh (`const`/`let`/`var`), khối mã nguồn (code block) có highlight ngữ pháp JS/HTML.
- **Nội dung giải trình sâu sắc (5 điểm)**:
  - Giải thích mạch lạc luồng thực thi JS trong V8 Engine và viết được đoạn mã JS ngắn minh họa bài toán Đặt lịch khám bệnh đúng quy chuẩn ES6.

---

#### **5. Quy chuẩn nộp bài GitHub (10 điểm)**
- **Tên Repository & Cấu trúc thư mục (5 điểm)**:
  - Đặt đúng định dạng `[Tên Lớp]_[Môn Học]_Session02_Mindmap`.
  - Phân chia thư mục `docs/`, `src/` và file `summary.md` chuẩn yêu cầu.
- **Cam kết mã nguồn (Git Commits) (5 điểm)**:
  - Lịch sử commit rõ ràng, mô tả thông điệp commit đúng quy chuẩn (ví dụ: `feat: add mindmap image and summary documentation`).

---

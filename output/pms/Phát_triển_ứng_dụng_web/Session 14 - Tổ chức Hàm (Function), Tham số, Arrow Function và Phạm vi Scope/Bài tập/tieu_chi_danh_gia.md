## [Vận dụng cơ bản 1] Sửa lỗi tính tổng tiền đơn hàng vé concert trong hệ thống Ticketbox

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính tổng tiền đơn hàng vé concert trong hệ thống Ticketbox — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng mã nguồn gán gượng ép `const finalDiscount = discountRate || 0.15;` khiến giá trị `0` bị coi là falsy.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% dữ liệu chính xác cho dòng 2 và dòng 3 trong bảng báo cáo kiểm thử (Input, Buggy Output, Expected Output, Failing Line, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi thành công hàm tính tổng tiền sang cú pháp Arrow Function ES6; tính toán đúng tổng tiền cho cả 3 kịch bản (không bị trừ nhầm 15% khi discountRate = 0).
*   **[20 điểm] Sử dụng chuẩn xác ES6 Default Parameters:** Khai báo tham số mặc định trực tiếp trên chữ ký của hàm (function signature) thay vì kiểm tra bằng toán tử `||` hoặc mệnh đề `if` thủ công.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra và ném ngoại lệ khi `basePrice <= 0` hoặc `quantity <= 0`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra điều kiện biên của `discountRate` (nằm trong khoảng từ `0` đến `1`), ném ra ngoại lệ `Error` với thông điệp rõ ràng khi dữ liệu không hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn vì sao toán tử `||` không an toàn khi làm việc với dữ liệu số (number) trong JavaScript và sự khác biệt khi dùng `Default Parameters ES6`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm tiếng Anh theo chuẩn `camelCase`, comment tiếng Việt rõ ràng, mã nguồn trình bày đúng thụt lề chuẩn ES6.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session14_Ex1`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Bọc khối try...catch kiểm thử:** Viết thêm khối `try...catch` gọi hàm với dữ liệu lỗi (ví dụ: `basePrice = -100` hoặc `discountRate = 1.5`) để chứng minh ứng dụng bắt lỗi an toàn không bị crash ngột ngạt.

---

## [Vận dụng cơ bản 2] Sửa Lỗi Tính Giá Vé Concert Khi Khuyết Hoặc Tùy Chỉnh Chiết Khấu Mặc Định

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa Lỗi Tính Giá Vé Concert Khi Khuyết Hoặc Tùy Chỉnh Chiết Khấu Mặc Định — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác các dòng lệnh gán `finalDiscount` và `finalServiceFee` đang lạm dụng toán tử `||` để gán giá trị mặc định trong mã nguồn.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% dữ liệu cho các ô `...` ở STT 2 và STT 3 với Buggy Output, Expected Output, dòng code gây lỗi và giải thích rõ bản chất toán tử `||` coi số `0` là giá trị Falsy nên bị nhảy sang nhánh mặc định.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi thành công sang cú pháp Tham số mặc định ES6 chuẩn (`(basePrice, discountRate = 0.15, serviceFee = 30000) => ...`), đảm bảo tính chính xác kết quả cho cả 3 kịch bản testcase (đặc biệt khi truyền `0`).
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng câu lệnh rẽ nhánh kiểm tra dữ liệu đầu vào (`basePrice > 0`, `discountRate` từ 0 đến 1, `serviceFee >= 0`) và ném ra thông báo lỗi thích hợp bằng `throw new Error(...)`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Chặn các trường hợp truyền `basePrice` là số âm, không phải là kiểu số (`NaN`, `string`), hoặc các tham số không hợp lệ.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Hàm xử lý an toàn, không làm ứng dụng bị treo khi gặp tham số sai định dạng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ lý do vì sao trong JavaScript ES6+, việc sử dụng Tham số mặc định (Default Parameters) an toàn hơn nhiều so với toán tử logic `||` khi xử lý các tham số có thể nhận giá trị bằng `0` hoặc `false`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo chuẩn camelCase trong tiếng Anh, khai báo biến với `const`/`let`, mã nguồn có chú thích logic đầy đủ bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session14_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết bộ các câu lệnh kiểm thử tự động (sử dụng `console.assert`) để xác minh tự động tính đúng đắn của hàm `calculateTicketPayment` trên nhiều biên dữ liệu khác nhau.

---

## [Vận dụng cơ bản 3] Sửa lỗi gán tham số mặc định và scope tính tiền vé sự kiện

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi gán tham số mặc định và scope tính tiền vé sự kiện — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ các dòng code xử lý gán mặc định sai bằng toán tử `||` (`discountRate || 0.15` và `bookingFee || 20000`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ thông tin dòng 2 và dòng 3 trong bảng Test Case, tính toán chính xác Output lỗi và Output kỳ vọng khi `discountRate = 0` và khi khuyết tham số.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Sử dụng đúng ES6 Default Parameters:** Chuyển đổi hàm sang Arrow Function và khai báo tham số mặc định trực tiếp trên chữ ký hàm `(ticketPrice, discountRate = 0.15, bookingFee = 20000) => { ... }`.
*   **[20 điểm] Đóng gói an toàn bằng Closure:** Đưa biến tích lũy tổng doanh thu vào trong scope của Closure, không còn biến toàn cục (global variable) bị xâm nhập trực tiếp.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng giá vé:** Kiểm tra giá vé `ticketPrice` phải là kiểu số (`typeof ticketPrice === 'number'`) và có giá trị lớn hơn 0.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ném ngoại lệ `Error` với thông điệp tiếng Việt có dấu rõ ràng khi tham số truyền vào không hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được sự khác nhau giữa việc kiểm tra giá trị mặc định bằng toán tử `||` (Falsy values: `0`, `""`, `false`, `null`, `undefined`) và cú pháp ES6 Default Parameters (chỉ kích hoạt khi tham số là `undefined`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo tiếng Anh chuẩn `camelCase`, comment giải thích bằng tiếng Việt có dấu, trình bày thụt lề chuẩn ES6+.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session14_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết các câu lệnh kiểm thử tự động (assert/console.assert) kiểm tra các kịch bản mua vé Regular (`discountRate = 0`), Early Bird (khuyết tham số) và VIP (`discountRate = 0.1`).

---

## [Vận dụng cơ bản 4] Sửa lỗi tính tổng tiền vé sự kiện khi áp dụng mức chiết khấu 0%

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính tổng tiền vé sự kiện khi áp dụng mức chiết khấu 0% — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng lệnh `const finalDiscountRate = discountRate || 0.15;` trong mã nguồn cũ là nguyên nhân gây ra sự cố.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu 2 testcase còn thiếu (STT 2 và STT 3) với các thông số đầu ra hiện tại (bị lỗi), đầu ra mong đợi và lời giải thích ngắn gọn.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi thành công sang khai báo Tham số mặc định ES6 trên signature của Arrow Function: `(ticketPrice, ticketQuantity = 1, discountRate = 0.15, serviceFee = 30000) => { ... }`.
*   **[20 điểm] Xử lý chính xác giá trị 0%:** Kết quả tính toán cho trường hợp `discountRate = 0` trả về chính xác tổng tiền nguyên giá (không bị trừ 15%).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra các trường hợp giá vé hoặc số lượng vé không hợp lệ (ví dụ: `ticketPrice <= 0` hoặc `ticketQuantity <= 0`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Hàm xử lý mượt mà khi người dùng truyền thiếu tham số `ticketPrice` mà không làm sập ứng dụng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Trả lời rõ ràng sự khác nhau giữa Tham số mặc định ES6 và toán tử `||` đối với các giá trị falsy (`0`, `""`, `false`, `null`, `undefined`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng Arrow Function gọn gàng, biến đặt tên theo chuẩn camelCase tiếng Anh, chú thích Tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session14_Ex4`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm file test nhỏ hoặc tập hợp các câu lệnh `console.assert()` để tự động kiểm định hàm `calculateTicketOrderTotal` qua các kịch bản đợt bán Early Bird và Standard.

---

## [Vận dụng cơ bản 5] Sửa lỗi tính tổng tiền vé sự kiện khi áp dụng chiết khấu mặc định và phí tiện ích

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính tổng tiền vé sự kiện khi áp dụng chiết khấu mặc định và phí tiện ích — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã sử dụng toán tử gán mặc định `||` (`const finalDiscountRate = discountRate || 0.15;` và `const finalServiceFee = serviceFee || 30000;`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ 3 dòng trong bảng báo cáo test case với các giá trị Input, Output thực tế, Output mong đợi và lời giải thích bản chất toán tử `||` coi `0` là giá trị falsy.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Tái cấu trúc hàm thành công sử dụng ES6 Default Parameters: `(ticketPrice, quantity, discountRate = 0.15, serviceFee = 30000) => { ... }`.
*   **[20 điểm] Tính toán chính xác các kịch bản biên:** Đơn hàng có `discountRate = 0` trả về đúng giá không giảm; đơn hàng có `serviceFee = 0` trả về đúng tổng tiền không bị cộng 30,000 VNĐ; đơn hàng mua quá 4 vé trả về `-1`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra chính xác điều kiện hạn ngạch mua vé `quantity <= 0 || quantity > 4` và trả về mã lỗi thích hợp.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý an toàn các trường hợp không truyền tham số `discountRate` hoặc `serviceFee` (hệ thống tự lấy giá trị mặc định `0.15` và `30000`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn sự khác biệt giữa ES6 Default Parameters và toán tử `||` (hoặc toán tử `??` Nullish Coalescing) khi làm việc với các giá trị như `0`, `""`, `false`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn tiếng Anh camelCase (`ticketPrice`, `discountRate`, `serviceFee`), mã nguồn trình bày rõ ràng, thụt lùi dòng chuẩn mực.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 14_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết tập lệnh tự động in bảng so sánh kết quả mong đợi và kết quả thực tế cho 5 trường hợp kiểm thử khác nhau.

---

## [Vận dụng cơ bản 6] Sửa lỗi tính toán chiết khấu và phạm vi biến trong module bán vé Ticketbox

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính toán chiết khấu và phạm vi biến trong module bán vé Ticketbox — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code gán mặc định sai bằng toán tử `||` (`discountRate || 0.15`) và dòng code rò rỉ biến toàn cục `orderTotalAmount`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ 3 dòng trong bảng Test Case, mô tả chi tiết đầu vào (Input), đầu ra thực tế lỗi (Buggy Output), đầu ra kỳ vọng (Expected Output) và giải thích nguyên nhân logic.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng tham số mặc định ES6 `(quantity, baseUnitPrice, discountRate = 0.15, serviceFee = 30000) => ...`, đảm bảo khi truyền `discountRate = 0` thì tỷ lệ tính toán chính xác là 0%.
*   **[20 điểm] Đóng gói phạm vi biến (Local Scope):** Xóa bỏ biến toàn cục `orderTotalAmount`, khai báo biến tính toán cục bộ bằng `const`/`let` bên trong hàm và trả về trực tiếp giá trị hợp lệ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate điều kiện nghiệp vụ:** Kiểm tra chính xác điều kiện số lượng vé `quantity > 4` hoặc `quantity <= 0`, đơn giá `baseUnitPrice <= 0`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ném lỗi chuẩn bằng `throw new Error(...)` với thông báo tiếng Việt rõ ràng và bọc lời gọi hàm trong khối `try...catch` ở chương trình chính.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Phân tích lý thuyết Falsy Values và Scope:** Trả lời rõ ràng lý do tại sao toán tử `||` thất bại với giá trị `0` trong JavaScript và giải thích nguy cơ gây ra lỗi dữ liệu khi sử dụng biến toàn cục cho các luồng xử lý đơn hàng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng ES6+ chuẩn mực, thụt lùi dòng nhất quán, đặt tên biến/hàm theo chuẩn camelCase bằng tiếng Anh có ý nghĩa (`calculateTicketOrder`, `appliedDiscount`, `totalAmount`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tạo đúng thư mục và đẩy bài làm lên GitHub theo đúng cấu trúc yêu cầu: `[Tên Lớp]_[Môn Học]_Session14_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết hàm kiểm thử tự động (Automated Test Suite):** Viết thêm một đoạn mã ngắn tự động chạy 4-5 test case khác nhau và in ra màn hình `PASS`/`FAIL` tương ứng với mỗi kịch bản.

---

## [Vận dụng nâng cao 1] Xây dựng Module Quản lý Hạn ngạch và Chiết khấu Vé Concert

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Xây dựng Module Quản lý Hạn ngạch và Chiết khấu Vé Concert — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Trình bày đầy đủ kiểu dữ liệu của các tham số (bao gồm tham số mặc định `maxQuota = 4`, `zoneType = 'GA'`, `isEarlyBird = false`) và cấu trúc đối tượng dữ liệu trả về sau khi giao dịch thành công hoặc thất bại.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Giải thích rõ ràng nguyên lý hoạt động của Closure trong việc bảo vệ state `accumulatedTickets` và vẽ sơ đồ luồng xử lý (Mermaid hoặc các bước Pseudocode) logic mua vé đúng quy chuẩn.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Closure:** Triển khai đúng hàm khởi tạo quản lý vé sử dụng Closure để đóng gói biến nội bộ `accumulatedTickets`, chứng minh tính độc lập dữ liệu giữa các khách hàng khác nhau.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Viết phương thức mua vé bằng Arrow Function, tính toán chuẩn xác giá vé theo hệ số Zone (`VIP`, `ZONE_A`, `GA`) và trừ phần trăm chiết khấu Early Bird (15%).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Kiểm tra chính xác điều kiện `accumulatedTickets + ticketQuantity > maxQuota`. Từ chối giao dịch và không cộng dồn vé nếu vi phạm hạn ngạch.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kiểm tra giá vé cơ bản `basePrice > 0`, số lượng vé `ticketQuantity` phải là số nguyên nằm trong khoảng từ 1 đến 4, xử lý trường hợp mã Zone không hợp lệ một cách an toàn.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Khi giao dịch thất bại (do vượt hạn ngạch hoặc dữ liệu không hợp lệ), trả về thông báo lỗi rõ ràng, mô tả đúng lý do từ chối mà không làm sập ứng dụng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Sử dụng tên biến/hàm bằng tiếng Anh chuẩn camelCase (ví dụ: `createTicketManager`, `calculateTicketPrice`, `accumulatedTickets`), comment giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Tạo đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session14_Ex7` và đẩy đầy đủ file báo cáo + mã nguồn lên GitHub.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Viết mã nguồn ngắn gọn, tối ưu cú pháp Arrow Function (implicit return phù hợp), đóng gói thông tin báo cáo giao dịch chi tiết bao gồm cả số dư hạn ngạch còn lại của khách hàng ngay sau mỗi lần mua.

---

## [Vận dụng nâng cao 2] Xây dựng Trình Quản lý Đặt vé Sự kiện và Hạn ngạch theo Khu vực

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Xây dựng Trình Quản lý Đặt vé Sự kiện và Hạn ngạch theo Khu vực — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ tên tham số, kiểu dữ liệu, giá trị mặc định và xác định chính xác phạm vi biến (Global Scope, Local Scope, Closure State Scope) trong ứng dụng.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Mô tả kiến trúc Closure đóng gói dữ liệu và vẽ sơ đồ luồng Mermaid đầy đủ 5 hình khối chuẩn (Terminator, Input/Output, Decision, Process, Flowline).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Scope Closure:** Định nghĩa hàm tạo bộ quản lý khu vực vé (Zone Manager) sử dụng Closure để lưu trữ biến cục bộ `remainingQuota` và danh sách vé, không làm lộ biến ra Global Scope.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Sử dụng Arrow Function và Default Parameters (`earlyBirdRate = 0.15`, `serviceFee = 20000`) để tính toán hóa đơn và quản lý lượt check-in chính xác theo công thức nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu vượt ngưỡng:** Kiểm tra và từ chối xử lý khi khách hàng đặt ít hơn 1 vé, nhiều hơn 4 vé, hoặc khi số vé yêu cầu vượt quá số lượng vé còn lại trong khu vực.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao & Check-in:** Đảm bảo mỗi mã vé chỉ được check-in 1 lần duy nhất; chặn các thao tác check-in với mã vé giả lập không tồn tại.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Ném ra các lỗi rõ ràng bằng `throw new Error(...)` kèm mô tả Tiếng Việt nguyên nhân thất bại chi tiết cho từng kịch bản lỗi biên.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Sử dụng tên hàm/biến bằng Tiếng Anh chuẩn `camelCase`, comment giải thích logic bằng Tiếng Việt có dấu, cấu trúc mã nguồn mạch lạc không dùng các từ khóa/khái niệm cấm.
*   **[5 điểm] Nộp bài GitHub:** Đẩy báo cáo và mã nguồn lên repository GitHub đúng cấu trúc tên thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 14_Ex8`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & Mở rộng:** Đề xuất được giải pháp quản lý danh sách nhiều sự kiện khác nhau hoặc xây dựng cơ chế hủy đặt vé (ticket cancellation) hoàn trả hạn ngạch an toàn trong phạm vi Closure.

---

## [Vận dụng nâng cao 3] Thiết kế Module Quản lý Đặt vé và Hạn ngạch Sự kiện bằng Closure & Arrow Function

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Thiết kế Module Quản lý Đặt vé và Hạn ngạch Sự kiện bằng Closure & Arrow Function — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ tên tham số, kiểu dữ liệu (number, string, object, function...) và mô tả ý nghĩa dữ liệu đầu vào/đầu ra cho hàm tạo session và các phương thức con.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Giải thích rõ ràng nguyên lý Closure trong việc giấu biến `availableStock` và `userPurchasedCount`. Vẽ đúng sơ đồ luồng/các bước xử lý kiểm tra 2 lớp ràng buộc (Tồn kho & Hạn ngạch 4 vé).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Đóng gói State bằng Closure:** Khởi tạo biến private đúng cách trong hàm cha, trả về một đối tượng chứa các phương thức (Arrow Functions) có khả năng đọc/ghi các biến private đó mà không rò rỉ ra biến toàn cục.
*   **[15 điểm] Tính toán tài chính chuẩn xác:** Sử dụng đúng cú pháp Arrow Function và Tham số mặc định (Default Parameters) cho tỷ lệ chiết khấu (15%) và phí phát hành (20,000 VNĐ). Đảm bảo công thức tính giá sau chiết khấu và tổng thanh toán hoàn toàn chính xác.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy vượt hạn ngạch 4 vé:** Kiểm tra chính xác số vé đã tích lũy qua nhiều lần mua của một phiên giao dịch. Bắt lỗi và từ chối nếu `lượt_mua_mới + đã_mua > 4`.
*   **[15 điểm] Validate dữ liệu đầu vào & Tồn kho:** Kiểm tra số lượng mua phải là số nguyên dương (`Number.isInteger(qty) && qty > 0`), giá vé không âm, và số lượng mua không được vượt quá số vé khả dụng còn lại trong kho.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi rõ ràng:** Khi giao dịch bị từ chối (do vượt hạn ngạch, hết vé, dữ liệu sai format), hàm xử lý phải trả về đối tượng báo lỗi hoặc ném ra exception với thông điệp định danh tiếng Việt rõ ràng, giữ nguyên trạng thái kho vé trước đó.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch & Chuẩn ES6+:** Tên biến/hàm đặt bằng tiếng Anh chuẩn camelCase (`reserveTicket`, `getRemainingStock`, `calculateTotalPrice`), comment giải thích logic bằng tiếng Việt có dấu đầy đủ, tuyệt đối không dùng từ khóa `var` hoặc biến Global để lưu trữ state.
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đẩy mã nguồn lên GitHub đúng quy cách đặt tên thư mục theo hướng dẫn.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & Trả về Chi tiết Hóa đơn:** Phương thức đặt vé trả về thông tin hóa đơn chi tiết (bao gồm mã giao dịch duy nhất, giá gốc, tiền giảm giá, phí dịch vụ và số hạn ngạch còn lại được phép mua tiếp) dưới dạng Immutable Object.

---

## [Phân tích 1] Phân Tích Và Thiết Kế Bộ Xử Lý Đặt Vé Sự Kiện Vấn Đề Phạm Vi Biến Và Hạn Ngạch Check-in

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân Tích Và Thiết Kế Bộ Xử Lý Đặt Vé Sự Kiện Vấn Đề Phạm Vi Biến Và Hạn Ngạch Check-in — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Mô tả chi tiết giải pháp 1 (ví dụ: Sử dụng Function Declaration/Expression truyền thống kết hợp biến toàn cục hoặc kiểm tra tham số bằng toán tử logic `||`). Nêu rõ các lỗ hổng về Global Scope Pollution và falsy value (`serviceFee = 0`).
    *   Mô tả chi tiết giải pháp 2 (ví dụ: Sử dụng Arrow Functions, ES6 Default Parameters và mô hình Closure để đóng gói trạng thái biến cục bộ `remainingTickets`).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng so sánh hoàn chỉnh sử dụng thẻ HTML table đúng định dạng `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.
    *   Đánh giá chi tiết đủ 5 tiêu chí: Tốc độ xử lý (Speed), Chi phí bộ nhớ (Memory), Khả năng bảo trì (Maintainability), Độ rõ ràng (Readability), Mức độ phù hợp sản xuất (Suitability).

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Lý giải thuyết phục tại sao giải pháp sử dụng Closure và ES6 Default Parameters lại tối ưu vượt trội trong việc bảo vệ dữ liệu kho vé và tính toán chính xác hóa đơn dưới tải giao dịch cao.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ sơ đồ luồng Mermaid Flowchart hoặc viết Pseudocode chi tiết logic xử lý đặt vé.
    *   Nếu dùng Mermaid, bắt buộc tuân thủ đúng 5 chuẩn hình khối (Oval `([Bắt đầu/Kết thúc])`, Parallelogram `[/Đầu vào/Đầu ra/]`, Diamond `Kiểm tra điều kiện?`, Rectangle `["Tính toán/Xử lý"]`, Arrow `-->`). Không sử dụng Parallelogram cho khối xử lý tính toán.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Sử dụng cú pháp chuẩn ES6+ (Arrow Functions, `const`/`let`, Default Parameters).
    *   Tạo hàm Closure đóng gói an toàn biến `remainingTickets` (hoàn toàn không thể bị can thiệp từ bên ngoài).
    *   Viết hàm tính tổng chi phí thanh toán `calculateOrderTotal` chính xác theo công thức nghiệp vụ.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Kiểm tra số lượng vé hợp lệ (1 <= quantity <= 4), nếu sai trả về thông báo lỗi phù hợp.
    *   Xử lý chính xác tham số mặc định khi `serviceFee = 0` (không bị ghi đè thành 30,000).
    *   Từ chối đơn hàng và giữ nguyên số lượng tồn kho khi vé yêu cầu > vé còn lại trong Zone.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Hàm trả về đối tượng kết quả chứa đầy đủ thông tin: `success` (boolean), `message` (string), `totalAmount` (number), `remainingTickets` (number) mà không dư thừa các thuộc tính không cần thiết.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến, tên hàm sử dụng tiếng Anh chuẩn camelCase (ví dụ: `createTicketManager`, `calculateOrderTotal`, `discountRate`).
    *   Mã nguồn sạch rành mạch, có chú thích giải thích bằng tiếng Việt có dấu. Không sử dụng các từ ngữ cấm hoặc emoji trong mã nguồn.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn repository GitHub hợp lệ, đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session14_Ex10`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Viết đoạn mã thử nghiệm mô phỏng gọi liên tục 1,000 lượt đặt vé đồng thời để đo thời gian thực thi và xác nhận tính toàn vẹn dữ liệu kho vé không bị phá hỏng.

---

## [Phân tích 2] Đóng Gói Mô-đun Tính Giá Vé và Quản Lý Hạn Ngạch Đặt Vé Concert

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Đóng Gói Mô-đun Tính Giá Vé và Quản Lý Hạn Ngạch Đặt Vé Concert — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự khám phá và trình bày rõ ràng 2 phương án thiết kế kiến trúc hàm/scope/closure khác nhau (ví dụ: Phương án sử dụng Factory Function trả về Closure Object độc lập vs Phương án tổ chức hàm Module lồng nhau với biến đóng gói nội bộ), không trùng lặp logic.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Thiết lập bảng HTML chuẩn format, so sánh 2 giải pháp trên đủ 5 tiêu chí (Tốc độ thực thi, Bộ nhớ, Bảo trì, Độ dễ đọc, Mức độ đóng gói). Đánh giá có chiều sâu kĩ thuật.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Giải thích phục phục được lý do chọn phương án tối ưu dựa trên bài toán thực tế của Ticketbox (chống gian lận hạn ngạch, an toàn bộ nhớ khi mở rộng).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Vẽ sơ đồ Mermaid Flowchart chuẩn 100% hình dạng quy chuẩn (Terminator `([ ])`, Input/Output `[/ /]`, Decision `?`, Process `[" "]`). Luồng logic kiểm tra hạn ngạch và tính tiền được thể hiện chặt chẽ.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết mã nguồn JavaScript ES6+ hoàn chỉnh. Sử dụng đúng Arrow Function, Default Parameters, Closure để bảo vệ biến đếm vé không bị lộ ra Global Scope.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Xử lý triệt để tất cả rào chắn dữ liệu: kiểm tra số lượng vé hợp lệ (số nguyên dương), kiểm tra tổng số vé đã mua không vượt quá 4, xử lý an toàn giá trị mặc định khi truyền đối số bằng `0`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Hàm tính toán hoặc closure trả về đối tượng kết quả rõ ràng (gồm: số tiền gốc, chiết khấu, thuế, phí dịch vụ, tổng thanh toán, số vé còn lại có thể mua) không chứa thuộc tính thừa.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Đặt tên hàm, tham số, biến tiếng Anh theo chuẩn camelCase (ví dụ: `calculateTicketPrice`, `purchasedTicketsCount`, `maxTicketQuota`). Mã nguồn trình bày sạch đẹp, có ghi chú giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Khởi tạo repository và nộp đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session14_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Viết đoạn mã script đo lường thời gian xử lý và mức tiêu hao tài nguyên khi gọi hàm đếm vé/tính giá tiền 100,000 lần liên tiếp giữa 2 phương án để chứng minh tính vượt trội của phương án được chọn.

---

## [Phân tích 3] Thiết kế Module Quản lý Hạn ngạch và Tính giá Vé Sự kiện Ca nhạc

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Thiết kế Module Quản lý Hạn ngạch và Tính giá Vé Sự kiện Ca nhạc — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Tự đề xuất 2 giải pháp khác biệt về mặt cấu trúc lưu trữ trạng thái và cú pháp khai báo hàm (ví dụ: Giải pháp 1 dùng Global Variables + Function Declaration; Giải pháp 2 dùng Closure Scope + Arrow Functions + ES6 Default Parameters).
    *   Phân tích ưu/nhược điểm kiến trúc của từng giải pháp rõ ràng, không trùng lặp.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Tạo bảng HTML/Markdown đầy đủ 5 tiêu chí: Tốc độ thực thi, Bộ nhớ, Tính đóng gói, Độ đọc hiểu, Khả năng mở rộng.
    *   Bảng HTML phải chứa thuộc tính chuẩn: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lập luận thuyết phục vì sao chọn giải pháp Closure + Arrow Function + Default Parameters cho môi trường Production của hệ thống Ticketbox (tránh race condition, an toàn bộ nhớ, cú pháp hiện đại).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu (Mermaid):**
    *   Vẽ sơ đồ Mermaid đúng chuẩn 5 hình khối: Oval `([...])` cho Start/End, Hình bình hành `[/.../]` cho Input/Output, Hình chữ nhật `["..."]` cho Process, Hình thoi `...` cho Decision.
    *   Luồng logic thể hiện đầy đủ các bước kiểm tra hạn ngạch $N + \text{vé đã mua} \le 4$, tính giảm giá Early Bird, tính thuế VAT và phí dịch vụ.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code JavaScript:**
    *   Khởi tạo hàm đóng gói bằng Closure (ví dụ `createTicketManager(maxQuota = 4)`), chứa biến private đếm số vé đã mua.
    *   Áp dụng Arrow Function và ES6 Default Parameters đúng cú pháp cho logic tính toán thanh toán (`taxRate = 0.08`, `serviceFee = 20000`, `isEarlyBird = false`).
    *   Thực hiện return đúng đối tượng chứa các phương thức xử lý (như `buyTickets`, `getPurchasedCount`).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Từ chối và báo lỗi nếu `quantity` không phải số nguyên dương ($N \le 0$ hoặc `!Number.isInteger(quantity)`).
    *   Từ chối và báo lỗi nếu `basePrice` $\le 0$.
    *   Từ chối giao dịch và giữ nguyên số vé đã mua nếu vượt quá hạn ngạch 4 vé.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Kết quả trả về khi mua vé thành công phải dạng Object hoặc chuỗi thông báo rõ ràng gồm: Số vé vừa mua, Số tiền thanh toán thực tế, Số vé còn lại được phép mua.
    *   Định dạng dữ liệu chính xác, không thừa hoặc thiếu trường thông tin.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Sử dụng tên biến/hàm 100% bằng tiếng Anh chuẩn camelCase (ví dụ: `calculateTicketPrice`, `purchasedCount`, `remainingQuota`).
    *   Mã nguồn sạch đẹp, có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đúng cấu trúc thư mục GitHub: `[Tên Lớp]_[Môn Học]_Session14_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script / Kịch bản kiểm thử độc lập:**
    *   Viết kịch bản khởi tạo 2 instance khách hàng độc lập từ Closure để chứng minh tính cô lập dữ liệu (Scope Isolation) giữa 2 tài khoản mua vé khác nhau.

---

## [Sáng tạo 1] Thiết kế Module Đóng gói Quản lý Vé và Check-in Sự kiện Concert

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế Module Đóng gói Quản lý Vé và Check-in Sự kiện Concert — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa rõ ràng mô hình dữ liệu cho từng thao tác (Phát hành vé, Tính tiền, Check-in, Báo cáo Stats). Cấu trúc dữ liệu có tính mở rộng cao và thể hiện đầy đủ các trường thông tin cần thiết.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê ít nhất 3 bẫy lỗi nghiệp vụ thực tế (Ví dụ: `discountRate` truyền giá trị `0`, vượt quá số lượng 4 vé/lần mua, mã vé trùng lặp, check-in mã chưa phát hành hoặc đã check-in trước đó).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện đầy đủ luồng xử lý từ lúc khách chọn vé -> tính tiền -> lưu trữ vé vào Closure -> thực hiện check-in tại cổng. Tuân thủ 100% quy chuẩn hình dạng chuẩn (Oval cho Start/End, Song song cho Input/Output, Chữ nhật cho Process, Thoi cho Decision).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ cơ chế đóng gói phạm vi (Scope isolation) bằng Closure giúp bảo vệ dữ liệu vé không bị can thiệp bởi biến toàn cục như thế nào.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công Closure & Arrow Functions:** Sử dụng đúng cú pháp ES6 Arrow Functions, xây dựng thành công factory function trả về object chứa các hàm thao tác truy cập biến private qua Lexical Scope.
*   **[15 điểm] Xử lý tham số mặc định chuẩn xác:** Áp dụng Tham số mặc định (Default Parameters) cho thuế VAT và mức giảm giá. Không vi phạm lỗi logic của toán tử `||` khi đối số truyền vào có giá trị bằng `0`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết code validation chặt chẽ cho các lỗi biên đã nêu ở Phần 1, trả về thông báo lỗi rõ ràng và không làm sập chương trình.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn đặt tên:** Mã nguồn tổ chức mô-đun hóa tốt, tên biến/hàm đặt bằng tiếng Anh chuẩn `camelCase`, comment giải thích logic rõ ràng bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục đúng quy định `[Tên Lớp]_[Môn Học]_Session14_Ex13`, file README mô tả chi tiết kịch bản chạy thử nghiệm.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung hàm ghi nhật ký thao tác (Audit Log) theo thời gian thực khép kín bên trong Closure hoặc hàm hủy/hoàn vé (Cancel Ticket) khôi phục lại hạn ngạch chưa bán của khu vực.

---

## [Sáng tạo 2] Thiết kế Module Đóng gói Quản lý Vé & Đặt chỗ Concert bằng Closure

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Module Đóng gói Quản lý Vé & Đặt chỗ Concert bằng Closure — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc tham số đầu vào và dữ liệu trả về cho hàm khởi tạo Closure và các hàm thao tác con (đơn hàng vé, mã QR, giá trị chiết khấu) đầy đủ kiểu dữ liệu và mô tả rõ ràng.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 bẫy bối cảnh nghiệp vụ thực tế (ví dụ: mua vé vượt hạn ngạch 4 vé/tài khoản, kho hết vé, chiết khấu âm, quét mã QR trùng lặp) và đề xuất cách xử lý mạch lạc.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid mô tả chính xác vòng đời dữ liệu từ khởi tạo Closure đến check-in. Tuân thủ 100% quy chuẩn 5 dạng hình khối (Terminator, Input/Output, Decision, Process, Flowline).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ cơ chế chuyển đổi trạng thái của mã QR check-in (từ Chưa sử dụng -> Đã check-in) và cơ chế đóng gói bảo vệ biến private bằng Lexical Scope.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Xây dựng hàm tạo bộ quản lý vé bằng Closure + Arrow Function; tính đúng chiết khấu Early Bird (15%), xử lý phí xuất vé mặc định (20.000 VNĐ) qua Default Parameter.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Triển khai các phương thức truy xuất báo cáo (ví dụ: danh sách vé đã quét check-in, tổng doanh thu thực thu) từ dữ liệu private đóng gói trong Closure.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các điều kiện kiểm tra (guards) để chặn ngay khi người dùng cố tình mua > 4 vé/tài khoản, mua khi hết vé kho, hoặc quét check-in lại mã QR đã dùng với thông báo lỗi cụ thể.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết bằng ES6+, đặt tên biến/hàm bằng tiếng Anh theo chuẩn camelCase, chú thích tiếng Việt có dấu rõ ràng, tuyệt đối không lạm dụng biến toàn cục `var` hay `class`.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục repository đúng quy định (`[Tên Lớp]_[Môn Học]_Session14_Ex14`), file README trình bày mạch lạc kịch bản chạy thử nghiệm.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Triển khai thêm tính năng hủy vé đặt trước thời hạn (hoàn lại hạn ngạch cho kho và cho tài khoản) hoặc ghi vết nhật ký quét QR check-in kèm mốc thời gian thực thi (Timestamp log).

---

## [Sáng tạo 3] Thiết kế Module Đóng gói Quản lý Đặt vé và Kiểm soát QR Check-in Sự kiện Ca nhạc

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế Module Đóng gói Quản lý Đặt vé và Kiểm soát QR Check-in Sự kiện Ca nhạc — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, rõ ràng các thuộc tính đầu vào/đầu ra cho hàm đặt vé và hàm kiểm soát check-in QR mà không cần gợi ý mã.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích và mô tả chi tiết tối thiểu 3 kịch bản lỗi biên thực tế (ví dụ: cộng dồn số vé quá 4 vé/tài khoản qua nhiều lần mua, truyền giá trị phí dịch vụ bằng 0, quét mã QR trùng lặp, mã sự kiện không tồn tại).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid đúng cú pháp, thể hiện rõ các bước xử lý từ khởi tạo Closure, tính toán giá trị, đóng gói trạng thái private đến xác thực check-in.
*   **[10 điểm] Tuân thủ quy chuẩn hình họa Mermaid:** Sử dụng đúng 5 dạng hình chuẩn theo yêu cầu (Terminator `([ ])`, Input/Output `[/ /]`, Process `[" "]`, Decision Diamond, Flowline).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai Closure & Arrow Functions đóng gói dữ liệu:** Sử dụng hàm tạo Closure (`createTicketManager` hoặc tương đương) để giấu kín biến trạng thái `tickets`, trả về các phương thức dạng Arrow Function nhằm thao tác với dữ liệu mà không bị rò rỉ scope.
*   **[15 điểm] Triển khai đúng các quy tắc nghiệp vụ:**
    *   Tính đúng chiết khấu Early Bird (giảm 15%).
    *   Áp dụng tham số mặc định cho phí dịch vụ (20.000 VNĐ) một cách an toàn.
    *   Kiểm soát hạn ngạch tối đa 4 vé/tài khoản.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng mã nguồn kiểm tra dữ liệu chặt chẽ (Guard Clauses), trả về thông báo lỗi rõ ràng khi phát hiện vi phạm hạn ngạch hoặc quét trùng mã QR.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Standard Naming:** Đặt tên biến và hàm bằng tiếng Anh chuẩn camelCase, comment giải thích bằng Tiếng Việt có dấu đầy đủ, tuyệt đối không sử dụng biến toàn cục hoặc từ khóa bị cấm.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo cấu trúc thư mục đúng định dạng quy định `[Tên Lớp]_[Môn Học]_Session14_Ex15`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Auditing / Nhật ký thao tác:** Triển khai thêm phương thức private ghi lại lịch sử các lượt quét QR thất bại (mã không tồn tại, mã đã dùng) hoặc phương thức thống kê tổng doanh thu thực tế được đóng gói an toàn trong Closure.

---

## [Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
- Phân tích đúng phạm vi biến (Global vs Local Scope) và minh họa được Lexical Scope / Call Stack khi gọi hàm (10 điểm).
- Trình bày rõ ràng logic tính toán và cơ chế hoạt động của Closure trong việc bảo vệ dữ liệu biến private (10 điểm).

#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
- Xây dựng Hàm 1 đúng cú pháp Function Declaration / Expression, nhận đủ tham số và trả về kết quả chính xác theo công thức nghiệp vụ (10 điểm).
- Xây dựng Hàm 2 đúng cú pháp Arrow Function ES6, sử dụng đúng Tham số mặc định (Default Parameters) cho tỷ lệ chiết khấu và phụ phí VIP (15 điểm).
- Xây dựng Hàm 3 áp dụng chuẩn xác kỹ thuật Closure, biến số lượng vé được đóng gói an toàn trong scope của hàm khởi tạo, trả về object chứa đúng 2 phương thức theo yêu cầu (15 điểm).

#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
- Kiểm tra các trường hợp giá trị khuyết (undefined) khi gọi hàm để chứng minh tính hiệu quả của tham số mặc định (10 điểm).
- Đảm bảo biến private trong Closure không thể bị truy cập hoặc ghi đè trực tiếp từ phạm vi toàn cục (Global Scope) (10 điểm).

#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
- Đặt tên hàm, tên tham số và biến theo quy chuẩn camelCase chuẩn mực tiếng Anh chuyên ngành (10 điểm).
- Cấu trúc file rõ ràng, không sử dụng lại biến `var` gây xung đột scope, tuân thủ đúng tên thư mục theo yêu cầu nộp bài (10 điểm).

---

## [Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap)

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
- **Đạt tối đa (30 điểm)**:
  - Bao phủ 100% kiến thức của Session 14 bao gồm: Function Declaration, Function Expression, Hoisting, Call Stack Frame, Arrow Function, Implicit Return, Object Literal Return `()`, Default Parameters, Global Scope, Local/Block Scope, Lexical Scope, Closure và Private State.
  - Các từ khóa trọng tâm được phân loại chính xác vào từng nhánh.
- **Mức Khá (20 - 29 điểm)**: Bao phủ được 80-90% kiến thức, thiếu 1-2 khái niệm nâng cao (như Return Object Literal hoặc bẫy lỗi mặc định với `0`).
- **Mức Trung bình (10 - 19 điểm)**: Chỉ trình bày được các khái niệm hàm cơ bản, bỏ qua Closure hoặc Phạm vi Scope.
- **Mức Đạt tối thiểu (1 - 9 điểm)**: Sơ đồ quá sơ sài, thiếu trên 50% từ khóa cốt lõi.

---

#### **2. Phân tầng logic & Mối liên kết nghiệp vụ EVENT_TICKETING — 30 điểm**
- **Đạt tối đa (30 điểm)**:
  - Sơ đồ tư duy được chia nhánh chính/phụ cực kỳ khoa học, mạch lạc (Tối thiểu 3 nhánh chính ứng với 3 nội dung lớn).
  - Tích hợp nhuần nhuyễn ngữ cảnh nghiệp vụ bán vé sự kiện (**EVENT_TICKETING**) vào các nút (nodes) của sơ đồ (VD: Tính giá vé VIP, Phí đặt chỗ, Mã voucher ưu đãi, Bộ đếm vé giữ chỗ closure).
- **Mức Khá (20 - 29 điểm)**: Phân tầng tốt nhưng các ví dụ/từ khóa chưa thể hiện rõ đặc thù của domain EVENT_TICKETING (còn mang tính lý thuyết chung chung).
- **Mức Trung bình (10 - 19 điểm)**: Cấu trúc nhánh bị lộn xộn, xếp sai thứ tự quan hệ cha - con giữa các khái niệm (VD: Đặt Closure ngang hàng với Function).
- **Mức Đạt tối thiểu (1 - 9 điểm)**: Các nhánh không có tính liên kết, trình bày dạng danh sách liệt kê phẳng thay vì dạng cây tư duy.

---

#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
- **Đạt tối đa (20 điểm)**:
  - Nộp đầy đủ cả 2 file: File thiết kế gốc (`.xmind`/`.drawio`/`.pdf`) và file ảnh (`.png`/`.jpg`).
  - Ảnh xuất ra có độ phân giải cao, sắc nét, không bị vỡ chữ.
  - Sử dụng màu sắc, icon, hiệu ứng hình ảnh hợp lý để phân biệt rõ các cấp độ nhánh (Level 1, Level 2, Level 3).
- **Mức Khá (15 - 19 điểm)**: Nộp đủ file nhưng phối màu chưa hài hòa hoặc chữ hơi nhỏ, khó đọc ở một số nhánh sâu.
- **Mức Trung bình (8 - 14 điểm)**: Chỉ nộp 1 trong 2 loại file (chỉ có ảnh hoặc chỉ có file gốc), hoặc file ảnh bị mờ.
- **Mức Đạt tối thiểu (1 - 7 điểm)**: Không nộp được file sơ đồ trực quan.

---

#### **4. Bản tóm tắt giải trình (summary.md) & Code minh họa — 10 điểm**
- **Đạt tối đa (10 điểm)**:
  - File `summary.md` giải thích sâu sắc các mối liên kết trong sơ đồ.
  - Chứa đủ **3 đoạn mã nguồn minh họa** (chuẩn JavaScript ES6+, chạy được trên Node.js) áp dụng trực tiếp cho hệ thống bán vé **EVENT_TICKETING**:
    1. Ví dụ tính tổng hóa đơn vé (Function Declaration/Expression).
    2. Ví dụ tính tiền vé sau chiết khấu voucher & tạo đối tượng giỏ vé (Arrow Function + Default Params).
    3. Ví dụ đóng gói bộ đếm vé tự tăng/giảm độc lập (Closure).
- **Mức Khá (7 - 9 điểm)**: Có giải trình và mã nguồn nhưng thiếu 1 ví dụ hoặc mã nguồn chưa bám sát nghiệp vụ EVENT_TICKETING.
- **Mức Trung bình (4 - 6 điểm)**: File `summary.md` quá sơ sài, chỉ copy lại tiêu đề bài học mà không có mã nguồn minh họa.
- **Mức Đạt tối thiểu (1 - 3 điểm)**: Không có file `summary.md`.

---

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
- **Đạt tối đa (10 điểm)**:
  - Tên Repository đặt đúng cú pháp quy định.
  - Cấu trúc thư mục ngăn nắp, chứa đúng tên các file yêu cầu (`mindmap.png`, `summary.md`, ...).
  - Commit message viết đúng chuẩn kĩ thuật (`feat: ...`).
- **Mức Khá (7 - 9 điểm)**: Đặt tên Repo đúng nhưng commit message chưa chuẩn hóa hoặc thừa file rác.
- **Mức Trung bình (4 - 6 điểm)**: Đặt sai tên Repository hoặc nộp thiếu file trên GitHub.
- **Mức Đạt tối thiểu (0 điểm)**: Không nộp link GitHub hoặc Repo để chế độ Private.

---

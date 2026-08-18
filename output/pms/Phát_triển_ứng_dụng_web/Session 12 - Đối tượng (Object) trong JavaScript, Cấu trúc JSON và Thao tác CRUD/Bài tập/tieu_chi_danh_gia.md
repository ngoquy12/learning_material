## [Vận dụng cơ bản 1] Sửa lỗi đóng gói dữ liệu đặt phòng khách sạn và tính phụ thu check-in sớm

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi đóng gói dữ liệu đặt phòng khách sạn và tính phụ thu check-in sớm — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng code sử dụng sai cú pháp Bracket Notation thiếu dấu nháy chuỗi (`booking[roomPrice]`) và dòng code gán `undefined` thay vì sử dụng toán tử `delete`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác các ô còn thiếu (`...`) trong bảng Test Case (hàng 2 và hàng 3), thể hiện rõ sự khác biệt giữa Buggy Output và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công cú pháp truy cập `booking.roomPrice` (hoặc `booking["roomPrice"]`) để tính phụ thu check-in sớm 30% chính xác khi `checkInHour < 12`.
*   **[20 điểm] Xử lý xóa thuộc tính đúng chuẩn ES6:** Sử dụng câu lệnh `delete booking.tempToken;` (hoặc `delete booking["tempToken"];`) loại bỏ hoàn toàn key ra khỏi đối tượng trước khi thực hiện `JSON.stringify`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra đối tượng `rawBooking` hợp lệ và thuộc tính `roomPrice` phải là số lớn hơn 0.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo hàm xử lý an toàn, không làm biến đổi (mutate) đối tượng gốc `rawBooking` truyền vào.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao việc gán `booking.tempToken = undefined` vẫn làm thuộc tính tồn tại khi duyệt key đối tượng (`"tempToken" in booking` là `true`) và lý do toán tử `delete` giải quyết triệt để vấn đề này.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng, thụt lùi dòng chuẩn, không có lỗi cú pháp console.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session12_Ex1`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết đoạn mã kiểm thử tự động:** Viết thêm hàm kiểm thử tự động chạy qua nhiều trường hợp (check-in trước 12h, đúng 12h, sau 12h) và in thông báo kiểm chứng "PASS/FAIL" trên Console log.

---

## [Vận dụng cơ bản 2] Khắc phục lỗi cập nhật thông tin và đóng gói JSON đơn đặt phòng

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Khắc phục lỗi cập nhật thông tin và đóng gói JSON đơn đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Pinpoint chính xác 2 điểm lỗi trong mã nguồn ban đầu (dòng gán `undefined` thay vì dùng từ khóa `delete` và dòng truy cập trực tiếp thuộc tính trên chuỗi JSON).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ và chính xác dữ liệu 3 trường hợp thử nghiệm trong bảng báo cáo (STT 2 và STT 3).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    *   Sử dụng đúng cú pháp `delete rawBookingData.internalStaffNote` hoặc `delete rawBookingData["internalStaffNote"]`.
    *   Sử dụng `JSON.parse(jsonPayload)` để chuyển đổi chuỗi JSON về lại Object trước khi đọc giá trị `"early-checkin-fee"`.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Trả về đối tượng kết quả chính xác bao gồm chuỗi `jsonPayload` hợp lệ và giá trị `extractedFee` là một số thực tế.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra `rawBookingData` phải là Object hợp lệ (không bị `null` hoặc `undefined`), giá trị `earlyFee` phải là kiểu số (Number) không âm.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp chuỗi JSON bị lỗi cấu trúc khi parse bằng khối `try...catch` an toàn.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Trả lời rõ ràng sự khác biệt giữa việc gán `undefined` cho thuộc tính và việc dùng từ khóa `delete`, đồng thời giải thích tại sao không thể lấy thuộc tính trực tiếp từ một String dạng JSON.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến theo chuẩn `camelCase`, thụt lề đồng nhất 2 hoặc 4 khoảng trắng, ghi chú mã nguồn bằng tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm các hàm kiểm thử tự động (sử dụng `console.assert` hoặc câu lệnh điều kiện) để kiểm tra thuộc tính `internalStaffNote` hoàn toàn không còn tồn tại trong Object sau khi xử lý.

---

## [Vận dụng cơ bản 3] Sửa lỗi cập nhật thuộc tính và đóng gói JSON hồ sơ đặt phòng

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi cập nhật thuộc tính và đóng gói JSON hồ sơ đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code gán `undefined` thay vì dùng `delete` và dòng code cố gắng truy cập trực tiếp thuộc tính từ chuỗi JSON mà chưa parse.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% các ô trống (`...`) ở hàng 2 và 3 trong bảng Test Case với đầy đủ Input, Buggy Output, Expected Output, Failing Line và Logic Note giải thích cơ chế chuỗi JSON và toán tử `delete`.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Sử dụng toán tử delete đúng cách:** Sử dụng cú pháp `delete bookingObj.tempAuthToken;` hoặc `delete bookingObj["tempAuthToken"];` để loại bỏ hẳn key khỏi Object trước khi serialize.
*   **[20 điểm] Chuyển đổi và giải mã JSON chuẩn xác:** Thực hiện đúng `JSON.stringify()` khi đóng gói và `JSON.parse()` khi muốn khôi phục chuỗi JSON thành Object để truy cập thuộc tính `"early-checkin-fee"`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate đối tượng đầu vào cơ bản:** Kiểm tra `bookingObj` hợp lệ (không null/undefined và là kiểu Object) trước khi thao tác thuộc tính.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp tính phụ phí an toàn nếu `basePrice` thiếu hoặc không phải là số hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Phân tích lý thuyết chuyên sâu:** Giải thích được sự khác biệt giữa việc gán `obj.key = undefined` (vẫn còn key trong `Object.keys()`) và dùng `delete obj.key` (loại bỏ hoàn toàn key khỏi bộ nhớ).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo chuẩn camelCase trong JavaScript, định dạng mã nguồn thụt lùi rõ ràng, comment tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xây dựng hàm kiểm định tự động:** Viết thêm đoạn mã kiểm thử tự động (Assertion / Console check) so sánh `JSON.parse(resultPayload)["tempAuthToken"] === undefined` và xác nhận key không tồn tại trong chuỗi JSON.

---

## [Vận dụng cơ bản 4] Sửa lỗi đóng gói dữ liệu đặt phòng và chuẩn hóa JSON

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi đóng gói dữ liệu đặt phòng và chuẩn hóa JSON — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác các dòng mã nguồn chứa lỗi logic (Lỗi gán `undefined` giữ lại key trong Object ở dòng 16; Lỗi đọc thuộc tính trực tiếp trên chuỗi JSON chưa giải mã ở dòng 22-23).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% thông tin bị thiếu trong bảng Test Case (cột Buggy Output, Expected Output, Dòng code gây lỗi và Nguyên nhân giải thích).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    * Sử dụng cú pháp ngoặc vuông `bookingReservation[surchargeKey] = 250000` để cập nhật đúng thuộc tính động.
    * Sử dụng toán tử `delete bookingReservation.tempAuthToken` để loại bỏ sạch key nhạy cảm khỏi bộ nhớ.
    * Sử dụng `JSON.parse(jsonPayload)` để chuyển chuỗi JSON thành Object trước khi truy xuất dữ liệu `guestName` và `extra-services`.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Mã nguồn JavaScript ES6+ chạy thành công không phát sinh lỗi cú pháp hay lỗi tham chiếu Runtime.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo đối tượng ban đầu có đầy đủ cấu trúc thuộc tính theo yêu cầu và kiểm tra tính hợp lệ của biến key động.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Chuỗi JSON đầu ra (`jsonPayload`) đảm bảo hợp lệ, không chứa thuộc tính `tempAuthToken` và không chứa thuộc tính thừa `surchargeKey`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ sự khác biệt giữa việc gán giá trị `undefined` cho thuộc tính và việc sử dụng toán tử `delete`, đồng thời nêu rõ lý do tại sao không thể truy cập thuộc tính trực tiếp từ một chuỗi JSON (String type).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn đặt tên biến rõ ràng, thụt lùi dòng chuẩn mực, chú thích giải thích logic bằng tiếng Việt đầy đủ dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm đoạn mã kiểm thử tự động sử dụng `console.assert()` để kiểm tra thuộc tính `tempAuthToken` không còn tồn tại trong `bookingReservation` sau khi xóa (`console.assert(bookingReservation.tempAuthToken === undefined && !('tempAuthToken' in bookingReservation))`).

---

## [Vận dụng cơ bản 5] Sửa lỗi đóng gói và tính phụ phí đặt phòng khách sạn

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi đóng gói và tính phụ phí đặt phòng khách sạn — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã chứa toán tử so sánh sai (`<= 12`) và dòng mã gán `undefined` thay vì sử dụng toán tử `delete`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện chính xác các cột Input, Buggy Output, Expected Output, Line of Code và Logic Note cho toàn bộ 3 testcase trong bảng báo cáo.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh điều kiện kiểm tra check-in sớm (`checkInHour < 12`) và tính đúng phụ phí 30% giá cơ bản.
*   **[20 điểm] Thao tác xóa và đóng gói Object chuẩn xác:** Sử dụng đúng toán tử `delete bookingObj.tempSecurityToken` để xóa thuộc tính khỏi bộ nhớ và thực hiện đóng gói chuỗi JSON bằng `JSON.stringify`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra giá phòng `basePrice > 0` và giờ check-in nằm trong khoảng từ `0` đến `23`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ném ra `Error` với thông báo rõ ràng khi gặp dữ liệu không hợp lệ mà không làm dừng đột ngột chương trình.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được sự khác biệt giữa việc gán `obj.key = undefined` và dùng toán tử `delete obj.key` khi đóng gói dữ liệu sang chuỗi JSON (`JSON.stringify`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo chuẩn camelCase, mã nguồn trình bày rõ ràng, bổ sung ghi chú bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết hàm test kiểm thử tự động kiểm tra các trường hợp check-in lúc 11h, 12h và 13h để đảm bảo logic phụ phí làm việc chính xác 100%.

---

## [Vận dụng cơ bản 6] Sửa lỗi xử lý hóa đơn đặt phòng và đóng gói JSON

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi xử lý hóa đơn đặt phòng và đóng gói JSON — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng code gán `undefined` thay vì `delete` (Dòng 16) và dòng đọc thuộc tính trực tiếp trên chuỗi JSON string (Dòng 22).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Đã hoàn thành chính xác 2 dòng Test Case còn thiếu (STT 2, STT 3) với các thông số dữ liệu đầu vào, đầu ra bị lỗi thực tế và đầu ra mong đợi chuẩn xác.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    - Dùng đúng cú pháp `delete bookingObj.tempSecurityCode` để loại bỏ thuộc tính khỏi đối tượng.
    - Chuyển đổi thành chuỗi JSON bằng `JSON.stringify()`.
    - Giải mã chuỗi JSON về Object bằng `JSON.parse()` và lấy đúng giá trị `totalAmount` cho `confirmedTotal`.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng câu lệnh `throw new Error(...)` để báo lỗi khi dữ liệu đầu vào không hợp lệ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Bắt được các trường hợp `bookingObj` là `null`, `undefined` hoặc không phải đối tượng.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra `roomPrice` hợp lệ (kiểu `number` và `> 0`), tránh tính toán ra kết quả `NaN`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ lý do tại sao gán `obj.key = undefined` vẫn làm cho `key` tồn tại trong đối tượng (vẫn xuất hiện trong `Object.keys()` hoặc `hasOwnProperty()`) và phân biệt sự khác nhau về bản chất giữa Chuỗi JSON và JS Object.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến/hàm đặt theo chuẩn camelCase bằng tiếng Anh, viết chú thích mã nguồn rõ ràng, thụt lùi dòng đúng chuẩn ES6+.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository đúng tên thư mục yêu cầu: `[Tên Lớp]_[Môn Học]_Session12_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết một đoạn mã tự động kiểm thử (script test automation đơn giản) để gọi hàm `processBookingInvoice` với các tham số hợp lệ và bất hợp lệ, tự động in ra màn hình thông báo `PASS` hoặc `FAIL`.

---

## [Vận dụng nâng cao 1] Xử lý cập nhật phụ phí đặt phòng và đóng gói dữ liệu JSON

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Xử lý cập nhật phụ phí đặt phòng và đóng gói dữ liệu JSON — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** 
    * Xác định chính xác kiểu dữ liệu của đối tượng đầu vào `BookingReservation` (chứa `bookingId`: string, `roomPrice`: number, `checkInHour`: number, `tempToken`: string, `internalNote`: string).
    * Xác định chính xác kiểu dữ liệu của đầu ra (đối tượng JavaScript sau khi làm sạch và chuỗi `jsonPayload`: string).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:**
    * Trình bày logic kiểm tra đầu vào, áp dụng công thức tính phụ phí check-in sớm, cập nhật thuộc tính động qua Bracket Notation và xóa dữ liệu nhạy cảm bằng `delete`.
    * Vẽ sơ đồ luồng Mermaid Flowchart đúng quy chuẩn 5 hình (Oval, Parallelogram, Diamond, Rectangle, Flowline) không vi phạm lỗi cú pháp.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và thao tác thuộc tính:**
    * Tạo đối tượng `bookingReservation` lưu trữ đầy đủ các thuộc tính ban đầu.
    * Sử dụng Bracket Notation với biến động để thêm thành công thuộc tính `"emergency-contact"`.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:**
    * Tính đúng phụ thu 30% khi `checkInHour < 12.0` và gán chính xác thuộc tính `totalAmount`.
    * Sử dụng từ khóa `delete` để xóa bỏ hoàn toàn 2 thuộc tính `tempToken` và `internalNote`.
    * Thực hiện đúng chuyển đổi `JSON.stringify()` và `JSON.parse()`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:**
    * Kiểm tra tính hợp lệ của `checkInHour` (nằm ngoài khoảng `0.0` - `24.0` sẽ báo lỗi).
    * Kiểm tra tính hợp lệ của `roomPrice` (nhỏ hơn hoặc bằng 0 sẽ báo lỗi).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:**
    * Kiểm tra `bookingId` rỗng hoặc không phải dạng chuỗi ký tự hợp lệ.
    * Đảm bảo đối tượng JSON giải mã (`JSON.parse`) trùng khớp cấu trúc và không còn chứa các thuộc tính bị xóa.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    * Hiển thị thông điệp lỗi rõ ràng bằng Tiếng Việt khi dữ liệu đầu vào không hợp lệ (ví dụ: `[LỖI] Giá phòng không hợp lệ`, `[LỖI] Giờ check-in vượt quá phạm vi cho phép`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:**
    * Tên biến, hàm viết bằng Tiếng Anh chuẩn `camelCase`. Comment giải thích rõ ràng bằng Tiếng Việt có dấu. Không chứa emoji hoặc cú pháp bị cấm.
*   **[5 điểm] Nộp bài GitHub:**
    * Tạo cấu trúc thư mục nộp bài chuẩn quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:**
    * Đóng gói logic cập nhật và làm sạch vào một hàm xử lý tái sử dụng (reusable function), kiểm tra kỹ lưỡng đối tượng trước và sau khi `JSON.stringify()` để khẳng định không dư thừa dữ liệu trong bộ nhớ.

---

## [Vận dụng nâng cao 2] Đóng gói và Xử lý Chuẩn hóa Dữ liệu Đặt phòng Khách sạn

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Đóng gói và Xử lý Chuẩn hóa Dữ liệu Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** 
    *   Xác định chính xác kiểu dữ liệu và cấu trúc đối tượng `BookingReservation` (String, Number, Boolean, Key có ký tự đặc biệt).
    *   Xác định rõ ràng kết quả đầu ra bao gồm chuỗi JSON sạch và đối tượng được phục hồi từ JSON.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế sơ đồ luồng (Flowchart):**
    *   Đề xuất logic giải pháp rõ ràng, mạch lạc, giải thích lý do phải dùng `delete` thay vì gán `undefined`.
    *   Vẽ sơ đồ luồng Mermaid tuân thủ chính xác 5 dạng hình tiêu chuẩn: Oval `([Start/End])`, Bình hành `[/Input/Output/]`, Thoi `Condition?`, Chữ nhật `["Process"]`. Không dùng hình Bình hành cho các thao tác tính toán hay xóa thuộc tính.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:**
    *   Khai báo đối tượng Object Literal lưu trữ đầy đủ thông tin đặt phòng khách sạn.
    *   Định danh chính xác các key chứa ký tự đặc biệt như `early-checkin-fee`, `late-checkout-fee` và các trường nhạy cảm `tempSessionToken`, `internalCardCVV`.
*   **[15 điểm] Thao tác thuộc tính Đối tượng & Đóng gói JSON:**
    *   Sử dụng đúng Bracket Notation để truy cập và cộng dồn các thuộc tính phụ phí dynamic.
    *   Thêm/cập nhật thành công các thuộc tính mới (`totalAmount`, `isProcessed`, `exportTimestamp`) vào đối tượng.
    *   Sử dụng thành thạo toán tử `delete` để xóa bỏ hoàn toàn các trường dữ liệu tạm thời và nhạy cảm.
    *   Mã hóa thành công đối tượng thành chuỗi JSON bằng `JSON.stringify()`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng / Thiếu trường bắt buộc:**
    *   Kiểm tra sự tồn tại của các trường bắt buộc (`reservationId`, `guestName`, `roomCode`).
    *   Phát hiện và ngăn chặn quy trình nếu đối tượng thiếu dữ liệu quan trọng hoặc chứa giá trị không hợp lệ (ví dụ: giá phòng âm).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao & Phục hồi JSON:**
    *   Giải mã chuỗi JSON an toàn bằng `JSON.parse()`.
    *   Kiểm tra tính toàn vẹn của đối tượng sau khi parse, đảm bảo các trường đã bị `delete` không còn xuất hiện trong chuỗi JSON cũng như đối tượng mới.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    *   Bắt lỗi và ném ra ngoại lệ/thông điệp lỗi rõ ràng bằng tiếng Việt khi dữ liệu đầu vào thiếu trường bắt buộc hoặc khi thao tác parse chuỗi JSON thất bại.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** 
    *   Đặt tên biến, hàm 100% bằng tiếng Anh theo quy chuẩn `camelCase` (ví dụ: `sanitizeBookingData`, `parseReservationJson`).
    *   Viết ghi chú giải thích logic bằng tiếng Việt có dấu rõ ràng. Không sử dụng các từ khóa hoặc thư viện bị cấm.
*   **[5 điểm] Nộp bài GitHub:** 
    *   Tạo repository và đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex8`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & Dynamic Key Mapping:**
    *   Xây dựng hàm làm sạch dữ liệu nhận vào danh sách mảng các key cần xóa một cách linh hoạt (Dynamic Keys Deletion) thay vì hard-code tên key, giúp tái sử dụng module cho nhiều loại phiếu dịch vụ khác nhau trong hệ thống HOTEL_BOOKING.

---

## [Vận dụng nâng cao 3] Quản Lý Chuẩn Hóa và Đóng Gói Dữ Liệu Đặt Phòng Khách Sạn

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Quản Lý Chuẩn Hóa và Đóng Gói Dữ Liệu Đặt Phòng Khách Sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:**
    *   Liệt kê đầy đủ các thuộc tính của Object thô đầu vào (các thuộc tính số, chuỗi, boolean, key động có dấu gạch ngang như `"check-in-hour"`).
    *   Mô tả chính xác kiểu dữ liệu và cấu trúc của chuỗi JSON đầu ra.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:**
    *   Giải thích đúng sự khác biệt giữa `delete` và gán `undefined` đối với dung lượng bộ nhớ và kết quả `JSON.stringify()`.
    *   Vẽ sơ đồ Mermaid đáp ứng đúng chuẩn 5 hình dạng (Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Action/Process, Diamond cho Condition). Tuyệt đối không dùng Parallelogram cho bước tính toán.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và thao tác thuộc tính:**
    *   Khai báo Object thô chuẩn xác, minh họa truy cập đúng bằng Bracket Notation cho tên key có dấu gạch ngang (`"check-in-hour"`).
    *   Thêm mới và cập nhật thành công các thuộc tính `earlyCheckInFee`, `extraGuestFee`, `totalPayment`, `isPaid`.
*   **[15 điểm] Lập trình tính toán phụ phí nghiệp vụ:**
    *   Tính đúng 30% phụ thu check-in sớm nếu `"check-in-hour"` < 12.
    *   Tính đúng phụ thu khách phát sinh khi `adultsCount` > `standardCapacity` (miễn phí `childrenUnder6`).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Làm sạch dữ liệu nhạy cảm (Sanitization):**
    *   Sử dụng chính xác toán tử `delete` để xóa bỏ hoàn toàn 3 thuộc tính: `securityCode`, `tempToken`, `internalNote`.
    *   Đảm bảo đối tượng sau khi làm sạch không còn tồn tại các key này trong bộ nhớ.
*   **[15 điểm] Đóng gói và Giải mã JSON an toàn:**
    *   Chuyển đổi thành công đối tượng sang chuỗi JSON hợp lệ bằng `JSON.stringify()`.
    *   Xây dựng hàm `restoreAndValidateBooking(jsonString)` giải mã thành công bằng `JSON.parse()` và thực hiện validate các key bắt buộc (`bookingId`, `roomCode`, `totalPayment`).

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    *   Xử lý ngoại lệ khi truyền vào chuỗi JSON sai cú pháp hoặc chuỗi rỗng bằng khối `try...catch`.
    *   Báo lỗi rõ ràng bằng tiếng Việt khi thiếu một trong các thuộc tính bắt buộc sau khi giải mã.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:**
    *   Tên biến, tên hàm 100% bằng Tiếng Anh chuẩn (camelCase).
    *   Ghi chú giải thích logic bằng Tiếng Việt có dấu đầy đủ, rõ ràng.
*   **[5 điểm] Nộp bài GitHub:**
    *   Tạo repository và đặt tên thư mục theo đúng cú pháp hướng dẫn `[Tên Lớp]_[Môn Học]_Session12_Ex9`.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:**
    *   Viết hàm tiện ích reusable (ví dụ: `sanitizeObject(obj, keysToRemove)`) nhận vào danh sách các key cần xóa và trả về object sạch một cách linh hoạt, dễ bảo trì cho các thực thể khác trong hệ thống.

---

## [Phân tích 1] Phân tích và Xử lý Đóng gói Dữ liệu Đặt phòng Khách sạn

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân tích và Xử lý Đóng gói Dữ liệu Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Trình bày độc lập, chi tiết ít nhất 2 phương án kỹ thuật xử lý dữ liệu đối tượng (ví dụ: Thao tác biến đổi trực tiếp trên đối tượng gốc `Mutation` vs Tạo đối tượng clone mới làm sạch `Immutability`/`Helper Function`).
    *   Phân tích cơ chế bộ nhớ và cách truy cập thuộc tính của từng phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Xây dựng bảng HTML đầy đủ 5 tiêu chí: Tốc độ xử lý, Dung lượng bộ nhớ, Khả năng bảo trì, Độ rõ ràng, Độ phù hợp.
    *   Bảng HTML có sử dụng attribute bắt buộc: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** 
    *   Lập luận chặt chẽ vì sao phương án được chọn phù hợp với hệ thống đặt phòng trực tuyến (đảm bảo tính an toàn dữ liệu nhạy cảm, tối ưu RAM, mã nguồn sạch).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** 
    *   Vẽ Mermaid Flowchart hoặc viết mã giả chính xác logic xử lý.
    *   Tuân thủ 100% chuẩn hình dạng Mermaid: Terminator `([ ])`, Input/Output `[/ /]`, Decision `?`, Process `[" "]`. Tuyệt đối không dùng sai ký hiệu khối.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** 
    *   Viết code JavaScript Vanilla (ES6+) chạy đúng yêu cầu nghiệp vụ.
    *   Sử dụng đúng Dot Notation cho key tiêu chuẩn và Bracket Notation cho key chứa dấu gạch ngang/biến động.
    *   Tính chính xác phụ thu check-in sớm (30% `basePrice`) và phụ thu trẻ em (`150000`).
    *   Dùng đúng từ khóa `delete` để loại bỏ `tempAuthToken` và `draftDiscountCode`.
    *   Sử dụng đúng `JSON.stringify()` và `JSON.parse()`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** 
    *   Không để xảy ra lỗi `ReferenceError` khi dùng ngoặc vuông.
    *   Không gán `undefined`/`null` thay cho `delete`.
    *   Không cố tình truy cập thuộc tính trên chuỗi JSON chưa parse.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** 
    *   Chuỗi JSON thu được hoàn toàn sạch sẽ, không chứa các token nhạy cảm tạm thời.
    *   Đối tượng khôi phục sau khi parse truy xuất chính xác các thuộc tính động và phụ phí.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** 
    *   Đặt tên biến/thuộc tính bằng tiếng Anh chuẩn chuẩn camelCase (`bookingReservation`, `checkInHour`, `basePrice`, `earlyCheckInFee`).
    *   Chú thích giải thích bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** 
    *   Đường link GitHub hợp lệ, đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session12_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** 
    *   Viết đoạn mã đo lường thời gian xử lý (dùng `console.time`/`console.timeEnd`) để so sánh hiệu năng giữa phương án xóa trực tiếp (`delete`) và phương án tạo bản sao đối tượng mới trước khi chuyển sang JSON.

---

## [Phân tích 2] Chuẩn hóa và Đóng gói Dữ liệu Đặt phòng Khách sạn Agoda

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Chuẩn hóa và Đóng gói Dữ liệu Đặt phòng Khách sạn Agoda — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự đề xuất độc lập tối thiểu 2 phương án xử lý đối tượng (ví dụ: Biến đổi trực tiếp trên đối tượng gốc bằng toán tử `delete` vs Khởi tạo đối tượng mới và trích xuất các thuộc tính hợp lệ). Phân tích rõ sự khác biệt về cấu trúc logic của từng phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Thiết lập đầy đủ bảng so sánh HTML chuẩn theo 5 tiêu chí: Tốc độ xử lý, Bộ nhớ tiêu tốn, Khả năng bảo trì, Độ rõ ràng mã nguồn và Mức độ phù hợp hệ thống. Phân tích sắc bén, logic.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Đưa ra lập luận thuyết phục về việc chọn giải pháp tối ưu phù hợp với quy mô ứng dụng đặt phòng Agoda.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Sử dụng Mermaid Flowchart biểu diễn quy trình xử lý. Tuân thủ 100% quy chuẩn hình học (Oval `([ ])` cho Bắt đầu/Kết thúc, Bình hành `[/ /]` cho I/O, Chữ nhật `[" "]` cho Tiến trình/Tính toán, Hình thoi `?` cho Rẽ nhánh điều kiện).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Xây dựng mã nguồn JavaScript Vanilla ES6+ thực thi chính xác các bước: tính phụ thu `earlyCheckInFee` (30% khi `checkInHour < 12`), tính `totalAmount`, sử dụng `delete` để xóa `tempToken` và `draftSessionId`, truy xuất đúng key gạch ngang bằng Bracket Notation `["special-request"]`, và thực hiện chuyển đổi JSON qua lại.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Tránh bẫy lỗi gán `undefined` làm phình bộ nhớ đối tượng.
    *   Tránh bẫy lỗi cú pháp SyntaxError khi đọc key có ký tự đặc biệt.
    *   Kiểm tra tính hợp lệ của dữ liệu trước và sau khi `JSON.parse()`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Kết quả in ra console và chuỗi JSON đầu ra phải loại bỏ hoàn toàn các key rác, tính đúng tổng tiền thanh toán, hiển thị đầy đủ thông tin phòng đặt theo đúng yêu cầu nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến/hàm/thuộc tính chuẩn Tiếng Anh (camelCase), chú thích logic bằng Tiếng Việt có dấu. Tuyệt đối không dùng các từ cấm (frameworks, ORM, REST API, HTTP codes).
*   **[5 điểm] Nộp bài GitHub:** Nộp đúng đường dẫn repository GitHub theo định dạng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session12_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Xây dựng đoạn mã JavaScript sử dụng `console.time()` và `console.timeEnd()` để đo đạc thời gian thực thi của cả 2 giải pháp trên tập mẫu 10,000 lượt đặt phòng thô, rút ra kết luận thực nghiệm về hiệu năng.

---

## [Phân tích 3] Chuẩn hóa và đóng gói dữ liệu đặt phòng khách sạn

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Chuẩn hóa và đóng gói dữ liệu đặt phòng khách sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Trình bày rõ ràng cấu trúc tư duy của 2 phương án (Ví dụ: Phương án thao tác trực tiếp trên Object ban đầu - Direct Mutation; Phương án khởi tạo Object sạch mới và trích xuất trường - Object Transformation).
    *   Nêu rõ sự khác biệt về cú pháp truy cập thuộc tính tĩnh (Dot Notation) và thuộc tính động có ký tự đặc biệt (Bracket Notation).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Khởi tạo bảng so sánh đúng cấu trúc HTML style: `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`.
    *   So sánh đầy đủ 5 tiêu chí: Tốc độ xử lý, Tiêu tốn bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Ngữ cảnh áp dụng.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Phân tích lý do chọn phương án tối ưu dựa trên việc tránh rò rỉ dữ liệu nhạy cảm (`creditCardCVV`) và tối ưu vùng nhớ cho ứng dụng Hotel Booking.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ Mermaid Flowchart chính xác theo chuẩn 5 hình dạng (Oval cho Start/End, Parallelogram cho In/Out, Rectangle cho Process, Diamond cho Decision).
    *   Tuyệt đối không vi phạm bẫy lỗi dùng Parallelogram cho khối tính toán.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Khai báo Object `bookingData` ban đầu đầy đủ thuộc tính nghiệp vụ.
    *   Sử dụng Bracket Notation đúng cách để thêm/cập nhật thuộc tính `"early-checkin-fee"`.
    *   Tính toán chính xác `totalAmount` và gắn trường `isChildExempt`.
    *   Sử dụng đúng từ khóa `delete` để loại bỏ `creditCardCVV` và `tempAuthToken`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Bắt lỗi nếu `checkInHour` không hợp lệ (nhỏ hơn 0 hoặc lớn hơn 23).
    *   Đảm bảo thuộc tính bị `delete` không còn xuất hiện trong chuỗi JSON thu được.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Sử dụng `JSON.stringify()` để tạo chuỗi JSON hợp lệ.
    *   Sử dụng `JSON.parse()` để giải mã và truy xuất thành công thuộc tính `"early-checkin-fee"` từ Object đã khôi phục.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến/hàm 100% bằng tiếng Anh chuẩn camelCase (ví dụ: `roomPricePerNight`, `earlyCheckInFee`, `sanitizedBooking`).
    *   Chú thích mã nguồn bằng Tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub hợp lệ, thư mục đặt tên đúng định dạng quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Xây dựng đoạn mã đo lường thời gian thực thi (sử dụng `console.time` / `console.timeEnd`) để so sánh hiệu năng xử lý 10,000 lượt đặt phòng giữa 2 phương án kỹ thuật.

---

## [Sáng tạo 1] Thiết kế Module Đóng gói và Xử lý Payload Đặt phòng Khách sạn

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế Module Đóng gói và Xử lý Payload Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc đối tượng `BookingReservation` sáng tạo, hợp lý, đầy đủ thuộc tính cơ bản (id, customerName, basePrice) và thuộc tính có tên key chứa ký tự đặc biệt (ví dụ: `early-checkin-fee`, `extra-services`). Định nghĩa chuỗi JSON đầu ra minh bạch.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện và mô tả rõ ràng tối thiểu 3 bẫy lỗi kỹ thuật liên quan đến Object & JSON (Lỗi ReferenceError do truyền biến chưa khai báo vào Bracket Notation, lỗi SyntaxError do dùng Dot Notation cho key gạch ngang, lỗi giữ lại key ẩn do gán `undefined` thay vì dùng `delete`, hoặc lỗi khi parse JSON không đúng cú pháp).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid đúng cú pháp. Sử dụng chính xác 100% quy chuẩn hình dạng:
    *   Hình Stadium/Oval `([ ])` cho Start/End.
    *   Hình Bình hành `[/ /]` cho Input/Output.
    *   Hình Chữ nhật `[" "]` cho Process/Action (Tuyệt đối không dùng bình hành cho hành động xử lý).
    *   Hình Thoi `?` cho Decision.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày mạch lạc logic từng giai đoạn chuyển đổi dữ liệu từ đối tượng gốc -> đối tượng sau làm sạch -> chuỗi JSON đóng gói -> đối tượng phục hồi.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Mã nguồn JavaScript vận dụng linh hoạt Dot Notation cho key chuẩn và Bracket Notation cho key chứa ký tự đặc biệt. Thực hiện tính toán phụ thu check-in sớm hoặc phụ thu người ở thêm chính xác.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Sử dụng chuẩn xác từ khóa `delete` để xóa bỏ hoàn toàn các trường dữ liệu tạm thời/nhạy cảm (như `temp-token`, `secret-code`) trước khi thực hiện `JSON.stringify()`. Đảm bảo chuỗi JSON thu được hoàn toàn sạch sẽ.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các đoạn mã kiểm tra (Guard Clauses) hoặc xử lý an toàn nhằm ngăn ngừa các lỗi biên đã mô tả ở Phần 2 (ví dụ: kiểm tra sự tồn tại của thuộc tính trước khi parse hoặc truy cập dynamic key).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết bằng JavaScript ES6+, đặt tên biến/hàm 100% bằng Tiếng Anh (camelCase), chú thích giải thích logic bằng Tiếng Việt có dấu, mã nguồn phân chia hàm rõ ràng ngăn ngắn.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đóng gói thư mục đúng tên theo yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex13`, có file README.md mô tả dự án và hướng dẫn chạy file script.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng thêm hàm hỗ trợ sao lưu (Backup snapshot) đối tượng ban đầu trước khi xóa key nhạy cảm hoặc kiểm tra tính toàn vẹn của dữ liệu sau khi `JSON.parse()`.

---

## [Sáng tạo 2] Thiết kế Phân hệ Quản lý Đặt phòng Động và Chuẩn hóa JSON Payload

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Phân hệ Quản lý Đặt phòng Động và Chuẩn hóa JSON Payload — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc dữ liệu Object đặt phòng đầy đủ các trường thông tin tiêu chuẩn, trường phụ thu động và trường nhạy cảm; thể hiện rõ cấu trúc trước và sau khi làm sạch/đóng gói JSON.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Nhận diện ít nhất 3 bẫy dữ liệu thực tế (như sai cú pháp khi dùng Dot Notation cho key có ký tự đặc biệt, lỗi lãng phí bộ nhớ do dùng `undefined` thay cho `delete`, lỗi thao tác thuộc tính trực tiếp trên chuỗi JSON chưa được parse).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác vòng đời dữ liệu từ khởi tạo đối tượng, cập nhật dynamic property, xóa dữ liệu nhạy cảm, đến serialization và deserialization JSON.
*   **[10 điểm] Thiết kế quy chuẩn Mermaid:** Tuân thủ 100% quy chuẩn hình dạng node trong sơ đồ Mermaid (Oval cho Bắt đầu/Kết thúc, Chữ nhật cho Xử lý, Bình hành cho Đầu vào/Đầu ra, Hình thoi cho Điều kiện).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Thực hiện chính xác thao tác thêm/cập nhật phụ phí đặt phòng (`early-checkin-fee`, phụ thu người phát sinh) bằng Bracket Notation và Dynamic Key Access.
*   **[15 điểm] Chuẩn hóa và Đóng gói JSON Payload:** Sử dụng đúng từ khóa `delete` để loại bỏ hoàn toàn các trường nhạy cảm (`tempToken`, `paymentGatewayPin`) trước khi chuyển đổi bằng `JSON.stringify` và giải mã phục hồi chính xác bằng `JSON.parse`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng câu lệnh kiểm tra (guards) hoặc logic an toàn để ngăn chặn các bẫy dữ liệu đã liệt kê ở Phần 2 trong mã nguồn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết sạch sẻ, định danh biến/hàm bằng tiếng Anh rõ nghĩa (`bookingReservation`, `earlyCheckinFee`, `sanitizeBookingPayload`), chú thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session12_Ex14` kèm tệp Readme giải thích luồng hoạt động.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Viết thêm hàm mô phỏng việc kiểm thử tự động (Audit Log) so sánh dung lượng/danh sách key của Object trước và sau khi sanitize để chứng minh các trường nhạy cảm đã bị xoá hoàn toàn khỏi bộ nhớ.

---

## [Sáng tạo 3] Thiết Kế Hệ Thống Đóng Gói Và Quản Lý Hóa Đơn Đặt Phòng Khách Sạn

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết Kế Hệ Thống Đóng Gói Và Quản Lý Hóa Đơn Đặt Phòng Khách Sạn — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc dữ liệu Object đầy đủ các trường nghiệp vụ (mã đặt phòng, giá phòng, thông tin khách, thuộc tính tạm thời) và chuỗi JSON kết xuất chuẩn xác.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 bẫy lỗi nghiệp vụ/kỹ thuật (ví dụ: dùng sai Dot notation cho key có gạch ngang, nhầm lẫn giữa gán `undefined` và dùng `delete`, cố truy xuất thuộc tính trên chuỗi JSON chưa được `JSON.parse`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác vòng đời dữ liệu từ Object -> Thao tác CRUD -> Stringify -> Parse. Tuân thủ 100% quy chuẩn hình dạng Mermaid (Rectangle cho Process, Parallelogram CHỈ cho Input/Output, Diamond cho Decision, Oval cho Start/End).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích cơ chế biến đổi trạng thái của Object và quá trình đóng gói JSON minh bạch, logic.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Áp dụng chính xác quy tắc phụ thu check-in sớm, chính sách trẻ em và cập nhật thành công các thuộc tính bằng cả Dot Notation và Bracket Notation (truy cập dynamic key).
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Sử dụng từ khóa `delete` để loại bỏ hoàn toàn các trường dữ liệu tạm thời/nhạy cảm trước khi đóng gói bằng `JSON.stringify()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết mã nguồn kiểm tra hoặc truy xuất an toàn, tránh bị ngắt chương trình do ReferenceError hoặc SyntaxError khi xử lý Object và JSON.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Tên biến/hàm đặt bằng Tiếng Anh chuẩn camelCase (`roomPrice`, `earlyCheckInSurcharge`, `serializeInvoice`), giải thích logic bằng Tiếng Việt chuẩn.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo đúng thư mục bài tập theo cú pháp `[Tên Lớp]_[Môn Học]_Session12_Ex15` với file mã nguồn chạy độc lập thành công trên Node.js hoặc Browser Console.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Viết thêm mô-đun đối soát dữ liệu So sánh Object ban đầu và Object sau khi Parse từ JSON để phát hiện các thuộc tính đã bị loại bỏ (Audit log).

---

## [Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
- Trình bày rõ ràng cấu trúc dữ liệu đối tượng (Key-Value) và luồng thao tác biến đổi thuộc tính (10 điểm).
- Trình bày chính xác luồng chuyển đổi hai chiều giữa JavaScript Object và chuỗi dữ liệu JSON (10 điểm).

#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
- Khai báo Object Literal đúng cú pháp và truy cập chính xác bằng cả 3 cách: Dot Notation, Bracket Notation, Dynamic Key Access (15 điểm).
- Thực hiện chuẩn xác các thao tác Thêm thuộc tính mới, Sửa thuộc tính cũ và Xóa bỏ thuộc tính nhạy cảm/tạm thời bằng toán tử `delete` (15 điểm).
- Áp dụng thành thạo `JSON.stringify()` để đóng gói dữ liệu và `JSON.parse()` để giải mã đối tượng (10 điểm).

#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
- Xử lý xóa triệt để thuộc tính bằng toán tử `delete`, tránh bẫy gán `undefined` khiến key vẫn tồn tại trong Object (10 điểm).
- Tránh bẫy lỗi cú pháp (`SyntaxError`) khi dùng Dot Notation cho key chứa dấu gạch ngang và bẫy `ReferenceError` khi dùng Bracket Notation không đóng nháy (10 điểm).

#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
- Đặt tên biến, tên key theo chuẩn camelCase (trừ các key đặc biệt theo yêu cầu nghiệp vụ), mã nguồn rõ ràng (10 điểm).
- Cấu trúc thư mục nộp bài chuẩn quy định: `[Tên Lớp]_[Môn Học]_Session12_Demo` (10 điểm).

---

## [Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap)

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
- ** Object Literal & Truy cập thuộc tính (10 điểm):**
  - Thể hiện rõ cấu trúc Key-Value.
  - Phân biệt chính xác Dot Notation và Bracket Notation.
  - Giải thích đúng cơ chế Dynamic Key Access (truy cập key thông qua biến).
- ** Thao tác CRUD Thuộc tính (10 điểm):**
  - Đầy đủ các thao tác: Create (Thêm), Read (Đọc), Update (Sửa), Delete (Xóa bằng toán tử `delete`).
  - Phân tích hậu quả của việc dùng `undefined` thay vì `delete`.
- ** Cấu trúc JSON & Bẫy lỗi nghiệp vụ (10 điểm):**
  - Trình bày đúng vai trò và cú pháp của `JSON.stringify()` và `JSON.parse()`.
  - Bao phủ đủ 4 bẫy lỗi chính (`ReferenceError`, `SyntaxError`, lãng phí bộ nhớ với `undefined`, và lỗi truy cập thuộc tính trên chuỗi JSON chưa được `parse`).

---

#### **2. Phân tầng logic & Mối liên kết — 30 điểm**
- ** Tầng nút trung tâm (Root Node) (5 điểm):** Đặt tên rõ ràng, làm nổi bật chủ đề *Session 12: Object & JSON trong HOTEL_BOOKING*.
- ** Tầng nhánh chính (Main Branches) (10 điểm):** Chia thành 3-4 nhánh chính logic, không bị chồng chéo khái niệm.
- ** Tầng nhánh phụ (Sub-branches) & Minh họa nghiệp vụ (15 điểm):** 
  - Phân tầng chi tiết từ khái niệm lý thuyết đến cú pháp mã nguồn và ví dụ thực tế trong bài toán Đặt phòng khách sạn (ví dụ: `bookingTicket`, `customerProfile`).
  - Thể hiện được mối liên kết giữa việc khai báo Object -> Biến đổi CRUD -> Đóng gói JSON truyền dữ liệu.

---

#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
- ** Trực quan & Thẩm mỹ (10 điểm):** Sử dụng màu sắc phân biệt giữa các nhánh, icon minh họa bẫy lỗi (Cảnh báo/Bẫy lỗi/Thực hành tốt), chữ viết rõ ràng, không đè chữ.
- ** Định dạng tệp tin đầy đủ (10 điểm):** Có đủ file ảnh (`.png`/`.jpg`) sắc nét và file gốc (`.xmind`/`.pdf`) theo đúng yêu cầu bài toán.

---

#### **4. Bản tóm tắt giải trình (summary.md) — 10 điểm**
- ** Cấu trúc văn bản (3 điểm):** Trình bày mạch lạc bằng định dạng Markdown, có tiêu đề, danh sách, khối mã nguồn (code block).
- ** Minh họa Code JavaScript thực tế (4 điểm):** Cung cấp mã nguồn ví dụ hoàn chỉnh chạy không lỗi, áp dụng domain `HOTEL_BOOKING` (Khai báo đối tượng đặt phòng -> Thêm thuộc tính động -> Xóa token tạm bằng `delete` -> Chuyển sang JSON và ngược lại).
- ** Giải thích bẫy lỗi sâu sắc (3 điểm):** Phân tích rõ nguyên nhân và cách khắc phục cho 4 bẫy lỗi trọng tâm của buổi học.

---

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
- ** Đặt tên Repository chuẩn (5 điểm):** Đúng cú pháp `[Tên Lớp]_[Môn Học]_Session12_Mindmap` (Ví dụ: `HNKS25CNTT1_Core_Session12_Mindmap`).
- ** Cấu trúc thư mục đúng quy chuẩn (5 điểm):** Đẩy đầy đủ các file `mindmap.png` (hoặc `.jpg`), `mindmap.xmind` (hoặc `.pdf`), và `summary.md` lên thư mục gốc của repository.

---

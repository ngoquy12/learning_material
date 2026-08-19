# [Vận dụng cơ bản 1] Sửa lỗi tính phí hành lý quá cước tại quầy check-in

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính phí hành lý quá cước tại quầy check-in — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng lệnh kiểm tra điều kiện `else if (baggageWeight > 7)` đặt sai thứ tự ưu tiên logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền hoàn chỉnh bảng Test Case với ít nhất 3 kịch bản kiểm thử (bao gồm các mốc 5kg, 25kg, 40kg) phản ánh chính xác sự khác biệt giữa Buggy Output và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh lại chuỗi điều kiện `if / else if` theo đúng thứ tự (kiểm tra từ mốc cao nhất xuống mốc thấp nhất hoặc sử dụng điều kiện khoảng cách hợp lý `> 7 && <= 20`).
*   **[20 điểm] Tính toán chính xác công thức quá cước:** Áp dụng đúng công thức tính phí phát sinh cho hành lý trên 35 kg ($500.000 + (baggageWeight - 35) \times 50.000$).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra và loại bỏ các giá trị trọng lượng âm (`baggageWeight < 0`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp dữ liệu đầu vào bị rỗng, `null`, `undefined` hoặc không phải kiểu số (`isNaN`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao việc sắp xếp thứ tự biểu thức điều kiện trong cấu trúc `if - else if` lại quan trọng và nêu bẫy lập trình "điều kiện bao quát đặt lên trước điều kiện chi tiết".

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng JavaScript ES6+ chuẩn mực, căn lề 2 spaces, khai báo hằng số `const`/`let` phù hợp, tên biến chuẩn tiếng Anh (`baggageWeight`, `excessFee`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex1` trên GitHub.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động đơn giản:** Viết một hàm JavaScript hỗ trợ tự động chạy kiểm thử danh sách mốc hành lý đầu vào và in kết quả PASSED/FAILED ra terminal console.

---

## [Vận dụng cơ bản 2] Sửa lỗi trôi lệnh trong module tính phí hành lý ký gửi

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi trôi lệnh trong module tính phí hành lý ký gửi — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
* **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng code thiếu câu lệnh `break;` trong trường hợp `case "Business"`.
* **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 2 dòng còn lại trong bảng Test Case với đầy đủ thông tin Input, Buggy Output, Expected Output và giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
* **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Khắc phục hoàn toàn lỗi trôi lệnh (fall-through), bổ sung đầy đủ lệnh `break;` cho tất cả các nhánh trong `switch-case`.
* **[20 điểm] Tính toán chính xác cước phí quá cước:** Áp dụng đúng biểu thức toán tử ba ngôi để tính `excessWeight` và `excessFee` đúng quy định (50.000 VNĐ/kg quá cước).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
* **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra thành công điều kiện trọng lượng `actualWeight` phải là kiểu số (`typeof actualWeight === "number"`) và lớn hơn hoặc bằng 0. Trả về đúng thông báo `"Trọng lượng hành lý không hợp lệ"`.
* **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý nhánh `default` chính xác khi gặp hạng vé nằm ngoài danh mục `Business`, `Deluxe`, `Eco`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
* **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế hoạt động của hành vi fall-through trong `switch-case` của JavaScript và lý do tại sao thiếu `break;` lại tạo ra sai sót nghiệp vụ nghiêm trọng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng ES6+, sử dụng `const`/`let` đúng mục đích, tên biến tiếng Anh chuẩn Clean Code, thụt lề 2 spaces rõ ràng.
* **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository tuân thủ chính xác cấu trúc thư mục `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
* **[10 điểm] Viết bộ kiểm thử tự động (Test Runner):** Tạo hàm chạy thử tự động gọi `calculateBaggageFee` với nhiều bộ dữ liệu biên và in ra nhãn PASS/FAIL trực quan trên console.

---

## [Vận dụng cơ bản 3] Sửa lỗi tính phí hành lý ký gửi khi Check-in máy bay

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi tính phí hành lý ký gửi khi Check-in máy bay — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác 2 lỗi logic lớn:
    1. Lỗi thứ tự điều kiện trong khối `if...else if` (kiểm tra `baggageWeight > 7` trước nên các giá trị > 15 kg và > 25 kg không bao giờ chạm tới).
    2. Lỗi trôi lệnh (fall-through) do thiếu từ khóa `break` trong `case "DELUXE"` của câu lệnh `switch-case`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác 100% các giá trị còn thiếu (`...`) trong Bảng Test Case ở Phần 1 (bao gồm Buggy Output, Expected Output, Dòng code gây lỗi, và Giải thích nguyên nhân).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công khối `if...else if` (đặt điều kiện `> 25` lên đầu, hoặc đảo chiều so sánh tăng dần hợp lý) và thêm `break` đầy đủ vào câu lệnh `switch-case`.
*   **[20 điểm] Tính toán chính xác các trường hợp cước hành lý:**
    *   Hành lý <= 7kg: Phí cơ bản 0 VNĐ.
    *   Hành lý 8kg - 15kg: Phí 150.000 VNĐ.
    *   Hành lý 16kg - 25kg: Phí 300.000 VNĐ.
    *   Hành lý > 25kg: Tính đúng 500.000 VNĐ + 50.000 VNĐ/kg quá cước.
    *   Áp dụng chuẩn xác giảm giá theo hạng vé `BUSINESS` (giảm 100%), `DELUXE` (giảm 50%), `ECO` (giảm 0%).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra khối lượng hành lý `baggageWeight` không được âm (`< 0`) hoặc là `NaN`/không phải kiểu số (`typeof baggageWeight !== 'number'`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp `ticketClass` không hợp lệ thông qua nhánh `default` trong `switch-case` mà không làm ứng dụng bị văng lỗi runtime.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn cơ chế Fall-through trong `switch-case` (khi nào là tính năng có lợi, khi nào là lỗi lập trình) và tại sao thứ tự kiểm tra điều kiện lại vô cùng quan trọng trong chuỗi `if...else if`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng bằng Tiếng Anh (`ticketClass`, `baggageWeight`, `baseFee`, `discountRate`), thụt lề chuẩn 2 spaces, ghi chú thích giải thích logic bằng Tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu bằng Toán tử Ba ngôi (Ternary Operator):** Sử dụng toán tử ba ngôi để tính nhanh mức phí hành lý cho các trường hợp đơn giản hoặc tính tỷ lệ giảm giá một cách ngắn gọn, sạch đẹp nhưng vẫn đảm bảo tính dễ đọc của mã nguồn.

---

## [Vận dụng cơ bản 4] Sửa lỗi tính phí dịch vụ check-in và chọn vị trí ghế máy bay

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính phí dịch vụ check-in và chọn vị trí ghế máy bay — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng lệnh thiếu từ khóa `break;` trong khối `case 3` của câu lệnh `switch-case`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác thông tin cho các dòng STT 2 và STT 3 trong bảng báo cáo kiểm thử (Input, Buggy Output, Expected Output, Failing Line, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Bổ sung đầy đủ lệnh `break;` vào cuối tất cả các trường hợp `case` trong cấu trúc `switch-case`, đảm bảo không bị lỗi trôi lệnh (fall-through).
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng cấu trúc rẽ nhánh chính xác để xử lý trường hợp mã hạng vé không hợp lệ (`default`), gán đúng tên hạng và tính tổng phí bằng 0 VNĐ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra số cân hành lý không được là số âm (`baggageWeight >= 0`). Nếu âm thì thông báo dữ liệu không hợp lệ.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo khi `ticketClass` nhận giá trị bất kỳ nằm ngoài tập {1, 2, 3}, chương trình vẫn chạy an toàn, không sinh lỗi Runtime hoặc kết quả NaN.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích bản chất hiện tượng trôi lệnh (fall-through) trong `switch-case` của JavaScript và nêu rõ trường hợp nào trong thực tế lập trình chủ động áp dụng kỹ thuật fall-through có mục đích.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng theo tiếng Anh (`ticketClass`, `baggageWeight`, `seatFee`), thụt lề chuẩn 2 spaces, ghi chú rõ ràng bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub theo đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết đoạn mã kịch bản tự động kiểm thử cả 3 trường hợp hạng vé (Eco, Deluxe, Business) và in ra kết quả thông qua console (PASSED / FAILED).

---

## [Vận dụng cơ bản 5] Debug logic tính phí chọn ghế và hành lý máy bay

### **Tiêu chí chấm điểm (AI)**
**[Sửa lỗi code] Debug Logic Tính Phí Chọn Ghế Và Hành Lý Máy Bay — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng thiếu lệnh `break` trong `switch-case` và dòng điều kiện tính sai phí hành lý quá cước.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ các dòng còn thiếu trong bảng Test Case với đầy đủ thông số đầu vào, đầu ra thực tế bị lỗi, đầu ra kỳ vọng và giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng cấu trúc `switch-case` có đầy đủ `break` cho từng trường hợp hạng vé (Eco, Deluxe, Business) và tính đúng `seatFee`.
*   **[20 điểm] Xử lý chính xác điều kiện hành lý quá cước:** Áp dụng câu lệnh điều kiện `if (baggageWeight > 7)` hoặc toán tử ba ngôi để tính đúng phí `(baggageWeight - 7) * 50000` và gán 0 cho trường hợp `<= 7 kg`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Xử lý trường hợp `ticketClass` không thuộc tập `[1, 2, 3]` bằng khối `default` trong `switch-case` hoặc kiểm tra điều kiện bảo vệ (guard clause).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra trọng lượng hành lý âm (`baggageWeight < 0`) và không làm sập chương trình.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn khái niệm "Fall-through" trong `switch-case`, khi nào nên chủ động dùng và khi nào là lỗi lập trình.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng bằng tiếng Anh (`seatFee`, `excessBaggageFee`, `ticketClass`), căn lề chuẩn 2 spaces, comment bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản Kiểm thử Tự động:** Viết hàm tự động chạy qua mảng dữ liệu test case và so sánh kết quả trả về với kết quả kỳ vọng (sử dụng câu lệnh `console.assert` hoặc `console.table`).

---

## [Vận dụng cơ bản 6] Sửa lỗi tính phí hành lý ký gửi quá cước Vietjet

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính phí hành lý ký gửi quá cước Vietjet — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí thiếu lệnh `break;` trong khối `case 1` của cấu trúc `switch-case` (dòng 9-13).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu cho Row 2 và Row 3 trong bảng Test Case (Input, Buggy Output, Expected Output, Dòng lỗi, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa lỗi thiếu từ khóa `break;` trong `switch-case`, giúp hệ thống gán chính xác `ticketClassName` và `freeAllowance` cho hạng vé Eco, Deluxe và Business.
*   **[20 điểm] Tính toán chính xác chi phí:** Số kg quá cước (`excessWeight`) và tổng phí phạt (`excessFee`) được tính đúng theo mức giá 50.000 VNĐ/kg và không bị giá trị âm khi hành lý nhỏ hơn hạn mức.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate mã hạng vé đầu vào:** Khối `default` xử lý chính xác các trường hợp mã hạng vé không hợp lệ (ví dụ: `ticketClassCode = 99` hoặc âm).
*   **[10 điểm] An toàn hệ thống:** Chương trình ngắt tính toán hoặc hiển thị cảnh báo phù hợp khi mã hạng vé không hợp lệ, không gây tính toán ra số tiền sai.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Giải thích hiện tượng Fall-through:** Giải thích rõ bản chất của hiện tượng trôi lệnh (fall-through) trong `switch-case` và lý do vì sao luôn cần từ khóa `break;` cuối mỗi nhánh case nếu không có ý định gộp nhánh.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn tiếng Anh (`ticketClassCode`, `freeAllowance`, `excessFee`), căn lề chuẩn 2 spaces, mã nguồn rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository theo đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session06_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết hàm/kịch bản kiểm thử tự động:** Viết đoạn mã gọi thử nghiệm nhiều bộ dữ liệu đầu vào khác nhau để tự động in ra thông báo PASS/FAIL cho từng case.

---

## [Vận dụng nâng cao 1] Hệ thống tính phí cước hành lý sân bay tự động

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Hệ thống tính phí cước hành lý sân bay tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đầy đủ danh sách biến đầu vào (`ticketClass`, `baggageWeight`, `passengerType`, `isVipMember`) và đầu ra (`freeAllowance`, `excessWeight`, `totalPenalty`), gán đúng kiểu dữ liệu.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ sơ đồ luồng Mermaid đầy đủ logic nghiệp vụ, sử dụng chuẩn xác 5 dạng hình (Oval cho Start/End, Parallelogram cho I/O, Diamond cho điều kiện, Rectangle cho tính toán).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo hằng số và biến bằng `const`/`let` chuẩn ES6+, thiết lập bộ dữ liệu test case minh bạch.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Kết hợp chính xác `if-else` (tính hạn mức miễn cước cơ bản và ưu đãi), `switch-case` (tra cứu đơn giá phạt theo hạng vé) và toán tử ba ngôi (tính phụ phí quá tải > 15 kg).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Xử lý chính xác trường hợp hành lý không quá cước (`excessWeight <= 0` thì phí phạt bằng 0) và tính phụ phí 200.000 VNĐ khi `excessWeight > 15`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Bắt bẫy trọng lượng âm (`baggageWeight < 0`) và xử lý hạng vé không tồn tại bằng nhánh `default` trong `switch-case`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Hiển thị thông báo lỗi rõ ràng, chuyên nghiệp ra console khi phát hiện dữ liệu đầu vào không hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Đặt tên biến hoàn toàn bằng tiếng Anh theo quy tắc camelCase, căn lề chuẩn 2 spaces, ghi chú thích giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đặt tên thư mục đúng định dạng quy định `[Tên Lớp]_[Môn Học]_Session06_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Viết mã nguồn ngắn gọn, tối ưu luồng kiểm tra logic không bị lặp dư thừa, áp dụng nguyên lý DRY (Don't Repeat Yourself).

---

## [Vận dụng nâng cao 2] Triển khai logic kiểm tra check-in và tính toán phụ phí hành lý hàng không

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Triển khai logic kiểm tra check-in và tính toán phụ phí hành lý hàng không — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:**
    *   Xác định đúng và đầy đủ kiểu dữ liệu các tham số đầu vào (`ticketClass`: string, `passengerTier`: string, `handBaggageWeight`: number, `checkedBaggageWeight`: number, `isPriorityBoarding`: boolean).
    *   Xác định đúng kết quả đầu ra (tổng trọng lượng ký gửi thực tế, tổng phụ phí hành lý, phí ưu tiên, tổng chi phí thanh toán, trạng thái check-in).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:**
    *   Trình bày sơ đồ luồng quy trình xử lý logic bằng chuẩn Mermaid Flowchart.
    *   Tuân thủ nghiêm ngặt quy chuẩn hình dạng Mermaid (Hình thoi cho điều kiện, Hình chữ nhật cho tính toán, Hình bình hành cho I/O, Oval cho Start/End). Không dùng sai hình chữ nhật / hình bình hành.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Áp dụng đúng cấu trúc rẽ nhánh theo quy định:**
    *   Sử dụng `switch-case` chính xác để xác định hạn mức theo `ticketClass` có đầy đủ `break` và `default`.
    *   Sử dụng `if...else if...else` chính xác để tính toán dồn kg xách tay vượt mức và ưu đãi theo `passengerTier`.
    *   Sử dụng toán tử ba ngôi `ternary operator` đơn cho tính phí Boarding ưu tiên và gán trạng thái check-in.
*   **[15 điểm] Tính toán phụ phí và đơn giá cước lũy tiến:**
    *   Tính đúng logic chuyển kg dư thừa xách tay sang ký gửi.
    *   Áp dụng chuẩn đơn giá 50.000 VNĐ/kg hoặc đơn giá lũy tiến 75.000 VNĐ/kg khi tổng ký gửi vượt 40 kg.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy vượt ngưỡng an toàn quy định:**
    *   Bắt chính xác bẫy tổng hành lý ký gửi thực tế vượt quá 50 kg, đưa ra trạng thái `"REJECTED_OVERWEIGHT"` và cảnh báo an toàn.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:**
    *   Chặn các trường hợp cân nặng bị âm (`handBaggageWeight < 0` hoặc `checkedBaggageWeight < 0`).
    *   Xử lý trường hợp hạng vé hoặc hạng hội viên nhập không hợp lệ (không nằm trong danh sách chuẩn) bằng thông báo lỗi hệ thống.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    *   In ra thông báo rõ ràng, chuyên nghiệp trên console về chi tiết hóa đơn check-in, phân rã từng khoản phí và nguyên nhân từ chối nếu bị quá cước an toàn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:**
    *   Đặt tên biến/hằng số hoàn toàn bằng tiếng Anh rõ nghĩa (`ticketClass`, `allowanceWeight`, `excessFee`, `checkinStatus`).
    *   Chú thích giải thích bằng tiếng Việt có dấu đầy đủ, thụt lề 2 spaces chuẩn ES6+.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đẩy mã nguồn lên repository GitHub đúng cấu trúc tên thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:**
    *   Tổ chức code dưới dạng hàm ES6 hoàn chỉnh nhận tham số đầu vào và trả về đối tượng kết quả (`Object`) chứa đầy đủ thông tin hóa đơn phụ thu, tránh sử dụng biến toàn cục dư thừa.

---

## [Vận dụng nâng cao 3] Tính Phí Hành Lý Quá Cước Và Phụ Phí Chọn Ghế Máy Bay

### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Tính Phí Hành Lý Quá Cước Và Phụ Phí Chọn Ghế Máy Bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định chính xác các biến đầu vào (`ticketClassCode`, `carryOnWeight`, `checkedWeight`, `seatSelectionType`, `isPriorityCheckin`) kèm kiểu dữ liệu và các biến đầu ra (`excessCarryOn`, `totalCalculatedCheckedWeight`, `overweightKg`, `baggageFee`, `bulkyBaggageFee`, `seatFee`, `priorityFee`, `totalSurcharge`, `checkinStatus`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ sơ đồ luồng Mermaid Flowchart đúng quy chuẩn hình khối (Terminator `([ ])`, I/O `[/ /]`, Decision `Kiểm tra?`, Process `[" "]`) mô tả chính xác quy trình xử lý dữ liệu và các điểm rẽ nhánh.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo biến/hằng số chuẩn xác trong ES6 (`const`, `let`), lưu trữ các hằng số hạn mức (7kg xách tay; 0kg, 20kg, 40kg ký gửi) và mức phạt cồng kềnh (500.000 VNĐ).
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** 
    *   Tính toán chuẩn xác phần dồn cước xách tay quá hạn sang ký gửi.
    *   Sử dụng cấu trúc `switch-case` chính xác cho 3 mã hạng vé để tính phụ phí ghế ngồi đúng bảng giá.
    *   Sử dụng toán tử ba ngôi để gán trạng thái `checkinStatus`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu vượt ngưỡng & cộng dồn:** Xử lý đúng trường hợp tổng hành lý ký gửi tính toán vượt ngưỡng `50 kg` (cộng thêm 500.000 VNĐ) và không phụ thu phí ưu tiên với Hạng Business.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kiểm tra và chặn các trường hợp trọng lượng âm (`carryOnWeight < 0`, `checkedWeight < 0`), mã hạng vé khác {1, 2, 3} và mã ghế khác {1, 2, 3}.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất thông báo lỗi rõ ràng khi phát hiện dữ liệu không hợp lệ (ví dụ: `[ERROR] Mã hạng vé không hợp lệ`) và in hóa đơn thanh toán chi tiết khi dữ liệu hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Đặt tên biến/hằng số hoàn toàn bằng tiếng Anh theo chuẩn camelCase, viết ghi chú tiếng Việt có dấu rõ ràng, căn lề chuẩn 2 spaces.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session06_Ex9`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Tối ưu hóa cấu trúc rẽ nhánh, tránh lặp lại các đoạn mã thừa, viết mã nguồn theo phong cách Clean Code dễ đọc và có tính mở rộng cao.

---

## [Phân tích 1] Phân tích và Triển khai Module Tính Phụ phí Check-in Máy bay

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân tích và Triển khai Module Tính Phụ phí Check-in Máy bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự phát hiện và trình bày rõ ràng ít nhất 2 cấu trúc rẽ nhánh khác nhau (ví dụ: chuỗi `if...else if` lồng nhau đa tầng vs `switch-case` phân tầng kết hợp `ternary operator`), phân tích sự khác biệt về mặt cấu trúc điều kiện.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Xây dựng bảng so sánh HTML đầy đủ 5 tiêu chí (Tốc độ thực thi, Bộ nhớ, Độ bảo trì, Độ sạch mã nguồn, Ngữ cảnh áp dụng). Thẻ `<table>` tuân thủ đúng thuộc tính CSS `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Đưa ra lập luận rõ ràng, hợp lý lý giải tại sao phương án được chọn là tối ưu nhất trong bối cảnh ứng dụng thực tế.
*   **[10 điểm] Lưu đồ luồng Mermaid chuẩn hóa:** Vẽ thành công sơ đồ luồng Mermaid mô tả chính xác logic rẽ nhánh. Sử dụng đúng 5 hình dạng quy chuẩn (Stadium cho Start/End, Parallelogram cho Input/Output, Diamond cho Condition, Rectangle cho Process/Action, Arrow cho luồng nối). tuyệt đối không dùng sai hình dạng cho bước tính toán hay điều kiện.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Triển khai mã nguồn JavaScript ES6+ chạy chính xác tất cả các quy tắc nghiệp vụ (tính đúng mức miễn cước theo hạng vé, tính đúng đơn giá quá cước 50k/kg, áp dụng đúng phí làm thủ tục quầy 100k cho ECO không VIP, giảm 20% cho VIP).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Có logic kiểm tra dữ liệu đầu vào (Validation) chặn triệt để trường hợp `baggageWeight < 0` hoặc `ticketClass` không hợp lệ trước khi thực hiện tính toán.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Định dạng hiển thị Console rõ ràng:** In đầy đủ thông số báo cáo phụ phí (Số kg quá cước, Phí quá cước, Tiền giảm giá VIP, Phí in thẻ quầy, Tổng phụ phí) rõ ràng, dễ đọc, chính xác theo số liệu thực tế.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Sử dụng hằng số `const` và `let` đúng mục đích, tên biến bằng tiếng Anh đúng ngữ nghĩa (`ticketClass`, `baggageWeight`, `overweightFee`, `totalFee`), comment bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo repository và đẩy bài làm lên cấu trúc thư mục đúng mẫu: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Viết đoạn mã đo thời gian thực thi (sử dụng `console.time()` / `console.timeEnd()`) so sánh hiệu năng chạy 100.000 lần của cả 2 phương án đề xuất.

---

## [Phân tích 2] Thiết kế và tối ưu logic tính phí dịch vụ làm thủ tục chuyến bay

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Thiết kế và tối ưu logic tính phí dịch vụ làm thủ tục chuyến bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    - Mô tả chi tiết cấu trúc logic của ít nhất 2 phương án lập trình rẽ nhánh khác nhau trong JavaScript ES6+ (ví dụ: Cấu trúc Nested `if-else` truyền thống vs Cấu trúc Guard Clauses kết hợp `switch-case`).
    - Nêu rõ điểm khác biệt về mặt tổ chức luồng điều khiển và thứ tự đánh giá điều kiện.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    - Tạo bảng so sánh trực quan chứa đầy đủ 5 tiêu chí bắt buộc: Độ phức tạp thời gian, Dung lượng bộ nhớ, Tính bảo trì, Độ đọc hiểu, Bối cảnh phù hợp.
    - Phân tích có chiều sâu chuyên môn, thể hiện rõ ưu/nhược điểm của từng phương án.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    - Đưa ra lập luận thuyết phục chọn phương án tối ưu dựa trên tiêu chuẩn Clean Code và khả năng mở rộng khi hãng bổ sung hạng vé hoặc điều chỉnh mức phí.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    - Xây dựng mã giả hoặc lưu đồ Mermaid đúng quy định chuẩn hóa (Khối bắt đầu/kết thúc `([ ])`, Khối điều kiện `{ }`, Khối tính toán `[" "]`, Khối đầu vào/đầu ra `[/ /]`).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    - Triển khai thành công mã nguồn JavaScript (ES6+) phản ánh đúng phương án tối ưu đã chọn.
    - Tính toán chính xác phí hành lý quá cước theo từng mức miễn cước của 3 hạng vé (`1`, `2`, `3`) và áp dụng đúng ưu đãi giảm 10% phí hành lý cho `isVipMember === true`.
    - Tính toán đúng phí chọn chỗ ngồi theo khu vực ghế và hạng vé tương ứng.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    - Bắt và xử lý triệt để các trường hợp dữ liệu đầu vào vi phạm (`ticketClass` ngoài 1-3, `seatZone` ngoài 1-3, `baggageWeight < 0`).
    - Trả về tổng phí `-1` và hiển thị thông điệp cảnh báo phù hợp khi phát hiện lỗi dữ liệu.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    - Kết quả xuất ra màn hình console rõ ràng, đầy đủ các thông tin: Hạng vé, Khối lượng quá cước, Phí hành lý quá cước (sau giảm giá nếu có), Phí chọn chỗ ngồi, và Tổng phí làm thủ tục.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    - Đặt tên hằng số và biến bằng tiếng Anh, chuẩn `camelCase` (`ticketClass`, `baggageWeight`, `seatZone`, `isVipMember`, `excessBaggageFee`, `seatFee`, `totalFee`).
    - Sử dụng đúng `const`/`let`, không dùng `var`. Thụt lề chuẩn 2 spaces.
*   **[5 điểm] Nộp bài GitHub:**
    - Cung cấp link repository GitHub hợp lệ, đúng cấu trúc tên thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    - Viết đoạn mã kiểm thử hiệu năng (sử dụng `console.time` / `console.timeEnd`) so sánh tốc độ thực thi của 2 giải pháp qua 100.000 lượt giả lập dữ liệu check-in.

---

## [Phân tích 3] Thiết kế Hệ thống Phân luồng Check-in và Tính phí Phụ thu Hành lý Máy bay

### **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Thiết kế Hệ thống Phân luồng Check-in và Tính phí Phụ thu Hành lý Máy bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Học viên đề xuất đủ 2 phương án kỹ thuật rẽ nhánh rõ ràng (Ví dụ: Phương án 1 dùng các khối `if-else if` lồng nhau truyền thống; Phương án 2 kết hợp Guard Clauses loại bỏ case lỗi sớm, sau đó phân tách việc tính phí hành lý bằng `switch-case` và phân làn check-in bằng biểu thức logic điều kiện).
    *   Phân tích cụ thể sự khác biệt về mặt cấu trúc điều kiện giữa 2 phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng so sánh đủ 5 tiêu chí (Tốc độ xử lý, Bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Mức độ phù hợp quy mô) sử dụng đúng thẻ HTML `<table>` có thuộc tính inline style theo yêu cầu.
    *   Nội dung phân tích trong từng ô sắc bén, có căn cứ kỹ thuật lập trình thực tế, không viết chung chung.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lập luận thuyết phục lý giải vì sao phương án được chọn giúp hệ thống chạy nhanh hơn, giảm rủi ro bug khi bổ sung thêm hạng vé mới trong tương lai.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Trình bày mã giả hoặc lưu đồ Mermaid chính xác.
    *   Nếu dùng Mermaid, phải tuân thủ đúng 100% chuẩn hình dạng: Oval `([...])` cho Terminator, Rectangle `["..."]` cho Process, Diamond `?` cho Decision, Parallelogram `[/.../]` cho Input/Output.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Sử dụng đúng cú pháp JavaScript ES6+ (`const`, `let`, `if-else`, `switch-case`, ternary).
    *   Tính chính xác 100% cước phí hành lý quá cân cho 3 hạng vé (Eco 7kg/50k, Deluxe 20kg/40k, Business 40kg/30k).
    *   Tính chính xác phí trễ giờ làm thủ tục (Eco 200k, Deluxe 100k, Business 0k).
    *   Gán đúng 100% làn check-in (Priority Counter nếu VIP hoặc Business; Fast-track Counter nếu Deluxe; Standard Counter cho các trường hợp còn lại).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Bắt trọn vẹn trường hợp `ticketClass` không thuộc {1, 2, 3} và `baggageWeight < 0`.
    *   Xử lý đúng trường hợp hành lý không quá cân (`baggageWeight <= freeAllowance`) thì cước phí quá cân phải bằng `0`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   In ra màn hình console đầy đủ thông tin báo cáo check-in: Hạng vé, Trọng lượng hành lý, Phí hành lý quá cước, Phí trễ giờ, Tổng phụ thu, Làn phục vụ.
    *   Kết quả tính toán với các Test Case mẫu khớp hoàn toàn với quy tắc nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Biến và hằng số đặt bằng tiếng Anh theo chuẩn camelCase (`ticketClass`, `baggageWeight`, `excessBaggageFee`, `lateCheckinFee`, `counterLane`).
    *   Mã nguồn thụt lề chuẩn 2 spaces, không dư thừa mã rác, có comment giải thích bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub repository hợp lệ, đặt tên thư mục đúng chuẩn format: `[Tên Lớp]_[Môn Học]_Session06_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản Kiểm thử Tự động (Benchmark/Test Runner Script):**
    *   Tự thiết kế một chuỗi các lệnh gán đầu vào liên tiếp đại diện cho 5+ trường hợp thực tế khác nhau và in ra bảng tổng hợp kết quả tự động để kiểm tra tính toàn vẹn của logic.

---

## [Sáng tạo 1] Thiết Kế Hệ Thống Phân Luồng Check-in và Tính Phí Hành Lý Hàng Không

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết Kế Hệ Thống Phân Luồng Check-in và Tính Phí Hành Lý Hàng Không — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa danh sách biến đầu vào và đầu ra đầy đủ, hợp lý, phục vụ chính xác bài toán rẽ nhánh phân hạng vé, tuyến bay và hành lý check-in.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 kịch bản bẫy lỗi biên nghiệp vụ (Ví dụ: trọng lượng âm, cước phí vượt quá mức tối đa an toàn bay, mã tuyến bay không khớp switch-case default).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ đúng sơ đồ Mermaid minh họa luồng rẽ nhánh qua các tầng xử lý `switch-case` và `if-else`. Tuân thủ tuyệt đối quy chuẩn 5 hình khối chuẩn (Oval cho Start/End, Parallelogram cho Input/Output, Diamond cho Condition, Rectangle cho Action).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày mạch lạc logic xử lý từ bước nhận diện thông tin khách hàng đến bước đưa ra quyết định phí và luồng ưu tiên.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Kết hợp chuẩn xác `switch-case` để phân loại đơn giá theo tuyến bay và `if-else if-else` để tính cước phí hành lý quá cân theo hạn mức hạng vé + hạng thẻ.
*   **[15 điểm] Áp dụng Toán tử ba ngôi và Tối ưu mã nguồn:** Sử dụng toán tử ba ngôi `? :` đúng cách cho các câu gán nhãn ưu tiên và trạng thái hóa đơn; tuyệt đối không vi phạm bẫy lồng ghép quá mức (nested ternary).

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Triển khai các câu lệnh kiểm tra đầu vào (data guards) để phát hiện và cảnh báo dữ liệu không hợp lệ trước khi tính toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn đặt tên:** Mã nguồn sạch sẻ, căn lề chuẩn 2 spaces, biến đặt bằng tiếng Anh theo chuẩn `camelCase`, comment giải thích logic bằng Tiếng Việt có dấu đầy đủ.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo cấu trúc thư mục chuẩn theo yêu cầu, commit rõ ràng và có README mô tả kịch bản test.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng mô-đun in ra bảng tóm tắt nhật ký giao dịch check-in (Audit Log Text) ghi nhận chi tiết thời gian và lý do tính phí quá cước/cấp quyền ưu tiên cho khách hàng.

---

## [Sáng tạo 2] Thiết kế Động cơ Phân loại và Tự động hóa Check-in Hàng không

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Động cơ Phân loại và Tự động hóa Check-in Hàng không — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Khai báo đầy đủ các biến đầu vào (`ticketClass`, `baggageWeight`, `bookingStatusCode`, `isVip`) và biến tổng hợp đầu ra có cấu trúc mạch lạc, đúng kiểu dữ liệu.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê chính xác tối thiểu 3 trường hợp biên (Ví dụ: `baggageWeight < 0`, `bookingStatusCode` nằm ngoài dải 1-4, `ticketClass` không thuộc Eco/Deluxe/Business) và nêu rõ hướng xử lý.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid hoàn chỉnh thể hiện chính xác các bước kiểm tra từ tiếp nhận dữ liệu -> phân loại trạng thái -> tính phí hành lý -> gán nhãn ưu tiên -> xuất kết quả.
*   **[10 điểm] Chuẩn hóa hình khối Mermaid:** Tuân thủ 100% quy chuẩn hình khối (Oval cho Bắt đầu/Kết thúc, Bình hành cho I/O, Hình thoi cho Điều kiện, Chữ nhật cho Thao tác/Tính toán).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** 
    *   Sử dụng `switch-case` chính xác cho mã trạng thái đặt chỗ (có từ khóa `break` và trường hợp `default`).
    *   Sử dụng `if...else` phân cấp tính chính xác phí quá cước hành lý theo từng hạng vé.
    *   Sử dụng toán tử ba ngôi `?:` ngắn gọn, chuẩn mực để gán nhãn ưu tiên `boardingZone` và phí chọn ghế.
*   **[15 điểm] Xử lý tổng hợp chi phí:** Tính đúng tổng chi phí phụ thu `totalExtraFee = extraBaggageFee + seatSelectionFee` và hiển thị kết quả phân loại chi tiết ra màn hình CLI qua `console.log`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các khối điều kiện bảo vệ (Guard Clauses) ở đầu chương trình để phát hiện dữ liệu sai (như trọng lượng âm hoặc mã trạng thái hủy) và in thông báo lỗi rõ ràng trước khi tính toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Tên biến/hằng số 100% bằng Tiếng Anh (camelCase chuẩn ES6+), ghi chú giải thích logic bằng Tiếng Việt có dấu, căn lề chuẩn 2 spaces.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo đúng thư mục bài tập theo định dạng `[Tên Lớp]_[Môn Học]_Session06_Ex14` trên GitHub.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung biến lưu vết lịch sử kiểm duyệt (`auditLogMessage`) tổng hợp tóm tắt nguyên nhân chấp nhận hoặc từ chối lượt check-in để phục vụ công tác truy vết sau chuyến bay.

---

## [Sáng tạo 3] Sáng tạo hệ thống làm thủ tục check-in và tính phí hành lý hàng không

### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Sáng tạo hệ thống làm thủ tục check-in và tính phí hành lý hàng không — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ các biến Input/Output mô tả chi tiết thông tin hành khách (PassengerProfile), vé (FlightTicket), hành lý (BaggageInfo) và kết quả phụ thu.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện và mô tả rõ ràng giải pháp xử lý cho ít nhất 3 kịch bản lỗi biên nghiệp vụ (ví dụ: trọng lượng âm, mã trạng thái vé bất hợp lệ, mã vị trí ghế không tồn tại).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác vòng đời xử lý làm thủ tục.
*   **[10 điểm] Thiết kế hình khối chuẩn Mermaid:** Tuân thủ 100% quy tắc hình khối (Stadium cho Bắt đầu/Kết thúc, Parallelogram cho Input/Output, Diamond cho Decision, Rectangle cho Process).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Kết hợp chính xác `if-else`, `switch-case` và toán tử ba ngôi để tính toán phí cước hành lý (50.000 VNĐ/kg quá cước) và phí chọn vị trí ghế.
*   **[15 điểm] Tối ưu hóa cấu trúc rẽ nhánh:** Mã nguồn được tổ chức mạch lạc, thứ tự kiểm tra điều kiện hợp lý, không bị lỗi lặp logic hoặc lọt điều kiện.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết mã nguồn kiểm tra dữ liệu đầu vào (Guard Clauses) để ngắt chương trình hoặc đưa ra thông báo lỗi thích đáng khi gặp dữ liệu không hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn ES6+:** Sử dụng `const`/`let`, đặt tên biến/hằng số bằng tiếng Anh theo quy chuẩn CamelCase, comment bằng Tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đặt tên thư mục nộp bài đúng mẫu `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex15`, mã nguồn chạy thành công không có lỗi cú pháp.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung logic ghi nhật ký (Audit Log) theo dõi lịch sử thay đổi trạng thái check-in và tính tổng doanh thu thu thêm từ phí dịch vụ của chuyến bay.

---

## [Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
- **Sơ đồ tư duy / Luồng xử lý (10 điểm)**: Vẽ hoặc diễn giải đúng luồng rẽ nhánh điều kiện cho cả 3 chức năng trước khi viết mã.
- **Xác định điều kiện biên (10 điểm)**: Xác định chính xác các điểm ranh giới điều kiện (ví dụ: đúng 20kg, 30kg, 40kg; trường hợp mã hạng vé không nằm từ 1-4).

#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
- **Chức năng 1 - Cấu trúc if/else-if/else (15 điểm)**:
  - Viết chuẩn xác thứ tự so sánh từ nhỏ đến lớn hoặc từ lớn đến nhỏ.
  - Sử dụng đầy đủ khối ngoặc nhọn `{}` cho các nhánh lệnh.
- **Chức năng 2 - Cấu trúc switch-case (15 điểm)**:
  - Áp dụng chuẩn xác cú pháp `switch (ticketClassCode)`.
  - Có đầy đủ từ khóa `break;` ở cuối mỗi nhánh `case`, không bị lỗi trôi lệnh.
  - Khai báo và xử lý trường hợp ngoại lệ với khối `default`.
- **Chức năng 3 - Toán tử Ba ngôi (10 điểm)**:
  - Đặt đúng cú pháp `dieu_kien ? gia_tri_1 : gia_tri_2`.
  - Gán trực tiếp biểu thức vào hằng số/biến trên 1 dòng đơn giản, không lồng ghép ba ngôi phức tạp gây khó đọc.

#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
- **Bẫy trôi lệnh switch-case (10 điểm)**: Đảm bảo kiểm thử tất cả các trường hợp hạng vé đều dừng đúng case mong muốn, không nhảy tràn sang case phía dưới.
- **Bẫy thứ tự logic trong if-else (10 điểm)**: Không đảo ngược điều kiện dẫn đến việc câu lệnh bị bỏ qua vô lý (ví dụ: kiểm tra `>= 20` trước `>= 40` khiến nhánh `>= 40` không bao giờ chạy tới được).

#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
- **Đặt tên biến & Căn lề chuẩn (10 điểm)**: Sử dụng kiểu `camelCase` đúng ngữ nghĩa tiếng Anh (`baggageWeight`, `ticketClassCode`, `isVipMember`), căn lề thụt lề chuẩn 2 spaces.
- **Đóng gói & Cấu trúc thư mục (10 điểm)**: Đặt tên thư mục nộp bài chuẩn quy định `[Tên Lớp]_[Môn Học]_Session06_Demo`, mã nguồn chạy thành công không có lỗi cú pháp trên Console.

---

## [Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap)

### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
- **[10 điểm]** Thể hiện đầy đủ và chính xác cú pháp, bản chất hoạt động của `if / else if / else` (Lesson 01). Có minh họa bẫy sắp xếp thứ tự kiểm tra khoảng giá trị và tầm quan trọng của khối scope `{}`.
- **[10 điểm]** Thể hiện đầy đủ cú pháp `switch-case`, `break`, `default` (Lesson 02). Chỉ rõ bẫy trôi lệnh (Fall-through) khi quên `break` và bẫy so sánh bằng nghiêm ngặt `===`.
- **[10 điểm]** Thể hiện chính xác cú pháp toán tử ba ngôi `? :` (Lesson 03). Phân định rõ trường hợp nên dùng (gán giá trị đơn giản) và cảnh báo lỗi chống mẫu lồng ghép ba ngôi (Nested Ternary).

#### **2. Phân tầng logic & Mối liên kết — 30 điểm**
- **[15 điểm]** Cấu trúc cây sơ đồ tư duy có tính phân tầng logic chặt chẽ (Root Node -> Main Branches -> Sub-branches -> Technical Details -> Anti-patterns).
- **[15 điểm]** Tích hợp sáng tạo và hợp lý bối cảnh hệ thống **AIRLINE_CHECKIN** (Tính phí hành lý quá cước, Định tuyến trạng thái Check-in, Gán lối đi ưu tiên Fast-Track) vào từng nhánh kiến thức tương ứng.

#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
- **[10 điểm]** Thiết kế sơ đồ có tính thẩm mỹ: Phối màu có ý đồ (Phân biệt giữa Thực hành tốt - Good practice và Bẫy lỗi - Anti-patterns), biểu tượng icon minh họa trực quan, bố cục cân đối.
- **[10 điểm]** Đầy đủ các định dạng xuất file theo yêu cầu (File ảnh `.png`/`.jpg` chất lượng cao + File thiết kế gốc `.xmind`/`.pdf`/`.drawio`).

#### **4. Bản tóm tắt giải trình (summary.md) — 10 điểm**
- **[5 điểm]** Giải thích rõ ràng luồng tư duy rẽ nhánh logic và nguyên tắc chọn lựa giữa `if-else`, `switch-case` và `Ternary Operator` trong dự án thực tế.
- **[5 điểm]** Có mã nguồn minh họa minh bạch bằng JavaScript chuẩn Clean Code cho cả 3 kịch bản nghiệp vụ AIRLINE_CHECKIN (Có so sánh mẫu code đúng vs mẫu code dính lỗi anti-pattern).

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
- **[5 điểm]** Cấu trúc Repository và tên thư mục đặt chuẩn theo định dạng yêu cầu: `[Tên Lớp]_[Môn Học]_Session06_Mindmap`.
- **[5 điểm]** Commit message rõ ràng, file `summary.md` được định dạng Markdown chuẩn mực, đẹp mắt, không bị lỗi hiển thị.

---

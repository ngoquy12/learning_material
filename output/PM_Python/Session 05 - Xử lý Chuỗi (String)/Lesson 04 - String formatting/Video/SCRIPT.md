# HyperFrames Script: Session 05 — Lesson 04

**Lesson:** String formatting
**Technology Stack:** python/core
**Total Duration:** 431.39s
**Scene Count:** 12

---

## Scene_01: Dữ liệu thô trong doanh nghiệp
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Bài toán định dạng dữ liệu thô từ hệ thống sang các tài liệu kinh doanh chuẩn hóa như hóa đơn và báo cáo doanh nghiệp.

**Animation Timeline:**
- 0.2s: title-fade-in
- 3.0s: raw-data-table-draw
- 25.0s: transition-out

**Narration (VO):**
> Trong hệ thống phần mềm doanh nghiệp như xuất hóa đơn hay báo cáo tài chính, chương trình phải xử lý dữ liệu thô liên tục. Các con số thực có quá nhiều chữ số thập phân hoặc không thẳng hàng sẽ gây khó khăn cho người xem. Việc định dạng dữ liệu đầu ra giúp chuẩn hóa hiển thị và đảm bảo tính chuyên nghiệp.

## Scene_02: Hạn chế của toán tử cộng
**Timeline (root):** 39.24s → 74.24s (35s)

**Visual:** So sánh hiệu năng: Toán tử cộng (+) tạo đối tượng trung gian liên tục trong bộ nhớ RAM so với cơ chế điền giá trị trực tiếp.

**Animation Timeline:**
- 0.2s: comparison-table-appear
- 5.0s: highlight-red-concat
- 30.0s: transition-concept

**Narration (VO):**
> Phương pháp ghép chuỗi truyền thống sử dụng toán tử cộng tạo ra gánh nặng lớn cho bộ nhớ do tính chất im-mu-ta-bi-li-ti, tức là tính bất biến của chuỗi trong Python. Mỗi phép cộng sẽ sinh ra một đối tượng hoàn toàn mới trong RAM. Hơn nữa, mã nguồn rất khó đọc và không hỗ trợ định dạng số phức tạp.

## Scene_03: Tiến hóa của định dạng chuỗi
**Timeline (root):** 74.24s → 104.24s (30s)

**Visual:** Tiến trình phát triển các thế hệ định dạng chuỗi trong Python nhằm nâng cao hiệu năng và giảm độ phức tạp của code.

**Animation Timeline:**
- 0.2s: evolutionary-path-show
- 12.0s: highlight-f-string
- 28.0s: finish-scene

**Narration (VO):**
> Để nâng cao hiệu năng và độ tường minh, Python đã phát triển ba thế hệ định dạng: từ phần trăm format thừa kế từ ngôn ngữ C, qua phương thức chấm format ở các phiên bản Python tiếp theo, và cuối cùng là ép-string hiện đại ở phiên bản Python ba chấm sáu. Quy trình tiến hóa này trực tiếp giải quyết bài toán tối ưu hóa tài nguyên.

## Scene_04: Quy trình thiết lập định dạng
**Timeline (root):** 104.24s → 139.24s (35s)

**Visual:** Quy trình 3 bước từ xác định yêu cầu đầu ra, dựng khuôn mẫu đến điền tham số định dạng cụ thể.

**Animation Timeline:**
- 0.2s: workflow-nodes-appear
- 10.0s: highlight-step-3
- 32.0s: transition-code

**Narration (VO):**
> Quy trình chuẩn hóa chuỗi gồm ba bước. Đầu tiên, xác định cấu trúc dữ liệu đầu ra và các yêu cầu định dạng. Bước hai, thiết lập chuỗi mẫu sử dụng ép-string hoặc chấm format. Bước ba, bổ sung các ký tự đặc tả chi tiết sau dấu hai chấm để làm tròn số thực hoặc căn lề cột.

## Scene_05: Phương pháp Percent Format
**Timeline (root):** 139.24s → 174.24s (35s)

**Visual:** Định dạng chuỗi kiểu C-style sử dụng toán tử phần trăm (%) kết hợp các placeholder %s, %d, %.2f cùng tuple tham số truyền vào.

**Animation Timeline:**
- 0.2s: code-syntax-hl
- 10.0s: highlight-percent-operator
- 30.0s: evaluate-output

**Narration (VO):**
> Phương pháp đầu tiên là pe-sen format bản chất là định dạng kiểu C. Ký hiệu phần trăm s đại diện cho chuỗi, phần trăm d đại diện cho số nguyên và phần trăm chấm hai ép đại diện cho số thực lấy hai chữ số thập phân. Các biến tương ứng được đặt bên trong một túp-pồ đi sau ký tự phần trăm.

## Scene_06: Hạn chế của Percent Format
**Timeline (root):** 174.24s → 204.24s (30s)

**Visual:** Các rủi ro khi dùng Percent format: Lỗi cấu trúc tuple thiếu hoặc thừa tham số, cú pháp dài dòng khi có nhiều biến truyền vào.

**Animation Timeline:**
- 0.2s: alert-box-shake
- 8.0s: show-error-example
- 28.0s: transition-next

**Narration (VO):**
> Mặc dù quen thuộc, nhưng phương pháp này rất dễ gây lỗi nếu số lượng phần tử trong túp-pồ bị lệch so với số lượng placeholder. Ngoài ra, mã nguồn sẽ trở nên rất dài, khó bảo trì và không hỗ trợ căn lề linh hoạt khi có nhiều tham số.

## Scene_07: Phương thức str.format()
**Timeline (root):** 204.24s → 239.24s (35s)

**Visual:** Khay gán giá trị của str.format() sử dụng cặp ngoặc nhọn kết hợp cơ chế chỉ mục index hoặc đặt tên tham số khóa.

**Animation Timeline:**
- 0.2s: code-show
- 12.0s: format-mapping-arrows
- 32.0s: clean-editor

**Narration (VO):**
> Hàm chấm format sử dụng các cặp ngoặc nhọn để làm placeholder. Nhờ đó, chúng ta có thể truyền tham số theo vị trí mặc định, hoặc chỉ mục in-đếc, hoặc thậm chí là khai báo các từ khóa định danh. Điều này cải thiện khả năng đọc hiểu mã nguồn một cách rõ rệt.

## Scene_08: Định dạng hiện đại với f-string
**Timeline (root):** 239.24s → 274.24s (35s)

**Visual:** Cú pháp f-string hiện đại cho phép nhúng trực tiếp biểu thức Python vào ngoặc nhọn, xử lý nhanh ở runtime.

**Animation Timeline:**
- 0.2s: code-f-string-show
- 8.0s: highlight-brackets
- 32.0s: transition-specs

**Narration (VO):**
> F-string được thiết lập bằng cách thêm ký tự ép trước chuỗi. Bạn có thể chèn trực tiếp tên biến hoặc biểu thức logic vào trong cặp ngoặc nhọn mà không cần dùng hàm bổ trợ. Công nghệ này tối ưu tốc độ chạy của chương trình nhờ cơ chế biên dịch trực tiếp ở run-time.

## Scene_09: Đặc tả định dạng trong f-string
**Timeline (root):** 274.24s → 314.24s (40s)

**Visual:** Cơ chế định dạng nâng cao: {:<15} căn lề trái rộng 15 khoảng trắng, {:,.2f} phân tách hàng nghìn và làm tròn thực tế.

**Animation Timeline:**
- 0.2s: code-specs-show
- 12.0s: specifier-explanation-arrows
- 38.0s: done-specifier

**Narration (VO):**
> Đặc tả định dạng nằm sau dấu hai chấm. Cụ thể, hai chấm, bé hơn mười lăm nghĩa là căn trái với độ rộng mười lăm ký tự. Còn hai chấm, dấu phẩy, chấm hai ép được dùng để thêm dấu phẩy ngăn cách hàng nghìn và làm tròn đúng hai chữ số thập phân đối với dữ liệu tiền tệ.

## Scene_10: Lỗi TypeError và ValueError
**Timeline (root):** 314.24s → 349.24s (35s)

**Visual:** Phân tích nguyên nhân xảy ra lỗi TypeError và ValueError tại runtime do xung đột kiểu dữ liệu và định dạng đặc tả.

**Animation Timeline:**
- 0.2s: show-error-card
- 10.0s: visual-cross-out
- 32.0s: clear

**Narration (VO):**
> Khi thao tác với chuỗi, lỗi tai e-rơ xuất hiện nếu truyền kiểu dữ liệu chuỗi vào chỗ cần số nguyên phần trăm d. Lỗi va-liu e-rơ sẽ được kích hoạt nếu chúng ta áp dụng định dạng số float hai chấm ép cho dữ liệu đầu vào vốn dĩ là một chuỗi văn bản.

## Scene_11: Lỗi IndexError và KeyError
**Timeline (root):** 349.24s → 384.24s (35s)

**Visual:** Nguyên nhân xảy ra lỗi IndexError do thiếu chỉ mục index, và KeyError do thiếu khóa tương ứng khi gọi hàm format.

**Animation Timeline:**
- 0.2s: display-index-key-errors
- 12.0s: explanation-highlight
- 32.0s: transition-summary

**Narration (VO):**
> Hai lỗi tiếp theo liên quan trực tiếp đến hàm chấm format. Lỗi in-đếc e-rơ xảy ra khi bạn gọi placeholder dạng số thứ tự tương ứng nhưng các đối số truyền vào hàm bị thiếu. Còn ki e-rơ xảy ra khi tên từ khóa được chỉ ra trong chuỗi mẫu nhưng không được truyền giá trị cụ thể.

## Scene_12: Khuyến nghị thực tế từ chuyên gia
**Timeline (root):** 384.24s → 419.24s (35s)

**Visual:** Khuyến nghị từ Senior Engineer: Ưu tiên dùng f-string và kiểm soát chặt chẽ các đặc tả định dạng số thực.

**Animation Timeline:**
- 0.2s: checklist-displays
- 15.0s: highlight-fstring-rule
- 32.0s: fade-out-all

**Narration (VO):**
> Tóm lại, đối với các dự án sử dụng Python phiên bản ba chấm sáu trở lên, ép-string luôn là lựa chọn tối ưu về mặt hiệu suất và thẩm mỹ. Để hiển thị số liệu chính xác trên báo cáo và hóa đơn, hãy luôn sử dụng đặc tả hai chấm chấm N-ép để đảm bảo làm tròn số thực chính xác.


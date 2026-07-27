# HyperFrames Script: Session 02 — Lesson 02

**Lesson:** Toán tử so sánh
**Technology Stack:** python/core
**Total Duration:** 441.39s
**Scene Count:** 12

---

## Scene_01: Bối cảnh luồng so sánh dữ liệu doanh nghiệp
**Timeline (root):** 9.24s → 44.24s (35s)

**Visual:** Business Logic Flow: Inventory Check (Current Stock vs Min Stock) triggers alert.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: flow-item fade in
- 5.0s: flow-decision reveal
- 15.0s: flow-result highlight

**Narration (VO):**
> Trong phát triển phần mềm doanh nghiệp, hệ thống liên tục quyết định hướng xử lý dựa trên dữ liệu đầu vào. Một ứng dụng quản lý kho cần phát cảnh báo khi số lượng sản phẩm tồn kho giảm xuống dưới mức tối thiểu. Tương tự, cổng thanh toán phải kiểm tra số dư ví để xác nhận giao dịch. Để xây dựng cơ chế này, lập trình viên sử dụng các toán tử so sánh nhằm chuyển đổi các kiểm tra thực tế thành trạng thái logic nhị phân, định tuyến chính xác luồng vận hành của ứng dụng.

## Scene_02: Thách thức xử lý giá trị biên
**Timeline (root):** 44.24s → 79.24s (35s)

**Visual:** Boundary Logic Comparison: Strict inequality vs Inclusive inequality.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: comparison-table fade in
- 10.0s: strict-column highlight
- 20.0s: inclusive-column highlight

**Narration (VO):**
> Thách thức lớn nhất khi triển khai logic nghiệp vụ là xử lý giá trị biên. Sai sót nhỏ giữa toán tử lớn hơn và toán tử lớn hơn hoặc bằng có thể dẫn đến việc xuất kho sai quy định hoặc tính toán sai thuế suất. Việc thiếu kiểm duyệt chặt chẽ điều kiện biên sẽ âm thầm phá hủy tính toàn vẹn của cơ sở dữ liệu. Vì vậy, nắm vững các quy tắc toán tử so sánh trong ngôn ngữ lập trình Python là yêu cầu bắt buộc của một nhà phát triển chuyên nghiệp.

## Scene_03: Cấu trúc biểu thức so sánh chuẩn
**Timeline (root):** 79.24s → 114.24s (35s)

**Visual:** Execution Anatomy: [Operand 1] [Comparison Operator] [Operand 2] -> Returns Boolean.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: anatomy-block draw
- 8.0s: operands highlight
- 18.0s: result transition

**Narration (VO):**
> Công thức chuẩn của một biểu thức so sánh bao gồm toán hạng một, đi kèm toán tử quan hệ ở giữa, và kết thúc bằng toán hạng hai. Để biểu thức này hoạt động ổn định, hai toán hạng phải sở hữu kiểu dữ liệu tương thích, ví dụ như so sánh số nguyên in-tơ-giơ với số thực floát. Kết quả trả về từ biểu thức này luôn là một giá trị thuộc kiểu dữ liệu bu-li-ân, chỉ nhận một trong hai trạng thái duy nhất: Tru hoặc Phôn-sơ.

## Scene_04: Luồng logic rẽ nhánh chương trình
**Timeline (root):** 114.24s → 149.24s (35s)

**Visual:** Flowchart: decision block evaluating 'input_value >= 18' routing to Access Granted or Access Denied.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: flowchart render
- 8.0s: decision active
- 18.0s: path evaluation animate

**Narration (VO):**
> Hãy quan sát sơ đồ hoạt động của tiến trình. Hệ thống bắt đầu bằng việc đọc giá trị từ biến in-put va-lu. Sau đó, một nhánh điều kiện được thiết lập bằng toán tử lớn hơn hoặc bằng mười tám. Nếu kết quả đánh giá là đúng, tương đương giá trị Tru, hệ thống lập tức cấp quyền truy cập. Ngược lại, nếu kết quả là sai, tương đương giá trị Phôn-sơ, yêu cầu truy cập sẽ bị từ chối trước khi kết thúc tiến trình thực thi.

## Scene_05: Khai báo các biến giá trị ban đầu
**Timeline (root):** 149.24s → 184.24s (35s)

**Visual:** Code Editor Model: Setting average_score = 8.5, passing_score = 5.0, perfect_score = 10.0.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: code panel open
- 2.0s: line 1 type
- 10.0s: line 2 type
- 18.0s: line 3 type

**Narration (VO):**
> Bây giờ, chúng ta sẽ hiện thực hóa lý thuyết thông qua mã nguồn Python. Đầu tiên, chúng ta khởi tạo ba biến số để mô phỏng điểm số của học viên. Khai báo biến a-vơ-rich gạch dưới scô gán bằng tám chấm năm. Tiếp tục khai báo biến pa-sing gạch dưới scô bằng năm chấm không để làm mốc điểm đạt. Cuối cùng, thiết lập biến pơ-fect gạch dưới scô bằng mười chấm không hiển thị điểm tối đa trong hệ thống.

## Scene_06: Toán tử so sánh lớn hơn hoặc bằng
**Timeline (root):** 184.24s → 219.24s (35s)

**Visual:** Code Editor Model: Writing logic is_passed = average_score >= passing_score.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: operator line show
- 5.0s: '>=' operator focus
- 15.0s: explanation tooltip scale-in

**Narration (VO):**
> Để kiểm tra xem học sinh có vượt qua kỳ thi hay không, chúng ta sử dụng toán tử lớn hơn hoặc bằng, viết là ký tự lớn hơn đi kèm dấu bằng phía sau. Gán kết quả của biểu thức a-vơ-rich gạch dưới scô lớn hơn hoặc bằng pa-sing gạch dưới scô vào biến is gạch dưới pa-st. Việc sử dụng toán tử có dấu bằng giúp đảm bảo học viên có điểm số đúng bằng năm chấm không vẫn được tính là đạt điều kiện.

## Scene_07: Toán tử so sánh bằng và so sánh khác
**Timeline (root):** 219.24s → 254.24s (35s)

**Visual:** Code Editor Model: Adding is_perfect = average_score == perfect_score and is_not_perfect = average_score != perfect_score.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: code append
- 8.0s: '==' operator flash
- 18.0s: '!=' operator flash

**Narration (VO):**
> Tiếp theo, chúng ta đánh giá tính tuyệt đối của điểm số. Khởi tạo biến is gạch dưới pơ-fect và dùng toán tử so sánh bằng, biểu diễn bằng hai dấu bằng viết liền nhau, để kiểm tra xem điểm trung bình có bằng điểm tuyệt đối hay không. Đồng thời, khởi tạo biến is gạch dưới not gạch dưới pơ-fect bằng cách sử dụng toán tử khác, kết hợp dấu chấm than và dấu bằng, để lưu trữ trạng thái ngược lại.

## Scene_08: Thực thi kiểm tra kết quả terminal
**Timeline (root):** 254.24s → 289.24s (35s)

**Visual:** Terminal CLI Execution: Print matches expected boolean outputs, showing True, False, True.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: command simulation run
- 6.0s: output lines block display
- 15.0s: boolean outputs highlight

**Narration (VO):**
> Để kiểm chứng kết quả hoạt động, chúng ta viết các câu lệnh prin in dữ liệu ra terminal. Hãy thực thi file script python bằng dòng lệnh quen thuộc. Terminal lập tức trả về ba kết quả logic rõ ràng. Biến is gạch dưới pa-st nhận giá trị Tru do tám chấm năm lớn hơn năm. Ngược lại, biến is gạch dưới pơ-fect nhận giá trị Phôn-sơ, và biến is gạch dưới not gạch dưới pơ-fect nhận giá trị Tru do điểm số thực tế khác mười.

## Scene_09: Phân biệt toán tử gán và toán tử so sánh bằng
**Timeline (root):** 289.24s → 324.24s (35s)

**Visual:** Detailed difference matrix: Assignment Operator '=' vs. Comparison Operator '=='.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: operator-comp view block
- 8.0s: '=' animation flow
- 18.0s: '==' animation flow

**Narration (VO):**
> Một lỗi cú pháp phổ biến ở các lập trình viên mới bắt đầu là nhầm lẫn mục đích sử dụng giữa toán tử gán một dấu bằng và toán tử so sánh bằng hai dấu bằng. Toán tử gán dùng để gán giá trị ở vế phải vào vùng lưu trữ của biến ở vế trái. Trong khi đó, toán tử hai dấu bằng là phép toán quan hệ logic, thực hiện đánh giá sự tương đương giữa hai thực thể và trả về trạng thái bu-li-ân.

## Scene_10: Cảnh báo lỗi không tương thích kiểu dữ liệu
**Timeline (root):** 324.24s → 359.24s (35s)

**Visual:** TypeError warning details indicating string and number comparison failures.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: error-log highlight red
- 10.0s: correction logic code line show
- 20.0s: error-log status green

**Narration (VO):**
> Cảnh báo lỗi nghiêm trọng khi so sánh không tương thích kiểu dữ liệu. Nếu cố gắng so sánh số nguyên hoặc số thực với một chuỗi ký tự bằng toán tử lớn hơn hoặc nhỏ hơn, trình thông dịch Python sẽ lập tức ném ra lỗi Tai-pơ E-rrơ và dừng chương trình. Để khắc phục, lập trình viên buộc phải chuyển đổi kiểu dữ liệu của chuỗi ký tự về dạng số thông qua các hàm ép kiểu như int hoặc float trước khi so sánh.

## Scene_11: Sai số trong so sánh số thực
**Timeline (root):** 359.24s → 394.24s (35s)

**Visual:** Floating point comparative hazard details: recommended function math.isclose() over direct equality.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: float-pitfall render
- 8.0s: error display red
- 18.0s: solution path highlight

**Narration (VO):**
> Hãy đặc biệt cẩn trọng khi thực hiện so sánh bằng đối với kiểu dữ liệu số thực floát. Do cách thức lưu trữ nhị phân của phần cứng máy tính, các phép toán số thực thường gặp lỗi sai số làm tròn nhỏ ở phần thập phân. Để đảm bảo chương trình không bị sai lệch logic ngoài mong muốn, lập trình viên chuyên nghiệp nên sử dụng thư viện mát chấm i-clâu-sơ hoặc tính toán thông qua một ngưỡng sai số vô cùng nhỏ.

## Scene_12: Tổng kết quy tắc sử dụng toán tử so sánh
**Timeline (root):** 394.24s → 429.24s (35s)

**Visual:** Visual Summary Card: Key tips on comparison logic, datatype compatibility, and edge cases.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: summary-grid fade in
- 10.0s: cards highlights sequential
- 25.0s: final checkmark draw

**Narration (VO):**
> Tổng kết lại, các toán tử quan hệ bao gồm lớn hơn, nhỏ hơn, so sánh bằng, và khác luôn là nền tảng cốt lõi của tính năng rẽ nhánh chương trình. Hãy luôn phân biệt rõ ràng giữa toán tử gán và toán tử so sánh, đồng thời kiểm soát chặt chẽ kiểu dữ liệu của các toán hạng. Chú ý tính toán điều kiện ranh giới sẽ giúp mã nguồn của quý vị hoạt động ổn định và chính xác trong mọi kịch bản vận hành doanh nghiệp.


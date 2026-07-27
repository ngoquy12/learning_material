# HyperFrames Script: Session 01 — Lesson 03

**Lesson:** Khai báo Biến
**Technology Stack:** python/core
**Total Duration:** 351.39s
**Scene Count:** 10

---

## Scene_01: Thách thức lưu trữ dữ liệu
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Hạn chế của việc code cứng giá trị so với sự linh hoạt của việc sử dụng biến lưu trữ dữ liệu động.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Trong phát triển phần mềm doanh nghiệp, luồng dữ liệu thô liên tục đổ về hệ thống. Nếu không có cơ chế lưu trữ tạm thời, máy tính không thể duy trì trạng thái dữ liệu sau khi dòng lệnh kết thúc. Việc nhập trực tiếp các giá trị cố định vào công thức tính toán sẽ làm mã nguồn trở nên rối rắm, cực kỳ khó bảo trì và dễ gây sai sót hệ thống khi chính sách kinh doanh thay đổi.

## Scene_02: Triết lý thiết kế biến trong Python
**Timeline (root):** 39.24s → 74.24s (35s)

**Visual:** Phân vùng bộ nhớ Python: Định danh biến trỏ đến đối tượng trong bộ nhớ Heap.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Ngôn ngữ Python được sáng lập bởi Ghi-đô Van Rốt-xum vào năm một chín chín mốt với triết lý tối giản và tự động hóa. Trong Python, biến không phải là ô nhớ vật lý tĩnh. Bản chất của biến là một nhãn dán định danh động nằm trong vùng định danh, chỉ hướng đến các đối tượng dữ liệu được khởi tạo trong vùng nhớ híp.

## Scene_03: Bản chất tham chiếu bộ nhớ
**Timeline (root):** 74.24s → 109.24s (35s)

**Visual:** Sơ đồ ánh xạ biến daily_revenue và tax_rate trỏ đến các ô chứa giá trị tương ứng trong Heap.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Hãy quan sát mô hình liên kết bộ nhớ. Khi khai báo tên biến như đê-ly re-vơ-nyu hoặc tắc rết, Python không ghi trực tiếp giá trị vào tên biến. Nó tạo ra các đối tượng số thực năm nghìn và không phẩy một trong vùng nhớ híp, sau đó tạo liên kết tham chiếu từ nhãn biến trong namespace sang các đối tượng tương ứng.

## Scene_04: Quy tắc định danh biến hợp lệ
**Timeline (root):** 109.24s → 141.24s (32s)

**Visual:** Quy tắc định danh biến: Bắt đầu bằng chữ cái/dấu gạch dưới; Chấp nhận chữ số phía sau; Phân biệt ký tự hoa thường.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Để chương trình hoạt động ổn định, tên biến phải tuân thủ nghiêm ngặt các quy chuẩn cú pháp của Python. Tên biến chỉ được bắt đầu bằng chữ cái tiếng Anh từ a đến z hoặc dấu gạch dưới. Các ký tự tiếp theo có thể chứa chữ số từ không đến chín. Lưu ý quan trọng là Python phân biệt rõ ràng giữa chữ hoa và chữ thường.

## Scene_05: Chuẩn đặt tên PEP 8
**Timeline (root):** 141.24s → 171.24s (30s)

**Visual:** Nguyên tắc đặt tên PEP 8: Sử dụng định dạng snếk cây rõ nghĩa, loại bỏ từ viết tắt mơ hồ.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Chuẩn viết code PEP tám khuyến nghị lập trình viên chuyên nghiệp sử dụng định dạng snếk cây. Tất cả ký tự được viết thường và phân tách bằng dấu gạch dưới. Tên biến cần ngắn gọn nhưng phải phản ánh rõ ràng ý nghĩa nghiệp vụ, tránh viết tắt mơ hồ gây khó đọc cho các thành viên trong dự án.

## Scene_06: Cơ chế toán tử gán
**Timeline (root):** 171.24s → 204.24s (33s)

**Visual:** Toán tử gán: Tính toán vế phải trước, sau đó liên kết kết quả vào biến lưu trữ ở vế trái.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Phép gán bằng dấu bằng trong Python hoạt động theo cơ chế từ phải qua trái. Trình thông dịch sẽ đánh giá biểu thức ở vế phải của toán tử gán trước để tạo ra đối tượng dữ liệu trong bộ nhớ. Sau khi đối tượng được xác định, địa chỉ của nó mới được liên kết với tên biến nằm ở vế bên trái của biểu thức.

## Scene_07: Luồng xử lý khai báo biến
**Timeline (root):** 204.24s → 239.24s (35s)

**Visual:** Sơ đồ logic chạy chương trình: Kiểm tra hợp lệ -> Báo lỗi nếu sai -> Gán tham chiếu nếu đúng.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Quy trình khởi tạo biến bắt đầu bằng bước kiểm tra tính hợp lệ của tên. Nếu tên biến vi phạm cú pháp, hệ thống sẽ lập tức báo lỗi xin-tắc e-rơ. Nếu hợp lệ, biểu thức bên phải toán tử gán được tính toán để tạo đối tượng trong vùng nhớ híp và liên kết tham chiếu với tên biến trong Namespace.

## Scene_08: Thực hành khai báo biến
**Timeline (root):** 239.24s → 274.24s (35s)

**Visual:** Đoạn mã Python khai báo các biến tính toán hóa đơn bán hàng.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Hãy xem xét đoạn mã nguồn thực tế. Chúng ta khai báo các biến lưu trữ thông tin đơn hàng gồm yu-nít pri-xơ giá trị một trăm năm mươi phẩy năm, qoan-ti-ty bằng mười và đít-cao rết bằng không phẩy không năm. Tiếp tục thực hiện tính toán các biến phụ thuộc như sub-to-tal và truyền vào hàm brin để kiểm tra kết quả.

## Scene_09: Thực thi chương trình
**Timeline (root):** 274.24s → 304.24s (30s)

**Visual:** Terminal CLI chạy file script hiển thị kết quả giá trị subtotal và final_total.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Thực thi file python vừa viết trên công cụ dòng lệnh terminal. Kết quả in ra màn hình cho thấy giá trị tổng chưa chiết khấu sub-to-tal hiển thị là một nghìn năm trăm linh năm phẩy không, và giá trị thanh toán cuối cùng fai-nờ to-tal được tính toán chính xác sau khi trừ đi chiết khấu.

## Scene_10: Các lỗi khai báo thường gặp
**Timeline (root):** 304.24s → 339.24s (35s)

**Visual:** Cảnh báo lỗi: Tránh SyntaxError từ ký tự không hợp lệ, NameError do gọi biến chưa khai báo, và lỗi bóng ma ghi đè hàm hệ thống.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: main content show

**Narration (VO):**
> Hãy lưu ý các lỗi phổ biến khi quản lý biến. Lỗi xin-tắc e-rơ xảy ra nếu đặt tên biến bắt đầu bằng số hoặc chứa ký tự đặc biệt, hoặc sử dụng các từ khóa được bảo vệ như íp, đép, cờ-lát. Lỗi nêm e-rơ xuất hiện khi gọi một biến chưa được định nghĩa. Tuyệt đối không đặt tên trùng với các hàm dựng sẵn của hệ thống.


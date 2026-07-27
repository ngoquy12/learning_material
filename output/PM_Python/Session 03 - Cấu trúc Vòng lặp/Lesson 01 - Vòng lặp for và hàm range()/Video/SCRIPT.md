# HyperFrames Script: Session 03 — Lesson 01

**Lesson:** Vòng lặp for và hàm range()
**Technology Stack:** python/core
**Total Duration:** 407.39s
**Scene Count:** 12

---

## Scene_01: Bối cảnh doanh nghiệp và bài toán lặp tin học
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Khái niệm xử lý lặp trong doanh nghiệp: Duyệt danh sách đơn hàng để tính toán doanh thu và tự động hóa tác vụ gửi email theo định kỳ.

**Animation Timeline:**
- tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: flow-step-1 fade in
- 3.0s: flow-step-2 fade in

**Narration (VO):**
> Trong thực tế phát triển phần mềm, việc thực thi lặp đi lặp lại một hành động với sự thay đổi của các biến số là vô cùng phổ biến. Ví dụ điển hình bao gồm việc quét qua hàng nghìn đơn hàng để tính tổng doanh thu hoặc tự động hóa gửi thư xác nhận định kỳ tới danh sách địa chỉ người dùng hệ thống.

## Scene_02: Hạn chế của việc viết mã thủ công
**Timeline (root):** 39.24s → 69.24s (30s)

**Visual:** So sánh giữa sao chép câu lệnh thủ công (dễ lỗi, phình mã nguồn) và cấu trúc lặp tự động hóa (tối ưu hóa tài nguyên).

**Animation Timeline:**
- 0.2s: column-bad active
- 5.0s: column-good active highlight

**Narration (VO):**
> Sao chép thủ công các dòng lệnh cho từng đối tượng sẽ khiến mã nguồn phình to nhanh chóng. Điều này không chỉ gây lãng phí bộ nhớ mà còn làm tăng khả năng xảy ra lỗi cú pháp khi lập trình viên cần cập nhật hoặc sửa đổi logic nghiệp vụ chung của hệ thống.

## Scene_03: Giới thiệu giải pháp vòng lặp for
**Timeline (root):** 69.24s → 99.24s (30s)

**Visual:** Định nghĩa vòng lặp for: Cấu trúc điều khiển tinh gọn giúp máy ảo lặp qua miền dữ liệu xác định sẵn một cách an toàn.

**Animation Timeline:**
- 0.2s: editor-window slide in
- 2.5s: code-line-1 highlight

**Narration (VO):**
> Để khắc phục, chúng ta cần một cấu trúc điều khiển tinh gọn cho phép máy ảo lặp qua miền dữ liệu xác định trước. Vòng lặp for giúp quản lý hiệu quả tài nguyên tính toán của vi xử lý và hỗ trợ thay đổi khoảng giá trị lặp một cách nhanh chóng.

## Scene_04: Cấu trúc cú pháp và thụt lề bắt buộc
**Timeline (root):** 99.24s → 131.24s (32s)

**Visual:** Quy tắc cú pháp: Từ khóa for, biến đại diện, dấu hai chấm kết thúc khai báo, và thụt lề thụ động 4 khoảng trắng.

**Animation Timeline:**
- 0.2s: keyword-indent highlight-yellow
- 4.0s: operator-colon flash

**Narration (VO):**
> Cấu trúc vòng lặp for bắt đầu bằng từ khóa f-o-r, theo sau là biến đại diện đón nhận giá trị. Kết thúc dòng thiết lập bắt buộc phải có dấu hai chấm để khai báo phạm vi khối lệnh. Các câu lệnh bên trong bắt buộc phải được thụt lề chẵn bốn khoảng trắng để trình thông dịch Python phân biệt thuộc tính khối con.

## Scene_05: Sơ đồ thực thi vòng lặp trong máy ảo
**Timeline (root):** 131.24s → 166.24s (35s)

**Visual:** Tiến trình thực thi: Kiểm tra điều kiện dừng -> Gán biến -> Thực thi khối lệnh -> Cập nhật chỉ số đếm bằng step.

**Animation Timeline:**
- 0.2s: flowchart-start draw-line
- 4.5s: node-decision pulse
- 10.0s: loop-cycle-line active

**Narration (VO):**
> Quan sát luồng chạy, máy ảo khởi đầu bằng việc kiểm tra biến đếm đã đạt mức cận kết thúc stop hay chưa. Nếu đã đạt, vòng lặp dừng ngay lập tức. Nếu chưa đạt, giá trị được gán vào biến lặp để thực thi các lệnh thụt lề, tiếp theo biến đếm tự động cộng thêm giá trị step trước khi quay lại bước kiểm tra.

## Scene_06: Cơ chế hoạt động của hàm range
**Timeline (root):** 166.24s → 196.24s (30s)

**Visual:** Cơ chế của hàm range: Trình tạo số tuần tự động, tối ưu hóa RAM bằng cách không lưu toàn bộ phần tử cùng lúc.

**Animation Timeline:**
- 0.2s: ram-block color-green
- 3.5s: memory-usage-indicator drop-to-minimum

**Narration (VO):**
> Hàm range được xây dựng sẵn trong lớp nhân của Python với vai trò khởi tạo một chuỗi số tuần tự. Lợi thế lớn nhất của range là nó lưu trữ các chỉ số dưới dạng thực thể động thay vì nạp toàn bộ danh sách số nguyên vào bộ nhớ RAM, giúp giải phóng áp lực lưu trữ tài nguyên khi quét lượng phần tử lớn.

## Scene_07: Chi tiết ba tham số start, stop và step
**Timeline (root):** 196.24s → 228.24s (32s)

**Visual:** Chi tiết ba đối số của hàm range: start (bắt đầu), stop (điểm chặn), và step (khoảng cách bước nhảy).

**Animation Timeline:**
- 0.2s: param-start highlight-blue
- 3.5s: param-stop highlight-red
- 7.0s: param-step highlight-green

**Narration (VO):**
> Hàm range nhận vào ba đối số bao gồm start là điểm khởi hành, stop xác định điểm chặn, và step cấu hình bước tăng động. Ba tham số này phân cách bởi dấu phẩy, cho phép lập trình viên định cấu hình linh hoạt phạm vi hoạt động của cấu trúc lặp.

## Scene_08: Cơ chế loại trừ cận stop
**Timeline (root):** 228.24s → 258.24s (30s)

**Visual:** Nguyên lý loại trừ cận Stop: Vòng lặp luôn kết thúc tại (stop trừ một), phù hợp với quy toán chỉ số từ số không.

**Animation Timeline:**
- 0.2s: range-array highlights
- 5.0s: excluded-label shift-right scale-up

**Narration (VO):**
> Một quy tắc bất biến trong Python là tham số stop luôn bị loại trừ khỏi tập hợp các giá trị trả về của hàm range. Tức là, nếu thiết lập stop là mười, tiến trình lặp sẽ dừng bước tại vị trí số chín. Sự tính toán này tuân theo logic định vị mảng bắt đầu từ chỉ số không.

## Scene_09: Triển khai mã ví dụ thực tế
**Timeline (root):** 258.24s → 293.24s (35s)

**Visual:** Thực thi cấu trúc for current_step in range(1, 10, 2): In ra chuỗi số lẻ một, ba, năm, bảy, chín.

**Animation Timeline:**
- 0.2s: terminal-input type-in
- 4.0s: execution-wait
- 6.5s: terminal-output roll-in

**Narration (VO):**
> Quan sát ví dụ khai báo for cờ-ren-tờ step viết liền in range từ một đến mười với bước nhảy là hai. Khối lệnh in ra giá trị hiện tại của biến lặp. Khi chạy dòng lệnh này trên cửa số terminal, kết quả thu được sẽ là các số lẻ một, ba, năm, bảy, chín nhờ bước nhảy hai và quy tắc loại trừ số mười.

## Scene_10: Kỹ thuật dịch chuyển ngược sử dụng step âm
**Timeline (root):** 293.24s → 325.24s (32s)

**Visual:** Vòng lặp giảm dần: Yêu cầu bắt buộc start lớn hơn stop và step mang trị số âm để lùi biến đếm.

**Animation Timeline:**
- 0.2s: code-negative-step show
- 4.0s: negative-highlight pulse

**Narration (VO):**
> Khi muốn tạo một vòng lặp giảm dần các số, bạn bắt buộc phải chỉ định tham số start có giá trị lớn hơn stop, đồng thời cung cấp giá trị âm cho cấu hình tham số step. Nếu không tinh chỉnh bước nhảy âm, máy ảo sẽ không thể phát hiện chiều chuyển động và bỏ qua hoàn toàn khối code.

## Scene_11: Nhận diện lỗi Type Error và Value Error
**Timeline (root):** 325.24s → 360.24s (35s)

**Visual:** Cảnh báo lỗi: TypeError khi truyền số thực float và ValueError khi thiết lập tham số bước nhảy step bằng không.

**Animation Timeline:**
- 0.2s: error-type active-danger-red
- 6.0s: error-value active-danger-red

**Narration (VO):**
> Hai ngoại lệ runtime phổ biến gồm: lỗi Típ E-rờ, xảy ra khi truyền kiểu số thực float vào tham số của hàm range. Thứ hai là lỗi Va-lu E-rờ, xuất hiện nếu để step bằng không, vì máy ảo không thể cộng dồn số không để tính điểm dịch chuyển tiếp theo và sẽ sinh lỗi ngay lập tức.

## Scene_12: Cảnh báo vòng lặp vô hạn và cách khắc phục
**Timeline (root):** 360.24s → 395.24s (35s)

**Visual:** Khắc phục lỗi logic: Logic mâu thuẫn giữa hướng dịch chuyển của step và khoảng giá trị start-stop gây sập luồng lặp.

**Animation Timeline:**
- 0.2s: warning-box fade-in
- 5.0s: correction-highlight flashing

**Narration (VO):**
> Hãy luôn đảm bảo hướng của bước nhảy step tương thích với khoảng cách giữa start và stop. Việc thiết lập sai hướng chuyển động, ví dụ start nhỏ hơn stop nhưng step lại là số âm, hoặc ngược lại, sẽ khiến máy ảo bỏ qua toàn bộ vòng lặp ngay khi khởi tạo do không thỏa mãn tập hợp lặp.


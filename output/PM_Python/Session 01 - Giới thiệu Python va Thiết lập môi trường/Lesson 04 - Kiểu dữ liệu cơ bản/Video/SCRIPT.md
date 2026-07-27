# HyperFrames Script: Session 01 — Lesson 04

**Lesson:** Kiểu dữ liệu cơ bản
**Technology Stack:** python/core
**Total Duration:** 271.39s
**Scene Count:** 8

---

## Scene_01: Đặt vấn đề đầu vào dữ liệu hệ thống
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Luồng dữ liệu người dùng nhập từ giao diện được phân tách thành bốn nhóm thông tin: Tuổi kiểu số nguyên, Số dư kiểu số thực, Họ tên kiểu chuỗi và Trạng thái kích hoạt kiểu luận lý.

**Animation Timeline:**
- 0.2s: flow-container fade-in
- 2.5s: flow-step highlight
- 5.0s: flow-split slide-down

**Narration (VO):**
> Trong các hệ thống phần mềm doanh nghiệp, luồng thông tin người dùng nhập vào luôn ở dạng thô và chưa phân loại. Một hệ thống thanh toán hoặc đăng ký tài khoản cần phải lưu trữ chính xác từ tuổi tác, số dư ví đến họ tên và trạng thái kích hoạt tài khoản. Nếu hệ thống không xác định rõ kiểu dữ liệu cho từng trường thông tin này, máy tính sẽ không thể hiểu được mục đích xử lý, dẫn đến sự mơ hồ trong bộ nhớ tạm thời và lỗi hệ thống nghiêm trọng.

## Scene_02: Xung đột kiểu dữ liệu thực tế
**Timeline (root):** 39.24s → 69.24s (30s)

**Visual:** Bảng đối chiếu giữa phép cộng chuỗi không tương thích gây lỗi TypeError và phép cộng giá trị số học diễn ra hợp lệ trên hệ thống bộ nhớ.

**Animation Timeline:**
- 0.2s: comparison-table slide-in
- 4.0s: col-bad error-flash
- 8.0s: col-good success-glow

**Narration (VO):**
> Hãy xem xét tình huống khi thực hiện phép cộng trên dữ liệu thô. Nếu chuỗi ký tự chứa số hai mươi tám được cộng trực tiếp với số hai, trình biên dịch Python sẽ không thể tự động xử lý và ném ra lỗi. Sự mơ hồ giữa chuỗi biểu diễn số và giá trị số thực tế là nguyên nhân hàng đầu khiến các tiến trình giao dịch bị dừng đột ngột. Việc định nghĩa rõ ràng kiểu dữ liệu giúp trình thông dịch cấp phát bộ nhớ chính xác và bảo toàn tính toàn vẹn hệ thống.

## Scene_03: Kiểu dữ liệu số int và float
**Timeline (root):** 69.24s → 99.24s (30s)

**Visual:** Mẫu khai báo biến số nguyên đại diện cho tuổi tác và số thực đại diện cho số dư tài khoản theo đúng quy chuẩn định dạng mã nguồn PEP tám.

**Animation Timeline:**
- 0.2s: code-editor fade-in
- 3.0s: line-1 typing-effect
- 8.0s: line-2 typing-effect

**Narration (VO):**
> Để quản lý số liệu, Python cung cấp hai kiểu dữ liệu số cơ bản: kiểu in-tơ biểu diễn số nguyên và kiểu ph-lốt biểu diễn số thực dấu phẩy động. Ví dụ, ta khai báo biến u-sơ gạch dưới e-dʒ bằng hai mươi lăm, đây là kiểu số nguyên dùng cho đại lượng đếm được. Tiếp theo, biến u-sơ gạch dưới ba-lần-xơ biểu đạt số dư tài khoản được gán giá trị một nghìn năm trăm phẩy năm, thuộc kiểu số thực để phục vụ các tính toán tài chính có độ chính xác cao.

## Scene_04: Kiểu dữ liệu str và bool
**Timeline (root):** 99.24s → 131.24s (32s)

**Visual:** Mẫu khai báo biến dạng chuỗi chứa tên người dùng bằng dấu nháy kép và biến luận lý lưu giữ trạng thái hoạt động của tài khoản.

**Animation Timeline:**
- 0.2s: code-editor fade-in
- 4.0s: line-1 highlights-quotes
- 10.0s: line-2 highlights-boolean

**Narration (VO):**
> Đối với văn bản, ta sử dụng kiểu s-te-r thông qua việc đặt ký tự trong cặp dấu nháy kép hoặc nháy đơn đồng nhất. Như biến u-sơ gạch dưới nêm được gán giá trị chuỗi A-lít. Cuối cùng, kiểu dữ liệu luận lý bun chỉ nhận hai trạng thái trăng hoặc phó-lơ để kiểm soát luồng điều kiện. Ở đây, biến i-dơ gạch dưới ác-típ được gán trăng nhằm xác nhận tài khoản người dùng đang ở trạng thái hoạt động.

## Scene_05: Kiểm tra kiểu dữ liệu thực tế
**Timeline (root):** 131.24s → 161.24s (30s)

**Visual:** Kết quả xuất ra màn hình Terminal khi thực thi hàm kiểm tra kiểu dữ liệu cho bốn biến đặc trưng trong hệ thống.

**Animation Timeline:**
- 0.2s: terminal slide-in
- 3.5s: output-line-1 displays
- 7.0s: output-line-2-3-4 displays

**Narration (VO):**
> Để xác định chính xác kiểu dữ liệu hiện tại của biến trong runtime, ta sử dụng hàm taip tích hợp sẵn của Python. Bằng cách gọi lệnh in kết hợp hàm taip truyền vào tên biến, terminal sẽ hiển thị rõ nhãn phân lớp của từng dữ liệu từ in-tơ, ph-lốt, s-te-r cho đến bun. Việc thường xuyên kiểm tra kiểu dữ liệu giúp kiểm soát chặt chẽ luồng dữ liệu trước khi thực thi các tác vụ nghiệp vụ phức tạp.

## Scene_06: Quy trình ép kiểu dữ liệu
**Timeline (root):** 161.24s → 196.24s (35s)

**Visual:** Quy trình logic từ bước tiếp nhận đầu vào của người dùng, kiểm tra điều kiện tương thích, thực hiện ép kiểu an toàn và kết thúc tại bước xác nhận kiểu dữ liệu.

**Animation Timeline:**
- 0.2s: flowchart load
- 5.0s: node-decision blink
- 12.0s: validation-step show

**Narration (VO):**
> Khi tiếp nhận dữ liệu dạng chuỗi từ cổng đầu vào mà cần tính toán, ta thực hiện ép kiểu hay còn gọi là taip cát-tinh. Hàm in-tơ sẽ chuyển đổi chuỗi chữ số hợp lệ thành số nguyên, trong khi hàm ph-lốt đổi chuỗi thành số thực. Ngược lại, hàm s-te-r cho phép đưa bất kỳ kiểu giá trị nào về dạng chuỗi văn bản. Quy trình này bao gồm việc nhận dữ liệu, kiểm tra tính tương thích, thực hiện ép kiểu và cuối cùng là xác nhận lại kiểu dữ liệu mới.

## Scene_07: Nhận diện và xử lý lỗi Runtime
**Timeline (root):** 196.24s → 229.24s (33s)

**Visual:** Bảng cảnh báo các lỗi thực thi thường gặp bao gồm lỗi chuyển đổi Value Error và lỗi sai biệt kiểu dữ liệu Type Error.

**Animation Timeline:**
- 0.2s: pitfall-card border-red
- 6.0s: error-case-1 flashing-red
- 12.0s: error-case-2 flashing-red

**Narration (VO):**
> Trong quá trình ép kiểu, nếu chuỗi đầu vào chứa các ký tự chữ không thể chuyển đổi sang số, hệ thống sẽ ném ra lỗi va-liu e-rơ. Mặt khác, việc cố tình thực hiện các toán tử toán học giữa chuỗi văn bản và số mà không qua ép kiểu sẽ kích hoạt lỗi taip e-rơ. Các lỗi này sẽ làm dừng toàn bộ chương trình ngay lập tức nếu dữ liệu không được làm sạch đầu vào và xử lý ngoại lệ trước khi tính toán.

## Scene_08: Tổng kết nguyên tắc thao tác dữ liệu
**Timeline (root):** 229.24s → 259.24s (30s)

**Visual:** Bảng tổng kết ba quy tắc bảo mật và ổn định hệ thống khi thao tác với các kiểu dữ liệu cơ bản.

**Animation Timeline:**
- 0.2s: summary-table fade-in
- 5.0s: rule-1 highlight
- 10.0s: rule-2 highlight
- 15.0s: rule-3 highlight

**Narration (VO):**
> Tóm lại, để xây dựng hệ thống phần mềm ổn định, lập trình viên cần thuộc lòng ba nguyên tắc. Thứ nhất, luôn xác định đúng kiểu dữ liệu của biến đầu vào. Thứ hai, thực hiện làm sạch dữ liệu để tránh phát sinh lỗi runtime khi chuyển đổi kiểu. Cuối cùng, luôn ứng dụng hàm taip để kiểm soát chặt chẽ kiểu dữ liệu trước khi đưa vào các biểu thức logic hoặc toán học quan trọng của doanh nghiệp.


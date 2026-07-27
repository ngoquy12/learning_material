# HyperFrames Script: Session 05 — Lesson 01

**Lesson:** Giới thiệu string + indexing + immutable
**Technology Stack:** python/core
**Total Duration:** 461.39s
**Scene Count:** 12

---

## Scene_01: Bối cảnh dữ liệu mã định danh ERP
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Mã định danh hàng hóa trong hệ thống ERP đóng vai trò là khóa chính để đối chiếu thông tin giữa tất cả các phân hệ độc lập từ kho bãi đến thanh toán.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: flow-container fade in
- 15.0s: active-step highlight

**Narration (VO):**
> Trong các hệ thống phân phối cốt lõi quản lý thông tin lưu kho và chuỗi cung ứng bán lẻ, tính toàn vẹn của dữ liệu mã định danh hàng hóa giữ vai trò quyết định cấu trúc vận hành. Các mã định danh sản xuất như P-2026 liên tục được truyền dẫn và đối chiếu qua lại giữa nhiều thư viện từ khâu kiểm kho đến khâu thanh toán hóa đơn.

## Scene_02: Rủi ro từ tính khả biến dữ liệu
**Timeline (root):** 39.24s → 74.24s (35s)

**Visual:** So sánh rủi ro: Lập trình khả biến (Mutable) cho phép ghi đè ô nhớ âm thầm làm sai lệch mã hàng hóa toàn hệ thống, dẫn đến chuyển nhầm hàng hóa và thất thoát tài sản.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: compare-grid fade in
- 18.0s: column-bad highlight

**Narration (VO):**
> Nếu ngôn ngữ lập trình cho phép thay đổi trực tiếp nội dung ký tự trên cùng một vùng nhớ cũ, bất kỳ mô-đun nào trong hệ thống lớn bị lỗi logic đều có thể vô tình sửa đổi ký tự đại diện. Sự thay đổi này diễn ra mà không hề tạo ra một cảnh báo lỗi nào từ trình biên dịch, làm cho dữ liệu ban đầu bị ghi đè và hư hỏng không dấu vết.

## Scene_03: Mô hình bộ nhớ chuỗi trong Python
**Timeline (root):** 74.24s → 114.24s (40s)

**Visual:** Cấu trúc chuỗi bất biến trong bộ nhớ Python bao gồm các ô nhớ tuần tự, mỗi ô chứa một ký tự và được ánh xạ bằng hai hệ thống chỉ mục dương và âm.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: memory-layout show
- 12.0s: positive-row highlight
- 25.0s: negative-row highlight

**Narration (VO):**
> Nhằm giải quyết triệt để rủi ro ghi đè dữ liệu, Guido van Rossum khi thiết kế Python vào năm một chín chín mốt đã định nghĩa kiểu dữ liệu chuỗi là một cấu trúc bất biến tức im-miu-tơ-bơ trong bộ nhớ. Hãy quan sát cách chuỗi P-2026 được phân bổ trên các ô nhớ liên tiếp cùng với hệ thống chỉ mục tương ứng để hiểu rõ cơ chế quản lý dữ liệu này.

## Scene_04: Khởi tạo chuỗi định danh sản phẩm
**Timeline (root):** 114.24s → 149.24s (35s)

**Visual:** Quy trình thực tế: Khởi tạo biến lưu trữ dữ liệu chuỗi gốc bằng chuẩn snake_case: original_identifier bằng 'P-2026'.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: terminal-mock fade in
- 8.0s: code-line type-in

**Narration (VO):**
> Chúng ta bắt đầu bằng việc khởi tạo trình soạn thảo code và khai báo chuỗi định danh chuẩn. Ta gán giá trị P-2026 vào biến viết theo chuẩn snây-kây là ô-ri-gi-nơl gạch dưới ai-đên-ti-phai-ơ để lưu trữ thông tin sản phẩm một cách tường minh và an toàn.

## Scene_05: Cơ chế truy xuất chỉ mục dương
**Timeline (root):** 149.24s → 184.24s (35s)

**Visual:** Toán tử chỉ mục dương [index] bắt đầu từ 0 đại diện cho ký tự đầu tiên phía bên trái của chuỗi văn bản.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: code-block draw
- 15.0s: highlight print statement
- 28.0s: show output target

**Narration (VO):**
> Để truy cập các ký tự từ đầu chuỗi, ta dùng cú pháp toán tử chỉ mục dương dạng mở ngoặc vuông index đóng ngoặc vuông. Cụ thể, khi truy cập ô-ri-gi-nơl gạch dưới ai-đên-ti-phai-ơ chỉ mục không, trình thông dịch sẽ trả về ký tự đầu tiên là chữ pê viết hoa để kiểm tra logic định dạng.

## Scene_06: Cơ chế truy xuất chỉ mục âm
**Timeline (root):** 184.24s → 219.24s (35s)

**Visual:** Toán tử chỉ mục âm [-index] bắt đầu từ -1 đại diện cho phần tử cuối cùng bên phải của chuỗi, giảm dần về phía bên trái.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: code-block draw
- 15.0s: highlight negative access
- 28.0s: show negative output

**Narration (VO):**
> Trong nhiều trường hợp ta muốn nhanh chóng định vị các ký tự mang mã số ở phía cuối cùng của chuỗi mà không cần tính toán độ dài. Chúng ta sử dụng cú pháp toán tử chỉ mục âm dạng mở ngoặc vuông trừ index đóng ngoặc vuông. Tại đây, chỉ mục trừ một sẽ trích xuất chính xác ký tự số sáu nằm ở cuối chuỗi.

## Scene_07: Tương quan hai hướng chỉ mục
**Timeline (root):** 219.24s → 259.24s (40s)

**Visual:** Bảng tổng hợp đối chiếu chỉ mục: Hướng dương từ 0 đến N-1 (trái sang phải); Hướng âm từ -1 đến -N (phải sang trái).

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: index-table fade in
- 15.0s: positive-row effect
- 28.0s: negative-row effect

**Narration (VO):**
> Hãy so sánh trực quan hai cơ chế chỉ mục này. Chỉ mục dương tăng dần từ không đến n trừ một từ trái sang phải, trong khi chỉ mục âm giảm dần từ trừ một đến trừ n từ phải sang trái. Việc sử dụng linh hoạt hai hướng tiếp cận này giúp mã nguồn tối ưu hóa hiệu suất và tránh được các tác vụ lặp lại khi truy xuất.

## Scene_08: Thực nghiệm sửa đổi trực tiếp
**Timeline (root):** 259.24s → 294.24s (35s)

**Visual:** Kiểm chứng thực tế: Cố ý cập nhật trực tiếp phần tử đầu tiên của chuỗi thông qua thao tác gán: original_identifier[0] = 'D'.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: code-block display
- 15.0s: highlight invalid syntax

**Narration (VO):**
> Bây giờ chúng ta sẽ thử nghiệm hành vi thay đổi giá trị của chuỗi trực tiếp. Giả sử ta viết dòng lệnh gán ký tự đê viết hoa vào ô-ri-gi-nơl gạch dưới ai-đên-ti-phai-ơ tại chỉ mục không nhằm sửa mã định danh thành D-2026. Hãy lưu dự án và chuẩn bị thực thi để xem phản ứng từ hệ thống.

## Scene_09: Thông báo lỗi TypeError
**Timeline (root):** 294.24s → 334.24s (40s)

**Visual:** Cảnh báo Lỗi: TypeError xảy ra khi cố gắng thay đổi tại chỗ một ký tự của chuỗi vì kiểu dữ liệu str trong Python hoàn toàn bất biến.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: error-box pop up
- 18.0s: error-title highlight
- 30.0s: block-indicator wave

**Narration (VO):**
> Ngay khi thực thi, hệ thống sẽ ném ra lỗi tai-pơ-e-rơ kèm thông báo đối tượng chuỗi không hỗ trợ việc gán giá trị trực tiếp cho phần tử và lập tức dừng tiến trình. Cơ chế này bảo vệ vùng nhớ của chuỗi không bị ghi đè trái phép từ các phân nghiệp xử lý đồng thời, đảm bảo an toàn tuyệt đối cho dữ liệu gốc.

## Scene_10: Giới hạn chỉ mục và IndexError
**Timeline (root):** 334.24s → 369.24s (35s)

**Visual:** Cảnh báo Lỗi: IndexError xảy ra khi chỉ mục vượt quá giới hạn độ dài của chuỗi, khiến chương trình bị dừng đột ngột.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: error-box pop up
- 15.0s: warning-signal blink

**Narration (VO):**
> Một lỗi phổ biến khác là in-đếch-e-rơ. Lỗi runtime này xuất hiện bất cứ khi nào chỉ mục bạn truy cập vượt quá phạm vi giới hạn từ trừ n đến n trừ một của chuỗi. Hãy luôn kiểm soát độ dài của chuỗi trước khi thực hiện truy cập động để tránh làm sập các tiến trình chạy ngầm.

## Scene_11: Cách tái tạo chuỗi an toàn
**Timeline (root):** 369.24s → 414.24s (45s)

**Visual:** Giải pháp tối ưu: Xây dựng chuỗi mới bằng cách ghép ký tự 'D' với phần chuỗi cũ thông qua kỹ thuật slicing và toán tử cộng chuỗi.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: code-block update
- 20.0s: highlight slices syntax
- 35.0s: show success console output

**Narration (VO):**
> Để chỉnh sửa nội dung chuỗi một cách an toàn mà không ví phạm tính bất biến, ta phải tạo ra một vùng nhớ hoàn toàn mới. Chúng ta thực hiện việc ghép nối ký tự mới đê viết hoa với các phần tử từ chỉ mục cũ của chuỗi ban đầu. Vùng nhớ cũ được bảo toàn, còn biến mới sẽ tham chiếu đến chuỗi mới D-2026 một cách hợp lệ.

## Scene_12: Luồng dữ liệu một chiều tối ưu
**Timeline (root):** 414.24s → 449.24s (35s)

**Visual:** Nguyên tắc cốt lõi: Thiết kế luồng dữ liệu một chiều, tận dụng tính bất biến làm tấm khiên bảo vệ tính toàn vẹn dữ liệu trong hệ thống doanh nghiệp.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: summary-flow enter
- 15.0s: immutable-node highlight
- 25.0s: success-node glow

**Narration (VO):**
> Tóm lại khi làm việc với chuỗi văn bản trong Python, hãy luôn nghĩ đến việc xây dựng một luồng dữ liệu một chiều tức tạo ra dữ liệu mới thay vì sửa đổi trực tiếp dữ liệu cũ. Việc thấu hiểu tính bất biến và cách sử dụng chỉ mục thông minh sẽ giúp bạn xây dựng những hệ thống bảo mật cao và vận hành ổn định.


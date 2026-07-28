# HyperFrames Script: Session 08 — Lesson 01

**Lesson:** Giới thiệu hàm và cách định nghĩa
**Technology Stack:** python/core
**Total Duration:** 350.0s
**Scene Count:** 10

---

## Scene_01: Tổng quan về bài học
**Timeline (root):** 0.00s → 30.00s (30s)

**Visual:** Tiêu đề bài học trực quan kèm logo Rikkei Education và bản đồ tóm tắt 3 phần chính.

**Animation Timeline:**
- 0.2s: intro-title fade in
- 1.0s: main content show
- dur-0.8s: scene fade out

**Narration (VO):**
> Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong nội dung bài học này, chúng ta sẽ cùng tìm hiểu về Giới thiệu hàm và cách định nghĩa. Hàm là một trong những khối xây dựng cơ bản và quan trọng nhất trong lập trình Python. Việc hiểu rõ cách hoạt động của hàm sẽ giúp chúng ta cấu trúc mã nguồn một cách khoa học, tái sử dụng mã tối ưu và nâng cao khả năng bảo trì của hệ thống. Chúng ta sẽ đi sâu vào từ cú pháp cơ bản cho đến các mô hình bộ nhớ bên dưới.

## Scene_02: Động lực sử dụng hàm (Why Before How)
**Timeline (root):** 30.00s → 65.00s (35s)

**Visual:** So sánh giữa giải pháp lặp code lỗi thời và giải pháp khai báo hàm tái sử dụng gọn gàng.

**Animation Timeline:**
- 0.2s: titles slide-in
- 1.2s: duplicate code panel highlights red border
- 2.5s: positive function code reveals green border

**Narration (VO):**
> Để bắt đầu, hãy xem xét một kịch bản thực tế khi xây dựng ứng dụng tài chính. Khi chương trình cần tính toán thuế suất thuế thu nhập cá nhân ở nhiều nơi khác nhau, nếu không sử dụng hàm, chúng ta phải viết lặp đi lặp lại những khối lệnh logic giống nhau. Điều này không chỉ làm phình to mã nguồn mà còn gia tăng rủi ro khi có yêu cầu thay đổi logic kinh doanh. Một sửa đổi nhỏ cũng buộc chúng ta phải cập nhật thủ công tại tất cả các điểm xuất hiện mã lặp. Đây chính là động lực để hàm ra đời.

## Scene_03: Cú pháp khai báo cơ bản và Quy tắc đặt tên
**Timeline (root):** 65.00s → 100.00s (35s)

**Visual:** Minh họa cú pháp khai báo hàm với chú thích các thành phần: từ khóa def, tên hàm snake_case, tham số, dấu hai chấm.

**Animation Timeline:**
- 0.2s: title appears
- 0.8s: header definition code displays with highlighting
- 2.0s: sub-parameters components detail appear

**Narration (VO):**
> Kế tiếp, hãy cùng phân tích cú pháp tiêu chuẩn để khai báo một hàm trong Python. Chúng ta bắt đầu bằng từ khóa def, viết tắt của define. Theo sau là tên hàm được đặt theo quy tắc quy chuẩn snake gạch dưới kây, nghĩa là toàn bộ ký tự viết thường và phân tách bằng dấu gạch dưới. Cặp ngoặc đơn chứa danh sách tham số truyền vào và kết thúc dòng khai báo bắt buộc bằng dấu hai chấm. Cú pháp này báo hiệu cho trình biên dịch biết một khối chức năng mới đang được thiết lập.

## Scene_04: Quy tắc thụt lề và Docstring chuyên nghiệp
**Timeline (root):** 100.00s → 135.00s (35s)

**Visual:** Trực quan hóa khối thụt lề 4 khoảng trắng cùng cấu trúc viết docstring theo chuẩn PEP-257.

**Animation Timeline:**
- 0.2s: layout initialization
- 1.1s: show docstring block animation with border-yellow highlights
- 2.2s: show 4 space indentation indicators styling

**Narration (VO):**
> Bên trong thân hàm, có hai nguyên tắc kỹ thuật cực kỳ nghiêm ngặt cần tuân thủ. Thứ nhất là thụt lề bắt buộc bốn khoảng trắng cho toàn bộ các khối lệnh con. Thụt lề không chỉ giúp mã nguồn dễ đọc hơn mà còn là cú pháp bắt buộc trong Python. Thứ hai là việc viết tài liệu kỹ thuật bằng docstring. Đặt docstring bằng cặp nháy kép hoặc nháy đơn ba lần ngay dòng đầu tiên của thân hàm sẽ giúp mô tả chi tiết chức năng, kiểu dữ liệu trả về và cách thức sử dụng hàm một cách chuyên nghiệp.

## Scene_05: Luồng thực thi: Định nghĩa vs Lời gọi hàm
**Timeline (root):** 135.00s → 170.00s (35s)

**Visual:** Trực quan hóa luồng tuần tự khi biên dịch từ việc đăng ký hàm trên đầu xuống dòng gọi hàm ở cuối rồi nhảy ngược lại thực thi.

**Animation Timeline:**
- 0.2s: flow screen reveal
- 1.0s: highlight step 1 (def definition registration)
- 2.5s: highlight step 2 (call trace route activation)

**Narration (VO):**
> Tiếp theo, chúng ta sẽ xem xét luồng thực thi khi định nghĩa hàm và khi gọi hàm. Cần phân biệt rõ nét hai trạng thái này. Khi trình thông dịch Python quét qua khối định nghĩa bắt đầu bằng từ khóa def, nó sẽ đăng ký thực thể hàm nhưng chưa hề chạy các dòng mã bên trong thân hàm. Các câu lệnh bên trong chỉ thực sự được đánh giá và thực thi tuần tự khi có một lời gọi hàm chính thức xuất hiện bằng cách sử dụng tên hàm kèm theo cặp ngoặc đơn ở một vị trí khác trong chương trình.

## Scene_06: Bộ nhớ Python: Biến tham chiếu và Đối tượng trên Heap
**Timeline (root):** 170.00s → 210.00s (40s)

**Visual:** Mô hình bộ nhớ phân chia Stack chứa biến là tên hàm chỉ đến đối tượng Function thực tế nằm ở Heap.

**Animation Timeline:**
- 0.2s: layout elements display
- 1.2s: heap block pop-up with metadata values
- 2.2s: stack arrow connection to heap memory space

**Narration (VO):**
> Đằng sau hậu trường, cơ chế quản lý bộ nhớ của Python hoạt động thế nào khi định nghĩa một hàm? Hãy cùng quan sát lược đồ cấu trúc bộ nhớ. Khi một hàm được định nghĩa, Python sẽ tạo ra một đối tượng hàm đặc biệt nằm trên vùng nhớ Heap. Đối tượng này lưu trữ mã bytecode đã biên dịch cùng với các siêu dữ liệu khác của hàm. Tên hàm thực chất chỉ hoạt động như một biến tham chiếu, trỏ trực tiếp đến địa chỉ bộ nhớ của đối tượng hàm đó trên Heap.

## Scene_07: Ngăn xếp cuộc gọi: Phân rã Call Stack & Stack Frame
**Timeline (root):** 210.00s → 250.00s (40s)

**Visual:** Minh họa luồng Call Stack tăng lên khi gọi hàm và thu hẹp khi hàm hoàn tất trả lại kết quả.

**Animation Timeline:**
- 0.2s: base layout loading
- 1.1s: show base stack frame stack
- 2.3s: frame pop-up active and dissolve steps

**Narration (VO):**
> Thế nhưng, khi một lời gọi hàm được kích hoạt, một cấu trúc dữ liệu mới gọi là stack frame sẽ được tạo ra và đẩy vào ngăn xếp cuộc gọi call stack. Stack frame này đại diện cho không gian thực thi riêng biệt của hàm cụ thể, chứa các tham số truyền vào và toàn bộ biến cục bộ được khởi tạo bên trong. Sau khi hàm thực hiện xong nhiệm vụ và trả về kết quả, stack frame của nó sẽ lập tức bị hủy bỏ khỏi call stack để giải phóng bộ nhớ cho hệ thống chương trình.

## Scene_08: Lỗi thường gặp: Lỗi thụt lề (IndentationError)
**Timeline (root):** 250.00s → 285.00s (35s)

**Visual:** Trực quan hóa một đoạn code nguồn bị lỗi IndentationError và mã lỗi thực tế trên Console.

**Animation Timeline:**
- 0.2s: screen elements show up
- 1.2s: flag line 3 return error visual red highlight
- 2.2s: console crash output display

**Narration (VO):**
> Để tránh những trục trặc trong quá trình phát triển, chúng ta cần nhận diện lỗi đầu tiên rất phổ biến là indentation error. Lỗi này xảy ra khi các câu lệnh bên trong thân hàm không được thụt lề thống nhất bốn khoảng trắng, hoặc do sự pha trộn không hợp lý giữa phím tab và phím cách. Python đòi hỏi sự đồng bộ cấu trúc tuyệt đối, do đó chỉ một sai lệch nhỏ trong việc điều chỉnh thụt lề dòng lệnh cũng sẽ lập tức dừng chương trình và báo lỗi biên dịch.

## Scene_09: Lỗi thường gặp: Gọi hàm trước khi định nghĩa
**Timeline (root):** 285.00s → 320.00s (35s)

**Visual:** Trực quan hóa đoạn mã bị lỗi NameError khi hàm bị gọi từ dòng 1 nhưng phần def lại nằm ở dòng 3.

**Animation Timeline:**
- 0.2s: elements slide-up
- 1.1s: highlight compiler flow going top-down and crashing at line 1
- 2.5s: detail output panel update info status

**Narration (VO):**
> Một lỗi cơ bản tiếp theo là cố gắng gọi hàm trước khi định nghĩa nó. Do Python là một ngôn ngữ thông dịch thực thi mã tuần tự từ trên xuống dưới, việc sử dụng tên hàm để thực thi trước khi định nghĩa bằng từ khóa def xuất hiện sẽ dẫn đến lỗi name error. Trình thông dịch sẽ thông báo rằng tên hàm chưa được xác định. Quy chuẩn lập trình luôn đòi hỏi hàm phải được khai báo hoàn chỉnh trước khi sử dụng trong mã nguồn ứng dụng.

## Scene_10: Tóm tắt bài học & Bài học tiếp theo
**Timeline (root):** 320.00s → 350.00s (30s)

**Visual:** Trang tóm tắt kết thúc chứa danh sách kiến thức cốt lõi và lộ trình tiếp theo thiết kế theo thẻ màu tương phản.

**Animation Timeline:**
- 0.2s: ending page fade-in
- 1.1s: show review check points sequential display
- 2.5s: display next session preview card outline

**Narration (VO):**
> Như vậy, trong bài học này chúng ta đã tìm hiểu về khái niệm hàm, cú pháp khai báo chuẩn, cơ chế hoạt động của stack và heap cùng các lỗi thường gặp trong quá trình định nghĩa hàm. Trong bài học tiếp theo, chúng ta sẽ tìm hiểu về Tham số và Giá trị trả về của hàm trong Python. Xin cảm ơn và hẹn gặp lại.


# HyperFrames Script: Session 06 — Lesson 02

**Lesson:** Thao tác với List (thêm, sửa, xoá phần tử)
**Technology Stack:** python/core
**Total Duration:** 440.0s
**Scene Count:** 12

---

## Scene_01: Giới thiệu nội dung bài học
**Timeline (root):** 0.00s → 30.00s (30s)

**Visual:** Sơ đồ tổng quan về các nhóm thao tác cốt lõi trên List bao gồm: Thêm phần tử, Sửa phần tử bằng chỉ mục, và Xóa phần tử bằng các phương thức tích hợp.

**Animation Timeline:**
- 0.2s: intro-title fade in
- 2.5s: main categories display sequentially
- 29.0s: scene fade out

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education, trong nội dung bài học này, chúng ta sẽ cùng nhau tìm hiểu về Thao tác với List (thêm, sửa, xoá phần tử). Đây là những kỹ năng cơ bản nhưng cực kỳ quan trọng giúp chúng ta làm chủ cấu trúc dữ liệu mảng trong ngôn ngữ lập trình Python.

## Scene_02: Bối cảnh doanh nghiệp và bài toán thực tế
**Timeline (root):** 30.00s → 65.00s (35s)

**Visual:** Bảng so sánh giữa dữ liệu tĩnh không thể thay đổi và hệ thống giỏ hàng động sử dụng List linh hoạt.

**Animation Timeline:**
- tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: title header fade in
- 3.0s: static column show
- 7.0s: dynamic column highlights as the optimized solution

**Narration (VO):**
> Hãy tưởng tượng các em đang xây dựng một hệ thống giỏ hàng cho một trang thương mại điện tử. Giỏ hàng này liên tục thay đổi: khách hàng thêm sản phẩm mới vào cuối, chèn một quà tặng khuyến mãi vào vị trí bất kỳ, gộp danh sách sản phẩm quà tặng, cập nhật số lượng, hoặc xóa một mặt hàng khỏi giỏ. Làm thế nào để chúng ta xử lý danh sách động này một cách tối ưu hiệu năng bộ nhớ?

## Scene_03: Phương thức append()
**Timeline (root):** 65.00s → 105.00s (40s)

**Visual:** Đoạn code minh họa cách khởi tạo danh sách sản phẩm và sử dụng append thêm một phần tử vào cuối danh sách.

**Animation Timeline:**
- 0.2s: load code editor interface
- 4.0s: type line coding step by step
- 15.0s: highlight append execution result

**Narration (VO):**
> Phương thức đầu tiên là a-pen. Phương thức này giúp thêm một phần tử vào cuối danh sách hiện tại. Cú pháp rất đơn giản: tên lít chấm a-pen và truyền giá trị cần thêm vào cặp ngoặc tròn. Các em lưu ý phương thức này làm thay đổi trực tiếp lít ban đầu và có độ phức tạp thời gian cực nhanh là ô một.

## Scene_04: Phương thức insert()
**Timeline (root):** 105.00s → 145.00s (40s)

**Visual:** Mã nguồn Python minh họa việc chèn một quà tặng tại vị trí chỉ mục số một để đè dòng sản phẩm hiện tại lùi lại lý thuyết.

**Animation Timeline:**
- 0.2s: load source code container
- 3.5s: simulate code keyboard typing behavior
- 18.0s: highlight shift operations visualization

**Narration (VO):**
> Khi muốn chèn một phần tử vào một vị trí cụ thể chứ không phải ở cuối, chúng ta sử dụng phương thức in-sợt. Cú pháp yêu cầu hai đối số: đối số đầu tiên là in-đếch vị trí muốn chèn, đối số thứ hai là giá trị cần chèn. Các phần tử đứng sau vị trí này sẽ tự động dịch chuyển sang phải một đơn vị.

## Scene_05: Phương thức extend()
**Timeline (root):** 145.00s → 185.00s (40s)

**Visual:** Đoạn mã demo phương thức extend kết hợp giỏ hàng chính với danh sách sản phẩm tặng kèm một cách trực quan.

**Animation Timeline:**
- 0.2s: open script view window
- 5.0s: reveal extend syntax call
- 20.0s: render console printed output line

**Narration (VO):**
> Nếu muốn gộp toàn bộ các phần tử của một lít khác vào lít hiện tại, ta nên dùng ếch-xten để tối ưu hiệu năng thay vì sử dụng vòng lặp. Nó sẽ duyệt qua toàn bộ các phần tử của đối tượng truyền vào và lần lượt thêm chúng vào cuối danh sách đích.

## Scene_06: So sánh append(), insert() và extend()
**Timeline (root):** 185.00s → 220.00s (35s)

**Visual:** Bảng so sánh ba phương thức thêm phần tử dựa trên các tiêu chí: Vị trí thêm, loại dữ liệu truyền vào và Hiệu năng bộ nhớ.

**Animation Timeline:**
- 0.2s: create comparison table frame
- 4.0s: highlight append row
- 12.0s: highlight insert row
- 20.0s: highlight extend row

**Narration (VO):**
> Để ghi nhớ sâu hơn, chúng ta cùng nhìn vào bảng so sánh này. A-pen chỉ thêm một phần tử vào cuối. In-sợt cho phép chọn vị trí bất kỳ bằng chỉ mục nhưng tốn thời gian dịch chuyển vùng nhớ. Còn ếch-xten được sinh ra chuyên biệt để nối hai danh sách lại với nhau một cách hiệu quả.

## Scene_07: Sửa phần tử trong List bằng Index
**Timeline (root):** 220.00s → 255.00s (35s)

**Visual:** Đoạn mã Python thực hiện sửa phần tử tại chỉ mục 1 của giỏ hàng từ tên cũ thành tên mới chất lượng hơn.

**Animation Timeline:**
- 0.2s: dynamic text script load
- 4.0s: highlight target reassignment line using index
- 18.0s: draw update marker over terminal view

**Narration (VO):**
> Bây giờ chúng ta cùng chuyển sang thao tác sửa đổi giá trị. Việc cập nhật giá trị của một phần tử trong lít vô cùng đơn giản bằng cách truy cập trực tiếp qua chỉ mục và gán một giá trị mới cho nó thông qua toán tử gán dấu bằng.

## Scene_08: Xóa phần tử bằng phương thức pop()
**Timeline (root):** 255.00s → 295.00s (40s)

**Visual:** Đoạn code Python trình bày cách dùng pop loại bỏ phần tử cuối hoặc phần tử tại vị trí chỉ mục mong muốn và lưu trữ giá trị thu hồi đó.

**Animation Timeline:**
- 0.2s: load code panel structure
- 5.0s: highlight pop without arguments output
- 18.0s: detail target parameters for local deletion

**Narration (VO):**
> Tiếp theo là hành vi xóa phần tử. Phương thức póp được dùng khi các em muốn xóa một phần tử ra khỏi danh sách và đồng thời lấy ra giá trị đó để sử dụng cho mục đích khác như hoàn tác hay ghi nhật ký hệ thống. Nếu không truyền in-đếch, póp mặc định loại bỏ phần tử cuối cùng của lít.

## Scene_09: Xóa phần tử theo giá trị bằng remove()
**Timeline (root):** 295.00s → 335.00s (40s)

**Visual:** Minh họa code Python dùng remove để tìm và xóa phần tử có giá trị cụ thể trong danh sách sản phẩm thương mại điện tử.

**Animation Timeline:**
- 0.2s: build interface output state
- 6.5s: emphasize text matches list search path
- 20.0s: show state change inside array elements

**Narration (VO):**
> Khi các em chỉ biết giá trị của phần tử cần xóa chứ không biết vị trí in-đếch của nó, hãy sử dụng phương thức ri-muv. Một điểm cần hết sức lưu ý là nếu giá trị ấy xuất hiện nhiều lần trong lít, phương thức ri-muv chỉ xóa đi phần tử tìm thấy đầu tiên tính từ trái qua phải.

## Scene_10: Xóa sạch toàn bộ phần tử với clear()
**Timeline (root):** 335.00s → 370.00s (35s)

**Visual:** Mã thực thi phương thức clear đưa một danh sách có sẵn các phần tử về một danh sách rỗng.

**Animation Timeline:**
- 0.2s: render code window elements
- 4.0s: type clear execution command block
- 15.0s: showcase empty array bracket result

**Narration (VO):**
> Sau cùng, khi người dùng muốn xóa sạch toàn bộ sản phẩm để đưa giỏ hàng về trạng thái trống rỗng hoàn toàn, phương thức clia sẽ giải quyết gọn gàng điều này. Sau khi gọi clia, độ dài của danh sách sẽ trả về bằng không.

## Scene_11: Cảnh báo cạm bẫy lỗi thường gặp
**Timeline (root):** 370.00s → 405.00s (35s)

**Visual:** Cảnh báo lỗi IndexError khi pop chỉ mục không hợp lý và ValueError khi remove phần tử không tồn tại trong danh sách.

**Animation Timeline:**
- 0.2s: draw red alert container outline
- 4.0s: pop critical error points texts
- 18.0s: present best practice tips box below

**Narration (VO):**
> Các em lưu ý phần quan trọng này nhé. Khi thao tác với danh sách, các em rất dễ gặp lỗi in-đếch e-rơ hay va-liu e-rơ. Ví dụ, cố xóa bằng ri-muv một giá trị không nằm trong lít, hoặc truy cập chỉ mục vượt quá chiều dài của nó bằng póp sẽ làm chương trình bị đổ bể. Phải luôn viết mã kiểm tra hoặc sử dụng khối thử và bắt lỗi an toàn.

## Scene_12: Tổng kết bài học & Chào kết
**Timeline (root):** 405.00s → 440.00s (35s)

**Visual:** Sơ đồ tóm tắt ngắn gọn các hành vi quản trị list và các từ khóa cốt lõi cần nhớ từ bài học.

**Animation Timeline:**
- 0.2s: outline summary titles
- 6.0s: display final keywords lists
- 28.0s: fade out background components

**Narration (VO):**
> Thông qua bài học này, chúng ta đã cùng tìm hiểu thành công toàn bộ cách thêm, sửa, và xóa phần tử trong lít bằng các hàm tiêu chuẩn trong ngôn ngữ Python. Chúc các em luyện tập tốt và áp dụng thành thạo vào dự án thực tế của mình. Cảm ơn các em đã theo dõi, hẹn gặp lại trong các bài học tiếp theo!


# HyperFrames Script: Session 02 — Lesson 03

**Lesson:** Toán tử logic
**Technology Stack:** python/core
**Total Duration:** 100.0s
**Scene Count:** 4

---

## Scene_01: Vấn đề đặt ra
**Timeline (root):** 0.00s → 25.00s (25.0s)

**Visual:** Màn hình chia đôi. Bên trái hiển thị code rẽ nhánh lồng nhau phức tạp bị gạch chéo đỏ. Bên phải hiển thị hình ảnh minh họa về điều kiện tuổi (18-60) và sức khỏe được kết hợp tối ưu.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha: 1}, 0)
- 0.2s: #intro-title fade in
- 3.2s: #intro-title scale nhỏ lại và di chuyển lên góc trái làm label
- 4.0s: #panel-left (code phức tạp) slide in từ trái
- 10.0s: Dấu gạch chéo đỏ đè lên #panel-left thể hiện sự không tối ưu
- 14.0s: #panel-right (hình ảnh minh họa điều kiện kết hợp) hiện lên mượt mà

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong lập trình, chúng ta thường cần kiểm tra nhiều điều kiện cùng lúc để đưa ra quyết định, ví dụ như kiểm tra độ tuổi và sức khỏe. Làm thế nào để viết code ngắn gọn, tối ưu thay vì lồng nhiều câu lệnh phức tạp? Hôm nay chúng ta sẽ tìm hiểu về các toán tử logic trong Python.

## Scene_02: Toán tử logic & Bảng chân trị
**Timeline (root):** 25.00s → 50.00s (25.0s)

**Visual:** Phía dưới tiêu đề góc trái là một bảng chân trị (Truth Table) trống được điền dần kết quả. Bên phải là đoạn code Python sử dụng hai vòng lặp lồng nhau sinh ra bảng chân trị này.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha: 1}, 0)
- 0.2s: #intro-title fade in
- 3.2s: #intro-title scale nhỏ lại và di chuyển lên góc trái
- 4.2s: #code-card chứa đoạn code Python generator xuất hiện ở bên phải
- 8.0s: #table-card hiển thị cấu trúc bảng chân trị trống ở bên trái
- 12.0s: Các dòng kết quả True, False và kết quả biểu thức (A and not B) lần lượt xuất hiện ứng với vòng lặp code

**Narration (VO):**
> Python cung cấp ba toán tử logic chính gồm and, or và not. Để hiểu rõ cách chúng hoạt động, chúng ta sử dụng bảng chân trị. Hãy xem cách viết code tự động xuất bảng chân trị cho biểu thức A and not B bằng cách lặp qua các giá trị True và False để kiểm tra kết quả.

## Scene_03: Độ ưu tiên toán tử
**Timeline (root):** 50.00s → 75.00s (25.0s)

**Visual:** Một sơ đồ cấp bậc (hierarchy pyramid) hiển thị thứ tự ưu tiên toán tử từ trên xuống dưới: So sánh (>, <, ...) -> not -> and -> or. Các ví dụ minh họa tương ứng xuất hiện bên cạnh mỗi cấp bậc.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha: 1}, 0)
- 0.2s: #intro-title fade in
- 3.2s: #intro-title scale và di chuyển lên góc trái
- 4.5s: Cấp cao nhất của kim tự tháp (phép so sánh) xuất hiện
- 8.0s: Các cấp tiếp theo (not, and, or) xuất hiện từ trên xuống dưới bằng hiệu ứng slide down
- 15.0s: Một biểu thức ví dụ thực tế xuất hiện kèm highlight thứ tự tính toán thực tế của Python

**Narration (VO):**
> Khi kết hợp nhiều toán tử, Python đánh giá theo thứ tự ưu tiên mặc định. Đầu tiên là các phép so sánh toán học, tiếp theo là toán tử not, sau đó đến and, và cuối cùng là or. Hiểu rõ thứ tự này giúp các em tránh được lỗi logic nghiêm trọng khi viết biểu thức phức tạp.

## Scene_04: Lỗi thường gặp & Tổng kết
**Timeline (root):** 75.00s → 100.00s (25.0s)

**Visual:** Ba chiếc thẻ cảnh báo (Warning cards) tương ứng với 3 lỗi thường gặp xuất hiện trên màn hình. Mỗi thẻ có tiêu đề đỏ và mô tả ngắn dạng code highlight lỗi. Cuối cùng hiển thị lời chào tạm biệt.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha: 1}, 0)
- 0.2s: #intro-title fade in
- 3.2s: #intro-title scale và di chuyển lên góc trái
- 4.5s: Lần lượt 3 thẻ cảnh báo xuất hiện từ trái qua phải bằng hiệu ứng bounce drop
- 15.0s: Toàn bộ panel lỗi ẩn đi, chữ 'Cảm ơn các em & Hẹn gặp lại!' hiển thị to rõ giữa màn hình với hiệu ứng glow nhẹ

**Narration (VO):**
> Hãy lưu ý ba lỗi phổ biến: sai thứ tự ưu tiên do thiếu ngoặc đơn, ngăn mạch ngoài ý muốn, và nhầm lẫn các giá trị Falsy như số không hoặc chuỗi rỗng. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


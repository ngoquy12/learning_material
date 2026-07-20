# HyperFrames Script: Session 02 — Lesson 04

**Lesson:** Cấu trúc điều kiện rẽ nhánh if-elif-else
**Technology Stack:** python/core
**Total Duration:** 100.0s
**Scene Count:** 4

---

## Scene_01: Sự cần thiết của rẽ nhánh
**Timeline (root):** 0.00s → 25.00s (25.0s)

**Visual:** Màn hình chia đôi. Bên trái hiển thị luồng chạy tuần tự từ trên xuống dưới bị hạn chế. Bên phải hiển thị một sơ đồ tư duy rẽ nhánh trực quan dựa trên dữ liệu đầu vào.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: split-container hiển thị hai panel trái phải
- 8.5s: dòng chảy tuần tự bên panel trái chạy và dừng lại ở điểm cần rẽ nhánh
- 12.0s: sơ đồ quyết định bên panel phải sáng lên với mũi tên rẽ hướng
- 25.0s: timeline dừng lại

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong lập trình, đôi khi chúng ta cần chương trình đưa ra quyết định thông minh dựa trên dữ liệu thực tế, thay vì chỉ thực thi các dòng lệnh tuần tự từ trên xuống dưới. Đó là lúc cấu trúc rẽ nhánh xuất hiện.

## Scene_02: Cú pháp if-elif-else
**Timeline (root):** 25.00s → 55.00s (30.0s)

**Visual:** Khung soạn thảo code Python hiện ra ở giữa màn hình. Dòng code minh họa tính BMI được hiển thị với màu sắc cú pháp chuẩn (syntax highlighting). Cung cấp hiệu ứng highlight từng dòng tương ứng với thứ tự chạy logic.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title lên góc trái trên
- 4.0s: code block chứa biến bmi và cấu trúc if-elif-else xuất hiện
- 8.0s: highlight dòng điều kiện bmi < 18.5 (False)
- 14.0s: highlight dòng điều kiện tiếp theo bmi < 25.0 (True) và in ra kết quả 'Binh thuong'
- 30.0s: timeline dừng lại

**Narration (VO):**
> Chúng ta sử dụng các từ khóa if, elif và else kết hợp với toán tử so sánh để phân loại điều kiện. Hãy xem ví dụ phân loại chỉ số BMI sau đây. Nếu điều kiện đầu tiên sai, chương trình sẽ tiếp tục kiểm tra các điều kiện tiếp theo trước khi thực thi nhánh else.

## Scene_03: 3 lỗi thường gặp khi rẽ nhánh
**Timeline (root):** 55.00s → 80.00s (25.0s)

**Visual:** Ba thẻ ghi chú màu tối viền đỏ nổi lên lần lượt. Mỗi thẻ mô tả chi tiết một lỗi kèm ví dụ code sai tương ứng: Lỗi thiếu dấu hai chấm, lỗi thụt lề IndentationError, và Unreachable Code.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: thẻ lỗi thứ nhất (Thiếu dấu hai chấm) slide in từ dưới lên
- 10.0s: thẻ lỗi thứ hai (Thụt lề không chuẩn) slide in từ dưới lên
- 16.0s: thẻ lỗi thứ ba (Sắp xếp sai thứ tự) slide in báo động Unreachable Code
- 25.0s: timeline dừng lại

**Narration (VO):**
> Khi sử dụng cấu trúc rẽ nhánh, các em cần lưu ý ba lỗi phổ biến. Đó là thiếu dấu hai chấm ở cuối điều kiện gây lỗi cú pháp, thụt lề không đồng nhất dẫn đến lỗi logic, và sắp xếp sai thứ tự điều kiện khiến mã nguồn bị che khuất và không thể thực thi.

## Scene_04: Tổng kết bài học
**Timeline (root):** 80.00s → 100.00s (20.0s)

**Visual:** Một bảng tổng kết đẹp mắt hiện ra giữa màn hình với các ô check-box tổng kết kiến thức: Hiểu bản chất rẽ nhánh, Nhớ cú pháp chuẩn thụt lề, Sắp xếp thứ tự thông minh.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title dịch chuyển lên phía trên làm tiêu đề bảng
- 4.0s: bảng tổng kết hiện ra cùng hiệu ứng tick xanh lá lần lượt xuất hiện tại các đầu dòng ghi nhớ
- 20.0s: timeline kết thúc hoàn toàn

**Narration (VO):**
> Tóm lại, cấu trúc rẽ nhánh giúp điều khiển dòng chạy ứng dụng một cách linh hoạt dựa trên Boolean. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


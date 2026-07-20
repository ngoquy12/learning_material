# HyperFrames Script: Session 01 — Lesson 01

**Lesson:** Giới thiệu ngôn ngữ Python
**Technology Stack:** python/core
**Total Duration:** 105s
**Scene Count:** 4

---

## Scene_01: Nguồn gốc & Triết lý Python
**Timeline (root):** 0.00s → 25.00s (25s)

**Visual:** Màn hình tối nền tối giản hiển thị timeline lịch sử. Một card chân dung vector của Guido van Rossum xuất hiện bên trái, tiếp theo là cột mốc năm 1991, và hai card mô tả đặc trưng triết lý: Tối giản và Dễ đọc.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.0s: tl.set(['#creator-card', '#year-badge', '.philosophy-card'], {autoAlpha:0, y:30}, 0)
- 0.2s: tl.to('#intro-title', {autoAlpha:1, scale:1, duration:0.6, ease:'back.out(1.4)'}, 0.2)
- 3.2s: tl.to('#intro-title', {scale:0.38, x:-760, y:-460, duration:0.7, ease:'power3.inOut'}, 3.2)
- 4.2s: tl.to('#creator-card', {autoAlpha:1, y:0, duration:0.5, ease:'power3.out'}, 4.2)
- 5.0s: tl.to('#year-badge', {autoAlpha:1, y:0, duration:0.5, ease:'back.out(1.5)'}, 5.0)
- 6.5s: tl.to('.philosophy-card', {autoAlpha:1, y:0, duration:0.5, stagger:0.2, ease:'power3.out'}, 6.5)
- 25.0s: tl.set({}, {}, 25)

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay, chúng ta sẽ bắt đầu hành trình chinh phục Python. Được Guido van Rossum ra mắt vào năm 1991, Python nổi bật với triết lý tối giản, dễ học và dễ đọc.

## Scene_02: Cơ chế Trình thông dịch
**Timeline (root):** 25.00s → 50.00s (25s)

**Visual:** Sơ đồ khối ngang trực quan hóa trình thông dịch. Ba khối chính sáng lên tuần tự: Khối nguồn xanh dương (Code .py), khối xử lý cam (Interpreter), và khối đích vàng (Output) kết nối bởi các mũi tên động.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.0s: tl.set(['.flow-block', '.flow-arrow'], {autoAlpha:0, scale:0.9}, 0)
- 0.2s: tl.to('#intro-title', {autoAlpha:1, scale:1, duration:0.6, ease:'back.out(1.4)'}, 0.2)
- 3.2s: tl.to('#intro-title', {scale:0.38, x:-760, y:-460, duration:0.7, ease:'power3.inOut'}, 3.2)
- 4.2s: tl.to('#block-code', {autoAlpha:1, scale:1, duration:0.5, ease:'back.out(1.2)'}, 4.2)
- 6.0s: tl.to('#arrow-1', {autoAlpha:1, scale:1, duration:0.4}, 6.0)
- 7.2s: tl.to('#block-interpreter', {autoAlpha:1, scale:1, duration:0.5, ease:'back.out(1.2)'}, 7.2)
- 9.0s: tl.to('#arrow-2', {autoAlpha:1, scale:1, duration:0.4}, 9.0)
- 10.2s: tl.to('#block-output', {autoAlpha:1, scale:1, duration:0.5, ease:'back.out(1.2)'}, 10.2)
- 25.0s: tl.set({}, {}, 25)

**Narration (VO):**
> Khác với ngôn ngữ biên dịch, Python là ngôn ngữ thông dịch. Trình thông dịch Interpreter sẽ đọc trực tiếp mã nguồn chấm py, dịch các dòng lệnh và thực thi ra kết quả ngay lập tức, giúp tối ưu hóa thời gian kiểm tra và phát triển phần mềm.

## Scene_03: Kiểu dữ liệu động
**Timeline (root):** 50.00s → 80.00s (30s)

**Visual:** Khung giả lập IDE tối màu ở bên trái chứa mã nguồn chạy từ trên xuống. Bên phải hiển thị bảng gán kiểu tương tác thực tế, chuyển trạng thái từ Integer sang String khi code chạy qua dòng tương ứng.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.0s: tl.set(['#ide-container', '#variable-pane', '.code-line', '.type-badge'], {autoAlpha:0, x:-30}, 0)
- 0.2s: tl.to('#intro-title', {autoAlpha:1, scale:1, duration:0.6, ease:'back.out(1.4)'}, 0.2)
- 3.2s: tl.to('#intro-title', {scale:0.38, x:-760, y:-460, duration:0.7, ease:'power3.inOut'}, 3.2)
- 4.2s: tl.to('#ide-container', {autoAlpha:1, x:0, duration:0.6, ease:'power3.out'}, 4.2)
- 6.0s: tl.to('#code-line-1', {autoAlpha:1, duration:0.4}, 6.0)
- 8.5s: tl.to('#variable-pane', {autoAlpha:1, x:0, duration:0.5}, 8.5)
- 10.0s: tl.to('#type-badge-integer', {autoAlpha:1, scale:1, duration:0.4, ease:'back.out(1.2)'}, 10.0)
- 14.0s: tl.to('#code-line-2', {autoAlpha:1, duration:0.4}, 14.0)
- 16.5s: tl.to('#type-badge-integer', {autoAlpha:0, scale:0.8, duration:0.3}, 16.5)
- 17.2s: tl.to('#type-badge-string', {autoAlpha:1, scale:1, duration:0.4, ease:'back.out(1.2)'}, 17.2)
- 30.0s: tl.set({}, {}, 30)

**Narration (VO):**
> Điểm đặc biệt là Python sử dụng Dynamic Typing. Biến số x ban đầu nhận giá trị mười thuộc kiểu số nguyên, nhưng sau đó có thể gán ngay bằng một chuỗi chữ mà không cần khai báo lại kiểu dữ liệu, mang lại sự linh hoạt đáng kinh ngạc.

## Scene_04: Sai lầm cần tránh & Tổng kết
**Timeline (root):** 80.00s → 105.00s (25s)

**Visual:** Màn hình tổng kết hiển thị lưới 3 thẻ cảnh báo lỗi màu đỏ đậm với nhãn biểu tượng nguy hiểm. Toàn bộ thông tin được trình bày gọn gàng, súc tích trước khi chuyển sang logo Rikkei Academy kết thúc.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.0s: tl.set(['.error-card', '#outro-logo'], {autoAlpha:0, y:45}, 0)
- 0.2s: tl.to('#intro-title', {autoAlpha:1, scale:1, duration:0.6, ease:'back.out(1.4)'}, 0.2)
- 3.2s: tl.to('#intro-title', {autoAlpha:0, scale:0.9, duration:0.5, ease:'power2.in'}, 3.2)
- 4.2s: tl.to('.error-card', {autoAlpha:1, y:0, duration:0.5, stagger:0.25, ease:'power3.out'}, 4.2)
- 15.0s: tl.to('.error-card', {autoAlpha:0, scale:0.95, duration:0.5}, 15.0)
- 16.5s: tl.to('#outro-logo', {autoAlpha:1, y:0, duration:0.6, ease:'back.out(1.2)'}, 16.5)
- 25.0s: tl.set({}, {}, 25)

**Narration (VO):**
> Tóm lại, hãy chú ý ba sai lầm: tính toán sai kiểu dữ liệu, lỗi thụt lề IndentationError, và tự ý gán đè kiểu dữ liệu khác loại gây lỗi logic. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


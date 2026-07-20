# HyperFrames Script: Session 02 — Lesson 02

**Lesson:** Toán tử so sánh
**Technology Stack:** python/core
**Total Duration:** 90s
**Scene Count:** 3

---

## Scene_01: Đặt vấn đề & Vai trò
**Timeline (root):** 0.00s → 28.00s (28s)

**Visual:** Màn hình chia đôi. Bên trái hiển thị hoạt ảnh một người trước cổng bầu cử kèm cảnh báo đỏ 'Không rõ tuổi'. Bên phải hiện sơ đồ logic rẽ nhánh điều kiện so sánh tuổi >= 18 chuyển sang màu xanh.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: panel-problem slide in từ bên trái
- 10.0s: icon cảnh báo lắc nhẹ cảnh báo lỗi logic
- 15.0s: panel-solution fade in bên phải hiển thị giải pháp
- 28.0s: kết thúc scene

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong lập trình, để máy tính đưa ra quyết định tự động, chúng ta phải so sánh dữ liệu. Nếu không thể so sánh độ tuổi hay tải trọng, chương trình sẽ không có logic rẽ nhánh.

## Scene_02: Ví dụ thực tế trong Python
**Timeline (root):** 28.00s → 58.00s (30s)

**Visual:** Trình mô phỏng Code Editor tối giản hiển thị code Python. Đoạn code khai báo tuổi, thực hiện phép so sánh số và so sánh chuỗi, bên dưới hiển thị Console Output xuất ra kết quả tương ứng.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: mock-editor scale in nhẹ nhàng xuất hiện trung tâm
- 6.0s: fade in 2 dòng code đầu tiên (age = 20 và is_valid = age >= 18)
- 14.0s: fade in dòng so sánh chuỗi (compare_str = 'apple' < 'banana')
- 20.0s: console-panel slide up từ dưới lên
- 22.0s: kết quả 'Eligible: True' và 'String compare: True' hiện lên ở console
- 30.0s: kết thúc scene

**Narration (VO):**
> Hãy xem ví dụ, ta so sánh biến age có lớn hơn hoặc bằng mười tám hay không, kết quả trả về sẽ là True. Chúng ta cũng có thể so sánh thứ tự bảng chữ cái của các chuỗi như apple và banana.

## Scene_03: Tổng kết & Lỗi cần tránh
**Timeline (root):** 58.00s → 90.00s (32s)

**Visual:** Một bảng tổng kết trực quan hiện ra chia thành 3 phần cảnh báo lỗi màu đỏ-cam tương ứng với 3 sai lầm phổ biến nhất khi viết biểu thức so sánh kèm code sai được gạch chéo đỏ và sửa lại màu xanh.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: tiêu đề '3 LỖI PHỔ BIẾN' xuất hiện ở trên cùng
- 6.0s: card lỗi 1 (nhầm = và ==) slide in từ bên trái
- 13.0s: card lỗi 2 (TypeError chuỗi và số) slide in từ bên trái
- 20.0s: card lỗi 3 (sai thứ tự => thay vì >=) slide in từ bên trái
- 32.0s: kết thúc scene

**Narration (VO):**
> Tóm lại, toán tử so sánh trả về True hoặc False. Các em cần tránh ba lỗi: nhầm dấu bằng với so sánh bằng, so sánh sai kiểu dữ liệu, và viết sai ký tự toán tử kép. Cảm ơn các em đã theo dõi, hẹn gặp lại!


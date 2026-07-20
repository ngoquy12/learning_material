# HyperFrames Script: Session 01 — Lesson 03

**Lesson:** Biến và Kiểu dữ liệu cơ bản
**Technology Stack:** python/core
**Total Duration:** 84.0s
**Scene Count:** 4

---

## Scene_01: Tại sao cần sử dụng biến?
**Timeline (root):** 0.00s → 22.00s (22.0s)

**Visual:** Mô phỏng bộ lưu trữ RAM dưới dạng các ô lưới bộ nhớ chứa dữ liệu lộn xộn. Sau đó xuất hiện một chiếc hộp đại diện cho 'Biến' với nhãn dán cụ thể giúp sắp xếp thông tin một cách ngăn nắp.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title scale down và di chuyển lên góc trái
- 4.2s: ram-grid fade in giới thiệu giao diện bộ nhớ
- 8.5s: variable-container và variable-label slide up hiển thị khái niệm hộp chứa
- 15.0s: dữ liệu ảo bay từ ngoài vào đặt trong hộp chứa
- 22.0s: tl.set({}, {}, 22.0)

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Khi viết chương trình, máy tính cần lưu trữ các thông tin tạm thời như dữ liệu người dùng hay trạng thái hệ thống trong bộ nhớ RAM. Để giải quyết vấn đề này, chúng ta sử dụng biến.

## Scene_02: Khai báo & Quy tắc đặt tên
**Timeline (root):** 22.00s → 42.00s (20.0s)

**Visual:** Hiển thị cú pháp chuẩn 'tên_biến = giá_trị'. Bên dưới là bảng quy tắc đặt tên chia làm hai cột: Việc nên làm (hợp lệ) và Việc nên tránh (không hợp lệ).

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title scale down và di chuyển lên góc trái
- 4.0s: syntax-card scale in thể hiện công thức gán biến
- 8.0s: rule-valid và rule-invalid container đồng loạt slide in từ hai bên trái phải
- 12.5s: hiệu ứng highlight nhấp nháy cho toán tử gán bằng '='
- 20.0s: tl.set({}, {}, 20.0)

**Narration (VO):**
> Trong Python, ta khai báo biến bằng toán tử gán dấu bằng. Tên biến chỉ chứa chữ cái, chữ số và dấu gạch dưới, không bắt đầu bằng số và không trùng từ khóa của hệ thống.

## Scene_03: Thực hành & Ví dụ Code
**Timeline (root):** 42.00s → 64.00s (22.0s)

**Visual:** Giao diện IDE giả lập hiển thị code khai báo 4 biến đại diện cho 4 kiểu dữ liệu. Phía dưới là terminal hiển thị kết quả đầu ra trực quan sau khi ép kiểu và chạy hàm type().

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title scale down và di chuyển lên góc trái
- 4.2s: ide-editor card slide in từ phía dưới lên
- 6.0s: các dòng code line xuất hiện lần lượt (stagger)
- 12.0s: terminal-output slide up hiển thị các dòng kết quả
- 16.5s: highlight những cụm từ khóa int, float, str, bool trên màn hình
- 22.0s: tl.set({}, {}, 22.0)

**Narration (VO):**
> Hãy xem ví dụ sau với các kiểu dữ liệu cơ bản như số nguyên, số thực, chuỗi, và kiểu luận lý. Chúng ta sử dụng hàm pờ-rin và hàm tai để kiểm tra giá trị và kiểu dữ liệu thực tế của biến.

## Scene_04: Các lỗi phổ biến cần tránh
**Timeline (root):** 64.00s → 84.00s (20.0s)

**Visual:** Màn hình hiển thị bảng đối chiếu gồm 3 lỗi sai kinh điển bằng màu đỏ, kèm theo cách sửa đúng tương ứng màu xanh lá. Cuối cùng xuất hiện lời chào kết thúc khóa học.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.0s: errors-grid xuất hiện dạng scale in nhẹ nhàng
- 5.5s: các dấu gạch chéo đỏ xuất hiện tại cột lỗi sai (stagger)
- 10.0s: các dấu tích xanh lá hiện lên ở cột sửa đúng
- 14.0s: toàn bộ bảng biến mất, logo Rikkeisoft và outro-card xuất hiện nổi bật chính giữa
- 20.0s: tl.set({}, {}, 20.0)

**Narration (VO):**
> Để tổng kết, hãy tránh ba lỗi phổ biến: đặt tên bắt đầu bằng số, dùng từ khóa hệ thống, và viết thường từ khóa tru-phôn. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


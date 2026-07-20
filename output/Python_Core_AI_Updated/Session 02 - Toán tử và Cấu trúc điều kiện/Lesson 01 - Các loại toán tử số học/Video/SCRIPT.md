# HyperFrames Script: Session 02 — Lesson 01

**Lesson:** Các loại toán tử số học
**Technology Stack:** python/core
**Total Duration:** 150.0s
**Scene Count:** 4

---

## Scene_01: Tại sao cần toán tử số học?
**Timeline (root):** 0.00s → 30.00s (30.0s)

**Visual:** Màn hình chia đôi: Bên trái hiển thị các biểu thức toán học phức tạp bị gạch xéo đỏ đại diện cho khó khăn khi tính thủ công. Bên phải xuất hiện sơ đồ các bài toán thực tế cần giải quyết: Phân loại Chẵn/Lẻ, Chia trang dữ liệu, và Phép nhân lũy thừa nhanh.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title chuyen len goc trai
- 4.0s: left-problem-panel slide in tu ben trai
- 8.5s: gach cheo mau do de len left-problem-panel
- 12.0s: right-need-panel fade in tung the bang stagger
- 20.0s: highlight cac tu khoa quan trong: Chan/Le, Chia trang, Luy thua
- 30.0s: ket thuc scene

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong lập trình, tính toán là yêu cầu cốt lõi. Ngoài các phép tính cơ bản, làm sao để chia lấy dư phân loại chẵn lẻ, chia lấy nguyên để phân trang, hay tính lũy thừa hiệu suất cao? Hãy cùng tìm hiểu ngay sau đây.

## Scene_02: Hệ thống toán tử trong Python
**Timeline (root):** 30.00s → 70.00s (40.0s)

**Visual:** Bảng tổng hợp toán tử xuất hiện. Cột trái là các ký hiệu toán tử (+, -, *, /, %, //, **). Cột phải hiển thị chức năng tương ứng. Các toán tử đặc biệt (%, //, **) được phóng to và highlight bằng viền neon xanh lá.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.2s: operator-table hien thi tu tu
- 6.0s: hien thi 4 toan tu co ban (+, -, *, /) stagger
- 15.0s: highlight toan tu % (chia lay du) va hien ghi chu ben canh
- 22.0s: highlight toan tu // (chia lay nguyen) va kem vi du nhanh
- 30.0s: highlight toan tu ** (luy thua)
- 40.0s: ket thuc scene

**Narration (VO):**
> Python cung cấp các toán tử số học cơ bản gồm cộng, trừ, nhân, chia. Đặc biệt, ta có toán tử phần trăm để chia lấy dư, hai dấu gạch chéo để chia lấy phần nguyên, và hai dấu sao để thực hiện phép tính lũy thừa một cách nhanh chóng và tối ưu.

## Scene_03: Demo Code & Ép kiểu từ input
**Timeline (root):** 70.00s → 115.00s (45.0s)

**Visual:** Khung soạn thảo Code Editor chứa mã nguồn Python thực thi phép toán. Khi chạy code, màn hình Terminal bên dưới hiện kết quả đầu ra tương ứng. Một cảnh báo nháy sáng nhắc nhở việc ép kiểu int() và float() khi dùng input().

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title chuyen len goc trai
- 4.2s: code-panel slide in tu ben trai
- 10.0s: highlight dong khai bao tong, thuong_thuc, thuong_nguyen
- 18.0s: terminal-panel hien ket qua in ra tung dong tuong ung
- 28.0s: warning-toast bat len voi icon canh bao va dong code minh hoa long ham int(input())
- 45.0s: ket thuc scene

**Narration (VO):**
> Hãy quan sát ví dụ sau. Khi khai báo hai biến a và b, ta dễ dàng tính toán các giá trị tổng, thương thực, thương nguyên, số dư và lũy thừa. Lưu ý, khi nhận dữ liệu từ bàn phím qua hàm input, ta bắt buộc phải ép sang kiểu số nguyên int hoặc số thực float trước khi tính.

## Scene_04: Các lỗi thường gặp & Tổng kết
**Timeline (root):** 115.00s → 150.00s (35.0s)

**Visual:** Hiển thị 3 tấm thẻ cảnh báo lỗi màu đỏ đậm. Thẻ 1: ZeroDivisionError (chia cho 0). Thẻ 2: TypeError (chuỗi + số). Thẻ 3: Sai độ ưu tiên phép tính. Ở cuối scene, các thẻ thu nhỏ lại nhường chỗ cho logo Rikkei Education và lời chào tạm biệt.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: intro-title fade in
- 3.2s: intro-title fade out
- 4.2s: error-card 1 (ZeroDivisionError) xuat hien, highlight chia 0
- 10.0s: error-card 2 (TypeError) xuat hien, highlight loi input string
- 16.0s: error-card 3 (Do uu tien) xuat hien, bieu dien thieu dau ngoac
- 24.0s: 3 error-card bien mat bang cach thu nho scale
- 27.0s: footer-panel gom logo Rikkei Education va thong diep Cam on hien ra o trung tam
- 35.0s: ket thuc scene

**Narration (VO):**
> Khi làm việc với toán tử, hãy tránh ba sai lầm phổ biến: Chia cho số không gây lỗi ZeroDivisionError, quên ép kiểu gây TypeError, và tính sai thứ tự ưu tiên do thiếu dấu ngoặc đơn. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


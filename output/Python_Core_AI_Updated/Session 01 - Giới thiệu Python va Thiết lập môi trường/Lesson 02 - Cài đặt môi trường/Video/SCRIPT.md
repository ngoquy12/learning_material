# HyperFrames Script: Session 01 — Lesson 02

**Lesson:** Cài đặt môi trường
**Technology Stack:** python/core
**Total Duration:** 105.0s
**Scene Count:** 4

---

## Scene_01: Thử thách cài đặt
**Timeline (root):** 0.00s → 25.00s (25.0s)

**Visual:** Màn hình chia đôi. Bên trái hiển thị mô hình cửa sổ màu tối với biểu tượng lỗi PATH đỏ rực cùng thông tin Command not found. Bên phải hiển thị biểu đồ xung đột phiên bản của các package cài đè lên môi trường toàn cục (Global Dependency Conflict).

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set(['#panel-left', '#panel-right', '#scene-main-title'], { autoAlpha: 0, scale: 0.9 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { autoAlpha: 0, scale: 0.9, duration: 0.5, ease: 'power2.in' }, 3.2)
- 4.2s: tl.to('#scene-main-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 4.2)
- 4.8s: tl.to('#scene-main-title', { scale: 0.4, x: -700, y: -450, duration: 0.7, ease: 'power3.inOut' }, 4.8)
- 6.0s: tl.to('#panel-left', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'power3.out' }, 6.0)
- 8.5s: tl.to('#panel-right', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'power3.out' }, 8.5)
- 25.0s: tl.set({}, {}, 25.0)

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay, chúng ta sẽ tìm hiểu cách thiết lập môi trường lập trình Python chuẩn xác. Rào cản lớn nhất của người mới là lỗi biến môi trường PATH và xung đột phiên bản giữa các dự án.

## Scene_02: Giải pháp chuẩn
**Timeline (root):** 25.00s → 50.00s (25.0s)

**Visual:** Màn hình chuyển sang giao diện quy trình hai bước logic. Bước 1 hiển thị mô phỏng bộ cài đặt Python với checkbox 'Add python.exe to PATH' được bật sáng. Bước 2 hiển thị biểu tượng VS Code đi cùng giao diện quản lý Extension Python được cài đặt và kích hoạt thành công.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set(['.step-python-card', '.step-vscode-card'], { autoAlpha: 0, y: 50 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.5s: tl.to('.step-python-card', { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power3.out' }, 4.5)
- 9.0s: tl.to('.step-vscode-card', { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power3.out' }, 9.0)
- 25.0s: tl.set({}, {}, 25.0)

**Narration (VO):**
> Để giải quyết triệt để, chúng ta có quy trình chuẩn: Một là cài đặt Python từ trang chủ và tích chọn Add Python to PATH. Hai là cài đặt VS Code kèm extension Python để tối ưu hóa trình biên dịch mã nguồn.

## Scene_03: Virtual Environment
**Timeline (root):** 50.00s → 80.00s (30.0s)

**Visual:** Màn hình mô phỏng môi trường code thực tế. Phía bên trái hiển thị một khung Terminal gõ dòng lệnh tạo và kích hoạt môi trường ảo. Phía bên phải hiển thị một khung soạn thảo văn bản với đoạn code Python mẫu import sys và platform sáng rõ, kèm kết quả log hệ thống bên dưới.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set(['.terminal-window', '.code-editor-window'], { autoAlpha: 0, scale: 0.95 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.5s: tl.to('.terminal-window', { autoAlpha: 1, scale: 1, duration: 0.5, ease: 'power2.out' }, 4.5)
- 9.5s: tl.to('.code-editor-window', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'power2.out' }, 9.5)
- 30.0s: tl.set({}, {}, 30.0)

**Narration (VO):**
> Tiếp theo, hãy luôn sử dụng môi trường ảo venv để cô lập thư viện cho từng dự án. Đoạn mã sau sẽ giúp kiểm tra thông số hệ điều hành, phiên bản Python và đường dẫn execution hiện tại trên thiết bị của các em.

## Scene_04: Tổng kết lưu ý
**Timeline (root):** 80.00s → 105.00s (25.0s)

**Visual:** Hiển thị dashboard tổng kết gồm 3 thẻ cảnh báo nổi bật màu cam đỏ. Mỗi thẻ biểu thị một sai lầm phổ biến tương ứng với: Quên cấu hình PATH (bị gạch chéo), Môi trường ảo chưa được active (ký hiệu cảnh báo), và Lỗi Policy Windows chặn script.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set(['.warning-card-1', '.warning-card-2', '.warning-card-3'], { autoAlpha: 0, x: -30 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.5s: tl.to(['.warning-card-1', '.warning-card-2', '.warning-card-3'], { autoAlpha: 1, x: 0, duration: 0.5, ease: 'power3.out', stagger: 0.2 }, 4.5)
- 25.0s: tl.set({}, {}, 25.0)

**Narration (VO):**
> Tóm lại, hãy tránh ba sai lầm: quên cấu hình PATH, chưa kích hoạt môi trường ảo, và lỗi phân quyền Execution Policy trên Windows. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


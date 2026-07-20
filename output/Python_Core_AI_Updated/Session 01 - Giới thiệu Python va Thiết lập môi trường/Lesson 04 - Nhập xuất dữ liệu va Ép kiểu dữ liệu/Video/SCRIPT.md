# HyperFrames Script: Session 01 — Lesson 04

**Lesson:** Nhập xuất dữ liệu & Ép kiểu dữ liệu
**Technology Stack:** python/core
**Total Duration:** 80.0s
**Scene Count:** 3

---

## Scene_01: Vấn đề với hàm input()
**Timeline (root):** 0.00s → 25.00s (25.0s)

**Visual:** Màn hình chia đôi. Bên trái hiển thị code nhập liệu không ép kiểu. Bên phải hiển thị kết quả terminal gõ '5' và '10' nhưng in ra chuỗi '510' kèm cảnh báo lỗi logic màu đỏ.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.0s: tl.from('#code-panel', { autoAlpha: 0, x: -50, duration: 0.5 }, 4.0)
- 8.0s: tl.from('#terminal-panel', { autoAlpha: 0, x: 50, duration: 0.5 }, 8.0)
- 12.0s: tl.to('#error-glow', { autoAlpha: 1, scale: 1, duration: 0.4, ease: 'bounce.out' }, 12.0)
- 25.0s: tl.set({}, {}, 25.0)

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay, chúng ta sẽ tìm hiểu về nhập xuất và ép kiểu dữ liệu trong Python. Các em cần lưu ý, hàm input luôn trả về dữ liệu dạng chuỗi, khiến phép toán cộng bị biến thành phép ghép chuỗi sai lệch.

## Scene_02: Quy trình ép kiểu chuẩn
**Timeline (root):** 25.00s → 55.00s (30.0s)

**Visual:** Hiển thị sơ đồ Pipeline: User Input -> Type Casting (int/float) -> Process -> Output. Tiếp theo, hiển thị code mẫu minh họa chuyển chuỗi '25' và '10.5' thành số để cộng ra kết quả 35.5 chính xác.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.0s: tl.to(['.step-1', '.step-2', '.step-3'], { autoAlpha: 1, y: 0, duration: 0.4, stagger: 0.15 }, 4.0)
- 10.0s: tl.from('#code-block-success', { autoAlpha: 0, scale: 0.9, duration: 0.6 }, 10.0)
- 18.0s: tl.to('#result-text', { color: '#3fb950', scale: 1.1, duration: 0.3 }, 18.0)
- 30.0s: tl.set({}, {}, 30.0)

**Narration (VO):**
> Để xử lý chính xác, chúng ta cần ép kiểu dữ liệu bằng các hàm như int hay float. Quy trình chuẩn sẽ là: nhận chuỗi từ người dùng, ép kiểu sang dạng số, tiến hành tính toán số học nâng cao, và dùng hàm print để xuất kết quả hoàn thiện ra màn hình.

## Scene_03: Các sai lầm cần tránh
**Timeline (root):** 55.00s → 80.00s (25.0s)

**Visual:** Bảng tổng hợp 3 sai lầm phổ biến: Lỗi ValueError, nối chuỗi ngoài mong muốn, và ép sai định dạng số thực. Mỗi mục xuất hiện kèm một biểu tượng cảnh báo màu cam/đỏ.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.2s: tl.from('.mistake-card', { autoAlpha: 0, x: -30, duration: 0.5, stagger: 0.2 }, 4.2)
- 12.0s: tl.to('.warning-icon', { keyframes: [{scale: 1.2}, {scale: 1}], duration: 0.3, stagger: 0.1 }, 12.0)
- 25.0s: tl.set({}, {}, 25.0)

**Narration (VO):**
> Khi thực hiện ép kiểu, hãy đặc biệt lưu ý lỗi ValueError khi ép chuỗi chứa chữ sang số, lỗi nối chuỗi ngoài ý muốn, và tránh dùng int cho số thực. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


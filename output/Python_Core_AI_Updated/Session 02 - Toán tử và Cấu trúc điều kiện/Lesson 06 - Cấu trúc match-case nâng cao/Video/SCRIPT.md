# HyperFrames Script: Session 02 — Lesson 06

**Lesson:** Cấu trúc match-case nâng cao
**Technology Stack:** python/core
**Total Duration:** 92.0s
**Scene Count:** 3

---

## Scene_01: Hạn chế của if-elif-else
**Timeline (root):** 0.00s → 30.00s (30.0s)

**Visual:** Màn hình thể hiện sự so sánh logic. Bên trái hiển thị code if-elif-else lồng nhau phức tạp bị gạch đỏ chéo. Bên phải hiển thị biểu đồ rẽ nhánh tối ưu, nhấn mạnh sự tiện dụng của cơ chế pattern matching.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set('#intro-title, #left-box, #right-box, #arrow', { autoAlpha: 0 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut" }, 3.2)
- 4.2s: tl.to('#left-box', { autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }, 4.2)
- 10.0s: tl.to('#right-box', { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 10.0)
- 15.0s: tl.to('#arrow', { autoAlpha: 1, scale: 1, duration: 0.5 }, 15.0)
- 30.0s: tl.set({}, {}, 30.0)

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay, chúng ta sẽ tìm hiểu về cấu trúc match-case nâng cao từ Python 3.10. Trước đây, khi kiểm tra điều kiện phức tạp, các em thường dùng chuỗi if-elif-else dài dòng, cồng kềnh và dễ gây ra lỗi logic. Cấu trúc match-case ra đời để giúp giải quyết triệt để vấn đề này.

## Scene_02: Giải pháp match-case
**Timeline (root):** 30.00s → 62.00s (32.0s)

**Visual:** Một bảng IDE code editor hiển thị trực quan đoạn mã Python thực hiện hàm process_status(status_code). Điểm sáng di chuyển highlight qua từng keyword match, case, và ký tự wildcard gạch dưới.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set('#intro-title, #editor-panel, #highlight-case, #caption', { autoAlpha: 0 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut" }, 3.2)
- 4.2s: tl.to('#editor-panel', { autoAlpha: 1, scale: 1, duration: 0.7, ease: "back.out(1.2)" }, 4.2)
- 12.0s: tl.to('#highlight-case', { autoAlpha: 0.3, duration: 0.5 }, 12.0)
- 18.0s: tl.to('#caption', { autoAlpha: 1, y: 0, duration: 0.5 }, 18.0)
- 32.0s: tl.set({}, {}, 32.0)

**Narration (VO):**
> Hãy cùng xem ví dụ cụ thể này. Bằng cách sử dụng cấu trúc match-case mới, ta có thể so khớp trực tiếp status code một cách ngắn gọn. Ở đây, các case cụ thể như hai trăm, bốn trăm lẻ bốn được liệt kê rõ ràng, giúp mã nguồn tối giản hơn. Ký tự gạch dưới đại diện cho mọi trường hợp còn lại.

## Scene_03: Các lỗi thường gặp
**Timeline (root):** 62.00s → 92.00s (30.0s)

**Visual:** Hiển thị 3 tấm thẻ (warning cards) với biểu tượng cảnh báo màu đỏ/cam. Từng tấm thẻ trượt lên khi giọng đọc nhắc tới nội dung tương thích.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set('#intro-title, #card-1, #card-2, #card-3', { autoAlpha: 0 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut" }, 3.2)
- 4.5s: tl.to('#card-1', { autoAlpha: 1, x: 0, duration: 0.5 }, 4.5)
- 10.0s: tl.to('#card-2', { autoAlpha: 1, x: 0, duration: 0.5 }, 10.0)
- 15.0s: tl.to('#card-3', { autoAlpha: 1, x: 0, duration: 0.5 }, 15.0)
- 30.0s: tl.set({}, {}, 30.0)

**Narration (VO):**
> Trước khi kết thúc, các em cần lưu ý ba điểm quan trọng: luôn đặt wildcard gạch dưới ở cuối cùng, tránh nhầm lẫn gán biến, và chỉ sử dụng từ phiên bản Python 3.10 trở lên để tránh lỗi phiên bản. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


# HyperFrames Script: Session 02 — Lesson 05

**Lesson:** Điều kiện lồng nhau và toán tử ba ngôi
**Technology Stack:** python/core
**Total Duration:** 200.0s
**Scene Count:** 4

---

## Scene_01: Vấn đề: Lồng điều kiện Deep Nesting
**Timeline (root):** 0.00s → 50.00s (50.0s)

**Visual:** Màn hình hiển thị một đoạn code if-else lồng nhau sâu 4-5 cấp tạo thành hình mũi tên chĩa sang phải. Highlight màu đỏ vùng thụt lề sâu (Pyramid of Doom).

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: tl.to('#intro-title-1', {autoAlpha:1, scale:1, duration:0.6}, 0.2)
- 3.2s: tl.to('#intro-title-1', {scale:0.38, x:-760, y:-460, duration:0.7}, 3.2)
- 4.2s: tl.to('#scene-1-content', {autoAlpha:1, y:0, duration:0.8}, 4.2)
- 8.0s: tl.to('#bad-code-card', {autoAlpha:1, scale:1, duration:0.7}, 8.0)
- 15.0s: tl.to('#arrow-highlight', {autoAlpha:1, x:20, duration:0.6}, 15.0)
- 50.0s: tl.set({}, {}, 50.0)

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay, chúng ta sẽ tìm hiểu cách tối ưu hóa các cấu trúc rẽ nhánh phức tạp. Khi viết quá nhiều if-else lồng nhau, mã nguồn sẽ bị đẩy sâu về bên phải, tạo ra cấu trúc Arrow Anti-pattern cực kỳ khó đọc.

## Scene_02: Giải pháp 1: Mệnh đề bảo vệ (Guard Clauses)
**Timeline (root):** 50.00s → 100.00s (50.0s)

**Visual:** Màn hình chuyển sang mô phỏng hoạt động của Guard Clauses. Bên trái là sơ đồ luồng phẳng (flat flow). Bên phải là mã nguồn đã tái cấu trúc sử dụng static guard clauses (if amount <= 0: return 'Invalid amount').

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: tl.to('#intro-title-2', {autoAlpha:1, scale:1, duration:0.6}, 0.2)
- 3.2s: tl.to('#intro-title-2', {scale:0.38, x:-760, y:-460, duration:0.7}, 3.2)
- 4.2s: tl.to('#flat-flow-diagram', {autoAlpha:1, x:0, duration:0.6}, 4.2)
- 8.5s: tl.to('#guard-code-block', {autoAlpha:1, scale:1, duration:0.7}, 8.5)
- 15.0s: tl.to('.highlight-return', {color:'#3fb950', duration:0.5, stagger:0.2}, 15.0)
- 50.0s: tl.set({}, {}, 50.0)

**Narration (VO):**
> Để giải quyết vấn đề này, giải pháp đầu tiên là áp dụng Guard Clauses. Chúng ta sẽ kiểm tra và loại bỏ các điều kiện lỗi ngay ở đầu hàm bằng lệnh return. Kỹ thuật này giúp giải phóng các khối block lồng nhau, đưa mã nguồn về dạng phẳng, dễ dàng theo dõi.

## Scene_03: Giải pháp 2: Toán tử ba ngôi tối ưu
**Timeline (root):** 100.00s → 150.00s (50.0s)

**Visual:** Hiển thị so sánh code trước và sau khi dùng toán tử ba ngôi cho phần return cuối cùng. Đoạn code if amount > 1000: return 'Require approval' else: return 'Approved' được gộp thành return 'Require approval' if amount > 1000 else 'Approved' trên một dòng.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: tl.to('#intro-title-3', {autoAlpha:1, scale:1, duration:0.6}, 0.2)
- 3.2s: tl.to('#intro-title-3', {scale:0.38, x:-760, y:-460, duration:0.7}, 3.2)
- 4.2s: tl.to('#compare-container', {autoAlpha:1, y:0, duration:0.8}, 4.2)
- 9.0s: tl.to('#ternary-code-highlight', {borderColor:'rgba(56,189,248,0.8)', duration:0.5}, 9.0)
- 50.0s: tl.set({}, {}, 50.0)

**Narration (VO):**
> Tiếp theo, với các quyết định trả về kết quả đơn giản ở cuối luồng, ta sử dụng toán tử ba ngôi. Hãy xem ví dụ trực quan trên màn hình. Hàm check payment status được rút gọn tối đa bằng cách kết hợp cả Guard Clauses và toán tử ba ngôi một cách tinh tế.

## Scene_04: Tổng kết: 3 Lỗi cần tránh
**Timeline (root):** 150.00s → 200.00s (50.0s)

**Visual:** Một bảng tổng kết với 3 cảnh báo lớn (được đánh dấu icon cảnh báo màu đỏ/cam). Các điểm text được hiện ra tuần tự dạng stagger.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.2s: tl.to('#intro-title-4', {autoAlpha:1, scale:1, duration:0.6}, 0.2)
- 3.2s: tl.to('#intro-title-4', {scale:0.38, x:-760, y:-460, duration:0.7}, 3.2)
- 4.2s: tl.to('#list-errors', {autoAlpha:1, duration:0.6}, 4.2)
- 6.0s: tl.to('.error-item', {autoAlpha:1, x:0, duration:0.5, stagger:0.3}, 6.0)
- 50.0s: tl.set({}, {}, 50.0)

**Narration (VO):**
> Khi tối ưu rẽ nhánh, hãy đặc biệt tránh ba lỗi: lồng quá ba tầng if-else, lạm dụng toán tử ba ngôi lồng nhau, và quên return trong Guard Clauses. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


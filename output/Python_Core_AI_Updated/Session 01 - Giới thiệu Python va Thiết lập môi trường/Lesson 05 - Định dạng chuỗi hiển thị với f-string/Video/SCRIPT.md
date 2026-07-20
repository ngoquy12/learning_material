# HyperFrames Script: Session 01 — Lesson 05

**Lesson:** Định dạng chuỗi hiển thị với f-string
**Technology Stack:** python/core
**Total Duration:** 210.0s
**Scene Count:** 4

---

## Scene_01: Vấn đề của ghép chuỗi
**Timeline (root):** 0.00s → 50.00s (50.0s)

**Visual:** Màn hình chia đôi. Bên trái hiển thị code ghép chuỗi cổ điển bị gạch chéo đỏ. Bên phải xuất hiện code mẫu f-string sáng xanh hiện đại.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set('#intro-title', { autoAlpha: 0, scale: 0.8 }, 0)
- 0.0s: tl.set('.split-layout', { autoAlpha: 0, y: 50 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.0s: tl.to('.split-layout', { autoAlpha: 1, y: 0, duration: 0.8, ease: 'power3.out' }, 4.0)
- 8.5s: tl.to('.left-panel', { border: '2px solid #f85149', duration: 0.5 }, 8.5)
- 15.0s: tl.to('.right-panel', { border: '2px solid #3fb950', duration: 0.5 }, 15.0)
- 50.0s: tl.set({}, {}, 50.0)

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay chúng ta học cách định dạng chuỗi bằng f-string trong Python. Cách ghép chuỗi cũ bằng dấu cộng hoặc dùng format rất rườm rà, dễ gây lỗi ép kiểu thủ công.

## Scene_02: Cú pháp f-string cơ bản
**Timeline (root):** 50.00s → 100.00s (50.0s)

**Visual:** Màn hình zoom vào cú pháp một dòng code mẫu: print(f'Hello {name}, {age} years old.'). Ký tự 'f' và cặp ngoặc nhọn tương ứng với các biến 'name', 'age' được nhấp nháy làm nổi bật.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set('#intro-title', { autoAlpha: 0, scale: 0.8 }, 0)
- 0.0s: tl.set('.syntax-display', { autoAlpha: 0, scale: 0.95 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.0s: tl.to('.syntax-display', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'power2.out' }, 4.0)
- 10.0s: tl.to('.f-prefix', { scale: 1.3, color: '#ffa657', repeat: 3, yoyo: true, duration: 0.4 }, 10.0)
- 20.0s: tl.to('.variable-tag', { backgroundColor: 'rgba(121,192,255,0.2)', stagger: 0.3, duration: 0.5 }, 20.0)
- 50.0s: tl.set({}, {}, 50.0)

**Narration (VO):**
> Để giải quyết, f-string ra đời. Chúng ta chỉ cần thêm ký tự f trước dấu nháy của chuỗi. Khi đó, mọi biến số hoặc biểu thức nằm trong cặp ngoặc nhọn sẽ tự động được định dạng và hiển thị trực quan.

## Scene_03: Định dạng nâng cao
**Timeline (root):** 100.00s → 155.00s (55.0s)

**Visual:** Khối hiển thị chứa code định dạng gpa và căn lề. Phía dưới hiển thị bảng kết quả Console terminal tương ứng hoạt động của code.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set('#intro-title', { autoAlpha: 0, scale: 0.8 }, 0)
- 0.0s: tl.set('.workbench-layout', { autoAlpha: 0, x: -30 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.0s: tl.to('.workbench-layout', { autoAlpha: 1, x: 0, duration: 0.6, ease: 'power3.out' }, 4.0)
- 12.0s: tl.to('.terminal-box', { borderColor: '#ffa657', duration: 0.5 }, 12.0)
- 30.0s: tl.fromTo('.terminal-box p', { autoAlpha: 0 }, { autoAlpha: 1, stagger: 0.5, duration: 0.4 }, 30.0)
- 55.0s: tl.set({}, {}, 55.0)

**Narration (VO):**
> Ngoài ra, f-string hỗ trợ định dạng nâng cao sau dấu hai chấm. Ví dụ, dấu hai chấm chấm hai f giúp làm tròn số thập phân, hoặc ký tự bé hơn, lớn hơn kết hợp độ rộng giúp định hình căn lề cột dữ liệu.

## Scene_04: 3 Sai lầm cần tránh
**Timeline (root):** 155.00s → 210.00s (55.0s)

**Visual:** Một bảng lớn chứa 3 hàng tương ứng 3 lưu ý quan trọng. Mỗi khi nhắc tới sai lầm nào thì hàng đó phát sáng đỏ, sau đó kết thúc bằng dòng chữ cảm ơn hiện ra ở trung tâm.

**Animation Timeline:**
- 0.0s: tl.set('.clip', { autoAlpha: 1 }, 0)
- 0.0s: tl.set('#intro-title', { autoAlpha: 0, scale: 0.8 }, 0)
- 0.0s: tl.set('.summary-grid', { autoAlpha: 0 }, 0)
- 0.0s: tl.set('.outro-card', { autoAlpha: 0, scale: 0.8 }, 0)
- 0.2s: tl.to('#intro-title', { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 0.2)
- 3.2s: tl.to('#intro-title', { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: 'power3.inOut' }, 3.2)
- 4.0s: tl.to('.summary-grid', { autoAlpha: 1, duration: 0.5 }, 4.0)
- 10.0s: tl.to('.warning-card:nth-child(1)', { border: '1px solid #f85149', backgroundColor: 'rgba(248,81,73,0.1)', duration: 0.4 }, 10.0)
- 18.0s: tl.to('.warning-card:nth-child(2)', { border: '1px solid #f85149', backgroundColor: 'rgba(248,81,73,0.1)', duration: 0.4 }, 18.0)
- 26.0s: tl.to('.warning-card:nth-child(3)', { border: '1px solid #f85149', backgroundColor: 'rgba(248,81,73,0.1)', duration: 0.4 }, 26.0)
- 40.0s: tl.to('.summary-grid', { autoAlpha: 0, duration: 0.5 }, 40.0)
- 41.0s: tl.to('.outro-card', { autoAlpha: 1, scale: 1, duration: 0.8, ease: 'back.out(1.2)' }, 41.0)
- 55.0s: tl.set({}, {}, 55.0)

**Narration (VO):**
> Hãy tránh ba sai lầm: quên viết chữ f, trùng dấu nháy bao ngoài và bên trong biểu thức, và thiếu ký tự nhân đôi ngoặc nhọn khi muốn in trực tiếp chúng. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!


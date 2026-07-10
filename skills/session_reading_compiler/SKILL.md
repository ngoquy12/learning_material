---
name: session_reading_compiler
description: Standardize and compile all lesson-level Interactive Web Visualizers and Playgrounds within a session into a single, unified, interactive dashboard HTML document without JS/CSS namespace conflicts.
---

# Kỹ năng Tổng hợp & Biên dịch Trang Trực quan hóa Toàn bộ Session (Session Interactive Visualizer Compiler Skill)

## 1. Mục tiêu Cốt lõi
Tổng hợp tất cả các Trang Trực quan hóa & Tương tác Động (`reading.html` của từng Lesson) thuộc cùng một Session vào một tệp HTML bảng điều khiển hợp nhất duy nhất (`reading_all.html`).
Tài liệu hợp nhất này đóng vai trò như một **Hệ sinh thái Trực quan hóa Khái niệm toàn diện cho buổi học (Unified Session Interactive Playground)**, cho phép học viên linh hoạt chuyển đổi giữa các bộ Visualizer của từng Lesson mà không gặp xung đột về biến CSS hay Javascript namespace.

---

## 2. Tiêu chuẩn Cấu trúc Trang Hợp nhất (Unified Dashboard Layout)
Tài liệu HTML hợp nhất phải bao gồm:
1. **Header chung & Bộ chuyển hướng Lesson (Session Dashboard Header & Navigation Bar)**:
   - Thanh điều hướng ngang hoặc Tab Selector hiện đại cho phép học viên click chuyển qua lại giữa các Lesson nhanh chóng (ví dụ: `[Lesson 1: Khái niệm & Cơ chế]` | `[Lesson 2: Trực quan hóa Thuật toán]` | `[Lesson 3: Thực hành & Lab]`).
   - Mặc định mở Lesson đầu tiên khi vừa tải trang.
2. **Khối Không gian Trực quan Độc lập (Isolated Visualizer Containers)**:
   - Mỗi Lesson được đặt trong một container có thuộc tính `class="lesson-visualizer-tab"` và `id="lesson-tab-xx"`, sử dụng `display: none;` cho các tab ẩn và `display: block;` cho tab đang kích hoạt.
3. **Quản lý Tài nguyên & Bộ định dạng Trung tâm (Centralized Styling & Scoped Themes)**:
   - Gộp các quy tắc CSS chung (Dark mode, Glassmorphism, Rikkei Brand Colors `#0b1329`, `#6366f1`, `#e2231a`, Bảng điều khiển Control Panel, Code Tracker, Console Log) vào một thẻ `<style>` duy nhất tại `<head>`.
   - Đảm bảo các ID của từng Visualizer (như `canvas-container`, `log-box`, `code-block`, `speed-slider`) được tự động thêm tiền tố riêng theo Lesson (ví dụ: `l1-canvas-container`, `l2-canvas-container`, `l1-log-box`, `l2-log-box`) để tuyệt đối không trùng ID.

---

## 3. Quy tắc Biên dịch & Cô lập JavaScript (JS Namespace Isolation Rules)
Khi gộp các đoạn mã Javascript của từng Lesson vào `reading_all.html`, Compiler bắt buộc phải tuân thủ nguyên tắc cô lập:
1. **Bao gói trong IIFE (Immediately Invoked Function Expression)** hoặc **ES6 Class Namespace**:
   ```javascript
   // Lesson 1 Visualizer Scope
   (function() {
       const lessonId = "lesson-01";
       class Lesson1Visualizer {
           constructor() {
               this.currentStep = 0;
               // attach events to #l1-btn-start, #l1-log-box...
           }
           // ...
       }
       window.lesson1App = new Lesson1Visualizer();
   })();

   // Lesson 2 Visualizer Scope
   (function() {
       const lessonId = "lesson-02";
       class Lesson2Visualizer {
           // attach events to #l2-btn-start, #l2-log-box...
       }
       window.lesson2App = new Lesson2Visualizer();
   })();
   ```
2. **Quản lý Hiệu năng (Performance Management)**:
   - Khi học viên click chuyển sang Lesson tab mới, hệ thống tự động gọi hàm `.pause()` hoặc `clearInterval()` của Visualizer thuộc tab cũ để tránh lãng phí tài nguyên CPU/RAM chạy ngầm các vòng lặp animation không hiển thị.

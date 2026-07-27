---
name: session_reading_compiler
description: Đồng bộ 100% giao diện và nội dung các bài đọc Lesson vào reading_all.html mà không làm sai lệch hay ghi đè CSS đã được duyệt.
---

# Kỹ năng Biên dịch Bài đọc Tổng hợp Session (Session Reading Compiler Skill)

## 1. Nguyên tắc Cốt lõi & Bản chất (Core Principle)

> [!IMPORTANT]
> **QUY TẮC ĐỒNG BỘ 100% BÀI ĐỌC TỔNG HỢP SESSION (`reading_all.html`):**
> Các bài đọc của từng Lesson (`reading.html`) đã được duyệt chuẩn mực 100%. Tệp bài đọc tổng hợp `reading_all.html` **BẮT BUỘC KHÔNG ĐƯỢC GHI ĐÈ CSS CẠNH TRANH (`!important`)** hay thay đổi cấu trúc làm sai lệch format, font chữ, màu sắc, hay chức năng đã được phê duyệt của các bài đọc học liệu.
> 
> **Bản chất `reading_all.html`**:
> Là **Session Master Hub** giúp học viên và giảng viên dễ dàng tra cứu toàn bộ các bài đọc trong Session trên một giao diện tập trung duy nhất, giữ nguyên 100% trải nghiệm gốc của từng bài đọc.

---

## 2. Tiêu chuẩn Kiến trúc & Giao diện

Tài liệu `reading_all.html` được thiết kế theo chuẩn giao diện hiện đại:

1. **Thanh Điều Hướng Sidebar / Tab Selector Bên Trái (Left Navigation Sidebar)**:
   - Liệt kê đầy đủ danh sách bài học (`Lesson 01`, `Lesson 02`, `Lesson 03`...) với số thứ tự và biểu tượng trực quan.
   - Nhấp chọn bài học sẽ lập tức hiển thị bài đọc tương ứng.

2. **Khung Hiển Thị Bài Đọc Nguyên Bản (Pure Isolated Reading Viewport)**:
   - Sử dụng cơ chế nhúng iframe hoặc Scoped Document cách ly 100% không gian CSS/JS cho từng bài đọc (`<iframe class="lesson-viewport" src="Lesson XX.../reading.html"></iframe>`).
   - Đảm bảo 100% các thành phần đã duyệt được giữ nguyên vẹn:
     - **Format & Typography**: Giữ nguyên 100% phông chữ, khoảng cách, màu sắc card và layout.
     - **Pyodide WebAssembly Sandbox**: Nút chạy code tương tác thực thi trực tiếp 100%.
     - **Sơ đồ Mermaid Flowcharts**: Tự động hiển thị dạng đồ họa SVG sắc nét.
     - **Khảo thí & Đánh giá năng lực tự học**: Tự động căn giữa text câu hỏi và đóng/mở câu trả lời mượt mà.

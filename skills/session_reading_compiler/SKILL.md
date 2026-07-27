---
name: session_reading_compiler
description: Đồng bộ 100% giao diện nền trắng hiện đại có Logo Rikkei Education và nội dung bài đọc Lesson vào reading_all.html.
---

# Kỹ năng Biên dịch Bài đọc Tổng hợp Session (Session Reading Compiler Skill)

## 1. Nguyên tắc Cốt lõi & Bản chất (Core Principle)

> [!IMPORTANT]
> **QUY TẮC NỀN TRẮNG & ĐỒNG BỘ 100% BÀI ĐỌC TỔNG HỢP SESSION (`reading_all.html`):**
> 1. **Giao diện Nền Trắng Tươi Sáng & Thương hiệu Rikkei Education**:
>    - Giao diện Master Hub của `reading_all.html` **BẮT BUỘC** dùng tông nền trắng sạch sáng (`#f8fafc` / `#ffffff`), thanh Header chứa **Logo chính thức của Rikkei Education**: `https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png`.
> 2. **Cách ly 100% Không Gian CSS/JS**:
>    - Tệp bài đọc tổng hợp `reading_all.html` **BẮT BUỘC KHÔNG ĐƯỢC GHI ĐÈ CSS CẠNH TRANH (`!important`)** làm sai lệch format, font chữ, màu sắc, hay chức năng đã được phê duyệt của các bài đọc thành phần (`reading.html`).

---

## 2. Tiêu chuẩn Kiến trúc & Giao diện

Tài liệu `reading_all.html` được thiết kế theo chuẩn giao diện thương hiệu doanh nghiệp:

1. **Thanh Header Thương Hiệu (Brand Header Bar)**:
   - Hiển thị **Logo Rikkei Education** (`https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png`) ở góc trái.
   - Tiêu đề Session đậm nét thương hiệu (`font-family: Montserrat`, màu chữ đậm `#0f172a`).

2. **Thanh Điều Hướng Sidebar Bên Trái (Left Navigation Sidebar - Light Theme)**:
   - Nền trắng tinh tế (`#ffffff`), viền chia nhẹ nhàng (`#e2e8f0`).
   - Liệt kê các bài học với Badge số thứ tự màu đỏ thương hiệu Rikkei (`#be111c`).
   - Trạng thái Active: Nền hồng nhạt `rgba(190, 17, 28, 0.08)`, chữ màu đỏ đậm `#be111c`, viền `rgba(190, 17, 28, 0.25)`.

3. **Khung Hiển Thị Bài Đọc Nguyên Bản (Pure Isolated Viewport)**:
   - Sử dụng `<iframe class="lesson-frame" src="Lesson XX.../reading.html"></iframe>` cách ly 100% để hiển thị vẹn nguyên định dạng đã duyệt.

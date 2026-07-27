---
name: session_reading_compiler
description: Đồng bộ 100% giao diện nền trắng hiện đại có Logo Rikkei Education, loại bỏ Header dư thừa và áp dụng vị trí Opacity giúp Mermaid render sắc nét trong reading_all.html.
---

# Kỹ năng Biên dịch Bài đọc Tổng hợp Session (Session Reading Compiler Skill)

## 1. Nguyên tắc Cốt lõi & Bản chất (Core Principle)

> [!IMPORTANT]
> **QUY TẮC NỀN TRẮNG & ĐỒNG BỘ 100% BÀI ĐỌC TỔNG HỢP SESSION (`reading_all.html`):**
> 1. **Giao diện Nền Trắng Tươi Sáng & Thương hiệu Rikkei Education**:
>    - Giao diện Master Hub của `reading_all.html` **BẮT BUỘC** dùng tông nền trắng sạch sáng (`#f8fafc` / `#ffffff`), thanh Header chứa **Logo chính thức của Rikkei Education**: `https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png`.
> 2. **Cơ chế Ẩn/Hiện Opacity Định Vị (Opacity-Based Viewport Positioning)**:
>    - **CẤM DÙNG `display: none` TRÊN CÁC IFRAME BÀI HỌC**: Dùng `display: none` sẽ khiến các bài học bị ẩn không có kích thước bounding box (`getBBox() = 0x0`), làm thư viện Mermaid 10.9.6 bị sập và bắn ra lỗi `Syntax error in text`.
>    - **BẮT BUỘC DÙNG CSS OPACITY & Z-INDEX**:
>      ```css
>      .viewport-panel { flex: 1; height: 100%; background: #ffffff; position: relative; }
>      .lesson-frame { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; opacity: 0; pointer-events: none; z-index: 1; transition: opacity 0.15s ease-in-out; }
>      .lesson-frame.active { opacity: 1; pointer-events: auto; z-index: 10; }
>      ```
> 3. **Tối ưu Loại bỏ Header Dư Thừa (No Redundant Inner Headers)**:
>    - Khi nạp các bài đọc lesson thành phần (`reading.html`) vào `reading_all.html`, **BẮT BUỘC ẨN HOẶC LOẠI BỎ** phần Header riêng của lesson (`#sticky-header`, `header`) để tránh dư thừa trùng lặp với Thanh Header Master duy nhất của Session.
> 4. **Logic JS Thuần Tĩnh (No Auto-Reload / No History Triggers)**:
>    - CẤM dùng `history.replaceState`, `location.hash` hay `localStorage` trong hàm switch tab để tránh kích hoạt cơ chế Hot-Reload của trình duyệt/Live Server.

---

## 2. Tiêu chuẩn Kiến trúc & Giao diện

Tài liệu `reading_all.html` được thiết kế theo chuẩn giao diện thương hiệu doanh nghiệp:

1. **Thanh Header Thương Hiệu Duy Nhất (Single Master Header Bar)**:
   - Hiển thị **Logo Rikkei Education** (`https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png`) ở góc trái.
   - Tiêu đề Session đậm nét thương hiệu (`font-family: Montserrat`, màu chữ đậm `#0f172a`).

2. **Thanh Điều Hướng Sidebar Bên Trái (Left Navigation Sidebar - Light Theme)**:
   - Nền trắng tinh tế (`#ffffff`), viền chia nhẹ nhàng (`#e2e8f0`).
   - Liệt kê các bài học với Badge số thứ tự màu đỏ thương hiệu Rikkei (`#be111c`).
   - Trạng thái Active: Nền hồng nhạt `rgba(190, 17, 28, 0.08)`, chữ màu đỏ đậm `#be111c`, viền `rgba(190, 17, 28, 0.25)`.

3. **Khung Hiển Thị Bài Đọc Nguyên Bản (Pure Isolated Viewport)**:
   - Sử dụng `<iframe class="lesson-frame" src="Lesson XX.../reading.html"></iframe>` cách ly 100% để hiển thị vẹn nguyên định dạng đã duyệt.

---
name: session_reading_compiler
description: Biên dịch bài đọc tổng hợp Session (reading_all.html) bằng cách giữ nguyên 100% nội dung bài đọc của từng Lesson và bổ sung Menu chuyển hướng Sidebar & Session Header.
---

# Kỹ năng Biên dịch Bài đọc Tổng hợp Session (Session Reading Compiler Skill)

## 1. Nguyên tắc Cốt lõi & Bản chất (Core Principle)

> [!IMPORTANT]
> **BẢN CHẤT CỦA BÀI ĐỌC TỔNG HỢP SESSION (`reading_all.html`):**
> Bài đọc tổng hợp cấp Session **bản chất là trích xuất và bảo tồn 100% nội dung gốc (HTML, CSS, JS, Interactive Visualizers, Pyodide Sandbox, Mermaid Diagrams)** của từng tệp `reading.html` thuộc từng Lesson trong Session.
> Tệp hợp nhất **CHỈ THÊM**:
> 1. **Session Header**: Thanh tiêu đề thương hiệu Rikkei Education ở đầu trang.
> 2. **Sidebar / Tab Navigation Menu**: Thanh menu chuyển hướng linh hoạt danh sách bài học bên trái.

---

## 2. Tiêu chuẩn Cấu trúc Trang Hợp nhất (`reading_all.html`)

Tài liệu HTML hợp nhất `reading_all.html` phải được xây dựng theo đúng kiến trúc 3 phần:

### A. Session Header (Thanh Tiêu Đề Cấp Session)
- Hiển thị tên Session, môn học (ví dụ: `Python Core`), số lượng bài học và tiến trình học tập.
- Đặt cố định hoặc nằm ở vị trí đầu trang.

### B. Sidebar / Tab Navigation Menu (Menu Danh Sách Bài Học)
- Thanh menu dính góc bên trái (Sticky Left Sidebar) liệt kê đầy đủ các Bài học (`Lesson 01`, `Lesson 02`, `Lesson 03`...).
- Mỗi nút menu có icon, tiêu đề bài học và chỉ báo trạng thái Active.
- Cho phép học viên click chuyển tab bài học tức thì không cần load lại trang.

### C. Khối Nội dung Bài học Cô lập (Isolated Lesson Tab Containers)
- Mỗi Lesson giữ nguyên 100% cấu trúc HTML body của `reading.html` gốc, được đặt trong container:
  ```html
  <div id="lesson-tab-01" class="lesson-tab-panel" style="display: block;">
      <!-- 100% Nội dung gốc của Lesson 01 reading.html -->
  </div>
  <div id="lesson-tab-02" class="lesson-tab-panel" style="display: none;">
      <!-- 100% Nội dung gốc của Lesson 02 reading.html -->
  </div>
  ```

---

## 3. Quy tắc Cô lập JavaScript & Bảo tồn Styling

1. **Bảo tồn ID & Tiền tố Cô lập (Scoped Element IDs)**:
   - Các ID phần tử trong từng Lesson được gắn tiền tố `lessonX-` (ví dụ `l1-code-editor`, `l2-code-editor`) để tránh đụng độ ID giữa các bài học khi nằm chung trên một DOM tree.
2. **Tự Động Render Sơ Đồ Khái Niệm & Flowchart (Automatic Mermaid Diagram Rendering Engine)**:
   - Tất cả các khối sơ đồ Mermaid (`sequenceDiagram`, `flowchart`, `graph TD`, `classDiagram`) bất kể ở dạng `<div class="mermaid">` hay mã text code blocks **BẮT BUỘC** được tự động nhận diện và chuyển đổi trực tiếp sang đồ họa SVG tương tác trực quan sắc nét.
   - Thêm engine `renderAllMermaidDiagrams()` tự động quét và gọi `mermaid.run()` khi tải trang và khi người dùng chuyển đổi mở rộng các thẻ bài học.

---

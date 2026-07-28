# 📖 BỘ TÀI LIỆU HƯỚNG DẪN 03: BƯỚC 2 - SINH BÀI ĐỌC HTML W3SCHOOLS & MASTER HUB

## 1. 🎯 Mục Đích
Tạo ra các tệp bài đọc `reading.html` theo chuẩn giao diện W3Schools nền sáng hiện đại, tích hợp trình chạy Python trực tiếp trên trình duyệt (Pyodide Wasm Sandbox), sơ đồ Mermaid và các câu hỏi tự đánh giá (Accordion).

---

## 2. 📌 Các Tiêu Chuẩn Bắt Buộc Của Bài Đọc (`reading.html`)

1. **Giao Diện Nền Sáng & Typography**:
   - Sử dụng font chữ Inter & Montserrat cao cấp.
   - Màu sắc chủ đạo: Đỏ thương hiệu Rikkei (`#be111c`).
2. **Trình Chạy Code Trực Tiếp (Pyodide Wasm Sandbox)**:
   - Cho phép học viên nhấn **"▶ Trực quan hóa & Chạy Code"** để thực thi Python ngay trên trình duyệt mà không cần cài đặt.
3. **High-Contrast Dark Mode Code Trackers**:
   - Dòng highlight code sử dụng nền vàng `#fef08a` và màu chữ đen đậm `#0f172a` nổi bật 100%.
4. **Căn Trái Tuyệt Đối Cho Accordion (.selftest-question)**:
   - Các câu hỏi và đáp án tự kiểm tra bắt buộc sử dụng `text-align: left !important;` và `justify-content: flex-start !important;`.
5. **Tiếng Việt Có Dấu Nghêm Ngặt**:
   - Tất cả văn bản, nhãn SVG, node Mermaid phải dùng đúng dấu tiếng Việt (NFC Unicode).

---

## 3. 🛠️ Quy Trình Biên Dịch Master Reading Hub (`reading_all.html`)

Sau khi sinh xong các bài đọc thành phần, `compile_session_html` sẽ gộp toàn bộ thành tệp Master Dashboard:
```bash
python -X utf8 -c "from pathlib import Path; from core.session_compilers import compile_session_html; compile_session_html(Path(r'output/PM_Python/Session 06 - Cấu trúc dữ liệu List va Tuple'), 'Session 06 - Cấu trúc dữ liệu List và Tuple')"
```

### Đặc Điểm Của `reading_all.html`:
- Thanh Header cố định chứa **Logo chính thức Rikkei Education**.
- Sticky Left Sidebar chứa tab chuyển đổi mượt mà giữa các bài học.
- Đạt 100% DOM & JavaScript Isolation Verified.
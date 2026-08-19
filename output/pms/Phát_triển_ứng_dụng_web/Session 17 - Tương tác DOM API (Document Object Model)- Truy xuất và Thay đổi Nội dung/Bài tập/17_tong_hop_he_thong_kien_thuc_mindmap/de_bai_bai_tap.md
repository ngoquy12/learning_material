# Bài tập sơ đồ tư duy mindmap: Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung


## 1. Mục tiêu bài tập
- Hệ thống hóa toàn diện tư duy kiến trúc và cấu trúc luồng dữ liệu của Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung.
- Xây dựng sơ đồ tư duy Markmap / Mermaid trực quan, súc tích, liên kết các nhánh tri thức cốt lõi.
- Hiểu rõ cơ chế biểu diễn tài liệu HTML dưới dạng cây đối tượng (DOM Tree) và quy trình thao tác với các phần tử giao diện bằng JavaScript thuần.

---


## 2. Bối cảnh & Yêu cầu thiết kế Mindmap
- Học viên đóng vai trò Software Architect phân tích và trực quan hóa cấu trúc kiến thức của Session 17.
- Yêu cầu xây dựng sơ đồ dạng cây (Mindmap) bằng cú pháp **Markmap** hoặc **Mermaid** thể hiện đầy đủ 5 nhánh kiến thức bắt buộc.
- Cấu trúc tư duy phải logic, phân cấp từ khái niệm tổng quan đến chi tiết cú pháp, ví dụ minh họa và lưu ý kỹ thuật.

---


## 3. Cấu trúc các nhánh kiến thức bắt buộc


### Nhánh 1: Khái niệm & Vai trò
- **Bản chất DOM Tree**: Cấu trúc cây chứa các đối tượng (Nodes) đại diện cho tài liệu HTML.
- **Phân loại Node**: Document Node, Element Node, Attribute Node, Text Node.
- **Bài toán doanh nghiệp**: Cập nhật giao diện động mà không cần tải lại toàn bộ trang web.
- **Quy định độ dài**: Tối đa 10 từ cho mỗi node.


### Nhánh 2: Cú pháp & Giải nghĩa
- **Truy xuất Element**:
  - `document.getElementById(id)`: Tìm phần tử theo ID duy nhất.
  - `document.querySelector(selector)`: Trả về phần tử đầu tiên khớp với CSS Selector.
  - `document.querySelectorAll(selector)`: Trả về một `NodeList` chứa tất cả phần tử phù hợp.
- **Thay đổi nội dung**:
  - `element.textContent`: Thao tác với văn bản thuần (an toàn, hiệu năng cao).
  - `element.innerHTML`: Thao tác và biên dịch chuỗi thành các thẻ HTML.
- **Thay đổi thuộc tính & Style**:
  - `element.setAttribute(name, value)` / `element.getAttribute(name)`: Thao tác thuộc tính HTML.
  - `element.classList.add()` / `remove()` / `toggle()`: Quản lý danh sách lớp CSS.
  - `element.style.property`: Can thiệp trực tiếp CSS inline.


### Nhánh 3: Ví dụ thực hành
- Viết một đoạn mã nguồn minh họa ngắn gọn (từ 5 đến 8 dòng) thể hiện đầy đủ luồng: **Truy xuất phần tử -> Thay đổi nội dung -> Cập nhật thuộc tính/style**.

*Ví dụ mẫu cho học viên tham khảo:*
```javascript
// Truy xuất phần tử card thông báo
const alertBox = document.querySelector('.alert-message');

// Thay đổi nội dung văn bản và cấu trúc HTML
alertBox.textContent = 'Cập nhật thông tin thành công!';

// Thay đổi thuộc tính và phong cách hiển thị
alertBox.setAttribute('data-status', 'success');
alertBox.classList.add('active');
alertBox.style.backgroundColor = '#d4edda';
```


### Nhánh 4: Lưu ý triển khai / Lỗi thường gặp
- **Lỗi Script Blocking**: Thao tác khi cây DOM chưa hoàn tất render (thiếu thẻ `defer` hoặc đặt thẻ `<script>` sai vị trí).
- **Lỗi Bảo mật XSS**: Dùng `innerHTML` để chèn dữ liệu chưa qua kiểm duyệt từ người dùng.
- **Nhầm lẫn Static vs Live Collection**: Phân biệt `NodeList` (tĩnh từ `querySelectorAll`) và `HTMLCollection` (động từ `getElementsByClassName`).
- **Lỗi ghi đè Class**: Dùng `className` gây đè mất các lớp cũ thay vì sử dụng `classList`.


### Nhánh 5: Liên kết hệ thống
- **Luồng dữ liệu**: `HTML File` $\rightarrow$ `DOM Tree Construction` $\rightarrow$ `JS Selector (Query)` $\rightarrow$ `DOM Modification` $\rightarrow$ `Browser Reflow/Repaint` $\rightarrow$ `User Interface`.

---


## 4. Quy chuẩn định dạng & Nộp bài
- **Định dạng nộp bài**: File Markdown (.md) chứa khối mã cú pháp ```markmap hoặc ```mermaid mindmap.
- **Quy định súc tích**: Mỗi node lá không quá 15 từ, không viết đoạn văn dài dòng.
- **Cấu trúc phân cấp**: Chuẩn hóa từ Node trung tâm $\rightarrow$ 5 Nhánh chính $\rightarrow$ Các Nhánh con.

---


## 5. Checklist đánh giá sơ đồ tư duy
- [ ] Thể hiện đầy đủ 5 nhánh cấu trúc tri thức bắt buộc.
- [ ] Cú pháp mã nguồn trong ví dụ hoàn toàn chính xác theo javascript/web.
- [ ] Không chứa các kiến thức ngoài phạm vi cho phép (Không dùng Event Listeners, Form submit, Fetch API, LocalStorage).
- [ ] Các lưu ý lỗi thường gặp thực tế, chuẩn kỹ thuật.
- [ ] Tuân thủ giới hạn độ dài node (< 15 từ/node), bố cục rõ ràng, dễ nhìn.
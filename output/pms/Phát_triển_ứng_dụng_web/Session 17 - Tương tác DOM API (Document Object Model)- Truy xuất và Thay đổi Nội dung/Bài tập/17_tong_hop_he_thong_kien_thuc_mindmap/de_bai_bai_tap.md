# Bài tập sơ đồ tư duy mindmap: Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung


## 1. Mục tiêu bài tập
- Hệ thống hóa toàn diện tư duy kiến trúc và cấu trúc luồng dữ liệu của **Tương tác DOM API (Document Object Model) - Truy xuất và Thay đổi Nội dung**.
- Xây dựng sơ đồ tư duy Markmap / Mermaid trực quan, súc tích, liên kết các nhánh tri thức cốt lõi.

---


## 2. Bối cảnh & Yêu cầu thiết kế Mindmap
- Học viên đóng vai trò **Software Architect** phân tích và trực quan hóa cấu trúc kiến thức của Session 17.
- Yêu cầu xây dựng sơ đồ dạng cây (Mindmap) thể hiện đầy đủ **5 nhánh kiến thức bắt buộc**, phản ánh chính xác cơ chế hoạt động của DOM Tree, kỹ thuật truy xuất và thao tác sửa đổi nội dung/thuộc tính HTML bằng JavaScript thuần.

---


## 3. Cấu trúc các nhánh kiến thức bắt buộc


### 1. Khái niệm & Vai trò (Mindmap Node 1)
- **Bản chất DOM Tree**: Cấu trúc cây đối tượng hóa toàn bộ văn bản HTML trong bộ nhớ.
- **Node loại**: Document Node, Element Node, Attribute Node, Text Node.
- **Bài toán doanh nghiệp**: Cho phép JavaScript can thiệp động vào giao diện client mà không cần reload trang.


### 2. Cú pháp & Giải nghĩa (Mindmap Node 2)
- **Truy xuất Element**:
  - `document.getElementById(id)`: Truy vấn theo ID duy nhất, trả về 1 Element hoặc `null`.
  - `document.querySelector(selector)`: Truy vấn theo CSS Selector, trả về Element đầu tiên khớp.
  - `document.querySelectorAll(selector)`: Truy vấn theo CSS Selector, trả về danh sách NodeList (tĩnh).
- **Thay đổi Nội dung**:
  - `element.innerText`: Đọc/ghi văn bản hiển thị (tính đến CSS `display: none`).
  - `element.textContent`: Đọc/ghi toàn bộ văn bản thô (bỏ qua định dạng CSS).
  - `element.innerHTML`: Đọc/ghi cấu trúc mã HTML bên trong Element.
- **Thay đổi Thuộc tính & Style**:
  - `element.getAttribute(attr)` / `element.setAttribute(attr, value)`: Thao tác trực tiếp với thuộc tính HTML.
  - `element.classList.add()` / `.remove()` / `.toggle()`: Quản lý các lớp CSS linh hoạt.
  - `element.style.property`: Thay đổi CSS Inline trực tiếp.


### 3. Ví dụ thực hành (Mindmap Node 3)
```javascript
// Truy xuất element tiêu đề và card thông tin
const titleNode = document.querySelector('#main-title');
const cardNode = document.querySelector('.card-item');

// Cập nhật nội dung và thuộc tính CSS
titleNode.textContent = 'Khóa học Lập trình Web Fullstack';
titleNode.style.color = '#0056b3';

// Thao tác với class và thuộc tính dữ liệu
cardNode.classList.add('active');
cardNode.setAttribute('data-status', 'processed');
```


### 4. Lưu ý triển khai / Lỗi thường gặp (Mindmap Node 4)
- **Lỗi `TypeError: Cannot read properties of null`**: Do chạy script truy xuất DOM trước khi HTML được parse xong.
- **Nguy cơ bảo mật XSS**: Dùng `innerHTML` để chèn dữ liệu chưa qua lọc từ người dùng.
- **Nhầm lẫn `NodeList` với `Array`**: `querySelectorAll` trả về `NodeList`, không có sẵn các hàm `map`, `filter` của Array (cần chuyển đổi bằng `Array.from()` hoặc Spread Operator).
- **Ghi đè class bằng `className`**: Dùng `className = 'new-class'` sẽ xóa toàn bộ class cũ thay vì dùng `classList.add()`.


### 5. Liên kết hệ thống (Mindmap Node 5)
- **Luồng xử lý kiến trúc**: 
  `HTML Document`  `DOM Parser (Browser Engine)`  `DOM Tree in Memory`  `JavaScript Execution (Query & Mutate)`  `Reflow / Repaint`  `Updated View (UI)`.

---


## 4. Quy chuẩn định dạng & Nộp bài
- **Định dạng nộp bài**: File Markdown (`.md`) chứa cú pháp ```markmap hoặc ```mermaid mindmap.
- **Quy định súc tích**: 
  - Mỗi node lá không quá 15 từ.
  - Tuyệt đối không viết thành các đoạn văn dài dòng.
  - Đảm bảo tính phân cấp phân nhánh rõ ràng (Gốc  Nhánh chính  Nhánh phụ  Chi tiết).

---


## 5. Checklist đánh giá sơ đồ tư duy

- [ ] Thể hiện đầy đủ 5 nhánh cấu trúc tri thức bắt buộc.
- [ ] Cú pháp mã nguồn trong ví dụ hoàn toàn chính xác theo JavaScript / DOM API chuẩn.
- [ ] Các lưu ý lỗi thường gặp thực tế, đúng trọng tâm (null pointer, XSS, NodeList vs Array).
- [ ] Tuân thủ giới hạn độ dài node (< 15 từ/node), bố cục rõ ràng, dễ nhìn.
- [ ] Không chứa các kiến thức nằm ngoài phạm vi bài học (Event Listeners, Form Submit, Fetch API, LocalStorage).
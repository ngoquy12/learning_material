# Bài tập sơ đồ tư duy mindmap: Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung


## 1. Mục tiêu bài tập
- Hệ thống hóa toàn diện tư duy kiến trúc và cấu trúc luồng dữ liệu của Tương tác DOM API (Document Object Model) - Truy xuất và Thay đổi Nội dung.
- Xây dựng sơ đồ tư duy Markmap / Mermaid trực quan, súc tích, liên kết các nhánh tri thức cốt lõi.


## 2. Bối cảnh & Yêu cầu thiết kế Mindmap
- Học viên đóng vai trò Software Architect phân tích và trực quan hóa cấu trúc kiến thức của Session.
- Yêu cầu xây dựng sơ đồ dạng cây (Mindmap) thể hiện đầy đủ 5 nhánh kiến thức bắt buộc.


## 3. Cấu trúc các nhánh kiến thức bắt buộc


### 1. Khái niệm & Vai trò
- **Bản chất DOM Tree**: Cấu trúc cây phân cấp đại diện cho tài liệu HTML trong bộ nhớ RAM.
- **Node & Element**: Mỗi thẻ HTML, thuộc tính, đoạn văn bản đều là một Node.
- **Bài toán doanh nghiệp**:
  - Tương tác giao diện động trực tiếp trên trình duyệt.
  - Cập nhật dữ liệu thời gian thực cho người dùng không cần reload trang.
  - Tối ưu trải nghiệm người dùng (UX) thông qua việc điều khiển DOM linh hoạt.


### 2. Cú pháp & Giải nghĩa
- **Phương thức truy xuất Element**:
  - `document.getElementById('id')`: Truy xuất 1 element duy nhất qua ID.
  - `document.querySelector('selector')`: Truy xuất element đầu tiên khớp với CSS Selector.
  - `document.querySelectorAll('selector')`: Trả về một `NodeList` chứa tất cả element khớp selector.
  - `document.getElementsByClassName('class')`: Trả về `HTMLCollection` các element chứa class.
- **Phương thức thao tác Nội dung**:
  - `element.innerHTML`: Lấy hoặc ghi đè nội dung bao gồm cả thẻ HTML.
  - `element.innerText`: Lấy hoặc ghi đè văn bản nhìn thấy được (phụ thuộc CSS display).
  - `element.textContent`: Lấy hoặc ghi đè toàn bộ văn bản thô (bỏ qua CSS).
- **Phương thức thao tác Thuộc tính & Style**:
  - `element.getAttribute('attr')` / `element.setAttribute('attr', 'value')`: Đọc và ghi thuộc tính HTML.
  - `element.classList.add()` / `remove()` / `toggle()`: Thao tác danh sách class CSS.
  - `element.style.propertyName`: Thay đổi inline CSS trực tiếp (dùng kiểu camelCase, ví dụ: `backgroundColor`).


### 3. Ví dụ thực hành
```javascript
// Ví dụ thực hành thao tác DOM chuẩn
const titleEl = document.querySelector('#main-title');
const cardEl = document.querySelector('.card');

titleEl.textContent = 'Tiêu đề đã được cập nhật!';
cardEl.setAttribute('data-status', 'active');
cardEl.classList.add('highlight');
cardEl.style.backgroundColor = '#f0f0f0';
```


### 4. Lưu ý triển khai / Lỗi thường gặp
- **Lỗi Null Reference (`Cannot read properties of null`)**: Truy xuất element trước khi DOM được tải xong (do đặt thẻ `<script>` sai vị trí).
- **Nguy cơ bảo mật XSS với `innerHTML`**: Chèn chuỗi chứa mã độc HTML/JS từ nguồn dữ liệu không tin cậy.
- **Nhầm lẫn `NodeList` và `HTMLCollection`**: `NodeList` hỗ trợ `forEach`, còn `HTMLCollection` là tập hợp động không có `forEach` mặc định.
- **Lạm dụng `style` inline**: Làm khó quản lý CSS; khuyến khích dùng `classList` để quản lý giao diện.


### 5. Liên kết hệ thống
- **Luồng xử lý từ Code đến Giao diện**:
  `HTML/CSS Source Code`  `Trình duyệt Parser`  `DOM Tree & CSSOM Tree`  `JS Engine Query & Mutate DOM`  `Render Tree Update`  `Re-layout & Repaint`  `Hiển thị trên màn hình`.

---


## 4. Quy chuẩn định dạng & Nộp bài
- Định dạng nộp bài: File Markdown chứa cú pháp ```markmap hoặc ```mermaid mindmap.
- Quy định súc tích: Mỗi node lá không quá 15 từ, không viết văn bản dài dòng.


### Gợi ý mẫu khung Markmap cho học viên:
```markmap

# DOM API - Truy xuất & Thay đổi Nội dung

## 1. Khái niệm & Vai trò
- DOM Tree: Cấu trúc cây đối tượng đại diện HTML trong RAM
- Node: Mọi phần tử HTML, thuộc tính, text đều là Node
- Bài toán: Cập nhật giao diện động không cần reload trang

## 2. Cú pháp & Giải nghĩa
- Truy xuất Element
  - document.getElementById('id'): Lấy 1 element theo ID
  - document.querySelector('selector'): Lấy element đầu tiên khớp CSS Selector
  - document.querySelectorAll('selector'): Trả về NodeList chứa các element khớp
- Thay đổi Nội dung
  - element.innerHTML: Đọc/ghi cả thẻ HTML
  - element.innerText: Đọc/ghi text nhìn thấy được
  - element.textContent: Đọc/ghi toàn bộ text thô
- Thuộc tính & Style
  - setAttribute/getAttribute: Thao tác thuộc tính HTML
  - classList.add()/remove(): Thêm hoặc xóa class CSS
  - element.style.property: Can thiệp trực tiếp inline style

## 3. Ví dụ thực hành
- Code JS minh họa
  - Truy xuất element qua querySelector
  - Cập nhật textContent và classList
  - Thay đổi thuộc tính inline style

## 4. Lưu ý & Lỗi thường gặp
- Lỗi Null Reference: Script chạy trước khi DOM parse xong
- Nguy cơ XSS: Dùng innerHTML nhận dữ liệu không an toàn
- Nhầm lẫn NodeList với Array thuần
- Lạm dụng inline style thay vì classList

## 5. Liên kết hệ thống
- HTML Source -> Parser -> DOM Tree
- JS Mutate DOM -> Render Tree Re-layout -> Screen Display
```

---


## 5. Checklist đánh giá sơ đồ tư duy
- [ ] Thể hiện đầy đủ 5 nhánh cấu trúc tri thức bắt buộc.
- [ ] Cú pháp mã nguồn trong ví dụ hoàn toàn chính xác theo JavaScript/Web.
- [ ] Không sử dụng các phần kiến thức thuộc phạm vi bị cấm (Event Listeners, Form submit, Fetch API, LocalStorage).
- [ ] Các lưu ý lỗi thường gặp thực tế, chuẩn kỹ thuật (Null reference, XSS, NodeList).
- [ ] Tuân thủ giới hạn độ dài node (< 15 từ/node), bố cục rõ ràng, dễ nhìn.
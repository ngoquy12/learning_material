# Bài tập sơ đồ tư duy mindmap: Xử lý Sự kiện Người dùng (Event Handling) và Sự kiện Form Input


## 1. Mục tiêu bài tập
- Hệ thống hóa toàn diện tư duy kiến trúc và cấu trúc luồng dữ liệu của Xử lý Sự kiện Người dùng (Event Handling) và Sự kiện Form Input trong JavaScript.
- Xây dựng sơ đồ tư duy Markmap / Mermaid trực quan, súc tích, liên kết các nhánh tri thức cốt lõi từ cơ chế lắng nghe sự kiện đến xử lý dữ liệu biểu mẫu (Form).


## 2. Bối cảnh & Yêu cầu thiết kế Mindmap
- **Bối cảnh**: Bạn đóng vai trò là một Software Architect đang chuẩn bị tài liệu kỹ thuật chuẩn hóa để hướng dẫn lập trình viên Frontend nắm vững cơ chế tương tác người dùng trên giao diện web.
- **Yêu cầu**: Xây dựng một sơ đồ tư duy dạng cây (Mindmap) thể hiện đầy đủ 5 nhánh kiến thức bắt buộc. Sơ đồ phải trực quan hóa toàn bộ luồng xử lý từ lúc người dùng phát sinh hành động cho đến khi giao diện phản hồi.

---


## 3. Cấu trúc các nhánh kiến thức bắt buộc

Sơ đồ tư duy cần được trình bày chi tiết theo 5 nhánh chính dưới đây:


### Nhánh 1: Khái niệm & Vai trò
- **Bản chất Event Handling**: Cơ chế lắng nghe và phản hồi lại các tương tác từ người dùng (click, gõ phím, di chuột).
- **Bài toán giải quyết**: Giúp trang web tĩnh trở nên tương tác động, phản hồi tức thì với hành vi người dùng.
- **Vai trò của Form Event**: Kiểm soát toàn bộ quá trình thu thập, kiểm tra (validate) và xử lý dữ liệu đầu vào trước khi chuyển giao.


### Nhánh 2: Cú pháp & Giải nghĩa
- **Cú pháp `addEventListener`**: `target.addEventListener(type, listener)`
  - `target`: Element DOM muốn gán sự kiện.
  - `type`: Chuỗi tên sự kiện (`'click'`, `'submit'`, `'input'`, `'change'`).
  - `listener`: Callback function thực thi khi sự kiện kích hoạt.
- **Đối tượng Event (`e` / `event`)**: Tự động truyền vào callback, chứa thông tin chi tiết về sự kiện.
- **Phương thức `e.preventDefault()`**: Ngăn chặn hành vi mặc định của trình duyệt (ví dụ: ngăn reload trang khi submit form, ngăn chuyển trang khi click link).
- **Thuộc tính `e.target.value`**: Truy xuất giá trị tức thời từ các ô nhập liệu (`<input>`, `<select>`, `<textarea>`).


### Nhánh 3: Ví dụ thực hành
Cung cấp đoạn mã nguồn chuẩn hóa (5-8 dòng) xử lý sự kiện `submit` của Form:

```javascript
const loginForm = document.querySelector('#loginForm');
loginForm.addEventListener('submit', function(e) {
  e.preventDefault();
  const username = document.querySelector('#username').value.trim();
  if (username === '') {
    alert('Tên đăng nhập không được để trống!');
  } else {
    console.log('Dữ liệu hợp lệ:', username);
  }
});
```


### Nhánh 4: Lưu ý triển khai / Lỗi thường gặp
- **Lỗi thực thi hàm ngay lập tức**: Truyền `fn()` thay vì `fn` vào `addEventListener` khiến callback chạy ngay khi gán sự kiện.
- **Quên `e.preventDefault()` trong Form**: Khiến trang web bị tải lại (reload), làm mất dữ liệu tạm thời trên giao diện.
- **Nhầm lẫn giữa sự kiện `input` và `change`**:
  - `input`: Kích hoạt ngay lập tức khi giá trị thay đổi (mỗi ký tự gõ vào).
  - `change`: Chỉ kích hoạt khi giá trị thay đổi và element mất focus (blur).
- **Rò rỉ bộ nhớ (Memory Leak)**: Không gỡ bỏ sự kiện (`removeEventListener`) khi các DOM element bị xóa khỏi giao diện.


### Nhánh 5: Liên kết hệ thống
- **Luồng dữ liệu sự kiện thông thường**:
  `Người dùng tương tác`  `Trình duyệt phát sự kiện`  `Event Listener bắt sự kiện`  `Callback Function xử lý`  `Cập nhật DOM/UI`.
- **Luồng xử lý Form Input & Submit**:
  `Người dùng nhập dữ liệu`  `Sự kiện input/change kiểm tra dữ liệu (Validate)`  `Người dùng bấm Submit`  `Sự kiện submit kích hoạt`  `Ngăn reload bằng preventDefault()`  `Trích xuất dữ liệu & Phản hồi UI`.

---


## 4. Quy chuẩn định dạng & Nộp bài

- **Định dạng nộp bài**: Sử dụng mã Markdown chứa khối cú pháp ```markmap hoặc ```mermaid mindmap.
- **Quy định độ dài**: Mỗi node lá (leaf node) không được vượt quá **15 từ**, ngắn gọn, đi thẳng vào bản chất kỹ thuật, tuyệt đối không viết văn bản dài dòng.


### Gợi ý mẫu khung Markmap:

```markmap

# Session 19: Event Handling & Form Input


## 1. Khái niệm & Vai trò

### Bản chất: Lắng nghe và phản hồi tương tác người dùng

### Bài toán: Tăng tính tương tác động cho trang web

### Form Event: Kiểm soát dữ liệu nhập và xác thực trước khi gửi


## 2. Cú pháp & Giải nghĩa

### addEventListener(type, listener)

#### target: DOM Element nhận sự kiện

#### type: Tên sự kiện ('click', 'submit', 'input')

#### listener: Hàm callback xử lý logic

### Event Object (e)

#### e.preventDefault(): Ngăn hành vi mặc định trình duyệt

#### e.target.value: Lấy dữ liệu từ ô input


## 3. Ví dụ thực hành

### Form Submit Handling

#### Snippet: e.preventDefault() & Validate dữ liệu input


## 4. Lưu ý triển khai / Lỗi thường gặp

### Lỗi truyền fn(): Gọi hàm ngay khi đăng ký sự kiện

### Quên preventDefault: Làm reload trang và mất dữ liệu form

### Phân biệt input/change: input bắt tức thì, change bắt khi blur

### Memory Leak: Cần removeEventListener khi xóa DOM


## 5. Liên kết hệ thống

### Luồng Event: User Action -> Event -> Listener -> UI Update

### Luồng Form: Input -> Validate -> Submit -> preventDefault -> Update UI
```

---


## 5. Checklist đánh giá sơ đồ tư duy

Học viên tự kiểm tra sản phẩm sơ đồ tư duy trước khi nộp theo các tiêu chí sau:

- [ ] **Đầy đủ cấu trúc**: Thể hiện chính xác 5 nhánh tri thức bắt buộc không thiếu nhánh nào.
- [ ] **Tính chính xác kỹ thuật**: Cú pháp mã nguồn JavaScript và các sự kiện (`submit`, `input`, `change`, `preventDefault`) hoàn toàn chính xác.
- [ ] **Tính thực tiễn**: Phản ánh đúng các lỗi kinh điển (reload trang, gọi nhầm hàm) và đưa ra cách phòng tránh chuẩn.
- [ ] **Tuân thủ quy chuẩn hình thức**: Mỗi node lá không quá 15 từ, sử dụng đúng cú pháp Markdown (Markmap/Mermaid), bố cục phân cấp rõ ràng, dễ đọc.
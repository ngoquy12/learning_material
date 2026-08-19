# Đối tượng (Object) trong JavaScript, Cấu trúc JSON và Thao tác CRUD

## Lesson 01 — Khái niệm Object Literal (Key-Value)

### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Cấu trúc dữ liệu lưu trữ dưới dạng các cặp key-value.
- Vai trò: Gom nhóm thông tin và mô tả đối tượng thực tế một cách logic.

### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:

```javascript
  const objectName = {
    keyName: value,
    "special-key": value
  };
```

- Giải thích thành phần:
  - `keyName`: Tên thuộc tính, tuân thủ quy tắc đặt tên camelCase.
  - `special-key`: Key chứa ký tự đặc biệt, cần bọc trong dấu ngoặc kép.
  - `value`: Giá trị của thuộc tính, chấp nhận mọi kiểu dữ liệu trong JavaScript.

### Ví dụ thực hành
- Kịch bản áp dụng: Khai báo thông tin khóa học và thực hành truy cập thuộc tính.

```javascript
  const courseData = {
    id: "FE-2026",
    courseName: "Lập trình Web Frontend Enterprise",
    durationMonths: 6,
    "teacher-name": "Nguyễn Văn B"
  };
  console.log(courseData.courseName);
  console.log(courseData["teacher-name"]);
  const targetProperty = "durationMonths";
  console.log(courseData[targetProperty]);
```

- Giải thích ví dụ: Sử dụng Dot Notation cho key chuẩn và Bracket Notation cho key động hoặc chứa ký tự đặc biệt.

### Lưu ý triển khai
- **Truy cập sai biến trong Bracket Notation**: Thiếu ngoặc nháy khiến JavaScript hiểu lầm key là biến chưa khai báo và gây lỗi ReferenceError.
- **Lưu ý định dạng**: Thống nhất dùng camelCase cho tên thuộc tính chuẩn và dùng Dot Notation để mã nguồn sạch đẹp.

## Lesson 02 — Thao tác Thêm, Sửa, Xóa Thuộc tính Object và Cấu trúc JSON

### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Thao tác cập nhật thuộc tính đối tượng và chuyển đổi với chuỗi JSON.
- Vai trò: Quản lý vòng đời dữ liệu và trao đổi dữ liệu chuẩn hóa với Server.

### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:

```javascript
  // Thêm mới hoặc cập nhật thuộc tính
  objectName.keyName = newValue;

  // Xóa thuộc tính khỏi đối tượng
  delete objectName.keyName;

  // Chuyển đổi dữ liệu JSON
  const jsonString = JSON.stringify(objectName);
  const parsedObject = JSON.parse(jsonString);
```

- Giải thích thành phần:
  - `delete`: Toán tử loại bỏ hoàn toàn cặp key-value khỏi bộ nhớ đối tượng.
  - `JSON.stringify()`: Đóng gói đối tượng JavaScript thành chuỗi JSON dạng string.
  - `JSON.parse()`: Giải mã chuỗi JSON hợp lệ về lại đối tượng JavaScript ban đầu.

### Ví dụ thực hành
- Kịch bản áp dụng: Quản lý tài khoản người dùng, loại bỏ mật khẩu và đóng gói JSON.

```javascript
  const userProfile = {
    id: "USR_101",
    username: "nguyenvana",
    password: "super_secret_123"
  };
  userProfile.email = "vana@rikkei.edu.vn";
  userProfile["shipping-address"] = "Số 10 Trần Phú, Hà Nội";
  delete userProfile.password;

  const jsonPayload = JSON.stringify(userProfile);
  const restoredUser = JSON.parse(jsonPayload);
  console.log(restoredUser.username);
```

- Giải thích ví dụ: Thêm thông tin liên hệ, xóa trường nhạy cảm password trước khi đóng gói gửi đi.

### Lưu ý triển khai
- **Gán giá trị undefined thay vì xóa**: Việc gán undefined không loại bỏ key khỏi đối tượng, gây lãng phí bộ nhớ.
- **Truy cập thuộc tính trên chuỗi JSON**: Không thể dùng Dot Notation trực tiếp trên chuỗi JSON khi chưa thực hiện parse.

## Liên kết hệ thống
- Mối quan hệ logic: Lesson 01 định hình cấu trúc dữ liệu Object ban đầu; Lesson 02 cung cấp kỹ thuật biến đổi dữ liệu và chuẩn hóa thành JSON.
- Luồng dữ liệu xuyên suốt: Đóng gói thông tin đối tượng (Lesson 01) -> Cập nhật/Xóa thuộc tính và chuyển đổi JSON (Lesson 02).
- Ứng dụng tổng hợp: Quản lý trạng thái dữ liệu ứng dụng Web, làm sạch thông tin và truyền nhận dữ liệu qua API.

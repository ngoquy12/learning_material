# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript
vanilla (es6+), html5
function processUserProfile(rawUser, updateOptions) {
    let user = { ...rawUser };

    if (updateOptions.sanitize) {
        delete user.password;
    }

    if (updateOptions.dynamicField) {
        user[updateOptions.dynamicField.key] = updateOptions.dynamicField.value;
    }

    if (updateOptions.isVip) {
        user.role = "VIP";
    }

    const jsonString = JSON.stringify(user);
    const restoredObj = JSON.parse(jsonString);

    return {
        jsonLength: jsonString.length,
        hasPassword: "password" in restoredObj,
        userRole: restoredObj.role || "GUEST",
        keysCount: Object.keys(restoredObj).length
    };
}
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X): Nếu truyền vào hàm processUserProfile() dữ liệu đầu vào bao gồm: rawUser = { id: "U101 username: "nam_rikkei password: "secret123" } và updateOptions = { sanitize: true, dynamicField: { key: "phone value: "0912345678" }, isVip: true }, hãy chỉ ra các thuộc tính tồn tại trong restoredObj và kết quả trả về của hàm.
> **Gợi ý trả lời & Định hướng đáp án:**
> Chi tiết từng bước thực thi:
> 1. Khởi tạo user bằng cách sao chép rawUser: { id: "U101 username: "nam_rikkei password: "secret123" }.
> 2. Do updateOptions.sanitize = true -> câu lệnh 'delete user.password' được kích hoạt, xóa thuộc tính password khỏi object. Lúc này user còn: { id: "U101 username: "nam_rikkei" }.
> 3. Do updateOptions.dynamicField tồn tại -> câu lệnh 'user["phone"] = "0912345678"' bổ sung thuộc tính phone. Lúc này user gồm: { id: "U101 username: "nam_rikkei phone: "0912345678" }.
> 4. Do updateOptions.isVip = true -> câu lệnh 'user.role = "VIP"' thêm thuộc tính role. Lúc này user gồm: { id: "U101 username: "nam_rikkei phone: "0912345678 role: "VIP" }.
> 5. Chuỗi JSON được đóng gói và khôi phục thành restoredObj với đúng 4 thuộc tính trên.
> 6. Kết quả hàm trả về:
>    - hasPassword: false (do password đã bị delete).
>    - userRole: "VIP".
>    - keysCount: 4 (gồm id, username, phone, role).

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y): Nếu thay đổi tham số truyền vào thành: rawUser = { id: "U102 username: "hoa_le password: "myPassword123" } và updateOptions = { sanitize: false, dynamicField: null, isVip: false }, luồng xử lý sẽ diễn ra như thế nào và các giá trị hasPassword, userRole, keysCount thu được là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> Chi tiết luồng thực thi với dữ liệu thay đổi:
> 1. Khởi tạo user: { id: "U102 username: "hoa_le password: "myPassword123" }.
> 2. updateOptions.sanitize = false -> Khối if (updateOptions.sanitize) bị bỏ qua, thuộc tính password vẫn còn giữ nguyên.
> 3. updateOptions.dynamicField = null (falsy) -> Khối if (updateOptions.dynamicField) không chạy, không thêm thuộc tính động.
> 4. updateOptions.isVip = false -> Khối if (updateOptions.isVip) không chạy, không thêm thuộc tính role.
> 5. Đóng gói JSON.stringify() và giải mã JSON.parse() tạo ra restoredObj giữ nguyên 3 thuộc tính ban đầu (id, username, password).
> 6. Kết quả hàm trả về:
>    - hasPassword: true (do toán tử 'in' tìm thấy key "password").
>    - userRole: "GUEST" (do restoredObj.role là undefined, phép toán || lấy giá trị mặc định "GUEST").
>    - keysCount: 3 (gồm id, username, password).

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Cho dữ liệu đầu vào rawUser = { id: "U103 username: "binh_tran password: "pass123" }. Để hàm trả về kết quả chính xác là { hasPassword: false, userRole: "GUEST keysCount: 3 }, hãy xác định điều kiện cần có của các thuộc tính trong tham số updateOptions.
> **Gợi ý trả lời & Định hướng đáp án:**
> Phân tích ngược từ kết quả mong muốn Z:
> 1. hasPassword = false -> Bắt buộc thuộc tính password phải bị xóa -> updateOptions.sanitize phải mang giá trị thruthy (true).
> 2. Ban đầu rawUser có 3 thuộc tính. Sau khi xóa password, user còn 2 thuộc tính (id, username).
> 3. userRole = "GUEST" -> Thuộc tính role không được thiết lập là "VIP" -> updateOptions.isVip phải mang giá trị falsy (false/undefined/null).
> 4. keysCount = 3 -> Tổng số thuộc tính cuối cùng trong restoredObj là 3. Vì hiện tại đang có 2 thuộc tính (id, username) và không có role, nên bắt buộc phải thêm đúng 1 thuộc tính động từ dynamicField.
> 5. Kết luận: updateOptions cần thỏa mãn: sanitize = true, isVip = false (hoặc falsy), và dynamicField phải là một object có đủ key và value hợp lệ (ví dụ: { key: "address value: "Hà Nội" }).

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Nếu một lập trình viên sửa câu lệnh xóa mật khẩu từ 'delete user.password;' thành 'user.password = undefined;' với mục đích làm rỗng mật khẩu, điều gì sẽ xảy ra với toán tử 'in' khi kiểm tra thuộc tính password ở giai đoạn TRƯỚC và SAU khi qua JSON.stringify()/JSON.parse()? Hãy giải thích bản chất bẫy lỗi này.
> **Gợi ý trả lời & Định hướng đáp án:**
> Phân tích bẫy lỗi Gotcha giữa từ khóa delete và gán giá trị undefined:
> 1. Giai đoạn 1 (Trước JSON.stringify): Với 'user.password = undefined', thuộc tính 'password' vẫn tồn tại dưới dạng một key trong bộ nhớ Object JS, chỉ có giá trị của nó là undefined. Do đó, phép kiểm tra '"password" in user' ở giai đoạn này vẫn trả về TRUE.
> 2. Giai đoạn 2 (Sau JSON.stringify và JSON.parse): Chuẩn định dạng JSON không hỗ trợ kiểu dữ liệu undefined. Do đó, phương thức JSON.stringify(user) sẽ tự động BỎ QUA và LOẠI BỎ hoàn toàn các thuộc tính có giá trị undefined khỏi chuỗi JSON kết quả. Khi JSON.parse() tái tạo lại Object, thuộc tính 'password' đã không còn. Phép kiểm tra '"password" in restoredObj' lúc này trả về FALSE.
> 3. Hậu quả & Cách khắc phục: Việc gán undefined làm rò rỉ key trong bộ nhớ JS nội bộ và gây bất đồng bộ logic kiểm tra dữ liệu trước/sau khi serialize. Cách khắc phục chuẩn xác nhất là giữ nguyên việc dùng từ khóa 'delete user.password' để gỡ bỏ triệt để cả key và value ra khỏi Object ngay từ đầu.

---

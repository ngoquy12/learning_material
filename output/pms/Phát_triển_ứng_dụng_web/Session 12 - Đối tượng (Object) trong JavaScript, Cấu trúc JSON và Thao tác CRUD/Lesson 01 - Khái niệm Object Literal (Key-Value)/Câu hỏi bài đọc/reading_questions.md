# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript
vanilla (es6+), html5
const student = {
  name: "Nguyen Van A",
  age: 20,
  course: "JavaScript",
  isPaid: true,
  "registered-date": "2023-10-15"
};

function getPropertyDetail(key) {
  if (key in student) {
    return student[key];
  }
  return "Thuộc tính không tồn tại";
}

function verifyStudentStatus(minAge) {
  if (student.age < minAge) {
    return "Chưa đủ tuổi đăng ký";
  }
  if (student.isPaid && student.course === "JavaScript") {
    return `Học viên ${student.name} đã thanh toán khóa ${student["course"]}`;
  }
  return `Học viên ${student.name} chưa hoàn tất học phí khóa ${student.course}`;
}
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X): Nếu chương trình thực thi hai câu lệnh lần lượt là getPropertyDetail("registered-date") và verifyStudentStatus(18), hãy chỉ ra luồng thực thi qua các nhánh điều kiện và kết quả trả về của từng hàm.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Đối với hàm getPropertyDetail("registered-date"):
>   + Toán tử 'in' kiểm tra xem khóa "registered-date" có tồn tại trong đối tượng student hay không. Thuộc tính này có tồn tại, nên biểu thức (key in student) trả về true.
>   + Nhánh if được kích hoạt và thực thi lệnh return student["registered-date"]. Phương thức Bracket notation truy xuất chính xác giá trị tương ứng.
>   + Kết quả trả về: "2023-10-15".
> 
> - Đối với hàm verifyStudentStatus(18):
>   + Nhánh if thứ nhất kiểm tra: student.age (20) < minAge (18). Điều kiện này trả về false, bỏ qua khối lệnh đầu tiên.
>   + Nhánh if thứ hai kiểm tra: student.isPaid (true) && student.course === "JavaScript" (true). Cả hai vế đều đúng nên biểu thức trả về true.
>   + Khối lệnh if thứ hai được kích hoạt và thực thi nối chuỗi template string.
>   + Kết quả trả về: "Học viên Nguyen Van A đã thanh toán khóa JavaScript".

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y): Nếu người dùng thay đổi lời gọi hàm thành getPropertyDetail("address") và verifyStudentStatus(25), luồng xử lý sẽ rẽ sang nhánh điều kiện nào và trả về kết quả gì?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Đối với hàm getPropertyDetail("address"):
>   + Khóa "address" không có trong đối tượng student, do đó biểu thức ("address" in student) trả về false.
>   + Nhánh if bị bỏ qua, chương trình chuyển xuống dòng lệnh cuối cùng của hàm.
>   + Kết quả trả về: "Thuộc tính không tồn tại".
> 
> - Đối với hàm verifyStudentStatus(25):
>   + Nhánh if thứ nhất kiểm tra: student.age (20) < minAge (25). Điều kiện này trả về true.
>   + Khối lệnh if thứ nhất được kích hoạt ngay lập tức và thực thi lệnh return.
>   + Luồng thực thi dừng lại tại đây, các câu lệnh kiểm tra isPaid và course phía dưới hoàn toàn không được chạy (unreachable code trong lượt gọi này).
>   + Kết quả trả về: "Chưa đủ tuổi đăng ký".

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Để hàm verifyStudentStatus(minAge) trả về kết quả "Học viên Nguyen Van A chưa hoàn tất học phí khóa JavaScript tham số minAge truyền vào phải thỏa mãn điều kiện gì và đối tượng student cần có sự thay đổi giá trị thuộc tính nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Phân tích logic để hàm chạy đến câu lệnh return cuối cùng:
>   1. Để không bị chặn ở nhánh if thứ nhất: Điều kiện (student.age < minAge) phải nhận giá trị false. Vì student.age mặc định là 20, nên tham số minAge truyền vào phải thỏa mãn điều kiện: minAge <= 20.
>   2. Để không bị chặn ở nhánh if thứ hai: Biểu thức (student.isPaid && student.course === "JavaScript") phải nhận giá trị false. Do student.course hiện đang là "JavaScript" (true), nên thuộc tính student.isPaid bắt buộc phải mang giá trị false.
> 
> - Kết luận: Cần gán student.isPaid = false và truyền tham số minAge nhỏ hơn hoặc bằng 20 (ví dụ: minAge = 18).

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Nếu lập trình viên sửa mã nguồn hàm getPropertyDetail thành 'return student.key;' và gọi trực tiếp 'student.registered-date', chương trình sẽ gặp lỗi logic và lỗi cú pháp như thế nào? Giải thích chi tiết và nêu cách sửa chuẩn.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Phân tích lỗi 1 (Sai lầm khi dùng Dot notation với biến dynamic): 
>   + Khi viết student.key, JavaScript sẽ tìm đúng thuộc tính có tên là "key" nằm bên trong đối tượng student chứ không lấy giá trị của biến key. Do trong student không có thuộc tính nào tên là "key kết quả trả về luôn là undefined thay vì giá trị của thuộc tính cần tìm.
> 
> - Phân tích lỗi 2 (Sai lầm khi truy cập khóa có ký tự đặc biệt bằng Dot notation):
>   + Câu lệnh student.registered-date sẽ bị JavaScript hiểu nhầm là phép toán trừ: lấy giá trị của student.registered trừ đi biến date. Điều này dẫn đến lỗi ReferenceError (nếu biến date chưa khai báo) hoặc trả về NaN.
> 
> - Cách khắc phục chuẩn:
>   1. Trong hàm getPropertyDetail: Sử dụng Bracket notation với biến student[key] để JavaScript giải mã giá trị bên trong biến key.
>   2. Khi truy xuất thuộc tính có chứa dấu gạch ngang: Sử dụng Bracket notation kèm chuỗi ký tự student["registered-date"].

---

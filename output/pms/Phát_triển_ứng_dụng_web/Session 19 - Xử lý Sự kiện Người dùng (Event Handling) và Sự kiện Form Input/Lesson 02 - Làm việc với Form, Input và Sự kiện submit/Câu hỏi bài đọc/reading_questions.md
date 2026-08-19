# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript
const bookingForm = document.querySelector("#bookingForm");
const fullnameInput = document.querySelector("#fullname");
const phoneInput = document.querySelector("#phone");
const messageElement = document.querySelector("#message");

bookingForm.addEventListener("submit", function(event) {
  event.preventDefault();
  
  const fullname = fullnameInput.value.trim();
  const phone = phoneInput.value.trim();

  if (fullname === "") {
    messageElement.textContent = "Vui lòng nhập họ và tên!";
    messageElement.style.color = "red";
  } else if (phone.length < 10) {
    messageElement.textContent = "Số điện thoại phải có ít nhất 10 chữ số!";
    messageElement.style.color = "red";
  } else {
    messageElement.textContent = "Đăng ký thành công cho bệnh nhân: " + fullname;
    messageElement.style.color = "green";
  }
});
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X): Giả sử người dùng nhập giá trị fullnameInput.value = "   Nguyễn Văn A   " và phoneInput.value = "0987654321" rồi nhấn nút Submit. Hãy mô tả các bước thực thi của hàm xử lý và xác định giá trị cuối cùng của messageElement.textContent cũng như messageElement.style.color.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Phương thức `event.preventDefault()` được gọi để chặn hành vi nạp lại trang mặc định của trình duyệt.
> - Bước 2: Phương thức `.trim()` loại bỏ toàn bộ khoảng trắng ở đầu và cuối chuỗi. Biến `fullname` nhận giá trị `"Nguyễn Văn A"` và biến `phone` nhận giá trị `"0987654321"`.
> - Bước 3: Kiểm tra điều kiện 1 `fullname === ""` -> trả về `false` (vì `"Nguyễn Văn A" !== ""`).
> - Bước 4: Kiểm tra điều kiện 2 `phone.length < 10` -> trả về `false` (vì độ dài chuỗi `"0987654321"` bằng 10, điều kiện 10 < 10 là sai).
> - Bước 5: Mã nguồn chuyển sang thực thi nhánh `else`.
> - Kết quả cuối cùng:
>   + `messageElement.textContent` = `"Đăng ký thành công cho bệnh nhân: Nguyễn Văn A"`
>   + `messageElement.style.color` = `"green"`

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y): Nếu người dùng thay đổi dữ liệu đầu vào thành fullnameInput.value = "Trần Thị B" và phoneInput.value = "0912345", hãy chỉ ra nhánh rẽ điều kiện nào sẽ được kích hoạt và nội dung văn bản hiển thị trên giao diện là gì?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Biến `fullname` sau khi `.trim()` có giá trị `"Trần Thị B"`. Biến `phone` sau khi `.trim()` có giá trị `"0912345"`.
> - Bước 2: Kiểm tra `fullname === ""` -> `false` (bỏ qua nhánh `if` đầu tiên).
> - Bước 3: Kiểm tra `phone.length < 10` -> `phone.length` bằng 7, điều kiện 7 < 10 trả về `true`.
> - Bước 4: Nhánh `else if (phone.length < 10)` được kích hoạt.
> - Kết quả thu được:
>   + `messageElement.textContent` nhận giá trị `"Số điện thoại phải có ít nhất 10 chữ số!"`
>   + `messageElement.style.color` nhận giá trị `"red"`

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Để hệ thống kích hoạt nhánh thành công và hiển thị thông báo màu xanh (messageElement.style.color = "green"), dữ liệu người dùng nhập vào hai ô input fullnameInput và phoneInput bắt buộc phải thỏa mãn những điều kiện logic nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> Để mã nguồn rơi vào nhánh `else` (thành công), dữ liệu đầu vào phải đồng thời vượt qua hai rào cản điều kiện phía trước:
> 1. Giá trị `fullnameInput.value` sau khi loại bỏ khoảng trắng bằng phương thức `.trim()` phải là một chuỗi không rỗng (`fullname.trim() !== ""`), tức là chứa ít nhất 1 ký tự hợp lệ.
> 2. Giá trị `phoneInput.value` sau khi gọi `.trim()` phải có độ dài chuỗi đạt từ 10 ký tự trở lên (`phone.trim().length >= 10`).

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Phân tích 2 trường hợp bẫy lỗi thực tế sau: 1) Lập trình viên quên không gọi dòng lệnh event.preventDefault(); 2) Lập trình viên bỏ qua phương thức .trim() và người dùng chỉ nhập toàn ký tự khoảng trắng "    " vào ô Họ tên. Hãy nêu hậu quả vận hành và cách sửa chuẩn.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Trường hợp bẫy lỗi 1 (Thiếu `event.preventDefault()`):
>   + Hậu quả: Khi nhấn Submit, trình duyệt ngay lập tức tải lại toàn bộ trang web (reload). Mọi thông tin vừa nhập và thông báo lỗi/thành công trong `messageElement` bị xóa sạch hoàn toàn.
>   + Cách khắc phục: Bắt buộc phải đặt `event.preventDefault()` ngay ở dòng đầu tiên bên trong callback của sự kiện `submit`.
> - Trường hợp bẫy lỗi 2 (Không sử dụng `.trim()` khi kiểm tra chuỗi):
>   + Hậu quả: Chuỗi `"    "` (4 khoảng trắng) có `.length = 4` nên khác chuỗi rỗng `""`. Điều kiện `fullname === ""` trả về `false`, dẫn đến việc hệ thống bỏ qua kiểm tra rỗng và vẫn báo đăng ký thành công cho một họ tên không có thực.
>   + Cách khắc phục: Luôn sử dụng `.trim()` để loại bỏ khoảng trắng thừa trước khi thực hiện kiểm tra độ dài hoặc so sánh chuỗi rỗng.

---
# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript
const productCard = document.querySelector('#product-card');
const previewImage = document.querySelector('#preview-image');
const actionButton = document.querySelector('#btn-detail');

function handleCardClick() {
  console.log('[Sự kiện click] Đã mở modal chi tiết sản phẩm');
}

function handleTrackAnalytics() {
  console.log('[Sự kiện click] Đã ghi nhận phân tích hành vi người dùng');
}

function handleImageHover() {
  console.log('[Sự kiện mouseover] Đã hiển thị ảnh phóng to sản phẩm');
}

function handleFavoriteToggle() {
  console.log('[Sự kiện dblclick] Đã thêm sản phẩm vào danh sách yêu thích');
}

actionButton.addEventListener('click', handleCardClick);
actionButton.addEventListener('click', handleTrackAnalytics);
previewImage.addEventListener('mouseover', handleImageHover);
productCard.addEventListener('dblclick', handleFavoriteToggle);
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X): Giả sử người dùng thực hiện thao tác nhấp chuột trái một lần (click) vào nút actionButton (#btn-detail). Hãy xác định thứ tự thực thi của các hàm xử lý và kết quả hiển thị tại cửa sổ console.
> **Gợi ý trả lời & Định hướng đáp án:**
> Khi người dùng nhấp chuột trái vào actionButton, sự kiện 'click' được kích hoạt. Nhờ cơ chế đăng ký nhiều hàm xử lý của addEventListener, trình duyệt sẽ tra cứu danh sách lắng nghe sự kiện của nút này và thực thi các hàm callback theo đúng thứ tự đã đăng ký:
> 1. Hàm handleCardClick chạy trước, in ra: '[Sự kiện click] Đã mở modal chi tiết sản phẩm'.
> 2. Hàm handleTrackAnalytics chạy tiếp theo, in ra: '[Sự kiện click] Đã ghi nhận phân tích hành vi người dùng'.

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y): Nếu người dùng di chuyển con trỏ chuột vào vùng ảnh previewImage (#preview-image), sau đó thực hiện nhấp đôi chuột (dblclick) lên thẻ productCard (#product-card), luồng xử lý và kết quả hiển thị console sẽ thay đổi như thế nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> Quá trình xử lý diễn ra qua 2 giai đoạn thao tác độc lập:
> 1. Thao tác rơ chuột vào previewImage kích hoạt sự kiện 'mouseover', thực thi callback handleImageHover và in ra: '[Sự kiện mouseover] Đã hiển thị ảnh phóng to sản phẩm'.
> 2. Thao tác nhấp đôi chuột lên productCard kích hoạt sự kiện 'dblclick', thực thi callback handleFavoriteToggle và in ra: '[Sự kiện dblclick] Đã thêm sản phẩm vào danh sách yêu thích'.

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Để cửa sổ console xuất hiện chính xác thông điệp '[Sự kiện dblclick] Đã thêm sản phẩm vào danh sách yêu thích', người dùng cần phải tương tác thế nào trên giao diện và đối tượng DOM nào bị tác động?
> **Gợi ý trả lời & Định hướng đáp án:**
> Để nhận được kết quả đầu ra trên, người dùng bắt buộc phải thực hiện thao tác nhấp đôi chuột trái hai lần liên tiếp trong khoảng thời gian ngắn (tương ứng với loại sự kiện 'dblclick') trực tiếp lên phần tử DOM đại diện cho thẻ sản phẩm có id là 'product-card' (đã được gán tham chiếu thông qua biến productCard).

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Nếu lập trình viên viết sai dòng đăng ký sự kiện thành actionButton.addEventListener('click', handleCardClick()); (có dấu ngoặc tròn sau tên hàm), hiện tượng bất thường gì sẽ xảy ra khi tải trang và khi nhấp chuột? Hãy phân tích nguyên nhân và nêu cách sửa.
> **Gợi ý trả lời & Định hướng đáp án:**
> Phân tích bẫy lỗi:
> - Khi tải trang: Cặp dấu ngoặc tròn () khiến hàm handleCardClick() bị gọi ngay lập tức trong quá trình biên dịch script, dẫn đến dòng '[Sự kiện click] Đã mở modal chi tiết sản phẩm' bị in ra console ngay dù người dùng chưa hề nhấp chuột.
> - Khi người dùng nhấp chuột vào nút: Do handleCardClick() không trả về giá trị (tương đương undefined), addEventListener nhận vào handler là undefined. Do đó, khi sự kiện click thực sự xảy ra, không có logic nào được thực thi.
> Cách khắc phục: Bỏ cặp dấu ngoặc tròn và chỉ truyền tham chiếu tên hàm (function reference) là actionButton.addEventListener('click', handleCardClick);

---
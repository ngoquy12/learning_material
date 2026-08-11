# Bài thực hành: Quản lý danh sách đơn hàng và xử lý tọa độ giao hàng với List và Tuple

## 1. Mục tiêu
- Vận dụng kiến thức Python 3.12 để thao tác xóa dữ liệu trong List bằng các phương thức pop(), remove(), clear() và từ khóa del.
- Khai thác tính bất biến (Immutable) của Tuple để bảo vệ dữ liệu và áp dụng kỹ thuật Unpacking cùng thao tác hoán đổi giá trị (swap).
- Thành thạo thao tác thực hành và kiểm chuẩn kết quả xử lý dữ liệu trong Python 3.12.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.12 và tệp mã nguồn main.py.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp main.py và khai báo một List chứa mã đơn hàng 'orders = [101, 102, 103, 104, 105]' cùng một Tuple chứa tọa độ giao hàng 'location = (21.0285, 105.8542)'.
2. Bước 2: Thực thi thao tác xóa phần tử trên List: dùng remove(103) để xóa theo giá trị, pop() để lấy và xóa phần tử cuối cùng, del orders[0] để xóa theo vị trí chỉ số, và thử nghiệm phương thức clear() trên một List phụ.
3. Bước 3: Thực nghiệm tính bất biến của Tuple bằng cách gán lại giá trị cho location[0] để bắt lỗi TypeError; sau đó sử dụng Tuple Unpacking để giải nén tọa độ thành hai biến lat, lng và thực hiện hoán đổi giá trị 'lat, lng = lng, lat'.
4. Bước 4: Kiểm tra kết quả in ra màn hình console, đối chiếu trạng thái dữ liệu List và Tuple sau các thao tác để hoàn tất bài thực hành.

## 3. Checklist đánh giá
- [ ] Phân biệt và sử dụng chính xác các cơ chế xóa phần tử trong List: pop(), remove(), clear() và từ khóa del.
- [ ] Chứng minh và xử lý thành công đặc tính bất biến (Immutable) của Tuple trong Python 3.12.
- [ ] Thực hiện thành công kỹ thuật Tuple Unpacking và hoán đổi giá trị hai biến mà không cần biến trung gian.
- [ ] Mã nguồn tuân thủ quy chuẩn PEP 8 và chương trình thực thi không phát sinh lỗi cú pháp.
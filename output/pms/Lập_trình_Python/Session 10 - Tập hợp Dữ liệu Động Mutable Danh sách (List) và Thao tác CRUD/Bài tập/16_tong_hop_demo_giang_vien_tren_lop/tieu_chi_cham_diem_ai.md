# **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
- **10 điểm**: Xác định đúng bản chất dữ liệu danh sách động (Mutable List) và quy tắc chỉ số index bắt đầu từ 0.
- **10 điểm**: Sơ đồ hóa chính xác thứ tự biến đổi của danh sách qua 3 bước: Khởi tạo -> Cập nhật giá trị qua index -> Xóa phần tử bằng `del` -> Kiểm tra độ dài với `len()`.

#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
- **15 điểm**: Khai báo danh sách cước phí chính xác kiểu dữ liệu danh sách số nguyên (`list[int]`) với chuẩn Type Hints của Python 3.12.
- **15 điểm**: Thực hiện đúng cú pháp cập nhật phần tử qua index và xóa phần tử bằng câu lệnh `del` mà không sử dụng các phương thức bị cấm.
- **10 điểm**: Sử dụng chính xác hàm `len()` để lấy tổng số lượng phần tử còn lại.

#### **3. Xử lý sai sót dữ liệu & Ngoại lệ — 20 điểm**
- **10 điểm**: Thao tác chỉ số index chính xác, không truy cập vượt quá phạm vi độ dài của danh sách.
- **10 điểm**: Đảm bảo luồng dữ liệu thay đổi nhất quán, in thông tin trạng thái danh sách rõ ràng sau từng thao tác.

#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
- **10 điểm**: Đặt tên biến theo chuẩn `snake_case`, tuân thủ nghiêm ngặt quy định PEP 8.
- **10 điểm**: Tạo cấu trúc thư mục nộp bài và tên tệp tin chính xác theo hướng dẫn.

### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Xử lý Lịch sử Tương tác và Tọa độ Khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
* **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo đúng file `main.py`, thiết lập dự án chuẩn Python 3.12, chạy thực thi không có lỗi cú pháp.
* **[10 điểm] Xây dựng Cấu trúc dữ liệu:** Khai báo chính xác dữ liệu đầu vào Tuple `customer_info` và List `session_history` đúng kiểu dữ liệu và giá trị mô tả.

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
* **[20 điểm] Thao tác trên Tuple & Unpacking/Swap:** Giải nén thành công 4 biến từ Tuple, hoán đổi biến trực tiếp `latitude, longitude = longitude, latitude` không dùng biến trung gian, đóng gói lại thành Tuple mới chính xác.
* **[20 điểm] Thao tác trên List (Index & Slicing):** Cập nhật đúng phần tử tại chỉ số index 0 của List bằng phép gán trực tiếp (`session_history[0] = 9999`) và trích xuất đúng phân đoạn bằng kỹ thuật Slicing `[1:4]`.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
* **[10 điểm] Tuân thủ tính bất biến của Tuple:** Không cố tình sửa đổi trực tiếp các phần tử trong Tuple gốc (tránh lỗi `TypeError`), thể hiện sự hiểu biết về tính bất biến của Tuple.
* **[10 điểm] Chính xác về chỉ số Slicing và Index:** Cắt lát lấy chính xác 3 phần tử (index 1, 2, 3) mà không ghi đè hay làm hỏng cấu trúc danh sách ban đầu.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
* **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Mã nguồn đạt chuẩn PEP 8 (đặt tên biến dạng `snake_case`), hiển thị thông tin ra màn hình CLI khớp với định dạng yêu cầu.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
* **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub theo đúng định dạng tên thư mục `[Tên Lớp]_[Môn Học]_Session08_Ex06`.
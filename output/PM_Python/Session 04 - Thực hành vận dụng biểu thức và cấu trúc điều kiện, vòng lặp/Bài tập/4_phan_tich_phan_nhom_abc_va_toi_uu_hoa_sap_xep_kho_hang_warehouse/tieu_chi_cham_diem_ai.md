### **Tiêu chí chấm điểm (AI)**
**Phân Tích Phân Nhóm ABC và Tối Ưu Hóa Sắp Xếp Kho Hàng Warehouse — Tổng điểm: 100 điểm**

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
*   **10 điểm**: Khai báo và cấu trúc các bộ dữ liệu sản phẩm mẫu (dạng list các dict) đầy đủ các thông tin cần thiết: `id`, `name`, `quantity`, `unit_price`, `frequency` và định dạng dữ liệu đầu vào chuẩn xác, không có lỗi cú pháp.
*   **10 điểm**: Định nghĩa cấu trúc các hàm xử lý đúng với số lượng tham số đầu vào và kiểu dữ liệu trả về theo đặc tả đề bài.

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
*   **15 điểm**: Viết thuật toán phân loại ABC chính xác. Tính toán đúng tổng giá trị của toàn kho hàng, tỉ lệ phần trăm đóng góp của mỗi sản phẩm và tỉ lệ phần trăm lũy kế cộng dồn sau khi xếp hạng.
*   **15 điểm**: Phân bổ vị trí kệ chứa chính xác dựa trên sự kết hợp logic đa điều kiện (`if-elif-else`) giữa nhóm ABC (xác định `zone`) và tần suất xuất nhập kho `frequency` (xác định `shelf_level`).

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
*   **15 điểm**: Thực hiện thành công giải thuật sắp xếp thủ công (vd: Bubble Sort, Selection Sort,...) bằng vòng lặp lồng nhau mà không sử dụng hàm built-in `sorted()` hay phương thức `.sort()`.
*   **15 điểm**: Xử lý validation dữ liệu an toàn: Tránh các lỗi chia cho 0 khi tính tỷ trọng nếu tổng kho bằng 0; xử lý trường hợp giá trị của sản phẩm bị âm hoặc không hợp lệ bằng cách bỏ qua sản phẩm lỗi hoặc gán dữ liệu mặc định an toàn.

#### **4. Kiểm thử hoặc câu hỏi lý thuyết bổ sung — 10 điểm**
*   **10 điểm**: Tạo tập dữ liệu thử nghiệm phân trang (bao gồm ít nhất 8 sản phẩm). Chạy thử nghiệm hàm `search_and_filter_inventory` với các bộ giá trị lọc khác nhau để chứng minh kết quả phân trang chuẩn xác (ví dụ: yêu cầu trang 2, mỗi trang 3 phần tử phải trả đúng 3 phần tử tiếp theo của danh sách đã được lọc).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **5 điểm**: Đặt tên biến khoa học (camelCase hoặc snake_case thống nhất), viết code rõ ràng, có chú thích các phân đoạn nghiệp vụ cốt lõi, không chứa mã thừa hay các đoạn code debug cứng.
*   **5 điểm**: Cấu trúc thư mục dự án chuẩn, nộp bài đúng cách (cung cấp link GitHub repository hợp lệ và công khai mã nguồn).

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
*   **5 điểm**: Viết hàm tạo báo cáo tổng quan dưới dạng văn bản (không dùng thư viện ngoài) hiển thị bảng tóm tắt: Tổng số lượng hàng hóa các nhóm A, B, C; tổng giá trị dòng tiền của từng nhóm để giúp nhà quản lý có cái nhìn trực quan.
*   **5 điểm**: Xử lý logic trường hợp sản phẩm có mức độ ưu tiên xếp hạng bằng nhau (đồng giá trị `total_value`) thì sắp xếp phụ theo tần suất xuất kho `frequency` để tăng độ ổn định của hệ thống.
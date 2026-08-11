## <center>Bài kiểm tra đầu giờ: Ứng dụng Tìm kiếm & Thống kê Đánh giá Chuyến đi (Ride Rating Search & Analytics CLI)</center>

### **1. Mục tiêu**
- Đánh giá khả năng vận dụng cấu trúc dữ liệu danh sách (`list`) chứa các bộ (`tuple`) để lưu trữ dữ liệu đa thuộc tính.
- Kiểm tra kỹ năng thực thi logic tìm kiếm nâng cao, lọc dữ liệu có điều kiện và tính toán thống kê cơ bản bằng vòng lặp (`for`, `while`) và cấu trúc rẽ nhánh (`if-elif-else`).
- Rèn luyện kỹ năng xây dựng giao diện dòng lệnh (CLI Menu) tương tác và xử lý ngoại lệ nhập liệu cơ bản (`try-except`).

### **2. Yêu cầu**

#### **Ngữ cảnh bài toán**
Doanh nghiệp vận tải công nghệ cần một công cụ Console CLI nhẹ để vận hành viên có thể tra cứu và phân tích danh sách các chuyến đi. Danh sách dữ liệu chuyến đi ban đầu được khai báo sẵn dưới dạng một `list` chứa các `tuple`, với định dạng mỗi chuyến đi gồm 5 thông tin: `(trip_id, customer_name, rating_score, trip_fare, status)`:
- `trip_id` (str): Mã chuyến đi (ví dụ: `"TRIP01"`).
- `customer_name` (str): Tên khách hàng.
- `rating_score` (int): Điểm đánh giá (từ 1 đến 5).
- `trip_fare` (float): Cước phí chuyến đi (VND).
- `status` (str): Trạng thái chuyến đi (`"COMPLETED"` hoặc `"CANCELLED"`).

Dữ liệu mẫu ban đầu:
```python
trips_data = [
    ("TRIP01", "Alex Smith", 5, 150.0, "COMPLETED"),
    ("TRIP02", "John Doe", 2, 45.0, "COMPLETED"),
    ("TRIP03", "Elena Rostova", 4, 85.0, "CANCELLED"),
    ("TRIP04", "Michael Brown", 1, 60.0, "COMPLETED"),
    ("TRIP05", "Sarah Connor", 5, 210.0, "COMPLETED"),
    ("TRIP06", "David Miller", 3, 110.0, "CANCELLED")
]
```

#### **Bảng chi tiết các chức năng hệ thống**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%;">Tên chức năng / Thành phần</th>
      <th style="width: 20%;">Đầu vào / Tham số</th>
      <th style="width: 35%;">Lô-gíc xử lý & Quy tắc</th>
      <th style="width: 20%;">Đầu ra / Kết quả mong đợi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>[Lọc chuyến đi theo tiêu chí]</b><br><code>filter_trips_by_criteria</code></td>
      <td>
        - <code>min_rating</code> (int): Điểm đánh giá tối thiểu người dùng nhập.<br>
        - <code>target_status</code> (str): Trạng thái cần lọc (chuyển sang chữ hoa bằng <code>.upper()</code>).
      </td>
      <td>
        - Duyệt qua danh sách <code>trips_data</code> bằng vòng lặp <code>for</code>.<br>
        - Kiểm tra điều kiện: <code>rating_score >= min_rating</code> VÀ <code>status == target_status</code>.<br>
        - Nếu tìm thấy, in thông tin chuyến đi dạng dòng văn bản chuẩn hóa. Nếu không có kết quả phù hợp, in thông báo phản hồi.
      </td>
      <td>
        - Danh sách các chuyến đi thỏa mãn được in ra Console.<br>
        - Phản hồi báo không tìm thấy nếu danh sách rỗng.
      </td>
    </tr>
    <tr>
      <td><b>[Thống kê doanh thu & Đánh giá]</b><br><code>analyze_trip_statistics</code></td>
      <td>Không có đầu vào từ bàn phím. Dùng dữ liệu trong <code>trips_data</code>.</td>
      <td>
        - Duyệt qua danh sách các chuyến đi.<br>
        - Chỉ xét các chuyến có trạng thái <code>"COMPLETED"</code>.<br>
        - Tính <b>Tổng doanh thu</b> = Tổng <code>trip_fare</code> của các chuyến hoàn tất.<br>
        - Tính <b>Điểm đánh giá trung bình</b> = Tổng <code>rating_score</code> / Số lượng chuyến hoàn tất.<br>
        - Xử lý trường hợp không có chuyến hoàn tất (tránh lỗi chia cho 0).
      </td>
      <td>
        - In ra tổng số chuyến hoàn tất.<br>
        - In ra Tổng doanh thu thực tế.<br>
        - In ra Điểm đánh giá trung bình (làm tròn 2 chữ số thập phân).
      </td>
    </tr>
    <tr>
      <td><b>[Giao diện Menu Console]</b><br><code>interactive_cli_menu</code></td>
      <td>Lựa chọn menu từ bàn phím (<code>user_choice</code>).</td>
      <td>
        - Sử dụng vòng lặp <code>while True</code> để duy trì menu.<br>
        - Hiển thị các lựa chọn: 1. Lọc chuyến đi | 2. Thống kê | 3. Thoát chương trình.<br>
        - Bắt ngoại lệ nhập dữ liệu không hợp lệ bằng <code>try-except</code> (ví dụ nhập chữ thay vì nhập số <code>min_rating</code>).
      </td>
      <td>
        Vòng lặp điều hướng hoạt động ổn định, không bị ngắt rủ đột ngột khi nhập sai định dạng.
      </td>
    </tr>
  </tbody>
</table>

> **LƯU Ý CHÍNH CÁCH THỰC HIỆN (PHẠM VI CHO PHÉP):**
> - **KHÔNG** sử dụng Hàm tự định nghĩa (`def`), **KHÔNG** dùng Dictionary (`dict`), **KHÔNG** dùng Set (`set`), **KHÔNG** dùng Lớp (`class`).
> - Viết toàn bộ chương trình dưới dạng kịch bản điều khiển bằng cấu trúc menu `while True`, các khối lệnh rẽ nhánh `if-elif-else` và vòng lặp `for` trực tiếp.

---

### **3. Tiêu chí đánh giá**

- **2.0 điểm**: Khai báo cấu trúc dữ liệu ban đầu đúng chuẩn `list` chứa các `tuple` và dựng khung Menu tương tác người dùng `while True`.
- **3.5 điểm**: Thực thi chính xác logic Chức năng 1 (Lọc chuyến đi theo điểm rating tối thiểu và trạng thái chuyến đi bằng vòng lặp và câu lệnh `if`).
- **3.0 điểm**: Thực thi chính xác logic Chức năng 2 (Tính toán tổng doanh thu và điểm rating trung bình của các chuyến đi hoàn tất, xử lý chia cho 0 nếu cần).
- **1.5 điểm**: Bắt ngoại lệ nhập liệu (`try-except`) khi ép kiểu dữ liệu từ người dùng và tuân thủ quy chuẩn đặt tên biến bằng Tiếng Anh chuẩn `snake_case`.

---

### **4. Yêu cầu nộp bài**

- Sinh viên chuẩn bị mã nguồn trong file duy nhất theo đúng cấu trúc đặt tên: `bai_kiem_tra_01_tim_kiem_thong_ke_chuyen_di.py`.
- Đảm bảo mã nguồn chạy trực tiếp thành công trên môi trường Python 3.12 (`python main.py` hoặc `python bai_kiem_tra_01_tim_kiem_thong_ke_chuyen_di.py`).
- Thực hiện commit mã nguồn và push lên kho lưu trữ GitHub (GitHub Repository) cá nhân thuộc nhánh `main`.
- Dán đường dẫn URL file mã nguồn GitHub vào hệ thống nộp bài trước khi hết giờ làm bài.
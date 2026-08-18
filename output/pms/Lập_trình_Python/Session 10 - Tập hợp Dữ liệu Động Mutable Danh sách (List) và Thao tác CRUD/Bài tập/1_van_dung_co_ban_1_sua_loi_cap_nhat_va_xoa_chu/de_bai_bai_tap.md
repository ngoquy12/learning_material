## <center>[Vận dụng cơ bản 1] Sửa lỗi cập nhật và xóa chuyến đi trong danh sách cước phí GrabRide</center>

### **1. Mục tiêu**
*   Hiểu và vận dụng thành thạo các thao tác cập nhật phần tử theo chỉ số (index) và xóa phần tử bằng câu lệnh `del` trên danh sách động (`list`) trong Python 3.12.
*   Rèn luyện kỹ năng đọc vết mã nguồn (Code Tracing), phân tích hiện tượng lệch chỉ số (Index Shift Bug) khi thay đổi cấu trúc danh sách.
*   Tuân thủ chuẩn trình bày mã nguồn PEP 8 và chú giải kiểu dữ liệu (Type Hints).

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt xe công nghệ GrabRide (GRAB_RIDE), cước phí tạm tính của các chuyến đi hoàn thành trong ca làm việc của tài xế được lưu trữ dưới dạng một danh sách số nguyên `danh_sach_cuoc_phi` (đơn vị: VNĐ).

Bộ phận vận hành nhận được phản ánh từ tài xế với nội dung như sau: "Chương trình ghi nhận ca làm việc bị sai cước phí. Khi hệ thống cập nhật phụ phí thời tiết cho một chuyến đi và xóa chuyến đi bị khách hàng hủy, cước phí của chuyến đi thành công khác lại bị thay đổi sai lệch, trong khi chuyến đi cần cập nhật phụ phí vẫn giữ nguyên giá cũ."### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn `main.py` bị lỗi nghiệp vụ do lập trình viên tiền nhiệm bàn giao:

```python
# Virtualenv: venv | Python 3.12
# Chuẩn PEP 8 & Type Hints

# Khởi tạo danh sách cước phí 5 chuyến đi ban đầu của tài xế (VNĐ)
danh_sach_cuoc_phi: list[int] = [25000, 45000, 12000, 60000, 35000]
print("Danh sách cước phí ban đầu: danh_sach_cuoc_phi)

# Nghiệp vụ 1: Xóa chuyến đi thứ 2 (chuyến 45.000 VNĐ bị khách hủy)
del danh_sach_cuoc_phi[1]

# Nghiệp vụ 2: Cập nhật cước phí chuyến đi thứ 3 ban đầu lên 18.000 VNĐ (thêm phụ phí thời tiết)
danh_sach_cuoc_phi[2] = 18000

# Thống kê tổng số chuyến đi còn lại
so_luong_chuyen: int = len(danh_sach_cuoc_phi)

print("Danh sách cước phí sau xử lý: danh_sach_cuoc_phi)
print("Tổng số chuyến đi thành công: so_luong_chuyen)
```

### **4. Yêu cầu bài toán**
Học viên thực hiện đầy đủ 2 phần nhiệm vụ sau:

#### **Phần 1: Tracing code & Lập báo cáo Test Case**
1. Thực hiện truy vết mã nguồn từng dòng để xác định nguyên nhân tại sao chuyến đi thứ 3 không được cập nhật đúng giá cước trị giá 18.000 VNĐ.
2. Hoàn thiện bảng báo cáo Test Case theo mẫu dưới đây vào file báo cáo (hoặc phần ghi chú nộp bài):

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: center;">STT</th>
      <th style="padding: 8px; text-align: center;">Dữ liệu đầu vào (Input)</th>
      <th style="padding: 8px; text-align: center;">Đầu ra hiện tại bị lỗi (Buggy Output)</th>
      <th style="padding: 8px; text-align: center;">Đầu ra kỳ vọng (Expected Output)</th>
      <th style="padding: 8px; text-align: center;">Dòng code gây lỗi</th>
      <th style="padding: 8px; text-align: center;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: center;">1</td>
      <td style="padding: 8px;">danh_sach_cuoc_phi = [25000, 45000, 12000, 60000, 35000]</td>
      <td style="padding: 8px;">Danh sách: [25000, 12000, 18000, 35000]<br>Số chuyến: 4</td>
      <td style="padding: 8px;">Danh sách: [25000, 18000, 60000, 35000]<br>Số chuyến: 4</td>
      <td style="padding: 8px; text-align: center;">Dòng 11</td>
      <td style="padding: 8px;">Do lệnh del ở dòng 8 làm giảm chỉ số các phần tử đứng sau, dẫn đến việc gán index 2 ở dòng 11 bị ghi đè nhầm sang giá cước 60000 thay vì 12000.</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">2</td>
      <td style="padding: 8px;">danh_sach_cuoc_phi = [12000, 30000, 15000, 50000]</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">3</td>
      <td style="padding: 8px;">danh_sach_cuoc_phi = [50000, 20000, 40000, 10000, 80000]</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa mã nguồn nghiệp vụ**
1. Sửa lại mã nguồn `main.py` sao cho:
   * Chuyến đi thứ 3 (trị giá 12.000 VNĐ ban đầu) được cập nhật thành công thành 18.000 VNĐ.
   * Chuyến đi thứ 2 (trị giá 45.000 VNĐ ban đầu) bị xóa chính xác khỏi danh sách.
   * Hàm `len()` trả về đúng số lượng chuyến đi còn lại (4 chuyến).
2. Quy định kỹ thuật:
   * Chỉ sử dụng thao tác gán chỉ số `list[index] = value`, xóa `del list[index]` và đếm `len()`.
   * TUYỆT ĐỐI KHÔNG sử dụng các phương thức hoặc cấu trúc chưa học: `append()`, `pop()`, `remove()`, `insert()`, `def`, `class`, `dict`, `set`, `tuple`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex1`.
    Ví dụ: `HNKS25CNTT1_Core_Session10_Ex1`
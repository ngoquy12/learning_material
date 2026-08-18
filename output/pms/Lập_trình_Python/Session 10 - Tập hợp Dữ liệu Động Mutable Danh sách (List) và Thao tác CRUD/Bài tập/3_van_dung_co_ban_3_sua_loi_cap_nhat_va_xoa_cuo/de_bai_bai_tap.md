## <center>[Vận dụng cơ bản 3] Sửa lỗi cập nhật và xóa cước phí chuyến đi GrabRide</center>

### **1. Mục tiêu**
*   **Kỹ năng truy vết (Code Tracing):** Thực hành đọc hiểu và phân tích thứ tự thực thi lệnh liên quan đến danh sách động `list` trong Python 3.12.
*   **Hiểu bản chất danh sách mutable:** Nhận biết tác động của thao tác xóa phần tử (`del`) làm thay đổi vị trí chỉ số (index) của các phần tử còn lại trong danh sách.
*   **Sửa lỗi nghiệp vụ (Bug Fixing):** Điều chỉnh lại mã nguồn để quy trình cập nhật giá trị (`list[index] = new_value`) và xóa phần tử (`del list[index]`) tuân thủ đúng yêu cầu của hệ thống GrabRide.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt xe GrabRide, danh sách cước phí của các chuyến đi hoàn thành trong ca làm việc của tài xế được lưu trữ trong danh sách `list[int]`. Vào cuối ca, hệ thống thực hiện hai thao tác điều chỉnh dữ liệu:
1.  **Cập nhật cước phí:** Chuyến đi ở vị trí chỉ số `2` được tài xế báo bổ sung phụ phí thời tiết, cước phí mới cần điều chỉnh thành `50000` VNĐ.
2.  **Xóa chuyến đi hủy:** Chuyến đi ở vị trí chỉ số `1` bị khách hàng hủy thao tác trên ứng dụng, cần xóa khỏi danh sách cước phí.

Tuy nhiên, tài xế phản ánh rằng trên ứng dụng hiển thị cước phí chuyến đi số `2` (giá cũ `45000` VNĐ) vẫn giữ nguyên không thay đổi, trong khi một chuyến đi khác lại bị thay đổi số tiền bất thường thành `50000` VNĐ.### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn hiện tại đang chạy trên môi trường thử nghiệm bị phản ánh gặp lỗi logic:

```python
# Virtualenv: venv | Python 3.12
# Chuẩn PEP 8 & Type Hints

# Khởi tạo danh sách cước phí 5 chuyến đi trong ca của tài xế (đơn vị: VNĐ)
cuoc_phi_chuyen_di: list[int] = [12000, 25000, 45000, 30000, 18000]

print("Danh sách cước phí ban đầu: cuoc_phi_chuyen_di)

# Thực hiện xóa chuyến đi bị hủy ở vị trí chỉ số 1
del cuoc_phi_chuyen_di[1]

# Thực hiện cập nhật cước phí chuyến đi điều chỉnh ở vị trí chỉ số 2 thành 50000
cuoc_phi_chuyen_di[2] = 50000

# Kiểm tra tổng số chuyến đi còn lại trong ca
tong_so_chuyen: int = len(cuoc_phi_chuyen_di)

print("Danh sách cước phí sau xử lý: cuoc_phi_chuyen_di)
print("Tổng số chuyến đi hợp lệ: tong_so_chuyen)
```

### **4. Yêu cầu bài toán**

Học viên thực hiện bài tập theo 2 phần bắt buộc sau:

#### **Phần 1: Báo cáo truy vết lỗi (Test Case Report)**
Học viên tiến hành chạy thử mã nguồn, phân tích sự thay đổi chỉ số của các phần tử và hoàn thành bảng báo cáo kiểm thử dưới đây vào báo cáo cá nhân:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: center;">STT</th>
      <th style="padding: 8px; text-align: center;">Dữ liệu đầu vào (Input)</th>
      <th style="padding: 8px; text-align: center;">Kết quả lỗi hiện tại (Buggy Output)</th>
      <th style="padding: 8px; text-align: center;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="padding: 8px; text-align: center;">Dòng code gây lỗi (Failing Line)</th>
      <th style="padding: 8px; text-align: center;">Phân tích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: center;">1</td>
      <td style="padding: 8px;"><code>[12000, 25000, 45000, 30000, 18000]</code></td>
      <td style="padding: 8px;"><code>[12000, 45000, 50000, 18000]</code><br>Tổng: 4</td>
      <td style="padding: 8px;"><code>[12000, 50000, 30000, 18000]</code><br>Tổng: 4</td>
      <td style="padding: 8px; text-align: center;">Dòng 10</td>
      <td style="padding: 8px;">Thực hiện <code>del</code> ở dòng 10 trước làm các phần tử phía sau bị dồn sang trái 1 chỉ số, khiến dòng 13 gán <code>50000</code> vào sai vị trí chuyến đi.</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">2</td>
      <td style="padding: 8px;"><code>[15000, 30000, 20000, 60000, 40000]</code></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">3</td>
      <td style="padding: 8px;"><code>[10000, 20000, 30000, 40000, 50000]</code></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (Source Code Correction)**
*   Chỉnh sửa lại chương trình trong tệp `main.py` để kết quả cập nhật cước phí và xóa chuyến đi chính xác theo đúng nghiệp vụ.
*   Mã nguồn sau khi sửa phải tuân thủ chuẩn PEP 8, có Type Hints và đảm bảo thứ tự thực thi hợp lý.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex3`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session10_Ex3`
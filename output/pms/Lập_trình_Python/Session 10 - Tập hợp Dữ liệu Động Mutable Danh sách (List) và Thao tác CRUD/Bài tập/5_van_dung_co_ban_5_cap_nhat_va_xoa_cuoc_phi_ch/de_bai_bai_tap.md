## <center>[Vận dụng cơ bản 5] Cập nhật và Xóa cước phí chuyến đi GrabRide</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu và thao tác thành thạo việc cập nhật giá trị phần tử theo chỉ số (`index`), xóa phần tử bằng câu lệnh `del` và truy xuất độ dài danh sách bằng hàm `len()` trong Python 3.12.
*   **Kỹ năng:** Phân tích thứ tự thực thi thao tác làm biến đổi danh sách động (Mutable List), phát hiện lỗi lệch chỉ số (Index Shift Bug) khi xóa phần tử trước khi cập nhật.
*   **Thái độ:** Rèn luyện tư duy cẩn trọng khi thao tác trực tiếp trên danh sách mutable trong các ứng dụng thực tế.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống quản lý chuyến đi **GrabRide**, sau mỗi ca làm việc, danh sách cước phí các chuyến đi của tài xế được lưu trữ dưới dạng một danh sách số nguyên `trip_fares` (đơn vị: VNĐ). Hệ thống cần hỗ trợ hai thao tác điều chỉnh dữ liệu trong ca:
1.  **Cập nhật cước phí:** Điều chỉnh giá tiền của một chuyến đi cụ thể khi có phụ phí thời tiết hoặc phụ phí giờ cao điểm.
2.  **Xóa chuyến đi:** Loại bỏ cước phí của chuyến đi bị hủy hoặc vi phạm quy định khỏi danh sách.

Tài xế GrabRide gửi phản ánh lên trung tâm hỗ trợ: Khi chuyến đi ở vị trí thứ 2 (chỉ số `1`) bị hủy và hệ thống thực hiện điều chỉnh tăng cước cho chuyến đi ban đầu ở vị trí thứ 3 (chỉ số `2`), cước phí của chuyến đi thứ 3 lại không được cập nhật đúng, trong khi cước phí của một chuyến đi khác lại bị thay đổi sai lệch.### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn hiện tại đang thực thi quy trình điều chỉnh cước phí ca làm việc của tài xế:

```python
# Virtualenv: venv | Python 3.12
# Chuẩn PEP 8 & Type Hints

# Danh sách cước phí các chuyến đi ban đầu của tài xế (VNĐ)
trip_fares: list[int] = [25000, 45000, 60000, 35000, 80000]

print("Danh sách cước phí ban đầu: trip_fares)

# Xóa chuyến đi bị hủy tại chỉ số 1 (chuyến 45.000 VNĐ)
del trip_fares[1]

# Cập nhật cước phí chuyến đi ban đầu tại chỉ số 2 thành 65.000 VNĐ (phụ phí mưa)
trip_fares[2] = 65000

# Thống kê tổng số chuyến đi còn lại trong ca
remaining_trips: int = len(trip_fares)

print("Danh sách cước phí sau khi xử lý: trip_fares)
print("Tổng số chuyến đi còn lại: remaining_trips)
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Báo cáo Test Case (Code Tracing)**
Học viên tiến hành chạy thử chương trình, phân tích sự thay đổi chỉ số của danh sách qua từng dòng lệnh và hoàn thiện bảng báo cáo kịch bản kiểm thử bên dưới (điền vào các vị trí `...`):

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: center;">STT</th>
      <th style="padding: 8px; text-align: left;">Dữ liệu đầu vào (trip_fares ban đầu)</th>
      <th style="padding: 8px; text-align: left;">Kết quả hiện tại (Buggy Output)</th>
      <th style="padding: 8px; text-align: left;">Kết quả mong đợi (Expected Output)</th>
      <th style="padding: 8px; text-align: center;">Dòng code gây lỗi</th>
      <th style="padding: 8px; text-align: left;">Giải thích nguyên nhân</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: center;">1</td>
      <td style="padding: 8px;">[25000, 45000, 60000, 35000, 80000]</td>
      <td style="padding: 8px;">[25000, 60000, 65000, 80000]</td>
      <td style="padding: 8px;">[25000, 65000, 35000, 80000]</td>
      <td style="padding: 8px; text-align: center;">Lệnh del trip_fares[1] đứng trước trip_fares[2] = 65000</td>
      <td style="padding: 8px;">Việc xóa phần tử tại index 1 làm các phần tử phía sau dịch sang trái 1 vị trí. Khi đó phần tử 60000 chuyển về index 1. Lệnh gán trip_fares[2] = 65000 đã ghi đè nhầm vào phần tử 35000.</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">2</td>
      <td style="padding: 8px;">[12000, 30000, 50000, 40000]</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">3</td>
      <td style="padding: 8px;">[20000, 15000, 70000]</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (Source Code Correction)**
Viết lại mã nguồn Python 3.12 để đảm bảo các thao tác cập nhật và xóa cước phí được thực hiện đúng logic nghiệp vụ mà không làm sai lệch thông tin các chuyến đi khác.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo kịch bản kiểm thử (bảng Test Case hoàn chỉnh).
*   Mã nguồn Python đã hoàn thiện sửa lỗi.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex5`.
    Ví dụ: `HNKS25CNTT1_Core_Session10_Ex5`
## <center>Sửa lỗi tính toán dung tích ô kệ kho hàng Warehouse</center>

### **1. Mục tiêu**
*   Hiểu rõ sự khác biệt và cách hoạt động của các kiểu dữ liệu cơ bản trong Python: Chuỗi (`str`), Số nguyên (`int`), Số thực (`float`), và Logic (`bool`).
*   Làm chủ kỹ thuật ép kiểu dữ liệu (Type Casting) khi tiếp nhận dữ liệu đầu vào từ người dùng qua hàm `input()`.
*   Sử dụng thành thạo chuỗi định dạng f-string để hiển thị thông tin báo cáo chuyên nghiệp.
*   Ứng dụng tư duy toán học và toán tử logic để giải quyết bài toán nghiệp vụ mà không cần dùng đến cấu trúc điều kiện rẽ nhánh phức tạp.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản lý kho hàng (Warehouse Management System - WMS), việc tính toán chính xác dung tích còn trống của một ô kệ (Bin Location) là cực kỳ quan trọng. Hệ thống cần tự động tính toán xem sau khi xếp thêm một kiện hàng mới vào, ô kệ đó có bị quá tải (overloaded) hay không để đưa ra quyết định từ chối hoặc tiếp nhận. 

Một lập trình viên tập sự đã viết thử nghiệm một đoạn mã Python nhận đầu vào từ bàn phím để tính nhanh trạng thái ô kệ. Tuy nhiên, đoạn mã liên tục gặp lỗi sập hệ thống (TypeError) hoặc trả về các kết quả so sánh phi logic do gặp lỗi về kiểu dữ liệu.



<p align="center">
  <img src="../images/bai_01_van_dung_co_ban_1_sua_loi_tinh_toan_dung_tich_o_ke_kho_hang_warehouse_diagram.png" alt="Sơ đồ luồng nghiệp vụ" width="80%">
</p>



### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn đang gặp lỗi:

```python
# Chuỗi mô phỏng thông tin ô kệ nhập vào từ hệ thống
bin_code = "BIN-ZONEA-09"

# Nhập các thông số cấu hình ô kệ và kiện hàng mới từ thiết bị quét/bàn phím
max_volume = input("Nhập dung tích tối đa của ô kệ (m3): ")
current_volume = input("Nhập thể tích đã sử dụng hiện tại (m3): ")
new_item_volume = input("Nhập thể tích của kiện hàng mới cần xếp vào (m3): ")

# Tính toán tổng thể tích dự kiến sau khi xếp thêm kiện hàng mới
# [LỖI LOGIC]
total_volume_expected = current_volume + new_item_volume

# Tính toán dung tích còn lại của ô kệ
# [LỖI LOGIC]
remaining_volume = max_volume - total_volume_expected

# Kiểm tra xem ô kệ có bị quá tải hay không (True nếu quá tải, ngược lại là False)
# [LỖI LOGIC]
is_overloaded = total_volume_expected > max_volume

# Giả lập mã phản hồi hệ thống (HTTP Status Code)
# Nếu quá tải (True = 1) thì báo lỗi 409 (Conflict - Xung đột dung tích)
# Nếu không quá tải (False = 0) thì báo 200 (OK)
status_code = 409 * is_overloaded + 200 * (not is_overloaded)

# Xuất kết quả báo cáo trạng thái ô kệ bằng f-string
print(f"--- BÁO CÁO CẬP NHẬT Ô KỆ: {bin_code} ---")
print(f"Dung tích tối đa: {max_volume} m3")
print(f"Thể tích dự kiến sau khi xếp hàng: {total_volume_expected} m3")
print(f"Dung tích còn lại: {remaining_volume} m3")
print(f"Trạng thái quá tải (Overloaded): {is_overloaded}")
print(f"Hệ thống trả về mã (HTTP Status): {status_code}")
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo kịch bản kiểm thử (Test Cases Report)**
Học viên cần chạy thử chương trình trên với các bộ dữ liệu khác nhau và lập bảng báo cáo lỗi theo định dạng sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr>
      <th>Mã Case</th>
      <th>Dữ liệu đầu vào (Input)</th>
      <th>Kết quả thực tế từ code lỗi (Actual Output / Error)</th>
      <th>Kết quả mong muốn sau khi sửa (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>TC-01</td>
      <td>max_volume = "10.5"<br>current_volume = "5.0"<br>new_item_volume = "3.2"</td>
      <td>(Ghi lại lỗi TypeError hoặc kết quả sai ở đây)</td>
      <td>Tổng thể tích: 8.2 m3<br>Còn lại: 2.3 m3<br>Quá tải: False<br>HTTP Status: 200</td>
    </tr>
    <tr>
      <td>TC-02</td>
      <td>max_volume = "15.0"<br>current_volume = "10.0"<br>new_item_volume = "8.5"</td>
      <td>(Ghi lại lỗi TypeError hoặc kết quả sai ở đây)</td>
      <td>Tổng thể tích: 18.5 m3<br>Còn lại: -3.5 m3<br>Quá tải: True<br>HTTP Status: 409</td>
    </tr>
    <tr>
      <td>TC-03</td>
      <td>max_volume = "20"<br>current_volume = "15"<br>new_item_volume = "5"</td>
      <td>(Ghi lại lỗi TypeError hoặc kết quả sai ở đây)</td>
      <td>Tổng thể tích: 20.0 m3<br>Còn lại: 0.0 m3<br>Quá tải: False<br>HTTP Status: 200</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa đổi và hoàn thiện mã nguồn**
*   Sửa lỗi ép kiểu dữ liệu từ hàm `input()`. Do thể tích thùng hàng và ô kệ có thể chứa số thập phân, học viên bắt buộc phải ép sang kiểu số thực (`float`).
*   Sửa đổi các phép tính toán học để đảm bảo tính đúng đắn về mặt số học.
*   Căn chỉnh hệ thống in kết quả bằng f-string đẹp mắt, làm tròn kết quả số thực đến 2 chữ số thập phân (ví dụ: `{remaining_volume:.2f}`).
*   [YÊU CẦU ĐẶC BIỆT]: Không được phép sử dụng cấu trúc rẽ nhánh `if/else` (do chưa học trong Session 1). Hãy giữ nguyên cơ chế tính toán `status_code` bằng biểu thức logic/toán học dựa trên giá trị của biến boolean `is_overloaded`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích lỗi (Bảng Test Cases) và file mã nguồn Python sau khi sửa.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session01_Ex01`.
    Ví dụ: `HNKS25CNTT1_PythonCore_Session01_Ex01`
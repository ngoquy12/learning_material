## <center>[Vận dụng cơ bản 1] Sửa lỗi xử lý tọa độ chi nhánh và nhật ký tương tác CRM</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu rõ tính chất bất biến (immutability) của cấu trúc dữ liệu `Tuple` và khả năng thay đổi giá trị (mutable) của `List` thông qua chỉ số Index và cắt lát Slicing.
*   **Kỹ năng:** Đọc hiểu mã nguồn Python 3.12 legacy, phát hiện các lỗi vi phạm tính bất biến của Tuple, sửa lỗi truy cập Index và áp dụng kỹ thuật Tuple Unpacking kết hợp Swap biến trực tiếp tối ưu.
*   **Mức độ tư duy:** Vận dụng cơ bản 1 (Phân tích lỗi nghiệp vụ hiện có, lập bảng báo cáo kiểm thử và tái cấu trúc mã nguồn chạy ổn định).

### **2. Bối cảnh & Vấn đề**
Hệ thống Quản lý Quan hệ Khách hàng (CRM) của một doanh nghiệp bán lẻ đang lưu trữ thông tin hỗ trợ khách hàng theo hai cấu trúc dữ liệu chính:
1.  **Danh sách nhật ký phiên tương tác (`recent_logs`):** Dạng `List` chứa mã ID các cuộc gọi hỗ trợ gần nhất để nhân viên tư vấn cập nhật trạng thái.
2.  **Tọa độ văn phòng chi nhánh (`branch_geo`):** Dạng `Tuple` chứa cặp tọa độ GPS (Vĩ độ - Latitude, Kinh độ - Longitude) dùng cho việc định vị chính xác vị trí hỗ trợ khách hàng.

Một lập trình viên cấp thấp đã viết đoạn mã nguồn để cập nhật mã phiên tương tác bị lỗi, cắt lát trích xuất lịch sử cuộc gọi và hoán đổi vị trí tọa độ khi chi nhánh thay đổi trục định vị. Tuy nhiên, chương trình liên tục gặp lỗi sụp đổ hệ thống đột ngột (`TypeError`) và trích xuất sai phân đoạn nhật ký.



### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn legacy hiện tại đang chạy trên môi trường Python 3.12 chứa các lỗi logic và lỗi ngoại lệ:

```python
# Mã nguồn xử lý dữ liệu CRM - Lỗi vận hành hệ thống
recent_logs = [7001, 7002, 7003, 7004]
branch_geo = (10.76262, 106.66017)

# LỖI 1: Cập nhật sai vị trí index của danh sách nhật ký (yêu cầu sửa phần tử đầu tiên 7001 thành 9001)
recent_logs[1] = 9001

# LỖI 2: Cố tình ghi đè phần tử trực tiếp trong Tuple (Gây sụp đổ ứng dụng với TypeError)
branch_geo[0] = 106.66017

# LỖI 3: Cắt lát Slicing sai chỉ số để lấy 2 phần tử giữa (7002 và 7003)
sub_logs = recent_logs[1:2]

# LỖI 4: Hoán đổi tọa độ thủ công rườm rà bằng biến trung gian và sai giá trị
temp = branch_geo[0]
val_lat = branch_geo[1]
val_lng = temp

print("# Output:")
print("Danh sách log sau khi sửa:", recent_logs)
print("Phân đoạn log trung gian:", sub_logs)
print("Tọa độ mới:", branch_geo)
```

### **4. Yêu cầu đầu ra**
Học viên đóng vai trò Kỹ sư Phần mềm phụ trách khắc phục sự cố hệ thống CRM, thực hiện đầy đủ 2 phần nhiệm vụ sau:

#### **Phần 1: Báo cáo Phân tích lỗi & Bảng Test Case**
Lập bảng phân tích kiểm thử (Test Case Report) dạng bảng Markdown hoặc HTML trình bày tối thiểu 3 trường hợp thử nghiệm chứng minh các vị trí lỗi trong mã nguồn ban đầu và kết quả kỳ vọng sau khi sửa. Bảng phải tuân thủ chuẩn thuộc tính CSS hệ thống:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Mã Test Case</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Mô tả kịch bản / Đầu vào (Input)</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Kết quả lỗi thực tế (Buggy Output)</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Kết quả kỳ vọng đúng (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">TC01</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Cập nhật mã nhật ký phiên đầu tiên trong recent_logs thành 9001</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Ghi đè nhầm phần tử index 1: [7001, 9001, 7003, 7004]</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Cập nhật chính xác index 0: [9001, 7002, 7003, 7004]</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">TC02</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Cập nhật tọa độ trong Tuple branch_geo bằng gán trực tiếp index 0</td>
      <td style="border: 1px solid #ddd; padding: 8px;">TypeError: 'tuple' object does not support item assignment</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Tạo Tuple mới thông qua Unpacking và Swap biến không bị lỗi</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">TC03</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Trích xuất phân đoạn nhật ký thứ 2 và thứ 3 bằng kỹ thuật Slicing</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Chỉ lấy được 1 phần tử [7002] do chỉ số slicing [1:2]</td>
      <td style="border: 1px solid #ddd; padding: 8px;">Trích xuất chính xác 2 phần tử [7002, 7003] với chỉ số slicing [1:3]</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Mã nguồn hoàn chỉnh đã sửa lỗi**
Tái cấu trúc file mã nguồn Python (`main.py`) tuân thủ nghiêm ngặt chuẩn Python 3.12:
1.  **Sửa lỗi Index List:** Cập nhật lại chính xác phần tử đầu tiên (index `0`) của `recent_logs` thành `9001`.
2.  **Sửa lỗi Slicing List:** Cắt lát lấy đúng 2 phần tử giữa của `recent_logs` từ index 1 đến index 2 bằng chỉ số `[1:3]`.
3.  **Áp dụng Tuple Unpacking & Swap:** Giải nén `branch_geo` thành 2 biến `latitude, longitude`, thực hiện hoán đổi vị trí trực tiếp `latitude, longitude = longitude, latitude` (không dùng biến trung gian `temp`) và đóng gói lại thành Tuple mới `updated_geo`.
4.  **In đầu ra chuẩn hóa:** In ra các thông số theo định dạng kết quả mẫu bên dưới.

**Kết quả đầu ra kỳ vọng trên màn hình (Console Output):**
```text
# Output:
Phiên nhật ký sau khi sửa Index 0: [9001, 7002, 7003, 7004]
Kết quả trích xuất Slicing [1:3]: [7002, 7003]
Tọa độ sau khi Unpacking và Swap: (106.66017, 10.76262)
```

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex01`.
    Ví dụ: `HNKS25CNTT1_Core_Session08_Ex01`
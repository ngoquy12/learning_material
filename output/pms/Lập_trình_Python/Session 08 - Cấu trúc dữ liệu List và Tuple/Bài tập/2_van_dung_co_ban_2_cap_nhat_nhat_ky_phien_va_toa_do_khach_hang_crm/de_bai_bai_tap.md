## <center>[Vận dụng cơ bản 2] Cập nhật nhật ký phiên và tọa độ khách hàng CRM</center>

### **1. Mục tiêu**
*   **Hiểu và khắc phục lỗi tính bất biến (Immutability):** Nhận biết và xử lý lỗi crash ứng dụng khi cố tình thay đổi dữ liệu bên trong cấu trúc `Tuple`.
*   **Thao tác dữ liệu List & Tuple chuẩn Python 3.12:** Áp dụng kỹ thuật truy cập phần tử qua Index, cắt lát danh sách (**Slicing** `[1:3]`), giải nén dữ liệu (**Tuple Unpacking**) và hoán đổi biến (**Swap**) trực tiếp không qua biến trung gian.
*   **Rèn luyện kỹ năng kiểm thử và sửa lỗi (Debugging):** Xây dựng bảng báo cáo kịch bản kiểm thử (Test Case) và tái cấu trúc mã nguồn theo chuẩn PEP 8.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản lý quan hệ khách hàng (CRM), hệ thống cần theo dõi lịch sử 4 phiên hoạt động gần nhất của khách hàng lưu trong một danh sách `List` dạng `[session_1, session_2, session_3, session_4]` và tọa độ vị trí ưu tiên giao hàng được lưu trong một cấu trúc `Tuple` dạng `(latitude, longitude)`.

Bộ phận phát triển vừa bàn giao một đoạn mã nguồn dùng để:
1. Cập nhật mã phiên hoạt động mới nhất vào vị trí đầu tiên (`index 0`) của danh sách.
2. Trích xuất phân đoạn 2 phiên hoạt động ở giữa (`index 1` và `index 2`) bằng kỹ thuật Slicing để gửi tới hệ thống phân tích hành vi.
3. Chuẩn hóa lại cặp tọa độ bằng cách hoán đổi vị trí kinh độ/vĩ độ bị nhập ngược.

Tuy nhiên, trong quá trình vận hành thực tế, ứng dụng liên tục gặp sự cố dừng đột ngột (crash) với thông báo lỗi `TypeError`. Lập trình viên cũ đã cố gắng thay đổi trực tiếp giá trị tọa độ trong `Tuple` và hoán đổi biến bằng thủ công phức tạp. Nhiệm vụ của bạn là phân tích lỗi, lập báo cáo kiểm thử và sửa lại mã nguồn vận hành ổn định.



### **3. Mã nguồn hiện tại**

```python
def update_crm_session_and_coords(
    session_logs: list[int],
    geo_location: tuple[float, float],
    new_session_id: int
) -> tuple[list[int], list[int], tuple[float, float]]:
    """
    Cập nhật nhật ký phiên hoạt động và chuẩn hóa tọa độ giao hàng của khách hàng.
    """
    # Cập nhật phiên mới nhất vào đầu danh sách (Chưa kiểm tra tính hợp lệ của ID)
    session_logs[0] = new_session_id
    
    # Trích xuất 2 phiên lịch sử ở giữa
    sub_logs = session_logs[1:3]
    
    # LỖI NGHIỆP VỤ & CÚ PHÁP: Cố tình ghi đè giá trị phần tử của Tuple bất biến
    geo_location[0] = 10.8231
    
    # Hoán đổi tọa độ thủ công bằng biến trung gian
    temp = geo_location[0]
    lat = geo_location[1]
    lng = temp
    swapped_coords = (lat, lng)
    
    return session_logs, sub_logs, swapped_coords


# Chạy thử nghiệm gây lỗi crash ứng dụng
current_sessions = [5001, 5002, 5003, 5004]
current_location = (10.76262, 106.66017)
new_session = 9999

result_logs, middle_logs, updated_location = update_crm_session_and_coords(
    current_sessions, current_location, new_session
)
```

### **4. Yêu cầu đầu ra**

#### **Phần 1: Báo cáo phân tích & Bảng Test Case (30 điểm)**
1. Phân tích nguyên nhân kỹ thuật chi tiết vì sao dòng lệnh `geo_location[0] = 10.8231` gây ra lỗi dừng chương trình đột ngột (`TypeError`).
2. Lập bảng Báo cáo Test Case mô tả tối thiểu 3 kịch bản kiểm thử theo định dạng bảng HTML sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">STT</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Tên Kịch Bản</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Dữ Liệu Đầu Vào (Input)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Kết Quả Hiện Tại (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Kết Quả Kỳ Vọng (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">1</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Thay đổi phần tử Tuple</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">geo_location = (10.76, 106.66)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">TypeError: 'tuple' object does not support item assignment</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tạo Tuple mới thông qua Unpacking/Swap thành công</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">2</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Mã phiên không hợp lệ</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">new_session_id = -50</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Vẫn cập nhật giá trị âm vào List</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Ném ra ngoại lệ ValueError hợp lệ</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">3</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Danh sách phiên thiếu phần tử</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">session_logs = [5001, 5002]</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Cắt lát Slicing không đủ 2 phần tử</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Ném ra ngoại lệ ValueError thông báo số lượng phần tử</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (70 điểm)**
Tái cấu trúc lại hàm `update_crm_session_and_coords` tuân thủ các quy định nghiệp vụ sau:
*   [REQUIREMENT 1] **Kiểm tra dữ liệu đầu vào:**
    *   Nếu `new_session_id <= 0` hoặc không phải kiểu số nguyên `int`, ném ngoại lệ `raise ValueError("Mã phiên đăng nhập phải là số nguyên dương.")`.
    *   Nếu `len(session_logs) < 4`, ném ngoại lệ `raise ValueError("Danh sách phiên làm việc phải có ít nhất 4 phần tử.")`.
*   [REQUIREMENT 2] **Thao tác trên List:**
    *   Ghi đè giá trị phiên mới vào phần tử đầu tiên (`index 0`) của `session_logs`.
    *   Dùng kỹ thuật cắt lát danh sách (**Slicing** `[1:3]`) để tạo ra danh sách mới gồm 2 phần tử ở giữa.
*   [REQUIREMENT 3] **Thao tác trên Tuple (Không sửa trực tiếp Tuple):**
    *   Sử dụng kỹ thuật **Tuple Unpacking** để giải nén tọa độ: `lat, lng = geo_location`.
    *   Thực hiện hoán đổi vị trí trực tiếp bằng kỹ thuật **Swap**: `lat, lng = lng, lat` (Tuyệt đối KHÔNG dùng biến trung gian `temp`).
    *   Tạo Tuple tọa độ mới từ các biến đã hoán đổi và trả về kết quả.
*   [REQUIREMENT 4] Tuân thủ PEP 8, sử dụng Type Hints đầy đủ của Python 3.12. KHÔNG sử dụng các vòng lặp (`for`, `while`) hoặc các phương thức thêm/xóa phần tử List (`append`, `pop`, `remove`).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex02`.
    Ví dụ: `HNKS25CNTT1_Core_Session08_Ex02`
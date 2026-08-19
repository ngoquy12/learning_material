# <center>[Phân tích 3] Tối Ưu Hóa Dữ Liệu Chuyến Đi Hệ Thống GrabRide Bằng Thao Tác Cập Nhật Và Xóa Danh Sách</center>

### **1. Mục tiêu**
*   Phân tích chuyên sâu bài toán quản lý và xử lý dữ liệu động danh sách chuyến đi trong hệ thống đặt xe công nghệ **GrabRide**.
*   Tự thiết kế và đề xuất các phương án xử lý thao tác cập nhật giá trị phần tử qua chỉ số (index assignment) và xóa phần tử trực tiếp (`del`) trên danh sách mutable (`list`).
*   Đánh giá chi tiết ưu/nhược điểm (Trade-off) giữa các phương án xử lý duyệt chỉ số index khi kích thước danh sách bị biến đổi liên tục (`len()`).
*   Vẽ sơ đồ luồng thuật toán (Flowchart) chuẩn hóa và hiện thực hóa giải pháp tối ưu bằng ngôn ngữ Python 3.12 tuân thủ chuẩn PEP 8 và Type Hints trong phạm vi kiến thức đã học.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt xe **GrabRide**, máy chủ theo dõi ca làm việc của tài xế bằng cách ghi nhận danh sách khoảng cách di chuyển (đơn vị: km) của từng chuyến đi. Kết quả được lưu trữ bên trong một danh sách động các số thực `list[float]`.

Trong quá trình vận hành thực tế, danh sách dữ liệu này phát sinh hai vấn đề kỹ thuật dữ liệu cần xử lý:
1.  **Lỗi cảm biến định vị (GPS anomaly):** Một số chuyến đi bị ghi nhận khoảng cách âm (ví dụ: `-1.0` km) do mất tín hiệu GPS tạm thời. Theo quy định nghiệp vụ, các chuyến đi có khoảng cách âm cần được điều chỉnh/cập nhật lại về khoảng cách tối thiểu mặc định là `2.0` km tại đúng vị trí index hiện tại.
2.  **Khách hàng hủy chuyến (Canceled trip):** Các chuyến đi có khoảng cách bằng `0.0` km đại diện cho chuyến đi bị hủy. Những chuyến này cần phải bị loại bỏ hoàn toàn khỏi hệ thống bằng lệnh xóa `del`.Thách thức kỹ thuật nằm ở chỗ: Khi thực hiện câu lệnh xóa phần tử `del` trên danh sách mutable trong lúc đang duyệt, kích thước danh sách thay đổi và các phần tử phía sau sẽ dồn về trước. Nếu xử lý chỉ số index không khéo léo, chương trình sẽ gặp lỗi tràn chỉ số `IndexError` hoặc bỏ sót các phần tử `0.0` đứng liền kề nhau. Học viên cần nghiên cứu, phân tích và đưa ra giải pháp xử lý triệt để bài toán này.

### **3. Quy tắc nghiệp vụ**
*   **Dữ liệu đầu vào:** Một danh sách các số thực đại diện cho độ dài chuyến đi (km), ví dụ: `danh_sach_quang_duong: list[float] = [3.5, 0.0, 0.0, -1.5, 12.0, 0.0, 5.5, 1.8]`.
*   **Quy tắc Cập nhật (Update):** Nếu `danh_sach_quang_duong[i] < 0.0`, thực hiện cập nhật lại phần tử tại index `i` thành `2.0`.
*   **Quy tắc Xóa (Delete):** Nếu `danh_sach_quang_duong[i] == 0.0`, thực hiện xóa phần tử tại index `i` khỏi danh sách bằng câu lệnh `del`.
*   **Giới hạn công nghệ:** Chỉ được phép sử dụng các kiến thức đã học trong Session 10 và các bài trước:
    *   Cập nhật chỉ số phần tử: `danh_sach[i] = new_value`
    *   Xóa phần tử theo index: `del danh_sach[i]`
    *   Kiểm tra độ dài danh sách: `len(danh_sach)`
    *   Cấu trúc điều khiển và vòng lặp cơ bản (`if/elif/else`, `while`, `for range`).
    *   TUYỆT ĐỐI CẤM sử dụng: Các phương thức biến đổi danh sách `append()`, `pop()`, kiểu dữ liệu `dict`, `set`, `tuple`, khai báo hàm `def`, hay định nghĩa lớp `class`.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất & So sánh giải pháp (Proposal & Trade-off Report)**
*   Học viên tự nghiên cứu và đề xuất **ít nhất 2 phương án kỹ thuật khác nhau** để duyệt và xử lý biến đổi danh sách (cập nhật giá trị âm và xóa phần tử `0.0` bằng `del`) mà không vi phạm lỗi chỉ số index. *(Ví dụ: Suy nghĩ về cơ chế điều khiển biến đếm chỉ số index trong vòng lặp hoặc hướng duyệt danh sách từ trái sang phải / từ phải sang trái).*
*   Xây dựng bảng so sánh Trade-off chi tiết giữa các phương án đề xuất dựa trên 5 tiêu chí với cấu trúc HTML bên dưới:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Tiêu chí đánh giá</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án 1</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left;">Phương án 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>Độ phức tạp thời gian (Time Complexity)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>Sử dụng bộ nhớ (Memory Usage)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>Khả năng bảo trì (Maintainability)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>Độ dễ đọc & Hiểu code (Readability)</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><strong>Rủi ro sót phần tử / Tràn index</strong></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Lý giải Lựa chọn & Thiết kế Sơ đồ luồng (Justification & Flowchart)**
*   Lựa chọn 01 phương án tối ưu nhất từ các phương án đã phân tích và lập luận lý do khoa học cho sự lựa chọn này.
*   Vẽ sơ đồ luồng thuật toán (Mermaid Flowchart) biểu diễn chi tiết logic của phương án tối ưu. Tuân thủ nghiêm ngặt 5 hình dạng chuẩn:
    *   **Terminator:** Stadium `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`
    *   **Input/Output:** Hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]`
    *   **Decision:** Hình thoi `Kiểm tra điều kiện?`
    *   **Process:** Hình chữ nhật `["Thực hiện thao tác"]`
    *   **Flowline:** Mũi tên `-->` kèm nhãn `-->|Đúng|` hoặc `-->|Sai|`

#### **Phần 3: Triển khai Mã nguồn & Xử lý Trường hợp Biên (Implementation & Edge-cases)**
*   Viết đoạn mã nguồn Python 3.12 hoàn chỉnh triển khai phương án tối ưu đã chọn trong tệp `main.py`.
*   Tuân thủ chuẩn PEP 8 và Type Hints đầy đủ.
*   Kiểm thử và xử lý triệt để các trường hợp biên đặc biệt:
    *   Danh sách chứa các phần tử `0.0` đứng liên tiếp nhau (ví dụ: `[3.5, 0.0, 0.0, 4.0]`).
    *   Danh sách toàn bộ là các chuyến đi bị hủy `0.0` (ví dụ: `[0.0, 0.0, 0.0]`).
    *   Danh sách không có chuyến đi nào bị hủy (ví dụ: `[1.2, 5.0, 3.2]`).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex12`.
    Ví dụ: `HNKS25CNTT1_Core_Session10_Ex12`

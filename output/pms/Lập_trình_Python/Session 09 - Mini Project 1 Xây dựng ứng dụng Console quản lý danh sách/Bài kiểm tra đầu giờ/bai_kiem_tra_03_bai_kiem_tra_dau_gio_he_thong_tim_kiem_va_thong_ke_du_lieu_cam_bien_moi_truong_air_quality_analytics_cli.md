## <center>BÀI KIỂM TRA ĐẦU GIỜ: HỆ THỐNG TÌM KIẾM VÀ THỐNG KÊ DỮ LIỆU CẢM BIẾN MÔI TRƯỜNG (AIR QUALITY ANALYTICS CLI)</center>

### **1. Mục tiêu**
Bài kiểm tra đánh giá khả năng vận dụng kiến thức lập trình Python cốt lõi để xây dựng các thao tác **Tìm kiếm nâng cao, Lọc dữ liệu & Thống kê (Search, Filtering & Analytics)** trên cấu trúc dữ liệu danh sách (`List` & `Tuple`). 

Học viên cần triển khai chương trình điều khiển Console (CLI) xử lý tập dữ liệu trạm quan trắc chất lượng không khí (Air Quality Index - AQI), áp dụng các câu lệnh điều kiện (`if-elif-else`), vòng lặp (`for`/`while`), ép kiểu dữ liệu và xử lý lỗi ngoại lệ nhập xuất cơ bản.

---

### **2. Yêu cầu**

 Cho sẵn tập dữ liệu ban đầu lưu trữ thông tin các trạm cảm biến dưới dạng danh sách các Tuple (`sensor_records`):
```python
sensor_records = [
    (101, "Center District", 155, 32.5),
    (102, "North Park", 45, 28.0),
    (103, "Industrial Zone", 210, 35.2),
    (104, "South Lake", 85, 30.1),
    (105, "West Suburb", 120, 29.4)
]
# Định dạng mỗi tuple: (station_id, station_name, aqi_value, temperature)
```

Học viên triển khai mã nguồn procedural thực hiện các thành phần chức năng chi tiết trong bảng sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 25%;">Tên Chức năng / Thành phần</th>
      <th style="width: 20%;">Đầu vào / Tham số</th>
      <th style="width: 35%;">Logic xử lý & Quy tắc</th>
      <th style="width: 20%;">Đầu ra / Giá trị trả về</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <b>[Tìm kiếm & Lọc trạm đo theo ngưỡng AQI]</b><br>
        <code>filter_stations_by_aqi</code>
      </td>
      <td>
        - Danh sách dữ liệu: <code>sensor_records</code><br>
        - Nhập từ bàn phím: <code>min_aqi_threshold</code> (int/float)
      </td>
      <td>
        - Yêu cầu người dùng nhập ngưỡng chỉ số AQI tối thiểu cần lọc.<br>
        - Xử lý ngoại lệ <code>ValueError</code> nếu người dùng nhập dữ liệu không phải định dạng số nguyên/số thực hợp lệ.<br>
        - Duyệt danh sách <code>sensor_records</code> qua vòng lặp <code>for</code>.<br>
        - Đưa ra danh sách trạm có <code>aqi_value >= min_aqi_threshold</code>. Nếu không có trạm nào thỏa mãn, thông báo không tìm thấy kết quả.
      </td>
      <td>
        In danh sách các trạm thỏa mãn ra màn hình Console (Mã trạm, Tên trạm, Chỉ số AQI, Nhiệt độ) hoặc thông báo lỗi nhập liệu rõ ràng.
      </td>
    </tr>
    <tr>
      <td>
        <b>[Thống kê & Phân cấp mức độ ô nhiễm]</b><br>
        <code>analyze_pollution_statistics</code>
      </td>
      <td>
        - Danh sách dữ liệu: <code>sensor_records</code>
      </td>
      <td>
        - Khởi tạo các biến tích lũy và đếm:<br>
          + <code>total_aqi = 0</code><br>
          + <code>safe_count = 0</code> (AQI <= 50)<br>
          + <code>warning_count = 0</code> (51 <= AQI <= 150)<br>
          + <code>hazard_count = 0</code> (AQI > 150)<br>
          + <code>max_aqi_record = None</code><br>
        - Duyệt qua tập dữ liệu <code>sensor_records</code> bằng vòng lặp <code>for</code> để tính tổng điểm AQI, xác định trạm có AQI cao nhất, và phân loại vào các biến đếm.<br>
        - Tính AQI trung bình: <code>average_aqi = total_aqi / len(sensor_records)</code>.
      </td>
      <td>
        In báo cáo thống kê lên Console gồm:<br>
        - AQI trung bình toàn hệ thống (làm tròn 2 chữ số thập phân).<br>
        - Thông tin trạm ô nhiễm nhất (Mã, Tên, AQI).<br>
        - Số lượng trạm phân theo 3 mức độ (An toàn / Cảnh báo / Nguy hại).
      </td>
    </tr>
  </tbody>
</table>

> **LƯU Ý CẤM (FORBIDDEN SCOPE):** 
> - **TUYỆT ĐỐI CẤM** viết hàm tự định nghĩa (`def`), tạo lớp (`class`), dùng Dictionary (`dict`), tập hợp (`set`), hoặc thư viện bên thứ ba.
> - Xử lý toàn bộ yêu cầu thông qua các câu lệnh tuần tự, vòng lặp và câu lệnh điều kiện trực tiếp trong luồng chính của chương trình Python.

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Điểm tối đa |
| :--- | :--- | :--- |
| 1 | **Khởi tạo & Quản lý dữ liệu:** Khai báo danh sách dữ liệu `List[Tuple]` đúng cấu trúc mẫu, truy xuất phần tử chính xác qua chỉ số Index (Indexing). | **2.0 điểm** |
| 2 | **Chức năng Lọc dữ liệu (`filter_stations_by_aqi`):** Nhận input, bắt lỗi `ValueError` thành công, lặp duyệt và lọc đúng các trạm có AQI đạt ngưỡng. | **3.5 điểm** |
| 3 | **Chức năng Thống kê (`analyze_pollution_statistics`):** Tính chính xác AQI trung bình, tìm trạm có AQI lớn nhất và đếm đúng số lượng trạm theo 3 cấp độ ô nhiễm. | **3.5 điểm** |
| 4 | **Chuẩn mã nguồn:** Đặt tên biến 100% Tiếng Anh chuẩn `snake_case` (VD: `sensor_records`, `min_aqi_threshold`), mã nguồn định dạng chuẩn PEP 8. | **1.0 điểm** |
| **TỔNG ĐIỂM** | | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**

1. Tạo file script Python đặt tên theo quy chuẩn: `main.py`.
2. Kiểm thử chương trình trên Terminal/Console trước khi tiến hành nộp bài.
3. Thực hiện push mã nguồn lên repository GitHub cá nhân và nộp đường dẫn (URL) bài làm lên hệ thống quản lý học tập.
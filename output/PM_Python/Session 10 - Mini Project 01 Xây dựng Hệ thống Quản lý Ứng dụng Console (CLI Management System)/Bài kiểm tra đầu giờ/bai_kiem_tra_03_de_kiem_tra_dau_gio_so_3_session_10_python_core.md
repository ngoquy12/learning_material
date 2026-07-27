## <center>Hệ Thống Phân Tích Chiến Dịch Quảng Cáo (Marketing Campaign Analytics CLI)</center>

### **1. Mục tiêu**
Đánh giá khả năng của học viên trong việc áp dụng các cấu trúc dữ liệu cơ bản (List, Dictionary), vòng lặp, câu điều kiện, cấu trúc hàm và xử lý ngoại lệ cơ bản (như chia cho 0) trong Python nhằm xây dựng các tính năng tìm kiếm, lọc và thống kê dữ liệu trên môi trường Console (CLI).

---

### **2. Yêu cầu**

Học viên giả định có một danh sách dữ liệu đầu vào chứa thông tin của các chiến dịch quảng cáo dưới dạng danh sách các từ điển (`list` of `dict`). Mỗi từ điển biểu diễn một chiến dịch quảng cáo có cấu trúc như sau:
```python
campaigns = [
    {"id": 101, "name": "Summer Flash Sale", "budget": 1500.0, "clicks": 12000, "conversions": 450, "status": "active"},
    {"id": 102, "name": "New Year Promotion", "budget": 3000.0, "clicks": 25000, "conversions": 1250, "status": "completed"},
    {"id": 103, "name": "Black Friday Tech", "budget": 5000.0, "clicks": 45000, "conversions": 3150, "status": "active"},
    {"id": 104, "name": "Back to School", "budget": 800.0, "clicks": 0, "conversions": 0, "status": "paused"},
    {"id": 105, "name": "Christmas Gift Guide", "budget": 2000.0, "clicks": 18000, "conversions": 720, "status": "active"}
]
```

Học viên cần xây dựng các hàm phục vụ chức năng tìm kiếm, lọc và thống kê theo đặc tả sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse; border: 1px solid #ccc;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 20%;">Tên chức năng / Hàm</th>
      <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 20%;">Tham số / Input</th>
      <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 40%;">Logic xử lý</th>
      <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 20%;">Output / Kết quả trả về</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #ccc;">
        <b>Lọc chiến dịch nâng cao</b><br><code>filter_campaigns()</code>
      </td>
      <td style="padding: 8px; border: 1px solid #ccc;">
        - <code>campaigns</code> (list)<br>
        - <code>status</code> (str, mặc định là <code>None</code>)<br>
        - <code>min_budget</code> (float, mặc định là <code>0.0</code>)
      </td>
      <td style="padding: 8px; border: 1px solid #ccc;">
        Lọc danh sách chiến dịch thỏa mãn đồng thời cả 2 điều kiện:<br>
        1. Nếu tham số <code>status</code> được cung cấp (khác <code>None</code>), trạng thái của chiến dịch phải trùng khớp với <code>status</code> (không phân biệt chữ hoa, chữ thường).<br>
        2. Ngân sách (<code>budget</code>) của chiến dịch phải lớn hơn hoặc bằng <code>min_budget</code>.
      </td>
      <td style="padding: 8px; border: 1px solid #ccc;">
        <code>list</code> chứa các chiến dịch (dict) thỏa mãn điều kiện.
      </td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ccc;">
        <b>Phân tích hiệu suất chiến dịch</b><br><code>calculate_analytics()</code>
      </td>
      <td style="padding: 8px; border: 1px solid #ccc;">
        - <code>campaigns</code> (list)
      </td>
      <td style="padding: 8px; border: 1px solid #ccc;">
        Tính toán các thông số tổng hợp từ danh sách truyền vào bao gồm:<br>
        1. Tổng ngân sách (<code>total_budget</code>) của các chiến dịch.<br>
        2. Tổng số lượt nhấp chuột (<code>total_clicks</code>).<br>
        3. Tổng số lượt chuyển đổi (<code>total_conversions</code>).<br>
        4. Tỉ lệ chuyển đổi trung bình (<code>average_conversion_rate</code>) tính bằng công thức:<br>
        <code>(Tổng conversions / Tổng clicks) * 100</code>.<br>
        Lưu ý: Phải xử lý ngoại lệ chia cho 0 (<code>ZeroDivisionError</code>) nếu <code>total_clicks</code> bằng 0 thì tỉ lệ chuyển đổi trung bình trả về <code>0.0</code>.
      </td>
      <td style="padding: 8px; border: 1px solid #ccc;">
        Một <code>dict</code> chứa các kết quả thống kê có các key:<br>
        - <code>"total_budget"</code> (float)<br>
        - <code>"total_clicks"</code> (int)<br>
        - <code>"total_conversions"</code> (int)<br>
        - <code>"avg_conversion_rate"</code> (float, làm tròn 2 chữ số thập phân)
      </td>
    </tr>
  </tbody>
</table>

#### **Yêu cầu triển khai luồng chạy giao diện Console CLI:**
1. Khởi tạo danh sách dữ liệu mẫu như mô tả.
2. Thực hiện gọi hàm lọc chiến dịch hoạt động (`active`) có ngân sách tối thiểu từ `1000.0` trở lên và in kết quả ra màn hình.
3. Chạy hàm phân tích dữ liệu trên danh sách đã lọc được và in kết quả báo cáo dưới dạng định dạng trực quan trực tiếp lên màn hình Console.

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Trọng số điểm |
|---|---|---|
| 1 | Viết hàm `filter_campaigns` đúng logic lọc theo cả 2 tham số (bao gồm chuẩn hóa chữ hoa/chữ thường cho trạng thái). | 4.0 điểm |
| 2 | Viết hàm `calculate_analytics` tính chính xác các chỉ số và xử lý triệt để lỗi chia cho 0 khi dữ liệu click bằng 0. | 4.0 điểm |
| 3 | Triển khai chương trình chạy thử nghiệm, in kết quả hiển thị một cách rõ ràng và định dạng đẹp trên Console. | 2.0 điểm |
| - | **Tổng điểm** | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**
1. Đường dẫn tới kho lưu trữ GitHub chứa mã nguồn Python của bài làm.
2. Ảnh chụp màn hình kết quả chạy chương trình trên màn hình Console CLI.
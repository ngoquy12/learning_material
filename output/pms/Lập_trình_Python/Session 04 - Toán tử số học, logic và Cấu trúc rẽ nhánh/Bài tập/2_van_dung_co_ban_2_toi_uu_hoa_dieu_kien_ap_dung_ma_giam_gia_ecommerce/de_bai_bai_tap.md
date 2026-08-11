## <center>[Vận dụng cơ bản 2] Tối ưu hóa điều kiện áp dụng mã giảm giá E-commerce</center>

### **1. Mục tiêu**

- Phát hiện và phân tích các hạn chế của đoạn mã nguồn mắc lỗi lồng ghép điều kiện quá sâu (Arrow Anti-Pattern) và vi phạm quy chuẩn PEP 8.
- Vận dụng các toán tử logic (`and`, `or`, `not`) kết hợp cấu trúc rẽ nhánh phẳng (`if / elif / else`) để tối ưu mã nguồn nghiệp vụ thương mại điện tử.
- Xây dựng bảng báo cáo kiểm thử (Test Case Report Table) để đánh giá các kịch bản đầu vào của hệ thống xác thực mã giảm giá.

### **2. Bối cảnh & Vấn đề**

Trong phân hệ thanh toán (Checkout Subsystem) của một nền tảng E-commerce, hệ thống cần kiểm tra điều kiện để áp dụng mã giảm giá đặc biệt `"VIP_SUMMER"` cho đơn hàng.

Quy tắc áp dụng mã giảm giá như sau:

1. Độ tuổi của khách hàng phải từ 18 đến 60 tuổi (bao gồm cả 18 và 60).
2. Số lượng sản phẩm trong đơn hàng phải từ 2 sản phẩm trở lên.
3. Khách hàng phải thỏa mãn một trong hai điều kiện: là tài khoản VIP (`is_vip = True`) HOẶC có tổng giá trị đơn hàng từ 2,000,000 VNĐ trở lên.

Đội ngũ kỹ thuật nhận được đoạn mã legacy từ hệ thống cũ. Đoạn mã này bị phàn nàn là rất khó đọc, thụt lề sai quy chuẩn, đặt tên biến ngắn không rõ nghĩa và lồng các câu lệnh `if` quá sâu khiến công việc bảo trì gặp nhiều khó khăn.

### **3. Mã nguồn hiện tại**

```python
# Mã nguồn legacy vi phạm quy chuẩn PEP 8 và mắc lỗi Arrow Anti-Pattern
v=True
val=1500000
a=17
cnt=1

if a>=18:
  if a<=60:
    if cnt>=2:
      if v==True:
        print("Chấp nhận: Áp dụng mã giảm giá VIP_SUMMER")
      else:
        if val>=2000000:
          print("Chấp nhận: Áp dụng mã giảm giá VIP_SUMMER")
        else:
          print("Từ chối: Không đủ điều kiện VIP hoặc giá trị đơn hàng")
    else:
      print("Từ chối: Số lượng sản phẩm phải từ 2 trở lên")
  else:
    print("Từ chối: Độ tuổi không phù hợp")
else:
  print("Từ chối: Độ tuổi không phù hợp")
```

### **4. Yêu cầu bài toán**

Học viên thực hiện các yêu cầu sau:

#### **Phần 1: Lập bảng báo cáo kiểm thử (Test Case Report Table)**

Xây dựng bảng kiểm thử gồm tối thiểu 3 trường hợp (test cases) để minh họa hoạt động của chương trình với các bộ dữ liệu khác nhau.
Yêu cầu định dạng bảng HTML chuẩn:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr>
      <th style="text-align: center; padding: 8px;">STT</th>
      <th style="text-align: left; padding: 8px;">Dữ liệu đầu vào (Input)</th>
      <th style="text-align: left; padding: 8px;">Kết quả từ mã legacy (Buggy Output)</th>
      <th style="text-align: left; padding: 8px;">Kết quả mong đợi (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center; padding: 8px;">1</td>
      <td style="padding: 8px;">a = 17, cnt = 2, v = True, val = 3000000</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="text-align: center; padding: 8px;">2</td>
      <td style="padding: 8px;">a = 25, cnt = 1, v = True, val = 2500000</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="text-align: center; padding: 8px;">3</td>
      <td style="padding: 8px;">a = 30, cnt = 3, v = False, val = 1500000</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Tối ưu hóa và chuẩn hóa mã nguồn**

Viết lại đoạn mã nguồn trên đảm bảo các tiêu chí:

1. **Phẳng hóa cấu trúc (Flattening):** Loại bỏ hoàn toàn việc lồng các câu lệnh `if` quá 2 cấp. Sử dụng kết hợp các toán tử logic `and`, `or`, `not` cùng cấu trúc `if / elif / else`.
2. **Chuẩn hóa PEP 8:**
   - Đặt lại tên biến theo quy tắc `snake_case` minh bạch nghĩa (ví dụ: `age`, `order_value`, `is_vip`, `item_count`).
   - Tuân thủ khoảng trắng xung quanh toán tử gán, toán tử so sánh.
   - Thụt lề chuẩn 4 khoảng trắng (4 spaces per indentation level).

#### **Phần 3: Trả lời câu hỏi ngắn**

Giải thích ngắn gọn (từ 3 - 5 dòng): Tại sao hiện tượng Arrow Anti-Pattern (tháp rẽ nhánh) lại gây nguy hiểm cho việc bảo trì mã nguồn trong các dự án phần mềm thực tế?

### **5. Yêu cầu nộp bài**

Học viên cần nộp:

- Phần phân tích/báo cáo và mã nguồn triển khai.
- Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex02`.
  Ví dụ: `HNKS25CNTT1_Core_Session04_Ex02`

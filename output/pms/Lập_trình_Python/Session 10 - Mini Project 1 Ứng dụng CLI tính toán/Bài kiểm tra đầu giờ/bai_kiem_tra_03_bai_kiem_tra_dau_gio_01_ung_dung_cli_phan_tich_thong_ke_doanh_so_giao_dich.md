## <center>Công cụ Phân tích Doanh số & Thống kê Giao dịch CLI (CLI Sales Search & Analytics Tool)</center>

### **1. Mục tiêu**
- **Kiến thức & Kỹ năng:** Ôn tập cú pháp Python cơ bản, câu lệnh điều kiện `if/elif/else`, vòng lặp `while`, xử lý chuỗi và kỹ thuật tích lũy dữ liệu trực tiếp trong luồng CLI.
- **Tư duy lập trình:** Xây dựng tư duy xử lý dữ liệu dòng chảy (stream processing) sử dụng các biến tích lũy thay vì lưu trữ bằng danh sách; thực hành kiểm soát ngoại lệ nhập liệu (`try-except`) chuẩn ứng dụng Console.
- **Thời lượng làm bài:** 15 - 20 phút.

---

### **2. Yêu cầu**

Doanh nghiệp cần một công cụ Console CLI đơn giản để bộ phận kế toán nhập danh sách doanh số các giao dịch trong ca làm việc, thực hiện lọc các giao dịch đạt ngưỡng và thống kê các chỉ số kinh doanh cơ bản.

**CẤM SỬ DỤNG:** `List` (Danh sách), `Hàm` (`def`), `OOP` (`class`), `File` (`open`). Toàn bộ chương trình viết dưới dạng kịch bản chạy tuần tự trên luồng chính.

Chi tiết quy cách kỹ thuật và logic xử lý của các thành phần trong chương trình được tả cụ thể trong bảng dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 22%;">Thành phần / Logic</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 22%;">Dữ liệu đầu vào</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 36%;">Quy tắc & Logic xử lý</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 20%;">Kết quả đầu ra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Nhập Dữ Liệu Giao Dịch]</b><br>
        <code>transaction_input_step</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>transaction_amount_str</code> (Chuỗi nhập từ bàn phím)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Sử dụng vòng lặp <code>while True</code> để cho phép người dùng nhập giá trị giao dịch liên tục.<br>
        2. Nếu người dùng nhập <code>"stop"</code> hoặc <code>"STOP"</code>, thoát khỏi vòng lặp nhập liệu.<br>
        3. Sử dụng <code>try-except ValueError</code> để ép kiểu <code>float</code>. Nếu nhập sai định dạng số (và không phải <code>"stop"</code>), in thông báo lỗi và yêu cầu nhập lại.<br>
        4. Kiểm tra nếu giá trị <code>transaction_amount &lt;= 0</code>, hiển thị thông báo "Doanh số phải lớn hơn 0" và bỏ qua lượt nhập này.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Cập nhật các biến tích lũy: <code>total_sales</code>, <code>transaction_count</code>, <code>max_transaction</code>, <code>min_transaction</code>.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Lọc & Phân Tích Ngưỡng]</b><br>
        <code>search_and_filter_step</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>search_threshold</code> (Kiểu <code>float</code>)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Sau khi dừng nhập danh sách giao dịch, yêu cầu người dùng nhập một giá trị ngưỡng doanh số <code>search_threshold</code> để lọc.<br>
        2. Trong quá trình nhập chuỗi dữ liệu ban đầu, chương trình đồng thời kiểm tra nếu <code>transaction_amount &gt;= search_threshold</code> thì tăng biến đếm <code>filtered_count</code> lên 1.<br>
        <i>(Lưu ý: Hỏi người dùng nhập <code>search_threshold</code> trước hoặc ngay sau khi bắt đầu xử lý tính toán)</i>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Biến đếm <code>filtered_count</code> biểu thị số lượng giao dịch đạt hoặc vượt ngưỡng.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Thống Kê & Hiển Thị Report]</b><br>
        <code>analytics_output_step</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Các biến tổng hợp trong suốt quá trình chạy.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Kiểm tra nếu <code>transaction_count == 0</code>: In ra "Chưa có giao dịch hợp lệ nào được ghi nhận!".<br>
        2. Nếu <code>transaction_count &gt; 0</code>, thực hiện tính toán:<br>
        - Doanh số trung bình: <code>average_sales = total_sales / transaction_count</code><br>
        - Tỷ lệ giao dịch vượt ngưỡng: <code>filtered_ratio = (filtered_count / transaction_count) * 100</code><br>
        3. In báo cáo tổng hợp ra màn hình Console định dạng rõ ràng.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Báo cáo thống kê chi tiết in ra Console (Tổng doanh thu, Trung bình, Giá trị Max, Min, Tỷ lệ vượt ngưỡng).
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

Chương trình được chấm theo thang điểm **10.0**, phân bổ chi tiết như sau:

| STT | Tiêu chí đánh giá | Điểm tối đa |
| :--- | :--- | :--- |
| 1 | **Luồng nhập liệu CLI & Dừng hợp lệ:** Sử dụng vòng lặp `while`, dừng khi nhập `"stop"`/`"STOP"`. | **2.0 điểm** |
| 2 | **Xử lý ngoại lệ & Kiểm soát đầu vào:** Xử lý `ValueError` khi người dùng nhập chuỗi không phải số; từ chối số `<= 0`. | **2.0 điểm** |
| 3 | **Thuật toán tích lũy & Lọc dữ liệu:** Tích lũy đúng tổng, đếm số lượng, xác định `max_transaction`, `min_transaction` và đếm giao dịch vượt ngưỡng `search_threshold` mà **KHÔNG** dùng `List`. | **3.0 điểm** |
| 4 | **Tính toán thống kê & Hiển thị:** Tính chính xác giá trị trung bình, tỷ lệ %, định dạng đầu ra Console chuyên nghiệp. | **2.0 điểm** |
| 5 | **Chuẩn mực mã nguồn & Phạm vi:** Đặt tên biến 100% Tiếng Anh snake_case (`total_sales`, `transaction_count`...), tuân thủ tuyệt đối quy định **KHÔNG** dùng `def`, `list`, `class`, `file`. | **1.0 điểm** |

---

### **4. Yêu cầu nộp bài**

- Học viên tạo tệp mã nguồn Python theo cấu trúc tên file chuẩn: `main.py` hoặc `sales_analytics.py`.
- Tiến hành đẩy mã nguồn lên kho chứa GitHub cá nhân (GitHub Repository) theo hướng dẫn:
  ```bash
  git add .
  git commit -m "solution: complete entry test session 10 - sales analytics cli"
  git push origin main
  ```
- Dán đường dẫn (URL) bài nộp trên GitHub vào hệ thống LMS trước khi hết thời gian làm bài.
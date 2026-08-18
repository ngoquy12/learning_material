## <center>[Vận dụng cơ bản 5] Sửa lỗi tính phí và đếm số lượng trong vòng lặp quét sách thư viện</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu rõ cơ chế điều khiển luồng lặp trong Python với cấu trúc `for...in range()`, câu lệnh `continue`, `break` và khối `else` đi kèm vòng lặp.
*   **Kỹ năng:** Phân tích thứ tự thực thi câu lệnh (code tracing), phát hiện lỗi logic khi đặt vị trí tính toán trước câu lệnh điều hướng `continue`, và tiến hành sửa lỗi mã nguồn theo đúng nghiệp vụ.
*   **Thái độ:** Rèn luyện tư duy cẩn trọng đối với luồng dữ liệu và vị trí cập nhật trạng thái biến trong các hệ thống xử lý hàng loạt.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ xử lý kiểm kê và duyệt mượn tài liệu của **Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS)**, hệ thống thực hiện quét tự động một dải mã sách (dùng hàm `range(start_id, end_id)`) để tính phí kiểm định và ghi nhận số sách xử lý an toàn.

Mô hình nghiệp vụ quy định cụ thể như sau:
1. Mỗi sách xử lý thành công được ghi nhận tăng số lượng sách an toàn thêm `1` và cộng phí kiểm định `5.000 VNĐ` vào tổng chi phí (`total_processing_fee`).
2. Nếu mã sách là `4` (mã bị mờ/hỏng nhãn barcode), hệ thống cần đưa ra thông báo và sử dụng `continue` để bỏ qua. Mã sách bị bỏ qua này **TUYỆT ĐỐI KHÔNG** được tính vào số lượng sách xử lý thành công và **KHÔNG** được cộng phí kiểm định.
3. Nếu mã sách là `8` (sách bị báo mất hoặc cảnh báo gian lận), hệ thống cần phát cảnh báo và sử dụng `break` để dừng khẩn cấp tiến trình.
4. Khi vòng lặp duyệt hết toàn bộ danh sách mà không bị kích hoạt dừng khẩn cấp (`break`), khối `else` của vòng lặp sẽ thực thi để xuất báo cáo tổng kết.

**Vấn đề phát sinh:** Thủ thư phản ánh rằng khi quét danh sách mã sách có chứa mã bị lỗi (mã `4`), hệ thống vẫn tự động cộng thêm `5.000 VNĐ` tiền phí và tăng số lượng sách đã xử lý. Điều này khiến cho báo cáo thống kê tài chính và số lượng kiểm kê ở cuối ngày bị sai lệch nghiêm trọng so với thực tế.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn Python đang chạy trên hệ thống gặp sự cố logic:

```python
# Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS)
# Phân hệ: Kiểm định và quét mã sách hàng loạt

start_id = 1
end_id = 7
total_processing_fee = 0
scanned_count = 0

print("--- BẮT ĐẦU TIẾN TRÌNH KIỂM ĐỊNH MÃ SÁCH ---")

for book_id in range(start_id, end_id):
    # Cập nhật số lượng và tính phí xử lý
    total_processing_fee += 5000
    scanned_count += 1

    if book_id == 4:
        print("Mã sách", book_id, "bị hỏng nhãn barcode -> Bỏ qua")
        continue

    if book_id == 8:
        print("CẢNH BÁO: Mã sách", book_id, "bị báo mất -> DỪNG KHẨN CẤP!")
        break

    print("Xử lý thành công mã sách:", book_id)
else:
    print("--- BÁO CÁO KIỂM ĐỊNH HOÀN THÀNH ---")
    print("Tổng số sách xử lý an toàn:", scanned_count)
    print("Tổng phí kiểm định ghi nhận:", total_processing_fee, "VNĐ")
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo phân tích vết (Code Tracing & Bug Discovery)**
Học viên thực hiện chạy vết đoạn mã nguồn trên, xác định dòng mã gây ra lỗi logic và hoàn thành bảng báo cáo Test Case dưới đây vào bài nộp. 

*Lưu ý: Dòng đầu tiên (STT 1) đã được điền mẫu để hướng dẫn. Học viên cần phân tích và hoàn thiện các dòng còn lại (thay thế các dấu `...`).*

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="text-align: left;">Kết quả thực tế từ mã lỗi (Buggy Output)</th>
      <th style="text-align: left;">Kết quả kỳ vọng đúng (Expected Output)</th>
      <th style="text-align: center;">Dòng code gây lỗi</th>
      <th style="text-align: left;">Giải thích nguyên nhân logic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td><code>start_id = 1</code><br/><code>end_id = 6</code></td>
      <td>Số sách: 5<br/>Tổng phí: 25.000 VNĐ</td>
      <td>Số sách: 4<br/>Tổng phí: 20.000 VNĐ</td>
      <td style="text-align: center;">Dòng 11, 12</td>
      <td>Cộng <code>total_processing_fee</code> và <code>scanned_count</code> trước câu lệnh <code>continue</code> nên mã sách 4 dù bị bỏ qua vẫn bị tính phí.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td><code>start_id = 3</code><br/><code>end_id = 6</code></td>
      <td>...</td>
      <td>...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td><code>start_id = 1</code><br/><code>end_id = 9</code></td>
      <td>...</td>
      <td>...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa đổi và hoàn thiện mã nguồn (Source Code Correction)**
*   Tiến hành sửa mã nguồn Python để đảm bảo đúng quy tắc nghiệp vụ: Chỉ những sách không bị lỗi (không bị `continue` hay `break`) mới được cộng phí `5.000 VNĐ` và tăng biến đếm `scanned_count`.
*   Tuân thủ nghiêm ngặt phạm vi kiến thức đã học (chỉ dùng `for`, `range`, `if/elif/else`, `break`, `continue` và các biến đơn giản; **KHÔNG** sử dụng hàm `def`, cấu trúc dữ liệu List/Dict hay vòng lặp `while`).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex5`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 08_Ex5`
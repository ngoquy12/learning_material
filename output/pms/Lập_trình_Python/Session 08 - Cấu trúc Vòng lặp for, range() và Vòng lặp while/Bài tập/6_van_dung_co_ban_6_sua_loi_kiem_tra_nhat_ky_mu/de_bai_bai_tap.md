## <center>[Vận dụng cơ bản 6] Sửa lỗi kiểm tra nhật ký mượn sách bằng vòng lặp và điều khiển luồng</center>

### **1. Mục tiêu**
* Áp dụng cấu trúc vòng lặp `for` kết hợp hàm `range()` để duyệt qua danh sách các mã lượt mượn sách theo tiến trình.
* Sử dụng thành thạo các câu lệnh điều khiển luồng `break`, `continue` và khối `else` của vòng lặp `for` để xử lý các sự kiện nghiệp vụ trong thư viện.
* Phát hiện và khắc phục các lỗi logic về thứ tự thực thi câu lệnh làm sai lệch biến đếm và luồng thông báo của hệ thống LIBRARY_WMS.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ Quản lý Mượn trả Sách Thư viện (LIBRARY_WMS), hệ thống được thiết lập một tiến trình quét tự động cuối ngày để kiểm tra một lô các lượt mượn sách (mã lượt mượn từ 101 đến 110).

Quy tắc kiểm tra nghiệp vụ của hệ thống được quy định như sau:
* Tiến trình quét duyệt qua lần lượt từng mã lượt mượn trong khoảng từ 101 đến 110.
* **Quy tắc 1 (Bỏ qua lượt lỗi nhẹ):** Nếu lượt mượn có mã **104** (do thiếu thông tin vị trí kệ sách), hệ thống phải in thông báo bỏ qua và dùng `continue` để chuyển sang lượt tiếp theo. Lượt mượn này **không được tính** vào số lượng lượt mượn hợp lệ.
* **Quy tắc 2 (Dừng khẩn cấp khi rủi ro):** Nếu lượt mượn có mã **108** (được đánh dấu có rủi ro thất thoát tài liệu quý hiếm), hệ thống phải lập tức phát cảnh báo nguy hiểm và dùng `break` để chấm dứt ngay toàn bộ tiến trình quét.
* **Quy tắc 3 (Báo cáo hoàn thành):** Nếu tiến trình quét duyệt hết tất cả các mã mà không gặp sự cố dừng khẩn cấp (`break`), khối `else` của vòng lặp `for` sẽ thực thi để in thông báo xác nhận toàn bộ lô mượn an toàn.

**Vấn đề ghi nhận:** Cán bộ quản lý thư viện phản ánh rằng hệ thống đang gặp 2 lỗi bất thường:
1. Tổng số lượt mượn hợp lệ bị báo cáo sai (mã 104 bị bỏ qua nhưng vẫn bị cộng vào tổng số lượt mượn thành công).
2. Khi gặp lượt mượn rủi ro 108, hệ thống vẫn in dòng chữ "Xử lý thành công lượt mượn mã số: 108" trước khi đưa ra thông báo cảnh báo và dừng hệ thống.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn Python hiện tại do lập trình viên thử việc triển khai:

```python
# Hệ thống Quản lý Mượn trả Sách Thư viện (LIBRARY_WMS)
# Tiến trình kiểm tra nhật ký mượn sách tự động

start_id = 101
end_id = 110
valid_count = 0

print("--- BẮT ĐẦU QUÉT NHẬT KÝ MƯỢN SÁCH ---")

for loan_id in range(start_id, end_id + 1):
    # Cập nhật số lượng lượt mượn đã xử lý
    valid_count += 1

    # Kiểm tra trường hợp thiếu thông tin kệ sách
    if loan_id == 104:
        print("Lượt mượn", loan_id, "thiếu thông tin kệ sách -> Bỏ qua")
        continue

    # Thông báo xử lý lượt mượn thành công
    print("Xử lý thành công lượt mượn mã số:", loan_id)

    # Kiểm tra trường hợp cảnh báo thất thoát sách
    if loan_id == 108:
        print("CẢNH BÁO: Lượt mượn", loan_id, "có rủi ro thất thoát -> DỪNG KHẨN CẤP!")
        break
else:
    print("TẤT CẢ LƯỢT MƯỢN ĐÃ ĐƯỢC KIỂM KÊ AN TOÀN!")

print("Tổng số lượt mượn hợp lệ ghi nhận:", valid_count)
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Phát hiện lỗi logic (Báo cáo Test Case)**
Học viên đọc hiểu mã nguồn, đối chiếu với quy tắc nghiệp vụ và hoàn thành bảng theo dõi lỗi (Test Case Report Table) dưới đây. Bảng phải chỉ rõ dòng code gây lỗi và nguyên nhân logic làm hệ thống sai lệch.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 5%;">STT</th>
      <th style="width: 20%;">Dữ liệu đầu vào (Mã lượt mượn)</th>
      <th style="width: 25%;">Kết quả thực tế (Mã hiện tại)</th>
      <th style="width: 25%;">Kết quả kỳ vọng (Đúng nghiệp vụ)</th>
      <th style="width: 10%;">Dòng code gây lỗi</th>
      <th style="width: 15%;">Giải thích nguyên nhân</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Mã 104 (Thiếu vị trí kệ sách)</td>
      <td>In thông báo bỏ qua nhưng biến valid_count vẫn bị tăng lên thành 4.</td>
      <td>Bỏ qua lượt mượn 104 và không cộng vào biến valid_count.</td>
      <td>Dòng 11 (valid_count += 1)</td>
      <td>Biến valid_count bị tăng ở đầu vòng lặp trước khi thực hiện câu lệnh continue, dẫn đến tính sai số lượt thành công.</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Mã 108 (Rủi ro thất thoát)</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Lô mượn giả định không có mã rủi ro (Ví dụ: từ 101 đến 103)</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn nghiệp vụ**
Viết lại chương trình Python hoàn chỉnh để sửa toàn bộ các lỗi logic trên, đảm bảo:
1. Đặt câu lệnh tăng biến đếm `valid_count` đúng vị trí (chỉ tăng khi lượt mượn xử lý thành công).
2. Kiểm tra điều kiện ngắt dừng khẩn cấp (`loan_id == 108`) và điều kiện bỏ qua (`loan_id == 104`) trước khi in thông báo xử lý thành công.
3. Giữ nguyên cấu trúc khối `else` của vòng lặp `for` để thông báo khi lô quét hoàn tất an toàn.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo test case và mã nguồn đã được sửa hoàn chỉnh.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex6`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session08_Ex6`
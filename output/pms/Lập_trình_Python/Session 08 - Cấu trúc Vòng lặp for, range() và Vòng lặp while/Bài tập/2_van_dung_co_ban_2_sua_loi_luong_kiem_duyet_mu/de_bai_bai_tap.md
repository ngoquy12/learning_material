# <center>[Vận dụng cơ bản 2] Sửa lỗi luồng kiểm duyệt mượn sách trong LIBRARY_WMS</center>

### **1. Mục tiêu**
*   **Về kiến thức:** Củng cố cách thức hoạt động của vòng lặp `for`, hàm `range()`, các câu lệnh điều khiển luồng `break`, `continue` và khối `else` kết hợp với vòng lặp trong Python.
*   **Về kỹ năng:** Luyện tập kỹ năng đọc vết mã nguồn (Code Tracing), phát hiện lỗi sai thứ tự thực thi câu lệnh (Execution Order Bug) làm rò rỉ dữ liệu hoặc xử lý sai nghiệp vụ.
*   **Về thực tiễn:** Làm quen với nghiệp vụ xử lý hàng loạt (Batch Processing) trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS).

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS), bộ phận kỹ thuật được giao nhiệm vụ viết chương trình tự động kiểm duyệt một lô gồm 10 cuốn sách (mã từ 1 đến 10) do sinh viên đăng ký mượn qua thiết bị quét tự động.

Quy định xử lý nghiệp vụ của hệ thống bao gồm:
*   Mã sách số 4 là cuốn sách đang thuộc diện bảo trì (hỏng bìa, chờ đóng lại), hệ thống cần bỏ qua không ghi nhận mượn cho cuốn sách này và tiếp tục xử lý các sách tiếp theo.
*   Mã sách số 8 thuộc diện rủi ro bảo mật (sách quý hiếm bị khóa mượn hoặc tài khoản sinh viên đang có khoản nợ quá hạn), hệ thống phải phát thông báo cảnh báo và lập tức dừng toàn bộ tiến trình kiểm duyệt.
*   Nếu toàn bộ lô sách được quét duyệt qua an toàn (không bị dừng khẩn cấp bởi mã rủi ro), hệ thống sẽ thông báo hoàn thành thành công ở cuối tiến trình.

Tuy nhiên, sau khi đưa đoạn mã nguồn thử nghiệm vào vận hành, thủ thư phát hiện một sự cố dữ liệu: Hệ thống vẫn in ra thông báo *"Đã xác nhận mượn thành công"* đối với cuốn sách số 4 và cuốn sách số 8 trước khi đưa ra thông báo bỏ qua hoặc dừng hệ thống. Điều này khiến cho cơ sở dữ liệu bị ghi nhận sai thông tin mượn sách.

### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn Python đang bị lỗi logic nghiệp vụ do lập trình viên trước đó bàn giao:

```python

# Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS)

# Tiến trình kiểm duyệt mượn sách tự động theo lô (mã từ 1 đến 10)

print("--- BẮT ĐẦU TIẾN TRÌNH KIỂM DUYỆT MƯỢN SÁCH ---")

for book_id in range(1, 11):

# Tiến hành ghi nhận thông báo mượn sách thành công
    print("Đã xác nhận mượn thành công cuốn sách mã số:", book_id)

# Kiểm tra sách thuộc diện bảo trì
    if book_id == 4:
        print("Thông báo: Sách mã số", book_id, "đang bảo trì -> Bỏ qua")
        continue

# Kiểm tra sách thuộc diện rủi ro/bị khóa
    if book_id == 8:
        print("CẢNH BÁO: Sách mã số", book_id, "bị khóa quyền mượn -> DỪNG HỆ THỐNG!")
        break
else:
    print("TẤT CẢ SÁCH ĐÃ ĐƯỢC DUYỆT THÀNH CÔNG AN TOÀN!")

print("--- KẾT THÚC TIẾN TRÌNH KIỂM DUYỆT ---")
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo phân tích lỗi (Test Case Report Table)**
Học viên tiến hành chạy vết (trace) mã nguồn hiện tại, xác định dòng mã bị đặt sai vị trí và hoàn thành Bảng phân tích Test Case dưới đây vào báo cáo:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center; border: 1px solid #dddddd;">STT</th>
      <th style="text-align: center; border: 1px solid #dddddd;">Đầu vào (Input)</th>
      <th style="text-align: center; border: 1px solid #dddddd;">Kết quả hiện tại (Buggy Output)</th>
      <th style="text-align: center; border: 1px solid #dddddd;">Kết quả mong đợi (Expected Output)</th>
      <th style="text-align: center; border: 1px solid #dddddd;">Dòng code gây lỗi (Failing Line)</th>
      <th style="text-align: center; border: 1px solid #dddddd;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center; border: 1px solid #dddddd;">1</td>
      <td style="border: 1px solid #dddddd;">book_id = 4</td>
      <td style="border: 1px solid #dddddd;">In ra "Đã xác nhận mượn thành công cuốn sách mã số: 4" trước khi in thông báo bỏ qua.</td>
      <td style="border: 1px solid #dddddd;">Chỉ in "Thông báo: Sách mã số 4 đang bảo trì -> Bỏ qua không được in dòng xác nhận mượn.</td>
      <td style="border: 1px solid #dddddd;">Dòng 8</td>
      <td style="border: 1px solid #dddddd;">Câu lệnh print() xác nhận thành công được đặt trước khi kiểm tra điều kiện if book_id == 4 với continue.</td>
    </tr>
    <tr>
      <td style="text-align: center; border: 1px solid #dddddd;">2</td>
      <td style="border: 1px solid #dddddd;">book_id = 8</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
    <tr>
      <td style="text-align: center; border: 1px solid #dddddd;">3</td>
      <td style="border: 1px solid #dddddd;">Kiểm tra khối else của for</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Mã nguồn đã sửa lỗi (Source Code Correction)**
Học viên viết lại đoạn mã nguồn Python hoàn chỉnh, đáp ứng chính xác các yêu cầu:
1. Đưa câu lệnh kiểm tra điều kiện bảo trì (`book_id == 4`) và câu lệnh kiểm tra rủi ro (`book_id == 8`) lên trước câu lệnh in thông báo xác nhận mượn sách.
2. Đảm bảo cuốn sách mã số 4 bị bỏ qua không in thông báo mượn thành công.
3. Đảm bảo cuốn sách mã số 8 kích hoạt ngắt vòng lặp khẩn cấp bằng `break` và không in thông báo mượn thành công.
4. Giữ nguyên khối `else` của vòng lặp `for` để đảm bảo hệ thống chỉ đưa ra thông báo *"TẤT CẢ SÁCH ĐÃ ĐƯỢC DUYỆT THÀNH CÔNG AN TOÀN!"* khi vòng lặp kết thúc tự nhiên mà không bị ngắt bởi `break`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex2`.
    Ví dụ: `HNKS25CNTT1_Core_Session08_Ex2`

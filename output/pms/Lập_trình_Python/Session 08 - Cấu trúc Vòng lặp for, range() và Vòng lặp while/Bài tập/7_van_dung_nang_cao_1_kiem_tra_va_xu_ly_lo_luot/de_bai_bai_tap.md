## <center>[Vận dụng nâng cao 1] Kiểm tra và xử lý lô lượt mượn sách thư viện</center>

### **1. Mục tiêu**
*   **Về kiến thức**: Vận dụng thành thạo cấu trúc vòng lặp `for` với hàm `range()`, các câu lệnh điều khiển luồng `break`, `continue` và khối `else` kết hợp trong vòng lặp.
*   **Về kỹ năng**: Phân tích kịch bản nghiệp vụ thực tế, tự thiết kế cấu trúc luồng xử lý và cài đặt chương trình kiểm tra lô lượt mượn sách tự động mà không sử dụng các cấu trúc dữ liệu nâng cao hay hàm định nghĩa trước.
*   **Về tư duy**: Phát triển tư duy phòng thủ (defensive programming), nhận biết các trường hợp vi phạm an ninh hoặc tài liệu ngoại lệ để xử lý ngắt/bỏ qua đúng lúc.

---

### **2. Vấn đề**
Trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS), cuối mỗi ca làm việc, thủ thư cần thực hiện quy trình rà soát tự động một lô gồm `N` lượt mượn sách (có mã số thứ tự từ $1$ đến `N`). 

Tuy nhiên, quá trình xử lý lô gặp phải một số tình huống nghiệp vụ đặc thù:
1.  **Tài liệu ngoại lệ (Bỏ qua)**: Một số lượt mượn thuộc danh mục tài liệu tham khảo nội bộ hoặc sách hư hỏng nhẹ đang chờ thanh lý sẽ không tính tiền phạt quá hạn và không ghi nhận nợ. Chương trình cần bỏ qua các mã này để tiếp tục xử lý các mã khác trong lô.
2.  **Rủi ro an ninh (Dừng khẩn cấp)**: Khi phát hiện một mã lượt mượn gắn với tài khoản sinh viên có dấu hiệu gian lận thẻ hoặc nợ đọng quá hạn nghiêm trọng bị khóa hệ thống, chương trình phải dừng lập tức toàn bộ tiến trình rà soát để niêm phong tài khoản.
3.  **Xử lý thông thường**: Với các lượt mượn hợp lệ, hệ thống tính toán phí phạt quá hạn dựa trên số ngày trả trễ và cập nhật tổng tiền phạt của ca làm việc.
4.  **Xác nhận hoàn thành**: Nếu toàn bộ lô lượt mượn được duyệt qua mà không xảy ra bất kỳ sự cố dừng khẩn cấp nào, hệ thống phải xác nhận ca rà soát đã hoàn tất an toàn.---

### **3. Quy tắc nghiệp vụ**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">Yếu tố nghiệp vụ</th>
      <th style="padding: 8px; text-align: left;">Quy định chi tiết</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><strong>Phạm vi kiểm tra lô</strong></td>
      <td style="padding: 8px;">Số lượng lượt mượn trong lô là <code>total_records</code> (nguyên dương, nhập từ bàn phím). Mã lượt mượn chạy từ <code>1</code> đến <code>total_records</code>.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Tính phí phạt quá hạn</strong></td>
      <td style="padding: 8px;">Mỗi ngày quá hạn bị phạt <code>5.000 VNĐ/quyển/ngày</code>. Nếu số ngày quá hạn &le; 0 thì phí phạt = 0 VNĐ.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Trường hợp Bỏ qua (continue)</strong></td>
      <td style="padding: 8px;">Nếu mã lượt mượn là số chia hết cho 5 (mã tài liệu đặc biệt), hệ thống in thông báo bỏ qua lượt mượn này và sử dụng <code>continue</code> để sang mã tiếp theo.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Trường hợp Dừng khẩn (break)</strong></td>
      <td style="padding: 8px;">Nếu mã lượt mượn trùng với <code>critical_code</code> (mã vi phạm an ninh do thủ thư nhập trước), hệ thống in thông báo cảnh báo nghiêm trọng và sử dụng <code>break</code> để ngắt ngay lập tức toàn bộ vòng lặp.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Khối xác nhận an toàn (else)</strong></td>
      <td style="padding: 8px;">Sử dụng khối <code>else</code> gắn liền với vòng lặp <code>for</code> để in thông báo xác nhận toàn bộ lô được kiểm tra thành công (chỉ chạy khi vòng lặp không bị ngắt bởi <code>break</code>).</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><strong>Giới hạn kỹ thuật</strong></td>
      <td style="padding: 8px;"><strong>TUYỆT ĐỐI CẤM SỬ DỤNG</strong>: Vòng lặp <code>while</code>, danh sách (<code>list</code>), từ điển (<code>dict</code>), <code>tuple</code>, <code>set</code>, định nghĩa hàm (<code>def</code>), lớp (<code>class</code>). Chỉ dùng biến đơn cơ bản và cấu trúc điều khiển lặp/đáo nhánh.</td>
    </tr>
  </tbody>
</table>

---

### **4. Yêu cầu bài toán**

Học viên thực hiện đầy đủ 2 phần nhiệm vụ sau:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Nộp dạng văn bản/diagram trong báo cáo)**
1.  **Phân tích Đầu vào / Đầu ra (I/O Analysis)**:
    *   Xác định rõ các thông tin cần nhập, thông tin cần xuất, kiểu dữ liệu tương ứng và ý nghĩa nghiệp vụ của từng biến.
2.  **Đề xuất Giải pháp & Lập sơ đồ tiến trình**:
    *   Tự đề xuất các bước xử lý logic để giải quyết bài toán theo quy tắc nghiệp vụ.
    *   Vẽ sơ đồ luồng (Flowchart) thể hiện tiến trình bằng cú pháp Mermaid. Sơ đồ phải tuân thủ đúng 5 hình dạng chuẩn:
        *   **Oval `([ ... ])`**: Điểm bắt đầu / kết thúc quy trình.
        *   **Hình bình hành `[/ ... /]`**: Thao tác Nhập (Input) / Xuất (Output) dữ liệu.
        *   **Hình chữ nhật `[" ... "]`**: Thao tác Xử lý / Tính toán logic.
        *   **Hình thoi `Kiểm tra?`**: Thao tác Kiểm tra điều kiện rẻ nhánh.
        *   **Mũi tên `-->`**: Luồng di chuyển dữ liệu/tiến trình.

#### **Phần 2: Triển khai Mã nguồn Python (Coding)**
*   Viết chương trình Python hoàn chỉnh thực hiện chính xác giải pháp đã thiết kế ở Phần 1.
*   Chương trình phải kiểm tra tính hợp lệ của dữ liệu đầu vào (ví dụ `total_records` phải là số nguyên lớn hơn 0).
*   Áp dụng đúng cấu trúc `for ... in range(...)`, `break`, `continue` và khối `else` của vòng lặp `for`.
*   Mã nguồn phải sạch, có chú thích bằng tiếng Việt có dấu, tên biến sử dụng tiếng Anh chuẩn `snake_case`.

---

### **5. Yêu cầu nộp bài**

Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex7`.
    *   *Ví dụ*: `HNKS25CNTT1_Core_Session_Session 08_Ex7`
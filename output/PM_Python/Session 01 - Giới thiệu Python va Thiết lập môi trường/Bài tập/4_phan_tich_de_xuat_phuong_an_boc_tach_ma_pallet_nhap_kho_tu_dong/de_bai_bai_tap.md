## <center>[Phân tích] Đề xuất phương án bóc tách mã Pallet nhập kho tự động</center>

### **1. Mục tiêu**
*   Vận dụng tư duy phân tích hệ thống để đánh giá và lựa chọn giải pháp kỹ thuật tối ưu dựa trên cấu trúc bộ nhớ RAM và tốc độ xử lý của Python.
*   Củng cố hiểu biết sâu sắc về sự khác biệt giữa xử lý chuỗi (String Manipulation) và xử lý toán học (Mathematical Operators).
*   Thực hành khai báo biến, ép kiểu dữ liệu (`int`, `str`), tính toán số học (`//`, `%`), cắt chuỗi (string slicing) và xuất chuỗi định dạng biến (f-string) theo đúng phạm vi kiến thức đã học.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản lý kho hàng (WAREHOUSE), một hệ thống phân loại pallet tự động nhận tín hiệu đầu vào từ máy quét barcode tại băng chuyền. Mỗi khi một pallet đi qua, máy quét sẽ gửi về hệ thống một số nguyên gồm đúng 8 chữ số đại diện cho thông tin kiện hàng (Pallet ID). 



Quy luật định dạng của số nguyên Pallet ID này được quy định cứng như sau:
*   4 chữ số đầu tiên: Mã SKU của sản phẩm (ví dụ: `2098`).
*   4 chữ số tiếp theo: Số lượng thùng hàng đang được xếp trên pallet đó (ví dụ: `0120` nghĩa là có 120 thùng hàng).

Ví dụ: Máy quét gửi về số nguyên: `20980120`. Hệ thống cần bóc tách được:
*   Mã SKU của sản phẩm: `2098` (Kiểu số nguyên).
*   Số lượng thùng hàng: `120` (Kiểu số nguyên).

Bạn cần thiết kế một modul xử lý nhẹ, hiệu năng cực cao để chạy trực tiếp trên các thiết bị điều khiển biên (Edge devices/IoT Gateway trong kho) vốn có tài nguyên RAM và CPU cực kỳ hạn chế. Hãy nghiên cứu và đề xuất 2 giải pháp xử lý dữ liệu đầu vào này mà không sử dụng các cấu trúc điều khiển nâng cao (như câu lệnh điều kiện `if`, vòng lặp `for`/`while`, hoặc định nghĩa hàm `def` chưa học).

### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý thông tin cần đáp ứng các quy tắc nghiệp vụ sau:
1.  **Dữ liệu đầu vào**: Pallet ID luôn được nhận vào thông qua hàm nhập liệu `input()` từ bàn phím dưới dạng một chuỗi số, sau đó được lưu trữ và xử lý.
2.  **Yêu cầu xử lý**:
    *   Tách biệt hoàn toàn mã SKU (4 chữ số đầu) và Số lượng (4 chữ số cuối) thành hai biến số nguyên độc lập.
    *   Tính toán số lượng thùng hàng còn thiếu để lấp đầy pallet (Biết rằng một pallet tiêu chuẩn trong kho chứa tối đa là `500` thùng hàng).
3.  **Yêu cầu đầu ra (Output)**: Chương trình phải in ra màn hình chính xác thông tin theo định dạng f-string như mẫu dưới đây:
    ```text
    Mã SKU sản phẩm: [Mã SKU]
    Số lượng thùng hàng thực tế: [Số lượng]
    Số lượng thùng hàng cần xếp thêm để đầy pallet: [Khoảng trống]
    Log ghi nhận: Pallet [Mã SKU] chứa [Số lượng] thùng đã được quét thành công.
    ```

[WARNING] Nghiêm cấm sử dụng các thư viện ngoài, không dùng câu lệnh rẽ nhánh `if-else`, không dùng vòng lặp, không dùng hàm tự định nghĩa. Chỉ sử dụng các toán tử số học, phép ép kiểu, cắt chuỗi và f-string.

### **4. Yêu cầu đầu ra**

#### **Phần 1: Báo cáo phân tích so sánh Trade-off**
Học viên viết một báo cáo ngắn (dưới dạng bảng Markdown) so sánh 2 giải pháp kỹ thuật sau:
*   **Giải pháp 1 (String Slicing & Casting)**: Nhận chuỗi đầu vào -> Cắt chuỗi bằng chỉ số index (`[0:4]` và `[4:8]`) -> Ép kiểu các chuỗi thu được thành số nguyên `int`.
*   **Giải pháp 2 (Mathematical Operators)**: Nhận chuỗi đầu vào -> Ép toàn bộ chuỗi sang số nguyên `int` -> Dùng các toán tử chia lấy phần nguyên (`//`) và chia lấy phần dư (`%`) cho lũy thừa của 10 để trích xuất số SKU và Số lượng.

Bảng so sánh bắt buộc phải sử dụng định dạng HTML rộng 100% với các tiêu chí dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr>
      <th>Tiêu chí so sánh</th>
      <th>Giải pháp 1 (String Slicing & Casting)</th>
      <th>Giải pháp 2 (Mathematical Division)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Độ phức tạp thời gian (Time Complexity)</strong></td>
      <td>Phân tích thời gian trích xuất ký tự chuỗi.</td>
      <td>Phân tích tốc độ tính toán số học trên CPU.</td>
    </tr>
    <tr>
      <td><strong>Độ phức tạp bộ nhớ (RAM Space)</strong></td>
      <td>Mức độ tiêu thụ RAM khi tạo các chuỗi con.</td>
      <td>Độ hiệu quả bộ nhớ khi thao tác trực tiếp trên số.</td>
    </tr>
    <tr>
      <td><strong>Giải thích tính dễ bảo trì (Maintainability)</strong></td>
      <td>Nếu cấu trúc độ dài mã Pallet ID thay đổi.</td>
      <td>Nếu cấu trúc độ dài mã Pallet ID thay đổi.</td>
    </tr>
    <tr>
      <td><strong>Độ đọc hiểu (Readability)</strong></td>
      <td>Mức độ dễ hiểu đối với lập trình viên mới.</td>
      <td>Mức độ trực quan của các phép toán logic (`//` và `%`).</td>
    </tr>
    <tr>
      <td><strong>Bối cảnh phù hợp nhất</strong></td>
      <td>Khi nào nên áp dụng phương án này?</td>
      <td>Khi nào nên áp dụng phương án này?</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Lập luận lựa chọn phương án tối ưu**
*   Học viên đưa ra lập luận lựa chọn giải pháp nào làm giải pháp tối ưu để triển khai trên thiết bị IoT Gateway của kho hàng (thiết bị yêu cầu xử lý hàng triệu bản ghi và cực kỳ tiết kiệm tài nguyên).
*   Trình bày mã giả (Pseudocode) thiết kế luồng xử lý của phương án tối ưu đã chọn.

#### **Phần 3: Hiện thực hóa mã nguồn**
*   Viết chương trình Python hoàn chỉnh thực hiện giải pháp tối ưu được chọn ở Phần 2.
*   Chương trình phải nhận dữ liệu từ bàn phím (`input`), thực hiện tính toán và in ra màn hình bằng f-string theo đúng định dạng mẫu dòng log yêu cầu tại Mục 3.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Tài liệu báo cáo chi tiết so sánh các giải pháp (File Markdown hoặc PDF) chứa Phần 1 và Phần 2.
*   Mã nguồn phương án tối ưu đã chọn (File `.py`) chạy thành công không có lỗi.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session01_Ex04`.
    Ví dụ: `HNKS25CNTT1_PythonCore_Session01_Ex04`
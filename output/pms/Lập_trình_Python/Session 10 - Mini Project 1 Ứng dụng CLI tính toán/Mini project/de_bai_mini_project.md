## <center>[Mini project] Ứng dụng Máy tính Cá nhân CLI (CLI Arithmetic Calculator Engine)</center>

### **1. Mục tiêu dự án**
Dự án **Ứng dụng Máy tính Cá nhân CLI** được thiết kế nhằm giúp học viên củng cố vững chắc các kiến thức cốt lõi về ngôn ngữ lập trình Python trong phạm vi giai đoạn đầu. Thông qua dự án này, học viên sẽ:
* Nắm vững cách quản lý luồng thực thi liên tục của ứng dụng Console thông qua cấu trúc lặp `while`.
* Thành thạo việc phân nhánh xử lý nghiệp vụ bằng các câu lệnh điều kiện `if`, `elif`, `else`.
* Khởi tạo, cập nhật và thao tác chính xác với các kiểu dữ liệu nguyên thủy (số nguyên `int`, số thực `float`, chuỗi `str`, luận lý `bool`).
* Làm quen với kỹ thuật kiểm chuẩn dữ liệu đầu vào và xử lý trôi chảy các ngoại lệ hệ thống (`ValueError`, `ZeroDivisionError`) bằng khối `try-except`.
* Rèn luyện tư duy lập trình phẳng (Flat Code) tối ưu, đặt tên biến chuẩn hóa Tiếng Anh theo quy chuẩn `snake_case`.

[NOTE] **Phạm vi kiến thức áp dụng:** Học viên chỉ được sử dụng biến đơn, các toán tử số học, vòng lặp `while`, câu lệnh rẽ nhánh `if/elif/else` và khối xử lý ngoại lệ `try-except`. 
[WARNING] **Phạm vi cấm:** TUYỆT ĐỐI KHÔNG sử dụng Hàm (`def`), Danh sách/Tập hợp (`list`, `dict`, `tuple`, `set`), Lập trình hướng đối tượng (`class`), hoặc Đọc/Ghi tập tin (`open`).

---

### **2. Đề bài và Yêu cầu**

Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md).

#### **2.1. Bối cảnh nghiệp vụ**
Bạn được giao nhiệm vụ phát triển một công cụ tính toán số học trên giao diện dòng lệnh (CLI - Command Line Interface). Ứng dụng cho phép người dùng lựa chọn phép tính, nhập các giá trị số nguyên hoặc số thực, nhận kết quả tức thì và lựa chọn tiếp tục tính toán trên kết quả vừa thu được hoặc thực hiện một phép tính hoàn toàn mới.

#### **2.2. Danh sách khối xử lý nghiệp vụ**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center; width: 8%;">STT</th>
      <th style="text-align: left; width: 32%;">Tên chức năng / Khối xử lý</th>
      <th style="text-align: left; width: 60%;">Mô tả chi tiết yêu cầu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td><b>[Hiển thị Menu điều hướng]</b><br><code>display_menu</code></td>
      <td>In ra màn hình giao diện chọn phép tính bao gồm các mục: (1) Phép cộng, (2) Phép trừ, (3) Phép nhân, (4) Phép chia, (5) Chia lấy dư, (6) Lũy thừa, (7) Đặt lại bộ nhớ kết quả, (0) Thoát ứng dụng.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td><b>[Thực hiện Phép cộng]</b><br><code>execute_addition</code></td>
      <td>Thực hiện phép tính $a + b$. Lưu kết quả vào biến lưu trữ bộ nhớ <code>previous_result</code>.</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td><b>[Thực hiện Phép trừ]</b><br><code>execute_subtraction</code></td>
      <td>Thực hiện phép tính $a - b$. Lưu kết quả vào biến lưu trữ bộ nhớ <code>previous_result</code>.</td>
    </tr>
    <tr>
      <td style="text-align: center;">4</td>
      <td><b>[Thực hiện Phép nhân]</b><br><code>execute_multiplication</code></td>
      <td>Thực hiện phép tính $a \times b$. Lưu kết quả vào biến lưu trữ bộ nhớ <code>previous_result</code>.</td>
    </tr>
    <tr>
      <td style="text-align: center;">5</td>
      <td><b>[Thực hiện Phép chia]</b><br><code>execute_division</code></td>
      <td>Thực hiện phép tính $a / b$. Bắt lỗi chia cho 0 (<code>ZeroDivisionError</code>) và in thông báo cảnh báo.</td>
    </tr>
    <tr>
      <td style="text-align: center;">6</td>
      <td><b>[Thực hiện Chia lấy dư]</b><br><code>execute_modulo</code></td>
      <td>Thực hiện phép chia lấy phần dư $a \pmod b$. Yêu cầu các toán tử phải là số nguyên. Bắt lỗi chia cho 0.</td>
    </tr>
    <tr>
      <td style="text-align: center;">7</td>
      <td><b>[Thực hiện Lũy thừa]</b><br><code>execute_exponentiation</code></td>
      <td>Thực hiện phép tính mũ $a^b$ (ví dụ: $2^3 = 8$). Ghi nhận kết quả vào biến lưu trữ.</td>
    </tr>
    <tr>
      <td style="text-align: center;">8</td>
      <td><b>[Kế thừa kết quả tính toán]</b><br><code>reuse_previous_result</code></td>
      <td>Nếu <code>previous_result</code> khác <code>None</code>, ứng dụng hỏi người dùng có muốn dùng lại kết quả này làm số thứ nhất ($a$) cho phép tính tiếp theo hay không.</td>
    </tr>
    <tr>
      <td style="text-align: center;">9</td>
      <td><b>[Xóa bộ nhớ tính toán]</b><br><code>reset_calculator_memory</code></td>
      <td>Gán biến lưu trữ <code>previous_result</code> về giá trị ban đầu (<code>None</code>) và thông báo đã xóa kết quả lưu tạm.</td>
    </tr>
    <tr>
      <td style="text-align: center;">10</td>
      <td><b>[Kiểm chuẩn và Xử lý ngoại lệ]</b><br><code>validate_numeric_input</code></td>
      <td>Sử dụng <code>try-except</code> bọc các câu lệnh <code>input()</code> và ép kiểu (<code>float()</code> / <code>int()</code>) để xử lý lỗi nhập sai định dạng số (<code>ValueError</code>).</td>
    </tr>
  </tbody>
</table>

#### **2.3. Quy chuẩn kỹ thuật bắt buộc**
* [REQUIREMENT] **Quy chuẩn đặt tên biến:** Tất cả các biến số phải đặt bằng Tiếng Anh chuẩn `snake_case` (Ví dụ: `first_number`, `second_number`, `user_choice`, `previous_result`, `is_running`, `calculation_count`).
* [REQUIREMENT] **Giao diện CLI:** 100% thông báo in ra màn hình Console hiển thị bằng Tiếng Việt có dấu, trình bày rõ ràng, dễ quan sát.
* [WARNING] **Kiểm soát lỗi:** Không để ứng dụng dừng đột ngột (crash) khi người dùng nhập sai kiểu dữ liệu hoặc thực hiện phép chia cho 0. Chương trình phải in thông báo lỗi thân thiện và cho phép người dùng thao tác lại.

---

### **3. Yêu cầu nộp bài**
* **Mã nguồn:** Đẩy toàn bộ mã nguồn bài làm lên một Repository công khai trên GitHub.
* **Cấu trúc Repository:**
  * File mã nguồn chính: `main.py`
  * File hướng dẫn sử dụng: `README.md` (chứa thông tin mô tả dự án và hướng dẫn chạy chương trình).
* **Định dạng đường dẫn nộp bài:** Học viên nộp đường dẫn URL dạng: `https://github.com/username/cli-arithmetic-calculator`
## <center>Ứng Dụng CLI Tính Phí Lưu Trữ Máy Chủ (CLI Server Storage Fee Calculator)</center>

### **1. Mục tiêu**
Bài kiểm tra nhằm đánh giá khả năng vận dụng kiến thức lập trình Python cốt lõi cơ bản để xây dựng một ứng dụng Console CLI hoàn chỉnh trong 15-20 phút.
* **Kiến thức kiểm tra:** Cú pháp cơ bản, biến và kiểu dữ liệu scalar (int, float, str), câu lệnh điều kiện (`if/elif/else`), vòng lặp (`while`), và xử lý/định dạng chuỗi.
* **Phạm vi nghiêm cấm:** **TUYỆT ĐỐI CẤM** sử dụng Danh sách (`List`), Định nghĩa Hàm (`def`), Lập trình hướng đối tượng (`OOP/class`), và Đọc/Ghi tập tin (`File I/O`).

---

### **2. Yêu cầu**

#### **Ngữ cảnh nghiệp vụ**
Doanh nghiệp dịch vụ đám mây cần một công cụ dòng lệnh (CLI) cho phép quản trị viên nhập lần lượt thông tin các máy chủ lưu trữ (Server Entity) đang vận hành để tính toán chi phí lưu trữ hàng tháng cho từng máy chủ, đồng thời tổng hợp các chỉ số tài nguyên toàn hệ thống.

#### **Bảng tả chi tiết chức năng / khối xử lý**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 25%;">Tên Thao Tác / Khối Xử Lý</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 20%;">Dữ liệu đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 35%;">Quy tắc xử lý & Nghiệp vụ</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 20%;">Kết quả đầu ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Nhập và Kiểm Tra Thông Tin Máy Chủ]</b><br><code>process_server_input()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - <code>server_name</code> (str)<br>
        - <code>storage_gb</code> (float/int)<br>
        - <code>server_type</code> (str)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - Sử dụng vòng lặp <code>while</code> liên tục yêu cầu nhập thông tin.<br>
        - Nếu <code>server_name</code> bằng <code>"EXIT"</code> (không phân biệt hoa/thường), dừng vòng lặp.<br>
        - Đảm bảo <code>storage_gb > 0</code>. Nếu không hợp lệ, in thông báo lỗi và bỏ qua đợt tính toán.<br>
        - Kiểm tra <code>server_type</code> chỉ chấp nhận <code>"STD"</code> (Standard) hoặc <code>"HP"</code> (High Performance).
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Dữ liệu máy chủ hợp lệ hoặc thông báo lỗi console nếu nhập sai.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Tính Phí Lưu Trữ & Tích Lũy Báo Cáo]</b><br><code>calculate_and_accumulate()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - <code>storage_gb</code><br>
        - <code>server_type</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - Đơn giá cho <code>"STD"</code>: $0.15 / GB.<br>
        - Đơn giá cho <code>"HP"</code>: $0.35 / GB.<br>
        - Tính phí cho máy chủ hiện tại: <code>server_fee = storage_gb * unit_price</code>.<br>
        - Tích lũy các chỉ số toàn hệ thống vào các biến tổng (accumulator variables):<br>
          + <code>total_servers</code> (tăng 1)<br>
          + <code>total_storage</code> (cộng dồn <code>storage_gb</code>)<br>
          + <code>total_cost</code> (cộng dồn <code>server_fee</code>)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Phí hàng tháng của máy chủ vừa nhập (được in ra màn hình).</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Hiển Thị Báo Cáo Tổng Hợp]</b><br><code>render_summary_report()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - <code>total_servers</code><br>
        - <code>total_storage</code><br>
        - <code>total_cost</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - Khi kết thúc vòng lặp nhập liệu (`"EXIT"`), hiển thị báo cáo tổng quan.<br>
        - Làm tròn chi phí đến 2 chữ số thập phân.<br>
        - Định dạng bảng báo cáo rõ ràng trên màn hình Console.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Bảng tổng hợp tổng số máy chủ, tổng dung lượng và tổng chi phí ước tính.</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

Thang điểm tổng: **10 điểm**

| Tỷ lệ | Tiêu chí đánh giá | Chi tiết |
| :--- | :--- | :--- |
| **30%** | **Luồng điều khiển & Cấu trúc lặp** | Cho phép nhập liên tục nhiều máy chủ bằng vòng lặp `while`, xử lý thoát chương trình chính xác khi gặp từ khóa `'EXIT'`. |
| **30%** | **Kiểm tra dữ liệu & Tính toán nghiệp vụ** | Xử lý đúng câu điều kiện `if/elif/else` để phân loại đơn giá `STD`/`HP`, thông báo lỗi rõ ràng khi nhập sai loại máy chủ hoặc dung lượng `<= 0`. |
| **30%** | **Tích lũy & Định dạng đầu ra** | Sử dụng các biến tích lũy đơn lẻ để cộng dồn chỉ số hệ thống, in ra báo cáo tổng hợp với định dạng chuỗi chuyên nghiệp. |
| **10%** | **Quy chuẩn mã nguồn** | Đặt tên biến hoàn toàn bằng tiếng Anh chuẩn `snake_case` (ví dụ: `server_name`, `storage_gb`, `total_cost`), không dùng biến một ký tự vô nghĩa. |

---

### **4. Yêu cầu nộp bài**

* Thí sinh viết mã nguồn trong một tệp Python đơn lẻ đặt tên là: `main.py` (hoặc `server_calculator.py`).
* Đảm bảo chương trình chạy trực tiếp được qua dòng lệnh bằng lệnh: `python main.py`.
* Đẩy mã nguồn lên kho lưu trữ GitHub cá nhân và nộp liên kết (URL) của tệp mã nguồn theo hướng dẫn của giảng viên.
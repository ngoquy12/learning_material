## <center>ĐIỀU HƯỚNG QUY TRÌNH & TÍNH TOÁN HẠN MỨC TÍN DỤNG CLI (CLI CREDIT LIMIT NAVIGATION)</center>

### **1. Mục tiêu**
* Đánh giá khả năng điều khiển luồng chương trình Console tương tác nhiều bước bằng vòng lặp `while` và cấu trúc rẽ nhánh `if-elif-else`.
* Thực hành kỹ thuật quản lý trạng thái tác vụ (State Management) đơn giản thông qua các biến cờ (flags) và biến lưu trữ dữ liệu tạm thời.
* Xử lý lỗi chuyển đổi dữ liệu đầu vào từ người dùng bằng khối `try-except` nguyên bản của Python.
* Tuân thủ tuyệt đối quy định không áp dụng danh sách (`list`), hàm (`def`), lập trình hướng đối tượng (`OOP`) hay thao tác tập tin (`file`).

---

### **2. Yêu cầu**

Xây dựng một chương trình dòng lệnh (CLI) điều hướng quy trình tính toán hạn mức tín dụng cá nhân theo từng bước trạng thái.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">Khối chức năng / Bước xử lý</th>
      <th style="padding: 8px; text-align: left;">Đầu vào (Input)</th>
      <th style="padding: 8px; text-align: left;">Quy tắc & Logic xử lý</th>
      <th style="padding: 8px; text-align: left;">Đầu ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><b>[Khởi tạo & Điều hướng Menu]</b><br><code>process_menu_navigation</code></td>
      <td style="padding: 8px;"><code>user_choice</code> (str) nhập từ bàn phím.</td>
      <td style="padding: 8px;">
        - Duy trì vòng lặp hiển thị Menu 3 lựa chọn:<br>
        &nbsp;&nbsp;<code>1. Nhập hồ sơ khách hàng</code><br>
        &nbsp;&nbsp;<code>2. Tính toán hạn mức tín dụng</code><br>
        &nbsp;&nbsp;<code>3. Thoát chương trình</code><br>
        - Nếu <code>user_choice</code> không thuộc ["1", "2", "3"], in thông báo yêu cầu nhập lại.<br>
        - Khai báo biến <code>current_state = "INIT"</code> ban đầu.
      </td>
      <td style="padding: 8px;">Hiển thị giao diện điều hướng liên tục hoặc thoát chương trình khi chọn <code>3</code>.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>[Cập nhật Trạng thái Hồ sơ]</b><br><code>update_task_state</code></td>
      <td style="padding: 8px;">
        - <code>income_amount</code> (float)<br>
        - <code>credit_score</code> (int)<br>
        - <code>has_collateral</code> (str: 'y'/'n')
      </td>
      <td style="padding: 8px;">
        - Thực thi khi người dùng chọn tính năng <code>1</code>.<br>
        - Sử dụng <code>try-except</code> để bắt lỗi <code>ValueError</code> khi ép kiểu số.<br>
        - Điều kiện hợp lệ: <code>income_amount > 0</code> và <code>300 <= credit_score <= 850</code>.<br>
        - Nếu hợp lệ: cập nhật <code>current_state = "READY"</code> và lưu lại thông tin.<br>
        - Nếu vi phạm: in thông báo lỗi dữ liệu và giữ nguyên trạng thái cũ.
      </td>
      <td style="padding: 8px;">In thông báo cập nhật hồ sơ thành công hoặc báo lỗi nhập liệu không hợp lệ.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>[Tính toán & Xuất Kết quả Trạng thái]</b><br><code>execute_calculation_state</code></td>
      <td style="padding: 8px;">Đọc giá trị từ các biến trạng thái hiện tại: <code>current_state</code>, <code>income_amount</code>, <code>credit_score</code>, <code>has_collateral</code>.</td>
      <td style="padding: 8px;">
        - Thực thi khi người dùng chọn tính năng <code>2</code>.<br>
        - Nếu <code>current_state != "READY"</code>: Báo lỗi "Vui lòng hoàn thành bước 1 (Nhập hồ sơ) trước!".<br>
        - Nếu <code>current_state == "READY"</code>, tính toán <code>calculated_limit</code> theo công tắc:<br>
        &nbsp;&nbsp;+ Điểm <code>credit_score >= 750</code>: Hạn mức = <code>income_amount * 5</code><br>
        &nbsp;&nbsp;+ Điểm <code>600 <= credit_score < 750</code>: Hạn mức = <code>income_amount * 3</code><br>
        &nbsp;&nbsp;+ Điểm <code>credit_score < 600</code>: Hạn mức = <code>income_amount * 1</code><br>
        &nbsp;&nbsp;+ Nếu <code>has_collateral == "y"</code>: Tăng thêm 20% trên hạn mức đã tính.<br>
        - Chuyển trạng thái <code>current_state = "COMPLETED"</code>.
      </td>
      <td style="padding: 8px;">In hạn mức tín dụng được duyệt (định dạng 2 chữ số thập phân) và trạng thái xử lý mới.</td>
    </tr>
  </tbody>
</table>

> ⚠️ **LƯU Ý QUAN TRỌNG (FORBIDDEN SCOPE)**:
> - **TUYỆT ĐỐI CẤM SỬ DỤNG**: Danh sách (`list`), Định nghĩa hàm (`def`), Lập trình hướng đối tượng (`class`), Thao tác tập tin (`open()`).
> - Viết toàn bộ logic trong một luồng mã nguồn duy nhất bằng vòng lặp và câu lệnh rẽ nhánh.

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Điểm tối đa |
| :---: | :--- | :---: |
| 1 | **Điều hướng Menu & Trạng thái**: Xây dựng vòng lặp `while` điều hướng chính xác 3 tính năng, quản lý đúng biến trạng thái `current_state`. | **3.0 điểm** |
| 2 | **Kiểm tra Dữ liệu Đầu vào**: Bắt lỗi ép kiểu với `try-except` và kiểm tra miền giá trị hợp lệ cho thu nhập và điểm tín dụng. | **3.0 điểm** |
| 3 | **Logic Tính toán Hạn mức**: Tính toán đúng hạn mức dựa trên các mức điểm tín dụng và thuộc tính tài sản đảm bảo. | **3.0 điểm** |
| 4 | **Chuẩn Mã Nguồn**: Tên biến 100% Tiếng Anh `snake_case`, giao diện Console rõ ràng, tuân thủ phạm vi kiến thức cho phép. | **1.0 điểm** |
| **TỔNG** | | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**
* Tên tệp mã nguồn Python: `main.py`.
* Học viên tạo repository trên GitHub, đẩy mã nguồn lên branch `main` và nộp liên kết repository theo đúng quy định.
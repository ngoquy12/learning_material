## <center>Hệ Thống Điều Hướng Trạng Thái Tác Vụ CLI (CLI Task State Navigation System)</center>

### **1. Mục tiêu**
Đánh giá khả năng của học viên trong việc xử lý cấu trúc dữ liệu lồng nhau (List of Dictionaries), xây dựng luồng logic điều hướng trạng thái (State Transition Logic), quản lý lịch sử (State History Log) và kiểm soát lỗi nghiệp vụ bằng cơ chế ngoại lệ nguyên bản (Native Exceptions) trong Python CLI.

### **2. Yêu cầu**
Học viên giả định hệ thống quản lý có các trạng thái tác vụ và quy tắc chuyển đổi hợp lệ như sau:
*   `DRAFT` chỉ có thể chuyển sang `ASSIGNED`.
*   `ASSIGNED` có thể chuyển sang `IN_PROGRESS` hoặc quay lại `DRAFT`.
*   `IN_PROGRESS` chỉ có thể chuyển sang `RESOLVED`.
*   `RESOLVED` có thể chuyển sang `CLOSED` hoặc quay lại `IN_PROGRESS`.
*   `CLOSED` là trạng thái cuối cùng, không thể chuyển sang trạng thái khác.

Dữ liệu mô phỏng ban đầu của hệ thống:
```python
tasks_db = [
    {"task_id": "T01", "title": "Fix database connection leak", "state": "DRAFT", "history": ["DRAFT"]},
    {"task_id": "T02", "title": "Setup Jenkins pipeline", "state": "ASSIGNED", "history": ["DRAFT", "ASSIGNED"]}
]
```

Hãy hiện thực hóa các chức năng cốt lõi theo đặc tả chi tiết trong bảng dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%;">Tên chức năng / Hàm</th>
      <th style="width: 20%;">Tham số / Input</th>
      <th style="width: 35%;">Logic xử lý</th>
      <th style="width: 20%;">Output / Kết quả trả về</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Điều hướng chuyển đổi trạng thái</b><br><code>navigate_task_state()</code></td>
      <td>
        - <code>tasks</code>: list<br>
        - <code>task_id</code>: str<br>
        - <code>target_state</code>: str
      </td>
      <td>
        - Tìm kiếm tác vụ theo <code>task_id</code>. Nếu không tìm thấy, ném <code>KeyError</code>.<br>
        - Kiểm tra trạng thái hiện tại của tác vụ. Đối chiếu với quy tắc chuyển đổi hợp lệ:<br>
          + Nếu <code>target_state</code> nằm trong danh sách chuyển đổi hợp lệ của trạng thái hiện tại: tiến hành cập nhật <code>state</code> thành <code>target_state</code>, đồng thời thêm (append) trạng thái mới vào danh sách <code>history</code>.<br>
          + Nếu chuyển đổi không hợp lệ, ném <code>ValueError</code> thông báo lỗi logic chuyển đổi.<br>
        - Trạng thái <code>CLOSED</code> không cho phép chuyển đi bất kỳ đâu.
      </td>
      <td>Trả về <code>True</code> nếu chuyển đổi trạng thái thành công. Phục hồi luồng và hiển thị thông báo ra màn hình nếu xảy ra lỗi.</td>
    </tr>
    <tr>
      <td><b>Hoàn tác trạng thái trước đó</b><br><code>undo_state_transition()</code></td>
      <td>
        - <code>tasks</code>: list<br>
        - <code>task_id</code>: str
      </td>
      <td>
        - Tìm kiếm tác vụ theo <code>task_id</code> trong hệ thống. Nếu không thấy, ném <code>KeyError</code>.<br>
        - Kiểm tra độ dài danh sách lịch sử <code>history</code> của tác vụ:<br>
          + Nếu danh sách <code>history</code> có từ 2 trạng thái trở lên: loại bỏ (pop) trạng thái hiện tại ra khỏi lịch sử, cập nhật thuộc tính <code>state</code> của tác vụ bằng trạng thái đứng liền trước trong lịch sử.<br>
          + Nếu danh sách <code>history</code> chỉ có 1 trạng thái (trạng thái khởi tạo ban đầu), ném <code>ValueError</code> với nội dung "Cannot undo initial state".
      </td>
      <td>Trả về <code>str</code> là trạng thái mới sau khi hoàn tác thành công. Hoặc ném ngoại lệ nếu không thể hoàn tác.</td>
    </tr>
    <tr>
      <td><b>Lấy thông tin tổng quan điều hướng</b><br><code>get_navigation_summary()</code></td>
      <td>
        - <code>tasks</code>: list<br>
        - <code>task_id</code>: str
      </td>
      <td>
        - Tìm kiếm tác vụ theo <code>task_id</code>. Nếu không tìm thấy, ném <code>KeyError</code>.<br>
        - Tổng hợp thông tin trạng thái hiện tại, danh sách các trạng thái kế tiếp có thể chuyển hướng tới (dựa vào quy tắc chuyển đổi) và chuỗi lịch sử di chuyển (ví dụ định dạng hiển thị lịch sử: "DRAFT -> ASSIGNED").
      </td>
      <td>Trả về <code>dict</code> chứa các thông tin: <code>task_id</code>, <code>current_state</code>, <code>next_avaiable_states</code> (list), và <code>history_path</code> (str).</td>
    </tr>
  </tbody>
</table>

### **3. Tiêu chí đánh giá**
*   **Chức năng điều hướng (`navigate_task_state`) (4.0 điểm):**
    *   Tìm kiếm chính xác tác vụ trong danh sách (1.0 điểm).
    *   Bắt lỗi và ném `KeyError` nếu không tìm thấy tác vụ (1.0 điểm).
    *   Kiểm tra logic chuyển đổi trạng thái hợp lệ và cập nhật đúng lịch sử (1.5 điểm).
    *   Xử lý chặn chuyển tiếp từ trạng thái `CLOSED` và ném `ValueError` (0.5 điểm).
*   **Chức năng hoàn tác trạng thái (`undo_state_transition`) (3.0 điểm):**
    *   Kiểm tra điều kiện độ dài lịch sử `history` (1.0 điểm).
    *   Thực hiện pop và phục hồi trạng thái trước đó chính xác (1.0 điểm).
    *   Ném lỗi `ValueError` khi cố gắng undo từ trạng thái gốc (1.0 điểm).
*   **Chức năng lấy thông tin tổng quan (`get_navigation_summary`) (2.0 điểm):**
    *   Xác định chính xác các trạng thái kế tiếp có thể đi đến từ trạng thái hiện tại (1.0 điểm).
    *   Định dạng đúng chuỗi lịch sử di chuyển mong muốn (1.0 điểm).
*   **Kiểm thử và Sử dụng Ngoại lệ (1.0 điểm):**
    *   Viết mã thực thi minh họa (Driver Code) có cấu trúc `try-except` để bắt và in các thông báo lỗi trực quan của 3 hàm trên.

### **4. Yêu cầu nộp bài**
*   Học viên lưu mã nguồn vào một tệp duy nhất có tên `task_navigation.py`.
*   Đẩy mã nguồn lên kho lưu trữ GitHub cá nhân và gửi liên kết nộp bài theo đúng cú pháp quy định.
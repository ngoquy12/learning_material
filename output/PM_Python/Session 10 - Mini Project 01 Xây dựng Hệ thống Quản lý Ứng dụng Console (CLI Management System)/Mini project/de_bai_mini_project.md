## <center>[Mini project] Quản lý Kho hàng và Đơn hàng Console (Warehouse and Order Management CLI)</center>

[WARNING] Dự án này yêu cầu áp dụng nghiêm ngặt các quy định về cú pháp và kiến trúc lập trình cốt lõi của Python. Không sử dụng Class (Lập trình hướng đối tượng), File I/O (Đọc/ghi tệp tin), hoặc bất kỳ thư viện bên thứ ba nào (như NumPy, Pandas). Tất cả dữ liệu sẽ được lưu trữ tạm thời trong bộ nhớ (In-memory Data Structure) thông qua List, Dictionary, Tuple và Set.

### **1. Mục tiêu dự án**
- Làm chủ kỹ thuật thiết kế giao diện tương tác dòng lệnh (CLI - Command Line Interface) thân thiện, dễ vận hành.
- Vận dụng linh hoạt các cấu trúc dữ liệu cốt lõi trong Python (List, Dict) để tổ chức, biểu diễn và truy vấn thông tin nghiệp vụ một cách hiệu quả.
- Rèn luyện kỹ năng xây dựng mã nguồn mô-đun hóa bằng hàm (Function), kiểm chuẩn dữ liệu đầu vào (Validation) và xử lý ngoại lệ (Exception Handling) để hệ thống hoạt động ổn định, tránh bị lỗi tắt ứng dụng đột ngột.

### **2. Đề bài và Yêu cầu**

Học viên xây dựng một ứng dụng Console CLI mô phỏng phân hệ cơ bản của một Hệ thống Quản lý Kho và Đơn hàng (WOMS). Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md).

#### **2.1. Cấu trúc dữ liệu yêu cầu**
Hệ thống sử dụng các biến toàn cục (Global Variables) đại diện cho cơ sở dữ liệu tạm thời:
- `inventory`: Một danh sách chứa các Dictionary (List of Dicts). Mỗi sản phẩm/vật tư trong kho gồm các thông tin: `item_id` (chuỗi ký tự, mã duy nhất), `name` (tên vật tư), `category` (phân loại), `quantity` (số lượng tồn kho - số nguyên), `price` (đơn giá - số thực).
- `orders`: Một danh sách chứa các Dictionary (List of Dicts) lưu vết thông tin xuất kho. Mỗi đơn hàng gồm: `order_id` (mã đơn hàng duy nhất), `customer_name` (tên khách hàng), `items` (danh sách gồm các mã vật tư và số lượng xuất tương ứng), `total_amount` (tổng giá trị đơn hàng - số thực).

#### **2.2. Danh sách các chức năng nghiệp vụ cần triển khai**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 10px; text-align: left; width: 30%;">Chức năng / Hàm phát triển</th>
      <th style="padding: 10px; text-align: left; width: 70%;">Mô tả nghiệp vụ bổ chi tiết</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; vertical-align: top;">
        <b>Khởi tạo kho hàng thực tế</b><br>
        <code>initialize_system()</code>
      </td>
      <td style="padding: 10px; vertical-align: top;">
        Nạp dữ liệu mẫu ban đầu gồm ít nhất 3 vật tư/sản phẩm vào danh sách <code>inventory</code> và trạng thái ban đầu của danh sách đơn hàng <code>orders</code> phải trống.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; vertical-align: top;">
        <b>Thêm mới vật tư vào kho</b><br>
        <code>add_inventory_item(item_id, name, category, quantity, price)</code>
      </td>
      <td style="padding: 10px; vertical-align: top;">
        Yêu cầu kiểm tra mã <code>item_id</code> không được trùng lập. Các thông số <code>quantity</code> và <code>price</code> phải lớn hơn 0 (sử dụng khối kiểm tra điều khiển). Trả về kết quả thêm mới thành công hoặc ném ra ngoại lệ/thông báo lỗi nghiệp vụ cụ thể nếu không hợp lệ.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; vertical-align: top;">
        <b>Cập nhật số lượng tồn kho</b><br>
        <code>update_inventory_stock(item_id, adjustment_quantity)</code>
      </td>
      <td style="padding: 10px; vertical-align: top;">
        Dùng để điều chỉnh số lượng tồn kho (tăng/giảm) của một mã vật tư đã tồn tại. Nếu giảm tồn kho, phải đảm bảo số lượng giảm không vượt quá số lượng hàng hiện có trong kho.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; vertical-align: top;">
        <b>Tạo đơn hàng xuất kho</b><br>
        <code>process_new_order(order_id, customer_name, items_list)</code>
      </td>
      <td style="padding: 10px; vertical-align: top;">
        Nhận vào thông tin đơn hàng mới. Tham số <code>items_list</code> là danh sách Tuple <code>(item_id, order_quantity)</code>. Kiểm tra điều kiện tồn kho trước khi xuất:
        - Nếu bất kỳ vật tư nào không đủ số lượng, ném ra ngoại lệ ứng dụng (ví dụ: <code>ValueError</code>) báo lỗi thiếu hàng và <b>không thực hiện trừ kho bất kỳ vật tư nào</b> (nguyên tắc Transaction).
        - Nếu đủ hàng, tiến hành trừ kho lượng hàng tồn tương ứng, sau đó tính toán tổng tiền <code>total_amount</code> và ghi nhận dữ liệu vào danh sách <code>orders</code>.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; vertical-align: top;">
        <b>Báo cáo tồn kho trực quan</b><br>
        <code>show_inventory_report()</code>
      </td>
      <td style="padding: 10px; vertical-align: top;">
        Hiển thị danh sách vật tư hiện tại ra màn hình Console dưới dạng bảng ASCII căn lề rõ ràng để quản trị viên dễ theo dõi.
      </td>
    </tr>
    <tr>
      <td style="padding: 10px; vertical-align: top;">
        <b>Khởi chạy trình điều khiển CLI</b><br>
        <code>run_cli_menu()</code>
      </td>
      <td style="padding: 10px; vertical-align: top;">
        Chứa vòng lặp <code>while True</code> để hiển thị menu các thao tác từ 1 đến 6 và xử lý các đầu vào từ bàn phím thông qua <code>input()</code>. Mọi dữ liệu do người dùng gõ vào (như số lượng, đơn giá, mã số) cần được bọc trong các khối <code>try-except</code> để bắt lỗi dữ liệu sai định dạng mà không làm sập ứng dụng.
      </td>
    </tr>
  </tbody>
</table>

[NOTE] **Luồng kiểm chuẩn đầu vào (Validation Input):**
- Khi người dùng chọn chức năng và thực hiện nhập các thông số từ bàn phím, đối với các trường yêu cầu số (như Số lượng, Đơn giá), hệ thống phải bắt được lỗi nếu người dùng cố tình nhập chuỗi chữ cái hoặc ký tự đặc biệt, đồng thời đưa ra thông báo cảnh báo yêu cầu nhập lại thay vì kết thúc chương trình.

### **3. Yêu cầu nộp bài**
Học viên hoàn thành dự án và nộp các thành phần cấu thành sản phẩm thông qua kho lưu trữ Git:
- Đường dẫn tới mã nguồn trên kho lưu trữ trực tuyến (GitHub/GitLab) ở chế độ công khai (Public).
- Bản ghi chép (README.md) mô tả chức năng của hệ thống và hướng dẫn cách chạy chương trình.
- Tệp mã nguồn Python chính (.py) chứa toàn bộ mã nguồn xử lý dự án.
- Ảnh chụp màn hình giao diện điều khiển (CLI Screenshot) chứng minh chương trình chạy thành công các chức năng.
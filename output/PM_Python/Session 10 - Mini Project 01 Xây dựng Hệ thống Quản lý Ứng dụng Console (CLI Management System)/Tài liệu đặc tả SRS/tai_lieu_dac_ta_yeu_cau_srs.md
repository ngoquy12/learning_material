## <center>Tài liệu đặc tả Hệ thống Quản lý Kho hàng và Đơn hàng CLI (Warehouse and Order Management System - WOMS)</center>

### **1. Tổng quan hệ thống**
Hệ thống Quản lý Kho hàng và Đơn hàng CLI (Warehouse and Order Management System - WOMS) là một ứng dụng Console (command-line interface) được thiết kế nhằm mục đích hỗ trợ các cửa hàng bán lẻ quy mô nhỏ quản lý danh mục sản phẩm, theo dõi lượng tồn kho và thực hiện quy trình tạo đơn hàng tự động. Hệ thống hoạt động hoàn toàn trên bộ nhớ đệm (RAM) với cấu trúc dữ liệu nguyên bản của Python, đảm bảo tốc độ xử lý nhanh, tối ưu hóa bộ nhớ và giao diện tương tác dòng lệnh tường minh, trực quan cho người vận hành.

<div class="mermaid-diagram-container" style="background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin: 20px 0; overflow-x: auto;">
  <div class="mermaid" style="display: flex; justify-content: center; color: #f8fafc;">
flowchart TD
  %% Node definitions
  INIT(["Khởi chạy Hệ thống CLI"]):::startEnd
  RAM[("In-Memory RAM Storage\n- inventory: dict\n- orders: list")]:::storage
  MAIN_MENU{"Menu Chính CLI\n(Chọn chức năng 1-4)"}:::menu

  %% Main Options
  OP_INV["1. Quản lý Kho hàng"]:::submenu
  OP_ORD["2. Quản lý Đơn hàng"]:::submenu
  OP_REP["3. Báo cáo & Thống kê"]:::submenu
  OP_EXIT(["4. Thoát Chương trình"]):::startEnd

  %% Sub-operations: Inventory
  INV_MENU{"Menu Quản lý Kho"}:::decision
  INV_VIEW["Xem danh sách sản phẩm"]:::process
  INV_ADD["Thêm/Cập nhật sản phẩm"]:::process
  INV_DEL["Xóa sản phẩm khỏi kho"]:::process

  VAL_INV{"Dữ liệu nhập\nhợp lệ?"}:::decision
  SAVE_INV["Cập nhật vào RAM\n- inventory[product_id]"]:::process
  DEL_INV["Xóa key sản phẩm\ntrong dict 'inventory'"]:::process

  %% Sub-operations: Orders
  ORD_MENU{"Menu Quản lý Đơn"}:::decision
  ORD_VIEW["Xem danh sách đơn hàng"]:::process
  ORD_CREATE["Tạo đơn hàng mới"]:::process
  ORD_STATUS["Cập nhật trạng thái đơn"]:::process

  CHECK_STOCK{""Tìm sản phẩm & Khả dụng?\n(Requested <= Stock)""}:::decision
  STOCK_ERR["Báo lỗi: Thiếu hàng / Không tồn tại"]:::process
  DEDUCT_STOCK["Trừ tồn kho hàng\ntrong dict 'inventory'"]:::process
  SAVE_ORDER["Thêm đơn hàng mới\nvào list 'orders'"]:::process
  UPDATE_STATUS["Cập nhật trạng thái đơn\n(Pending -> Done/Cancel)"]:::process

  %% Sub-operations: Reports
  REP_MENU{"Chọn tiêu chí báo cáo"}:::decision
  REP_REV["Tính tổng doanh thu\ntừ các đơn thành công"]:::process
  REP_LOW["Lọc sản phẩm tồn kho thấp\n(Tồn kho < Threshold)"]:::process
  REP_TOP["Phân tích sản phẩm bán chạy"]:::process
  DISP_REP["Hiển thị báo cáo lên Console"]:::process

  %% Flow Logic
  INIT --> RAM
  RAM --> MAIN_MENU

  MAIN_MENU -->|Chọn 1| OP_INV
  MAIN_MENU -->|Chọn 2| OP_ORD
  MAIN_MENU -->|Chọn 3| OP_REP
  MAIN_MENU -->|Chọn 4| OP_EXIT

  %% Inventory Flows
  OP_INV --> INV_MENU
  INV_MENU -->|1. Xem| INV_VIEW
  INV_MENU -->|2. Thêm/Sửa| INV_ADD
  INV_MENU -->|3. Xóa| INV_DEL
  INV_MENU -->|4. Quay lại| MAIN_MENU

  INV_VIEW -.->|Đọc trực tiếp| RAM
  INV_ADD --> VAL_INV
  VAL_INV -->|Hợp lệ| SAVE_INV
  VAL_INV -->|Không hợp lệ| INV_ADD
  SAVE_INV -->|Ghi dữ liệu| RAM
  INV_DEL --> DEL_INV
  DEL_INV -->|Cập nhật| RAM

  %% Orders Flows
  OP_ORD --> ORD_MENU
  ORD_MENU -->|1. Xem| ORD_VIEW
  ORD_MENU -->|2. Tạo mới| ORD_CREATE
  ORD_MENU -->|3. Cập nhật| ORD_STATUS
  ORD_MENU -->|4. Quay lại| MAIN_MENU

  ORD_VIEW -.->|Đọc trực tiếp| RAM
  ORD_CREATE --> CHECK_STOCK
  CHECK_STOCK -->|Không đủ| STOCK_ERR --> ORD_CREATE
  CHECK_STOCK -->|Đủ hàng| DEDUCT_STOCK
  DEDUCT_STOCK -->|Cập nhật tồn kho| RAM
  DEDUCT_STOCK --> SAVE_ORDER
  SAVE_ORDER -->|Lưu đơn| RAM
  ORD_STATUS --> UPDATE_STATUS
  UPDATE_STATUS -->|Cập nhật đơn| RAM

  %% Reports Flows
  OP_REP --> REP_MENU
  REP_MENU -->|1. Doanh thu| REP_REV
  REP_MENU -->|2. Tồn kho thấp| REP_LOW
  REP_MENU -->|3. Bán chạy nhất| REP_TOP
  REP_MENU -->|4. Quay lại| MAIN_MENU

  REP_REV -.->|Đọc dữ liệu| RAM
  REP_LOW -.->|Đọc dữ liệu| RAM
  REP_TOP -.->|Đọc dữ liệu| RAM

  REP_REV --> DISP_REP
  REP_LOW --> DISP_REP
  REP_TOP --> DISP_REP
  DISP_REP --> MAIN_MENU

  %% Styling class assignments
  classDef startEnd fill:#f43f5e,stroke:#fda4af,stroke-width:2px,color:#ffffff;
  classDef storage fill:#10b981,stroke:#6ee7b7,stroke-width:2px,color:#ffffff;
  classDef menu fill:#8b5cf6,stroke:#c084fc,stroke-width:2px,color:#ffffff;
  classDef submenu fill:#3b82f6,stroke:#93c5fd,stroke-width:2px,color:#ffffff;
  classDef decision fill:#eab308,stroke:#fde047,stroke-width:2px,color:#1e293b;
  classDef process fill:#fdba74,stroke:#f97316,stroke-width:2px,color:#1e293b;
</div>
</div>

---

### **2. Đặc tả chức năng (Functional Requirements)**

Hệ thống cung cấp các chức năng chính dưới dạng menu tương tác liên tục cho người dùng. Dưới đây là bảng đặc tả chi tiết các hàm chức năng:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left; width: 5%;">STT</th>
      <th style="padding: 8px; text-align: left; width: 25%;">Tên chức năng/Hàm</th>
      <th style="padding: 8px; text-align: left; width: 45%;">Quy tắc nghiệp vụ chi tiết</th>
      <th style="padding: 8px; text-align: left; width: 25%;">Dữ liệu Đầu vào & Đầu ra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><b>Cập nhật / Thêm sản phẩm mới</b><br><code>add_or_update_product()</code></td>
      <td>
        - Tiếp nhận thông tin sản phẩm.<br>
        - Nếu mã sản phẩm (Product ID) đã tồn tại, tiến hành cộng dồn số lượng tồn kho và cập nhật đơn giá mới.<br>
        - Nếu mã sản phẩm chưa tồn tại, tạo mới sản phẩm trong hệ thống với số lượng tối thiểu phải từ 0 trở lên và đơn giá lớn hơn 0.
      </td>
      <td>
        - <b>Đầu vào:</b> <code>product_id</code> (str), <code>name</code> (str), <code>price</code> (float), <code>quantity</code> (int), <code>category</code> (str).<br>
        - <b>Đầu ra:</b> Trả về <code>True</code> nếu thành công, <code>False</code> nếu dữ liệu đầu vào không hợp lệ.
      </td>
    </tr>
    <tr>
      <td>2</td>
      <td><b>Hiển thị danh sách sản phẩm</b><br><code>display_inventory()</code></td>
      <td>
        - Duyệt qua toàn bộ danh sách sản phẩm trong kho.<br>
        - Hiển thị thông tin dưới dạng bảng phân cột rõ ràng trên Console CLI (bao gồm: ID, Tên, Giá, Số lượng, Danh mục).<br>
        - Đánh dấu cảnh báo đặc biệt (ví dụ: gắn nhãn "[LOW STOCK]") đối với các sản phẩm có số lượng tồn kho nhỏ hơn 5.
      </td>
      <td>
        - <b>Đầu vào:</b> Không có.<br>
        - <b>Đầu ra:</b> In trực tiếp bảng dữ liệu ra màn hình Console. Trả về số lượng sản phẩm đang có.
      </td>
    </tr>
    <tr>
      <td>3</td>
      <td><b>Tạo đơn bán hàng</b><br><code>create_sales_order()</code></td>
      <td>
        - Cho phép người dùng nhập tên khách hàng và chọn nhiều sản phẩm vào giỏ hàng.<br>
        - Kiểm tra tính hợp lệ của mã sản phẩm và số lượng tồn kho hiện tại.<br>
        - Nếu số lượng mua vượt quá số lượng tồn kho, từ chối thêm sản phẩm đó vào đơn và thông báo lỗi cụ thể.<br>
        - Trừ bớt số lượng tồn kho tương ứng của sản phẩm sau khi đơn hàng được tạo thành công.<br>
        - Tự động sinh ID đơn hàng duy nhất (ví dụ: 'ORD_001', 'ORD_002'...) dựa trên bộ đếm tăng dần.
      </td>
      <td>
        - <b>Đầu vào:</b> <code>customer_name</code> (str), <code>cart_items</code> (list of dicts dạng <code>[{"product_id": str, "quantity": int}]</code>).<br>
        - <b>Đầu ra:</b> Trả về thông tin đơn hàng mới tạo hoặc thông báo/Tuple báo lỗi nếu thất bại.
      </td>
    </tr>
    <tr>
      <td>4</td>
      <td><b>Tìm kiếm sản phẩm</b><br><code>search_products()</code></td>
      <td>
        - Cho phép tìm kiếm sản phẩm theo tên (không phân biệt chữ hoa, chữ thường - case insensitive) hoặc theo danh mục sản phẩm (category).
      </td>
      <td>
        - <b>Đầu vào:</b> <code>keyword</code> (str), <code>search_type</code> (str: 'name' hoặc 'category').<br>
        - <b>Đầu ra:</b> Danh sách (list) các sản phẩm tìm thấy phù hợp với tiêu chí lọc.
      </td>
    </tr>
    <tr>
      <td>5</td>
      <td><b>Báo cáo thống kê hoạt động</b><br><code>generate_revenue_report()</code></td>
      <td>
        - Tính toán tổng doanh thu tích lũy từ tất cả các đơn hàng đã tạo thành công.<br>
        - Tìm ra sản phẩm bán chạy nhất (dựa trên tổng số lượng đã bán được qua các đơn hàng).<br>
        - Hiển thị danh sách các sản phẩm đang rơi vào trạng thái cần nhập hàng gấp (tồn kho dưới hạn định).
      </td>
      <td>
        - <b>Đầu vào:</b> Không có.<br>
        - <b>Đầu ra:</b> Trả về một dict chứa các chỉ số: <code>total_revenue</code> (float), <code>best_seller</code> (str), <code>low_stock_items</code> (list).
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Đặc tả phi chức năng (Non-Functional Requirements)**

1. **Hiệu năng & Khả năng đáp ứng thời gian thực (Performance):**
   - Do chạy hoàn toàn trên RAM và sử dụng cấu trúc dữ liệu băm (Hash Map - Dictionary của Python), các thao tác tìm kiếm sản phẩm theo ID hoặc cập nhật số lượng tồn kho phải đạt độ phức tạp tiệm cận $O(1)$.
   
2. **Giao diện người dùng CLI trực quan (Console UX):**
   - Sử dụng định dạng căn lề chuỗi (String formatting - f-string với định dạng chiều rộng cố định) để căn đều các cột dữ liệu khi in ra màn hình.
   - Menu chính phải sử dụng vòng lặp vô hạn `while True` và hiển thị lời chào, danh sách lựa chọn đánh số từ 1 đến 6 rõ ràng, chỉ thoát chương trình khi người dùng chủ động lựa chọn lệnh thích hợp.

3. **Tính toàn vẹn dữ liệu (Data Integrity):**
   - Đảm bảo cơ chế đồng bộ số lượng: Khi tạo một đơn hàng thành công, số lượng tồn kho của sản phẩm trong biến lưu trữ hệ thống phải được trừ ngay lập tức. Nếu quá trình tạo đơn gặp lỗi giữa chừng (ví dụ: một trong số các sản phẩm bị thiếu hàng), toàn bộ giao dịch mua hàng của đơn đó phải bị hủy bỏ để tránh tình trạng trừ kho không đồng đều (Atomic operations).

---

### **4. Đặc tả dữ liệu (Data Model / Schemas)**

Vì dự án bị giới hạn ở phạm vi kiến thức Session 09, hệ thống không sử dụng Lớp (Class/OOP) hay tập tin ngoại vi (File I/O). Toàn bộ dữ liệu được quản lý tập trung thông qua hai cấu trúc dữ liệu chính ở phạm vi toàn cục (global variables):

```python
# Cấu trúc lưu trữ kho hàng (Inventory): Sử dụng Dictionary với Key là mã sản phẩm
# product_id (str) -> dict chứa thông tin chi tiết sản phẩm.
inventory = {
    "PROD001": {
        "name": "Mechanical Keyboard",
        "price": 89.99,
        "quantity": 12,
        "category": "Accessories"
    },
    "PROD002": {
        "name": "Wireless Mouse",
        "price": 25.50,
        "quantity": 3,  # Gắn nhãn LOW STOCK do < 5
        "category": "Accessories"
    }
}

# Cấu trúc lưu trữ danh sách đơn hàng (Orders): Sử dụng List chứa các Dictionary con
orders = [
    {
        "order_id": "ORD_001",
        "customer_name": "Alice Pham",
        "items": [
            {"product_id": "PROD001", "quantity": 1},
            {"product_id": "PROD002", "quantity": 2}
        ],
        "total_amount": 140.99,
        "status": "Completed"
    }
]
```

---

### **5. Quy tắc kiểm soát lỗi và Xử lý ngoại lệ (Exception Handling & Error Rules)**

Hệ thống quản lý lỗi thông qua việc kiểm tra tính hợp lệ của dữ liệu đầu vào (Input Validation) kết hợp khối lệnh kiểm soát lỗi `try-except` của Python để ngăn chặn ứng dụng bị dừng đột ngột (crash). Các quy định xử lý lỗi chi tiết bao gồm:

1. **Lỗi nhập liệu sai kiểu dữ liệu (TypeError / ValueError):**
   - Khi người dùng nhập giá bán sản phẩm hoặc số lượng mặt hàng cần mua, chương trình phải bọc lệnh chuyển đổi kiểu dữ liệu (`float(input())` hoặc `int(input())`) trong khối lệnh `try-except ValueError`.
   - Nếu phát hiện đầu vào chứa chữ cái hoặc ký tự đặc biệt, chương trình phải in thông báo lỗi: *"Error: Invalid digital formats. Please try again."* và quay trở lại luồng nhập liệu.

2. **Lỗi logic nghiệp vụ kho hàng (Business Logic Errors):**
   - **Lỗi hết hàng (Out of Stock Error):** Khi lượng tồn kho thực tế của sản phẩm nhỏ hơn số lượng yêu cầu trong đơn đặt hàng. Hàm xử lý cần trả về mã lỗi cụ thể hoặc một Tuple dạng `(False, "Requested quantity exceeds available stock.")`.
   - **Lỗi trùng lặp dữ liệu không mong muốn:** Khi trường dữ liệu đầu vào rỗng (Empty String) hoặc giá trị của đơn giá/số lượng mang giá trị âm.

3. **Nguyên tắc phản hồi lỗi:**
   - Hoàn toàn không sử dụng định dạng JSON bao đóng (REST API envelopes) hay mã trạng thái HTTP. Mọi thông báo lỗi phải được xuất trực tiếp ra màn hình console bằng các chuỗi ký tự tường minh và dễ hiểu với người dùng cuối.

---

### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left; width: 5%;">STT</th>
      <th style="padding: 8px; text-align: left; width: 25%;">Tình huống biên / Tình huống lỗi</th>
      <th style="padding: 8px; text-align: left; width: 40%;">Hành vi mong muốn của hệ thống</th>
      <th style="padding: 8px; text-align: left; width: 30%;">Ngoại lệ phát sinh/Cách xử lý</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Người dùng nhập đơn giá hoặc số lượng là số âm hoặc bằng 0 khi thêm sản phẩm.</td>
      <td>Hệ thống từ chối cập nhật dữ liệu vào kho hàng, in ra cảnh báo yêu cầu nhập số dương lớn hơn 0.</td>
      <td>Giải quyết bằng cấu trúc điều kiện <code>if price <= 0 or quantity < 0</code> để chặn trước khi gán giá trị.</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Tạo đơn hàng với mã sản phẩm không tồn tại trong danh mục <code>inventory</code>.</td>
      <td>Hệ thống phát hiện mã sản phẩm không khớp, hủy bỏ việc tạo đơn và hiển thị danh sách các mã lỗi.</td>
      <td>Bắt lỗi <code>KeyError</code> hoặc dùng phương thức <code>dict.get()</code> trả về <code>None</code> để thông báo mã hàng không hợp lệ.</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Nhập chuỗi trống (rỗng hoặc chỉ toàn khoảng trắng) cho Tên sản phẩm hoặc Tên khách hàng.</td>
      <td>Yêu cầu nhập lại trường tương ứng, không chấp nhận lưu trữ các thông tin rỗng vào danh mục.</td>
      <td>Sử dụng phương thức <code>strip()</code>: <code>if not name.strip():</code> để kiểm tra tính hợp lệ của chuỗi ký tự đầu vào.</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Nhập lựa chọn menu không có trong danh sách hiển thị (Ví dụ: Nhập vào số '9' hoặc chữ 'abc').</td>
      <td>Hệ thống thông báo lựa chọn không hợp lệ và hiển thị lại menu để người dùng tiếp tục thao tác.</td>
      <td>Sử dụng khối lệnh điều kiện <code>if user_choice not in ['1', '2', '3', '4', '5', '6']</code> kết hợp vòng lặp điều hướng.</td>
    </tr>
  </tbody>
</table>

---

### **7. Quy trình chạy thử nghiệm Console (Console Execution & Test Scenarios)**

Để kiểm thử tính ổn định và chính xác của Hệ thống WOMS, người vận hành thực hiện tuần tự kịch bản thử nghiệm kiểm thử hộp đen đầu cuối (End-to-End Blackbox Testing) trên giao diện CLI như sau:

*   **Bước 1: Khởi động hệ thống & Tạo dữ liệu ban đầu**
    *   *Hành động:* Chọn menu `1` để thêm sản phẩm mới.
    *   *Dữ liệu nhập:* `ID = PROD001`, `Tên = Monitor LG 24`, `Giá = 150`, `Số lượng = 10`, `Phân loại = Screen`.
    *   *Kết quả mong đợi:* Hệ thống báo thêm mới thành công. Tiếp tục chọn menu `2` hiển thị danh sách sản phẩm cấu trúc dạng bảng để xác minh dữ liệu đã vào kho một cách chính xác.

*   **Bước 2: Kiểm thử tính năng sửa đổi cập nhật**
    *   *Hành động:* Chọn menu `1` một lần nữa để cập nhật sản phẩm có mã trùng lặp.
    *   *Dữ liệu nhập:* `ID = PROD001`, `Tên = Monitor LG 24`, `Giá = 160`, `Số lượng = 5`, `Phân loại = Screen`.
    *   *Kết quả mong đợi:* Hệ thống không tạo thêm sản phẩm mới mà cập nhật giá bán thành `160` và cộng dồn số lượng hiện tại lên thành `15` (`10` cũ + `5` mới).

*   **Bước 3: Kiểm thử kịch bản tạo đơn hàng thông thường**
    *   *Hành động:* Chọn menu `3` để tạo đơn đặt hàng mới.
    *   *Dữ liệu nhập:* Tên khách hàng: `Bob Vance`. Chọn mã sản phẩm `PROD001` với số lượng mua là `4`.
    *   *Kết quả dự kiến:* Đơn hàng được tạo với mã đơn hàng tự động tăng (ví dụ: `ORD_001`), tổng tiền đơn hàng là $4 \times 160 = 640$. Số lượng tồn kho thực tế của mã `PROD001` giảm xuống còn `11`.

*   **Bước 4: Kiểm thử kịch bản mua vượt quá tồn kho (Edge Case)**
    *   *Hành động:* Chọn tiếp menu `3` để tạo đơn hàng khác.
    *   *Dữ liệu nhập:* Tên khách hàng: `Charlotte`. Chọn mã sản phẩm `PROD001` với số lượng mua là `15` (trong khi kho hiện tại chỉ còn `11`).
    *   *Kết quả dự kiến:* Hệ thống thông báo lỗi thiếu hàng trong kho, chấm dứt việc tạo đơn hàng mới và bảo toàn con số tồn kho `11` của sản phẩm phụ.
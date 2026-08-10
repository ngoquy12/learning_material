## <center>Tài liệu đặc tả Hệ thống Quản lý Kho hàng Bán lẻ (Retail Inventory Management Console System)</center>

### **1. Tổng quan hệ thống**

Hệ thống **Quản lý Kho hàng Bán lẻ (Retail Inventory Management Console System)** là ứng dụng giao diện dòng lệnh (CLI Core Application) phục vụ các cửa hàng bán lẻ vừa và nhỏ trong việc theo dõi, thêm mới, cập nhật, xóa và thống kê danh mục sản phẩm trong kho. Hệ thống được triển khai trên nền tảng Python thuần (`python/core`), vận hành hoàn toàn trong môi trường dòng lệnh thông qua vòng lặp menu tương tác, không yêu cầu cơ sở dữ liệu bên ngoài hay thư viện ngoài phức tạp.

Hệ thống tận dụng tối đa các cấu trúc dữ liệu căn bản (danh sách `list`, bộ dữ liệu `tuple`) và các luồng điều khiển chuẩn (`while`, `for`, `if-elif-else`) kết hợp xử lý ngoại lệ nguyên bản (`try-except`) nhằm đảm bảo tính toàn vẹn dữ liệu, hiệu năng phản hồi tức thì và sự ổn định cao trong suốt phiên làm việc.

<div class="mermaid-diagram-container" style="background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin: 20px 0; overflow-x: auto;">
  <div class="mermaid" style="display: flex; justify-content: center; color: #f8fafc;">
flowchart TD
    classDef startEnd fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#ecfdf5;
    classDef process fill:#1e293b,stroke:#64748b,stroke-width:2px,color:#f8fafc;
    classDef inputOutput fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#e0e7ff;
    classDef decision fill:#451a03,stroke:#f59e0b,stroke-width:2px,color:#fffbeb;
    classDef storage fill:#0369a1,stroke:#38bdf8,stroke-width:2px,color:#f0f9ff;
    classDef errorState fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#fef2f2;

    subgraph SubInit ["1. Khởi Tạo Bộ Nhớ & Dữ Liệu"]
        Start(["Khởi động ứng dụng Console"]):::startEnd
        InitRAM["Khởi tạo danh sách trong bộ nhớ RAM<br>inventory = [('SKU001', 'Áo thun', 50, 150000.0)]"]:::storage
    end

    subgraph SubMenu ["2. Vòng Lập Menu Điều Hướng"]
        ShowMenu["Hiển thị Menu chức năng CLI & Nhận input"]:::inputOutput
        CheckChoice{"Lựa chọn của người dùng?"}:::decision
    end

    subgraph SubView ["3. Xem Danh Sách & Trị Giá Kho"]
        V_Loop["Duyệt danh sách inventory bằng vòng lặp for"]:::process
        V_Unpack["Giải nén Tuple: (sku, name, qty, price)"]:::process
        V_Calc["Cộng dồn giá trị: total_val += qty * price"]:::process
        V_Display["In thông tin dạng dòng & Tổng giá trị tồn kho"]:::inputOutput
    end

    subgraph SubAdd ["4. Thêm Sản Phẩm Mới"]
        A_Input["Nhập SKU, Tên, Số lượng, Đơn giá từ CLI"]:::inputOutput
        A_CheckSKU{"SKU đã tồn tại trong inventory?"}:::decision
        A_CheckVal{"Số lượng > 0 và Đơn giá > 0?"}:::decision
        A_ErrMsg["Báo lỗi: SKU trùng hoặc dữ liệu nhập không hợp lệ"]:::errorState
        A_MakeTuple["Tạo Tuple sản phẩm: new_item = (sku, name, qty, price)"]:::process
        A_Append["Thêm Tuple vào RAM: inventory.append(new_item)"]:::storage
        A_Success["In thông báo thêm sản phẩm thành công"]:::inputOutput
    end

    subgraph SubUpdate ["5. Cập Nhật Sản Phẩm"]
        U_InputSKU["Nhập SKU sản phẩm cần cập nhật"]:::inputOutput
        U_Search{"Tìm kiếm vị trí index của SKU trong danh sách?"}:::decision
        U_ErrSKU["Báo lỗi: Không tìm thấy SKU trong hệ thống"]:::errorState
        U_InputData["Nhập Số lượng mới & Đơn giá mới từ CLI"]:::inputOutput
        U_CheckVal{"Số lượng mới > 0 và Đơn giá mới > 0?"}:::decision
        U_ErrVal["Báo lỗi: Số lượng và giá phải lớn hơn 0"]:::errorState
        U_Replace["Ghi đè phần tử tại index:<br>inventory[idx] = (sku, original_name, new_qty, new_price)"]:::storage
        U_Success["In thông báo cập nhật thành công"]:::inputOutput
    end

    subgraph SubDelete ["6. Xóa Sản Phẩm Kho"]
        D_InputSKU["Nhập SKU sản phẩm cần xóa từ CLI"]:::inputOutput
        D_Search{"Tìm kiếm vị trí index của SKU trong danh sách?"}:::decision
        D_ErrSKU["Báo lỗi: Không tìm thấy SKU để xóa"]:::errorState
        D_Pop["Xóa Tuple khỏi bộ nhớ RAM: inventory.pop(idx)"]:::storage
        D_Success["In thông báo xóa sản phẩm thành công"]:::inputOutput
    end

    subgraph SubSearch ["7. Tìm Kiếm & Lọc Sản Phẩm"]
        S_InputKw["Nhập từ khóa tìm kiếm (SKU hoặc Tên) từ CLI"]:::inputOutput
        S_Loop["Duyệt từng Tuple trong danh sách inventory"]:::process
        S_Match{"Tên hoặc SKU chứa từ khóa?"}:::decision
        S_PrintMatch["Hiển thị dòng sản phẩm phù hợp"]:::inputOutput
        S_Skip["Bỏ qua phần tử không tương thích"]:::process
    end

    subgraph SubExit ["8. Kết Thúc Chương Trình"]
        ExitMsg["In thông báo tạm biệt & Thoát vòng lặp"]:::inputOutput
        End(["Kết thúc ứng dụng"]):::startEnd
    end

    Start --> InitRAM
    InitRAM --> ShowMenu
    ShowMenu --> CheckChoice

    CheckChoice -- "1. Xem danh sách" --> V_Loop
    V_Loop --> V_Unpack
    V_Unpack --> V_Calc
    V_Calc --> V_Display
    V_Display --> ShowMenu

    CheckChoice -- "2. Thêm mới" --> A_Input
    A_Input --> A_CheckSKU
    A_CheckSKU -- "Đã tồn tại" --> A_ErrMsg
    A_CheckSKU -- "Chưa tồn tại" --> A_CheckVal
    A_CheckVal -- "Không hợp lệ" --> A_ErrMsg
    A_ErrMsg --> ShowMenu
    A_CheckVal -- "Hợp lệ" --> A_MakeTuple
    A_MakeTuple --> A_Append
    A_Append --> A_Success
    A_Success --> ShowMenu

    CheckChoice -- "3. Cập nhật" --> U_InputSKU
    U_InputSKU --> U_Search
    U_Search -- "Không tìm thấy" --> U_ErrSKU
    U_ErrSKU --> ShowMenu
    U_Search -- "Tìm thấy" --> U_InputData
    U_InputData --> U_CheckVal
    U_CheckVal -- "Không hợp lệ" --> U_ErrVal
    U_ErrVal --> ShowMenu
    U_CheckVal -- "Hợp lệ" --> U_Replace
    U_Replace --> U_Success
    U_Success --> ShowMenu

    CheckChoice -- "4. Xóa sản phẩm" --> D_InputSKU
    D_InputSKU --> D_Search
    D_Search -- "Không tìm thấy" --> D_ErrSKU
    D_ErrSKU --> ShowMenu
    D_Search -- "Tìm thấy" --> D_Pop
    D_Pop --> D_Success
    D_Success --> ShowMenu

    CheckChoice -- "5. Tìm kiếm / Lọc" --> S_InputKw
    S_InputKw --> S_Loop
    S_Loop --> S_Match
    S_Match -- "Khớp từ khóa" --> S_PrintMatch
    S_Match -- "Không khớp" --> S_Skip
    S_PrintMatch --> ShowMenu
    S_Skip --> ShowMenu

    CheckChoice -- "6. Thoát" --> ExitMsg
    ExitMsg --> End

    CheckChoice -- "Nhập sai tùy chọn" --> ShowMenu
</div>
</div>

---

### **2. Đặc tả chức năng (Functional Requirements)**

Hệ thống cung cấp danh mục 7 chức năng cốt lõi được điều khiển qua Menu chính trên màn hình Console. Toàn bộ logic xử lý được thực thi tuần tự trong vòng lặp chính của ứng dụng.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 10%; text-align: center;">Mã CN</th>
      <th style="width: 25%; text-align: left;">Tên chức năng / Cú pháp logic</th>
      <th style="width: 30%; text-align: left;">Mô tả nghiệp vụ</th>
      <th style="width: 35%; text-align: left;">Luồng xử lý chính</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><b>FR-01</b></td>
      <td><b>Hiển thị menu và Điều hướng</b><br><code>display_menu_logic</code></td>
      <td>Hiển thị danh sách các lựa chọn thao tác từ 1 đến 7 và tiếp nhận lựa chọn của người dùng từ bàn phím.</td>
      <td>In giao diện dạng bảng bản văn; nhập chuỗi lựa chọn; kiểm tra hợp lệ bằng <code>if-elif-else</code>; chuyển tiếp luồng nghiệp vụ tương ứng.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><b>FR-02</b></td>
      <td><b>Xem danh sách hàng hóa</b><br><code>display_inventory_logic</code></td>
      <td>Xuất ra màn hình toàn bộ mặt hàng hiện có trong kho theo dạng bảng căn chỉnh cột chuẩn mực.</td>
      <td>Duyệt qua danh sách <code>inventory_list</code> bằng vòng lặp <code>for</code>; đọc từng <code>tuple</code> chứa thông tin sản phẩm; định dạng chuỗi in ra màn hình. Nếu danh sách rỗng, hiển thị thông báo kho rỗng.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><b>FR-03</b></td>
      <td><b>Thêm mới hàng hóa</b><br><code>add_inventory_item_logic</code></td>
      <td>Thêm một mặt hàng mới vào danh sách kho với mã định danh không trùng lặp và các thuộc tính hợp lệ.</td>
      <td>Nhập Mã hàng (`item_id`), Tên hàng (`item_name`), Danh mục (`category`), Số lượng (`quantity`), Đơn giá (`price`). Kiểm tra trùng lặp mã; ép kiểu dữ liệu; đóng gói vào <code>tuple</code> và `append` vào danh sách `inventory_list`.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><b>FR-04</b></td>
      <td><b>Cập nhật thông tin hàng hóa</b><br><code>update_item_by_id_logic</code></td>
      <td>Cho phép điều chỉnh số lượng tồn kho hoặc giá bán của mặt hàng dựa trên Mã hàng (`item_id`).</td>
      <td>Nhập `item_id`; tìm vị trí chỉ số (index) trong `inventory_list`; nếu tìm thấy thì yêu cầu nhập Số lượng mới và Giá mới; tạo <code>tuple</code> cập nhật và ghi đè tại vị trí chỉ số đã xác định.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><b>FR-05</b></td>
      <td><b>Xóa hàng hóa khỏi kho</b><br><code>delete_item_by_id_logic</code></td>
      <td>Loại bỏ hoàn toàn mặt hàng ra khỏi danh sách lưu trữ theo Mã hàng (`item_id`).</td>
      <td>Nhập `item_id`; duyệt tìm chỉ số tương ứng trong `inventory_list`; thực hiện thao tác xóa phần tử bằng <code>pop()</code> hoặc <code>del</code> sau khi người dùng xác nhận.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><b>FR-06</b></td>
      <td><b>Tìm kiếm và lọc hàng hóa</b><br><code>search_filter_item_logic</code></td>
      <td>Tra cứu mặt hàng theo Tên sản phẩm (chứa từ khóa) hoặc Lọc theo Danh mục sản phẩm.</td>
      <td>Nhập từ khóa tìm kiếm; chuyển chuỗi về dạng chữ thường (`lower()`); duyệt `inventory_list` và hiển thị các `tuple` thỏa mãn điều kiện lọc.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><b>FR-07</b></td>
      <td><b>Thống kê tổng giá trị kho hàng</b><br><code>calculate_total_value_logic</code></td>
      <td>Tính tổng số lượng mặt hàng, tổng số lượng tồn kho và tổng giá trị tài sản trong kho.</td>
      <td>Khởi tạo các biến tích lũy `total_items`, `total_quantity`, `total_inventory_value`; duyệt danh sách để tính toán; in báo cáo tổng hợp chi tiết ra màn hình CLI.</td>
    </tr>
  </tbody>
</table>

---

### **3. Đặc tả phi chức năng (Non-Functional Requirements)**

1. **Hiệu năng & Tốc độ phản hồi (Performance)**:
   - Thao tác xử lý dữ liệu trên danh sách `inventory_list` có quy mô dưới 5,000 phần tử phải hoàn tất dưới 0.05 giây.
   - Thời gian hiển thị giao diện menu và phản hồi lệnh từ bàn phím ngay lập tức (không có độ trễ perceptible).

2. **Giao diện dòng lệnh & Trải nghiệm người dùng (CLI UX/UI)**:
   - Giao diện dạng bản văn trực quan, sử dụng các ký tự phân cách (`=`, `-`) để chia ranh giới khu vực rõ ràng.
   - Dữ liệu hiển thị dạng bảng phải được căn chỉnh cột chính xác bằng định dạng chuỗi (`f-string` format specifiers: e.g., `{item_id:<8}`).
   - Các thông báo thành công hoặc lỗi phải phân biệt bằng tiền tố rõ ràng: `[THÀNH CÔNG]`, `[LỖI]`, `[CẢNH BÁO]`.

3. **Tính toàn vẹn dữ liệu & Khả năng chịu lỗi (Data Integrity & Fault Tolerance)**:
   - Sai sót nhập liệu của người dùng (nhập chữ vào trường số, nhập số âm) không được làm sụp đổ (crash) chương trình.
   - Chương trình tự động quay lại menu chính sau khi thông báo lỗi mà không làm mất dữ liệu đã lưu trong bộ nhớ RAM.

4. **Khả năng duy trì và Tương thích (Compatibility & Standards)**:
   - Mã nguồn tương thích hoàn toàn với Python phiên bản 3.8+.
   - Không phụ thuộc vào bất kỳ thư viện bên thứ ba (Third-party library) nào ngoài thư viện chuẩn của Python.

---

### **4. Đặc tả dữ liệu (Data Model / Schemas)**

Dữ liệu kho hàng được quản lý dưới dạng cấu trúc Danh sách chứa các Bộ dữ liệu không thay đổi (`List` of `Tuple`).

#### **4.1. Cấu trúc lưu trữ chính (In-Memory Data Structure)**
```python
# Cấu trúc tổng quát của danh sách kho hàng
inventory_list = [
    (item_id, item_name, category, quantity, price),
    (101, "Aao Sơ mi Nam Oxford", "Thời trang", 45, 350000.0),
    (102, "Quần Jean Slimfit", "Thời trang", 30, 520000.0),
    (201, "Giày Sneaker Thể thao", "Giày dép", 15, 890000.0)
]
```

#### **4.2. Bảng đặc tả các trường dữ liệu (Data Element Dictionary)**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 15%; text-align: left;">Tên trường (Field Name)</th>
      <th style="width: 12%; text-align: center;">Kiểu dữ liệu</th>
      <th style="width: 10%; text-align: center;">Bắt buộc</th>
      <th style="width: 25%; text-align: left;">Mô tả chi tiết</th>
      <th style="width: 38%; text-align: left;">Ràng buộc dữ liệu (Validation Rules)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>item_id</code></td>
      <td style="text-align: center;"><code>int</code></td>
      <td style="text-align: center;">Có</td>
      <td>Mã định danh duy nhất của sản phẩm.</td>
      <td>Số nguyên dương (<code>item_id > 0</code>), duy nhất trong toàn bộ danh sách.</td>
    </tr>
    <tr>
      <td><code>item_name</code></td>
      <td style="text-align: center;"><code>str</code></td>
      <td style="text-align: center;">Có</td>
      <td>Tên tên chi tiết của mặt hàng.</td>
      <td>Độ dài từ 2 đến 100 ký tự, không được để trống hoặc chỉ chứa khoảng trắng.</td>
    </tr>
    <tr>
      <td><code>category</code></td>
      <td style="text-align: center;"><code>str</code></td>
      <td style="text-align: center;">Có</td>
      <td>Phân loại hàng hóa.</td>
      <td>Chuỗi ký tự nhận diện nhóm mặt hàng (VD: "Thời trang", "Điện máy").</td>
    </tr>
    <tr>
      <td><code>quantity</code></td>
      <td style="text-align: center;"><code>int</code></td>
      <td style="text-align: center;">Có</td>
      <td>Số lượng tồn kho hiện tại.</td>
      <td>Số nguyên không âm (<code>quantity >= 0</code>).</td>
    </tr>
    <tr>
      <td><code>price</code></td>
      <td style="text-align: center;"><code>float</code></td>
      <td style="text-align: center;">Có</td>
      <td>Đơn giá bán niêm yết (VNĐ).</td>
      <td>Số thực lớn hơn 0 (<code>price > 0.0</code>).</td>
    </tr>
  </tbody>
</table>

---

### **5. Quy tắc kiểm soát lỗi và Xử lý ngoại lệ (Exception Handling & Error Rules)**

Để bảo đảm ứng dụng CLI hoạt động liên tục mà không bị dừng đột ngột do lỗi nhập liệu, hệ thống áp dụng các quy tắc kiểm soát lỗi sau:

1. **Khôi phục lỗi nhập kiểu dữ liệu (Data Type Error Recovery)**:
   - Sử dụng khối `try-except ValueError` bọc quanh các thao tác chuyển kiểu `int(input(...))` hoặc `float(input(...))`.
   - Nếu phát sinh `ValueError`, hệ thống in thông báo `[LỖI] Dữ liệu nhập vào phải là số hợp lệ!` và dùng câu lệnh `continue` để quay lại đầu vòng lặp menu hoặc cho phép nhập lại.

2. **Ràng buộc logic giá trị (Business Domain Validations)**:
   - Giá trị `quantity` < 0 hoặc `price` <= 0 sẽ kích hoạt thông báo lỗi giá trị âm và ngắt luồng thêm/sửa sản phẩm.
   - Khi thực hiện thêm mới, kiểm tra sự tồn tại của `item_id` bằng vòng lặp quét danh sách. Nếu `item_id` đã tồn tại, hủy thao tác thêm và báo trùng lặp.

3. **Kiểm tra ranh giới danh sách (Boundary checks)**:
   - Thao tác sửa/xóa yêu cầu quét tìm vị trí phần tử trong `inventory_list`. Nếu duyệt hết danh sách mà không thấy `item_id` phù hợp, xuất thông báo `[LỖI] Không tìm thấy sản phẩm có mã ID đã nhập`.

---

### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 15%; text-align: left;">Mã tình huống</th>
      <th style="width: 25%; text-align: left;">Kịch bản phát sinh lỗi</th>
      <th style="width: 20%; text-align: center;">Ngoại lệ / Điều kiện phát hiện</th>
      <th style="width: 40%; text-align: left;">Hành vi xử lý của ứng dụng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>EC-01</b></td>
      <td>Người dùng nhập ký tự chữ khi chọn menu hoặc nhập ID/Số lượng/Đơn giá.</td>
      <td style="text-align: center;"><code>ValueError</code></td>
      <td>Bắt ngoại lệ <code>ValueError</code>, in ra: <i>"[LỖI] Vui lòng chỉ nhập số nguyên/số thực!"</i>, bỏ qua thao tác hiện tại và hiển thị lại Menu.</td>
    </tr>
    <tr>
      <td><b>EC-02</b></td>
      <td>Thêm sản phẩm mới với <code>item_id</code> trùng với một mặt hàng đã tồn tại.</td>
      <td style="text-align: center;">Cờ kiểm tra trùng dư (Duplicate Flag) trong vòng lặp Duyệt</td>
      <td>Hủy thao tác thêm, in ra: <i>"[LỖI] Mã sản phẩm [ID] đã tồn tại trong hệ thống!"</i>, giữ nguyên danh sách cũ.</td>
    </tr>
    <tr>
      <td><b>EC-03</b></td>
      <td>Nhập số lượng âm (<code>quantity < 0</code>) hoặc giá bán không hợp lệ (<code>price <= 0</code>).</td>
      <td style="text-align: center;">Kiểm tra điều kiện Logic (<code>if quantity < 0 or price <= 0</code>)</td>
      <td>In ra: <i>"[LỖI] Số lượng không được âm và giá bán phải lớn hơn 0!"</i>, hủy bỏ quá trình tạo/sửa sản phẩm.</td>
    </tr>
    <tr>
      <td><b>EC-04</b></td>
      <td>Thao tác Sửa (FR-04) hoặc Xóa (FR-05) với một <code>item_id</code> không có trong kho.</td>
      <td style="text-align: center;">Chỉ số tìm kiếm <code>item_index == -1</code> sau khi duyệt danh sách</td>
      <td>In ra: <i>"[LỖI] Không tìm thấy sản phẩm có mã ID [ID] trong hệ thống!"</i>, quay về menu chính.</td>
    </tr>
    <tr>
      <td><b>EC-05</b></td>
      <td>Thực hiện Xem/Thống kê/Xóa khi danh sách kho hàng <code>inventory_list</code> đang rỗng (0 phần tử).</td>
      <td style="text-align: center;">Kiểm tra độ dài <code>len(inventory_list) == 0</code></td>
      <td>In ra: <i>"[THÔNG BÁO] Kho hàng hiện đang rỗng. Chưa có dữ liệu để thực thi!"</i>, ngừng duyệt danh sách.</td>
    </tr>
    <tr>
      <td><b>EC-06</b></td>
      <td>Tên sản phẩm nhập vào chỉ chứa khoảng trắng hoặc để trống.</td>
      <td style="text-align: center;">Kiểm tra chuỗi rỗng <code>len(item_name.strip()) == 0</code></td>
      <td>In ra: <i>"[LỖI] Tên sản phẩm không được để trống!"</i>, yêu cầu nhập lại hoặc hủy thao tác.</td>
    </tr>
  </tbody>
</table>

---

### **7. Quy trình chạy thử nghiệm Console (Console Execution & Test Scenarios)**

Dưới đây là kịch bản chạy thử nghiệm thực tế của ứng dụng CLI Quản lý kho hàng:

#### **Kịch bản 1: Khởi chạy và Thêm mới sản phẩm hợp lệ**
```text
==================================================
   HỆ THỐNG QUẢN LÝ KHO HÀNG BÁN LẺ (CONSOLE)
==================================================
1. Xem danh sách kho hàng
2. Thêm mới sản phẩm
3. Cập nhật số lượng / giá bán
4. Xóa sản phẩm theo Mã ID
5. Tìm kiếm sản phẩm
6. Báo cáo thống kê kho hàng
7. Thoát chương trình
==================================================
Lựa chọn của bạn (1-7): 2

--- THÊM MỚI SẢN PHẨM ---
Nhập Mã sản phẩm (ID): 101
Nhập Tên sản phẩm: Áo Sơ mi Nam Oxford
Nhập Danh mục: Thời trang
Nhập Số lượng tồn kho: 50
Nhập Đơn giá bán (VNĐ): 350000

[THÀNH CÔNG] Đã thêm sản phẩm 'Áo Sơ mi Nam Oxford' vào kho hàng!
```

#### **Kịch bản 2: Bắt lỗi nhập liệu sai kiểu dữ liệu và trùng ID**
```text
Lựa chọn của bạn (1-7): 2

--- THÊM MỚI SẢN PHẨM ---
Nhập Mã sản phẩm (ID): abc
[LỖI] Dữ liệu nhập vào phải là số hợp lệ!

Lựa chọn của bạn (1-7): 2

--- THÊM MỚI SẢN PHẨM ---
Nhập Mã sản phẩm (ID): 101
Nhập Tên sản phẩm: Áo Thun Polo
[LỖI] Mã sản phẩm 101 đã tồn tại trong hệ thống!
```

#### **Kịch bản 3: Hiển thị danh sách kho hàng định dạng chuẩn**
```text
Lựa chọn của bạn (1-7): 1

========================================================================================
                               DANH SÁCH HÀNG HÓA TRONG KHO
========================================================================================
STT   Mã ID   Tên sản phẩm                Danh mục        Số lượng   Đơn giá (VNĐ)   
----------------------------------------------------------------------------------------
1     101     Áo Sơ mi Nam Oxford         Thời trang      50         350,000.0       
2     102     Quần Jean Slimfit           Thời trang      30         520,000.0       
========================================================================================
Tổng số mặt hàng: 2
```

#### **Kịch bản 4: Thống kê tổng giá trị kho hàng**
```text
Lựa chọn của bạn (1-7): 6

==================================================
             BÁO CÁO THỐNG KÊ KHO HÀNG
==================================================
- Tổng số loại mặt hàng: 2 mặt hàng
- Tổng số lượng tồn kho: 80 sản phẩm
- Tổng giá trị kho hàng: 33,100,000.0 VNĐ
==================================================
```
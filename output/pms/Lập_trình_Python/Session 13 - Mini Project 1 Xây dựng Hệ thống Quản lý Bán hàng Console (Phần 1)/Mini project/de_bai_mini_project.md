## <center>[Mini project] Xây dựng Hệ thống Quản lý Bán hàng Console (Phần 1) (Console Sales Management System - Part 1)</center>

### **1. Mục tiêu dự án**

Dự án Mini Project 1 yêu cầu học viên xây dựng một ứng dụng Console (Command Line Interface - CLI) quản lý bán hàng cốt lõi bằng ngôn ngữ **Python 3.12**. Hệ thống tập trung vào việc quản lý danh mục sản phẩm, xử lý giỏ hàng, tính toán hóa đơn và lưu trữ dữ liệu thông qua các hàm xử lý logic (Functional Programming) cùng cấu trúc dữ liệu nguyên bản (Dictionary, List, Tuple).

Thông qua dự án này, học viên sẽ đạt được các mục tiêu sau:
*   [REQUIREMENT] Thành thạo kỹ năng thiết lập môi trường phát triển ứng dụng Python chuẩn với `virtualenv`, quản lý thư viện và sử dụng các IDE hiện đại như Cursor / Windsurf AI IDE.
*   [REQUIREMENT] Áp dụng triệt để quy chuẩn viết mã **PEP 8** và hệ thống gợi ý kiểu dữ liệu **Type Hints** (`typing` module) trong Python 3.12 để mã nguồn rõ ràng, dễ bảo trì.
*   [REQUIREMENT] Làm chủ tư duy lập trình cấu trúc/hàm (Procedural / Functional Programming), xử lý cấu trúc dữ liệu phức tạp dạng lồng nhau (Nested Data Structures) mà không sử dụng Lập trình hướng đối tượng (OOP Class).
*   [REQUIREMENT] Tối ưu hóa mô hình xử lý lỗi nguyên bản (Native Exceptions Handling) với `try-except` để đảm bảo ứng dụng Console hoạt động liên tục, không bị ngắt đột ngột khi người dùng nhập sai dữ liệu.

---

### **2. Đề bài và Yêu cầu**

Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md).

#### **2.1. Cấu trúc dữ liệu yêu cầu**
Hệ thống sử dụng các cấu trúc dữ liệu tiêu chuẩn (List, Dict) để lưu trữ thông tin trong bộ nhớ tạm (In-memory) hoặc qua các tệp văn bản (JSON/CSV):
*   **Sản phẩm (Product Dict):** Cấu trúc bao gồm các khóa: `productId` (str), `productName` (str), `unitPrice` (float), `quantityInStock` (int), `category` (str).
*   **Mục giỏ hàng (Cart Item Dict):** Cấu trúc bao gồm: `productId` (str), `quantity` (int), `subTotal` (float).
*   **Đơn hàng (Order Dict):** Cấu trúc bao gồm: `orderId` (str), `items` (List[Dict]), `totalAmount` (float), `createdAt` (str).

#### **2.2. Danh mục chức năng nghiệp vụ**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="6">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%; text-align: left;">Phân hệ / Nhóm hàm</th>
      <th style="width: 30%; text-align: left;">Tên chức năng / Hàm</th>
      <th style="width: 45%; text-align: left;">Mô tả nghiệp vụ kỹ thuật</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Quản lý Kho hàng</b></td>
      <td><b>[Thêm sản phẩm mới]</b><br><code>addProduct()</code></td>
      <td>Nhận đầu vào thông tin sản phẩm. Kiểm tra `productId` trùng lặp, `unitPrice` > 0, `quantityInStock` >= 0. Trả về sản phẩm vừa tạo hoặc báo lỗi qua Native Exception / tuple trạng thái.</td>
    </tr>
    <tr>
      <td><b>Quản lý Kho hàng</b></td>
      <td><b>[Cập nhật số lượng kho]</b><br><code>updateProductQuantity()</code></td>
      <td>Tìm sản phẩm theo `productId` và cập nhật lại `quantityInStock`. Đảm bảo số lượng kho mới không âm.</td>
    </tr>
    <tr>
      <td><b>Tra cứu thông tin</b></td>
      <td><b>[Tìm kiếm theo mã/tên]</b><br><code>findProductById()</code><br><code>searchProductsByName()</code></td>
      <td>Tìm kiếm chính xác theo `productId` hoặc tìm kiếm gần đúng (case-insensitive) theo `productName`. Trả về `Dict` chứa sản phẩm hoặc `None`.</td>
    </tr>
    <tr>
      <td><b>Tra cứu thông tin</b></td>
      <td><b>[Lọc theo danh mục]</b><br><code>filterProductsByCategory()</code></td>
      <td>Lọc danh sách sản phẩm thuộc một danh mục (`category`) cụ thể. Trả về danh sách `List[Dict]`.</td>
    </tr>
    <tr>
      <td><b>Nghiệp vụ Bán hàng</b></td>
      <td><b>[Thêm vào giỏ hàng]</b><br><code>addItemToCart()</code></td>
      <td>Thêm `productId` và `quantity` vào giỏ hàng. Kiểm tra số lượng mua không vượt quá `quantityInStock`. Cập nhật `subTotal`.</td>
    </tr>
    <tr>
      <td><b>Nghiệp vụ Bán hàng</b></td>
      <td><b>[Tính tổng giỏ hàng]</b><br><code>calculateCartTotal()</code></td>
      <td>Duyệt qua danh sách giỏ hàng, tính tổng số tiền `totalAmount`. Áp dụng giảm giá (nếu có chiết khấu hợp lệ).</td>
    </tr>
    <tr>
      <td><b>Nghiệp vụ Bán hàng</b></td>
      <td><b>[Thanh toán đơn hàng]</b><br><code>checkoutCart()</code></td>
      <td>Tạo `Order Dict`, trừ số lượng tồn kho tương ứng trong danh sách sản phẩm, làm rỗng giỏ hàng và lưu lịch sử đơn hàng.</td>
    </tr>
    <tr>
      <td><b>Lưu trữ & Khôi phục</b></td>
      <td><b>[Lưu và Đọc tệp dữ liệu]</b><br><code>saveDataToFile()</code><br><code>loadDataFromFile()</code></td>
      <td>Ghi danh sách sản phẩm và đơn hàng vào tệp JSON/CSV để duy trì dữ liệu khi khởi động lại ứng dụng. Xử lý lỗi `FileNotFoundError` hoặc tệp bị hỏng.</td>
    </tr>
    <tr>
      <td><b>Điều khiển CLI</b></td>
      <td><b>[Menu và Điều hướng]</b><br><code>displayMenu()</code><br><code>runConsoleApp()</code></td>
      <td>Vòng lặp Console CLI chính (`while True`), hiển thị bảng chọn, nhận đầu vào người dùng, lỗi thường gặp nhập liệu và điều hướng hàm tương ứng.</td>
    </tr>
  </tbody>
</table>

#### **2.3. Phạm vi Cấm (Forbidden Scope)**
[WARNING] Học viên tuyệt đối **KHÔNG** được sử dụng các kiến thức và công nghệ sau trong phiên này:
1.  **TUYỆT ĐỐI CẤM** sử dụng Lập trình hướng đối tượng (OOP Class - từ khóa `class`). Tất cả phải viết dạng Module và các Hàm thuần túy (Functions).
2.  **TUYỆT ĐỐI CẤM** kết nối Cơ sở dữ liệu SQL (SQLite, PostgreSQL, MySQL...). Chỉ dùng bộ nhớ RAM (In-memory Structures) và Tệp tin phẳng (JSON/CSV).
3.  **TUYỆT ĐỐI CẤM** sử dụng HTTP Status Code (200, 400, 404), REST API Envelopes (`{"status": "success", "data": ...}`), Controllers hoặc Web Frameworks.

---

### **3. Yêu cầu nộp bài**

1.  **Cấu trúc thư mục mã nguồn:**
    ```text
    sales_console_app/
    ├── .venv/                      # Môi trường ảo virtualenv
    ├── data/
    │   ├── products.json           # Tệp lưu trữ dữ liệu sản phẩm
    │   └── orders.json             # Tệp lưu trữ lịch sử đơn hàng
    ├── src/
    │   ├── __init__.py
    │   ├── product_service.py      # Module chứa logic quản lý sản phẩm
    │   ├── order_service.py        # Module chứa logic giỏ hàng & thanh toán
    │   ├── storage_service.py      # Module lưu/đọc file JSON
    │   └── utils.py                # Hàm tiện ích (validate, format tiền tệ)
    ├── main.py                     # Điểm chạy chính của ứng dụng CLI
    ├── requirements.txt            # Danh sách thư viện (nếu có)
    └── README.md                   # Hướng dẫn cài đặt và chạy ứng dụng
    ```
2.  **Hình thức nộp bài:**
    *   Học viên khởi tạo một GitHub Repository công khai (hoặc riêng tư và thêm quyền truy cập cho giảng viên).
    *   Nộp liên kết GitHub Repository lên hệ thống quản lý học tập theo đúng thời hạn quy định.
    *   Commit history trên Git phải thể hiện rõ tiến trình tự làm việc và sử dụng Cursor/Windsurf AI IDE một cách minh bạch.
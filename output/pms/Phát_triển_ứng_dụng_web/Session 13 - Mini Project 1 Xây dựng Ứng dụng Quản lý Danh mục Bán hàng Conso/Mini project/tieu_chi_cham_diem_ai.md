# **Tiêu chí chấm điểm (AI)**
**Mini Project 1: Xây dựng Ứng dụng Quản lý Danh mục Bán hàng Console (Phần 1) — Tổng điểm: 100 điểm**

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
* **Tổ chức thư mục dự án (10 điểm):** Cấu trúc cây thư mục hợp lý, tách biệt file dữ liệu JSON, file cấu hình và file mã nguồn xử lý logic (`index.js`, `catalogManager.js`).
* **Định dạng và Đọc dữ liệu JSON (10 điểm):** Cấu trúc file `initialCatalog.json` đúng chuẩn JSON specification. Khởi tạo mảng sản phẩm thành công từ chuỗi dữ liệu JSON thông qua `JSON.parse()`.

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
* **Thêm sản phẩm mới `addProduct()` (10 điểm):** Thêm đối tượng vào mảng đúng phương thức (`.push()`), gán đúng chỉ số và lưu trữ dữ liệu chính xác.
* **Cập nhật và Xóa sản phẩm `updateProduct()`, `removeProduct()` (10 điểm):** Tìm kiếm đúng phần tử theo `productId`, cập nhật giá trị thuộc tính object chuẩn xác và xóa đúng phần tử bằng `.splice()`.
* **Duyệt và Báo cáo Danh mục `displayCatalogReport()` (10 điểm):** Sử dụng vòng lặp duyệt mảng hiệu quả, tính đúng tổng giá trị tồn kho (`price * quantity`), đếm chính xác sản phẩm hết hàng và in kết quả bằng Template Literals.

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
* **Validation dữ liệu đầu vào (15 điểm):** Kiểm tra trùng lặp `productId`, bắt lỗi tên sản phẩm rỗng, lỗi đơn giá <= 0, lỗi số lượng tồn kho âm (`quantity < 0`).
* **Xử lý ngoại lệ dữ liệu & Khôi phục luồng (15 điểm):** Sử dụng khối `try-catch` để bắt lỗi parse JSON hỏng, bắt lỗi khi không tìm thấy `productId` cần sửa/xóa và thông báo lỗi rõ nghĩa ra Console mà không làm sập ứng dụng.

#### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
* **Lọc và Định dạng Nâng cao (10 điểm):** Định dạng hiển thị tiền tệ (VND) chuẩn xác có dấu phân cách hàng nghìn (ví dụ: `1,250,000 VND`), triển khai tính năng lọc sản phẩm theo nhóm danh mục (`category`) hoặc tìm kiếm theo từ khóa tên sản phẩm.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **Quy chuẩn mã sạch Clean Code (5 điểm):** Tên biến, thuộc tính object, hàm được đặt 100% bằng Tiếng Anh có nghĩa theo quy chuẩn camelCase (`productId`, `productName`, `isAvailable`). Mã nguồn thụt lề chuẩn xác, không dư thừa code rác.
* **Quy chuẩn Git & Nộp bài (5 điểm):** Repository Public trên GitHub, file `README.md` đầy đủ hướng dẫn chạy mã nguồn bằng Node.js CLI, lịch sử commit rõ ràng.

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
* **Bonus (+5 điểm):** Viết module ghi nhận nhật ký thao tác (Log Activity) lưu trữ các hành động Thêm/Sửa/Xóa vào một mảng nhật ký hệ thống kèm mốc thời gian (Timestamp).
* **Bonus (+5 điểm):** Thiết lập menu tương tác lựa chọn chức năng dạng CLI bằng vòng lặp `while` và câu lệnh `switch-case`.

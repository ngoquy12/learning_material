# <center>[Phân tích 2] Phân tích và Thiết kế Module Tính Tiền Hóa Đơn POS Highlands Coffee</center>

### **1. Mục tiêu**
*   **Phân tích kỹ thuật chuyên sâu:** Đánh giá các phương án xử lý số liệu tiền tệ trên giao diện dòng lệnh (CLI) nhằm tránh hiện tượng mất chính xác do sai số dấu chấm động (floating-point precision loss) khi thực hiện các phép tính phần trăm chiết khấu và thuế VAT.
*   **Ứng dụng kiến thức nền tảng:** Sử dụng thành thạo thao tác khai báo biến, chuyển đổi kiểu dữ liệu (`int`, `float`, `str`), phép toán số học và định dạng chuỗi xuất dữ liệu (`f-string`) trong Python.
*   **Thiết kế luồng xử lý chuẩn hóa:** Xây dựng sơ đồ tư duy/lưu đồ thuật toán (Flowchart) cho bài toán tính hóa đơn thanh toán trước khi hiện thực hóa bằng mã nguồn.

### **2. Bối cảnh & Vấn đề**
Chuỗi cửa hàng Highlands Coffee đang nâng cấp hệ thống phần mềm tính tiền tại quầy (Highlands POS). Khi nhân viên thu ngân nhập dữ liệu order của khách hàng từ màn hình CLI, hệ thống cần tính toán chính xác tổng tiền của từng ly đồ uống dựa trên các tùy chọn size, topping, giảm giá thành viên và thuế VAT.

Tuy nhiên, trong các hệ thống tài chính thực tế, việc tính toán tỉ lệ phần trăm giảm giá (10%) hoặc thuế VAT (8%) nếu không được thiết kế kiểu dữ liệu cẩn thận sẽ dễ dẫn đến các lỗi làm tròn (ví dụ: `49500.00000000001` VNĐ thay vì `49500` VNĐ). Điều này khiến hóa đơn in ra thiếu chuyên nghiệp và có thể gây lệch sổ sách kế toán cuối ngày.

Dưới góc độ một kỹ sư phần mềm, bạn được giao nhiệm vụ nghiên cứu bài toán, đề xuất các phương án kỹ thuật xử lý dữ liệu tiền tệ, phân tích ưu/nhược điểm (Trade-off) của từng phương án, và lập trình giải pháp tối ưu nhất.

### **3. Quy tắc nghiệp vụ**
Hệ thống tính tiền POS cần tuân thủ các quy tắc nghiệp vụ sau:
1.  **Giá đồ uống gốc (Base Price):** Là đơn giá niêm yết dành cho Size S (nhập từ bàn phím, ví dụ: 45000 VNĐ).
2.  **Phụ thu Size (Size Upcharge):** 
    *   Size S: +0 VNĐ.
    *   Size M: +6.000 VNĐ so với Size S.
    *   Size L: +10.000 VNĐ so với Size S.
    *(Nhập số tiền phụ thu size trực tiếp từ CLI tùy theo lựa chọn của khách).*
3.  **Phụ thu Topping (Topping Fee):** Mỗi phần topping thêm có giá cố định **8.000 VNĐ** (nhập số lượng topping `topping_count` từ CLI).
4.  **Giảm giá Thành viên Vàng (Gold Membership Discount):** Giảm **10%** trên tổng tiền món ăn (bao gồm: Giá gốc + Phụ thu Size + Phụ thu Topping).
5.  **Thuế Giá trị gia tăng (VAT):** Thuế suất **8%** tính trên số tiền thanh toán thực tế sau khi đã trừ giảm giá thành viên.
6.  **Định dạng đầu ra:** Mọi khoản tiền xuất ra hóa đơn phải được làm tròn chính xác về số nguyên đơn vị VNĐ, trình bày dưới dạng dòng văn bản căn chỉnh lề rõ ràng.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off (Multi-Solution Proposal & Trade-off Report)**
*   Tự nghiên cứu và đề xuất **ít nhất 2 phương án kỹ thuật khác nhau** để giải quyết bài toán tính tiền tệ và xử lý làm tròn số trong Python (chỉ sử dụng các kiểu dữ liệu và toán tử cơ bản đã học).
*   Xây dựng bảng so sánh Trade-off giữa các phương án theo đúng 5 tiêu chí tiêu chuẩn:
    1.  Tốc độ xử lý (Speed / Execution Time).
    2.  Dung lượng bộ nhớ chiếm dụng (Memory Usage).
    3.  Khả năng bảo trì (Maintainability).
    4.  Độ dễ đọc của mã nguồn (Readability).
    5.  Kịch bản áp dụng phù hợp (Suitability / Precision Guard).

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Lưu đồ luồng (Justification & Flowchart)**
*   Giải thích ngắn gọn lý do chọn phương án tối ưu dựa trên bài toán tính tiền POS.
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) cho giải pháp được chọn. Sơ đồ Mermaid phải tuân thủ nghiêm ngặt quy chuẩn 5 dạng hình:
    *   Terminator (Bắt đầu/Kết thúc): `([Bắt đầu])` / `([Kết thúc])`
    *   Input/Output (Nhập/Xuất): `[/Nhập dữ liệu/]` / `[/In hóa đơn/]`
    *   Process (Xử lý/Tính toán): `["Tính toán tổng tiền"]`
    *   Decision (Điều kiện): `{"Kiểm tra..."}`
    *   Flowline (Dòng chảy): `-->`

#### **Phần 3: Triển khai Mã nguồn Python (CLI Implementation)**
*   Viết chương trình Python thu thập các thông số từ CLI:
    *   Tên món ăn/đồ uống (`drink_name`).
    *   Giá gốc món Size S (`base_price`).
    *   Số tiền phụ thu size (`size_upcharge`).
    *   Số lượng topping (`topping_count`).
*   Thực hiện các phép toán đại số để tính:
    *   Tổng tiền trước giảm giá (`subtotal`).
    *   Số tiền được giảm giá thành viên Vàng 10% (`discount_amount`).
    *   Số tiền sau giảm giá (`net_subtotal`).
    *   Số tiền thuế VAT 8% (`vat_amount`).
    *   Tổng tiền thanh toán cuối cùng (`final_total`).
*   In hóa đơn ra màn hình console theo định dạng văn bản chuẩn mực.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (Phần 1, Phần 2) và mã nguồn triển khai (Phần 3).
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex11`

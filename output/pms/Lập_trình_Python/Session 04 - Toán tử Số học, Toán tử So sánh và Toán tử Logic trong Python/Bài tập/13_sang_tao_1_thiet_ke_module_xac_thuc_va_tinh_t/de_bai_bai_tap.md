## <center>[Sáng tạo 1] Thiết kế Module Xác thực và Tính toán Hóa đơn POS Trà sữa</center>

### **1. Mục tiêu**
*   **Kiến thức:** Vận dụng sáng tạo các toán tử số học (`+`, `-`, `*`, `/`, `//`, `%`), toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`) và toán tử logic (`and`, `or`, `not`) để xây dựng module tính tiền và xác thực hóa đơn.
*   **Kỹ năng:** Tự thiết kế cấu trúc dữ liệu đầu vào/đầu ra (I/O Schema), phân tích các trường hợp biên (Edge Cases), vẽ sơ đồ luồng dữ liệu (Data Flow Diagram) chuẩn hóa bằng Mermaid và hiện thực mã nguồn Python không phụ thuộc vào câu lệnh điều khiển rẽ nhánh (`if/else`).
*   **Tư duy:** Rèn luyện tư duy lập trình chuyển đổi logic nghiệp vụ phức tạp thành các biểu thức đại số Boole và công thức toán học thuần túy.

---

### **2. Bối cảnh & Vấn đề**
Hệ thống Quản lý Bán hàng Quán Cà phê / Trà sữa (Highlands POS) đang thực hiện nâng cấp phân hệ tính tiền tự động tại quầy checkout. Thu ngân cần nhập nhanh các thông tin món uống, tùy chọn size, số lượng topping và hạng thành viên của khách để máy POS tự động xác minh tính hợp lệ và tính toán hóa đơn.

Do hệ thống xử lý ở tầng lõi siêu nhẹ (Core Engine), phân hệ này yêu cầu dữ liệu phải được xử lý tức thì thông qua biểu thức toán học và logic trực tiếp, hạn chế tối đa việc sử dụng các cấu trúc rẽ nhánh phức tạp. Bạn được giao nhiệm vụ tự thiết kế kịch bản dữ liệu, xây dựng tài liệu kỹ thuật và hiện thực hóa module tính toán hóa đơn POS này.

<p align="center">
  <img src="../images/bai_13_sang_tao_1_thiet_ke_module_xac_thuc_va_tinh_t_diagram.png" alt="Sơ đồ luồng nghiệp vụ" width="80%">
</p>

---

### **3. Quy tắc nghiệp vụ**
Hệ thống Highlands POS vận hành dựa trên các quy tắc nghiệp vụ cốt lõi sau:
1.  **Phụ thu Size đồ uống:** 
    *   Size S (mặc định): Phụ thu `0` VNĐ.
    *   Size M: Phụ thu `6.000` VNĐ.
    *   Size L: Phụ thu `10.000` VNĐ.
2.  **Phụ thu Topping:** Mỗi phần topping đi kèm tính phụ thu đồng giá `8.000` VNĐ.
3.  **Chiết khấu Thẻ thành viên:** 
    *   Thành viên Vàng (Gold Member) được giảm `10%` trên tổng chi phí đơn hàng (gồm giá gốc + phụ thu size + phụ thu topping).
    *   **Điều kiện áp dụng ưu đãi:** Đơn hàng phải có tổng giá trị trước giảm đạt tối thiểu `100.000` VNĐ **VÀ** khách hàng có cờ xác nhận là thành viên Vàng.
4.  **Điều kiện xác thực Đơn hàng hợp lệ (`is_valid_order`):**
    *   Số lượng món mua phải từ `1` đến `50` sản phẩm.
    *   Số lượng topping nhập vào không được là số âm (`>= 0`).
    *   Giá gốc đơn hàng phải lớn hơn `0` VNĐ.

[REQUIREMENT] RÀNG BUỘC PHẠM VI KIẾN THỨC:
Học viên CHỈ ĐƯỢC PHÉP sử dụng các kiến thức đã học tính đến Session 04: Biến số, kiểu dữ liệu cơ bản (`int`, `float`, `str`, `bool`), `input()`, `print()`, ép kiểu dữ liệu, các toán tử số học, so sánh, logic và thứ tự ưu tiên toán tử.
TUYỆT ĐỐI CẤM SỬ DỤNG: Câu lệnh rẽ nhánh (`if/else/elif`), vòng lặp (`for/while`), cấu trúc dữ liệu tập hợp (`list`, `dict`, `set`, `tuple`), hàm tự định nghĩa (`def`), hoặc lớp (`class`).

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Kỹ sư Phần mềm phụ trách phân hệ POS, hoàn thành 4 phần báo cáo và mã nguồn sau:

#### **Phần 1: Tự thiết kế I/O Schema (Schema Đầu vào / Đầu ra)**
*   Tự xác định danh sách các biến dữ liệu đầu vào thu thập từ người dùng (ví dụ: đơn giá món, số lượng, cờ chọn size, số lượng topping, trạng thái thành viên).
*   Tự xác định các biến kết quả tính toán đầu ra cần in ra màn hình POS.

#### **Phần 2: Tự phát hiện bẫy dữ liệu (Edge Cases)**
*   Phân tích và nêu rõ ít nhất **03 trường hợp biên** hoặc bẫy dữ liệu nghiệp vụ (ví dụ: nhập số lượng topping âm, nhập số lượng món quá giới hạn cho phép, đơn hàng không đủ điều kiện giảm giá dù là thành viên Vàng).
*   Đề xuất công thức logic/số học để phát hiện các bẫy dữ liệu này mà không dùng `if/else`.

#### **Phần 3: Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram)**
*   Sử dụng cú pháp Mermaid để vẽ sơ đồ luồng dữ liệu minh họa toàn bộ quá trình nhập liệu, kiểm tra hợp lệ, tính toán phụ thu, chiết khấu và xuất hóa đơn.
*   **Quy chuẩn bắt buộc về dạng hình Mermaid:**
    1.  `([Start / End])`: Hình bầu dục (Stadium) cho điểm Bắt đầu / Kết thúc.
    2.  `[/Input / Output/]`: Hình hình bình hành (Parallelogram) CHỈ dùng cho nhập/xuất dữ liệu.
    3.  `["Process / Calculation"]`: Hình chữ nhật (Rectangle) dùng cho các bước tính toán/xử lý.
    4.  `Kiểm tra điều kiện?`: Hình thoi (Diamond) dùng cho câu hỏi kiểm tra logic điều kiện.

#### **Phần 4: Triển khai mã nguồn Python chuẩn mực**
*   Viết chương trình Python hoàn chỉnh thực thi toàn bộ logic đã thiết kế.
*   Yêu cầu mã nguồn tuân thủ Clean Code: Đặt tên biến hoàn toàn bằng tiếng Anh theo chuẩn `snake_case`, chú thích mã nguồn bằng tiếng Việt có dấu.
*   Thực hiện ép kiểu chính xác dữ liệu từ `input()`.
*   Sử dụng tính chất của kiểu dữ liệu `bool` trong Python (`True` tương đương `1`, `False` tương đương `0` khi tham gia phép toán số học) để tính toán tiền phụ thu và tiền chiết khấu mà không dùng `if/else`.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, sơ đồ Mermaid) và mã nguồn triển khai trong file Python.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex13`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session04_Ex13`
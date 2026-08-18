## <center>[Sáng tạo 1] Thiết kế mô hình tính hóa đơn POS tích hợp ưu đãi và VAT linh hoạt</center>

### **1. Mục tiêu**
*   Vận dụng sáng tạo kiến thức về khai báo biến, nhập xuất dữ liệu màn hình dòng lệnh (`input()`, `print()`) và chuyển đổi kiểu dữ liệu (`int`, `float`, `str`) trong Python.
*   Tự phân tích bối cảnh nghiệp vụ thực tế tại quầy thanh toán Highlands POS để thiết kế cấu trúc dữ liệu đầu vào/đầu ra (I/O Schema).
*   Chủ động phát hiện các kịch bản dữ liệu biên (Edge Cases) tiềm ẩn nguy cơ gây lỗi ứng dụng hoặc sai lệch số tiền.
*   Xây dựng sơ đồ luồng dữ liệu (Data Flow Diagram) chuẩn hóa quy trình xử lý hóa đơn POS.
*   Triển khai mã nguồn Python hoàn chỉnh, tổ chức mã nguồn theo chuẩn Clean Code với danh xưng biến bằng tiếng Anh và chú thích logic bằng tiếng Việt.

### **2. Bối cảnh & Vấn đề**
Tại chuỗi cửa hàng cà phê Highlands POS, quy trình tính tiền tại quầy thu ngân đang thực hiện nâng cấp phân hệ xử lý hóa đơn cho khách hàng mua trực tiếp. Hệ thống cần tiếp nhận thông tin tên thức uống, giá niêm yết (Size S), phụ thu nâng size (Size M/L), số lượng phần topping gọi thêm, phần trăm giảm giá theo hạng thành viên (như hạng Vàng giảm 10%), và tỷ lệ thuế giá trị gia tăng VAT áp dụng cho hóa đơn.

Nhân viên vận hành phản ánh rằng ứng dụng cũ thường xuyên xảy ra lỗi sai lệch tổng tiền do nhân viên nhập giá trị dạng chuỗi (String) mà hệ thống lại tính toán ghép chuỗi thay vì cộng số học, hoặc gây dừng đột ngột chương trình do chưa có cơ chế kiểm tra kiểu dữ liệu trước khi ép kiểu. Ngoài ra, định dạng hiển thị phiếu thu tiền chưa chuyên nghiệp, thiếu minh bạch các khoản trừ ưu đãi và thuế.

Ban dự án yêu cầu bạn - với vai trò Kỹ sư Phần mềm - chủ động thiết kế mô hình dữ liệu cho hóa đơn POS, tự xác định các vùng bẫy dữ liệu (Edge Cases), vẽ sơ đồ luồng dữ liệu và viết chương trình Python CLI thực hiện tính toán và in hóa đơn thanh toán hoàn chỉnh.### **3. Quy tắc nghiệp vụ**
Hệ thống tính tiền POS tuân thủ các quy tắc nghiệp vụ thực tế sau:
*   **Đơn giá sản phẩm**: Bằng đơn giá gốc (Size S) cộng với phí nâng size (Size M tăng 6.000 VNĐ, Size L tăng 10.000 VNĐ).
*   **Phụ thu Topping**: Mỗi suất topping gọi thêm tính đồng giá 8.000 VNĐ.
*   **Tổng tiền hàng trước giảm giá**: `(Đơn giá sản phẩm sau nâng size + Phụ thu topping) * Số lượng món`.
*   **Chiết khấu thành viên**: Tính theo tỷ lệ % giảm giá trên tổng tiền hàng (ví dụ: Thành viên Vàng được giảm 10% tương ứng 0.10).
*   **Thuế VAT**: Tính theo tỷ lệ % thuế VAT (ví dụ: 8% hoặc 10%) trên tổng số tiền sau khi đã trừ chiết khấu thành viên.
*   **Tổng thanh toán cuối cùng**: `(Tổng tiền hàng - Tiền chiết khấu) * (1 + Tỷ lệ VAT)`.

[REQUIREMENT] Bài tập này đóng vai trò là một module độc lập thuộc cấp độ Sáng tạo 1. Học viên được trao toàn quyền tự đề xuất cấu trúc tham số và kịch bản hiển thị, không sử dụng lại mã mẫu hay bộ dữ liệu cố định.

### **4. Yêu cầu bài toán**
Học viên cần trình bày bài nộp gồm 4 phần chi tiết:

#### **Phần 1: Tự thiết kế I/O Schema (Self-Designed I/O Schema)**
Lập bảng mô tả danh sách các biến dữ liệu đầu vào và đầu ra. Định rõ tên biến (bằng tiếng Anh), kiểu dữ liệu (Data Type) và mục đích nghiệp vụ tương ứng.

#### **Phần 2: Chủ động phát hiện bẫy dữ liệu (Self-Discovered Edge Cases)**
Phân tích và liệt kê ít nhất 3 kịch bản bẫy dữ liệu có thể xảy ra khi nhân viên thu ngân nhập liệu từ bàn phím (ví dụ: nhập chữ vào trường số tiền, nhập số lượng âm, nhập phần trăm giảm giá vượt quá 100%...). Đề xuất hướng xử lý hoặc câu thông báo tương ứng cho từng trường hợp.

#### **Phần 3: Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram)**
Vẽ sơ đồ luồng dữ liệu dạng Mermaid Flowchart mô tả chi tiết từ bước nhập liệu CLI -> Ép kiểu dữ liệu -> Tính toán tiền hàng, ưu đãi, thuế -> In phiếu hóa đơn ra màn hình.
[QUY CHUẨN MERMAID]:
*   Oval `([Bắt đầu / Kết thúc])` cho điểm khởi đầu và kết thúc quy trình.
*   Parallelogram `[/Nhập dữ liệu / Xuất kết quả/]` CHỈ dùng cho thao tác Input / Output dữ liệu.
*   Rectangle `["Thực hiện tính toán / Xử lý logic"]` dùng cho các bước xử lý biến và phép toán.
*   Diamond `Kiểm tra điều kiện?` dùng cho các nhánh quyết định kiểm tra.

#### **Phần 4: Triển khai mã nguồn Python (Implementation)**
Viết chương trình Python CLI hoàn chỉnh trong tập tin `main.py` đáp ứng mô hình I/O đã thiết kế, thực hiện đầy đủ việc nhập dữ liệu từ bàn phím, chuyển đổi kiểu dữ liệu an toàn, tính toán chính xác và in ra hóa đơn bán hàng POS được định dạng rõ ràng, chuyên nghiệp.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (Phần 1, Phần 2, Phần 3) và mã nguồn triển khai (Phần 4).
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex13`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex13`
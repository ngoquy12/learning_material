# <center>[Vận dụng nâng cao 1] Điều chỉnh và Cập nhật Nhật ký Chuyến đi GrabRide</center>

### **1. Mục tiêu**
*   **Vận dụng thao tác cập nhật và xóa phần tử:** Thực hành thành thạo kỹ thuật truy cập chỉ số (index), cập nhật trực tiếp giá trị (`list[index] = new_value`) và xóa phần tử dữ liệu không hợp lệ (`del list[index]`) trên danh sách dữ liệu động.
*   **Kiểm soát quy mô danh sách:** Sử dụng hàm `len()` để theo dõi biến đổi về độ dài danh sách sau khi điều chỉnh dữ liệu RAM.
*   **Phân tích và thiết kế hệ thống:** Tự phân tích luồng dữ liệu, xác định kiểu dữ liệu Input/Output và xử lý các tình huống biên (Edge Cases) trong bài toán quản lý cước phí chuyến đi GrabRide mà không sử dụng các phương thức cấm như `append()`, `pop()`, hàm tự định nghĩa (`def`), Dictionary hay OOP.

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Đặt xe công nghệ GrabRide, trung tâm điều hành ghi nhận nhật ký quãng đường di chuyển (tính bằng km) của từng chuyến đi do tài xế thực hiện trong ca làm việc dưới dạng một danh sách các số thực.Trong suốt ca làm việc, dữ liệu thực tế phát sinh hai tình huống nghiệp vụ cần can thiệp xử lý:
1.  **Cập nhật khoảng cách chuyến đi:** Do sự cố định vị GPS ban đầu ghi nhận sai hoặc khách hàng thay đổi lộ trình giữa chừng, khoảng cách của chuyến đi tại chỉ số được chỉ định cần được cập nhật lại chính xác.
2.  **Xóa chuyến đi bị hủy hoặc lỗi dữ liệu:** Chuyến đi có quãng đường không hợp lệ (ví dụ bằng 0 km hoặc âm do lỗi ứng dụng tài xế) cần phải được xóa bỏ hoàn toàn khỏi danh sách bằng câu lệnh xóa theo chỉ số.

Sau khi cập nhật và xóa dữ liệu lỗi, hệ thống phải tự động tính toán tổng số chuyến đi hợp lệ còn lại, tổng quãng đường tài xế đã di chuyển và tổng doanh thu thu được trong ca dựa trên biểu phí chuẩn của hệ thống GrabRide.

### **3. Quy tắc nghiệp vụ**
Hệ thống áp dụng các quy tắc tính cước và xử lý dữ liệu sau:

1.  **Dữ liệu đầu vào ban đầu (RAM):**
    *   Danh sách quãng đường các chuyến đi trong ca: `khoang_cach_chuyen: list[float] = [2.5, 1.0, 8.0, 0.0, 15.0, 4.2]`
    *   Trạng thái khung giờ cao điểm / thời tiết xấu: `is_gio_cao_diem: bool = True` (Nếu `True`, hệ số phụ phí là `1.2`; nếu `False`, hệ số phụ phí là `1.0`).

2.  **Quy tắc tính giá cước cho từng chuyến đi:**
    *   **2 km đầu tiên:** Tính giá cố định 12.000 VNĐ.
    *   **Từ km thứ 3 trở đi (quãng đường > 2.0 km):** Phần quãng đường vượt quá 2 km tính giá 4.500 VNĐ/km.
        *   *Công thức cước gốc:* 
            *   Nếu `khoang_cach <= 2.0`: `cuoc_goc = 12000.0`
            *   Nếu `khoang_cach > 2.0`: `cuoc_goc = 12000.0 + (khoang_cach - 2.0) * 4500.0`
    *   **Áp dụng phụ phí:** `cuoc_thuc_te = cuoc_goc * he_so_phu_phi`

3.  **Quy tắc điều chỉnh và xử lý danh sách:**
    *   **Thao tác 1 (Cập nhật):** Chuyến đi tại chỉ số `1` ban đầu ghi nhận `1.0` km cần được cập nhật thành `3.5` km.
    *   **Thao tác 2 (Xóa phần tử):** Chuyến đi tại chỉ số `3` có khoảng cách `0.0` km (chuyến bị hủy/lỗi) phải được xóa khỏi danh sách bằng lệnh `del`.
    *   *Lưu ý nghiệp vụ:* Việc xóa phần tử tại một chỉ số sẽ làm thay đổi độ dài danh sách và làm dịch chuyển chỉ số của tất cả các phần tử đứng sau nó.

4.  **Ràng buộc kỹ thuật NGIÊM NGẶT:**
    *   TUYỆT ĐỐI CẤM sử dụng các hàm tự định nghĩa (`def`), lớp OOP (`class`), từ điển (`dict`), `set`, `tuple`.
    *   TUYỆT ĐỐI CẤM sử dụng các phương thức biến đổi danh sách nâng cao: `append()`, `pop()`, `insert()`, `remove()`, `clear()`, `sort()`.
    *   Chỉ được phép dùng thao tác gán chỉ số `list[index] = new_value`, câu lệnh `del list[index]`, hàm `len()`, các vòng lặp (`for`, `while`) và câu lệnh điều kiện (`if`, `elif`, `else`).

### **4. Yêu cầu bài toán**

Học viên thực hiện bài tập theo 2 phần bắt buộc:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Solution Analysis & Design Report)**
*   **Phân tích I/O:** Xác định rõ các biến đầu vào, kiểu dữ liệu, phạm vi chỉ số cần thao tác và các chỉ số đầu ra cần tính toán (tổng quãng đường, tổng doanh thu, số chuyến còn lại).
*   **Đề xuất giải pháp & Thiết kế luồng xử lý:** 
    *   Trình bày chiến lược xử lý tính toàn vẹn dữ liệu khi thực hiện cập nhật trước và xóa sau.
    *   Vẽ sơ đồ luồng (Mermaid Flowchart) hoặc viết giả mã (Pseudocode) mô tả toàn bộ quá trình: khởi tạo danh sách -> kiểm tra biên & cập nhật -> kiểm tra biên & xóa phần tử -> duyệt danh sách tính toán cước phí và tổng hợp doanh thu.
    *   *Quy chuẩn sơ đồ Mermaid:* Bắt buộc dùng đúng 5 hình khối chuẩn (Oval cho Bắt đầu/Kết thúc, Hình bình hành cho Input/Output, Hình thoi cho Điều kiện, Hình chữ nhật cho Tiến trình xử lý, Mũi tên cho Luồng thực thi).

#### **Phần 2: Mã nguồn Triển khai & Chặn sai sót biên (Implementation & Edge Guards)**
*   Viết mã nguồn Python 3.12 hoàn chỉnh đáp ứng các yêu cầu nghiệp vụ.
*   Thực hiện đầy đủ lỗi thường gặp và kiểm định biên:
    *   Kiểm tra chỉ số cập nhật/xóa có nằm trong phạm vi hợp lệ của danh sách (`0 <= index < len(danh_sach)`) trước khi thực hiện thao tác để tránh lỗi `IndexError`.
    *   Kiểm tra giá trị khoảng cách cập nhật phải là số dương (`> 0`).
*   In ra màn hình kết quả theo từng bước:
    *   Danh sách chuyến đi ban đầu.
    *   Thông báo xác nhận sau khi cập nhật thành công.
    *   Thông báo xác nhận sau khi xóa phần tử thành công.
    *   Danh sách chuyến đi sau khi hoàn tất xử lý.
    *   Tổng số chuyến đi còn lại, tổng quãng đường di chuyển (km) và tổng doanh thu toàn ca (VNĐ).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo thiết kế giải pháp và mã nguồn triển khai trong cùng tệp bài làm.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex7`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session10_Ex7`

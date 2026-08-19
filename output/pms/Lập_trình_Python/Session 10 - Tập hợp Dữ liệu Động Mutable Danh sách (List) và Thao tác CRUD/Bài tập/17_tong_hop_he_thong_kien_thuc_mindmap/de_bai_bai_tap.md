# <center>[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) - Session 10</center>

### **1. Mục tiêu**
- Hệ thống hóa toàn bộ kiến thức cốt lõi và các lỗi thường gặp nghiệp vụ về Tập hợp Dữ liệu Động Mutable: Danh sách (List) và thao tác Cập nhật / Xóa phần tử (Update & Delete) trong Session 10.
- Trực quan hóa cấu trúc dữ liệu List trong Python 3.12 và luồng thực thi các thao tác biến đổi dữ liệu thông qua Sơ đồ Tư duy (Mindmap).
- Vận dụng kiến thức vào bài toán quản lý danh sách chuyến xe, cước phí và tài xế trong hệ thống đặt xe công nghệ **GRAB_RIDE**.
- Rèn luyện kỹ năng phân tầng logic, quản lý bộ nhớ động và kết nối tri thức hệ thống một cách khoa học.

### **2. Bối cảnh & Vấn đề**
Bạn đang đóng vai trò là một **Software Engineer** thuộc đội ngũ phát triển Core System của ứng dụng **GRAB_RIDE**. Hệ thống đang gặp bài toán quản lý danh sách cước phí chuyến xe động trong ngày của tài xế (`cuoc_phi_chuyen_xe`), xử lý các tình huống cập nhật lại giá cước khi có khuyến mãi/phụ phí, xóa bỏ các chuyến xe bị hủy hoặc gian lận, và thống kê tổng số chuyến xe hoàn tất.

Để đào tạo cho các kỹ sư mới (Onboarding), bạn được giao nhiệm vụ thiết kế **Sơ đồ tư duy (Mindmap) Kiến thức Kỹ thuật** tổng hợp toàn bộ tri thức về `List Mutable`, thao tác `Update` (gán lại chỉ số), thao tác `Delete` (sử dụng câu lệnh `del`), và truy xuất độ dài danh sách (`len()`).

### **3. Quy tắc nghiệp vụ**
Sơ đồ tư duy BẮT BUỘC bao phủ và kết nối logic các từ khóa trọng tâm và nghiệp vụ **GRAB_RIDE** sau:

1. **Khái niệm List Mutable (Đặc tính biến đổi):**
   - Bộ nhớ động của List trong Python: Cho phép chỉnh sửa trực tiếp giá trị các phần tử mà không làm thay đổi định danh (ID/địa chỉ) của đối tượng danh sách trong bộ nhớ.
   - Cú pháp chuẩn hóa với Type Hints: `cuoc_phi_chuyen_xe: list[float] = [25.0, 50.0, 120.0, 35.0]` (đơn vị: 1,000 VNĐ).

2. **Thao tác Cập nhật (Update Element by Index):**
   - Cú pháp gán theo chỉ số: `danh_sach[index] = gia_tri_moi`.
   - Nghiệp vụ GRAB_RIDE: Cập nhật lại cước phí chuyến xe tại vị trí `index` khi tính thêm phụ phí thời tiết xấu hoặc áp dụng mã giảm giá RideCoupon (Ví dụ: `cuoc_phi_chuyen_xe[2] = 145.0`).
   - lỗi thường gặp runtime: `IndexError: list assignment index out of range` khi truy xuất index không tồn tại trong danh sách.

3. **Thao tác Xóa (Delete Element by Index):**
   - Cú pháp xóa bằng câu lệnh `del`: `del danh_sach[index]`.
   - Cơ chế dịch chuyển chỉ số (Index Shifting): Khi xóa phần tử tại vị trí `i`, toàn bộ các phần tử phía sau sẽ tự động dịch chuyển sang trái (giảm index đi 1).
   - Nghiệp vụ GRAB_RIDE: Xóa chuyến xe bị hủy khỏi danh sách chờ thanh toán (Ví dụ: `del cuoc_phi_chuyen_xe[1]`).

4. **Hàm truy xuất độ dài danh sách (`len()`):**
   - Cú pháp: `len(danh_sach)`.
   - Trả về số lượng phần tử hiện tại trong List (Trả về kiểu `int`).
   - Nghiệp vụ GRAB_RIDE: Đếm tổng số chuyến xe thực tế hợp lệ còn lại sau khi cập nhật và xóa (`tong_so_chuyen: int = len(cuoc_phi_chuyen_xe)`).

5. **Chuẩn mã nguồn & Chất lượng Code (PEP 8 & Type Hints):**
   - Đặt tên biến snake_case rõ ràng (`danh_sach_cuoc_phi`, `so_luong_chuyen_xe`).
   - Khai báo Type Hint rõ ràng cho biến (`list[float]`, `list[int]`).
   - Chú thích mã nguồn (Comments) giải thích rõ lý do cập nhật/xóa phần tử theo nghiệp vụ.

### **4. Yêu cầu bài toán (Sản phẩm nộp)**
1. **File ảnh Sơ đồ tư duy** (`.png` hoặc `.jpg`): Hình ảnh sơ đồ tư duy trực quan, bố cục rõ ràng, phối màu chuẩn chuyên nghiệp.
2. **File thiết kế gốc** (`.xmind`, `.pdf` hoặc định dạng của công cụ vẽ sơ đồ tư duy như EdrawMind, Draw.io).
3. **Bản tóm tắt giải trình Markdown (`summary.md`)**: Giải thích chi tiết các nhánh liên kết chính trong sơ đồ tư duy và kèm theo kịch bản minh họa Python 3.12 thực thi quy trình CRUD (Update/Delete/Len) cho hệ thống **GRAB_RIDE**.

### **5. Yêu cầu nộp bài**
Học viên nộp bài theo quy chuẩn GitHub:
* Đẩy toàn bộ mã nguồn, file thiết kế và sơ đồ lên GitHub Repository theo cấu trúc tên thư mục/repository: `[Tên Lớp]_[Môn Học]_Session10_Mindmap`.
  Ví dụ: `HNKS25CNTT1_Core_Session10_Mindmap`

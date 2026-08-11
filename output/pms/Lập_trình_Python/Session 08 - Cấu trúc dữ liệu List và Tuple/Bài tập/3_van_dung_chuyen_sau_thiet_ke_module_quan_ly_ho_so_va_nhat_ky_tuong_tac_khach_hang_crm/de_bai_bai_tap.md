## <center>[Vận dụng chuyên sâu] Thiết kế Module Quản lý Hồ sơ và Nhật ký Tương tác Khách hàng CRM</center>

### **1. Mục tiêu**
- Áp dụng kỹ thuật truy cập và cập nhật trực tiếp phần tử trong List qua chỉ số (Index).
- Thực hành kỹ thuật cắt lát danh sách (List Slicing) để trích xuất phân đoạn nhật ký tương tác CRM.
- Khai thác tính bất biến (Immutability) của Tuple để bảo vệ dữ liệu tọa độ địa lý cố định của doanh nghiệp khách hàng.
- Vận dụng kỹ thuật Tuple Unpacking và Hoán đổi biến (Variable Swap) trực tiếp không dùng biến trung gian.
- Xây dựng tư duy thiết kế giải thuật và xử lý ngoại lệ dữ liệu (`ValueError`, `IndexError`) theo quy chuẩn PEP 8 và Python 3.12.

### **2. Bối cảnh & Vấn đề**
Hệ thống CRM của một tập đoàn cung cấp giải pháp doanh nghiệp quản lý thông tin khách hàng VIP bao gồm hai khối dữ liệu chính:
1. Khối dữ liệu vị trí cố định (tọa độ GPS trụ sở khách hàng): Lưu giữ dưới dạng Tuple để đảm bảo tính bất biến, chống ghi đè trái phép từ các luồng xử lý bất đồng bộ.
2. Khối nhật ký mã tương tác gần nhất (Touchpoint Interaction IDs): Lưu trữ dưới dạng List có thứ tự để ghi nhận chuỗi sự kiện chăm sóc khách hàng.

Trong quá trình vận hành, hệ thống phát sinh các nhu cầu xử lý:
- Khi hoán đổi chuyên viên quản lý tài khoản (Account Manager), hệ thống cần tráo đổi vị trí của hai chuyên viên phụ trách.
- Khi tọa độ ghi nhận bị sai lệch thứ tự (Latitude và Longitude bị đảo), hệ thống phải giải nén Tuple, hoán đổi và đóng gói lại Tuple mới.
- Khi mã tương tác đầu tiên bị ghi nhận lỗi, hệ thống phải sửa trực tiếp giá trị tại vị trí Index 0 trong List nhật ký.
- Bộ phận phân tích CRM cần trích xuất nhanh phân đoạn tương tác trung gian bằng kỹ thuật Slicing để lập báo cáo đánh giá.



### **3. Quy tắc nghiệp vụ**
1. **Bảo toàn dữ liệu bất biến (Tuple)**:
   - Tọa độ địa lý của trụ sở khách hàng được lưu dưới dạng Tuple `(latitude, longitude)`. Cấm thay đổi trực tiếp phần tử của Tuple.
   - Khi hoán đổi vai trò giữa 2 chuyên viên tư vấn `(primary_agent, secondary_agent)`, phải dùng kỹ thuật Swap trực tiếp trong Python (không dùng biến tạm).
   - Khi chuẩn hóa tọa độ mới, phải giải nén Tuple (Unpacking), thực hiện hoán đổi vị trí Latitude và Longitude, sau đó tạo ra Tuple mới.
2. **Thao tác trên Nhật ký Tương tác (List)**:
   - Danh sách mã tương tác CRM gồm các mã định dạng số nguyên (tối thiểu 4 phần tử).
   - Cập nhật trực tiếp mã lỗi ở đầu danh sách (Index 0) bằng một mã xử lý ưu tiên mới (`new_urgent_code`).
   - Trích xuất phân đoạn nhật ký ở giữa bằng kỹ thuật Slicing từ chỉ số 1 đến 3 (không bao gồm vị trí 3).
3. **Ràng buộc hạ tầng & Bẫy lỗi**:
   - Tuyệt đối KHÔNG sử dụng vòng lặp (`for`, `while`) và KHÔNG dùng các phương thức thêm/xóa của List (`append`, `insert`, `remove`, `pop`, `del`, `clear`).
   - Phải kiểm tra giá trị đầu vào: Tọa độ Vĩ độ (Latitude) phải nằm trong đoạn `[-90.0, 90.0]`, Kinh độ (Longitude) phải nằm trong đoạn `[-180.0, 180.0]`. Nếu vi phạm, kích hoạt ngoại lệ `ValueError`.
   - Nếu danh sách nhật ký tương tác truyền vào có ít hơn 4 phần tử, kích hoạt ngoại lệ `IndexError`.

### **4. Yêu cầu bài toán**
Học viên thực hiện bài nộp gồm 2 phần độc lập:

**Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Bắt buộc)**
- Trình bày Schema dữ liệu đầu vào (Input) và đầu ra (Output) cho từng chức năng nghiệp vụ.
- Viết giả mã (Pseudocode) hoặc vẽ sơ đồ luồng dữ liệu thể hiện các bước Unpacking, Variable Swap, Index Mutation và List Slicing.

**Phần 2: Triển khai Mã nguồn Python 3.12**
Viết mã nguồn đáp ứng đầy đủ các hàm sau (sử dụng Type Hints chuẩn PEP 8):
- `process_crm_location(location: tuple[float, float]) -> tuple[float, float]`: Nhận vào Tuple tọa độ `(latitude, longitude)`, kiểm tra tính hợp lệ về mặt địa lý. Nếu hợp lệ, thực hiện hoán đổi vị trí bằng kỹ thuật Swap và trả về Tuple tọa độ mới.
- `swap_crm_agents(agent_a: str, agent_b: str) -> tuple[str, str]`: Hoán đổi hai chuyên viên tư vấn bằng kỹ thuật Swap trực tiếp và trả về Tuple kết quả `(agent_b, agent_a)`.
- `update_and_slice_logs(logs: list[int], new_urgent_code: int) -> tuple[list[int], list[int]]`: Kiểm tra độ dài danh sách nhật ký. Thay thế giá trị tại Index 0 bằng `new_urgent_code`, sau đó trích xuất phân đoạn Slicing `[1:3]`. Trả về một Tuple chứa `(danh_sách_đã_sửa, phân_đoạn_slicing)`.

*Dữ liệu mẫu kiểm thử (Payload Example):*
```text
Input Tọa độ ban đầu: (10.76262, 106.66017)
Input Chuyên viên: agent_a = "Nguyen Van A", agent_b = "Tran Thi B"
Input Nhật ký CRM ban đầu: [5001, 5002, 5003, 5004]
Mã ưu tiên mới: 9999

Kỳ vọng Output:
- Tọa độ sau khi hoán đổi: (106.66017, 10.76262)
- Chuyên viên sau hoán đổi: ("Tran Thi B", "Nguyen Van A")
- Nhật ký CRM sau khi sửa Index 0: [9999, 5002, 5003, 5004]
- Phân đoạn Nhật ký Cắt lát [1:3]: [5002, 5003]
```

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex03`.
    Ví dụ: `HNKS25CNTT1_Core_Session08_Ex03`
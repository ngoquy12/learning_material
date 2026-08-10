### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Quản lý Khách hàng và Lịch sử Tương tác CRM với Pytest — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo đầy đủ các tệp mã nguồn `crm_service.py` và `test_crm_service.py`, chạy thành công lệnh `pytest` từ Terminal mà không gặp lỗi ImportError.
*   **[10 điểm] Xây dựng Cấu trúc dữ liệu & Custom Exceptions:** Khai báo đúng 3 lớp Custom Exception kế thừa từ `Exception` (`DuplicateCustomerError`, `CustomerNotFoundError`, `InvalidCustomerDataError`) và cấu trúc lưu trữ RAM của lớp `CRMManager`.

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Chức năng Quản lý Khách hàng:** Hiện thực phương thức `add_customer` và `get_customer_details` đúng theo đặc tả nghiệp vụ, lưu trữ dữ liệu chính xác trên RAM.
*   **[20 điểm] Chức năng Ghi nhận Tương tác & Xếp hạng:** Hiện thực phương thức `record_interaction` và `get_customer_tier`, tính toán chính xác điểm `lead_score` kèm kỹ thuật giới hạn biên (clamping 0-100) và trả về đúng hạng `"Cold"`, `"Warm"`, `"Hot"`.

#### **3. Kiểm chuẩn logic & Bẫy dữ liệu với Pytest — 20 điểm**
*   **[10 điểm] Kiểm chuẩn và Raise Ngoại lệ chủ động:** Kích hoạt chính xác các ngoại lệ `DuplicateCustomerError`, `CustomerNotFoundError`, `InvalidCustomerDataError`, `ValueError` khi dữ liệu đầu vào không hợp lệ hoặc không tìm thấy bản ghi.
*   **[10 điểm] Bộ test cases Pytest hoàn chỉnh:** Viết đầy đủ ít nhất 6 test cases sử dụng `pytest.raises` và các câu lệnh `assert` để kiểm định thành công tất cả các kịch bản biên và ngoại lệ.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Chuẩn hóa mã nguồn PEP 8 & Type Hints:** Sử dụng Type Hints chuẩn Python 3.10+ (`int | str`, `dict`), đặt tên biến/hàm theo chuẩn `snake_case`, chú thích mã nguồn bằng tiếng Việt có dấu rõ ràng.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng định dạng tên thư mục `[Tên Lớp]_[Môn Học]_Session14_Ex06`, có commit history rõ ràng.
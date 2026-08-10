### **Tiêu chí chấm điểm (AI)**
**[Mini project] Xây dựng ứng dụng Console quản lý danh sách kho hàng bán lẻ — Tổng điểm: 100 điểm**

---

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
* **Chương trình khởi chạy liên tục (10 điểm):**
  * **10 điểm:** Khởi tạo vòng lặp Menu chính (`while True`) chạy liên tục, hiển thị rõ ràng danh sách lựa chọn từ 1 đến 7 và chỉ dừng khi người dùng chọn tùy chọn Thoát.
  * **5 điểm:** Menu chạy được nhưng bị ngắt luồng bất ngờ khi chọn sai mục hoặc chưa hiển thị đầy đủ tùy chọn.
  * **0 điểm:** Chương trình bị lỗi ngay khi vừa khởi chạy hoặc không có vòng lặp duy trì.
* **Cấu trúc lưu trữ dữ liệu hợp lệ (10 điểm):**
  * **10 điểm:** Khởi tạo danh sách lưu trữ chính (`inventory_list = []`) đúng chuẩn danh sách đa chiều (List of Lists), lưu trữ đầy đủ 5 trường dữ liệu (`item_id`, `item_name`, `category`, `quantity`, `unit_price`). Tuân thủ nghiêm ngặt cấm dùng Dictionary/Class/Set.
  * **5 điểm:** Dùng danh sách nhưng thiếu trường dữ liệu hoặc cấu trúc không đồng nhất giữa các phần tử.
  * **0 điểm:** Vi phạm quy chuẩn cấm (sử dụng `dict`, `set`, `class` hoặc thư viện ngoài).

---

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
* **Chức năng Hiển thị & Thêm mới (10 điểm):**
  * **10 điểm:** Hiển thị danh sách đẹp mắt dạng bảng; Thêm mới sản phẩm hoạt động chính xác, dữ liệu được chèn đúng vào `inventory_list`.
  * **5 điểm:** Hiển thị hoặc Thêm mới bị lỗi định dạng nhẹ nhưng vẫn thêm được dữ liệu.
  * **0 điểm:** Không hiển thị được danh sách hoặc không thêm được sản phẩm vào danh sách.
* **Chức năng Cập nhật & Xóa sản phẩm (10 điểm):**
  * **10 điểm:** Tìm đúng sản phẩm theo `item_id` để cập nhật số lượng/giá bán; Xóa sản phẩm chuẩn xác có bước xác nhận (Y/N).
  * **5 điểm:** Cập nhật hoặc xóa bị nhầm vị trí chỉ số (index error) hoặc thiếu bước xác nhận khi xóa.
  * **0 điểm:** Cập nhật và xóa không hoạt động hoặc làm hỏng cấu trúc danh sách.
* **Chức năng Tìm kiếm & Thống kê (10 điểm):**
  * **10 điểm:** Tìm kiếm sản phẩm theo tên không phân biệt hoa/thường (`.lower()`); Thống kê chính xác tổng giá trị kho hàng, sản phẩm đắt nhất và danh sách cảnh báo tồn kho thấp (`quantity < 10`).
  * **5 điểm:** Tìm kiếm phân biệt hoa thường khắt khe; Thống kê tính toán sai công thức tổng tiền hoặc bỏ sót cảnh báo tồn kho.
  * **0 điểm:** Không triển khai logic tìm kiếm và thống kê.

---

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
* **Kiểm tra trùng lặp và Ràng buộc dữ liệu (15 điểm):**
  * **15 điểm:** Kiểm tra không cho phép thêm `item_id` trùng lặp trong kho hàng; Ràng buộc thành công `quantity >= 0` và `unit_price > 0`.
  * **8 điểm:** Có kiểm tra số dương nhưng bỏ sót logic kiểm tra trùng mã `item_id`.
  * **0 điểm:** Cho phép nhập mã trùng thoải mái, nhập số lượng và giá bán là số âm mà không báo lỗi.
* **Bắt ngoại lệ nhập sai kiểu dữ liệu (15 điểm):**
  * **15 điểm:** Sử dụng khối `try-except ValueError` ở tất cả các vị trí nhập số (`int`, `float`). Khi người dùng nhập chữ vào ô số lượng/giá bán, chương trình in thông báo lỗi thân thiện và không bị crash.
  * **8 điểm:** Đã có `try-except` ở chức năng thêm mới nhưng thiếu ở chức năng cập nhật hoặc chọn menu.
  * **0 điểm:** Không dùng `try-except`, chương trình bị ngắt đột ngột (Crash Exception) ngay khi nhập sai định dạng số.

---

#### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
* **Sắp xếp và Phân loại dữ liệu hiển thị (10 điểm):**
  * **10 điểm:** Triển khai thêm khả năng sắp xếp danh sách kho hàng theo Đơn giá giảm dần/tăng dần hoặc lọc danh sách theo Danh mục (`category`) trước khi hiển thị (dùng thuật toán sắp xếp cơ bản hoặc `list.sort()` / `sorted()`).
  * **5 điểm:** Có ý định thực hiện tính năng sắp xếp/lọc nhưng kết quả chưa chính xác hoàn toàn.
  * **0 điểm:** Không thực hiện chức năng nâng cao này.

---

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **Quy chuẩn đặt tên Tiếng Anh & Mã nguồn sạch (5 điểm):**
  * **5 điểm:** Tất cả các biến (`item_id`, `total_inventory_value`, `inventory_list`...) đều là Tiếng Anh chuẩn `snake_case`. Mã nguồn có chú thích [NOTE] rõ ràng, trình bày thụt lề chuẩn PEP 8.
  * **2 điểm:** Đặt tên biến lẫn lộn Tiếng Việt không dấu (ví dụ: `giam gia`, `danh_sach_sp`).
  * **0 điểm:** Đặt tên biến vô nghĩa (`a, b, c, x, y`), mã nguồn không tuân thủ thụt lề.
* **Quy chuẩn Repository & Lịch sử Commit (5 điểm):**
  * **5 điểm:** Nộp đúng link GitHub Public Repository, cấu trúc file (`main.py`, `README.md`) chính xác. Có từ 4-5 commit thể hiện quá trình làm bài.
  * **2 điểm:** Nộp file nén `.zip` hoặc repository chỉ có 1 commit duy nhất "first commit".
  * **0 điểm:** Link repository không tồn tại hoặc ở chế độ Private.

---

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
* **+5 điểm:** Định dạng hiển thị tiền tệ VNĐ cực kỳ đẹp mắt (ví dụ: `25,000 VNĐ` thay vì `25000.0`) và căn chỉnh bảng Console bằng các ký tự phân cách cột rõ ràng.
* **+5 điểm:** Tự động tạo sẵn dữ liệu giả lập ban đầu (Initial Mock Data gồm 3-5 sản phẩm) khi vừa bật ứng dụng để giảng viên/người chấm dễ dàng kiểm thử mà không cần mất thời gian nhập mới từ đầu.
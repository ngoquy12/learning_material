# **Tiêu chí chấm điểm (AI)**
**Mini Project 1: Xây dựng Hệ thống Quản lý Bán hàng Console (Phần 1) — Tổng điểm: 100 điểm**

---

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
*   **Môi trường & Thư mục (10 điểm):**
    *   Khởi tạo thành công môi trường ảo `virtualenv` trên Python 3.12.
    *   Cấu trúc thư mục phân chia rõ ràng các module (`product_service.py`, `order_service.py`, `storage_service.py`, `main.py`). Có tệp `README.md` hướng dẫn chi tiết cách khởi chạy.
*   **Cú pháp & Type Hints (10 điểm):**
    *   Sử dụng Type Hints chuẩn của Python 3.12 (`List`, `Dict`, `Tuple`, `Optional`) cho 100% các tham số đầu vào và giá trị trả về của hàm.
    *   Mã nguồn tuân thủ quy chuẩn **PEP 8** (đặt tên biến/hàm dạng `camelCase` theo chuẩn yêu cầu đề bài hoặc `snake_case` chuẩn PEP 8 Python, thụt lùi 4 dấu cách, không dư thừa dòng trống).

---

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
*   **Quản lý sản phẩm (10 điểm):**
    *   Hàm `addProduct()` thêm sản phẩm mới chính xác vào danh sách/dict, kiểm tra trùng lặp `productId`.
    *   Hàm `updateProductQuantity()` cập nhật tồn kho chính xác.
    *   Hàm `findProductById()` và `searchProductsByName()` tìm kiếm đúng và tối ưu.
*   **Quản lý giỏ hàng & Thanh toán (10 điểm):**
    *   Hàm `addItemToCart()` xử lý chính xác việc kiểm tra số lượng tồn kho trước khi cho phép thêm vào giỏ.
    *   Hàm `calculateCartTotal()` tính tổng tiền chính xác, có xử lý làm tròn hoặc định dạng số thực tiền tệ.
    *   Hàm `checkoutCart()` trừ tồn kho sản phẩm thực tế, khởi tạo bản ghi đơn hàng thành công.
*   **Thiết kế hàm & Không dùng OOP (10 điểm):**
    *   Tuân thủ 100% phạm vi cấm: Không sử dụng từ khóa `class`, không sử dụng kết nối SQL Database.
    *   Các hàm được thiết kế nguyên tử (Atomic functions), nhận đầu vào qua tham số và trả về kết quả qua `return`.

---

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
*   **lỗi thường gặp đầu vào Console (15 điểm):**
    *   lỗi thường gặp thành công khi người dùng nhập sai kiểu dữ liệu trên Console (ví dụ nhập chuỗi ký tự cho số lượng hoặc đơn giá) bằng `try-except (ValueError)`.
    *   Xử lý chọn menu hợp lệ, hiển thị thông báo lỗi rõ ràng bằng Tiếng Việt thân thiện và cho phép người dùng nhập lại mà không bị sập ứng dụng (Crash).
*   **Ràng buộc nghiệp vụ (15 điểm):**
    *   Kiểm tra đơn giá `unitPrice` phải lớn hơn 0; `quantityInStock` không được âm.
    *   Cảnh báo và ngăn chặn khi số lượng sản phẩm mua vượt quá số lượng tồn kho hiện có trong `addItemToCart()`.
    *   Xử lý ngoại lệ `KeyError` hoặc `IndexError` khi truy cập dữ liệu sản phẩm/đơn hàng không tồn tại.

---

#### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
*   **Lưu trữ tệp dữ liệu Persistency (5 điểm):**
    *   Hàm `saveDataToFile()` và `loadDataFromFile()` đọc/ghi dữ liệu sản phẩm và lịch sử đơn hàng ra tệp `JSON` hoặc `CSV` thành công.
    *   Tự động khôi phục dữ liệu cũ khi ứng dụng khởi chạy lại và tạo tệp mới nếu tệp chưa tồn tại (`FileNotFoundError`).
*   **Kiểm thử đơn vị hoặc Chức năng nâng cao (5 điểm):**
    *   Viết mã kiểm thử đơn vị cơ bản (`doctest` hoặc các hàm test dạng `test_product_service.py`) cho các hàm logic chính.
    *   Hoặc tích hợp tính năng lọc nâng cao `filterProductsByCategory()` kết hợp sắp xếp giá tăng/giảm.

---

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **Đặt tên tiếng Anh chuẩn mực (5 điểm):**
    *   100% tên hàm, tên biến, tham số và các khóa Dictionary (`productId`, `unitPrice`, `addItemToCart`...) viết bằng Tiếng Anh có nghĩa.
    *   Không đặt tên biến dạng tiếng Việt không dấu (như `them_san_pham`, `gia_tien`).
*   **Quy chuẩn nộp bài & Git (5 điểm):**
    *   Nộp đúng link GitHub Repository hoạt động.
    *   Tệp `.gitignore` được cấu hình chuẩn (bỏ qua thư mục `.venv/`, `__pycache__/`, `.cursor/`).
    *   Commit history thể hiện quá trình phát triển bài bản.

---

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
*   **[BONUS 5 ĐIỂM]:** Giao diện Console CLI được trình bày dưới dạng bảng đẹp mắt (sử dụng format chuỗi căn lề hoặc thư viện `tabulate`/`rich`).
*   **[BONUS 5 ĐIỂM]:** Tìm kiếm sản phẩm thông minh gần đúng (Fuzzy Search / Case-insensitive substring matching) theo tên sản phẩm.

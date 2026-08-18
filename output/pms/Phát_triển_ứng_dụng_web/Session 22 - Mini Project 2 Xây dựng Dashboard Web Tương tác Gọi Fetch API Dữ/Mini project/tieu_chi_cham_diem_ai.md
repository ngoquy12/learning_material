### **Tiêu chí chấm điểm (AI)**
**Dynamic Product Analytics Dashboard — Tổng điểm: 100 điểm**

---

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
- **HTML5 & CSS3 Layout (10 điểm):**
  - Đạt (10 điểm): Cấu trúc HTML5 chuẩn Semantic (`header`, `main`, `section`, `aside`). Sử dụng CSS Grid hoặc Flexbox để dựng giao diện Dashboard cân đối, phân chia rõ vùng Metrics, Thanh công cụ Filter/Search và Danh sách Sản phẩm.
  - Không đạt (0-5 điểm): Giao diện vỡ layout, không responsive cơ bản, sử dụng thẻ HTML không đúng ngữ nghĩa.
- **Tổ chức thư mục và Khởi tạo DOM (10 điểm):**
  - Đạt (10 điểm): Tổ chức tệp chuẩn theo đề bài (`index.html`, `css/styles.css`, `js/app.js`, `js/api.js`). Truy xuất và tham chiếu đúng các phần tử DOM thông qua `querySelector` / `getElementById`.
  - Không đạt (0-5 điểm): Để chung toàn bộ code trong một tệp duy nhất, khai báo sai đường dẫn script.

---

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
- **Xử lý Bất đồng bộ với Fetch API & Async/Await (10 điểm):**
  - Đạt (10 điểm): Sử dụng thành thạo cú pháp `async/await` kết hợp `fetch()` để truy xuất dữ liệu động từ máy chủ. Nhận và bóc tách thành công định dạng JSON.
  - Không đạt (0-4 điểm): Sử dụng sai cú pháp async/await, không lấy được dữ liệu từ API.
- **Tính toán Chỉ số Metrics Nghiệp vụ (10 điểm):**
  - Đạt (10 điểm): Viết hàm `calculateMetrics()` chính xác 100% các chỉ số: Tổng số lượng sản phẩm, Giá trị kho (`price * stock`), Đánh giá trung bình, Số lượng hàng hết tồn kho bằng các phương thức mảng ES6+ (`reduce`, `filter`).
  - Không đạt (0-4 điểm): Tính toán sai công thức, kết quả hiển thị không chính xác.
- **Render Dynamic DOM Danh sách Sản phẩm (10 điểm):**
  - Đạt (10 điểm): Render mảng sản phẩm thành các Card/Row sinh động. Cập nhật chính xác các thông tin: hình ảnh, tên, danh mục, giá bán, điểm đánh giá và badge phân loại tồn kho.
  - Không đạt (0-4 điểm): Không render được danh sách hoặc render trùng lặp phần tử.

---

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
- **Quản lý Trạng thái Tải dữ liệu UI (Loading State) (10 điểm):**
  - Đạt (10 điểm): Hiển thị hiệu ứng Spinner hoặc Skeleton trong thời gian chờ gọi API và tự động ẩn khi hoàn tất tải dữ liệu.
  - Không đạt (0-4 điểm): Trắng màn hình trong thời gian chờ API, không có phản hồi thị giác cho người dùng.
- **Xử lý Ngoại lệ Network & API Error (10 điểm):**
  - Đạt (10 điểm): Bọc toàn bộ thao tác async trong khối `try...catch`. Xử lý các trường hợp Response HTTP Error (404, 500) hoặc lỗi mất kết nối mạng và hiển thị Banner thông báo lỗi màu đỏ trực quan trên UI.
  - Không đạt (0-4 điểm): Không có khối `try...catch`, ứng dụng bị crash im lặng (uncaught error trong Console) khi API bị lỗi.
- **Bộ lọc & Tìm kiếm Động (10 điểm):**
  - Đạt (10 điểm): Lọc danh sách tức thì theo từ khóa nhập vào (không phân biệt hoa/thường) và chọn danh mục. Trường hợp không tìm thấy sản phẩm thỏa điều kiện, hiển thị thông báo "Không tìm thấy sản phẩm phù hợp".
  - Không đạt (0-4 điểm): Bộ lọc không hoạt động hoặc bị lỗi khi mảng rỗng.

---

#### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
- **Xem Chi tiết Sản phẩm với Modal Dialog (5 điểm):**
  - Đạt (5 điểm): Bắt sự kiện click vào sản phẩm, hiển thị Modal hiển thị thông tin chi tiết đầy đủ (mô tả sản phẩm, thương hiệu, số lượng tồn kho) và xử lý sự kiện đóng Modal chuẩn xác.
  - Không đạt (0 điểm): Không xây dựng chức năng Modal chi tiết.
- **Sắp xếp Đa tiêu chí Dynamic (5 điểm):**
  - Đạt (5 điểm): Cho phép người dùng sắp xếp danh sách theo Giá tăng/giảm dần, hoặc Đánh giá (Rating) từ cao xuống thấp bằng hàm `sort()`.
  - Không đạt (0 điểm): Không có chức năng sắp xếp.

---

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
- **Quy chuẩn Đặt tên & Clean Code ES6+ (5 điểm):**
  - Đạt (5 điểm): Tất cả tên biến, hàm, tham số sử dụng 100% Tiếng Anh có nghĩa theo quy chuẩn `camelCase` (ví dụ: `fetchProducts`, `totalInventoryValue`, `renderProductList`). Mã nguồn rõ ràng, không chứa code thừa.
  - Không đạt (0-2 điểm): Đặt tên tiếng Việt không dấu, tên biến 1 ký tự (`a`, `b`, `x`), đặt tên sai quy chuẩn camelCase.
- **Tuân thủ Quy chuẩn GitHub & Document (5 điểm):**
  - Đạt (5 điểm): Đẩy mã nguồn lên GitHub Repository public theo đúng cấu trúc gợi ý. Tệp `README.md` trình bày chuyên nghiệp, có mô tả và ảnh chụp ứng dụng.
  - Không đạt (0-2 điểm): Thiếu tệp README, nộp sai định dạng link hoặc repository ở chế độ Riêng tư (Private).

---

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
- **Tối ưu hóa UI/UX & Kỹ thuật Advanced (10 điểm):**
  - +5 điểm: Áp dụng kỹ thuật Debounce cho ô tìm kiếm giúp giảm tần suất xử lý khi người dùng nhập liệu liên tục.
  - +5 điểm: Thiết kế giao diện Chế độ Tối/Sáng (Dark/Light Mode Toggle) bằng CSS Variables và xử lý sự kiện chuyển đổi giao diện động trên DOM.
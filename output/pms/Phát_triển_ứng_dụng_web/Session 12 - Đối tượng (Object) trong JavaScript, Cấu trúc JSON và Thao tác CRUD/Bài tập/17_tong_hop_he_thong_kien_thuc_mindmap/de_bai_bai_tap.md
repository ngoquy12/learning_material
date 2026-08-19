# <center>[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) - Session 12</center>

### **1. Mục tiêu**
- Hệ thống hóa toàn bộ kiến thức cốt lõi về **Object Literal, Cấu trúc JSON và các thao tác CRUD thuộc tính** trong JavaScript.
- Trực quan hóa cấu trúc dữ liệu nghiệp vụ của hệ thống **Quản lý Đặt phòng Khách sạn (HOTEL_BOOKING)** bằng Sơ đồ Tư duy (Mindmap).
- Rèn luyện tư duy phân tầng logic, nhận diện và khắc phục các bẫy lỗi cú pháp (`ReferenceError`, `SyntaxError`, rò rỉ bộ nhớ do gán `undefined`, lỗi thao tác trực tiếp trên chuỗi JSON).

### **2. Bối cảnh & Vấn đề**
Bạn đang đảm nhận vai trò **Kỹ sư Phần mềm (Software Engineer)** tại hệ thống quản lý đặt phòng khách sạn **GrandStay Hotel Booking System**. Để hỗ trợ đào tạo và hội nhập (onboarding) cho các lập trình viên mới gia nhập dự án, bạn được giao nhiệm vụ xây dựng một **Sơ đồ Tư duy (Mindmap) Kiến thức Tổng hợp** kết hợp với **Tài liệu Giải trình (summary.md)**. 

Toàn bộ sơ đồ và các ví dụ mã nguồn phải phản ánh trực quan nghiệp vụ xử lý dữ liệu đặt phòng khách sạn (ví dụ: `bookingTicket`, `guestProfile`, `roomDetail`).

---

### **3. Quy tắc nghiệp vụ**
Sơ đồ tư duy của bạn BẮT BUỘC phải bao phủ 3 nhánh kiến thức chính cùng các từ khóa trọng tâm được mô hình hóa theo dự án **HOTEL_BOOKING**:

#### **Nhánh 1: Khái niệm Object Literal & Phương thức truy cập thuộc tính**
- **Cấu trúc Key-Value**: Đóng gói thông tin đơn đặt phòng `bookingTicket` (ví dụ: `bookingId`, `roomType`, `pricePerNight`, `isPaid`).
- **Dot Notation (Truy cập bằng dấu chấm)**:
  - Cú pháp chuẩn cho tên key tiêu chuẩn (`camelCase`).
  - Ví dụ: `bookingTicket.roomType`, `bookingTicket.pricePerNight`.
- **Bracket Notation (Truy cập bằng dấu ngoặc vuông)**:
  - Bắt buộc dùng khi tên key chứa ký tự đặc biệt (như dấu gạch ngang `-`).
  - Ví dụ: `bookingTicket["check-in-date"]`, `bookingTicket["promo-code"]`.
- **Dynamic Key Access (Truy cập key động qua biến số)**:
  - Dùng ngoặc vuông khi tên thuộc tính được lưu trong một biến số.
  - Ví dụ: `const targetField = "pricePerNight"; console.log(bookingTicket[targetField]);`.
- **Bẫy lỗi cần phòng tránh**:
  - *ReferenceError*: Quên dấu nháy `'` hoặc `"` trong ngoặc vuông (ví dụ: `bookingTicket[roomType]` -> JS hiểu nhầm `roomType` là biến chưa khai báo).
  - *SyntaxError*: Dùng Dot Notation cho key chứa ký tự đặc biệt (ví dụ: `bookingTicket.check-in-date` -> JS hiểu là phép trừ).

#### **Nhánh 2: Thao tác CRUD thuộc tính trên Object**
- **Create (Thêm mới)**: Thêm trường dữ liệu mới vào Object đang tồn tại (ví dụ: `bookingTicket.discountAmount = 200000;`, `bookingTicket["special-request"] = "Late check-out";`).
- **Read (Đọc/Truy xuất)**: Đọc giá trị thuộc tính để tính toán hoặc hiển thị lên giao diện hóa đơn.
- **Update (Cập nhật)**: Thay đổi giá trị thuộc tính hiện có (ví dụ: `bookingTicket.isPaid = true;`).
- **Delete (Xóa thuộc tính)**:
  - Sử dụng toán tử `delete` để xóa hoàn toàn key khỏi bộ nhớ (ví dụ: `delete bookingTicket.tempSessionToken;`).
- **Bẫy lỗi cần phòng tránh**:
  - Gán `bookingTicket.tempToken = undefined` thay vì dùng `delete`: Thuộc tính vẫn tồn tại trong Object, gây lãng phí bộ nhớ và lỗi logic khi kiểm tra sự tồn tại của key.

#### **Nhánh 3: Cấu trúc JSON & Chuyển đổi Dữ liệu API**
- **Khái niệm JSON (JavaScript Object Notation)**: Định dạng chuỗi văn bản dùng để trao đổi dữ liệu giữa giao diện (Frontend) và máy chủ (Backend).
- **JSON.stringify(object)**:
  - Đóng gói Object JavaScript thành chuỗi JSON tiêu chuẩn để truyền qua mạng.
  - Tự động bỏ qua các thuộc tính có giá trị `undefined`.
- **JSON.parse(jsonString)**:
  - Giải mã chuỗi JSON thành Object JavaScript để truy xuất dữ liệu.
- **Bẫy lỗi cần phòng tránh**:
  - Cố gắng truy cập thuộc tính trực tiếp trên chuỗi JSON chưa được `parse` (ví dụ: `const jsonStr = '{"bookingId":"BK-101"}'; console.log(jsonStr.bookingId);` -> trả về `undefined`).

---

### **4. Yêu cầu bài toán (Sản phẩm nộp)**
Học viên cần hoàn thiện và đóng gói bộ hồ sơ thiết kế gồm **03 sản phẩm**:
1. **File ảnh Sơ đồ tư duy** (`mindmap.png` hoặc `mindmap.jpg`): Ảnh chụp rõ nét, bố cục khoa học của sơ đồ.
2. **File thiết kế gốc** (`mindmap.xmind` hoặc `mindmap.pdf`): File xuất từ các công cụ vẽ sơ đồ (XMind, MindMeister, Draw.io, hoặc PDF).
3. **Bản tóm tắt giải trình** (`summary.md`): File Markdown giải thích chi tiết các nhánh tư duy, kèm đoạn mã nguồn ví dụ hoàn chỉnh bằng JavaScript áp dụng bài toán **HOTEL_BOOKING**.

---

### **5. Yêu cầu nộp bài**
Học viên nộp bài theo đúng quy chuẩn GitHub của khóa học:
* Đẩy toàn bộ thư mục bài tập lên GitHub Repository cá nhân/nhóm theo cấu trúc tên chuẩn:
  `[Tên Lớp]_[Môn Học]_Session12_Mindmap`
  
  *Ví dụ:* `HNKS25CNTT1_Core_Session12_Mindmap`

* **Cấu trúc cây thư mục trong Repository:**

```text
  HNKS25CNTT1_Core_Session12_Mindmap/
  ├── mindmap.png (hoặc mindmap.jpg)
  ├── mindmap.xmind (hoặc mindmap.pdf)
  └── summary.md
```

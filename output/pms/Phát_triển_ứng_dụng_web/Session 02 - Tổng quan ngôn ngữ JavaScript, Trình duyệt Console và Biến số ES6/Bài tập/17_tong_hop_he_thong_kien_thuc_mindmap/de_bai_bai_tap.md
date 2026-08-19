# <center>[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) - Session 02</center>

### **1. Mục tiêu**
- Hệ thống hóa toàn bộ kiến thức cốt lõi và các bẫy lỗi nghiệp vụ trong **Session 02: Tổng quan ngôn ngữ JavaScript, Trình duyệt Console và Biến số ES6**.
- Trực quan hóa cấu trúc dữ liệu, cơ chế thực thi của JS Engine (V8 Engine) và luồng xử lý nhập/xuất dữ liệu hệ thống thông qua **Sơ đồ Tư duy (Mindmap)**.
- Áp dụng trực tiếp vào dự án thực tế **Hệ thống Đặt lịch Khám bệnh trực tuyến (CLINIC_APPOINTMENT)** để định chuẩn quy tắc đặt tên, quản lý phạm vi biến số và tính toán chi phí khám bệnh.
- Rèn luyện kỹ năng phân tầng logic, tối ưu hóa mã nguồn ES6 và trình bày tài liệu kỹ thuật chuẩn doanh nghiệp cho thành viên mới (Onboarding Developers).

---

### **2. Bối cảnh & Vấn đề**
Bạn đang đảm nhận vai trò **Kỹ sư Phần mềm Cấp cao (Senior Software Engineer)** tại phòng khám đa khoa quốc tế, thuộc dự án xây dựng ứng dụng **Hệ thống Đặt lịch Khám bệnh (CLINIC_APPOINTMENT)**. 

Để chuẩn bị đào tạo và chuyển giao công nghệ cho các lập trình viên mới (Junior Developers), bạn được yêu cầu xây dựng một **Sơ đồ tư duy toàn diện (System & Knowledge Mindmap)** kết hợp với **Bản giải trình kỹ thuật (summary.md)**. Sơ đồ này phải đóng vai trò là "Kim chỉ nam" kỹ thuật giúp toàn đội nắm vững bản chất JavaScript, từ cơ chế biên dịch bytecode của V8 Engine đến quy định khai báo biến ES6 và các bẫy ép kiểu dữ liệu trong module tính phí dịch vụ y tế.

---

### **3. Quy tắc nghiệp vụ**
Sơ đồ tư duy và tài liệu tổng hợp của bạn **BẮT BUỘC** phải bao phủ và kết nối chặt chẽ các nhóm kiến thức sau trong ngữ cảnh hệ thống **CLINIC_APPOINTMENT**:

#### **Nhánh 1: Tong quan JavaScript & Cơ che V8 Engine trong Ung dung Y te**
- **Cơ chế thực thi V8 Engine**: Luồng xử lý từ HTML Parser -> Tải tệp `script.js` vào RAM -> **V8 Engine (Parser -> Ignition Bytecode)** -> Thực thi và cập nhật DOM giao diện phòng khám (`h1#clinic-title`, `div#appointment-status`).
- **Vị trí nhúng mã JavaScript chuẩn**:
  - *Thực hành tốt (Best Practice)*: Đặt thẻ `<script src="app.js">` ở cuối `<body>` hoặc trước thẻ đóng `</body>` để tránh hiện tượng chặn luồng dựng DOM (DOM Blocking) và giúp V8 Engine cache bytecode hiệu quả.
  - *Cạm bẫy thực tế (Anti-pattern)*: Nhúng JS trực tiếp trong thẻ `<head>` không có thuộc tính điều hướng hoặc viết mã inline vào thuộc tính HTML (`onclick="calculateFee()"`), làm vi phạm nguyên tắc tách biệt giao diện - logic.

#### **Nhánh 2: Môi truong Phap trien & Runtime Environment**
- **Trình duyệt (Browser Console) vs Node.js Runtime**:
  - Trình duyệt: Môi trường Client-side, thao tác với DOM (`document.getElementById`), nhận dữ liệu từ `prompt()` và xuất dữ liệu qua `alert()`, `console.log()`.
  - Node.js Runtime: Môi trường Server-side, chạy file mã nguồn độc lập bằng dòng lệnh `node app.js`, kiểm tra phiên bản qua Terminal (`node -v`).
- **Máy chủ phát triển Live Server HTTP vs Giao thức File (file:///)**:
  - Tải trang qua giao thức HTTP/HTTPS bằng **Live Server** để đảm bảo khả năng nạp lại tự động (Live Reload), hỗ trợ cơ chế bảo mật trình duyệt và tối ưu đường dẫn tài nguyên.
  - Tránh mở trực tiếp file `file:///C:/project/index.html` làm phát sinh lỗi CORS và không mô phỏng đúng môi trường vận hành thực tế của phòng khám.

#### **Nhánh 3: Bien so ES6 & Quy chuan Dat ten trong CLINIC_APPOINTMENT**
- **So sánh 3 từ khóa khai báo biến (`const`, `let`, `var`)**:
  - `const`: Dùng cho hằng số không thay đổi trong toàn bộ vòng đời ứng dụng. *Ví dụ phòng khám*: `const clinicId = "CLINIC-VN-001"`, `const baseConsultationFee = 200000`, `const vatRate = 0.08`.
  - `let`: Dùng cho biến số có thể thay đổi giá trị theo tiến trình xử lý. *Ví dụ*: `let patientName = "Nguyễn Văn A"`, `let appointmentDate = "2026-03-20"`, `let totalPayment = 0`, `let discountCode = null`.
  - `var`: **CẤM SỬ DỤNG** trong dự án do gây ô nhiễm phạm vi toàn cục (Global Scope Leak), rủi ro Hoisting ngầm gán `undefined` và cho phép khai báo trùng tên biến dẫn đến ghi đè dữ liệu bệnh nhân.
- **Quy chuẩn đặt tên (Naming Conventions)**:
  - Sử dụng chuẩn **camelCase** cho tên biến/hằng số dạng đối tượng thông thường (`patientAge`, `doctorSpecialty`, `isFirstVisit`).
  - Phải dùng tên tiếng Anh có nghĩa, tuyệt đối không dùng tiếng Việt không dấu (`tenBenhNhan`), ký tự viết tắt khó hiểu (`pName`, `cFee`) hoặc bắt đầu bằng chữ số (`1stAppointment`).

#### **Nhánh 4: Nhap xuat Du lieu & Tinh toan Phieu Dat lich (Template Literals)**
- **Nhập/Xuất dữ liệu nguyên thủy**:
  - Lấy thông tin từ lễ tân/bệnh nhân qua `prompt("Nhập tên bệnh nhân:")`, `prompt("Nhập phí dịch vụ bổ sung:")`.
  - Xuất thông báo qua `alert()` và ghi nhật ký hệ thống qua `console.log()`.
- **Bẫy ép kiểu dữ liệu minh bạch (Type Casting)**:
  - Giá trị trả về từ `prompt()` luôn ở dạng Chuỗi (**String**).
  - *Lỗi nghiêm trọng (Bug)*: Phép cộng `prompt("Phí khám") + prompt("Phí xét nghiệm")` dẫn đến nối chuỗi toán học (`"300000" + "150000" = "300000150000"`).
  - *Giải pháp*: Phải ép kiểu minh bạch sang kiểu **Number** ngay tại đầu vào bằng `Number(prompt(...))` để đảm bảo phép tính tổng chi phí khám bệnh đúng logic số học.
- **Chuỗi Template Literals (ES6 Backticks)**:
  - Thay thế việc nối chuỗi thủ công bằng toán tử `+` rườm rà.
  - Sử dụng cú pháp nhúng biểu thức `` `Mã phiếu: ${appointmentId} | Bệnh nhân: ${patientName} | Tổng phí: ${consultationFee + serviceFee} VNĐ` `` để hiển thị hóa đơn và thông báo xác nhận đặt lịch khám rõ ràng, chuyên nghiệp.

---

### **4. Yêu cầu bài toán (Sản phẩm nộp)**
Học viên đóng vai trò Lead Engineer để thiết kế bộ hồ sơ Onboarding bao gồm **3 sản phẩm bắt buộc**:

1. **File ảnh Sơ đồ tư duy (`mindmap.png` hoặc `mindmap.jpg`)**:
   - Hình ảnh xuất ra rõ nét, trình bày trực quan, sử dụng màu sắc phân biệt giữa 4 nhánh kiến thức chính.
2. **File thiết kế gốc (`mindmap.xmind` hoặc `mindmap.pdf`)**:
   - File chỉnh sửa từ các công cụ Mindmap (XMind, MindMaster, Diagrams.net, Canva, Figma...).
3. **Bản tóm tắt giải trình kỹ thuật (`summary.md`)**:
   - VIết theo định dạng Markdown mô tả cấu trúc Sơ đồ tư duy, bao gồm:
     - Giải thích luồng hoạt động từ V8 Engine đến việc render trang đặt lịch khám.
     - Ma trận so sánh `const` vs `let` vs `var` áp dụng vào mô hình dữ liệu Bệnh nhân/Bác sĩ.
     - Kịch bản minh họa bằng mã nguồn JS (chuẩn ES6) thực hiện tính toán Phiếu đặt lịch khám có sử dụng `prompt()`, `Number()`, `console.log()` và Template Literals.

---

### **5. Yêu cầu nộp bài**
Học viên nộp bài theo quy chuẩn quản lý mã nguồn GitHub:
- Đẩy toàn bộ mã nguồn, file sơ đồ và file `summary.md` lên GitHub Repository công khai với tên đặt theo chuẩn:
  `[Tên Lớp]_[Môn Học]_Session02_Mindmap`
  *Ví dụ*: `HNKS25CNTT1_Core_Session02_Mindmap`

- **Cấu trúc thư mục Repository bắt buộc**:

```text
  HNKS25CNTT1_Core_Session02_Mindmap/
  ├── docs/
  │   ├── mindmap.png (hoặc mindmap.jpg)
  │   └── mindmap.xmind (hoặc mindmap.pdf)
  ├── src/
  │   ├── index.html (Trang HTML gắn script chuẩn)
  │   └── app.js (Mã nguồn JS tính phí khám bệnh theo chuẩn ES6)
  └── summary.md (Bản tóm tắt giải trình kiến thức hệ thống)
```

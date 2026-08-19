# Bài thực hành: Xây dựng Phân hệ Nhập xuất Dữ liệu và Tính Hóa đơn Đặt vé Xem phim TRUEMAX

## 1. Mục tiêu bài học
- Vận dụng kiến thức JavaScript Vanilla (ES6+), HTML5/CSS3 và Cursor AI IDE để thu thập, xử lý và hiển thị dữ liệu người dùng.
- Thành thạo việc nhận dữ liệu từ prompt(), xử lý giá trị mặc định chuỗi và ép kiểu dữ liệu an toàn bằng parseInt(), parseFloat().
- Kiểm soát các bẫy dữ liệu (NaN, số âm) với Number.isNaN() và đưa ra cảnh báo console.warn() / console.error() thích hợp.
- Ứng dụng chuỗi Template Literals (backticks), các phương thức xử lý chuỗi (toUpperCase), toLocaleString() và console.table() để định dạng và in hóa đơn thanh toán chuyên nghiệp.
- Thành thạo thao tác thực hành và kiểm chuẩn kết quả trên môi trường Trình duyệt và Console của Cursor AI IDE.

## 2. Yêu cầu bài toán
Doanh nghiệp rạp chiếu phim TRUEMAX yêu cầu xây dựng phân hệ nhập xuất dữ liệu và tính toán hóa đơn tự động cho khách hàng. Hệ thống cần nhận 5 tham số đầu vào từ khách hàng thông qua hàm prompt(): Tên khách hàng, Tên phim, Số lượng vé, Đơn giá vé (VNĐ), và Tỷ lệ giảm giá (%).

Nghiệp vụ hệ thống yêu cầu cài đặt các logic sau:
1. Thu thập dữ liệu: Nếu người dùng không nhập hoặc nhấn Hủy (Cancel), hệ thống phải tự động gán giá trị mặc định chuỗi an toàn (Ví dụ: Tên khách hàng = 'Khách hàng vô danh', Tên phim = 'Chưa chọn phim').
2. Ép kiểu và Kiểm tra dữ liệu: Chuyển đổi dữ liệu Số lượng vé sang số nguyên (parseInt), Đơn giá vé và Tỷ lệ giảm giá sang số thực (parseFloat). Kiểm tra nếu dữ liệu không phải là số (NaN) hoặc là số âm, hệ thống phải tự động đưa về 0 và phát cảnh báo console.warn() ra Console.
3. Tính toán tài chính: Tổng tiền gốc = Số lượng vé * Đơn giá vé. Số tiền giảm giá = Tổng tiền gốc * (Tỷ lệ giảm giá / 100). Tổng chi phí thanh toán = Tổng tiền gốc - Số tiền giảm giá.
4. Xuất dữ liệu theo dõi: Hiển thị bảng tổng quan dữ liệu đặt vé bằng hàm console.table().
5. Xuất hóa đơn chi tiết: Sử dụng chuỗi Template Literals (cặp dấu backticks `` ` ``) để định dạng và in ra hóa đơn thanh toán hoàn chỉnh. Tên khách hàng phải được in hoa (.toUpperCase()), các giá trị tiền tệ được định dạng theo chuẩn Việt Nam (.toLocaleString('vi-VN')), và hiển thị trạng thái hóa đơn dựa trên tổng chi phí thanh toán.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Cursor AI IDE, trình duyệt web (Google Chrome hoặc Microsoft Edge), thư mục bài thực hành chứa tệp index.html và script.js.

### Các bước thực hiện:
1. Bước 1: Mở Cursor AI IDE, khởi tạo cấu trúc thư mục bài thực hành bao gồm tệp index.html và tệp script.js. Nhúng tệp script.js vào trang HTML bằng thẻ <script>.
2. Bước 2: Khai báo các biến và sử dụng hàm prompt() để nhận dữ liệu đầu vào. Áp dụng toán tử logic OR (||) để thiết lập giá trị mặc định cho chuỗi.
3. Bước 3: Thực hiện ép kiểu dữ liệu từ Chuỗi sang Số. Sử dụng hàm Number.isNaN() và câu lệnh điều kiện để kiểm tra dữ liệu hợp lệ, đưa ra thông báo console.warn() nếu phát hiện dữ liệu lỗi.
4. Bước 4: Thực hiện các phép tính tài chính (Tổng tiền gốc, Tiền giảm giá, Tổng thanh toán thực tế).
5. Bước 5: Tạo đối tượng chứa dữ liệu hóa đơn và hiển thị dạng bảng trong Console bằng hàm console.table().
6. Bước 6: Xây dựng chuỗi Template Literals đa dòng thể hiện hóa đơn thanh toán chuyên nghiệp, áp dụng các hàm định dạng chuỗi và tiền tệ toLocaleString('vi-VN'), sau đó xuất kết quả ra Console và hiển thị thông báo alert() cho người dùng.

## 4. Mã nguồn tham khảo (Code Demo)

```text
// ==========================================
// HỆ THỐNG TÍNH HÓA ĐƠN ĐẶT VÉ XEM PHIM TRUEMAX
// Bài thực hành: Nhập xuất dữ liệu Console & Template Literals
// ==========================================

// Bước 1: Thu thập dữ liệu đầu vào với giá trị mặc định an toàn
const rawCustomerName = prompt("Nhập tên khách hàng:") || "Khách hàng vô danh";
const rawMovieName = prompt("Nhập tên phim chiếu:") || "Chưa chọn phim";
const rawTicketQuantity = prompt("Nhập số lượng vé đặt:");
const rawTicketPrice = prompt("Nhập đơn giá vé (VNĐ):");
const rawDiscountRate = prompt("Nhập tỷ lệ giảm giá (%):") || "0";

// Bước 2: Ép kiểu dữ liệu và kiểm soát bẫy NaN / Số âm
const parsedQuantity = parseInt(rawTicketQuantity, 10);
const parsedPrice = parseFloat(rawTicketPrice);
const parsedDiscount = parseFloat(rawDiscountRate);

// Gán giá trị fallback an toàn nếu nhập sai định dạng hoặc nhập số âm
const safeQuantity = Number.isNaN(parsedQuantity) || parsedQuantity < 0 ? 0 : parsedQuantity;
const safePrice = Number.isNaN(parsedPrice) || parsedPrice < 0 ? 0 : parsedPrice;
const safeDiscount = Number.isNaN(parsedDiscount) || parsedDiscount < 0 || parsedDiscount > 100 ? 0 : parsedDiscount;

// Phát cảnh báo trên Console nếu phát hiện dữ liệu bất thường
if (safeQuantity === 0 || safePrice === 0) {
  console.warn("[CẢNH BÁO HỆ THỐNG] Phát hiện số lượng hoặc đơn giá vé không hợp lệ! Đã tự động điều chỉnh về 0.");
}

// Bước 3: Tính toán các thông số tài chính
const originalTotal = safeQuantity * safePrice;
const discountAmount = originalTotal * (safeDiscount / 100);
const finalPayment = originalTotal - discountAmount;

// Bước 4: Hiển thị dữ liệu dạng bảng tổng quan bằng console.table()
const bookingSummary = {
  "Tên khách hàng": rawCustomerName,
  "Phim đặt vé": rawMovieName,
  "Số lượng vé": safeQuantity,
  "Đơn giá (VNĐ)": safePrice,
  "Mức giảm (%)": safeDiscount,
  "Tổng thanh toán (VNĐ)": finalPayment
};

console.log("[HỆ THỐNG TRUEMAX] Dữ liệu đặt vé ghi nhận thành công:");
console.table(bookingSummary);

// Bước 5: Định dạng chuỗi và xuất hóa đơn chi tiết bằng Template Literals
const formattedCustomerName = rawCustomerName.toUpperCase();
const formattedOriginalTotal = originalTotal.toLocaleString("vi-VN");
const formattedDiscountAmount = discountAmount.toLocaleString("vi-VN");
const formattedFinalPayment = finalPayment.toLocaleString("vi-VN");
const paymentStatus = finalPayment > 0 ? "HỢP LỆ (ĐÃ XÁC NHẬN)" : "CẦN CẢNH BÁO / KIỂM TRA LẠI";

const finalReceipt = `
==================================================
           HÓA ĐƠN ĐẶT VÉ TRUEMAX CINEMA          
==================================================
+ Khách hàng         : ${formattedCustomerName}
+ Phim chiếu         : ${rawMovieName}
+ Số lượng vé đặt    : ${safeQuantity} vé
+ Đơn giá niêm yết   : ${safePrice.toLocaleString("vi-VN")} VNĐ
--------------------------------------------------
+ Tổng tiền gốc      : ${formattedOriginalTotal} VNĐ
+ Giảm giá (${safeDiscount}%)     : -${formattedDiscountAmount} VNĐ
+ Tổng tiền thanh toán: ${formattedFinalPayment} VNĐ
--------------------------------------------------
+ Trạng thái hóa đơn : ${paymentStatus}
==================================================
`;

// Bước 6: In hóa đơn ra Console và hiển thị thông báo alert
console.log(finalReceipt);
alert(`Đặt vé thành công cho khách hàng: ${formattedCustomerName}\nTỔNG TIỀN THANH TOÁN: ${formattedFinalPayment} VNĐ`);
```

# 5. Checklist đánh giá kết quả
- [ ] Khởi tạo đúng cấu trúc thư mục và liên kết tệp JavaScript thành công trên Cursor AI IDE.
- [ ] Thu thập đầy đủ 5 trường thông tin đầu vào thông qua hàm prompt() và xử lý giá trị mặc định bằng toán tử OR (||).
- [ ] Ép kiểu dữ liệu chuỗi sang kiểu số chính xác (parseInt, parseFloat), tránh hoàn toàn lỗi cộng nối chuỗi ngoài ý muốn.
- [ ] Kiểm tra bẫy NaN và số âm bằng Number.isNaN(), xuất cảnh báo cảnh báo console.warn() chính xác khi dữ liệu đầu vào bị lỗi.
- [ ] Sử dụng đúng cú pháp Template Literals (bao bọc bởi cặp dấu backticks ` `) để nội suy biến ${} và định dạng hóa đơn đa dòng.
- [ ] Định dạng thành công tiền tệ bằng toLocaleString('vi-VN'), chuyển chữ hoa với toUpperCase(), và hiển thị danh mục dạng bảng qua console.table().

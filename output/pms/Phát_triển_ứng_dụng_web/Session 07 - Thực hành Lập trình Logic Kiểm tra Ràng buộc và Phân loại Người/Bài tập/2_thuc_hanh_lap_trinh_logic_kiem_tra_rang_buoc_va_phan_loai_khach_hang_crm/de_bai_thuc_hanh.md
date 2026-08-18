## <center>Thực Hành Lập Trình Logic Kiểm Tra Ràng Buộc Và Phân Loại Khách Hàng CRM</center>

### **1. Mục tiêu**
- **Về kiến thức:** Củng cố tư duy lập trình điều kiện nâng cao, nắm vững cú pháp `if/else`, cấu trúc rẽ nhánh `switch-case`, và biểu thức điều kiện ba ngôi (`ternary operator`).
- **Về kỹ năng:** Thực hành kiểm chuẩn dữ liệu đầu vào (data validation), xử lý logic phân loại đa tầng và định dạng dữ liệu đầu ra chuyên nghiệp bằng Template Literals trên môi trường Node.js / Cursor AI IDE.
- **Về thái độ:** Rèn luyện tư duy viết mã nguồn sạch (clean code), chuẩn hóa quy tắc đặt tên camelCase, thụt lề chuẩn xác và tối ưu hóa logic rẽ nhánh trong hệ thống quản trị khách hàng (CRM).

### **2. Vấn đề**
Bộ phận Quản trị Quan hệ Khách hàng (CRM) của một công ty cung cấp giải pháp doanh nghiệp cần một module tự động kiểm tra tính hợp lệ của dữ liệu đầu vào, đồng thời phân loại mức độ ưu tiên chăm sóc và phê duyệt hạn mức tín dụng cho từng đối tượng khách hàng.

Dữ liệu đầu vào của khách hàng được khai báo dưới dạng các biến nguyên thủy. Chương trình cần thực hiện qua 3 giai đoạn xử lý chính theo biểu đồ luồng dữ liệu dưới đây:

```mermaid

flowchart TD
    A(["Bắt đầu quy trình"]) --> B[/ "Đầu vào: Thông tin khách hàng (Tên, Tuổi, Doanh thu, Điểm tín nhiệm, Mã hạng, Nợ quá hạn)" /]
    B --> C{"Kiểm tra tính hợp lệ dữ liệu?"}
    C -->|Không hợp lệ| D[/ "Đầu ra: Hiển thị thông báo lỗi chi tiết và dừng xử lý" /]
    D --> Z(["Kết thúc: Dừng chương trình"])
    C -->|Hợp lệ| E[/"Xử lý switch-case: Xác định Tên hạng hội viên và Tỷ lệ chiết khấu"/]
    E --> F[/"Xử lý if-else-if: Phân loại cấp độ ưu tiên chăm sóc CRM"/]
    F --> G[/"Xử lý Ternary Operator: Đánh giá phê duyệt hạn mức tín dụng"/]
    G --> H[/ "Đầu ra: In báo cáo tổng hợp thông tin khách hàng ra Console" /]
    H --> Z

```

### **3. Yêu cầu bài toán**

Doanh nghiệp yêu cầu viết một file mã nguồn `crm_classifier.js` để lưu trữ và xử lý thông tin của khách hàng với các biến nguyên thủy mô tả trong bảng bên dưới:

<table border="1" style="width: 100%; border-collapse: collapse;">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">Tên biến (Identifier)</th>
      <th style="padding: 8px; text-align: left;">Kiểu dữ liệu</th>
      <th style="padding: 8px; text-align: left;">Mô tả giá trị</th>
      <th style="padding: 8px; text-align: left;">Ràng buộc hợp lệ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><code>customerName</code></td>
      <td style="padding: 8px;">String</td>
      <td style="padding: 8px;">Họ và tên khách hàng</td>
      <td style="padding: 8px;">Không được để chuỗi rỗng</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>customerAge</code></td>
      <td style="padding: 8px;">Number</td>
      <td style="padding: 8px;">Độ tuổi khách hàng</td>
      <td style="padding: 8px;">Từ 18 đến 100 (bao gồm 18 và 100)</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>annualRevenue</code></td>
      <td style="padding: 8px;">Number</td>
      <td style="padding: 8px;">Doanh thu đóng góp hàng năm (VNĐ)</td>
      <td style="padding: 8px;">Lớn hơn hoặc bằng 0</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>creditScore</code></td>
      <td style="padding: 8px;">Number</td>
      <td style="padding: 8px;">Điểm tín nhiệm đánh giá</td>
      <td style="padding: 8px;">Từ 300 đến 850 (bao gồm 300 và 850)</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>tierCode</code></td>
      <td style="padding: 8px;">Number</td>
      <td style="padding: 8px;">Mã số hạng hội viên hiện tại</td>
      <td style="padding: 8px;">Nhận các giá trị số 1, 2, 3, 4</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>hasOverdueDebt</code></td>
      <td style="padding: 8px;">Boolean</td>
      <td style="padding: 8px;">Trạng thái nợ quá hạn tín dụng</td>
      <td style="padding: 8px;"><code>true</code> (Có nợ) hoặc <code>false</code> (Không có nợ)</td>
    </tr>
  </tbody>
</table>

### **4. Quy tắc xử lý**

Chương trình phải áp dụng đúng các cấu trúc điều kiện đã học để giải quyết 4 yêu cầu theo đúng trình tự:

Yêu cầu 1: Kiểm chuẩn dữ liệu đầu vào (Data Validation)
- Sử dụng cấu trúc `if` và toán tử logic (`&&`, `||`, `!`) để kiểm tra tính hợp lệ của tất cả các biến nguyên thủy.
- Nếu có bất kỳ trường thông báo dữ liệu không hợp lệ nào, lập tức in thông báo lỗi rõ ràng ra console (Ví dụ: `"LỖI DỮ LIỆU: Độ tuổi khách hàng không hợp lệ!"`) và không thực hiện các bước phân loại phía sau.

Yêu cầu 2: Xác định thông tin Hạng hội viên với `switch-case`
Dựa vào biến `tierCode`, hãy xác định tên hạng (`tierName`) và tỷ lệ chiết khấu dịch vụ (`discountPercent`) tương ứng:
- Mã `1`: Tên hạng `"Standard"`, Chiết khấu `0%`
- Mã `2`: Tên hạng `"Silver"`, Chiết khấu `5%`
- Mã `3`: Tên hạng `"Gold"`, Chiết khấu `10%`
- Mã `4`: Tên hạng `"Platinum"`, Chiết khấu `15%`
- Nhánh `default`: Tên hạng `"Unassigned"`, Chiết khấu `0%`

Yêu cầu 3: Phân cấp độ ưu tiên chăm sóc CRM với `if / else-if / else`
Dựa vào các chỉ số kinh doanh, hãy xác định cấp độ ưu tiên chăm sóc (`priorityLevel`):
- Điều kiện rủi ro: Nếu `hasOverdueDebt === true` hoặc `creditScore < 500`, gán `priorityLevel = "Cần chú ý đặc biệt (Rủi ro cao)"`.
- Nếu không bị rủi ro, xét tiếp:
  - Nếu `annualRevenue >= 100000000` (100 triệu VNĐ) và `creditScore >= 750`: gán `priorityLevel = "Ưu tiên cao nhất (VIP)"`.
  - Nếu `annualRevenue >= 50000000` (50 triệu VNĐ) hoặc `creditScore >= 650`: gán `priorityLevel = "Ưu tiên trung bình"`.
  - Các trường hợp còn lại: gán `priorityLevel = "Ưu tiên tiêu chuẩn"`.

Yêu cầu 4: Đánh giá cấp duyệt hạn mức tín dụng bằng toán tử ba ngôi (Ternary Operator)
- Viết một biểu thức ba ngôi ngắn gọn kiểm tra điều kiện: Nếu `creditScore >= 700` và `hasOverdueDebt === false` thì gán `creditApproval = "Đã phê duyệt hạn mức đề xuất"`, ngược lại gán `creditApproval = "Yêu cầu thẩm định bổ sung"`.

Yêu cầu 5: In kết quả báo cáo CRM
Sử dụng Chuỗi Template Literals (backticks ``` `${...}` ```) để in báo cáo ra Console theo đúng định dạng mẫu bên dưới.

**Ví dụ đầu vào và đầu ra mẫu:**

*Kịch bản 1: Khách hàng hợp lệ - Phân loại VIP*
```javascript
// Mã nguồn khai báo đầu vào
const customerName = "Nguyen Van A";
const customerAge = 35;
const annualRevenue = 120000000;
const creditScore = 780;
const tierCode = 4;
const hasOverdueDebt = false;
```
```text
=== BÁO CÁO PHÂN LOẠI KHÁCH HÀNG CRM ===
Khách hàng: Nguyen Van A (35 tuổi)
Hạng hội viên: Platinum (Chiết khấu dịch vụ: 15%)
Điểm tín nhiệm: 780 | Tình trạng nợ quá hạn: Không
Phân cấp ưu tiên CRM: Ưu tiên cao nhất (VIP)
Trạng thái duyệt tín dụng: Đã phê duyệt hạn mức đề xuất
========================================
```

*Kịch bản 2: Dữ liệu không hợp lệ (Độ tuổi không thuộc khoảng 18 - 100)*
```javascript
const customerName = "Tran Van B";
const customerAge = 15;
const annualRevenue = 50000000;
const creditScore = 600;
const tierCode = 2;
const hasOverdueDebt = false;
```
```text
LỖI DỮ LIỆU: Độ tuổi khách hàng không hợp lệ (Phải từ 18 đến 100 tuổi).
```

*Kịch bản 3: Khách hàng có rủi ro nợ quá hạn*
```javascript
const customerName = "Le Thi C";
const customerAge = 42;
const annualRevenue = 200000000;
const creditScore = 450;
const tierCode = 3;
const hasOverdueDebt = true;
```
```text
=== BÁO CÁO PHÂN LOẠI KHÁCH HÀNG CRM ===
Khách hàng: Le Thi C (42 tuổi)
Hạng hội viên: Gold (Chiết khấu dịch vụ: 10%)
Điểm tín nhiệm: 450 | Tình trạng nợ quá hạn: Có
Phân cấp ưu tiên CRM: Cần chú ý đặc biệt (Rủi ro cao)
Trạng thái duyệt tín dụng: Yêu cầu thẩm định bổ sung
========================================
```

### **5. Yêu cầu nộp bài**
- Tạo một thư mục dự án đặt tên theo cấu trúc: `CRM_Validation_[HoTen_MaSinhVien]`.
- Lưu mã nguồn chính trong file `crm_classifier.js`.
- Thực hiện kiểm thử chương trình với ít nhất 3 kịch bản dữ liệu đầu vào khác nhau (Hợp lệ VIP, Không hợp lệ, Rủi ro tín dụng).
- Đẩy mã nguồn lên kho chứa GitHub cá nhân và nộp đường dẫn (URL) repository lên hệ thống quản lý học tập.
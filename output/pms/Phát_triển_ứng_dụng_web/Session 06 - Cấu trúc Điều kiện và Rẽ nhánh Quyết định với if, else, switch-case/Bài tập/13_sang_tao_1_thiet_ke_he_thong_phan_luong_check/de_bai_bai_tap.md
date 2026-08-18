#

# <center>[Sáng tạo 1] Thiết Kế Hệ Thống Phân Luồng Check-in và Tính Phí Hành Lý Hàng Không</center>

### **1. Mục tiêu**
*   **Tự chủ phân tích nghiệp vụ:** Tự định hình và thiết kế cấu trúc dữ liệu đầu vào / đầu ra (I/O Schema) cho bài toán làm thủ tục tự động (Kiosk Check-in) ngành hàng không.
*   **Vận dụng tổng hợp cấu trúc điều kiện:** Kết hợp linh hoạt `if-else if-else`, câu lệnh rẽ nhánh nhiều trường hợp `switch-case` và toán tử ba ngôi `? :` để giải quyết bài toán tính cước hành lý quá cân và phân luồng dịch vụ ưu tiên.
*   **Mô hình hóa quy trình:** Trực quan hóa toàn bộ logic nghiệp vụ bằng sơ đồ luồng dữ liệu (Data Flow Diagram) chuẩn Mermaid trước khi viết mã nguồn.
*   **Chủ động phát hiện bẫy lỗi:** Dự đoán các trường hợp lỗi dữ liệu biên (Edge Cases) phát sinh tại quầy check-in sân bay và viết mã nguồn ngăn chặn triệt để.

---

### **2. Bối cảnh & Vấn đề**
Hãng hàng không Vietjet / Vietnam Airlines đang triển khai nâng cấp hệ thống Kiosk Check-in tự động tại các sân bay quốc tế. Khi hành khách quét mã đặt chỗ (PNR) tại Kiosk, hệ thống cần tính toán lệ phí hành lý ký gửi quá cước, xác định luồng ưu tiên check-in (Lối đi ưu tiên Priority vs Lối đi Thường Standard), và đưa ra khuyến nghị dịch vụ bổ sung dựa trên 4 yếu tố chính:
1.  **Hạng vé hành khách:** Thương gia (Business), Linh hoạt (Deluxe), Phổ thông (Eco).
2.  **Hạng thẻ thành viên thân thiết:** Thường (Member), Bạc (Silver), Vàng (Gold), Bạch Kim (Platinum).
3.  **Tuyến bay:** Nội địa (Domestic), Đông Nam Á (Regional), Quốc tế đường dài (International).
4.  **Hành lý thực tế:** Trọng lượng hành lý ký gửi hành khách mang theo tại quầy (tính theo kg).

Hệ thống cũ đang gặp sự cố nghẽn logic do lồng ghép quá nhiều điều kiện phức tạp, dẫn đến tính sai phí quá cước cho khách hàng VIP và không phân loại chính xác lối đi ưu tiên. Bạn được giao nhiệm vụ thiết kế lại toàn bộ mô-đun rẽ nhánh quyết định này bằng ngôn ngữ JavaScript Vanilla.---

### **3. Quy tắc nghiệp vụ**
Hệ thống cần tuân thủ các nguyên lý phân luồng sau (Học viên tự cụ thể hóa các chỉ số cụ thể trong I/O Schema của mình):

1.  **Xử lý Đơn giá quá cước theo Tuyến bay (`switch-case`)**:
    *   Mỗi tuyến bay (Domestic, Regional, International) sẽ có một đơn giá phạt hành lý quá cân cơ bản trên mỗi kg vượt cước khác nhau.
    *   Bắt buộc dùng `switch-case` trên mã tuyến bay để xác định đơn giá cơ bản và thông báo tên tuyến bay tương ứng. Cần có trường hợp `default` cho mã tuyến bay không hợp lệ.

2.  **Tính Hạn mức Miễn phí & Phí phạt Hành lý (`if-else if-else`)**:
    *   Hạn mức miễn phí hành lý ký gửi ban đầu dựa vào Hạng vé (Business có hạn mức cao nhất, Eco thấp nhất).
    *   Hạng thẻ Platinum và Gold được cộng thêm hạn mức miễn phí thưởng (Ví dụ: Platinum được cộng thêm 10kg, Gold cộng 5kg).
    *   Nếu tổng trọng lượng hành lý ký gửi thực tế vượt quá hạn mức miễn phí cho phép: Tính số kg quá cước và nhân với đơn giá tuyến bay để ra tổng phí phạt quá cước. Nếu không vượt quá, phí phạt bằng 0.

3.  **Xác định Quyền ưu tiên & Gán nhãn dịch vụ (Toán tử Ba ngôi `? :`)**:
    *   **Quyền vào Lối đi Ưu tiên (Priority Pass):** Hành khách sở hữu hạng vé Business HOẶC có thẻ Platinum/Gold sẽ được dán nhãn `"Lối đi Ưu tiên (Priority Gate)"`, ngược lại là `"Lối đi Tiêu chuẩn (Standard Gate)"`.
    *   **Thông báo Trạng thái Phí:** Sử dụng toán tử ba ngôi để gán nhãn trạng thái thanh toán đơn giản: `"Hành lý hợp lệ - Miễn phí"` nếu phí bằng 0, hoặc `"Yêu cầu thanh toán cước vượt hạn mức"` nếu phát sinh phí phạt.

[WARNING] **Quy định kỹ thuật bắt buộc**:
*   Không được dùng các thư viện ngoài hoặc cú pháp JavaScript nâng cao chưa học (như mảng phức tạp, hàm nâng cao, async/await khi chưa học DOM/Fetch API nâng cao). Chỉ tập trung dùng `const`, `let`, `if-else`, `switch-case`, toán tử ba ngôi `? :` và các toán tử số học/logic cơ bản.
*   Tránh mắc bẫy "Anti-pattern": Tuyệt đối không lồng ghép quá 2 cấp toán tử ba ngôi (Nested Ternary) gây khó đọc mã nguồn.

---

### **4. Yêu cầu bài toán**
Học viên trình bày bài làm theo 4 phần chi tiết:

#### **Phần 1: Tự thiết kế I/O Schema**
*   Khai báo và mô tả đầy đủ danh sách các biến đầu vào (Inputs) như: `ticketClass`, `memberTier`, `flightRoute`, `actualBaggageWeight`...
*   Khai báo và mô tả danh sách các biến kết quả đầu ra (Outputs) như: `allowedFreeWeight`, `excessWeight`, `baggagePenaltyFee`, `priorityAccessStatus`, `billingMessage`...

#### **Phần 2: Phát hiện kịch bản lỗi biên (Edge Cases)**
Liệt kê tối thiểu 3 kịch bản bẫy lỗi dữ liệu thực tế và nêu rõ cách chương trình sẽ ứng xử. (Ví dụ: Trọng lượng hành lý nhập vào là số âm hoặc bằng 0, mã tuyến bay nhập sai không có trong danh mục hệ thống, hạng vé nhập ký tự thường/hoa không đồng nhất...).

#### **Phần 3: Sơ đồ luồng dữ liệu (Mermaid Flowchart)**
Vẽ sơ đồ luồng bằng Mermaid thể hiện toàn bộ chu trình xử lý từ tiếp nhận dữ liệu đầu vào -> phân nhánh `switch-case` tuyến bay -> tính toán `if-else` hạn mức & cước phí -> đánh giá toán tử ba ngôi gán nhãn ưu tiên -> xuất kết quả.
*Chú ý quy chuẩn shape:* Oval `([ ])` cho Bắt đầu/Kết thúc, Hình bình hành `[/ /]` cho Input/Output, Hình thoi `?` cho Điều kiện, Hình chữ nhật `[" "]` cho Tiến trình tính toán.

#### **Phần 4: Triển khai Mã nguồn JavaScript**
Viết toàn bộ mã nguồn xử lý bằng JavaScript Vanilla ES6+, có chú thích giải thích logic bằng Tiếng Việt rõ ràng và in kết quả đầy đủ ra console bằng `console.log()`.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai trong tập tin mã nguồn.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex13`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex13`
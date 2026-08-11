# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Dựa vào kịch bản hệ thống thương mại điện tử phục vụ 50.000 người dùng hàng ngày được mô tả trong bài đọc, hãy chỉ ra hai nguyên nhân kỹ thuật cụ thể dẫn đến hiện tượng vỡ layout trên thiết bị di động (dưới 768px) và làm gia tăng 60% thời gian bảo trì mã nguồn. Hệ quả của những tồn đọng này đối với quá trình phát triển nhóm là gì?
> **Gợi ý trả lời & Định hướng đáp án:** Đáp án cần trích xuất chính xác từ bài đọc:
1. Vỡ layout di động (< 768px): Do lập trình viên viết mã CSS cứng cố định pixel.
2. Tăng 60% thời gian bảo trì: Do cấu trúc mã nguồn gom chung trong một tập tin duy nhất và đặt tên biến không rõ nghĩa.
3. Hệ quả phát triển nhóm: Thiếu quy chuẩn đánh giá mã nguồn dẫn đến việc phát sinh nhiều lỗi trùng lặp khi tích hợp làm việc nhóm.

---

### Câu 2: Theo sơ đồ kiến trúc thư mục mã nguồn chuẩn doanh nghiệp trong bài đọc, các tập tin `ProductCard.js`, `productService.js` và `formatCurrency.js` phải được sắp xếp vào những thư mục con cụ thể nào thuộc thư mục `src/`? Hãy giải thích rõ vai trò nhiệm vụ của từng thư mục con đó.
> **Gợi ý trả lời & Định hướng đáp án:** Đáp án dựa trên sơ đồ và phân tích cơ chế trong bài đọc:
1. Tập tin `ProductCard.js` nằm trong thư mục `src/components/`: Có nhiệm vụ quản lý và lưu trữ các thành phần giao diện (UI) tái sử dụng (như nút bấm, thẻ hiển thị sản phẩm).
2. Tập tin `productService.js` nằm trong thư mục `src/services/`: Có nhiệm vụ quản lý các hàm xử lý logic và gọi ứng dụng giao diện dữ liệu (API / kết nối dữ liệu).
3. Tập tin `formatCurrency.js` nằm trong thư mục `src/utils/`: Có nhiệm vụ lưu trữ các hàm tiện ích dùng chung (định dạng tiền tệ, xử lý điểm ngắt màn hình).

---

### Câu 3: Dựa trên mô hình kỳ vọng sản phẩm Web Responsive trong bài đọc, hãy so sánh sự khác biệt về cấu trúc hiển thị cột giữa Desktop Viewport (1440px) và Mobile Viewport (375px). Mục tiêu của việc điều chỉnh này là để khắc phục sự cố gì?
> **Gợi ý trả lời & Định hướng đáp án:** Đáp án cần nêu rõ:
1. Desktop Viewport (1440px): Sử dụng cấu trúc layout 4 cột (4 Columns), tạo giao diện đa cột tự điều chỉnh linh hoạt.
2. Mobile Viewport (375px): Sử dụng cấu trúc layout 1 cột (1 Column Layout), giúp tối ưu trải nghiệm cảm ứng trên màn hình nhỏ.
3. Mục tiêu: Khắc phục triệt để sự cố vỡ layout trên thiết bị di động (màn hình dưới 768px) do cố định pixel, đảm bảo đạt chuẩn trải nghiệm trên mọi kích thước màn hình.

---

### Câu 4: Để xử lý triệt để bẫy lỗi (Gotcha) phát sinh lỗi trùng lặp khi tích hợp mã nguồn trong làm việc nhóm, giải pháp chuẩn doanh nghiệp được đề xuất trong bài đọc bao gồm những trụ cột nào? Hãy phân tích vai trò của bước kiểm duyệt cuối cùng trước khi đóng gói sản phẩm.
> **Gợi ý trả lời & Định hướng đáp án:** Đáp án gồm các ý chính từ bài đọc:
1. Các trụ cột giải pháp chuẩn doanh nghiệp:
- Áp dụng kiến trúc thư mục mô-đun hóa (`src/components`, `src/services`, `src/utils`).
- Xây dựng hệ thống Web Responsive dựa trên các điểm ngắt Breakpoints (375px, 768px, 1440px).
- Thiết lập luồng kiểm duyệt chất lượng mã nguồn (Code Review Pipeline) nghiêm ngặt.
2. Vai trò của luồng kiểm duyệt (Code Review Pipeline): Đảm bảo mã nguồn tuân thủ quy chuẩn, ngăn chặn các lỗi trùng lặp phát sinh khi hợp nhất mã nguồn của các thành viên trong nhóm trước khi đóng gói sản phẩm.

---
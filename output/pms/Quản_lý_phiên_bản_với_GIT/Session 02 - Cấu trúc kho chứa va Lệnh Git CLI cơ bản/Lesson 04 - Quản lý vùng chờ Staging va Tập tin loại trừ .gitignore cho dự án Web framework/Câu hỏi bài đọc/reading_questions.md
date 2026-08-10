# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Dựa vào kịch bản thực tế của dự án Web Framework (React/Vue/Node.js) được trình bày trong bài đọc, hãy phân tích rủi ro bảo mật và rủi ro về hiệu năng hệ thống khi không sử dụng tệp `.gitignore`. Đồng thời, từ mô hình sơ đồ Working Directory chuyển sang Staging Area, hãy chỉ ra cụ thể danh sách tệp/thư mục nào bị loại bỏ và danh sách tệp nào được phép nạp vào Staging Area.
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải chi tiết cần trình bày đủ các điểm sau dựa trên bài đọc:
1. Rủi ro bảo mật: Tệp `.env` chứa các tham số cấu hình nhạy cảm và mã khóa bí mật (`DATABASE_URL`, `JWT_SECRET`) bị đưa nhầm vào hệ thống quản lý phiên bản, làm rò rỉ dữ liệu bảo mật của doanh nghiệp.
2. Rủi ro hiệu năng: Đóng gói và lưu trữ hàng ngàn tệp phụ thuộc nặng nề trong thư mục `node_modules/` (dung lượng hơn 500MB) cùng các tệp biên dịch tạm (`dist/`, `build/`).
3. Phân loại theo sơ đồ:
- Danh sách bị bộ lọc `.gitignore` loại bỏ: `.env`, `node_modules/`, `dist/`.
- Danh sách tệp an toàn được chuyển sang Staging Area: `src/App.jsx` và `package.json`.

---

### Câu 2: Dựa vào phần sơ đồ giải mã cú pháp cấu hình `.gitignore`, hãy so sánh chi tiết sự khác biệt về cơ chế tác động giữa quy tắc `/build` (có dấu gạch chéo ở đầu) và quy tắc `node_modules/` (có dấu gạch chéo ở cuối). Nếu trong cấu trúc dự án thực tế có thư mục `/src/build`, quy tắc `/build` có loại bỏ thư mục này không? Giải thích rõ nguyên lý.
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải chi tiết cần phân tích đúng theo bài đọc:
1. Quy tắc `/build`: Dấu gạch chéo `/` ở đầu có tác dụng neo vị trí kiểm tra ngay tại thư mục gốc của dự án. Quy tắc này chỉ loại trừ thư mục `build` nằm trực tiếp ở thư mục gốc.
2. Do cơ chế neo ở thư mục gốc, quy tắc `/build` KHÔNG loại bỏ thư mục `/src/build` vì thư mục này nằm bên trong thư mục con `src/`.
3. Quy tắc `node_modules/`: Dấu gạch chéo `/` ở cuối bắt buộc đối tượng bị loại trừ phải là thư mục. Cơ chế này sẽ tự động loại bỏ tất cả các thư mục có tên `node_modules` ở mọi cấp thư mục (mọi vị trí lồng nhau) trong dự án.

---

### Câu 3: Trong bài đọc có phân tích các ký tự đại diện khớp mẫu bao gồm `*` và `!`. Giả sử dự án khai báo quy tắc lọc gồm các dòng:
- `.env*.local`
- `*.log`
- `!important.log`

Hãy giải thích cơ chế hoạt động của bộ lọc trên đối với các tệp sau trong làm việc: `.env.development.local`, `.env.production.local`, `system.log`, và `important.log`. Tệp nào sẽ bị loại trừ và tệp nào được phép đưa vào Staging Area?
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải chi tiết cần làm rõ cơ chế khớp mẫu và thứ tự từ trên xuống dưới:
1. Tệp `.env.development.local` và `.env.production.local`: Bị loại bỏ bởi quy tắc `.env*.local`. Ký tự đại diện `*` khớp với chuỗi bất kỳ (`development` hoặc `production`) nằm giữa tiền tố `.env.` và hậu tố `.local`.
2. Tệp `system.log`: Bị loại bỏ bởi quy tắc `*.log` (khớp với mọi tệp có phần mở rộng là `.log`).
3. Tệp `important.log`: Mặc dù khớp với quy tắc `*.log`, nhưng do có quy tắc phủ định `!important.log` (sử dụng dấu chấm cảm `!`), quy tắc loại trừ bị hủy bỏ đối với tệp này.
4. Kết luận: Các tệp bị loại trừ gồm `.env.development.local`, `.env.production.local`, và `system.log`. Tệp duy nhất được giữ lại để đưa vào Staging Area là `important.log`.

---

### Câu 4: Phân tích vai trò của kiến trúc vùng đệm Staging Area trong quy trình làm việc với mã nguồn. Ngoài ra, dựa trên phân tích cú pháp ký tự `**` trong bài đọc (ví dụ: `src/**/temp`), hãy giải thích cách quy tắc này xử lý nếu dự án xuất hiện các đường dẫn: `src/temp`, `src/components/temp`, và `src/modules/auth/temp`.
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải chi tiết cần đạt các ý:
1. Vai trò của Staging Area: Là vùng đệm trung gian giữ nhiệm vụ ghi nhận trạng thái các tệp tin được lựa chọn trước khi lưu trữ chính thức. Giúp người phát triển chủ động rà soát, chọn lọc chính xác các thay đổi cần đưa vào phiên bản mới thay vì nạp toàn bộ Working Directory.
2. Cơ chế của ký tự `**`: Ký tự `**` đại diện cho khả năng khớp với các thư mục lồng nhau nhiều cấp (bao gồm cả 0 cấp, 1 cấp hoặc nhiều cấp thư mục trung gian).
3. Tác động tới các đường dẫn:
- `src/temp`: Khớp (0 cấp trung gian).
- `src/components/temp`: Khớp (1 cấp trung gian là `components`).
- `src/modules/auth/temp`: Khớp (2 cấp lồng nhau là `modules/auth`).
-> Quy tắc `src/**/temp` sẽ loại bỏ tất cả 3 thư mục `temp` nằm trong cả 3 đường dẫn nêu trên.

---
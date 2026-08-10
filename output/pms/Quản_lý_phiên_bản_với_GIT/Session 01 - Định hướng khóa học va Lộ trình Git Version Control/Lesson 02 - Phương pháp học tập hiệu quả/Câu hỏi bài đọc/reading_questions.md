# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Dựa vào kịch bản thực tế và sơ đồ so sánh phương pháp học tập trong bài đọc, hãy phân tích sự khác biệt rõ rệt giữa 'Phương pháp học tập thụ động' và 'Phương pháp chủ động kết hợp AI'. Cụ thể, con số lãng phí từ 4 đến 5 giờ trong vận hành cũ được giải quyết triệt để như thế nào thông qua việc kết hợp Quy tắc 15 phút và mô hình Prompt RCTC?
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải cần thể hiện được các điểm sau từ bài đọc:
1. Phương pháp thụ động: Lập trình viên tốn 4 đến 5 giờ đọc tài liệu lan man, tìm từ khóa ngẫu nhiên khi gặp lỗi, gây quá tải cho Senior Developer và sa lầy vào lỗi cả ngày.
2. Phương pháp chủ động + AI: Rút ngắn thời gian tra cứu và cô đọng kiến thức nhờ đặt câu hỏi theo mô hình RCTC (Role - Context - Task - Constraint) trên ChatGPT/Claude.
3. Sự kết hợp với Quy tắc 15 phút: Giới hạn tự tra cứu và hỏi AI tối đa trong 15 phút. Nếu chưa giải quyết được thì tổng hợp thông tin đã tra cứu để thảo luận với nhóm, tránh làm phiền đồng nghiệp liên tục và tối ưu hóa thời gian vận hành.

---

### Câu 2: Trong sơ đồ luồng Mermaid về vòng đời tự học và xử lý sự cố, khi bước 'Đánh giá câu trả lời của AI' trả về kết quả 'Kết quả chung chung / Sai', người học phải thực hiện hành động cụ thể nào trước khi gửi lại truy vấn? Ngược lại, nếu đạt 'Kết quả chính xác & Rõ ràng', quy trình sẽ tiếp tục qua những bước xử lý nào tiếp theo?
> **Gợi ý trả lời & Định hướng đáp án:** Đáp án cần trích dẫn chính xác các bước trong sơ đồ Mermaid:
1. Khi kết quả chung chung hoặc sai: Người học đi theo nhánh rẽ quay lại bước 'Bổ sung Bối cảnh & Ràng buộc' (cung cấp thêm thông tin bối cảnh lỗi hoặc giới hạn lại câu trả lời) rồi mới tiến hành gửi lại truy vấn tới AI.
2. Khi kết quả chính xác & rõ ràng: Người học chuyển sang bước 'Lưu trữ vào Knowledge Base' (cơ sở dữ liệu tri thức cá nhân) và sau đó chuyển sang bước cuối cùng là 'Áp dụng thực hành & Kiểm chứng'.

---

### Câu 3: Hãy phân tích đoạn mẫu Prompt chuẩn RCTC được trích dẫn ở Bước 3 & Bước 4 trong bài đọc:
`[Role]: Đóng vai một Trợ lý Giảng dạy (Teaching Assistant) chuyên nghiệp.`
`[Context]: Tôi là sinh viên mới bắt đầu khóa học lập trình, đang đọc tài liệu định hướng môn học.`
`[Task]: Hãy tóm tắt 3 mục tiêu quan trọng nhất của bài học và giải thích thuật ngữ 'Chủ động tự học'.`
`[Constraint]: Trình bày bằng Tiếng Việt, sử dụng danh sách gạch đầu dòng, ngôn từ ngắn gọn và không quá 200 từ.`

Chỉ ra vai trò của từng dòng lệnh trong việc định hướng AI và giải thích lý do tại sao nếu thiếu thành phần [Constraint], phản hồi của AI có thể làm gián đoạn tiến độ tự học.
> **Gợi ý trả lời & Định hướng đáp án:** Câu trả lời cần chi tiết các ý:
1. Phân tích 4 thành phần trong prompt mẫu:
- [Role]: Trợ lý Giảng dạy chuyên nghiệp -> Giúp AI xác định chuyên môn và văn phong sư phạm phù hợp.
- [Context]: Sinh viên mới bắt đầu khóa học -> Cung cấp góc nhìn người học nhập môn để AI dùng từ ngữ dễ hiểu.
- [Task]: Tóm tắt 3 mục tiêu & giải thích thuật ngữ 'Chủ động tự học' -> Xác định chính xác hành động và mục tiêu cần output.
- [Constraint]: Tiếng Việt, gạch đầu dòng, không quá 200 từ -> Giới hạn khuôn mẫu đầu ra rõ ràng.
2. Tác hại khi thiếu [Constraint]: Theo bài đọc, nếu không có ràng buộc, AI có thể trả về câu trả lời quá dài, lan man, phức tạp hoặc không đúng định dạng mong muốn, khiến người học tốn thời gian đọc lại và phải thực hiện tinh chỉnh nhiều lần (Iterative Refinement).

---

### Câu 4: Trong 'Quy Trình 4 Bước Áp Dụng Prompt Engineering', Bước 4 quy định cụ thể hành động của lập trình viên trong và sau 'Quy tắc 15 phút'. Hãy mô tả chi tiết lập trình viên cần thực hiện công việc gì trong 15 phút đầu tiên, và hành động chuẩn xác bắt buộc phải làm ngay sau khi hết 15 phút mà sự cố vẫn chưa được giải quyết để tránh vi phạm các tắc nghẽn vận hành đã nêu?
> **Gợi ý trả lời & Định hướng đáp án:** Gợi ý đáp án cần bám sát Bước 4 của quy trình:
1. Trong 15 phút đầu tiên: Lập trình viên tự mình tập trung tra cứu thông tin, thu thập thông báo lỗi console và đặt câu hỏi cho AI (ChatGPT/Claude) bằng câu lệnh Prompt chuẩn RCTC để tìm nguyên nhân và cách khắc phục.
2. Ngay sau khi hết 15 phút mà chưa giải quyết được: Không được tiếp tục sa lầy một mình cả ngày. Lập trình viên phải dừng lại, tổng hợp lại toàn bộ thông tin bối cảnh lỗi và các câu trả lời/phương án đã thử nghiệm từ AI, sau đó mang thông tin đã tổng hợp này đi thảo luận với Senior Developer hoặc nhóm làm việc để nhận sự hỗ trợ.

---
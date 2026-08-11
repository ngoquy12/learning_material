# 🤖 BÁO CÁO AI REVIEW REPORT — RE AI DAY
### Dự án: Hệ Thống Tự Động Sản Xuất Học Liệu Bằng AI (E-Learning Content Factory)

---

## 1. Thông tin chung
* **Phòng ban:** Phòng Đào tạo & Nghiên cứu Phát triển Công nghệ AI (Rikkei Education)
* **Người trình bày:** Đội ngũ Dự án AI Elearning
* **Thời gian báo cáo:** Tháng 08/2026

---

## 2. Bối cảnh
- **Vấn đề hoặc nhu cầu thực tế của phòng ban:**
  - **Biên soạn học liệu truyền thống tốn nhiều thời gian và chi phí:** Để tạo ra trọn bộ tài liệu học tập đầy đủ cho 1 môn học (gồm bài đọc lý thuyết, slide bài giảng, bài tập thực hành và đề thi trắc nghiệm), đội ngũ giảng viên và chuyên gia phải mất trung bình **1 tháng làm việc** (khoảng 160 - 200 giờ thủ công).
  - **Chất lượng chưa đồng đều giữa các giảng viên:** Mỗi giảng viên có cách soạn bài khác nhau: người làm quá dài, người làm quá ngắn, hình ảnh chưa đẹp mắt, câu hỏi trắc nghiệm dễ tra Google hoặc nội dung bài giảng chưa thu hút học viên.
  - **Bài học khô khan, thiếu tính tương tác:** Tài liệu truyền thống chủ yếu là file Word/PDF tĩnh, học viên đọc xong khó hình dung bài tập chạy thực tế như thế nào.
- **Vì sao lựa chọn ứng dụng AI cho bài toán này?:**
  - **Tự động hóa từ A đến Z:** AI có thể đọc chương trình khung của khóa học và tự động tạo ra trọn bộ tài nguyên học tập đa dạng chỉ trong vài phút.
  - **Đảm bảo chuẩn mực chất lượng:** Trí tuệ nhân tạo làm việc theo bộ quy chuẩn sư phạm nghiêm ngặt, đảm bảo mọi bài học đều đạt tính thẩm mỹ cao, dễ hiểu và chuyên nghiệp.
  - **Giải phóng sức lao động cho chuyên gia:** Giảm hơn 98% thời gian soạn bài, giúp giảng viên tập trung vào việc giảng dạy và hỗ trợ học viên thay vì phải gõ từng trang tài liệu.

---

## 3. Giải pháp AI
- **Công cụ AI đã sử dụng:**
  - **Mô hình trí tuệ nhân tạo thế hệ mới (LLMs):** Sử dụng các mô hình AI tiên tiến nhất hiện nay (Gemini 3.6 Flash, Gemini 3 Flash, OpenAI) có khả năng đọc hiểu, tư duy sư phạm và tạo nội dung tiếng Việt tự nhiên chuẩn xác.
  - **Bộ mô phỏng thực hành trực tuyến (Live Code Sandbox & Interactive Visualizer):** Công nghệ nhúng trình chạy thử nghiệm trực tiếp trên bài đọc website, giúp học viên thao tác và thấy kết quả ngay mà không cần cài đặt phần mềm phức tạp.
  - **Hệ thống lưu trữ & Bộ nhớ thông minh (Semantic Cache & State Store):** Giúp ghi nhớ các nội dung đã xử lý, loại bỏ trùng lặp và tiết kiệm chi phí tối đa.
- **Cách triển khai (quy trình, prompt, workflow...):**
  - **Động cơ điều phối luồng công việc Antigravity (Antigravity Asynchronous DAG Engine):**
    - Hệ thống điều phối các trợ lý AI làm việc song song qua 4 bước tự động khép kín:
      1. *AI Kiến trúc sư:* Đọc file đề cương `syllabus.json`, lập đồ thị phụ thuộc bài học và tính toán giới hạn phạm vi kiến thức để tránh rò rỉ bài sau.
      2. *AI Biên tập Học liệu:* Tự động viết Bài đọc chuẩn sư phạm (tích hợp live sandbox), làm Slide bài giảng 16:9 modern, tạo Bài tập thực hành 6 cấp độ Bloom và đề thi trắc nghiệm Anti-Google.
      3. *Bộ Kiểm định Chất lượng Tự động:* Quét tự động bằng mã Python (Regex & AST) để loại bỏ lỗi format, lỗi cú pháp và từ khóa cấm rườm rà.
      4. *Đóng gói Xuất bản:* Đóng gói dữ liệu ra file HTML, Markdown, JSON và zip SCORM 1.2 nạp thẳng lên LMS.
  - **Thiết lập bộ quy chuẩn Prompt cố định (`.agents/AGENTS.md`):**
    - Quy định cụ thể: Slide 16:9 modern, Typography 3-30-300 (tối đa 3 ý/slide), không icon rườm rà; Bài đọc 100% tiếng Việt ngắt ý bullet scannable; Bài tập gắn với bài toán doanh nghiệp.
  - **Các câu lệnh CLI thực thi trực tiếp:**
    - Tạo trọn bộ học liệu môn học:
      ```bash
      python main.py --syllabus "path/to/syllabus.json" --output "output/PM_Python"
      ```
    - Tạo tùy chọn loại học liệu (Bài đọc & Slide hoặc Bài tập & Quizz):
      ```bash
      python main.py --syllabus "path/to/syllabus.json" --types reading,slide
      python main.py --syllabus "path/to/syllabus.json" --types exercise,quiz
      ```
- **Vai trò của AI trong quy trình làm việc:**
  - **Tự động hóa 90 - 95% khối lượng công việc sản xuất:** AI đóng vai trò là "lực lượng sản xuất chính" - đảm nhận từ khâu thiết kế khung bài học, viết bài đọc, làm slide đến tạo câu hỏi trắc nghiệm và bài tập thực hành.
  - **Đảm bảo tính đồng bộ:** AI hoạt động 24/7 không biết mệt mỏi và luôn tuân thủ theo bộ quy chuẩn chất lượng của công ty, khắc phục hoàn toàn tình trạng chất lượng trập trùng giữa các giảng viên.
  - **Tối ưu hóa vai trò của Con người:** Giảng viên không còn phải gõ từng trang tài liệu thủ công. Họ chuyển sang đóng vai trò là "Người thẩm định & Đẩy nút xuất bản" (Reviewer & Approver), tập trung thời gian nâng cao chất lượng giảng dạy và tương tác với học viên.

---

## 4. Kết quả đạt được
- **Những thay đổi sau khi ứng dụng AI:**
  - **Chuẩn hóa 100% hình thức & nội dung:** Mọi bài đọc đều ngắn gọn, trình bày thoáng mắt, slide đẹp hiện đại, bài tập bám sát thực tế doanh nghiệp.
  - **Học viên tương tác trực tiếp:** Bài đọc được tích hợp khung chạy bài tập minh họa ngay trên trang web, học viên bấm nút là thấy ngay kết quả hoạt động mà không cần cài phần mềm phức tạp.
- **Hiệu quả về thời gian, chất lượng, chi phí hoặc năng suất (Số liệu thực tế từ hệ thống):**
  - **Khối lượng sản phẩm đã sản xuất thành công:**
    - Tạo ra **hơn 602 tệp học liệu hoàn chỉnh** phục vụ cho nhiều môn học khác nhau (Python, Git, Thiết kế Web...).
    - Chi tiết bao gồm: **215 bài tập thực hành & đề án**, **184 bộ dữ liệu chuẩn**, **94 bài đọc và trang slide bài giảng**, **69 hình ảnh minh họa bài học**, **31 bộ ngân hàng đề thi trắc nghiệm**.
  - **Khối lượng công việc AI đã gánh vác:**
    - Thực hiện **hơn 6,400 lượt xử lý công việc tự động**.
    - Đã xử lý **hơn 62 triệu lượt từ ngữ và thông tin** từ AI.
    - Tổng thời gian AI làm việc liên tục: **hơn 31 giờ tự động hoàn toàn**.
  - **Tiết kiệm thời gian & Chi phí cho công ty (So sánh bài toán 1 môn học):**
    - **Trước đây (Soạn thủ công):** Để hoàn thiện 1 môn học (gồm bài đọc SSOT, slide bài giảng, bài tập 6 cấp độ Bloom và ngân hàng trắc nghiệm), 1 giảng viên/chuyên gia phải làm việc liên tục trong **1 tháng** (khoảng 160 - 200 giờ).
    - **Hiện tại (Ứng dụng AI Antigravity):** Hệ thống AI tự động tạo trọn bộ học liệu cho 1 môn học chỉ mất **khoảng 15 - 30 phút chạy tự động** (cộng thêm 1 - 2 giờ kiểm tra/duyệt nội dung của giảng viên).
    - **Hiệu quả:** Rút ngắn thời gian sản xuất từ **1 tháng xuống còn dưới 2 giờ tổng cộng** (tiết kiệm **trên 98% thời gian**).
- **Minh chứng (hình ảnh, video, sản phẩm, dashboard...):**
  - **Màn hình theo dõi tiến độ & chi phí AI (`token_dashboard.html`):** Giúp quản lý theo dõi AI đang làm việc đến đâu, tốn bao nhiêu chi phí theo thời gian thực.
  - **Sơ đồ bài học trực quan (`graph_view.html`):** Giúp giảng viên bao quát toàn bộ lộ trình khóa học chỉ trên một trang màn hình.
  - **Kho học liệu đa dạng:** File bài đọc trên website tích hợp công cụ chạy code trực tiếp và ngân hàng bài tập, câu hỏi và đề thi trắc nghiệm hoàn chỉnh.

---

## 5. Bài học kinh nghiệm
- **Điều gì đã làm tốt?:**
  - **Phân công công việc rõ ràng cho từng AI:** Mỗi AI làm đúng 1 nhiệm vụ chuyên môn (AI viết bài riêng, AI làm slide riêng, AI tạo bài tập riêng) nên sản phẩm đầu ra rất chất lượng.
  - **Đưa ra quy tắc rõ ràng cho AI:** Đặt ra các tiêu chuẩn cụ thể như "Slide tối đa 3 ý, phông chữ to rõ, không dùng từ ngữ rườm rà" giúp AI làm việc chính xác ngay từ đầu.
  - **Antigravity điều phối hiệu quả:** Giúp tự động kết hợp các phần việc của nhiều AI mà không lo bị trùng lặp hay ghi đè nội dung.
- **Khó khăn gặp phải (Của bản thân & Đội ngũ thực hiện):**
  - **Thiếu kinh nghiệm ban đầu trong việc "giao việc" (Prompting) chuẩn xác cho AI:** Thời gian đầu, bản thân và đội ngũ chưa biết cách viết câu lệnh cho AI hiệu quả, yêu cầu còn chung chung nên AI tạo ra sản phẩm không như ý. Đội ngũ phải mất nhiều tuần tự mày mò, thử sai liên tục để đúc kết thành bộ quy chuẩn chuẩn mực.
  - **Áp lực bị "ngợp" khi phải kiểm soát & rà soát khối lượng học liệu khổng lồ:** Khi AI tạo ra hàng trăm tệp tài liệu cùng lúc chỉ trong vài phút, đội ngũ gặp khó khăn trong việc kiểm tra, rà soát thủ công từng bài đọc, slide và câu hỏi trắc nghiệm để đảm bảo không bị sai sót kiến thức.
  - **Thách thức trong việc thay đổi tư duy và thói quen làm việc cũ:** Đội ngũ phải trải qua quá trình thích nghi từ thói quen "tự tay ngồi gõ từng trang slide/bài đọc" sang tư duy mới: "thiết kế luật cho AI làm và kiểm định kết quả".
- **Kinh nghiệm hoặc lưu ý khi áp dụng AI:**
  - **Đưa yêu cầu (Prompt) cực kỳ cụ thể thay vì chung chung:** Thay vì bảo AI "làm cho tôi một báo cáo đẹp", hãy ghi rõ tiêu chuẩn "Báo cáo gồm 3 phần, ngắn gọn, có số liệu minh họa và bảng so sánh".
  - **Luôn giữ vai trò kiểm soát của con người (Human-in-the-loop):** AI là trợ lý đắc lực giúp làm 95% công việc, nhưng bản thân chúng ta vẫn phải là người rà soát cuối cùng để đảm bảo tính chính xác và chịu trách nhiệm về chất lượng sản phẩm.

---

## 6. Đề xuất
- **Hướng cải tiến trong thời gian tới:**
  - **Nâng cấp tính năng AI tự sửa lỗi:** Khi phát hiện bài viết hoặc bài tập có lỗi nhỏ, AI sẽ tự động phát hiện và sửa lại ngay mà không cần con người nhắc nhở.
  - **Xây dựng trang web bấm nút đơn giản cho Giảng viên:** Giảng viên chỉ cần tải lên file đề cương và bấm 1 nút là hệ thống tự trả về toàn bộ học liệu.
- **Cơ hội mở rộng hoặc nhân rộng cho các phòng ban khác:**
  - **Ứng dụng cho mọi chương trình đào tạo của Rikkei Education:** Nhân rộng mô hình cho tất cả các môn học khác (Lập trình Mobile, Phân tích dữ liệu, Quản lý dự án, Kiểm thử phần mềm...).
  - **Đóng gói thành giải pháp chuyển giao cho đối tác:** Đóng gói công nghệ này thành một sản phẩm dịch vụ để cung cấp cho các Trường Đại học và Doanh nghiệp có nhu cầu tự động hóa tài liệu đào tạo nội bộ.

---

# Project Rules - Rikkei Education Learning Material Standards

## Bắt đầu mỗi cuộc trò chuyện

1. Đọc `docs/PROJECT_STATE.md` trước tiên. Không phân tích lại toàn bộ dự án.
2. Nếu người dùng không chỉ định việc gì, tiếp tục việc đầu tiên ở mục "Việc tiếp theo" trong tệp đó.
3. Cuối mỗi lượt làm việc, cập nhật `docs/PROJECT_STATE.md` (việc đã xong, đang dở, quyết định mới). Workflow: `/resume`, `/handoff`.
4. Chi tiết (kích thước, lớp CSS, danh sách cấm đầy đủ): `docs/quy_chuan_chi_tiet.md`, chỉ mở khi cần.

## Phạm vi và ngôn ngữ

- Repo phục vụ nhiều môn (web/HTML/CSS, JavaScript, Python, C, Git, Agile, thiết kế...). KHÔNG mặc định Python. Chọn công cụ theo bản chất môn: môn lập trình chạy được dùng sandbox chạy mã trong trình duyệt (JS, Pyodide cho Python, SQL...); môn khái niệm/công cụ/quy trình (Git, CLI, Agile, kiến trúc, UML) dùng khối lệnh tĩnh, sơ đồ, bảng so sánh, KHÔNG dùng sandbox giả.
- Chỉ dẫn agent và system prompt viết bằng tiếng Anh. Mọi sản phẩm đầu ra (bài đọc, bài tập, slide, câu hỏi, kịch bản, comment mã, nhãn giao diện, rubric) 100% tiếng Việt có dấu.

## 0. Nguyên tắc bắt buộc

1. **Bài đọc 5 mục cố định** (`section-1` đến `section-5`):
   - Mục 1, Bài toán thực tế: tiêu đề do LLM sinh theo bài, nêu vấn đề cụ thể. Cấm tiêu đề chung như "Giới thiệu" hoặc chép nguyên tên bài. Tiêu đề tổng quát.
   - Mục 2, Cú pháp và cơ chế: tiêu đề nêu kiến thức kỹ thuật cụ thể. Bài lập trình/cú pháp: mỗi mục con (2.1, 2.2...) có khối chạy thử hoặc minh họa cú pháp ngay bên dưới. Bài khái niệm/công cụ/quy trình: không sandbox rỗng; dùng sơ đồ SVG/Mermaid, bảng so sánh, khối lệnh.
   - Mục 3, Ví dụ tăng dần: tối thiểu 3 ví dụ (3.1 đơn giản, 3.2 nghiệp vụ, 3.3 doanh nghiệp), mỗi ví dụ có `<h3>` đánh số, khung yêu cầu và mã đầy đủ.
   - Mục 4, Lỗi thường gặp và cách tránh: lỗi phổ biến, khi nào nên và không nên dùng (ma trận quyết định).
   - Mục 5, Tóm tắt và tự kiểm tra tương tác 1 trang (nút "Kiểm tra đáp án").
2. **15-Minute Micro-Learning**: 15 phút đọc (giới hạn cứng), 1.500-2.000 từ kể cả mã, nội dung trọng tâm vào một vấn đề chính. Gọn, dễ quét, nhiều hình; cấm tường chữ.
3. **Problem-First**: cấm mở đầu bằng định nghĩa trừu tượng. Trình tự: tình huống thực tế, nỗi đau nghiệp vụ, hạn chế cách cũ, rồi mới khái niệm mới.
4. **Giàu hình ảnh**: bắt buộc có sơ đồ Mermaid, ảnh 16:9, visualizer khi phù hợp; không chỉ có chữ.
   - Mermaid dùng đúng 5 hình: Bắt đầu/Kết thúc `([...])`; Vào/Ra `[/.../]`; Quyết định `{"..."}`; Xử lý `["..."]`; Mũi tên `-->` hoặc `-->|Đúng|`/`-->|Sai|`. Cấm dùng hình bình hành cho hành động/tính toán.
   - Ảnh: vector phẳng 2D, tối giản, bảng màu doanh nghiệp (navy `#0f172a`, xám slate, xanh lục nhạt). Không chèn banner tiêu đề trong ảnh (tiêu đề thuộc `<h2>` và chú thích "Hình 1.1"). Nhãn trong ảnh 100% tiếng Việt có dấu, không trộn thuật ngữ Anh (biểu thức mã giữ nguyên cú pháp). Bố cục 3 lớp (ngữ cảnh, biến đổi dữ liệu, kết quả); cấm 3D, neon, cyberpunk.
5. **Câu hỏi theo tình huống**: không hỏi học thuộc; 100% câu hỏi nhắm vào tình huống nghiệp vụ, ứng dụng thực tế.
6. **Câu hỏi bài đọc chống tìm tắt** (`reading_questions.md`, self_test): kiểm tra người học thật sự đã đọc. Cấm câu hỏi giáo khoa chung ("Git là gì?"). Mỗi câu gắn với dữ liệu, mã, con số, trình tự, lỗi hoặc tham số tình huống riêng của chính bài đó, để tìm kiếm hay AI chung không trả lời được.
7. **Tự kiểm tra nhúng 1 trang** cuối bài đọc, một nút kiểm tra.
8. **Mindmap**: ít chữ, nhiều biểu tượng, cô đọng; cấm biến thành bài đọc thu nhỏ.
9. **Video**: AI tạo kịch bản (khung 5 lớp cảnh), mã, sơ đồ 2D, tài nguyên demo; giảng viên thật quay hình, live coding, giải thích.
10. **Chất lượng như người viết**: rõ, đủ, trực quan, thực tế, có chuẩn đầu ra đo lường được (động từ Bloom đo lường được, không "hiểu", "ghi nhớ").
    - Cấm "bẫy", "gotcha", "anti-pattern". Dùng "Lỗi thường gặp", "Sai sót phổ biến", "Ngoại lệ cần lưu ý".
    - Cấm "khám phá", "tìm hiểu ngay", "bí kíp", "tất tần tật", "thần thánh", "tuyệt vời", "bậc nhất", "vô cùng", "viên ngọc", "triệt để".
11. **Chỉ Light Mode**: khung chứa, thẻ mã, callout, sidebar dùng nền sáng, tương phản cao (`bg-white`, `bg-slate-50`, `border-slate-200`, `text-slate-900`/`700`). Cấm panel nền tối hoặc đen trong bài đọc. Nền pastel dùng chữ tối, không `text-white`.
12. **Ranh giới kiến thức**: chỉ dùng kiến thức đã dạy đến bài hiện tại (bài đọc, mã, bài tập, quiz). Cấm nhắc khái niệm/lệnh chưa học, kể cả trong tên biến và comment. Bài mở đầu/tổng quan/khái niệm: cấm chuỗi lệnh thực thi thuộc bài sau (`git init`, `docker run`, `try-except`, `class`...); tập trung lý do, bài toán tổng quát, infographic, sơ đồ, bảng so sánh. Reviewer phải từ chối nội dung vi phạm.
13. **Tiêu đề bài sạch**: `<h1>` chỉ là tên chủ đề, cấm tiền tố `Lesson 01 -`, `Bài 01 -`.
14. **Thứ tự cú pháp**: khi giới thiệu cú pháp, đặt thẻ Cú pháp (Syntax Card) trước, ngay sau là danh sách giải thích từng thành phần; từ khóa/placeholder đặt trong `<code>` in đậm.
15. **Hình theo bản chất bài**: bài khái niệm/tổng quan/kiến trúc (không có mã hay lệnh chạy được): ẨN hẳn Step-Tracker, dùng minh họa 2D, sơ đồ, thẻ so sánh. Bài thực thi/thuật toán: nhúng visualizer chạy từng bước (Play/Pause/Step, tô sáng dòng). Mục 3: môn lập trình dùng Live Code Sandbox (nút Chạy, console); môn công cụ/CLI/quy trình dùng khối lệnh tĩnh `<pre><code class="language-bash">`, thẻ so sánh luồng lệnh hoặc thẻ cấu hình.
16. **Một kịch bản thực tế duy nhất**: mỗi bài thiết lập đúng MỘT kịch bản nghiệp vụ ở Mục 1; 100% mã, sandbox, thẻ cú pháp và visualizer ở Mục 2 và 3 mở rộng đúng kịch bản đó, giữ tên biến và logic nhất quán. Cấm đổi sang đề tài rời rạc giữa các ví dụ.

## 1. Bài đọc (`reading.html`) - nguồn sự thật của khóa học

- Không đoạn văn dài: dùng gạch đầu dòng và gạch con, mỗi ý 1-2 câu, in đậm thuật ngữ.
- Mục 1 có đúng 1 ảnh bối cảnh 16:9: tối đa 800px, căn giữa, `border-radius: 12px`, `box-shadow: 0 4px 20px rgba(0,0,0,0.08)`, viền `1px solid var(--border-color)`, chú thích in nghiêng ngay dưới.
- Thẻ so sánh Nên làm/Không nên làm: mã chuẩn có comment tốt đối lại mã dễ lỗi kèm comment giải thích lỗi.
- Tự kiểm tra: `.selftest-question` có `justify-content: flex-start !important; gap: 8px !important; text-align: left !important;` (cấm `space-between`); `.selftest-answer` và phần tử con `text-align: left !important;`.
- Trước MỖI sandbox chạy mã (Mục 2, 3) có khung yêu cầu `p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4` nêu bài toán ("Yêu cầu bài toán thực hành: ...").
- Đánh số `<h3>` theo mục cha (2.1, 2.2; 3.1, 3.2, 3.3; 4.1, 4.2), cấm đánh số độc lập 1., 2., 3.
- Visualizer từng bước (theo nguyên tắc 15) rộng 100%: `w-full my-8 rounded-2xl overflow-hidden shadow-xl`; có Play/Pause, Bước trước, Bước sau, Reset; chọn tốc độ (1.5s, 1.0s, 0.5s); tô sáng dòng đang chạy; vùng trạng thái biến/bộ nhớ; vùng console đầu ra (nền sáng theo nguyên tắc 11).
- Phong cách: câu, gạch đầu dòng, câu hỏi, giải thích và tiêu đề con kết thúc bằng dấu chấm. Chữ nghiêng chỉ cho chú thích dưới ảnh/sơ đồ. Cấm viết HOA toàn bộ trên tiêu đề, nút, nhãn (dùng Sentence Case hoặc Title Case). Cấm emoji dạng chữ; dùng biểu tượng SVG/Phosphor hoặc nhãn `[NOTE]`, `[TIP]`, `[WARNING]`.
- Mã: đúng cú pháp, quy ước đặt tên, thụt lề của ngôn ngữ; nhãn khối mã đúng (`python`, `javascript`, `html`, `css`, `bash`, `sql`...).

## 2. Bài tập (6 bài thực tế)

- Dựa trên vai trò doanh nghiệp thật (LMS, giỏ hàng...), không dùng bài thuật toán khô (kim tự tháp sao, giai thừa).
- Bloom: Bài 1-2 cơ bản: mã cũ có lỗi logic, người học đọc mã, lập bảng test, sửa lỗi. Bài 3-4 nâng cao: vai trò dev nhận việc, quy tắc nghiệp vụ và ca biên (có dữ liệu vào/ra mẫu). Bài 5 phân tích: tối ưu quy trình, ít nhất 2 phương án, bảng đánh đổi, lưu đồ trước khi viết mã. Bài 6 sáng tạo: mô-đun hoàn chỉnh, tự chủ tối đa, cấm cho sẵn mẫu vào/ra hay JSON schema; người học tự thiết kế schema, liệt kê ca lỗi biên, vẽ DFD, cài đặt theo thiết kế của mình.
- Đề Markdown, đúng 5 mục H3: `1. Mục tiêu`, `2. Bối cảnh và vấn đề` (kèm lưu đồ Mermaid), `3. Quy tắc nghiệp vụ` (hoặc `3. Mã cũ`), `4. Yêu cầu`, `5. Quy định nộp bài`; cấm nhúng rubric vào đề.
- Rubric tách riêng (`rubric_XX.md`): bảng 100 điểm, 5 nhóm tiêu chí.
- Bài tập lập trình chạy được (xem PROJECT_STATE): có `starter/` kèm `tests.html` và `harness.js` để tự chấm.

## 3. Lab và Mini Project

Ba phần: Mục tiêu (2-3 kỹ năng, sản phẩm bàn giao); Mô tả và quy trình (tài nguyên đầu vào, bước đánh số); Checklist định lượng dạng `[ ]` để tự kiểm.

## 4. Quiz (9 nguyên tắc)

1. Mỗi câu đo đúng 1 khái niệm/kỹ năng cốt lõi của bài.
2. Không hỏi kiến thức chung tra Google được.
3. Dựa trên tình huống kỹ thuật cụ thể đã dạy.
4. Trình bày khách quan, độc lập: cấm cụm viện dẫn nguồn trong câu hỏi, đáp án, giải thích ("ở/trong slide", "trong/theo bài giảng", "theo/trong video", "theo lời giảng viên", "Theo Phần ...", "trong bài đọc", "dựa vào đoạn văn trên", "trong kịch bản doanh nghiệp").
5. Đáp án nhiễu dựa trên hiểu lầm có thật; cấm "Tất cả đều đúng", "Tất cả đều sai".
6. Bốn lựa chọn A-D dài và cấu trúc câu tương đương.
7. Không để lộ manh mối giữa câu hỏi và đáp án đúng.
8. Vị trí đáp án đúng phân bố ngẫu nhiên.
9. Chỉ hỏi kiến thức đã dạy đến buổi hiện tại.

## 5. Slide HTML (hỗ trợ bài giảng 1,5 giờ, không phải giáo trình nén)

- 15-20 slide mỗi buổi. Bìa: thẻ đỏ mã buổi (`Session 01`), tiêu đề đậm tối (`#0f172a`), tên môn chính thức. Mục lục: danh sách `1.`, `2.`..., tiêu đề `Nội dung bài học`.
- Tổng kết bài học: ngay trước slide kết thúc/Q&A, 3-6 ý cốt lõi, danh sách số phẳng, chữ lớn, cùng màu và bố cục với Mục lục.
- Chữ: nội dung tối thiểu 18px, gạch con tối thiểu 16px; quy tắc 3-30-300: tối đa 3 ý chính mỗi slide, tối đa 30 từ mỗi ý. Không emoji (dùng Phosphor SVG hoặc badge CSS).

## 6. Kịch bản video

- Chỉ sản xuất kịch bản (`Video/SCRIPT.md`), không dựng hay render video. Chuẩn đầy đủ: `skills/video_script_generator/SKILL.md` (3 phần Mở đầu, Nội dung chính, Kết luận; mỗi phân cảnh có thời lượng, hình ảnh/hành động, lời thoại).
- Lời thoại là câu nói tự nhiên đầy đủ (ngữ cảnh, khái niệm, ví dụ, tóm tắt); phần hình ảnh chỉ mô tả ngắn gọn từ khóa, thẻ mã, sơ đồ.
- Cấm nói số slide ("Nhìn vào slide 3"); tránh so sánh nhất khoa trương ("nhất", "vô cùng", "triệt để").

## 7. Quy tắc dùng chung

- Mã dùng màu tương phản cao (`#79c0ff` biến, `#7ee787` chuỗi/số, `#ff7b72` từ khóa, `#ffa657` hàm). Console đầu ra: panel terminal font `JetBrains Mono`, chữ `#4ade80` (riêng visualizer trong bài đọc theo nguyên tắc 11).
- Sandbox chạy mã Python dùng Pyodide (`https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js`) với nút Chạy; môn JS chạy mã JS thật trong trình duyệt (ô sửa mã, nút Chạy, console giả lập, chống lặp vô hạn). Môn không chạy mã: không nhúng runtime.

## 8. Lỗi thường gặp và cách tránh

Kho kinh nghiệm theo nhóm: `skills/lessons_learned/SKILL.md` (mỗi `<img>` có chú thích dưới; `<table>` bọc `div.overflow-x-auto`; đóng đủ thẻ; không placeholder chưa render; nhãn ngôn ngữ khớp công nghệ).

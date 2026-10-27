# Gói kỹ năng tạo học liệu (Rikkei Education)

Gói này gom MỘT chỗ toàn bộ 20 kỹ năng (skill) đang dùng để tạo học liệu: bài đọc, câu hỏi bài đọc, quiz lesson, quiz cấp buổi, bài tập, bài tập tại lớp, bài thực hành (lab), slide, bài giảng trên lớp, mindmap, kịch bản video, đề thi và các thành phần hỗ trợ. Gói là bản sao nguyên văn từ `skills/` và các tài liệu chuẩn của dự án sau khi viết lại skill slide (thay `skill-1`, `skill-2`, `skill-3` bằng `slide_deck` và `slide_html`), để mang đi dùng riêng hoặc đọc nhanh mà không phải tìm trong cả kho mã. Nguồn gốc vẫn là `skills/` của dự án: khi sửa chuẩn, sửa ở đó rồi chạy lại bước đóng gói.

## 1. Gói gồm những gì

```
goi_ky_nang_hoc_lieu/
├── README.md                  tệp này: danh mục, thứ tự làm việc, cách dùng
├── skills/                    20 skill, mỗi skill một thư mục có SKILL.md (`slide_deck` và `slide_html` có thêm `scripts/` và `reference/`)
├── chuan/                     chuẩn chung: AGENTS.md, quy_chuan_chi_tiet.md, TIEU_CHUAN_BAI_DOC.md, HUONG_DAN_SU_DUNG.md
├── mau/                       mẫu giao diện: reading.html, slide_template.html, SLIDE TEMPLATE.pptx, các mẫu .j2, PM_Template_Standard.xlsx
└── vi_du_dac_ta_mon/          đặc tả và brief mẫu của hai môn đã làm (ReactJS, NodeJS) để bắt đầu một môn mới
```

## 2. Danh mục skill

### 2.1. Học liệu cốt lõi của một bài học (cấp lesson)

| Skill | Tạo ra | Đầu ra / vị trí điển hình | Điểm chốt |
|---|---|---|---|
| `reading_generator` | Bài đọc tương tác | `Bai doc/reading.html` (các môn viết tay gần đây có thêm `reading.md` cùng nội dung) | 5 mục cố định, tối đa 15 phút (1.500-2.000 từ kể cả mã), một kịch bản nghiệp vụ, ví dụ chạy được, mô phỏng tương tác, hero SVG, câu tự kiểm tra; không emoji |
| `reading_questions_generator` | 3 câu hỏi kiểm tra đã đọc | `Cau hoi bai doc/reading_questions.md` | 3 mức Thông hiểu, Vận dụng, Phân tích; bám dữ liệu cụ thể trong bài đọc, có gợi ý đáp án |
| `quiz_generator` | Quiz lesson 5 câu (và lược đồ câu hỏi dùng chung) | `Quizz lesson/quiz.md` và tệp xlsx nhập hệ thống | Mỗi câu một khái niệm, tình huống thực tế, bốn phương án, đáp án đã chạy thật; thứ tự SYNTAX, EXECUTION_FLOW, CODE_TRACE, COMPARISON, TRAP_PREDICTION |
| `lab_generator` | Bài thực hành (lab) | `Bai thuc hanh/practical_lab.md` (các môn gần đây đặt tên `lab_guide.md`) | Mục tiêu, các bước chạy tuần tự, checklist đánh giá định lượng; độ khó theo đúng phạm vi đã học |
| `video_script_generator` | Kịch bản quay video | `Video/SCRIPT.md` | Chỉ sinh kịch bản, không dựng video; ba phần Mở đầu, Nội dung chính, Kết luận; phân cảnh gộp lời đọc và hình |
| `visualizer_generator` | Mô phỏng tương tác theo chủ đề | khối HTML/JS dùng trong bài đọc hoặc bài giảng | Máy trạng thái bằng JavaScript thuần, lược đồ JSON đầu ra |
| `image_prompt_standard` | Chuẩn câu lệnh tạo ảnh | prompt cho Imagen, DALL-E, Stable Diffusion | Infographic vector phẳng, không emoji chữ, tiêu đề tiếng Việt có dấu, tỉ lệ 16:9 |

### 2.2. Học liệu cấp buổi (session)

| Skill | Tạo ra | Đầu ra / vị trí điển hình | Điểm chốt |
|---|---|---|---|
| `quizz_session` | Quiz cấp buổi 45 câu | `Quizz session/quizz_cuoi_gio.md` và xlsx 13 cột | Bố cục 18 + 15 + 12 câu, độ khó 6, 10, 11; phủ mọi lesson của buổi, không lặp câu quiz lesson |
| `exercise_generator` | Bộ bài tập lập trình có chấm tự động | `Bai tap/<N>_<cap_do>_<ten>/` gồm đề, rubric, starter, tài liệu giảng viên, đáp án mẫu | Đề 5 mục, rubric 100 + Bonus 10, "cổng kiểm chứng trước khi giao" (đáp án 100% test, starter chạy được nhưng đỏ, nhiều lời giải sai đều đỏ) |
| `session_inclass_exercise_generator` | Bài tập tổng hợp tại lớp 30 phút | tệp bài tập cấp buổi | Một tình huống nghiệp vụ gộp mọi lesson, nêu rõ Input/Output, không lộ lời giải |
| `session_mindmap_compiler` | Mindmap cả buổi | `So do tu duy/mindmap.md` và `mindmap.html` (Markmap, XMind, HTML tự chứa) | Nút là cụm từ khóa ngắn, cây có bậc cố định, một nhánh cho mỗi lesson |
| `session_reading_compiler` | Trang tổng hợp bài đọc cả buổi | `reading_all.html` | Giao diện sáng, thương hiệu Rikkei, nhúng từng bài đọc |
| `classroom_lecture_generator` | Bài giảng trên lớp tương tác | `Bai giang tren lop/slides.html` | Bố cục hai cột (lý thuyết ngắn, mô phỏng và mã chạy trực tiếp), một bối cảnh nghiệp vụ, không dùng kiến thức chưa học |
| `lecture_ui_reviewer` | Thẩm định giao diện bài giảng | báo cáo kiểm tra | Chụp màn hình bằng Playwright, phát hiện tràn khung, lỗi console, rò rỉ mẫu, đánh giá bằng mười tiêu chí |
| `slide_deck` | Slide PowerPoint của buổi | `Slide bai giang/slide.pptx` | Agent chỉ viết `slides.json`; bộ dựng của dự án áp template Rikkei; `build_deck.py` kiểm dữ liệu rồi dựng, `check_deck.py --render` đo chữ tràn thật và xuất ảnh để xem; 14-18 slide, tiêu đề mệnh đề khẳng định, ghi chú giảng |
| `slide_html` | Slide chiếu trên lớp | `Bai giang tren lop/slides.html` | Bắt đầu từ khung đã duyệt (`reference/slides_frame.html`), nền sáng phẳng, mỗi slide vừa khung 1366x768 và 1920x1080; `check_slides_html.py` đo tràn dọc, lỗi console, cấm kính mờ, gradient, emoji |

### 2.3. Đánh giá, môn phi lập trình và hỗ trợ

| Skill | Tạo ra | Điểm chốt |
|---|---|---|
| `exam_generator` | Đề thi giữa môn và cuối môn: đề thực hành, đề trắc nghiệm, câu hỏi vấn đáp | Hình thức đề theo kiến trúc môn (console, REST API, giao diện web, di động, SQL, DevOps); có cổng thẩm định trước khi xuất bản |
| `effective_biz_generator` | Trực quan và sơ đồ khung chiến lược cho môn kinh doanh, kinh tế, quản trị, phi IT | HTML tự chứa tương tác, tiếng Việt có dấu |
| `lessons_learned` | Kho kinh nghiệm phòng lỗi rút ra từ phản hồi reviewer | Mọi agent đọc trước khi sinh hoặc rà soát học liệu; nhóm A cho mọi môn, nhóm B theo công nghệ |
| `obsidian_graph_view` | Vault Obsidian có liên kết WikiLink | Xem toàn bộ chương trình dưới dạng đồ thị Session, Lesson, bài đọc, slide, quiz, mindmap |

## 3. Thứ tự làm việc để tạo một môn mới

1. Chốt đặc tả môn (số session, số lesson, công nghệ và phiên bản, chủ đề nghiệp vụ, phạm vi "không đưa vào"). Xem `vi_du_dac_ta_mon/` (ReactJS và NodeJS) để lấy khung. Dùng `mau/PM_Template_Standard.xlsx` nếu chạy pipeline từ file PM.
2. Cấp lesson, theo thứ tự: bài đọc (`reading_generator`), rồi câu hỏi bài đọc, quiz lesson và lab bám bài đọc đã viết; kịch bản video khi cần. Quiz và câu hỏi KHÔNG sinh trước bài đọc.
3. Cấp buổi sau khi đủ bài đọc của buổi: quiz cấp buổi, bài tập, slide, bài giảng trên lớp, mindmap; thẩm định bài giảng bằng `lecture_ui_reviewer`.
4. Bài tập lập trình: viết xong bài đọc trước, mã nền dùng lại sao chép nguyên văn từ đáp án bài trước, rồi chạy cổng kiểm chứng của `exercise_generator` (mục 8).
5. Đọc `lessons_learned` trước mỗi lần sinh và sau mỗi lần rà soát.

Trong pipeline của dự án, tài nguyên cấp bài (`html`, `quiz`, `practical_lab`, `reading_questions`, `video_script`) và cấp buổi (`homework`, `mindmap`, `lecture`, `slide`, `session_quiz`) chọn bằng `--parts`; chi tiết lệnh ở `chuan/HUONG_DAN_SU_DUNG.md`.

## 4. Quy tắc chung đã chốt (áp dụng cho mọi skill)

- Ngôn ngữ đầu ra: tiếng Việt có dấu, giữ nguyên thuật ngữ và từ khóa tiếng Anh. Không emoji, không thẻ ngoặc vuông kiểu `[NOTE]`, tránh từ sáo rỗng (nhé, bẫy lập trình, thần thánh, bí kíp, tất tần tật, thân mến, thực chiến, gotcha, anti-pattern, khám phá, tuyệt vời).
- Bài đọc tối đa 15 phút: 1.500-2.000 từ kể cả mã, một vấn đề chính; hằng số `READING_WORD_BUDGET` ở `core/reading_budget.py` của dự án.
- Mọi đoạn mã, truy vấn, kết quả và đáp án trong tài liệu phải được CHẠY THẬT trước khi giao; câu hỏi dạng dự đoán có ba đáp án sai thật sự sai.
- Không gắn cứng một môn hay một công nghệ vào skill hoặc prompt: dự án phục vụ nhiều môn, mọi giá trị riêng của môn nằm trong đặc tả môn.
- Không tự thêm kiến thức chưa học vào bài, bài tập, quiz hay slide (giữ ranh giới phạm vi từng lesson).
- Giữ nguyên khung HTML, CSS và phong cách bài đọc và slide đã duyệt; chỉ thay nội dung.
- Khi tạo học liệu, chỉ ghi vào `output/` và `storage/`; không sửa mã nguồn, lỗi của pipeline thì báo cáo (xem `chuan/AGENTS.md`).

## 5. Cách dùng gói

- Dùng với agent trong IDE: đưa cho agent đường dẫn `skills/<tên>/SKILL.md` của loại học liệu cần làm cùng `chuan/AGENTS.md` và đặc tả môn; yêu cầu agent đọc skill trước khi viết.
- Dùng trong dự án: các skill này đã nằm sẵn ở `skills/` của kho mã; gói chỉ là bản gom để đọc và chia sẻ.
- Script kiểm tra trong gói (`check_reading.py`, `check_slides_html.py`, `check_deck.py`, `deck_lint.py`) nay cần `core/harness` của kho dự án: chỉ chạy được khi gói nằm trong kho (hoặc kho có trên `sys.path`).
- Cập nhật gói: sao chép lại `skills/`, `.agents/AGENTS.md`, `docs/quy_chuan_chi_tiet.md`, `docs/TIEU_CHUAN_BAI_DOC.md`, `docs/HUONG_DAN_SU_DUNG.md` và `templates/` sau mỗi lần chuẩn thay đổi, rồi cập nhật dòng commit ở đầu tệp này.
- Ghi chú về `vi_du_dac_ta_mon/`: là bản mẫu, chứa đường dẫn tuyệt đối của máy đã dựng hai môn (ReactJS, NodeJS). Khi dùng cho môn mới, đổi đường dẫn và nội dung theo môn.

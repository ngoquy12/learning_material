# Phân tích 21 skill tạo học liệu và nhận xét

> Cập nhật sau phân tích: chuỗi `skill-1`, `skill-2`, `skill-3` đã được thay bằng hai skill mới `slide_deck` (PPTX) và `slide_html` (slides.html), có script kiểm tra đã thử trên dữ liệu thật; `quiz_generator` đã có frontmatter; `classroom_lecture_generator` có ghi chú phạm vi. Các mục 2.1 đến 2.4 và 3.19 đến 3.21 bên dưới mô tả hiện trạng TRƯỚC khi viết lại. `lessons_learned`, `quiz_generator`, `lab_generator` và `reading_generator` cũng đã sửa theo các nhận xét ở mục 3 (bản `reading_generator` cũ lưu ở `docs/archive/`); các mục 3.1 đến 3.4 và 3.7 mô tả hiện trạng trước khi sửa.

Phạm vi: đã đọc toàn văn 21 `SKILL.md` trong `skills/`, mã dựng slide của dự án (`agents/creators/slide_deck_creator.py`, `agents/reviewers/slide_deck_reviewer.py`, `core/renderers/pptx/deck_engine.py`, `core/renderers/pptx/slide_validator.py`, `templates/prompts/slide_deck_stage1.j2` và `stage2.j2`, `templates/html/classroom_lecture.html.j2`), mục 5 của `.agents/AGENTS.md`, và skill PPTX của Claude để đối chiếu.

Cách đọc các nhận định: mục "Bằng chứng" là điều kiểm được trong tệp. Mục "Suy luận" là diễn giải từ bằng chứng; tôi chưa quan sát trực tiếp lần chạy lỗi của bạn trên Antigravity (Gemini), nên phần "vì sao agent làm theo phong cách riêng" là suy luận có căn cứ, chưa phải kết quả đo. Nếu bạn gửi một bộ slide sai kèm lệnh đã dùng, tôi đối chiếu được chính xác hơn.

---

## 1. Kết luận nhanh

| Mức | Skill |
|---|---|
| Tốt, dùng được gần như nguyên trạng | `reading_questions_generator`, `session_mindmap_compiler`, `video_script_generator`, `exercise_generator`, `exam_generator`, `session_inclass_exercise_generator`, `lessons_learned`, `skill-1-phan-tich-noi-dung-tho` |
| Khá, cần sửa mâu thuẫn hoặc bổ sung | `reading_generator`, `quiz_generator`, `quizz_session`, `lab_generator`, `visualizer_generator`, `lecture_ui_reviewer`, `session_reading_compiler`, `skill-2-kien-truc-noi-dung-bai-giang`, `effective_biz_generator`, `obsidian_graph_view` |
| Cần viết lại | `skill-3-thiet-ke-slide-tu-template`, `classroom_lecture_generator`, `image_prompt_standard` |

Ba vấn đề lớn nhất của cả bộ:
1. Chuỗi skill slide (skill-1, 2, 3) không có phần đầu `---` (frontmatter `name` và `description`) nên agent trong IDE không tự nhận ra khi nào cần dùng chúng. `quiz_generator` cũng thiếu như vậy.
2. Skill dựng slide chỉ có bộ kiểm tra, không có công cụ dựng; công cụ dựng thật (`deck_engine.py`) nằm trong mã dự án mà skill không nhắc tới.
3. Các skill mâu thuẫn nhau về cùng một quy tắc (emoji, nhãn ngoặc vuông, chế độ nền tối, chữ in hoa), nên agent làm theo skill nào đọc sau cùng.

---

## 2. Vì sao skill slide sai yêu cầu và ra phong cách riêng của Gemini

### 2.1. Bằng chứng

1. **Không có frontmatter.** `skill-1-phan-tich-noi-dung-tho`, `skill-2-kien-truc-noi-dung-bai-giang`, `skill-3-thiet-ke-slide-tu-template` và `quiz_generator` bắt đầu bằng `# ...` chứ không phải `---`. Cơ chế nạp skill của IDE chọn skill theo `description`. Không có `description` thì không có gì để khớp.
2. **Skill-3 là danh sách quy tắc, không phải quy trình có công cụ.** Nó yêu cầu sửa XML OOXML trực tiếp (mục 2.1: cấm `add_slide`, bắt buộc nhân bản slide có sẵn rồi sửa XML) nhưng thư mục skill chỉ có `scripts/validator.py` (79 dòng), không có script dựng, nhân bản slide hay xuất ảnh. Mã dự án có sẵn bộ dựng đầy đủ là `core/renderers/pptx/deck_engine.py` (khoảng 1.050 dòng, 14 kiểu slide), nhưng skill không hề nhắc nó.
3. **Validator kiểm ít hơn skill hứa.** Mục 7 của skill-3 hứa "`sz` mọi text khớp đúng vai trò". `validator.py` khai báo `SZ_H1`, `SZ_H2`, `SZ_BODY`... ở đầu tệp nhưng không dùng chúng ở đâu. Nó chỉ kiểm 5 thứ: `spcPts`, placeholder rỗng, giá trị bo góc, chữ in hoa, và in thông tin viền màu chủ đạo. Không kiểm: cỡ chữ, tràn khung, chồng lấn, emoji, căn giữa, đổ bóng, thanh màu, font.
4. **Bộ duyệt tự động không chặn lỗi hình.** `slide_deck_reviewer.py` cho `PASSED` nếu không có lỗi cấu trúc; ảnh xuất ra chỉ thành cảnh báo "cần soi mắt". Điểm 100 vẫn có thể đi kèm slide tràn hoặc chồng chữ.
5. **Bốn chuẩn "slide" cùng tồn tại và không chỉ rõ mỗi chuẩn áp cho sản phẩm nào:**

| Nguồn | Sản phẩm | Quy định chính |
|---|---|---|
| skill-1, 2, 3 và `deck_engine.py` | `slide.pptx` | Slide để quay video E-learning, 8 loại slide bắt buộc, tiêu đề H1 kèm mệnh đề H2 trên mọi slide, chữ ngắn, ghi chú giảng 3-5 câu |
| `slide_deck_stage2.j2` | `slide.pptx` | 14-18 slide cho một buổi, kiểu `h1` là nhãn còn `h2` là mệnh đề; khác skill-2 (H1 đánh số phần) |
| `AGENTS.md` mục 5 | `slides.html` | 15-20 slide mỗi buổi, chữ tối thiểu 18px, quy tắc 3-30-300, tiêu đề mục lục "Nội dung bài học" |
| `classroom_lecture_generator` | `slides.html` hoặc `index.html` | Bảng điều khiển hai cột, thẻ kính mờ, mô phỏng trực tiếp cho buổi giảng 2 giờ |

   Bài giảng trên lớp và slide HTML cùng tên tệp `slides.html` nhưng thiết kế hoàn toàn khác nhau. Skill-2 coi slide là tư liệu quay video; `AGENTS.md` coi slide hỗ trợ buổi dạy 1,5 giờ; skill lớp học coi là buổi 2 giờ. Mật độ chữ vì thế mâu thuẫn.
6. **Phong cách "premium" nằm sẵn trong chính skill và mẫu của nhánh HTML.** `classroom_lecture_generator` mô tả "premium", "Glass-Card", ghi sẵn lớp Tailwind và biểu tượng tô màu (`ph-lightbulb text-amber-500`, `ph-warning-octagon text-rose-600`), nhãn viết hoa (`KHÁI NIỆM & CÚ PHÁP`). Mẫu `classroom_lecture.html.j2` có `glass-card` với `backdrop-filter: blur`, `gradient-text` chuyển từ đỏ sang chàm (`#be111c` tới `#4f46e5`) và hoạt ảnh `pulse`. `lecture_ui_reviewer` còn chấm điểm thưởng cho Glassmorphism và hoạt ảnh (tiêu chí 6 và 7). Các nhãn viết hoa trái với quy tắc "cấm ALL CAPS" của skill khác.
7. **Skill-3 là danh sách cấm sau khi gặp lỗi, không phải mô tả điều cần làm.** Mục 2.12 cấm emoji, thanh màu, viền một cạnh, chữ in hoa, ảnh ngoài, đổ bóng... Đây chính là những thứ mô hình hay tự thêm. Danh sách cấm dài mà không có công cụ chặn thì mô hình dễ vẫn làm.
8. **Skill tự mâu thuẫn về thương hiệu.** Đầu tệp skill-3 nói "KHÔNG áp cứng mã màu/font của thương hiệu nào" và yêu cầu trích token từ template. Nhưng mục 2.2 và 2.9b ghi cứng `Montserrat ExtraBold`, `#C00000`, 28-30pt, và cả ba nội dung trang bìa. `deck_engine.py` và `validator.py` cũng ghi sẵn `C00000`, `Montserrat`. Font `Montserrat` không được nhúng vào tệp nên máy không có font này sẽ đổi sang font khác, độ rộng chữ lệch và dễ tràn khung.
9. **Tham chiếu chéo cũ và sai.** Skill-2 (dòng 21-23) gọi bước dựng slide là "Skill 1" với tệp `SKILL_1_Thiet_Ke_Slide_Da_Nang.md` (không tồn tại); skill-1 trỏ tới "Skill 1 mục 2.12" trong khi mục đó thuộc skill-3. Đánh số trong thư mục (`skill-1/2/3`) và đánh số trong nội dung không khớp.

### 2.2. Suy luận về "luôn làm theo phong cách Gemini"

Khi skill không tự kích hoạt (mục 1), không có công cụ dựng (mục 2) và không có kiểm tra hình (mục 3, 4), agent chỉ còn cách dùng thư viện mặc định và gu thẩm mỹ mặc định của nó. Với nhánh HTML, "phong cách Gemini" thực ra khớp rất sát với chỉ dẫn trong chính skill (mục 6): thẻ kính mờ, gradient, biểu tượng tô màu, hoạt ảnh nhấp nháy. Tức là agent đang làm đúng skill, chỉ có điều skill mô tả sai thứ bạn muốn.

### 2.3. Vì sao skill PPTX của Claude cho kết quả tốt hơn

| Khía cạnh | Skill PPTX của Claude | Skill slide hiện tại |
|---|---|---|
| Công cụ | Có sẵn bộ script đọc, ảnh thu nhỏ, nhân bản slide, dọn rác, kiểm tra gói, chuyển ảnh; thư viện dựng đã cài sẵn | Chỉ có một validator 79 dòng, không có công cụ dựng |
| Cách dựng | Một đường duy nhất: viết script `pptxgenjs`, dựng theo chủ đề, bố cục, chỗ giữ chỗ | Hai đường song song: sửa XML tay (skill) và `deck_engine.py` (mã), không nối với nhau |
| Quy tắc | Ngắn, có số cụ thể, mỗi điều cấm đi kèm lý do kiểm chứng được ("`#` trong màu làm hỏng tệp") | Rất dài (35 KB cho skill-3), nhiều quy tắc thẩm mỹ chủ quan |
| Kiểm tra | Bắt buộc ba lớp: nội dung, tệp, hình (chuyển ảnh rồi xem) | Có nêu nhưng không có công cụ chạy, reviewer chỉ cảnh báo |
| Thương hiệu | Lấy từ template hoặc yêu cầu người dùng, không ghi cứng | Ghi cứng đỏ, Montserrat dù tuyên bố ngược lại |
| Font | Liệt kê font an toàn, cảnh báo font nào kiểm tra lệch | Ghi cứng font không có sẵn trên mọi máy |
| Kích hoạt | Có mô tả rõ khi nào dùng | Không có frontmatter |

Hai điểm Claude đưa vào mà skill hiện tại chưa có: bước "thử render rồi nhìn từng ảnh" bắt buộc cho mọi bản dựng, và danh sách các lỗi tệp thực tế (ví dụ màu 8 chữ số làm hỏng tệp). Chuẩn kích thước chữ của Claude (14-16pt cho phần chữ) thấp hơn chuẩn dự án (18px) vì mục đích khác (xem trên màn hình so với chiếu lớp), nên không nên bê nguyên.

### 2.4. Đề xuất viết lại chuỗi slide

1. Gộp skill-1, 2, 3 thành MỘT skill `slide_deck` có frontmatter, thân dưới 10 KB, tách phần tra cứu dài ra tệp phụ.
2. Quyết định rõ ba sản phẩm và đặt tên khác nhau: `slide.pptx` (bài giảng quay video hoặc slide giảng), `slides.html` (slide chiếu trên lớp), bảng điều khiển mô phỏng (đặt tên khác, ví dụ `lecture_dashboard.html`).
3. Một đường dựng duy nhất: skill gọi `deck_engine.py` (hoặc script tương đương nằm trong thư mục skill), agent chỉ chuẩn bị dữ liệu slide dạng JSON.
4. Thêm bước xuất ảnh và đo vừa khung vào `validator.py`: kiểm cỡ chữ theo vai trò, tràn khung và chồng lấn bằng toạ độ shape, và để reviewer trả `REJECTED` khi lỗi hình.
5. Bỏ mã thương hiệu và font ghi cứng khỏi quy tắc phổ quát; chỉ lấy từ template; dùng font có trong template hoặc font an toàn.
6. Cho nhánh HTML: bỏ "premium", thẻ kính mờ, gradient, hoạt ảnh nhấp nháy khỏi skill và mẫu; thay bằng chuẩn đã dùng thành công cho môn ReactJS và NodeJS (nền sáng phẳng, chữ tối thiểu 18px, mỗi slide vừa khung 1366x768 và 1920x1080, tab "Mã nguồn" và "Mô phỏng").

---

## 3. Phân tích từng skill

Mỗi mục có: mục đích, điểm mạnh, vấn đề (kèm bằng chứng), đề xuất.

### 3.1. `reading_generator` (bài đọc) — Khá

- Điểm mạnh: kiến trúc 5 mục cố định; 25 chỉ thị đánh số; bảng "Code-level enforcement" (mục 0.15) thừa nhận rõ chỉ thị nào đã được mã kiểm thật (chống mặc định Python, chống ảnh rác ở mục 2-4, cấm từ sáo rỗng ở tiêu đề). Ràng buộc 15 phút và 1.500-2.000 từ có hằng số trong mã.
- Vấn đề:
  1. Dài 54 KB (khoảng 14.000 token) và nạp nguyên cho mỗi lần sinh; nhiều chỉ thị trùng ý (cấm từ sáo rỗng xuất hiện ở chỉ thị 5, 19, 23).
  2. Mâu thuẫn nội bộ: chỉ thị "chỉ Light Mode, cấm nền tối" nhưng mẫu mã dùng `bg-slate-900`, bảng màu có cột Dark Mode, lớp `dark:` khắp nơi; chỉ thị 4 "không tự vẽ SVG" nhưng tiêu chí duyệt 4 đòi `viewBox="0 0 800 450"`; chỉ thị cấm emoji nhưng chỉ thị 13 và danh sách điều khiển dùng emoji.
  3. Ghi cứng chủ đề: Mục 1 "bắt buộc" mô tả `if/elif/else`, "Conditional Branching Solution" và ShopeeFood; chỉ thị 6 buộc định danh `snake_case` (đúng cho Python, sai cho JavaScript); sandbox mẫu viết riêng cho Pyodide. Tuyên bố "không ghi cứng chủ đề" bị chính mẫu phủ nhận.
  4. Khung ngân sách: bắt buộc sandbox cho từng mục con, trình mô phỏng đầy đủ, 3 ví dụ và tự kiểm tra, nhưng chỉ có 1.500-2.000 từ.
  5. Cổng duyệt cuối chỉ là 6 lệnh `grep` (neo mục, `viewBox`, `ph-check-circle`...), không kiểm mã có chạy được.
- Đề xuất: tách thành lõi dưới 10 KB và tệp mẫu riêng; giải quyết ba mâu thuẫn Light Mode, SVG, emoji; chuyển ví dụ `if/else` sang phần minh họa có nhãn; thêm quy tắc "mọi đoạn mã chạy thật" (đã dùng cho ReactJS và NodeJS) vào cổng duyệt.

### 3.2. `reading_questions_generator` — Tốt

- Điểm mạnh: ngắn, rõ; bám mã thật trong bài đọc ("không bịa", trích nguyên văn); hai ví dụ mẫu ở hai ngăn xếp khác nhau chủ ý để mô hình không bám một ngôn ngữ; cấm nhãn meta.
- Vấn đề: mục 4 liệt kê cây thư mục cũ (`Bài thực hành/practical_lab.html`, `Câu hỏi Quizz/quiz.json`) không khớp cấu trúc đang dùng (`Quizz lesson/quiz.md` và xlsx); dùng emoji thư mục ở khối cây.
- Đề xuất: cập nhật cây thư mục; giữ nguyên phần còn lại.

### 3.3. `quiz_generator` (quiz lesson 5 câu) — Khá

- Điểm mạnh: ma trận 5 dạng câu rõ; 9 nguyên tắc câu hỏi tốt (đơn nhiệm, nhiễu thông minh, đồng nhất độ dài, không mách nước).
- Vấn đề:
  1. Thiếu frontmatter (mục 1 báo cáo) nên không tự kích hoạt.
  2. Tự mâu thuẫn: cấm cụm viện dẫn nguồn như "Theo Mục ..." nhưng ví dụ `instant_feedback` lại ghi "tham khảo lại Mục 2.1 trong bài đọc". `lessons_learned` mục A4 cấm cả "trong bài đọc".
  3. Dẫn một tệp không có trong kho (`RE_Tiêu chuẩn quizz.pdf`), không kiểm chứng được.
  4. Dùng emoji ở tiêu đề mục (ba ký tự biểu tượng) dù cấm emoji; trùng lặp danh sách cụm cấm với `quizz_session`.
  5. Không có quy tắc "đáp án phải được chạy thật" (đã áp dụng thực tế ở hai môn vừa làm).
- Đề xuất: thêm frontmatter; định nghĩa rõ `instant_feedback` được phép chỉ tới mục nào (hoặc bỏ tham chiếu mục); đưa danh sách cụm cấm về một nguồn chung.

### 3.4. `quizz_session` (quiz cấp buổi 45 câu) — Khá

- Điểm mạnh: phân bổ cụ thể, rõ (bố cục 18+15+12 hoặc 30 cũ + 15 mới), có bộ trích 15 câu cho phòng thi.
- Vấn đề: mô tả nói tạo hai bộ (Entrance và Exit, mỗi bộ 45 câu) nhưng thực tế các môn chỉ cần bộ cuối giờ; thang độ khó 4 đến 11 không định nghĩa thang gốc; lẫn phần phân tích học viên (hai ma trận phân loại, ký hiệu LaTeX) vào skill sinh đề, không phải hướng dẫn sinh câu; không có ví dụ mẫu.
- Đề xuất: tách phần phân loại học viên ra tài liệu giảng viên; thêm một câu mẫu cho mỗi bậc độ khó; ghi rõ điều kiện dùng Entrance.

### 3.5. `exercise_generator` (bài tập) — Tốt

- Điểm mạnh: nguyên tắc "đóng cách làm, mở điều cần đạt" rõ; phân tầng Bloom; bối cảnh doanh nghiệp, cấm bài toán khô; bảng định dạng mã theo ngôn ngữ; mục 8 "cổng kiểm chứng trước khi giao" (bài đọc trước, mã nền sao chép nguyên văn, cổng quét phạm vi) rút ra từ lỗi thực.
- Vấn đề: mô tả vẫn là bộ 15 bài trong khi dự án đã dùng thang 6 bài cho vài môn (ghi ở `AGENTS.md`, không ghi ở skill); mục 8 giả định tệp `starter/script.js` (đúng cho JavaScript thuần, chưa nói cho dự án có `src/`, cơ sở dữ liệu, bộ test tự chấm; cổng quét lúc đầu chỉ đọc `script.js`, đã sửa ở commit `d04ae30e`); chưa nói bộ test tự động là cách chấm chính; lẫn tiếng Anh và tiếng Việt trong khối mẫu.
- Đề xuất: thêm phần "dự án có build, có cơ sở dữ liệu" (khuôn dự án, `.env.example`, cơ sở dữ liệu thử có hàng rào tên `_test`, cổng kiểm chứng đáp án 100% và lời giải sai đều đỏ) từ thực tế ReactJS và NodeJS.

### 3.6. `session_inclass_exercise_generator` (bài tập tại lớp 30 phút) — Tốt

- Điểm mạnh: ngắn, bố cục 4 phần cố định, ràng buộc "không lộ lời giải", gắn một bối cảnh nghiệp vụ.
- Vấn đề: ví dụ và bảng ngăn xếp nghiêng về `for/while/range` (chủ đề vòng lặp) và chỉ bốn ngôn ngữ (Python, C, Java, JavaScript); chưa có cổng kiểm chứng như `exercise_generator`; gắn chặt vào đường dẫn "bài số 16" của bộ 15.
- Đề xuất: bỏ ví dụ vòng lặp cứng; thêm cổng kiểm chứng; mở rộng bảng ngăn xếp (web framework, SQL).

### 3.7. `lab_generator` (bài thực hành) — Khá

- Điểm mạnh: ví dụ mẫu đầy đủ có bảng giải thích; "độ khó tăng dần"; bối cảnh nghiệp vụ xuyên suốt cả buổi.
- Vấn đề: ví dụ mẫu dùng tên biến tiếng Việt (`so_dem`, `gia_moi_dem`) trái quy tắc "định danh 100% tiếng Anh" ngay trong skill; đánh số mục lộn xộn (1, 2, 3 rồi nhảy tới "4" và "8"); mục 8 chép nguyên từ `exercise_generator` và nói về `starter/script.js` trong khi lab là tệp Markdown; định dạng 3 phần quá mỏng so với bài lab nhiều chặng đang dùng (6 lab nối tiếp, mỗi lab có "Kết quả mong đợi" lấy từ lần chạy thật).
- Đề xuất: sửa ví dụ sang tên tiếng Anh; thêm khuôn lab nhiều chặng và quy tắc "kết quả mong đợi phải lấy từ lần chạy thật".

### 3.8. `classroom_lecture_generator` (bài giảng trên lớp) — Cần viết lại

- Điểm mạnh: ý tưởng tốt (một bối cảnh nghiệp vụ xuyên suốt buổi, tách tham số đầu vào, bước nhỏ tăng dần, vết chạy khớp từng dòng mã).
- Vấn đề: xem 2.1 (mục 5, 6). Thêm: tuyên bố "ZERO HARDCODING" nhưng điều 2.1 cấm cụ thể `function`, `if-else`, vòng lặp ở "Session 1 đến 5" và ví dụ toán tử JavaScript, tức gắn cứng vào một môn; hợp đồng sinh bằng LLM yêu cầu trả `controllers_html`, `code_box_html`, `js_code` là các chuỗi HTML và JavaScript, rất dễ vỡ; tên `slides.html / index.html` va chạm với slide HTML của `AGENTS.md`.
- Đề xuất: đổi tên sản phẩm; bỏ phong cách kính mờ; bỏ ràng buộc theo số buổi; nếu giữ mô phỏng, sinh dữ liệu JSON rồi để mẫu cố định dựng HTML.

### 3.9. `lecture_ui_reviewer` — Khá

- Điểm mạnh: ý tưởng đúng (Playwright chụp ảnh, bắt lỗi console, phát hiện rò rỉ mẫu, kiểm tràn ngang).
- Vấn đề: tiêu chí chấm theo giao diện bảng điều khiển kính mờ (mục lục dính trên, Glassmorphism, hoạt ảnh `pulse-active`), nên sẽ phạt một bộ slide đúng chuẩn; chỉ kiểm tràn NGANG (`scrollWidth > innerWidth`), trong khi lỗi chính thực tế là tràn DỌC (đã đo: 15 trên 30 slide tràn ở 1366x768 trước khi sửa); chỉ thử 1680 và 1920 pixel, bỏ sót laptop 1366x768 là kích thước chiếu thông dụng; phần "Vision AI" chủ quan.
- Đề xuất: kiểm từng slide có tràn dọc không ở ít nhất ba độ phân giải (1366x768, 1536x864, 1920x1080); tách tiêu chí theo loại sản phẩm.

### 3.10. `visualizer_generator` — Khá

- Điểm mạnh: năm kiểu mô phỏng rõ; cấu trúc máy trạng thái với mảng bước tính trước; không phụ thuộc thư viện.
- Vấn đề: mẫu `canvas_title` chứa emoji () trái quy tắc; lược đồ JSON chứa chuỗi HTML dài và mã JavaScript (dễ vỡ khi mô hình sinh); các kiểu mô phỏng nghiêng về lập trình cơ bản (bộ nhớ, vòng lặp), chưa có kiểu cho HTTP, cơ sở dữ liệu, giao dịch, JWT (những mô phỏng đã phải thiết kế riêng cho NodeJS).
- Đề xuất: thêm các kiểu Request/Response, SQL, pool kết nối, luồng xác thực; bỏ emoji.

### 3.11. `session_mindmap_compiler` — Tốt

- Điểm mạnh: cây cố định (một gốc, một `##` cho mỗi lesson, đúng 4 nhánh `###`); nút chỉ là cụm từ khóa ≤ 8-10 từ; nhãn dạng `Khai báo:`, `Kết quả:` được vẽ thành thẻ màu; cấm emoji.
- Vấn đề nhỏ: ví dụ trong skill là chủ đề điều kiện (có ghi "chỉ minh họa"); dẫn "buổi 1,5 giờ".
- Đề xuất: giữ nguyên.

### 3.12. `session_reading_compiler` — Khá

- Điểm mạnh: giải quyết một lỗi thật (khung `iframe` ẩn bằng `display: none` làm Mermaid lỗi).
- Vấn đề: rất hẹp, gần như là ghi chú sửa lỗi; dùng URL logo khác với skill bài giảng (`rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png` so với `qldt.rikkei.edu.vn/re-logo.png` trong mẫu slide), nên logo không nhất quán giữa các sản phẩm.
- Đề xuất: thống nhất một nguồn logo; ghép vào `reading_generator` dưới dạng một mục kỹ thuật.

### 3.13. `video_script_generator` — Tốt

- Điểm mạnh: ba dạng bài, ba phần bắt buộc; hai câu mở và kết nguyên văn; mỗi phân cảnh có thời lượng, hình, lời; ràng buộc 3-7 phút (tối đa 15); danh sách kiểm tra tuân thủ rõ.
- Vấn đề nhỏ: dùng nhãn ngoặc vuông in đậm `**[Chú thích]**` trong lời thoại trong khi nhiều skill khác cấm thẻ ngoặc vuông; danh sách từ cấm khác với danh sách ở skill khác; nhắc tệp PDF trong `resources/`.
- Đề xuất: thống nhất danh sách từ cấm và cách đánh dấu hành động.

### 3.14. `exam_generator` — Tốt

- Điểm mạnh: hình thức đề theo kiến trúc môn (CLI, backend, frontend, SQL...); thi giữa kỳ và cuối kỳ khác phạm vi và số lượng; phần vấn đáp chống nhờ AI; cổng duyệt có thử lại tối đa 3 lần.
- Vấn đề: cổng duyệt phụ thuộc mã (`exam_reviewer_agent`, `lint_document_architecture()`), nên dùng riêng trong IDE không chạy được; `time_limit_sec` là 45 ở đây nhưng 30 ở skill quiz; cây thư mục dùng emoji.
- Đề xuất: ghi rõ phần nào chỉ chạy trong pipeline; thống nhất thời gian mỗi câu.

### 3.15. `image_prompt_standard` — Cần viết lại

- Điểm mạnh: một công thức prompt duy nhất; cấm 3D, neon, nhãn viết hoa, banner tiêu đề trong ảnh.
- Vấn đề: dài khoảng 15 KB, trùng ý nhiều; mâu thuẫn nội bộ ("tối giản" nhưng "giàu chi tiết kỹ thuật": vùng màu, chú thích mũi tên, bảng trạng thái nhỏ; hướng "trên xuống dưới" ở mục 1.7 nhưng "trái sang phải" ở mục 1.6); mâu thuẫn với `reading_generator` (skill bài đọc cấm đưa mã vào ảnh, skill này yêu cầu khung mã IDE trong ảnh); chính tệp dùng nhiều emoji dù cấm emoji; ảnh sinh ra cần xác minh bằng mắt mà skill không có bước kiểm tra.
- Đề xuất: rút còn khoảng 4 KB; chọn một hướng dòng chảy; thống nhất quy tắc mã trong ảnh.

### 3.16. `effective_biz_generator` — Khá

- Điểm mạnh: lấp một khoảng trống thực (môn kinh doanh, không phải lập trình); bố cục có sân khấu SVG kéo thả, ngăn chi tiết, ma trận chiến lược.
- Vấn đề: bắt buộc chế độ Sáng/Tối với `localStorage`, trái chuẩn "chỉ Light Mode" của bài đọc; tiêu đề mẫu tiếng Anh viết hoa (`BUSINESS ADMINISTRATION PROGRAM`) dù yêu cầu tiếng Việt và cấm chữ hoa; chưa có hướng dẫn kiểm chứng; phái sinh từ kho ngoài mà không có ví dụ tiếng Việt hoàn chỉnh.
- Đề xuất: thử trên một môn thật rồi chuẩn hóa; thống nhất chế độ nền với bài đọc.

### 3.17. `lessons_learned` — Tốt

- Điểm mạnh: kho kinh nghiệm gom nhóm A (mọi môn) và B (theo công nghệ), có cơ chế tự ghi thêm từ phản hồi reviewer.
- Vấn đề: mục A2 yêu cầu thay emoji bằng nhãn `[NOTE]`, `[TIP]`, `[WARNING]` — trái quy tắc "không thẻ ngoặc vuông" đang áp dụng ở nơi khác; nhóm B chỉ có Python, FastAPI, C, JavaScript, Git, Docker; chưa có React, Node/Express, MySQL, mock API, cơ sở dữ liệu thử; chưa ghi các bài học mới (chạy thật mọi ví dụ, `LIMIT ?` không dùng được với `execute`, test phải chịu độ trễ máy, mock API chỉ chạy trong Vitest...).
- Đề xuất: sửa quy tắc nhãn; bổ sung nhóm B cho ngăn xếp mới và nhóm "kiểm chứng".

### 3.18. `obsidian_graph_view` — Khá

- Điểm mạnh: quy tắc liên kết và frontmatter rõ.
- Vấn đề: bí danh liên kết dùng emoji (ký tự nhà, mũi tên trái, mũi tên quay lại); cấu trúc giả định `Lesson XX.Y`, Entrance/Exit Quiz, không khớp tên thư mục hiện hành; ưu tiên thấp.
- Đề xuất: bỏ emoji, cập nhật tên.

### 3.19. `skill-1-phan-tich-noi-dung-tho` — Tốt

- Điểm mạnh: nguyên tắc trung thực rất tốt (không bịa; đánh dấu nội dung đề xuất; ghi mâu thuẫn; xác nhận đối tượng và thời lượng với người dùng trước khi khóa).
- Vấn đề: thiếu frontmatter; tham chiếu sai "Skill 1 mục 2.12".
- Đề xuất: thêm frontmatter; sửa tham chiếu.

### 3.20. `skill-2-kien-truc-noi-dung-bai-giang` — Khá

- Điểm mạnh: nền sư phạm tốt (tiêu đề mệnh đề khẳng định, mỗi 3-4 slide có một slide tương tác, ghi chú giảng 3-5 câu, sợi chỉ đỏ, bảng phân bổ thời lượng, phương án rút gọn).
- Vấn đề: thiếu frontmatter; giả định slide dùng để quay video (mâu thuẫn với chuẩn slide chiếu lớp, xem 2.1); dài 20 KB; tên "Skill 1" cũ trong phần đầu; quy tắc cấu trúc 8 loại slide khác với `slide_deck_stage2.j2` (H1 đánh số so với H1 là nhãn).
- Đề xuất: hợp nhất với skill-3 (xem 2.4), đưa quy tắc sư phạm cốt lõi vào thân dưới 10 KB.

### 3.21. `skill-3-thiet-ke-slide-tu-template` — Cần viết lại

- Điểm mạnh: ý tưởng trích token từ template trước khi dựng (Giai đoạn 1); chọn loại minh họa theo bản chất nội dung (Giai đoạn 2b); card ngữ cảnh phân biệt bằng ba kênh (màu, nhãn, hình), tốt cho người mù màu.
- Vấn đề: chi tiết ở 2.1 (mục 1 đến 3, 7, 8, 9). Thêm: 35 KB; nhiều quy tắc thẩm mỹ cực chi tiết (đúng 1.5 dòng, đúng `adj 4000`, màu chữ đen tuyệt đối) mà không có công cụ chặn nên chỉ làm tăng nguy cơ mâu thuẫn; yêu cầu sửa XML bằng tay là việc mô hình làm kém.
- Đề xuất: viết lại như 2.4.

---

## 4. Mâu thuẫn giữa các skill

| Chủ đề | Skill nói gì | Mâu thuẫn |
|---|---|---|
| Emoji | `reading_generator`, `lessons_learned`, `image_prompt_standard`, `session_inclass_exercise_generator`, `session_mindmap_compiler` cấm | `reading_generator` (chỉ thị 13, điều khiển trình mô phỏng), `visualizer_generator` (ký tự biểu tượng xoay vòng), `quiz_generator` (tiêu đề), `obsidian_graph_view`, `exam_generator` (cây thư mục), `image_prompt_standard` (tiêu đề mục) dùng |
| Thẻ ngoặc vuông | `exercise_generator` cấm `[NOTE]` | `lessons_learned` yêu cầu thay emoji bằng `[NOTE]`, `[TIP]`, `[WARNING]`; `video_script_generator` dùng `**[Chú thích]**` |
| Nền tối | `reading_generator` và `lessons_learned` cấm hoàn toàn | Mẫu của `reading_generator` có `bg-slate-900`, `dark:`; `effective_biz_generator` bắt buộc chế độ tối; `skill-3` dùng khối mã nền tối |
| Chữ in hoa | `reading_generator`, `skill-3`, `image_prompt_standard` cấm | `classroom_lecture_generator` (nhãn `KHÁI NIỆM & CÚ PHÁP`), `visualizer_generator` (`TỰ NHẬP MẢNG DỮ LIỆU`), `effective_biz_generator` |
| Mã trong ảnh | `reading_generator` cấm mã trong ảnh | `image_prompt_standard` yêu cầu khung mã IDE trong ảnh |
| Viện dẫn nguồn trong câu quiz | `quiz_generator` cấm "Theo Mục ..." | Chính ví dụ `instant_feedback` trong cùng tệp viện dẫn "Mục 2.1 trong bài đọc" |
| Định danh mã | `reading_generator` chỉ thị 6 và `lab_generator`, `exercise_generator` yêu cầu tiếng Anh | Ví dụ mẫu của `lab_generator` dùng `so_dem`, `gia_moi_dem` |
| Mục đích slide | `skill-2` quay video | `AGENTS.md` mục 5 và `classroom_lecture_generator` là buổi dạy trực tiếp (1,5 giờ và 2 giờ) |
| Số slide | `slide_deck_stage2.j2` 14-18 | `AGENTS.md` 15-20; `skill-2` tính theo thời lượng (khoảng 2-4 phút mỗi slide) |
| Thời gian mỗi câu | `quiz_generator` 30 giây | `exam_generator` 45 giây |
| URL logo | `session_reading_compiler` | Mẫu slide dùng nguồn khác |
| Hardcode chủ đề | Nhiều skill ghi "domain-agnostic" | Ví dụ và quy tắc của `classroom_lecture_generator`, `reading_generator` Mục 1, `session_inclass_exercise_generator` nghiêng về JavaScript và Python |

---

## 5. Vấn đề hệ thống

1. **Skill không tự kích hoạt:** bốn skill thiếu frontmatter. Việc này khắc phục chỉ mất vài phút (thêm `name` và `description`).
2. **Lời hứa không có công cụ chặn:** nhiều quy tắc ghi "MANDATORY" nhưng chỉ nằm trong lời nhắc. Chỉ `reading_generator` có bảng nêu rõ phần nào đã được mã kiểm. Nên áp dụng bảng "Enforced by" cho mọi skill, và coi quy tắc chưa có công cụ chặn là chỉ dẫn mềm.
3. **Cổng kiểm phụ thuộc mã dự án:** nhiều cổng duyệt (`exam_reviewer_agent`, `lint_document_architecture()`, `scripts/check_exercise_scope.py`) cần kho mã đầy đủ. Khi agent chạy trong IDE riêng (Antigravity), nó không có các cổng này. Nên đặt script tự chứa trong thư mục skill (như `skill-3/scripts/validator.py`).
4. **Skill quá dài:** `reading_generator` (54 KB), `skill-3` (35 KB), `skill-2` (20 KB), `exercise_generator` (17 KB) khiến mô hình bỏ sót quy tắc ở giữa. Nên tách lõi ngắn và tệp tham chiếu.
5. **Danh sách quy tắc lặp ở nhiều nơi** (từ cấm, cụm viện dẫn nguồn, quy tắc mã): mỗi nơi sửa một kiểu. Nên có một nguồn duy nhất.
6. **Ghi cứng một môn trong skill "đa môn":** ví dụ JavaScript và Python chiếm đa số; môn mới (React, Node, SQL) không có mẫu.
7. **Chưa có quy tắc "chạy thật mọi ví dụ" ở cấp bài đọc, quiz, slide:** quy tắc này chỉ có ở `exercise_generator` và `lab_generator` mục 8, nhưng đã chứng tỏ hiệu quả khi áp dụng cho toàn bộ môn ReactJS và NodeJS.
8. **Ngôn ngữ chỉ dẫn lẫn lộn:** `AGENTS.md` quy định chỉ dẫn viết tiếng Anh, nhưng skill-1, 2, 3, `video_script_generator`, `lessons_learned` viết tiếng Việt, các skill khác viết tiếng Anh.

---

## 6. Lộ trình sửa đề xuất (theo thứ tự ưu tiên)

| # | Việc | Công sức | Tác động |
|---|---|---|---|
| 1 | Thêm frontmatter cho skill-1, 2, 3 và `quiz_generator` | Rất nhỏ | Skill tự kích hoạt |
| 2 | Viết lại chuỗi slide thành một skill `slide_deck` (mục 2.4): một đường dựng, validator đo thật, reviewer chặn lỗi hình | Lớn | Sửa nguyên nhân gốc của lỗi slide |
| 3 | Đổi tên và viết lại `classroom_lecture_generator`; bỏ phong cách kính mờ; sửa `lecture_ui_reviewer` theo đo tràn dọc ba độ phân giải | Vừa | Hết va chạm tên tệp và giao diện "premium" |
| 4 | Giải quyết 12 mâu thuẫn ở mục 4 (emoji, ngoặc vuông, nền tối, chữ hoa...) | Vừa | Agent không còn phải chọn bên |
| 5 | Rút `image_prompt_standard` còn khoảng 4 KB và sửa mâu thuẫn mã trong ảnh | Nhỏ | Ảnh nhất quán |
| 6 | Tách `reading_generator` thành lõi ngắn và tệp mẫu; đưa quy tắc "chạy thật mọi ví dụ" vào cổng duyệt | Lớn | Bài đọc ổn định hơn |
| 7 | Bổ sung nhóm B của `lessons_learned` cho React, Node, SQL và nhóm "kiểm chứng" | Nhỏ | Giữ lại bài học của hai môn vừa làm |
| 8 | Cập nhật `exercise_generator` và `lab_generator` cho dự án có build, cơ sở dữ liệu, lab nhiều chặng | Vừa | Khớp thực tế |

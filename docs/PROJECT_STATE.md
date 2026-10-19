# Trạng thái dự án (đọc đầu tiên mỗi cuộc trò chuyện)

## 1. Cách đọc tệp này

- Đây là tệp bàn giao giữa các cuộc trò chuyện: agent mới KHÔNG nhớ phiên trước nên đọc tệp này thay vì phân tích lại cả dự án.
- Thứ tự đọc: mục 5 "Việc tiếp theo", rồi mục 3 (trạng thái môn đang làm), rồi mục 4 (chuẩn đã chốt). Mục 2 chỉ đọc khi cần tìm thư mục.
- Cuối mỗi lượt làm việc: cập nhật mục 3, 5, 6 và thêm 1 dòng vào mục 7 (workflow `/handoff` làm việc này). Giữ dưới khoảng 120 dòng; không dán nội dung dài.
- Luật chi tiết: `.agents/AGENTS.md` (gọn) và `docs/quy_chuan_chi_tiet.md` (đầy đủ).

## 2. Bản đồ repo

- `main.py`, `cli/`: điểm vào dòng lệnh (`cli/args.py` có `--pm`, `--session`, `--parts`, `--parallel`, `--scaffold`, `--approve-pm`).
- `agents/`: các agent sinh và rà soát (creators, reviewers, lessons_learned, knowledge_memory...).
- `core/`: đồ thị pipeline (`graph.py`), prompt (`prompts.py`), LLM (`llm.py`, `llm_router.py`), renderer, sandbox, schema, phiên bản học liệu.
- `skills/`: tiêu chuẩn từng loại học liệu nạp vào prompt (qua `core/skills.py`); `skills/lessons_learned/SKILL.md` là kho kinh nghiệm.
- `templates/`, `resources/`: mẫu giao diện, mẫu slide, tài nguyên.
- `documents/`: tệp PM Excel đầu vào (ví dụ `documents/PM_Python.xlsx`); `CLO-PLO/`, `obsidian_vault/`: chuẩn đầu ra và đồ thị tri thức.
- `tests/`: bộ kiểm thử; `scripts/`: tiện ích (quét bí mật `scan_secrets.py`, scaffold, lint DOM...).
- `docs/`: tài liệu; `docs/archive/`: bản lưu cũ.
- Chạy pipeline: `python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --approve-pm` (`--session all` cho cả khóa, `--parts html,slide` cho từng phần).
- Kiểm thử: `python -m pytest tests -q -x --ignore=tests/evals`.
- `output/` (học liệu từng môn, ví dụ `output/pms/<môn>/`) bị gitignore (dòng `output/` trong `.gitignore`), nên KHÔNG có trong git. Chỉ tồn tại trong thư mục làm việc chính của máy này; worktree mới tạo không có sẵn. Cần sao lưu riêng; commit không bảo vệ được học liệu.

## 3. Trạng thái các môn trong `output/pms`

| Môn (thư mục) | Nội dung | Trạng thái |
|---|---|---|
| `git_ai_driven` | Git cho dự án nhóm 10 người. Session 01 lý thuyết (6 lesson, slide, quiz, mindmap), Session 02 thực hành GitHub (bài thực hành, bài tập, tài liệu phát tay), `du_an_mau_campus_smart_hub`, `index.html`, `quiz_viewer.html` | Đã có đủ bộ; chưa rà lại theo chuẩn 15 phút (ghi nhận, chưa kiểm). |
| `web_ai_driven` | HTML/CSS cho giao diện web, 2 session. Session 01: 6 lesson, 6 bài dựng giao diện từ ảnh mẫu, slide, quiz, mindmap. Session 02: lab guide 6 lab + 6 bài từ ảnh mẫu chủ đề Rikkei Student Admin; `rikkei-coffee-starter` | Đã có đủ bộ theo README môn; không JS, không framework. |
| `js_ai_driven` | JavaScript cơ bản. Session 01 (Rikkei Learn): 6 lesson (bài đọc 15 phút) + 6 bài tập + quiz + slides + mindmap. Session 02 (Rikkei Shop): lab guide + 6 bài tập cùng một mô-đun giỏ hàng | Đã sinh đủ; bài tập có `starter/` (index.html, script.js, harness.js, tests.js, tests.html). Đang rà soát chất lượng (xem mục 5, 6). |
| `js_advanced_ai_driven` | JavaScript nâng cao: bất đồng bộ và gọi API (HTTP, event loop, Promise, async/await, fetch, axios). Session 01 (Rikkei Learn, JSONPlaceholder): 7 lesson (bài đọc 15 phút, mô phỏng chạy mã thật) + quiz + Quizz session + 6 bài tập + slides.html (28 slide) + slide.pptx + mindmap (md và html). Session 02 (Rikkei Shop, DummyJSON): lab guide + 6 bài tập. Hạ tầng dùng chung `_shared/` (mock-api.js, harness.js async, axios.min.js) | Đã sinh đủ (2026-10-12). 12 bài tập: đáp án mẫu qua 100% test. Còn mở: bài 6 Session 02 dùng closure ngầm (xem mục 6); đối chiếu tên hàm giữa bài đọc và bài tập Session 01 bài 1-4; chưa commit (output/ bị gitignore). |
| Môn cũ | `Lập trình JavaScript`, `Phát_triển_ứng_dụng_web`, `Lập_trình_Python`, `Lập_trình_Python_Cơ_Bản`, `Lập_trình_Python_học_lại`, `Lập_trình_C_học_lại`, `Lập_trình_Back_end_với_FastAPI`, `Cơ_sở_dữ_liệu`, `PM_Agile_Scrum_Standard`, `PM_Git_Teamwork_Standard`, `PM_IT103_UI_UX_Design_Standard`, `PM_IT104_Web_Interface_Development_Standard`, `PM_Phan_Tich_Thiet_Ke_He_Thong_Standard`, `default_course` | Chưa rà soát (có thư mục Session và tệp PM; chất lượng chưa kiểm theo chuẩn mới). |

## 4. Chuẩn đã chốt gần đây

- Bài đọc: 15 phút đọc (giới hạn cứng), 1.500-2.000 từ kể cả mã, 5 mục cố định, tập trung 1 vấn đề chính.
- Bài tập lập trình: có `starter/` kèm `tests.html` và `harness.js`, sinh viên mở `tests.html` thấy PASS/FAIL tự chấm; đáp án mẫu giảng viên qua 100% test, mã khởi tạo gốc phần lớn FAIL.
- Môn JS: bỏ closure (không dạy, chỉ nhắc ở "Tự học thêm"); chạy trên trình duyệt (Console, Live Server), không Node.js, không DOM/Promise/class ở bản này.
- Không dùng từ cấm (bẫy, gotcha, anti-pattern, khám phá, tuyệt vời...), không emoji; tiếng Việt có dấu.
- Windows: ghi tệp bằng Python với UTF-8 (tránh mã hóa mặc định cp1252); chạy Playwright bằng Chrome cài sẵn (`chrome.exe`).
- Không hardcode giá trị riêng của một môn trong mã/prompt (repo phục vụ nhiều môn). Chỉ dùng model Gemini hiện có; không đổi style bài đọc/slide đã chốt.

## 5. Việc tiếp theo

1. Các thay đổi chưa commit (xem `git status`): đồng bộ 15 phút (`core/reading_budget.py` và các prompt/skill/tài liệu), mindmap HTML (`core/renderers/mindmap_html.py`, skill mindmap mới), bộ nhớ dự án (tệp này, `.agents/workflows`, `docs/quy_chuan_chi_tiet.md`, gom `lessons_learned`). Chờ người dùng rà rồi commit.
2. Chạy lại `python -m pytest tests -q --ignore=tests/evals` trước khi commit (mốc hiện tại: 596 passed, 2 skipped).
3. Sinh lại mindmap bằng pipeline với LLM thật để xác nhận skill mới cho nút ngắn; mindmap JS hiện có chỉ là `mindmap.md` cũ (chưa có `mindmap.html`, sinh bằng `build_mindmap_html`).
4. Cân nhắc thêm validator ép số từ bài đọc trong `READING_WORD_BUDGET` (hiện chưa có kiểm tra tự động).
5. Rà đề bài 6 Session 02 JS (~717 từ, hơi dài).
6. Rà soát lần lượt các môn cũ (mục 3) theo chuẩn mới nếu người dùng yêu cầu.

## 6. Quyết định / còn mở

- Đề bài 6 Session 02 JS khoảng 717 từ, hơi dài so với các đề khác.
- Mindmap HTML: nền tối ở khối mã, chữ có thể tràn mép phải khi mở rộng tất cả ở 1280px (cần cuộn ngang); chưa chỉnh.
- Mâu thuẫn quy chuẩn: nguyên tắc 11 (Light Mode) và mục 7 của quy chuẩn chi tiết (khung mã, console, visualizer nền tối). Tạm thời: khung chứa sáng, console visualizer trong bài đọc nền sáng.
- Đường dẫn workflow Antigravity (`.agents/workflows` hay `.agent/workflows`) cần xác nhận theo phiên bản IDE.
- AGENTS.md có thể bị cắt nếu vượt giới hạn mỗi file rule (một nguồn ghi khoảng 12.000 ký tự, chưa xác nhận chính thức); hiện dưới 11.000.
- `skills/lessons_learned/SKILL.md` đã gom nhóm; liên kết nguồn từng bài chỉ còn trong `docs/archive/lessons_learned_full_2026-10-12.md`, nên agent có thể ghi lại quy tắc cho bài đã có.

- `js_advanced_ai_driven` Session 02 bài 6: `createShopClient` dùng closure ngầm (hàm trả về dùng lại `state` và `http`) dù môn chưa dạy closure; cân nhắc đổi sang đối tượng trạng thái ở phạm vi ngoài.
- `js_advanced_ai_driven`: lab và bài đọc dùng API thật nên có thể lệch nếu DummyJSON/JSONPlaceholder đổi; `_shared/compare_live.py` so mock với API thật.
## 7. Nhật ký thay đổi

- 2026-10-12: tạo tệp này; rút gọn `.agents/AGENTS.md` (chi tiết chuyển sang `docs/quy_chuan_chi_tiet.md`); thêm workflow `/resume`, `/handoff`; gom `skills/lessons_learned/SKILL.md` (bản đầy đủ lưu ở `docs/archive/`).
- 2026-10-12: đồng bộ thời lượng bài đọc 15 phút (hằng số `core/reading_budget.py`); viết lại skill mindmap và thêm renderer HTML tự chứa; cập nhật mục "Việc tiếp theo".
- 2026-10-12: tạo môn `js_advanced_ai_driven` (xem mục 3); `_shared/README.md` mô tả mock API và cách viết test bất đồng bộ.
- 2026-10-12: gỡ toàn bộ phần dựng video HyperFrames (TTS, render, FFmpeg, bộ chuẩn hóa phiên âm); chỉ giữ tạo kịch bản video (`video_script_creator`, skill `video_script_generator`, đầu ra `Video/SCRIPT.md`).
- 2026-10-12: sửa nhóm lỗi quy trình làm kết quả sai: reviewer không còn bị bỏ qua khi bản bị từ chối; phản hồi reviewer đưa vào lần sinh lại (`core/retry_feedback.py`); cache băm toàn bộ prompt, reviewer không cache; không còn nội dung giả cho quiz/lab/video (`GenerationError`); reviewer không tự duyệt khi lỗi JSON; tạo sườn không ghi đè bài có sẵn; session chỉ PUBLISHED khi mọi tài nguyên đạt. Còn lại: phạm vi kiến thức (--session), slide/homework bám lesson, resume mất tham số, hardcode domain.
- 2026-10-12: sửa tiếp: phạm vi kiến thức tính trên toàn khóa (không ghi đè bằng cửa sổ 3 session, đúng khi dùng `--session`); regex bỏ câu cấm có ranh giới từ; resume giữ cấu hình lần chạy mới (`core/resume.py`); batch song song đánh dấu FAILED; tóm tắt lesson từ bài đọc thật cho slide/bài tập/mindmap (`core/lesson_summary.py`). Còn: giới hạn 15 phút chưa có validator, validator bài đọc thiếu metadata, hardcode domain, `pm_updater_agent` ImportError.
- 2026-10-12: giới hạn 15 phút có hiệu lực: prompt bài đọc nêu ngân sách từ (từ `core/reading_budget.py`), validator đếm từ (từ chối khi >2.400 hoặc <750 từ), bỏ ngưỡng 45 KB cũ (hạ còn 20 KB); reviewer truyền `lesson_title`/`lesson_type` để nhánh bài định hướng chạy; môn không viết mã không bắt buộc khối mã ở Section 3. Rủi ro: ngưỡng từ chưa hiệu chỉnh trên bài sinh thật, cần chạy thử 1 lesson.
- 2026-10-12: kinh nghiệm đã học (`state["lessons_learned_prompt"]`) tới bài đọc, quiz, lab và UX reviewer (`core/memory_context.py`); kho tri thức chỉ học từ nhật ký reviewer nội dung. Gỡ hardcode: khớp `extract_lang_tag` theo từ, hash domain ổn định, tiêu đề slide theo `tech_stack`, bỏ ví dụ PostgreSQL/MongoDB và URL docs Python, Sandbox chỉ chạy mã Python, PM generator dựng prompt theo từng khóa. Sửa `pm_updater_agent` ImportError (`app.utils` -> `core.utils.json_sanitizer`). Còn hardcode: cấu trúc buổi 1/buổi 2 trong PM (chuẩn Rikkei), xoay vòng domain theo số buổi.
- 2026-10-12: phân loại buổi/lesson nhất quán: loại do BUỔI quyết định (không suy từ tiêu đề lesson có chữ "dự án"/"project"); từ khóa khớp theo ranh giới từ (`core/utils/text_match.py`), hết bắt nhầm "ide"/"lab". Còn: race giữa nhánh song song, kiểm tra domain bằng ID, skill lệch AGENTS.md, cắt ngữ cảnh.
- 2026-10-12: pipeline 2 giai đoạn: HTML + PracticalLab chạy trước, Quiz/ReadingQuestions/VideoScript chạy sau và bám bài đọc đã sinh (`DEPENDS_ON_READING`, `approved_reading_text`); kiểm tra trôi domain nhận diện theo tên/thực thể (`text_mentions_domain`) thay vì mã ID. Còn: skill lệch AGENTS.md, cắt ngữ cảnh, bài đọc có sẵn trên đĩa bỏ qua scope audit.
- 2026-10-12: thống nhất quy tắc nhãn (cấm thẻ [NOTE]/[TIP]; dùng "Lưu ý:", "Mẹo:", "Cảnh báo:"); ngữ cảnh bài đọc đưa vào quiz/video/câu hỏi nâng lên 20.000 ký tự (`READING_CONTEXT_CHARS`); bài đọc có sẵn trên đĩa vẫn qua scope audit (cảnh báo, không sinh đè); validator cấm "gotcha"/"anti-pattern". Chưa đổi: pipeline homework sinh 15+1 bài trong khi AGENTS ghi 6 bài (cần quyết định).
- 2026-10-12: thêm cổng kiểm tra trước khi giao bài tập lập trình: `core/validators/code_scope_linter.py` + `scripts/check_exercise_scope.py` (cấu trúc chưa dạy: class/this/module/closure; lệch chữ ký hàm dùng chung); quy trình viết bài đọc trước, dấu mã nền chuẩn, sao chép nguyên văn mã nền (skill exercise_generator/lab_generator mục 8). Gốc rễ của lỗi closure ở bài 6 và lệch fakeApi bài 3/4 môn JS nâng cao. Quét thử `js_advanced_ai_driven` còn 2 điểm lệch chữ ký cần người quyết định (buildQuery bài 1 và bài 2; getMe bài 3 và bài 6).
- 2026-10-12: thêm `docs/HUONG_DAN_SU_DUNG.md` (quy trình vận hành chuẩn, đọc trạng thái, tối ưu chi phí, xử lý sự cố, danh sách bàn giao).
- 2026-10-19: chặn tác tử tự sửa mã nguồn khi tạo học liệu: AGENTS.md thêm mục "Ranh giới sửa đổi" và bỏ việc tự làm theo "Việc tiếp theo"/tự ghi trạng thái; `core/source_guard.py` + `scripts/source_guard.py` (snapshot/verify/status) và `main.py` tự báo ở cuối lượt; `lessons_learned_agent` ghi vào `storage/lessons_learned_auto/` thay vì `skills/`. 
- 2026-10-19: `--approve` có tác dụng thật: tài nguyên đã duyệt không bị sinh lại (`skip_if_locked` trong graph) và không bị ghi đè (artifact_writer); khóa khóa-học dùng chung qua `course_key_from_pm`; `html_writer_agent` không còn ghi placeholder đè `reading.html` trước khi sinh. Còn: blueprint/SSOT/self_test fallback giả, exam luôn APPROVED, quiz đầu/cuối giờ không try/except, 15 bài so với 6 bài.

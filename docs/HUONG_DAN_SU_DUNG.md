# Hướng dẫn sử dụng chuẩn để đạt hiệu quả cao nhất

Tài liệu này dành cho người vận hành dự án Learning-Material: cách chạy đúng thứ tự, đọc đúng kết quả và tránh những lỗi đã làm hỏng đầu ra trước đây. Chi tiết kỹ thuật nằm ở `README.md`, quy chuẩn sư phạm nằm ở `.agents/AGENTS.md` và `docs/quy_chuan_chi_tiet.md`, tình trạng hiện tại nằm ở `docs/PROJECT_STATE.md`.

## 1. Chọn đúng đường sản xuất

Dự án có hai đường làm việc, dùng cho hai loại việc khác nhau.

| Đường | Dùng khi | Công cụ |
|---|---|---|
| Pipeline Python (`main.py`) | Sinh hàng loạt bài đọc, quiz, lab, câu hỏi bài đọc, kịch bản video, bài tập session từ file PM Excel; xuất SCORM | `python main.py ...` |
| Làm việc cùng agent trong IDE theo skill | Bài tập lập trình có chấm tự động, slide, mindmap, tài liệu giảng viên, chỉnh sửa theo từng bài | Các skill trong `skills/`, workflow `/resume` và `/handoff` |

Quy tắc chọn: việc lặp lại nhiều lần trên nhiều bài thì chạy pipeline; việc cần phán đoán sư phạm hoặc kiểm chứng bằng trình duyệt thì làm cùng agent theo skill. Hai đường dùng chung một bộ quy chuẩn.

## 2. Chuẩn bị môi trường (làm một lần)

1. Cài Python 3.10 đến 3.12, Node.js 18 trở lên và Git.
2. Tạo môi trường ảo rồi cài thư viện: `python -m venv .venv`, kích hoạt, `pip install -r requirements.txt`.
3. Sao chép `.env.example` thành `.env`. Chọn một chế độ LLM: proxy cục bộ hoặc khóa Gemini thật (`USE_REAL_GEMINI_API_KEY=true` cùng `GEMINI_API_KEY`).
4. Chạy `python scripts/check_environment.py` để kiểm tra Python, Node, thư viện và khóa API. Chỉ tiếp tục khi các mục bắt buộc đều đạt.
5. Chạy `pytest`. Nhánh `main` hiện có 6 test `test_golden_design` đang lỗi do thay đổi renderer chưa hoàn tất của một phiên khác; mọi test còn lại phải đạt.
6. Trên Windows PowerShell, đặt `$env:PYTHONIOENCODING="utf-8"` nếu tiếng Việt hiển thị sai.

## 3. Quy trình chuẩn từ yêu cầu đến sản phẩm

### Bước 0. Nắm hiện trạng (30 giây)
Trong IDE, gọi `/resume`. Agent đọc `docs/PROJECT_STATE.md`, `git status`, `git log` rồi tóm tắt năm dòng. Không yêu cầu agent phân tích lại toàn bộ dự án. Kết thúc mỗi lượt làm việc, gọi `/handoff` để cập nhật trạng thái cho phiên sau.

### Bước 1. Làm rõ yêu cầu trước khi sinh
Chốt các điểm sau với người đặt yêu cầu, vì sửa sau tốn nhiều hơn:
- Đối tượng người học và mục tiêu cuối môn.
- Công nghệ và phiên bản (`--tech-stack`, ví dụ `python/core`, `typescript/nestjs`).
- Môn có viết mã hay không (quyết định cấu trúc bài đọc và bài tập).
- Cấu trúc nào của ngôn ngữ chưa dạy (ví dụ `class`, `this`, `closure`, `module`). Danh sách này dùng cho cổng kiểm tra ở bước 6.
- Chủ đề nghiệp vụ xuyên suốt từng session.

### Bước 2. Chuẩn bị file PM (khung chương trình)
- Tạo mới bằng `python main.py --generate-pm --pm-config config/pm_generator_config.json --output-pm-name <tên>` hoặc viết tay. Môn mới: `python main.py --init-config <MÃ_MÔN>` để có cấu hình mẫu.
- Mỗi lesson cần đủ: tiêu đề cụ thể, chi tiết và chuẩn đầu ra đo lường được (động từ Bloom), phạm vi được phép và cấm, loại buổi (lý thuyết, thực hành, dự án, thi). Phạm vi cấm và loại buổi là hai cột quyết định chất lượng phần kiểm soát kiến thức về sau.
- Mỗi lesson trong buổi lý thuyết phải vừa một bài đọc 15 phút. Bài nào chứa hai vấn đề chính thì tách đôi ngay ở PM.
- Chạy `python main.py --pm <file.xlsx>` không kèm `--approve-pm` để chỉ rà PM. Đọc `structure_review_report.md`, sửa đến khi hết lỗi nghiêm trọng, sau đó mới dùng `--approve-pm`.

### Bước 3. Dựng khung rỗng
`python main.py --pm <file.xlsx> --scaffold` tạo cây thư mục và tệp rỗng mà không gọi LLM. Dùng để kiểm tra tên buổi, tên bài và đường dẫn trước khi tốn chi phí. Tệp đã có nội dung không bị ghi đè.

### Bước 4. Chạy thử một lesson trước, rồi mới chạy cả buổi
1. `python main.py --pm <file.xlsx> --session "Session 02" --parts html --approve-pm`
2. Mở `reading.html`, đối chiếu năm điểm: đúng phạm vi kiến thức, đúng một kịch bản nghiệp vụ, độ dài 1.500 đến 2.000 từ, ví dụ chạy được, không emoji.
3. Nếu đạt, chạy đủ phần còn lại của buổi đó: bỏ `--parts` hoặc liệt kê (`html,quiz,practical_lab,video_script`).
4. Sau cùng mới chạy `--session all`. Dùng `--parallel --concurrency 4` khi có nhiều lesson độc lập; hạ `--concurrency` nếu gặp giới hạn tốc độ (đặt `MAX_LLM_RPM` trong `.env`).

Lưu ý quan trọng:
- `--session "Session 1"` khớp theo chuỗi con, nên có thể bắt thêm Session 10 trở đi. Dùng đúng dạng `Session 01`.
- Chạy lại cùng lệnh sẽ tiếp tục từ điểm lưu: phần đã duyệt không bị sinh lại. Cấu hình của lần chạy mới (`--parts`, phạm vi) luôn được áp dụng.
- `--force` sinh lại tất cả và có thể ghi đè bản bạn đã chỉnh. Chỉ dùng cho đúng phần cần làm lại, và nên kèm `--session` và `--parts` hẹp.

### Bước 5. Rà soát kết quả
Mỗi lượt chạy tạo `review_dashboard.html` trong thư mục khóa học, xếp những tài nguyên cần người xem lên đầu. Đọc trạng thái như sau:

| Trạng thái | Ý nghĩa | Việc cần làm |
|---|---|---|
| Approved | Qua reviewer và kiểm tra phạm vi | Đọc lướt rồi duyệt |
| Approved with Warnings | Qua nhưng còn cảnh báo (ví dụ quiz chưa qua sandbox sau 3 lần) | Đọc cảnh báo, sửa nếu cần |
| Approved with Scope Warnings | Dùng khái niệm chưa dạy hoặc lệch chủ đề nghiệp vụ | Bắt buộc rà; sửa tay hoặc sinh lại phần đó |
| Pending Human Review | Reviewer từ chối cả ba lần | Đọc phản hồi cuối trong nhật ký, sửa tay hoặc chỉnh PM rồi chạy lại |
| FAILED | Nhánh sinh gặp lỗi (ví dụ mô hình không trả đủ 5 câu quiz) | Đọc nguyên nhân, chạy lại đúng phần đó |
| Skipped | Không thuộc bộ tài nguyên của loại buổi này | Kiểm tra loại buổi trong PM nếu không đúng ý |
| PUBLISHED | Mọi tài nguyên của lesson đều đạt | Có thể xuất bản |

Buổi chỉ đạt PUBLISHED khi không còn tài nguyên FAILED hoặc cần người rà. Hệ thống không còn ghi nội dung mẫu chung thay cho nội dung thật; nếu thấy FAILED thì đó là lỗi cần xử lý, không phải lỗi hiển thị.

Sau khi rà xong một tài nguyên, ghi nhận vào hồ sơ kiểm định. Tài nguyên đã duyệt được KHÓA: các lần chạy sau không sinh lại và không ghi đè tệp trên đĩa, trừ khi dùng `--force`. Nên truyền kèm `--pm <file.xlsx>` để hồ sơ gắn đúng khóa học:
`python main.py --pm <file.xlsx> --approve "Session 02/Lesson 01/html" --reviewer "Họ Tên" --approve-note "Đã sửa tay phần ví dụ"`. Tài nguyên cấp bài (`"<Buổi>/<Bài>/<tên>"`): `html`, `quiz`, `practical_lab`, `reading_questions`, `video_script`. Tài nguyên cấp buổi (`"<Buổi>/<tên>"`): `homework`, `mindmap`, `lecture`, `slide`, `session_quiz`.
Từ chối: thêm `--reject`. Xuất hồ sơ: `--export-approvals ho_so.csv`.

### Bước 6. Cổng kiểm tra bài tập lập trình trước khi giao
Với môn lập trình, thứ tự làm việc là bài đọc trước, bài tập và lab sau (để dùng đúng tên hàm, nhãn, thông báo lỗi mà bài đọc đã dạy). Mã nền trong `starter/script.js` được bọc giữa `// ===== Mã nền (có sẵn, KHÔNG sửa) =====` và `// ===== HẾT MÃ NỀN =====`, sau đó là `// ===== BÀI LÀM: ... =====`. Mã nền dùng lại giữa các bài phải sao chép nguyên văn từ bài trước.

Trước khi giao chạy:
`python scripts/check_exercise_scope.py <thư mục môn> --forbid class,this,module,closure --language javascript`
(môn Python: `--language python --forbid class,lambda,comprehension,decorator`). Sửa đến khi báo 0 vấn đề. Mỗi điểm lệch chữ ký hàm được báo phải được xử lý: hoặc là lỗi cần sửa, hoặc là thay đổi có chủ đích và đã nêu trong đề.
Sau đó chạy `tests.html` của đáp án mẫu (phải đạt 100%) và của starter (phải gần như không đạt).

### Bước 7. Xuất bản và vòng phản hồi
- Xuất LMS: `python main.py --pm <file.xlsx> --scorm`, thêm `--xapi-endpoint` nếu có LRS.
- Sau khi có dữ liệu người học: `python main.py --ingest-xapi <file> --ingest-dry-run` để xem trước, rồi chạy không `--dry-run` để ghi vào kho kinh nghiệm. Giữ ngưỡng cỡ mẫu mặc định 15 khi chạy thật.
- Kho kinh nghiệm chỉ học từ nhật ký của reviewer nội dung và tín hiệu người học, rồi được nạp lại vào bài đọc, quiz, lab và reviewer UX ở lượt sinh sau.

## 4. Quy tắc chất lượng cần nhớ khi đọc kết quả

- Thời lượng bài đọc: 15 phút, tương đương 1.500 đến 2.000 từ kể cả mã và phần mô phỏng. Validator từ chối bài trên khoảng 2.400 hoặc dưới khoảng 750 từ. Nguồn của các con số: `core/reading_budget.py`.
- Ranh giới kiến thức: chỉ dùng cái đã dạy đến bài hiện tại, kể cả tên biến và chú thích.
- Một kịch bản nghiệp vụ duy nhất cho mỗi bài; cả buổi dùng chung một chủ đề nghiệp vụ.
- Không emoji, không thẻ ngoặc vuông kiểu `[NOTE]`; dùng "Lưu ý:", "Mẹo:", "Cảnh báo:". Không dùng "gotcha", "anti-pattern", "bẫy".
- Chỉ giao diện sáng, 100% tiếng Việt có dấu ở sản phẩm đầu ra.
- Kịch bản video: dự án chỉ sinh kịch bản (`Video/SCRIPT.md`), không dựng hay render video.

## 5. Cách tăng hiệu quả và giảm chi phí

1. Đầu tư vào PM: phạm vi cấm, loại buổi và chuẩn đầu ra rõ ràng giảm mạnh số lần sinh lại.
2. Luôn chạy thử một lesson trước khi chạy cả khóa; sai ở PM sẽ nhân lên theo số bài.
3. Dùng `--parts` để chỉ sinh thứ cần. Quiz, câu hỏi bài đọc và kịch bản video bám bài đọc đã sinh, nên sinh bài đọc trước.
4. Giữ semantic cache (mặc định bật). Xem thống kê bằng `python main.py --cache-stats`. Chi phí mỗi lượt chạy được in ở cuối.
5. Bật kiểm tra ngữ nghĩa phạm vi (`SCOPE_AUDIT_SEMANTIC=true`) cho các buổi cuối khóa, nơi danh sách kiến thức đã học dài và từ khóa khó bắt vi phạm. Đổi lại tốn thêm lượt gọi LLM.
6. Đã sửa tay một tài nguyên thì duyệt nó ngay bằng `--approve`: tệp được khóa khỏi bị sinh lại hoặc ghi đè. Vẫn nên có bản sao lưu vì `--force` bỏ qua khóa.
7. Đừng dùng `--force` toàn khóa. Nếu cần làm lại một phần, giới hạn bằng `--session` và `--parts`.
8. Tin vào nhật ký: phản hồi của reviewer đã được đưa vào lần sinh lại. Nếu một bài bị từ chối ba lần cùng một lý do thì lỗi nằm ở PM hoặc quy chuẩn, không nằm ở may rủi; sửa nguồn thay vì chạy lại.

## 6. Khắc phục sự cố thường gặp

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| Báo thiếu khóa API | `.env` chưa cấu hình hoặc sai chế độ | Xem mục 2, chạy `check_environment.py` |
| Quiz hoặc lab ở trạng thái FAILED | Mô hình trả sai định dạng nhiều lần | Chạy lại đúng phần: `--parts quiz` kèm `--session` |
| Bài đọc bị từ chối vì "quá dài" hoặc "quá ngắn" | Lesson chứa nhiều hơn một vấn đề chính, hoặc quá mỏng | Tách hoặc gộp lesson trong PM, rồi chạy lại |
| Cảnh báo "lệch bối cảnh nghiệp vụ" | Bài viết không nhắc domain đã chọn cho buổi | Kiểm tra `chosen_domain`; nếu bài dùng domain khác thì sinh lại |
| Cảnh báo "dùng khái niệm chưa học" | Phạm vi cấm trong PM thiếu hoặc quá chung | Bổ sung phạm vi cấm theo từng lesson, chạy lại |
| Lesson bị bỏ qua không sinh gì | Loại buổi trong PM là dự án, thực hành hoặc thi | Đổi loại buổi trong PM nếu không đúng; loại lesson do buổi quyết định, không do tiêu đề lesson |
| Chạy `--parts quiz` sau `--parts html` mà quiz không sinh | Bản cũ của hệ thống dùng lại cấu hình lần trước | Đã sửa; nếu vẫn gặp, chạy lại và báo kèm nhật ký |
| Bài đã chỉnh tay bị ghi đè | Chưa `--approve`, hoặc dùng `--force` | Khôi phục từ bản sao lưu; lần sau duyệt bằng `--approve` trước khi chạy lại |
| Tiếng Việt lỗi trên console Windows | Mã hóa terminal | `$env:PYTHONIOENCODING="utf-8"` |
| Test `test_golden_design` đỏ | Thay đổi renderer dở của phiên khác | Không phải lỗi của bạn; xem `docs/PROJECT_STATE.md` |

## 7. Làm việc với Git khi nhiều người hoặc nhiều phiên cùng sửa

- Thư mục `output/` nằm ngoài Git. Tài liệu môn học không được sao lưu qua Git; sao lưu riêng.
- Làm việc trong worktree hoặc nhánh riêng. Khi gộp vào `main` đang có thay đổi chưa commit của người khác, sao lưu trạng thái trước (một tham chiếu `refs/backup/...`), gộp từng tệp bằng 3-way merge, rồi mới fast-forward. Không dùng `git stash` chung và không `reset --hard`.
- Chỉ đẩy lên origin khi test đạt (trừ nhóm test đã biết lỗi) và đã ghi `docs/PROJECT_STATE.md`.
- Mỗi lượt kết thúc: `/handoff`.

## 8. Danh sách kiểm tra trước khi bàn giao một môn

- PM đã qua rà soát, phạm vi cấm và loại buổi đúng.
- Mọi lesson lý thuyết ở trạng thái Approved hoặc đã được duyệt bằng `--approve`; không còn FAILED, Pending Human Review hay Scope Warnings chưa xử lý.
- Bài đọc 1.500 đến 2.000 từ, không emoji, không thẻ ngoặc vuông, đúng một kịch bản nghiệp vụ.
- Quiz hỏi đúng nội dung bài đọc; câu hỏi bài đọc gắn với dữ liệu cụ thể của bài.
- Bài tập lập trình: cổng `check_exercise_scope.py` báo 0 vấn đề, đáp án mẫu 100% test, starter gần như không đạt, ít nhất sáu lời giải sai tiêu biểu đều bị test bắt.
- Slide, mindmap và kịch bản video khớp với bài đọc.
- `docs/PROJECT_STATE.md` đã cập nhật; mã nguồn đã đẩy lên Git; tài liệu trong `output/` đã sao lưu.

## 9. Giữ mã nguồn nguyên vẹn khi tạo học liệu (tác tử không được tự sửa mã)

Quy tắc: lượt tạo hoặc sửa học liệu chỉ được ghi vào `output/` (và `storage/`). Mã nguồn, skill, template, cấu hình, test là vùng cấm; danh sách đầy đủ nằm ở mục "Ranh giới sửa đổi" của `.agents/AGENTS.md`.

Thực hành khi giao việc cho tác tử trong Antigravity:
1. Trước khi giao: `python scripts/source_guard.py snapshot`.
2. Giao việc bằng câu lệnh nêu rõ phạm vi, ví dụ: "Tạo bài đọc Lesson 03 vào output/<môn>/..., không sửa bất kỳ tệp nào ngoài output/. Nếu pipeline lỗi thì báo lại, đừng sửa mã."
3. Sau khi xong: `python scripts/source_guard.py verify`. Mã thoát 1 liệt kê tệp đã bị đổi. Xem bằng `git diff`, giữ lại nếu chủ đích, hoàn tác bằng `git checkout -- <tệp>` nếu không.
4. Lệnh `python main.py ...` tự chạy kiểm tra này ở cuối lượt và in cảnh báo `[SOURCE GUARD]`.
5. Muốn sửa mã thật sự: yêu cầu riêng, làm trên nhánh hoặc worktree riêng, commit riêng từng mục đích.

Lưu ý khác:
- Kho kinh nghiệm tự học nay ghi vào `storage/lessons_learned_auto/SKILL.md` (không theo dõi bởi Git), không còn ghi vào `skills/lessons_learned/SKILL.md`. Muốn đưa một luật vào skill chính thức, chép tay và commit.
- Workflow `/resume` chỉ tóm tắt và hỏi; `/handoff` mới cập nhật `docs/PROJECT_STATE.md`.

## 10. Cấu hình và kiểm tra tự động bổ sung

- **Sandbox kiểm chứng mã.** Mặc định chạy trong tiến trình con ở thư mục tạm (Bash chỉ kiểm tra cú pháp, không thực thi). Muốn cô lập thật, đặt `SANDBOX_PROVIDER=docker` (hoặc `e2b`) trong `.env`; cần Docker đang chạy và image đã có sẵn, nếu không lỗi kéo image sẽ bị hiểu là mã bị lỗi.
- **Cổng cấu trúc mã trong pipeline.** Khi PM liệt kê khái niệm chưa dạy như `closure`, `class`, `this`, `lambda`, `decorator`, `comprehension`, các khối mã trong bài đọc, lab và bài tập bị quét; dùng cấu trúc bị cấm sẽ bị báo vi phạm phạm vi và kích hoạt sinh lại. Đây là bản tự động của `scripts/check_exercise_scope.py`.
- **Môn không viết mã.** Danh sách từ khóa nằm ở `config/course_nature.json` (mạnh/yếu/thiết kế). Thêm môn mới chỉ sửa tệp này.

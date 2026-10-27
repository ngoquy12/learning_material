# Harness dự án con 2: đặc tả môn và bộ lập lịch nhiệm vụ

Ngày: 2026-10-27. Thuộc lộ trình trong `2026-10-27-harness-design.md` (mục 3, dòng 2). Người dùng bỏ qua phần hỏi đáp và giao cho Claude chọn mặc định; mọi lựa chọn dưới đây là của Claude.

## 1. Vấn đề

Khi làm môn ReactJS và NodeJS, "đặc tả môn" là một tệp Markdown viết tay trong scratchpad (danh sách session, lesson, phạm vi được dạy, quy ước). Việc chia nhiệm vụ cho agent, theo dõi cái gì xong và cái gì còn thiếu đều nằm trong đầu người điều phối. Sau khi mất ngữ cảnh, người điều phối phải dò lại thư mục `output/` để biết tiến độ.

Dự án con 1 đã có cổng `verify` cho từng tài nguyên. Thiếu phần trên nó: một tệp đặc tả máy đọc được, và một lệnh suy ra danh sách nhiệm vụ, thứ tự, và trạng thái từ đặc tả cộng với kết quả `verify`.

## 2. Mục tiêu

1. **Đặc tả môn máy đọc được**: `course_spec.yaml` đặt ở gốc thư mục môn (`output/pms/<môn>/course_spec.yaml`). Kiểm bằng pydantic. Phần văn xuôi (quy ước, dữ liệu mẫu, phiên bản) vẫn ở Markdown, đặc tả chỉ trỏ tới nó.
2. **Lập kế hoạch**: từ đặc tả suy ra danh sách nhiệm vụ (một nhiệm vụ = một tài nguyên cần tạo), quan hệ phụ thuộc, và đợt (wave) theo thứ tự topo.
3. **Trạng thái suy ra, không đánh dấu tay**: trạng thái một nhiệm vụ = tài nguyên có tồn tại không + kết quả `verify` gần nhất. Không có lệnh "đánh dấu xong"; xong nghĩa là cổng đạt.
4. **Cho agent biết làm gì tiếp**: lệnh in các nhiệm vụ sẵn sàng (phụ thuộc đã xong, bản thân chưa xong) kèm đường dẫn đích, skill phải đọc, tệp ghi chú của môn.
5. **Dựng đặc tả nháp từ môn đã có** để hai môn đã duyệt dùng được ngay.

## 3. Không làm

- Không gọi LLM, không sinh nội dung, không tự chạy agent con. Harness chỉ lập lịch và kiểm.
- Không nối vào LangGraph `core/graph.py` (để sau; pipeline có thể gọi cùng thư viện).
- Không sổ ghi lần chạy chung (dự án con 5); chỉ lưu trạng thái hiện tại.
- Không thay đổi `verify` hay các cổng, trừ khi cần thêm loại tài nguyên "chỉ kiểm tồn tại" (mục 4.3).

## 4. Thiết kế

### 4.1 Tệp đặc tả

```yaml
course_id: nodejs_ai_driven          # trùng tên thư mục môn
title: NodeJS và Express với MySQL
tech_stack: javascript               # truyền cho cổng và cho agent
notes: course_spec.md                # tùy chọn, đường dẫn tương đối từ thư mục môn
defaults:
  lesson_resources: [reading, reading_questions, quiz_lesson]
sessions:
  - folder: "Session 01 - Ly thuyet NodeJS Express MySQL"
    kind: theory                     # theory | practice
    resources: [quiz_session, exercises, slide_html, slide_pptx, mindmap]
    exercises: 6                     # số bài tập, khi có `exercises`
    lessons:
      - folder: "Lesson 01 - Tong quan NodeJS va may chu HTTP"
        title: Tổng quan NodeJS và máy chủ HTTP
        allowed: [...]               # tùy chọn, phạm vi được dạy
        forbidden: [...]             # tùy chọn
        resources: [...]             # tùy chọn, ghi đè defaults.lesson_resources
  - folder: "Session 02 - Thuc hanh API voi Rikkei Learn"
    kind: practice
    resources: [lab, exercises]
    exercises: 6
    depends_on_sessions: [0]         # tùy chọn; mặc định practice phụ thuộc session theory ngay trước
```

Ràng buộc kiểm khi nạp: `course_id` không rỗng; tên thư mục session/lesson duy nhất trong môn; mỗi tên tài nguyên thuộc danh sách ở 4.2; `exercises` ≥ 1 khi có tài nguyên `exercises`; `depends_on_sessions` chỉ trỏ về session đứng trước. Lỗi trả thông báo tiếng Việt có vị trí (`sessions[1].lessons[0].resources`).

### 4.2 Tài nguyên và nhiệm vụ

| Tài nguyên trong đặc tả | Nhiệm vụ sinh ra (id) | Đích (tương đối thư mục môn) | Cổng | Skill | Phụ thuộc |
|---|---|---|---|---|---|
| `reading` (lesson) | `s01/l01/reading` | `<session>/<lesson>/Bai doc/reading.html` | `reading` | `reading_generator` | không |
| `reading_questions` (lesson) | `s01/l01/reading_questions` | `<session>/<lesson>/Cau hoi bai doc/reading_questions.md` | tồn tại | `reading_questions_generator` | reading của lesson |
| `quiz_lesson` (lesson) | `s01/l01/quiz_lesson` | `<session>/<lesson>/Quizz lesson/` | `quiz_lesson` | `quiz_generator` | reading của lesson |
| `quiz_session` | `s01/quiz_session` | `<session>/Quizz session/` | `quiz_session` | `quizz_session` | mọi reading của session |
| `exercises` (N bài) | `s01/exercise_1` … `s01/exercise_N` | `<session>/Bai tap/<i>_*/` (thư mục đầu tiên khớp `^<i>_`) | `exercise` | `exercise_generator` | mọi reading của session (theory) hoặc của các session phụ thuộc (practice) |
| `slide_html` | `s01/slide_html` | `<session>/Bai giang tren lop/slides.html` | `slide_html` | `slide_html` | mọi reading của session |
| `slide_pptx` | `s01/slide_pptx` | `<session>/Slide bai giang/*.pptx` (tệp đầu tiên) | `slide_pptx` | `slide_deck` | mọi reading của session |
| `mindmap` | `s01/mindmap` | `<session>/So do tu duy/mindmap.md` | tồn tại | `session_mindmap_compiler` | mọi reading của session |
| `lab` | `s02/lab` | `<session>/Bai thuc hanh/lab_guide.md` | `lab` | `lab_generator` | mọi reading của các session phụ thuộc |

- `s01`, `l01` là số thứ tự (1-based, hai chữ số) theo vị trí trong đặc tả, không phải trích từ tên thư mục.
- Đường dẫn khớp thư mục bằng `registry.normalize_name` (bỏ dấu, không phân biệt hoa thường) để môn cũ có tên có dấu vẫn dùng được: ví dụ đặc tả ghi `Bai doc` nhưng đĩa có `Bài đọc`.
- **Cổng "tồn tại"**: nhiệm vụ đạt khi tệp tồn tại và không rỗng. Không thêm cổng mới vào `GATES`; logic này nằm trong bộ lập lịch.
- **Đợt**: đợt của nhiệm vụ = 1 + đợt lớn nhất trong các phụ thuộc (không phụ thuộc → đợt 1).

### 4.3 Trạng thái

Mỗi nhiệm vụ có một trong các trạng thái:

| Trạng thái | Nghĩa |
|---|---|
| `missing` | đích chưa tồn tại |
| `failed` | đích tồn tại, cổng báo lỗi (mã 1) |
| `blocked_tool` | đích tồn tại, cổng bỏ qua vì thiếu công cụ (mã 2) |
| `done` | đích tồn tại, cổng đạt (mã 0) |

Một nhiệm vụ **sẵn sàng** khi trạng thái khác `done` và mọi phụ thuộc là `done`. `blocked_tool` không tính là `done` cho phụ thuộc.

Trạng thái được tính lại mỗi lần chạy `status`, bằng cách gọi `verify_path` (thư viện, không qua tiến trình con) trên từng đích tồn tại. Kết quả ghi vào `storage/harness/<course_id>/state.json`:

```json
{"course_id": "...", "spec_path": "...", "updated_at": "ISO", "runtime": false,
 "tasks": {"s01/l01/reading": {"status": "done", "kind": "reading", "target": "...", "wave": 1,
            "depends_on": [], "errors": 0, "warnings": 2, "first_error": "", "checked_at": "ISO"}}}
```

Tệp này là bộ nhớ đệm để `next` đọc nhanh; nguồn sự thật luôn là đĩa cộng `verify`.

### 4.4 Lệnh

Thêm các lệnh con vào CLI hiện có `python -m core.harness`:

```
python -m core.harness init <thư mục môn> [--force]      # dựng course_spec.yaml nháp từ thư mục đã có
python -m core.harness plan <spec.yaml> [--json]         # in nhiệm vụ theo đợt, không chạy cổng
python -m core.harness status <spec.yaml> [--runtime] [--json]   # chạy cổng, ghi state.json, in bảng
python -m core.harness next <spec.yaml> [--limit N] [--json]     # in nhiệm vụ sẵn sàng từ state.json (tự chạy status nếu chưa có hoặc đặc tả mới hơn)
```

- `init`: duyệt thư mục môn; mỗi thư mục con có tên bắt đầu bằng `Session` (sau chuẩn hóa) là một session theo thứ tự tên; trong đó mỗi thư mục bắt đầu bằng `Lesson` là một lesson; `kind` = `practice` nếu session có `Bai thuc hanh/`, ngược lại `theory`; `resources` và `exercises` suy ra từ những gì đang có trên đĩa; `title` của lesson = phần sau dấu ` - ` của tên thư mục; `course_id` = tên thư mục môn; `tech_stack` để trống. Không ghi đè tệp đã có trừ khi `--force`. In đường dẫn tệp đã ghi.
- `plan`: chỉ đọc đặc tả; in theo đợt, mỗi dòng `[đợt] id  kind  đích  ← phụ thuộc`.
- `status`: in tổng số theo trạng thái, rồi các nhiệm vụ không `done` kèm lỗi đầu tiên; mã thoát 0 nếu mọi nhiệm vụ `done`, 1 nếu có `failed`, 3 nếu còn `missing` mà không có `failed`, 2 nếu chỉ còn `blocked_tool`. (Mã 3 là mới, nghĩa "chưa xong", khác lỗi.)
- `next`: mỗi nhiệm vụ sẵn sàng in một khối: id, kind, đích tuyệt đối, skill `skills/<tên>/SKILL.md`, phụ thuộc, `notes` của môn, phạm vi `allowed`/`forbidden` của lesson nếu có, lệnh kiểm `python -m core.harness verify "<đích>" --kind <kind>` (thêm `--runtime` cho exercise). Thứ tự: đợt tăng dần rồi id. `--json` in mảng các khối.

### 4.5 Đặt mã

- `core/harness/course_spec.py`: mô hình pydantic và `load_spec(path) -> CourseSpec`.
- `core/harness/planner.py`: `build_tasks(spec, course_dir) -> list[Task]`, gán đợt, phát hiện chu trình (không thể xảy ra với quy tắc 4.2 nhưng vẫn kiểm).
- `core/harness/state.py`: `compute_status(spec_path, runtime=False) -> StateSnapshot`, đọc/ghi `state.json`, `ready_tasks(snapshot)`.
- `core/harness/spec_init.py`: `draft_spec(course_dir) -> dict`, ghi YAML.
- CLI: `core/harness/verify.py` hiện giữ `main`; tách bộ phân tích lệnh con thành `core/harness/cli.py` để `verify` và các lệnh mới cùng một chỗ, `__main__.py` gọi `cli.main`. Hành vi `verify` không đổi (các test hiện có phải đạt nguyên).

### 4.6 Ràng buộc

- Không hardcode tên môn, session, công nghệ; mọi thứ đến từ đặc tả hoặc đĩa.
- Không ghi gì vào thư mục môn ngoài `course_spec.yaml` khi chạy `init`. Trạng thái và báo cáo chỉ ghi vào `storage/`.
- Thông báo tiếng Việt có dấu, không emoji. Test kín: dựng môn giả trong `tmp_path`, không đọc `output/`.
- `yaml.safe_load` / `yaml.safe_dump` (PyYAML 6 có sẵn), pydantic 2 (có sẵn).
- Hai môn đã duyệt: `init` rồi `status` trên `nodejs_ai_driven` và `reactjs_ai_driven` phải cho mọi nhiệm vụ có cổng là `done` ở chế độ tĩnh (đây là kiểm thử thủ công cuối cùng, không phải test đơn vị).

## 5. Để người làm tự quyết

Tên hàm phụ, cách in bảng, thứ tự trường trong YAML nháp, cách so "đặc tả mới hơn state" (mtime là đủ).

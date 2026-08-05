# Phân Tích Chuyên Sâu Các Thách Thức Kỹ Thuật Trước Khi Triển Khai
*(Deep-Dive & Technical Preparations for Syllabus Agent Implementation)*

Để đảm bảo Agent hoạt động chính xác theo quy chuẩn Đại học của tệp [PM_PTIT_2026_Chương trình đào tạo.xlsx](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/CLO-PLO/PM_PTIT_2026_Chương-trình-đào-tạo.xlsx) và không mắc lỗi logic sư phạm, chúng ta cần đi sâu giải quyết **13 bài toán thực chiến** sau đây trước khi đặt những dòng code đầu tiên.

---

## Bài Toán 1: Định Lượng Toán Học Cho Hệ Số Nhịp Độ Học (Pacing Index Math)

**Thách thức**: Làm sao dịch chuyển hồ sơ sinh viên định tính (Ví dụ: "Beginner, Non-IT") thành số lượng buổi học và bài học một cách toán học, thay vì để AI tự đoán tự do?

### Giải pháp thiết kế:
Chúng ta thiết lập một hệ thống **Hệ số Điều chỉnh Sư phạm (Pedagogical Adjustment Factors)** cố định trong mã nguồn làm tham chiếu cho AI:

1. **Hệ số Trình độ Đầu vào ($F_{\text{entry}}$)**:
   - `beginner`: $0.8$
   - `intermediate`: $1.0$
   - `advanced`: $1.2$
2. **Hệ số Nền tảng ($F_{\text{background}}$)**:
   - `non-it` (chuyển ngành): $0.8$
   - `it-student` (chuyên ngành): $1.0$
   - `professional` (đã đi làm): $1.15$
3. **Mật độ Khái niệm Cơ sở ($C_{\text{base}}$)**:
   - Mặc định: $3.0$ khái niệm kỹ thuật cốt lõi / Session Lý thuyết.

### Công thức tính số lượng khái niệm mục tiêu mỗi buổi ($C_{\text{target}}$):
$$C_{\text{target}} = C_{\text{base}} \times F_{\text{entry}} \times F_{\text{background}} \times \text{Speed}_{\text{student}}$$

- **Trường hợp A (Sinh viên chuyển ngành, Beginner, Speed=0.95)**:
  $$C_{\text{target}} = 3.0 \times 0.8 \times 0.8 \times 0.95 = 1.82 \text{ khái niệm/buổi}$$
  ➔ *Hành động của Agent*: Chia nhỏ 1 buổi chuẩn (3 khái niệm) thành 1.6 buổi, đồng thời tự động chèn thêm các buổi Thực hành ôn luyện xen kẽ.
- **Trường hợp B (Sinh viên CNTT, Intermediate, Speed=1.1)**:
  $$C_{\text{target}} = 3.0 \times 1.0 \times 1.0 \times 1.1 = 3.3 \text{ khái niệm/buổi}$$
  ➔ *Hành động của Agent*: Đẩy nhanh tốc độ học, cho phép nhồi thêm các kiến thức nâng cao vào cùng một buổi học.

---

## Bài Toán 2: Xử Lý Ô Gộp (Merged Cells) Của Excel Trong `curriculum_parser.py`

**Thách thức**: Tệp Excel PTIT 2026 sử dụng rất nhiều ô gộp (Merged Cells) cho cột Học kỳ (Semester), Mã môn, Môn học, và Session. Khi dùng thư viện `openpyxl` đọc thông thường, chỉ có ô góc trên bên trái của vùng gộp chứa giá trị, tất cả các ô còn lại trong vùng gộp sẽ trả về `None`. Điều này khiến các dòng Lesson con bị mất liên kết với Session và Môn học tương ứng.

### Giải pháp kỹ thuật (Cơ chế Fill-Forward):
Chúng ta phải nâng cấp thuật toán đọc dòng của bộ Parser: Thiết lập các biến trạng thái tạm thời để "kéo dãn" giá trị của dòng trên xuống dòng dưới nếu phát hiện giá trị `None` ở các cột gộp:

```python
def parse_with_merged_cell_recovery(sheet):
    current_semester = ""
    current_course_code = ""
    current_course_name = ""
    current_session_id = ""
    current_session_title = ""
    
    rows = list(sheet.iter_rows(values_only=True))
    for row in rows[4:]:  # Duyệt từ hàng dữ liệu
        # Đọc và giữ lại giá trị nếu có, nếu không thì lấy giá trị đã lưu trước đó
        if row[2] is not None: current_semester = str(row[2]).strip()
        if row[1] is not None: current_course_code = str(row[1]).strip()
        if row[3] is not None: current_course_name = str(row[ mon_idx ]).strip()
        
        # Áp dụng cơ chế này cho cả Session và Lesson
        # ...
```

---

## Bài Toán 3: Prompt Engineering Cho Ma Trận Ánh Xạ PLO-CLO Chặt Chẽ

**Thách thức**: LLM rất dễ sinh ra các ánh xạ ảo (Hallucinated PLO) hoặc ánh xạ bừa bãi (CLO nào cũng ánh xạ vào toàn bộ PLOs). Chúng ta cần thiết lập hàng rào kỹ thuật Prompt chặt chẽ.

### Giải pháp kỹ thuật:
Sử dụng cấu trúc **System Instruction** giới hạn cứng và định dạng trả về qua **Structured Outputs (Pydantic Schema)**:

```python
class CloToPloMapping(BaseModel):
    clo_id: str = Field(description="Mã chuẩn đầu ra môn học, ví dụ: CLO1")
    mapped_plos: List[str] = Field(
        description="Danh sách các mã PLO được đóng góp trực tiếp. Chỉ được chọn từ danh sách PLOs đầu vào!"
    )
    rational: str = Field(
        description="Giải thích ngắn gọn cơ sở sư phạm tại sao CLO này đóng góp vào PLO này."
    )
```

**Mẫu Prompt ràng buộc cứng**:
> "Bạn CHỈ được phép chọn các mã PLO nằm trong danh sách đầu vào sau: {list_plos}. Tuyệt đối không tự sinh ra mã PLO mới. Mỗi CLO chỉ được ánh xạ sang tối đa 2 PLOs đóng góp trực tiếp nhất."

---

## Bài Toán 4: Cơ Chế Tích Hợp Đồ Thị Antigravity Mà Không Làm Hỏng Pipeline Hiện Tại

**Thách thức**: Làm sao để khi chạy lệnh `python main.py` cho các môn học cũ đã có sẵn file PM tĩnh, hệ thống vẫn chạy bình thường; còn khi cấu hình thiết kế môn học mới, hệ thống tự động kích hoạt Agent thiết kế chương trình?

### Giải pháp kỹ thuật:
Chúng ta phân rã cấu hình khởi chạy qua cờ lệnh (CLI flags):
- **Cờ `--pm`**: Đường dẫn tới file PM tĩnh (chế độ cũ ➔ bỏ qua bước sinh PM, chạy thẳng pipeline sinh học liệu).
- **Cờ `--generate-pm`**: Kích hoạt **Syllabus PM Generator Agent (SPGA)**. Nhận đầu vào là file cấu hình hồ sơ môn học/sinh viên, tự động sinh ra file PM đạt chuẩn, ghi đĩa, sau đó tự động nạp tiếp vào pipeline hiện tại để sinh học liệu.

---

## Bài Toán 5: Cơ Chế Đồng Bộ & Cập Nhật Lũy Tiến Khi Thay Đổi Khung Môn Học (Incremental Sync & Cascading Invalidation)

**Thách thức**: Chương trình đào tạo không bao giờ cố định. Ví dụ: Ban đầu môn *Phát triển ứng dụng web với FastAPI* được thiết kế là 20 buổi với mục tiêu xây dựng API RESTful. Sau đó, Ban Giám đốc đổi yêu cầu thành 22 buổi và dịch chuyển mục tiêu sang xây dựng API GraphQL.
Làm sao hệ thống tự động đồng bộ lại học liệu mà:
1. **Không phải sinh lại từ đầu** 20 buổi học cũ (gây tốn tokens và mất bản sửa tay của người dùng).
2. **Tự động dịch chuyển (Shift)** các buổi học khi thời lượng tăng/giảm.
3. **Cập nhật nội dung có mục tiêu (Cascading Invalidation)**: Chỉ viết lại các buổi học/bài học bị ảnh hưởng trực tiếp bởi thay đổi mục tiêu (GraphQL).

### Giải pháp kỹ thuật:

#### 1. Thuật toán so khớp Dịch chuyển Buổi học (Pacing Shift & Remapping Algorithm)
Khi cấu trúc số buổi thay đổi (ví dụ 20 ➔ 22 buổi), hệ thống không xóa thư mục cũ mà sử dụng thuật toán so khớp **LCS (Longest Common Subsequence)** hoặc so khớp chuỗi (String Similarity) để ánh xạ các buổi cũ sang buổi mới:
- AI thiết kế chương trình mới sẽ tạo ra danh sách buổi mới.
- Hệ thống quét đĩa, đối chiếu tên thư mục cũ.
- Thực hiện **Auto-Rename** thư mục trên đĩa (sử dụng hàm `get_or_rename_sanitized_folder` hiện tại) để di chuyển vị trí bài học.
  *Ví dụ*: Buổi 19 (Thực hành tổng hợp) cũ dịch chuyển thành Buổi 21 mới ➔ Đổi tên thư mục `Session 19` thành `Session 21`.

#### 2. Cơ chế Hủy hiệu lực Lan truyền (Cascading Invalidation)
Để cập nhật đúng mục tiêu (RESTful ➔ GraphQL), hệ thống sử dụng một lớp giám sát phiên bản **Dependency Tracker**:
- Mỗi Session/Lesson ghi nhận một chữ ký mã hóa Hash (`content_hash`) đại diện cho các trường: `title`, `details`, `allowed_scope`, và `expected_output` lưu trong file `.state` checkpoint.
- Khi chương trình học mới được sinh ra:
  - Hệ thống tính toán `content_hash` mới của từng bài học và đối chiếu với hash cũ.
  - **Trường hợp A (Không đổi)**: `content_hash` trùng khớp ➔ Giữ nguyên trạng thái `Approved` trong `AgentState.artifacts_status` ➔ Bỏ qua không sinh lại.
  - **Trường hợp B (Thay đổi nội dung)**: `content_hash` lệch nhau ➔ Tự động chuyển đổi trạng thái:
    ```python
    state["artifacts_status"]["html"] = "Outdated"
    state["artifacts_status"]["slide"] = "Outdated"
    state["artifacts_status"]["video_script"] = "Outdated"
    ```
  - **Trường hợp C (Buổi học mới tinh)**: Trạng thái là `Pending` ➔ AI kích hoạt sinh mới.

#### 3. Kỹ thuật LLM Refactoring thông minh (AI Update Injection)
Đối với các bài học bị đánh dấu là `Outdated` (ví dụ chuyển RESTful sang GraphQL):
- Chúng ta không bắt LLM viết lại 100% bài học. Thay vào đó, Creator Agent nhận đầu vào gồm:
  - Bản cũ đang có trên đĩa (đọc từ đĩa qua cơ chế Sync).
  - Yêu cầu thay đổi mục tiêu (Ví dụ: "Thay thế RESTful API bằng GraphQL Query/Mutation").
- LLM sẽ chạy ở chế độ **Refactor Mode** (chỉ sửa các phần liên quan đến kỹ thuật, giữ nguyên bố cục đặt vấn đề, các bối cảnh doanh nghiệp và cấu trúc format có sẵn). Điều này giảm 70% lượng tokens tiêu thụ và giữ lại các chỉnh sửa thủ công có giá trị của con người.

---

## Bài Toán 6: Trộn Lẫn Phiên Bản Thư Viện Kỹ Thuật (Tech-Stack Version Hallucination)

- **Thách thức (Rất Cao)**: LLM thường xuyên trộn lẫn cú pháp của các phiên bản khác nhau (Ví dụ: Dùng cú pháp Pydantic v1 trong FastAPI dự án chạy Pydantic v2; hoặc kết hợp cú pháp LangChain cũ `LLMChain` với cú pháp LCEL mới). 
- **Giải pháp**: Nạp sơ đồ phiên bản thư viện chính xác (Ví dụ: `fastapi==0.100.0`, `pydantic>=2.0`) vào System Prompt của Creator Agent làm luật cứng để đảm bảo mã nguồn tự sinh không vấp lỗi cú pháp runtime khi sinh viên thực thi.

---

## Bài Toán 7: Rò Rỉ Tri Thức Gián Tiếp Qua Ví Dụ (Indirect Concept Leakage)

- **Thách thức (Cao)**: Dù đã khai báo `forbidden_scope` cho một buổi học (Ví dụ: Cấm hàm nâng cao Lambda), LLM vẫn vô tình sử dụng cú pháp cấm này trong phần giải thích hoặc phần comment của ví dụ mã nguồn (Ví dụ: dùng `map(lambda x: x*2, list)` để giải thích vòng lặp đơn giản).
- **Giải pháp**: Xây dựng bộ quét Regex phân tích cú pháp mã nguồn (AST Parser) để quét và chặn các node cú pháp cấm trong code trước khi đưa ra phê duyệt bản thảo.

---

## Bài Toán 8: Vòng Lặp Phản Biện Vô Hạn (Agent Critique Deadlock)

- **Thách thức (Cao)**: Creator Agent sinh code ➔ Reviewer Agent phát hiện lỗi và Reject ➔ Creator Agent cố sửa lỗi đó nhưng vô tình làm hỏng phần khác ➔ Reviewer tiếp tục Reject. Hai agent này bị rơi vào vòng lặp phản biện vô hạn, làm treo hệ thống và tiêu tốn hàng triệu Tokens API.
- **Giải pháp**: Cài đặt ngưỡng số lần thử tối đa (Max Attempts = 3). Nếu vượt quá, kích hoạt fallback: Ghi đĩa bản nháp tốt nhất và báo cáo cảnh báo cho con người vào xử lý thủ công (Human-in-the-loop).

---

## Bài Toán 9: Phá Vỡ Cấu Trúc JSON Đầu Ra Khi Sinh Học Liệu Độ Dài Lớn (JSON Schema Fragility)

- **Thách thức (Trung bình - Cao)**: Khi yêu cầu sinh học liệu dài (800 - 1,200 từ) lồng trong một trường JSON cụ thể, LLM rất dễ gặp lỗi quên đóng dấu ngoặc kép `"`, dấu ngoặc nhọn `}`, hoặc thoát ký tự xuống dòng `\n` sai quy cách.
- **Giải pháp**: Sử dụng thư viện parse JSON mềm dẻo (`robust_json_parse` thông qua `regex` và `ast.literal_eval` đã triển khai) kết hợp với công nghệ Structured Outputs của Gemini/OpenAI để ép định dạng từ tầng API.

---

## Bài Toán 10: Quá Tải Ngữ Cảnh Trên Các Môn Học Dài (Context Window Saturation)

- **Thách thức (Trung bình)**: Với các môn học dài 25-30 buổi, khi thiết kế buổi thứ 25, việc nhồi toàn bộ lịch sử 24 buổi trước kèm đống lý thuyết và code mẫu vào prompt để AI kiểm tra trùng lặp sẽ làm tràn cửa sổ ngữ cảnh (Context Window) hoặc làm chậm tốc độ phản hồi.
- **Giải pháp**: Sử dụng cơ chế nạp ngữ cảnh thu gọn (`get_context_curriculum` chỉ lấy buổi trước/sau và ma trận tóm tắt tri thức) thay vì nạp toàn bộ curriculum thô.

---

## Bài Toán 11: Bất Đồng Bộ Thuật Ngữ Giữa Các Loại Học Liệu (Terminology Inconsistency)

- **Thách thức (Trung bình)**: Creator Agent viết Bài đọc dùng từ "Khởi tạo đối tượng", Slide Agent dùng từ "Tạo instance", Video Script Agent lại dịch thành "Sinh đối tượng thực thể" gây hoang mang cho người học.
- **Giải pháp**: Định nghĩa một từ điển thuật ngữ chuẩn (Glossary) trong file SSOT và chia sẻ chung từ điển này cho tất cả các Agent nhánh con.

---

## Bài Toán 12: Trực Quan Hóa Hoạt Họa JS Tự Sinh Thiếu Ổn Định (Visualizer Code Instability)

- **Thách thức (Trung bình)**: Mã nguồn JavaScript do LLM sinh ra để điều khiển visualizer vẽ sơ đồ động trên trình duyệt thường bị lỗi tham chiếu phần tử DOM không tồn tại, lỗi vòng lặp vô hạn hoặc lỗi syntax JS.
- **Giải pháp**: Định nghĩa các Class Base JS dùng chung có sẵn trong hệ thống (`InteractiveVisualizerEngine`), LLM chỉ được phép cấu hình dữ liệu đầu vào (config payload) thay vì tự viết code logic JS điều khiển từ đầu.

---

## Bài Toán 13: Cạn Kiệt Hạn Mức API Khi Chạy Song Song Nhiều Nhánh (Rate Limit Exhaustion - 429)

- **Thách thức (Thấp)**: Cơ chế chạy song song các nhánh dẫn xuất còn lại (Slide, Quiz, Mindmap - sau khi đã loại bỏ Video Script) gọi LLM cùng một thời điểm có thể chạm trần giới hạn hạn mức của nhà cung cấp API.
- **Giải pháp**: Sử dụng semaphore khóa Concurrent Limiter (`MAX_CONCURRENT_LLM_CALLS = 4` đã triển khai trong `core/llm.py`) để điều phối hàng đợi yêu cầu an toàn.

---

## 📅 Kế Hoạch Các Bước Triển Khai Tiếp Theo (Action Plan)

1. **Bước 1: Nâng cấp Parser (`cli/curriculum_parser.py`)**:
   - Viết hàm `parse_program_structure_from_ptit` hỗ trợ đọc đa sheet và phục hồi ô gộp.
   - Thêm unit test kiểm tra việc đọc file Excel PTIT 2026 xem đã lấy đủ 26 môn học và các lessons con chưa.
2. **Bước 2: Xây dựng Module Agent mới (`agents/pm_generator_agent.py`)**:
   - Định nghĩa Pydantic Schemas cho đầu vào (Student Profile, PLO, CLO) và đầu ra (Syllabus PM).
   - Viết prompt hai giai đoạn cho SCAA.
3. **Bước 3: Tích hợp vào Đồ thị tuần tự (`core/graph.py`)**:
   - Thêm node `generate_syllabus_pm` và cấu hình cờ kích hoạt trong `cli/runner.py`.
4. **Bước 4: Kiểm thử liên kết**:
   - Chạy giả lập sinh chương trình học môn `IT-106` cho đối tượng `beginner/non-it` xem AI có tự động chia nhỏ bài học và chèn thêm các buổi thực hành không.

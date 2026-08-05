# Báo Cáo Phân Tích Chi Tiết Chương Trình Đào Tạo PTIT 2026 (KS26)
*(Góc nhìn Quản lý Giáo dục & Kiến trúc sư AI Agent)*

Chúng tôi đã thực hiện cào dữ liệu và phân tích cấu trúc tệp Excel [PM_PTIT_2026_Chương trình đào tạo.xlsx](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/CLO-PLO/PM_PTIT_2026_Chương-trình-đào-tạo.xlsx). Đây là một chương trình khung đào tạo kỹ sư công nghệ chuyên sâu theo mô hình **AI-Native & Multi-Agent (Kỷ nguyên AI 2026)** có quy mô và tính nhất quán học thuật rất cao.

Dưới đây là báo cáo phân tích chi tiết về mặt **Thiết kế sư phạm** và **Phương án kỹ thuật tích hợp AI**.

---

## 1. Cấu Trúc Tổng Quan File Excel

Tệp Excel bao gồm **11 Sheets** phân tách rõ ràng thành 2 nhóm nhiệm vụ chính:

1. **Khung chương trình cấp Học kỳ (Kỳ I ➔ Kỳ V)**:
   - `KS26 - Khung chương trình - Kỳ I - Nền tảng`
   - `KS26 - Khung chương trình - Kỳ II - Nền tảng`
   - `KS26 - Khung chương trình - Kỳ III - Chuyên ngành`
   - `KS26 - Khung chương trình - Kỳ IV - Chuyên ngành`
   - `KS26 - Khung chương trình - Kỳ V - Chuyên ngành`
   ➔ *Nhiệm vụ*: Quản lý mục tiêu vĩ mô (**PLO**), liên kết danh sách môn học, chuẩn đầu ra cấp môn (**CLO**), hình thức khảo thí và phân bổ quỹ thời gian (Lý thuyết, Thực hành, Mini Project, Project, Exam).
2. **Chi tiết môn học cấp Module (IT-101 ➔ IT-106)**:
   - Các sheet từ `IT-101` đến `IT-106` chứa kịch bản phân bổ chi tiết của từng buổi học:
     - `IT-101 Nhập môn CNTT` (23 Sessions)
     - `IT-102 Kỹ năng prompting với AI` (10 Sessions)
     - `IT-103 Thiết kế giao diện người dùng` (10 Sessions)
     - `IT-104 Phát triển giao diện web` (23 Sessions)
     - `IT-105 Quản lý phiên bản với GIT` (10 Sessions)
     - `IT-106 Phát triển ứng dụng web` (25 Sessions)

---

## 2. Phân Tích Sư Phạm & Tính Kế Thừa Tri Thức (Knowledge Inheritance)

Điểm đắt giá nhất của chương trình đào tạo **KS26** là **Chuỗi Kế Thừa Tri Thức Đóng (Closed Knowledge Loop)**. Các môn học không đứng độc lập mà liên kết chặt chẽ theo mô hình thiết kế ngược (Backward Design):

### 2.1. Bản đồ Kế thừa Kỳ I (Kiến thức nền tảng ➔ Fresher Frontend Developer)
- **IT-101 (Nhập môn CNTT)**: Setup hệ điều hành, phím tắt, sơ đồ file system và quy tắc đặt tên biến (`camelCase`, `snake_case`).
- **IT-102 (AI Prompting)**: Dạy sinh viên tư duy dùng AI làm "cặp bài trùng" để học tập và giải quyết lỗi.
- **IT-103 (UI/UX Figma)**: Sinh viên dùng prompt (IT-102) lên ý tưởng và thiết kế bản vẽ Website Ecommerce trên Figma.
- **IT-104 (HTML/CSS)**: Sinh viên xuất thông số màu sắc/kích thước từ Figma (IT-103), kết hợp AI để viết code HTML/CSS hoàn thiện giao diện tĩnh.
- **IT-105 (Git/GitHub)**: Gom toàn bộ code từ IT-104, khởi tạo Git và quản lý phiên bản nhóm trên GitHub.
- **IT-106 (JavaScript)**: Kế thừa toàn bộ giao diện tĩnh từ IT-104, lập trình các tương tác logic động và kết nối dữ liệu API.

### 2.2. Lộ trình phát triển Chuyên ngành (Kỳ II ➔ Kỳ V)
- **Kỳ II (Web Fullstack)**:
  - Sinh viên dùng kỹ thuật phân tích nghiệp vụ (`IT-201` - viết tài liệu SRS) ➔ Thiết kế Database PostgreSQL (`IT-202`) ➔ Viết logic cốt lõi bằng Python OOP (`IT-203`) ➔ Đóng gói thành RESTful API Server với FastAPI (`IT-204`) kết hợp AI trợ giúp (`IT-205`).
- **Kỳ III (AI & RAG Engine)**:
  - Cung cấp nền tảng Toán học cho AI (`IT-301`) và cấu trúc giải thuật tìm kiếm (`IT-302`) ➔ Thiết lập CSDL Vector bằng pgvector và LangChain (`IT-304`) kết hợp mô hình cục bộ Hugging Face (`IT-303`) để tạo ra Trợ lý AI hỏi đáp tài liệu nội bộ.
- **Kỳ IV (Autonomous Agents & Multi-Agent)**:
  - Cấu trúc Đồ thị DAG (`IT-401`) ➔ Xây dựng tác nhân tự hành đơn lẻ biết gọi tool và tích hợp MCP Server (`IT-402`) ➔ Nối các tác nhân lại thành mạng lưới Đa tác nhân với LangGraph (`IT-403`) ➔ Đóng gói container Docker DevOps (`IT-404`).
- **Kỳ V (Enterprise Operations - LLMOps)**:
  - Cài đặt Redis Semantic Caching, tối ưu hóa chi phí API và đo lường PostHog (`IT-501`) ➔ Bảo mật chống Prompt Injection bằng NeMo Guardrails và đưa dockerized app lên AWS Cloud (`IT-502`).

---

## 3. Phân Tích Sự Khác Biệt Của File Excel Mới Với Parser Hiện Tại

Hệ thống Elearning Content Factory hiện tại đang sử dụng bộ phân tích [cli/curriculum_parser.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/cli/curriculum_parser.py) để đọc tệp Excel. Cần ghi nhận các điểm khác biệt lớn để nâng cấp:

| Đặc tính | Cấu trúc Parser Hiện Tại | Cấu trúc Tệp Excel PTIT 2026 Mới |
| :--- | :--- | :--- |
| **Số lượng Sheet** | Đọc 1 sheet duy nhất (thường là sheet mặc định hoạt động). | Đọc và liên kết **nhiều sheets** (Khung tổng quan kỳ học + Từng sheet module môn học chi tiết). |
| **Cấu trúc Cấp bậc** | Phẳng: 1 hàng trong Excel chứa cả thông tin Session và Lesson tương ứng. | Cấu trúc khối (Block-based): 1 hàng chính định nghĩa Session, các hàng con bên dưới đại diện cho các Lessons (STT trống, chỉ có chỉ số Lesson và mô tả chi tiết ở Col 5 & Col 6). |
| **Loại hình Buổi học** | Giả định mọi buổi học đều có bài đọc lý thuyết, slide, quiz. | Phân loại rõ ràng qua cột "Hình thức học" (Lý thuyết có bài đọc nhỏ; Thực hành/Mini project/Exam không chia nhỏ bài học và không sinh học liệu dạng đọc). |
| **Chuẩn đầu ra vĩ mô** | Chưa khai thác PLO/CLO ở tầng chiến lược chương trình. | Tích hợp sẵn ma trận PLO ở phần đầu của Khung kỳ học và các CLO chi tiết ứng với từng Mã môn. |

---

## 4. Phương Án Kỹ Thuật Nâng Cấp Parser & Đồ Thị Điều Phối

Để hệ thống thích ứng tự động với tệp Excel PTIT 2026 mới mà không làm phá vỡ kiến trúc cũ, chúng tôi đề xuất kế hoạch nâng cấp như sau:

### 4.1. Định nghĩa Cấu trúc Trạng thái Đa Chương Trình (ProgramState Schema)
Thêm các thực thể mới để quản lý chương trình học ở cấp độ cao:

```python
class LessonSchema(BaseModel):
    lesson_id: str
    title: str
    details: str
    note: Optional[str] = ""

class SessionSchema(BaseModel):
    session_num: int
    hinh_thuc: str  # Lý thuyết | Thực hành | Mini project | Project | Exam
    title: str
    lessons: List[LessonSchema] = []

class CourseSchema(BaseModel):
    course_id: str  # Ví dụ: IT-101
    course_name: str
    clos: List[str] = []
    sessions: List[SessionSchema] = []

class ProgramSemesterSchema(BaseModel):
    semester_id: str  # Ví dụ: SEM I
    plos: List[str] = []
    courses: List[CourseSchema] = []
```

### 4.2. Viết lại Cơ chế Parsing Khối (Block-Based Parsing) trong `curriculum_parser.py`
Nâng cấp hàm `parse_all_sessions` để xử lý các khối Session/Lesson lồng nhau:

```python
def parse_block_based_sheet(sheet):
    sessions = []
    current_session = None
    
    # Bắt đầu đọc từ hàng 4 (bỏ qua tiêu đề cột)
    for row in sheet.iter_rows(min_row=4, values_only=True):
        if not any(row):
            continue
            
        stt = row[0]
        hinh_thuc = row[1]
        session_title = row[4]
        lesson_idx = row[5]
        lesson_title = row[6]
        
        # Nếu có STT -> Khởi tạo một Session mới
        if stt is not None and str(stt).strip() != "":
            current_session = {
                "session_id": f"Session {str(stt).strip()}",
                "session_type": str(hinh_thuc).strip() if hinh_thuc else "Lý thuyết",
                "title": str(session_title).strip() if session_title else str(hinh_thuc).strip(),
                "lessons": []
            }
            sessions.append(current_session)
            
        # Nếu có chi tiết bài học và STT trống -> Đây là Lesson con của Session hiện tại
        if lesson_title and str(lesson_title).strip() and current_session:
            current_session["lessons"].append({
                "lesson_id": f"Lesson {str(lesson_idx).strip()}" if lesson_idx else "",
                "title": str(lesson_title).strip(),
                "details": str(lesson_title).strip()  # Đối với file PTIT, nội dung nằm ở cột này
            })
            
    return sessions
```

### 4.3. Bổ sung Strategic Curriculum Agent (SCAA) để tự động thiết kế
Sau khi Parser cào được cấu trúc thô từ Excel, SCAA sẽ:
1. Đọc danh sách CLOs và PLOs từ sheet Khung chương trình.
2. Đối chiếu hiện trạng sinh viên (nạp từ biến môi trường hoặc file config).
3. Tinh chỉnh các nội dung lý thuyết (chèn các bài đọc cơ chế nâng cao nếu sinh viên chuyên ngành CNTT, hoặc đơn giản hóa bằng sơ đồ trực quan nếu sinh viên chuyển ngành).
4. Tự động xuất ra file `syllabus.json` đã chuẩn hóa hoàn toàn cấu trúc, sẵn sàng kích hoạt các Creators.

---

## 5. Kết Luận

Tệp Excel **PM_PTIT_2026_Chương trình đào tạo.xlsx** là một tài liệu chuẩn mực mẫu về thiết kế sư phạm kỹ thuật số. Việc hệ thống nâng cấp để thích ứng tự động với cấu trúc này sẽ mang lại 2 lợi ích vượt trội:
- **Tự động hóa hoàn toàn luồng biên dịch**: Phòng Đào tạo chỉ cần thiết kế tệp Excel theo cấu trúc này, AI Agent sẽ tự động cào và biên dịch toàn bộ học liệu (HTML, Slide, Video, Quiz) mà không cần lập trình viên can thiệp thủ công.
- **Tính nhất quán tri thức vĩ mô**: Đảm bảo sự kế thừa chặt chẽ giữa các môn học, tránh tình trạng môn học sau giảng dạy các kiến thức sinh viên chưa từng được học ở các môn học trước.

Bản báo cáo phân tích này đề xuất hướng triển khai thực tế. Chúng tôi có thể bắt tay vào nâng cấp mã nguồn `cli/curriculum_parser.py` ngay khi nhận được tín hiệu phê duyệt.

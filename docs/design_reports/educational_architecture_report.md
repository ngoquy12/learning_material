# Báo Cáo Phân Tích & Đề Xuất Nâng Cấp Hệ Thống Thiết Kế Chương Trình Học
*(Góc nhìn Quản lý Giáo dục & Kiến trúc sư AI Agent)*

Chào Ban Giám đốc và các chuyên gia,

Dưới góc nhìn của một **Quản lý Giáo dục (Academic Manager)** kết hợp với **Kiến trúc sư Giải pháp AI (AI Solution Architect)**, yêu cầu nâng cấp hệ thống từ việc "sinh học liệu cho môn học đơn lẻ" lên "thiết kế chương trình học tổng thể cấp độ đa chương trình (Multi-Program) dựa trên năng lực đầu ra và hiện trạng sinh viên" là một bước chuyển dịch chiến lược tất yếu. 

Nâng cấp này đưa hệ thống tiếp cận triết lý giáo dục hiện đại: **Giáo dục dựa trên chuẩn đầu ra (Outcome-Based Education - OBE)** và **Thiết kế ngược (Backward Design)**.

Dưới đây là bản phân tích chi tiết và đề xuất giải pháp kỹ thuật nâng cấp hệ thống.

---

## Phần 1: Phân Tích Sư Phạm & Quản Lý Giáo Dục

Việc chia nhỏ bài học (Lesson) trước đây thường dựa vào cảm tính hoặc sao chép rập khuôn mục lục sách giáo khoa. Cách tiếp cận mới yêu cầu AI thiết kế dựa trên các dữ liệu đầu vào định lượng và định tính:

### 1. Phân tích các dữ liệu đầu vào (Core Inputs)
- **Hiện trạng sinh viên (Student Entry Profile)**:
  - *Ý nghĩa sư phạm*: Xác định mức độ sẵn sàng (readiness) và khả năng tiếp thu. Một sinh viên chuyển ngành (Non-IT) cần lộ trình kéo giãn các bài học nền tảng, tăng thời lượng thực hành cầm tay chỉ việc; trong khi sinh viên chuyên ngành CNTT cần đẩy nhanh phần cú pháp cơ bản và tập trung vào kiến trúc/tối ưu hóa.
  - *Tác động định lượng*: Điều chỉnh hệ số phức tạp nhận thức (Cognitive Complexity Coefficient - CCC) để co giãn số lượng bài học và phân bổ thời lượng phù hợp.
- **PLO (Program Learning Outcome - Chuẩn đầu ra cấp chương trình)**:
  - *Ý nghĩa sư phạm*: Đây là mục tiêu tối thượng mà một chương trình đào tạo (ví dụ: "Lập trình viên Full-Stack") cam kết với xã hội. Mọi môn học trong chương trình phải là một viên gạch đóng góp vào PLO này.
- **CLO (Course Learning Outcome - Chuẩn đầu ra cấp môn học)**:
  - *Ý nghĩa sư phạm*: Cụ thể hóa PLO vào từng môn học. CLO phải đo lường được (theo Bloom's Taxonomy từ Nhận biết -> Vận dụng -> Phân tích -> Sáng tạo).
- **Phân bổ thời lượng (Time Allocation Constraints)**:
  - *Thời lượng tự học (Self-study)*: Đo lường tải nhận thức độc lập (Independent Cognitive Load).
  - *Thời lượng trên lớp (In-class)*: Thời gian tương tác trực tiếp với Giảng viên, tập trung giải quyết bẫy lỗi và tư duy phản biện.
  - *Thời lượng bài tập (Practice/Homework)*: Thời gian rèn luyện kỹ năng thực chiến (Skill-building).

### 2. Nguyên lý đề xuất đầu ra của AI (Backward Planning Model)
Thay vì chia lesson theo cảm tính, AI sẽ chạy thuật toán tối ưu hóa phân bổ dựa trên:
1. **Liên kết cấu trúc chuẩn đầu ra (PLO-CLO Alignment)**: Phân rã các CLO thành các mục tiêu nhỏ hơn (Micro-Outcomes).
2. **Định luật Tải nhận thức (Cognitive Load Guard)**:
   - Tổng thời lượng thực tế của một buổi (Session) = Trên lớp + Tự học + Bài tập.
   - AI sẽ chia nhỏ kiến thức thành các hạt tri thức (Knowledge Units) sao cho tổng tải nhận thức của mỗi Lesson không vượt quá giới hạn chịu đựng của nhóm đối tượng sinh viên hiện tại.
3. **Phân bổ phân phối (Spaced Repetition & Pacing)**: AI tính toán khoảng cách và mật độ bài tập thực hành xen kẽ lý thuyết.

---

## Phần 2: Đề Xuất Kiến Trúc Hệ Thống AI Agent Nâng Cấp

Để đáp ứng tầm nhìn thiết kế chương trình học đa môn, chúng tôi đề xuất bổ sung tầng kiến trúc **Strategic Curriculum Architect Agent (SCAA)** đóng vai trò Agent Chỉ huy cấp cao (Master Agent) đứng trước pipeline hiện tại.

```
       ┌─────────────────────────────────────────────────────────────┐
       │             ĐẦU VÀO: HỒ SƠ CHƯƠNG TRÌNH ĐÀO TẠO             │
       │  (PLO, CLOs, Hiện trạng sinh viên, Phân bổ thời gian định lượng)│
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │         Strategic Curriculum Architect Agent (SCAA)         │
       │   - Tính toán Hệ số Phức tạp Nhận thức (CCC)                │
       │   - Đề xuất: Số Session, số Lesson và phân bổ thời lượng   │
       │   - Xuất ra: Syllabus Master Schema (Chương trình tối ưu)   │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
                      ┌───────────────┴───────────────┐
                      │    Human-in-the-Loop Gate     │ (Duyệt/Sửa Syllabus)
                      └───────────────┬───────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │             Hệ thống Elearning Content Factory              │
       │  (Antigravity Graph Engine - Sinh tài liệu chi tiết)         │
       └─────────────────────────────────────────────────────────────┘
```

### 1. Cấu trúc Schema Dữ liệu Đầu vào (Pydantic Input Models)
Hệ thống sẽ định nghĩa cấu trúc dữ liệu chặt chẽ để hướng dẫn AI:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class StudentProfile(BaseModel):
    entry_level: str = Field(description="Mức độ đầu vào: beginner | intermediate | advanced")
    background_category: str = Field(description="Đối tượng: non-it (chuyển ngành) | it-student | professional")
    strengths_weaknesses: str = Field(description="Mô tả điểm mạnh/yếu của sinh viên")
    cognitive_speed: float = Field(default=1.0, description="Hệ số tiếp thu: 0.8 (chậm) đến 1.5 (nhanh)")

class ProgramLearningOutcome(BaseModel):
    plo_id: str
    description: str
    target_role: str  # Ví dụ: Junior Backend Dev

class CourseLearningOutcome(BaseModel):
    clo_id: str
    description: str
    cognitive_level: str  # Bloom: Apply, Analyze, Create...
    mapped_plos: List[str]  # Liên kết với PLOs nào

class TimeReference(BaseModel):
    in_class_hours_per_session: float  # Thời lượng trên lớp (VD: 2.0 giờ)
    self_study_hours_per_session: float  # Thời lượng tự học (VD: 4.0 giờ)
    exercise_hours_per_session: float  # Thời lượng làm bài tập (VD: 3.0 giờ)
    total_sessions: int  # Tổng số buổi quy định cứng của môn học (nếu có)
```

### 2. Thiết kế Strategic Curriculum Architect Agent (SCAA)
Agent mới này sẽ đảm nhận 3 bước tư duy chính:

- **Bước 1: Tính toán Khung Tải Nhận Thức (Cognitive Load Estimation)**:
  - Nếu `background_category` = `non-it` và `entry_level` = `beginner`: Hệ thống sẽ tự động gán hệ số điều chỉnh nội dung nhận thức là thấp.
  - Phép tính phân bổ: Số lượng bài tập thực hành sẽ tăng lên, các lý thuyết trừu tượng được chia nhỏ ra gấp 1.5 lần so với lớp IT chuyên nghiệp.
- **Bước 2: Phân Rã và Ánh Xạ Học Tập (Learning Decomposition & Mapping)**:
  - SCAA phân rã từng `CourseLearningOutcome` thành danh sách các Concept cần học.
  - Sau đó, SCAA lập bản đồ phân bổ Concept vào từng Buổi học (Session) sao cho phân bổ đều, không dồn dập.
- **Bước 3: Lập Lịch Khung Chương Trình (Syllabus Scheduling)**:
  - Đầu ra của Agent này là một file JSON có cấu trúc sạch chứa:
    - Danh sách các Session.
    - Trong mỗi Session, phân bổ cụ thể bao nhiêu Lessons.
    - Thời lượng chi tiết cho từng Lesson (Lý thuyết, Thảo luận, Thực hành).
    - Cấu hình **Forbidden Scope** (Cấm từ khóa vượt cấp) và **Allowed Scope** (Phạm vi cho phép) được tính toán tự động dựa trên vị trí của Session trong đồ thị tri thức.

---

## Phần 3: Kế Hoạch Nâng Cấp Hệ Thống Kỹ Thuật

Để thực thi nhiệm vụ này một cách hệ thống, chúng tôi đề xuất thực hiện các thay đổi mã nguồn sau:

### 1. [NEW] Thiết kế Agent mới: `strategic_curriculum_agent.py`
Tạo file mới tại `agents/strategic_curriculum_agent.py` chứa prompt và logic gọi LLM để lập chương trình đào tạo. Agent này sẽ nhận vào:
- Hồ sơ sinh viên (`StudentProfile`)
- Khung mục tiêu (`ProgramLearningOutcome`, `CourseLearningOutcome`)
- Ràng buộc thời gian (`TimeReference`)
Và xuất ra cấu trúc file syllabus tối ưu định dạng JSON.

### 2. [MODIFY] Tích hợp cấu trúc đa môn học vào `core/course_architecture.py`
Nâng cấp logic quản lý cấu trúc cây môn học để lưu trữ sơ đồ quan hệ:
`Program` ➔ `Course` ➔ `Session` ➔ `Lesson`.

### 3. [MODIFY] Tích hợp Dynamic Pacing vào `core/scope_calculator.py`
Cải tiến `scope_calculator.py` để tự động điều chỉnh độ khó của bài học dựa trên hồ sơ hiện trạng sinh viên đã lưu trong AgentState.

---

## Phần 4: Đánh Giá Tác Động & Lợi Ích Quản Lý Giáo Dục

1. **Chuẩn hóa chất lượng đào tạo (Standardization)**: Mọi chương trình học được thiết kế qua hệ thống đều được đảm bảo toán học sư phạm: 100% các bài học liên kết chặt chẽ với chuẩn đầu ra PLO/CLO, không bị trùng lặp hay sót kiến thức.
2. **Cá nhân hóa lộ trình học (Personalization)**: Cùng một môn học (ví dụ: Lập trình Python), nhưng lớp chuyển ngành (Non-IT) và lớp chính quy CNTT sẽ có số lượng bài học và phân bổ thời gian thực hành hoàn toàn khác nhau, khớp với năng lực tiếp thu thực tế của sinh viên.
3. **Tiết kiệm chi phí vận hành (Operational Efficiency)**: Rút ngắn thời gian thiết kế chương trình học của Phòng Đào Tạo từ 2-3 tuần xuống còn 30 phút, đồng thời tạo ra đầu vào chuẩn hóa tự động làm nguồn dữ liệu (SSOT) cho Elearning Content Factory sinh học liệu.

---
Báo cáo này được tổng hợp để đệ trình lên Ban Giám đốc phê duyệt định hướng nâng cấp hệ thống. Chúng tôi sẵn sàng chuyển sang giai đoạn lên kế hoạch triển khai chi tiết mã nguồn ngay khi được phê duyệt.

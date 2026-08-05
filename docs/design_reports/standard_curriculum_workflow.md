# Quy Trình Chuẩn Hóa Đại Học: Thiết Kế Chương Trình Học Dựa Trên PLO & CLO
*(University-Standard Outcomes-Based Education Workflow)*

Tài liệu này đặc tả quy trình chuẩn hóa thiết kế chương trình học tự động bằng AI Agent dựa trên chuẩn đầu ra **PLO (Program Learning Outcomes)** và **CLO (Course Learning Outcomes)**, bám sát cấu trúc của tệp mẫu [PM_PTIT_2026_Chương trình đào tạo.xlsx](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/CLO-PLO/PM_PTIT_2026_Chương-trình-đào-tạo.xlsx).

---

## 1. Sơ Đồ Quy Trình Thiết Kế Ngược (Backward Design Flowchart)

Quy trình chuẩn hóa 7 bước đi từ Mục tiêu tổng thể của Chương trình (Vĩ mô) đến từng bài học nhỏ của mỗi buổi học (Vi mô):

```mermaid
flowchart TD
    %% Khai báo các Node chính
    Start([Đầu vào: Khung Chương trình & Hiện trạng]) --> Step1[Bước 1: Trích xuất PLOs & CLOs từ Excel Khung]
    Step1 --> Step2[Bước 2: Xây dựng Ma trận Ánh xạ CLO-to-PLO]
    Step2 --> Step3[Bước 3: Tính toán Hệ số Nhịp độ & Phân bổ Quỹ Session]
    Step3 --> Step4[Bước 4: Thiết lập Bản đồ Tri thức & Phân chia Session]
    Step4 --> Step5[Bước 5: Phân rã Micro-lessons cho Buổi Lý thuyết]
    Step5 --> Step6[Bước 6: Kiểm định Tuần tự & Ranh giới Kiến thức]
    Step6 --> Step7[Bước 7: Phê duyệt Sư phạm & Xuất Bản Bản thảo PM]
    
    %% Chi tiết xử lý từng bước
    subgraph Step3_Detail ["Chi tiết Bước 3: Phép toán Phân bổ Sư phạm"]
        Direction[Hồ sơ Học viên] --> Pacing[Tính Hệ số Nhịp độ PI]
        Pacing --> Alloc[Quyết định tỷ lệ Lý thuyết / Thực hành / Project]
    end
    
    subgraph Step6_Detail ["Chi tiết Bước 6: Kiểm định An toàn tri thức"]
        Prereq[Prerequisite Guard Agent] -->|Phát hiện lỗi tiên quyết| Step4
        Cognitive[Cognitive Load Linter] -->|Lý thuyết vượt quá 4 bài/buổi| Step5
    end
    
    %% Kết nối luồng chi tiết
    Step3 -.-> Step3_Detail
    Step6 -.-> Step6_Detail
    
    %% Định dạng màu sắc
    style Start fill:#f1f5f9,stroke:#64748b,stroke-width:2px
    style Step7 fill:#eff6ff,stroke:#be111c,stroke-width:2px
    style Step6_Detail fill:#fffbeb,stroke:#d97706,stroke-width:1px
```

---

## 2. Sơ Đồ Tuần Tự Tương Tác Giữa Các Tác Nhân (Agent Interaction Sequence Diagram)

Sơ đồ thể hiện sự phối hợp nhịp nhàng giữa Đội ngũ AI Agents chuyên biệt trong việc biên soạn chương trình học:

```mermaid
sequenceDiagram
    autonumber
    actor User as Phòng Đào tạo (Giáo vụ)
    participant SCAA as Strategic Curriculum Agent (SCAA)
    participant DB as Vector / Database Adapter
    participant PGA as Prerequisite Guard Agent (PGA)
    participant ORA as Objective Reviewer Agent (ORA)
    
    User->>SCAA: 1. Nạp hồ sơ SV, PLOs/CLOs & Quỹ số buổi
    activate SCAA
    SCAA->>DB: 2. Tra cứu Kho tri thức nền tảng (Domain Concepts)
    activate DB
    DB-->>SCAA: 3. Trả về Danh sách hạt tri thức (Knowledge Units) & Mối liên hệ
    deactivate DB
    
    Note over SCAA: SCAA tính toán Hệ số Nhịp độ PI<br/>Sắp xếp KUs thành Đồ thị DAG<br/>Phân bổ KUs vào danh sách Buổi học
    
    SCAA->>PGA: 4. Gửi Dự thảo phân bổ Sessions & Lessons để thẩm định
    activate PGA
    Note over PGA: PGA quét tính tuần tự tri thức<br/>Kiểm tra ranh giới Allowed/Forbidden Scope
    PGA-->>SCAA: 5. Báo cáo kiểm định (Đạt chuẩn / Lỗi Blocker)
    deactivate PGA
    
    alt Có lỗi tuần tự tri thức (Blocker)
        Note over SCAA: SCAA tự điều chỉnh vị trí các buổi học<br/>Hoặc gộp/tách bài học để giảm tải
    end
    
    SCAA->>ORA: 6. Gửi Bản thảo hoàn thiện để kiểm định sư phạm
    activate ORA
    Note over ORA: ORA đánh giá mức độ Bloom<br/>Đo lường độ bám sát chuẩn CLO
    ORA-->>SCAA: 7. Duyệt / Yêu cầu hiệu chỉnh
    deactivate ORA
    
    SCAA-->>User: 8. Xuất file PM chương trình đào tạo JSON/Excel chuẩn
    deactivate SCAA
```

---

## 3. Đặc Tả Chi Tiết 7 Bước Xây Dựng Quy Trình Chuẩn

### Bước 1: Trích xuất PLOs & CLOs
- **Hành động**: Đọc sheet Khung chương trình (Kỳ I ➔ V) của môn học được yêu cầu.
- **Trích xuất**:
  - Danh sách chuẩn đầu ra cấp học kỳ (`PLO 1` đến `PLO 5`).
  - Danh sách chuẩn đầu ra môn học (`CLO 1` đến `CLO 4`) của môn học cụ thể (ví dụ: `IT-106`).

### Bước 2: Xây dựng Ma trận Ánh xạ CLO-to-PLO
- **Hành động**: AI lập bảng ma trận liên kết. Mỗi `CLO` của môn học bắt buộc phải đánh dấu đóng góp vào ít nhất một `PLO` của học kỳ.
- **Mục tiêu**: Đảm bảo không có bài học nào "vô nghĩa" (không đóng góp vào chuẩn đầu ra chung của chương trình).

### Bước 3: Tính toán Hệ số Nhịp độ & Phân bổ Quỹ Session
- **Hành động**: Đọc hồ sơ sinh viên đầu vào.
  - Lớp chuyển ngành (Non-IT, Beginner): Tăng tỷ lệ thực hành (Session loại `Thực hành`) và phân bổ xen kẽ lý thuyết.
  - Lớp chất lượng cao (IT-student, Fast learner): Tăng tốc độ dạy lý thuyết nền tảng, tăng tỷ lệ tự học.

### Bước 4: Thiết lập Bản đồ Tri thức & Phân chia Session
- **Hành động**: Phân tách các CLO thành các **Hạt tri thức** (Knowledge Units - KUs). Sắp xếp các KUs theo mô hình Đồ thị có hướng không chu trình (DAG).
- **Phân bổ**: Gán các KUs vào từng buổi học (`Session`). Buổi Lý thuyết sẽ nhận các KUs mới; Buổi Thực hành/Project sẽ nhận các KUs cũ để ôn luyện.

### Bước 5: Phân rã Micro-lessons cho Buổi Lý thuyết
- **Hành động**: Với các buổi học được gán nhãn `Lý thuyết`, AI tiến hành chia nhỏ KUs thành **3 - 4 bài học nhỏ (Lessons)** có cấu trúc scannable (dạng Bullet list).
- **Quy tắc**: Tuyệt đối cấm chia quá 4 bài học nhỏ trong một buổi lý thuyết đối với lớp Beginner để tránh quá tải nhận thức.

### Bước 6: Kiểm định Tuần tự & Ranh giới Kiến thức (Prerequisite Guard)
- **Hành động**: PGA kiểm duyệt chéo. 
  - Đảm bảo các hàm/cú pháp nâng cao không được xuất hiện ở buổi đầu (Forbidden Scope).
  - Đảm bảo các bài học có tính kế thừa tri thức (ví dụ: Bài học về Hàm bắt buộc phải nằm sau bài học về Vòng lặp và Biến).

### Bước 7: Phê duyệt Sư phạm & Xuất Bản
- **Hành động**: Xuất bản chương trình học chi tiết dưới dạng JSON/Excel. Lưu trữ cấu hình ranh giới tri thức (`Allowed Scope` và `Forbidden Scope`) cho môn học để sẵn sàng cấp phát cho các Creator Agents sinh nội dung học liệu chi tiết.

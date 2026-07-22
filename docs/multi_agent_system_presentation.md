# 🚀 BÁO CÁO THUYẾT TRÌNH HỆ THỐNG MULTI-AGENT CONTENT FACTORY
> **Hệ thống Tự động hóa Sản xuất Học liệu Công nghệ Thông tin Chuyên nghiệp**
> *Tác giả: Rikkei Education Multi-Agent AI Team*

---

## 🎯 1. TỔNG QUAN HỆ THỐNG & GIÁ TRỊ CỐT LÕI

### 1.1 Vấn đề của phương pháp sản xuất học liệu truyền thống:
- **Tốn kém thời gian & Chi phí:** Để biên soạn 1 khóa học IT 30 buổi (bài đọc, slide, bài tập thực hành, đề thi, mini project) cần trung bình 3-6 tháng của đội ngũ Giảng viên & Solution Architect.
- **Không đồng nhất chất lượng:** Nội dung giữa Slide, Bài đọc và Bài tập thường bị lệch pha, lặp lại hoặc rò rỉ kiến thức chưa học.
- **Thiếu tính trực quan:** Bài đọc học liệu khô khan, thiếu bộ công cụ mô phỏng code (Visualizer Canvas) chạy từng bước cho học viên.

### 1.2 Giải pháp Hệ thống Multi-Agent Content Factory:
- **Tự động hóa 95% quy trình:** Chuyển đổi file Đề cương môn học (PM Excel) thành bộ học liệu hoàn chỉnh chỉ trong vài phút.
- **Kiểm soát chất lượng nhiều lớp (Self-Correction Loop):** Hệ thống các Agent Kiểm duyệt (Reviewer) làm việc độc lập, tự động phát hiện lỗi và yêu cầu Agent Tạo (Creator) sửa đổi tối đa 3 lần.
- **Nguồn Sự Thật Duy Nhất (Single Source of Truth - SSOT):** Toàn bộ tri thức môn học được khóa vào SQLite Database trước khi phân rã sản xuất, đảm bảo 100% tính nhất quán.

---

## 🔄 2. QUY TRÌNH & LUỒNG XỬ LÝ NÂNG CAO (END-TO-END PIPELINE)

Hệ thống hoạt động qua **6 Giai đoạn khép kín (End-to-End Phases)**:

```
[PM Excel] ──► (GĐ 0: Thẩm định & Chuẩn hóa) ──► (GĐ 1: Hoạch định & SSOT)
                                                          │
┌─────────────────────────────────────────────────────────┘
▼
(GĐ 2: Trí nhớ & Semantic Cache) ──► (GĐ 3: Luồng Sản xuất Chuyên biệt)
                                              │
┌─────────────────────────────────────────────┘
▼
(GĐ 4: Biên dịch & Đóng gói Exporters) ──► (GĐ 5: Hệ sinh thái Web & Dashboard)
```

---

### GIAI ĐOẠN 0: KIỂM DUYỆT ĐẦU VÀO & CHUẨN HÓA CẤU TRÚC
1. **PM Reviewer & PM Updater Agent:** 
   - Tiếp nhận file Excel Đề cương môn học (`pms/PM_*.xlsx`).
   - Kiểm tra định dạng 7 cột tiêu chuẩn: `STT`, `Hình thức`, `Session`, `Nội dung Session`, `Lesson`, `Chi tiết bài học`, `Kết quả đầu ra`.
   - Nếu file PM bị thiếu cột hoặc lỗi định dạng, **PM Updater Agent** dùng AI tự động khắc phục và xuất ra file `_AI_Updated.xlsx`.
2. **Prerequisite Guard Agent & DAG Graph Engine:**
   - Phân tích toàn bộ chuỗi bài học thành Đồ thị Hướng không Chu trình (**DAG Dependency Graph**).
   - Phát hiện sớm các rủi ro vi phạm tiên quyết (ví dụ: học `Dictionary` trước `List`, dùng `FastAPI` trước khi học `Python Core`).
   - Nếu phát hiện lỗi nghiêm trọng (BLOCKER) $\rightarrow$ Dừng pipeline lập tức và xuất báo cáo `prerequisite_report.md` để tiết kiệm chi phí Token API.

---

### GIAI ĐOẠN 1: HOẠCH ĐỊNH CHIẾN LƯỢC SƯ PHẠM & KHÓA SSOT
1. **Objective Architect Agent:** Phân rã chuẩn đầu ra của từng bài học theo **Thang đo Bloom (Bloom's Taxonomy L1-L6)** (Nhớ, Hiểu, Vận dụng, Phân tích, Đánh giá, Sáng tạo).
2. **Scheduler Agent:** Phân bổ quỹ thời gian, tính toán tải nhận thức (**Cognitive Load Time**) để cân bằng khối lượng học lý thuyết và thực hành cho học viên.
3. **Knowledge Base Agent & SQLite SSOT:** Tổng hợp tri thức nền từ PM và kết quả tìm kiếm RAG, sau đó khóa vào SQLite Database làm Nguồn Sự Thật Duy Nhất (**SSOT**).

---

### GIAI ĐOẠN 2: BỘ LỌC TRÍ NHỚ & SEMANTIC CACHE LAYER
1. **Semantic Cache Layer (Tối ưu 40% Chi phí API):**
   - Áp dụng thuật toán **SHA-256 Exact Match** và **TF-IDF Fuzzy Similarity Matching** (ngưỡng 88%).
   - Nếu yêu cầu tạo bài học trùng khớp với dữ liệu đã tạo trong quá khứ $\rightarrow$ Trả về kết quả từ Cache ngay lập tức mà **không tốn token LLM**.
2. **Knowledge Memory Agent (`knowledge_store.db`):**
   - Đóng vai trò là "Kinh nghiệm tích lũy của hệ thống".
   - Phân loại lỗi từ các lần chạy trước (10 categories: rò rỉ kiến thức, lỗi cú pháp JS, bẫy Indentation,...) và tiêm quy tắc khắc phục (Bad vs Good Example) cho Creator Agent ở lần chạy sau.

---

### GIAI ĐOẠN 3: ĐIỀU HƯỚNG LUỒNG SẢN XUẤT CHUYÊN BIỆT (SPECIALIZED FACTORY ROUTING)

Hệ thống tự động phân loại cột **`Hình thức`** của Session để điều hướng đến Nhà máy sản xuất phù hợp:

#### A. Phân hệ Buổi Lý thuyết (Theory Factory):
- **HTML Writer Agent (Chuẩn W3Schools & Anti-Reload):**
  - Sinh bài đọc tự học 400-800 từ, đầy đủ cơ chế vận hành nội bộ (low-level internals).
  - Tích hợp **Visualizer Canvas (Playground)** với 3 phân vùng đồng bộ: Code Tracker highlight dòng lệnh running, Memory Variable Table, Console System Log.
  - **Quy chuẩn Anti-Reload:** 100% thẻ `<button>` bắt buộc có `type="button"`, cô lập hàm JS per-lesson (`lesson{idx}_...`) chống xung đột và chống reload trang.
  - **Quy chuẩn Cấm Emoji:** Tuyệt đối không dùng emoji, thay bằng nhãn văn bản chuẩn `[NOTE]`, `[TIP]`, `[WARNING]`, `[BEST PRACTICE]`, `[ANTI-PATTERN]`.
- **Slide Creator Agent & Marp CLI:** Sinh Slide trình chiếu Markdown chuẩn kích thước 16:9, xuất trực tiếp ra HTML/PDF.
- **Mindmap Agent & Video Script Agent:** Sinh sơ đồ tư duy Markmap và kịch bản video giảng dạy theo khung HyperFrames.
- **Vòng lặp Kiểm duyệt (UX Reviewer, Academic Reviewer, Sandbox Reviewer):** Chạy kiểm thử tự động, tự động feedback và yêu cầu sửa lỗi tối đa 3 lần.

#### B. Phân hệ Buổi Thực hành (Practice Factory):
- **Practice Exercises Generator:**
  - Tự động sinh bộ 4 bài tập phân tầng độ khó: **Dễ (Easy)**, **Trung bình (Medium)**, **Khá (Hard)**, **Thách thức (Challenge)**.
  - Mỗi bài tập có đầy đủ: Mô tả bài toán nghiệp vụ doanh nghiệp, Đầu vào/Đầu ra (Input/Output sample), Mã nguồn sườn (Starter Code), Mã nguồn đáp án (Solution Code) và Bộ kiểm thử Unit Test.
- **Sandbox Execution Agent:** Chạy thử nghiệm mã nguồn trong môi trường cô lập để đảm bảo test cases PASS 100%.

#### C. Phân hệ Buổi Dự án (Mini Project Factory):
- **Project SRS Generator:** Tạo hồ sơ đặc tả yêu cầu phần mềm chuyên nghiệp (SRS), kiến trúc hệ thống, danh mục API, danh mục mã lỗi.
- **Project Architecture & Starter Template:** Tạo cấu trúc thư mục mã nguồn mẫu chuyên nghiệp, giúp học viên bắt tay vào làm dự án ngay.
- **Rubrics Evaluator:** Sinh bảng tiêu chí chấm điểm chi tiết theo thang điểm 100.

#### D. Phân hệ Buổi Kiểm tra & Thi kết thúc môn (Assessment Factory):
- Sinh bộ đề thi trắc nghiệm & tự luận kèm đáp án và hướng dẫn chấm thi tự động.

---

### GIAI ĐOẠN 4: BIÊN DỊCH & XUẤT BẢN ĐA ĐỊNH DẠNG (COMPILERS & EXPORTERS)
1. **Session Reading Compiler:** Biên dịch và tổng hợp toàn bộ các bài đọc `reading.html` thành tệp bảng điều khiển duy nhất `reading_all.html`.
2. **SCORM 1.2 Exporter:** Đóng gói toàn bộ tài nguyên khóa học thành tệp `.zip` chuẩn SCORM 1.2, sẵn sàng nạp thẳng vào LMS (Moodle, Canvas, Blackboard, TalentLMS).
3. **Obsidian Knowledge Linker:** Xuất toàn bộ lộ trình tri thức thành Vault Obsidian với **Prerequisite Map** và liên kết hai chiều (**Bidirectional WikiLinks `[[...]]`**).

---

### GIAI ĐOẠN 5: HỆ SINH THÁI WEB DASHBOARD & TRUY XUẤT TĨNH
- **FastAPI Backend (`web/backend`):** Cung cấp hệ thống RESTful API kết nối cơ sở dữ liệu SQLite local, hỗ trợ upload & thẩm định PM tự động, mount tĩnh thư mục `/static` xem trực tiếp bài đọc.
- **React + Vite Frontend (`web/frontend`):** Giao diện Dashboard hiện đại, hỗ trợ giám sát tiến trình sản xuất, xem trực tiếp bài đọc W3Schools, Slide trình chiếu và Sơ đồ tư duy interactive.

---

## 📊 3. BẢNG SO SÁNH GIỮA PHƯƠNG PHÁP CŨ VS HỆ THỐNG MULTI-AGENT

| Tiêu chí | Phương pháp Thủ công (Truyền thống) | Hệ thống Multi-Agent Content Factory |
| :--- | :--- | :--- |
| **Thời gian sản xuất (1 Môn học)** | 3 - 6 tháng / môn học | **15 - 30 phút / môn học** |
| **Đồng bộ Tri thức (SSOT)** | Thường xuyên lệch pha giữa Slide & Bài đọc | **Khóa 100% vào SQLite SSOT Database** |
| **Trải nghiệm Học viên** | Đọc tài liệu text khô khan | **Bài đọc W3Schools + Visualizer Code Canvas** |
| **Kiểm soát Tiên quyết** | Phát hiện muộn khi sinh viên ngợp học tập | **Prerequisite Guard ngăn chặn từ khâu Đồ thị DAG** |
| **Khả năng Xuất bản** | Xuất file Word/PDF rời rạc | **Xuất đa định dạng: HTML, SCORM 1.2, Obsidian Vault** |
| **Tự tối ưu Chi phí & Trí nhớ** | Không có | **Semantic Cache (tiết kiệm 40%) & Memory Store** |

---

## 💡 4. KẾT LUẬN & HƯỚNG DẪN TRÌNH DIỄN CHO KHÁCH HÀNG (DEMO SCRIPT)

Khi trình diễn trước Khách hàng / Ban Giám đốc, bạn có thể thực hiện theo 4 bước ấn tượng sau:

1. **Bước 1 (Upload PM & Thẩm định):** Mở giao diện Web Frontend, tải lên file `PM_Python.xlsx`. Cho khách hàng xem **PM Reviewer & Prerequisite Guard** phát hiện lỗi và xây dựng Đồ thị tiên quyết DAG.
2. **Bước 2 (Chạy Sản xuất Tự động):** Nhấn nút kích hoạt Pipeline. Cho khách hàng thấy hệ thống điều hướng song song tạo bài đọc Lý thuyết, bài tập Thực hành 4 cấp độ và đề bài Mini Project.
3. **Bước 3 (Trải nghiệm Bài đọc W3Schools):** Mở tệp `reading_all.html` trên web. Nhấn các nút `▶ Bắt đầu`, `⏭ Từng bước` trên bộ Visualizer Canvas để minh họa khả năng highlight code và bảng theo dõi biến thời gian thực không reload trang.
4. **Bước 4 (Xuất bản SCORM & Obsidian):** Cho khách hàng xem file `.zip` SCORM 1.2 nạp lên Moodle và Ma trận Đồ thị tri thức trong Obsidian Vault.

---
*Tài liệu được khởi tạo tự động bởi Hệ thống Multi-Agent Learning Content Factory.*

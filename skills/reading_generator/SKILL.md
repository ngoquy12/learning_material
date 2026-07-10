---
name: reading_generator
description: Generate dynamic, interactive step-by-step Web Visualizers and E-Learning Playgrounds (HTML, CSS, Vanilla JavaScript) instead of dry text articles.
---

# Kỹ năng Xây dựng Bài đọc Trực quan hóa & Tương tác Web Động (Interactive Web Visualizer & Step-by-Step Playground Skill)

## 1. Triết lý Đào tạo & Cuộc cách mạng Trực quan hóa (Visual Learning Revolution)
Để khơi dậy cảm hứng học tập mãnh liệt và triệt tiêu hoàn toàn cảm giác "khô khan, buồn ngủ" khi đọc tài liệu lý thuyết kỹ thuật, toàn bộ bài đọc tự học (`reading.html`) phải được **chuyển đổi hoàn toàn sang mô hình Trực quan hóa & Tương tác Động ngay trên trình duyệt (Interactive E-Learning Web Playground)** bằng HTML5, Vanilla CSS3 và Vanilla JavaScript.

Thay vì đưa ra định nghĩa, đoạn code tĩnh và lời giải thích dài dòng một chiều, bài đọc phải đóng vai trò như một **phòng thí nghiệm ảo (Virtual Sandbox / Algorithm & System Visualizer)** nơi sinh viên có thể:
1. **Tự tay thao tác & Thử nghiệm (Interactive Control & Experimentation)**: Bấm chạy (`Bắt đầu / Run`), `Tạm dừng / Pause`, đi qua `Từng bước / Step-by-Step`, `Đặt lại / Reset`, hoặc tự nhập tham số/mảng dữ liệu/payload tùy ý để quan sát thay đổi tức thì.
2. **Theo dõi Trạng thái Từng bước (Step-by-Step State Tracking)**: Quan sát luồng dữ liệu biến đổi, các phần tử di chuyển/so sánh/hoán đổi (như sắp xếp nổi bọt), vòng đời request HTTP, hoặc cấu trúc bộ nhớ thay đổi theo thời gian thực.
3. **Đồng bộ Mã nguồn chạy thực tế (Live Code Tracker)**: Tự động highlight chính xác dòng code đang được thực thi (`active-line`) song hành cùng hình ảnh trực quan mô phỏng.
4. **Nhật ký Hệ thống Thời gian thực (Real-time Execution Console Log)**: Đọc giải thích bằng ngôn ngữ tự nhiên xuất hiện liên tục trong terminal log ứng với từng bước thực thi của hệ thống.

---

## 2. Kiến trúc Giao diện & Bố cục Đa bảng (Multi-Panel Visualizer Dashboard)
Giao diện bài đọc phải mang thẩm mỹ hiện đại, chuyên nghiệp, truyền cảm hứng tối đa cho lập trình viên (Sleek Tech UI / Dark Mode / Glassmorphism) được truyền cảm hứng từ các Dashboard trực quan hóa chuẩn mực:

```
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [Header/Navbar]  TÊN MÔN HỌC & BÀI HỌC • Badges: [Thực Tiễn • Sáng Tạo • Tự Tin • Hợp Tác]  |
+─────────────────────────────────────────────────────────────────┬─────────────────────────────+
| [Panel 1: Interactive Visualizer Canvas - Khu vực Trực quan]    | [Panel 2: Metrics / Stats]  |
| • Mô phỏng động bằng SVG / Canvas / DOM Bars / Node Graph      | SO SÁNH: 0 | HOÁN ĐỔI: 0  |
| • Legend màu sắc chỉ rõ trạng thái (Chưa xử lý, Đang so sánh...) | THỜI GIAN: 0.0s             |
|                                                                 +─────────────────────────────+
| (Khung hiển thị đồ họa, thanh biểu đồ, node mạng, luồng data)    | [Panel 3: Code Tracker]     |
|                                                                 | function bubbleSort(arr) {  |
|                                                                 |   for (...) {               |
|                                                                 |     -> if (arr[j] > ...)    |
|                                                                 |        swap(...);           |
+─────────────────────────────────────────────────────────────────+   }                         |
| [Panel 4: Control Panel & Input Workspace - Bảng Điều khiển]    | }                           |
| [▶ Bắt đầu]  [⏸ Tạm dừng]  [⏭ Từng bước]  [↻ Đặt lại]           +─────────────────────────────+
|                                                                 | [Panel 5: Console Log]      |
| • Slider Kích thước: [=====O---] 5 phần tử                      | > NHẬT KÝ THUẬT TOÁN / LOG  |
| • Slider Tốc độ:     [===O-----] 400ms                          | ✓ [Thành công] Phần tử [4]..|
| • Tự nhập dữ liệu:   [ 10, 5, 3, -3      ] [ Áp dụng ]         | ℹ [Hệ thống] Đang tạm dừng  |
+─────────────────────────────────────────────────────────────────┴─────────────────────────────+
| [Panel 6: Structured Theory & Practice Accordions - Khối Lý thuyết & Luyện tập bên dưới]       |
| <details> 1. Đặt vấn đề & Thách thức thực tế (Problem Breakdown) </details>                 |
| <details> 2. Phân tích Bản chất & Cơ chế vận hành nội bộ (Deep Dive Internals) </details>    |
| <details> 3. Lỗi thường gặp & Giải pháp khắc phục (Pitfalls & Best Practices) </details>     |
| <details> 4. Bộ câu hỏi Tự khảo thí & Đánh giá năng lực (Self-Test Questions) </details>     |
+───────────────────────────────────────────────────────────────────────────────────────────────+
```

### Chi tiết 6 Bảng thành phần (6 Core Panels):
1. **Panel 1: Interactive Visualizer Canvas (Khung Trực quan hóa Động)**
   - Không gian trung tâm hiển thị trạng thái động của hệ thống.
   - Cần có **chú thích màu sắc rõ ràng (Legend/Badge)** ngay phía trên (ví dụ: `■ Chưa xử lý` màu xanh tím, `■ Đang kiểm tra/so sánh` màu vàng, `■ Thay đổi/Hoán đổi` màu đỏ/cam, `■ Đã hoàn thành/Chuẩn xác` màu xanh lá).
   - Hiệu ứng chuyển động (CSS transitions / transform / flexbox / absolute positioning) mượt mà khi trạng thái thay đổi.

2. **Panel 2: Real-time Stats & Metrics Card (Thẻ Chỉ số Kỹ thuật)**
   - Hiển thị các tham số quan trọng đang thay đổi theo thời gian thực (Ví dụ với thuật toán: `SO SÁNH (Count)`, `HOÁN ĐỔI (Swaps)`, `THỜI GIAN (Elapsed Time)`. Ví dụ với API/Backend: `HTTP STATUS (200 OK / 400 Bad Request)`, `LATENCY (ms)`, `MEMORY ALLOCATION (KB)`).

3. **Panel 3: Code Tracker (Theo dõi Mã nguồn Đồng bộ theo dòng - Active Line Highlighting)**
   - Mã nguồn code (Python / Javascript / TypeScript / Java tùy theo công nghệ của khóa học) được hiển thị sạch sẽ trong hộp code nền tối (`#1e1f29`).
   - Có cơ chế gắn class `active-line` vào đúng dòng hoặc khối lệnh đang được thực hiện tương ứng với bước thực thi hiện tại trong bộ máy mô phỏng JavaScript. Dòng code kích hoạt sẽ nổi bật với màu nền highlight vàng/xanh kèm thanh viền trái nổi bật.

4. **Panel 4: Interactive Control Panel & Custom Workspace (Bảng Điều khiển & Nhập liệu tự do)**
   - **Nhóm nút điều khiển thời gian thực**:
     * `▶ Bắt đầu (Start/Play)`: Tự động chạy tuần tự các bước theo tốc độ cài đặt.
     * `⏸ Tạm dừng (Pause)`: Dừng ngay tại bước hiện tại để sinh viên ngắm kỹ trạng thái.
     * `⏭ Từng bước (Step-by-Step / Next Step)`: Bước tới đúng 1 hành động/dòng lệnh để phân tích kỹ lưỡng cách giải quyết.
     * `↻ Đặt lại (Reset)`: Khôi phục về trạng thái ban đầu hoặc tạo dữ liệu mới.
   - **Nhóm tùy chỉnh tham số (Sliders & Custom Inputs)**:
     * Slider chỉnh kích thước dữ liệu hoặc độ phức tạp.
     * Slider chỉnh tốc độ chạy (`Tốc độ thực thi: Chậm (1000ms) - Trung bình (400ms) - Nhanh (100ms)`).
     * Ô input cho phép sinh viên tự nhập dữ liệu của riêng mình (`Tự nhập mảng / Tự nhập chuỗi JSON / Tự cấu hình API parameter -> bấm Áp dụng`).

5. **Panel 5: Execution Console Log (Nhật ký Thuật toán & Hệ thống)**
   - Khung terminal mô phỏng (`NHẬT KÝ THUẬT TOÁN / SYSTEM EXECUTION LOG`) với thanh cuộn tự động (auto-scroll).
   - Hiển thị thông báo chi tiết bằng tiếng Việt theo từng mốc thời gian:
     * `ℹ [Hệ thống]`: Thông báo trạng thái khởi tạo, đặt lại, tạm dừng.
     * `⚡ [Đang xử lý/So sánh]`: Mô tả logic đang diễn ra (ví dụ: `Đang so sánh phần tử arr[3]=91 và arr[4]=19`).
     * `✓ [Thành công]`: Cập nhật kết quả bước đúng (ví dụ: `Phần tử cực đại (91) đã nổi lên vị trí cuối mảng index [4]`).
     * `⚠ [Lỗi/Cảnh báo]`: Minh họa tình huống ngoại lệ hoặc lỗi sai nếu có.
   - Có nút `Xóa log (Clear Log)` tiện lợi ở góc phải trên cùng.

6. **Panel 6: Structured Theory Accordions (Lý thuyết & Luyện tập cô đọng bên dưới)**
   - Sau khi học viên trải nghiệm trực quan và "hiểu ngay tại chỗ", phần lý thuyết chi tiết được đóng gói gọn gàng trong các khối Accordion (`<details class="knowledge-card">`) bên dưới để phục vụ tra cứu chuyên sâu mà không gây ngợp mắt:
     * `Khối 1: Đặt vấn đề & Bối cảnh thực tế tại doanh nghiệp`
     * `Khối 2: Phân tích cơ chế vận hành nội bộ (Low-level Internals)`
     * `Khối 3: Lỗi thường gặp (Pitfalls) & Cú pháp triển khai chuẩn (Best Practices)`
     * `Khối 4: Bộ câu hỏi Khảo thí tự học (Self-Test Checklist)`

---

## 3. Quy chuẩn Kỹ thuật Vanilla HTML5/CSS3/JavaScript (Engine Rules)
Để tài liệu tự chạy độc lập 100% khi học viên mở trên bất kỳ trình duyệt nào mà không cần cài đặt server hay phụ thuộc thư viện nặng ngoài CDN cơ bản:

1. **CSS Đóng gói tự trị (Scoped & Responsive CSS)**:
   - Tất cả CSS phải nằm trong thẻ `<style>` ở `<head>`, sử dụng CSS Variables chuẩn:
     ```css
     :root {
         --bg-main: #0b1329;
         --bg-panel: #131f3e;
         --bg-card: #1c2d5a;
         --accent-primary: #6366f1;
         --accent-secondary: #8b5cf6;
         --accent-glow: rgba(99, 102, 241, 0.4);
         --text-light: #f8fafc;
         --text-muted: #94a3b8;
         --state-idle: #475569;
         --state-compare: #eab308;
         --state-swap: #ef4444;
         --state-done: #10b981;
         --border-glow: #2d3f6f;
         --radius-lg: 16px;
         --radius-md: 10px;
     }
     ```
   - Sử dụng CSS Grid / Flexbox hiện đại để chia cột, tự động chuyển về 1 cột (stack vertical) trên màn hình mobile/tablet dưới 992px.

2. **Cơ chế Mô phỏng Trạng thái trong Vanilla JavaScript (Interactive State Machine Engine)**:
   - Trong thẻ `<script>` ở cuối `<body>`, xây dựng một State Machine rõ ràng bao gói trong class hoặc namespace độc lập (ví dụ `class LessonVisualizer Engine`):
     * **`state`**: Lưu trữ dữ liệu hiện tại, chỉ số bước `currentStepIndex`, mảng lịch sử các bước `stepsTimeline`, cờ `isPlaying`, biến hẹn giờ `timerInterval`, tốc độ `speedMs`.
     * **`generateSteps(inputData)`**: Hàm tiền xử lý (pre-calculate) toàn bộ các bước thực thi của thuật toán/bài toán dựa trên input. Mỗi bước (`Step`) là một object chứa: `type`, `description`, `activeLine` (ID dòng code), `visualState` (mạng lưới/mảng/DOM state tại bước đó), và `stats` (số lần so sánh/hoán đổi...).
     * **`renderStep(stepIndex)`**: Hàm cập nhật giao diện (`Canvas/Bar charts`, `Metrics`, `Code Tracker highlight`, và đẩy tin nhắn mới vào `Console Log`) tương ứng với bước số `stepIndex`.
     * **`play()`, `pause()`, `stepForward()`, `reset()`**: Các hàm xử lý sự kiện gắn trực tiếp vào các nút bấm tương tác.

3. **Nguyên tắc Đồng bộ Mã nguồn & Ràng buộc Công nghệ (Technology Stack Isolation)**:
   - Nếu môn học là **Python Core (`python/core`)**: Visualizer mô phỏng cấu trúc dữ liệu Python (List, Dict, Loop, Recursion, Class memory, Algorithm step-by-step). Code Tracker phải là mã Python chuẩn, tuyệt đối không chứa từ khóa FastAPI, SQLAlchemy hay Database.
   - Nếu môn học là **Python Web Services (`python/fastapi`)**: Visualizer mô phỏng vòng đời HTTP Request $\rightarrow$ Uvicorn ASGI $\rightarrow$ FastAPI Router $\rightarrow$ Pydantic Validation $\rightarrow$ Async Execution $\rightarrow$ Response JSON.
   - Nếu môn học là **TypeScript / NestJS (`typescript/nestjs`)**: Visualizer mô phỏng Dependency Injection Container, Guard/Interceptor Lifecycle hoặc DTO transformation.
   - Nếu môn học là **Java Spring Boot (`java/springboot`)**: Visualizer mô phỏng Spring IoC Container, Bean Lifecycle, DispatcherServlet hoặc JPA Hibernate Transactional flow.

---

## 4. Tiêu chuẩn Kiểm duyệt Chất lượng (Validation Rubric)
Mọi tài liệu HTML tạo ra theo kỹ năng này phải đạt các tiêu chí sau trước khi được xuất bản:
1. **Tính tương tác ngay lập tức**: Khi mở file HTML trên trình duyệt, nhấn nút `▶ Bắt đầu` hoặc `⏭ Từng bước` thì giao diện phải chuyển động ngay lập tức, console log phải cuộn và code tracker phải nhảy dòng chính xác.
2. **Không có mã giả hay placeholder**: Không viết `// todo`, `// implement animation here`, hoặc code không chạy. Mọi nút bấm đều phải có sự kiện Javascript hoạt động thực tế.
3. **Hiệu năng & Mượt mà**: Sử dụng `requestAnimationFrame` hoặc `setTimeout` được quản lý chặt chẽ, không gây đơ/treo trình duyệt khi thao tác nhanh với nút bấm hoặc thay đổi kích thước dữ liệu.

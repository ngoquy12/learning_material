---
name: visualizer_generator
description: Generate dynamic, topic-specific interactive visualizers (HTML/JS/CSS) for learning materials.
---

# Visualizer Generator Skill

## 1. Mục tiêu (Objective)

Skill này hướng dẫn Agent cách tạo ra các bộ "Interactive Visualizer" (Trực quan hóa tương tác) linh hoạt và thích ứng với **mọi tình huống/chủ đề bài học** (không bị fix cứng vào STACK/HEAP). Dựa vào `lesson_title` và `tech_stack`, Agent phải tự động thiết kế Canvas, Legend, Stats, và JavaScript State Machine Engine phù hợp nhất.

## 2. Các Mẫu Trực quan hóa Khuyến nghị (Visualizer Archetypes)

Tùy thuộc vào nội dung bài học, Agent cần chọn 1 trong các mô hình (Archetype) sau để thiết kế giao diện `Canvas`:

1. **Memory & Variable Allocator (Mô hình Bộ nhớ):**
   - **Áp dụng:** Khai báo biến, kiểu dữ liệu, con trỏ, tham chiếu.
   - **Giao diện:** Chia 2 cột (Stack & Heap).
2. **Logic & Branching Flow (Mô hình Rẽ nhánh):**
   - **Áp dụng:** Toán tử, if/else, switch case.
   - **Giao diện:** Sơ đồ khối (Flowchart) hoặc Cây quyết định (Decision Tree). Các khối sáng lên theo luồng thực thi (True/False).
3. **Loop & Iterator Track (Mô hình Vòng lặp):**
   - **Áp dụng:** For, While, Iterator, Array Traversal.
   - **Giao diện:** Trục thời gian (Timeline) hoặc Mảng 1 chiều (1D Array boxes). Một con trỏ (Pointer) di chuyển qua từng phần tử.
4. **Data Structure & Graph (Mô hình Cấu trúc dữ liệu):**
   - **Áp dụng:** Tree, Graph, LinkedList, Dictionary.
   - **Giao diện:** Các Node liên kết với nhau bằng mũi tên (SVG lines).
5. **Web Service & Architecture (Mô hình Kiến trúc Web):**
   - **Áp dụng:** FastAPI, Request/Response, Middleware, Database.
   - **Giao diện:** Client (Trình duyệt) -> Server -> Database. Di chuyển các gói tin (Packet) giữa các tầng.

## 3. Cấu trúc Output (JSON format)

Agent cần sinh ra cấu trúc dữ liệu JSON chứa 6 thành phần chính để nhúng vào template HTML:

```json
{
  "canvas_title": "Biểu tượng + Tiêu đề Trực quan hóa (VD: 🔄 Trực quan hóa Vòng lặp For)",
  "legend_html": "Các chú giải màu sắc (VD: <div class='legend-item'>...</div>)",
  "stats_html": "3 thẻ hiển thị thông số realtime (VD: Số vòng lặp, Thời gian, Biến tạm)",
  "code_tracker_html": "Mã nguồn minh họa được bọc trong <span class='code-line' id='line-X'>...</span>",
  "input_label": "Tiêu đề cho ô input (VD: TỰ NHẬP MẢNG DỮ LIỆU)",
  "input_default": "Giá trị mặc định của input",
  "engine_js": "Toàn bộ mã JavaScript ES6 (Class InteractiveVisualizerEngine)"
}
```

## 4. Nguyên tắc cốt lõi của JavaScript Engine (engine_js)

Mã JavaScript phải tự đóng gói (Self-contained) và tuân thủ mô hình State Machine:

1. **Class Structure:**
   ```javascript
   class InteractiveVisualizerEngine {
     constructor() {
       this.steps = [];
       this.currentStep = 0;
       this.init();
     }
     init() {
       this.generateSteps();
       this.render();
     }
     generateSteps() {
       /* Tính toán trước toàn bộ các bước (Pre-compute states) */
     }
     render() {
       /* Cập nhật DOM (Canvas, Stats, Code Tracker Highlight) dựa trên this.steps[this.currentStep] */
     }
     step() {
       /* Tăng currentStep và gọi render() */
     }
     // Các hàm play, pause, reset...
   }
   ```
2. **Pre-computed State:** Toàn bộ quá trình chạy thuật toán phải được mô phỏng trước và lưu vào mảng `this.steps`. Mỗi `step` object chứa trạng thái UI hoàn chỉnh của bước đó (VD: Vị trí con trỏ, giá trị biến, dòng code đang active, thông báo log).
3. **No External Dependencies:** Chỉ sử dụng Vanilla JS và thao tác DOM trực tiếp. Không dùng React/Vue. Khuyến khích dùng Template Literals để tạo HTML động bên trong hàm `render()`.
4. **Dynamic CSS Variables:** Tái sử dụng các biến CSS có sẵn trong dự án: `var(--primary)`, `var(--bg-panel)`, `var(--text-main)`, `var(--color-idle)`, `var(--color-done)`.

## 5. Quy trình làm việc của Agent

1. **Phân tích (Analyze):** Đọc kỹ `lesson_title` và mục tiêu bài học để xác định Archetype phù hợp.
2. **Thiết kế Kịch bản (Storyboard):** Lên kịch bản mã nguồn (`code_tracker_html`) khoảng 5-10 dòng. Xác định các bước biến đổi trạng thái.
3. **Sinh mã JS (Implement JS):** Viết logic `generateSteps()` mô phỏng mã nguồn. Viết `render()` để vẽ giao diện đồ họa.
4. **Trả về Output:** Đóng gói thành định dạng JSON chuẩn.

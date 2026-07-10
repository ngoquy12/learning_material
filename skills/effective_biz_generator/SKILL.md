---
name: effective_biz_generator
description: Generate self-contained, high-impact interactive HTML Visualizations & Strategic Framework Diagrams (based on plannotator/effective-html) for Business Administration, Economics, Management, and Non-IT subjects.
---

# Kỹ năng Xây dựng Bài đọc & Trực quan hóa Khung Quản trị Kinh doanh (Effective HTML Business & Framework Visualizer Skill)

Được kế thừa và chuẩn hóa từ kiến trúc **[plannotator/effective-html](https://github.com/plannotator/effective-html)**, kỹ năng này chuyên biệt phục vụ các môn học thuộc lĩnh vực **Quản trị Kinh doanh, Kinh tế, Marketing, Tài chính, Quản trị Nhân sự & các môn Non-IT**.

---

## 1. Triết lý Thiết kế "Effective HTML" cho Khối Quản trị Kinh doanh
Khác với các môn Lập trình (IT) cần khung theo dõi mã nguồn (Code Tracker) hay Terminal Log, các môn Quản trị Kinh doanh cần trực quan hóa **Mô hình Khái niệm (Conceptual Frameworks), Quy trình Vận hành (Business Workflows), Chuỗi Giá trị (Value Chains)** và **Ma trận Chiến lược (Strategic Matrices)**.

Tài liệu HTML tạo ra phải tuân thủ 5 nguyên tắc cốt lõi của `effective-html`:
1. **Sân khấu Đồ họa Toàn màn hình (Full-screen High-Density Visual Stage)**:
   - Phần trung tâm của trang là một Biểu đồ kiến trúc / Mô hình kinh doanh dạng SVG tương tác chất lượng cao (`html-diagram`).
   - Các nút (Nodes), luồng (Paths) và thẻ chiến lược (Chips) được thiết kế sắc nét, cân đối, thể hiện rõ mối quan hệ nguyên nhân - kết quả.
2. **Khám phá Tương tác & Thẻ Thông tin Nổi (Dismissible Overlay Detail Panels)**:
   - Khi học viên click vào bất kỳ Node hoặc bước nào trên Sơ đồ, luồng dữ liệu liên quan sẽ sáng lên và một Thẻ chi tiết (`Detail Drawer / Card Panel`) xuất hiện để giải thích:
     * Định nghĩa & Ý nghĩa chiến lược.
     * Chỉ số đo lường trọng yếu (KPIs / Metrics).
     * Ví dụ thực tiễn tại doanh nghiệp (Case Study / Real-world Scenario).
   - Mọi overlay panel BẮT BUỘC có nút đóng (`[×] Close button`) dễ nhìn để không che khuất toàn bộ sơ đồ.
3. **Hỗ trợ Pan & Zoom cho Sơ đồ Lớn (Interactive Canvas Pan & Zoom)**:
   - Cho phép kéo thả (`Drag to Pan` 1:1 trong không gian SVG) và cuộn chuột phóng to/thu nhỏ (`Mouse Wheel Zoom` tại vị trí con trỏ).
   - Có thanh điều khiển Zoom (`[ - ] 100% [ + ] [ Đặt lại ]`).
4. **Hệ thống Chế độ Tối/Sáng Đóng gói (Theme System & Dark Mode)**:
   - Tích hợp sẵn CSS Variables trên `:root` và `html.dark`.
   - Nút chuyển đổi giao diện Sáng/Tối với lưu trữ tự động vào `localStorage`.
5. **Cấu trúc Kế hoạch & Bảng Chiến lược (`html-plan` Mode)**:
   - Bên dưới sơ đồ trực quan là bảng phân tích chiến lược, các checklist hành động thực tế và ma trận quyết định (ví dụ SWOT/TOWS, Porter's 5 Forces, Business Model Canvas).

---

## 2. Kiến trúc Giao diện Chuẩn mực (Effective Business Dashboard Layout)

```
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [Header] CHƯƠNG TRÌNH QUẢN TRỊ KINH DOANH • BÀI HỌC CỐT LÕI  | [☀/🌙 Theme Toggle]  [Reset Zoom] |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [INTERACTIVE FRAMEWORK STAGE - KHUNG SƠ ĐỒ CHIẾN LƯỢC TOÀN CẢNH (SVG PAN/ZOOM)]               |
|                                                                                               |
|      +───────────────────+             +───────────────────+             +─────────────────+  |
|      |  1. Nghiên cứu &  |   ────────> |  2. Hoạch định    |   ────────> |  3. Thực thi &  |  |
|      |  Phân tích Thị    |             |  Chiến lược       |             |  Kiểm soát KPI  |  |
|      +───────────────────+             +───────────────────+             +─────────────────+  |
|               │                                  │                                 │          |
|               ▼                                  ▼                                 ▼          |
|      [ Khách hàng Mục tiêu ]            [ Lợi thế Cạnh tranh ]            [ Dashboard Doanh thu ] |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [DISMISSIBLE DETAIL DRAWER - THẺ CHI TIẾT TƯƠNG TÁC (Xuất hiện khi chọn Node)]          [× Đóng] |
| • Tiêu đề Node đã chọn: HOẠCH ĐỊNH CHIẾN LƯỢC CẠNH TRANH                                      |
| • Định nghĩa: Xác định định vị thương hiệu và các điểm khác biệt cốt lõi (USP)...             |
| • KPI chính: Thị phần (Market Share % CPS), CAC, LTV...                                        |
| • Tình huống Case Study: Cách Apple áp dụng khác biệt hóa sản phẩm...                          |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [STRATEGIC PLAN & IMPLEMENTATION MATRICES (`html-plan` Section)]                              |
| <details open> 1. Phân tích Tình huống Doanh nghiệp & Thách thức Quản trị </details>          |
| <details> 2. Ma trận Lựa chọn Chiến lược & Quy trình Triển khai </details>                    |
| <details> 3. Bài tập Tình huống (Case Study Workshop) & Thảo luận </details>                  |
+───────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Quy chuẩn Mã nguồn HTML/CSS/JS (Effective HTML Template Rules)

1. **Font chữ & Hệ thống Màu sắc Thương hiệu (Curated Palette)**:
   - Sử dụng bộ font thương hiệu: `Inter` cho nội dung, `Montserrat` cho tiêu đề.
   - Bảng màu quản trị cao cấp (Corporate Professional Dark/Light Palette):
     * Màu chính (`--primary`): Navy / Deep Slate (`#1E293B` / `#38BDF8`).
     * Màu nhấn (`--accent`): Warm Rust / Gold (`#D97757` / `#F59E0B`).
     * Nền trang (`--bg-body`): Clean Sand (`#FAF9F5`) cho Light Mode, Deep Obsidian (`#0B0F19`) cho Dark Mode.

2. **Cơ chế Điều khiển Đồ họa SVG & Sự kiện Tương tác**:
   - Toàn bộ đồ họa SVG được bao bọc trong `<g id="svg-content">`.
   - Viết Javascript thuần xử lý sự kiện `pointerdown`, `pointermove`, `pointerup` để hỗ trợ kéo thả Pan 1:1.
   - Mỗi Node trên SVG có thuộc tính `data-node-id="node-1"` và gắn sự kiện click để hiển thị thẻ `Detail Panel`.

3. **Tính Độc lập & Tự trị (100% Self-Contained Offline Portability)**:
   - Tất cả mã CSS và Javascript được gom đầy đủ trong cùng 1 file HTML, có thể mở trực tiếp trên mọi trình duyệt mà không cần cài server hay thư viện nặng ngoài CDN cơ bản.

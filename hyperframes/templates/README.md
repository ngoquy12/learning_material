# HYPERFRAMES SHARED SKELETON TEMPLATES SYSTEM

Thư mục này chứa các **Tệp Mẫu Khung Xương Dùng Chung (Shared Skeleton Templates)** dành cho hệ thống tự động sinh video HyperFrames của Agent.

---

## 📂 Danh sách Skeleton Templates:

### 1. `light_theme_skeleton.html` (Mẫu Khung Xương Nền Sáng Chuẩn Thương Hiệu)
Tệp mẫu khung xương giao diện Video Nền Sáng chuẩn mực, được tích hợp phông chữ **Be Vietnam Pro**, Logo Rikkei Edu góc trên-phải, tiêu đề căn trái góc trên-trái màu đỏ thương hiệu `#ba252a`, căn lề $100\%$ và khung Code Monospace Fira Code.

#### 🛠️ Các Tham số Đầu vào (Dynamic Slots):
- `{scene_n}`: Số thứ tự Scene (`01`, `02`, `03`...)
- `{scene_slug}`: Chuỗi slug của Scene (VD: `scene-01`)
- `{scene_title}`: Tiêu đề phân cảnh sinh động từ kịch bản
- `{dur}`: Thời lượng Scene tính theo giây (loại từ tệp `durations.json` giọng đọc TTS)
- `{clean_content}`: Slot nhúng nội dung UI linh hoạt (Thẻ danh sách số thứ tự, Sublist, Khung Code, Sơ đồ khối, Hình ảnh minh họa Infographic...)

---

## ⚙️ Cơ chế Hoạt động của Agent (`UIManager`):
- Khi sinh phân cảnh mới, `hyperframes/ui_manager.py` sẽ tự động load tệp `hyperframes/templates/light_theme_skeleton.html`, điền các giá trị dynamic slot và tạo ra tệp HTML Composition hoàn chỉnh mà không fix cứng nội dung thủ công.

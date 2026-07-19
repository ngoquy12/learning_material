# Hướng Dẫn Vận Hành: Quy Trình Duyệt & Cập Nhật Chương Trình (PM Workflow)

Tài liệu này hướng dẫn chi tiết quy trình đưa Khung chương trình (PM - Project Manager Input) vào hệ thống Elearning Agent, cách AI tự động đánh giá chất lượng PM, và các thao tác tự động cập nhật toàn bộ học liệu khi PM có sự thay đổi.

---

## 1. Giai Đoạn 1: Đưa PM Vào Hệ Thống Để AI Kiểm Định (PM Review)

Trước khi tiến hành tự động sinh hàng loạt học liệu (Slide, HTML, Quiz, Video), hệ thống được trang bị một "Chốt chặn" (Gatekeeper). Một AI đóng vai trò là **Giám đốc Đào tạo (Chief Learning Officer) kiêm Kiến trúc sư phần mềm** sẽ đọc và soi xét kỹ lưỡng cấu trúc PM.

### Thao tác thực hiện:
Mở Terminal và chạy lệnh mặc định:
```bash
python main.py
```

### Chuyện gì sẽ xảy ra?
1. **Hệ thống sẽ bị đóng băng tạm thời**: Luồng Antigravity Workflow sẽ DỪNG NGAY LẬP TỨC tại chốt kiểm dịch `node_pm_review`.
2. **AI Thẩm định chuyên sâu**: Agent sẽ đánh giá PM trên 3 khía cạnh cốt lõi:
   - **Mức độ phân rã**: Các Lesson có đủ chi tiết và rõ chuẩn đầu ra chưa?
   - **Tải lượng nhận thức**: Có bài học nào nhồi nhét quá nhiều kiến thức phức tạp không?
   - **Lỗ hổng Nhảy cóc (Prerequisites)**: Kiến thức các bài có móc xích logic không? Có khái niệm nào bị "nhảy cóc" chưa dạy nền tảng đã bắt học viên tiếp thu cái mới không?
3. **Xuất báo cáo**: Một file Markdown sẽ được tự động tạo và lưu tại:
   👉 `dist/pm_review_report.md`
4. **Cảnh báo**: Terminal hiển thị lỗi `[CHỜ DUYỆT PM]`, yêu cầu con người vào can thiệp và đọc báo cáo.
5. **AI Auto-Updater (Tính năng Tương tác)**: Ngay lập tức, Terminal sẽ hỏi bạn:
   > `Bạn có muốn AI tự động chỉnh sửa file Excel PM dựa trên các đề xuất này không? (y/n):`
   - Nếu bạn chọn `y`: Một Agent "Chuyên gia Cập nhật" (`pm_updater_agent`) sẽ được đánh thức. Nó sẽ lấy bản báo cáo lỗi kia, tự động sửa đổi lại toàn bộ cấu trúc bài học, chèn thêm nội dung còn thiếu, sắp xếp lại Logic và **xuất ra một file Excel mới** mang đuôi `_AI_Updated.xlsx` (Ví dụ: `PM_Python_Core_AI_Updated.xlsx`).
   - Nếu bạn chọn `n`: Hệ thống dừng lại hoàn toàn để bạn tự mở Excel lên sửa thủ công.

---

## 2. Giai Đoạn 2: Duyệt PM và Chạy Hệ Thống Sản Xuất (Approve & Generate)

Sau khi đọc file báo cáo và file PM đã được AI tự động cập nhật (hoặc bạn tự sửa bằng tay), nếu bạn đã hoàn toàn tự tin với file Excel mới:

### Thao tác thực hiện:
Nhập lệnh khởi chạy với cờ `--approve-pm`:
```bash
python main.py --approve-pm
```

### Chuyện gì sẽ xảy ra?
1. **Mở khóa Workflow**: Cờ `--approve-pm` báo hiệu cho hệ thống biết con người đã "Nhấn nút xanh" và chấp nhận mọi rủi ro về cấu trúc.
2. **Khởi chạy Parallel Pipelines**: Hệ thống nhảy qua rào chắn và kích hoạt toàn bộ các luồng Agent chạy song song (Sinh bài đọc, Slide, Quiz, Script Video, Mindmap).
3. **Xuất bản**: Toàn bộ học liệu sẽ được sinh ra chuẩn chỉ và sắp xếp gọn gàng vào thư mục `output/<Tên_Khóa_Học>/...`.

---

## 3. Giai Đoạn 3: Cập Nhật Toàn Bộ Học Liệu Khi PM Bị Đổi (Force Update)

Trong thực tế vận hành, chương trình học thường xuyên phải thay đổi, cắt xén hoặc bổ sung bài giảng giữa chừng. Thay vì phải đi vào từng thư mục vật lý để xóa file hay sửa thủ công, hệ thống hỗ trợ cơ chế "Tái thiết đồng bộ 100%".

### Thao tác thực hiện:
Bạn chỉ cần chỉnh sửa trực tiếp vào file PM Excel cho đúng nội dung mới, sau đó chạy lệnh với cả hai cờ:
```bash
python main.py --approve-pm --force
```

### Chuyện gì sẽ xảy ra?
1. Hệ thống ghi nhận lệnh bỏ qua bước Review PM (`--approve-pm`).
2. Cờ `--force` sẽ ra lệnh cho hệ thống **xóa bỏ mọi trạng thái đã lưu trước đó** (bypass checkpoints & SQLite state).
3. Các Agent sẽ thu thập lại nội dung PM Excel mới nhất và **tiến hành viết lại toàn bộ** từ Slide đến bài đọc HTML.
4. **Cập nhật Folder/File tự động**: Các file cũ trong thư mục `output/` sẽ tự động bị ghi đè, cấu trúc thư mục tự động uốn nắn theo chuẩn mới mà không gây rác hệ thống hay dư thừa dữ liệu. Bạn hoàn toàn rảnh tay!

---

## 💡 Bảng Tổng Hợp CLI Commands (Thần Chú Vận Hành)

| Lệnh trong Terminal | Ý Nghĩa / Mục Đích Sử Dụng |
|---|---|
| `python main.py` | Chạy thử nghiệm để AI dò lỗi PM và **xuất báo cáo Review** ra file `.md`. Hệ thống bị đóng băng. |
| `python main.py --approve-pm` | **Chốt duyệt PM** và bắt đầu quá trình sinh học liệu hàng loạt. |
| `python main.py --approve-pm --force` | Dùng khi PM Excel bị thay đổi. Ép hệ thống **cập nhật & ghi đè lại toàn bộ** thư mục, folder và file theo nội dung mới. |
| `python main.py --approve-pm --session "Session 01"` | Lệnh rút gọn: Chỉ duyệt và chạy riêng biệt cho một Session cụ thể (ở đây là Session 01) để tiết kiệm thời gian chờ. |

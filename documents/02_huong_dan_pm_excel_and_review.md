# TÀI LIỆU HƯỚNG DẪN 02: BƯỚC 1 - NẠP VÀ KIỂM ĐỊNH FILE PM EXCEL (PM AUDITOR GATE)

## 1. Mục Đích
Tự động hóa việc nạp file khung chương trình PM (`PM_Python.xlsx`), đánh giá tính hợp lý sư phạm, phát hiện lỗ hổng nhảy cóc kiến thức và hỗ trợ AI tự động cập nhật file Excel PM.

---

## 2. Cấu Trúc File Excel PM Đầu Vào
Tệp Excel PM đặt tại thư mục `documents/PM_Python.xlsx` chứa các cột thông tin:
- **Session ID**: Tên buổi học (ví dụ: `Session 06`)
- **Session Title**: Chủ đề buổi học (ví dụ: `Cấu trúc dữ liệu List và Tuple`)
- **Lesson ID**: Tên bài học (ví dụ: `Lesson 01`)
- **Lesson Title**: Tiêu đề bài học (`Khái niệm List và cách khởi tạo`)
- **Details & Objectives**: Mô tả chi tiết và chuẩn đầu ra bài học.

---

## 3. Quy Trình Thực Thi Bước PM

### Bước 3.1: Chạy Lệnh Quét và Đánh Giá PM
```bash
python main.py --pm "documents/PM_Python.xlsx" --approve-pm
```

### Bước 3.2: Cơ Chế Đánh Giá Của PM Auditor Agent
Agent sẽ phân tích 4 tiêu chí cốt lõi:
1. **Phân rã bài học**: Các Lesson có đủ độ sâu và rõ chuẩn đầu ra hay chưa?
2. **Tải lượng nhận thức**: Có bài nào nhồi nhét quá nhiều kiến thức phức tạp không?
3. **Lỗ hổng Nhảy cóc (Prerequisites)**: Kiến thức các bài có móc xích logic không?
4. **Báo cáo kiểm định**: Xuất báo cáo chi tiết tại `output/pms/<Tên_Khóa_Học>/structure_review_report.md`.

### Bước 3.3: AI Auto-Updater (Tự Động Sửa Excel)
Khi phát hiện lỗi cấu trúc, Agent `pm_updater_agent` sẽ tự động đề xuất sửa đổi và cập nhật lại file PM.

---

## 4. Quy Tắc Phê Duyệt (Approval Checklist)
- Cờ `--approve-pm` mở khóa cho các Agent phía sau (Reading, Quiz, Slide, Homework) tiếp tục khởi chạy.
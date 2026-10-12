---
description: Bàn giao cuối phiên. Cập nhật docs/PROJECT_STATE.md với việc đã xong, đang dở, việc tiếp theo, quyết định mới và lệnh kiểm tra.
---

# /handoff - Bàn giao cuối phiên

Ghi chú cho người bảo trì: định dạng workflow Antigravity (markdown có frontmatter `description`). Cần kiểm tra đường dẫn theo phiên bản IDE: `.agents/workflows/` hay `.agent/workflows/`.

## Các bước

1. Mở `docs/PROJECT_STATE.md`.
2. Cập nhật mục "Trạng thái các môn" nếu có môn thay đổi.
3. Cập nhật mục "Việc tiếp theo": đánh dấu hoặc xóa việc đã xong, thêm việc đang dở (nói rõ dừng ở đâu), sắp việc đầu tiên là việc nên làm kế tiếp.
4. Ghi quyết định mới và điều còn mở vào mục "Quyết định / còn mở".
5. Ghi lệnh kiểm tra cần chạy lại (ví dụ `python -m pytest tests -q -x --ignore=tests/evals`, lệnh mở `tests.html` bằng Live Server) kèm kết quả lần cuối.
6. Thêm 1 dòng vào "Nhật ký thay đổi" với ngày và nội dung ngắn.
7. Không dán nội dung dài (mã, bài đọc, log); chỉ ghi tên tệp và tóm tắt. Giữ tệp dưới khoảng 120 dòng.
8. Báo cho người dùng đã cập nhật những mục nào.

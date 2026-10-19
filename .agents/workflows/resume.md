---
description: Tiếp tục công việc từ phiên trước. Đọc docs/PROJECT_STATE.md, git status, git log rồi làm tiếp việc đầu tiên trong "Việc tiếp theo".
---

# /resume - Tiếp tục công việc

Ghi chú cho người bảo trì: theo định dạng workflow của Antigravity (markdown có frontmatter `description`, gọi bằng `/resume`). Cần kiểm tra đường dẫn theo phiên bản IDE: thư mục có thể là `.agents/workflows/` hoặc `.agent/workflows/`. Nếu `/resume` không hiện trong IDE, sao chép tệp sang thư mục còn lại.

## Các bước

1. Đọc `docs/PROJECT_STATE.md`. Không phân tích lại toàn bộ dự án.
2. Chạy `git status` và `git log -10 --oneline` để biết thay đổi chưa commit và các commit gần nhất.
3. Tóm tắt đúng 5 dòng cho người dùng: (1) dự án đang ở đâu, (2) việc gần nhất đã làm, (3) thay đổi chưa commit, (4) quyết định còn mở, (5) việc sẽ làm tiếp.
4. Nếu người dùng đã nói việc cần làm, làm đúng việc đó. Nếu chưa, liệt kê tối đa 3 việc đầu trong mục "Việc tiếp theo" và HỎI người dùng chọn việc nào; không tự bắt đầu.
5. Không sửa mã nguồn, skill, template hay cấu hình nếu người dùng chưa yêu cầu rõ (xem mục "Ranh giới sửa đổi" trong `AGENTS.md`).
6. Chỉ cập nhật `docs/PROJECT_STATE.md` khi người dùng gọi `/handoff`.

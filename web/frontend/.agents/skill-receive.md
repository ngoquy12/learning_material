# AGENT SKILL: NHẬN YÊU CẦU & PHÂN TÍCH (RECEIVE SKILL) - FE

Skill này hướng dẫn Agent cách nhận, tiếp cận và phân tích yêu cầu từ phía người dùng đối với dự án Frontend.

---

## 1. QUY TRÌNH TIẾP CẬN
1. **Lắng nghe yêu cầu**: Đọc kỹ mô tả tính năng UI/UX, yêu cầu tương tác API hoặc sửa bug từ người dùng (bằng Tiếng Việt).
2. **Định vị phạm vi ảnh hưởng**:
   - Xác định xem yêu cầu liên quan đến Module FE nào trong `src/modules/` (ví dụ: `vehicleManager`, `warehouseManager`).
   - Nếu là Module cũ, tìm kiếm các Pages, Components, Hooks hoặc API Service liên quan bằng cách sử dụng `grep_search` hoặc chỉ đọc trực tiếp các file trong thư mục module đó.
   - Nếu liên quan đến luồng Route, hãy tìm kiếm trong `src/routes/` để xem cấu hình router.
3. **Tuyệt đối KHÔNG quét bừa bãi**:
   - Tránh việc chạy `list_dir` trên toàn bộ dự án hoặc đọc tràn lan các file không liên quan để tiết kiệm token.
   - Tập trung vào file `PROJECT_CONTEXT.md` trước để hiểu bức tranh lớn, sau đó tìm đúng module đích.
4. **Kiểm tra quy định bảo mật**:
   - Đảm bảo trong danh sách file phân tích **KHÔNG** chứa các file `.env` nhạy cảm.

---

## 2. OUTPUT CỦA BƯỚC NHẬN YÊU CẦU
Sau khi nhận yêu cầu, Agent phải phản hồi lại người dùng:
1. Tóm tắt ngắn gọn yêu cầu (bằng Tiếng Việt) để xác nhận sự hiểu biết.
2. Chỉ ra các page, component, hook hoặc service hiện tại sẽ bị ảnh hưởng (nếu có).
3. Đề xuất các component, page, hook hoặc API service mới cần tạo (nếu có).
4. Đặt các câu hỏi làm rõ (nếu yêu cầu của người dùng chưa đủ thông tin đầu vào).

# AGENT SKILL: XÓA CODE & FILE (DELETE SKILL) - FE

Skill này hướng dẫn Agent cách xử lý an toàn khi cần xóa code, file hoặc module trong dự án Frontend nhằm tránh gây vỡ giao diện hoặc lỗi biên dịch.

---

## 1. NGUYÊN TẮC AN TOÀN
> [!CAUTION]
> **Yêu cầu xác nhận từ người dùng là bắt buộc.** Agent KHÔNG ĐƯỢC tự ý xóa bất kỳ file hoặc đoạn code quan trọng nào mà chưa có sự đồng ý tường minh từ phía người dùng.

---

## 2. QUY TRÌNH XÓA CODE AN TOÀN
1. **Kiểm tra phụ thuộc (Dependencies)**:
   - Trước khi xóa một component, hook hoặc service, hãy tìm kiếm trong toàn bộ dự án (`grep_search`) để xem có file nào khác đang `import` hoặc sử dụng chúng không.
   - Nếu có, phải chuẩn bị phương án sửa đổi các file phụ thuộc đó trước.
2. **Kiểm tra Router**:
   - Nếu xóa một trang (Page Component), hãy kiểm tra xem Route tương ứng trong `src/routes/` có đang trỏ tới trang đó không. Nếu có, cần cập nhật cấu hình Router (xóa route hoặc cấu hình redirect).
3. **Nêu rõ ảnh hưởng & lý do xóa**:
   - Trình bày cho người dùng biết chính xác những file/đoạn code nào sẽ bị xóa.
   - Giải thích lý do tại sao cần xóa chúng (ví dụ: component cũ không còn sử dụng, refactor sang cấu trúc mới).
   - Nêu ra các ảnh hưởng/rủi ro tiềm ẩn (nếu có).
4. **Yêu cầu xác nhận (User Confirmation)**:
   - Đưa ra câu hỏi xác nhận rõ ràng: *"Bạn có chắc chắn muốn xóa [danh sách file/code] này không? Vui lòng xác nhận để tôi thực hiện."*
5. **Thực hiện xóa và kiểm tra**:
   - Sau khi người dùng đồng ý, thực hiện xóa.
   - Chạy lệnh build kiểm tra lỗi biên dịch TypeScript để đảm bảo ứng dụng không bị lỗi sau khi xóa.

---
name: video_script_generator
description: Generate structured video recording storyboard scripts with conversational voiceover and visual directives.
---

# Kỹ năng biên soạn kịch bản quay Video (Video Script Generator Skill)

## 1. Tổng quan

Kịch bản video dùng để giảng viên giảng dạy và ghi hình các bài học E-learning có thời lượng lý tưởng từ 3 đến 7 phút. Nội dung phải kết hợp nhuần nhuyễn giữa phần lời thoại đối thoại (narration) và chỉ dẫn visual (màn hình/slide/cử chỉ).

## 2. Cấu trúc Kịch bản 3 Phần

Bắt buộc chia kịch bản thành cấu trúc sau:

1. **Mở đầu (Introduction - 00:00 đến 00:45)**:
   - Giới thiệu khái niệm/chủ đề bài học ngắn gọn.
   - Gây ấn tượng và tạo lý do học viên cần tập trung xem video.
   - Lời thoại mở đầu mẫu: _"Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education, trong nội dung bài học này, chúng ta sẽ cùng nhau tìm hiểu về..."_
2. **Nội dung chính (Main Content - 00:45 đến 03:30 / 04:30)**:
   - Đặt vấn đề/bài toán thực tế (Problem).
   - Giải quyết vấn đề bằng ví dụ thực tế cụ thể, viết code mẫu và chạy kiểm thử (Solution/Example).
   - Đưa ra khái niệm kỹ thuật chuẩn hóa.
   - Thao tác: chia sẻ màn hình IDE, terminal (ví dụ: `uvicorn main:app --reload`), duyệt Swagger UI `/docs`.
3. **Kết luận (Conclusion - Cuối video)**:
   - Tóm tắt 3 ý chính cốt lõi của bài giảng.
   - Đưa ra các cảnh báo/lỗi hay gặp (pitfalls).
   - Kêu gọi hành động (CTA): làm bài tập Lab, trả lời câu hỏi tự luận.
   - Lời thoại kết thúc mẫu: _"Cảm ơn các em đã theo dõi, hẹn gặp lại trong các bài học tiếp theo."_

## 3. Định dạng Kịch bản (Storyboard Table)

Kịch bản được viết dưới dạng bảng Markdown gồm 3 cột:

- **Thời gian (Timeline)**: Mốc thời gian dự kiến (ví dụ: `00:00 - 00:45`).
- **Chỉ dẫn quay hình & Slide Visuals**: Mô tả chi tiết những gì xuất hiện trên màn hình (ví dụ: camera talking head giảng viên, chuyển sang VS Code chia sẻ màn hình, highlight cú pháp lệnh, uvicorn terminal console, v.v.).
- **Lời thoại chi tiết giảng viên**: Văn phong đối thoại tự nhiên, gần gũi, giải thích tường tận từng bước. Bắt buộc chứa các câu chuyển đoạn mượt mà (ví dụ: _"Bây giờ chúng ta cùng chuyển sang phần tiếp theo"_, _"Các em lưu ý phần quan trọng này"_).

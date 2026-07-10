---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 01 - Lesson 02: Cài đặt môi trường
### Lớp học thực chiến Python Web Services

---

# Đặt vấn đề & Thách thức
- Bối cảnh thực tế: Trong lập trình Python cơ bản, việc học viên tiếp cận và triển khai **Cài đặt môi trường** luôn đi kèm với những thử thách tư duy logic thực tế. Khi mới bắt đầu học lập trình Python, học viên thường gặp khó khăn trong việc thiết lập môi trường phát triển (IDE), cài đặt trình thông dịch Python và cấu hình biến môi trường. Việc viết chương trình đầu tiên mà không hiểu cơ chế biên dịch và thông dịch của ngôn ngữ, cách khai báo biến cũng như nhập xuất cơ bản sẽ làm học viên bối rối trước các lỗi cú pháp sơ đẳng.
- Vấn đề gặp phải: Khi phân tích sâu về **Cài đặt môi trường**, chúng ta nhận thấy: Cài đặt Python, VS Code, Anaconda/Virtual Environment Python là một ngôn ngữ thông dịch (interpreted language), có nghĩa là mã nguồn được thực thi từng dòng bởi trình thông dịch Python (Python Interpreter) chứ không biên dịch trực tiếp ra mã máy như C/C++. Việc khai báo biến trong Python cực kỳ linh hoạt vì Python sử dụng kiểu dữ liệu động (dynamic typing) và tự động quản lý bộ nhớ thông qua cơ chế Garbage Collection. Việc xuất dữ liệu dùng `print()` và nhập dữ liệu dùng `input()` là nền tảng giao tiếp giữa người dùng và máy tính.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Tiêu chí</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Định kiểu động (Python)</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Định kiểu tĩnh (Java/C++)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Khai báo biến</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Không cần chỉ định kiểu dữ liệu (x = 10)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Bắt buộc chỉ định kiểu (int x = 10)</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Độ linh hoạt</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Cực cao, có thể đổi kiểu dữ liệu của biến</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Thấp, biến không được đổi kiểu</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Phát hiện lỗi kiểu</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Khi chương trình đang chạy (Runtime)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Khi biên dịch chương trình (Compile time)</td>
        </tr>
    </tbody>
</table>
- Giải pháp: Áp dụng Để giải quyết triệt để vấn đề này, chúng ta cần áp dụng các cấu trúc lập trình Python chuẩn mực. Mục tiêu đầu ra là đạt được chuẩn: **Môi trường Python hoạt động**. Cài đặt Python phiên bản mới nhất, cấu hình IDE VS Code chuyên nghiệp. Sử dụng các biến để lưu trữ dữ liệu tạm thời, thực hiện ép kiểu (type casting) hợp lý để chuyển đổi giữa các kiểu dữ liệu cơ bản (int, float, str, bool), và sử dụng f-string để định dạng chuỗi xuất ra màn hình một cách khoa học.

---

# Ví dụ Minh họa Triển khai
- Cú pháp code chuẩn hóa và an toàn
- Sử dụng công cụ tương tác trực quan
- Xem ví dụ triển khai chi tiết trong bài đọc

---

# Tổng kết & Luyện tập
- Bài học cốt lõi: Lưu ý quan trọng cho **Cài đặt môi trường**: Luôn ép kiểu rõ ràng khi nhận dữ liệu từ `input()`. Lỗi thường gặp nhất là quên f ở đầu f-string làm tên biến không được thế giá trị.
- Thực hành làm bài Lab tuần đầy đủ
- Tự đối chiếu kết quả theo checklist tự học

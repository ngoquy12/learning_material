---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 05: Điều kiện lồng nhau và toán tử ba ngôi
### Lớp học thực chiến Python Web Services

---

# Đặt vấn đề & Thách thức
- Bối cảnh thực tế: Trong lập trình Python cơ bản, việc học viên tiếp cận và triển khai **Điều kiện lồng nhau và toán tử ba ngôi** luôn đi kèm với những thử thách tư duy logic thực tế. Khi xây dựng các luồng quyết định (decision-making) trong chương trình, học viên thường gặp khó khăn trong việc kết hợp các toán tử so sánh và toán tử logic để tạo ra các biểu thức điều kiện chính xác. Ngoài ra, việc lạm dụng cấu trúc `if-else` lồng nhau sâu khiến mã nguồn trở nên rối rắm, khó đọc và khó kiểm thử các trường hợp biên.
- Vấn đề gặp phải: Khi phân tích sâu về **Điều kiện lồng nhau và toán tử ba ngôi**, chúng ta nhận thấy: Tối ưu hóa cấu trúc rẽ nhánh phức tạp Python cung cấp hệ thống toán tử phong phú gồm toán tử số học (`+`, `-`, `*`, `/`, chia lấy nguyên `//`, chia lấy dư `%`, lũy thừa `**`), toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`) và toán tử logic (`and`, `or`, `not`). Cấu trúc rẽ nhánh `if-elif-else` và cấu trúc `match-case` (từ Python 3.10) giúp phân tách luồng chạy của chương trình dựa trên kết quả của biểu thức điều kiện logic. Việc tối ưu hóa biểu thức logic bằng toán tử ba ngôi (ternary operator) giúp mã nguồn ngắn gọn hơn.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Toán tử</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Ý nghĩa</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Ví dụ</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">%</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Chia lấy phần dư (Modulo)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">5 % 2 = 1</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">//</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Chia lấy phần nguyên (Floor Division)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">5 // 2 = 2</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">**</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Lũy thừa (Power)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">5 ** 2 = 25</td>
        </tr>
    </tbody>
</table>
- Giải pháp: Áp dụng Để giải quyết triệt để vấn đề này, chúng ta cần áp dụng các cấu trúc lập trình Python chuẩn mực. Mục tiêu đầu ra là đạt được chuẩn: **Mã nguồn rẽ nhánh sạch và gọn**. Sử dụng đúng độ ưu tiên của các toán tử số học và logic (sử dụng dấu ngoặc đơn `()` để tường minh). Áp dụng cấu trúc rẽ nhánh `if-elif-else` một cách khoa học, tránh lồng nhau quá 3 cấp, hoặc chuyển sang dùng `match-case` khi so sánh một biến với nhiều giá trị cụ thể nhằm tăng tính thẩm mỹ và dễ bảo trì.

---

# Ví dụ Minh họa Triển khai
- Cú pháp code chuẩn hóa và an toàn
- Sử dụng công cụ tương tác trực quan
- Xem ví dụ triển khai chi tiết trong bài đọc

---

# Tổng kết & Luyện tập
- Bài học cốt lõi: Lưu ý quan trọng cho **Điều kiện lồng nhau và toán tử ba ngôi**: Luôn dùng dấu ngoặc đơn để làm rõ độ ưu tiên của toán tử. Lỗi thường gặp nhất là dùng một dấu bằng = thay cho hai dấu bằng == trong lệnh so sánh if.
- Thực hành làm bài Lab tuần đầy đủ
- Tự đối chiếu kết quả theo checklist tự học

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Phân tích & Liệt kê lỗi (Debug Report)** | **20đ** | - Chỉ ra chính xác 7/7 lỗi trong đoạn mã ban đầu (14đ).<br/>- Giải thích đúng nguyên nhân kỹ thuật (ví dụ: `span` không có thuộc tính `.value`, `getElementById` không nhận tiền tố `#`) (6đ). |
| **Thao tác DOM API đúng cú pháp** | **30đ** | - Sử dụng đúng `document.getElementById("late-minutes")` (không dấu `#`).<br/>- Sử dụng đúng `document.querySelector(".emp-name")` (có dấu `.`).<br/>- Sử dụng `.innerText` / `.textContent` thay cho `.value` đối với các thẻ non-input.<br/>- Đọc đúng attribute `data-type` qua `.dataset.type` hoặc `.getAttribute("data-type")`.<br/>- Gán CSS class đúng qua `.className` hoặc `.classList.add()`. |
| **Xử lý Logic Chấm công & Tính lương** | **30đ** | - Áp dụng đúng điều kiện phạt đi muộn: `lateMinutes > 15`.<br/>- Tính đúng tiền OT theo hệ số ca `WEEKDAY` (1.5) hoặc `HOLIDAY` (3.0).<br/>- Tính đúng Tổng lương thực nhận = `Lương ca + OT - Phạt`.<br/>- Hiển thị đúng kết quả `390.625` VNĐ cho bộ test case mặc định. |
| **Trình bày Code & Chuẩn mực** | **20đ** | - Tuân thủ cấu trúc thư mục quy định (5đ).<br/>- Code trình bày sạch đẹp, không dư thừa console.log lỗi (5đ).<br/>- Tuân thủ phạm vi kiến thức (Không sử dụng Event Listener, Fetch, LocalStorage) (10đ). |
# HyperFrames Script: Session 03 — Lesson 05

**Lesson:** Khối else trong vòng lặp
**Technology Stack:** python/core
**Total Duration:** 271.39s
**Scene Count:** 8

---

## Scene_01: Vấn đề tìm kiếm tuần tự
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Bài toán tìm kiếm tuần tự yêu cầu xử lý một hành động dự phòng khi không tìm thấy kết quả.

**Animation Timeline:**
- 0.2s: step-1 fade in
- 5.0s: arrow-1 draw
- 10.0s: step-2 fade in
- 15.0s: arrow-2 draw
- 20.0s: step-fallback highlight

**Narration (VO):**
> Trong phát triển phần mềm doanh nghiệp, bài toán tìm kiếm tuần tự diễn ra vô cùng phổ biến. Ví dụ như quét danh sách giao dịch tài chính để phát hiện gian lận. Khi phần tử đích không tồn tại, hệ thống bắt buộc phải thực thi một hành động dự phòng như ghi nhật ký lỗi hoặc khởi tạo lại cơ sở dữ liệu.

## Scene_02: Hạn chế của biến cờ hiệu
**Timeline (root):** 39.24s → 69.24s (30s)

**Visual:** Sử dụng biến cờ hiệu làm tăng dung lượng mã nguồn và tăng nguy cơ sinh lỗi logic.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: comparison-table fade in
- 5.0s: highlight-bad-code
- 15.0s: highlight-redundant-if

**Narration (VO):**
> Phương pháp truyền thống bắt buộc lập trình viên sử dụng một biến cờ hiệu kiểu bu-li-an để ghi nhận trạng thái. Việc này làm phình to mã nguồn do phải cập nhật cờ trước khi gọi lệnh brếch và viết thêm cấu trúc điều kiện ít để kiểm tra sau vòng lặp.

## Scene_03: Cơ chế vận hành của loop-else
**Timeline (root):** 69.24s → 104.24s (35s)

**Visual:** Sơ đồ hoạt động: Hoàn thành vòng lặp bình thường sẽ kích hoạt khối else; thoát bằng break sẽ bỏ qua else.

**Animation Timeline:**
- 0.2s: flowchart-draw
- 8.0s: highlight-path-break
- 18.0s: highlight-path-normal

**Narration (VO):**
> Khối lệnh eo của vòng lặp hoạt động theo nguyên tắc: chỉ thực thi khi vòng lặp hoàn thành tuần tự và trọn vẹn mà không bị gián đoạn giữa chừng. Nếu vòng lặp gặp câu lệnh brếch và thoát ra sớm, toàn bộ khối eo sẽ bị trình biên dịch bỏ qua.

## Scene_04: Thực thi mã nguồn thực tế
**Timeline (root):** 104.24s → 139.24s (35s)

**Visual:** Cấu trúc điều khiển for-else tối ưu hóa luồng code bằng cách loại bỏ biến cờ logic trung gian.

**Animation Timeline:**
- 0.2s: code-syntax-highlight
- 10.0s: line-if-break highlight
- 20.0s: line-else-block highlight

**Narration (VO):**
> Hãy xem ví dụ quét mã lỗi hệ thống. Vòng lặp pho duyệt qua danh sách trạng thái. Nếu tìm thấy mã lỗi nguy hiểm năm trăm, lệnh brếch sẽ lập tức dừng vòng lặp. Khối eo chỉ chạy khi toàn bộ danh sách được duyệt mà không có lỗi nguy hiểm nào.

## Scene_05: Tầm quan trọng của thụt lề
**Timeline (root):** 139.24s → 169.24s (30s)

**Visual:** Từ khóa else phải được căn lề thẳng hàng với từ khóa for hoặc while của vòng lặp chính.

**Animation Timeline:**
- 0.2s: show-indent-guidelines
- 10.0s: highlight-correct-alignment
- 20.0s: pulse-incorrect-warning

**Narration (VO):**
> Điểm mấu chốt khi triển khai cú pháp này là từ khóa eo phải nằm thẳng hàng và cùng cấp độ thụt lề với từ khóa pho hoặc oai. Việc thụt lề sai sẽ biến khối eo này thành của lệnh ít bên trong, gây ra các lỗi logic nghiêm trọng.

## Scene_06: Thực hành tốt với for-else
**Timeline (root):** 169.24s → 199.24s (30s)

**Visual:** Ví dụ thực hành tốt: Căn lề chính xác else thẳng cột với for để đảm bảo logic chạy đúng.

**Animation Timeline:**
- 0.2s: code-fade-in
- 8.0s: highlight-loop-flow
- 18.0s: highlight-else-safe-action

**Narration (VO):**
> Đây là đoạn mã chuẩn để quét cơ sở dữ liệu thư rác. Khối eo được thụt lề ngang hàng với pho. Điều này đảm bảo hành động thông báo địa chỉ email an toàn chỉ thực thi một lần duy nhất sau khi đã kiểm tra toàn bộ danh sách mà không trùng khớp.

## Scene_07: Cảnh báo lỗi thụt lề
**Timeline (root):** 199.24s → 229.24s (30s)

**Visual:** Cảnh báo: Thụt lề else thẳng hàng với if bên trong vòng lặp sẽ khiến logic chạy lặp vô ích.

**Animation Timeline:**
- 0.2s: show-alert-card
- 10.0s: highlight-wrong-indent
- 20.0s: blink-warning-message

**Narration (VO):**
> Nếu thụt lề eo thẳng hàng với lệnh ít bên trong vòng lặp, chương trình sẽ kiểm tra và in ra thông báo lệch pha cho từng phần tử không khớp. Điều này dẫn đến kết quả sai lệch toàn cục do thực thi lặp đi lặp lại nhiều lần.

## Scene_08: Quy tắc thiết kế hệ thống
**Timeline (root):** 229.24s → 259.24s (30s)

**Visual:** Tóm tắt: Giảm thiểu biến trạng thái trung gian, tối ưu bộ nhớ, tránh lồng ghép quá sâu để bảo trì dễ dàng.

**Animation Timeline:**
- 0.2s: show-summary-grid
- 10.0s: highlight-benefit
- 20.0s: highlight-rule

**Narration (VO):**
> Cấu trúc vòng lặp eo giúp tối ưu dung lượng bộ nhớ nhờ tránh khai báo biến cờ toàn cục. Tuy nhiên, lập trình viên không nên lạm dụng lồng ghép quá nhiều vòng lặp chứa cấu trúc này để tránh làm giảm khả năng đọc hiểu và bảo trì mã nguồn về lâu dài.


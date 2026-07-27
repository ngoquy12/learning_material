# HyperFrames Script: Session 03 — Lesson 04

**Lesson:** Vòng lặp lồng nhau (Nested loops)
**Technology Stack:** python/core
**Total Duration:** 461.39s
**Scene Count:** 12

---

## Scene_01: Giới thiệu dữ liệu đa chiều
**Timeline (root):** 9.24s → 44.24s (35s)

**Visual:** Dữ liệu đa chiều xuất hiện phổ biến trong vận hành doanh nghiệp gồm sơ đồ ghế (hàng và cột), lịch làm việc (nhân viên và ngày), báo cáo tài chính (năm và tháng).

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 1.5s: intro-title fade-in
- 4.0s: dimensional-blocks animate-up
- 12.0s: use-cases-icons highlight

**Narration (VO):**
> Trong lập trình phần mềm thực tế, dữ liệu hiếm khi tồn tại dưới dạng danh sách phẳng đơn giản. Các bài toán quản lý tài nguyên như thiết lập sơ đồ ghế ngồi rạp chiếu phim với hàng và cột, quản lý ca làm việc của nhân viên theo ngày, hay xuất báo cáo tài chính theo nhiều tháng đều yêu cầu mô hình hóa dữ liệu đa chiều. Việc hiểu cách xử lý cấu trúc này là bước đệm quan trọng để xây dựng thuật toán tối ưu.

## Scene_02: Hạn chế của vòng lặp đơn
**Timeline (root):** 44.24s → 79.24s (35s)

**Visual:** So sánh cách tiếp cận: Vòng lặp đơn lẻ (gây tối nghĩa, lạm dụng chia lấy dư/nguyên) với Vòng lặp lồng nhau (rõ ràng, dễ bảo trì).

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 1.5s: comparison-header highlight
- 5.0s: complexity-formula show
- 15.0s: alternative-solution reveal

**Narration (VO):**
> Nếu cố gắng giải quyết cấu trúc hai chiều bằng một vòng lặp đơn, mã nguồn sẽ trở nên vô cùng phức tạp. Lập trình viên bắt buộc phải sử dụng liên tiếp các phép chia lấy dư và chia lấy nguyên để dò tìm vị trí dòng và cột từ một chỉ số phẳng duy nhất. Điều này không chỉ gây khó khăn cho việc bảo trì mà còn dễ tạo ra các lỗi logic tiềm ẩn khi nâng cấp hệ thống.

## Scene_03: Triết lý thiết kế Python
**Timeline (root):** 79.24s → 109.24s (30s)

**Visual:** Triết lý thiết kế của Guido van Rossum (1991) đề cao tính tường minh và trực quan hóa cấu trúc lặp lồng nhau.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 2.0s: quote-text write-effect
- 8.0s: timeline-node-1991 pop

**Narration (VO):**
> Được thiết kế bởi Gido van Rốt sum vào năm một chín chín mốt, Python luôn ưu tiên tính tường minh và dễ đọc của cú pháp. Để mô phỏng tự nhiên các không gian đa chiều này mà không làm tăng độ phức tạp thuật toán, cấu trúc vòng lặp lồng nhau ra đời, cho phép liên kết các chiều dữ liệu một cách trực quan và dễ hiểu nhất.

## Scene_04: Mô hình tính toán tọa độ hai chiều
**Timeline (root):** 109.24s → 149.24s (40s)

**Visual:** Mô hình Row & Column: Với mỗi dòng (Outer Loop), lập trình viên duyệt qua tất cả cột (Inner Loop). Tổng số bước lặp lý thuyết bằng M x N.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 1.5s: coordinate-grid scale-in
- 6.0s: outer-loop-pointer advance
- 12.0s: inner-loop-cycle flash
- 25.0s: total-formula scale-up

**Narration (VO):**
> Cơ chế vận hành của vòng lặp lồng nhau dựa trên nguyên lý tọa độ hai chiều. Vòng lặp ngoài đại diện cho dòng, đi qua từng bước một. Với mỗi bước của vòng lặp ngoài, vòng lặp trong đóng vai trò là cột sẽ phải thực thi đầy đủ chu kỳ lặp từ đầu đến cuối. Tổng số bước tính toán sẽ là tích số lần lặp của vòng ngoài và vòng trong.

## Scene_05: Khởi tạo vòng lặp ngoài
**Timeline (root):** 149.24s → 184.24s (35s)

**Visual:** Khởi tạo các biến giới hạn hàng, cột và xây dựng cấu trúc vòng lặp ngoài (phạm vi từ 1 đến row_limit + 1).

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 1.5s: variables-code highlight
- 8.0s: for-outer-loop highlight

**Narration (VO):**
> Hãy bắt đầu viết mã nguồn thực tế. Đầu tiên, khởi tạo biến giới hạn dòng râu li-mít bằng ba, và giới hạn cột co-lum li-mít bằng bốn. Tiếp theo, khai báo vòng lặp ngoài bằng lệnh pho râu năm-bờ in ren-giơ từ một đến râu li-mít cộng một. Việc cộng thêm một giúp hàm ren-giơ giữ đúng phạm vi lặp đến hết dòng thứ ba.

## Scene_06: Khởi tạo vòng lặp trong
**Timeline (root):** 184.24s → 219.24s (35s)

**Visual:** Lồng vòng lặp trong (inner loop) quản lý cột phía dưới vòng lặp ngoài với thụt dòng 4 ký tự trắng chuẩn PEP 8.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 2.0s: indentation-guides show
- 7.0s: inner-for-loop highlight

**Narration (VO):**
> Tại bước này, thực hiện thụt đầu dòng đúng bốn khoảng trắng theo tiêu chuẩn pếp tám. Khởi tạo vòng lặp trong bằng câu lệnh pho co-lum năm-bờ in ren-giơ từ một đến co-lum li-mít cộng một. Quy tắc thụt dòng bắt buộc này giúp Python hiểu rằng vòng lặp co-lum năm-bờ là một khối mã con, phụ thuộc hoàn toàn vào chu kỳ của vòng lặp cha bên ngoài.

## Scene_07: Thực thi lô-gíc xuất tọa độ
**Timeline (root):** 219.24s → 254.24s (35s)

**Visual:** Xuất giá trị tọa độ trên cùng một hàng nhờ sử dụng tham số end=' ' để ngăn hành vi tự động ngắt dòng của lệnh print.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 2.0s: print-statement highlight
- 10.0s: end-parameter tooltips

**Narration (VO):**
> Bên trong vòng lặp con, sử dụng lệnh prin để in ra tọa độ hiện tại định dạng râu năm-bờ gạch ngang co-lum năm-bờ. Bổ sung tham số en bằng ký tự rỗng và một khoảng trắng. Tham số này ghi đè hành vi xuống dòng mặc định của hàm prin, giúp các giá trị cột trên cùng một dòng được xếp liên tiếp theo chiều ngang phẳng.

## Scene_08: Ngắt dòng sau mỗi chu kỳ hàng
**Timeline (root):** 254.24s → 289.24s (35s)

**Visual:** Sử dụng lệnh print() rỗng thẳng hàng với vòng lặp trong (thụt lề mức 1) để ngắt dòng sau khi in hết các cột.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 2.0s: empty-print select
- 8.0s: indentation-align vertical-line

**Narration (VO):**
> Sau khi kết thúc chu kỳ xử lý của toàn bộ các cột trong một hàng, ta cần xuống dòng để chuẩn bị cho hàng kế tiếp. Viết lệnh prin rỗng ngay dưới cấp thụt lề của vòng lặp ngoài. Vị trí đặt lệnh này cực kỳ quan trọng, nó chỉ được kích hoạt sau khi vòng lặp trong đã hoàn tất chu kỳ chạy của hàng hiện tại.

## Scene_09: Chạy chương trình trên Terminal
**Timeline (root):** 289.24s → 334.24s (45s)

**Visual:** Giao diện Terminal thực thi chương trình hiển thị kết xuất ma trận tọa độ dạng lưới gồm 3 hàng và 4 cột.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 1.5s: terminal-prompt focus
- 5.0s: output-row-1 print-sequential
- 12.0s: output-row-2 print-sequential
- 19.0s: output-row-3 print-sequential

**Narration (VO):**
> Khi thực thi chương trình trong cửa sổ ci el ai, luồng điều khiển hoạt động như sau. Ở dòng một, vòng trong chạy bốn lần để tạo ra các cột từ một đến bốn. Khi gặp lệnh prin rỗng, hệ thống ngắt dòng. Quá trình này tiếp tục lặp lại ở dòng hai và dòng ba, tạo ra cấu trúc lưới hoàn chỉnh chứa mười hai tọa độ dữ liệu.

## Scene_10: Tránh lỗi trùng biến và thụt lề
**Timeline (root):** 334.24s → 374.24s (40s)

**Visual:** Cảnh báo lỗi trùng tên biến lặp (variable collision) và lỗi cú pháp khoảng thụt đầu dòng (IndentationError).

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 2.0s: warning-icon shake-animation
- 7.0s: error-line highlight-red
- 15.0s: fix-solution display

**Narration (VO):**
> Lưu ý rằng sự độc lập của biến điều khiển là bắt buộc. Tuyệt đối không dùng chung một tên biến cho cả vòng trong lẫn vòng ngoài vì sẽ gây lỗi ghi đè dữ liệu. Đồng thời, lỗi in-den-tây-sơn e-rơ rất dễ xảy ra nếu bạn vô tình trộn lẫn dấu cách và phím tab. Hãy đồng bộ sử dụng duy nhất bốn dấu cách để cấu trúc code luôn ổn định.

## Scene_11: Bẫy lặp vô hạn và Giới hạn cấp lồng
**Timeline (root):** 374.24s → 414.24s (40s)

**Visual:** Tránh lỗi vòng lặp vô hiệu (Infinite Loops) ở vòng lặp while và tối ưu hiệu năng bằng cách giới hạn số cấp lồng tối đa là 3.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 2.0s: alert-infinite show
- 8.0s: recursion-limit shadow-effect
- 18.0s: best-practice-card SlideLeft

**Narration (VO):**
> Một nguy cơ tiềm ẩn khác là bẫy logic vòng lặp vô hạn khi kết hợp các cấu trúc oai lồng nhau. Hãy chắc chắn rằng biến dừng của cả hai vòng lặp đều được cập nhật ở cuối mỗi chu kỳ. Ngoài ra, hạn chế tối đa thiết kế cấu trúc lồng nhau vượt quá ba cấp để tránh quá tải tài nguyên tính toán và suy giảm hiệu năng hệ thống.

## Scene_12: Tổng kết và thực hành tốt nhất
**Timeline (root):** 414.24s → 449.24s (35s)

**Visual:** Biểu đồ tổng kết quy trình: Thiết lập mục tiêu -> Khai báo tách biệt -> Định dạng PEP 8 -> Chạy kiểm tra.

**Animation Timeline:**
- 0.0s: active-scene-clip visible
- 1.5s: summary-tree fade-in
- 6.0s: steps-nodes-fill color-green
- 15.0s: outro-logo zoom-out

**Narration (VO):**
> Tổng kết lại, vòng lặp lồng nhau là giải pháp mạnh mẽ để quản lý tối ưu dữ liệu dạng bảng lưới hoặc cây phân cấp trong Python. Bằng việc tuân thủ quy tắc đặt tên biến tách biệt, thụt đầu dòng chuẩn pếp tám và kiểm soát tốt điều kiện dừng, bạn sẽ làm chủ kỹ năng xử lý dữ liệu phức tạp trong thực tế dự án.


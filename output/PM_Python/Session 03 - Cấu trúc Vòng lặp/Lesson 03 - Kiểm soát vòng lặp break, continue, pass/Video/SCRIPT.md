# HyperFrames Script: Session 03 — Lesson 03

**Lesson:** Kiểm soát vòng lặp: break, continue, pass
**Technology Stack:** python/core
**Total Duration:** 451.39s
**Scene Count:** 12

---

## Scene_01: Bài toán đối soát giao dịch ngân hàng
**Timeline (root):** 9.24s → 44.24s (35s)

**Visual:** Hệ thống xử lý tuần tự dễ gây quá tải hệ thống khi gặp giao dịch bất thường hoặc lỗi dữ liệu. Cần cơ chế kiểm soát trực tiếp luồng lặp.

**Animation Timeline:**
- 0.2s: step-active fade in
- 2.5s: arrow-1 fade in
- 5.0s: step-alert fade in
- 10.0s: arrow-2 fade in
- 12.0s: step-highlight fade in

**Narration (VO):**
> Trong các hệ thống tài chính lớn, việc duyệt qua hàng triệu giao dịch mỗi giây đòi hỏi tối ưu tài nguyên tối đa. Nếu xử lý tuần tự mà không có cơ chế rẽ nhánh sớm, hệ thống sẽ lãng phí chu kỳ xử lý của xi-pi-u cho các tác vụ lỗi hoặc các giao dịch bất hợp lệ. Do đó, chúng ta cần nắm vững các công cụ điều hướng vòng lặp.

## Scene_02: Cơ chế điều phối vòng lặp
**Timeline (root):** 44.24s → 79.24s (35s)

**Visual:** Ba công cụ điều phối luồng chính: bờ-rếch (thoát vòng lặp), cần-ti-niu (bỏ qua lượt hiện tại), và pát (giữ chỗ cấu trúc mã).

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: box-critical slide in
- 3.5s: box-warning slide in
- 7.2s: box-helper slide in

**Narration (VO):**
> Để kiểm soát luồng thực thi trong ngôn ngữ Python, chúng ta sử dụng ba từ khóa cốt lõi: bờ-rếch để ngắt toàn bộ vòng lặp ngay lập tức, cần-ti-niu để bỏ qua phần còn lại của lượt hiện tại và chuyển sang lượt tiếp theo, và pát để giữ chỗ cú pháp khi chưa triển khai logic.

## Scene_03: Dừng khẩn cấp bằng Break
**Timeline (root):** 79.24s → 114.24s (35s)

**Visual:** Câu lệnh bờ-rếch chấm dứt hoàn toàn vòng lặp chứa nó, bỏ qua mọi câu lệnh phía sau và nhảy đến dòng code đầu tiên bên ngoài vòng lặp.

**Animation Timeline:**
- 0.2s: code-block render
- 4.5s: highlight lines 2-4
- 9.0s: pointer-focus break-keyword

**Narration (VO):**
> Khi phát hiện nguy cơ bảo mật nghiêm trọng như giao dịch âm chín trăm chín mươi chín, việc tiếp tục xử lý sẽ gây nguy hiểm. Lệnh bờ-rếch được kích hoạt để dừng ngay lập tức tiến trình quét, giải phóng tài nguyên hệ thống và ngăn chặn bất kỳ hành vi phá hoại nào tiếp diễn.

## Scene_04: Sơ đồ hoạt động của Break
**Timeline (root):** 114.24s → 149.24s (35s)

**Visual:** Luồng chạy gặp bờ-rếch sẽ thoát ra khỏi khối lệnh của vòng lặp pho hoặc oai và đi tới khối lệnh kế tiếp sau vòng lặp.

**Animation Timeline:**
- 0.2s: flow-graph show
- 3.5s: connection-lines draw
- 8.0s: flow-focus external-node

**Narration (VO):**
> Hãy quan sát luồng điều hướng của lệnh bờ-rếch. Khi biểu thức điều kiện trả về giá trị đúng, chương trình sẽ không thực hiện bất kỳ lệnh nào bên dưới trong khối lặp nữa. Nó lập tức nhảy thẳng ra ngoài vòng lặp để tiếp tục các câu lệnh ở cấp độ cha cao hơn.

## Scene_05: Bỏ qua phần tử lỗi bằng Continue
**Timeline (root):** 149.24s → 184.24s (35s)

**Visual:** Câu lệnh cần-ti-niu kết thúc lượt lặp hiện tại ngay lập tức, đẩy tiến trình lặp sang lượt tiếp theo của vòng lặp.

**Animation Timeline:**
- 0.2s: code-block render
- 4.0s: highlight line 3
- 8.5s: arrow-back-to-loop-start animate

**Narration (VO):**
> Khác với bờ-rếch, khi gặp một lỗi nhẹ như số tiền giao dịch nhỏ hơn hoặc bằng không, chúng ta không cần dừng toàn bộ hệ thống. Câu lệnh cần-ti-niu sẽ bỏ qua các dòng lệnh xử lý bên dưới của lượt này và chuyển ngay sang phần tử tiếp theo trong danh sách.

## Scene_06: Giữ cấu trúc thiết kế bằng Pass
**Timeline (root):** 184.24s → 219.24s (35s)

**Visual:** Từ khóa pát đóng vai trò giữ chỗ (placeholder), không thực hiện hành động nào và giúp tránh lỗi thụt lề khi viết khung giao diện lập trình.

**Animation Timeline:**
- 0.2s: code-block render
- 3.8s: comment-line highlight
- 7.5s: pass-keyword focus

**Narration (VO):**
> Trong thực tế phát triển phần mềm, bạn thường xuyên phải phác thảo cấu trúc trước khi code chi tiết. Nếu bạn để trống một khối lệnh íp hay vòng lặp, Python sẽ báo lỗi cú pháp. Sử dụng pát giúp mã nguồn hợp lệ để kiểm thử các luồng khác trước khi quay lại hoàn thiện logic.

## Scene_07: Demo tổng hợp kiểm soát vòng lặp
**Timeline (root):** 219.24s → 259.24s (40s)

**Visual:** Kết hợp bờ-rếch, cần-ti-niu và pát trên danh sách transaction_list để xử lý các phân khúc giao dịch thực tế.

**Animation Timeline:**
- 0.2s: code-block render
- 8.0s: highlight break-statement
- 15.0s: highlight continue-statement
- 22.0s: highlight pass-statement

**Narration (VO):**
> Hãy quan sát mã nguồn tổng hợp này. Chúng ta khởi tạo một danh sách các giá trị giao dịch. Vòng lặp pho duyệt từng phần tử. Tùy thuộc vào các điều kiện kiểm tra, hệ thống sẽ đưa ra quyết định dừng khẩn cấp, bỏ qua dữ liệu lỗi, hoặc phân nhánh giữ chỗ cho nhóm khách hàng VIP.

## Scene_08: Thực thi mã nguồn trên Terminal
**Timeline (root):** 259.24s → 294.24s (35s)

**Visual:** Kiểm thử output trên màn hình dòng lệnh. Hệ thống dừng đúng lúc khi quét trúng phần tử độc hại và bỏ qua các bản ghi lỗi.

**Animation Timeline:**
- 0.2s: command command-typing
- 4.0s: line-1-output show
- 9.0s: line-2-output show
- 14.0s: line-3-output show
- 19.0s: line-4-output show

**Narration (VO):**
> Tiến hành chạy tệp tin python bằng lệnh python tên tệp tin chấm pi-oai. Quan sát kết quả logs trên màn hình terminal: Giao dịch một trăm năm mươi được xử lý, giá trị âm năm bị bỏ qua, và ngay khi gặp lỗi độc hại âm chín trăm chín mươi chín, chương trình in ra cảnh báo và kết thúc ngay lập tức.

## Scene_09: Lỗi chí tử - Vòng lặp vô tận
**Timeline (root):** 294.24s → 334.24s (40s)

**Visual:** So sánh lỗi lặp vô tận (Infinite Loop) khi dùng cần-ti-niu trong vòng lặp oai. Phải tăng chỉ số in-đếch trước khi gọi cần-ti-niu.

**Animation Timeline:**
- 0.2s: load-comparison
- 5.0s: bad-code highlight-error
- 15.0s: good-code highlight-fix

**Narration (VO):**
> Một lỗi cực kỳ phổ biến của lập trình viên là sử dụng cần-ti-niu trong vòng lặp oai mà quên cập nhật biến đếm. Điều này làm cho điều kiện lặp luôn đúng ở giá trị lỗi, dẫn đến hiện tượng treo chương trình và tràn bộ nhớ. Bạn luôn phải tăng biến chỉ mục trước khi gọi cần-ti-niu.

## Scene_10: Cảnh báo Code Chết (Unreachable Code)
**Timeline (root):** 334.24s → 369.24s (35s)

**Visual:** Các dòng mã nằm ngay sau bờ-rếch hoặc cần-ti-niu trong cùng một khối lệnh sẽ không bao giờ được thực thi, tạo ra mã nguồn chết.

**Animation Timeline:**
- 0.2s: card-alert pulse
- 4.5s: code-dead highlight-red

**Narration (VO):**
> Hãy lưu ý về mã nguồn chết. Khi một câu lệnh bờ-rếch hay cần-ti-niu được thực thi không điều kiện hoặc đặt sai vị trí, toàn bộ khối lệnh phía sau nó trong phạm vi lặp sẽ bị trình biên dịch bỏ qua. Hãy tránh cấu trúc này để giữ mã nguồn tường minh, dễ bảo trì.

## Scene_11: Giải quyết lỗi IndentationError bằng Pass
**Timeline (root):** 369.24s → 404.24s (35s)

**Visual:** Viết khối lệnh rỗng không có pát gây lỗi cú pháp nghiêm trọng so với việc sử dụng pát để biên dịch thành công.

**Animation Timeline:**
- 0.2s: panels fade-in
- 5.0s: left-panel highlight-error
- 12.0s: right-panel highlight-success

**Narration (VO):**
> Để so sánh trực quan, việc để trống khối lệnh con của các câu lệnh cấu trúc như íp hoặc pho sẽ khiến trình biên dịch ném ra lỗi in-đen-tây-sơn e-rơ ngay lập tức. Khi đặt từ khóa pát vào, trình thông dịch hiểu rằng đây là một khối rỗng hợp lệ và chương trình chạy hoàn toàn bình thường.

## Scene_12: Quy tắc thiết kế vòng lặp chuẩn hóa
**Timeline (root):** 404.24s → 439.24s (35s)

**Visual:** Quy trình 3 bước thiết kế vòng lặp an toàn: Định hình logic thoát sớm, xử lý ngoại lệ trung gian và giữ chỗ cấu trúc phát triển tương lai.

**Animation Timeline:**
- 0.2s: step-1 fade-in
- 4.0s: step-2 fade-in
- 8.0s: step-3 fade-in

**Narration (VO):**
> Tóm lại, quy trình tối ưu khi làm việc với vòng lặp gồm ba bước: Thứ nhất, xác định điều kiện dừng khẩn cấp bằng bờ-rếch để bảo vệ tài nguyện. Thứ hai, lọc nhanh các bản ghi lỗi bằng cần-ti-niu và luôn nhớ tăng biến đếm. Thứ ba, dùng pát để phác thảo các tính năng mở rộng sau này.


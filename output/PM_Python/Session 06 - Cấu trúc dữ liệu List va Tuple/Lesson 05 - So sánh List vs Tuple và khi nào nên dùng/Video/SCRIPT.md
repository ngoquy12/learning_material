# HyperFrames Script: Session 06 — Lesson 05

**Lesson:** So sánh List vs Tuple và khi nào nên dùng
**Technology Stack:** python/core
**Total Duration:** 260.0s
**Scene Count:** 8

---

## Scene_01: Giới thiệu bài học & Bối cảnh thực tế
**Timeline (root):** 0.00s → 30.00s (30s)

**Visual:** List và Tuple là hai cấu trúc cơ bản lưu trữ tuần tự nhưng khác biệt hoàn toàn về tối ưu bộ nhớ và khả năng chỉnh sửa dữ liệu.

**Animation Timeline:**
- 0.2s: intro-title fade in
- 3.0s: flow-diagram-fade-in
- 25.0s: transition-out

**Narration (VO):**
> Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education, trong nội dung bài học này, chúng ta sẽ cùng nhau tìm hiểu về So sánh List vs Tuple và khi nào nên dùng. Trong phát triển phần mềm thực tế, việc quản lý tài nguyên bộ nhớ và tốc độ xử lý là bài toán vô cùng quan trọng. Các em sẽ thường xuyên phải đưa ra quyết định lựa chọn cấu trúc dữ liệu lưu trữ để tối ưu hóa hệ thống. Chúng ta sẽ cùng phân tích sự khác nhau cốt lõi về bản chất để đưa ra những quyết định thiết kế tối ưu nhất.

## Scene_02: Tính chất Đột biến vs Bất biến
**Timeline (root):** 30.00s → 62.00s (32s)

**Visual:** List hỗ trợ thay đổi (mutable: append, pop) còn Tuple thì cố định (immutable), ngăn chặn mọi hành vi chỉnh sửa sau khi khai báo.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: comparison-table-appear
- 10.0s: highlight-list-methods
- 20.0s: highlight-tuple-immutable
- 30.0s: exit-cleanup

**Narration (VO):**
> Hãy xem xét thuộc tính cơ bản nhất: tính đột biến. Kiểu dữ liệu List trong Python là miu-tơ-bồ, cho phép sửa đổi dữ liệu động. Ngược lại, Tuple là im-miu-tơ-bồ, tức là bất biến sau khi được khởi tạo. Để thay đổi dữ liệu trong lít-xtơ, chúng ta dùng phương thức úp-pen hoặc gán trực tiếp. Còn đối với tơ-pồ, mọi cố gắng thay đổi giá trị một phần tử sẽ khiến hệ thống ném ra lỗi Tai-pơ-Lỗi lập tức.

## Scene_03: Phân tích cơ chế bộ nhớ của List
**Timeline (root):** 62.00s → 95.00s (33s)

**Visual:** List sử dụng cơ chế cấp phát thừa bộ nhớ (Over-allocation) để tăng tốc độ cho xử lý động, làm dung lượng tiêu hao cao hơn.

**Animation Timeline:**
- 0.2s: code-syntax-hl
- 8.0s: highlight-empty-list-size
- 18.0s: draw-over-allocation-block
- 30.0s: fade-out

**Narration (VO):**
> Chúng ta hãy cùng kiểm chứng sự khác biệt này thông qua mã nguồn Python thực tế. Bằng việc import thư viện sys và sử dụng hàm sys chấm get-sai-ợp-xai, ta thấy kích thước khởi tạo của một lít-xtơ rỗng là năm mươi sáu bai. Khi thêm các phần tử mới, Python sẽ chủ động cấp phát thừa bộ nhớ để tối ưu cho các thao tác append tiếp theo. Cơ chế này gọi là dynamic over allocation, giúp giảm tần suất cấp phát lại bộ nhớ.

## Scene_04: Tối ưu hóa bộ nhớ của Tuple
**Timeline (root):** 95.00s → 127.00s (32s)

**Visual:** Tuple cấp phát bộ nhớ tĩnh vừa khít với kích thước cấu trúc, giúp tiết kiệm bộ nhớ RAM cực kỳ hiệu quả.

**Animation Timeline:**
- 0.2s: code-render
- 6.0s: highlight-tuple-empty-size
- 16.0s: draw-exact-allocation-block
- 29.0s: slide-out

**Narration (VO):**
> Bây giờ, chúng ta chạy đoạn mã tương tự đối với tơ-pồ rỗng. Kết quả trả về từ sys chấm get-sai-ợp-xai chỉ là bốn mươi bai, cực kỳ nhỏ gọn so với lít-xtơ. Vì là bất biến, Tuple không cần cấu trúc dự phòng Dynamic Over Allocation. Bộ nhớ cho các phần tử được cấp phát chính xác vừa đủ. Nhờ đó, việc sử dụng tơ-pồ giúp tiết kiệm tài nguyên RAM đáng kể khi làm việc với hàng triệu dòng dữ liệu.

## Scene_05: Đo lường Hiệu năng Tốc độ
**Timeline (root):** 127.00s → 162.00s (35s)

**Visual:** Tuple có tốc độ khởi tạo nhanh hơn đáng kể so với List nhờ vào cơ chế tái sử dụng tài nguyên (constant folding và caching).

**Animation Timeline:**
- 0.2s: cli-display
- 5.0s: run-list-timing
- 15.0s: run-tuple-timing
- 22.0s: highlight-speedup-multiplier
- 32.0s: fade-out

**Narration (VO):**
> Bên cạnh bộ nhớ, tốc độ khởi tạo cũng là điểm khác biệt lớn vượt trội của tơ-pồ. Các em hãy chú ý màn hình, chúng ta cùng sử dụng thư viện tai-mit để so sánh. Khi ta tạo một lít-xtơ liên tục một triệu lần so với một tơ-pồ tương ứng, tơ-pồ chạy nhanh hơn khoảng năm đến sáu lần. Đó là do Python lưu trữ các tơ-pồ tĩnh vào vùng nhớ đệm tái sử dụng giúp hệ thống không phải liên tục yêu cầu hệ điều hành phân phối tài nguyên.

## Scene_06: Quy tắc lựa chọn cấu trúc dữ liệu
**Timeline (root):** 162.00s → 197.00s (35s)

**Visual:** Chọn List cho dữ liệu thay đổi linh hoạt (giỏ hàng, stack/queue). Chọn Tuple cho dữ liệu cố định (tọa độ, cấu hình hệ thống, bản ghi database).

**Animation Timeline:**
- 0.5s: table-headers-show
- 8.0s: row-one-animate
- 18.0s: row-two-animate
- 30.0s: exit

**Narration (VO):**
> Vậy thì, quy tắc áp dụng trong thực tiễn là gì? Các em hãy ghi nhớ nguyên tắc đơn giản sau. Dùng lít-xtơ khi tập hợp dữ liệu cần thay đổi liên tục, ví dụ như danh sách giỏ hàng của người dùng, hoặc danh sách tác vụ chờ xử lý. Ngược lại, hãy dùng tơ-pồ cho các tập hợp dữ liệu không thay đổi, chẳng hạn tọa độ bản đồ, thông tin cấu hình cổng hệ thống, hay các bản ghi đọc từ cơ sở dữ liệu lên.

## Scene_07: Cạm bẫy thiết kế: Tuple chứa List
**Timeline (root):** 197.00s → 230.00s (33s)

**Visual:** Không nên để List bên trong Tuple, vì tính đổi được của List sẽ phá vỡ mục tiêu an toàn dữ liệu của Tuple.

**Animation Timeline:**
- 0.2s: alert-banner-pop
- 5.0s: code-segment-type
- 15.0s: highlight-mutable-element-mutation
- 28.0s: fade-out

**Narration (VO):**
> Các em lưu ý phần quan trọng này nhé! Có một hiểu lầm cực kỳ tai hại, đó là nghĩ rằng mọi phần tử trong tơ-pồ đều bất biến. Điều này không đúng nếu tơ-pồ chứa một phần tử thuộc kiểu miu-tơ-bồ như một lít-xtơ chẳng hạn. Mặc dù chúng ta không thể gán lại trực tiếp phần tử đó, nhưng ta vẫn có thể sửa đổi nội dung bên trong lít-xtơ đó. Điều này phá vỡ tính bất biến tuyệt đối của tơ-pồ, tạo ra những lỗi logic khó phát hiện.

## Scene_08: Tóm tắt bài học & Kết quả
**Timeline (root):** 230.00s → 260.00s (30s)

**Visual:** Chìa khóa tối ưu hiệu năng Python: List linh hoạt tối đa; Tuple tiết kiệm bộ nhớ và an toàn tuyệt đối.

**Animation Timeline:**
- 0.2s: summary-display
- 10.0s: highlight-summary-points
- 25.0s: sign-off-text-show
- 29.5s: fade-out-all

**Narration (VO):**
> Tóm lại, hiểu rõ bản chất cơ học bên dưới của lít-xtơ và tơ-pồ giúp các em viết code Python hiệu năng cao và an toàn hơn cho hệ thống. Hãy cân nhắc kỹ giữa tính linh hoạt của lít-xtơ và sự tối ưu, bảo mật dữ liệu của tơ-pồ. Trong nội dung bài học kế tiếp, chúng ta sẽ bắt đầu nghiên cứu sâu hơn về cấu trúc Set và Dictionary. Cảm ơn các em đã theo dõi, hẹn gặp lại trong các bài học tiếp theo!


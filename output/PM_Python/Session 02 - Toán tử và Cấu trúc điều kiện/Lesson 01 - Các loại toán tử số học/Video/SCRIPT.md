# HyperFrames Script: Session 02 — Lesson 01

**Lesson:** Các loại toán tử số học
**Technology Stack:** python/core
**Total Duration:** 476.39s
**Scene Count:** 12

---

## Scene_01: Bài toán thực tế trong kho vận thông minh
**Timeline (root):** 9.24s → 44.24s (35s)

**Visual:** Bài toán tối ưu quy trình đóng gói hàng hóa trong kho vận thông minh thông qua việc xác định số lượng thùng chứa và sản phẩm dư thừa.

**Animation Timeline:**
- 0.2s: flowchart-container fade-in
- 4.5s: logistic-problem-statement highlight
- 12.0s: flow-nodes connection line draw

**Narration (VO):**
> Trong ngành logistics, tối ưu hóa quy trình đóng gói là bài toán quyết định chi phí vận hành. Khi xử lý hàng triệu mặt hàng mỗi ngày, các hệ thống quản lý kho vận thông minh cần tự động tính toán cách phân phối đều sản phẩm vào các thùng chứa chuyên dụng có kích thước tiêu chuẩn cố định. Thử thách lập trình ở đây là xác định chính xác số lượng thùng hàng được đóng đầy hoàn toàn để xếp lên xe tải, đồng thời lọc ra lượng sản phẩm dư thừa còn lại để chuyển sang dây chuyền xử lý thủ công mà không xảy ra sai sót.

## Scene_02: Thiết lập các biến số ban đầu
**Timeline (root):** 44.24s → 79.24s (35s)

**Visual:** Khai báo các biến số đầu vào biểu thị tổng số lượng sản phẩm và sức chứa của thùng hàng theo quy chuẩn PEP 8.

**Animation Timeline:**
- 0.2s: code-editor-mockup show
- 3.5s: line-1-highlight keyframe
- 15.0s: code-annotation-tooltip active

**Narration (VO):**
> Để giải quyết bài toán này trong Python, bước đầu tiên là khai báo các biến số biểu diễn tham số đầu vào tuân thủ theo tiêu chuẩn pep 8. Chúng ta gán giá trị năm trăm hai mươi bảy cho biến total_products đại diện cho tổng lượng hàng hóa, và giá trị hai mươi lăm cho biến box_capacity thể hiện sức chứa tối đa của một thùng hàng tiêu chuẩn. Việc định hình cấu trúc dữ liệu minh bạch ở bước này giúp mã nguồn dễ dàng thích ứng khi quy mô sản xuất thay đổi.

## Scene_03: Toán tử chia lấy nguyên để tính số thùng hàng
**Timeline (root):** 79.24s → 119.24s (40s)

**Visual:** Sử dụng toán tử phép chia lấy phần nguyên (//) nhằm triệt tiêu phần thập phân lẻ, cho ra chính xác số lượng thùng hàng cần xếp.

**Animation Timeline:**
- 0.2s: display-code-block enter
- 5.0s: highlight-floor-division-operator color-cyan
- 18.0s: show-operation-result-badge 'full_boxes = 21'

**Narration (VO):**
> Để xác định chuẩn xác số lượng thùng hàng được lấp đầy hoàn toàn, ta sử dụng toán tử hai gạch chéo, tức là phép chia lấy phần nguyên trong Python. Phép toán này tiến hành chia lượng tổng sản phẩm cho sức chứa tối đa của thùng và cắt bỏ toàn bộ phần thập phân phía sau kết quả, trả về cho ta giá trị nguyên là hai mươi mốt. Nhờ toán tử này, hệ thống sẽ chỉ xếp hàng lên xe tải những thùng đã được đóng gói kín kẽ mà không lo gặp lỗi số lẻ thập phân.

## Scene_04: Toán tử chia lấy dư để trích xuất sản phẩm thừa
**Timeline (root):** 119.24s → 159.24s (40s)

**Visual:** Toán tử chia lấy dư (%) được sử dụng để xác định số lượng mẫu vật còn lại chưa thể đóng gói theo tiêu chuẩn.

**Animation Timeline:**
- 0.2s: line-code-display active
- 6.0s: highlight-modulo-operator color-green
- 20.0s: show-modulo-result-badge 'remaining_products = 2'

**Narration (VO):**
> Những sản phẩm dư thừa không thể lấp đầy một thùng nguyên vẹn sẽ được lọc ra nhờ toán tử phần trăm, ký hiệu của phép chia lấy dư. Bằng lập luận toán học này, hệ thống thực hiện phép tính chia năm trăm hai mươi bảy cho hai mươi lăm và trích xuất phần dư cuối cùng là hai. Số dư này phản ánh đúng số sản phẩm chưa thể đóng thùng hàng loạt mà sẽ được định hướng trực tiếp sang làn đóng gói thủ công của kho bãi.

## Scene_05: So sánh phép chia thông thường và chia lấy nguyên
**Timeline (root):** 159.24s → 204.24s (45s)

**Visual:** Bảng đối chiếu sự khác biệt về kết quả và kiểu dữ liệu trả về giữa phép chia thông thường (/) và phép chia lấy nguyên (//).

**Animation Timeline:**
- 0.2s: comparison-table-container fade-in
- 8.0s: row-normal-division highlight-yellow
- 25.0s: row-floor-division highlight-green

**Narration (VO):**
> Trong lập trình Python, việc phân biệt cơ chế hoạt động của toán tử một gạch chéo là phép chia thông thường và hai gạch chéo là phép chia lấy nguyên là cực kỳ tối quan trọng. Toán tử một gạch chéo luôn mặc định trả về kết quả dưới dạng số thực float, kể cả khi phép chia hết. Trái lại, toán tử hai gạch chéo chỉ giữ lại phần nguyên dạng số nguyên int nếu tất cả toán hạng là số nguyên, giúp tối ưu hóa bộ nhớ và tăng tốc độ xử lý khi phân tích số lượng thực tế.

## Scene_06: Quy tắc tự động ép kiểu với toán hạng số thực
**Timeline (root):** 204.24s → 239.24s (35s)

**Visual:** Bảng minh họa quy luật tự động ép kiểu: Nếu một toán hạng là float, kết quả phép toán // hoặc % sẽ có kiểu float.

**Animation Timeline:**
- 0.2s: casting-rules-panel show
- 6.0s: test-case-1-highlight animation
- 18.0s: test-case-2-highlight animation

**Narration (VO):**
> Một quy tắc cần ghi nhớ là hành vi tự động ép kiểu số học trong Python. Khi thực hiện phép chia lấy nguyên hoặc chia lấy dư, nếu có bất kỳ toán hạng nào tham gia tính toán là kiểu số thực float, thì kết quả trả về sẽ tự động chuyển đổi sang kiểu số thực float tương ứng. Việc nắm chắc cơ chế này giúp người lập trình tránh được các sai số logic tinh vi khi kết hợp các phép tính có cấu trúc dữ liệu không đồng nhất.

## Scene_07: Tính toán tài chính bằng toán tử nhân và trừ
**Timeline (root):** 239.24s → 279.24s (40s)

**Visual:** Sử dụng toán tử nhân (*) và trừ (-) để thực hiện các phép tính tài chính nâng cao về chi phí cơ sở và chiết khấu.

**Animation Timeline:**
- 0.2s: code-financials-block visible
- 4.5s: highlight-multiplication-operation line-1
- 18.0s: highlight-subtraction-operation line-2

**Narration (VO):**
> Tiếp theo, ta ứng dụng toán tử nhân và trừ để hoàn tất việc xử lý hóa đơn tự động. Số tiền cơ bản được tính bằng toán tử nhân giữa số thùng hàng nguyên vẹn thu được với đơn giá của mỗi thùng hàng. Tiếp theo, ta trừ đi khoản chiết khấu năm phần trăm cho doanh nghiệp bằng cách áp dụng toán tử trừ. Phép toán mở rộng này giúp xuất ra hóa đơn thực tế và minh bạch cho dòng tiền hệ thống.

## Scene_08: Thực thi chương trình trên Terminal
**Timeline (root):** 279.24s → 314.24s (35s)

**Visual:** Sử dụng giao diện dòng lệnh terminal để thực thi chương trình Python và kiểm chứng các thông số tính toán đầu ra.

**Animation Timeline:**
- 0.2s: terminal-window open
- 4.0s: type-command-simulation active
- 12.0s: output-lines-sequence print-result

**Narration (VO):**
> Sau khi hoàn thành phần viết mã nguồn, chúng ta thực hiện gọi tệp tin Python trên giao diện dòng lệnh terminal để kiểm thử kết quả. Dòng lệnh print sẽ hiển thị chi tiết các chỉ số đầu ra. Kết quả cho thấy đúng hai mươi mốt thùng hàng đã đóng đầy, hai sản phẩm còn dư, và tổng chi phí vận hành thực tế đã được khấu trừ chính xác. Chương trình vận hành hoàn hảo không xảy ra trục trặc.

## Scene_09: Cảnh báo lỗi chia cho không - ZeroDivisionError
**Timeline (root):** 314.24s → 354.24s (40s)

**Visual:** Lỗi hệ thống thường gặp: ZeroDivisionError xuất hiện khi thực hiện phép chia đầu vào với giá trị bộ chia bằng không.

**Animation Timeline:**
- 0.2s: display-red-alert-card shown
- 8.0s: exception-traceback-text blink
- 22.0s: guard-clause-code-snippet highlight

**Narration (VO):**
> Trong lập trình cần lưu ý lỗi bảo mật nghiêm trọng là ZeroDivisionError. Lỗi này bùng phát khi hệ thống xử lý tính toán mà bộ chia của phép chia thông thường, phép chia lấy nguyên hoặc chia lấy dư có giá trị bằng không. Để ngăn chặn hệ thống bị sập đột ngột trong môi trường sản xuất thực tế, chúng ta luôn cần triển khai cơ chế kiểm tra điều kiện nhằm xác thực mẫu số khác không trước khi tính toán.

## Scene_10: Cảnh báo lỗi bất tương thích kiểu dữ liệu - TypeError
**Timeline (root):** 354.24s → 394.24s (40s)

**Visual:** Lỗi kiểu dữ liệu: TypeError xuất hiện khi tính toán số học giữa kiểu dữ liệu số và dữ liệu chuỗi ký tự text.

**Animation Timeline:**
- 0.2s: display-warning-alert-card shown
- 6.0s: error-text-highlight animation
- 22.0s: fix-command-hint text-green

**Narration (VO):**
> Lỗi runtime phổ biến tiếp theo là TypeError. Ngoại lệ này xảy ra khi cố gắng thực hiện các phép toán số học như cộng, trừ, nhân, chia giữa kiểu dữ liệu số và kiểu chuỗi văn bản str chưa được chuyển đổi loại hình phù hợp. Giải pháp triệt để là chuyển đổi kiểu chuỗi chữ số thu được về dạng số nguyên hoặc số thực thích hợp bằng các hàm int hoặc float trước khi đưa vào luồng tính toán số học.

## Scene_11: Tối ưu hóa hiệu năng cấp kiến trúc hệ thống
**Timeline (root):** 394.24s → 429.24s (35s)

**Visual:** Vị trí tối ưu trong xử lý tính toán tốc độ cao tại tầng xử lý trung tâm nhờ áp dụng toán tử cơ bản.

**Animation Timeline:**
- 0.2s: architecture-flow-diagram draw
- 5.5s: CPU-process-node focus
- 18.0s: loadrate-indicator-graph dynamic-pulse

**Narration (VO):**
> Ở góc độ thiết kế kiến trúc hệ thống lớn, việc tận dụng hiệu quả các phép toán số học cơ bản là chìa khóa để tinh chỉnh hiệu suất. Việc thực thi phép chia lấy nguyên và lấy dư đơn giản giúp giảm bớt cấu trúc phức tạp, giảm tải chu kỳ xử lý của CPU khi phải giải quyết hàng triệu đơn hàng của hệ thống phân phối trong thời gian thực mà không phụ thuộc vào thư viện cồng kềnh ngoài.

## Scene_12: Tổng kết bài học toán tử số học
**Timeline (root):** 429.24s → 464.24s (35s)

**Visual:** Tổng kết kiến thức cốt lõi: Các loại toán tử số học cơ bản, cơ chế ép kiểu tự động và các quy tắc phòng tránh lỗi runtime.

**Animation Timeline:**
- 0.2s: summary-cheat-sheet active
- 5.0s: summary-first-bullet highlight-effect
- 15.0s: summary-second-bullet highlight-effect

**Narration (VO):**
> Tóm lại, việc nắm vững sáu toán tử số học cơ bản cùng với các quy tắc tự động ép kiểu dữ liệu giúp viết mã sạch, tối ưu hóa thuật toán logistics. Hãy luôn lưu ý kiểm soát các lỗi ngoại lệ hệ thống như chia cho không và sai lệch kiểu dữ liệu để hệ thống đạt được hiệu suất và độ tin cậy vượt trội nhất. Chúc lộ trình học tập của quý vị đạt được năng suất cao.


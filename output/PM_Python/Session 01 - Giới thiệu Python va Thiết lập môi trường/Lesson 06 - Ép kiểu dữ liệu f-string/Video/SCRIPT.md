# HyperFrames Script: Session 01 — Lesson 06

**Lesson:** Ép kiểu dữ liệu f-string
**Technology Stack:** python/core
**Total Duration:** 446.39s
**Scene Count:** 12

---

## Scene_01: Bối cảnh nghiệp vụ thu thập dữ liệu
**Timeline (root):** 9.24s → 44.24s (35s)

**Visual:** Luồng nghiệp vụ xử lý dữ liệu đầu vào: Nhập liệu thô, thực hiện ép kiểu số học, và xuất báo cáo trực quan cho người dùng.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: flow-step-1 fade-in
- 10.0s: flow-arrow-1 active
- 18.0s: flow-step-2 fade-in
- 25.0s: flow-arrow-2 active
- 30.0s: flow-step-3 fade-in

**Narration (VO):**
> Trong phát triển phần mềm doanh nghiệp, luồng dữ liệu bắt nguồn từ việc thu thập thông tin người dùng. Khi hệ thống nhận các giá trị như đơn giá hoặc số lượng qua thiết bị ngoại vi, tính chuẩn xác của kiểu dữ liệu quyết định sự ổn định của toàn bộ logic xử lý phía sau.

## Scene_02: Bản chất dữ liệu từ hàm input
**Timeline (root):** 44.24s → 79.24s (35s)

**Visual:** So sánh kiểu dữ liệu thực tế nhận được từ bàn phím đối lập với kiểu dữ liệu mong đợi cho tính toán số học.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 1.0s: col-1 show-active
- 15.0s: col-2 show-active

**Narration (VO):**
> Bản chất hàm in-put trong ngôn ngữ Python luôn trả về một chuỗi ký tự, hay còn gọi là dòng định dạng xtring, ngay cả khi người dùng nhập số nguyên hay số thực. Điều này tạo ra sự bất đồng nhất giữa định dạng lưu trữ vật lý và ý đồ tính toán thực tế.

## Scene_03: Rủi ro lỗi logic TypeError
**Timeline (root):** 79.24s → 114.24s (35s)

**Visual:** Cảnh báo lỗi hệ thống TypeError khi nhân trực tiếp kiểu chuỗi thay vì kiểu số.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 2.0s: alert-box shake
- 12.0s: highlight-reason show

**Narration (VO):**
> Nếu tiến hành tính toán số học trực tiếp trên giá trị trả về từ hàm in-put, Python sẽ lập tức báo lỗi taip e-rơ. Hệ thống không thể nhân một chuỗi ký tự với một chuỗi ký tự khác, gây ngắt quãng chương trình đột ngột.

## Scene_04: Quy trình ép kiểu Type Casting
**Timeline (root):** 114.24s → 149.24s (35s)

**Visual:** Sơ đồ chuyển đổi kiểu dữ liệu đầu vào: Lọc điều kiện để phân phối sang hàm chuyển đổi số nguyên hoặc số thực tương ứng.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 1.0s: node-main fade-in
- 15.0s: branch-split activate

**Narration (VO):**
> Giải pháp triệt để là thực hiện ép kiểu, hay còn gọi là taip cát-tinh. Đây là quá trình chuyển đổi kiểu dữ liệu từ chuỗi ký tự ban đầu sang các kiểu số chuyên biệt trước khi chuyển sang các tầng xử lý logic tiếp theo.

## Scene_05: Ép kiểu số nguyên bằng hàm int
**Timeline (root):** 149.24s → 184.24s (35s)

**Visual:** Phương pháp sử dụng hàm int() để ép kiểu chuỗi số nguyên thành kiểu dữ liệu Integer trong Python.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: code-line-1 type
- 10.0s: code-line-2 type
- 20.0s: comment-highlight show

**Narration (VO):**
> Đối với các đại lượng đếm được như số lượng sản phẩm hay số lượng đơn hàng, hàm int sẽ phân tích chuỗi ký tự và chuyển đổi thành số nguyên trong bộ nhớ, tối ưu hóa không gian lưu trữ và tốc độ xử lý.

## Scene_06: Ép kiểu số thực bằng hàm float
**Timeline (root):** 184.24s → 219.24s (35s)

**Visual:** Cách sử dụng hàm float() để xử lý số thực có phần thập phân từ nguồn dữ liệu đầu vào dạng chuỗi.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: code-line-1 type
- 12.0s: code-line-2 type
- 22.0s: highlight-float show

**Narration (VO):**
> Với các đại lượng đo lường cần độ chính xác cao như đơn giá, tỷ lệ phần trăm hoặc thuế suất, hàm phờ-lốt là lựa chọn bắt buộc để chuyển đổi chuỗi sang định dạng số thực dấu phẩy động.

## Scene_07: Rủi ro lỗi định dạng ValueError
**Timeline (root):** 219.24s → 254.24s (35s)

**Visual:** Cảnh báo lỗi ValueError khi chuỗi ký tự đầu vào chứa ký tự không hợp lệ để thực hiện ép kiểu.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 2.0s: error-shake
- 15.0s: highlight-solution show

**Narration (VO):**
> Lỗi va-liu e-rơ xảy ra khi chuỗi đầu vào chứa các ký tự đặc biệt hoặc chữ cái mà các hàm int hoặc phờ-lốt không thể biên dịch thành số. Việc kiểm soát lỗi này rất quan trọng để đảm bảo tính an toàn của luồng nghiệp vụ.

## Scene_08: Sai số dấu phẩy động trong hiển thị
**Timeline (root):** 254.24s → 289.24s (35s)

**Visual:** Đối chiếu việc hiển thị số thực thô làm giảm trải nghiệm người dùng với việc định dạng chuẩn hóa tiền tệ.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 1.0s: show-bad-output
- 15.0s: show-good-output

**Narration (VO):**
> Trong kết xuất báo cáo tài chính, số thực thường gặp lỗi biểu diễn dấu phẩy động với các chữ số thập phân kéo dài vô hạn. Điều này làm giảm tính chuyên nghiệp của giao diện và gây khó khăn cho việc đối soát số liệu.

## Scene_09: Cơ chế nội suy của f-string
**Timeline (root):** 289.24s → 324.24s (35s)

**Visual:** Cơ chế nội suy trực tiếp biến vào trong chuỗi ký tự bằng cách đặt ký tự f trước dấu nháy.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: type-code
- 15.0s: highlight-f-prefix
- 25.0s: show-console-output

**Narration (VO):**
> Cú pháp ép-xtring ra đời như một giải pháp thay thế hoàn hảo cho phương thức chấm pho-mát truyền thống hay toán tử phần trăm kiểu ngôn ngữ C cổ điển. Ép-xtring giúp nhúng trực tiếp các biểu thức lô-gíc vào chuỗi với hiệu năng vượt trội.

## Scene_10: Định dạng số thực với f-string và .2f
**Timeline (root):** 324.24s → 359.24s (35s)

**Visual:** Kỹ thuật định dạng độ chính xác phần thập phân của số thực bằng đặc tả :.2f trong f-string.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 1.0s: type-pi-code
- 12.0s: highlight-format-specifier
- 22.0s: run-formatted-output

**Narration (VO):**
> Bằng cách áp dụng đặc tả định dạng hai chấm chấm hai ép vào trong cặp dấu ngoặc nhọn của ép-xtring, hệ thống sẽ thực hiện làm tròn số thực đến hai chữ số thập phân, đảm bảo hiển thị đúng chuẩn tiền tệ doanh nghiệp.

## Scene_11: Xây dựng kịch bản tính toán hoàn chỉnh
**Timeline (root):** 359.24s → 399.24s (40s)

**Visual:** Chương trình Python hoàn chỉnh kết hợp ép kiểu từ luồng nhập liệu và xuất hóa đơn chuẩn định dạng số thực.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 1.0s: write-inputs
- 10.0s: write-calculation
- 20.0s: write-fstrings
- 32.0s: show-final-terminal

**Narration (VO):**
> Trong ví dụ thực tế này, đơn giá dạng chuỗi được chuyển đổi qua hàm phờ-lốt, số lượng được chuyển đổi qua hàm int. Kết quả nhân logic sau đó được trình bày mạch lạc, căn chỉnh chuyên nghiệp nhờ sự kết hợp giữa ép-xtring và đặc tả định dạng.

## Scene_12: Nguyên tắc thiết kế hệ thống tối ưu
**Timeline (root):** 399.24s → 434.24s (35s)

**Visual:** Ba nguyên tắc nền tảng: Ép kiểu nguồn rõ ràng, Kiểm soát ngoại lệ định dạng, Trình diễn thông tin tối giản bằng f-string.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 1.5s: rule-1 active
- 12.0s: rule-2 active
- 22.0s: rule-3 active

**Narration (VO):**
> Tổng kết lại, việc phân tách rạch ròi quy trình nhận dữ liệu đầu vào, ép kiểu nghiêm ngặt và sử dụng ép-xtring để kiểm soát kết quả đầu ra là tiêu chuẩn phát triển bắt buộc để xây dựng hệ thống phần mềm Python an toàn và tối giản.


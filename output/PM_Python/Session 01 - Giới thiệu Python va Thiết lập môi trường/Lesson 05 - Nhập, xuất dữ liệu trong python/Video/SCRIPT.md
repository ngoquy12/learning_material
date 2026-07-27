# HyperFrames Script: Session 01 — Lesson 05

**Lesson:** Nhập, xuất dữ liệu trong python
**Technology Stack:** python/core
**Total Duration:** 446.39s
**Scene Count:** 12

---

## Scene_01: Tầm quan trọng của tương tác CLI
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Ứng dụng đóng (Giá trị tĩnh, thiếu linh hoạt) đối lập với Ứng dụng tương tác CLI (Nhận giá trị thực tế qua luồng dữ liệu chuẩn).

**Animation Timeline:**
- 0.2s: static-flow fade in
- 2.5s: interactive-flow active icon show
- 5.0s: arrow connections highlighted

**Narration (VO):**
> Trong kỹ nghệ phần mềm chuyên nghiệp, việc xây dựng các ứng dụng tĩnh với giá trị biến gán cứng sẽ biến hệ thống thành một môi trường đóng, thiếu linh hoạt. Để tương tác với người dùng hoặc hệ thống khác, chúng ta cần sử dụng các kênh chuẩn hóa đầu vào và đầu ra. Dòng lệnh CLI là giao thức tương tác trực tiếp giúp nhận dữ liệu thời gian thực và trả về kết quả lập tức thông qua luồng dữ liệu chuẩn.

## Scene_02: Luồng tuần tự thu thập dữ liệu
**Timeline (root):** 39.24s → 74.24s (35s)

**Visual:** Quy trình chuyển đổi dữ liệu: Terminal nhấp nháy nhận đầu vào -> Gửi luồng Byte dạng String -> Ép kiểu int/float -> Đẩy vào CPU xử lý toán học.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: step-1 highlighting edge
- 5.0s: step-2 memory allocation visual effect
- 10.0s: step-3 casting engine transition
- 15.0s: step-4 computation path finalization

**Narration (VO):**
> Hãy phân tích luồng vòng đời dữ liệu. Khi người dùng nhập dữ liệu qua bàn phím và nhấn Enter, Terminal gửi luồng byte thô đến hàm in-put. Hàm này lưu trữ giá trị dưới dạng chuỗi trong bộ nhớ ảo Virtual Machine. Trước khi tính toán, dữ liệu chuỗi cần đi qua bộ ép kiểu để chuyển thành số thực hoặc số nguyên, giúp CPU thực thi chính xác các phép toán.

## Scene_03: Bản chất mặc định của hàm input()
**Timeline (root):** 74.24s → 109.24s (35s)

**Visual:** Hàm input() luôn trả về kiểu dữ liệu chuỗi văn bản (str), kể cả khi người dùng nhập chữ số.

**Animation Timeline:**
- 0.3s: terminal lines typed
- 3.5s: user enters 100
- 7.2s: type command execution highlights class str result

**Narration (VO):**
> Để bắt đầu thu thập dữ liệu, Python cung cấp API toàn cục in-put. Khi chương trình thực thi hàm in-put, tiến trình sẽ tạm ngưng, giải phóng quyền kiểm soát màn hình giao diện dòng lệnh cơ bản để chờ người dùng nhập giá trị. Mọi ký tự được nhập từ bàn phím trước khi ấn phím Enter sẽ được đóng gói nguyên bản dưới dạng một chuỗi văn bản duy nhất.

## Scene_04: Lỗi toán tử trên kiểu chuỗi mặc định
**Timeline (root):** 109.24s → 144.24s (35s)

**Visual:** Lỗi TypeError: Trình biên dịch không thể thực thi phép tính số học trực tiếp trên dữ liệu kiểu str của hàm input.

**Animation Timeline:**
- 0.5s: bad-code highlighted in red
- 4.0s: error details popup dynamic zoom
- 8.5s: solution card slides into frame

**Narration (VO):**
> Một lỗi nghiêm trọng mà biên dịch viên thường gặp là áp đặt các toán tử số học trực tiếp lên chuỗi do hàm in-put trả về. Do kiểu dữ liệu mặc định là xtr, việc thực hiện nhân hai chuỗi hoặc cộng chuỗi với số nguyên sẽ kích hoạt lỗi liên kết kiểu dữ liệu Taip Ê-rơ. Hệ thống sẽ dừng lập tức vì kiểu chuỗi và các loại số nguyên không cùng biểu diễn nhị phân trong bộ nhớ.

## Scene_05: Kỹ thuật ép kiểu số nguyên int()
**Timeline (root):** 144.24s → 179.24s (35s)

**Visual:** Sử dụng hàm int() để chuyển đối tượng chuỗi số nguyên thành số nguyên thực thụ trong bộ nhớ.

**Animation Timeline:**
- 0.2s: line 1 type animation
- 3.0s: line 2 type animation focusing on int() wrapper
- 6.5s: memory visual conversion tag pops up

**Narration (VO):**
> Để khắc phục, chúng ta sử dụng ép kiểu tường minh. Hàm in-t nhận tham số là một chuỗi văn bản và cố gắng biên dịch chuỗi đó thành cấu trúc số nguyên hệ cơ số mười. Quá trình này cấp phát lại không gian bộ nhớ mới cho kiểu số nguyên, cho phép máy ảo Python thực thi các phép toán toán học giống như phép cộng hoặc phép nhân truyền thống.

## Scene_06: Kỹ thuật ép kiểu số thực float()
**Timeline (root):** 179.24s → 214.24s (35s)

**Visual:** Sử dụng hàm float() để xử lý các số có chứa phần thập phân hoặc giá trị đo lường phân số.

**Animation Timeline:**
- 0.2s: line 1 input text highlighted
- 3.5s: float function signature highlighted in cyan
- 7.0s: output precision pointer shows decimal dot

**Narration (VO):**
> Tương tự, đối với các giá trị đo lường độ chính xác cao như giá cả sản phẩm hoặc lãi suất ngân hàng, chúng ta cần ép kiểu sang kiểu phờ-lốt. Hàm phờ-lốt sẽ diễn dịch chuỗi đầu vào thành định dạng số chấm động tương thích tiêu chuẩn I-tri-pơ-lơ bảy trăm tám mươi tư, giúp bảo toàn phần thập phân trong chuỗi số học.

## Scene_07: Cơ chế xuất dữ liệu cơ bản
**Timeline (root):** 214.24s → 249.24s (35s)

**Visual:** Đầu ra mặc định của phương thức print: Tự động ngăn cách các tham số bằng một khoảng trắng đơn.

**Animation Timeline:**
- 0.2s: code writing animation
- 3.5s: space delimiter highlighting under standard output stream

**Narration (VO):**
> Sau khi xử lý thành công, kết quả cần được xuất ra luồng đầu ra tiêu chuẩn thông qua hàm prin-t. Hàm prin-t mặc định nhận danh sách các đối tượng, chuyển đổi chúng thành chuỗi văn bản ký tự thô và gửi trực tiếp ra màn hình dòng lệnh. Các tham số truyền vào hàm được ngăn cách mặc định bằng một khoảng trắng đơn.

## Scene_08: Tùy biến bộ phân tách với tham số sep
**Timeline (root):** 249.24s → 284.24s (35s)

**Visual:** Tham số sep (Separator) chỉ định ký tự ngăn cách các giá trị in thay thế cho kí tự khoảng trắng mặc định.

**Animation Timeline:**
- 0.2s: code structure dynamic layout
- 4.0s: sep keyword highlighted in gold
- 8.0s: console output preview shows vertical lines replacing spaces

**Narration (VO):**
> Hàm prin-t cho phép tùy biến ký tự ngăn cách thông qua đối số từ khóa xép. Theo mặc định, đối số xép nhận giá trị một khoảng trống. Khi chúng ta thay đổi xép thành ký tự gạch đứng hoặc gạch ngang, trình thông dịch sẽ tự động chèn chuỗi này vào giữa các đối số được in ra, giúp định dạng dữ liệu đầu ra chuyên nghiệp.

## Scene_09: Kiểm soát kết thúc dòng với tham số end
**Timeline (root):** 284.24s → 319.24s (35s)

**Visual:** Tham số end quyết định ký tự được in ở cuối dòng đầu ra, mặc định là ký tự xuống dòng n.

**Animation Timeline:**
- 0.2s: line with end parameter visual emphasis
- 4.0s: buffer line output validation without line feed character

**Narration (VO):**
> Tương tự, hành vi kết thúc dòng hiển thị của hàm prin-t được kiểm soát bởi đối số en-đơ. Mặc định, đối số en-đơ chứa ký tự xuống dòng xuyệt n. Bằng cách gán lại tham số en-đơ với các chuỗi ký tự tùy chỉnh hoặc một chuỗi rỗng, lập trình viên có thể giữ con trỏ trên cùng một dòng hoặc hiển thị trạng thái hoàn thành ngay sau kết quả.

## Scene_10: Xây dựng chương trình thanh toán
**Timeline (root):** 319.24s → 364.24s (45s)

**Visual:** Kịch bản đầy đủ đầu vào dữ liệu, ép kiểu tương thích, xử lý logic và cấu hình xuất kết quả.

**Animation Timeline:**
- 0.2s: full script loads
- 5.0s: input and casting highlights sequentially
- 15.0s: calculation tracing line by line
- 28.0s: visual print parameters evaluation

**Narration (VO):**
> Hãy quan sát chương trình thực tế hoàn chỉnh giả lập hệ thống thanh toán. Chúng ta khai báo biến giá sản phẩm và số lượng thông qua hai hàm in-put. Tiếp theo thực hiện ép kiểu sang kiểu phờ-lốt và kiểu in-t chuyên biệt. Cuối cùng, kết quả được tính toán và in ra màn hình sử dụng kết hợp cả hai đối số từ khóa xép và en-đơ để tạo báo cáo chuẩn hóa.

## Scene_11: Mối nguy ngoại lệ ValueError khi ép kiểu
**Timeline (root):** 364.24s → 399.24s (35s)

**Visual:** Ngoại lệ ValueError phát sinh khi chuỗi đầu vào chứa các chữ cái không thể chuyển đổi thành các biểu diễn số.

**Animation Timeline:**
- 0.2s: invalid inputs simulation shown
- 4.5s: ValueError terminal log highlights
- 8.5s: error prevention tips display

**Narration (VO):**
> Lưu ý quan trọng khi chạy chương trình trong thực tế. Nếu người dùng nhập vào các chuỗi không thể ánh xạ thành số như ký tự chữ cái, máy ảo Python sẽ lập tức kích hoạt lỗi ngoại lệ Va-lưu Ê-rơ. Điều này xảy ra do bộ giải mã chuỗi của hàm in-t hoặc phờ-lốt gặp phải cấu trúc biểu diễn không hợp lệ trong hệ đếm.

## Scene_12: Tổng kết quy trình tương tác chuẩn
**Timeline (root):** 399.24s → 434.24s (35s)

**Visual:** Bản đồ quy chuẩn: Đầu vào (luôn là str) -> Ép kiểu bảo vệ (int/float) -> Đầu ra tùy chỉnh (sep/end).

**Animation Timeline:**
- 0.5s: row 1 highlighting
- 3.5s: row 2 highlighting casting operations
- 7.0s: row 3 highlighting outputs logic

**Narration (VO):**
> Tóm lại, quy trình tương tác dữ liệu chuẩn trong Python đòi hỏi việc nắm vững cơ chế thu nhận chuỗi qua hàm in-t, ép kiểu an toàn và định dạng đầu ra tùy biến cao với hàm prin-t. Việc kiểm soát cấu trúc dữ liệu đầu vào và các tham số điều khiển bộ luồng ký tự là tiền đề xây dựng phần mềm ổn định.


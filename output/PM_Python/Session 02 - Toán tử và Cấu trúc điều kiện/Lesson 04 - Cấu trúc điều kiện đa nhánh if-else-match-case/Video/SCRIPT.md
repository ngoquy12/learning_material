# HyperFrames Script: Session 02 — Lesson 04

**Lesson:** Cấu trúc điều kiện đa nhánh if-else-match-case
**Technology Stack:** python/core
**Total Duration:** 416.39s
**Scene Count:** 12

---

## Scene_01: Đặt vấn đề nghiệp vụ xử lý giao dịch
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Hệ thống định tuyến giao dịch trực tuyến đối mặt với bài toán kiểm tra đồng thời Trạng thái giao dịch và Hạng thành viên để phân loại chiết khấu.

**Animation Timeline:**
- 0.2s: intro-title fade in
- 2.5s: columns comparison display
- 28.0s: columns comparison fade out

**Narration (VO):**
> Trong các hệ thống thanh toán trực tuyến, việc định tuyến giao dịch để áp dụng phí và chiết khấu là một lõi nghiệp vụ quan trọng. Hệ thống phải đánh giá đồng thời hai biến số: trạng thái của giao dịch và phân hạng thành viên của khách hàng. Cách tiếp cận truyền thống sử dụng các khối lệnh íp eo lồng nhau thường dẫn đến mã nguồn phức tạp, khó bảo trì khi các chiều dữ liệu phình to.

## Scene_02: Phân tích luồng xử lý điều kiện
**Timeline (root):** 39.24s → 71.24s (32s)

**Visual:** Luồng quyết định kiểm tra trạng thái đơn hàng (Success, Failed, Pending) rồi tiếp tục phân nhánh phân hạng thành viên để tính toán phí.

**Animation Timeline:**
- 0.5s: flow diagram animate in
- 10.0s: highlights active branch success
- 20.0s: highlights active branch failed and pending
- 30.0s: diagram fade out

**Narration (VO):**
> Hãy quan sát luồng xử lý của hệ thống. Luồng dữ liệu đi qua hai tầng kiểm tra. Đầu tiên là kiểm tra trạng thái giao dịch: thành công, thất bại hoặc đang chờ xử lý. Từ nhánh thành công, chúng ta tiếp tục rẽ nhánh dựa trên phân hạng thành viên gồm vàng, bạc và đồng để áp dụng mức chiết khấu. Việc thiết kế sơ đồ rõ ràng sẽ giúp việc thiết lập mã nguồn chính xác.

## Scene_03: Nhược điểm của cấu trúc if lồng nhau
**Timeline (root):** 71.24s → 106.24s (35s)

**Visual:** Đoạn mã mẫu sử dụng cấu trúc if-elif-else nhiều lớp lồng nhau gây ra hiện tượng mã nguồn phình to và giảm tính khả thi khi kiểm thử.

**Animation Timeline:**
- 0.2s: code mockup displayed
- 12.0s: highlight internal depth of nested if statements
- 33.0s: code mockup fade out

**Narration (VO):**
> Trước phiên bản Python 3 chấm 10, các lập trình viên thường dùng cấu trúc íp, e-líp, eo lồng nhau để xử lý hai chiều biến số này. Hãy nhìn vào đoạn mã mẫu. Việc lồng khối lệnh điều kiện này tạo ra cấu trúc mã hình kim tự tháp. Nó làm tăng độ phức tạp thuật toán, đồng thời dễ phát sinh sai sót logic ngoài ý muốn khi có thêm các trạng thái giao dịch hoặc hạng thành viên mới.

## Scene_04: Sức mạnh của match-case trong Python
**Timeline (root):** 106.24s → 136.24s (30s)

**Visual:** Nguyên lý Pattern Matching của match-case cho phép định tuyến logic dựa trên so khớp cấu trúc tuple gồm nhiều biến cùng lúc.

**Animation Timeline:**
- 0.5s: pattern match layout visual loading
- 12.0s: highlights tuple matching route diagram
- 28.0s: layout fade out

**Narration (VO):**
> Nhằm tối ưu hóa luồng rẽ nhánh đa hướng phức tạp, Python 3 chấm 10 đã giới thiệu cấu trúc mátch-kết. Công cụ này cho phép so khớp mẫu cấu trúc dữ liệu một cách trực quan và tường minh. Thay vì phải so sánh từng biến bằng toán tử logic, chúng ta có thể truyền một cặp giá trị túp-pồ vào mệnh đề mátch và so khớp trực tiếp trong các khối kết.

## Scene_05: Khai báo hàm và khởi tạo
**Timeline (root):** 136.24s → 169.24s (33s)

**Visual:** Định nghĩa hàm apply_transaction_policy với các biến baseline fee và discount được định cấu hình bằng 0.0.

**Animation Timeline:**
- 0.5s: code editor setup showing function header
- 15.0s: highlight variables initialization fee and discount
- 31.0s: fade out

**Narration (VO):**
> Hãy bắt đầu triển khai hàm áp dụng chính sách giao dịch. Chúng ta khai báo hàm a-play-tran-sắc-sơn-pô-li-si nhận hai tham số đầu vào là sta-tút và ti-ơ. Đầu tiên, chúng ta khởi tạo giá trị mặc định cho hai biến là phi bằng không chấm không và đít-khao bằng không chấm không. Việc này đảm bảo các biến số luôn được khởi tạo giá trị cơ sở trước khi đi vào cấu trúc mátch.

## Scene_06: Triển khai các case giao dịch thành công
**Timeline (root):** 169.24s → 204.24s (35s)

**Visual:** Sử dụng match-case để kiểm thử cấu trúc tuple (status, tier) cho các trường hợp thành công tương ứng với từng hạng Gold, Silver, Bronze.

**Animation Timeline:**
- 0.2s: typing python match blocks
- 10.0s: highlight gold tier pattern
- 20.0s: highlight silver and bronze tier pattern
- 33.0s: slide selection block

**Narration (VO):**
> Bây giờ, chúng ta viết luồng mátch cho cặp sta-tút và ti-ơ. Mỗi mẫu so khớp sẽ được khai báo bằng từ khóa kết. Trường hợp đầu tiên: nếu trạng thái thành công và hạng vàng, mức phí là năm chấm không và chiết khấu không chấm mười. Tiếp theo, nếu hạng bạc, mức phí là bảy chấm năm và chiết khấu không chấm không năm. Với hạng đồng, mức phí là mười chấm không và chiết khấu bằng không.

## Scene_07: Xử lý trạng thái thất bại và chờ xử lý
**Timeline (root):** 204.24s → 237.24s (33s)

**Visual:** Sử dụng ký tự đại diện gạch dưới (_) để bỏ qua giá trị cấu trúc của phân hạng thành viên trong các case failed và pending.

**Animation Timeline:**
- 0.5s: display code updates
- 12.0s: highlight wildcard character usage in tuple
- 30.0s: fade line focus

**Narration (VO):**
> Đối với các trạng thái thất bại hoặc đang chờ xử lý, chúng ta không cần quan tâm đến phân hạng thành viên của khách hàng. Chúng ta sử dụng ký tự gạch dưới để đại diện cho bất kỳ giá trị nào. Nếu trạng thái thất bại, mức phí mặc định là hai chấm không. Nếu là đang chờ xử lý, mức phí được tính là một chấm không. Việc sử dụng ký tự đại diện giúp đơn giản hóa mã nguồn.

## Scene_08: Cấu hình nhánh mặc định phòng ngừa lỗi
**Timeline (root):** 237.24s → 269.24s (32s)

**Visual:** Bổ sung case dự phòng mặc định để xử lý ngoại lệ và trả lại giá trị tính toán phí và chiết khấu.

**Animation Timeline:**
- 0.5s: type code default block and return statement
- 15.0s: highlight return statement of function
- 30.0s: editor window fade out

**Narration (VO):**
> Cuối cùng, chúng ta cấu hình nhánh mặc định bằng ký tự gạch dưới đơn lẻ. Nhánh này sẽ bắt toàn bộ các trường hợp dữ liệu bất thường hoặc không hợp lệ để tránh lỗi hệ thống, gán mức phí cao là mười lăm chấm không. Sau đó, hàm trả về kết quả là một túp-pồ chứa phi và đít-khao. Toàn bộ logic nghiệp vụ được gói gọn và cực kỳ dễ hiểu.

## Scene_09: Chạy thử nghiệm hàm qua terminal
**Timeline (root):** 269.24s → 304.24s (35s)

**Visual:** Thực thi kiểm thử với nhiều tham số đầu vào trong Terminal để kiểm chứng tính đúng đắn của logic match-case.

**Animation Timeline:**
- 0.5s: trigger terminal display
- 5.0s: type execute command and display lines output
- 32.0s: terminal window fade out

**Narration (VO):**
> Hãy cùng chạy kiểm thử hàm vừa tạo trong môi trường thực tế. Trên màn hình tơ-mi-nơ, chúng ta thực thi tập tin python. Kết quả trả về cho giao dịch thành công của khách hàng hạng vàng là phí năm chấm không và chiết khấu mười phần trăm. Khi thay đổi trạng thái sang thất bại, hệ thống tự động gán phí hai chấm không mà không bị ảnh hưởng bởi hạng thành viên.

## Scene_10: Lỗi IndentationError và SyntaxError
**Timeline (root):** 304.24s → 337.24s (33s)

**Visual:** Các lỗi thụt lề (IndentationError) và thiếu dấu hai chấm (SyntaxError) phổ biến khi triển khai cú pháp match-case.

**Animation Timeline:**
- 0.5s: show pitfall warning card
- 15.0s: highlight bad vs good indentation spacing
- 30.0s: exit active card

**Narration (VO):**
> Trong quá trình viết mã nguồn, hãy chú ý tránh hai lỗi cơ bản là in-đen-tây-sơn-e-rơ và sin-tắc-e-rơ. In-đen-tây-sơn-e-rơ xảy ra khi căn lề thụt dòng không đồng đều giữa các lệnh kết bên dưới khối mátch. Còn sin-tắc-e-rơ thường do thiếu dấu hai chấm ở cuối các dòng điều kiện mátch hoặc kết. Trình biên dịch sẽ báo lỗi lập tức khi phát hiện các lỗi này.

## Scene_11: Lỗi UnboundLocalError và ValueError
**Timeline (root):** 337.24s → 371.24s (34s)

**Visual:** Lỗi UnboundLocalError xuất hiện khi một biến không được định nghĩa ở nhánh điều kiện được thực thi và cách phòng tránh bằng việc khởi tạo biến.

**Animation Timeline:**
- 0.5s: show validation and variable context warnings
- 16.0s: highlight solutions: initialize values at top
- 31.0s: clear layout

**Narration (VO):**
> Tiếp theo là lỗi an-bao-lô-cồ-e-rơ và va-liêu-e-rơ. An-bao-lô-cồ-e-rơ xuất hiện khi bạn sử dụng một biến số bên ngoài khối điều kiện mà biến đó chưa từng được khởi tạo ở các nhánh chạy trước. Chúng ta khắc phục bằng cách luôn khai báo biến mặc định ở đầu hàm. Tránh va-liêu-e-rơ bằng cách ép kiểu và kiểm tra đầu vào trước khi đưa vào cấu trúc so khớp dữ liệu.

## Scene_12: Tổng kết hướng dẫn áp dụng
**Timeline (root):** 371.24s → 404.24s (33s)

**Visual:** So sánh trực quan giữa if-elif-else truyền thống và match-case giúp nhà phát triển quyết định công cụ tối ưu cho từng bài toán.

**Animation Timeline:**
- 0.5s: summary analysis table slides in
- 15.0s: focus highlights on usecases columns
- 30.0s: outro credits fadeout

**Narration (VO):**
> Tổng kết lại, cấu trúc rẽ nhánh giúp điều khiển chương trình xử lý chính xác dựa trên đầu vào. Hãy dùng cấu trúc mátch-kết khi cần tối ưu hóa các điều kiện xử lý đa luồng phức tạp dựa trên hằng số và thuộc tính tĩnh. Với các biểu thức so sánh logic động phức tạp hơn, các bạn vẫn nên lựa chọn cấu trúc íp, e-líp truyền thống để đảm bảo tính linh hoạt tối đa.


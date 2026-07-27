# HyperFrames Script: Session 02 — Lesson 05

**Lesson:** Điều kiện lồng nhau và toán tử ba ngôi
**Technology Stack:** python/core
**Total Duration:** 441.39s
**Scene Count:** 12

---

## Scene_01: Bối cảnh nghiệp vụ doanh nghiệp
**Timeline (root):** 9.24s → 39.24s (30s)

**Visual:** Sơ đồ luồng quyết định thương mại điện tử liên kết giữa cấp độ tài khoản Gold, Silver và giá trị đơn hàng để xác định mức chiết khấu.

**Animation Timeline:**
- 0.2s: flow-nodes fade in
- 2.5s: connection-arrows draw
- 28.0s: scene-out fade out

**Narration (VO):**
> Trong các hệ thống thương mại điện tử thực tế, việc tính toán mức ưu đãi dựa trên cấp độ khách hàng mem-bơ-íp tia và giá trị đơn hàng o-đơ va-lu thường tạo ra các biểu thức kiểm tra phức tạp. Khi các quy định kinh doanh thay đổi liên tục, mã nguồn dễ lâm vào tình trạng phình to theo chiều ngang do lồng ghép quá nhiều câu lệnh rẽ nhánh điều kiện.

## Scene_02: Hiện tượng Pyramid of Doom
**Timeline (root):** 39.24s → 74.24s (35s)

**Visual:** Đoạn mã nguồn Python minh họa cấu trúc if lồng nhau 3 tầng thụt lề sâu tạo thành hình tam giác.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: code-editor zoom in
- 5.0s: highlight-nesting draw-bounds
- 33.0s: code-editor fade out

**Narration (VO):**
> Cách tiếp cận truyền thống sử dụng các khối lệnh íp lồng nhau để xử lý logic này. Cấu trúc lồng nhau tạo ra hiện tượng gọi là pi-ra-mít óp dum. Điều này tăng độ phức tạp thuật toán, cản trở việc kiểm thử tự động, đồng thời gây lãng phí chu kỳ xử lý của luồng điều khiển khi phải duyệt qua nhiều cấu trúc cây quyết định sâu.

## Scene_03: Nguyên lý Flat Structure
**Timeline (root):** 74.24s → 104.24s (30s)

**Visual:** Bảng so sánh cấu trúc rẽ nhánh sâu dạng kim tự tháp với luồng logic phẳng tối giản.

**Animation Timeline:**
- 0.2s: comparison-columns slide in
- 4.0s: bad-column highlight red
- 8.0s: good-column highlight green
- 28.0s: comparison-grid out

**Narration (VO):**
> Để giải quyết vấn đề này, các kỹ sư thường áp dụng nguyên lý thiết kế phẳng. Mục tiêu là duy trì tối đa hai cấp độ rẽ nhánh. Việc cấu trúc lại sơ đồ logic giúp tối ưu hóa bộ nhớ tạm của hệ thống và định hướng các luồng thực thi lệnh của bộ vi xử lý diễn ra trực diện hơn.

## Scene_04: Cấu trúc Toán tử ba ngôi
**Timeline (root):** 104.24s → 139.24s (35s)

**Visual:** Cú pháp định chuẩn của toán tử ba ngôi: variable = value_if_true if condition else value_if_false.

**Animation Timeline:**
- 0.2s: syntax-block scale up
- 3.5s: highlight-keywords green
- 33.0s: syntax-block fade out

**Narration (VO):**
> Toán tử ba ngôi chính là công cụ đắc lực để làm phẳng mã nguồn trong Python. Cú pháp cơ bản bao gồm biến gán, giá trị trả về nếu điều kiện đúng, từ khóa íp, biểu thức lô-gíc, và từ khóa eo-sơ đi kèm giá trị trả về nếu điều kiện sai. Toàn bộ biểu thức được gói gọn trên một dòng lệnh duy nhất.

## Scene_05: Quy trình tối ưu hóa rẽ nhánh
**Timeline (root):** 139.24s → 169.24s (30s)

**Visual:** Sơ đồ 3 bước tối ưu hóa logic: Bước 1 Xác định điều kiện biên, Bước 2 Tách biểu thức phức tạp, Bước 3 Áp dụng toán tử ba ngôi.

**Animation Timeline:**
- 0.2s: step-1 show
- 5.0s: step-2 show
- 10.0s: step-3 show
- 28.0s: steps-list fade out

**Narration (VO):**
> Quy trình tái cấu trúc gồm ba bước rõ ràng. Bước đầu tiên, chúng ta xác định các điều kiện biên để loại bỏ trường hợp ngoại lệ ngay lập tức. Bước thứ hai, tách biệt các kiểm tra biểu thức phức tạp ra các biến trung gian độc lập. Bước cuối cùng, thực hiện gán trực tiếp bằng toán tử ba ngôi để hoàn thiện luồng xử lý.

## Scene_06: Sơ đồ luồng rẽ nhánh phẳng
**Timeline (root):** 169.24s → 204.24s (35s)

**Visual:** Mô hình đồ họa phân luồng dữ liệu khi thực thi toán tử ba ngôi lồng nhau ở mức độ cơ bản.

**Animation Timeline:**
- 0.2s: root-node active
- 4.5s: left-branch show
- 8.5s: right-branch show
- 33.0s: tree-graph fade out

**Narration (VO):**
> Sơ đồ này mô tả chi tiết đường đi của dữ liệu. Khởi đầu từ việc kiểm tra điều kiện chính, chương trình sẽ đánh giá nhánh thành công thông qua một kiểm tra phụ, hoặc chuyển ngay sang việc trả về một giá trị mặc định. Đường đi của mã lệnh sạch hơn, loại bỏ hoàn toàn các cấu trúc rẽ nhánh lồng nhau vô tận.

## Scene_07: Triển khai Code - Gán điều kiện đầu
**Timeline (root):** 204.24s → 244.24s (40s)

**Visual:** Không gian làm việc của VS Code khởi tạo các biến đầu vào cho mô hình mua sắm điện tử.

**Animation Timeline:**
- 0.2s: setup-vars typing
- 38.0s: block-editor freeze

**Narration (VO):**
> Hãy bắt đầu quá trình viết code thực tế. Tôi khai báo biến cớt-xtơ-mơ mem-bơ-íp bằng chuỗi gôl và o-đơ tô-tồ bằng sáu trăm năm mươi chấm không. Đây là các dữ liệu biên chuẩn bị cho việc thực thi giải thuật tính toán giá trị chiết khấu tối ưu trực tiếp.

## Scene_08: Tích hợp Toán tử ba ngôi lồng nhau
**Timeline (root):** 244.24s → 284.24s (40s)

**Visual:** Đoạn mã định nghĩa discount_rate sử dụng toán tử ba ngôi lồng nhau viết gọn trên một dòng.

**Animation Timeline:**
- 0.2s: ternary-line typing
- 10.0s: highlight-condition-1 yellow
- 20.0s: highlight-condition-2 blue
- 38.0s: line-out exit

**Narration (VO):**
> Bây giờ, chúng ta viết toán tử ba ngôi để tính toán đít-cao rết. Giá trị bằng không chấm hai mươi nếu o-đơ tô-tồ lớn hơn năm trăm chấm không. Ngược lại, giá trị sẽ bằng không chấm mười nếu cớt-xtơ-mơ mem-bơ-íp bằng gôl, và nhận giá trị mặc định là không chấm không năm cho các trường hợp còn lại.

## Scene_09: Thực thi tính toán và hiển thị kết quả
**Timeline (root):** 284.24s → 319.24s (35s)

**Visual:** Giao diện Terminal thực thi file main.py in ra kết quả tính toán chiết khấu cụ thể.

**Animation Timeline:**
- 0.2s: terminal-command entry
- 3.0s: output-text reveal
- 33.0s: terminal clear

**Narration (VO):**
> Tiếp theo, ta tính toán giá trị final đít-cao bằng cách nhân o-đơ tô-tồ với đít-cao rết, sau đó in các kết quả ra terminal. Thực thi lệnh python main chấm py, bạn có thể thấy kết quả trả về chính xác với tỷ lệ chiết khấu mong muốn mà không cần tới bất kỳ khối lệnh íp eo-sơ đa tầng nào.

## Scene_10: Quy tắc cốt lõi về giới hạn ký tự
**Timeline (root):** 319.24s → 354.24s (35s)

**Visual:** Cảnh báo chỉ số phức tạp của dòng mã nguồn và giới hạn tiêu chuẩn 80 ký tự để bảo trì hệ thống.

**Animation Timeline:**
- 0.2s: alert-box bounce in
- 5.0s: rule-80-chars highlight
- 33.0s: alert-box slide out

**Narration (VO):**
> Cần chú ý quy tắc kỹ thuật nghiêm ngặt sau. Chỉ áp dụng toán tử ba ngôi cho các biểu thức gán giá trị đơn giản có độ dài dưới tám mươi ký tự. Tuyệt đối tránh việc lồng ghép từ hai toán tử ba ngôi trở lên trên cùng một dòng lệnh, vì điều này sẽ phá vỡ tính dễ đọc của mã nguồn Python.

## Scene_11: Lỗi Runtime thường gặp: Thiếu Else
**Timeline (root):** 354.24s → 389.24s (35s)

**Visual:** Mã lỗi SyntaxError phát sinh khi viết toán tử ba ngôi không có mệnh đề else đi kèm.

**Animation Timeline:**
- 0.2s: error-log appearance
- 4.0s: highlight-missing-else red
- 33.0s: error-log fade out

**Narration (VO):**
> Một lỗi runtime phổ biến là lỗi cú pháp xin-tắc e-rơ khi thiếu thành phần eo-sơ trong biểu thức toán tử ba ngôi. Trình biên dịch của Python yêu cầu bắt buộc phải có đầy đủ giá trị cho cả hai trường hợp đúng và sai để đảm bảo tính toàn vẹn của kết quả trả về trong quá trình gán.

## Scene_12: Lỗi UnboundLocalError và Thứ tự ưu tiên
**Timeline (root):** 389.24s → 429.24s (40s)

**Visual:** Ví dụ về lỗi UnboundLocalError và giải pháp dùng dấu ngoặc đơn để tăng tính tường minh.

**Animation Timeline:**
- 0.2s: fix-box scale in
- 6.5s: highlight-brackets active
- 38.0s: fix-box fade out

**Narration (VO):**
> Cuối cùng, hãy đề phòng lỗi nem e-rơ hoặc ăn-baon-đơ lô-cồ e-rơ khi một nhánh điều kiện chưa khởi tạo giá trị cho biến. Phải đảm bảo thứ tự ưu tiên bằng cách sử dụng dấu ngoặc đơn một cách rõ ràng khi kết hợp toán tử ba ngôi với các phép toán so sánh hoặc các toán tử lô-gíc khác.


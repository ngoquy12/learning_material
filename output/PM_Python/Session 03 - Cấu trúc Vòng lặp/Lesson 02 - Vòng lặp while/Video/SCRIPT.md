# HyperFrames Script: Session 03 — Lesson 02

**Lesson:** Vòng lặp while
**Technology Stack:** python/core
**Total Duration:** 456.39s
**Scene Count:** 12

---

## Scene_01: Bài toán thực tế về luồng dữ liệu động
**Timeline (root):** 9.24s → 44.24s (35s)

**Visual:** Xử lý luồng dữ liệu động có độ dài không cố định là yêu cầu cốt lõi trong các hệ thống xác thực người dùng bảo mật và truyền nhận dữ liệu I O T tuần tự liên tục.

**Animation Timeline:**
- 0.2s: flow-container fade in
- 1.5s: flow-step-1 highlight
- 10.0s: flow-step-2 highlight
- 22.0s: flow-step-3 highlight

**Narration (VO):**
> Trong phát triển phần mềm thực tế, lập trình viên thường xuyên đối mặt với các bài toán xử lý luồng dữ liệu có độ dài không cố định. Ví dụ điển hình là hệ thống yêu cầu người dùng nhập mật khẩu xác thực cho đến khi chính xác, hoặc luồng đọc gói tin liên tục từ thiết bị cảm biến I O T truyền về bộ nhớ đệm cho đến khi xuất hiện tín hiệu ngắt. Những kịch bản này đòi hỏi một cơ chế lặp thông minh, có khả năng kích hoạt và dừng lại dựa trên điều kiện thực tế của dữ liệu.

## Scene_02: Hạn chế của vòng lặp xác định
**Timeline (root):** 44.24s → 74.24s (30s)

**Visual:** Vòng lặp pho bị giới hạn bởi số lần lặp xác định trước và không thể tự động kéo dài hoặc dừng lại theo điều kiện thực tế của luồng dữ liệu đầu vào.

**Animation Timeline:**
- 0.2s: comparison-table fade in
- 2.0s: col-1 highlight
- 15.0s: col-2 highlight

**Narration (VO):**
> Vòng lặp pho với hàm ren sơ đòi hỏi chương trình phải xác định rõ số lần lặp hoặc kích thước của tập hợp dữ liệu trước khi thực thi. Khi áp dụng vào bài toán đọc dữ liệu động, cơ chế này trở nên bất khả thi do không thể dự đoán thời điểm người dùng dừng nhập hoặc thời điểm dữ liệu kết thúc. Đây là lý do chúng ta cần đến một cấu trúc lặp kiểm tra điều kiện linh hoạt hơn.

## Scene_03: Nguyên lý hoạt động của vòng lặp while
**Timeline (root):** 74.24s → 109.24s (35s)

**Visual:** Vòng lặp oai chỉ thực thi khối lệnh khi biểu thức logic đạt giá trị tru, và lập tức thoát luồng xử lý để giải phóng tài nguyên CPU khi điều kiện trả về phôn.

**Animation Timeline:**
- 0.2s: diagram fade in
- 5.0s: path-to-condition animate
- 15.0s: condition-true loop
- 28.0s: condition-false exit

**Narration (VO):**
> Vòng lặp oai giải quyết hạn chế này bằng cách kiểm tra chân trị của một biểu thức logic trước mỗi chu kỳ lặp. Nếu điều kiện trả về giá trị tru, khối lệnh bên trong thân vòng lặp sẽ được thực thi. Sau mỗi chu kỳ kết thúc, luồng điều khiển quay trở lại kiểm tra tiếp điều kiện. Tiến trình chỉ dừng lại và thoát ra ngoài khi biểu thức logic mang giá trị phôn, giúp tối ưu hiệu năng của C P U và bộ nhớ RAM.

## Scene_04: 4 bước thiết kế vòng lặp while an toàn
**Timeline (root):** 109.24s → 144.24s (35s)

**Visual:** Quy trình thiết kế oai an toàn: 1. Khởi tạo biến trạng thái; 2. Thiết lập điều kiện biên; 3. Thực thi nghiệp vụ; 4. Cập nhật biến trạng thái đưa về điểm dừng.

**Animation Timeline:**
- 0.2s: grid-steps fade in
- 3.0s: step-1 active
- 10.0s: step-2 active
- 18.0s: step-3 active
- 26.0s: step-4 active

**Narration (VO):**
> Để xây dựng một vòng lặp oai an toàn, lập trình viên cần tuân thủ cấu trúc bốn bước. Bước một, khởi tạo biến điều khiển trước khi khai báo vòng lặp. Bước hai, thiết lập biểu thức logic chặt chẽ ngay sau từ khóa oai. Bước ba, viết mã xử lý nghiệp vụ bên trong thân vòng lặp. Bước tư, cập nhật giá trị của biến điều khiển ở cuối chu kỳ để tiệm cận đến mốc dừng, tránh lỗi lặp vô hạn.

## Scene_05: Giải thuật tính trung bình cộng bằng Sentinel Value
**Timeline (root):** 144.24s → 184.24s (40s)

**Visual:** Thuật toán tính điểm trung bình sử dụng giá trị lính canh trừ một để xác định thời điểm dừng nhập liệu và tính toán kết quả.

**Animation Timeline:**
- 0.2s: flowchart fade in
- 5.0s: box-1 active
- 15.0s: decision active
- 30.0s: result active

**Narration (VO):**
> Hãy cùng phân tích giải thuật tính giá trị trung bình cộng bằng kỹ thuật ghim giá trị lính canh sen-ti-nơ va-ly. Chương trình sẽ liên tục yêu cầu người dùng nhập số nguyên từ bàn phím cho đến khi người dùng nhập giá trị trừ một để báo hiệu kết thúc. Hệ thống sẽ tích lũy tổng số, đếm số lượng số đã nhập, sau đó kiểm tra điều kiện hợp lệ trước khi thực hiện phép chia để tính trung bình.

## Scene_06: Khởi tạo biến trạng thái ban đầu
**Timeline (root):** 184.24s → 219.24s (35s)

**Visual:** Thiết lập trạng thái bộ nhớ ban đầu bằng cách khai báo các biến tích lũy và định nghĩa hằng số lính canh dùng để dừng vòng lặp.

**Animation Timeline:**
- 0.2s: code-editor show
- 1.0s: line-1 write
- 8.0s: line-2 write
- 16.0s: line-3 write

**Narration (VO):**
> Bắt đầu viết mã nguồn trong môi trường phát triển. Chúng ta khởi tạo biến tích lũy tổng tô-tần săm bằng không, biến đếm số lượng in-pút kao bằng không để đếm chu kỳ, và biến hằng sen-ti-nơ va-ly bằng trừ một để làm mốc dừng vòng lặp. Việc định nghĩa rõ ràng các biến này giúp mã nguồn tường minh và dễ kiểm soát trạng thái bộ nhớ.

## Scene_07: Nhập liệu đầu vào và chuyển đổi kiểu dữ liệu
**Timeline (root):** 219.24s → 254.24s (35s)

**Visual:** Sử dụng in-pút để nhận dữ liệu động từ bàn phím và ép kiểu định dạng dữ liệu sang dạng số nguyên trước khi kiểm tra logic.

**Animation Timeline:**
- 0.2s: code-editor update
- 1.0s: line-4 write
- 10.0s: line-5 write
- 20.0s: line-6 write

**Narration (VO):**
> Trước khi bước vào vòng lặp, chúng ta sử dụng hàm in-pút để nhận dữ liệu thô đầu tiên từ người dùng và gán vào biến róa in-pút. Do hàm in-pút mặc định trả về chuỗi văn bản, chúng ta thực hiện ép kiểu sang số nguyên bằng hàm in và lưu vào biến diu-dơ va-ly. Đây là bước đệm quan trọng để cung cấp dữ liệu kiểm tra cho biểu thức điều kiện của vòng lặp oai sắp tới.

## Scene_08: Thiết lập điều kiện dừng oai
**Timeline (root):** 254.24s → 289.24s (35s)

**Visual:** Khai báo từ khóa oai kết hợp biểu thức logic so sánh biến giá trị người dùng với giá trị lính canh để điều khiển luồng lặp.

**Animation Timeline:**
- 0.2s: code-editor update
- 2.0s: line-7 write
- 15.0s: indent-block highlight

**Narration (VO):**
> Bây giờ, chúng ta khai báo cấu trúc oai với điều kiện diu-dơ va-ly khác sen-ti-nơ va-ly, tức là khác trừ một. Trình thông dịch của Pai-thơn sẽ kiểm tra giá trị của biến diu-dơ va-ly. Nếu người dùng nhập bất kỳ số nào khác trừ một, biểu thức so sánh này trả về tru và cho phép luồng thực thi đi vào trong khối lệnh lặp để xử lý tính toán.

## Scene_09: Xử lý nghiệp vụ và cập nhật biến điều khiển
**Timeline (root):** 289.24s → 329.24s (40s)

**Visual:** Cập nhật dữ liệu tích lũy và thực hiện thay đổi giá trị của biến điều kiện ở dòng cuối cùng của thân vòng lặp để tránh vòng lặp vô tận.

**Animation Timeline:**
- 0.2s: code-editor update
- 2.0s: line-8-to-9 write
- 18.0s: line-10-to-11 write
- 30.0s: line-10-to-11 highlight

**Narration (VO):**
> Bên trong thân vòng lặp, chúng ta cộng dồn giá trị diu-dơ va-ly vào biến tích lũy tô-tần săm, sau đó tăng biến đếm in-pút kao lên một đơn vị. Dòng cuối cùng của khối lệnh vô cùng quan trọng: chúng ta lặp lại thao tác yêu cầu nhập dữ liệu mới và ép kiểu gán vào diu-dơ va-ly. Dòng lệnh này có vai trò thay đổi trạng thái của biến điều kiện, đảm bảo vòng lặp sẽ tiệm cận đến điểm dừng.

## Scene_10: Kiểm tra biên an toàn và tính toán kết quả
**Timeline (root):** 329.24s → 369.24s (40s)

**Visual:** Sử dụng cấu trúc điều kiện để ngăn chặn lỗi chia cho số không trước khi tính toán giá trị trung bình cộng.

**Animation Timeline:**
- 0.2s: code-editor update
- 2.0s: block-if write
- 20.0s: block-else write
- 32.0s: safety-check highlight

**Narration (VO):**
> Sau khi thoát khỏi vòng lặp oai, ta thực hiện tính toán kết quả cuối cùng. Để đề phòng lỗi runtime nghiêm trọng di-rô đi-vi-dân e-rờ xảy ra khi người dùng nhập trừ một ngay lập tức, ta sử dụng một khối điều kiện if để kiểm tra xem in-pút kao có lớn hơn không. Nếu lớn hơn không, chương trình tính trung bình cộng bằng phép chia tô-tần săm cho in-pút kao, ngược lại sẽ hiển thị thông báo lỗi phù hợp.

## Scene_11: Thực thi kiểm thử chương trình trên Terminal
**Timeline (root):** 369.24s → 404.24s (35s)

**Visual:** Kết quả chạy thử trên Terminal hiển thị việc tính toán chính xác giá trị trung bình cộng khi người dùng nhập giá trị lính canh để kết thúc.

**Animation Timeline:**
- 0.2s: terminal open
- 4.0s: cli-input-1 show
- 10.0s: cli-input-2 show
- 16.0s: cli-input-3 show
- 22.0s: cli-input-sentinel show
- 28.0s: cli-success show

**Narration (VO):**
> Thử nghiệm chạy chương trình trên môi trường Terminal. Chúng ta nhập chuỗi giá trị mười, hai mươi, ba mươi và sau cùng nhập trừ một. Hệ thống ghi nhận chính xác ba số đầu tiên, bỏ qua giá trị lính canh trừ một, tính toán tổng bằng sáu mươi và xuất ra trung bình cộng bằng hai mươi chấm không. Vòng lặp đã thực thi và dừng lại hoàn toàn đúng thiết kế.

## Scene_12: Cảnh báo lỗi Infinite Loop và nguyên tắc lập trình an toàn
**Timeline (root):** 404.24s → 444.24s (40s)

**Visual:** Lỗi vòng lặp vô hạn gây tràn bộ nhớ do thiếu câu lệnh cập nhật trạng thái biến điều khiển sau mỗi chu kỳ xử lý.

**Animation Timeline:**
- 0.2s: alert-card fade in
- 15.0s: warning-text flash
- 28.0s: solution-text glow

**Narration (VO):**
> Một lỗi phổ biến nhất khi viết vòng lặp oai là quên cập nhật biến điều kiện bên trong khối lệnh, dẫn đến lỗi vòng lặp vô hạn in-phi-nít lúp tàn phá bộ nhớ. Hãy luôn đảm bảo cấu trúc logic của bạn có dòng lệnh làm thay đổi chân trị của biểu thức điều kiện. Bên cạnh đó, luôn đặt các cơ chế kiểm tra biên chặt chẽ để hệ thống vận hành trơn tru và an toàn tối đa.


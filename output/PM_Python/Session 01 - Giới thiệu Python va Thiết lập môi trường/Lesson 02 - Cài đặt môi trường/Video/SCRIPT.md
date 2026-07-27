# HyperFrames Script: Session 01 — Lesson 02

**Lesson:** Cài đặt môi trường
**Technology Stack:** python/core
**Total Duration:** 441.39s
**Scene Count:** 11

---

## Scene_01: Thách thức về tính nhất quán môi trường toàn cục
**Timeline (root):** 9.24s → 44.24s (35s)

**Visual:** So sánh giữa môi trường toàn cục bị xung đột phiên bản (Project A yêu cầu Package X v1.0, Project B yêu cầu Package X v2.0) dẫn đến lỗi hệ thống và giải pháp môi trường ảo cô lập.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: comparison-wrapper fade in
- 5.0s: highlight global-env error border
- 15.0s: draw red cross over global conflict link
- 22.0s: highlight virtual-envs green glow

**Narration (VO):**
> Trong phát triển phần mềm chuyên nghiệp, việc chạy đồng thời nhiều dự án có phiên bản thư viện khác nhau trên cùng một thiết bị là thử thách lớn. Nếu cài đặt trực tiếp mọi thứ lên phân vùng hệ thống toàn cục, xung đột phiên bản sẽ xuất hiện tức thì, gây ra hiện tượng địa ngục phụ thuộc hay còn gọi là dependency hell.

## Scene_02: Lỗi đồng bộ hệ điều hành và bất cập từ cấu hình thủ công
**Timeline (root):** 44.24s → 79.24s (35s)

**Visual:** Quy trình phát sinh lỗi từ việc chỉnh sửa thủ công Path dẫn tới lỗi runtime ở giai đoạn deploy trên máy chủ.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: flow-container fade in
- 8.0s: step-1 active border
- 18.0s: step-2 connect line draw
- 28.0s: step-3 alert color active

**Narration (VO):**
> Không chỉ xung đột thư viện, sự không nhất quán về cấu hình đường dẫn và biến môi trường giữa các hệ điều hành Windows, macOS, Linux còn khiến mã nguồn hoạt động không ổn định. Lỗi runtime âm thầm chỉ xuất hiện trên máy chủ hoặc máy của thành viên khác là hậu quả của việc thiếu cơ chế cô lập và tự động hóa.

## Scene_03: Quy trình tải Python và thiết lập biến môi trường PATH
**Timeline (root):** 79.24s → 119.24s (40s)

**Visual:** Tiến trình cài đặt chuẩn hóa: Tải installer từ python.org -> Đánh dấu chọn 'Add Python to PATH' -> Cho phép chạy lệnh python tại terminal.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: install-flow fade in
- 10.0s: path-check blink green selection
- 25.0s: terminal preview element shows valid execute python command

**Narration (VO):**
> Giải pháp đầu tiên là cài đặt chuẩn hóa. Khi tải bản cài đặt Python chính thức từ website python chấm o-r-g, tùy chọn 'Add Python to PATH' là bắt buộc. Điều này giúp đăng ký đường dẫn chứa tệp thực thi vào danh sách tìm kiếm của hệ điều hành, cho phép kích hoạt lệnh python trực tiếp từ bất kỳ dòng lệnh nào.

## Scene_04: Cấu hình Visual Studio Code và tiện ích mở rộng Python
**Timeline (root):** 119.24s → 149.24s (30s)

**Visual:** VS Code Interface Mockup hiển thị Extensions Marketplace và cài đặt Extension Python cung cấp bởi Microsoft.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: vscode-mockup slide in out-from-left
- 8.0s: focus search-bar typing text 'python'
- 18.0s: click install and show installed status for Python extension

**Narration (VO):**
> Tiếp theo là cấu hình Visual Studio Code. Làm việc với Python hiệu quả đòi hỏi cài đặt tiện ích mở rộng chính thức từ Microsoft. Tiện ích này đóng vai trò phân tích cú pháp, trợ giúp gợi ý cú pháp thông minh và giúp editor kết nối chuẩn xác với các môi trường ảo cục bộ.

## Scene_05: Bản chất kiến trúc của Môi trường ảo (venv)
**Timeline (root):** 149.24s → 184.24s (35s)

**Visual:** Sơ đồ kiến trúc cô lập: Phân biệt System Scope (site-packages toàn hệ thống) và Projects Local Scope (vùng chứa site-packages riêng biệt cho từng folder dự án).

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: scope-comparison show
- 12.0s: scale system scope illustration
- 22.0s: isolate local scope with dashed border frame

**Narration (VO):**
> Trước khi gõ lệnh, ta cần hiểu rõ lý do sử dụng venv. Môi trường ảo thực chất là một thư mục cô lập hoàn toàn chứa bản sao gọn nhẹ của trình thông dịch Python và một thư mục site gạch dưới packages riêng biệt. Cơ chế này đảm bảo mọi gói cài đặt qua pip sẽ chỉ nằm trong giới hạn dự án đó.

## Scene_06: Tạo lập môi trường ảo thông qua terminal
**Timeline (root):** 184.24s → 224.24s (40s)

**Visual:** Terminal CLI gõ lệnh python -m venv app_env để tạo môi trường ảo.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: terminal-win show
- 6.0s: type text 'python -m venv app_env' char by char
- 18.0s: show prompt return cursor, highlight folder tree structure with app_env directory

**Narration (VO):**
> Để khởi tạo môi trường ảo, hãy mở cửa sổ dòng lệnh tại thư mục gốc của dự án, sau đó thực thi lệnh: python trừ m venv app gạch dưới env. Ở đây, cờ trừ m chỉ định chạy module venv tích hợp sẵn trong thư viện chuẩn, và app gạch dưới env là tên thư mục chứa toàn bộ môi trường ảo.

## Scene_07: Kích hoạt môi trường ảo: Windows vs macOS/Linux
**Timeline (root):** 224.24s → 264.24s (40s)

**Visual:** Bảng so sánh câu lệnh kích hoạt môi trường ảo trên các hệ điều hành: Windows PowerShell và macOS/Linux.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: os-commands overlay show
- 10.0s: win-cmd card glow
- 22.0s: unix-cmd card glow
- 30.0s: show terminal prompt updating to (app_env) indicator

**Narration (VO):**
> Bước kế tiếp là kích hoạt môi trường. Trên Windows PowerShell, chạy script chấm xuệc app gạch dưới env xuệc Scripts xuệc Activate chấm p-s-một. Trên macOS hoặc Linux, bạn dùng lệnh source cách app gạch dưới env xuệc bin xuệc activate. Command prompt sẽ xuất hiện hậu tố tên môi trường đầu dòng lệnh.

## Scene_08: Liên kết môi trường ảo với Visual Studio Code Interpreter
**Timeline (root):** 264.24s → 299.24s (35s)

**Visual:** Thao tác trên giao diện VS Code, mở Command Palette, nhập Select Interpreter và chọn trình thông dịch thuộc môi trường ảo cục bộ.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: palette-mockup fade in
- 10.0s: highlight select interpreter input text
- 20.0s: select the local venv path option in user list

**Narration (VO):**
> Để đảm bảo VS Code thực thi mã nguồn bằng đúng môi trường vừa tạo, hãy mở Command Palette bằng tổ hợp phím Control Shift P hoặc Command Shift P trên macOS. Gõ tìm kiếm cụm từ Python hai chấm Select Interpreter, rồi tìm và chọn đường dẫn trỏ thẳng đến tệp thực thi nằm trong thư mục app gạch dưới env.

## Scene_09: Viết mã kiểm tra trạng thái môi trường venv
**Timeline (root):** 299.24s → 344.24s (45s)

**Visual:** Mã nguồn Python sử dụng module sys để kiểm tra và in ra đường dẫn của trình thông dịch cùng biến môi trường.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: code-editor structure render syntax highlight
- 15.0s: highlight sys.executable library dependency line
- 28.0s: highlight base_prefix configuration logic statement

**Narration (VO):**
> Hãy kiểm nghiệm bằng một tập lệnh Python. Ta import thư viện sys của hệ điều hành, truy xuất sys chấm executable nhằm xác định chính xác đường dẫn tệp thực thi hiện hành. Sự chênh lệch giữa thuộc tính sys chấm prefix và base gạch dưới prefix sẽ cho biết trạng thái cô lập của ứng dụng đã hoạt động hay chưa.

## Scene_10: Thực thi kết quả kiểm chứng trên Terminal
**Timeline (root):** 344.24s → 384.24s (40s)

**Visual:** So sánh hai đầu ra terminal: Một cái chạy khi đã kích hoạt venv (True) và một cái chạy ở chế độ global (False).

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: terminal-outputs render side by side
- 12.0s: highlight active-venv outputs text green highlight
- 25.0s: highlight active-global outputs text red highlight

**Narration (VO):**
> Khi chạy file kiểm tra bằng lệnh python app chấm p-y ngay trong terminal đã kích hoạt, màn hình sẽ hiển thị Virtual Env bằng True đi kèm đường dẫn thư mục dự án cục bộ. Ngược lại, nếu tắt kích hoạt môi trường và chạy lại, kết quả trả về sẽ là False và đường dẫn chỉ tới thư viện gốc của hệ thống.

## Scene_11: Các lỗi phổ biến khi cấu hình hệ thống và cách khắc phục
**Timeline (root):** 384.24s → 429.24s (45s)

**Visual:** Thẻ cảnh báo danh sách lỗi kinh điển: ModuleNotFoundError, FileNotFoundError, PermissionError và giải pháp xử lý ngắn gọn cho mỗi lỗi.

**Animation Timeline:**
- 0.0s: tl.set('.clip', {autoAlpha:1}, 0)
- 0.5s: pitfalls-box render containing cards
- 10.0s: highlight ModuleNotFoundError card with warning color
- 20.0s: highlight FileNotFoundError card with warning color
- 30.0s: highlight PermissionError card with warning color

**Narration (VO):**
> Cuối cùng, cần ghi nhớ lỗi ModuleNotFoundError phát sinh khi quên kích hoạt môi trường ảo trước khi pip install, lỗi FileNotFoundError do đường dẫn làm việc của terminal lệch so với vị trí chứa file script, và lỗi PermissionError báo hiệu terminal thiếu đặc quyền quản trị cao nhất trên hệ điều hành.


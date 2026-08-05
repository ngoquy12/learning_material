## <center>Tài liệu đặc tả Hệ thống Ứng dụng Máy tính Cá nhân CLI (CLI Arithmetic Calculator Engine)</center>

### **1. Tổng quan hệ thống**

Hệ thống **Ứng dụng Máy tính Cá nhân CLI (CLI Arithmetic Calculator Engine)** là giải pháp phần mềm chạy trên giao diện dòng lệnh (Command Line Interface - CLI), cung cấp công cụ tính toán số học cốt lõi, nhanh chóng và chính xác. Ứng dụng được thiết kế nhằm xử lý các phép toán từ cơ bản (Cộng, Trừ, Nhân, Chia) đến mở rộng (Chia lấy phần dư, Lũy thừa) thông qua luồng tương tác liên tục với người dùng.

Hệ thống vận hành dưới mô hình kiến trúc **Ứng dụng Console / Lập trình Cốt lõi (CLI Core Application)**. Toàn bộ luồng điều khiển được duy trì qua vòng lặp trạng thái (`while`), tiếp nhận và chuẩn hóa dữ liệu đầu vào dưới dạng chuỗi (String), thực hiện ép kiểu sang số thực (`float`), và định tuyến xử lý bằng cấu trúc rẽ nhánh (`if-elif-else`). Hệ thống tích hợp biến tích lũy bộ nhớ (`current_result`) cho phép thực hiện chuỗi tính toán liên hoàn mà không làm ngắt ngắt luồng làm việc.

<div class="mermaid-diagram-container" style="background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin: 20px 0; overflow-x: auto;">
  <div class="mermaid" style="display: flex; justify-content: center; color: #f8fafc;">
flowchart TD
    classDef startEnd fill:#059669,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef inputNode fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef validNode fill:#334155,stroke:#f59e0b,stroke-width:2px,color:#f8fafc;
    classDef execNode fill:#1e293b,stroke:#8b5cf6,stroke-width:2px,color:#f8fafc;
    classDef memNode fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#f8fafc;
    classDef errorNode fill:#881337,stroke:#f43f5e,stroke-width:2px,color:#f8fafc;

    Start(["Khởi chạy Ứng dụng Calculator CLI"]):::startEnd --> InitRAM["Khởi tạo Biến Đơn trong In-memory RAM Storage"]:::memNode

    InitRAM --> ShowBanner["Hiển thị Banner Chào mừng & Menu Hướng dẫn"]:::inputNode

    subgraph InputPhase ["Phân khúc 1: Nhập Dữ liệu Console (Input Layer)"]
        ShowBanner --> ReadStr1["Nhập Chuỗi Số thứ Nhất (input)"]:::inputNode
        ReadStr1 --> ReadOp["Nhập Ký tự Phép tính (input)"]:::inputNode
        ReadOp --> ReadStr2["Nhập Chuỗi Số thứ Hai (input)"]:::inputNode
    end

    subgraph ValidPhase ["Phân khúc 2: Kiểm tra Dữ liệu (Validation Layer)"]
        ReadStr2 --> CheckNum1{"Chuỗi Số 1 có thể ép kiểu float()?"}:::validNode
        CheckNum1 -- "Không" --> ErrParse1["Ghi nhận Lỗi: Số thứ Nhất Không Hợp lệ"]:::errorNode
        CheckNum1 -- "Có" --> CheckNum2{"Chuỗi Số 2 có thể ép kiểu float()?"}:::validNode
        
        CheckNum2 -- "Không" --> ErrParse2["Ghi nhận Lỗi: Số thứ Hai Không Hợp lệ"]:::errorNode
        CheckNum2 -- "Có" --> CheckOpValid{"Toán tử thuộc tập +, -, *, / ?"}:::validNode

        CheckOpValid -- "Không" --> ErrOp["Ghi nhận Lỗi: Toán tử Không Hợp lệ"]:::errorNode
        CheckOpValid -- "Có" --> CheckZeroDiv{"Phép tính là Chia và Số 2 bằng 0?"}:::validNode

        CheckZeroDiv -- "Có" --> ErrZero["Ghi nhận Lỗi: ZeroDivisionError"]:::errorNode
    end

    subgraph ExecPhase ["Phân khúc 3: Điều hướng Rẽ nhánh (if-elif-else)"]
        CheckZeroDiv -- "Không" --> BranchCalc{"Điều kiện Rẽ nhánh Cấu trúc if-elif-else"}:::execNode
        
        BranchCalc -- "op == '+'" --> DoAdd["Thực hiện Phép Cộng: result = num1 + num2"]:::execNode
        BranchCalc -- "op == '-'" --> DoSub["Thực hiện Phép Trừ: result = num1 - num2"]:::execNode
        BranchCalc -- "op == '*'" --> DoMul["Thực hiện Phép Nhân: result = num1 * num2"]:::execNode
        BranchCalc -- "op == '/'" --> DoDiv["Thực hiện Phép Chia: result = num1 / num2"]:::execNode
    end

    subgraph StateDisplayPhase ["Phân khúc 4: Cập nhật RAM State & Hiển thị (Display Layer)"]
        DoAdd --> StoreRAM["Cập nhật Giá trị Biến result vào RAM Storage"]:::memNode
        DoSub --> StoreRAM
        DoMul --> StoreRAM
        DoDiv --> StoreRAM

        StoreRAM --> FormatStr["Định dạng Chuỗi Kết quả (Console f-string)"]:::memNode
        FormatStr --> PrintSuccess["Xuất Kết quả Tính toán ra Console (print)"]:::memNode
    end

    ErrParse1 --> PrintErr["Xuất Thông báo Lỗi ra Console (print)"]:::errorNode
    ErrParse2 --> PrintErr
    ErrOp --> PrintErr
    ErrZero --> PrintErr

    subgraph LoopControlPhase ["Phân khúc 5: Điều khiển Vòng lặp Console (Loop Control)"]
        PrintSuccess --> PromptCont["Nhập Lựa chọn Tiếp tục y/n (input)"]:::inputNode
        PrintErr --> PromptCont
        
        PromptCont --> CheckCont{"Người dùng nhập ký tự 'y'?"}:::validNode
        CheckCont -- "Có (Tái khởi tạo State)" --> ShowBanner
        CheckCont -- "Không ('n')" --> ExitApp["Hiển thị Thông điệp Tạm biệt"]:::inputNode
    end

    ExitApp --> EndProgram(["Kết thúc Chương trình CLI"]):::startEnd
</div>
</div>

---

### **2. Đặc tả chức năng (Functional Requirements)**

Hệ thống cung cấp các nhóm chức năng tính toán và quản lý trạng thái bộ nhớ thông qua bảng đặc tả dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #1e293b; color: #ffffff;">
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 8%;">Mã CN</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 22%;">Tên chức năng / Khối xử lý</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 35%;">Luồng xử lý nghiệp vụ</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 17%;">Dữ liệu đầu vào</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 18%;">Kết quả đầu ra</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>FN-01</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Phép cộng & Cộng dồn</b><br><code>calculate_addition()</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Nhận 2 toán hạng hoặc lấy <code>current_result</code> cộng với toán hạng mới. Thực hiện <code>first_operand + second_operand</code>. Gán kết quả vào <code>current_result</code>.</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>first_operand</code> (float), <code>second_operand</code> (float)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Tổng hai số (float), cập nhật bộ nhớ.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>FN-02</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Phép trừ & Trừ dồn</b><br><code>calculate_subtraction()</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Nhận 2 toán hạng. Thực hiện phép toán <code>first_operand - second_operand</code>. Cập nhật kết quả vào biến lưu trữ bộ nhớ.</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>first_operand</code> (float), <code>second_operand</code> (float)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Hiệu hai số (float), cập nhật bộ nhớ.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>FN-03</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Phép nhân số học</b><br><code>calculate_multiplication()</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Thực hiện <code>first_operand * second_operand</code>. Kiểm tra giới hạn tràn số cơ bản và trả về tích số.</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>first_operand</code> (float), <code>second_operand</code> (float)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Tích hai số (float), cập nhật bộ nhớ.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>FN-04</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Phép chia số thực</b><br><code>calculate_division()</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Kiểm tra <code>second_operand != 0</code>. Nếu hợp lệ, tính <code>first_operand / second_operand</code>. Nếu bằng 0, thông báo lỗi.</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>first_operand</code> (float), <code>second_operand</code> (float)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Thương số (float) hoặc thông báo lỗi chia cho 0.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>FN-05</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Phép chia lấy dư</b><br><code>calculate_modulo()</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Kiểm tra <code>second_operand != 0</code>. Thực hiện tính dư <code>first_operand % second_operand</code>.</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>first_operand</code> (float), <code>second_operand</code> (float)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Phần dư (float) hoặc thông báo lỗi chia cho 0.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>FN-06</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Tính toán lũy thừa</b><br><code>calculate_power()</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Thực hiện <code>first_operand ** second_operand</code> (cơ số ** số mũ). Kiểm tra lỗi toán học khi cơ số bằng 0 và số mũ âm.</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>base_number</code> (float), <code>exponent_number</code> (float)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Kết quả lũy thừa (float), cập nhật bộ nhớ.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>FN-07</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Đặt lại bộ nhớ</b><br><code>reset_calculator_state()</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Gán <code>current_result = 0.0</code> và <code>has_stored_result = False</code>, xóa lịch sử tính tạm thời trong vòng lặp.</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Lệnh xác nhận từ bàn phím (str)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Thông báo bộ nhớ đã đặt lại về 0.0.</td>
    </tr>
  </tbody>
</table>

#### **Chi tiết luồng vận hành điều hướng (Control Flow & Dynamic Prompting)**
1. **Khởi tạo**: Hệ thống khởi tạo biến bộ nhớ `current_result = 0.0` và biến cờ trạng thái `has_stored_result = False`.
2. **Hiển thị Menu**: In danh sách các tùy chọn tính toán (`1` đến `7`) và tùy chọn thoát (`0`).
3. **Tiếp nhận thao tác**:
   - Nếu `has_stored_result == True`, hệ thống hỏi người dùng có muốn tiếp tục tính toán dựa trên kết quả cũ (`current_result`) hay bắt đầu phép tính mới.
   - Tiếp nhận dữ liệu số nhập từ bàn phím bằng `input()`, tiến hành xác thực chuỗi đầu vào.
4. **Định tuyến logic**: Cấu trúc rẽ nhánh `if-elif-else` thực hiện tính toán và gán lại `current_result`.

---

### **3. Đặc tả phi chức năng (Non-Functional Requirements)**

1. **Hiệu năng (Performance)**:
   - Thời gian phản hồi tính toán và in kết quả ra màn hình Console < 10 milliseconds cho mọi phép toán đơn lẻ.
   - Mức độ sử dụng bộ nhớ RAM duy trì dưới 15 MB trong suốt thời gian ứng dụng thực thi.

2. **Độ tin cậy & Khả năng phục hồi (Reliability & Robustness)**:
   - Hệ thống không được phép bị dừng đột ngột (crash) khi người dùng nhập dữ liệu sai định dạng (ví dụ: nhập chữ cái thay cho số) hoặc thực hiện phép tính vi phạm quy tắc toán học (chia cho số 0).
   - Vòng lặp Console (`while`) phải tiếp tục chạy và khôi phục trạng thái nhập liệu an toàn sau khi hiển thị thông báo lỗi.

3. **Giao diện người dùng trên Console (Usability & Text-UI)**:
   - Màn hình Console được định dạng trực quan bằng các ký tự trang trí ASCII (ví dụ: `=`, `-`, `*`).
   - Kết quả số thực được định dạng gọn gàng, hiển thị tối đa 4 chữ số thập phân (`{result:.4f}`) nếu có phần thập phân dài.

4. **Tính dễ bảo trì (Maintainability)**:
   - Mã nguồn tuân thủ tiêu chuẩn đặt tên biến tiếng Anh chuẩn `snake_case`.
   - Phân tách rõ ràng giữa luồng nhập dữ liệu, kiểm tra lỗi và luồng tính toán số học.

---

### **4. Đặc tả dữ liệu (Data Model / Schemas)**

Hệ thống lưu trữ và quản lý dữ liệu trong bộ nhớ ngắn hạn (RAM) thông qua các biến đơn giá trị (Scalar Primitive Variables) và chuỗi ký tự trong suốt thời gian thực thi:

#### **Danh sách biến trạng thái hệ thống (System State Variables)**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #1e293b; color: #ffffff;">
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 25%;">Tên biến (English Name)</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 15%;">Kiểu dữ liệu</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 20%;">Giá trị mặc định</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 40%;">Mô tả vai trò nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>current_result</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>float</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>0.0</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Lưu trữ kết quả tính toán gần nhất (Bộ nhớ tích lũy).</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>has_stored_result</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>bool</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>False</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Cờ xác định bộ nhớ hiện tại có chứa kết quả trước đó hay không.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>first_operand</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>float</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>0.0</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Toán hạng thứ nhất của phép tính hiện tại.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>second_operand</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>float</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>0.0</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Toán hạng thứ hai của phép tính hiện tại.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>menu_choice</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>str</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>""</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Lưu chuỗi nhập lựa chọn menu tính toán của người dùng.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>is_app_running</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>bool</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>True</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Điều khiển vòng lặp chính của ứng dụng Console.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>raw_input_buffer</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>str</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>""</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Vùng đệm chuỗi tạm thời nhận dữ liệu nhập thô từ <code>input()</code>.</td>
    </tr>
  </tbody>
</table>

#### **Mô hình chuyển đổi trạng thái (State Transition Logic)**

```text
[Bắt đầu] 
   │
   ▼
[Khởi tạo: current_result = 0.0, has_stored_result = False]
   │
   ▼
┌─► [Hiển thị Menu & Nhận menu_choice]
│      │
│      ├─► [menu_choice == '0'] ───────────────► [Thoát ứng dụng]
│      ├─► [menu_choice == '7'] ───────────────► [reset_calculator_state] ──► [Gán current_result = 0.0] ──┐
│      └─► [menu_choice in '1'..'6']                                                                          │
│             │                                                                                               │
│             ▼                                                                                               │
│         [Kiểm tra has_stored_result]                                                                        │
│             ├─ True  ──► Nhận second_operand (gán first_operand = current_result)                           │
│             └─ False ──► Nhận first_operand & second_operand                                                │
│             │                                                                                               │
│             ▼                                                                                               │
│         [Xác thực dữ liệu nhập & Bắt ngoại lệ try-except]                                                   │
│             ├─ Lỗi ──► In thông báo lỗi ────────────────────────────────────────────────────────────────────┤
│             └─ Hợp lệ ─► Thực hiện phép tính (if-elif) ─► Cập nhật current_result ─► In kết quả ────────────┘
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **5. Quy tắc kiểm soát lỗi và Xử lý ngoại lệ (Exception Handling & Error Rules)**

Mô hình kiểm soát lỗi trong môi trường Console tuân thủ cơ chế ngoại lệ nguyên bản của Python (`try-except`) và kiểm tra điều kiện logic tiền xử lý:

1. **Lỗi nhập sai kiểu dữ liệu (Invalid Numeric Parsing - `ValueError`)**:
   - *Nguyên nhân*: Người dùng nhập chuỗi không phải số (ví dụ: `"abc"`, `"12a3"`, chuỗi rỗng `""`).
   - *Xử lý*: Bắt ngoại lệ `ValueError` trong khối `try-except` khi ép kiểu `float(raw_input_buffer)`. Thông báo: `"[LỖI DỮ LIỆU]: Giá trị nhập vào không phải là số hợp lệ. Vui lòng thử lại!"`. Luồng ứng dụng dùng `continue` để quay lại đầu vòng lặp.

2. **Lỗi chia cho số 0 (Division by Zero - `ZeroDivisionError`)**:
   - *Nguyên nhân*: Thực hiện phép chia `/` hoặc phép chia lấy dư `%` với `second_operand == 0`.
   - *Xử lý*: Kiểm tra tiền điều kiện `if second_operand == 0:` trước khi tính toán hoặc bắt ngoại lệ `ZeroDivisionError`. Thông báo: `"[LỖI TOÁN HỌC]: Không thể thực hiện phép chia hoặc phép lấy dư cho số 0!"`. Giữ nguyên giá trị `current_result` trước đó.

3. **Lỗi toán học lũy thừa không xác định (Invalid Exponentiation)**:
   - *Nguyên nhân*: Cơ số bằng 0 với số mũ âm (ví dụ: `0 ** -2`).
   - *Xử lý*: Bắt ngoại lệ `ZeroDivisionError` phát sinh khi thực hiện lũy thừa số mũ âm của 0. Thông báo: `"[LỖI TOÁN HỌC]: Cơ số 0 không thể nâng lên lũy thừa âm!"`.

4. **Lỗi lựa chọn Menu không hợp lệ (Invalid Menu Selection)**:
   - *Nguyên nhân*: Người dùng nhập ký tự không nằm trong danh sách tùy chọn (ví dụ: `"9"`, `"x"`, `"key"`).
   - *Xử lý*: Kiểm tra bằng điều kiện `if menu_choice not in ('0', '1', '2', '3', '4', '5', '6', '7'):`. Thông báo: `"[LỖI TÙY CHỌN]: Tùy chọn không hợp lệ. Vui lòng chọn từ 0 đến 7!"`.

---

### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #1e293b; color: #ffffff;">
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 10%;">Mã TH</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 25%;">Kịch bản kiểm thử (Scenario)</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 20%;">Loại lỗi / Điều kiện phát sinh</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 45%;">Hành vi xử lý của ứng dụng & Thông báo màn hình</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>EC-01</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Nhập ký tự chuỗi chữ cái cho toán hạng (VD: <code>first_operand = "abc"</code>)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>ValueError</code> (Ép kiểu float thất bại)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Bắt ngoại lệ, in: <i>"[LỖI DỮ LIỆU]: Giá trị nhập vào không phải là số hợp lệ!"</i>. Bỏ qua phép tính và hiển thị lại Menu.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>EC-02</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Thực hiện phép chia thực cho 0 (VD: <code>10.5 / 0</code>)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>ZeroDivisionError</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Chặn trước tính toán, in: <i>"[LỖI TOÁN HỌC]: Không thể thực hiện phép chia cho số 0!"</i>. Bộ nhớ không bị thay đổi.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>EC-03</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Thực hiện phép lấy dư cho 0 (VD: <code>25 % 0</code>)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>ZeroDivisionError</code> (Modulo by Zero)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">In thông báo: <i>"[LỖI TOÁN HỌC]: Không thể thực hiện phép chia lấy dư cho 0!"</i>. Yêu cầu chọn thao tác mới.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>EC-04</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Tính lũy thừa với cơ số 0 và số mũ âm (VD: <code>0 ** -3</code>)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;"><code>ZeroDivisionError</code> trong lũy thừa</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Bắt ngoại lệ, in: <i>"[LỖI TOÁN HỌC]: Cơ số 0 không thể nâng lên lũy thừa âm!"</i>. Hủy thao tác tính.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>EC-05</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Nhập khoảng trắng hoặc bấm Enter rỗng (VD: <code>""</code> hoặc <code>"   "</code>)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Empty String Input Error</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Phát hiện chuỗi rỗng sau <code>.strip()</code>, thông báo: <i>"[LỖI DỮ LIỆU]: Dữ liệu nhập không được để rỗng!"</i>. Yêu cầu nhập lại.</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>EC-06</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Chọn tùy chọn menu nằm ngoài dải 0-7 (VD: <code>"99"</code>)</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Out of Range Option Selection</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">In thông báo: <i>"[LỖI TÙY CHỌN]: Tùy chọn '99' không tồn tại. Vui lòng chọn lại!"</i>. Tiếp tục vòng lặp Menu.</td>
    </tr>
  </tbody>
</table>

---

### **7. Quy trình chạy thử nghiệm Console (Console Execution & Test Scenarios)**

#### **Giao diện mô phỏng chạy thực tế trên Terminal**

```text
==================================================
      CHƯƠNG TRÌNH MÁY TÍNH CÁ NHÂN CLI (CORE)
==================================================
Bộ nhớ hiện tại [current_result]: 0.0000

--- DANH SÁCH CHỨC NĂNG ---
1. Phép cộng (+)
2. Phép trừ (-)
3. Phép nhân (*)
4. Phép chia thực (/)
5. Phép chia lấy phần dư (%)
6. Phép tính lũy thừa (^)
7. Đặt lại bộ nhớ (Reset)
0. Thoát chương trình
--------------------------------------------------
Vui lòng chọn chức năng (0-7): 1

---> NGUYÊN TẮC: Bắt đầu phép tính mới.
Nhập số thứ nhất (first_operand): 15.5
Nhập số thứ hai (second_operand): 4.5

[KẾT QUẢ]: 15.5000 + 4.5000 = 20.0000
=> Bộ nhớ đã được cập nhật: current_result = 20.0000

==================================================
Bộ nhớ hiện tại [current_result]: 20.0000

Vui lòng chọn chức năng (0-7): 4
Bạn có muốn dùng tiếp kết quả 20.0000 làm số bị chia? (y/n): y
Nhập số chia (second_operand): 0

[LỖI TOÁN HỌC]: Không thể thực hiện phép chia cho số 0!
=> Bộ nhớ giữ nguyên: current_result = 20.0000

==================================================
Bộ nhớ hiện tại [current_result]: 20.0000

Vui lòng chọn chức năng (0-7): 0
Cảm ơn bạn đã sử dụng ứng dụng Máy tính CLI. Tạm biệt!
==================================================
```

#### **Bảng kịch bản thử nghiệm kiểm thử (Test Scenarios Matrix)**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #1e293b; color: #ffffff;">
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 10%;">Mã KBN</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 20%;">Mục tiêu kiểm thử</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 30%;">Dữ liệu đầu vào (Input)</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 25%;">Kết quả mong đợi (Expected Output)</th>
      <th style="padding: 10px; border: 1px solid #cbd5e1; width: 15%;">Trạng thái</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>TS-01</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Kiểm tra phép cộng số thực hợp lệ</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Menu: <code>1</code><br>Op1: <code>12.5</code>, Op2: <code>7.3</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">In <code>19.8000</code><br><code>current_result = 19.8</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center; color: #16a34a;"><b>PASSED</b></td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>TS-02</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Kiểm tra phép nhân dồn từ bộ nhớ</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Menu: <code>3</code><br>Dùng bộ nhớ cũ (<code>19.8</code>)<br>Op2: <code>2</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">In <code>39.6000</code><br><code>current_result = 39.6</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center; color: #16a34a;"><b>PASSED</b></td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>TS-03</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Xử lý ngoại lệ chia cho 0</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Menu: <code>4</code><br>Op1: <code>100</code>, Op2: <code>0</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Hiển thị thông báo Lỗi chia cho 0, không dừng chương trình</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center; color: #16a34a;"><b>PASSED</b></td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>TS-04</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Xử lý ngoại lệ nhập chữ cái</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Menu: <code>2</code><br>Op1: <code>"abc"</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Hiển thị <code>[LỖI DỮ LIỆU]</code>, yêu cầu chọn lại menu</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center; color: #16a34a;"><b>PASSED</b></td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>TS-05</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Đặt lại trạng thái bộ nhớ</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Menu: <code>7</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">In thông báo đặt lại,<br><code>current_result = 0.0</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center; color: #16a34a;"><b>PASSED</b></td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center;"><b>TS-06</b></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Thoát chương trình an toàn</td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">Menu: <code>0</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1;">In lời chào tạm biệt, kết thúc vòng lặp <code>while</code></td>
      <td style="padding: 8px; border: 1px solid #cbd5e1; text-align: center; color: #16a34a;"><b>PASSED</b></td>
    </tr>
  </tbody>
</table>
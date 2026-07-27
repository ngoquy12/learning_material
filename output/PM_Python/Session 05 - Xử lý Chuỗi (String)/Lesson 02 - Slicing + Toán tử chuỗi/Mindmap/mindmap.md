```markmap
# Session 05 - Lesson 02: Slicing và Toán tử Chuỗi trong Python

## index_duong_am
- Cơ chế đánh chỉ mục chuỗi (String Indexing Resolution)
  - Chỉ mục dương (Positive Indexing): Đi từ trái sang phải, bắt đầu từ 0 đến N-1
  - Chỉ mục âm (Negative Indexing): Đi từ phải sang trái, bắt đầu từ -1 đến -N
  - ![](../images/mindmap_img_1.png)
- Mã nguồn minh họa
  - ```python
    s = "PYTHON"
    first_char = s[0]    # 'P'
    last_char = s[-1]    # 'N' (chỉ mục âm đầu tiên bên phải)
    third_char = s[-4]   # 'T' (tương đương s[2])
    ```

## slicing_co_ban
- Cú pháp cắt chuỗi `[start:stop]`
  - Start (mặc định 0): Vị trí bắt đầu (bao gồm)
  - Stop (mặc định độ dài chuỗi): Vị trí kết thúc (không bao gồm - Exclusive)
  - Tính bất biến (Immutability): Phép cắt luôn tạo ra một chuỗi mới trong vùng nhớ, giữ nguyên chuỗi gốc
- Mã nguồn minh họa
  - ```python
    raw_payload = "TXN-20241105-99482-SUCCESS"
    txn_prefix = raw_payload[0:3]     # Trích xuất "TXN"
    txn_date = raw_payload[4:12]      # Trích xuất "20241105"
    txn_status = raw_payload[-7:]     # Trích xuất từ chỉ mục -7 đến cuối: "SUCCESS"
    ```

## slicing_nang_cao_va_dao_chuoi
- Cú pháp bước nhảy nâng cao `[start:stop:step]`
  - Step (mặc định 1): Khoảng cách bước nhảy, xác định hướng trích xuất
  - `step > 0`: Cắt từ trái sang phải
  - `step < 0`: Cắt tương tác ngược từ phải sang trái
- Thủ thuật đảo chuỗi (String Reversal)
  - `[::-1]`: Đảo chuỗi toàn phần bằng cơ chế viết dưới C-level, chạy nhanh nhất trong Python
- Mã nguồn minh họa
  - ```python
    s = "PYTHON"
    odd_chars = s[::2]       # Trích xuất ký tự ở chỉ mục chẵn: "PTO"
    reversed_s = s[::-1]     # Đảo ngược toàn bộ chuỗi: "NOHTYP"
    slice_reverse = s[4:1:-1] # Cắt ngược từ chỉ mục 4 về 2: "OHT"
    ```

## phong_tranh_loi_bien
- Cơ chế xử lý lỗi ngoài vùng phủ (Bound-Safe Processing)
  - Truy cập chỉ mục đơn (`s[index]`): Gây lỗi nghiêm trọng `IndexError` nếu chỉ mục nằm ngoài khoảng phủ
  - Lát cắt chuỗi (`s[start:stop]`): Tự động thu gọn khoảng phủ (Silent Truncation) mà không gây lỗi runtime
- Mã nguồn minh họa
  - ```python
    s = "PYTHON"
    # char = s[10]       # Gây lỗi: IndexError: string index out of range
    safe_slice = s[0:50] # Không lỗi, trả về bản sao "PYTHON"
    empty_slice = s[8:15] # Không lỗi, trả về chuỗi rỗng ""
    ```

## toan_tu_chuoi_pep8
- Phép nhân bản chuỗi `*` (String Repetition)
  - Tạo chuỗi lặp lại nhanh để định dạng giao diện dòng lệnh (CLI Banners)
- Phép cộng chuỗi `+` (String Concatenation)
  - Hợp nhất hai hoặc nhiều đối tượng chuỗi
  - Cảnh báo hiệu năng: Tránh lặp cộng chuỗi liên tục vì gây cấp phát bộ nhớ lại liên tục $O(N^2)$
- Quy chuẩn PEP8
  - Sắp xếp và xuống dòng hợp lý, thụt lề chuẩn khi xử lý nối các chuỗi dài
- Mã nguồn minh họa
  - ```python
    separator = "=" * 40   # Nhân bản tạo dải phân cách dài 40 ký tự
    title = "BAO CAO" + " TAI CHINH" # Cộng chuỗi trực tiếp
    # PEP8 khuyến cáo căn lề đối với các khối chuỗi dài dòng
    long_msg = (
        "Bat dau phan tich du lieu giao dich... \n"
        "He thong dang khoi tao tien trinh."
    )
    ```

## cli_trich_xuat_dinh_danh
- Kịch bản xử lý và vẽ giao diện báo cáo dòng lệnh
  - ![](../images/mindmap_img_2.png)
- Mã nguồn minh họa hoàn chỉnh
  - ```python
    payload = "TXN-20241105-99482-SUCCESS"
    # Trích xuất và định dạng dữ liệu
    txn_prefix = payload[0:3]
    txn_date = payload[4:12]
    txn_id = payload[-13:-8]
    txn_status = payload[-7:]
    obfuscated_key = payload[::2]
    # In báo cáo sử dụng toán tử định dạng chuỗi
    print("=" * 40)
    print("BAO CAO GIAO DICH: " + txn_prefix)
    print("-" * 40)
    print("MA SKU  : " + txn_id)
    print("NGAY    : " + txn_date)
    print("TRANG THAI: " + txn_status)
    print("MA MA HOA: " + obfuscated_key)
    print("=" * 40)
    ```
```
```
```
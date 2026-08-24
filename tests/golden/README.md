# Golden Files — Hàng rào bảo vệ thiết kế học liệu

Thư mục này khoá **diện mạo** của bài đọc (`reading.html`) và bài thực hành
(`practical_lab.html`) ở trạng thái đã được duyệt. Thiết kế hai loại học liệu này
là **vùng đóng băng**: không redesign, không đổi CSS/typography/màu.

Test thực thi: [`tests/test_golden_design.py`](../test_golden_design.py).

## Cấu trúc

| Thư mục | Vai trò |
| :--- | :--- |
| `fixtures/*.json` | Payload đầu vào cố định. Mỗi file khai báo `renderer` (`reading` hoặc `lab`), `metadata`, `payload`, và `description` giải thích fixture đó bảo vệ nhánh nào. |
| `expected/*.html` | Bản HTML đã chốt. So sánh **nguyên văn từng byte**. |

## Bộ fixture phủ nhánh nào

| Fixture | Nhánh template được phủ |
| :--- | :--- |
| `reading_python_full` | engine `pyodide`, ảnh bối cảnh (`context_image_url`), visualizer rời, self-test, nhiều reference |
| `reading_javascript_visual` | engine `js_worker`, `sec1_visual_html` (nhánh `if`, không phải `elif`), không visualizer |
| `reading_sql_minimal` | engine `sql_sim`, **thiếu** ảnh/visualizer/self-test — phủ toàn bộ nhánh phủ định |
| `reading_concept_static` | engine `static` (Git/CLI) — không được chèn khối sandbox nào |
| `lab_python` | lab công nghệ Python — phải nạp runtime Pyodide |
| `lab_sql` | lab công nghệ khác — tuyệt đối không nạp runtime Pyodide |

## Khi test đỏ

Trước hết hãy giả định **code sai, không phải golden sai**. Thông báo lỗi in ra
diff dạng unified chỉ đúng dòng đã lệch. Nếu thay đổi đó ngoài ý muốn, sửa code.

Chỉ khi bạn **cố ý** đổi thiết kế mới cập nhật bản chốt:

```bash
UPDATE_GOLDEN=1 python -m pytest tests/test_golden_design.py
```

Sau đó **bắt buộc** đọc `git diff tests/golden/expected/` trước khi commit. Diff
chứa thứ bạn không định đổi chính là hồi quy mà hàng rào này sinh ra để bắt.

## Vì sao có hai lớp kiểm

`TestGoldenSnapshot` (so nguyên văn) bắt được mọi thay đổi, nhưng có điểm yếu:
ai đó chạy lệnh cập nhật ở trên để "cho CI xanh lại" là bản lệch trở thành chuẩn
mới và hàng rào tự vô hiệu hoá trong im lặng.

`TestDesignInvariants` kiểm các dấu hiệu nhận diện bắt buộc — bảng màu Rikkei
`#be111c`, font Montserrat / JetBrains Mono, đủ 5 section của bài đọc, engine
sandbox khớp công nghệ, không sót cú pháp Jinja chưa render — **trực tiếp trên
bản golden**, nên một lần regenerate cẩu thả vẫn bị chặn.

`TestFixtureCoverage` canh chính bộ fixture: nếu có nhánh template không còn
fixture nào phủ, hàng rào có lỗ và test báo ngay.

## Ghi nhận: mã chết trong lab non-Python

`format_lab_to_html` luôn phát ra khoảng 20 dòng JS trợ giúp Pyodide, kể cả cho
bài lab SQL/Java/Git. Khối này **vô hại về chức năng** — nó bị cờ
`const isPython = "false" === "true"` vô hiệu hoá và thẻ `<script>` tải runtime
Pyodide không hề được nhúng (có test khẳng định điều đó). Đây thuần tuý là mã
chết. Dọn nó sẽ làm đổi HTML thành phẩm, tức chạm vùng đóng băng, nên cố ý để
nguyên và ghi nhận tại đây thay vì tự ý sửa.

# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Giả sử bạn là Lập trình viên Python Senior tại một công ty công nghệ, đang tư vấn cho đội ngũ kĩ thuật nâng cấp hệ thống xử lý dữ liệu từ Python 3.9 lên Python 3.12. Hãy phân tích 3 lý do kỹ thuật cốt lõi (liên quan đến hiệu năng thực thi, thông báo lỗi hệ thống và cú pháp F-string mới theo PEP 701) để thuyết phục Ban Giám đốc phê duyệt dự án nâng cấp này.
> **Gợi ý trả lời & Định hướng đáp án:** Định hướng trả lời:
1. Hiệu năng thực thi: Python 3.12 tiếp tục tối ưu hóa theo dự án Faster CPython (Specializing Adaptive Interpreter), giúp tăng tốc tổng thể từ 5% đến 15% so với Python 3.11 và vượt trội đáng kể so với Python 3.9 mà không cần sửa đổi mã nguồn logic nghiệp vụ.
2. Thông báo lỗi cải tiến (Enhanced Error Messages): Hệ thống Traceback chỉ ra vị trí dòng lỗi chính xác hơn, hỗ trợ tự động gợi ý tên biến, thuộc tính gõ sai (Did you mean...?) hoặc các module quên import. Điều này giúp giảm thiểu thời gian gỡ lỗi (debug) và chi phí bảo trì phần mềm.
3. Cú pháp F-string mới (PEP 701): Loại bỏ các hạn chế cố hữu ở các phiên bản cũ. Python 3.12 cho phép lồng ghép dấu ngoặc trùng loại bên trong F-string, sử dụng ký tự thoát (backslash '\'), biểu thức nhiều dòng và chú thích (comments), giúp mã nguồn sạch hơn, dễ đọc và dễ bảo trì khi xử lý các chuỗi JSON hoặc HTML phức tạp.

---

### Câu 2: Xét đoạn mã nguồn Python dưới đây đang cố gắng định dạng chuỗi và xử lý dữ liệu:

```python
user_info = {"name": "Alice", "role": "Admin"}
# Đoạn mã 1
print(f"User details: {user_info['name'] if user_info['role'] == 'Admin' else 'Guest'}")

# Đoạn mã 2
print(f"List of roles: {', '.join(['Admin', 'User'])}")
```

Hãy phân tích tại sao đoạn mã trên gặp lỗi SyntaxError trên các phiên bản Python trước 3.12 (như Python 3.11 trở về trước) nhưng lại hoạt động hoàn hảo trên Python 3.12. Hãy giải thích cơ chế thay đổi trong trình phân tích cú pháp (Parser) của Python 3.12 đối với PEP 701.
> **Gợi ý trả lời & Định hướng đáp án:** Định hướng trả lời:
1. Nguyên nhân lỗi trên các phiên bản cũ (trước 3.12):
- Đoạn mã 1: Dùng cùng loại dấu ngoặc đơn `'` bên trong biểu thức `{}` và ngoặc đơn bên ngoài f-string. Trước 3.12, điều này làm trình phân tích cú pháp hiểu nhầm chuỗi f-string đã kết thúc sớm, gây ra lỗi SyntaxError.
- Đoạn mã 2: Chứa dấu gạch chéo ngược `\` (trong `', '.join()`) bên trong biểu thức f-string. Các phiên bản cũ cấm sử dụng ký tự `\` trực tiếp bên trong biểu thức `{}`.
2. Cơ chế thay đổi trong trình phân tích cú pháp của Python 3.12 (PEP 701):
- Trước Python 3.12, f-string được xử lý bằng một bộ phân tích cú pháp riêng (custom lexer/parser) độc lập với trình phân tích cú pháp chính của Python.
- Từ Python 3.12, việc phân tích f-string được tích hợp trực tiếp vào trình phân tích cú pháp PEG (PEG Parser) chính của ngôn ngữ. Do đó, các token bên trong biểu thức `{}` được phân tích giống hệt như một đoạn mã Python thông thường, cho phép tái sử dụng dấu ngoặc, chứa ký tự thoát `\`, viết biểu thức nhiều dòng và thêm chú thích mà không bị giới hạn.

---

### Câu 3: Trong Python 3.12, PEP 695 giới thiệu cú pháp hoàn toàn mới cho Generic Types và Type Aliases thông qua từ khóa `type`. Giả sử bạn có đoạn mã nguồn khai báo biệt danh kiểu (Type Alias) theo phong cách cũ sử dụng module `typing` như sau:

```python
from typing import TypeVar, Dict

T = TypeVar('T')
Point = Dict[str, T]
```

Hãy viết lại đoạn mã trên theo cú pháp chuẩn mới của Python 3.12 (PEP 695). Đồng thời, hãy phân tích ưu điểm về tính rõ ràng của cú pháp và hiệu năng khởi tạo (Lazy Evaluation) của cách viết mới so with cách viết cũ.
> **Gợi ý trả lời & Định hướng đáp án:** Định hướng trả lời:
1. Mã nguồn viết lại theo chuẩn Python 3.12:
```python
type Point[T] = dict[str, T]
```
2. Phân tích ưu điểm kỹ thuật:
- Cú pháp gọn gàng và tường minh: Sử dụng trực tiếp từ khóa `type` thay vì gán biến thông thường. Không cần phải import `TypeVar` hay khai báo biến kiểu `T = TypeVar('T')` thủ công, giúp giảm mã thừa (boilerplate code).
- Quản lý phạm vi tên (Scope Management): Tham số kiểu `T` chỉ tồn tại trong phạm vi cục bộ của khai báo `type Point[T]`, tránh hiện tượng rò rỉ biến kiểu ra phạm vi toàn cục (global scope).
- Cơ chế đánh giá lười (Lazy Evaluation): Biệt danh kiểu tạo bởi từ khóa `type` thuộc lớp `TypeAliasType`. Giá trị của kiểu dữ liệu chỉ được tính toán/đánh giá khi thực sự được truy cập (evaluate on demand), giúp tăng hiệu năng khi khởi chạy ứng dụng (startup time) và hỗ trợ khai báo kiểu đệ quy (recursive types) tự nhiên mà không cần dùng chuỗi ký tự.

---

### Câu 4: Phân tích cơ chế "Enhanced Error Messages" (Thông báo lỗi cải tiến) của Python 3.12. Cho một tình huống lập trình viên thực hiện gọi một hàm từ thư viện chưa import hoặc gõ sai tên biến, Python 3.12 sẽ xử lý và đưa ra gợi ý như thế nào?

Hãy đưa ra một ví dụ minh họa về lỗi `NameError` hoặc `AttributeError` và giải thích cách thuật toán của Python 3.12 hỗ trợ lập trình viên rút ngắn thời gian phát hiện lỗi.
> **Gợi ý trả lời & Định hướng đáp án:** Định hướng trả lời:
1. Cơ chế vận hành:
- Khi xảy ra các ngoại lệ như `NameError`, `AttributeError`, hay `ModuleNotFoundError`, Python 3.12 sẽ kích hoạt cơ chế phân tích ngữ cảnh dựa trên Cây cú pháp trừu tượng (AST) và bảng ký hiệu (Symbol Table).
- Python sử dụng thuật toán tính khoảng cách Levenshtein (Levenshtein distance algorithm) để so sánh chuỗi ký tự bị lỗi với tập hợp các biến, thuộc tính hoặc module khả thi trong phạm vi (scope) hiện tại. Nếu mức độ tương đồng cao, Python sẽ tự động đề xuất dòng chữ "Did you mean: '...'?" ở cuối thông báo lỗi Traceback.
2. Ví dụ minh họa:
- Giả sử gõ sai tên thuộc tính của module:
```python
import math
print(math.sqr(16))
```
- Kết quả trên Python 3.12:
`AttributeError: module 'math' has no attribute 'sqr'. Did you mean: 'sqrt'?`
3. Ý nghĩa thực tế: Giúp lập trình viên ngay lập tức nhận diện được lỗi đánh máy (typo) thay vì phải tra cứu tài liệu hoặc mất thời gian dò lại toàn bộ tệp mã nguồn, từ đó cải thiện đáng kể trải nghiệm lập trình (Developer Experience).

---
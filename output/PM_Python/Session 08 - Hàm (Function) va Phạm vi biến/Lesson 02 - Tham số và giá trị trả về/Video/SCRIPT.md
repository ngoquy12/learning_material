# Kịch Bản Video — Session 08 Lesson 02
## Tham số và giá trị trả về

> **Tech stack:** Python/Core | **Lesson slug:** `session_08_lesson_02`

---

## Scene_01 — Tổng quan bài học

### Giọng đọc (TTS):
> Hãy cùng bắt đầu bài học thứ hai trong Session 8. Nếu ở bài trước chúng ta đã biết cách khai báo một hàm, thì hôm nay chúng ta sẽ đi sâu hơn vào hai phần mà bất kỳ hàm nào cũng cần: tham số — cách chúng ta đưa dữ liệu vào hàm — và giá trị trả về — cách hàm gửi kết quả trở lại nơi đã gọi nó. Đây là hai cơ chế làm cho hàm thực sự trở nên linh hoạt và có ích trong dự án thực tế. Hãy cùng khám phá từng phần một.

### Nội dung UI (màn hình):
```
Tham số (Parameters) — đưa dữ liệu vào hàm
Giá trị trả về (Return) — hàm gửi kết quả ra ngoài
Ứng dụng thực tế trong dự án
```

---

## Scene_02 — Positional Arguments

### Giọng đọc (TTS):
> Hãy cùng tìm hiểu loại tham số đầu tiên và cơ bản nhất — đó là Positional Argument, hay còn gọi là tham số vị trí. Đây là một trong những khái niệm vô cùng quan trọng mà mọi lập trình viên Python cần nắm vững. Nguyên lý hoạt động rất trực quan: Python ghép từng giá trị bạn truyền vào với từng tham số theo đúng thứ tự từ trái sang phải. Xem ví dụ bên phải — hàm greet nhận name rồi mới đến age. Khi gọi greet('An', 25), Python tự động hiểu 'An' là name và 25 là age. Điều quan trọng cần nhớ: sai thứ tự sẽ dẫn đến sai logic mà Python không báo lỗi.

### Nội dung UI (màn hình):
```
Ghép giá trị theo thứ tự từ trái sang phải
Số lượng argument phải khớp chính xác
Sai thứ tự → sai logic, không có lỗi cú pháp
```

---

## Scene_03 — Keyword Arguments

### Giọng đọc (TTS):
> Bây giờ hãy cùng khám phá một cải tiến rất thú vị so với tham số vị trí — đó là Keyword Argument, hay tham số định danh. Thay vì phải nhớ thứ tự, bạn chỉ cần ghi rõ tên tham số kèm dấu bằng khi gọi hàm. Python sẽ tự biết giá trị nào đi với tham số nào, dù bạn viết theo thứ tự nào. Lợi ích rõ ràng nhất là code trở nên tự giải thích — nhìn vào lời gọi hàm là biết ngay từng giá trị có ý nghĩa gì. Trong dự án thực tế, khi hàm có từ ba tham số trở lên, dùng keyword argument là lựa chọn được khuyến nghị.

### Nội dung UI (màn hình):
```
Ghi rõ tên tham số khi gọi: name='An'
Thứ tự hoàn toàn tự do
Code tự giải thích, dễ đọc hơn
```

---

## Scene_04 — Default Arguments

### Giọng đọc (TTS):
> Hãy tưởng tượng bạn đang xây dựng hàm tính thuế cho một hệ thống kế toán. Hầu hết giao dịch đều dùng thuế suất mặc định mười phần trăm, chỉ một số ít trường hợp cần thuế suất khác. Đây chính là lúc Default Argument — tham số mặc định — phát huy giá trị. Bạn gán sẵn giá trị ngay khi định nghĩa hàm; nếu người gọi không truyền vào, Python dùng giá trị đó. Tuy nhiên có một quy tắc sắt: tham số mặc định phải đứng SAU tất cả tham số bắt buộc. Vi phạm quy tắc này, Python sẽ báo SyntaxError ngay lập tức.

### Nội dung UI (màn hình):
```
Gán sẵn giá trị khi định nghĩa hàm
Không bắt buộc truyền khi gọi
Phải đứng SAU tham số bắt buộc — vi phạm gây SyntaxError
```

---

## Scene_05 — *args — Tham số vị trí động

### Giọng đọc (TTS):
> Hãy đặt ra một câu hỏi thú vị: điều gì xảy ra nếu bạn muốn viết một hàm nhưng không biết trước người dùng sẽ truyền vào bao nhiêu giá trị? Đây chính là bài toán mà star args giải quyết một cách thanh lịch. Viết dấu sao trước tên tham số, Python sẽ tự động gom tất cả giá trị positional thành một tuple để bạn dễ dàng duyệt qua. Nhìn vào hàm sum_all bên phải — dù bạn truyền ba hay một trăm số, hàm vẫn hoạt động hoàn hảo. Pattern này cực kỳ phổ biến trong các utility function, logging, và decorator.

### Nội dung UI (màn hình):
```
Dấu * gom tất cả positional arguments thành tuple
Số lượng argument hoàn toàn linh hoạt
Phổ biến trong utility, logging, decorator
```

---

## Scene_06 — **kwargs — Tham số từ khóa động

### Giọng đọc (TTS):
> Tiếp nối từ star args, hãy cùng khám phá người anh em song sinh của nó — double star kwargs. Nếu star args gom positional arguments thành tuple, thì double star kwargs gom tất cả keyword arguments thành một dictionary. Điều này cực kỳ mạnh mẽ khi bạn cần xây dựng hàm nhận cấu hình động. Bạn sẽ gặp pattern này ở khắp nơi trong các framework lớn — Django, Flask, FastAPI đều dùng kwargs để xây dựng API nhận payload JSON linh hoạt. Nắm vững kwargs sẽ giúp bạn đọc hiểu và viết được framework-level code.

### Nội dung UI (màn hình):
```
Dấu ** gom tất cả keyword arguments thành dict
Linh hoạt với cấu hình động
Nền tảng của Django, Flask, FastAPI
```

---

## Scene_07 — Thứ tự kết hợp tham số

### Giọng đọc (TTS):
> Đến đây bạn đã biết bốn loại tham số. Câu hỏi tự nhiên xuất hiện là: khi cần dùng nhiều loại trong cùng một hàm, thì thứ tự chúng phải viết như thế nào? Python có quy định rất rõ ràng và bắt buộc bạn phải tuân theo. Đầu tiên là tham số bắt buộc, tiếp đến là tham số mặc định, rồi star args gom positional động, sau đó là keyword-only, và cuối cùng là double star kwargs. Đây không phải quy ước — vi phạm thứ tự này Python sẽ báo SyntaxError ngay khi đọc file. Hãy nhớ kỹ thứ tự này, nó sẽ theo bạn suốt sự nghiệp lập trình Python.

### Nội dung UI (màn hình):
```
1. Tham số bắt buộc
2. Tham số mặc định
3. *args
4. Keyword-only
5. **kwargs
```

---

## Scene_08 — Câu lệnh return

### Giọng đọc (TTS):
> Hãy cùng chuyển sang phần thứ hai của bài học — giá trị trả về. Cho đến giờ các hàm của chúng ta mới chỉ in ra màn hình. Nhưng trong thực tế, bạn thường muốn hàm tính toán một kết quả để dùng tiếp trong logic chương trình. Đây là lúc câu lệnh return xuất hiện. Return kết thúc hàm ngay lập tức và gửi giá trị trở về nơi gọi. Một hàm có thể có nhiều return ở nhiều nhánh điều kiện — Python dừng tại return đầu tiên được thực thi. Nếu không viết return, hàm tự động trả về None.

### Nội dung UI (màn hình):
```
return kết thúc hàm và trả giá trị về
Nhiều return ở các nhánh điều kiện khác nhau
Không có return → tự động trả về None
```

---

## Scene_09 — Trả về nhiều giá trị

### Giọng đọc (TTS):
> Một trong những tính năng đặc biệt của Python mà nhiều ngôn ngữ khác không có đó là khả năng trả về nhiều giá trị từ một hàm duy nhất. Bí quyết ở đây là Python tự động đóng gói chúng vào một tuple. Và với tuple unpacking, bạn có thể nhận từng giá trị vào biến riêng biệt chỉ với một dòng code. Xem hai ví dụ bên phải — hàm divide trả về cả thương và phần dư cùng lúc, hàm min_max trả về cả giá trị nhỏ nhất và lớn nhất. Pattern này giúp code súc tích và biểu đạt ý tưởng tự nhiên hơn nhiều.

### Nội dung UI (màn hình):
```
Python tự đóng gói nhiều giá trị thành tuple
Tuple unpacking nhận từng biến một dòng
Pattern súc tích, tự nhiên
```

---

## Scene_10 — Tổng kết & Best Practices

### Giọng đọc (TTS):
> Chúng ta đã đi qua toàn bộ hệ thống tham số và giá trị trả về của Python. Hãy cùng chốt lại những điểm quan trọng nhất. Bốn loại tham số: positional theo thứ tự, keyword theo tên, default có giá trị sẵn, và variadic args kwargs cho số lượng linh hoạt. Return kết thúc hàm và trả giá trị — không có return thì trả None. Python cho phép trả về nhiều giá trị qua tuple unpacking. Và best practice quan trọng nhất: hãy dùng type hint để code tự tài liệu hóa và IDE hỗ trợ tốt hơn nhiều. Đây là nền tảng vững chắc để bạn viết hàm chuyên nghiệp.

### Nội dung UI (màn hình):
```
4 loại tham số: positional, keyword, default, variadic
return trả giá trị — không có return → None
Type hint: def fn(x: int) -> str
```

---

# Tài liệu giáo trình — Chương: Vòng lặp trong JavaScript

_(Trích từ tập bài giảng nội bộ "Lập trình JavaScript cơ bản" — chưa qua
biên tập thành slide, dùng làm nội dung thô đầu vào)_

---

## Mở đầu chương

Khi lập trình, có rất nhiều tình huống chúng ta cần thực hiện một hành động
lặp đi lặp lại nhiều lần. Ví dụ đơn giản nhất: nếu muốn in ra dòng chữ
"Xin chào" 100 lần ra console, cách viết tay từng dòng `console.log("Xin
chào")` một trăm lần rõ ràng là không thực tế — vừa tốn thời gian, vừa khó
sửa nếu sau này cần đổi số lần in từ 100 sang 1000. Đây chính là lý do các
ngôn ngữ lập trình, trong đó có JavaScript, cung cấp cấu trúc gọi là **vòng
lặp (loop)**.

Vòng lặp cho phép một khối lệnh được thực thi lặp lại nhiều lần mà không
cần viết lại nhiều lần trong mã nguồn. Ví dụ với vòng lặp, đoạn code in
"Xin chào" 100 lần chỉ cần viết:

```js
for (let i = 0; i < 100; i++) {
  console.log("Xin chào");
}
```

Mọi vòng lặp, dù là loại nào, về bản chất đều xoay quanh 4 thành phần:

1. **Khởi tạo (initialization):** thiết lập giá trị ban đầu cho biến điều
   khiển vòng lặp, thường chỉ chạy đúng một lần khi vòng lặp bắt đầu.
2. **Điều kiện (condition):** một biểu thức logic được kiểm tra trước (hoặc
   sau, tùy loại vòng lặp) mỗi lần lặp — nếu đúng thì tiếp tục, nếu sai thì
   dừng lại.
3. **Thân vòng lặp (loop body):** khối lệnh sẽ được thực thi lặp lại.
4. **Cập nhật (update):** biểu thức thay đổi giá trị của biến điều khiển
   sau mỗi lần lặp, thường dùng để tiến dần tới điều kiện dừng.

Nếu quên mất bước cập nhật, hoặc cập nhật sai cách khiến điều kiện không
bao giờ trở thành sai, chương trình sẽ rơi vào tình trạng **vòng lặp vô hạn
(infinite loop)** — chạy mãi không dừng, khiến trình duyệt bị treo. Đây là
một trong những lỗi phổ biến nhất mà người mới học lập trình hay gặp phải.

JavaScript cung cấp 5 loại vòng lặp chính: `for`, `while`, `do-while`,
`for...in`, và `for...of`. Mỗi loại phù hợp với một tình huống sử dụng
khác nhau.

---

## 1. Vòng lặp `for`

Vòng lặp `for` là loại vòng lặp được sử dụng phổ biến nhất trong JavaScript,
đặc biệt khi lập trình viên **đã biết trước số lần cần lặp**. Cú pháp tổng
quát:

```js
for (khởi_tạo; điều_kiện; cập_nhật) {
  // khối lệnh
}
```

Cả 3 thành phần (khởi tạo, điều kiện, cập nhật) được gộp chung trên một
dòng, giúp code gọn gàng và dễ theo dõi luồng chạy hơn so với các loại vòng
lặp khác.

Thứ tự thực thi của `for` như sau: đầu tiên phần khởi tạo chạy đúng một
lần. Sau đó, điều kiện được kiểm tra — nếu đúng, thân vòng lặp được thực
thi, rồi tới phần cập nhật, rồi quay lại kiểm tra điều kiện; nếu điều kiện
sai ngay từ đầu hoặc sau một vòng lặp nào đó, vòng lặp dừng lại ngay.

Ví dụ in ra các số từ 1 đến 5:

```js
for (let i = 1; i <= 5; i++) {
  console.log(i);
}
// Kết quả: 1 2 3 4 5
```

Ở đây, biến `i` bắt đầu bằng 1, mỗi lần lặp được in ra rồi tăng thêm 1, cho
tới khi `i` vượt quá 5 thì dừng.

Một ứng dụng cực kỳ phổ biến của vòng lặp `for` là **duyệt qua các phần tử
của mảng**, kết hợp với thuộc tính `.length`:

```js
const subjects = ["Toán", "Lý", "Hóa"];
for (let i = 0; i < subjects.length; i++) {
  console.log(subjects[i]);
}
// Output: Toán  Lý  Hóa
```

Lưu ý quan trọng: chỉ số mảng trong JavaScript luôn bắt đầu từ 0, không
phải từ 1. Vì vậy điều kiện đúng phải là `i < subjects.length` (không phải
`i <= subjects.length`) — nếu dùng `<=`, vòng lặp sẽ cố truy cập một phần tử
không tồn tại ở cuối mảng, và JavaScript sẽ trả về giá trị `undefined` thay
vì báo lỗi rõ ràng, khiến lỗi này rất dễ bị bỏ sót khi debug. Đây gọi là
lỗi "off-by-one" (lệch một đơn vị) — một trong những lỗi kinh điển nhất khi
làm việc với vòng lặp và chỉ số mảng.

Vòng lặp `for` cũng có thể được **lồng vào nhau** để xử lý cấu trúc dữ liệu
nhiều chiều, ví dụ in ra bảng cửu chương hoặc duyệt một ma trận hai chiều:

```js
for (let i = 1; i <= 3; i++) {
  for (let j = 1; j <= 3; j++) {
    console.log(`${i} x ${j} = ${i * j}`);
  }
}
```

Với mỗi lần lặp của vòng ngoài, toàn bộ vòng trong sẽ chạy đủ số lần của
nó. Nếu vòng ngoài chạy n lần và vòng trong cũng chạy n lần, tổng số lần
thực thi sẽ là n², nên cần cẩn trọng khi lồng nhiều vòng lặp với dữ liệu
lớn vì độ phức tạp tính toán tăng rất nhanh.

---

## 2. Vòng lặp `while`

Khác với `for`, vòng lặp `while` phù hợp hơn khi lập trình viên **chưa biết
trước chính xác số lần cần lặp**, mà số lần lặp phụ thuộc vào một điều kiện
sẽ thay đổi trong quá trình chạy chương trình.

Cú pháp:

```js
while (điều_kiện) {
  // khối lệnh
}
```

Cũng giống `for`, điều kiện được kiểm tra **trước** khi thực thi thân vòng
lặp. Nếu điều kiện sai ngay từ đầu, thân vòng lặp sẽ không chạy dù chỉ một
lần.

Khác biệt lớn nhất so với `for` là: `while` không có phần khởi tạo và cập
nhật gộp sẵn trong cú pháp — lập trình viên phải tự khởi tạo biến điều
khiển trước vòng lặp, và tự cập nhật nó bên trong thân vòng lặp. Nếu quên
bước cập nhật, chương trình chắc chắn rơi vào vòng lặp vô hạn.

Ví dụ cùng bài toán in số 1 đến 5, viết bằng `while`:

```js
let i = 1;
while (i <= 5) {
  console.log(i);
  i++;
}
// Kết quả: 1 2 3 4 5
```

`while` đặc biệt hữu ích khi số lần lặp phụ thuộc vào một điều kiện động,
ví dụ xử lý một hàng đợi công việc cho tới khi hàng đợi rỗng:

```js
const tasks = ["Upload File", "Send Email"];
while (tasks.length > 0) {
  const current = tasks.shift();
  console.log(`Task done: ${current}`);
}
```

Ở đây ta không biết trước hàng đợi có bao nhiêu phần tử tại thời điểm chạy
— vòng lặp cứ tiếp tục cho tới khi mảng `tasks` rỗng.

---

## 3. Vòng lặp `do-while`

`do-while` là một biến thể của `while`, nhưng với một khác biệt cốt lõi:
**thân vòng lặp được thực thi trước, sau đó điều kiện mới được kiểm tra.**
Điều này đảm bảo thân vòng lặp **luôn chạy ít nhất một lần**, kể cả khi
điều kiện sai ngay từ đầu.

Cú pháp:

```js
do {
  // khối lệnh
} while (điều_kiện);
```

Lưu ý cú pháp có dấu chấm phẩy `;` bắt buộc ở cuối, sau `while (...)` — đây
là điểm khác biệt dễ gây lỗi cú pháp nếu quên.

Ví dụ minh họa rõ sự khác biệt với `while`:

```js
let x = 10;
do {
  console.log("Chạy ít nhất 1 lần");
  x++;
} while (x < 5);
// Kết quả: chỉ in ra đúng 1 dòng, dù điều kiện x < 5 sai ngay từ đầu (x = 10)
```

Nếu đoạn code trên viết bằng `while` thông thường, thân vòng lặp sẽ không
chạy lần nào cả, vì điều kiện `x < 5` sai ngay từ lần kiểm tra đầu tiên
(lúc đó `x = 10`).

`do-while` thường được dùng trong các tình huống như: hiển thị menu chức
năng cho người dùng ít nhất một lần rồi mới hỏi có muốn tiếp tục hay không,
hoặc yêu cầu người dùng nhập dữ liệu và lặp lại việc yêu cầu nhập cho tới
khi dữ liệu hợp lệ.

---

## 4. Kiểm soát luồng lặp: `break` và `continue`

Đôi khi cần thoát khỏi vòng lặp sớm hơn dự kiến, hoặc bỏ qua một lần lặp cụ
thể mà không dừng hẳn toàn bộ vòng lặp. JavaScript cung cấp hai từ khóa cho
việc này:

- **`break`**: thoát ngay lập tức khỏi vòng lặp, bỏ qua toàn bộ các lần
  lặp còn lại.
- **`continue`**: bỏ qua phần còn lại của lần lặp hiện tại, nhảy thẳng tới
  lần lặp kế tiếp (vẫn tiếp tục vòng lặp, không thoát hẳn).

Ví dụ minh họa cả hai trong cùng một vòng lặp:

```js
for (let i = 1; i <= 10; i++) {
  if (i === 5) break;
  if (i % 2 === 0) continue;
  console.log(i);
}
// Kết quả: 1 3
```

Giải thích: vòng lặp chạy từ 1 tới 10. Khi `i === 5`, `break` được gọi nên
vòng lặp dừng hẳn tại đó — các số từ 5 trở đi không được xét tới. Trước đó,
với các số chẵn (2, 4), `continue` khiến chương trình bỏ qua dòng
`console.log`, nên chỉ số lẻ 1 và 3 được in ra.

---

## 5. Những lỗi và lưu ý thường gặp

**Vòng lặp vô hạn.** Đây là lỗi nghiêm trọng nhất liên quan tới vòng lặp,
có 3 nguyên nhân phổ biến:

- Quên bước cập nhật biến điều khiển (đặc biệt hay gặp với `while`).
- Cập nhật sai chiều — ví dụ điều kiện là `i < n` nhưng lại viết `i--`
  thay vì `i++`, khiến `i` không bao giờ đạt tới `n`.
- Điều kiện dừng không bao giờ trở thành sai, ví dụ viết `while (true)` mà
  quên đặt `break` ở đâu đó bên trong.

Cách phòng tránh: luôn rà lại đầy đủ cả 3 phần (khởi tạo, điều kiện, cập
nhật) trước khi chạy thử; nên thử với số vòng lặp nhỏ trước (ví dụ giới
hạn 5 thay vì 10.000) để kiểm tra logic đúng chưa, rồi mới mở rộng quy mô.

**Độ phức tạp khi lồng vòng lặp.** Như đã đề cập ở phần vòng lặp `for`,
lồng nhiều vòng lặp làm số phép tính tăng theo cấp số nhân. Với n = 10, một
vòng lặp đơn cần 10 phép tính, nhưng lồng 2 tầng cần 100 phép tính; với
n = 1.000, con số này nhảy lên 1.000.000. Với dữ liệu lớn, cần cân nhắc kỹ
trước khi lồng sâu, hoặc tìm thuật toán/cấu trúc dữ liệu khác hiệu quả hơn.

---

## Ghi chú thêm (chưa được biên tập, để tham khảo)

- Phần `break`/`continue` nên có thêm ví dụ với vòng lặp lồng nhau (label)
  nếu muốn nâng cao — hiện chưa đề cập tới `labeled break/continue`.
- Chưa có phần liên hệ giữa vòng lặp và đệ quy (recursion) — có thể là chủ
  đề mở rộng cho buổi học sau, không thuộc phạm vi chương này.
- Tài liệu tham khảo gốc dùng khi biên soạn chương này: MDN Web Docs mục
  "Loops and iteration", và javascript.info mục "Loops: while and for".

# SKILL 3: Thiết Kế Slide Từ Template (Design & Kỹ Thuật)

> **File này chỉ quyết định HÌNH THỨC** — không quyết định nội dung/cấu trúc
> bài giảng (xem **Skill 2 — "Kiến Trúc Nội Dung Bài Giảng Đa Lĩnh Vực"**,
> thư mục `skill-2-kien-truc-noi-dung-bai-giang/SKILL.md`, dùng chung với
> file này). Skill này chạy **CUỐI CÙNG** trong pipeline 3 skill.
>
> **Khác biệt cốt lõi so với bản chỉ dùng được 1 template:** Skill này KHÔNG
> áp cứng bất kỳ mã màu/font/kích thước nào của một thương hiệu cụ thể. Mọi
> con số hình thức đều được **trích xuất từ chính file template đầu vào** ở
> Giai đoạn 1, sau đó các quy tắc phổ quát ở Giai đoạn 2 mới áp dụng lên trên
> bộ số đó. Nhờ vậy, cùng 1 skill này dùng được cho template của bất kỳ
> trường/tổ chức nào mà vẫn tuân thủ 100% bản sắc của template đó.
>
> **Input:** 1 file `.pptx`/`.potx` template bất kỳ + 1 file nội dung đã có
> cấu trúc theo khuôn của Skill 2 ("Kiến Trúc Nội Dung Bài Giảng Đa Lĩnh
> Vực", thư mục `skill-2-kien-truc-noi-dung-bai-giang/SKILL.md`).
> **Output:** file `.pptx` hoàn chỉnh, đã qua validator.

---

## 0. VAI TRÒ

Bạn là chuyên gia dựng slide PowerPoint bằng thao tác XML trực tiếp (OOXML).
Nhiệm vụ gồm 2 pha bắt buộc theo đúng thứ tự: **(A) phân tích template đầu
vào để rút ra bộ Design Tokens riêng của nó**, rồi **(B) dựng nội dung theo
đúng Design Tokens đó + quy tắc phổ quát**. Không được bỏ qua pha (A) và
nhảy thẳng vào dựng nội dung bằng "gu thẩm mỹ mặc định" của bạn.

---

## GIAI ĐOẠN 1 — TRÍCH XUẤT DESIGN TOKENS TỪ TEMPLATE

Đây là bước **bắt buộc làm đầu tiên**, trước khi viết bất kỳ dòng nội dung
nào. Giải nén `.pptx` template, đọc các file sau và điền vào **Bảng Design
Tokens** (mẫu ở Phụ lục, mục 8):

### 1.1 Màu sắc

- Mở `ppt/theme/theme1.xml` → lấy `<a:clrScheme>`: `dk1`/`lt1` (đen/trắng
  cơ bản), `accent1`...`accent6` (các màu nhấn theo thứ tự ưu tiên).
- Quét thêm các `<a:srgbClr>` xuất hiện lặp lại nhiều lần trên các slide mẫu
  có sẵn (tiêu đề, khối trang trí, footer) — đây thường là **màu thương
  hiệu thật sự dùng trong thiết kế**, có thể khác với accent1 lý thuyết.
- Chốt lại: **1 màu chủ đạo (brand color)** — màu xuất hiện ở tiêu đề/logo/
  trang trí nhiều nhất.

### 1.2 Font chữ

- `<a:majorFont>` (dùng cho tiêu đề) và `<a:minorFont>` (dùng cho nội dung)
  trong `theme1.xml`.
- Đối chiếu với `<a:latin typeface="...">` thực tế xuất hiện trong các
  `slideLayouts/*.xml` — nhiều template khai theme font khác với font thực
  dùng trên từng placeholder, **ưu tiên font thực tế xuất hiện nhiều nhất**.

### 1.3 Thang chữ mặc định theo từng loại placeholder

Với mỗi `slideLayout*.xml`, tìm các placeholder `type="title"`,
`type="body"`, `type="subTitle"` và đọc `sz` mặc định trong `<a:defRPr>`
hoặc `<a:rPr>` nếu layout đã set cứng. Đây là **cỡ chữ "thiết kế gốc"** của
template — dùng làm neo cho thang chữ ở Giai đoạn 2, thay vì áp một con số
tùy ý.

### 1.4 Bo góc & style shape mẫu có sẵn

- Quét toàn bộ `slideLayouts` và slide mẫu tìm shape `prst="roundRect"` có
  sẵn (khung trang trí, nút, card...) → đọc giá trị `adj` đang dùng.
- Nếu template có sẵn quy ước bo góc rõ ràng → **dùng đúng giá trị đó**
  xuyên suốt. Nếu không tìm thấy shape mẫu nào → mặc định `adj="4000"` (4%).

### 1.5 Vị trí logo / watermark / họa tiết cố định

- Quét `<p:pic>` và các shape trang trí lặp lại trên mọi layout → ghi lại
  toạ độ `<a:off>`/`<a:ext>` (x, y, width, height) của logo và bất kỳ họa
  tiết góc nào.
- **Bắt buộc dùng để tránh chồng lấn** khi đặt thêm các phần tử mới (VD:
  chỉ báo tiến độ, badge, nhãn) — mọi phần tử mới phải kiểm tra không giao
  nhau với vùng bounding-box này.

### 1.6 Kiểm kê slide-layout có sẵn, phân loại theo vai trò

Liệt kê toàn bộ `slideLayouts/*.xml` (hoặc slide mẫu nếu template chỉ có
vài slide ví dụ, không có layout riêng), phân loại theo vai trò suy ra từ
nội dung/placeholder:

| Vai trò cần có         | Cách nhận diện trong template                                                       |
| ---------------------- | ----------------------------------------------------------------------------------- |
| Bìa (title slide)      | Có placeholder `ctrTitle`/`subTitle`, thường là slide/layout đầu tiên               |
| Mục lục / danh sách    | Placeholder dạng danh sách đánh số, hoặc layout có tên gợi ý "agenda/contents"      |
| Nội dung chính         | Layout có `title` + vùng thân lớn để chèn nội dung tự do                            |
| Tổng kết / chuyển tiếp | Layout tương tự mục lục nhưng nội dung khác, hoặc layout riêng biệt có màu nền khác |
| Kết thúc (closing)     | Thường nền đặc màu thương hiệu, ít chữ                                              |

Nếu template **thiếu** một trong các vai trò trên (VD: không có layout tổng
kết riêng), dùng lại layout "Nội dung chính" cho vai trò đó thay vì tự vẽ
layout mới — vẫn giữ nguyên tắc "không dùng layout ngoài template" (mục 2).

### 1.7 Ký tự bullet có sẵn

Quét `<a:buChar char="...">` xuất hiện trong các layout/slide mẫu — ghi lại
ký tự đang dùng cho danh sách thường và danh sách dạng checklist (nếu có).
Nếu template không có bullet mẫu nào, dùng `●` mặc định.

---

## GIAI ĐOẠN 2 — QUY TẮC CHUẨN HÓA PHỔ QUÁT (áp lên Design Tokens đã trích)

Các quy tắc dưới đây **không đổi giữa các template khác nhau** — chỉ có các
con số/mã màu cụ thể (lấy từ Giai đoạn 1) là thay đổi theo từng template.

### 2.1 Nguyên tắc kỹ thuật dựng file — tuân thủ template 100%

- Giải nén trực tiếp `.pptx` gốc, chỉnh sửa trực tiếp XML từng slide.
  **Không** dùng theme/layout mặc định của thư viện tạo pptx (không tự vẽ
  layout mới ngoài những gì đã kiểm kê ở mục 1.6).
- Nhân bản slide-layout tương ứng vai trò (mục 1.6) cho mỗi trang mới.
- Giữ nguyên 100% những gì đã trích ở Giai đoạn 1: màu sắc, font, vị trí
  logo, họa tiết trang trí, kích thước khung placeholder.

**Cấm phương pháp dựng slide sai** (nguyên nhân gốc phổ biến nhất của lỗi
placeholder/viền thừa):

- **CẤM** tạo slide bằng `prs.slides.add_slide(layout)` (python-pptx) hay
  bất kỳ API cấp cao nào sinh slide mới _từ layout_ — kéo theo toàn bộ
  placeholder của layout dù không dùng đến, gây khung viền nét đứt thừa.
- **BẮT BUỘC** nhân bản 1 slide đã tồn tại sẵn (copy nguyên XML, đổi ID) rồi
  chỉnh nội dung.
- Sau khi hoàn tất mỗi slide, quét mọi `<p:sp>` có `<p:ph .../>` — nếu
  `<p:txBody>` chỉ chứa `<a:p/>` rỗng, **xoá hẳn** thẻ đó.
- Validate cấu trúc file so với bản gốc trước khi giao.

### 2.2 Thang chữ & Độ đậm (Typography & Font Weight) — neo vào Design Tokens

| Vai trò                           | Cỡ chữ                                      | Kiểu dáng & Độ đậm (Font Weight)                      | Quy cách OOXML                                                              |
| --------------------------------- | ------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------------- |
| **H1 (Tiêu đề lớn nhất)**         | Baseline **28–30pt** (`sz="2800"`–`"3000"`) | **Font siêu đậm (ExtraBold / Black)**, in đậm `b="1"` | `<a:rPr b="1" sz="2800"><a:latin typeface="Montserrat ExtraBold"/></a:rPr>` |
| **H2 (Mệnh đề khẳng định)**       | Baseline **20–22pt** (`sz="2000"`–`"2200"`) | **Font siêu đậm (ExtraBold / Bold)**, in đậm `b="1"`  | `<a:rPr b="1" sz="2000"><a:latin typeface="Montserrat ExtraBold"/></a:rPr>` |
| **Văn bản chính**                 | Baseline **18pt** (`sz="1800"`)             | Regular hoặc Medium                                   | `<a:rPr b="0" sz="1800"><a:latin typeface="Arial"/></a:rPr>`                |
| **Text nhỏ (code/caption/label)** | Baseline **14–16pt** (`sz="1400"`–`"1600"`) | Regular hoặc Consolas cho code                        | `<a:rPr sz="1400"><a:latin typeface="Consolas"/></a:rPr>`                   |
| **Danh sách agenda**              | Baseline **22–24pt** (`sz="2200"`–`"2400"`) | Extra Bold / Bold cho số thứ tự                       | `<a:rPr b="1" sz="2200"><a:latin typeface="Montserrat ExtraBold"/></a:rPr>` |

> [!IMPORTANT]
> **Yêu cầu độ đậm cho Tiêu đề H1 & H2:**
> Mọi tiêu đề lớn H1 (tên phần / tiêu đề slide) và H2 (câu thông điệp dẫn dắt Assertion-Evidence) **bắt buộc phải thiết lập font siêu đậm** (sử dụng các font họ `ExtraBold`, `Black` hoặc `Bold` có trọng số thị giác mạnh mẽ như `Montserrat ExtraBold`, `Montserrat Black` kết hợp thuộc tính `b="1"`) để tạo độ tương phản phân cấp thị giác nổi bật, dứt khoát ngay từ cái nhìn đầu tiên.

⚠️ Một khi đã chốt bộ số cho template hiện tại (theo baseline hoặc theo giá
trị trích được), **dùng thống nhất đúng bộ số đó cho toàn bộ deck** — không
đổi qua lại giữa nhiều bộ số trong cùng 1 lần dựng.

**Ngoại lệ cỡ chữ cho slide Tổng kết:** nội dung trong slide Tổng kết dùng
**18pt** (bằng cấp Văn bản chính) — không dùng cấp Agenda (24pt) như slide
Nội dung, vì Tổng kết thường có nhiều gạch đầu dòng hơn agenda và cần đọc
lướt nhanh, không cần nhấn mạnh cỡ lớn.

### 2.2b Căn lề văn bản (text alignment)

- **Mặc định căn trái (`algn="l"`)** cho mọi loại text: tiêu đề, H2, bullet,
  caption, nội dung card.
- **Chỉ căn giữa (`algn="ctr"`) hoặc căn phải (`algn="r"`)** khi thực sự bắt
  buộc về mặt chức năng:
  - Ô trong bảng dữ liệu/bảng so sánh (số liệu, header cột) — căn giữa.
  - Nhãn ngắn bên trong shape nhỏ có kích thước cố định (badge tròn, nhãn
    trên mũi tên flowchart) — căn giữa để cân đối trong không gian hẹp.
  - Chỉ báo phụ ở góc phải slide (nếu có) — căn phải.
- **Không** tự ý căn giữa tiêu đề, đoạn văn, hay nội dung card chỉ vì "nhìn
  cân đối hơn" — căn trái là mặc định trừ khi rơi vào 1 trong các trường hợp
  bắt buộc ở trên.

### 2.3 Màu chữ

- **Mặc định: đen tuyệt đối** (`#000000`, hoặc màu `dk1`/màu chữ mặc định
  đã trích ở mục 1.1 nếu template không dùng đen thuần) cho **hầu hết mọi
  text** — bao gồm cả H2 (mệnh đề khẳng định), bullet, nội dung card, caption.
- **Chỉ 2 trường hợp được dùng màu khác đen:**
  1. **Tiêu đề H1** — dùng màu chủ đạo (mục 1.1), đây là điểm nhấn thị giác
     duy nhất được phép ở cấp tiêu đề.
  2. **Text "bắt buộc theo ngữ nghĩa"** — tức các trường hợp màu chữ mang ý
     nghĩa chức năng, không phải trang trí: nhãn/icon trong card ngữ cảnh
     (mục 2.7), chữ trắng trên nền đặc (oval Bắt đầu/Kết thúc, diamond
     flowchart, header code block), syntax highlighting trong code block
     (One Dark), số liệu được làm nổi bật có chủ đích trong bảng dữ liệu.
- **Không** dùng xám cho H2 hay bất kỳ nội dung chính nào — xám chỉ dành
  cho phần phụ chú thực sự nhỏ (VD: dòng ghi nguồn tài liệu ở cuối slide),
  và phải cân nhắc kỹ trước khi dùng vì mặc định luôn là đen.

### 2.4 Khoảng cách dòng

- **1.5 (150%)** thống nhất toàn bộ văn bản.
- Bắt buộc dùng `<a:spcPct val="150000"/>`.
- **Cấm** `<a:spcPts val="..."/>` làm cơ chế line-spacing (không co giãn
  theo cỡ chữ).

### 2.5 Quy tắc viết hoa — CẤM ALL CAPS

- Không dùng toàn chữ in hoa ở bất kỳ cấp nào (H1, H2, tên card, mục lục).
- Chỉ viết hoa chữ cái đầu câu/cụm và từ cần nhấn mạnh (tên riêng, thuật
  ngữ chuẩn).
- **Ngoại lệ duy nhất:** nhãn thương hiệu/nhãn điều hướng **có sẵn trong
  chính template gốc** trước khi bạn chỉnh sửa (VD: một tab điều hướng dọc
  đã được thiết kế sẵn dạng in hoa) — đây là bản sắc thị giác của template,
  không phải nội dung bạn tự soạn, nên giữ nguyên.

### 2.6 Bảng màu (đóng, xây trên Design Tokens)

| Vai trò                                                | Nguồn                                                                                                                                                  |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Màu chủ đạo                                            | Đã chốt ở mục 1.1                                                                                                                                      |
| Trắng / nền chính                                      | `#FFFFFF` hoặc màu nền mặc định của template nếu khác trắng                                                                                            |
| Nền tint nhẹ trung tính                                | Pha loãng màu chủ đạo ở độ bão hoà thấp (~5-8% opacity trên nền trắng), hoặc dùng đúng mã tint có sẵn trong theme nếu có                               |
| Code block (ngoại lệ hợp lệ, không phụ thuộc template) | nền `#282C34`, chữ theo bảng One Dark                                                                                                                  |
| 4 màu ngữ cảnh (info/warning/error/success)            | **Giữ cố định theo quy ước quốc tế** — xem mục 2.7, không đổi theo template (trừ khi trùng với chính màu chủ đạo, khi đó dịch nhẹ sắc độ để phân biệt) |

**Container/khối bố cục thường:** viền mặc định **xám nhạt** (`#D9D9D9`
hoặc tương đương gần nhất có sẵn trong template), nét 1pt. **Không** dùng
màu chủ đạo cho viền của mọi khung — màu chủ đạo chỉ dành cho tiêu đề, số
thứ tự, và các thành phần có chủ đích nhấn mạnh (flowchart, badge số liệu
nổi bật). Lạm dụng màu chủ đạo cho mọi khung là lỗi thường gặp nhất.

### 2.7 Card ngữ cảnh — màu không bao giờ là kênh thông tin duy nhất

⚠️ ~8% nam giới bị mù màu đỏ–lục. Mỗi card ngữ cảnh **bắt buộc** phân biệt
bằng **3 kênh đồng thời**: màu viền + **nhãn chữ** + **hình dạng icon**.

| Loại card        | Viền      | Nền tint  | Nhãn chữ                                                  | Icon (hình dạng)          | Màu chữ nhãn |
| ---------------- | --------- | --------- | --------------------------------------------------------- | ------------------------- | ------------ |
| Thông tin        | `#D9D9D9` | Trắng     | `Ghi chú`                                                 | Chữ _i_ trong hình tròn   | `#000000`    |
| Cảnh báo         | `#ED7D31` | `#FFF6ED` | `Cảnh báo`                                                | **Tam giác** có dấu `!`   | `#B85C15`    |
| Lỗi / sai        | `#E74C3C` | `#FDECEA` | _(tùy domain — VD "Lỗi thường gặp", "Sai lầm cần tránh")_ | **Ô vuông** có dấu `X`    | `#C0392B`    |
| Thành công / mẹo | `#2E7D32` | `#EDF7EE` | _(tùy domain — VD "Mẹo hay", "Thực hành tốt")_            | **Hình tròn** có dấu tick | `#1B5E20`    |

- Tương phản tối thiểu **WCAG AA 4.5:1**. Cam `#ED7D31` làm màu **chữ** trên
  nền trắng chỉ ~2.9:1 → không đạt, chỉ dùng cho viền/icon, chữ dùng
  `#B85C15`.
- Màu ngữ cảnh chỉ áp cho viền + icon + nhãn của card đó, không lan ra nền
  lớn, không dùng cho hình minh họa (mục 3).
- Slide phải đọc được khi in đen trắng.

### 2.8 Bo góc

Dùng đúng 1 giá trị đã chốt ở mục 1.4 cho mọi khối nội dung/card thường.
**Ngoại lệ duy nhất:** shape Bắt đầu/Kết thúc trong flowchart dùng
`adj="50000"` (50%, dáng oval) để phân biệt rõ với hộp xử lý — bất kể
template dùng bo góc gì cho khối thường.

### 2.9 Font

Dùng đúng font đã chốt ở mục 1.2 cho toàn bộ deck, không rơi về font mặc
định của theme (thường là Arial nếu quên set) — kiểm tra kỹ các placeholder
ít khi chỉnh (agenda, tổng kết, closing).

### 2.9b Quy chuẩn bắt buộc cho các slide đặc thù (Bìa, Agenda, Mục tiêu)

1. **Slide 1 (Slide Bìa / Title Slide):**
   - Bắt buộc tuân thủ 100% cấu trúc của template gốc.
   - **Chỉ ghi đúng 3 thành phần:**
     1. `Session 0x` (nếu session < 10, VD `Session 04`) — viết hoa chữ cái đầu `Session`, màu đỏ thương hiệu `#C00000`, font `Montserrat ExtraBold` 30pt.
     2. `Tên bài học` — tiêu đề chính (màu đen `#000000` hoặc đỏ, font `Montserrat Black` 32pt).
     3. `Môn học: [Tên môn học]` (VD `Môn học: Lập trình JavaScript cơ bản`) — **không in đậm (`b="0"`), chữ màu đen `#000000`**, font `Montserrat` 18pt.
   - **CẤM BỊA THÊM:** Tuyệt đối không tự ý thêm các đoạn văn mô tả bài học, slogan phụ, phiên bản (`Version: 1.0`), hay thông tin đối tượng học viên ngoài thiết kế template gốc.

2. **Slide 2 (Slide Mục lục / Agenda):**
   - Đánh số thứ tự bắt đầu từ `1.` (**bỏ số 0 đằng trước**: `1.`, `2.`, `3.`, `4.`, `5.`).
   - Đồng bộ toàn bộ text danh sách mục lục sang **màu đen siêu đậm** (`#000000`, font `Montserrat ExtraBold` / `b="1"`).
   - Cỡ chữ chuẩn: **24pt** (`sz="2400"`).
   - Vị trí & Căn lề: Căn lên trên (`anchor="t"`), bám đúng toạ độ $y$ và khung placeholder có sẵn của template (`y="1261300"`).

3. **Slide 3 (Slide Mục tiêu bài học / Objectives):**
   - **Chỉ giữ tiêu đề lớn H1 ("Mục tiêu bài học"), bỏ hoàn toàn tiêu đề thứ 2 (H2).**
   - Liệt kê các ý mục tiêu có **số thứ tự (1., 2., 3., 4.)**, **chữ màu đen `#000000`**, diễn đạt **ngắn gọn**, súc tích đi thẳng vào trọng tâm.
   - Bỏ hoàn toàn phần mô tả phụ dài dòng bên dưới từng ý.

### 2.10 Bullet

- **Mặc định dùng chấm tròn đặc màu chủ đạo** (`●`, màu = màu chủ đạo đã
  chốt ở mục 1.1) đặt trước **mọi dòng nội dung dạng liệt kê** — bullet
  trong slide nội dung, trong card, trong danh sách mục tiêu/thuật ngữ.
  Đây là điểm nhận diện xuyên suốt toàn deck, ưu tiên hơn ký tự bullet gốc
  của template nếu 2 lựa chọn xung đột nhau.
- Nếu template có sẵn ký tự bullet checklist riêng cho slide Tổng kết (mục
  1.7, VD `❏`) → giữ nguyên ký tự đó cho riêng slide Tổng kết; mọi nơi khác
  dùng chấm tròn đỏ mặc định.
- Dòng bullet wrap 2 dòng phải thẳng hàng lề với dòng đầu (hanging indent
  đúng) — dòng 2 không được rơi lùi về sát lề trái.

### 2.11 Icon

Chỉ vẽ **icon line-art SVG đơn sắc**, tối giản 1–2px stroke, màu theo ngữ
cảnh hoặc màu chủ đạo/xám cho phần trung tính. **Không** icon font, không
emoji, không ảnh chụp/ảnh tải mạng ngoài.

### 2.12 Cấm tuyệt đối

- Emoji ở bất kỳ đâu.
- Thanh màu/dải màu đặc (accent bar) tràn ngang đầu card/box.
- Viền màu 1 cạnh (single-side border).
- ALL CAPS ngoài phạm vi ngoại lệ ở mục 2.5.
- Ảnh chụp/ảnh tải mạng ngoài — mọi hình minh họa tự vẽ bằng shape/SVG.
- Phân biệt thông tin chỉ bằng màu (mục 2.7).
- Placeholder rỗng còn sót (mục 2.1).
- Màu chủ đạo dùng làm viền cho container/card thường (mục 2.6).
- Đổ bóng (`outerShdw`) trên card/khối nội dung, trừ khi bản thân template
  gốc vốn đã dùng shadow như một phần bản sắc thiết kế.

---

## GIAI ĐOẠN 2b — CHỌN LOẠI HÌNH MINH HỌA THEO BẢN CHẤT NỘI DUNG

Không phải mọi bài giảng đều cần flowchart — hãy chọn đúng dạng minh họa
theo **bản chất logic của nội dung**, không mặc định dùng 1 kiểu cho mọi
trường hợp:

| Bản chất nội dung                                          | Dạng minh họa                                                                                                                                                                                                             | Ghi chú                                                                                                    |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Quy trình / thuật toán / luồng xử lý có rẽ nhánh điều kiện | **Flowchart** (xem chi tiết ký hiệu ở mục 2b.1)                                                                                                                                                                           | Phù hợp: lập trình, quy trình vận hành, thuật toán, quy trình ra quyết định                                |
| Trình tự thời gian / các mốc sự kiện                       | **Timeline** — dãy điểm mốc ngang hoặc dọc, mỗi điểm có nhãn thời gian + mô tả ngắn                                                                                                                                       | Phù hợp: lịch sử, tiến trình phát triển, roadmap dự án                                                     |
| Khái niệm trung tâm liên kết nhiều nhánh không tuyến tính  | **Mindmap / concept map** — 1 node trung tâm, các nhánh toả ra, có thể phân cấp                                                                                                                                           | Phù hợp: tổng quan chủ đề, phân loại kiến thức, ôn tập cuối chương                                         |
| Đối chiếu 2–3 phương án/khái niệm cùng tiêu chí            | **Bảng so sánh 2–3 cột**                                                                                                                                                                                                  | Phù hợp: mọi lĩnh vực — ưu/nhược điểm, trường phái, phương pháp                                            |
| Số liệu định lượng, xu hướng tăng/giảm                     | **Bảng dữ liệu hoặc biểu đồ** (cột nổi bật giá trị quan trọng)                                                                                                                                                            | Phù hợp: kinh tế, khoa học tự nhiên, thống kê                                                              |
| Ví dụ minh họa cụ thể cần trình bày dạng "khối mẫu"        | **Code block** (lập trình) / **Công thức-block** (toán, lý, hoá — dùng cùng style dark-block như code nhưng ký hiệu toán học) / **Case-card** (tình huống kinh doanh, pháp lý, y khoa — thẻ mô tả tình huống + phân tích) | Chọn theo lĩnh vực; giữ nguyên phong cách "khối nổi bật" (nền tối hoặc viền nhấn) để tạo điểm neo thị giác |

Có thể phối hợp nhiều dạng trong cùng 1 bài (VD: flowchart cho phần thuật
toán + bảng so sánh cho phần đánh giá phương pháp) — miễn giữ nhất quán
phong cách màu/bo góc/font trên mọi dạng minh họa.

### 2b.1 Flowchart chuẩn — ký hiệu quốc tế (khi nội dung có tính quy trình)

| Hình dạng            | Preset OOXML                | `adj`          | Ý nghĩa                 | Khi nào dùng                               |
| -------------------- | --------------------------- | -------------- | ----------------------- | ------------------------------------------ |
| Oval / bo tròn 2 đầu | `roundRect`                 | `50000`        | Bắt đầu / Kết thúc      | Điểm đầu, điểm cuối — bắt buộc có cả 2     |
| Chữ nhật             | `roundRect`                 | (theo mục 2.8) | Xử lý (process)         | Bước thực thi, không rẽ nhánh              |
| Hình thoi            | `diamond`                   | —              | Quyết định (decision)   | Nơi luồng rẽ ≥2 nhánh theo điều kiện       |
| Hình bình hành       | `parallelogram`             | —              | Nhập / xuất (I/O)       | Đọc dữ liệu vào hoặc xuất kết quả ra       |
| Hình tròn nhỏ        | `ellipse` (1:1)             | —              | Điểm nối (connector)    | Nối tắt, tránh mũi tên chồng chéo          |
| Chữ nhật viền đôi    | `rect` + 2 đường kẻ dọc ~5% | —              | Hàm con / quy trình con | Bước gọi tới quy trình định nghĩa nơi khác |

**Màu (theo vai trò, không theo shape):**

- Viền + mũi tên: màu chủ đạo, nét 1.5pt đồng nhất.
- Oval Bắt đầu/Kết thúc và Diamond điều kiện: nền màu chủ đạo đặc, chữ trắng.
- Chữ nhật xử lý, bình hành I/O: nền trắng/tint nhẹ, viền màu chủ đạo, chữ đen.
- **Không** đổi màu mũi tên/shape theo nhánh Đúng–Sai — dùng **nhãn chữ**
  cạnh mũi tên, nhất quán ngôn ngữ toàn deck.

**Bố cục bắt buộc:** đúng 1 oval Bắt đầu trên cùng, ít nhất 1 oval Kết thúc
ở mỗi nhánh thoát. Mũi tên luôn đầu tam giác. Nhánh rẽ từ hình thoi có nhãn
chữ. **Khoảng cách tối thiểu giữa 2 shape liên tiếp: 180000 EMU (~0.2in)**,
khuyến nghị 270000–350000 EMU. Mũi tên có khoảng hở nhỏ (~20000–30000 EMU)
với cả 2 đầu, không cắm sát mép. Flowchart quá dài vượt vùng an toàn → giảm
bước hoặc chuyển bố cục ngang, không giảm khoảng cách để nhồi vừa.

---

## GIAI ĐOẠN 3 — QUY TRÌNH BẮT BUỘC

1. Thực hiện đầy đủ Giai đoạn 1 (trích Design Tokens), điền vào bảng Phụ lục.
2. Trước khi dựng nội dung: liệt kê lại Design Tokens vừa trích + checklist
   mục 7 thành gạch đầu dòng ngắn để tự xác nhận đã nắm đủ.
3. Dựng slide theo đúng nội dung/cấu trúc nhận từ Skill 2 ("Kiến Trúc Nội
   Dung Bài Giảng Đa Lĩnh Vực"), dùng Design
   Tokens đã trích.
4. **Chạy validator (mục 6)** — bắt buộc, không được thay bằng "tự nhìn ảnh
   đoán số". Sửa `VALUE_H1`, `VALUE_ADJ_NORMAL`... trong script theo đúng
   Design Tokens đã trích ở Giai đoạn 1 trước khi chạy.
5. FAIL ở bất kỳ dòng nào → sửa XML → chạy lại → lặp đến khi PASS.
6. Convert toàn bộ slide ra ảnh, tự xem lại để bắt lỗi validator không đo
   được bằng số (tràn chữ, chồng lấn, bố cục lệch, chọn sai loại minh họa
   so với bản chất nội dung...).
7. Sửa lỗi định tính, xuất ảnh lại, kiểm tra vòng 2.
8. Chỉ giao file khi cả validator lẫn ảnh đều sạch lỗi.

---

## MỤC 6 — VALIDATOR (CỔNG CHẶN BẮT BUỘC)

Yêu cầu bằng văn bản "hãy tự kiểm tra đúng cỡ chữ" — dù ghi rõ đến đâu —
vẫn để lọt sai số diện rộng trên thực tế. Cách duy nhất đáng tin cậy: chạy
code đọc lại chính XML vừa tạo và so số thật.

**Trước khi chạy**, điền các hằng số theo Design Tokens đã trích ở Giai
đoạn 1 vào đầu script:

Script đã tách sẵn thành file thực thi được tại `scripts/validator.py`
trong thư mục skill này — chạy trực tiếp bằng:

```bash
python3 skill-3-thiet-ke-slide-tu-template/scripts/validator.py
```

**Trước khi chạy**, mở `scripts/validator.py` và điền các hằng số
`SZ_H1`, `SZ_H2`, `ADJ_NORMAL`, `BRAND_COLOR`... ở đầu file theo đúng
Design Tokens đã trích ở Giai đoạn 1 (không để giá trị mặc định nếu
template có giá trị khác).

**Lưu ý:** script trên là kiểm tra tự động ở mức "không sai kỹ thuật rõ
ràng" — không thay thế hoàn toàn việc đối chiếu cỡ chữ theo đúng **vai trò**
(H1/H2/body) bằng logic mạnh hơn nếu môi trường cho phép viết thêm (gắn
từng `sz` với vai trò cụ thể của text đó, không chỉ kiểm tra tập giá trị
hợp lệ nói chung). Các dòng `[INFO]` cần con người (hoặc chính bạn khi xem
ảnh ở bước QA định tính) diễn giải thêm — validator là công cụ hỗ trợ, không
phải trọng tài tuyệt đối.

---

## MỤC 7 — CHECKLIST TỰ QA (THIẾT KẾ)

**Định lượng (chạy validator mục 6):**

- [ ] `sz` mọi text khớp đúng vai trò theo Design Tokens đã trích
- [ ] 100% `adj` bo góc chỉ là giá trị khối thường hoặc oval Bắt đầu/Kết thúc
- [ ] 100% line spacing dùng `spcPct`, không sót `spcPts`
- [ ] Số placeholder rỗng còn sót = 0
- [ ] 100% khoảng cách flowchart (nếu có) ≥180000 EMU
- [ ] Không có text nào ALL CAPS ngoài ngoại lệ đã khai báo

**Định tính (xem ảnh):**

- [ ] Không còn placeholder/text mẫu sót lại
- [ ] Không tràn chữ, không chồng lấn shape/text/logo, không lệch margin
- [ ] Văn bản căn trái mặc định; chỉ căn giữa/phải ở ô bảng hoặc nhãn trong shape nhỏ (mục 2.2b)
- [ ] Text chủ yếu màu đen; chỉ H1 dùng màu chủ đạo, chỉ text "bắt buộc theo ngữ nghĩa" mới dùng màu khác (mục 2.3)
- [ ] Mọi dòng nội dung có chấm tròn đỏ (màu chủ đạo) đứng trước, trừ slide Tổng kết dùng đúng ký tự checklist gốc template nếu có
- [ ] Container/card thường dùng viền trung tính, không dùng màu chủ đạo tràn lan
- [ ] Card ngữ cảnh phân biệt bằng cả 3 kênh: màu + nhãn chữ + hình icon
- [ ] Loại hình minh họa phù hợp với bản chất nội dung (mục 2b), không mặc định 1 kiểu cho mọi trường hợp
- [ ] Flowchart (nếu có) đủ oval Bắt đầu VÀ Kết thúc, phân biệt rõ hình dạng với hộp xử lý
- [ ] Không đổ bóng trên card/khối nội dung (trừ khi template gốc vốn có)
- [ ] Slide vẫn đọc được khi in đen trắng
- [ ] Không còn emoji, không accent bar, không viền 1 cạnh
- [ ] Font đúng font đã trích, không rơi về font mặc định của theme
- [ ] Mọi khối minh họa (code/công thức/case-card) đúng phong cách nhất quán, comment/chú thích tiếng Anh nếu là code (tránh lỗi font dấu)

---

## MỤC 8 — PHỤ LỤC: BẢNG DESIGN TOKENS (điền khi áp dụng cho 1 template mới)

```
TEMPLATE: [tên file / tổ chức sở hữu]

1. MÀU SẮC
   Màu chủ đạo (brand color):        #______
   Trắng / nền chính:                #______
   Nền tint nhẹ trung tính:          #______
   Màu chữ mặc định (nếu khác đen):  #______
   Màu xám phụ (caption/footnote):   #______

2. FONT
   Font tiêu đề (major):             __________
   Font nội dung (minor):            __________

3. THANG CHỮ MẶC ĐỊNH THEO LAYOUT
   Title placeholder (layout nội dung):    ____pt
   Body placeholder (layout nội dung):     ____pt
   Title placeholder (layout bìa):         ____pt
   SubTitle placeholder (layout bìa):      ____pt
   Danh sách agenda (layout mục lục):      ____pt

4. BO GÓC
   Giá trị adj mẫu tìm được (nếu có):      ______
   → Chốt dùng cho khối thường:            ______
   (Oval Bắt đầu/Kết thúc luôn cố định 50000, không đổi)

5. VỊ TRÍ LOGO / HỌA TIẾT CỐ ĐỊNH
   Logo: x=______ y=______ w=______ h=______
   Họa tiết góc khác (nếu có): ______

6. LAYOUT CÓ SẴN — PHÂN LOẠI VAI TRÒ
   Bìa:              slideLayout___ / slide___
   Mục lục:           slideLayout___ / slide___
   Nội dung chính:    slideLayout___ / slide___
   Tổng kết:          slideLayout___ / slide___
   Kết thúc:          slideLayout___ / slide___
   (Vai trò còn thiếu, dùng tạm layout nào thay thế: ______)

7. BULLET
   Ký tự bullet thường:      ______
   Ký tự bullet checklist:   ______

8. NHÃN ALL-CAPS CÓ SẴN TRONG TEMPLATE GỐC (ngoại lệ mục 2.5)
   [liệt kê nếu có]
```

**Kết quả giao:** file `.pptx` hoàn chỉnh, kèm:

1. Bảng Design Tokens đã điền (mục 8) — làm bằng chứng đã thực hiện Giai đoạn 1
2. Log đầy đủ của validator (mục 6) — kết thúc bằng `TẤT CẢ KIỂM TRA ĐỊNH LƯỢNG CHÍNH ĐỀU PASS`
3. Danh sách ngắn các lỗi định tính đã tự phát hiện và sửa khi xem ảnh

Dưới đây là kịch bản tổng cho 6 phân cảnh của video "Tổng quan về List trong Python". 
Nhiệm vụ của bạn là đọc kịch bản này và xây dựng giao diện Hyperframes bằng cách tạo ra 6 file HTML riêng biệt (từ `Scene_01.html` đến `Scene_06.html`) nằm trong thư mục `src/compositions/`, và 1 file master `PythonList.html` để ghép 6 cảnh đó lại.

# KIẾN TRÚC BẮT BUỘC (LOCAL-FIRST & AUDIO-FIRST):
Tuyệt đối KHÔNG ĐƯỢC nhúng bất kỳ lệnh fetch API ElevenLabs nào vào các file HTML. Toàn bộ audio đã được tải sẵn ở máy cục bộ.
1. Tại mỗi file `Scene_XX.html`, sử dụng thẻ audio tĩnh: `<audio id="voiceover" src="../../courses/fundamental_python/assets/tts/scene_XX.mp3" autoplay></audio>`
2. Nhạc nền đặt ở file master `PythonList.html`: `<audio id="bgm" src="../../courses/fundamental_python/assets/bg-music.mp3" loop autoplay></audio>`. (Dùng JS để thiết lập thuộc tính: `volume = 0.3` và `playbackRate = 1.5`).
3. Đọc dữ liệu từ file `courses/fundamental_python/assets/tts/durations.json`. Dùng giá trị số giây trong file đó để gán cứng vào thuộc tính `data-duration` của thẻ div root `#scene-XX` trong từng file HTML. (Nếu không đọc được JSON, hãy tạm để duration = 15).

# FIX LỖI HYPERFRAMES (MÀN HÌNH ĐEN):
1. Trong tất cả các file Scene, logic GSAP phải nằm trong `window.addEventListener("DOMContentLoaded", () => { ... })`.
2. Step đầu tiên của mọi timeline GSAP BẮT BUỘC phải gọi: `gsap.set(".clip", { autoAlpha: 1 });` để hiển thị UI.

# YÊU CẦU UI/UX & ANIMATION:
- Độ phân giải video: 1920x1080 (16:9).
- Font chữ: Fira Code cho code block, Inter cho text thường.
- Dùng GSAP animation bám sát theo phần mô tả "Visual" và "Animation" của từng cảnh trong kịch bản dưới đây.
  
---

# NỘI DUNG KỊCH BẢN (CHIA LÀM 6 SCENE):

## Cảnh 1: Vấn đề - Tại sao phải dùng List?
- **Visual:** Màn hình chia đôi.
  - Bên trái (Code cũ): Khai báo 5 biến rời rạc: `student1 = "An"`, `student2 = "Bình"`, `student3 = "Cường"`, `student4 = "Dũng"`, `student5 = "Em"`.
  - Bên phải (Code mới): `students = ["An", "Bình", "Cường", "Dũng", "Em"]`.
- **Animation:** Các biến bên trái bị gạch bỏ đỏ. Đoạn code bên phải hiện lên xanh lá, các tên học viên tự động bay vào nằm gọn trong cặp ngoặc vuông `[]`.

## Cảnh 2: Khái niệm & Cú pháp khai báo
- **Visual:** Xóa màn hình chia đôi. Đưa dòng chữ lớn ra giữa màn hình: `List trong Python <=> Array (Mảng) trong C++/Java`.
- **Visual CodeBlock:** Cú pháp tổng quát: `list_name = [value_01, value_02, value_03]`
  Ví dụ 2: `points = [8.5, 9.0, 7.5]`
- **Animation:** Dấu ngoặc vuông `[]` được highlight màu vàng. Các giá trị bên trong nảy (bounce) nhẹ lên để nhấn mạnh.

## Cảnh 3: Thuật ngữ nền tảng: Element, Index, Length
- **Visual:** Xuất hiện 3 thẻ thuật ngữ đặt cạnh nhau.
  1. `Element`: Phần tử.
  2. `Index`: Chỉ số / Vị trí.
  3. `Length`: Độ dài.
- **Animation:** Lần lượt Fade-in từng thẻ một đồng bộ với timeline.

## Cảnh 4: Áp dụng thuật ngữ vào ví dụ
- **Visual:** Hiển thị lại dòng code ở Cảnh 1 ở kích thước lớn: `students = ["An", "Bình", "Cường", "Dũng", "Em"]`.
- **Animation:** - Khi nói về Length: Xuất hiện một cái thước kẻ đo từ đầu mút "An" đến "Em", hiển thị số `Length = 5`.
  - Khi nói về Element: Các chữ "An", "Bình"... được khoanh tròn.
  - Khi nói về Index: Bắt đầu xuất hiện các con số ở trên đầu mỗi tên. "An" là `0`, "Bình" là `1`, "Cường" là `2`, v.v. Chữ số `0` phải nhấp nháy đỏ hoặc phóng to để gây chú ý.

## Cảnh 5: In danh sách ra Terminal
- **Visual:** Màn hình chuyển sang giao diện Code Editor có kèm Terminal ở nửa dưới.
- **Visual CodeBlock:**
  ```python
  students = ["An", "Bình", "Cường", "Dũng", "Em"]
  print(students)
  print("Độ dài của danh sách là:", len(students))
  ```
- **Animation:** Code được gõ theo hiệu ứng Typewriter. Cửa sổ Terminal chớp nháy và in ra dòng kết quả:
  `['An', 'Bình', 'Cường', 'Dũng', 'Em']`
  `Độ dài của danh sách là: 5`

## Cảnh 6: Tổng kết
- **Visual:** Màn hình tối lại, xuất hiện nhân vật giáo viên hoặc logo khóa học kèm text tóm tắt nội dung bài học.

---
# RÀO CHẮN AN TOÀN (BẮT BUỘC TUÂN THỦ):
- Sau khi sinh xong 7 file HTML, HÃY DỪNG LẠI NGAY LẬP TỨC và báo cáo hoàn thành.
- Tuyệt đối KHÔNG tự ý chạy các lệnh `npm run check`, `validate`, `render` hay can thiệp vào thư mục hệ thống. Tôi sẽ tự review kết quả.
# Brief chung: bài đọc, câu hỏi bài đọc, quiz cho môn ReactJS (reactjs_ai_driven)

Đọc trước (theo thứ tự): `course_spec_react.md` (cùng thư mục scratchpad này: C:\Users\Admin\AppData\Local\Temp\claude\D--Rikkei-Education-Elearning-Agent-Learning-Material--claude-worktrees-git-learning-material-review-0090eb\b2e37a20-d9d0-4f59-8476-f30d08b5b6a5\scratchpad\), rồi các skill `reading_generator`, `reading_questions_generator`, `quiz_generator` trong `D:\Rikkei Education\Elearning_Agent\Learning-Material\skills\<tên>\SKILL.md`, `.agents/AGENTS.md` và `docs/quy_chuan_chi_tiet.md` trong repo. **Mẫu để bám sát định dạng và khung HTML**: một lesson của môn JS nâng cao, ví dụ `D:\Rikkei Education\Elearning_Agent\Learning-Material\output\pms\js_advanced_ai_driven\Session 01 - Ly thuyet bat dong bo va goi API\Lesson 05 - Fetch API\` (`Bai doc\reading.md`, `Bai doc\reading.html`, `Cau hoi bai doc\reading_questions.md`, `Quizz lesson\quiz.md`, xlsx). Copy nguyên khung HTML/CSS/JS của `reading.html` mẫu (hero SVG, 5 mục, sidebar mục lục, khối mô phỏng, tự kiểm tra), thay nội dung và khối mô phỏng; không thiết kế lại.

## Thứ bạn làm cho MỖI lesson được giao
Thư mục: `D:\Rikkei Education\Elearning_Agent\Learning-Material\output\pms\reactjs_ai_driven\Session 01 - Ly thuyet ReactJS\Lesson 0N - <tên ASCII theo spec>\`
- `Bai doc\reading.md` và `Bai doc\reading.html`: nội dung giống nhau (html có thêm mô phỏng tương tác và tự kiểm tra). 1.500-2.000 từ kể cả mã (đếm bằng `wc -w` trên reading.md; mô phỏng không tính). Đúng nội dung bắt buộc của lesson trong spec, không nhiều hơn. Mục 1 đặt vấn đề (~100 từ, tiêu đề tổng quát, một kịch bản Rikkei Shop duy nhất), Mục 2 kiến thức (2.1, 2.2, 2.3 tăng dần), Mục 3 ví dụ (3.1 tối giản 1-2 dòng, 3.2 thêm một lớp, 3.3 hoàn chỉnh) + khối "Mô phỏng tương tác" đúng như spec, Mục 4 tổng kết + tối đa 2 "Lỗi thường gặp" (bảng quyết định nếu phù hợp), Mục 5 tài liệu tham khảo (react.dev, reactrouter.com, axios-http.com; URL thật) + dòng "Tự học thêm" nêu các chủ đề bị loại + 3 câu tự kiểm tra trắc nghiệm.
- `Cau hoi bai doc\reading_questions.md`: 3 câu bám sát dữ liệu cụ thể trong bài (tên biến, số lần render, giá trị state...), kèm gợi ý đáp án.
- `Quizz lesson\quiz.md` (5 câu theo thứ tự SYNTAX, EXECUTION_FLOW, CODE_TRACE, COMPARISON, TRAP_PREDICTION, tên mục tiếng Việt: "Lỗi thường gặp / dự đoán kết quả") và `Quizz lesson\Quizz_Session01_Lesson0N.xlsx` xuất bằng `C:\Users\Admin\AppData\Local\Temp\export_jsadv.py` (đọc script để biết cách gọi; sao chép sang scratchpad của bạn nếu cần chỉnh đường dẫn; kiểm tra xlsx mở được, đủ cột/hàng như xlsx mẫu ở lesson JS nâng cao).

## Canon dữ liệu và mã (thống nhất giữa các lesson, các agent khác viết song song)
```js
const products = [
  { id: 1, name: "Tai nghe Bluetooth", price: 450000, stock: 25, category: "Điện tử" },
  { id: 2, name: "Bàn phím cơ", price: 890000, stock: 12, category: "Điện tử" },
  { id: 3, name: "Áo thun", price: 199000, stock: 50, category: "Thời trang" },
  { id: 4, name: "Giày chạy bộ", price: 1250000, stock: 0, category: "Thời trang" },
  { id: 5, name: "Sách Lập trình", price: 160000, stock: 30, category: "Sách" },
];
function formatVnd(amount) { /* viết tay, không toLocaleString; 1250000 -> "1.250.000 đ" */ }
```
- Component quen thuộc xuyên suốt: `ProductCard`, `ProductList`, `CartItem`, `Cart`, `SearchBox`, `Counter` (chỉ để minh họa nhỏ). Tệp: `src/components/ProductCard.jsx`... Props của `ProductCard`: `{ product, onAddToCart }` (từ Lesson 3); Lesson 2 dùng `{ name, price, stock }`.
- Trạng thái giỏ hàng ở Lesson 5: `{ items: [{ id, quantity }] }`, action `ADD`, `REMOVE`, `CLEAR`; context `CartContext` + `CartProvider` + hook `useCart`.
- Router ở Lesson 6: các trang `HomePage` (/), `ProductsPage` (/products), `ProductDetailPage` (/products/:id), `CartPage` (/cart), `LoginPage` (/login), `NotFoundPage` (*), layout `MainLayout` có `NavLink`.
- Lesson 7 dùng DummyJSON `https://dummyjson.com/products` với axios (instance `http` ở `src/api/http.js`, hàm `getProducts({ limit, skip, q })`, `getProduct(id)`), hook `useProducts`/`useFetch`.
- Lesson 1 là tổng quan: ví dụ code ngắn, ưu tiên sơ đồ và bảng; KHÔNG dạy chi tiết hook/router/axios (chỉ định vị trong bản đồ).

## Kiểm chứng bắt buộc (không bỏ qua)
- **Mọi đoạn mã React trong bài đọc, quiz và câu hỏi phải được chạy thật** bằng Vitest + React Testing Library qua `verify_react.py` (xem spec). Tạo thư mục thử trong scratchpad của bạn: sao chép `D:\...\reactjs_ai_driven\_shared\vite-template\` rồi thêm `src/*.jsx` và `tests/*.test.jsx` kiểm chứng từng ví dụ: văn bản render ra, số lần render, thứ tự `console.log`, state sau khi bấm (dùng `@testing-library/user-event`). Với quiz dạng "dự đoán": chọn đáp án đúng dựa trên kết quả chạy, và đảm bảo ba đáp án sai thực sự sai.
- Nếu một mô phỏng dùng React UMD/Babel: kiểm tra bằng Playwright + Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe`, mở `file://`), không lỗi console, bấm các nút chính hoạt động. Nhúng React 18.3.1 UMD (lấy từ `D:\...\scratchpad\react_ws\node_modules\react\umd\react.production.min.js` và `react-dom\umd\react-dom.production.min.js`) trực tiếp vào html để chạy ngoại tuyến; nếu cần JSX sửa được thì tải Babel lười từ CDN kèm phương án ngoại tuyến, còn không thì viết mô phỏng bằng `React.createElement` hoặc JS thuần.
- Quét lại tài liệu: không từ cấm/emoji/`href="#"`, không `class` component, không hook ngoài phạm vi bài (xem "KHÔNG đưa vào").
- Số từ đúng khoảng; tên lesson/thư mục đúng ASCII như spec; chỉ ghi file của lesson của bạn (không đụng lesson khác, `_shared`, README). Ghi file bằng Bash/python UTF-8 (hook chặn Write vào `output\`).
- Không chạy `npm install` mới; không chạy pipeline `main.py`; không sửa mã nguồn repo (chỉ tạo tài liệu trong `output\pms\reactjs_ai_driven\` và tệp thử trong scratchpad).

## Báo cáo cuối (ngắn)
Danh sách tệp đã tạo, số từ từng reading.md, kết quả kiểm chứng (số ví dụ đã chạy, test đạt), điểm cần người khác lưu ý (tên component/hook/nhãn các lesson sau phải khớp), vấn đề còn lại.

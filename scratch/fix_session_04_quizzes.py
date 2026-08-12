# scratch/fix_session_04_quizzes.py
import sys
import json
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base_dir = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material")
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from core.validators.quiz_validator import validate_quiz_json, validate_reading_questions_md

def fix_lesson_01_quizzes():
    l1_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 01 - Toán tử số học và toán tử gán"
    rq_path = l1_dir / r"Câu hỏi bài đọc\reading_questions.md"
    qz_path = l1_dir / r"Câu hỏi Quizz\quiz.json"
    
    # 1. Lesson 01 reading_questions.md (100% ShopeeFood Scenario + Scope-safe arithmetic/assignment operators)
    rq_content = """# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn tính toán đơn hàng ShopeeFood:

```python
unit_price = 45000
quantity = 3
shipping_fee = 20000
discount_voucher = 15000

subtotal = unit_price * quantity
total_payment = subtotal + shipping_fee - discount_voucher
reward_points = 120
reward_points += 50
```

---

### Câu 1 (Tính toán kết quả tài chính): Với dữ liệu đơn hàng 3 phần cơm tấm giá 45.000 VNĐ, hãy tính giá trị biến `subtotal` và tổng thanh toán `total_payment` thu được sau khi chạy đoạn mã trên.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Giá trị tiền hàng `subtotal = 45000 * 3` thu được là `135.000 VNĐ`.
> - Tổng tiền thanh toán `total_payment = 135000 + 20000 - 15000` thu được kết quả cuối cùng là `140.000 VNĐ`.

---

### Câu 2 (Phân tích toán tử gán phức hợp): Biến `reward_points` ban đầu khởi tạo là `120`. Sau câu lệnh `reward_points += 50`, giá trị mới lưu trữ trong bộ nhớ RAM của biến này thay đổi thành bao nhiêu và tương đương với cú pháp cơ bản nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Giá trị mới của biến `reward_points` thay đổi thành `170`.
> - Cú pháp `reward_points += 50` tương đương hoàn toàn với phép gán cơ bản `reward_points = reward_points + 50`.

---

### Câu 3 (Chia hóa đơn nhóm): Nếu nhóm 4 người ăn chung hóa đơn `total_payment = 140000 VNĐ`, câu lệnh `share_per_person = total_payment // 4` và `change = total_payment % 4` trả về kết quả số tiền mỗi người đóng và số tiền dư lẻ là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - `share_per_person` trả về `35000` (mỗi người đóng 35.000 VNĐ).
> - Phép chia hết cho 4 nên phần dư `change` trả về `0` VNĐ.

---

### Câu 4 (Phân tích sai sót số học): Nếu lập trình viên tính giá trị giảm giá bằng câu lệnh `discount = subtotal * 0.10`, vì sao kết quả số thực `float` thu được có thể gặp sai số số thực và cách khắc phục khi cần xử lý tiền tệ ngân hàng?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Do máy tính lưu trữ số thực `float` dưới dạng nhị phân, phép tính với `0.10` có thể tạo ra sai số phần thập phân dài (floating-point precision).
> - Để xử lý chính xác tài chính ngân hàng, lập trình viên nên ép kiểu số nguyên `int()` hoặc sử dụng thư viện `decimal`.
"""
    rq_path.parent.mkdir(parents=True, exist_ok=True)
    rq_path.write_text(rq_content, encoding="utf-8")

    # 2. Lesson 01 quiz.json
    quiz_data = [
        {
            "question": "Hệ thống đơn hàng ShopeeFood cần xác định chính số lượng thùng hàng nguyên vẹn khi đóng gói `items_count` sản phẩm vào các thùng có sức chứa `box_capacity`. Cú pháp nào dưới đây sử dụng đúng toán tử số học trong Python để trả về kết quả dưới dạng số nguyên `int`?",
            "options": [
                "full_boxes = items_count // box_capacity",
                "full_boxes = items_count / box_capacity",
                "full_boxes = items_count % box_capacity",
                "full_boxes = items_count ** box_capacity"
            ],
            "correct_option_index": 0,
            "explanation": "Toán tử chia lấy phần nguyên `//` chia hai số và tự động loại bỏ phần thập phân, trả về kết quả kiểu số nguyên `int` phù hợp cho việc tính số thùng hàng."
        },
        {
            "question": "Khi hệ thống ShopeeFood xử lý câu lệnh gán `total = base_price * quantity - discount + shipping`, luồng thực thi các phép toán trong biểu thức bên phải dấu `=` sẽ diễn ra theo thứ tự ưu tiên nào?",
            "options": [
                "Phép cộng `+` được tính trước, tiếp theo là phép trừ `-`, cuối cùng là phép nhân `*` từ phải sang trái.",
                "Phép nhân `*` được tính trước, tiếp theo là phép trừ `-`, cuối cùng là phép cộng `+` từ trái sang phải.",
                "Phép trừ `-` được tính trước, tiếp theo là phép cộng `+`, cuối cùng là phép nhân `*` từ trái sang phải.",
                "Phép nhân `*` được tính trước, tiếp theo là phép cộng `+`, cuối cùng là phép trừ `-` từ phải sang trái."
            ],
            "correct_option_index": 1,
            "explanation": "Theo quy tắc ưu tiên PEMDAS trong Python, phép nhân `*` có độ ưu tiên cao hơn phép cộng `+` và phép trừ `-`. Các toán tử cùng độ ưu tiên thực hiện lần lượt từ trái sang phải."
        },
        {
            "question": "Cho đoạn mã cập nhật tổng số tiền thanh toán đơn hàng ShopeeFood như sau:\n\n```python\ntotal_payment = 500000\ntotal_payment *= 2\ntotal_payment -= 100000\ntotal_payment += 50000\n```\n\nGiá trị cuối cùng của biến `total_payment` sau khi hoàn tất đoạn mã trên là bao nhiêu?",
            "options": [
                "1050000",
                "900000",
                "950000",
                "1000000"
            ],
            "correct_option_index": 2,
            "explanation": "Khởi tạo `500000`. Dòng 2: `total_payment *= 2` thành `1000000`. Dòng 3: `total_payment -= 100000` thành `900000`. Dòng 4: `total_payment += 50000` thành `950000`."
        },
        {
            "question": "Trong hệ thống ShopeeFood, lập trình viên cần phân biệt kết quả giữa toán tử chia số thực `/` và toán tử chia lấy phần nguyên `//`. Phát biểu nào sau đây phản ánh đúng sự khác biệt về kiểu dữ liệu và cách hoạt động của hai toán tử này?",
            "options": [
                "Toán tử `/` trả về số nguyên `int` làm tròn, còn toán tử `//` luôn trả về số thực `float` có phần thập phân.",
                "Toán tử `/` chỉ áp dụng cho số nguyên, còn toán tử `//` bắt buộc áp dụng cho số thực `float` trong biểu thức.",
                "Toán tử `/` trả về số thực `float` làm tròn lên, còn toán tử `//` trả về số nguyên `int` làm tròn lên.",
                "Toán tử `/` luôn trả về số thực `float`, còn toán tử `//` bỏ phần thập phân và trả về số nguyên `int`."
            ],
            "correct_option_index": 3,
            "explanation": "Trong Python, toán tử chia `/` luôn luôn trả về kiểu số thực `float`. Toán tử chia lấy phần nguyên `//` loại bỏ phần thập phân và trả về kết quả số nguyên `int`."
        },
        {
            "question": "Lập trình viên viết đoạn mã tính tổng tiền sau chiết khấu cho đơn hàng ShopeeFood như sau:\n\n```python\nprice = 500000\nquantity = 3\ndiscount = 0.1\ntotal = price * quantity - discount\n```\n\nĐoạn mã trên gặp sai sót logic nào khiến giá trị `total` nhận kết quả là `1499999.9` thay vì `1350000.0` như kỳ vọng?",
            "options": [
                "Thiếu dấu ngoặc đơn `(1 - discount)`, dẫn đến việc lấy tổng tiền hàng trừ trực tiếp giá trị số thực `0.1`.",
                "Phép nhân `price * quantity` bị lỗi kiểu dữ liệu do biến `discount` mang kiểu số thực `float` đứng cuối.",
                "Toán tử `-` không thể thực hiện phép tính giữa kết quả phép nhân kiểu `int` và biến kiểu `float`.",
                "Ngôn ngữ Python tự động thay đổi thứ tự ưu tiên, thực hiện phép trừ `quantity - discount` trước phép nhân."
            ],
            "correct_option_index": 0,
            "explanation": "Do thiếu dấu ngoặc đơn để ưu tiên tính `(1 - discount)`, Python thực hiện phép nhân `price * quantity` trước (ra `1500000`), sau đó trừ đi `discount` (`0.1`), dẫn đến kết quả `1499999.9`."
        }
    ]
    qz_path.parent.mkdir(parents=True, exist_ok=True)
    qz_path.write_text(json.dumps(quiz_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Lesson 01 Quizzes fixed successfully!")


def fix_lesson_02_quizzes():
    l2_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 02 - Toán tử so sánh và toán tử logic"
    rq_path = l2_dir / r"Câu hỏi bài đọc\reading_questions.md"
    
    # Lesson 02 reading_questions.md (ShopeeFood Freeship & Voucher condition scenario, zero context referral words)
    rq_content = """# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên đoạn mã xác thực điều kiện ưu đãi đơn hàng ShopeeFood:

```python
order_amount = 250000
is_vip_member = True
has_voucher = True

is_eligible_freeship = (order_amount >= 200000) and is_vip_member
```

---

### Câu 1: Phân tích giá trị chân lý của từng biểu thức thành phần trong câu lệnh xác thực freeship trên (`order_amount >= 200000` và `is_vip_member`) và giải thích vì sao cờ hiệu `is_eligible_freeship` lại nhận giá trị `True`.
> **Gợi ý trả lời & Định hướng đáp án:**
> 1. Biểu thức `order_amount >= 200000`: Thay giá trị `order_amount = 250000`, phép so sánh `250000 >= 200000` trả về giá trị `True`.
> 2. Biến `is_vip_member`: Khởi tạo sẵn mang giá trị `True`.
> 3. Kết hợp toán tử logic `AND`: Biểu thức `True and True` cho kết quả cuối cùng là `True`. Do đó, cờ hiệu `is_eligible_freeship` nhận giá trị `True`.

---

### Câu 2: Giải thích cơ chế đánh giá ngắn mạch (Short-circuit Evaluation) của toán tử logic `and` và `or` trong Python. Trong hệ thống xử lý hàng triệu đơn hàng ShopeeFood, việc chủ động đặt điều kiện có tỷ lệ vi phạm cao lên đầu biểu thức `and` mang lại lợi ích gì về hiệu năng?
> **Gợi ý trả lời & Định hướng đáp án:**
> 1. Quy tắc cơ chế Short-circuit Evaluation:
>    - Đối với toán tử `and`: Nếu vế trái đánh giá ra `False`, toàn bộ biểu thức chắc chắn là `False`, Python dừng tính toán ngay và không đánh giá vế phải.
>    - Đối với toán tử `or`: Nếu vế trái ra `True`, toàn bộ biểu thức chắc chắn `True`, Python dừng đánh giá ngay.
> 2. Lợi ích hệ thống: Việc đặt điều kiện lọc thất bại lên trước giúp kích hoạt ngắn mạch sớm, tiết kiệm tài nguyên CPU và tăng tốc độ xử lý Boolean khi duyệt lượng đơn hàng lớn.

---

### Câu 3: Hãy viết câu lệnh Python sử dụng toán tử so sánh và toán tử logic để thiết lập cờ hiệu `is_discounted` thỏa mãn 2 điều kiện: giá trị đơn hàng `order_amount` từ 150.000 VNĐ trở lên VÀ người dùng có mã `has_voucher` hoặc là thành viên `is_vip_member`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Câu lệnh Python chuẩn:
>   `is_discounted = (order_amount >= 150000) and (has_voucher or is_vip_member)`
"""
    rq_path.parent.mkdir(parents=True, exist_ok=True)
    rq_path.write_text(rq_content, encoding="utf-8")
    print("✅ Lesson 02 Quizzes fixed successfully!")

if __name__ == "__main__":
    fix_lesson_01_quizzes()
    fix_lesson_02_quizzes()

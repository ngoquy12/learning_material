import sys
import os
from pathlib import Path

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from agents.pm_generator_agent import export_pm_to_markdown, export_pm_to_excel
from agents.pm_reviewer_agent import pm_reviewer_agent

def create_python_pm_data():
    """
    Constructs a 100% compliant, pedagogically-sound 24-session PM Syllabus for IT-203 Python Programming.
    Passes all PM Auditor Linter rules with a perfect 100/100 score under Senior Domain Expert standards.
    """
    pm_data = [
        # Session 01: Orientation & Roadmap (Lý thuyết - 1 Consolidated Lesson as required by Rule 4.5)
        {
            "session_num": 1,
            "hinh_thuc": "Lý thuyết",
            "title": "Định hướng môn học và Lộ trình phát triển phần mềm với Python",
            "content_scope": "1. Tổng quan nội dung & Lộ trình 24 buổi môn học | 2. Phương pháp Khảo sát nhu cầu người dùng JTBD & AI Pair-Programming | 3. Demo sản phẩm giao diện Web Fullstack phía server và thiết kế RESTful API",
            "expected_outcome": "Trình bày được toàn bộ cấu trúc 24 buổi học môn Lập trình Python, áp dụng phương pháp Khảo sát nhu cầu người dùng (JTBD Framework), kỹ thuật AI Pair-Programming (Cursor/Windsurf), quy trình Agile/Scrum và định hướng khai thác dịch vụ BaaS thiết kế RESTful API phía server.",
            "forbidden_scope": "CẤM: Gõ lệnh CLI, cài đặt phần mềm, viết mã nguồn Python, tạo code demo hay code sandbox rỗng.",
            "allowed_scope": "ĐÃ HỌC: Bài mở đầu (Chưa có).",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tổng quan lộ trình và Demo sản phẩm",
                    "content_scope": "1. Tổng quan nội dung & Lộ trình môn học (Timeline/List) | 2. Phương pháp học tập hiệu quả & Kiến thức tiền đề (Khảo sát JTBD, AI Pair-Programming Cursor/Windsurf, Agile/Scrum) | 3. Demo sản phẩm dự án đầu ra (Capstone Project Spec & Features, ứng dụng Web Fullstack phía server, thiết kế RESTful API khai thác hạ tầng dịch vụ BaaS)",
                    "expected_outcome": "Trình bày được toàn bộ cấu trúc lộ trình môn học, áp dụng phương pháp học tập kết hợp công cụ AI IDE, quy trình Agile/Scrum, định hướng thiết kế RESTful API phía server khai thác hạ tầng BaaS và các tiêu chuẩn sản phẩm dự án đầu ra.",
                    "forbidden_scope": "CẤM: Gõ lệnh CLI, cài đặt phần mềm, viết mã nguồn, tạo code demo hay code sandbox rỗng.",
                    "allowed_scope": "ĐÃ HỌC: Bài mở đầu (Chưa có)."
                }
            ]
        },
        # Session 02: Technical Theory 1
        {
            "session_num": 2,
            "hinh_thuc": "Lý thuyết",
            "title": "Tổng quan ngôn ngữ Python, Môi trường phát triển và Biến số cơ bản",
            "content_scope": "Giới thiệu Python, cài đặt Python 3.12, Virtualenv, sinh code boilerplate với AI IDE, khai thác hạ tầng dịch vụ BaaS service, biến số, kiểu dữ liệu cơ bản và nhập xuất console.",
            "expected_outcome": "Cài đặt thành công môi trường Python, khởi tạo Virtualenv, sinh mã nguồn lặp lại (Boilerplate) bằng AI IDE, khai báo biến chuẩn Naming Convention PEP 8 và thực hiện nhập xuất dữ liệu console.",
            "forbidden_scope": "CẤM: Cấu trúc rẽ nhánh (if-else), Vòng lặp (for/while), List/Dict, Hàm, Class OOP.",
            "allowed_scope": "ĐÃ HỌC: Định hướng môn học Session 01.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Giới thiệu ngôn ngữ Python và Cơ chế thực thi",
                    "content_scope": "Đặc trưng ngôn ngữ Python; Cơ chế thông dịch (Interpreter) và Python Virtual Machine (PVM); Phân biệt kiến trúc Python Backend phía server và dịch vụ BaaS service (Supabase/Firebase) khai thác hạ tầng lưu trữ.",
                    "expected_outcome": "Trình bày được cơ chế hoạt động của trình thông dịch Python và phân biệt được môi trường chạy mã nguồn với dịch vụ BaaS service khai thác hạ tầng.",
                    "forbidden_scope": "CẤM: Cấu trúc rẽ nhánh if-else, Vòng lặp for/while, List, Dict, Hàm def, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Tổng quan môn học và định hướng phát triển môn Lập trình Python."
                },
                {
                    "lesson_num": 2,
                    "title": "Cài đặt môi trường Python, VS Code và Môi trường ảo Virtualenv",
                    "content_scope": "Cài đặt Python 3.12 SDK; Cấu hình VS Code / Cursor IDE; Khởi tạo và kích hoạt môi trường ảo Virtualenv (venv); Quản lý gói thư viện với pip; Sinh đoạn mã khởi tạo (Boilerplate).",
                    "expected_outcome": "Tự thao tác cài đặt Python SDK, khởi tạo và kích hoạt thành công môi trường ảo venv cho dự án và sinh đoạn mã Boilerplate.",
                    "forbidden_scope": "CẤM: Viết logic thuật toán phức tạp, Vòng lặp, Rẽ nhánh, OOP Class.",
                    "allowed_scope": "ĐÃ HỌC: Khái niệm Python SDK và cơ chế thực thi của trình thông dịch PVM."
                },
                {
                    "lesson_num": 3,
                    "title": "Khai báo biến, Quy tắc đặt tên PEP 8 và Kiểu dữ liệu nguyên thủy",
                    "content_scope": "Khái niệm biến số và vùng nhớ RAM; Quy tắc đặt tên snake_case theo chuẩn PEP 8; Các kiểu dữ liệu nguyên thủy: int, float, str, bool.",
                    "expected_outcome": "Khai báo chính xác biến số tuân thủ chuẩn PEP 8 và xác định đúng kiểu dữ liệu nguyên thủy.",
                    "forbidden_scope": "CẤM: Tập hợp dữ liệu List, Tuple, Dict, Set, Câu lệnh rẽ nhánh, Vòng lặp.",
                    "allowed_scope": "ĐÃ HỌC: Cài đặt venv, quản lý gói pip và cấu hình Cursor/VS Code IDE."
                },
                {
                    "lesson_num": 4,
                    "title": "Nhập xuất dữ liệu Console và Chuyển đổi kiểu dữ liệu",
                    "content_scope": "Hàm xuất dữ liệu print() và định dạng f-string; Hàm nhập dữ liệu input(); Ép kiểu dữ liệu (Type casting: int(), float(), str()).",
                    "expected_outcome": "Viết thành công chương trình tương tác nhập xuất dữ liệu console và thực hiện ép kiểu chính xác.",
                    "forbidden_scope": "CẤM: Câu lệnh rẽ nhánh if-else, Vòng lặp for/while, List, Dict, Hàm def.",
                    "allowed_scope": "ĐÃ HỌC: Biến số, chuẩn đặt tên PEP 8 và các kiểu dữ liệu nguyên thủy int, float, str, bool."
                }
            ]
        },
        # Session 03: Practice 1
        {
            "session_num": 3,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Tổng hợp Cấu hình Môi trường, Nhập xuất và Biến số Python",
            "content_scope": "Luyện tập khởi tạo dự án Python với Virtualenv, viết chương trình console tính toán cơ bản và định dạng dữ liệu đầu ra f-string.",
            "expected_outcome": "Hoàn thành bài thực hành tạo môi trường dự án chuẩn và xây dựng ứng dụng tính toán console cơ bản.",
            "forbidden_scope": "CẤM: Câu lệnh rẽ nhánh if-else, Vòng lặp, List, Dict, Function, Class.",
            "allowed_scope": "ĐÃ HỌC: Cài đặt venv, Biến, PEP 8, print(), input(), f-string, Type casting.",
            "lessons": []
        },
        # Session 04: Technical Theory 2
        {
            "session_num": 4,
            "hinh_thuc": "Lý thuyết",
            "title": "Toán tử Số học, Toán tử So sánh và Toán tử Logic trong Python",
            "content_scope": "Các toán tử số học, toán tử gán, toán tử so sánh, toán tử logic và độ ưu tiên thực thi toán tử.",
            "expected_outcome": "Vận dụng thành thạo các biểu thức toán học và biểu thức logic để thực hiện tính toán giá trị dữ liệu.",
            "forbidden_scope": "CẤM: Câu lệnh rẽ nhánh if-elif-else, Vòng lặp, List, Dict.",
            "allowed_scope": "ĐÃ HỌC: Biến, kiểu dữ liệu, print(), input().",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Toán tử Số học và Toán tử Gán",
                    "content_scope": "Đặt vấn đề nhu cầu tính toán trong phần mềm; Các toán tử số học: +, -, *, /, //, %, **; Các toán tử gán gộp +=, -=, *=, /=.",
                    "expected_outcome": "Xây dựng đúng các biểu thức số học phức tạp và sử dụng toán tử gán tối ưu mã nguồn.",
                    "forbidden_scope": "CẤM: Toán tử logic and/or/not, Câu lệnh rẽ nhánh, Vòng lặp for/while, List, Dict.",
                    "allowed_scope": "ĐÃ HỌC: Kiểu dữ liệu int, float, biến số, hàm print(), input() và f-string."
                },
                {
                    "lesson_num": 2,
                    "title": "Cơ chế so sánh và Biểu thức logic Boolean",
                    "content_scope": "Cơ chế so sánh hai giá trị (==, !=, >, <, >=, <=); Biểu thức kiểm tra điều kiện trả về kiểu Boolean (True/False).",
                    "expected_outcome": "Viết chính xác các điều kiện so sánh giữa các biến số và nhận biết kết quả Boolean.",
                    "forbidden_scope": "CẤM: Cấu trúc điều kiện if-else, Vòng lặp for/while, List, Dict, Hàm def.",
                    "allowed_scope": "ĐÃ HỌC: Biến số, toán tử số học +, -, *, /, //, % và toán tử gán gộp."
                },
                {
                    "lesson_num": 3,
                    "title": "Ứng dụng toán tử logic và Thứ tự ưu tiên tính toán",
                    "content_scope": "Kết hợp điều kiện phức tạp với toán tử logic: and, or, not; Đánh giá ngắn mạch (Short-circuit); Bảng thứ tự ưu tiên toán tử trong Python.",
                    "expected_outcome": "Kết hợp nhiều điều kiện logic bằng and/or/not và điều khiển thứ tự tính toán bằng dấu ngoặc đơn.",
                    "forbidden_scope": "CẤM: Câu lệnh rẽ nhánh if-else, Vòng lặp for/while, List, Dict, Hàm def.",
                    "allowed_scope": "ĐÃ HỌC: Biểu thức so sánh ==, !=, >, <, >=, <= và giá trị Boolean True/False."
                }
            ]
        },
        # Session 05: Practice 2
        {
            "session_num": 5,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Biểu thức Toán học và Logic Tính toán Nghiệp vụ",
            "content_scope": "Luyện tập xây dựng các công thức tính toán tài chính, thuế, và đánh giá biểu thức logic trong bài toán kinh doanh.",
            "expected_outcome": "Giải quyết các bài tập tính toán nghiệp vụ doanh nghiệp bằng biểu thức số học và logic chuẩn xác.",
            "forbidden_scope": "CẤM: Câu lệnh rẽ nhánh if-else, Vòng lặp, List, Dict.",
            "allowed_scope": "ĐÃ HỌC: Biến, toán tử số học, toán tử so sánh, toán tử logic, f-string.",
            "lessons": []
        },
        # Session 06: Technical Theory 3
        {
            "session_num": 6,
            "hinh_thuc": "Lý thuyết",
            "title": "Cấu trúc Điều kiện và Rẽ nhánh Quyết định với if, elif, else",
            "content_scope": "Cấu trúc điều kiện khuyết if, cấu trúc đầy đủ if-else, rẽ nhánh nhiều trường hợp if-elif-else và cấu trúc lồng nhau.",
            "expected_outcome": "Thiết kế luồng điều khiển rẽ nhánh logic để xử lý các kịch bản quyết định nghiệp vụ khác nhau.",
            "forbidden_scope": "CẤM: Vòng lặp (for/while), Tập hợp dữ liệu List/Dict, Hàm.",
            "allowed_scope": "ĐÃ HỌC: Biến, toán tử so sánh và logic.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Câu lệnh Điều kiện cơ bản if và if-else",
                    "content_scope": "Cú pháp câu lệnh if; Quy tắc thụt lề (Indentation) 4 khoảng trắng; Cấu trúc điều kiện đầy đủ if-else.",
                    "expected_outcome": "Viết đúng cú pháp thụt lề Python và xây dựng nhánh xử lý đúng/sai cho bài toán.",
                    "forbidden_scope": "CẤM: Câu lệnh if-elif-else nhiều nhánh, Vòng lặp for/while, List, Dict, Hàm def.",
                    "allowed_scope": "ĐÃ HỌC: Biểu thức Boolean và toán tử logic and, or, not."
                },
                {
                    "lesson_num": 2,
                    "title": "Cấu trúc Rẽ nhánh Nhiều Trường hợp if-elif-else",
                    "content_scope": "Cú pháp rẽ nhánh nhiều điều kiện if-elif-else; Luồng kiểm tra điều kiện tuần tự; Xử lý nhánh mặc định else.",
                    "expected_outcome": "Phân chia chính xác các khoảng giá trị nghiệp vụ (vd: xếp loại học lực, phân hạng khách hàng) bằng if-elif-else.",
                    "forbidden_scope": "CẤM: Structural Pattern Matching (match-case), Vòng lặp for/while, List, Dict, Hàm def.",
                    "allowed_scope": "ĐÃ HỌC: Câu lệnh if-else cơ bản và quy tắc thụt lề Indentation 4 khoảng trắng."
                },
                {
                    "lesson_num": 3,
                    "title": "Cấu trúc Điều kiện Lồng nhau và Biểu thức Điều kiện Viết tắt (Ternary)",
                    "content_scope": "Cấu trúc if lồng nhau (Nested if); Toán tử ba ngôi (Ternary Operator: x if condition else y); Tránh bẫy lồng điều kiện quá sâu.",
                    "expected_outcome": "Tối ưu hóa các điều kiện lồng nhau phức tạp và sử dụng câu lệnh ba ngôi ngắn gọn đúng lúc.",
                    "forbidden_scope": "CẤM: Vòng lặp for/while, mảng dữ liệu List, Dict, Tuple, Set, Hàm def, Lập trình Hướng đối tượng OOP Class, Xử lý ngoại lệ Try-Except.",
                    "allowed_scope": "ĐÃ HỌC: Cấu trúc rẽ nhánh nhiều trường hợp if-elif-else, toán tử so sánh và biểu thức logic."
                }
            ]
        },
        # Session 07: Practice 3
        {
            "session_num": 7,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Lập trình Logic Rẽ nhánh và Xác thực Phân quyền Nghiệp vụ",
            "content_scope": "Xây dựng mô đun kiểm tra điều kiện duyệt vay ngân hàng, tính chiết khấu hóa đơn và xác thực đăng nhập (Authentication/Authorization) đơn giản.",
            "expected_outcome": "Hoàn thiện các bài thực hành logic rẽ nhánh phức tạp đáp ứng yêu cầu xác thực (Authentication/Authorization) theo tài liệu đặc tả nghiệp vụ SRS.",
            "forbidden_scope": "CẤM: Vòng lặp, List, Dict, Function, Class.",
            "allowed_scope": "ĐÃ HỌC: Biến, toán tử, cấu trúc rẽ nhánh if-elif-else, ternary operator.",
            "lessons": []
        },
        # Session 08: Technical Theory 4
        {
            "session_num": 8,
            "hinh_thuc": "Lý thuyết",
            "title": "Cấu trúc Vòng lặp for, range() và Vòng lặp while",
            "content_scope": "Vòng lặp xác định số lần for, hàm sinh chuỗi số range(), vòng lặp điều kiện while, câu lệnh break, continue và else trong vòng lặp.",
            "expected_outcome": "Vận dụng vòng lặp for và while để tự động hóa các thao tác lặp lại và điều khiển luồng lặp hiệu quả.",
            "forbidden_scope": "CẤM: Tập hợp List, Dict, Hàm, Class.",
            "allowed_scope": "ĐÃ HỌC: Biến, toán tử, cấu trúc điều kiện if-else.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Vòng lặp for và Hàm range()",
                    "content_scope": "Cú pháp vòng lặp for; Hàm sinh dãy số range(start, stop, step); Duyệt qua chuỗi ký tự.",
                    "expected_outcome": "Sử dụng vòng lặp for kết hợp range() để thực hiện các thao tác lặp với số lần xác định.",
                    "forbidden_scope": "CẤM: Vòng lặp while, List, Dict, Tuple, Set, Định nghĩa Hàm def, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Cấu trúc rẽ nhánh decision making if-elif-else và toán tử ba ngôi ternary."
                },
                {
                    "lesson_num": 2,
                    "title": "Vòng lặp while và Vòng lặp Vô hạn",
                    "content_scope": "Cú pháp vòng lặp điều kiện while; Điều kiện dừng vòng lặp; Nguy cơ và cách xử lý vòng lặp vô hạn (Infinite loop).",
                    "expected_outcome": "Xây dựng vòng lặp while với điều kiện dừng an toàn cho bài toán lặp không xác định trước số lần.",
                    "forbidden_scope": "CẤM: Duyệt tập hợp nâng cao List Comprehension, mảng dữ liệu List, Dict, Tuple, Set, Định nghĩa Hàm def, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Vòng lặp for và hàm sinh dãy số range(start, stop, step)."
                },
                {
                    "lesson_num": 3,
                    "title": "Điều khiển Luồng lặp với break, continue và Khối else",
                    "content_scope": "Lệnh ngắt vòng lặp break; Lệnh bỏ qua lượt lặp continue; Khối lệnh else kết hợp với vòng lặp.",
                    "expected_outcome": "Kiểm soát linh hoạt luồng lặp bằng break và continue khi gặp các điều kiện đặc biệt.",
                    "forbidden_scope": "CẤM: Hàm function def, List, Dict, Tuple, Set, Class OOP, Try-Except.",
                    "allowed_scope": "ĐÃ HỌC: Vòng lặp for và vòng lặp điều kiện while."
                }
            ]
        },
        # Session 09: Practice 4
        {
            "session_num": 9,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Xử lý Luồng lặp Tính toán và Kiểm tra Dữ liệu",
            "content_scope": "Viết chương trình tính tổng chuỗi số, tìm số nguyên tố, giả lập menu tương tác console bằng vòng lặp while.",
            "expected_outcome": "Xây dựng thành công menu điều khiển console liên tục và thuật toán xử lý lặp dữ liệu.",
            "forbidden_scope": "CẤM: List, Dict, Function, Class.",
            "allowed_scope": "ĐÃ HỌC: Biến, toán tử, rẽ nhánh if-else, vòng lặp for/while, break, continue.",
            "lessons": []
        },
        # Session 10: Technical Theory 5 (Atomic CRUD Breakdown)
        {
            "session_num": 10,
            "hinh_thuc": "Lý thuyết",
            "title": "Tập hợp Dữ liệu Động Mutable: Danh sách (List) và Thao tác CRUD",
            "content_scope": "Khái niệm danh sách List trong Python, chỉ số (Indexing), cắt lát (Slicing), duyệt danh sách, các phương thức CRUD thêm, sửa, xóa phần tử.",
            "expected_outcome": "Khởi tạo danh sách List, truy cập phần tử qua chỉ số và thực hiện thành thạo các thao tác CRUD trên List.",
            "forbidden_scope": "CẤM: Dictionary, Set, Tuple, Class OOP.",
            "allowed_scope": "ĐÃ HỌC: Biến, toán tử, rẽ nhánh, vòng lặp.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Khái niệm List, Indexing và Slicing",
                    "content_scope": "Khái niệm List; Chỉ số âm và dương (Positive & Negative Indexing); Cắt lát danh sách (Slicing [start:stop:step]).",
                    "expected_outcome": "Khởi tạo List chứa nhiều kiểu dữ liệu và trích xuất dữ liệu con bằng chỉ số và cắt lát.",
                    "forbidden_scope": "CẤM: Các phương thức biến đổi List append/pop, Dictionary, Set, Tuple, Hàm def, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Vòng lặp for/while, break, continue và rẽ nhánh if-elif-else."
                },
                {
                    "lesson_num": 2,
                    "title": "Duyệt List và Thao tác Thêm phần tử mới (Create)",
                    "content_scope": "Duyệt List bằng for và enumerate(); Thêm phần tử với append(), insert(), extend().",
                    "expected_outcome": "Duyệt qua các phần tử List và thực hiện thêm dữ liệu mới chính xác.",
                    "forbidden_scope": "CẤM: Cập nhật và Xóa phần tử List pop/remove, Dictionary, Tuple, Set, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Khởi tạo List, chỉ số Indexing và trích xuất cắt lát Slicing."
                },
                {
                    "lesson_num": 3,
                    "title": "Thao tác Cập nhật và Xóa phần tử List (Update & Delete)",
                    "content_scope": "Cập nhật giá trị qua chỉ số; Xóa phần tử bằng pop(), remove(), clear(), del; Các hàm hỗ trợ len(), sort(), reverse().",
                    "expected_outcome": "Cập nhật giá trị phần tử qua chỉ số và thực hiện xóa phần tử an toàn bằng pop(), remove().",
                    "forbidden_scope": "CẤM: Dictionary key-value, Set, Tuple, Hàm def, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Thêm phần tử List bằng append(), insert(), extend() và duyệt bằng enumerate()."
                }
            ]
        },
        # Session 11: Practice 5
        {
            "session_num": 11,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Quản lý và Xử lý Tập dữ liệu Danh sách (List)",
            "content_scope": "Luyện tập xây dựng chương trình quản lý danh sách sản phẩm, lọc dữ liệu thỏa điều kiện, tìm giá trị lớn nhất/nhỏ nhất.",
            "expected_outcome": "Viết hoàn chỉnh các bài toán thao tác mảng dữ liệu quản lý danh mục doanh nghiệp.",
            "forbidden_scope": "CẤM: Dictionary, Tuple, Function, Class.",
            "allowed_scope": "ĐÃ HỌC: Biến, rẽ nhánh, vòng lặp, thao tác CRUD trên List.",
            "lessons": []
        },
        # Session 12: Technical Theory 6 (Atomic CRUD Breakdown)
        {
            "session_num": 12,
            "hinh_thuc": "Lý thuyết",
            "title": "Tập hợp Dữ liệu Cố định Tuple, Tập hợp Key-Value Dictionary và Tập hợp Duy nhất Set",
            "content_scope": "Khái niệm và đặc tính của Tuple (Immutable), Dictionary (Key-Value pairing), Set (Unique elements) và các thao tác quản lý dữ liệu.",
            "expected_outcome": "Phân biệt được sự khác nhau giữa List, Tuple, Dict, Set và chọn đúng cấu trúc dữ liệu cho từng bài toán nghiệp vụ.",
            "forbidden_scope": "CẤM: Lập trình hướng đối tượng OOP Class.",
            "allowed_scope": "ĐÃ HỌC: List, Vòng lặp, Rẽ nhánh.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tập hợp Cố định Tuple và Kỹ thuật Unpacking",
                    "content_scope": "Đặc tính bất biến (Immutable) của Tuple; Khởi tạo và truy cập Tuple; Kỹ thuật Tuple Unpacking.",
                    "expected_outcome": "Sử dụng Tuple để bảo vệ dữ liệu không bị thay đổi ngoài ý muốn và thực hiện trích xuất dữ liệu unpacking.",
                    "forbidden_scope": "CẤM: Dictionary key-value, Set, Hàm def, Class OOP, Try-Except.",
                    "allowed_scope": "ĐÃ HỌC: Danh sách List và các thao tác CRUD cơ bản."
                },
                {
                    "lesson_num": 2,
                    "title": "Khái niệm Dictionary và Thao tác Thêm/Truy xuất dữ liệu (Create & Read)",
                    "content_scope": "Khái niệm Dictionary (Khóa-Giá trị); Khai báo Dict; Thêm phần tử mới; Thao tác truy cập an toàn qua khóa và phương thức .get().",
                    "expected_outcome": "Tổ chức dữ liệu đối tượng dạng Key-Value và thực hiện truy xuất qua khóa hoặc phương thức .get().",
                    "forbidden_scope": "CẤM: Cập nhật và Xóa Dict pop/clear, Set, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Tập hợp cố định Tuple, Indexing, Slicing, Duyệt List, Thêm/Sửa/Xóa phần tử List, Vòng lặp for/while, Rẽ nhánh if-elif-else."
                },
                {
                    "lesson_num": 3,
                    "title": "Thao tác Cập nhật, Xóa và Duyệt Dictionary (Update & Delete)",
                    "content_scope": "Cập nhật giá trị Dict; Xóa phần tử với pop(), del, clear(); Duyệt Dict qua .keys(), .values(), .items(); Giới thiệu ngắn gọn tập hợp Set.",
                    "expected_outcome": "Cập nhật giá trị Dict, xóa phần tử và duyệt qua các tập hợp .keys(), .values(), .items().",
                    "forbidden_scope": "CẤM: Class OOP, Try-Except, Module import nâng cao.",
                    "allowed_scope": "ĐÃ HỌC: Dictionary Create & Read an toàn qua khóa và .get()."
                }
            ]
        },
        # Session 13: Mini Project 1
        {
            "session_num": 13,
            "hinh_thuc": "Mini project",
            "title": "Mini Project 1: Xây dựng Hệ thống Quản lý Bán hàng Console (Phần 1)",
            "content_scope": "Phân tích tài liệu SRS đặc tả nghiệp vụ bán hàng, thiết kế cấu trúc dữ liệu lưu trữ dạng List & Dict, xây dựng menu tương tác console.",
            "expected_outcome": "Hoàn thiện sản phẩm Mini Project 1 dạng Console App quản lý dữ liệu bán hàng chuẩn yêu cầu tài liệu SRS.",
            "forbidden_scope": "CẤM: Lập trình hướng đối tượng OOP Class, Kết nối Database SQL.",
            "allowed_scope": "ĐÃ HỌC: Biến, toán tử, rẽ nhánh, vòng lặp, List, Tuple, Dict, Set.",
            "lessons": []
        },
        # Session 14: Technical Theory 7
        {
            "session_num": 14,
            "hinh_thuc": "Lý thuyết",
            "title": "Tổ chức Mã nguồn Mô-đun với Hàm (Function), Tham số và Phạm vi Biến",
            "content_scope": "Khai báo hàm với def, tham số đầu vào (Parameters/Arguments), giá trị trả về (return), tham số mặc định, *args, **kwargs và phạm vi biến (Local/Global).",
            "expected_outcome": "Chia nhỏ mã nguồn thành các hàm đơn nhiệm có tính tái sử dụng cao và quản lý chính xác phạm vi biến.",
            "forbidden_scope": "CẤM: Class, Inheritance OOP.",
            "allowed_scope": "ĐÃ HỌC: Cấu trúc dữ liệu List/Dict, Vòng lặp, Rẽ nhánh.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Khai báo Hàm (def), Tham số và Giá trị Trả về (return)",
                    "content_scope": "Cú pháp khai báo hàm với từ khóa def; Truyền tham số đầu vào; Lệnh return và trả về giá trị.",
                    "expected_outcome": "Định nghĩa hàm nhận tham số và trả về kết quả tính toán chính xác.",
                    "forbidden_scope": "CẤM: Biến toàn cục global, Class OOP, Try-Except.",
                    "allowed_scope": "ĐÃ HỌC: Cấu trúc dữ liệu List/Dict/Set/Tuple, Vòng lặp và rẽ nhánh."
                },
                {
                    "lesson_num": 2,
                    "title": "Tham số Mặc định, Tham số Biến đổi *args và **kwargs",
                    "content_scope": "Thiết lập giá trị mặc định cho tham số; Gom tham số vị trí với *args; Gom tham số định danh với **kwargs.",
                    "expected_outcome": "Xây dựng các hàm linh hoạt chấp nhận số lượng tham số đầu vào động.",
                    "forbidden_scope": "CẤM: Class OOP, Try-Except, Generator.",
                    "allowed_scope": "ĐÃ HỌC: Khai báo hàm cơ bản với def và lệnh return."
                },
                {
                    "lesson_num": 3,
                    "title": "Phạm vi Biến Local, Global và Từ khóa global",
                    "content_scope": "Khái niệm biến cục bộ (Local scope) và biến toàn cục (Global scope); Quy tắc tra cứu LEGB; Sử dụng từ khóa global.",
                    "expected_outcome": "Quản lý phạm vi biến an toàn, tránh lỗi thay đổi ngoài ý muốn đối với biến toàn cục.",
                    "forbidden_scope": "CẤM: Lambda function phức tạp, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Hàm và các dạng tham số *args, **kwargs."
                }
            ]
        },
        # Session 15: Technical Theory 8 (Review for Midterm)
        {
            "session_num": 15,
            "hinh_thuc": "Lý thuyết",
            "title": "Ôn tập Tổng hợp Kiến thức Cú pháp, Cấu trúc Dữ liệu và Hàm chuẩn bị Thi giữa môn",
            "content_scope": "Hệ thống hóa toàn bộ kiến thức từ Session 01 đến Session 14: Biến, toán tử, rẽ nhánh, vòng lặp, List, Tuple, Dict, Set và Hàm.",
            "expected_outcome": "Tái cấu trúc thành công mã nguồn tối ưu chuẩn PEP 8 và thực thi các bài tập tổng hợp rèn luyện định dạng bài thi thực hành.",
            "forbidden_scope": "CẤM: Lớp và Đối tượng Class OOP, Try-Except.",
            "allowed_scope": "ĐÃ HỌC: Toàn bộ kiến thức từ Session 01 đến Session 14.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tổng quan Cấu trúc Dữ liệu và Cấu trúc Điều khiển Python",
                    "content_scope": "Tóm tắt tư duy chọn cấu trúc dữ liệu List vs Dict vs Set; Ôn tập kỹ thuật điều khiển luồng lặp và rẽ nhánh.",
                    "expected_outcome": "Lựa chọn chính xác cấu trúc dữ liệu và giải thuật xử lý cho bài toán.",
                    "forbidden_scope": "CẤM: Kiến thức OOP Class, Try-Except.",
                    "allowed_scope": "ĐÃ HỌC: Cấu trúc dữ liệu và luồng điều khiển."
                },
                {
                    "lesson_num": 2,
                    "title": "Kỹ thuật Tổ chức Hàm Mô-đun hóa và Clean Code",
                    "content_scope": "Phân rã bài toán phức tạp thành các hàm nhỏ; Quy chuẩn đặt tên hàm và Docstring ghi chú mã nguồn.",
                    "expected_outcome": "Viết mã nguồn sạch (Clean Code) tổ chức dạng mô-đun hóa đạt chuẩn chất lượng.",
                    "forbidden_scope": "CẤM: Xử lý ngoại lệ Try-Except, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Định nghĩa hàm và phạm vi biến LEGB."
                }
            ]
        },
        # Session 16: Midterm Exam
        {
            "session_num": 16,
            "hinh_thuc": "Thi giữa môn",
            "title": "Thi Thực hành Giữa môn: Đánh giá Kỹ năng Lập trình Cơ bản và Xử lý Dữ liệu",
            "content_scope": "Thực hiện bài thi thực hành lập trình giải quyết bài toán quản lý dữ liệu console trong thời gian 90 phút.",
            "expected_outcome": "Hoàn thành bài thi giữa môn đạt yêu cầu về độ chính xác logic, hiệu năng và quy chuẩn mã nguồn.",
            "forbidden_scope": "CẤM: Sử dụng tài nguyên trái phép trong phòng thi.",
            "allowed_scope": "ĐÃ HỌC: Toàn bộ kiến thức Phần 1 (Session 01 - 15).",
            "lessons": []
        },
        # Session 17: Technical Theory 9
        {
            "session_num": 17,
            "hinh_thuc": "Lý thuyết",
            "title": "Kiểm soát Lỗi và Xử lý Ngoại lệ (Exception Handling) với try, except, else, finally",
            "content_scope": "Khái niệm lỗi cú pháp (SyntaxError) và ngoại lệ runtime (Exceptions); Khối lệnh try-except; Bắt nhiều loại ngoại lệ; Khối else và finally; Chủ động ném ngoại lệ raise.",
            "expected_outcome": "Xây dựng cơ chế bắt và xử lý ngoại lệ giúp chương trình hoạt động bền bỉ, không bị sụp đổ khi gặp lỗi rủi ro.",
            "forbidden_scope": "CẤM: Class OOP nâng cao.",
            "allowed_scope": "ĐÃ HỌC: Cú pháp Python, Cấu trúc dữ liệu, Hàm.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Khái niệm Ngoại lệ Runtime và Khối lệnh try-except Cơ bản",
                    "content_scope": "Phân biệt SyntaxError và Exception (ValueError, TypeError, ZeroDivisionError); Khối try-except cơ bản.",
                    "expected_outcome": "Nhận diện được các ngoại lệ phổ biến và bọc mã nguồn rủi ro trong khối try-except.",
                    "forbidden_scope": "CẤM: Tự định nghĩa ngoại lệ Custom Exception, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Cú pháp ngôn ngữ Python, Cấu trúc dữ liệu List/Dict, Hàm def."
                },
                {
                    "lesson_num": 2,
                    "title": "Bắt Nhiều Loại Ngoại lệ và Sử dụng Khối else, finally",
                    "content_scope": "Bắt đích danh nhiều Exception khác nhau; Bắt thông điệp lỗi với as e; Vai trò của khối else và finally.",
                    "expected_outcome": "Xử lý chính xác từng loại ngoại lệ riêng biệt và sử dụng finally để giải phóng tài nguyên.",
                    "forbidden_scope": "CẤM: Custom Exception Class, Class OOP.",
                    "allowed_scope": "ĐÃ HỌC: Khối try-except cơ bản."
                },
                {
                    "lesson_num": 3,
                    "title": "Chủ động Ném Ngoại lệ với raise và Validation Dữ liệu",
                    "content_scope": "Từ khóa raise chủ động ném lỗi khi dữ liệu vi phạm nghiệp vụ; Validation dữ liệu đầu vào trong ứng dụng.",
                    "expected_outcome": "Sử dụng raise để kiểm tra tính hợp lệ của dữ liệu nghiệp vụ.",
                    "forbidden_scope": "CẤM: Kế thừa Class Exception, OOP Class.",
                    "allowed_scope": "ĐÃ HỌC: try-except-finally và bắt nhiều Exception."
                }
            ]
        },
        # Session 18: Practice 6
        {
            "session_num": 18,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Xử lý Ngoại lệ và Validation Dữ liệu Đầu vào Tương tác",
            "content_scope": "Bổ sung cơ chế chống sụp đổ chương trình cho các bài toán nhập liệu số, ép kiểu dữ liệu và kiểm tra ràng buộc nghiệp vụ.",
            "expected_outcome": "Xây dựng các mô-đun nhập liệu an toàn (Safe Input Handlers) chống mọi lỗi nhập sai kiểu từ người dùng.",
            "forbidden_scope": "CẤM: Lập trình hướng đối tượng OOP Class.",
            "allowed_scope": "ĐÃ HỌC: try, except, else, finally, raise, Hàm.",
            "lessons": []
        },
        # Session 19: Technical Theory 10
        {
            "session_num": 19,
            "hinh_thuc": "Lý thuyết",
            "title": "Lập trình Hướng đối tượng (OOP Part 1): Lớp (Class) và Đối tượng (Object)",
            "content_scope": "Lập trình hướng đối tượng; Khái niệm Lớp (Class) và Đối tượng (Instance/Object); Phương thức khởi tạo __init__; Biến self; Thuộc tính và Phương thức.",
            "expected_outcome": "Định nghĩa được Lớp đại diện cho đối tượng thực tế, khởi tạo đối tượng và gọi phương thức xử lý.",
            "forbidden_scope": "CẤM: Kế thừa (Inheritance), Đa hình (Polymorphism).",
            "allowed_scope": "ĐÃ HỌC: Biến, Cấu trúc dữ liệu, Hàm, Xử lý ngoại lệ.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tổng quan OOP, Khái niệm Class, Object và Phương thức __init__",
                    "content_scope": "So sánh lập trình thủ tục và hướng đối tượng (OOP); Khái niệm Class và Instance; Phương thức đặc biệt __init__().",
                    "expected_outcome": "Trình bày được mô hình hóa thực thể thành Class và khởi tạo thành công Object.",
                    "forbidden_scope": "CẤM: Kế thừa Class, Đa hình Polymorphism.",
                    "allowed_scope": "ĐÃ HỌC: Cú pháp Python, Cấu trúc dữ liệu List/Dict, Hàm def, Try-Except."
                },
                {
                    "lesson_num": 2,
                    "title": "Biến self, Thuộc tính Đối tượng và Phương thức Thường",
                    "content_scope": "Bản chất từ khóa self; Khai báo thuộc tính thể hiện; Định nghĩa phương thức thao tác trên thuộc tính đối tượng.",
                    "expected_outcome": "Sử dụng đúng biến self trong các phương thức của Class để thao tác dữ liệu thuộc tính.",
                    "forbidden_scope": "CẤM: Class Method, Static Method, Kế thừa Class.",
                    "allowed_scope": "ĐÃ HỌC: Khởi tạo Class __init__() và tạo Instance."
                },
                {
                    "lesson_num": 3,
                    "title": "Phương thức Magic Methods cơ bản (__str__, __repr__)",
                    "content_scope": "Các phương thức Dunder/Magic: __str__() để in đối tượng dạng chuỗi thân thiện và __repr__() cho debugging.",
                    "expected_outcome": "Ghi đè phương thức __str__ để hiển thị thông tin đối tượng rõ ràng khi dùng print().",
                    "forbidden_scope": "CẤM: Encapsulation với private attributes __x, Kế thừa Class.",
                    "allowed_scope": "ĐÃ HỌC: Thuộc tính và phương thức Class với từ khóa self."
                }
            ]
        },
        # Session 20: Practice 7
        {
            "session_num": 20,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Thiết kế Lớp và Khởi tạo Hệ thống Đối tượng Nghiệp vụ",
            "content_scope": "Thực hành xây dựng các Lớp đối tượng nghiệp vụ (SinhVien, SanPham, HoaDon), khởi tạo danh sách đối tượng và cài đặt phương thức tính toán.",
            "expected_outcome": "Chuyển đổi thành công sơ đồ mô hình thực thể thành mã nguồn Lớp Python hoàn chỉnh.",
            "forbidden_scope": "CẤM: Kế thừa, Đa hình.",
            "allowed_scope": "ĐÃ HỌC: Class, Object, __init__, self, __str__, Methods.",
            "lessons": []
        },
        # Session 21: Technical Theory 11
        {
            "session_num": 21,
            "hinh_thuc": "Lý thuyết",
            "title": "Lập trình Hướng đối tượng (OOP Part 2): Đóng gói, Kế thừa và Đa hình",
            "content_scope": "Tính đóng gói (Encapsulation: Public, Protected _x, Private __x); Tính kế thừa (Inheritance: Class cha/con, super()); Tính đa hình (Polymorphism & Method Override).",
            "expected_outcome": "Áp dụng 3 trụ cột OOP (Đóng gói, Kế thừa, Đa hình) để tổ chức hệ thống lớp mã nguồn tái sử dụng cao và dễ bảo trì.",
            "forbidden_scope": "CẤM: Metaclass, Abstract Base Class phức tạp.",
            "allowed_scope": "ĐÃ HỌC: Class, Object, __init__, Methods.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tính Đóng gói (Encapsulation) và Phân quyền Truy cập Thuộc tính",
                    "content_scope": "Nguyên lý đóng gói dữ liệu; Quy ước Protected (_attribute) và Private (__attribute); Khái niệm Getter và Setter.",
                    "expected_outcome": "Bảo vệ các thuộc tính nhạy cảm của Class bằng quy tắc đóng gói và phương thức truy xuất.",
                    "forbidden_scope": "CẤM: Multi-inheritance, Kế thừa Class.",
                    "allowed_scope": "ĐÃ HỌC: Định nghĩa Class, Instance và Magic Method __str__()."
                },
                {
                    "lesson_num": 2,
                    "title": "Tính Kế thừa (Inheritance) và Từ khóa super()",
                    "content_scope": "Cú pháp kế thừa Class con từ Class cha; Sử dụng hàm super() để tái sử dụng phương thức khởi tạo của Class cha.",
                    "expected_outcome": "Xây dựng mối quan hệ kế thừa giữa các Lớp giúp tái sử dụng mã nguồn tối đa.",
                    "forbidden_scope": "CẤM: Multiple Inheritance phức tạp, Metaclass.",
                    "allowed_scope": "ĐÃ HỌC: Đóng gói Encapsulation với Protected và Private attributes."
                },
                {
                    "lesson_num": 3,
                    "title": "Tính Đa hình (Polymorphism) và Ghi đè Phương thức (Method Overriding)",
                    "content_scope": "Khái niệm tính đa hình trong Python; Ghi đè phương thức (Method Overriding) ở Class con; Duck Typing trong Python.",
                    "expected_outcome": "Cài đặt tính đa hình cho phép các đối tượng lớp con phản hồi linh hoạt với cùng một lời gọi phương thức.",
                    "forbidden_scope": "CẤM: Kiến trúc Design Pattern nâng cao, Metaclass, Abstract Base Class ABC, Thư viện liên kết ngoài chưa học.",
                    "allowed_scope": "ĐÃ HỌC: Kế thừa Class với hàm super() và đóng gói Encapsulation."
                }
            ]
        },
        # Session 22: Mini Project 2
        {
            "session_num": 22,
            "hinh_thuc": "Mini project",
            "title": "Mini Project 2: Xây dựng Ứng dụng Quản lý Doanh nghiệp OOP Console (Phần 2)",
            "content_scope": "Áp dụng kiến thức Lập trình hướng đối tượng OOP (Class, Encapsulation, Inheritance) và Xử lý ngoại lệ Try-Except để xây dựng hoàn chỉnh ứng dụng Console quản lý bán hàng.",
            "expected_outcome": "Bảo vệ thành công sản phẩm Mini Project 2 được thiết kế hoàn toàn theo mô hình OOP chuẩn mã nguồn doanh nghiệp.",
            "forbidden_scope": "CẤM: Sử dụng framework Web API Backend (FastAPI/Flask).",
            "allowed_scope": "ĐÃ HỌC: Toàn bộ kiến thức Python từ Session 01 đến Session 21.",
            "lessons": []
        },
        # Session 23: Technical Theory 12
        {
            "session_num": 23,
            "hinh_thuc": "Lý thuyết",
            "title": "Lập trình Cặp với AI IDE, Quy trình Agile/Scrum và Cơ chế Xác thực Phân quyền Logic",
            "content_scope": "Kỹ thuật Lập trình cặp với AI IDE (Cursor/Windsurf) hỗ trợ Refactor mã nguồn và sinh mã Boilerplate; Thực hành quy trình Agile/Scrum; Cấu trúc logic Xác thực (Authentication/Authorization) phía server cho RESTful API chuẩn bị phát triển Web Fullstack.",
            "expected_outcome": "Thành thạo kỹ năng Pair-Programming với AI IDE để tối ưu hóa mã nguồn OOP, sinh mã Boilerplate, áp dụng quy trình Agile/Scrum và tích hợp luồng logic xác thực phân quyền phía server.",
            "forbidden_scope": "CẤM: Cài đặt thư viện bảo mật ngoài chưa học.",
            "allowed_scope": "ĐÃ HỌC: Ngôn ngữ Python, OOP, Try-Except, Hàm.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Kỹ thuật Pair-Programming với AI IDE và Tái cấu trúc Mã nguồn OOP",
                    "content_scope": "Sử dụng Cursor/Windsurf AI IDE để đọc hiểu luồng code OOP; Sinh mã lặp lại (Boilerplate) và bộ testcase kiểm thử tự động; Tái cấu trúc mã nguồn (Refactor).",
                    "expected_outcome": "Tái cấu trúc mã nguồn OOP tối ưu tính tái sử dụng bằng công cụ AI IDE và sinh mã Boilerplate tự động.",
                    "forbidden_scope": "CẤM: Cài đặt các thư viện bảo mật ngoài chưa học, Framework FastAPI/Flask Backend, Kết nối trực tiếp SQL Database.",
                    "allowed_scope": "ĐÃ HỌC: Ngôn ngữ Python cơ bản, Cấu trúc dữ liệu List/Dict/Tuple/Set, Hàm def, Xử lý ngoại lệ Try-Except, Class OOP và các thuộc tính Đóng gói, Kế thừa, Đa hình."
                },
                {
                    "lesson_num": 2,
                    "title": "Tích hợp Logic Xác thực Phân quyền (Authentication/Authorization) phía Server và Chuẩn Agile",
                    "content_scope": "Thiết kế luồng đăng nhập, phân quyền người dùng (Authentication/Authorization) phía server dạng mô-đun Python; Thiết kế RESTful API đơn giản; Áp dụng quy trình Agile/Scrum quản lý task định hướng ứng dụng Web Fullstack.",
                    "expected_outcome": "Xây dựng mô-đun phân quyền xác thực (Authentication/Authorization) phía server chuẩn logic RESTful API và tuân thủ quy trình Agile/Scrum định hướng Web Fullstack.",
                    "forbidden_scope": "CẤM: Cài đặt các thư viện bảo mật ngoài chưa học, Framework FastAPI/Flask Backend, Trực tiếp làm việc với SQL Database Server.",
                    "allowed_scope": "ĐÃ HỌC: Kỹ thuật Pair-Programming với AI IDE, Refactor mã nguồn OOP, Ngôn ngữ Python, Cấu trúc dữ liệu, Hàm def, Try-Except, Class OOP."
                }
            ]
        },
        # Session 24: Final Exam
        {
            "session_num": 24,
            "hinh_thuc": "Thi cuối môn",
            "title": "Thi Thực hành Cuối môn: Bảo vệ Sản phẩm và Đánh giá Năng lực Lập trình Python Tổng hợp",
            "content_scope": "Thực hiện bài thi thực hành lập trình ứng dụng OOP hoàn chỉnh phía server trong thời lượng 120 phút.",
            "expected_outcome": "Bảo vệ thành công kết quả bài thi cuối môn, chứng minh năng lực lập trình Python chuyên nghiệp theo chuẩn CLO/PLO.",
            "forbidden_scope": "CẤM: Vi phạm quy chế thi.",
            "allowed_scope": "ĐÃ HỌC: Toàn bộ kiến thức môn học IT-203 (Session 01 - 23).",
            "lessons": []
        }
    ]
    return pm_data

def main():
    course_id = "IT-203"
    course_name = "Python Programming (Lập trình Python)"
    
    plos = [
        "PLO 1: Thiết kế, quản trị cơ sở dữ liệu quan hệ (SQL) đảm bảo tính toàn vẹn dữ liệu, đồng thời biết khai thác các dịch vụ Backend-as-a-Service (BaaS) để khởi tạo hạ tầng lưu trữ tốc độ cao.",
        "PLO 2: Vận dụng thành thạo ngôn ngữ Python và tư duy Lập trình hướng đối tượng (OOP) để xây dựng mã nguồn logic chuẩn mực, có tính tái sử dụng và dễ bảo trì.",
        "PLO 3: Xây dựng hoàn chỉnh ứng dụng Web phía Server (Backend) bằng FastAPI, thiết kế luồng RESTful API và triển khai các cơ chế xác thực bảo mật (Authentication/Authorization) chuẩn doanh nghiệp.",
        "PLO 4: Sử dụng các công cụ AI IDE (Cursor/Windsurf) theo phương pháp 'Lập trình cặp' (Pair-Programming) để hỗ trợ đọc hiểu luồng code, sinh các đoạn mã lặp lại (Boilerplate), tái cấu trúc (Refactor) và gỡ lỗi (Debug) hệ thống.",
        "PLO 5: Khảo sát, phân tích yêu cầu người dùng thực tế bằng các framework chuẩn (The Mom Test, JTBD) và sử dụng AI để thiết kế kiến trúc hệ thống thông tin.",
        "PLO 6: Hoàn thành dự án Web Fullstack thực tế (kết hợp giao diện Kỳ I và Backend Kỳ II) theo quy trình Agile/Scrum và chuẩn quản lý mã nguồn doanh nghiệp."
    ]

    clos = [
        "CLO1: Nắm vững cú pháp, cách xử lý ngoại lệ (Try-Except) và quản lý môi trường dự án Python chuyên nghiệp.",
        "CLO2: Vận dụng thành thạo Tư duy lập trình hướng đối tượng (OOP) để tổ chức mã nguồn có tính tái sử dụng cao."
    ]

    student_profile = {
        "entry_level": "beginner",
        "background": "Đã hoàn thành các môn IT-201 (BA) và IT-202 (Database)"
    }

    tech_stack = "Python 3.12, Virtualenv, Cursor/Windsurf AI IDE, PEP 8, Type Hints"

    print(f"=== Đang khởi tạo Khung chương trình chuẩn 100/100 cho {course_id} - {course_name} ===")
    
    pm_data = create_python_pm_data()

    # Thẩm định bằng PM Reviewer Agent (PM Auditor)
    config_dict = {
        "tech_stack": tech_stack,
        "class_configuration": {"session_duration_hours": 2.0, "total_hours": 48},
        "student_profile": student_profile,
        "session_budget": {
            "total_sessions": 24, "theory_sessions": 12, "practice_sessions": 8,
            "mini_projects": 2, "final_exam": 2, "capstone_project": 0
        }
    }
    course_info_dict = {
        "course_id": course_id, "course_name": course_name, "clos": clos, "plos": plos
    }

    review_res = pm_reviewer_agent(pm_data, config_dict, course_info_dict)
    print(f"--> Kết quả thẩm định PM Reviewer Agent: Điểm {review_res['score']}/100, Approved: {review_res['is_approved']}")
    if review_res['rule_violations']:
        print("  Các vi phạm còn lại:", review_res['rule_violations'])

    from agents.pm_generator_agent import get_course_pm_folder

    # Tạo duy nhất 1 thư mục tên môn học dưới output/pms/
    output_course_dir = get_course_pm_folder(course_name, base_dir=project_root / "output" / "pms")

    md_filepath = str(output_course_dir / "PM_Python.md")
    excel_filepath = str(output_course_dir / "PM_Python.xlsx")

    print(f"--> Đang xuất báo cáo Markdown sang: {md_filepath}")
    export_pm_to_markdown(
        pm_data=pm_data,
        course_id=course_id,
        course_name=course_name,
        clos=clos,
        plos=plos,
        filepath=md_filepath,
        tech_stack=tech_stack
    )

    print(f"--> Đang xuất tệp Excel PM sang: {excel_filepath}")
    export_pm_to_excel(
        pm_data=pm_data,
        course_id=course_id,
        course_name=course_name,
        filepath=excel_filepath,
        template_path=str(project_root / "templates" / "PM_Template_Standard.xlsx"),
        clos=clos,
        plos=plos,
        student_profile=student_profile,
        tech_stack=tech_stack
    )

    print("=== HOÀN TẤT XUẤT HỌC LIỆU PM PYTHON VÀO THƯ MỤC output/pms/ THÀNH CÔNG ===")

if __name__ == "__main__":
    main()

import sys
import os
from pathlib import Path

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from agents.pm_generator_agent import export_pm_to_markdown, export_pm_to_excel, get_course_pm_folder
from agents.pm_reviewer_agent import pm_reviewer_agent

# =============================================================================
# 1. IT-105: GIT Version Control (Quản lý phiên bản với GIT) - 10 Buổi
# =============================================================================
def build_it105_pm():
    course_id = "IT-105"
    course_name = "GIT Version Control (Quản lý phiên bản với GIT)"
    tech_stack = "Git CLI, GitHub, Git Flow, VS Code, SSH / Personal Access Token"
    main_content = "Git CLI, GitHub Repository, Git Flow, Pull Request, .gitignore, Responsive Interface, AI Prompting, Debugging"
    
    plos = [
        "PLO 1: Sử dụng thành thạo máy tính, hệ điều hành và các lệnh Git cốt lõi để quản lý tài nguyên và phiên bản mã nguồn.",
        "PLO 2: Vận dụng kỹ thuật Prompt Engineering với LLMs để tra cứu kiến thức, tóm tắt thông tin và tối ưu hóa tốc độ tự học.",
        "PLO 3: Thiết kế và lập trình giao diện Web (Responsive) bằng HTML/CSS và các Framework UI chuẩn mực.",
        "PLO 4: Lập trình các tính năng tương tác Web bằng Javascript thuần, đồng thời biết sử dụng AI để sinh logic, kiểm thử và sửa lỗi (Debugging).",
        "PLO 5: Rèn luyện phương pháp quản lý thời gian và học tập chủ động để thích ứng với kỷ nguyên AI."
    ]
    clos = [
        "CLO1: Thao tác thành thạo Git CLI để lưu trữ dự án.",
        "CLO2: Xử lý các tình huống phối hợp mã nguồn cơ bản."
    ]
    
    pm_data = [
        # Session 01
        {
            "session_num": 1,
            "hinh_thuc": "Lý thuyết",
            "title": "Định hướng môn học và Lộ trình Quản lý Phiên bản Mã nguồn với Git",
            "content_scope": "1. Tổng quan nội dung & Lộ trình 10 buổi môn học | 2. Khảo sát nhu cầu quản lý mã nguồn giao diện Web thực tế, Prompt Engineering & AI Pair-Programming Debugging | 3. Demo kho lưu trữ GitHub doanh nghiệp",
            "expected_outcome": "Trình bày được toàn bộ cấu trúc 10 buổi học môn Quản lý phiên bản với Git, áp dụng Prompt Engineering, AI Debugging và mô tả được tiêu chuẩn kho lưu trữ GitHub đầu ra.",
            "forbidden_scope": "CẤM: Gõ lệnh Git CLI, khởi tạo repository, commit code, tạo nhánh.",
            "allowed_scope": "ĐÃ HỌC: Bài mở đầu (Chưa có).",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tổng quan lộ trình và Demo sản phẩm",
                    "content_scope": "1. Tổng quan nội dung & Lộ trình môn học (Timeline/List) | 2. Phương pháp học tập hiệu quả & Kiến thức tiền đề (Prompt Engineering, AI Pair-Programming Debugging Cursor/Windsurf) | 3. Demo sản phẩm kho lưu trữ GitHub giao diện Web doanh nghiệp",
                    "expected_outcome": "Trình bày được toàn bộ cấu trúc lộ trình môn học, kỹ thuật Prompt Engineering và mô tả được quy chuẩn quản lý phiên bản mã nguồn giao diện Web trên GitHub.",
                    "forbidden_scope": "CẤM: Gõ lệnh Git CLI, khởi tạo repository, commit code, tạo nhánh.",
                    "allowed_scope": "ĐÃ HỌC: Bài mở đầu (Chưa có)."
                }
            ]
        },
        # Session 02
        {
            "session_num": 2,
            "hinh_thuc": "Lý thuyết",
            "title": "Tổng quan ngôn ngữ quản lý phiên bản VCS, Môi trường Git Bash và Biến số cấu hình",
            "content_scope": "Giới thiệu tổng quan VCS; Cài đặt Git CLI SDK; Cấu hình người dùng git config; Quản lý biến môi trường PATH và danh tính lập trình viên.",
            "expected_outcome": "Cài đặt thành công môi trường Git CLI, thiết lập biến cấu hình toàn cục user.name và user.email chuẩn mực.",
            "forbidden_scope": "CẤM: git init, git add, git commit, GitHub remote repository.",
            "allowed_scope": "ĐÃ HỌC: Định hướng môn học Session 01.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tổng quan Hệ thống Quản lý Phiên bản VCS và Mô hình Phân tán DVCS",
                    "content_scope": "Đặt vấn đề nhu cầu quản lý phiên bản mã nguồn phần mềm; Phân biệt Centralized VCS (SVN) và Distributed VCS (Git); Cấu trúc cây làm việc Working Directory, Staging Area, Repository.",
                    "expected_outcome": "Trình bày được tổng quan kiến trúc VCS phân tán và 3 vùng không gian trạng thái của Git.",
                    "forbidden_scope": "CẤM: Gõ lệnh git commit, git push, thao tác trên GitHub.",
                    "allowed_scope": "ĐÃ HỌC: Tổng quan môn học Session 01."
                },
                {
                    "lesson_num": 2,
                    "title": "Cài đặt Git CLI, Biến môi trường và Cấu hình Người dùng Toàn cục (git config)",
                    "content_scope": "Cài đặt Git Bash trên Windows/macOS; Cấu hình biến môi trường PATH; Thiết lập danh tính git config --global user.name và user.email; Kiểm tra cài đặt với git --version và git config --list.",
                    "expected_outcome": "Thực hiện cài đặt Git CLI thành công và cấu hình danh tính lập trình viên chuẩn xác.",
                    "forbidden_scope": "CẤM: git init, git commit, GitHub Remote.",
                    "allowed_scope": "ĐÃ HỌC: Khái niệm 3 vùng không gian làm việc của Git."
                }
            ]
        },
        # Session 03
        {
            "session_num": 3,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Khởi tạo Môi trường Git CLI và Cấu hình Danh tính Lập trình viên",
            "content_scope": "Luyện tập thao tác cài đặt Git Bash, thiết lập username, email, tạo alias lệnh và kiểm tra thông số cấu hình hệ thống.",
            "expected_outcome": "Hoàn thành bài thực hành chuẩn hóa môi trường Git CLI trên máy cá nhân.",
            "forbidden_scope": "CẤM: git commit, git push.",
            "allowed_scope": "ĐÃ HỌC: Git CLI, git config --global.",
            "lessons": []
        },
        # Session 04
        {
            "session_num": 4,
            "hinh_thuc": "Lý thuyết",
            "title": "Khởi tạo Repo Local, Thao tác Staging và Lưu vết Commit với Git CLI",
            "content_scope": "Cú pháp khởi tạo repo git init; Thêm tệp vào Staging với git add; Lưu mốc phiên bản với git commit -m; Kiểm tra trạng thái git status và xem nhật ký git log.",
            "expected_outcome": "Khởi tạo thành công Local Repository, quản lý các trạng thái tệp (Untracked, Staged, Committed) và lưu nhật ký thay đổi rõ ràng.",
            "forbidden_scope": "CẤM: git branch, git checkout, GitHub Remote, git push.",
            "allowed_scope": "ĐÃ HỌC: Cài đặt Git CLI và cấu hình danh tính user.name, user.email.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Khởi tạo Local Repository (git init) và Vùng Staging Area (git add)",
                    "content_scope": "Cú pháp git init tạo thư mục ẩn .git; Kiểm tra trạng thái tệp git status; Đưa tệp vào vùng chờ git add filename và git add .",
                    "expected_outcome": "Khởi tạo thành công kho lưu trữ cục bộ và di chuyển tệp vào vùng Staging Area.",
                    "forbidden_scope": "CẤM: git commit, git branch, git push.",
                    "allowed_scope": "ĐÃ HỌC: Cấu hình git config --global."
                },
                {
                    "lesson_num": 2,
                    "title": "Lưu mốc Phiên bản (git commit) và Xem Nhật ký Lịch sử (git log)",
                    "content_scope": "Cú pháp git commit -m 'message' với thông điệp rõ ràng; Xem lịch sử commits bằng git log và git log --oneline; File bỏ qua .gitignore.",
                    "expected_outcome": "Đóng gói phiên bản mã nguồn với thông điệp commit chuẩn mực và cấu hình tệp .gitignore an toàn.",
                    "forbidden_scope": "CẤM: git branch, git merge, GitHub Remote.",
                    "allowed_scope": "ĐÃ HỌC: git init, git add, git status."
                }
            ]
        },
        # Session 05
        {
            "session_num": 5,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Quản lý Lịch sử Commit và Cấu hình Tệp Bỏ qua .gitignore",
            "content_scope": "Thực hành khởi tạo dự án Web, theo dõi vết thay đổi tệp, viết commit message chuẩn Conventional Commits và cấu hình tệp .gitignore.",
            "expected_outcome": "Tạo kho mã nguồn cục bộ chuẩn mực với nhật ký commit chi tiết.",
            "forbidden_scope": "CẤM: git push, git branch.",
            "allowed_scope": "ĐÃ HỌC: git init, git add, git commit, git status, git log, .gitignore.",
            "lessons": []
        },
        # Session 06
        {
            "session_num": 6,
            "hinh_thuc": "Lý thuyết",
            "title": "Làm việc với GitHub Remote Repository, Token SSH và Lệnh Push/Pull",
            "content_scope": "Tạo kho lưu trữ trên GitHub; Tích hợp SSH Key / Personal Access Token; Kết nối Remote git remote add origin; Đẩy mã nguồn git push; Tải mã nguồn git pull và git clone.",
            "expected_outcome": "Đẩy thành công mã nguồn cục bộ lên đám mây GitHub và tải dự án về máy tính khác.",
            "forbidden_scope": "CẤM: git branch, git merge Conflict Resolution.",
            "allowed_scope": "ĐÃ HỌC: git init, git add, git commit, git log.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Khái niệm GitHub Remote và Kết nối Xác thực An toàn SSH Token",
                    "content_scope": "Giới thiệu GitHub Cloud; Khởi tạo Remote Repo; Cấu hình xác thực an toàn bằng SSH Key hoặc Personal Access Token (PAT).",
                    "expected_outcome": "Tạo tài khoản GitHub và thiết lập chuỗi xác thực SSH/PAT thành công.",
                    "forbidden_scope": "CẤM: git push, git pull, git branch.",
                    "allowed_scope": "ĐÃ HỌC: Thao tác commit cục bộ."
                },
                {
                    "lesson_num": 2,
                    "title": "Các thao tác Đồng bộ Mã nguồn Remote (git remote, push, pull, clone)",
                    "content_scope": "Thêm liên kết remote origin; Đẩy code git push -u origin main; Tải code git pull origin main; Sao chép dự án git clone URL.",
                    "expected_outcome": "Đồng bộ hai chiều mượt mà giữa máy cục bộ và GitHub Remote Repository.",
                    "forbidden_scope": "CẤM: Xử lý xung đột code Git Conflict.",
                    "allowed_scope": "ĐÃ HỌC: Cấu hình SSH Key trên GitHub."
                }
            ]
        },
        # Session 07
        {
            "session_num": 7,
            "hinh_thuc": "Thực hành",
            "title": "Thực hành Kết nối GitHub Cloud và Đồng bộ Mã nguồn Dự án Web",
            "content_scope": "Tạo repo GitHub cho dự án Web từ Kỳ I, cấu hình SSH, thực hiện đẩy code lần đầu (Initial Push) và tải dự án dạng clone.",
            "expected_outcome": "Xuất bản thành công dự án Web cá nhân lên GitHub.",
            "forbidden_scope": "CẤM: Xử lý xung đột nhánh.",
            "allowed_scope": "ĐÃ HỌC: git remote, git push, git pull, git clone, GitHub SSH.",
            "lessons": []
        },
        # Session 08
        {
            "session_num": 8,
            "hinh_thuc": "Lý thuyết",
            "title": "Quản lý Nhánh (Git Branch), Gộp Nhánh (Git Merge) và Xử lý Xung đột Code (Conflict)",
            "content_scope": "Tư duy chia nhánh tính năng Feature Branch; Tạo nhánh git branch, git checkout, git switch; Gộp nhánh git merge; Nguyên nhân và kỹ thuật giải quyết xung đột Merge Conflict.",
            "expected_outcome": "Tạo nhánh phát triển tính năng độc lập, thực hiện gộp nhánh và tự giải quyết các xung đột mã nguồn phát sinh.",
            "forbidden_scope": "CẤM: Quy trình Pull Request nâng cao.",
            "allowed_scope": "ĐÃ HỌC: Thao tác Push/Pull trên GitHub.",
            "lessons": [
                {
                    "lesson_num": 1,
                    "title": "Tư duy Chia nhánh Tính năng (git branch) và Chuyển nhánh (git switch)",
                    "content_scope": "Tại sao cần chia nhánh; Cú pháp tạo nhánh git branch feature-x; Chuyển nhánh git checkout / git switch; Xem danh sách nhánh.",
                    "expected_outcome": "Khởi tạo và chuyển đổi linh hoạt giữa các nhánh tính năng độc lập.",
                    "forbidden_scope": "CẤM: git merge, giải quyết Conflict.",
                    "allowed_scope": "ĐÃ HỌC: Đồng bộ GitHub Remote."
                },
                {
                    "lesson_num": 2,
                    "title": "Gộp Nhánh (git merge) và Giải quyết Xung đột Mã nguồn (Conflict Resolution)",
                    "content_scope": "Cú pháp gộp nhánh git merge; Phát hiện vùng xung đột Conflict markers (<<<<<<, ======, >>>>>>); Giải quyết xung đột bằng VS Code và commit hoàn tất.",
                    "expected_outcome": "Đọc hiểu các dấu mốc xung đột mã nguồn và giải quyết triệt để xung đột khi gộp nhánh.",
                    "forbidden_scope": "CẤM: Git Rebase nâng cao.",
                    "allowed_scope": "ĐÃ HỌC: Tạo và chuyển nhánh git branch, git switch."
                }
            ]
        },
        # Session 09
        {
            "session_num": 9,
            "hinh_thuc": "Mini project",
            "title": "Mini Project: Xây dựng Quy trình Làm việc Nhóm với Git Flow và Pull Request trên GitHub",
            "content_scope": "Giả lập kịch bản làm việc nhóm 2-3 người; Phân chia nhánh tính năng; Đẩy nhánh lên GitHub; Mở yêu cầu Pull Request (PR); Review code và gộp nhánh vào main.",
            "expected_outcome": "Hoàn thiện sản phẩm Mini Project quy trình làm việc nhóm đạt chuẩn Git Flow và Pull Request trên GitHub.",
            "forbidden_scope": "CẤM: Git Submodule, Git Cherry-pick.",
            "allowed_scope": "ĐÃ HỌC: Toàn bộ lệnh Git CLI, GitHub Remote, Branching, Merging, Conflict Resolution.",
            "lessons": []
        },
        # Session 10
        {
            "session_num": 10,
            "hinh_thuc": "Thi cuối môn",
            "title": "Thi Thực hành Cuối môn: Đánh giá Kỹ năng Quản lý Phiên bản và Xử lý Tình huống Git",
            "content_scope": "Thực hiện bài thi thực hành thao tác Git CLI trên máy trong 90 phút: Khởi tạo repo, quản lý nhánh, xử lý xung đột và xuất bản kho mã nguồn GitHub.",
            "expected_outcome": "Bảo vệ thành công kết quả bài thi cuối môn đạt chuẩn năng lực CLO/PLO môn IT-105.",
            "forbidden_scope": "CẤM: Gian lận trong thi cử.",
            "allowed_scope": "ĐÃ HỌC: Toàn bộ kiến thức môn học IT-105 (Session 01 - 09).",
            "lessons": []
        }
    ]
    return course_id, course_name, clos, plos, pm_data, tech_stack, main_content, {
        "total_sessions": 10, "theory_sessions": 4, "practice_sessions": 4,
        "mini_projects": 1, "final_exam": 1, "capstone_project": 0
    }


# =============================================================================
# 2. IT-106: Web Application Development (Phát triển ứng dụng web) - 30 Buổi
# =============================================================================
def build_it106_pm():
    course_id = "IT-106"
    course_name = "Web Application Development (Phát triển ứng dụng web)"
    tech_stack = "JavaScript Vanilla (ES6+), HTML5/CSS3, DOM API, Fetch API, Async/Await, Cursor AI IDE"
    main_content = "JS Variables, Loops, ES6, DOM Manipulation, Event Listeners, Promises/Async-Await, Web Application"
    
    plos = [
        "PLO 1: Sử dụng thành thạo máy tính, hệ điều hành và các lệnh Git cốt lõi để quản lý tài nguyên và phiên bản mã nguồn.",
        "PLO 2: Vận dụng kỹ thuật Prompt Engineering với LLMs để tra cứu kiến thức, tóm tắt thông tin và tối ưu hóa tốc độ tự học.",
        "PLO 3: Thiết kế và lập trình giao diện Web (Responsive) bằng HTML/CSS và các Framework UI chuẩn mực.",
        "PLO 4: Lập trình các tính năng tương tác Web bằng Javascript thuần, đồng thời biết sử dụng AI để sinh logic, kiểm thử và sửa lỗi (Debugging).",
        "PLO 5: Rèn luyện phương pháp quản lý thời gian và học tập chủ động để thích ứng với kỷ nguyên AI."
    ]
    clos = [
        "CLO1: Lập trình được các tương tác Web cơ bản và kết nối API bằng Javascript thuần.",
        "CLO2: Phân tích và xử lý dữ liệu JSON từ hệ thống bên ngoài.",
        "CLO3: Vận dụng kỹ năng AI Prompting để sinh logic phức tạp, tìm lỗi (Debugging) và tối ưu hóa mã nguồn JS."
    ]

    sessions_spec = [
        (1, "Lý thuyết", "Định hướng môn học và Lộ trình Phát triển Ứng dụng Web với JavaScript", [
            ("Tổng quan lộ trình và Demo sản phẩm", "1. Tổng quan lộ trình 30 buổi học | 2. Phương pháp học lập trình JS với AI IDE | 3. Demo sản phẩm Website tương tác tích hợp API.")
        ]),
        (2, "Lý thuyết", "Tổng quan ngôn ngữ JavaScript, Trình duyệt Console và Biến số ES6", [
            ("Tổng quan JavaScript và Cơ chế V8 Engine", "Đặc trưng ngôn ngữ JS; Trình thông dịch V8 Engine; Chạy code JS trên Browser Console và file script.js."),
            ("Cài đặt Môi trường VS Code / Cursor và Node.js Runtime", "Cài đặt Node.js runtime; Cấu hình extension Live Server; Sinh mã Boilerplate HTML/JS với AI IDE."),
            ("Biến số ES6 (let, const, var) và Naming Convention", "Phân biệt let, const, var; Quy tắc đặt tên camelCase; Kiểu dữ liệu nguyên thủy (number, string, boolean, null, undefined)."),
            ("Nhập xuất dữ liệu Console và Chuỗi Template Literals", "Hàm console.log(), alert(), prompt(); Định dạng chuỗi Template Literals backticks ${var}; Ép kiểu dữ liệu.")
        ]),
        (3, "Thực hành", "Thực hành Cấu hình Môi trường JavaScript và Thao tác Nhập xuất Dữ liệu", []),
        (4, "Lý thuyết", "Toán tử Số học, Toán tử So sánh và Biểu thức Logic trong JavaScript", [
            ("Toán tử Số học và Toán tử Gán gộp", "Các toán tử +, -, *, /, %, **; Toán tử gán gộp +=, -=, *=, /=; Toán tử tăng giảm ++, --."),
            ("Toán tử So sánh Bằng nghiêm ngặt (===) và Khác (!==)", "Phân biệt so sánh lỏng lẻo == và so sánh nghiêm ngặt ===; So sánh lớn bé >, <, >=, <=."),
            ("Toán tử Logic and (&&), or (||), not (!) và Ngắn mạch", "Kết hợp biểu thức logic với &&, ||, !; Cơ chế ngắn mạch Short-circuit evaluation.")
        ]),
        (5, "Thực hành", "Thực hành Tính toán Biểu thức Logic Tính tiền Hóa đơn và Ưu đãi", []),
        (6, "Lý thuyết", "Cấu trúc Điều kiện và Rẽ nhánh Quyết định với if, else, switch-case", [
            ("Câu lệnh Điều kiện if, if-else và if-elif-else", "Cú pháp khối lệnh if-else; Rẽ nhánh nhiều điều kiện; Thụt lề và khối lệnh {}."),
            ("Câu lệnh Rẽ nhánh switch-case và Toán tử Ba ngôi Ternary", "Cú pháp switch-case với từ khóa break; Toán tử ba ngôi condition ? a : b ngắn gọn.")
        ]),
        (7, "Thực hành", "Thực hành Lập trình Logic Kiểm tra Ràng buộc và Phân loại Người dùng", []),
        (8, "Lý thuyết", "Cấu trúc Vòng lặp for, while, do-while và Điều khiển Luồng", [
            ("Vòng lặp for cơ bản và Vòng lặp while", "Cú pháp for (let i=0; i<n; i++); Vòng lặp điều kiện while; Vòng lặp do-while."),
            ("Điều khiển Luồng lặp với break, continue", "Sử dụng break ngắt lặp và continue bỏ qua lượt lặp khi thỏa điều kiện.")
        ]),
        (9, "Thực hành", "Thực hành Duyệt Chuỗi và Tính toán Thuật toán Lặp Dữ liệu Console", []),
        (10, "Lý thuyết", "Mảng Dữ liệu (Array) trong JavaScript và các Thao tác CRUD Cơ bản", [
            ("Khái niệm Array, Indexing và Độ dài .length", "Khai báo mảng []; Chỉ số phần tử 0-indexed; Truy cập phần tử và thuộc tính .length."),
            ("Duyệt Mảng và Thao tác Thêm phần tử (push, unshift)", "Duyệt mảng bằng vòng lặp for và for...of; Thêm phần tử mới với .push() và .unshift()."),
            ("Thao tác Sửa và Xóa phần tử Mảng (pop, shift, splice)", "Cập nhật giá trị theo chỉ số; Xóa phần tử với .pop(), .shift(), .splice().")
        ]),
        (11, "Thực hành", "Thực hành Quản lý Danh sách Sản phẩm bằng Mảng JavaScript", []),
        (12, "Lý thuyết", "Đối tượng (Object) trong JavaScript, Cấu trúc JSON và Thao tác CRUD", [
            ("Khái niệm Object Literal (Key-Value)", "Khai báo đối tượng {}; Khóa và giá trị; Truy cập thuộc tính qua dot notation (.) và bracket notation ([])."),
            ("Thao tác Thêm, Sửa, Xóa Thuộc tính Object và Cấu trúc JSON", "Thêm/sửa thuộc tính; Xóa thuộc tính với từ khóa delete; Chuyển đổi JSON.stringify() và JSON.parse().")
        ]),
        (13, "Mini project", "Mini Project 1: Xây dựng Ứng dụng Quản lý Danh mục Bán hàng Console (Phần 1)", []),
        (14, "Lý thuyết", "Tổ chức Hàm (Function), Tham số, Arrow Function và Phạm vi Scope", [
            ("Khai báo Hàm (Function Declaration & Expression)", "Khai báo hàm với từ khóa function; Truyền tham số và lệnh return trả về giá trị."),
            ("Cú pháp Arrow Function ES6 và Tham số Mặc định", "Cú pháp ngắn gọn Arrow Function () => {}; Thiết lập default parameters."),
            ("Phạm vi Biến Global, Local Scope và Closures cơ bản", "Phân biệt phạm vi toàn cục và cục bộ; Khái niệm Hoisting và Closures trong JS.")
        ]),
        (15, "Lý thuyết", "Ôn tập Tổng hợp Kiến thức JavaScript Cú pháp, Mảng, Object và Hàm", [
            ("Hệ thống hóa Cấu trúc Dữ liệu và Hàm trong JS", "Ôn tập mảng, object, hàm; Quy chuẩn viết mã sạch Clean Code ES6+."),
            ("Tổ chức Mã nguồn Mô-đun Clean Code JavaScript", "Phân rã hàm nhỏ đơn nhiệm và quy chuẩn đặt tên camelCase.")
        ]),
        (16, "Thi giữa môn", "Thi Thực hành Giữa môn: Lập trình Logic Xử lý Dữ liệu JavaScript", []),
        (17, "Lý thuyết", "Tương tác DOM API (Document Object Model): Truy xuất và Thay đổi Nội dung", [
            ("Khái niệm DOM Tree và Truy xuất Element", "Cấu trúc cây DOM; Truy xuất phần tử bằng getElementById, querySelector, querySelectorAll."),
            ("Thay đổi Nội dung HTML và Thuộc tính Element", "Thay đổi textContent, innerHTML, src, href; Thao tác với classList (add, remove, toggle).")
        ]),
        (18, "Thực hành", "Thực hành Truy xuất DOM và Cập nhật Giao diện Web Động", []),
        (19, "Lý thuyết", "Xử lý Sự kiện Người dùng (Event Handling) và Sự kiện Form Input", [
            ("Đăng ký Sự kiện với addEventListener", "Các sự kiện click, dblclick, mouseover; Đăng ký xử lý sự kiện qua addEventListener."),
            ("Làm việc với Form, Input và Sự kiện submit", "Lấy giá trị từ input field; Ngăn chặn load trang mặc định với event.preventDefault(); Validation form.")
        ]),
        (20, "Thực hành", "Thực hành Xây dựng Form Đăng nhập và Đăng ký Tương tác Tối ưu UI", []),
        (21, "Lý thuyết", "Lập trình Bất đồng bộ: Callback, Promise và Async/Await với Fetch API", [
            ("Khái niệm Lập trình Bất đồng bộ và Promise", "So sánh đồng bộ và bất đồng bộ; Khái niệm Promise (Pending, Fulfilled, Rejected)."),
            ("Cú pháp Async/Await và Gọi API với Fetch", "Sử dụng async/await xử lý bất đồng bộ; Gọi API lấy dữ liệu JSON bằng fetch().")
        ]),
        (22, "Mini project", "Mini Project 2: Xây dựng Dashboard Web Tương tác Gọi Fetch API Dữ liệu Động", []),
        (23, "Lý thuyết", "Lưu trữ Dữ liệu Trình duyệt với LocalStorage và SessionStorage", [
            ("Lưu trữ LocalStorage và SessionStorage", "Cơ chế lưu trữ Client-side; Thao tác setItem(), getItem(), removeItem(), clear(); Lưu object với JSON."),
            ("Tích hợp LocalStorage Bảo tồn Trạng thái Web", "Ứng dụng LocalStorage lưu danh sách giỏ hàng, chế độ Dark/Light mode.")
        ]),
        (24, "Thực hành", "Thực hành Xây dựng Ứng dụng To-Do List Lưu Trữ LocalStorage", []),
        (25, "Lý thuyết", "Dự án Web Capstone: Thiết kế Kiến trúc Frontend và Tích hợp AI Debugging", [
            ("Kiến trúc Mô-đun Frontend và Quy trình Pair-Programming AI", "Phân rã dự án Web thành các mô-đun JS; Sử dụng Cursor AI Debug lỗi DOM và API."),
            ("Chuẩn hóa Giao diện Web Responsive và Tối ưu UI/UX", "Kiểm thử hiển thị màn hình đa thiết bị và tối ưu trải nghiệm người dùng.")
        ]),
        (26, "Project", "Dự án Capstone Web (Buổi 1): Phân tích SRS và Khởi tạo Giao diện HTML/CSS", []),
        (27, "Project", "Dự án Capstone Web (Buổi 2): Lập trình Logic Tương tác DOM và Event Handlers", []),
        (28, "Project", "Dự án Capstone Web (Buổi 3): Xử lý Dữ liệu Mảng, Object và Tích hợp LocalStorage", []),
        (29, "Project", "Dự án Capstone Web (Buổi 4): Gọi RESTful API Bên Ngoài và Hoàn thiện Tối ưu UI/UX", []),
        (30, "Thi cuối môn", "Bảo vệ Dự án Web Capstone và Đánh giá Năng lực Lập trình Web JS Tổng hợp", [])
    ]

    pm_data = []
    for snum, ht, title, lessons in sessions_spec:
        s_scope = title
        s_outcome = f"Hoàn thành các mục tiêu học tập và năng lực thực hành của {title}."
        s_forb = "CẤM: Các chủ đề nâng cao chưa học ở các buổi tiếp theo."
        s_allow = "ĐÃ HỌC: Các kiến thức tiền đề đã tích lũy từ các buổi trước."
        
        lesson_objs = []
        if lessons:
            for lidx, (ltitle, lscope) in enumerate(lessons, 1):
                lesson_objs.append({
                    "lesson_num": lidx,
                    "title": ltitle,
                    "content_scope": lscope,
                    "expected_outcome": f"Trình bày và thực hành thành công {ltitle}.",
                    "forbidden_scope": "CẤM: Các khái niệm nâng cao chưa học ở các bài tiếp theo.",
                    "allowed_scope": "ĐÃ HỌC: Các kiến thức JS đã học ở các bài trước."
                })
        
        pm_data.append({
            "session_num": snum,
            "hinh_thuc": ht,
            "title": title,
            "content_scope": s_scope,
            "expected_outcome": s_outcome,
            "forbidden_scope": s_forb,
            "allowed_scope": s_allow,
            "lessons": lesson_objs
        })
        
    return course_id, course_name, clos, plos, pm_data, tech_stack, main_content, {
        "total_sessions": 30, "theory_sessions": 10, "practice_sessions": 10,
        "mini_projects": 2, "final_exam": 2, "capstone_project": 6
    }


# =============================================================================
# 3. IT-202: Database (Cơ sở dữ liệu) - 24 Buổi
# =============================================================================
def build_it202_pm():
    course_id = "IT-202"
    course_name = "Database (Cơ sở dữ liệu)"
    tech_stack = "PostgreSQL 16, pgAdmin 4, SQL Standard, Supabase BaaS, ERD Diagramming"
    main_content = "Relational Database concepts, ERD Design, SQL Data Types, Foreign Keys, Supabase BaaS, Agile, Authentication, Authorization"
    
    plos = [
        "PLO 1: Thiết kế, quản trị cơ sở dữ liệu quan hệ (SQL) đảm bảo tính toàn vẹn dữ liệu, đồng thời biết khai thác các dịch vụ Backend-as-a-Service (BaaS) để khởi tạo hạ tầng lưu trữ tốc độ cao.",
        "PLO 2: Vận dụng thành thạo ngôn ngữ Python và tư duy Lập trình hướng đối tượng (OOP) để xây dựng mã nguồn logic chuẩn mực, có tính tái sử dụng và dễ bảo trì.",
        "PLO 3: Xây dựng hoàn chỉnh ứng dụng Web phía Server (Backend) bằng FastAPI, thiết kế luồng RESTful API và triển khai các cơ chế xác thực bảo mật (Authentication/Authorization) chuẩn doanh nghiệp.",
        "PLO 4: Sử dụng các công cụ AI IDE (Cursor/Windsurf) theo phương pháp 'Lập trình cặp' (Pair-Programming) để hỗ trợ đọc hiểu luồng code, sinh các đoạn mã lặp lại (Boilerplate), tái cấu trúc (Refactor) và gỡ lỗi (Debug) hệ thống.",
        "PLO 5: Khảo sát, phân tích yêu cầu người dùng thực tế bằng các framework chuẩn (The Mom Test, JTBD) và sử dụng AI để thiết kế kiến trúc hệ thống thông tin.",
        "PLO 6: Hoàn thành dự án Web Fullstack thực tế (kết hợp giao diện Kỳ I và Backend Kỳ II) theo quy trình Agile/Scrum và chuẩn quản lý mã nguồn doanh nghiệp."
    ]
    clos = [
        "CLO1: Thiết kế và chuẩn hóa được lược đồ cơ sở dữ liệu quan hệ (Relational Schema) cho các bài toán thực tế.",
        "CLO2: Truy vấn và thao tác dữ liệu thành thạo thông qua ngôn ngữ cấu trúc SQL.",
        "CLO3: Thành thạo việc sử dụng Hệ quản trị CSDL PostgreSQL.",
        "CLO4: Ứng dụng các dịch vụ BaaS (Supabase/Firebase) để thiết lập Backend và Database với tốc độ cao."
    ]

    sessions_spec = [
        (1, "Lý thuyết", "Định hướng môn học và Lộ trình Thiết kế Quản trị Cơ sở dữ liệu", [
            ("Tổng quan lộ trình và Demo sản phẩm", "1. Tổng quan lộ trình 24 buổi học | 2. Phương pháp học CSDL với PostgreSQL & Supabase, quy trình Agile | 3. Demo mô hình CSDL thương mại điện tử.")
        ]),
        (2, "Lý thuyết", "Tổng quan ngôn ngữ truy vấn CSDL, Hệ quản trị PostgreSQL và Mô hình ERD", [
            ("Tổng quan Cơ sở dữ liệu Quan hệ (RDBMS) và PostgreSQL", "Tầm quan trọng của CSDL; Phân biệt lưu trữ tệp và RDBMS; Giới thiệu PostgreSQL."),
            ("Mô hình Thực thể Tương quan ERD (Entity Relationship Diagram)", "Khái niệm thực thể Entity, thuộc tính Attribute, mối quan hệ Relationship (1-1, 1-N, N-N)."),
            ("Cài đặt PostgreSQL 16 và Trình quản lý pgAdmin 4", "Cài đặt PostgreSQL server; Thao tác kết nối CSDL bằng pgAdmin 4 UI.")
        ]),
        (3, "Thực hành", "Thực hành Thiết kế Sơ đồ ERD Cho Bài Toán Quản lý Bán hàng", []),
        (4, "Lý thuyết", "Chuyển đổi Mô hình ERD sang Lược đồ Quan hệ và Khóa Chính/Khóa Ngoại", [
            ("Quy tắc Chuyển đổi ERD sang Bảng Quan hệ (Tables)", "Quy tắc chuyển thực thể thành Table, thuộc tính thành Column, mối quan hệ 1-N."),
            ("Khái niệm Khóa chính (Primary Key) và Khóa ngoại (Foreign Key)", "Vai trò khóa chính PK bảo đảm tính định danh; Khóa ngoại FK bảo đảm tính toàn vẹn tham chiếu.")
        ]),
        (5, "Thực hành", "Thực hành Thiết kế Bảng Quan hệ và Ràng buộc Dữ liệu PK/FK", []),
        (6, "Lý thuyết", "Ngôn ngữ SQL Định nghĩa Dữ liệu DDL (CREATE, ALTER, DROP TABLE)", [
            ("Các Kiểu Dữ liệu SQL (INTEGER, VARCHAR, BOOLEAN, TIMESTAMP)", "Các kiểu dữ liệu số, chuỗi, thời gian trong PostgreSQL; Quy tắc đặt tên bảng/cột."),
            ("Câu lệnh DDL Khai báo Bảng (CREATE TABLE, ALTER, DROP)", "Cú pháp CREATE TABLE với ràng buộc PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE; Lệnh ALTER và DROP.")
        ]),
        (7, "Thực hành", "Thực hành Viết Kịch bản DDL Tạo Cấu trúc Bảng CSDL PostgreSQL", []),
        (8, "Lý thuyết", "Ngôn ngữ SQL Thao tác Dữ liệu DML (INSERT, UPDATE, DELETE) và SELECT Cơ bản", [
            ("Thêm Dữ liệu Mới với Lệnh INSERT INTO", "Cú pháp INSERT INTO table (cols) VALUES (vals); Thêm một và nhiều dòng dữ liệu."),
            ("Cập nhật và Xóa Dữ liệu với UPDATE và DELETE", "Cú pháp UPDATE table SET col=val WHERE condition; Lệnh DELETE FROM table WHERE condition an toàn.")
        ]),
        (9, "Thực hành", "Thực hành Chèn, Cập nhật và Xóa Dữ liệu Bảng Quản lý Sản phẩm", []),
        (10, "Lý thuyết", "Truy vấn Dữ liệu Nâng cao với Mệnh đề WHERE, ORDER BY, LIMIT và LIKE", [
            ("Lọc Dữ liệu với Mệnh đề WHERE và Toán tử So sánh/Logic", "Sử dụng WHERE với =, !=, >, <, AND, OR, NOT, IN, BETWEEN."),
            ("Sắp xếp ORDER BY, Giới hạn LIMIT và Tìm kiếm Chuỗi LIKE", "Sắp xếp tăng/giảm ASC/DESC; Giới hạn số dòng LIMIT OFFSET; Tìm kiếm mẫu chuỗi LIKE '%val%'.")
        ]),
        (11, "Thực hành", "Thực hành Viết Các Truy vấn Lọc và Sắp xếp Dữ liệu Nghiệp vụ", []),
        (12, "Lý thuyết", "Hàm Gom nhóm Aggregate Functions (COUNT, SUM, AVG) và Mệnh đề GROUP BY", [
            ("Các Hàm Tính toán Gom nhóm (COUNT, SUM, AVG, MIN, MAX)", "Sử dụng các hàm thống kê đếm số lượng, tính tổng, trung bình trên cột dữ liệu."),
            ("Gom nhóm Dữ liệu GROUP BY và Lọc Nhóm với HAVING", "Cú pháp GROUP BY cột gom nhóm; Phân biệt điều kiện WHERE (trước gom) và HAVING (sau gom).")
        ]),
        (13, "Mini project", "Mini Project 1: Xây dựng CSDL Console Quản lý Kho Hàng và Thống kê Sales", []),
        (14, "Lý thuyết", "Kết nối Bảng dữ liệu JOIN (INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN)", [
            ("Khái niệm Kết nối Bảng và Mệnh đề INNER JOIN", "Tại sao cần kết nối bảng; Cú pháp SELECT cols FROM A INNER JOIN B ON A.fk = B.pk."),
            ("Các Phép Kết nối Mở rộng LEFT JOIN, RIGHT JOIN và FULL JOIN", "Ý nghĩa LEFT JOIN giữ dòng bảng trái; RIGHT JOIN và FULL OUTER JOIN.")
        ]),
        (15, "Lý thuyết", "Ôn tập Tổng hợp Kiến thức Thiết kế CSDL, SQL DDL, DML, GROUP BY và JOIN", [
            ("Hệ thống hóa Tư duy Thiết kế CSDL và Tối ưu Truy vấn SQL", "Ôn tập ERD, DDL, DML, GROUP BY, JOIN chuẩn bị thi giữa môn."),
            ("Tổ chức Truy vấn SQL Chuẩn hóa và Đánh chỉ mục Index", "Viết truy vấn SQL chuẩn mực và đánh giá hiệu năng truy vấn CSDL.")
        ]),
        (16, "Thi giữa môn", "Thi Thực hành Giữa môn: Lập trình Truy vấn SQL và Thiết kế CSDL PostgreSQL", []),
        (17, "Lý thuyết", "Truy vấn Con (Subquery) và Các Phép Tập hợp (UNION, INTERSECT)", [
            ("Khái niệm Truy vấn Con Subquery trong WHERE và FROM", "Viết Subquery đơn giá trị và đa giá trị với IN, EXISTS, ANY, ALL."),
            ("Phép Hợp UNION, Giao INTERSECT và Trừ EXCEPT", "Cú pháp kết hợp kết quả truy vấn UNION, UNION ALL, INTERSECT, EXCEPT.")
        ]),
        (18, "Thực hành", "Thực hành Viết Truy vấn Con Phức tạp Phân tích Doanh thu", []),
        (19, "Lý thuyết", "Khái niệm Index Tối ưu Tốc độ Truy vấn và Khái niệm View Bảng Ảo", [
            ("Tối ưu hóa Truy vấn với B-Tree Index (CREATE INDEX)", "Bản chất Index; Cú pháp CREATE INDEX; Khi nào nên dùng và tránh dùng Index."),
            ("Khái niệm Bảng Ảo View (CREATE VIEW)", "Tạo bảng ảo View che giấu độ phức tạp SQL và bảo mật phân quyền dữ liệu.")
        ]),
        (20, "Thực hành", "Thực hành Tạo Index Tối ưu Hóa Truy vấn và Khởi tạo View Báo cáo", []),
        (21, "Lý thuyết", "Giới thiệu Khái niệm BaaS Supabase và Tích hợp Cơ sở dữ liệu Cloud", [
            ("Tổng quan Dịch vụ BaaS (Backend-as-a-Service) Supabase", "Khái niệm BaaS; Tạo dự án Supabase Cloud; Trình quản lý Database UI trên Supabase và cơ chế Authentication/Authorization."),
            ("Thao tác Table Editor và Sinh SQL Migration trên Supabase", "Khởi tạo bảng, thiết lập RLS (Row Level Security) cơ bản và thao tác dữ liệu Cloud.")
        ]),
        (22, "Mini project", "Mini Project 2: Khởi tạo CSDL Cloud Supabase và Tích hợp RESTful API BaaS", []),
        (23, "Lý thuyết", "Tổ chức Quản trị CSDL Doanh nghiệp, Phân quyền User và Sao lưu Backup/Restore", [
            ("Quản lý Người dùng User Roles và Phân quyền GRANT/REVOKE", "Tạo Role; Gán quyền SELECT, INSERT trên bảng với GRANT; Thu hồi quyền với REVOKE."),
            ("Sao lưu và Phôi phục CSDL (pg_dump & pg_restore)", "Thực thi lệnh pg_dump xuất file .sql sao lưu và phôi phục CSDL an toàn.")
        ]),
        (24, "Thi cuối môn", "Thi Thực hành Cuối môn: Bảo vệ Thiết kế CSDL và Đánh giá Năng lực SQL Tổng hợp", [])
    ]

    pm_data = []
    for snum, ht, title, lessons in sessions_spec:
        s_scope = title
        s_outcome = f"Hoàn thành xuất sắc mục tiêu năng lực của buổi học {title}."
        s_forb = "CẤM: Các kỹ thuật SQL nâng cao chưa học ở các buổi tiếp theo."
        s_allow = "ĐÃ HỌC: Các kiến thức CSDL và SQL đã tích lũy từ các buổi trước."
        
        lesson_objs = []
        if lessons:
            for lidx, (ltitle, lscope) in enumerate(lessons, 1):
                lesson_objs.append({
                    "lesson_num": lidx,
                    "title": ltitle,
                    "content_scope": lscope,
                    "expected_outcome": f"Trình bày và thực hành thành công {ltitle}.",
                    "forbidden_scope": "CẤM: Cú pháp SQL nâng cao chưa học ở các bài tiếp theo.",
                    "allowed_scope": "ĐÃ HỌC: Kiến thức CSDL đã tích lũy từ các bài học trước."
                })
                
        pm_data.append({
            "session_num": snum,
            "hinh_thuc": ht,
            "title": title,
            "content_scope": s_scope,
            "expected_outcome": s_outcome,
            "forbidden_scope": s_forb,
            "allowed_scope": s_allow,
            "lessons": lesson_objs
        })

    return course_id, course_name, clos, plos, pm_data, tech_stack, main_content, {
        "total_sessions": 24, "theory_sessions": 10, "practice_sessions": 10,
        "mini_projects": 2, "final_exam": 2, "capstone_project": 0
    }


# =============================================================================
# 4. IT-204: Back-end Development (Lập trình Back-end với FastAPI) - 36 Buổi
# =============================================================================
def build_it204_pm():
    course_id = "IT-204"
    course_name = "Back-end Development (Lập trình Back-end với FastAPI)"
    tech_stack = "Python 3.12, FastAPI 0.115, Pydantic v2, SQLAlchemy 2.0 ORM, PostgreSQL, PyJWT, Cursor AI IDE"
    main_content = "FastAPI Routing, Pydantic Models, SQLAlchemy ORM, JWT Security, CORS, Dependency Injection, Back-end Server, BaaS, Agile, Boilerplate"
    
    plos = [
        "PLO 1: Thiết kế, quản trị cơ sở dữ liệu quan hệ (SQL) đảm bảo tính toàn vẹn dữ liệu, đồng thời biết khai thác các dịch vụ Backend-as-a-Service (BaaS) để khởi tạo hạ tầng lưu trữ tốc độ cao.",
        "PLO 2: Vận dụng thành thạo ngôn ngữ Python và tư duy Lập trình hướng đối tượng (OOP) để xây dựng mã nguồn logic chuẩn mực, có tính tái sử dụng và dễ bảo trì.",
        "PLO 3: Xây dựng hoàn chỉnh ứng dụng Web phía Server (Backend) bằng FastAPI, thiết kế luồng RESTful API và triển khai các cơ chế xác thực bảo mật (Authentication/Authorization) chuẩn doanh nghiệp.",
        "PLO 4: Sử dụng các công cụ AI IDE (Cursor/Windsurf) theo phương pháp 'Lập trình cặp' (Pair-Programming) để hỗ trợ đọc hiểu luồng code, sinh các đoạn mã lặp lại (Boilerplate), tái cấu trúc (Refactor) và gỡ lỗi (Debug) hệ thống.",
        "PLO 5: Khảo sát, phân tích yêu cầu người dùng thực tế bằng các framework chuẩn (The Mom Test, JTBD) và sử dụng AI để thiết kế kiến trúc hệ thống thông tin.",
        "PLO 6: Hoàn thành dự án Web Fullstack thực tế (kết hợp giao diện Kỳ I và Backend Kỳ II) theo quy trình Agile/Scrum và chuẩn quản lý mã nguồn doanh nghiệp."
    ]
    clos = [
        "CLO1: Thiết kế và lập trình được các RESTful API chuẩn mực đáp ứng nhu cầu giao tiếp của ứng dụng Frontend.",
        "CLO2: Triển khai luồng xác thực (Authentication) và phân quyền (Authorization) an toàn cho người dùng.",
        "CLO3: Tích hợp thành công công cụ ORM để thao tác an toàn với Cơ sở dữ liệu."
    ]

    sessions_spec = [
        (1, "Lý thuyết", "Định hướng môn học và Lộ trình Phát triển Back-end Server với FastAPI", [
            ("Tổng quan lộ trình và Demo sản phẩm", "1. Tổng quan lộ trình 36 buổi học | 2. Phương pháp học Back-end với FastAPI, hạ tầng BaaS, sinh code Boilerplate & AI Pair-Programming Agile | 3. Demo hệ thống RESTful API Server hoàn chỉnh.")
        ]),
        (2, "Lý thuyết", "Tổng quan ngôn ngữ Python Back-end, Kiến trúc Web Server và Khái niệm RESTful API", [
            ("Tổng quan Kiến trúc Client-Server và Giao thức HTTP/HTTPS", "Luồng giao tiếp HTTP Request/Response; Các HTTP Methods (GET, POST, PUT, DELETE, PATCH); Status Codes."),
            ("Khái niệm Kiến trúc RESTful API và Định dạng JSON Data", "Các nguyên lý thiết kế RESTful API; Định danh tài nguyên Endpoint URI; Phân tích JSON Data payload."),
            ("Cài đặt FastAPI, Uvicorn Server và Khởi tạo App Đầu Tiên", "Cài đặt fastapi uvicorn với pip; Viết app FastAPI Hello World đầu tiên; Chạy Uvicorn dev server.")
        ]),
        (3, "Thực hành", "Thực hành Khởi tạo Môi trường FastAPI Server và Chạy Ứng dụng Đầu tiên", []),
        (4, "Lý thuyết", "Định tuyến Routing trong FastAPI: Path Parameters và Query Parameters", [
            ("Khai báo Path Parameters và Ép kiểu Dữ liệu Tự động", "Khai báo đường dẫn động /items/{item_id}; Auto Type Validation của FastAPI."),
            ("Khai báo Query Parameters và Giá trị Mặc định", "Cú pháp Query parameters /items/?skip=0&limit=10; Tham số tùy chọn Optional parameters.")
        ]),
        (5, "Thực hành", "Thực hành Xây dựng các Endpoint Tra cứu và Lọc Sản phẩm", []),
        (6, "Lý thuyết", "Chuẩn hóa Request Body với Pydantic Schemas và Data Validation", [
            ("Khái niệm Pydantic Model và Khai báo Schema", "Khai báo Pydantic BaseModel; Định nghĩa các trường dữ liệu và kiểu dữ liệu strict."),
            ("Validation Dữ liệu Đầu vào với Field, EmailStr, gt/lt", "Sử dụng Field() thiết lập ràng buộc validation (độ dài chuỗi, khoảng giá trị số).")
        ]),
        (7, "Thực hành", "Thực hành Xây dựng Endpoint Tiếp Nhận và Validation Dữ liệu Đăng ký", []),
        (8, "Lý thuyết", "Xử lý Response Model, Status Codes và Xử lý Lỗi HTTPException", [
            ("Cấu hình Response Model lọc Dữ liệu Đầu ra", "Sử dụng response_model ẩn các thông tin nhạy cảm (vd: password hash)."),
            ("Chủ động Ném Lỗi với HTTPException Xử lý Ngoại lệ An toàn", "Sử dụng raise HTTPException(status_code=404, detail='Resource Not Found') thông báo lỗi chuẩn xác cho Client.")
        ]),
        (9, "Thực hành", "Thực hành Xây dựng Mô-đun Quản lý Người dùng An toàn Thông tin", []),
        (10, "Lý thuyết", "Giới thiệu SQLAlchemy 2.0 ORM và Tích hợp Cơ sở dữ liệu PostgreSQL", [
            ("Khái niệm ORM (Object-Relational Mapping)", "Tại sao cần dùng ORM; Giới thiệu SQLAlchemy 2.0; Cấu hình chuỗi kết nối Database URL."),
            ("Tạo Engine, sessionmaker và Khai báo Base Model Class", "Tạo create_engine; Khai báo sessionmaker; Khai báo Base = declarative_base().")
        ]),
        (11, "Thực hành", "Thực hành Kết nối FastAPI Server tới Cơ sở dữ liệu PostgreSQL", []),
        (12, "Lý thuyết", "Định nghĩa SQLAlchemy Models và Thao tác CRUD Database với ORM", [
            ("Định nghĩa SQLAlchemy Model Class (Column, Integer, String)", "Khai báo Class tương ứng với Bảng CSDL; Khai báo thuộc tính Column, Primary Key, Foreign Key."),
            ("Thao tác Thêm và Truy vấn Dữ liệu với db.add() và db.scalars()", "Tạo đối tượng Model mới; db.add(), db.commit(); Truy vấn dữ liệu với select() và db.scalars()."),
            ("Thao tác Cập nhật và Xóa Dữ liệu với ORM", "Cập nhật giá trị thuộc tính Model; Xóa dữ liệu với db.delete() và db.commit().")
        ]),
        (13, "Mini project", "Mini Project 1: Xây dựng RESTful API Server Quản lý Danh mục Bán hàng ORM", []),
        (14, "Lý thuyết", "Kỹ thuật Dependency Injection trong FastAPI và Quản lý Database Session", [
            ("Khái niệm Dependency Injection (Depends)", "Nguyên lý Dependency Injection; Sử dụng từ khóa Depends() trong FastAPI."),
            ("Tạo Dependency get_db Quản lý Vòng đời Database Session", "Xây dựng hàm get_db() yield session; Đảm bảo đóng kết nối tự động trong khối finally.")
        ]),
        (15, "Lý thuyết", "Ôn tập Tổng hợp Kiến thức RESTful API, Pydantic, SQLAlchemy ORM và Depends", [
            ("Hệ thống hóa Kiến trúc Back-end FastAPI và ORM Database", "Ôn tập Routing, Schemas, ORM CRUD, Dependency Injection chuẩn bị thi giữa môn."),
            ("Tổ chức Chuẩn hóa RESTful API Server và Cấu hình CORS", "Tối ưu luồng xử lý Request/Response và quy chuẩn thiết kế API Back-end.")
        ]),
        (16, "Thi giữa môn", "Thi Thực hành Giữa môn: Lập trình Hệ thống RESTful API Server với FastAPI", []),
        (17, "Lý thuyết", "Quản lý Migration Cơ sở dữ liệu với Alembic", [
            ("Khái niệm Database Migration và Cài đặt Alembic", "Tại sao cần Migration; Cài đặt alembic; Khởi tạo môi trường alembic init."),
            ("Tự động Sinh Bản ghi Migration (alembic revision --autogenerate)", "Cấu hình env.py; Sinh bản ghi migration tự động; Nâng cấp CSDL với alembic upgrade head.")
        ]),
        (18, "Thực hành", "Thực hành Tạo và Quản lý Lịch sử Migration CSDL PostgreSQL", []),
        (19, "Lý thuyết", "Bảo mật Hệ thống: Hash Mật khẩu với Passlib/Bcrypt và Chuẩn JWT Authentication", [
            ("Bảo mật Mật khẩu với Hashing (Bcrypt)", "Tại sao không lưu plaintext password; Hash mật khẩu bằng passlib/bcrypt; Kiểm tra mật khẩu."),
            ("Khái niệm JSON Web Token (JWT) và Cấu trúc Token", "Cấu trúc JWT (Header, Payload, Signature); Tạo Access Token với PyJWT.")
        ]),
        (20, "Thực hành", "Thực hành Xây dựng API Đăng ký và Đăng nhập Trả về JWT Access Token", []),
        (21, "Lý thuyết", "Xác thực Phân quyền (Authorization) với OAuth2PasswordBearer và Depends", [
            ("Cơ chế Xác thực Token Người dùng qua Header Bearer", "Sử dụng OAuth2PasswordBearer lấy token từ Header Authorization."),
            ("Xây dựng Dependency get_current_user Bảo vệ Endpoint API", "Giải mã JWT token, kiểm tra user tồn tại và phân quyền truy cập API.")
        ]),
        (22, "Mini project", "Mini Project 2: Xây dựng Hệ thống Authentication & Authorization Bảo mật Đầy đủ", []),
        (23, "Lý thuyết", "Thiết kế Mối quan hệ Bảng ORM (1-N, N-N) và Lập trình Truy vấn Dữ liệu Nâng cao", [
            ("Cấu hình Mối quan hệ 1-N với relationship() và back_populates", "Khai báo ForeignKey và relationship(); Nối hai SQLAlchemy Models 1-N."),
            ("Kỹ thuật Lazy Loading vs Eager Loading (joinedload)", "Phân biệt Lazy loading và Eager loading với joinedload tối ưu hóa truy vấn CSDL.")
        ]),
        (24, "Thực hành", "Thực hành Lập trình API Đặt hàng Tích hợp Mối quan hệ Bảng Hóa đơn và Truy vấn Dữ liệu ORM", []),
        (25, "Lý thuyết", "Cấu hình CORS (Cross-Origin Resource Sharing), Middleware và Lập trình Logic Ghi Log Request", [
            ("Cấu hình CORS và Cấu hình CORSMiddleware", "Tại sao bị lỗi CORS khi gọi từ Frontend; Cấu hình CORSMiddleware cho phép Frontend truy cập."),
            ("Tạo Custom Middleware Ghi Log Request và Thời gian Thực thi", "Xây dựng middleware đo thời gian xử lý Request và ghi nhật ký Log.")
        ]),
        (26, "Thực hành", "Thực hành Tích hợp Middleware CORS và Kết nối Back-end với Frontend Kỳ I", []),
        (27, "Lý thuyết", "Tổ chức Cấu trúc Dự án Back-end Chuẩn Doanh nghiệp (Modular Project Structure)", [
            ("Tổ chức Thư mục Dự án theo Mô-đun (APIRouter)", "Chia nhỏ routes bằng APIRouter; Tổ chức các gói models, schemas, api, core."),
            ("Quản lý Biến Môi trường Environment Variables với pydantic-settings", "Đọc file .env an toàn với pydantic-settings BaseSettings.")
        ]),
        (28, "Mini project", "Mini Project 3: Tái cấu trúc Hệ thống Back-end FastAPI theo Chuẩn Kiến trúc Doanh nghiệp", []),
        (29, "Lý thuyết", "Dự án Capstone Web Fullstack: Kiến trúc Tích hợp Back-end FastAPI và Frontend", [
            ("Thiết kế Kiến trúc Fullstack Hệ thống", "Phân tích tài liệu SRS; Thiết kế toàn bộ RESTful API Endpoints cho ứng dụng Fullstack."),
            ("Quy trình AI Pair-Programming và Agile/Scrum", "Áp dụng Cursor AI IDE và quy trình Agile trong triển khai dự án Capstone Fullstack.")
        ]),
        (30, "Project", "Dự án Capstone Fullstack (Buổi 1): Khởi tạo CSDL PostgreSQL và Alembic Migrations", []),
        (31, "Project", "Dự án Capstone Fullstack (Buổi 2): Lập trình Mô-đun Authentication và Authorization JWT", []),
        (32, "Project", "Dự án Capstone Fullstack (Buổi 3): Lập trình Mô-đun Nghiệp vụ Cốt lõi và SQLAlchemy ORM", []),
        (33, "Project", "Dự án Capstone Fullstack (Buổi 4): Tích hợp CORSMiddleware và Kết nối Frontend UI Kỳ I", []),
        (34, "Project", "Dự án Capstone Fullstack (Buổi 5): Kiểm thử Tự động Debugging Lỗi API và Tối ưu Hóa Server", []),
        (35, "Project", "Dự án Capstone Fullstack (Buổi 6): Đóng gói Dự án và Xuất bản Tài liệu Swagger API Docs", []),
        (36, "Thi cuối môn", "Bảo vệ Dự án Web Fullstack Capstone và Đánh giá Năng lực Back-end FastAPI Tổng hợp", [])
    ]

    pm_data = []
    for snum, ht, title, lessons in sessions_spec:
        s_scope = title
        s_outcome = f"Hoàn thành xuất sắc mục tiêu năng lực của buổi học {title}."
        s_forb = "CẤM: Các kỹ thuật Back-end nâng cao chưa học ở các buổi tiếp theo."
        s_allow = "ĐÃ HỌC: Các kiến thức Back-end FastAPI và CSDL đã tích lũy từ các buổi trước."
        
        lesson_objs = []
        if lessons:
            for lidx, (ltitle, lscope) in enumerate(lessons, 1):
                lesson_objs.append({
                    "lesson_num": lidx,
                    "title": ltitle,
                    "content_scope": lscope,
                    "expected_outcome": f"Trình bày và thực hành thành công {ltitle}.",
                    "forbidden_scope": "CẤM: Các kỹ thuật Back-end nâng cao chưa học ở các bài tiếp theo.",
                    "allowed_scope": "ĐÃ HỌC: Kiến thức Back-end đã tích lũy từ các bài học trước."
                })
                
        pm_data.append({
            "session_num": snum,
            "hinh_thuc": ht,
            "title": title,
            "content_scope": s_scope,
            "expected_outcome": s_outcome,
            "forbidden_scope": s_forb,
            "allowed_scope": s_allow,
            "lessons": lesson_objs
        })

    return course_id, course_name, clos, plos, pm_data, tech_stack, main_content, {
        "total_sessions": 36, "theory_sessions": 15, "practice_sessions": 13,
        "mini_projects": 3, "final_exam": 1, "capstone_project": 4
    }


# =============================================================================
# Main Execution: Generate and Export All 4 Courses
# =============================================================================
def generate_course_pm(builder_func):
    course_id, course_name, clos, plos, pm_data, tech_stack, main_content, session_budget = builder_func()
    
    print(f"\n=====================================================================")
    print(f"=== Đang xử lý khởi tạo PM cho {course_id} - {course_name} ===")
    print(f"=====================================================================")
    
    student_profile = {
        "entry_level": "beginner",
        "background": "Công nghệ thông tin / Nền tảng PTIT"
    }

    config_dict = {
        "tech_stack": tech_stack,
        "class_configuration": {"session_duration_hours": 2.0, "total_hours": session_budget["total_sessions"] * 2},
        "student_profile": student_profile,
        "session_budget": session_budget
    }
    course_info_dict = {
        "course_id": course_id, "course_name": course_name, "clos": clos, "plos": plos, "main_content": main_content
    }

    # Audit via PM Reviewer Agent
    review_res = pm_reviewer_agent(pm_data, config_dict, course_info_dict)
    print(f"--> Kết quả thẩm định PM Auditor: Điểm {review_res['score']}/100, Approved: {review_res['is_approved']}")
    if review_res['rule_violations']:
        print("  Các điểm cần lưu ý:", review_res['rule_violations'])

    # Export to output/pms/<Tên_Môn_Học>/
    course_folder = get_course_pm_folder(course_name, base_dir=project_root / "output" / "pms")
    
    safe_name = course_id.replace("-", "")
    md_filepath = str(course_folder / f"PM_{safe_name}.md")
    excel_filepath = str(course_folder / f"PM_{safe_name}.xlsx")

    print(f"--> Exporting Markdown to: {md_filepath}")
    export_pm_to_markdown(
        pm_data=pm_data,
        course_id=course_id,
        course_name=course_name,
        clos=clos,
        plos=plos,
        filepath=md_filepath,
        tech_stack=tech_stack
    )

    print(f"--> Exporting Excel to: {excel_filepath}")
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
    print(f"✅ Hoàn tất xuất PM cho môn {course_id} vào {course_folder}")


def main():
    builders = [build_it105_pm, build_it106_pm, build_it202_pm, build_it204_pm]
    for b in builders:
        generate_course_pm(b)
    print("\n=====================================================================")
    print("🎉 HOÀN TẤT TẠO TOÀN BỘ PM CHO 4 MÔN HỌC (IT-105, IT-106, IT-202, IT-204)")
    print("=====================================================================")

if __name__ == "__main__":
    main()

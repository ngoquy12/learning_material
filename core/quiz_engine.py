import random
import re
import json
from typing import List, Dict, Any

# Topic metadata containing terms, actions, and configs
FASTAPI_TOPIC_DETAILS = {
    "orientation": {
        "name": "Định hướng học tập",
        "terms": ["Thiết kế ngược (Backward Design)", "Học tập chủ động (Active Learning)", "Dự án cuối môn", "Bài thực hành Lab"],
        "correct_syntax": "thiết kế ngược từ dự án thực tế",
        "wrong_1": "học lý thuyết suông trước",
        "wrong_2": "bỏ qua các bài thực hành Lab",
        "wrong_3": "chỉ học cú pháp cơ bản",
        "action": "bắt đầu môn học và định hình lộ trình",
        "error": "mơ hồ về sản phẩm cuối khóa",
        "solution": "áp dụng Thiết kế ngược (Backward Design)"
    },
    "intro": {
        "name": "FastAPI & ASGI",
        "terms": ["ASGI server", "FastAPI app", "Uvicorn running", "Async / Await", "Swagger UI docs"],
        "correct_syntax": "async def read_root()",
        "wrong_1": "def sync_read_root()",
        "wrong_2": "lambda read_root()",
        "wrong_3": "async class ReadRoot()",
        "action": "khởi tạo máy chủ ASGI và xử lý request",
        "error": "chặn Event Loop (I/O blocking)",
        "solution": "sử dụng async/await và ASGI server"
    },
    "validation": {
        "name": "Pydantic Validation",
        "terms": ["Pydantic BaseModel", "Field Validation", "Query Parameters", "Path Parameters", "Request Body"],
        "correct_syntax": "class Item(BaseModel): name: str",
        "wrong_1": "class Item(): name: str",
        "wrong_2": "class Item(dict): name: str",
        "wrong_3": "def Item(name: str)",
        "action": "kiểm tra tính hợp lệ của dữ liệu đầu vào",
        "error": "lỗi định dạng dữ liệu (ValidationError)",
        "solution": "khai báo Pydantic schemas kế thừa BaseModel"
    },
    "crud": {
        "name": "CRUD Operations",
        "terms": ["HTTP GET / POST / PUT", "Status Codes", "Response Model", "Path Parameters", "Query Filter"],
        "correct_syntax": "@app.post('/items', response_model=Item)",
        "wrong_1": "@app.route('/items', methods=['POST'])",
        "wrong_2": "@app.post('/items', schema=Item)",
        "wrong_3": "@app.send('/items', response=Item)",
        "action": "thực hiện các thao tác thêm, đọc, sửa, xóa dữ liệu",
        "error": "lỗi mã trạng thái (HTTP 500 Internal Server Error)",
        "solution": "sử dụng các HTTP methods tương ứng kết hợp Status Codes chuẩn"
    },
    "database": {
        "name": "SQLAlchemy ORM & Database",
        "terms": ["SQLAlchemy SessionLocal", "Declarative Base", "Database Engine", "Alembic migrations", "DB Connection Pool"],
        "correct_syntax": "db = SessionLocal(); try: yield db; finally: db.close()",
        "wrong_1": "db = SessionLocal(); return db",
        "wrong_2": "db = engine.connect(); yield db",
        "wrong_3": "db = Session(); yield db; db.commit()",
        "action": "truy vấn cơ sở dữ liệu quan hệ PostgreSQL / MySQL / SQLite",
        "error": "rò rỉ kết nối cơ sở dữ liệu (connection leak)",
        "solution": "sử dụng dependency injection yield db để tự động đóng connection"
    },
    "structure": {
        "name": "FastAPI Router & Structure",
        "terms": ["APIRouter instances", "Project Layout", "Dependency Injection (Depends)", "Sub-modules routing", "Common dependencies"],
        "correct_syntax": "router = APIRouter(prefix='/users', tags=['users'])",
        "wrong_1": "router = app.router(prefix='/users')",
        "wrong_2": "router = RouterClass('/users')",
        "wrong_3": "router = APIRouter.create('/users')",
        "action": "chia tách module và quản lý routing dự án lớn",
        "error": "trùng lặp tiền tố đường dẫn (duplicate route prefix)",
        "solution": "tách biệt các endpoint bằng APIRouter và nạp vào app chính"
    },
    "relationship": {
        "name": "SQLAlchemy Relationships",
        "terms": ["ForeignKey constraint", "relationship() helper", "lazy loading / join", "Back_populates", "Many-to-Many link table"],
        "correct_syntax": "owner = relationship('User', back_populates='items')",
        "wrong_1": "owner = ForeignKey('User')",
        "wrong_2": "owner = relationship('User', join='items')",
        "wrong_3": "owner = relationship('User', key='items')",
        "action": "thiết lập liên kết giữa các bảng trong ORM",
        "error": "lỗi tải chậm truy vấn (N+1 queries problem)",
        "solution": "sử dụng relationship() kết hợp lazy='joined' hoặc lazy='subquery'"
    },
    "security": {
        "name": "Security & JWT Auth",
        "terms": ["JWT token encoding", "OAuth2PasswordBearer", "bcrypt hashing", "Token expiration", "Role-based Access Control"],
        "correct_syntax": "pwd_context.hash(password)",
        "wrong_1": "hashlib.md5(password)",
        "wrong_2": "base64.encode(password)",
        "wrong_3": "pwd_context.verify(password)",
        "action": "mã hóa mật khẩu và phân quyền truy cập endpoint",
        "error": "mật khẩu bị rò rỉ dưới dạng text thuần",
        "solution": "sử dụng thư viện passlib với thuật toán bcrypt để hash mật khẩu"
    },
    "middleware": {
        "name": "FastAPI Middleware & CORS",
        "terms": ["CORS Middleware", "Request-Response lifecycle", "CORSMiddleware origins", "TrustedHostMiddleware", "Custom middleware decorator"],
        "correct_syntax": "app.add_middleware(CORSMiddleware, allow_origins=origins)",
        "wrong_1": "app.middleware(CORSMiddleware, origins=origins)",
        "wrong_2": "app.add_middleware(CORS, origins=origins)",
        "wrong_3": "app.config.middleware(CORSMiddleware)",
        "action": "chặn lọc request đầu vào và xử lý CORS",
        "error": "lỗi chặn tài nguyên giữa các domain khác nhau (CORS block)",
        "solution": "cấu hình CORSMiddleware với danh sách allow_origins được phép"
    },
    "upload": {
        "name": "File Upload & Static Files",
        "terms": ["UploadFile metadata", "StaticFiles mounting", "File size validation", "MIME type checking", "File read/write chunks"],
        "correct_syntax": "async def upload(file: UploadFile = File(...))",
        "wrong_1": "def upload(file: File)",
        "wrong_2": "async def upload(file: bytes)",
        "wrong_3": "async def upload(file: UploadFile = Form(...))",
        "action": "tải file avatar, tài liệu lên máy chủ và lưu trữ",
        "error": "tràn bộ nhớ RAM khi người dùng upload file dung lượng lớn",
        "solution": "sử dụng đối tượng UploadFile để tự động ghi đệm vào file tạm trên đĩa"
    },
    "testing": {
        "name": "FastAPI Testing & Pytest",
        "terms": ["pytest fixtures", "TestClient instances", "Database Mocking", "Assertion status_code", "Async testing"],
        "correct_syntax": "client = TestClient(app); response = client.get('/')",
        "wrong_1": "client = app.test_client(); response = client.get('/')",
        "wrong_2": "response = app.get('/')",
        "wrong_3": "client = TestClient(); response = client.get(app, '/')",
        "action": "viết kịch bản kiểm thử tích hợp tự động",
        "error": "lọc dữ liệu thử nghiệm ảnh hưởng đến database thật",
        "solution": "sử dụng Mocking hoặc thiết lập cơ sở dữ liệu test riêng thông qua pytest fixtures"
    }
}

NESTJS_TOPIC_DETAILS = {
    "orientation": {
        "name": "Định hướng học tập",
        "terms": ["Thiết kế ngược (Backward Design)", "Học tập chủ động (Active Learning)", "Dự án cuối môn", "Bài thực hành Lab"],
        "correct_syntax": "thiết kế ngược từ dự án thực tế",
        "wrong_1": "học lý thuyết suông trước",
        "wrong_2": "bỏ qua các bài thực hành Lab",
        "wrong_3": "chỉ học cú pháp cơ bản",
        "action": "bắt đầu môn học và định hình lộ trình",
        "error": "mơ hồ về sản phẩm cuối khóa",
        "solution": "áp dụng Thiết kế ngược (Backward Design)"
    },
    "intro": {
        "name": "NestJS CLI & Modules",
        "terms": ["NestJS CLI", "AppModule root", "Controllers decorators", "Providers providers", "Dependency Injection"],
        "correct_syntax": "@Module({ controllers: [AppController] })",
        "wrong_1": "class AppModule extends Controller",
        "wrong_2": "@Module({ routes: ['/'] })",
        "wrong_3": "@AppControllerModule()",
        "action": "khởi tạo module gốc và chạy ứng dụng NestJS",
        "error": "lỗi Dependency Injection và khởi tạo Container",
        "solution": "khai báo controller và provider trong @Module decorator"
    },
    "validation": {
        "name": "Validation & Pipes",
        "terms": ["ValidationPipe", "class-validator decorators", "class-transformer", "BadRequestException", "DTO schemas"],
        "correct_syntax": "class CreateDto { @IsString() name: string; }",
        "wrong_1": "class CreateDto { name: string; }",
        "wrong_2": "class CreateDto { name = IsString(); }",
        "wrong_3": "function CreateDto(name: string)",
        "action": "tự động kiểm tra định dạng dữ liệu request body",
        "error": "nhận dữ liệu sai định dạng (BadRequestException)",
        "solution": "sử dụng ValidationPipe kết hợp decorators của class-validator"
    },
    "crud": {
        "name": "Controllers & Routing",
        "terms": ["@Get() / @Post() decorators", "HttpCode status", "Response mapping", "Param decorators", "Query pipes"],
        "correct_syntax": "@Post() create(@Body() createDto: CreateDto)",
        "wrong_1": "@Route('/items', methods=['POST'])",
        "wrong_2": "@Post() create(createDto)",
        "wrong_3": "router.post('/items', create)",
        "action": "nhận HTTP request và gọi service xử lý tương ứng",
        "error": "sai HttpCode trả về hoặc thiếu Body parameter",
        "solution": "sử dụng decorator @Body() và @HttpCode()"
    },
    "database": {
        "name": "TypeORM / Prisma & DB Connection",
        "terms": ["TypeORM InjectRepository", "PrismaClient service", "Entity schemas", "Database migrations", "Repository pattern"],
        "correct_syntax": "@InjectRepository(User) private repo: Repository<User>",
        "wrong_1": "this.repo = new Repository(User)",
        "wrong_2": "@InjectRepository() repo: Repository",
        "wrong_3": "repo = User.getRepository()",
        "action": "kết nối CSDL và thực hiện thao tác ORM",
        "error": "lỗi mất kết nối (connection timeout/pool overflow)",
        "solution": "sử dụng Dependency Injection InjectRepository để quản lý kết nối"
    },
    "structure": {
        "name": "NestJS Modules & Structure",
        "terms": ["Feature modules", "Core Modules", "Shared Modules", "APIRouter equivalent", "Dynamic Modules"],
        "correct_syntax": "@Module({ imports: [UsersModule], exports: [UsersService] })",
        "wrong_1": "@Module({ controllers: [UsersService] })",
        "wrong_2": "export class UsersModule extends AppModule",
        "wrong_3": "@Module({ providers: [UsersModule] })",
        "action": "chia tách module và quản lý routing dự án lớn",
        "error": "trùng lặp tiền tố đường dẫn hoặc vòng lặp module dependency",
        "solution": "tách biệt các module chức năng độc lập và imports vào module gốc"
    },
    "relationship": {
        "name": "TypeORM Relationships",
        "terms": ["@ManyToOne / @OneToMany", "@JoinColumn constraint", "@ManyToMany link table", "Eager/Lazy loading", "Cascade operations"],
        "correct_syntax": "@ManyToOne(() => User, (user) => user.items)",
        "wrong_1": "@ForeignKey(() => User)",
        "wrong_2": "@ManyToOne(() => User, JoinColumn='items')",
        "wrong_3": "@ManyToOne(() => User, user => user.items, { join: true })",
        "action": "thiết lập liên kết giữa các bảng trong ORM",
        "error": "lỗi tải chậm truy vấn (N+1 queries problem)",
        "solution": "sử dụng relation decorator kết hợp options relations trong find"
    },
    "security": {
        "name": "NestJS Guards & JWT Auth",
        "terms": ["JwtService sign", "AuthGuard strategies", "PassportStrategy config", "bcrypt hashing", "Role Guards"],
        "correct_syntax": "@UseGuards(JwtAuthGuard) @Get('profile')",
        "wrong_1": "@UseMiddleware(JwtGuard) @Get()",
        "wrong_2": "@Guard(JwtAuthGuard) @Get()",
        "wrong_3": "@VerifyJwt() @Get()",
        "action": "mã hóa mật khẩu và phân quyền truy cập endpoint",
        "error": "mật khẩu bị rò rỉ dưới dạng text thuần",
        "solution": "sử dụng bcrypt để hash mật khẩu và bảo vệ endpoint bằng JwtAuthGuard"
    },
    "middleware": {
        "name": "NestJS Middleware & CORS",
        "terms": ["NestMiddleware interface", "App.enableCors()", "Global Middlewares", "ExecutionContext inspect", "ExceptionFilter custom"],
        "correct_syntax": "app.enableCors({ origin: 'http://localhost:3000' })",
        "wrong_1": "app.useCors('http://localhost:3000')",
        "wrong_2": "app.addMiddleware(Cors)",
        "wrong_3": "app.config.cors({ origin: 'http://localhost:3000' })",
        "action": "chặn lọc request đầu vào và xử lý CORS",
        "error": "lỗi chặn tài nguyên giữa các domain khác nhau (CORS block)",
        "solution": "cấu hình app.enableCors() với các options origin cụ thể"
    },
    "upload": {
        "name": "File Upload & Static Assets",
        "terms": ["FileInterceptor helper", "@UploadedFile decorator", "Multer config", "ServeStaticModule", "File size bounds"],
        "correct_syntax": "@UseInterceptors(FileInterceptor('file'))",
        "wrong_1": "@UseInterceptors(UploadedFile)",
        "wrong_2": "upload(@Body() file: File)",
        "wrong_3": "@FileUploaded('file') upload()",
        "action": "tải file avatar, tài liệu lên máy chủ và lưu trữ",
        "error": "tràn bộ nhớ RAM khi người dùng upload file dung lượng lớn",
        "solution": "sử dụng FileInterceptor kết hợp cấu hình limits và storage của Multer"
    },
    "testing": {
        "name": "NestJS Testing & Jest",
        "terms": ["Test.createTestingModule", "TestingModule compile", "Jest spyOn", "E2E testing Supertest", "Mocking providers"],
        "correct_syntax": "const module = await Test.createTestingModule({ ... }).compile()",
        "wrong_1": "const module = new TestingModule()",
        "wrong_2": "const module = Test.compile({ ... })",
        "wrong_3": "const module = await Test.createModule({ ... }).compile()",
        "action": "viết kịch bản kiểm thử tích hợp tự động",
        "error": "lọc dữ liệu thử nghiệm ảnh hưởng đến database thật",
        "solution": "sử dụng createTestingModule để mock các database providers"
    }
}

PYTHON_CORE_TOPIC_DETAILS = {
    "core_intro": {
        "name": "Giới thiệu Python & Thiết lập môi trường",
        "terms": ["Trình thông dịch CPython", "Biến môi trường PATH", "Định kiểu động (Dynamic Typing)", "Ép kiểu (Type Casting)", "Định dạng chuỗi f-string"],
        "correct_syntax": "age = int(input('Nhập tuổi: '))",
        "wrong_1": "int age = input('Nhập tuổi')",
        "wrong_2": "age = (int)input('Nhập tuổi')",
        "wrong_3": "age = input(int('Nhập tuổi'))",
        "action": "nhập xuất dữ liệu và ép kiểu an toàn",
        "error": "lỗi kiểu dữ liệu TypeError khi cộng chuỗi với số",
        "solution": "sử dụng hàm int() hoặc float() để ép kiểu dữ liệu rõ ràng trước khi tính toán"
    },
    "core_operators": {
        "name": "Toán tử & Cấu trúc điều kiện",
        "terms": ["Chia lấy phần nguyên //", "Chia lấy dư %", "Đánh giá ngắn mạch (Short-circuit)", "Toán tử ba ngôi", "Match-case (Python 3.10+)"],
        "correct_syntax": "result = 'Chẵn' if x % 2 == 0 else 'Lẻ'",
        "wrong_1": "result = x % 2 == 0 ? 'Chẵn' : 'Lẻ'",
        "wrong_2": "result = if x % 2 == 0: 'Chẵn' else 'Lẻ'",
        "wrong_3": "result = x % 2 == 0 else 'Lẻ' if 'Chẵn'",
        "action": "kiểm tra điều kiện rẽ nhánh và so sánh giá trị",
        "error": "lỗi cú pháp SyntaxError hoặc sai độ ưu tiên toán tử logic",
        "solution": "sử dụng cấu trúc rẽ nhánh if-elif-else hoặc match-case kết hợp dấu ngoặc đơn để tường minh độ ưu tiên"
    },
    "core_loops": {
        "name": "Cấu trúc Vòng lặp",
        "terms": ["Vòng lặp for và range()", "Vòng lặp while", "Lệnh break/continue", "Khối else trong vòng lặp", "Vòng lặp vô hạn"],
        "correct_syntax": "for i in range(1, 10, 2):",
        "wrong_1": "for i in range(1, 10) step 2:",
        "wrong_2": "for (i=1; i<10; i+=2):",
        "wrong_3": "for i = 1 to 10 by 2:",
        "action": "lặp qua một tập hợp hoặc thực hiện lặp theo điều kiện",
        "error": "vòng lặp vô hạn (infinite loop) làm treo chương trình",
        "solution": "cập nhật điều kiện dừng bên trong thân vòng lặp while hoặc sử dụng range() chuẩn xác"
    },
    "core_practice": {
        "name": "Thực hành Tổng hợp Python Core",
        "terms": ["Giải quyết bài toán logic", "Kiểm thử điều kiện", "Tối ưu hóa vòng lặp", "Xử lý lỗi nhập liệu", "Chương trình CLI tương tác"],
        "correct_syntax": "while True: try: val = int(input()); break; except ValueError: pass",
        "wrong_1": "val = int(input())",
        "wrong_2": "while True: val = int(input())",
        "wrong_3": "val = try int(input()) except ValueError",
        "action": "vận dụng tổng hợp toán tử, điều kiện và vòng lặp",
        "error": "sập chương trình đột ngột do người dùng nhập sai kiểu dữ liệu",
        "solution": "sử dụng vòng lặp while True kết hợp với khối try-except để bắt lỗi ValueError từ input()"
    },
    "core_strings": {
        "name": "Xử lý Chuỗi (String)",
        "terms": ["Tính bất biến (Immutable)", "Slicing [start:stop:step]", "Phương thức split() và join()", "Làm sạch dữ liệu với strip()", "Định dạng chuỗi format()"],
        "correct_syntax": "sub_str = s[1:5:2]",
        "wrong_1": "sub_str = s(1, 5, 2)",
        "wrong_2": "sub_str = s[1, 5, 2]",
        "wrong_3": "sub_str = s.slice(1, 5, 2)",
        "action": "cắt chuỗi, ghép chuỗi và định dạng văn bản hiển thị",
        "error": "lỗi IndexError khi cố gắng truy cập chỉ mục vượt quá chiều dài chuỗi",
        "solution": "sử dụng kỹ thuật slicing an sau hoặc kiểm tra len(s) trước khi truy cập chỉ mục"
    },
    "core_lists": {
        "name": "Cấu trúc dữ liệu: List & Tuple",
        "terms": ["Mảng động List (Mutable)", "Tuple bất biến (Immutable)", "Duyệt mảng với enumerate()", "Phương thức append() và pop()", "Unpacking tuple"],
        "correct_syntax": "for idx, val in enumerate(my_list):",
        "wrong_1": "for idx, val in my_list.enumerate():",
        "wrong_2": "for idx, val in my_list.items():",
        "wrong_3": "for i, v in count(my_list):",
        "action": "lưu trữ, duyệt và cập nhật danh sách phần tử động hoặc cố định",
        "error": "suy giảm hiệu năng hoặc thay đổi ngoài ý muốn dữ liệu hằng số",
        "solution": "sử dụng Tuple cho các dữ liệu cố định/hằng số và dùng List cho các danh sách cần thay đổi phần tử"
    },
    "core_dicts": {
        "name": "Cấu trúc dữ liệu: Dictionary & Set",
        "terms": ["Cặp Key-Value duy nhất", "Tập hợp Set không trùng lặp", "Phép toán tập hợp (Union, Intersection)", "Phương thức get() an toàn", "Bảng băm (Hash map)"],
        "correct_syntax": "val = my_dict.get('key', 'default')",
        "wrong_1": "val = my_dict['key'] if 'key' not in my_dict else 'default'",
        "wrong_2": "val = my_dict.fetch('key', 'default')",
        "wrong_3": "val = my_dict.get('key') or 'default'",
        "action": "truy xuất phần tử cực nhanh theo khóa và lọc trùng lặp dữ liệu",
        "error": "lỗi KeyError khi truy cập khóa không tồn tại trong từ điển",
        "solution": "sử dụng phương thức dict.get() thay vì truy cập trực tiếp bằng dấu ngoặc vuông []"
    },
    "core_functions": {
        "name": "Hàm & Phạm vi biến",
        "terms": ["Từ khóa def", "Tham số mặc định (Default arguments)", "Tham số biến đổi *args và **kwargs", "Phạm vi biến (Local, Global, Nonlocal)", "Hàm vô danh Lambda"],
        "correct_syntax": "def my_func(a, b=10, *args, **kwargs):",
        "wrong_1": "def my_func(b=10, a, *args):",
        "wrong_2": "def my_func(*args, a, b=10):",
        "wrong_3": "def my_func(a, *args, b=10, **kwargs, c):",
        "action": "tái sử dụng mã nguồn và quản lý phạm vi biến",
        "error": "lỗi thay đổi giá trị biến toàn cục ngoài ý muốn hoặc SyntaxError về thứ tự tham số",
        "solution": "khai báo các tham số không có giá trị mặc định trước, sử dụng từ khóa global hoặc nonlocal khi cần sửa biến ở scope cha"
    },
    "core_advanced": {
        "name": "Các hàm nâng cao & Xử lý tập hợp",
        "terms": ["Biểu thức List Comprehension", "Hàm map() và filter()", "Regex kiểm tra định dạng", "Sorting với key=lambda", "Module re"],
        "correct_syntax": "cleaned = [x for x in lst if x is not None]",
        "wrong_1": "cleaned = lst.filter(lambda x: x is not None)",
        "wrong_2": "cleaned = [for x in lst if x is not None: x]",
        "wrong_3": "cleaned = list(x if x is not None for x in lst)",
        "action": "lọc và biến đổi tập hợp dữ liệu một cách ngắn gọn",
        "error": "mã nguồn quá dài dòng hoặc biểu thức comprehension quá phức tạp khó đọc",
        "solution": "áp dụng List Comprehension ở mức độ vừa phải và dùng hàm lambda đơn giản làm key cho hàm sorted()"
    },
    "core_midterm": {
        "name": "Kiểm tra giữa môn",
        "terms": ["Đánh giá năng lực", "Thuật toán cơ bản", "Cấu trúc dữ liệu", "Kiểm soát luồng chạy", "Tối ưu hóa mã nguồn"],
        "correct_syntax": "def solve(data): return sorted([x for x in data if check(x)])",
        "wrong_1": "solve = lambda data: for x in data: if check(x)",
        "wrong_2": "def solve(data): pass",
        "wrong_3": "def solve(data): sorted(filter(check, data))",
        "action": "giải quyết bài toán tổng hợp đánh giá tư duy lập trình",
        "error": "lỗi logic thuật toán hoặc xử lý thiếu các trường hợp biên (edge cases)",
        "solution": "viết hàm rõ ràng, kiểm thử kỹ các trường hợp đầu vào đặc biệt như danh sách rỗng hoặc giá trị âm"
    },
    "core_clean_code": {
        "name": "Clean Code & Debugging chuyên nghiệp",
        "terms": ["Nguyên lý DRY (Don't Repeat Yourself)", "Nguyên lý KISS (Keep It Simple)", "Thụt lề PEP 8 chuẩn hóa", "Khối try-except-finally", "Sử dụng Breakpoint"],
        "correct_syntax": "try: perform_action() except SpecialException: handle_error()",
        "wrong_1": "try: perform_action() except: pass",
        "wrong_2": "try: perform_action() finally: handle_error()",
        "wrong_3": "try: perform_action() except Exception: raise",
        "action": "bắt lỗi ngoại lệ và làm sạch mã nguồn",
        "error": "nuốt lỗi âm thầm (bare except) khiến việc debug cực kỳ khó khăn",
        "solution": "luôn chỉ định rõ loại exception cần bắt trong khối except và ghi log lỗi đầy đủ"
    },
    "core_modules": {
        "name": "Module và Package",
        "terms": ["Từ khóa import", "Biến đặc biệt __name__", "Absolute vs Relative import", "File cấu hình __init__.py", "Thư viện datetime và random"],
        "correct_syntax": "if __name__ == '__main__': main()",
        "wrong_1": "if name == 'main': main()",
        "wrong_2": "if __name__ == main: main()",
        "wrong_3": "if __name__ == '__main__': run main()",
        "action": "tổ chức mã nguồn thành các module và package có thể tái sử dụng",
        "error": "lỗi nhập vòng (circular import) hoặc chạy script tự động khi import",
        "solution": "sử dụng khối điều kiện __name__ == '__main__' để ngăn mã chạy tự động khi file bị import và thiết kế import phân cấp"
    },
    "core_file_io": {
        "name": "Làm việc với File I/O",
        "terms": ["Context manager 'with'", "Chế độ mở file (r, w, a, x)", "Phương thức readlines()", "Module json tích hợp", "Module csv chuẩn"],
        "correct_syntax": "with open('file.txt', 'r', encoding='utf-8') as f:",
        "wrong_1": "f = open('file.txt'); content = f.read()",
        "wrong_2": "with open('file.txt', 'r') as f: close(f)",
        "wrong_3": "f = open('file.txt', 'r'); with f:",
        "action": "đọc ghi dữ liệu từ file văn bản, CSV hoặc JSON an toàn",
        "error": "rò rỉ tài nguyên hệ thống (file descriptor leak) khi không đóng file",
        "solution": "luôn sử dụng câu lệnh with (context manager) khi thao tác với file để tự động đóng file"
    },
    "core_practice_file": {
        "name": "Thực hành Tổng hợp: Quản lý File I/O",
        "terms": ["Xây dựng CLI app", "Lưu trữ dữ liệu dạng CSV/JSON", "Đọc ghi dữ liệu liên tục", "Xử lý file ghi đè", "Kiểm tra sự tồn tại file"],
        "correct_syntax": "import os; if os.path.exists('data.json'):",
        "wrong_1": "if 'data.json' in directory:",
        "wrong_2": "try: open('data.json') except:",
        "wrong_3": "if check_file('data.json'):",
        "action": "xây dựng ứng dụng hoàn chỉnh quản lý dữ liệu qua file",
        "error": "lỗi FileNotFoundError hoặc mất mát dữ liệu do ghi đè ngoài ý muốn",
        "solution": "sử dụng module os.path hoặc pathlib để kiểm tra sự tồn tại của file trước khi thao tác"
    },
    "core_numpy": {
        "name": "Thư viện NumPy",
        "terms": ["Mảng đa chiều ndarray", "Vectorization (Vector hóa)", "Broadcasting (Lan truyền)", "Slicing mảng Numpy", "Hàm thống kê np.mean()"],
        "correct_syntax": "arr = np.array([1, 2, 3])",
        "wrong_1": "arr = np.ndarray([1, 2, 3])",
        "wrong_2": "arr = np.list([1, 2, 3])",
        "wrong_3": "arr = np.create_array([1, 2, 3])",
        "action": "tính toán ma trận và thống kê số liệu hiệu năng cao",
        "error": "lỗi kích thước không tương thích (ValueError: operands could not be broadcast together)",
        "solution": "kiểm tra thuộc tính shape của các mảng ndarray trước khi thực hiện các phép toán vector hóa"
    },
    "core_practice_numpy": {
        "name": "Thực hành Phân tích dữ liệu với NumPy",
        "terms": ["Xử lý ma trận thực tế", "Tính toán thống kê dữ liệu", "Biến đổi hình dạng reshape", "Lọc mảng theo điều kiện Boolean index", "Tối ưu hóa hiệu năng số học"],
        "correct_syntax": "filtered_arr = arr[arr > 5]",
        "wrong_1": "filtered_arr = [x for x in arr if x > 5]",
        "wrong_2": "filtered_arr = arr.filter(lambda x: x > 5)",
        "wrong_3": "filtered_arr = np.where(arr > 5)",
        "action": "phân tích dữ liệu số và ma trận trên thực tế",
        "error": "viết vòng lặp for thủ công làm mất đi lợi thế tốc độ của mảng C-speed NumPy",
        "solution": "sử dụng cơ chế lọc Boolean Indexing hoặc hàm Vectorized của NumPy để xử lý nhanh nhất"
    },
    "core_pandas": {
        "name": "Thư viện Pandas",
        "terms": ["Series và DataFrame", "Chỉ mục loc và iloc", "Làm sạch dữ liệu dropna/fillna", "Gom nhóm GroupBy", "Merge & Join DataFrame"],
        "correct_syntax": "df_cleaned = df.drop_duplicates().fillna(0)",
        "wrong_1": "df_cleaned = df.clean()",
        "wrong_2": "df_cleaned = df.remove_duplicates()",
        "wrong_3": "df_cleaned = df.dropna().fillna()",
        "action": "nạp, làm sạch và gom nhóm bảng dữ liệu có cấu trúc",
        "error": "lỗi KeyError hoặc mất dữ liệu khi merge DataFrame sai khóa chung",
        "solution": "chỉ định rõ cột khóa trong tham số 'on' hoặc sử dụng left_on và right_on khi gọi merge()"
    },
    "core_practice_pandas": {
        "name": "Thực hành Phân tích dữ liệu thực tế với Pandas",
        "terms": ["Đọc tệp Sales Dataset", "Trích xuất insight doanh thu", "Gom nhóm theo khu vực", "Vẽ biểu đồ số liệu", "Xuất file Excel báo cáo"],
        "correct_syntax": "sales_report = df.groupby('Region')['Revenue'].sum()",
        "wrong_1": "sales_report = df.groupby('Region').Revenue.sum",
        "wrong_2": "sales_report = sum(df.groupby('Region')['Revenue'])",
        "wrong_3": "sales_report = df.Region.sum_revenue()",
        "action": "phân tích dữ liệu kinh doanh thực tế để rút ra thông tin có ích",
        "error": "báo cáo thống kê sai lệch do dữ liệu rác hoặc giá trị khuyết",
        "solution": "luôn thực hiện tiền xử lý làm sạch dữ liệu khuyết bằng fillna() hoặc dropna() trước khi chạy groupby"
    },
    "core_review": {
        "name": "Tổng ôn tập kiến thức toàn khóa",
        "terms": ["Hệ thống hóa kiến thức", "Cấu trúc dữ liệu Python", "Thư viện NumPy & Pandas", "Thuật toán cơ bản"],
        "correct_syntax": "summary_data = df.describe()",
        "wrong_1": "summary_data = df.summary()",
        "wrong_2": "summary_data = describe(df)",
        "wrong_3": "summary_data = df.info(stats=True)",
        "action": "tổng hợp và hệ thống hóa toàn bộ tri thức đã học",
        "error": "nhầm lẫn giữa cú pháp của Python Core và các thư viện phân tích dữ liệu",
        "solution": "nắm vững bản chất từng công cụ để lựa chọn và áp dụng chính xác trong từng tình huống thực tế"
    }
}


def shuffle_options_and_explanations(q: Dict[str, Any]) -> None:
    """Randomly shuffles the 4 multiple-choice options and their corresponding explanations, updating isCorrect index (1 to 4)."""
    options = [
        (q.get("answer_1", ""), q.get("explanation_answer_1", ""), 1 == q.get("isCorrect", 1)),
        (q.get("answer_2", ""), q.get("explanation_answer_2", ""), 2 == q.get("isCorrect", 1)),
        (q.get("answer_3", ""), q.get("explanation_answer_3", ""), 3 == q.get("isCorrect", 1)),
        (q.get("answer_4", ""), q.get("explanation_answer_4", ""), 4 == q.get("isCorrect", 1))
    ]
    random.shuffle(options)
    for idx, (ans, exp, is_correct) in enumerate(options, 1):
        q[f"answer_{idx}"] = ans
        q[f"explanation_answer_{idx}"] = exp
        if is_correct:
            q["isCorrect"] = idx


def generate_questions_for_topic(topic_key: str, count: int, category: str, start_stt: int, difficulty: int, tech_stack: str = "python/fastapi") -> List[Dict[str, Any]]:
    """Generates a batch of distinct, high-quality, academic questions for a given topic key."""
    details_map = FASTAPI_TOPIC_DETAILS
    fallback_key = "intro"
    if "nestjs" in tech_stack:
        details_map = NESTJS_TOPIC_DETAILS
    elif "core" in tech_stack:
        details_map = PYTHON_CORE_TOPIC_DETAILS
        fallback_key = "core_intro"
        
    topic = details_map.get(topic_key, details_map[fallback_key])
    questions = []
    
    framework = "FastAPI"
    if "nestjs" in tech_stack:
        framework = "NestJS"
    elif "react" in tech_stack:
        framework = "React"
    elif "springboot" in tech_stack or "java" in tech_stack:
        framework = "Spring Boot"
    elif "core" in tech_stack:
        framework = "Python Core"

    if "core" in tech_stack:
        templates = [
            # Type A: Syntax & Concept (Understand/Remember)
            {
                "q_template": "Trong lập trình Python cơ bản, để thực hiện {action} đối với {term_1}, cú pháp chuẩn hóa nào được khuyến nghị?",
                "ans_correct": "Triển khai khai báo '{correct_syntax}' kèm xử lý kiểu dữ liệu phù hợp.",
                "exp_correct": "Đúng, đây là tiêu chuẩn giúp đảm bảo tính rõ ràng và tránh lỗi runtime.",
                "ans_w1": "Triển khai '{wrong_1}' bằng các cú pháp không chuẩn.",
                "exp_w1": "Sai, cú pháp này không đúng tiêu chuẩn của Python Core và sẽ gây lỗi SyntaxError/TypeError.",
                "ans_w2": "Sử dụng cách viết '{wrong_2}' để đơn giản hóa cấu hình đầu vào.",
                "exp_w2": "Sai, cú pháp này sai quy tắc ngữ pháp của Python và không thể thực thi.",
                "ans_w3": "Triển khai qua '{wrong_3}' mà không có kiểu dữ liệu phù hợp.",
                "exp_w3": "Sai, cách viết này gây lỗi khi chương trình thực hiện tính toán hoặc xử lý logic."
            },
            # Type B: Debugging & Flow Control (Analyze)
            {
                "q_template": "Một chương trình Python thực tế gặp tình trạng {error} khi thực hiện tác vụ liên quan đến {term_2}. Đâu là nguyên nhân cốt lõi?",
                "ans_correct": "Do không áp dụng '{solution}', dẫn tới luồng xử lý bị lỗi hoặc thiếu ép kiểu phù hợp.",
                "exp_correct": "Đúng, việc thiếu giải pháp xử lý hoặc ép kiểu phù hợp sẽ trực tiếp gây ra lỗi logic hoặc dừng chương trình.",
                "ans_w1": "Do cấu hình nhầm '{wrong_1}' trong môi trường chạy lệnh.",
                "exp_w1": "Sai, cấu hình này không ảnh hưởng trực tiếp đến luồng logic xử lý lỗi trong mã nguồn.",
                "ans_w2": "Do bỏ sót việc khai báo '{wrong_2}' trong hàm main.",
                "exp_w2": "Sai, việc thiếu khai báo này sẽ gây lỗi khác thay vì lỗi runtime của luồng xử lý.",
                "ans_w3": "Do gán sai giá trị sang dạng '{wrong_3}' cho biến.",
                "exp_w3": "Sai, việc gán sai giá trị này chỉ ảnh hưởng đến kết quả chứ không trực tiếp gây ra lỗi luồng tương tự."
            },
            # Type C: Architecture & Optimization (Create/Design)
            {
                "q_template": "Khi tối ưu hóa và xây dựng mã nguồn sử dụng {term_3}, để giải quyết triệt để {error}, giải pháp lập trình nào là tối ưu?",
                "ans_correct": "Áp dụng '{solution}' kết hợp quản lý tài nguyên và kiểm soát luồng chạy.",
                "exp_correct": "Đúng, giải pháp tích hợp này giúp giải quyết toàn diện cả lỗi logic lẫn tính ổn định của ứng dụng.",
                "ans_w1": "Chuyển toàn bộ các luồng xử lý dữ liệu sang cấu trúc '{wrong_1}'.",
                "exp_w1": "Sai, cấu trúc này làm tăng đáng kể độ phức tạp thuật toán và giảm hiệu năng thực thi.",
                "ans_w2": "Khởi tạo tài nguyên trực tiếp thông qua cơ chế '{wrong_2}'.",
                "exp_w2": "Sai, khởi tạo trực tiếp không giải quyết được vấn đề quản lý tài nguyên an toàn.",
                "ans_w3": "Tăng giới hạn phần cứng máy tính và đổi cấu hình sang '{wrong_3}'.",
                "exp_w3": "Sai, nâng cấp phần cứng chỉ giải quyết tạm thời và tốn kém hơn tối ưu hóa giải thuật mã nguồn."
            }
        ]
    else:
        templates = [
            # Type A: Syntax & Concept (Understand/Remember)
            {
                "q_template": "Trong lập trình Web API bằng {framework}, để thực hiện {action} đối với {term_1}, cú pháp chuẩn hóa nào được khuyến nghị?",
                "ans_correct": "Triển khai khai báo '{correct_syntax}' kèm định nghĩa kiểu dữ liệu.",
                "exp_correct": "Đúng, đây là tiêu chuẩn của framework giúp tự động hóa quá trình sinh Swagger docs và kiểm tra kiểu dữ liệu.",
                "ans_w1": "Triển khai '{wrong_1}' bằng các hàm callback đồng bộ.",
                "exp_w1": "Sai, cú pháp này không tận dụng được cơ chế kiểm soát kiểu của {framework}.",
                "ans_w2": "Sử dụng cách viết '{wrong_2}' để đơn giản hóa cấu hình đầu vào.",
                "exp_w2": "Sai, cú pháp này thiếu tính chặt chẽ và không thể render Swagger UI.",
                "ans_w3": "Triển khai qua '{wrong_3}' mà không cần kế thừa.",
                "exp_w3": "Sai, cách viết này gây lỗi runtime khi parser cố gắng phân tích đối tượng."
            },
            # Type B: Debugging & Flow Control (Analyze)
            {
                "q_template": "Một ứng dụng thực tế gặp tình trạng {error} khi thực hiện tác vụ liên quan đến {term_2}. Đâu là nguyên nhân cốt lõi?",
                "ans_correct": "Do không áp dụng '{solution}', dẫn tới luồng xử lý bị chặn hoặc thiếu validation dữ liệu đầu vào.",
                "exp_correct": "Đúng, việc thiếu giải pháp kỹ thuật phù hợp sẽ trực tiếp gây ra lỗi logic hoặc quá tải tài nguyên.",
                "ans_w1": "Do cấu hình nhầm '{wrong_1}' trong file cấu hình môi trường.",
                "exp_w1": "Sai, cấu hình này không ảnh hưởng trực tiếp đến luồng logic xử lý lỗi.",
                "ans_w2": "Do bỏ sót việc import module '{wrong_2}' ở file main chính.",
                "exp_w2": "Sai, thiếu import sẽ gây ra NameError/ImportError ngay lập tức thay vì lỗi runtime luồng.",
                "ans_w3": "Do khai báo sai kiểu trả về sang dạng '{wrong_3}' cho endpoint.",
                "exp_w3": "Sai, kiểu dữ liệu trả về chỉ làm sai cấu trúc response chứ không gây treo luồng xử lý."
            },
            # Type C: Architecture & Optimization (Create/Design)
            {
                "q_template": "Khi thiết kế hệ thống có lượng tải lớn sử dụng {term_3}, để giải quyết triệt để {error}, giải pháp kiến trúc nào là tối ưu?",
                "ans_correct": "Áp dụng '{solution}' kết hợp quản lý tài nguyên và kiểm thử hiệu năng tự động.",
                "exp_correct": "Đúng, giải pháp tích hợp này giải quyết toàn diện cả hiệu năng xử lý lẫn tính toàn vẹn dữ liệu.",
                "ans_w1": "Chuyển toàn bộ các endpoint xử lý dữ liệu sang cấu trúc '{wrong_1}'.",
                "exp_w1": "Sai, cấu trúc này làm tăng đáng kể I/O blocking và giảm thông lượng hệ thống.",
                "ans_w2": "Khởi tạo tài nguyên trực tiếp thông qua cơ chế '{wrong_2}'.",
                "exp_w2": "Sai, khởi tạo trực tiếp không giải quyết được vấn đề phân bổ và thu hồi tài nguyên tự động.",
                "ans_w3": "Tăng giới hạn phần cứng máy chủ và đổi cấu hình sang '{wrong_3}'.",
                "exp_w3": "Sai, tối ưu hóa phần cứng chỉ là giải pháp tạm thời và tốn kém chi phí hơn tối ưu hóa mã nguồn."
            }
        ]
    
    for i in range(count):
        # Pick template based on sequence
        tpl = templates[i % len(templates)]
        
        # Select random terms
        terms_selected = random.sample(topic["terms"], 3) if len(topic["terms"]) >= 3 else (topic["terms"] * 3)[:3]
        
        q_text = tpl["q_template"].format(
            framework=framework,
            action=topic["action"],
            error=topic["error"],
            solution=topic["solution"],
            term_1=terms_selected[0],
            term_2=terms_selected[1],
            term_3=terms_selected[2]
        )
        
        ans_1 = tpl["ans_correct"].format(correct_syntax=topic["correct_syntax"], solution=topic["solution"])
        exp_1 = tpl["exp_correct"].format(correct_syntax=topic["correct_syntax"], solution=topic["solution"])
        
        ans_2 = tpl["ans_w1"].format(wrong_1=topic["wrong_1"], wrong_2=topic["wrong_2"])
        exp_2 = tpl["exp_w1"].format(wrong_1=topic["wrong_1"], wrong_2=topic["wrong_2"], framework=framework)
        
        ans_3 = tpl["ans_w2"].format(wrong_2=topic["wrong_2"], wrong_3=topic["wrong_3"])
        exp_3 = tpl["exp_w2"].format(wrong_2=topic["wrong_2"], wrong_3=topic["wrong_3"])
        
        ans_4 = tpl["ans_w3"].format(wrong_3=topic["wrong_3"], wrong_1=topic["wrong_1"])
        exp_4 = tpl["exp_w3"].format(wrong_3=topic["wrong_3"], wrong_1=topic["wrong_1"])
        
        # Clean double quotes or spaces
        q_text = re.sub(r'\s+', ' ', q_text).strip()
        
        q = {
            "STT": start_stt + i,
            "question_content": q_text,
            "answer_1": ans_1,
            "explanation_answer_1": exp_1,
            "answer_2": ans_2,
            "explanation_answer_2": exp_2,
            "answer_3": ans_3,
            "explanation_answer_3": exp_3,
            "answer_4": ans_4,
            "explanation_answer_4": exp_4,
            "isCorrect": 1, # default correct is A (1)
            "difficulty": difficulty,
            "category": category
        }   
        
        shuffle_options_and_explanations(q)
        questions.append(q)
        
    return questions

def generate_quiz_batch_via_llm(topic_name: str, tech_stack: str, count: int, difficulty: int, category: str, start_stt: int) -> List[Dict[str, Any]]:
    """Generates a batch of quiz questions via LLM using RAG content from local Vector DB."""
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        return []
        
    from core.llm import call_llm
    from core.skills import load_skill_content
    from core.vector_store import LightweightVectorStore
    
    rag_context = ""
    try:
        store = LightweightVectorStore()
        matches = store.query(topic_name, k=3)
        if matches:
            rag_context = "\nNgữ cảnh tham chiếu từ Vector DB:\n" + "\n".join([m["text"] for m in matches])
    except Exception:
        pass
        
    skill_content = load_skill_content("quizz_session")
    
    system_prompt = f"""Bạn là Chuyên gia thiết kế câu hỏi kiểm tra lập trình (Assessment Specialist).
Nhiệm vụ của bạn là tạo ra đúng {count} câu hỏi trắc nghiệm khách quan có chất lượng cao về chủ đề '{topic_name}' sử dụng công nghệ '{tech_stack}'.

Quy tắc sinh câu hỏi (Quizz Session Skill):
{skill_content}

RÀNG BUỘC CỦA ĐỢT SINH NÀY:
- Số câu hỏi cần tạo: {count} câu.
- Số thứ tự bắt đầu (STT): {start_stt}.
- Độ khó (difficulty): {difficulty}.
- Phân loại (category): "{category}".
{rag_context}

Yêu cầu định dạng đầu ra:
Bạn phải trả về duy nhất một mảng JSON chứa đúng {count} câu hỏi có cấu trúc như sau:
[
  {{
    "STT": {start_stt},
    "question_content": "Nội dung câu hỏi tình huống thực tế...",
    "answer_1": "Đáp án đúng A",
    "explanation_answer_1": "Giải thích vì sao A đúng...",
    "answer_2": "Đáp án nhiễu B",
    "explanation_answer_2": "Giải thích vì sao B sai...",
    "answer_3": "Đáp án nhiễu C",
    "explanation_answer_3": "Giải thích...",
    "answer_4": "Đáp án nhiễu D",
    "explanation_answer_4": "Giải thích...",
    "isCorrect": 1,
    "difficulty": {difficulty},
    "category": "{category}"
  }}
]
Mẹo: Luôn xếp đáp án đúng vào 'answer_1' và 'isCorrect' là 1. Hệ thống sẽ tự động xáo trộn ngẫu nhiên sau đó.
"""
    
    user_prompt = f"Hãy tạo đúng {count} câu hỏi trắc nghiệm định dạng JSON."
    
    try:
        response = call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            agent_name="Session_Quiz_Agent",
            session_id=category,
            lesson_id=topic_name
        )
        
        clean_json = response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json.split("```json", 1)[1]
        if clean_json.endswith("```"):
            clean_json = clean_json.rsplit("```", 1)[0]
        clean_json = clean_json.strip()
        
        qs = json.loads(clean_json)
        if isinstance(qs, list) and len(qs) > 0:
            for idx, q in enumerate(qs):
                q["STT"] = start_stt + idx
                q["difficulty"] = difficulty
                q["category"] = category
                if "isCorrect" not in q:
                    q["isCorrect"] = 1
            return qs
    except Exception as e:
        print(f"  [Session Quiz Agent Warning] LLM generation failed: {e}. Falling back to templates...")
        
    return []

def generate_entrance_quiz(session_id: str, current_topic: str, previous_topic: str, tech_stack: str = "python/fastapi") -> List[Dict[str, Any]]:
    """Generates a 45-question Entrance Quiz dynamically or via rule-based fallback."""
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if gemini_key or openai_key:
        print(f"  [Quiz Engine] Generating Entrance Quiz via LLM RAG for stack: {tech_stack}...")
        questions = []
        
        # 12 questions (difficulty 4)
        q1 = generate_quiz_batch_via_llm(previous_topic, tech_stack, 12, 4, "BÀI CŨ", 1)
        if q1: questions.extend(q1)
        
        # 9 questions (difficulty 6)
        q2 = generate_quiz_batch_via_llm(previous_topic, tech_stack, 9, 6, "BÀI CŨ", len(questions) + 1)
        if q2: questions.extend(q2)
        
        # 9 questions (difficulty 8)
        q3 = generate_quiz_batch_via_llm(previous_topic, tech_stack, 9, 8, "BÀI CŨ", len(questions) + 1)
        if q3: questions.extend(q3)
        
        # 6 questions (difficulty 5)
        q4 = generate_quiz_batch_via_llm(current_topic, tech_stack, 6, 5, "BÀI MỚI", len(questions) + 1)
        if q4: questions.extend(q4)
        
        # 6 questions (difficulty 7)
        q5 = generate_quiz_batch_via_llm(current_topic, tech_stack, 6, 7, "BÀI MỚI", len(questions) + 1)
        if q5: questions.extend(q5)
        
        # 3 questions (difficulty 9)
        q6 = generate_quiz_batch_via_llm(current_topic, tech_stack, 3, 9, "BÀI MỚI", len(questions) + 1)
        if q6: questions.extend(q6)
        
        if len(questions) == 45:
            for q in questions:
                shuffle_options_and_explanations(q)
            for idx, q in enumerate(questions, 1):
                q["STT"] = idx
            return questions
        print(f"  [Quiz Engine Warning] LLM generated {len(questions)}/45 questions. Falling back to templates...")
        
    questions = []
    questions.extend(generate_questions_for_topic(previous_topic, 12, "BÀI CŨ", 1, 4, tech_stack))
    questions.extend(generate_questions_for_topic(previous_topic, 9, "BÀI CŨ", 13, 6, tech_stack))
    questions.extend(generate_questions_for_topic(previous_topic, 9, "BÀI CŨ", 22, 8, tech_stack))
    questions.extend(generate_questions_for_topic(current_topic, 6, "BÀI MỚI", 31, 5, tech_stack))
    questions.extend(generate_questions_for_topic(current_topic, 6, "BÀI MỚI", 37, 7, tech_stack))
    questions.extend(generate_questions_for_topic(current_topic, 3, "BÀI MỚI", 43, 9, tech_stack))
    for idx, q in enumerate(questions, 1):
        q["STT"] = idx
    return questions

def generate_exit_quiz(session_id: str, current_topic: str, tech_stack: str = "python/fastapi") -> List[Dict[str, Any]]:
    """Generates a 45-question Exit Quiz dynamically or via rule-based fallback."""
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if gemini_key or openai_key:
        print(f"  [Quiz Engine] Generating Exit Quiz via LLM RAG for stack: {tech_stack}...")
        questions = []
        
        # 18 questions (difficulty 6)
        q1 = generate_quiz_batch_via_llm(current_topic, tech_stack, 18, 6, "BÀI MỚI", 1)
        if q1: questions.extend(q1)
        
        # 15 questions (difficulty 10)
        q2 = generate_quiz_batch_via_llm(current_topic, tech_stack, 15, 10, "BÀI MỚI", len(questions) + 1)
        if q2: questions.extend(q2)
        
        # 12 questions (difficulty 11)
        q3 = generate_quiz_batch_via_llm(current_topic, tech_stack, 12, 11, "BÀI MỚI", len(questions) + 1)
        if q3: questions.extend(q3)
        
        if len(questions) == 45:
            for q in questions:
                shuffle_options_and_explanations(q)
            for idx, q in enumerate(questions, 1):
                q["STT"] = idx
            return questions
        print(f"  [Quiz Engine Warning] LLM generated {len(questions)}/45 questions. Falling back to templates...")
        
    questions = []
    questions.extend(generate_questions_for_topic(current_topic, 18, "BÀI MỚI", 1, 6, tech_stack))
    questions.extend(generate_questions_for_topic(current_topic, 15, "BÀI MỚI", 19, 10, tech_stack))
    questions.extend(generate_questions_for_topic(current_topic, 12, "BÀI MỚI", 34, 11, tech_stack))
    for idx, q in enumerate(questions, 1):
        q["STT"] = idx
    return questions

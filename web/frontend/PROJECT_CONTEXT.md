# PROJECT CONTEXT - SHIPUP CARRIER FRONTEND (FE)

Bản đồ ngữ cảnh dự án Frontend dành cho các Agent AI. Đọc file này giúp hiểu toàn bộ cấu trúc dự án mà không cần quét toàn bộ mã nguồn.

---

## 1. THÔNG TIN CHUNG & QUY TẮC BẢO MẬT

- **Stack**: React + TypeScript + Vite + Ant Design (`antd`) + React Query (`@tanstack/react-query`) + Tailwind CSS / Custom CSS.
- **Kiến trúc**: Hướng Module Chức năng (Modular Architecture).
- **Quy tắc bảo mật quan trọng**:
  > [!IMPORTANT]
  > **TUYỆT ĐỐI KHÔNG ĐỌC** các file môi trường nhạy cảm như `.env`, `.env.development`, `.env.test`, `.env.production` hoặc bất kỳ file chứa thông tin credentials nào.
- **Quy tắc ngôn ngữ**:
  - Giải thích và giao tiếp với người dùng bằng **Tiếng Việt**.

---

## 2. BẢN ĐỒ CẤU TRÚC THƯ MỤC (FE)

```text
web_shipup_carrier/
├── .agents/                    # Chứa các skill chuyên biệt của Agent
│   ├── skill-receive.md        # Skill Nhận yêu cầu
│   ├── skill-process.md        # Skill Xử lý logic & lập kế hoạch
│   ├── skill-generate.md       # Skill Tạo/Sinh code FE (Components, Hooks, API, UI)
│   └── skill-delete.md         # Skill Xóa code (yêu cầu xác nhận)
├── src/
│   ├── common/                 # Components, hooks, utils, apis dùng chung cho toàn bộ dự án
│   │   ├── components/         # Button, Table, Notification dùng chung
│   │   ├── interfaces/         # Định nghĩa các interface chung
│   │   │   └── response.interface.ts # Định nghĩa các kiểu Response từ API (SingleResponse, PaginatedResponse)
│   │   └── utils/              # Các hàm helper định dạng ngày tháng, số, v.v.
│   ├── layouts/                # Các layout chính của web (MainLayout, AuthLayout)
│   ├── lib/                    # Cấu hình http client (axios instance)
│   │   └── index.ts            # Export 'http' client dùng để gọi API
│   ├── routes/                 # Định nghĩa React Router DOM config
│   ├── services/               # Các API service chung toàn cục
│   ├── styles/                 # Custom styles, CSS variables
│   └── modules/                # Thư mục chứa các module nghiệp vụ
│       └── [moduleName]/       # Ví dụ: vehicleManager, warehouseManager
│           ├── components/     # Các components đặc thù của module (ví dụ: VehicleTable.tsx)
│           ├── constants/      # Các hằng số nghiệp vụ của module
│           ├── enums/          # Các enum nghiệp vụ của module (ví dụ: VehicleStatus)
│           ├── hooks/          # React Query hooks (useFetchVehicles.ts, useVehicleMutations.ts)
│           ├── interfaces/     # TypeScript interfaces (DTO, Entity) cho module
│           ├── pages/          # Các page chính (ví dụ: VehicleList.tsx, VehicleDetail.tsx)
│           └── services/       # File gọi API nghiệp vụ (ví dụ: vehicle.api.ts)
```

---

## 3. CHUẨN ĐỒNG BỘ API RESPONSE (FE)

Khi tương tác API, sử dụng các kiểu dữ liệu khai báo trong [response.interface.ts](file:///d:/Workspace/web_shipup_carrier/src/common/interfaces/response.interface.ts):

- API Trả về 1 object đơn (Create/Update/Detail): Sử dụng `SingleResponse<T>` hoặc `BaseResponse<T>`.
- API Trả về danh sách không phân trang: Sử dụng `ListResponse<T>`.
- API Trả về danh sách có phân trang: Sử dụng `PaginatedResponse<T>` hoặc `PaginatedDataResponse<T>`.

---

## 4. QUY TẮC ĐẶT TÊN (FE CONVENTIONS)

- **Tên Component / Page File**: Dạng PascalCase.
  - Ví dụ: `VehicleList.tsx`, `VehicleFormModal.tsx`.
- **Tên Hook File**: Dạng camelCase, bắt đầu bằng `use`.
  - Ví dụ: `useFetchVehicles.ts`, `useVehicleDetail.ts`.
- **Tên API Service File**: Dạng `[name].api.ts`.
  - Ví dụ: `vehicle.api.ts`.
- **Tên Class / Interface / Enum**: Dạng PascalCase.
  - Ví dụ: `Vehicle`, `VehicleStatus`.
- **Tên Biến/Hàm**: Dạng camelCase.
  - Ví dụ: `isLoading`, `handleDeleteClick`, `createVehicle`.

---

## 5. SKILL ENTRY POINTS (AGENT WORKFLOW)

Khi thực hiện bất kỳ nhiệm vụ nào trên dự án này, Agent phải tuân thủ nghiêm ngặt 4 bước tương ứng với 4 skill file trong thư mục `.agents/`:

1. **Bước 1: Nhận yêu cầu** - Xem chi tiết tại [.agents/skill-receive.md](file:///d:/Workspace/web_shipup_carrier/.agents/skill-receive.md)
2. **Bước 2: Xử lý & Thiết kế** - Xem chi tiết tại [.agents/skill-process.md](file:///d:/Workspace/web_shipup_carrier/.agents/skill-process.md)
3. **Bước 3: Tạo code** - Xem chi tiết tại [.agents/skill-generate.md](file:///d:/Workspace/web_shipup_carrier/.agents/skill-generate.md)
4. **Bước 4: Xóa code** - Xem chi tiết tại [.agents/skill-delete.md](file:///d:/Workspace/web_shipup_carrier/.agents/skill-delete.md)

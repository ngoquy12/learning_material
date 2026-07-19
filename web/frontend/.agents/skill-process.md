# AGENT SKILL: XỬ LÝ LOGIC & LẬP KẾ HOẠCH (PROCESS SKILL) - FE

Skill này hướng dẫn Agent cách lập kế hoạch chi tiết, thiết kế UI/UX và lập sơ đồ tích hợp API trước khi viết code Frontend.

---

## 1. QUY TRÌNH XỬ LÝ & THIẾT KẾ
1. **Thiết kế UI/UX & Layout**:
   - Xác định giao diện cần làm: Form nhập liệu, bảng danh sách hiển thị, modal xác nhận hay trang chi tiết.
   - Chọn các UI components thích hợp từ Ant Design (`antd`) như `Form`, `Input`, `Table`, `Modal`, `Select`, `Button`, `Pagination`, `Tooltip`, v.v.
   - Lên layout responsive và khoảng cách (spacing), phối hợp màu sắc hài hòa với CSS hoặc Tailwind.
2. **Thiết kế State & Data Flow**:
   - **Local State**: Xác định các trạng thái bật/tắt modal, loading nội bộ, tab hiện tại bằng `useState`.
   - **URL Query Parameters**: Với các màn hình danh sách, ưu tiên đẩy trạng thái `page`, `pageSize`, `search` lên URL qua `useSearchParams` để hỗ trợ bookmark và reload trang không mất trạng thái.
   - **Server State**: Sử dụng React Query (`useQuery` cho fetch dữ liệu, `useMutation` cho thêm/sửa/xóa).
3. **Thiết kế API Service & Interfaces**:
   - Khai báo các TypeScript interfaces tương thích với dữ liệu trả về từ Backend (thông qua `response.interface.ts`).
   - Định nghĩa các phương thức gọi API trong `services/[name].api.ts`.
4. **Thiết kế Custom Hooks**:
   - Gom các logic query/mutation vào custom hooks để tăng tính tái sử dụng và tách biệt UI với Data logic (ví dụ: `useFetchVehicles`, `useVehicleMutations`).

---

## 2. OUTPUT CỦA BƯỚC XỬ LÝ
Trước khi viết code, Agent cần trình bày:
1. **Bản phác thảo UI/UX**: Mô tả cấu trúc các Component và cách tương tác của người dùng.
2. **Kế hoạch gọi API**: Danh sách các API Endpoint của Backend sẽ tích hợp, cách map dữ liệu trả về (SingleResponse, PaginatedResponse) vào các component Table/Form.

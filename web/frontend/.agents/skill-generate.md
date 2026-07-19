# AGENT SKILL: TẠO VÀ CẬP NHẬT CODE (GENERATE SKILL) - FE

Skill này hướng dẫn Agent cách viết code React + TypeScript chuẩn mực, tạo UI sắc nét, chuyên nghiệp và tích hợp API hiệu quả.

---

## 1. TIÊU CHUẨN CODE FE

1. **Ant Design & Form Handling**:
   - Sử dụng Ant Design Components đúng cách, không tự chế các component cơ bản.
   - Dùng `Form` từ `antd` kết hợp với `rules` để thực hiện validation phía Client.
2. **React Query & API Integration**:
   - Mọi hoạt động tải dữ liệu phải qua `useQuery`. Đặt `queryKey` rõ ràng, có chứa các biến filter để auto-refetch khi filter thay đổi.
   - Mọi hoạt động thay đổi dữ liệu (POST, PATCH, DELETE) phải qua `useMutation`. Khi mutation thành công, sử dụng `queryClient.invalidateQueries` để cập nhật lại dữ liệu màn hình danh sách.
   - Bắt lỗi API và hiển thị thông báo thân thiện bằng `openNotification` từ `@/common/components/base/notification`.
3. **Quy tắc đặt tên file & thư mục**:
   - File React Component / Page: `PascalCase.tsx` (ví dụ: `VehicleList.tsx`).
   - File Hook: `camelCase.ts` (ví dụ: `useFetchVehicles.ts`).
   - File Service: `[name].api.ts` (ví dụ: `vehicle.api.ts`).
4. **Clean Code & Typings**:
   - Định nghĩa đầy đủ `interface` cho tất cả các props và dữ liệu API. Hạn chế tối đa sử dụng kiểu `any`.
   - Giữ code ngắn gọn, chia nhỏ component nếu vượt quá 300 dòng code.
5. **Quy tắc Comment & JSDoc**:
   - Khi hoàn thành viết hoặc cập nhật code cho mỗi tính năng, bắt buộc phải viết comment mô tả mã nguồn theo quy chuẩn JSDoc bằng **tiếng Việt**.
   - Nội dung comment/JSDoc phải bao gồm thông tin tác giả và thời gian thực hiện:
     - Tác giả: **Ngọ Văn Quý**
     - Ngày thực hiện: **04/06/2026** (hoặc ngày hiện tại khi sửa đổi code).
     - Ví dụ:
       ```typescript
       /**
        * @description Hook custom xử lý lấy danh sách chuyến hàng của tài xế
        * @author Ngọ Văn Quý
        * @date 04/06/2026
        * @param {GetDriverShipmentsDto} query - Bộ lọc danh sách chuyến hàng
        * @returns Hook React Query chứa data chuyến hàng và trạng thái loading
        */
       ```

---

## 2. QUY TRÌNH THỰC HIỆN

1. Định nghĩa interfaces cho DTO, Request, Response trong thư mục `interfaces/` của module.
2. Viết API service trong thư mục `services/` (gọi http client `@/lib`).
3. Viết custom hooks trong `hooks/` để quản lý các query và mutation.
4. Tạo các Component con trong `components/` phục vụ hiển thị (bảng, form, bộ lọc).
5. Tạo hoặc cập nhật Page component trong `pages/` để lắp ráp các Component con.
6. Cập nhật router config trong `src/routes/` nếu cần khai báo đường dẫn trang mới.

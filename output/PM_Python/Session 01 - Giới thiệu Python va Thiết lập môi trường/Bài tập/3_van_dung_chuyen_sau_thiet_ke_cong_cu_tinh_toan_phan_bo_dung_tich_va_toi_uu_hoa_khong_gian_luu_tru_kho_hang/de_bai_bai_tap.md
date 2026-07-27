## <center>[Vận dụng chuyên sâu] Thiết kế công cụ tính toán phân bổ dung tích và tối ưu hóa không gian lưu trữ kho hàng</center>

### **1. Mục tiêu**
Học viên vận dụng tư duy phân tích hệ thống và kiến thức cơ bản trong Session 01 (Khai báo biến, kiểu dữ liệu cơ bản, nhập/xuất dữ liệu, ép kiểu và định dạng f-string) để tự thiết kế giải pháp và hiện thực hóa một chương trình tính toán hiệu suất sử dụng không gian kho hàng (Warehouse Space Utilization). Bài tập này giúp học viên hình thành tư duy phân rã bài toán nghiệp vụ logistics thực tế thành các công thức toán học và cấu trúc chương trình tuần tự mà không cần sử dụng các cấu trúc điều khiển nâng cao.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản lý kho hàng (Warehouse Management System - WMS), việc ước tính chính xác khả năng lưu trữ của kho và chi phí vận hành dự kiến đóng vai trò sống còn trước khi tiến hành xếp dỡ hàng hóa thực tế. Một kho hàng mới xây dựng cần được cấu hình các thông số vật lý cơ bản để xác định xem nó có thể chứa tối đa bao nhiêu pallet tiêu chuẩn sau khi đã trừ đi diện tích hao hụt cho lối đi của xe nâng, hành lang PCCC (Phòng cháy chữa cháy) và các cột trụ kỹ thuật.

Người quản lý kho cần một công cụ dòng lệnh (CLI Utility) nhanh chóng, cho phép nhập vào kích thước định danh của kho và kích thước của một pallet tiêu chuẩn, từ đó tự động tính toán dung tích thực tế, số lượng pallet tối đa có thể xếp và dự phóng doanh thu, lợi nhuận vận hành trên mỗi mét khối không gian khả dụng.



<p align="center">
  <img src="../images/bai_03_van_dung_chuyen_sau_thiet_ke_cong_cu_tinh_toan_phan_bo_dung_tich_va_toi_uu_hoa_khong_gian_luu_tru_kho_hang_diagram.png" alt="Sơ đồ luồng nghiệp vụ" width="80%">
</p>



### **3. Quy tắc nghiệp vụ**
Chương trình phải tính toán dựa trên các quy tắc và công thức nghiệp vụ sau:

1.  **Tính thể tích thô của kho hàng (Gross Volume - $V_{raw}$):**
    $$V_{raw} = Chiều\ dài \times Chiều\ rộng \times Chiều\ cao$$
    *(Đơn vị: mét khối - $m^3$)*

2.  **Tính thể tích lưu trữ hữu dụng (Usable Volume - $V_{usable}$):**
    Kho hàng bắt buộc phải dành ra một tỷ lệ không gian chết cố định là $38.5\%$ cho lối đi của xe nâng, hệ thống thông gió và hành lang an toàn PCCC. Do đó, tỷ lệ không gian hữu dụng cho phép đặt pallet chỉ chiếm $61.5\%$ ($0.615$) tổng thể tích thô.
    $$V_{usable} = V_{raw} \times 0.615$$

3.  **Tính thể tích của một pallet tiêu chuẩn ($V_{pallet}$):**
    $$V_{pallet} = Dài\ pallet \times Rộng\ pallet \times Cao\ pallet$$
    *(Đơn vị: mét khối - $m^3$)*

4.  **Tính sức chứa pallet tối đa (Maximum Pallet Capacity - $N_{max}$):**
    Số lượng pallet tối đa có thể xếp vào kho phải là một số nguyên (phần không gian thừa không đủ xếp một pallet nguyên vẹn sẽ bị bỏ qua).
    $$N_{max} = V_{usable} // V_{pallet}$$
    *(Sử dụng phép chia lấy phần nguyên)*

5.  **Dự phóng tài chính vận hành kho (Financial Projection):**
    *   Đơn giá thuê kho cố định trên thị trường: $25,000$ VND / $m^3$ / ngày.
    *   Doanh thu tối đa dự kiến của kho trong một tháng (tính tròn 30 ngày) khi lấp đầy 100% dung tích hữu dụng:
        $$Revenue = V_{usable} \times 25,000 \times 30$$
    *   Chi phí vận hành cố định (bảo vệ, điện nước, nhân công xếp dỡ) chiếm đúng $42\%$ doanh thu tối đa.
        $$Operating\_Cost = Revenue \times 0.42$$
    *   Lợi nhuận ròng dự kiến trước thuế:
        $$Profit = Revenue - Operating\_Cost$$

### **4. Yêu cầu đầu ra**

#### **Phần 1: Báo cáo phân tích và thiết kế giải pháp**
Trước khi viết mã nguồn, học viên phải tạo một tài liệu phân tích ngắn gọn thực hiện các nội dung sau:
*   [Yêu cầu 1.1] Xác định cấu trúc Input/Output: Liệt kê danh sách các biến cần nhập từ người dùng (kèm kiểu dữ liệu mong muốn sau khi ép kiểu) và các thông số đầu ra cần tính toán.
*   [Yêu cầu 1.2] Mã giả (Pseudocode): Viết các bước thực hiện tuần tự của chương trình từ khâu bắt đầu nhập liệu, các bước trung gian xử lý toán học cho đến khâu in báo cáo.

#### **Phần 2: Hiện thực hóa mã nguồn Python**
Học viên viết chương trình Python hoàn chỉnh (ví dụ lưu trong file `warehouse_calculator.py`) thực thi theo đúng thiết kế:
*   [Yêu cầu 2.1] Cho phép người dùng nhập trực tiếp 6 thông số đầu vào từ bàn phím bằng hàm `input()`.
*   [Yêu cầu 2.2] Thực hiện ép kiểu dữ liệu phù hợp (sang kiểu số thực `float`) để phục vụ tính toán.
*   [Yêu cầu 2.3] Áp dụng các toán tử số học cơ bản để tính toán các thông số theo quy tắc nghiệp vụ.
*   [Yêu cầu 2.4] Xuất báo cáo kết quả ra màn hình bằng kỹ thuật định dạng chuỗi `f-string`. Báo cáo phải được căn lề thẳng hàng, trình bày chuyên nghiệp. Các số liệu về kích thước và thể tích phải làm tròn đúng 2 chữ số thập phân. Các số liệu về doanh thu, chi phí, lợi nhuận và số lượng pallet phải hiển thị dưới dạng số nguyên (`int`).

**Ví dụ trực quan về luồng dữ liệu:**

*Dữ liệu nhập vào tham khảo từ bàn phím:*
```text
Nhập chiều dài kho hàng (m): 50.0
Nhập chiều rộng kho hàng (m): 20.0
Nhập chiều cao kho hàng (m): 8.5
Nhập chiều dài pallet (m): 1.2
Nhập chiều rộng pallet (m): 1.0
Nhập chiều cao pallet (m): 1.5
```

*Dự kiến kết quả hiển thị trên màn hình:*
```text
============================================================
              BÁO CÁO PHÂN BỔ DUNG TÍCH KHO HÀNG            
============================================================
KÍCH THƯỚC VÀ DUNG TÍCH:
- Thể tích thô của kho: 8500.00 m3
- Thể tích hữu dụng (61.5%): 5227.50 m3
- Thể tích của một pallet: 1.80 m3
- Khả năng lưu trữ tối đa: 2904 pallet

DỰ PHÒNG TÀI CHÍNH VẬN HÀNH (30 NGÀY):
- Doanh thu tối đa dự kiến: 3,920,625,000 VND
- Chi phí vận hành dự kiến (42%): 1,646,662,500 VND
- Lợi nhuận ròng dự kiến: 2,273,962,500 VND
============================================================
```
[NOTE] Sinh viên chỉ cần định dạng chuỗi hiển thị số nguyên cho phần tài chính mà không bắt buộc phải hiển thị dấu phân cách hàng nghìn `,` nếu kiến thức định dạng f-string nâng cao chưa tự tìm hiểu được. Nếu hiển thị được dấu phân cách hàng nghìn (ví dụ dùng cấu trúc `{bien_so:,.0f}` hoặc tương đương), sinh viên sẽ được tính điểm cộng tối đa.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Bản phân tích thiết kế (File MD hoặc tài liệu thiết kế PDF/TXT).
*   Mã nguồn hoàn chỉnh từ đầu (File `.py`).
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session01_Ex03`.
    Ví dụ: `HNKS25CNTT1_PythonCore_Session01_Ex03`
# TAI LIEU HUONG DAN 03: BUOC 2 - SINH BAI DOC HTML & MASTER HUB

## 1. Muc Dich
Tao ra cac tep bai doc `reading.html` theo chuan giao dien nen sang hien dai, tich hop trinh chay Python truc tiep tren trinh duyet (Pyodide Wasm Sandbox), so do Mermaid va cac cau hoi tu danh gia (Interactive Self-Test).

---

## 2. Cac Tieu Chuan Bat Buoc Cua Bai Doc (`reading.html`)

1. **Giao Dien Nen Sang & Typography**:
   - Su dung font chu Inter & Montserrat cao cap.
   - Mau sac chu dao: Do thuong hieu Rikkei (`#be111c`).
2. **Trinh Chay Code Truc Tiep (Pyodide Wasm Sandbox)**:
   - Cho phep hoc vien thuc thi ma nguon truc tiep tren trinh duyet ma khong can cai dat runtime.
3. **High-Contrast Code Trackers**:
   - Dong highlight code su dung nen ro rang va chu dam noi bat 100%.
4. **Can Trai Tuyet Doi Cho Self-Test Accordion (.selftest-question)**:
   - Cac cau hoi va dap an tu kiem tra bat buoc su dung `text-align: left !important;` va `justify-content: flex-start !important;`.
5. **Tieng Viet Co Dau Nghiem Ngat**:
   - Tat ca van ban, nhan SVG, node Mermaid phai dung dung dau tieng Viet (NFC Unicode).

---

## 3. Quy Trinh Bien Dich Master Reading Hub (`reading_all.html`)

Sau khi sinh xong cac bai doc thanh phan, `compile_session_html` se gop toan bo thanh tep Master Dashboard:
```bash
python -c "from pathlib import Path; from core.session_compilers import compile_session_html; compile_session_html(Path(r'output/pms/PM_Python/Session 01'), 'Session 01 - Gioi thieu Python')"
```

### Dac Diem Cua `reading_all.html`:
- Thanh Header co dinh chua Logo chinh thuc Rikkei Education.
- Sticky Left Sidebar chua tab chuyen doi muot ma giua cac bai hoc.
- Dat 100% DOM & JavaScript Isolation Verified.
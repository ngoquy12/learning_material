# TAI LIEU HUONG DAN 02: BUOC 1 - NAP & KIEM DINH FILE PM EXCEL (PM AUDITOR GATE)

## 1. Muc Dich
Tu dong hoa viec nap file khung chuong trinh PM (`PM_Python.xlsx`), danh gia tinh hop ly su pham, phat hien lo hong nhay coc kien thuc va ho tro AI tu dong cap nhat file Excel PM.

---

## 2. Cau Truc File Excel PM Dau Vao
Tep Excel PM dat tai thu muc `documents/PM_Python.xlsx` chua cac cot thong tin:
- **Session ID**: Ten buoi hoc (vi du: `Session 06`)
- **Session Title**: Chu de buoi hoc (vi du: `Cau truc du lieu List va Tuple`)
- **Lesson ID**: Ten bai hoc (vi du: `Lesson 01`)
- **Lesson Title**: Tieu de bai hoc (`Khai niem List va cach khoi tao`)
- **Details & Objectives**: Mo ta chi tiet va chuan dau ra bai hoc.

---

## 3. Quy Trinh Thuc Thi Buoc PM

### Buoc 3.1: Chay Lenh Quet & Danh Gia PM
```bash
python main.py --pm "documents/PM_Python.xlsx" --approve-pm
```

### Buoc 3.2: Co Che Danh Gia Cua PM Auditor Agent
Agent se phan tich 4 tieu chi cot loi:
1. **Phan ra bai hoc**: Cac Lesson co du do sau va ro chuan dau ra hay chua?
2. **Tai luong nhan thuc**: Co bai nao nhoi nhet qua nhieu kien thuc phuc tap khong?
3. **Lo hong Nhay coc (Prerequisites)**: Kien thuc cac bai co moc xich logic khong?
4. **Bao cao kiem dinh**: Xuat bao cao chi tiet tai `output/pms/<Course>/structure_review_report.md`.

### Buoc 3.3: AI Auto-Updater (Tu Dong Sua Excel)
Khi phat hien loi cau truc, Agent `pm_updater_agent` se tu dong de xuat sua doi va cap nhat lai file PM.

---

## 4. Quy Tac Phe Duyet (Approval Checklist)
- Co `--approve-pm` mo khoa cho cac Agent phia sau (Reading, Quiz, Slide, Homework) tiep tuc khoi chay.
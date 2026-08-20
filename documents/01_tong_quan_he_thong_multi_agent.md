# TAI LIEU HUONG DAN 01: TONG QUAN HE THONG MULTI-AGENT HARNESS

## 1. Gioi Thieu He Thong
He thong **Multi-Agent Elearning Content Factory** la nen tang tu dong hoa san xuat hoc lieu E-learning toan dien chuan doanh nghiep do Rikkei Education phat trien. He thong tich hop cac AI Agents chuyen biet phoi hop theo do thi trang thai (**Asynchronous DAG & State Machine**) de sinh hoc lieu chuan SEO, chuan su pham va chuan doanh nghiep cho moi ngon ngu lap trinh va cong nghe.

---

## 2. Kien Truc Cac Agents Trong He Thong

```mermaid
flowchart TD
    PM["PM Excel / Syllabus JSON"] --> A1["PM Auditor & Scope Calculator<br>(Kiem tra & Phan dinh pham vi kien thuc)"]
    A1 --> A2["Reading Generator Agent<br>(Bai doc chuan 5 phan, Pyodide Wasm Sandbox)"]
    A2 --> A3["Slide Deck Generator Agent<br>(PowerPoint .pptx & Master HTML Slides)"]
    A2 --> A4["Quiz & Homework Suite Agent<br>(Quiz Excel 45 cau & 17 Thu muc bai tap Bloom)"]
    A2 --> A5["Session Compiler Agent<br>(reading_all.html & Obsidian Knowledge Graph)"]
    A2 --> A6["SCORM 1.2 Exporter Agent<br>(Goi ZIP LMS Moodle, Canvas)"]
    
    A2 -.-> R["Reviewer & Reflexion Loop<br>(Tu dong kiem dinh & sua loi vi pham)"]
    R -.-> A2
```

### Cac Agent Chinh Va Vai Tro:
1. **PM Auditor & Scope Calculator Agent**: Quet file chuong trinh khung, phan dinh pham vi kien thuc dong (Dynamic Scope Boundaries), ngan chan hien tuong nhay coc kien thuc.
2. **Reading Generator Agent**: Bien soan Bai doc HTML (`reading.html`) theo cau truc 5 phan chuan hoa, tich hop Pyodide Wasm Sandbox, Mermaid Flowchart 5 hinh khoi chuan va Interactive Self-Test.
3. **Slide Deck Generator Agent**: Tu dong tao Slide bai giang PowerPoint chuyen nghiep (`Slide_Bai_Giang.pptx`) va Slide HTML tuong tac (`slides.html`) kem Outline su pham cho giang vien.
4. **Quiz & Homework Agent**: Sinh Quiz dau gio/cuoi gio (45 cau Excel `.xlsx`) va bo 17 bai tap phan cap theo thang nhan thuc Bloom, co tieu chi cham diem chi tiet 100 diem (`tieu_chi_danh_gia.md`).
5. **Session Compiler Agent**: Gop tat ca bai doc thanh Master Hub `reading_all.html` voi sticky sidebar navigation va lien ket Obsidian Knowledge Graph 2 chieu.
6. **Master Reviewer & Reflexion Engine**: Tu dong kiem tra chat luong (PQM Engine, Bloom alignment, khong dung AI cliche) va kich hoat vong lap tu sua loi khi phat hien sai pham.
7. **SCORM 1.2 Exporter**: Dong goi chuan e-learning quoc te tuong thich 100% voi LMS doanh nghiep.

---

## 3. Cau Truc Thu Muc Hoc Lieu Dau Ra Chuan (`output/pms/`)

```
output/pms/<Ten_Khoa_Hoc>/
├── Session 01 - <Ten_Session>/
│   ├── Lesson 01 - <Ten_Lesson>/
│   │   ├── Bai doc/ (reading.html)
│   │   ├── Bai thuc hanh/ (practical_lab.md, practical_lab.json)
│   │   ├── Cau hoi Quizz/ (Quizz_Session01_Lesson01.xlsx, quiz.json)
│   │   └── Cau hoi bai doc/ (reading_questions.md, reading_questions.json)
│   ├── Slide bai giang/
│   │   ├── Slide_Bai_Giang_Session_01.pptx
│   │   ├── outline_bai_giang.md
│   │   └── slide_deck_review_report.md
│   ├── Bai tap/
│   │   ├── tieu_chi_danh_gia.md (Bang rubric tong hop 100 diem)
│   │   ├── 1_van_dung_co_ban_1_.../ (de_bai_bai_tap.md, tieu_chi_cham_diem_ai.md)
│   │   ├── 2_van_dung_co_ban_2_.../
│   │   ├── ...
│   │   └── 17_tong_hop_he_thong_kien_thuc_mindmap/
│   ├── Mindmap/ (session_mindmap.md)
│   ├── Session 01._Quizz_Dau_Gio_*.xlsx
│   └── Session 01._Quizz_Cuoi_Gio_*.xlsx
└── structure_review_report.md
```
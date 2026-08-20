# TAI LIEU HUONG DAN 06: HUONG DAN SU DUNG LENH CLI & CONG CU VAN HANH (DA KIEM CHUNG)

Tai lieu nay cung cap danh sach day du cac cau lenh CLI da duoc **kiem chung thuc te (verified & tested)** tren moi truong he thong.

---

## 1. Kiem Tra Trang Thai & Cau Hinh He Thong

### 1.1. Xem Tro Giup & Danh Sach Tuy Chon CLI
```bash
python main.py --help
```
*Tac dung: Hien thi toan bo co tuy chon (options) va mo ta cach su dung cua he thong.*

### 1.2. Kiem Tra Thong Ke Semantic Cache
```bash
python main.py --cache-stats
```
*Tac dung: Thong ke so luong response da cache, so lan cache hit va uoc tinh token tiet kiem duoc.*

### 1.3. Kiem Tra Cau Hinh Centralized Settings & Secrets
```bash
python -c "from config.settings import get_settings; import json; print(json.dumps(get_settings().redacted_dict(), indent=2))"
```
*Tac dung: Kiem tra toan bo tham so moi truong va dam bao API Key duoc che giau an toan (`***REDACTED***`).*

---

## 2. Lenh Sinh Hoc Lieu Chinh (Content Generation Workflows)

### 2.1. Sinh Toan Bo Hoc Lieu Cho 1 Session Cu The
```bash
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --approve-pm
```

### 2.2. Sinh Toan Bo Khoa Hoc (All Sessions)
```bash
python main.py --pm "documents/PM_Python.xlsx" --session all --approve-pm
```

### 2.3. Sinh Chon Loc Tung Loai Hoc Lieu (Selective Generation)
Su dung co `--parts` voi danh sach phan tach bang dau phay (`html`, `slide`, `quiz`, `practical_lab`):
```bash
# Chi sinh Bai doc HTML va Slide bai giang:
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parts html,slide --approve-pm

# Chi sinh Bai tap & Bo Quiz trac nghiem 45 cau:
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parts quiz,practical_lab --approve-pm
```

### 2.4. Chay Xu Ly Bat Dong Bo Song Song (Async Parallel Batch Mode)
Kich hoat chay song song cac Lesson doc lap trong Session de tang toc do sinh hoc lieu:
```bash
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parallel --concurrency 4 --approve-pm
```

### 2.5. Khoi Tao Nhanh Cay Cau Truc Thu Muc (Scaffolding Mode)
Khoi tao cau truc thu muc rong chuan hoa tu file PM ma khong can goi LLM sinh noi dung chi tiet:
```bash
python main.py --pm "documents/PM_Python.xlsx" --scaffold
```

---

## 3. Lenh Dong Goi Xuat Ban (Export LMS & Obsidian Vault)

### 3.1. Xuat Ban Goi SCORM 1.2 Cho He Thong LMS (Moodle / Canvas)
```bash
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --scorm --approve-pm
```
*Ket qua: Tao file nen `.zip` chuan SCORM 1.2 san sang import vao LMS.*

### 3.2. Xuat Ban Do Thi Tri Thuc Obsidian Vault
```bash
python main.py --pm "documents/PM_Python.xlsx" --obsidian
```
*Ket qua: Dong bo toan bo lien ket 2 chieu va the bai hoc vao thu muc `obsidian_vault/`.*

---

## 4. Lenh Kiem Thu & Chan Doan Loi (Testing & Core Verification)

### 4.1. Chay Toan Bo Test Suite (159 Tests)
```bash
pytest
```

### 4.2. Chay Kiem Thu Rieng Cho Tung Module
```bash
# Kiem thu Quan ly Cau hinh & Bao mat:
pytest tests/test_centralized_settings.py -v

# Kiem thu Dong co Chan ro ri kien thuc (Scope Calculator):
pytest tests/test_scope_calculator.py -v

# Kiem thu Dong co Sinh Slide PowerPoint:
pytest tests/test_slide_deck_generator.py -v
```

### 4.3. Kiem Tra Truc Tiep Cac Module Core Qua Python CLI
```bash
# Kiem tra danh sach framework bi cam theo Tech Stack:
python -c "from core.scope_calculator import get_forbidden_frameworks_for_stack; print(get_forbidden_frameworks_for_stack('python/core'))"

# Kiem tra phan loai Tier cua Agent trong LLM Router:
python -c "from core.llm_router import AntigravityLLMRouter; print(AntigravityLLMRouter.classify_agent_tier('reading_creator'))"
```
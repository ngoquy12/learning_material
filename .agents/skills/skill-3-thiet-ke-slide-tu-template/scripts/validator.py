import re, glob, sys

SLIDES_DIR = "unpacked/ppt/slides"

# ==== ĐIỀN THEO DESIGN TOKENS ĐÃ TRÍCH Ở GIAI ĐOẠN 1 (không để mặc định
#      nếu template có giá trị khác) ====
SZ_H1 = 2800          # cỡ chữ H1 x100 (VD 2800 = 28pt)
SZ_H2 = 2000
SZ_BODY = 1800
SZ_SMALL_MIN, SZ_SMALL_MAX = 1400, 1600
SZ_AGENDA = 2400
ADJ_NORMAL = 4000     # bo góc khối thường, theo mục 1.4
ADJ_OVAL = 50000      # cố định, không đổi theo template
BRAND_COLOR = "C00000"  # màu chủ đạo đã trích ở mục 1.1
BORDER_NEUTRAL = "D9D9D9"
TEMPLATE_NATIVE_LABELS = set()  # điền các nhãn ALL CAPS có sẵn trong template gốc, nếu có

FAIL = []
def check(desc, condition):
    status = "PASS" if condition else "FAIL"
    if not condition: FAIL.append(desc)
    print(f"[{status}] {desc}")

files = sorted(glob.glob(f"{SLIDES_DIR}/slide*.xml"))
all_xml = {f: open(f, encoding="utf-8").read() for f in files}

# 1) Cấm spcPts làm cơ chế line-spacing
bad = [f for f, c in all_xml.items() if "<a:lnSpc><a:spcPts" in c]
check(f"Không còn <a:lnSpc><a:spcPts> — {len(bad)} file lỗi", len(bad) == 0)

# 2) Placeholder rỗng
empty_ph = []
for f, c in all_xml.items():
    for m in re.finditer(r'<p:sp>((?:(?!</p:sp>).)*?<p:ph[^/]*/>(?:(?!</p:sp>).)*?)</p:sp>', c, re.S):
        if '<a:t>' not in m.group(1):
            empty_ph.append(f)
check(f"Không còn placeholder rỗng — {len(empty_ph)} chỗ lỗi", len(empty_ph) == 0)

# 3) adj bo góc chỉ ADJ_NORMAL hoặc ADJ_OVAL
bad_adj = []
for f, c in all_xml.items():
    for m in re.finditer(r'fmla="val (\d+)"', c):
        v = int(m.group(1))
        if v not in (ADJ_NORMAL, ADJ_OVAL, 9000, 0):
            bad_adj.append((f, v))
check(f"Mọi adj chỉ {ADJ_NORMAL} hoặc {ADJ_OVAL} — {len(bad_adj)} giá trị lạ", len(bad_adj) == 0)

# 4) ALL CAPS tự soạn (loại trừ nhãn thương hiệu gốc)
import unicodedata
all_caps_hits = []
NATIVE_NORM = {unicodedata.normalize("NFC", s) for s in TEMPLATE_NATIVE_LABELS}
for f, c in all_xml.items():
    for m in re.finditer(r'<a:t>([^<]+)</a:t>', c):
        t = m.group(1)
        if unicodedata.normalize("NFC", t.strip()) in NATIVE_NORM:
            continue
        letters = re.sub(r'[^A-Za-zÀ-ỹ]', '', t)
        if len(letters) >= 6 and letters == letters.upper() and letters != letters.lower():
            all_caps_hits.append((f, t))
check(f"Không còn ALL CAPS tự soạn — {len(all_caps_hits)} chỗ: {all_caps_hits[:10]}", len(all_caps_hits) == 0)

# 5) Viền màu chủ đạo dùng cho container thường — chỉ IN RA để soát thủ công
#    (không tự động phân biệt được container thường vs flowchart hợp lệ)
red_borders = []
for f, c in all_xml.items():
    for m in re.finditer(r'<p:sp>((?:(?!</p:sp>).)*?)</p:sp>', c, re.S):
        seg = m.group(1)
        if 'diamond' in seg or 'straightConnector' in seg:
            continue
        if re.search(rf'<a:ln[^>]*><a:solidFill><a:srgbClr val="{BRAND_COLOR}"', seg) and 'roundRect' in seg:
            name = re.search(r'name="([^"]*)"', seg)
            red_borders.append((f, name.group(1) if name else "?"))
print(f"[INFO] Shape dùng viền màu chủ đạo (soát thủ công xem có phải flowchart hợp lệ không): {len(red_borders)}")

print("\n=== TỔNG KẾT ===")
if FAIL:
    print(f"CÒN {len(FAIL)} MỤC FAIL — SỬA XONG MỚI XUẤT ẢNH/GIAO FILE.")
    sys.exit(1)
else:
    print("TẤT CẢ KIỂM TRA ĐỊNH LƯỢNG CHÍNH ĐỀU PASS.")
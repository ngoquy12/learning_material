"""Vietnamese Text Normalization (TN) for TTS.
Converts numbers, dates, times, currencies, units, and common Vietnamese abbreviations to spoken Vietnamese text.
"""

from __future__ import annotations

import re

UNITS_MAP = [
    ("", ""),
    ("một", "mốt"),
    ("hai", "hai"),
    ("ba", "ba"),
    ("bốn", "bốn"),
    ("năm", "lăm"),
    ("sáu", "sáu"),
    ("bảy", "bảy"),
    ("tám", "tám"),
    ("chín", "chín"),
]

DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def number_to_words(n: int) -> str:
    """Converts a non-negative integer to Vietnamese words."""
    if n == 0:
        return "không"

    if n < 10:
        return DIGITS[n]

    if n < 100:
        ten = n // 10
        unit = n % 10
        ten_str = "mười" if ten == 1 else f"{DIGITS[ten]} mươi"
        if unit == 0:
            return ten_str
        if unit == 1 and ten > 1:
            unit_str = "mốt"
        elif unit == 4 and ten > 1:
            unit_str = "tư"
        elif unit == 5:
            unit_str = "lăm"
        else:
            unit_str = DIGITS[unit]
        return f"{ten_str} {unit_str}"

    if n < 1000:
        hundred = n // 100
        remainder = n % 100
        hundred_str = f"{DIGITS[hundred]} trăm"
        if remainder == 0:
            return hundred_str
        if remainder < 10:
            return f"{hundred_str} lẻ {DIGITS[remainder]}"
        return f"{hundred_str} {number_to_words(remainder)}"

    if n < 1_000_000:
        thousand = n // 1000
        remainder = n % 1000
        thousand_str = f"{number_to_words(thousand)} nghìn"
        if remainder == 0:
            return thousand_str
        if remainder < 100:
            if remainder < 10:
                return f"{thousand_str} không trăm lẻ {DIGITS[remainder]}"
            return f"{thousand_str} không trăm {number_to_words(remainder)}"
        return f"{thousand_str} {number_to_words(remainder)}"

    if n < 1_000_000_000:
        million = n // 1_000_000
        remainder = n % 1_000_000
        million_str = f"{number_to_words(million)} triệu"
        if remainder == 0:
            return million_str
        return f"{million_str} {number_to_words(remainder)}"

    billion = n // 1_000_000_000
    remainder = n % 1_000_000_000
    billion_str = f"{number_to_words(billion)} tỷ"
    if remainder == 0:
        return billion_str
    return f"{billion_str} {number_to_words(remainder)}"


def _replace_number_match(match: re.Match) -> str:
    num_str = match.group(0).replace(".", "").replace(",", "")
    try:
        val = int(num_str)
        return number_to_words(val)
    except ValueError:
        return match.group(0)


# Comprehensive Production Vietnamese & Tech Abbreviations Rules
# Format: (pattern, replacement, flags)
ABBREVIATIONS_RULES = [
    # ----------------------------------------------------
    # 1. Công nghệ & CNTT (Technology & Computing) - Case-sensitive
    # ----------------------------------------------------
    (r"\bA\.?I\.?\b", "ây ai", 0),
    (r"\bA\.?P\.?I\.?\b", "ây pi ai", 0),
    (r"\bI\.?T\.?\b", "ai ti", 0),
    (r"\bU\.?I\.?\b", "ju ai", 0),
    (r"\bU\.?X\.?\b", "ju ích", 0),
    (r"\bC\.?P\.?U\.?\b", "xi pi u", 0),
    (r"\bG\.?P\.?U\.?\b", "gi pi u", 0),
    (r"\bI\.?P\.?\b", "ai pi", 0),
    (r"\bO\.?S\.?\b", "ô ét", 0),
    (r"\bP\.?C\.?\b", "pi si", 0),
    (r"\bU\.?R\.?L\.?\b", "u rờ el", 0),
    (r"\bD\.?N\.?S\.?\b", "đê en ét", 0),
    (r"\bS\.?M\.?S\.?\b", "ét em ét", 0),
    (r"\bP\.?D\.?F\.?\b", "pê đê ép", 0),
    (r"\bH\.?T\.?M\.?L\.?\b", "hát tê em el", 0),
    (r"\bC\.?S\.?S\.?\b", "xi ét ét", 0),
    (r"\bJ\.?S\.?\b", "gây ét", 0),
    (r"\bV\.?I\.?P\.?\b", "víp", re.IGNORECASE),
    (r"\bWi-?Fi\b", "oai fai", re.IGNORECASE),
    (r"\bBluetooth\b", "blu tút", re.IGNORECASE),
    (r"\bApp\b", "áp", re.IGNORECASE),
    (r"\bWeb\b", "wép", re.IGNORECASE),
    (r"\bBot\b", "bốt", re.IGNORECASE),
    (r"\bRam\b", "ram", re.IGNORECASE),
    (r"\bRom\b", "rom", re.IGNORECASE),
    (r"\bSim\b", "sim", re.IGNORECASE),
    (r"\b4G\b", "bốn gơ", re.IGNORECASE),
    (r"\b5G\b", "năm gơ", re.IGNORECASE),

    # ----------------------------------------------------
    # 2. Hành chính & Chính trị & Chức danh (Administration & Titles)
    # ----------------------------------------------------
    (r"\bUBND\b", "ủy ban nhân dân", re.IGNORECASE),
    (r"\bHĐND\b", "hội đồng nhân dân", re.IGNORECASE),
    (r"\bHDND\b", "hội đồng nhân dân", re.IGNORECASE),
    (r"\bBCH\b", "ban chấp hành", re.IGNORECASE),
    (r"\bTW\b", "trung ương", re.IGNORECASE),
    (r"\bTƯ\b", "trung ương", re.IGNORECASE),
    (r"\bBHXH\b", "bảo hiểm xã hội", re.IGNORECASE),
    (r"\bBHYT\b", "bảo hiểm y tế", re.IGNORECASE),
    (r"\bPCCC\b", "phòng cháy chữa cháy", re.IGNORECASE),
    (r"\bCSGT\b", "cảnh sát giao thông", re.IGNORECASE),
    (r"\bCAND\b", "công an nhân dân", re.IGNORECASE),
    (r"\bQĐND\b", "quân đội nhân dân", re.IGNORECASE),
    (r"\bBQP\b", "bộ quốc phòng", re.IGNORECASE),
    (r"\bBCA\b", "bộ công an", re.IGNORECASE),
    (r"\bBYT\b", "bộ y tế", re.IGNORECASE),
    (r"\bBGDĐT\b", "bộ giáo dục và đào tạo", re.IGNORECASE),
    (r"\bGS\.?\b", "giáo sư", re.IGNORECASE),
    (r"\bP\.?GS\.?\b", "phó giáo sư", re.IGNORECASE),
    (r"\bTS\.?\b", "tiến sĩ", re.IGNORECASE),
    (r"\bThS\.?\b", "thạc sĩ", re.IGNORECASE),
    (r"\bBS\.?\b", "bác sĩ", re.IGNORECASE),
    (r"\bNSND\b", "nghệ sĩ nhân dân", re.IGNORECASE),
    (r"\bNSƯT\b", "nghệ sĩ ưu tú", re.IGNORECASE),
    

    # ----------------------------------------------------
    # 3. Địa danh & Đơn vị hành chính (Geography & Locations)
    # ----------------------------------------------------
    (r"\bTP\.?\s*HCM\b", "thành phố hồ chí minh", re.IGNORECASE),
    (r"\bTPHCM\b", "thành phố hồ chí minh", re.IGNORECASE),
    (r"\bTP\.?\s*Hà Nội\b", "thành phố hà nội", re.IGNORECASE),
    (r"\bHN\b", "hà nội", 0),
    (r"\bĐN\b", "đà nẵng", 0),
    (r"\bHP\b", "hải phòng", 0),
    (r"\bCT\b", "cần thơ", 0),
    (r"\bQN\b", "quảng ninh", 0),
    (r"\bBD\b", "bình dương", 0),
    (r"\bQ\.?\s*(\d+)\b", r"quận \1", re.IGNORECASE),
    (r"\bP\.?\s*(\d+)\b", r"phường \1", re.IGNORECASE),

    # ----------------------------------------------------
    # 4. Giáo dục & Trường học (Education & Schools)
    # ----------------------------------------------------
    (r"\bTHPT\b", "trung học phổ thông", re.IGNORECASE),
    (r"\bTHCS\b", "trung học cơ sở", re.IGNORECASE),
    (r"\bĐH\b", "đại học", re.IGNORECASE),
    (r"\bCĐ\b", "cao đẳng", re.IGNORECASE),
    (r"\bGDĐT\b", "giáo dục đào tạo", re.IGNORECASE),
    (r"\bCLB\b", "câu lạc bộ", re.IGNORECASE),
    (r"\bHV\b", "học viện", re.IGNORECASE),

    # ----------------------------------------------------
    # 5. Kinh tế, Tài chính & Doanh nghiệp (Finance & Business)
    # ----------------------------------------------------
    (r"\bVNĐ\b", "đồng", re.IGNORECASE),
    (r"\bVND\b", "đồng", re.IGNORECASE),
    (r"\bUSD\b", "đô la", re.IGNORECASE),
    (r"\bEUR\b", "ơ rơ", re.IGNORECASE),
    (r"\bTNHH\b", "trách nhiệm hữu hạn", re.IGNORECASE),
    (r"\bCP\b", "cổ phần", 0),
    (r"\bCty\b", "công ty", re.IGNORECASE),
    (r"\bCTY\b", "công ty", re.IGNORECASE),
    (r"\bDNTN\b", "doanh nghiệp tư nhân", re.IGNORECASE),
    (r"\bVAT\b", "vát", re.IGNORECASE),
    (r"\bGDP\b", "gi đi pi", re.IGNORECASE),
    (r"\bWTO\b", "dáp lưu tê ô", re.IGNORECASE),
    (r"\bCEO\b", "si i ô", re.IGNORECASE),
    (r"\bCFO\b", "xi ép ô", re.IGNORECASE),
    (r"\bHR\b", "át rờ", re.IGNORECASE),
    (r"\bPR\b", "pi ar", re.IGNORECASE),
    (r"\bKPI\b", "kei pi ai", re.IGNORECASE),

    # ----------------------------------------------------
    # 6. Truyền thông, Mạng xã hội & Giải trí (Media & Entertainment)
    # ----------------------------------------------------
    (r"\bVTV1\b", "vê tê vê một", re.IGNORECASE),
    (r"\bVTV2\b", "vê tê vê hai", re.IGNORECASE),
    (r"\bVTV3\b", "vê tê vê ba", re.IGNORECASE),
    (r"\bVTV6\b", "vê tê vê sáu", re.IGNORECASE),
    (r"\bVTV\b", "vê tê vê", re.IGNORECASE),
    (r"\bHTV\b", "hát tê vê", re.IGNORECASE),
    (r"\bVOV\b", "vê o vê", re.IGNORECASE),
    (r"\bFacebook\b", "phây búc", re.IGNORECASE),
    (r"\bFB\b", "phây búc", 0),
    (r"\bZalo\b", "za lô", re.IGNORECASE),
    (r"\bYouTube\b", "ju tuýp", re.IGNORECASE),
    (r"\bTikTok\b", "tíc tót", re.IGNORECASE),
    (r"\bMC\b", "em si", re.IGNORECASE),
    (r"\bMV\b", "em vi", re.IGNORECASE),

    # ----------------------------------------------------
    # 7. Viết tắt nhắn tin & Giao tiếp mạng (Chat & Daily Written)
    # ----------------------------------------------------
    (r"\bđc\b", "được", re.IGNORECASE),
    (r"\bdc\b", "được", 0),
    (r"\bko\b", "không", re.IGNORECASE),
    (r"\bkh\b", "không", 0),
    (r"\bmn\b", "mọi người", 0),
    (r"\bsp\b", "sản phẩm", 0),
    (r"\binbox\b", "in bốc", re.IGNORECASE),
    (r"\bib\b", "in bốc", 0),
]


import json
import os

_TECH_DICT_CACHE = None

def get_tech_dictionary() -> dict:
    global _TECH_DICT_CACHE
    if _TECH_DICT_CACHE is not None:
        return _TECH_DICT_CACHE
    
    _TECH_DICT_CACHE = {}
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "configs", "tech_dictionary.json"),
        os.path.join(os.path.dirname(__file__), "..", "configs", "tech_dictionary.json"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../configs/tech_dictionary.json")),
    ]
    for path in possible_paths:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    _TECH_DICT_CACHE = data.get("entries", {})
                    break
            except Exception:
                pass
    return _TECH_DICT_CACHE


def normalize_vietnamese_text(text: str) -> str:
    """Normalizes raw Vietnamese text into spoken text format."""
    if not text:
        return ""

    normalized = text

    # 0. Tech Dictionary Auto-Phonetic Replacement (Training Dictionary)
    tech_dict = get_tech_dictionary()
    for term, phonetic in sorted(tech_dict.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r"\b" + re.escape(term) + r"\b"
        normalized = re.sub(pattern, phonetic, normalized)

    # 1. Date format: DD/MM/YYYY or DD-MM-YYYY
    def _date_repl(m: re.Match) -> str:
        day = number_to_words(int(m.group(1)))
        month = number_to_words(int(m.group(2)))
        year = number_to_words(int(m.group(3)))
        return f"ngày {day} tháng {month} năm {year}"

    normalized = re.sub(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b", _date_repl, normalized)

    # 2. Time format: HH:MM or HHhMM
    def _time_repl(m: re.Match) -> str:
        hour = number_to_words(int(m.group(1)))
        minute = int(m.group(2))
        if minute == 0:
            return f"{hour} giờ"
        return f"{hour} giờ {number_to_words(minute)} phút"

    normalized = re.sub(r"\b(\d{1,2})[h:](\d{2})\b", _time_repl, normalized, flags=re.IGNORECASE)

    # 3. Currency / Money shortcuts (e.g. 100k USD, 100kđ, 500tr, 10 tỷ)
    def _money_k_repl(m: re.Match) -> str:
        val = number_to_words(int(m.group(1)))
        currency = (m.group(2) or "").strip().lower()
        if currency in ("usd", "$", "đô la"):
            return f"{val} nghìn đô la"
        if currency in ("đ", "đ", "vnđ", "vnd", "đồng"):
            return f"{val} nghìn đồng"
        return f"{val} nghìn"

    normalized = re.sub(r"\b(\d+)\s*[kK]\s*(usd|\$|đ|đ|vnđ|vnd|đô la|đồng)?\b", _money_k_repl, normalized, flags=re.IGNORECASE)

    def _money_tr_repl(m: re.Match) -> str:
        val = number_to_words(int(m.group(1)))
        currency = (m.group(2) or "").strip().lower()
        if currency in ("usd", "$", "đô la"):
            return f"{val} triệu đô la"
        return f"{val} triệu đồng"

    normalized = re.sub(r"\b(\d+)\s*(?:tr|triệu)\s*(usd|\$|đ|đ|vnđ|vnd|đô la|đồng)?\b", _money_tr_repl, normalized, flags=re.IGNORECASE)

    # 4. Units (km, m, cm, mm, kg, g, °C, %)
    normalized = re.sub(r"(\d+)\s*% ", r"\1 phần trăm ", normalized)
    normalized = re.sub(r"(\d+)\s*%", r"\1 phần trăm", normalized)
    normalized = re.sub(r"(\d+)\s*°C\b", r"\1 độ cê", normalized)
    normalized = re.sub(r"(\d+)\s*km\b", r"\1 ki lô mét", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"(\d+)\s*kg\b", r"\1 ki lô gam", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"(\d+)\s*cm\b", r"\1 xen ti mét", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"(\d+)\s*m\b", r"\1 mét", normalized, flags=re.IGNORECASE)

    # 5. Abbreviations & Tech Acronyms
    for item in ABBREVIATIONS_RULES:
        if len(item) == 3:
            pattern, repl, flags = item
        else:
            pattern, repl = item
            flags = re.IGNORECASE
        normalized = re.sub(pattern, repl, normalized, flags=flags)

    # 6. Vietnamese Thousand Separators (e.g. 1.000 -> 1000, 1.000.000 -> 1000000)
    normalized = re.sub(r"\b(\d{1,3})(?:\.\d{3})+\b", lambda m: m.group(0).replace(".", ""), normalized)

    # 7. Decimal numbers (e.g. 3,5 hoặc 3.5 -> ba phẩy năm)
    def _decimal_repl(m: re.Match) -> str:
        int_part = number_to_words(int(m.group(1)))
        dec_part = " ".join(DIGITS[int(d)] for d in m.group(2))
        return f"{int_part} phẩy {dec_part}"

    normalized = re.sub(r"\b(\d+)[.,](\d{1,3})\b", _decimal_repl, normalized)

    # 8. Standalone Integers (e.g. 1000 -> một nghìn)
    normalized = re.sub(r"\b\d+\b", _replace_number_match, normalized)

    # 8. Special symbols cleanup
    normalized = normalized.replace("&", " và ").replace("@", " a còng ")
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized

"""Vietnamese Text Normalization (TN) & Smart Technical G2P Engine for Elearning TTS.
Converts numbers, dates, currencies, code symbols, CamelCase errors, English technical terms,
and abbreviations into natural spoken Vietnamese text.
"""

from __future__ import annotations

import re
import json
import os

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


# Built-in Phonetic Dictionary for Common IT Components & English Technical Words
DEFAULT_TECH_PHONETICS = {
    # Languages & Core Concepts
    "python": "Pai-thon",
    "javascript": "Gia-va-xơ-cơ-ríp",
    "typescript": "Tai-pơ-xơ-cơ-ríp",
    "html": "Hát-Tê-Em-El",
    "css": "Xi-Ét-Ét",
    "bytecode": "bai-cốt",
    "interpreter": "in-tơ-prơ-tơ",
    "compiler": "com-pai-lơ",
    "pvm": "P-Vi-Em",
    "pep": "pép",
    "pep 8": "pép tám",
    "snake_case": "snếch kê-xơ",
    "camelcase": "ca-mel kê-xơ",
    "pascalcase": "pas-cal kê-xơ",

    # Common Exceptions & Errors (CamelCase)
    "typeerror": "Tai-pơ É-rơ",
    "valueerror": "Vá-liu É-rơ",
    "indentationerror": "In-đen-tay-sơn É-rơ",
    "syntaxerror": "Sin-tắc É-rơ",
    "attributeerror": "Á-tri-biu-tơ É-rơ",
    "indexerror": "In-đếch É-rơ",
    "keyerror": "Ki É-rơ",
    "nameerror": "Nêm É-rơ",
    "zerodivisionerror": "Gi-rô Đi-vi-dần É-rơ",
    "recursionerror": "Ri-cơ-sần É-rơ",
    "keyboardinterrupt": "Ki-bo-đơ In-tơ-ráp",
    "overflowerror": "Ô-vơ-flô É-rơ",
    "runtimeerror": "Răn-taim É-rơ",
    "exception": "Éch-xép-sần",

    # Functions & Functions Calls
    "input()": "hàm in-pút",
    "input": "in-pút",
    "print()": "hàm pơ-rin",
    "print": "pơ-rin",
    "int()": "ép kiểu in-tơ-dơ",
    "int": "in-tơ-dơ",
    "str()": "ép kiểu xơ-trinh",
    "str": "xơ-trinh",
    "float()": "ép kiểu phơ-lốt",
    "float": "phơ-lốt",
    "bool()": "ép kiểu bu-lin",
    "bool": "bu-lin",
    "len()": "hàm len",
    "range()": "hàm reng",
    "type()": "hàm tai-pơ",

    # Built-in terms & Environment
    "vs code": "Vê-Ét Cốt",
    "vscode": "Vê-Ét Cốt",
    "console": "con-xôn",
    "terminal": "tơ-mi-nồ",
    "ide": "Ai-Đi-I",
    "cli": "Si-El-Ai",
    "api": "Ây-Pi-Ai",
    "json": "Giai-xơn",
    "yaml": "Ya-mần",
    "git": "gít",
    "github": "gít-háp",
    "main": "mên",
    "def": "đép",
    "__main__": "mên",
    "__name__": "nêm",
    "time-to-market": "Taim tu Má-két",
    "built-in": "biu-in",
    "runtime": "răn-taim",
    "source code": "xót cốt"
}


ABBREVIATIONS_RULES = [
    # ----------------------------------------------------
    # 1. Công nghệ & CNTT (Technology & Computing)
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
    (r"\bWi-?Fi\b", "oai fai", re.IGNORECASE),
    (r"\bBluetooth\b", "blu tút", re.IGNORECASE),

    # ----------------------------------------------------
    # 2. Hành chính & Trường học
    # ----------------------------------------------------
    (r"\bUBND\b", "ủy ban nhân dân", re.IGNORECASE),
    (r"\bTHPT\b", "trung học phổ thông", re.IGNORECASE),
    (r"\bĐH\b", "đại học", re.IGNORECASE),
    (r"\bVNĐ\b", "đồng", re.IGNORECASE),
    (r"\bVND\b", "đồng", re.IGNORECASE),
    (r"\bUSD\b", "đô la", re.IGNORECASE),
    (r"\bđc\b", "được", re.IGNORECASE),
    (r"\bko\b", "không", re.IGNORECASE),
]


_TECH_DICT_CACHE = None

def get_tech_dictionary() -> dict:
    global _TECH_DICT_CACHE
    if _TECH_DICT_CACHE is not None:
        return _TECH_DICT_CACHE
    
    _TECH_DICT_CACHE = dict(DEFAULT_TECH_PHONETICS)
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
                    user_entries = data.get("entries", {})
                    # Lowercase mapping for robust matching
                    for k, v in user_entries.items():
                        _TECH_DICT_CACHE[k.lower()] = v
                        _TECH_DICT_CACHE[k] = v
                    break
            except Exception:
                pass
    return _TECH_DICT_CACHE


def _smart_fallback_english_g2p(term: str) -> str:
    """Smart heuristic G2P converter for un-mapped English technical words."""
    # Split CamelCase or PascalCase (e.g. AttributeError -> Attribute Error)
    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", term).split()
    converted_parts = []
    
    dict_map = get_tech_dictionary()
    
    for word in words:
        w_lower = word.lower()
        if w_lower in dict_map:
            converted_parts.append(dict_map[w_lower])
        elif word.isupper() and len(word) <= 5:
            # Spell out uppercase acronyms (e.g. SDK -> S-D-K)
            spelled = "-".join(list(word))
            converted_parts.append(spelled)
        else:
            # Common English suffix/prefix replacements for natural speech
            w_norm = word
            w_norm = re.sub(r"Error$", " É-rơ", w_norm, flags=re.IGNORECASE)
            w_norm = re.sub(r"Type", "Tai-pơ ", w_norm, flags=re.IGNORECASE)
            w_norm = re.sub(r"Value", "Vá-liu ", w_norm, flags=re.IGNORECASE)
            w_norm = re.sub(r"Index", "In-đếch ", w_norm, flags=re.IGNORECASE)
            w_norm = re.sub(r"Syntax", "Sin-tắc ", w_norm, flags=re.IGNORECASE)
            w_norm = re.sub(r"Key", "Ki ", w_norm, flags=re.IGNORECASE)
            w_norm = re.sub(r"Code", "Cốt", w_norm, flags=re.IGNORECASE)
            w_norm = re.sub(r"\s+", " ", w_norm).strip()
            converted_parts.append(w_norm)
            
    return " ".join(converted_parts)


def normalize_vietnamese_text(text: str) -> str:
    """Normalizes raw Vietnamese text into natural spoken Elearning text."""
    if not text:
        return ""

    normalized = text

    # 0. Smart Tech Dictionary & G2P Auto-Replacement
    tech_dict = get_tech_dictionary()
    # Sort keys by length descending to match longest terms first
    sorted_terms = sorted(tech_dict.keys(), key=lambda x: len(x), reverse=True)
    
    for term in sorted_terms:
        phonetic = tech_dict[term]
        pattern = r"\b" + re.escape(term) + r"\b"
        normalized = re.sub(pattern, phonetic, normalized, flags=re.IGNORECASE)

    # Auto-detect leftover unmapped CamelCase Error classes (e.g. ZeroDivisionError)
    def _camel_error_repl(m: re.Match) -> str:
        term = m.group(0)
        return _smart_fallback_english_g2p(term)

    normalized = re.sub(r"\b[A-Z][a-zA-Z0-9]*(?:Error|Exception|Interrupt)\b", _camel_error_repl, normalized)

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

    # 3. Currency / Money shortcuts
    def _money_k_repl(m: re.Match) -> str:
        val = number_to_words(int(m.group(1)))
        currency = (m.group(2) or "").strip().lower()
        if currency in ("usd", "$", "đô la"):
            return f"{val} nghìn đô la"
        if currency in ("đ", "vnđ", "vnd", "đồng"):
            return f"{val} nghìn đồng"
        return f"{val} nghìn"

    normalized = re.sub(r"\b(\d+)\s*[kK]\s*(usd|\$|đ|vnđ|vnd|đô la|đồng)?\b", _money_k_repl, normalized, flags=re.IGNORECASE)

    # 4. Units (% , °C, km, kg, cm, m)
    normalized = re.sub(r"(\d+)\s*%", r"\1 phần trăm", normalized)
    normalized = re.sub(r"(\d+)\s*°C\b", r"\1 độ cê", normalized)
    normalized = re.sub(r"(\d+)\s*km\b", r"\1 ki lô mét", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"(\d+)\s*kg\b", r"\1 ki lô gam", normalized, flags=re.IGNORECASE)

    # 5. Abbreviations
    for item in ABBREVIATIONS_RULES:
        if len(item) == 3:
            pattern, repl, flags = item
        else:
            pattern, repl = item
            flags = re.IGNORECASE
        normalized = re.sub(pattern, repl, normalized, flags=flags)

    # 6. Numbers & Decimals
    def _decimal_repl(m: re.Match) -> str:
        int_part = number_to_words(int(m.group(1)))
        dec_part = " ".join(DIGITS[int(d)] for d in m.group(2))
        return f"{int_part} phẩy {dec_part}"

    normalized = re.sub(r"\b(\d+)[.,](\d{1,3})\b", _decimal_repl, normalized)
    normalized = re.sub(r"\b\d+\b", _replace_number_match, normalized)

    # 7. Special symbols & Whitespace cleanup
    normalized = normalized.replace("&", " và ").replace("@", " a còng ")
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized

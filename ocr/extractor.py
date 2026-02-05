

import re


def normalize_currency(text):
    """
    Fix OCR issues where ₹ is misread as 2, rs, inr, etc.
    """
    if not text:
        return ""

    replacements = {
        " rs.": " ₹ ",
        " rs ": " ₹ ",
        "inr": " ₹ ",
        "rupees": " ₹ ",
        " 2 ": " ₹ ",
        "2 ": "₹ ",
        "₹₹": "₹"
    }

    t = text.lower()
    for k, v in replacements.items():
        t = t.replace(k, v)

    return t


def extract_amount(text):
    """
    Detects payment amount from 1 to 5 digits.
    Handles UPI receipts & OCR noise.
    """
    if not text:
        return None

    text = normalize_currency(text)
    text = text.replace(",", "")

    matches = re.findall(r"₹\s?(\d{1,5})", text)

    if matches:
        return max(map(int, matches))  

    return None


def extract_date(text):
    date_patterns = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{2}\s\w+\s\d{4}\b"
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return None


def extract_vendor(text):
    vendor_keywords = [
        "store", "mart", "hotel", "restaurant",
        "shop", "traders", "enterprises", "services"
    ]

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    for line in lines:
        for key in vendor_keywords:
            if key in line.lower():
                return line

    return "Unknown"


def extract_invoice_fields(text):
    """
    Extracts structured fields from OCR text.
    """

    text = normalize_currency(text)

    data = {
        "vendor": extract_vendor(text),
        "amount": extract_amount(text),
        "date": extract_date(text)
    }

    return data
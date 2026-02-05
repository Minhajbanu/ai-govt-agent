
import re

def extract_amount(text):
    """
    OCR-robust UPI amount extractor.
    Handles cases where ₹ is misread as '2'.
    """

    if not text:
        return None

    text = text.replace(",", "")
    lines = [l.strip().lower() for l in text.splitlines() if l.strip()]

    candidates = []

    for i, line in enumerate(lines):
        if any(k in line for k in ["paid", "amount", "payment", "debited"]):
            nums = re.findall(r"\b\d{1,7}\b", line)
            for n in nums:
                candidates.append((int(n), 5))

        if i > 0 and any(k in lines[i - 1] for k in ["paid", "amount"]):
            nums = re.findall(r"\b\d{1,7}\b", line)
            for n in nums:
                candidates.append((int(n), 4))

        nums = re.findall(r"\b\d{1,7}\b", line)
        for n in nums:
            candidates.append((int(n), 1))

    final = []
    for amt, score in candidates:
        if amt > 1000000:
            continue

        if amt >= 200 and amt <= 299:
            amt = amt - 200

        if amt > 0:
            final.append((amt, score))

    if not final:
        return None

    final.sort(key=lambda x: (-x[1], x[0]))
    return final[0][0]


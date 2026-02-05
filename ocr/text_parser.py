

import re
import uuid
from ocr.amount_extractor import extract_amount

def parse_transaction_text(text):
    """
    Convert OCR text into structured transaction fields.
    Supports PhonePe / GPay / Paytm / UPI receipts.
    """

    if not text or len(text.strip()) < 10:
        return None

    data = {}

    tx_match = re.search(
        r"(Transaction|Txn|TXN)[\s#:]*([A-Z0-9\-]+)",
        text,
        re.IGNORECASE
    )

    data["transaction_id"] = (
        tx_match.group(2)
        if tx_match
        else f"OCR-{uuid.uuid4().hex[:8]}"
    )

    amount = extract_amount(text)
    data["amount"] = amount if amount else None

    vendor_match = re.search(
        r"(Paid to|Merchant|Vendor|To)[:\s]+([A-Za-z0-9 &.\-]+)",
        text,
        re.IGNORECASE
    )

    data["vendor"] = (
        vendor_match.group(2).strip()
        if vendor_match
        else "Unknown Merchant"
    )

    date_match = re.search(
        r"(\d{1,2}\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*\d{2,4})",
        text,
        re.IGNORECASE
    )

    if not date_match:
        date_match = re.search(
            r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
            text
        )

    data["date"] = date_match.group(1) if date_match else "Unknown Date"

    data["department"] = "Uploaded Document"
    data["payment_method"] = "UPI"
    data["source"] = "OCR Image"

    return data

def validate_transaction_template(text):
    """
    Validates whether the OCR text matches a known transaction document type.
    Supported:
    - UPI Receipts (PhonePe, GPay, Paytm)
    - Invoices / Bills
    """

    text_lower = text.lower()

    upi_keywords = [
        "upi",
        "paid to",
        "paid",
        "transaction",
        "successful",
        "ref",
        "utr",
        "phonepe",
        "gpay",
        "paytm"
    ]

    invoice_keywords = [
        "invoice",
        "bill",
        "gst",
        "vendor",
        "total",
        "tax",
        "amount payable"
    ]

    upi_matches = [k for k in upi_keywords if k in text_lower]
    invoice_matches = [k for k in invoice_keywords if k in text_lower]

    if len(upi_matches) >= 3:
        return {
            "valid": True,
            "type": "UPI Receipt",
            "matched_keywords": upi_matches,
            "missing_fields": []
        }

    if len(invoice_matches) >= 3:
        return {
            "valid": True,
            "type": "Invoice",
            "matched_keywords": invoice_matches,
            "missing_fields": []
        }

    return {
        "valid": False,
        "type": "Unknown / Suspicious",
        "matched_keywords": [],
        "missing_fields": [
            "Transaction identifiers not detected"
        ]
    }

import os

def load_evidence(transaction_id, base_dir):
    evidence_dir = os.path.join(base_dir, "data", "raw_docs")
    file_path = os.path.join(evidence_dir, f"{transaction_id}_invoice.txt")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "No supporting document found."

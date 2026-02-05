import pandas as pd
import os

from rules.compliance_rules import detect_duplicate_payments
from ml.anomaly_detection import detect_anomalies
from llm.reasoning_agent import explain_fraud
from ocr.evidence_loader import load_evidence

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_ai_audit(df):
    df = df.copy()

    rule_flags = detect_duplicate_payments(df)
    df["rule_score"] = df["transaction_id"].isin(
        rule_flags["transaction_id"]
    ).astype(int)

    ml_flags = detect_anomalies(df)
    df["ml_score"] = df["transaction_id"].isin(
        ml_flags["transaction_id"]
    ).astype(int)

    df["amount_risk"] = df["amount"] / df["amount"].max()

    vendor_counts = df["vendor"].value_counts()
    df["frequency_risk"] = (
        df["vendor"].map(vendor_counts) / vendor_counts.max()
    )

    df["risk_score"] = (
        0.35 * df["rule_score"] +
        0.30 * df["ml_score"] +
        0.20 * df["amount_risk"] +
        0.15 * df["frequency_risk"]
    )

    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[0, 0.4, 0.7, 1.0],
        labels=["Low", "Medium", "High"]
    )

    flagged = df[df["risk_score"] >= 0.4].copy()

    flagged["evidence"] = flagged["transaction_id"].apply(
        lambda tx_id: load_evidence(tx_id, BASE_DIR)
    )

    flagged["explanation"] = flagged.apply(
        lambda row: explain_fraud(row, row["evidence"]),
        axis=1
    )

    return flagged

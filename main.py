import pandas as pd
from rules.compliance_rules import detect_duplicate_payments
from ml.anomaly_detection import detect_anomalies
from llm.reasoning_agent import explain_fraud
from reports.audit_report import generate_report

df = pd.read_csv("data/transactions.csv")

duplicates = detect_duplicate_payments(df)
anomalies = detect_anomalies(df)

flagged = pd.concat([duplicates, anomalies]).drop_duplicates()

for _, row in flagged.iterrows():
    print(explain_fraud(row))

print(generate_report(flagged))



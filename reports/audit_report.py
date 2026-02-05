def generate_report(flagged_cases):
    report = "AI AUDIT REPORT\n\n"
    report += f"Total suspicious cases: {len(flagged_cases)}\n\n"

    for _, row in flagged_cases.iterrows():
        report += f"- {row['transaction_id']} | {row['vendor']} | ₹{row['amount']}\n"

    return report

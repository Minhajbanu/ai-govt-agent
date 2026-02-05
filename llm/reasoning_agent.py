def explain_fraud(transaction, evidence_text=None):
    """
    Generate an explainable, audit-friendly reasoning
    for why a transaction was flagged as risky.
    """

    explanation = f"""
🔍 TRANSACTION ANALYSIS
----------------------
• Transaction ID : {transaction['transaction_id']}
• Department     : {transaction['department']}
• Vendor         : {transaction['vendor']}
• Amount         : ₹{transaction['amount']}
• Risk Score     : {transaction['risk_score']:.2f}
• Risk Level     : {transaction['risk_level']}

⚠️ FLAGGING REASONS
------------------
"""

    reasons = []

    if transaction["rule_score"] == 1:
        reasons.append(
            "• Rule-based compliance check triggered (possible duplicate or policy violation)."
        )

    if transaction["ml_score"] == 1:
        reasons.append(
            "• Machine Learning anomaly detected (transaction deviates from normal spending patterns)."
        )

    if not reasons:
        reasons.append(
            "• Transaction shows elevated risk due to amount or vendor frequency patterns."
        )

    explanation += "\n".join(reasons)

    explanation += f"""

🧠 AI RISK INTERPRETATION
------------------------
The combined impact of compliance rules, anomaly detection,
transaction amount, and vendor activity resulted in a
{transaction['risk_level']} risk classification. This transaction
requires further human audit review.

📄 SUPPORTING EVIDENCE
---------------------
{evidence_text if evidence_text else "No supporting document available for this transaction."}
"""

    return explanation.strip()

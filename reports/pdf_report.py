from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def generate_pdf_report(flagged_df, output_path="audit_report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=A4)

    elements = []

    elements.append(Paragraph("<b>AI AUDIT REPORT</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(
        Paragraph(
            f"Total high-risk transactions identified: {len(flagged_df)}",
            styles["Normal"]
        )
    )
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Flagged Transactions</b>", styles["Heading2"]))

    table_data = [
        ["Transaction ID", "Vendor", "Amount", "Risk Score", "Risk Level"]
    ]

    for _, row in flagged_df.iterrows():
        table_data.append([
            row["transaction_id"],
            row["vendor"],
            f"₹{row['amount']}",
            f"{row['risk_score']:.2f}",
            row["risk_level"]
        ])

    table = Table(table_data, hAlign="LEFT")
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Detailed AI Findings</b>", styles["Heading2"]))

    for _, row in flagged_df.iterrows():
        elements.append(
            Paragraph(
                f"<b>Transaction {row['transaction_id']}</b><br/>"
                f"Vendor: {row['vendor']}<br/>"
                f"Amount: ₹{row['amount']}<br/>"
                f"Risk Level: {row['risk_level']}<br/><br/>"
                f"<b>AI Explanation:</b><br/>{row['explanation']}<br/><br/>"
                f"<b>Evidence:</b><br/><pre>{row['evidence']}</pre>",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 0.3 * inch))

    doc.build(elements)

    return output_path

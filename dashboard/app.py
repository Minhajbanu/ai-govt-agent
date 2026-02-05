

import streamlit as st
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from ai_agent import run_ai_audit
from reports.pdf_report import generate_pdf_report

st.set_page_config(
    page_title="AI Audit Agent",
    layout="wide"
)

st.title("🧠 AI Audit Agent – Government Expenditure")
st.caption("🔁 Continuous AI Monitoring Enabled")


st.subheader("📁 Upload Transaction Data (CSV)")

uploaded_csv = st.file_uploader(
    "Upload transaction CSV to begin analysis",
    type=["csv"]
)

df = None

if uploaded_csv:
    try:
        df = pd.read_csv(uploaded_csv)
        st.success("✅ Transaction data loaded successfully")
    except Exception:
        st.error("❌ Invalid CSV file format")
        st.stop()
else:
    st.info("ℹ️ No transaction data loaded. Please upload a CSV file.")


st.sidebar.header("🔍 Filter Transactions")

if df is not None:
    dept_filter = st.sidebar.multiselect(
        "Select Department",
        options=sorted(df["department"].dropna().unique())
    )

    vendor_filter = st.sidebar.multiselect(
        "Select Vendor",
        options=sorted(df["vendor"].dropna().unique())
    )

    filtered_df = df.copy()

    if dept_filter:
        filtered_df = filtered_df[filtered_df["department"].isin(dept_filter)]

    if vendor_filter:
        filtered_df = filtered_df[filtered_df["vendor"].isin(vendor_filter)]
else:
    filtered_df = None


st.divider()
st.subheader("🚨 Run AI Audit Agent")

if st.button("Run AI Audit"):
    if filtered_df is None:
        st.error("❌ Please upload a transaction CSV before running audit")
        st.stop()

    flagged = run_ai_audit(filtered_df)

    if flagged.empty:
        st.success("✅ No high-risk transactions detected")
    else:
        st.subheader("⚠️ Flagged Transactions")
        st.dataframe(
            flagged[
                [
                    "transaction_id",
                    "vendor",
                    "department",
                    "amount",
                    "risk_score",
                    "risk_level"
                ]
            ].sort_values("risk_score", ascending=False),
            use_container_width=True
        )

        st.subheader("📈 Risk Score Distribution")
        st.bar_chart(flagged.set_index("transaction_id")["risk_score"])

        st.subheader("🧠 AI Reasoning & Evidence")
        for _, row in flagged.iterrows():
            with st.expander(
                f"Transaction {row['transaction_id']} | "
                f"Risk: {row['risk_level']} ({row['risk_score']:.2f})"
            ):
                st.write(row["explanation"])
                st.code(row.get("evidence", "AI Analysis"))

        st.subheader("📄 Generate Audit Report")

        report_path = generate_pdf_report(flagged)

        with open(report_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="📥 Download PDF Audit Report",
            data=pdf_bytes,
            file_name="AI_Audit_Report.pdf",
            mime="application/pdf"
        )

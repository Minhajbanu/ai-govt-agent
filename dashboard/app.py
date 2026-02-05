# import streamlit as st
# import pandas as pd
# import os
# import sys


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)

# from ai_agent import run_ai_audit
# from reports.pdf_report import generate_pdf_report
# from PIL import Image


# from ocr.image_ocr import extract_text_from_image
# from ocr.text_parser import parse_transaction_text
# from ocr.template_validator import validate_transaction_template
# from ocr.amount_extractor import extract_amount


# st.set_page_config(
#     page_title="AI Audit Agent",
#     layout="wide"
# )

# st.title("🧠 AI Audit Agent – Government Expenditure")
# st.caption("🔁 Continuous AI Monitoring Enabled")


# st.subheader("📁 Upload Transaction Data (CSV)")

# uploaded_csv = st.file_uploader(
#     "Upload transaction CSV to begin analysis",
#     type=["csv"]
# )

# df = None  

# if uploaded_csv:
#     try:
#         df = pd.read_csv(uploaded_csv)
#         st.success("✅ Transaction data loaded successfully")
#     except Exception:
#         st.error("❌ Invalid CSV file format")
#         st.stop()
# else:
#     st.info("ℹ️ No transaction data loaded. Please upload a CSV file.")


# st.sidebar.header("🔍 Filter Transactions")

# if df is not None:
#     dept_filter = st.sidebar.multiselect(
#         "Select Department",
#         options=sorted(df["department"].dropna().unique())
#     )

#     vendor_filter = st.sidebar.multiselect(
#         "Select Vendor",
#         options=sorted(df["vendor"].dropna().unique())
#     )

#     filtered_df = df.copy()

#     if dept_filter:
#         filtered_df = filtered_df[filtered_df["department"].isin(dept_filter)]

#     if vendor_filter:
#         filtered_df = filtered_df[filtered_df["vendor"].isin(vendor_filter)]
# else:
#     filtered_df = None


# st.divider()
# st.subheader("📸 Upload Transaction Image (Receipt / Invoice)")

# uploaded_image = st.file_uploader(
#     "Upload transaction image",
#     type=["png", "jpg", "jpeg"]
# )

# image_df = None
# ocr_risk_notes = []

# if uploaded_image:
#     #st.image(uploaded_image, caption="Uploaded Receipt", use_container_width=True)
#     image = Image.open(uploaded_image)
#     st.image(image, caption="Uploaded Receipt")

#     #extracted_text = extract_text_from_image(uploaded_image)
#     extracted_text = extract_text_from_image(image)

#     st.markdown("### 📝 Extracted OCR Text")
#     st.text_area("OCR Output", extracted_text, height=200)

#     template_result = validate_transaction_template(extracted_text)

#     if template_result["valid"]:
#         st.success(f"✅ Valid {template_result['type']} detected")
#     else:
#         st.error("❌ Invalid / Suspicious Document Structure")
#         ocr_risk_notes.append("Invalid receipt format")

#     parsed_data = parse_transaction_text(extracted_text)

#     if parsed_data:
#         ocr_amount = extract_amount(extracted_text)
#         if ocr_amount:
#             parsed_data["amount"] = ocr_amount

#         parsed_data["source"] = "OCR"
#         parsed_data["evidence"] = (
#             " | ".join(ocr_risk_notes)
#             if ocr_risk_notes
#             else "OCR verified transaction"
#         )

#         image_df = pd.DataFrame([parsed_data])
#     else:
#         st.warning("⚠️ Could not extract structured data from image")

# st.divider()
# st.subheader("🚨 Run AI Audit Agent")

# if st.button("Run AI Audit"):
#     if filtered_df is None and image_df is None:
#         st.error("❌ Please upload transaction CSV or receipt image before running audit")
#         st.stop()

#     if filtered_df is not None and image_df is not None:
#         audit_df = pd.concat([filtered_df, image_df], ignore_index=True)
#     elif filtered_df is not None:
#         audit_df = filtered_df
#     else:
#         audit_df = image_df

#     flagged = run_ai_audit(audit_df)

#     if flagged.empty:
#         st.success("✅ No high-risk transactions detected")
#     else:
#         st.subheader("⚠️ Flagged Transactions")
#         st.dataframe(
#             flagged[
#                 [
#                     "transaction_id",
#                     "vendor",
#                     "department",
#                     "amount",
#                     "risk_score",
#                     "risk_level"
#                 ]
#             ].sort_values("risk_score", ascending=False),
#             use_container_width=True
#         )

#         st.subheader("📈 Risk Score Distribution")
#         st.bar_chart(flagged.set_index("transaction_id")["risk_score"])

#         st.subheader("🧠 AI Reasoning & Evidence")
#         for _, row in flagged.iterrows():
#             with st.expander(
#                 f"Transaction {row['transaction_id']} | "
#                 f"Risk: {row['risk_level']} ({row['risk_score']:.2f})"
#             ):
#                 st.write(row["explanation"])
#                 st.code(row.get("evidence", "AI + OCR Analysis"))

#         st.subheader("📄 Generate Audit Report")

#         report_path = generate_pdf_report(flagged)

#         with open(report_path, "rb") as f:
#             pdf_bytes = f.read()

#         st.download_button(
#             label="📥 Download PDF Audit Report",
#             data=pdf_bytes,
#             file_name="AI_Audit_Report.pdf",
#             mime="application/pdf"
#         )

import streamlit as st
import pandas as pd
import os
import sys

# ---- Path setup ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from ai_agent import run_ai_audit
from reports.pdf_report import generate_pdf_report

# ---- Page config ----
st.set_page_config(
    page_title="AI Audit Agent",
    layout="wide"
)

st.title("🧠 AI Audit Agent – Government Expenditure")
st.caption("🔁 Continuous AI Monitoring Enabled")

# ===============================
# CSV UPLOAD SECTION
# ===============================
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

# ===============================
# FILTERS
# ===============================
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

# ===============================
# AI AUDIT
# ===============================
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

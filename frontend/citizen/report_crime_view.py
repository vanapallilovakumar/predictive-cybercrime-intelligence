from datetime import datetime, time, timezone

import streamlit as st

from frontend import api_client


def render() -> None:
    st.markdown("## Lodge Cybercrime Complaint")
    st.caption("Submit the details that help investigators issue fast bank-freeze advisories.")
    user = st.session_state.get("user", {})
    with st.form("complaint_form"):
        st.markdown("### 1. Incident details")
        typology = st.selectbox("Crime typology", ["OTP fraud", "Digital arrest", "Job fraud", "UPI fraud", "Investment scam", "Loan app extortion"])
        incident_date = st.date_input("Incident date", value=datetime.now().date())
        incident_time = st.time_input("Incident time", value=time(12, 0))
        description = st.text_area("Brief description")
        st.markdown("### 2. Financial impact")
        amount = st.number_input("Amount lost (INR)", min_value=0.0, step=1000.0)
        victim_name = st.text_input("Your name", value=user.get("name", ""))
        victim_bank = st.text_input("Your bank name")
        victim_account = st.text_input("Your account number (masked or last 4 digits)", value="XXXXXX")
        victim_district = st.text_input("Your district / city")
        st.markdown("### 3. Suspect / beneficiary")
        beneficiary_bank = st.text_input("Beneficiary bank")
        beneficiary_account = st.text_input("Beneficiary account / UPI ID")
        reported_district = st.text_input("Reported withdrawal district / location")
        st.markdown("### 4. Evidence")
        evidence = st.file_uploader("Upload PNG, JPG, or PDF", type=["png", "jpg", "jpeg", "pdf"])
        submitted = st.form_submit_button("Submit Official Complaint", type="primary", use_container_width=True)
    if not submitted:
        return
    email = user.get("email", st.session_state.get("login_email", "citizen@example.com"))
    required = [victim_district, beneficiary_bank, beneficiary_account, reported_district]
    if amount <= 0 or not all(required):
        st.error("Complete the amount, district, and beneficiary fields before submitting.")
        return
    payload = {
        "typology": typology,
        "loss_amount_inr": amount,
        "victim_name": victim_name or "Anonymous Citizen",
        "victim_email": email,
        "victim_account_no": victim_account,
        "victim_bank_name": victim_bank or "Not Disclosed",
        "victim_district": victim_district,
        "beneficiary_bank": beneficiary_bank,
        "beneficiary_account": beneficiary_account,
        "reported_district": reported_district,
        "incident_timestamp": datetime.combine(incident_date, incident_time, tzinfo=timezone.utc).isoformat(),
        "description": description,
    }
    result = api_client.report_crime(payload, evidence)
    if result and result.get("success"):
        st.session_state["last_reference"] = result["reference_no"]
        st.success("Complaint lodged successfully.")
        st.code(result["reference_no"])
        st.info("If the fraud occurred within the last two hours, call 1930 immediately.")
    else:
        st.error("Complaint submission failed. Please retry.")

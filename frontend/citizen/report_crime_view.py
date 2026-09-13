from datetime import datetime, time, timezone

import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("INTAKE")

    st.markdown(
        """
        <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #ffffff;">
                ■ LODGE OFFICIAL CYBERCRIME COMPLAINT
            </div>
            <div style="font-size: 0.76rem; color: #a3a3a3; margin-top: 0.2rem;">
                Golden Hour Immediate Debit Freeze & NCRP Portal Automated Integration.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user = st.session_state.get("user", {})

    with st.form("complaint_form"):
        st.markdown(
            '<div style="font-size: 0.82rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">■ 1. INCIDENT DETAILS & TYPOLOGY</div>',
            unsafe_allow_html=True,
        )
        c_typ, c_date, c_time = st.columns([2, 1, 1])
        with c_typ:
            typology = st.selectbox("Crime Typology", ["OTP fraud", "Digital arrest", "Job fraud", "UPI fraud", "Investment scam", "Loan app extortion", "Other Cyber Fraud"])
        with c_date:
            incident_date = st.date_input("Incident Date", value=datetime.now().date())
        with c_time:
            incident_time = st.time_input("Incident Time", value=time(12, 0))
            
        description = st.text_area("Narrative & Chronology of Incident", placeholder="Explain how contact occurred and what instructions were given...")

        st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size: 0.82rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">■ 2. FINANCIAL LOSS & VICTIM ACCOUNT</div>',
            unsafe_allow_html=True,
        )
        c_amt, c_vname = st.columns(2)
        with c_amt:
            amount = st.number_input("Amount Defrauded (INR)", min_value=0.0, step=5000.0, value=75000.0)
        with c_vname:
            victim_name = st.text_input("Complainant Name", value=user.get("name", ""))

        c_vbank, c_vacc, c_vdist = st.columns(3)
        with c_vbank:
            victim_bank = st.text_input("Your Bank Name", placeholder="e.g. State Bank of India")
        with c_vacc:
            victim_account = st.text_input("Your Account (Masked or Last 4)", value="XXXXXX")
        with c_vdist:
            victim_district = st.text_input("Your City / District", value="Ranchi")

        st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size: 0.82rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">■ 3. SUSPECT BENEFICIARY DETAILS (CRUCIAL FOR RAPID FREEZE)</div>',
            unsafe_allow_html=True,
        )
        c_bbank, c_bacc, c_rdist = st.columns(3)
        with c_bbank:
            beneficiary_bank = st.text_input("Beneficiary Bank (Target for Freeze)", value="Bank of India")
        with c_bacc:
            beneficiary_account = st.text_input("Beneficiary Account Number / UPI ID", value="9876543210@upi")
        with c_rdist:
            reported_district = st.text_input("Suspected Withdrawal District", value="Deoghar")

        st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size: 0.82rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">■ 4. DOCUMENTARY EVIDENCE</div>',
            unsafe_allow_html=True,
        )
        evidence = st.file_uploader("Upload Bank Transaction Screenshot / PDF Receipt", type=["png", "jpg", "jpeg", "pdf"])

        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Official Incident Report", type="primary", use_container_width=True)

    if not submitted:
        return

    email = user.get("email", st.session_state.get("login_email", "citizen@example.com"))
    required = [victim_district, beneficiary_bank, beneficiary_account, reported_district]
    if amount <= 0 or not all(required):
        st.error("Please ensure the loss amount, districts, and beneficiary fields are completed.")
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
        ref = result["reference_no"]
        st.session_state["last_reference"] = ref
        st.markdown(
            f"""
            <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 1.25rem; margin-top: 1rem;">
                <div style="font-size: 1.05rem; font-weight: 900; color: #ffffff; margin-bottom: 0.25rem;">[✓] COMPLAINT LODGED SUCCESSFULLY</div>
                <div style="font-size: 0.85rem; color: #ffffff; margin-bottom: 0.75rem;">
                    NCRP Case Reference: <b style="font-family: 'Electrolize', sans-serif; color: #ffffff; font-weight: 900;">{ref}</b>
                </div>
                <div style="font-size: 0.78rem; color: #a3a3a3;">
                    Automated predictive intelligence has registered this cash-out corridor and notified field patrol nodes.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Complaint registration encountered an error. Please retry.")

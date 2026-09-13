import streamlit as st

from frontend import api_client


def render() -> None:
    st.markdown("## Cyber Safely")
    st.caption("Citizen Protection & Reporting Portal")
    st.markdown('<div class="prahari-card">Use any email in demo mode. The OTP is <b>123456</b>.</div>', unsafe_allow_html=True)
    email = st.text_input("Email address", placeholder="citizen@example.com")
    if st.button("Send Login Code (OTP)", type="primary", use_container_width=True):
        if not email or "@" not in email:
            st.error("Enter a valid email address.")
        else:
            result = api_client.request_otp(email)
            if result and result.get("success"):
                st.session_state["login_email"] = email
                st.session_state["otp_requested"] = True
                st.success(result.get("message", "OTP sent."))
            else:
                st.error("Unable to request an OTP.")
    if st.session_state.get("otp_requested"):
        otp = st.text_input("6-digit OTP", max_chars=6, type="password")
        if st.button("Verify & Enter Portal", type="primary", use_container_width=True):
            result = api_client.verify_otp(st.session_state["login_email"], otp)
            if result and result.get("success"):
                st.session_state["authenticated"] = True
                st.session_state["user"] = result.get("user") or {"email": st.session_state["login_email"], "name": "Citizen User"}
                st.rerun()
            else:
                st.error("OTP verification failed.")

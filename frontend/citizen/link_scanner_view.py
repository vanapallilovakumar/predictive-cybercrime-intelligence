import streamlit as st

from frontend import api_client


def render() -> None:
    st.markdown("## Link Security Checker")
    st.caption("Paste a suspicious SMS, WhatsApp, or email link before opening it.")
    url = st.text_input("Website link", placeholder="http://sbi-reward-kyc.top/claim-bonus.apk")
    if st.button("Analyze Link Security", type="primary"):
        if not url.strip():
            st.warning("Paste a URL to analyze.")
            return
        result = api_client.scan_link(url)
        if not result:
            st.error("The scanner is unavailable.")
            return
        factors = "".join(f"<li>{item}</li>" for item in result.get("risk_factors", []))
        if result.get("verdict") == "SAFE":
            st.markdown(
                f'<div class="phishing-safe"><h3>SAFE - no immediate fraud pattern detected</h3>'
                f'<p>Threat score: {result.get("threat_score", 0):.2f}</p>'
                f'<p>{result.get("safety_guidance", "")}</p></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="phishing-danger"><h3>HIGH-RISK {result.get("verdict", "SUSPICIOUS")}</h3>'
                f'<p>Threat score: {result.get("threat_score", 0):.2f}</p><ul>{factors}</ul>'
                f'<p><b>Safety advice:</b> {result.get("safety_guidance", "")}</p></div>',
                unsafe_allow_html=True,
            )

import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("SCANNER")

    st.markdown(
        """
        <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #f8fafc;">
                CYBER THREAT LINK SCANNER
            </div>
            <div style="font-size: 0.76rem; color: #8b949e; margin-top: 0.2rem;">
                Heuristic APK lure, typosquatting, and entropy-based credential harvesting analyzer.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    url = st.text_input("Suspicious Link (SMS / WhatsApp / Email)", placeholder="http://sbi-reward-kyc.top/claim-bonus.apk")

    if st.button("Analyze Threat Signature", type="primary"):
        if not url.strip():
            st.warning("Please supply a valid URL to analyze.")
            return

        result = api_client.scan_link(url)
        if not result:
            st.error("Scanner heuristics engine unavailable.")
            return

        score = float(result.get("threat_score", 0.0))
        score_pct = int(score * 100)
        verdict = result.get("verdict", "SAFE")

        factors = "".join(f"<li style='margin-bottom: 0.25rem;'>{item}</li>" for item in result.get("risk_factors", []))

        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

        if verdict == "SAFE":
            st.markdown(
                f"""
                <div class="phishing-safe">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-weight: 800; font-size: 1rem; color: #10b981;">VERDICT: SAFE / LOW RISK</span>
                        <span style="font-family: 'Electrolize', sans-serif; font-weight: 700; color: #10b981;">{score_pct}% RISK</span>
                    </div>
                    <div class="threat-bar-container" style="height: 8px; margin-bottom: 0.75rem;">
                        <div style="width: {score_pct}%; height: 100%; background: #10b981; border-radius: 3px;"></div>
                    </div>
                    <div style="font-size: 0.85rem; color: #d1fae5;">{result.get("safety_guidance", "")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="phishing-danger">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-weight: 800; font-size: 1rem; color: #f43f5e;">THREAT DETECTED: {verdict}</span>
                        <span style="font-family: 'Electrolize', sans-serif; font-weight: 700; color: #f43f5e;">{score_pct}% PROBABILITY</span>
                    </div>
                    <div class="threat-bar-container" style="height: 10px; margin-bottom: 0.75rem;">
                        <div class="threat-bar-fill" style="width: {score_pct}%;"></div>
                    </div>
                    <div style="font-size: 0.82rem; font-weight: 600; margin-bottom: 0.35rem; color: #f8fafc;">Flagged Threat Indicators:</div>
                    <ul style="font-size: 0.8rem; color: #fecdd3; padding-left: 1.25rem;">{factors}</ul>
                    <div style="margin-top: 0.6rem; padding-top: 0.5rem; border-top: 1px solid rgba(225, 29, 72, 0.3); font-size: 0.8rem; color: #cbd5e1;">
                        <b>Safety Advisory:</b> {result.get("safety_guidance", "")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("TRIAGE")

    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.25rem;">
            <div>
                <div style="font-size: 1.1rem; font-weight: 800; letter-spacing: 0.06em; color: #ffffff;">
                    ■ RESPONSE ACTION QUEUE // CASH-OUT TRIAGE
                </div>
                <div style="font-size: 0.74rem; color: #a3a3a3; margin-top: 0.2rem;">
                    Priority-ranked interdiction corridor flagging imminent siphon-off at CSPs and ATMs.
                </div>
            </div>
            <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #ffffff; font-weight: 800; background: #000000; border: 1px solid #ffffff; padding: 0.3rem 0.7rem; border-radius: 2px;">
                [!] LEGAL POWERS: SEC 91 BNSS / CRPC
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    alerts = api_client.command_list("/api/v1/alerts", "alerts")
    if not alerts:
        st.info("No active high-priority alerts in current corridor.")
        return

    for alert in alerts:
        prob = int(alert.get("probability_pct", 50))
        loss = float(alert.get("loss_amount_inr", 0))
        status = alert.get("status", "OPEN")
        status_class = "status-open" if status == "OPEN" else ("status-dispatched" if status == "DISPATCHED" else "status-acknowledged")

        title = f"[{alert.get('alert_code')}] {alert.get('node_name')} • {alert.get('district')} • ₹{loss:,.0f} • {status}"
        
        with st.expander(title, expanded=(status == "OPEN")):
            st.markdown(
                f"""
                <div style="background: #000000; border: 1px solid #262626; border-radius: 2px; padding: 0.85rem; margin-bottom: 0.65rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span class="status-badge {status_class}">{status}</span>
                        <span style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #ffffff; font-weight: 900;">
                            ■ {alert.get('priority')} PRIORITY ({prob}% CONFIDENCE)
                        </span>
                    </div>
                    <div style="margin-bottom: 0.65rem;">
                        <div style="font-size: 0.68rem; color: #a3a3a3; font-family: 'Electrolize', sans-serif; text-transform: uppercase;">
                            Threat Velocity Meter
                        </div>
                        <div class="threat-bar-container" style="height: 8px; margin-top: 0.2rem;">
                            <div class="threat-bar-fill" style="{theme.threat_bar_style(prob)}"></div>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; font-size: 0.8rem;">
                        <div>
                            <span style="color: #a3a3a3;">Target Node:</span> <b style="color: #ffffff; font-weight: 700;">{alert.get('node_name')}</b><br>
                            <span style="color: #a3a3a3;">Bank:</span> <b style="color: #ffffff; font-weight: 700;">{alert.get('bank_name')}</b><br>
                            <span style="color: #a3a3a3;">Linked NCRP Ref:</span> <code style="color: #ffffff; font-weight: 700;">{alert.get('complaint_ref')}</code>
                        </div>
                        <div>
                            <span style="color: #a3a3a3;">Beneficiary Bank:</span> <b style="color: #ffffff; font-weight: 700;">{alert.get('beneficiary_bank')}</b><br>
                            <span style="color: #a3a3a3;">Beneficiary Account:</span> <code style="color: #ffffff; font-weight: 800;">{alert.get('beneficiary_account')}</code><br>
                            <span style="color: #a3a3a3;">Amount at Risk:</span> <b style="color: #ffffff; font-weight: 900;">₹{loss:,.0f}</b>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #262626; font-size: 0.76rem; color: #a3a3a3;">
                        <b style="color: #ffffff;">Detection Logic:</b> {alert.get('reason_text')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                if st.button("Generate Section 91 Freeze Notice", key=f"adv-{alert.get('id')}", type="primary"):
                    advisory = api_client.generate_advisory(alert.get("id") or alert.get("alert_code"))
                    if advisory:
                        st.session_state[f"advisory-{alert.get('id')}"] = advisory
            with c2:
                next_status = {"OPEN": "DISPATCHED", "DISPATCHED": "ACKNOWLEDGED", "ACKNOWLEDGED": "RESOLVED"}.get(status)
                if next_status and st.button(f"Mark {next_status}", key=f"status-{alert.get('id')}"):
                    updated = api_client.update_alert(alert.get("id") or alert.get("alert_code"), next_status, "Triage updated from PRAHARI console")
                    if updated:
                        st.success(f"Alert transitioned to {next_status}.")
                        st.rerun()

            advisory = st.session_state.get(f"advisory-{alert.get('id')}")
            if advisory:
                st.markdown(
                    f"""
                    <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 0.75rem; margin-top: 0.65rem;">
                        <div style="font-size: 0.78rem; font-weight: 800; color: #ffffff; margin-bottom: 0.3rem;">
                            [!] OFFICIAL LEGAL ADVISORY: {advisory.get('notice_ref')}
                        </div>
                        <div style="font-size: 0.72rem; color: #a3a3a3; margin-bottom: 0.4rem;">
                            Dispatched to Nodal Fraud Desk: {advisory.get('recipient_bank')} • Account: {advisory.get('target_account')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.text_area("Advisory Text (Ready to Dispatch)", advisory.get("advisory_text", ""), height=180, key=f"text-{alert.get('id')}")

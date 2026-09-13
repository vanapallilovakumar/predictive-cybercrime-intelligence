import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("TRIAGE")

    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.25rem;">
            <div>
                <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #f8fafc;">
                    RESPONSE ACTION QUEUE • IMMINENT CASH-OUT TRIAGE
                </div>
                <div style="font-size: 0.76rem; color: #8b949e; margin-top: 0.2rem;">
                    Priority-ranked bank corridors flagging imminent siphon-off at CSPs and ATMs.
                </div>
            </div>
            <div style="font-family: 'Electrolize', sans-serif; font-size: 0.75rem; color: #e11d48; font-weight: 700; background: rgba(225, 29, 72, 0.1); border: 1px solid #e11d48; padding: 0.35rem 0.75rem; border-radius: 4px;">
                LEGAL POWERS: SEC 91 BNSS / CRPC
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
                <div style="background: #131824; border: 1px solid #222c3d; border-radius: 6px; padding: 1rem; margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <span class="status-badge {status_class}">{status}</span>
                        <span style="font-family: 'Electrolize', sans-serif; font-size: 0.75rem; color: #e11d48; font-weight: 700;">
                            {alert.get('priority')} PRIORITY ({prob}% CONFIDENCE)
                        </span>
                    </div>
                    <div style="margin-bottom: 0.75rem;">
                        <div style="font-size: 0.7rem; color: #8b949e; font-family: 'Electrolize', sans-serif; text-transform: uppercase;">
                            Threat Velocity Meter
                        </div>
                        <div class="threat-bar-container" style="height: 12px; margin-top: 0.25rem;">
                            <div class="threat-bar-fill" style="width: {prob}%;"></div>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.82rem;">
                        <div>
                            <span style="color: #8b949e;">Target Node:</span> <b>{alert.get('node_name')}</b><br>
                            <span style="color: #8b949e;">Bank:</span> <b>{alert.get('bank_name')}</b><br>
                            <span style="color: #8b949e;">Linked NCRP Ref:</span> <code style="color: #60a5fa;">{alert.get('complaint_ref')}</code>
                        </div>
                        <div>
                            <span style="color: #8b949e;">Beneficiary Bank:</span> <b>{alert.get('beneficiary_bank')}</b><br>
                            <span style="color: #8b949e;">Beneficiary Account:</span> <code style="color: #f43f5e;">{alert.get('beneficiary_account')}</code><br>
                            <span style="color: #8b949e;">Amount at Risk:</span> <b style="color: #e11d48;">₹{loss:,.0f}</b>
                        </div>
                    </div>
                    <div style="margin-top: 0.6rem; padding-top: 0.6rem; border-top: 1px solid #222c3d; font-size: 0.78rem; color: #cbd5e1;">
                        <b>Detection Logic:</b> {alert.get('reason_text')}
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
                    <div style="background: rgba(225, 29, 72, 0.08); border: 1px solid #e11d48; border-radius: 6px; padding: 0.75rem; margin-top: 0.75rem;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #fecdd3; margin-bottom: 0.35rem;">
                            OFFICIAL LEGAL ADVISORY: {advisory.get('notice_ref')}
                        </div>
                        <div style="font-size: 0.74rem; color: #8b949e; margin-bottom: 0.5rem;">
                            Dispatched to Nodal Fraud Desk: {advisory.get('recipient_bank')} • Account: {advisory.get('target_account')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.text_area("Advisory Text (Ready to Dispatch)", advisory.get("advisory_text", ""), height=180, key=f"text-{alert.get('id')}")

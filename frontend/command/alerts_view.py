import streamlit as st

from frontend import api_client


def render() -> None:
    st.markdown("## Alert Triage & Bank Freeze Notices")
    alerts = api_client.command_list("/api/v1/alerts", "alerts")
    if not alerts:
        st.info("No alerts available.")
        return
    for alert in alerts:
        title = f"{alert.get('alert_code')} | {alert.get('priority')} | {alert.get('district')} | {alert.get('status')}"
        with st.expander(title, expanded=alert.get("status") == "OPEN"):
            st.write(f"**Node:** {alert.get('node_name')} ({alert.get('bank_name')})")
            st.write(f"**Complaint:** {alert.get('complaint_ref')} | **Probability:** {alert.get('probability_pct')}%")
            st.write(f"**Reason:** {alert.get('reason_text')}")
            st.write(f"**Beneficiary:** {alert.get('beneficiary_bank')} / {alert.get('beneficiary_account')} | ₹{alert.get('loss_amount_inr', 0):,.0f}")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Generate Sec 91 Notice", key=f"adv-{alert.get('id')}"):
                    advisory = api_client.generate_advisory(alert.get("id") or alert.get("alert_code"))
                    if advisory:
                        st.session_state[f"advisory-{alert.get('id')}"] = advisory
            with c2:
                next_status = {"OPEN": "DISPATCHED", "DISPATCHED": "ACKNOWLEDGED", "ACKNOWLEDGED": "RESOLVED"}.get(alert.get("status"))
                if next_status and st.button(f"Mark {next_status}", key=f"status-{alert.get('id')}"):
                    updated = api_client.update_alert(alert.get("id") or alert.get("alert_code"), next_status, "Updated from PRAHARI console")
                    if updated:
                        st.success(f"Alert moved to {next_status}.")
                        st.rerun()
            advisory = st.session_state.get(f"advisory-{alert.get('id')}")
            if advisory:
                st.success(f"Notice {advisory.get('notice_ref')} generated for {advisory.get('recipient_bank')}.")
                st.text_area("Advisory text", advisory.get("advisory_text", ""), height=220, key=f"text-{alert.get('id')}")

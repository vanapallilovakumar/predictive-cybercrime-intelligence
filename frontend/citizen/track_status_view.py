import streamlit as st

from frontend import api_client


def render() -> None:
    st.markdown("## Track Complaint Status")
    reference = st.text_input("Complaint reference", value=st.session_state.get("last_reference", "NCRP/2026/000181"))
    if st.button("Check Status", type="primary"):
        result = api_client.track(reference)
        if not result:
            st.error("Complaint reference not found.")
            return
        status = result.get("tracking_status", "Under Review")
        status_class = {"Under Review": "status-review", "Investigation Active": "status-active", "Criminal Traced": "status-recovered", "Money Recovered": "status-recovered", "Returned to Victim": "status-returned"}.get(status, "status-review")
        st.markdown(f'<span class="status-badge {status_class}">{status}</span>', unsafe_allow_html=True)
        st.write(f"**{result.get('reference_no')}** | {result.get('typology')} | ₹{result.get('loss_amount_inr', 0):,.0f}")
        st.write(f"**Victim bank:** {result.get('victim_bank_name')} ({result.get('victim_account_no')})")
        st.write(f"**Assigned officer:** {result.get('assigned_officer')}")
        st.info(result.get("status_notes", "Under active review."))
        steps = ["Complaint lodged & assigned", "Investigation active", "Criminal traced / funds recovered", "Money returned to victim"]
        current = int(result.get("status_step", 1))
        for index, label in enumerate(steps, 1):
            st.write(f"{'[x]' if index <= current else '[ ]'} {index}. {label}")

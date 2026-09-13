import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("TRACK")

    st.markdown(
        """
        <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #ffffff;">
                ■ CASE RESTITUTION TRACKER
            </div>
            <div style="font-size: 0.76rem; color: #a3a3a3; margin-top: 0.2rem;">
                Four-Stage Restitution Workflow under Section 503 BNSS / Court Restitution Mandate.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reference = st.text_input("Enter NCRP / PRAHARI Complaint Reference", value=st.session_state.get("last_reference", "NCRP/2026/000188"))

    if st.button("Track Case Progress", type="primary"):
        result = api_client.track(reference)
        if not result:
            st.error(f"Complaint reference '{reference}' not found in registry.")
            return

        status = result.get("tracking_status", "Under Review")
        current_step = int(result.get("status_step", 1))

        status_class = {
            "Under Review": "status-open",
            "Investigation Active": "status-dispatched",
            "Criminal Traced": "status-acknowledged",
            "Returned to Victim": "status-resolved",
        }.get(status, "status-open")

        st.markdown(
            f"""
            <div style="background: #000000; border: 1px solid #262626; border-radius: 2px; padding: 1.25rem; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <div>
                        <span class="status-badge {status_class}">{status}</span>
                        <span style="font-family: 'Electrolize', sans-serif; font-size: 0.95rem; font-weight: 800; margin-left: 0.75rem; color: #ffffff;">
                            {result.get('reference_no')}
                        </span>
                    </div>
                    <div style="font-family: 'Electrolize', sans-serif; font-size: 1.05rem; font-weight: 900; color: #ffffff;">
                        ₹{result.get('loss_amount_inr', 0):,.0f}
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.82rem; margin-bottom: 1rem; padding: 0.75rem; background: #000000; border: 1px solid #262626; border-radius: 2px;">
                    <div>
                        <span style="color: #a3a3a3;">Crime Typology:</span> <b style="color: #ffffff; font-weight: 700;">{result.get('typology')}</b><br>
                        <span style="color: #a3a3a3;">Victim Bank:</span> <b style="color: #ffffff; font-weight: 700;">{result.get('victim_bank_name')} ({result.get('victim_account_no')})</b>
                    </div>
                    <div>
                        <span style="color: #a3a3a3;">Investigating Officer:</span> <b style="color: #ffffff; font-weight: 700;">{result.get('assigned_officer')}</b><br>
                        <span style="color: #a3a3a3;">Latest Status Note:</span> <span style="color: #ffffff; font-weight: 800;">{result.get('status_notes')}</span>
                    </div>
                </div>

                <div style="font-size: 0.76rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.6rem;">
                    ■ RESTITUTION WORKFLOW PROGRESS:
                </div>
            """,
            unsafe_allow_html=True,
        )

        steps = [
            ("Stage 1", "Complaint Registered & Patrol Corridors Alerted"),
            ("Stage 2", "Investigation Active & Immediate Debit Freeze Issued"),
            ("Stage 3", "Mule Ring Located & Bank Account Interdicted"),
            ("Stage 4", "Funds Restituted to Victim (Sec 503 BNSS)"),
        ]

        for idx, (stage_code, stage_label) in enumerate(steps, 1):
            is_done = idx <= current_step
            bar_color = "#ffffff" if is_done else "#262626"
            text_color = "#ffffff" if is_done else "#737373"
            icon = "[✓]" if is_done else "[ ]"
            font_wt = "800" if is_done else "500"
            bg = "#121212" if is_done else "#000000"
            
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; margin-bottom: 0.35rem; background: {bg}; border-left: 2px solid {bar_color}; border-radius: 0 2px 2px 0;">
                    <div style="font-family: 'Electrolize', sans-serif; font-size: 0.75rem; font-weight: 800; color: {bar_color}; width: 28px;">{icon}</div>
                    <div style="font-size: 0.82rem; font-weight: {font_wt}; color: {text_color};">
                        <b>{stage_code}:</b> {stage_label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

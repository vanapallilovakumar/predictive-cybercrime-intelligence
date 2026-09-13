import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("TRACK")

    st.markdown(
        """
        <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #f8fafc;">
                CASE RESTITUTION TRACKER
            </div>
            <div style="font-size: 0.76rem; color: #8b949e; margin-top: 0.2rem;">
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
            <div style="background: #131824; border: 1px solid #222c3d; border-radius: 8px; padding: 1.25rem; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <div>
                        <span class="status-badge {status_class}">{status}</span>
                        <span style="font-family: 'Electrolize', sans-serif; font-size: 0.95rem; font-weight: 700; margin-left: 0.75rem; color: #f8fafc;">
                            {result.get('reference_no')}
                        </span>
                    </div>
                    <div style="font-family: 'Electrolize', sans-serif; font-size: 1.05rem; font-weight: 800; color: #e11d48;">
                        ₹{result.get('loss_amount_inr', 0):,.0f}
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.82rem; margin-bottom: 1rem; padding: 0.75rem; background: #171e2c; border-radius: 6px;">
                    <div>
                        <span style="color: #8b949e;">Crime Typology:</span> <b>{result.get('typology')}</b><br>
                        <span style="color: #8b949e;">Victim Bank:</span> <b>{result.get('victim_bank_name')} ({result.get('victim_account_no')})</b>
                    </div>
                    <div>
                        <span style="color: #8b949e;">Investigating Officer:</span> <b>{result.get('assigned_officer')}</b><br>
                        <span style="color: #8b949e;">Latest Status Note:</span> <span style="color: #60a5fa;">{result.get('status_notes')}</span>
                    </div>
                </div>

                <div style="font-size: 0.76rem; font-weight: 700; color: #8b949e; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.6rem;">
                    Restitution Workflow Progress:
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
            bar_color = "#10b981" if is_done else "#222c3d"
            text_color = "#f8fafc" if is_done else "#64748b"
            icon = "✓" if is_done else "○"
            
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; margin-bottom: 0.35rem; background: {'rgba(16, 185, 129, 0.08)' if is_done else 'transparent'}; border-left: 3px solid {bar_color}; border-radius: 0 4px 4px 0;">
                    <div style="font-family: 'Electrolize', sans-serif; font-size: 0.8rem; font-weight: 700; color: {bar_color}; width: 24px;">{icon}</div>
                    <div style="font-size: 0.82rem; font-weight: 600; color: {text_color};">
                        <b>{stage_code}:</b> {stage_label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

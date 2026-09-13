import streamlit as st

from frontend import api_client
from frontend import theme
from frontend.citizen import link_scanner_view, login_view, report_crime_view, safety_guidance_view, track_status_view
from frontend.command import alerts_view, hotspots_view, overview_view

st.set_page_config(page_title="PRAHARI & Cyber Safely", page_icon="P", layout="wide", initial_sidebar_state="expanded")
theme.apply_unified_theme(st.session_state.get("portal", "citizen"))


def render_header() -> None:
    st.markdown("# PRAHARI & Cyber Safely")
    st.caption("Predictive cybercrime intelligence and citizen protection")


if not st.session_state.get("authenticated"):
    render_header()
    login_view.render()
    st.stop()

user = st.session_state.get("user", {})
with st.sidebar:
    st.markdown("### Navigation")
    st.write(user.get("name", "Citizen User"))
    st.caption(user.get("email", ""))
    portal = st.radio("Portal", ["Citizen Safety", "Command Center"], index=0 if st.session_state.get("portal", "citizen") == "citizen" else 1)
    st.session_state["portal"] = "command" if portal == "Command Center" else "citizen"
    if st.button("Log out", use_container_width=True):
        for key in ("authenticated", "user", "otp_requested", "login_email"):
            st.session_state.pop(key, None)
        st.rerun()

render_header()
if st.session_state["portal"] == "citizen":
    page = st.selectbox("Cyber Safely", ["Check Suspicious Link", "Report Cybercrime", "Track Complaint", "Safety Guidance"])
    {"Check Suspicious Link": link_scanner_view.render, "Report Cybercrime": report_crime_view.render, "Track Complaint": track_status_view.render, "Safety Guidance": safety_guidance_view.render}[page]()
else:
    page = st.selectbox("PRAHARI Command", ["Overview", "Hotspots", "Alerts"])
    {"Overview": overview_view.render, "Hotspots": hotspots_view.render, "Alerts": alerts_view.render}[page]()

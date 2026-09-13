import streamlit as st

from frontend import api_client
from frontend import theme
from frontend.citizen import link_scanner_view, login_view, report_crime_view, safety_guidance_view, track_status_view
from frontend.command import alerts_view, hotspots_view, overview_view

st.set_page_config(
    page_title="Prahari • Cyber Saver",
    page_icon="docs/logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)

portal_mode = st.session_state.get("portal", "command")
theme.apply_unified_theme(portal_mode)

if not st.session_state.get("authenticated"):
    theme.render_tactical_header(
        title="Prahari",
        subtitle="Cyber Saver"
    )
    login_view.render()
    st.stop()

user = st.session_state.get("user", {})
user_role = user.get("role", "citizen")

with st.sidebar:
    logo_sidebar = theme.get_logo_img(40)
    st.markdown(
        f"""
        <div style="padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid #262626; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                {logo_sidebar}
                <div>
                    <div style="font-weight: 900; font-size: 1.2rem; letter-spacing: 0.08em; color: #ffffff; line-height: 1.1;">
                        PRAHARI
                    </div>
                    <div style="font-size: 0.68rem; color: #a3a3a3; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.2rem;">
                        Cyber Saver
                    </div>
                </div>
            </div>
            <div style="font-size: 0.72rem; color: #737373; margin-top: 0.6rem; font-family: 'Electrolize', sans-serif;">
                OPERATOR: <span style="color: #ffffff; font-weight: 800;">{user.get("name", "Operator")}</span>
            </div>
            <div style="font-size: 0.68rem; color: #ffffff; font-weight: 800; margin-top: 0.2rem; letter-spacing: 0.05em;">
                [●] AUTHENTICATED
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size: 0.7rem; font-weight: 800; letter-spacing: 0.12em; color: #ffffff; text-transform: uppercase; margin-bottom: 0.5rem;">[ PORTAL MODE ]</div>',
        unsafe_allow_html=True,
    )
    portal = st.radio(
        "Select Portal",
        ["Command Center", "Citizen Safety"],
        index=0 if st.session_state.get("portal", "command") == "command" else 1,
        label_visibility="collapsed",
    )
    st.session_state["portal"] = "command" if portal == "Command Center" else "citizen"

    st.markdown('<div style="height: 1.25rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size: 0.7rem; font-weight: 800; letter-spacing: 0.12em; color: #ffffff; text-transform: uppercase; margin-bottom: 0.5rem;">[ NAVIGATION ]</div>',
        unsafe_allow_html=True,
    )

    if st.session_state["portal"] == "command":
        cmd_pages = ["Threat Triage & Overview", "H3 Spatial Radar", "Alert Queue & Freeze Notices", "API Documentation"]
        default_cmd = st.session_state.get("cmd_page", "Threat Triage & Overview")
        cmd_idx = cmd_pages.index(default_cmd) if default_cmd in cmd_pages else 0
        page = st.radio(
            "Command Navigation",
            cmd_pages,
            index=cmd_idx,
            label_visibility="collapsed",
        )
        st.session_state["cmd_page"] = page
    else:
        cit_pages = ["Link Security Checker", "Lodge Complaint", "Track Case Restitution", "Safety Guidance", "System Health"]
        default_cit = st.session_state.get("cit_page", "Link Security Checker")
        cit_idx = cit_pages.index(default_cit) if default_cit in cit_pages else 0
        page = st.radio(
            "Citizen Navigation",
            cit_pages,
            index=cit_idx,
            label_visibility="collapsed",
        )
        st.session_state["cit_page"] = page

    st.markdown('<div style="height: 2.5rem;"></div>', unsafe_allow_html=True)
    if st.button("End Session / Logout", use_container_width=True):
        for key in ("authenticated", "user", "otp_requested", "login_email"):
            st.session_state.pop(key, None)
        st.rerun()


# Top Section: Header & Slim Side-by-Side Routes Strip
if st.session_state["portal"] == "command":
    theme.render_tactical_header(
        title="Prahari Command",
        subtitle="Cyber Saver"
    )

    # Top Slim Side-by-Side Routes Buttons (Names Only - Direct Navigation)
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem; padding-bottom: 0.25rem; border-bottom: 1px solid #262626;">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; color: #ffffff; text-transform: uppercase;">
                [ ROUTES ]
            </div>
            <div style="font-size: 0.68rem; color: #737373; letter-spacing: 0.05em;">
                PROTOCOL: MHA-SIH26184
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    r_cols = st.columns(9)
    if r_cols[0].button("Stats", key="rt_stats", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.rerun()
    if r_cols[1].button("Timing", key="rt_timing", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.rerun()
    if r_cols[2].button("Risk", key="rt_risk", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.rerun()
    if r_cols[3].button("Mix", key="rt_mix", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.rerun()
    if r_cols[4].button("Radar", key="rt_radar", use_container_width=True):
        st.session_state["cmd_page"] = "H3 Spatial Radar"
        st.rerun()
    if r_cols[5].button("Alerts", key="rt_alerts", use_container_width=True):
        st.session_state["cmd_page"] = "Alert Queue & Freeze Notices"
        st.rerun()
    if r_cols[6].button("Freeze", key="rt_freeze", use_container_width=True):
        st.session_state["cmd_page"] = "Alert Queue & Freeze Notices"
        st.rerun()
    if r_cols[7].button("Scenarios", key="rt_scen", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.rerun()
    if r_cols[8].button("Docs", key="rt_docs", use_container_width=True):
        st.session_state["cmd_page"] = "API Documentation"
        st.rerun()

    st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)

    if page == "Threat Triage & Overview":
        overview_view.render()
    elif page == "H3 Spatial Radar":
        hotspots_view.render()
    elif page == "Alert Queue & Freeze Notices":
        alerts_view.render()
    elif page == "API Documentation":
        st.markdown(
            """
            <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 1.25rem; margin-bottom: 1rem;">
                <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff; letter-spacing: 0.05em; margin-bottom: 0.35rem;">
                    ■ PRAHARI API SPECIFICATION // OPENAPI 3.1
                </div>
                <div style="font-size: 0.75rem; color: #a3a3a3; margin-bottom: 1rem;">
                    Full interactive Swagger documentation and REST endpoints for SIH26184 integration.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem;">
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <b style="color: #ffffff; font-weight: 800;">GET /docs</b><br>
                        <span style="font-size: 0.72rem; color: #a3a3a3;">Interactive Swagger UI with test console.</span>
                    </div>
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <b style="color: #ffffff; font-weight: 800;">GET /api/v1/alerts</b><br>
                        <span style="font-size: 0.72rem; color: #a3a3a3;">Live threat triage queue with loss velocity ratings.</span>
                    </div>
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <b style="color: #ffffff; font-weight: 800;">GET /api/v1/hotspots</b><br>
                        <span style="font-size: 0.72rem; color: #a3a3a3;">Uber H3 resolution 8 spatial anomaly cells.</span>
                    </div>
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <b style="color: #ffffff; font-weight: 800;">POST /api/v1/cyber-safely/report-crime</b><br>
                        <span style="font-size: 0.72rem; color: #a3a3a3;">Automated incident ingestion & Section 91 dispatch.</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("Launch Swagger OpenAPI Console (/docs)", "/docs", use_container_width=True)

else:
    theme.render_tactical_header(
        title="Prahari Citizen",
        subtitle="Cyber Saver"
    )

    # Top Slim Side-by-Side Routes Buttons (Names Only - Direct Navigation)
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem; padding-bottom: 0.25rem; border-bottom: 1px solid #262626;">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; color: #ffffff; text-transform: uppercase;">
                [ ROUTES ]
            </div>
            <div style="font-size: 0.68rem; color: #737373; letter-spacing: 0.05em;">
                DIAL: 1930
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_cols = st.columns(5)
    if c_cols[0].button("Scanner", key="rt_cit_scan", use_container_width=True):
        st.session_state["cit_page"] = "Link Security Checker"
        st.rerun()
    if c_cols[1].button("Report", key="rt_cit_rep", use_container_width=True):
        st.session_state["cit_page"] = "Lodge Complaint"
        st.rerun()
    if c_cols[2].button("Track", key="rt_cit_trk", use_container_width=True):
        st.session_state["cit_page"] = "Track Case Restitution"
        st.rerun()
    if c_cols[3].button("Guidance", key="rt_cit_guide", use_container_width=True):
        st.session_state["cit_page"] = "Safety Guidance"
        st.rerun()
    if c_cols[4].button("Health", key="rt_cit_health", use_container_width=True):
        st.session_state["cit_page"] = "System Health"
        st.rerun()

    st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)

    if page == "Link Security Checker":
        link_scanner_view.render()
    elif page == "Lodge Complaint":
        report_crime_view.render()
    elif page == "Track Case Restitution":
        track_status_view.render()
    elif page == "Safety Guidance":
        safety_guidance_view.render()
    elif page == "System Health":
        st.markdown(
            """
            <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 1.25rem;">
                <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff; letter-spacing: 0.05em; margin-bottom: 0.35rem;">
                    [✓] PRAHARI SYSTEM DIAGNOSTICS & TELEMETRY
                </div>
                <div style="font-size: 0.75rem; color: #a3a3a3; margin-bottom: 1rem;">
                    Universal health check status for local services and cloud resilience pipelines.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.75rem;">
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <span style="font-size: 0.7rem; color: #a3a3a3;">FASTAPI CORE</span><br>
                        <b style="color: #ffffff; font-weight: 900;">ONLINE (HTTP 200)</b>
                    </div>
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <span style="font-size: 0.7rem; color: #a3a3a3;">AI PREDICTIVE ENGINE</span><br>
                        <b style="color: #ffffff; font-weight: 900;">ACTIVE (HIST-GBT + DBSCAN)</b>
                    </div>
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <span style="font-size: 0.7rem; color: #a3a3a3;">SPATIAL RADAR INDEX</span><br>
                        <b style="color: #ffffff; font-weight: 900;">UBER H3 RES 8 READY</b>
                    </div>
                    <div style="border: 1px solid #262626; padding: 0.75rem; background: #050505;">
                        <span style="font-size: 0.7rem; color: #a3a3a3;">NCRP RESTITUTION PIPELINE</span><br>
                        <b style="color: #ffffff; font-weight: 900;">SEC 91 / 503 BNSS ENGAGED</b>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

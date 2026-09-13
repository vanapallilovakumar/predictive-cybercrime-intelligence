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
    logo_sidebar = theme.get_logo_img(44)
    st.markdown(
        f"""
        <div style="padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid #1b2536; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                {logo_sidebar}
                <div>
                    <div style="font-weight: 800; font-size: 1.25rem; letter-spacing: 0.08em; color: #ffffff; line-height: 1.1;">
                        PRAHARI
                    </div>
                    <div style="font-size: 0.68rem; color: #00f0ff; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.2rem;">
                        Cyber Saver
                    </div>
                </div>
            </div>
            <div style="font-size: 0.72rem; color: #8b9cb0; margin-top: 0.6rem; font-family: 'Electrolize', sans-serif;">
                OPERATOR: <span style="color: #ffffff; font-weight: 600;">{user.get("name", "Operator")}</span>
            </div>
            <div style="font-size: 0.68rem; color: #00ff66; margin-top: 0.2rem; letter-spacing: 0.05em;">
                ■ RADAR LINK ONLINE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size: 0.7rem; font-weight: 800; letter-spacing: 0.12em; color: #00f0ff; text-transform: uppercase; margin-bottom: 0.5rem;">■ PORTAL MODE</div>',
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
        '<div style="font-size: 0.7rem; font-weight: 800; letter-spacing: 0.12em; color: #00f0ff; text-transform: uppercase; margin-bottom: 0.5rem;">■ TACTICAL QUEUE</div>',
        unsafe_allow_html=True,
    )

    if st.session_state["portal"] == "command":
        cmd_pages = ["Threat Triage & Overview", "H3 Spatial Radar", "Alert Queue & Freeze Notices"]
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
        cit_pages = ["Link Security Checker", "Lodge Complaint", "Track Case Restitution", "Safety Guidance"]
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

    # Top Slim Side-by-Side Routes Buttons (Only Names)
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem; padding-bottom: 0.25rem; border-bottom: 1px solid #1b2536;">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; color: #00f0ff; text-transform: uppercase;">
                ■ ROUTES // DISPATCH TELEMETRY
            </div>
            <div style="font-size: 0.68rem; color: #8b9cb0; letter-spacing: 0.05em;">
                PROTOCOL: MHA-SIH26184
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    r_cols = st.columns(9)
    if r_cols[0].button("Stats", key="rt_stats", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.session_state["preview_route"] = ("GET /api/v1/command/stats", api_client.command_stats())
        st.rerun()
    if r_cols[1].button("Timing", key="rt_timing", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.session_state["preview_route"] = ("GET /api/v1/command/timing-pattern", api_client.command_list("/api/v1/command/timing-pattern", "timing-pattern"))
        st.rerun()
    if r_cols[2].button("Risk", key="rt_risk", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.session_state["preview_route"] = ("GET /api/v1/command/district-risk", api_client.command_list("/api/v1/command/district-risk", "district-risk"))
        st.rerun()
    if r_cols[3].button("Mix", key="rt_mix", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.session_state["preview_route"] = ("GET /api/v1/command/typology-mix", api_client.command_list("/api/v1/command/typology-mix", "typology-mix"))
        st.rerun()
    if r_cols[4].button("Radar", key="rt_radar", use_container_width=True):
        st.session_state["cmd_page"] = "H3 Spatial Radar"
        st.session_state["preview_route"] = ("GET /api/v1/hotspots", api_client.command_list("/api/v1/hotspots", "hotspots"))
        st.rerun()
    if r_cols[5].button("Alerts", key="rt_alerts", use_container_width=True):
        st.session_state["cmd_page"] = "Alert Queue & Freeze Notices"
        st.session_state["preview_route"] = ("GET /api/v1/alerts", api_client.command_list("/api/v1/alerts", "alerts"))
        st.rerun()
    if r_cols[6].button("Freeze", key="rt_freeze", use_container_width=True):
        st.session_state["cmd_page"] = "Alert Queue & Freeze Notices"
        st.rerun()
    if r_cols[7].button("Scenarios", key="rt_scen", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.session_state["preview_route"] = ("GET /api/v1/scenarios", api_client.scenarios())
        st.rerun()
    if r_cols[8].button("Docs", key="rt_docs", use_container_width=True):
        st.session_state["cmd_page"] = "Threat Triage & Overview"
        st.session_state["preview_route"] = ("GET /docs (Swagger OpenAPI UI)", {"swagger_url": "/docs", "openapi_spec": "/openapi.json", "status": "ONLINE"})
        st.rerun()

    # Telemetry Preview Modal / Accordion
    if st.session_state.get("preview_route"):
        route_name, route_data = st.session_state["preview_route"]
        with st.expander(f"◈ Live Telemetry Response: {route_name}", expanded=True):
            st.json(route_data)
            if st.button("Clear Preview", key="clr_cmd"):
                st.session_state.pop("preview_route", None)
                st.rerun()

    st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)

    if page == "Threat Triage & Overview":
        overview_view.render()
    elif page == "H3 Spatial Radar":
        hotspots_view.render()
    elif page == "Alert Queue & Freeze Notices":
        alerts_view.render()

else:
    theme.render_tactical_header(
        title="Prahari Citizen",
        subtitle="Cyber Saver"
    )

    # Top Slim Side-by-Side Routes Buttons (Only Names)
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem; padding-bottom: 0.25rem; border-bottom: 1px solid #1b2536;">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; color: #00f0ff; text-transform: uppercase;">
                ■ ROUTES // CITIZEN PROTECTION
            </div>
            <div style="font-size: 0.68rem; color: #8b9cb0; letter-spacing: 0.05em;">
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
        st.session_state["preview_cit_route"] = ("GET /api/v1/cyber-safely/track/NCRP/2026/000188", api_client.track("NCRP/2026/000188"))
        st.rerun()
    if c_cols[3].button("Guidance", key="rt_cit_guide", use_container_width=True):
        st.session_state["cit_page"] = "Safety Guidance"
        st.session_state["preview_cit_route"] = ("GET /api/v1/cyber-safely/guidance", api_client.guidance())
        st.rerun()
    if c_cols[4].button("Health", key="rt_cit_health", use_container_width=True):
        st.session_state["preview_cit_route"] = ("GET /health", {"status": "online", "service": "Prahari • Cyber Saver Engine", "version": "2.0.0"})
        st.rerun()

    # Telemetry Preview Modal / Accordion
    if st.session_state.get("preview_cit_route"):
        route_name, route_data = st.session_state["preview_cit_route"]
        with st.expander(f"◈ Live Telemetry Response: {route_name}", expanded=True):
            st.json(route_data)
            if st.button("Clear Preview", key="clr_cit"):
                st.session_state.pop("preview_cit_route", None)
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

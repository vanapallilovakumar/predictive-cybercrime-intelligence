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
        <div style="padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid #222c3d; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                {logo_sidebar}
                <div>
                    <div style="font-weight: 800; font-size: 1.25rem; letter-spacing: 0.06em; color: #f8fafc; line-height: 1.1;">
                        PRAHARI
                    </div>
                    <div style="font-size: 0.68rem; color: #e11d48; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.2rem;">
                        Cyber Saver
                    </div>
                </div>
            </div>
            <div style="font-size: 0.72rem; color: #8b949e; margin-top: 0.6rem; font-family: 'Electrolize', sans-serif;">
                USER: <span style="color: #f8fafc; font-weight: 600;">{user.get("name", "Operator")}</span>
            </div>
            <div style="font-size: 0.68rem; color: #10b981; margin-top: 0.2rem;">
                ● SESSION AUTHENTICATED
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size: 0.7rem; font-weight: 800; letter-spacing: 0.12em; color: #8b949e; text-transform: uppercase; margin-bottom: 0.5rem;">PORTAL MODE</div>',
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
        '<div style="font-size: 0.7rem; font-weight: 800; letter-spacing: 0.12em; color: #8b949e; text-transform: uppercase; margin-bottom: 0.5rem;">RESPONSE ACTION QUEUE</div>',
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


# Top Section: Header & Top-Left Routes Box
if st.session_state["portal"] == "command":
    theme.render_tactical_header(
        title="Prahari Command",
        subtitle="Cyber Saver"
    )

    # Top-Left "Routes" Box for Command Center
    c_routes, c_space = st.columns([2.2, 2.8])
    with c_routes:
        with st.expander("📍 Routes • Command Center (Click to Open)", expanded=False):
            st.markdown(
                '<div style="font-size: 0.75rem; color: #8b949e; margin-bottom: 0.5rem;">Click any endpoint below to open that route and preview live data:</div>',
                unsafe_allow_html=True,
            )

            # Route 1: Stats & Overview
            if st.button("GET  /api/v1/command/stats ➔ [Overview: KPIs]", use_container_width=True):
                st.session_state["cmd_page"] = "Threat Triage & Overview"
                st.session_state["preview_route"] = ("GET /api/v1/command/stats", api_client.command_stats())
                st.rerun()

            # Route 2: Timing Pattern
            if st.button("GET  /api/v1/command/timing-pattern ➔ [Overview: 24h Velocity]", use_container_width=True):
                st.session_state["cmd_page"] = "Threat Triage & Overview"
                st.session_state["preview_route"] = ("GET /api/v1/command/timing-pattern", api_client.command_list("/api/v1/command/timing-pattern", "timing-pattern"))
                st.rerun()

            # Route 3: District Risk
            if st.button("GET  /api/v1/command/district-risk ➔ [Overview: Risk Bars]", use_container_width=True):
                st.session_state["cmd_page"] = "Threat Triage & Overview"
                st.session_state["preview_route"] = ("GET /api/v1/command/district-risk", api_client.command_list("/api/v1/command/district-risk", "district-risk"))
                st.rerun()

            # Route 4: Hotspots
            if st.button("GET  /api/v1/hotspots ➔ [H3 Spatial Radar Map]", use_container_width=True):
                st.session_state["cmd_page"] = "H3 Spatial Radar"
                st.session_state["preview_route"] = ("GET /api/v1/hotspots", api_client.command_list("/api/v1/hotspots", "hotspots"))
                st.rerun()

            # Route 5: Alerts & Triage
            if st.button("GET  /api/v1/alerts ➔ [Alert Queue & Triage]", use_container_width=True):
                st.session_state["cmd_page"] = "Alert Queue & Freeze Notices"
                st.session_state["preview_route"] = ("GET /api/v1/alerts", api_client.command_list("/api/v1/alerts", "alerts"))
                st.rerun()

            # Route 6: Freeze Advisory
            if st.button("POST /api/v1/alerts/{id}/generate-advisory ➔ [Sec 91 Freeze]", use_container_width=True):
                st.session_state["cmd_page"] = "Alert Queue & Freeze Notices"
                st.rerun()

            # Route 7: Scenarios
            if st.button("GET  /api/v1/scenarios ➔ [Threat Simulation Corridors]", use_container_width=True):
                st.session_state["cmd_page"] = "Threat Triage & Overview"
                st.session_state["preview_route"] = ("GET /api/v1/scenarios", api_client.scenarios())
                st.rerun()

            # Live Route Preview Accordion
            if st.session_state.get("preview_route"):
                route_name, route_data = st.session_state["preview_route"]
                with st.expander(f"⚡ Live Telemetry: {route_name}", expanded=True):
                    st.json(route_data)
                    if st.button("Clear Route Preview"):
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

    # Top-Left "Routes" Box for Citizen Safety
    c_routes, c_space = st.columns([2.2, 2.8])
    with c_routes:
        with st.expander("📍 Routes • Citizen Safety (Click to Open)", expanded=False):
            st.markdown(
                '<div style="font-size: 0.75rem; color: #8b949e; margin-bottom: 0.5rem;">Click any endpoint below to open that route and preview live data:</div>',
                unsafe_allow_html=True,
            )

            # Route 1: Link Scanner
            if st.button("POST /api/v1/cyber-safely/scan-link ➔ [Link Scanner]", use_container_width=True):
                st.session_state["cit_page"] = "Link Security Checker"
                st.rerun()

            # Route 2: Report Crime
            if st.button("POST /api/v1/cyber-safely/report-crime ➔ [Lodge Complaint]", use_container_width=True):
                st.session_state["cit_page"] = "Lodge Complaint"
                st.rerun()

            # Route 3: Track Status
            if st.button("GET  /api/v1/cyber-safely/track/{ref} ➔ [Track Case]", use_container_width=True):
                st.session_state["cit_page"] = "Track Case Restitution"
                st.session_state["preview_cit_route"] = ("GET /api/v1/cyber-safely/track/NCRP/2026/000188", api_client.track("NCRP/2026/000188"))
                st.rerun()

            # Route 4: Safety Guidance
            if st.button("GET  /api/v1/cyber-safely/guidance ➔ [Safety Guidance]", use_container_width=True):
                st.session_state["cit_page"] = "Safety Guidance"
                st.session_state["preview_cit_route"] = ("GET /api/v1/cyber-safely/guidance", api_client.guidance())
                st.rerun()

            # Live Route Preview Accordion
            if st.session_state.get("preview_cit_route"):
                route_name, route_data = st.session_state["preview_cit_route"]
                with st.expander(f"⚡ Live Telemetry: {route_name}", expanded=True):
                    st.json(route_data)
                    if st.button("Clear Route Preview"):
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

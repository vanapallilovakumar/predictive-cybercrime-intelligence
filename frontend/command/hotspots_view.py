import folium
import streamlit as st
from streamlit_folium import st_folium

from frontend import api_client
from frontend import theme
from backend.ml_pipeline.features import h3_to_geo_boundary_safe


def render() -> None:
    theme.render_watermark("RADAR")

    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.25rem;">
            <div>
                <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #f8fafc;">
                    H3 SPATIO-TEMPORAL RISK RADAR
                </div>
                <div style="font-size: 0.76rem; color: #8b949e; margin-top: 0.2rem;">
                    Uber H3 Resolution 8 Hexagonal Clustering forecasting cash-out density corridors.
                </div>
            </div>
            <div style="font-family: 'Electrolize', sans-serif; font-size: 0.75rem; color: #10b981; font-weight: 700; background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 0.35rem 0.75rem; border-radius: 4px;">
                AI PIPELINE: HIST-GBT + DBSCAN
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_ctrl, c_legend = st.columns([2, 2])
    with c_ctrl:
        horizon = st.select_slider("Forecast Prediction Horizon", options=[2, 4, 6], value=6, format_func=lambda val: f"Next {val} Hours")
    with c_legend:
        st.markdown(
            """
            <div style="display: flex; gap: 1rem; justify-content: flex-end; align-items: center; height: 100%; font-size: 0.74rem; font-family: 'Electrolize', sans-serif;">
                <span style="color: #ef4444;">■ HIGH THREAT (>70%)</span>
                <span style="color: #f59e0b;">■ WATCH ZONE (40-70%)</span>
                <span style="color: #64748b;">■ BASELINE (<40%)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    hotspots = api_client.command_list("/api/v1/hotspots", "hotspots")
    if not hotspots:
        st.info("No spatial telemetry cells found.")
        return

    center = [hotspots[0].get("center_lat", 24.2), hotspots[0].get("center_lon", 86.6)]
    fmap = folium.Map(location=center, zoom_start=7, tiles="CartoDB dark_matter")

    colors = {"HIGH": "#ff8800", "WATCH": "#00f0ff", "NORMAL": "#334155"}

    for cell in hotspots:
        prob = cell.get("probability_pct", 0)
        lat, lon = cell.get("center_lat"), cell.get("center_lon")
        popup_content = (
            f"<div style='font-family: sans-serif; font-size: 12px; color: #0f172a; min-width: 160px;'>"
            f"<b>{cell.get('district')} District</b><br>"
            f"<span style='color: #e11d48; font-weight: bold;'>Risk: {prob}% ({cell.get('risk_tier')})</span><br>"
            f"Horizon: Next {horizon}h<br>"
            f"Loss at Risk: ₹{cell.get('total_loss_at_risk_inr', 0):,.0f}<br>"
            f"<small>{cell.get('reason_text', '')}</small></div>"
        )
        boundary = h3_to_geo_boundary_safe(cell.get("h3_index", ""))
        tier_color = colors.get(cell.get("risk_tier"), "#475569")

        if boundary:
            folium.Polygon(
                locations=boundary,
                color=tier_color,
                fill=True,
                fill_color=tier_color,
                fill_opacity=0.6,
                weight=2,
                popup=folium.Popup(popup_content, max_width=250),
            ).add_to(fmap)
        else:
            folium.CircleMarker(
                [lat, lon],
                radius=12 + prob / 10,
                color=tier_color,
                fill=True,
                fill_color=tier_color,
                fill_opacity=0.75,
                popup=folium.Popup(popup_content, max_width=250),
            ).add_to(fmap)

    st_folium(fmap, use_container_width=True, height=520)

    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size: 0.82rem; font-weight: 700; color: #8b949e; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Spatial Cell Telemetry Table</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(hotspots, use_container_width=True, hide_index=True)

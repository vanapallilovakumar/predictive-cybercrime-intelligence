import folium
import streamlit as st
from streamlit_folium import st_folium

from frontend import api_client
from backend.ml_pipeline.features import h3_to_geo_boundary_safe


def render() -> None:
    st.markdown("## Predictive H3 Hotspots")
    st.caption("Decision support only: validate each lead with the assigned investigator and bank nodal desk.")
    horizon = st.select_slider("Forecast horizon", options=[2, 4, 6], value=6, format_func=lambda value: f"Next {value} hours")
    hotspots = api_client.command_list("/api/v1/hotspots", "hotspots")
    if not hotspots:
        st.info("No forecast cells available.")
        return
    center = [hotspots[0].get("center_lat", 23.5), hotspots[0].get("center_lon", 85.5)]
    fmap = folium.Map(location=center, zoom_start=6, tiles="CartoDB dark_matter")
    colors = {"HIGH": "#ef4444", "WATCH": "#f59e0b", "NORMAL": "#64748b"}
    for cell in hotspots:
        probability = cell.get("probability_pct", 0)
        lat, lon = cell.get("center_lat"), cell.get("center_lon")
        popup = f"<b>{cell.get('district')}</b><br>{probability}% risk<br>Next {horizon}h<br>{cell.get('reason_text')}<br>Loss at risk: ₹{cell.get('total_loss_at_risk_inr', 0):,.0f}"
        boundary = h3_to_geo_boundary_safe(cell.get("h3_index", ""))
        if boundary:
            folium.Polygon(
                locations=boundary,
                color=colors.get(cell.get("risk_tier"), "#64748b"),
                fill=True,
                fill_color=colors.get(cell.get("risk_tier"), "#64748b"),
                fill_opacity=0.55,
                weight=2,
                popup=popup,
            ).add_to(fmap)
        else:
            folium.CircleMarker([lat, lon], radius=10 + probability / 12, color=colors.get(cell.get("risk_tier"), "#64748b"), fill=True, fill_opacity=.7, popup=popup).add_to(fmap)
    st_folium(fmap, use_container_width=True, height=560)
    st.dataframe(hotspots, use_container_width=True, hide_index=True)

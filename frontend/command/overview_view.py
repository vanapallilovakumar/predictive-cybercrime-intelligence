import pandas as pd
import streamlit as st

from frontend import api_client


def render() -> None:
    st.markdown("## PRAHARI Command Overview")
    scenario_items = api_client.scenarios()
    if scenario_items:
        active = next((item for item in scenario_items if item.get("is_active")), scenario_items[0])
        scenario_names = {item.get("name"): item.get("id") for item in scenario_items}
        selected_name = st.selectbox("Simulation scenario", list(scenario_names), index=list(scenario_names).index(active.get("name")))
        if st.button("Activate scenario"):
            result = api_client.activate_scenario(scenario_names[selected_name])
            if result and result.get("success"):
                st.success(f"Active scenario: {selected_name}")
                st.rerun()
    stats = api_client.command_stats()
    metrics = [
        ("Complaints / loss at risk", f"{stats.get('active_complaints', 0)} / ₹{stats.get('loss_at_risk_inr', 0):,.0f}"),
        ("Open alerts", stats.get("open_alerts", 0)),
        ("Monitored cash-out nodes", stats.get("monitored_nodes", 0)),
        ("Mean confidence", f"{stats.get('mean_confidence_pct', 0)}%"),
    ]
    columns = st.columns(4)
    for column, (label, value) in zip(columns, metrics):
        with column:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.markdown("### 24h cash-out timing")
        timing = api_client.command_list("/api/v1/command/timing-pattern", "timing-pattern")
        if timing:
            st.line_chart(pd.DataFrame(timing).set_index("hour")["cashouts"])
        st.markdown("### District risk")
        for item in api_client.command_list("/api/v1/command/district-risk", "district-risk"):
            st.progress(min(int(item.get("probability_pct", 0)), 100) / 100, text=f"{item.get('district')} - {item.get('probability_pct')}% ({item.get('tier')})")
        st.markdown("### Next opening windows")
        timing = api_client.command_list("/api/v1/command/timing-pattern", "timing-pattern")
        for item in sorted(timing, key=lambda value: value.get("cashouts", 0), reverse=True)[:3]:
            st.write(f"**{item.get('hour')}** — {item.get('cashouts')} predicted cash-outs")
    with right:
        st.markdown("### Typology mix")
        mix = api_client.command_list("/api/v1/command/typology-mix", "typology-mix")
        if mix:
            st.bar_chart(pd.DataFrame(mix).set_index("typology")["count"])
        st.markdown("### Anomalies")
        for item in api_client.command_list("/api/v1/command/anomalies", "anomalies"):
            st.warning(f"{item.get('severity')}: {item.get('title')} - {item.get('description')}")
    st.markdown("### Recent complaints")
    complaints = api_client.command_list("/api/v1/command/recent-complaints", "recent-complaints")
    if complaints:
        st.dataframe(pd.DataFrame(complaints)[["reference_no", "typology", "reported_district", "loss_amount_inr", "tracking_status"]], use_container_width=True, hide_index=True)

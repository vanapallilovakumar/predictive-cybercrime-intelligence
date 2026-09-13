import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    # 1. Simulation Scenario Switcher Bar (DataV HUD style)
    scenario_items = api_client.scenarios()
    if scenario_items:
        active = next((item for item in scenario_items if item.get("is_active")), scenario_items[0])
        scenario_names = {item.get("name"): item.get("id") for item in scenario_items}
        
        c_scen, c_act = st.columns([4, 1])
        with c_scen:
            selected_name = st.selectbox(
                "Active Threat Simulation Corridor",
                list(scenario_names),
                index=list(scenario_names).index(active.get("name")),
                label_visibility="collapsed"
            )
        with c_act:
            if st.button("Activate Corridor", use_container_width=True):
                result = api_client.activate_scenario(scenario_names[selected_name])
                if result and result.get("success"):
                    st.success(f"Corridor active: {selected_name}")
                    st.rerun()

    # 2. Key Telemetry Metrics Strip (Top KPIs matching DataV HUD)
    stats = api_client.command_stats()
    kpis = [
        ("Complaints / At Risk", f"{stats.get('active_complaints', 0)} / ₹{stats.get('loss_at_risk_inr', 0):,.0f}"),
        ("Active Triage Alerts", f"{stats.get('open_alerts', 0)} ACTIVE"),
        ("Monitored Cash-Out Nodes", stats.get("monitored_nodes", 0)),
        ("Model Confidence Score", f"{stats.get('mean_confidence_pct', 0)}%"),
    ]
    
    cols = st.columns(4)
    for col, (label, val) in zip(cols, kpis):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)

    # 3. Top Analytical Grid: Priority Score Bar Chart (Monochrome Wireframe aesthetic)
    c_chart, c_score = st.columns([3, 1])
    
    with c_chart:
        st.markdown(
            '<div style="font-size: 0.8rem; font-weight: 800; color: #ffffff; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.25rem;">■ 24H CASH-OUT VELOCITY // PRIORITY HUD</div>',
            unsafe_allow_html=True,
        )
        timing = api_client.command_list("/api/v1/command/timing-pattern", "timing-pattern")
        if timing:
            df_timing = pd.DataFrame(timing)
            hours = df_timing["hour"].tolist()
            cashouts = df_timing["cashouts"].tolist()

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=hours,
                        y=cashouts,
                        marker=dict(
                            color="#ffffff",
                            line=dict(color="#ffffff", width=1),
                        ),
                        hovertemplate="<b>Hour %{x}</b><br>Predicted Cash-Outs: %{y}<extra></extra>",
                    )
                ]
            )
            fig.update_layout(
                plot_bgcolor="#000000",
                paper_bgcolor="#000000",
                margin=dict(l=10, r=10, t=15, b=10),
                height=165,
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(color="#a3a3a3", size=9, family="Electrolize, sans-serif"),
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#262626",
                    tickfont=dict(color="#a3a3a3", size=9, family="Electrolize, sans-serif"),
                ),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c_score:
        st.markdown(
            '<div style="font-size: 0.8rem; font-weight: 800; color: #ffffff; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.25rem;">■ TELEMETRY SCORE</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style="background: #000000; border: 1px solid #262626; border-radius: 2px; padding: 0.75rem; height: 165px; display: flex; flex-direction: column; justify-content: space-around;">
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #a3a3a3;">
                    SURGE INDEX: <span style="color: #ffffff; font-weight: 900;">136.4 (HIGH)</span>
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #a3a3a3;">
                    GOLDEN HOUR: <span style="color: #ffffff; font-weight: 800;">< 82 MINS</span>
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #a3a3a3;">
                    FREEZE SUCCESS: <span style="color: #ffffff; font-weight: 800;">89.2%</span>
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #a3a3a3;">
                    CORRIDOR: <span style="color: #ffffff; font-weight: 800;">JAMTARA-DEOGHAR</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4. Center Watermark
    theme.render_watermark("PRAHARI")

    # 5. Threat Log Table (DataV High-Tech Cyber Table)
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-size: 0.95rem; font-weight: 800; letter-spacing: 0.06em; color: #ffffff;">
                ■ THREAT LOG // INTERDICTION QUEUE
            </div>
            <div style="font-size: 0.72rem; color: #ffffff; font-family: 'Electrolize', sans-serif; letter-spacing: 0.05em; font-weight: 800;">
                [!] SEC 91 BNSS PROTOCOL ACTIVE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    alerts = api_client.command_list("/api/v1/alerts", "alerts")
    if alerts:
        # Table Header Row
        st.markdown(
            """
            <div style="display: grid; grid-template-columns: 1.4fr 1.6fr 2.5fr 1fr 1fr; background: #000000; border: 1px solid #262626; border-radius: 2px 2px 0 0; padding: 0.55rem 0.85rem; font-size: 0.7rem; font-weight: 700; color: #a3a3a3; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'Electrolize', sans-serif;">
                <div>Alert ID / Code</div>
                <div>Source & Bank</div>
                <div>Predicted Severity / Velocity</div>
                <div>Status</div>
                <div style="text-align: right;">Amount (INR)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for alert in alerts[:6]:
            prob = int(alert.get("probability_pct", 50))
            loss = float(alert.get("loss_amount_inr", 0))
            status = alert.get("status", "OPEN")
            status_class = "status-open" if status == "OPEN" else ("status-dispatched" if status == "DISPATCHED" else "status-acknowledged")
            
            st.markdown(
                f"""
                <div style="display: grid; grid-template-columns: 1.4fr 1.6fr 2.5fr 1fr 1fr; background: #000000; border-left: 1px solid #262626; border-right: 1px solid #262626; border-bottom: 1px solid #262626; padding: 0.65rem 0.85rem; font-size: 0.8rem; align-items: center;">
                    <div style="font-family: 'Electrolize', sans-serif; font-weight: 800; color: #ffffff;">
                        ■ {alert.get("alert_code")}
                    </div>
                    <div>
                        <div style="color: #ffffff; font-weight: 700;">{alert.get("node_name", "Target ATM")}</div>
                        <div style="font-size: 0.7rem; color: #a3a3a3;">{alert.get("bank_name", "Bank")} • {alert.get("district", "Deoghar")}</div>
                    </div>
                    <div style="padding-right: 1.25rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.68rem; font-family: 'Electrolize', sans-serif; margin-bottom: 0.2rem;">
                            <span style="color: #ffffff; font-weight: 900;">{alert.get("priority", "HIGH")} RISK</span>
                            <span style="color: #a3a3a3; font-weight: 600;">{prob}% PROBABILITY</span>
                        </div>
                        <div class="threat-bar-container">
                            <div class="threat-bar-fill" style="width: {prob}%;"></div>
                        </div>
                    </div>
                    <div>
                        <span class="status-badge {status_class}">{status}</span>
                    </div>
                    <div style="text-align: right; font-family: 'Electrolize', sans-serif; font-weight: 800; color: #ffffff;">
                        ₹{loss:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="height: 1.25rem;"></div>', unsafe_allow_html=True)

    # 6. Secondary Grid: District Risk & Real-Time Anomalies
    c_dist, c_anom = st.columns(2)

    with c_dist:
        st.markdown(
            '<div style="font-size: 0.8rem; font-weight: 800; color: #ffffff; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.4rem;">■ DISTRICT RISK RANKINGS</div>',
            unsafe_allow_html=True,
        )
        districts = api_client.command_list("/api/v1/command/district-risk", "district-risk")
        for item in (districts or [])[:4]:
            d_prob = min(int(item.get("probability_pct", 0)), 100)
            st.markdown(
                f"""
                <div style="background: #000000; border: 1px solid #262626; border-radius: 2px; padding: 0.6rem 0.8rem; margin-bottom: 0.35rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.76rem; font-weight: 600; margin-bottom: 0.25rem;">
                        <span>{item.get('district')} ({item.get('tier')})</span>
                        <span style="font-family: 'Electrolize', sans-serif; color: #ffffff; font-weight: 800;">{d_prob}%</span>
                    </div>
                    <div class="threat-bar-container" style="height: 6px;">
                        <div class="threat-bar-fill" style="width: {d_prob}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c_anom:
        st.markdown(
            '<div style="font-size: 0.8rem; font-weight: 900; color: #ffffff; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.4rem;">[!] LIVE TACTICAL ANOMALIES</div>',
            unsafe_allow_html=True,
        )
        anomalies = api_client.command_list("/api/v1/command/anomalies", "anomalies")
        for item in (anomalies or [])[:3]:
            st.markdown(
                f"""
                <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 0.6rem 0.8rem; margin-bottom: 0.35rem;">
                    <div style="font-size: 0.78rem; font-weight: 900; color: #ffffff;">{item.get('title')}</div>
                    <div style="font-size: 0.7rem; color: #a3a3a3; margin-top: 0.15rem;">{item.get('description')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

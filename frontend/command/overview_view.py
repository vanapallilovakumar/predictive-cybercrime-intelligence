import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    # 1. Simulation Scenario Switcher Bar
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
            if st.button("Activate Scenario", use_container_width=True):
                result = api_client.activate_scenario(scenario_names[selected_name])
                if result and result.get("success"):
                    st.success(f"Corridor active: {selected_name}")
                    st.rerun()

    # 2. Key Telemetry Metrics Strip (Top KPIs)
    stats = api_client.command_stats()
    kpis = [
        ("Active Complaints / At Risk", f"{stats.get('active_complaints', 0)} / ₹{stats.get('loss_at_risk_inr', 0):,.0f}"),
        ("High Priority Alerts", f"{stats.get('open_alerts', 0)} ACTIVE"),
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

    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

    # 3. Top Analytical Grid: Priority Score Bar Chart (Matching ui2.jpg)
    c_chart, c_score = st.columns([3, 1])
    
    with c_chart:
        st.markdown(
            '<div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.25rem;">Priority Score • 24H Cash-Out Velocity</div>',
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
                            color=cashouts,
                            colorscale=[
                                [0.0, "#ea580c"],
                                [0.35, "#f97316"],
                                [0.7, "#ef4444"],
                                [1.0, "#e11d48"],
                            ],
                            line=dict(color="#f43f5e", width=1),
                        ),
                        hovertemplate="<b>%{x}</b><br>Predicted Cash-Outs: %{y}<extra></extra>",
                    )
                ]
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(19, 24, 36, 0.6)",
                margin=dict(l=10, r=10, t=15, b=10),
                height=165,
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(color="#8b949e", size=9, family="Electrolize, sans-serif"),
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#222c3d",
                    tickfont=dict(color="#8b949e", size=9, family="Electrolize, sans-serif"),
                ),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c_score:
        st.markdown(
            '<div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.25rem;">Incident Score</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style="background: rgba(19, 24, 36, 0.6); border: 1px solid #222c3d; border-radius: 8px; padding: 0.75rem; height: 165px; display: flex; flex-direction: column; justify-content: space-around;">
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #8b949e;">
                    NODE SURGE INDEX: <span style="color: #e11d48; font-weight: 700;">HIGH (136.4)</span>
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #8b949e;">
                    GOLDEN HOUR WINDOW: <span style="color: #f59e0b; font-weight: 700;">< 82 MINS</span>
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #8b949e;">
                    FREEZE SUCCESS RATE: <span style="color: #10b981; font-weight: 700;">89.2%</span>
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.72rem; color: #8b949e;">
                    CORRIDOR INTEL: <span style="color: #60a5fa; font-weight: 700;">JAMTARA-DEOGHAR</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4. Center Watermark
    theme.render_watermark("PRAHARI")

    # 5. Threat Log Table (Direct visual replica of ui2.jpg)
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-size: 1.05rem; font-weight: 800; letter-spacing: 0.04em; color: #f8fafc;">
                THREAT LOG & INTERDICTION QUEUE
            </div>
            <div style="font-size: 0.75rem; color: #8b949e; font-family: 'Electrolize', sans-serif;">
                AUTO-REFRESH: 5s • PROTOCOL: SEC 91 BNSS
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
            <div style="display: grid; grid-template-columns: 1.4fr 1.6fr 2.5fr 1fr 1fr; background: #131824; border: 1px solid #222c3d; border-radius: 6px 6px 0 0; padding: 0.6rem 1rem; font-size: 0.72rem; font-weight: 700; color: #8b949e; text-transform: uppercase; letter-spacing: 0.06em; font-family: 'Electrolize', sans-serif;">
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
                <div style="display: grid; grid-template-columns: 1.4fr 1.6fr 2.5fr 1fr 1fr; background: #171e2c; border-left: 1px solid #222c3d; border-right: 1px solid #222c3d; border-bottom: 1px solid #222c3d; padding: 0.75rem 1rem; font-size: 0.82rem; align-items: center;">
                    <div style="font-family: 'Electrolize', sans-serif; font-weight: 700; color: #f8fafc;">
                        <span style="color: #e11d48; margin-right: 0.35rem;">■</span>{alert.get("alert_code")}
                    </div>
                    <div>
                        <div style="color: #f8fafc; font-weight: 600;">{alert.get("node_name", "Target ATM")}</div>
                        <div style="font-size: 0.72rem; color: #8b949e;">{alert.get("bank_name", "Bank")} • {alert.get("district", "Deoghar")}</div>
                    </div>
                    <div style="padding-right: 1.5rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; font-family: 'Electrolize', sans-serif; margin-bottom: 0.2rem;">
                            <span style="color: #e11d48; font-weight: 700;">{alert.get("priority", "HIGH")} RISK</span>
                            <span style="color: #8b949e;">{prob}% PROBABILITY</span>
                        </div>
                        <div class="threat-bar-container">
                            <div class="threat-bar-fill" style="width: {prob}%;"></div>
                        </div>
                    </div>
                    <div>
                        <span class="status-badge {status_class}">{status}</span>
                    </div>
                    <div style="text-align: right; font-family: 'Electrolize', sans-serif; font-weight: 700; color: #f8fafc;">
                        ₹{loss:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    # 6. Secondary Grid: District Risk & Real-Time Anomalies
    c_dist, c_anom = st.columns(2)

    with c_dist:
        st.markdown(
            '<div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;">District Risk Rankings</div>',
            unsafe_allow_html=True,
        )
        districts = api_client.command_list("/api/v1/command/district-risk", "district-risk")
        for item in (districts or [])[:4]:
            d_prob = min(int(item.get("probability_pct", 0)), 100)
            st.markdown(
                f"""
                <div style="background: #131824; border: 1px solid #222c3d; border-radius: 6px; padding: 0.65rem 0.85rem; margin-bottom: 0.4rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-weight: 600; margin-bottom: 0.3rem;">
                        <span>{item.get('district')} ({item.get('tier')})</span>
                        <span style="font-family: 'Electrolize', sans-serif; color: #e11d48;">{d_prob}%</span>
                    </div>
                    <div class="threat-bar-container" style="height: 8px;">
                        <div class="threat-bar-fill" style="width: {d_prob}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c_anom:
        st.markdown(
            '<div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;">Live Tactical Anomalies</div>',
            unsafe_allow_html=True,
        )
        anomalies = api_client.command_list("/api/v1/command/anomalies", "anomalies")
        for item in (anomalies or [])[:3]:
            st.markdown(
                f"""
                <div style="background: rgba(225, 29, 72, 0.08); border-left: 3px solid #e11d48; border-top: 1px solid #222c3d; border-right: 1px solid #222c3d; border-bottom: 1px solid #222c3d; border-radius: 0 6px 6px 0; padding: 0.65rem 0.85rem; margin-bottom: 0.4rem;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #fecdd3;">{item.get('title')}</div>
                    <div style="font-size: 0.72rem; color: #8b949e; margin-top: 0.2rem;">{item.get('description')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

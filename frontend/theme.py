import streamlit as st

BACKGROUND = "#0b0f19"
PANEL = "#111827"
BORDER = "#1f2937"
DANGER = "#ef4444"
AMBER = "#f59e0b"
SUCCESS = "#22c55e"
PRIMARY = "#3b82f6"
TEXT_MUTED = "#94a3b8"


def apply_unified_theme(mode: str = "citizen") -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {BACKGROUND};
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}
        [data-testid="stHeader"] {{ background: rgba(11,15,25,0.96); }}
        [data-testid="stSidebar"] {{ background: {PANEL}; border-right: 1px solid {BORDER}; }}
        .prahari-card {{
            background: {PANEL}; border: 1px solid {BORDER}; border-radius: 10px;
            padding: 1.1rem; margin-bottom: 1rem;
        }}
        .label-caps {{
            color: {TEXT_MUTED}; font-size: .72rem; font-weight: 700;
            letter-spacing: .08em; text-transform: uppercase;
        }}
        .metric-card {{
            background: {PANEL}; border: 1px solid {BORDER}; border-radius: 10px;
            padding: 1rem;
        }}
        .metric-value {{ font-size: 1.65rem; font-weight: 800; }}
        .metric-label {{ color: {TEXT_MUTED}; font-size: .78rem; }}
        .phishing-danger {{
            background: rgba(239,68,68,.12); border: 1px solid {DANGER};
            border-radius: 10px; padding: 1rem; color: #fecaca;
        }}
        .phishing-safe {{
            background: rgba(34,197,94,.12); border: 1px solid {SUCCESS};
            border-radius: 10px; padding: 1rem; color: #bbf7d0;
        }}
        .status-badge {{
            display: inline-block; padding: .35rem .8rem; border-radius: 999px;
            font-weight: 700; border: 1px solid currentColor;
        }}
        .status-review {{ color: #facc15; background: rgba(250,204,21,.12); }}
        .status-active {{ color: {AMBER}; background: rgba(245,158,11,.12); }}
        .status-recovered {{ color: #60a5fa; background: rgba(96,165,250,.12); }}
        .status-returned {{ color: {SUCCESS}; background: rgba(34,197,94,.12); }}
        .small-muted {{ color: {TEXT_MUTED}; font-size: .86rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str) -> None:
    st.markdown(
        f'<div class="prahari-card"><div class="label-caps">{title}</div>{body}</div>',
        unsafe_allow_html=True,
    )

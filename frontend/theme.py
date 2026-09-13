import streamlit as st

# Color Palette derived from docs/ui2.jpg (Dark Tactical Cybersecurity Console)
BG_MAIN = "#0d111a"
BG_PANEL = "#131824"
BG_CARD = "#171e2c"
BG_SURFACE_HOVER = "#1c2435"
BORDER = "#222c3d"
BORDER_ACCENT = "#2d3a50"

# Accents
ACCENT_RED = "#e11d48"
ACCENT_RED_GLOW = "rgba(225, 29, 72, 0.35)"
ACCENT_CORAL = "#f43f5e"
ACCENT_ORANGE = "#ea580c"
ACCENT_AMBER = "#f59e0b"
ACCENT_GREEN = "#10b981"
ACCENT_BLUE = "#3b82f6"

TEXT_WHITE = "#f8fafc"
TEXT_MUTED = "#8b949e"
TEXT_DIM = "#64748b"


def apply_unified_theme(mode: str = "citizen") -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Electrolize&display=swap');

        /* Universal Electrolize Font Override */
        *, html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], [data-testid="stMain"], .stApp, section.main, p, span, div, label, input, button, select, textarea, code, pre {{
            font-family: 'Electrolize', sans-serif !important;
        }}

        /* Root Application Base & Anti-White Screen Enforcers */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], [data-testid="stMain"], .stApp, section.main {{
            background: {BG_MAIN} !important;
            background-color: {BG_MAIN} !important;
            color: {TEXT_WHITE} !important;
        }}

        iframe {{
            background-color: {BG_MAIN} !important;
            color-scheme: dark;
        }}

        /* Header & Nav */
        [data-testid="stHeader"] {{
            background: rgba(13, 17, 26, 0.88) !important;
            backdrop-filter: blur(12px);
            border-bottom: 1px solid {BORDER};
        }}

        /* Sidebar - Response Action Queue aesthetic */
        [data-testid="stSidebar"] {{
            background: {BG_PANEL};
            border-right: 1px solid {BORDER};
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.5rem;
        }}

        /* Sidebar Navigation Radio Buttons */
        [data-testid="stSidebar"] .stRadio label {{
            color: {TEXT_MUTED} !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.03em !important;
            padding: 0.4rem 0.6rem !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
        }}
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {{
            background: {BG_SURFACE_HOVER} !important;
            color: {TEXT_WHITE} !important;
        }}

        /* Global Cards & Panels */
        .prahari-card {{
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        }}

        /* Watermark Background like AXIONIS / PRAHARI */
        .tactical-watermark {{
            position: relative;
            text-align: center;
            font-size: 3.8rem;
            font-weight: 900;
            letter-spacing: 0.28em;
            color: rgba(255, 255, 255, 0.04);
            text-transform: uppercase;
            user-select: none;
            margin: -1.2rem 0 0.5rem 0;
            pointer-events: none;
            font-family: 'Electrolize', sans-serif;
        }}

        /* Tactical Header Bar */
        .tactical-top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 0.85rem 1.25rem;
            margin-bottom: 1.25rem;
        }}
        .tactical-brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: 0.04em;
            color: {TEXT_WHITE};
        }}
        .brand-icon {{
            color: {ACCENT_RED};
            font-size: 1.3rem;
            animation: pulse 2.5s infinite;
        }}
        .tactical-badges {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}
        .hud-pill {{
            font-family: 'Electrolize', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 4px;
            border: 1px solid {BORDER_ACCENT};
            background: {BG_CARD};
            color: {TEXT_MUTED};
        }}
        .hud-pill.live {{
            border-color: rgba(225, 29, 72, 0.5);
            background: rgba(225, 29, 72, 0.12);
            color: #fecdd3;
        }}
        .hud-pill.live::before {{
            content: "●";
            color: {ACCENT_RED};
            margin-right: 0.35rem;
            animation: blink 1.2s infinite;
        }}
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
            100% {{ opacity: 1; }}
        }}

        /* Threat Log Table & Row styling */
        .threat-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: {BG_PANEL};
            border-bottom: 1px solid {BORDER};
            padding: 0.75rem 1rem;
            font-size: 0.88rem;
            transition: background 0.15s ease;
        }}
        .threat-row:hover {{
            background: {BG_SURFACE_HOVER};
        }}
        .threat-bar-container {{
            width: 100%;
            height: 18px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
            overflow: hidden;
            position: relative;
        }}
        .threat-bar-fill {{
            height: 100%;
            border-radius: 3px;
            background: linear-gradient(90deg, #ea580c 0%, #ef4444 65%, #e11d48 100%);
            box-shadow: 0 0 10px rgba(225, 29, 72, 0.4);
        }}

        /* Metric Cards */
        .metric-card {{
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 1rem 1.15rem;
            position: relative;
            overflow: hidden;
        }}
        .metric-card::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, {ACCENT_RED}, transparent);
        }}
        .metric-value {{
            font-size: 1.65rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: {TEXT_WHITE};
            font-family: 'Electrolize', sans-serif;
        }}
        .metric-label {{
            color: {TEXT_MUTED};
            font-size: 0.76rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 0.25rem;
        }}

        /* Buttons matching the Red / Tactical Action aesthetics */
        .stButton > button {{
            background: {BG_CARD};
            color: {TEXT_WHITE};
            border: 1px solid {BORDER_ACCENT};
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            padding: 0.45rem 1rem;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            background: {BG_SURFACE_HOVER};
            border-color: {ACCENT_RED};
            color: {TEXT_WHITE};
            box-shadow: 0 0 12px {ACCENT_RED_GLOW};
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
            border: 1px solid #f43f5e;
            color: #ffffff;
            box-shadow: 0 2px 14px rgba(225, 29, 72, 0.45);
        }}
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);
            box-shadow: 0 4px 20px rgba(244, 63, 94, 0.6);
            transform: translateY(-1px);
        }}

        /* Form Inputs & Selects */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            background: {BG_PANEL} !important;
            border: 1px solid {BORDER} !important;
            color: {TEXT_WHITE} !important;
            border-radius: 6px !important;
        }}
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {ACCENT_RED} !important;
            box-shadow: 0 0 8px {ACCENT_RED_GLOW} !important;
        }}
        [data-baseweb="select"] > div {{
            background: {BG_PANEL} !important;
            border-color: {BORDER} !important;
            border-radius: 6px !important;
        }}

        /* Expanders */
        .streamlit-expanderHeader {{
            background: {BG_PANEL} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 6px !important;
            color: {TEXT_WHITE} !important;
            font-weight: 600 !important;
        }}
        .streamlit-expanderHeader:hover {{
            border-color: {ACCENT_RED} !important;
        }}

        /* Badges */
        .status-badge {{
            display: inline-block;
            padding: 0.22rem 0.65rem;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.72rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-family: 'Electrolize', sans-serif;
            border: 1px solid transparent;
        }}
        .status-open {{
            color: #ff4d4f;
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.4);
            box-shadow: 0 0 8px rgba(239, 68, 68, 0.25);
        }}
        .status-dispatched {{
            color: #fb923c;
            background: rgba(249, 115, 22, 0.15);
            border-color: rgba(249, 115, 22, 0.4);
        }}
        .status-acknowledged {{
            color: #60a5fa;
            background: rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.4);
        }}
        .status-resolved {{
            color: #34d399;
            background: rgba(16, 185, 129, 0.15);
            border-color: rgba(16, 185, 129, 0.4);
        }}

        /* Phishing Result Cards */
        .phishing-danger {{
            background: rgba(225, 29, 72, 0.1);
            border: 1px solid {ACCENT_RED};
            border-radius: 8px;
            padding: 1.25rem;
            color: #fecdd3;
            box-shadow: 0 0 16px {ACCENT_RED_GLOW};
        }}
        .phishing-safe {{
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid {ACCENT_GREEN};
            border-radius: 8px;
            padding: 1.25rem;
            color: #a7f3d0;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.2);
        }}

        /* Custom Scrollbars */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: {BG_MAIN};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {BORDER};
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {BORDER_ACCENT};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


import base64
from pathlib import Path

_LOGO_PATH = Path(__file__).resolve().parents[1] / "docs" / "logo.jpg"
_LOGO_B64 = ""
if _LOGO_PATH.exists():
    _LOGO_B64 = f"data:image/jpeg;base64,{base64.b64encode(_LOGO_PATH.read_bytes()).decode()}"


def get_logo_img(size: int = 36) -> str:
    if _LOGO_B64:
        return f'<img src="{_LOGO_B64}" style="width: {size}px; height: {size}px; border-radius: 6px; object-fit: contain; vertical-align: middle; filter: drop-shadow(0 0 10px rgba(225, 29, 72, 0.45));">'
    return '<span class="brand-icon">❖</span>'


def render_tactical_header(title: str = "Prahari", subtitle: str = "Cyber Saver") -> None:
    logo_html = get_logo_img(38)
    st.markdown(
        f"""
        <div class="tactical-top-bar">
            <div class="tactical-brand">
                {logo_html}
                <div>
                    <div>{title}</div>
                    <div style="font-size: 0.75rem; color: {TEXT_MUTED}; font-weight: 500;">{subtitle}</div>
                </div>
            </div>
            <div class="tactical-badges">
                <div class="hud-pill live">DEFCON 2 • ACTIVE SURGE</div>
                <div class="hud-pill">MHA-SIH26184</div>
                <div class="hud-pill">🔔 3 CRITICAL</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_watermark(text: str = "PRAHARI") -> None:
    st.markdown(f'<div class="tactical-watermark">{text}</div>', unsafe_allow_html=True)


def card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="prahari-card">
            <div style="color: {TEXT_MUTED}; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem;">
                {title}
            </div>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )

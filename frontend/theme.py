import base64
from pathlib import Path
import streamlit as st

# Color Palette derived from docs/ui.jpg (DataV Cyber Tactical HUD)
BG_MAIN = "#000000"
BG_PANEL = "#060911"
BG_CARD = "#0a0f1a"
BG_SURFACE_HOVER = "#101726"
BORDER = "#1b2536"
BORDER_ACCENT = "#2a3b54"

# High-Tech DataV Neon Accents
ACCENT_CYAN = "#00f0ff"
ACCENT_CYAN_GLOW = "rgba(0, 240, 255, 0.35)"
ACCENT_ORANGE = "#ff9900"
ACCENT_ORANGE_GLOW = "rgba(255, 153, 0, 0.4)"
ACCENT_GREEN = "#00ff66"
ACCENT_RED = "#ff2244"
ACCENT_RED_GLOW = "rgba(255, 34, 68, 0.35)"

TEXT_WHITE = "#ffffff"
TEXT_MUTED = "#8b9cb0"
TEXT_DIM = "#52627a"

_LOGO_PATH = Path(__file__).resolve().parents[1] / "docs" / "logo.jpg"
_LOGO_B64 = ""
if _LOGO_PATH.exists():
    _LOGO_B64 = f"data:image/jpeg;base64,{base64.b64encode(_LOGO_PATH.read_bytes()).decode()}"


def get_logo_img(size: int = 36) -> str:
    if _LOGO_B64:
        return f'<img src="{_LOGO_B64}" style="width: {size}px; height: {size}px; border-radius: 4px; object-fit: contain; vertical-align: middle; border: 1px solid {BORDER_ACCENT}; filter: drop-shadow(0 0 8px {ACCENT_CYAN_GLOW});">'
    return f'<span style="color: {ACCENT_CYAN}; font-size: 1.2rem;">◈</span>'


def apply_unified_theme(mode: str = "citizen") -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Electrolize&display=swap');

        /* Universal Electrolize Font Override */
        *, html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], [data-testid="stMain"], .stApp, section.main, p, span, div, label, input, button, select, textarea, code, pre {{
            font-family: 'Electrolize', sans-serif !important;
        }}

        /* Root Application Base & Anti-White Screen Enforcers (Pure DataV Black) */
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
            background: rgba(0, 0, 0, 0.94) !important;
            backdrop-filter: blur(12px);
            border-bottom: 1px solid {BORDER};
        }}

        /* Sidebar - DataV Tactical Drawer */
        [data-testid="stSidebar"] {{
            background: {BG_PANEL};
            border-right: 1px solid {BORDER};
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.25rem;
        }}

        /* Sidebar Navigation Radio Buttons */
        [data-testid="stSidebar"] .stRadio label {{
            color: {TEXT_MUTED} !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.05em !important;
            padding: 0.35rem 0.6rem !important;
            border-radius: 3px !important;
            border-left: 2px solid transparent !important;
            transition: all 0.15s ease !important;
        }}
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {{
            background: {BG_SURFACE_HOVER} !important;
            color: {ACCENT_CYAN} !important;
            border-left-color: {ACCENT_CYAN} !important;
        }}

        /* Global Cards & Panels with DataV HUD Wireframe Framing */
        .prahari-card {{
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 3px;
            padding: 1.2rem;
            margin-bottom: 0.85rem;
            position: relative;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
        }}
        .prahari-card::before {{
            content: "┌";
            position: absolute;
            top: 2px;
            left: 4px;
            color: {ACCENT_CYAN};
            font-size: 0.75rem;
            line-height: 1;
        }}

        /* Watermark Background like DATAV / PRAHARI */
        .tactical-watermark {{
            position: relative;
            text-align: center;
            font-size: 3.5rem;
            font-weight: 900;
            letter-spacing: 0.35em;
            color: rgba(0, 240, 255, 0.035);
            text-transform: uppercase;
            user-select: none;
            margin: -1rem 0 0.4rem 0;
            pointer-events: none;
            font-family: 'Electrolize', sans-serif;
            text-shadow: 0 0 20px rgba(0, 240, 255, 0.05);
        }}

        /* Tactical Header Bar (DataV Style) */
        .tactical-top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 3px;
            padding: 0.75rem 1.25rem;
            margin-bottom: 0.85rem;
            position: relative;
        }}
        .tactical-top-bar::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 60px; height: 2px;
            background: {ACCENT_CYAN};
            box-shadow: 0 0 10px {ACCENT_CYAN};
        }}
        .tactical-brand {{
            display: flex;
            align-items: center;
            gap: 0.85rem;
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: 0.06em;
            color: {TEXT_WHITE};
        }}
        .tactical-badges {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .hud-pill {{
            font-family: 'Electrolize', sans-serif;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            padding: 0.2rem 0.55rem;
            border-radius: 2px;
            border: 1px solid {BORDER_ACCENT};
            background: {BG_CARD};
            color: {TEXT_MUTED};
        }}
        .hud-pill.live {{
            border-color: rgba(0, 240, 255, 0.6);
            background: rgba(0, 240, 255, 0.08);
            color: {ACCENT_CYAN};
            box-shadow: 0 0 8px {ACCENT_CYAN_GLOW};
        }}
        .hud-pill.live::before {{
            content: "■";
            color: {ACCENT_CYAN};
            margin-right: 0.35rem;
            animation: datav-blink 1s infinite;
        }}
        @keyframes datav-blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.2; }}
            100% {{ opacity: 1; }}
        }}

        /* DataV Top-Left Routes Box Framing */
        .routes-hud-container {{
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-left: 3px solid {ACCENT_CYAN};
            border-radius: 3px;
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.85rem;
        }}

        /* Slim, Side-by-Side Tactical Buttons */
        .stButton > button {{
            background: #080d16 !important;
            color: {TEXT_WHITE} !important;
            border: 1px solid {BORDER_ACCENT} !important;
            border-radius: 2px !important;
            font-size: 0.72rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            padding: 0.2rem 0.55rem !important;
            min-height: 28px !important;
            height: 28px !important;
            line-height: 1 !important;
            transition: all 0.15s ease !important;
            box-shadow: none !important;
        }}
        .stButton > button:hover {{
            background: #0e1626 !important;
            border-color: {ACCENT_CYAN} !important;
            color: {ACCENT_CYAN} !important;
            box-shadow: 0 0 10px {ACCENT_CYAN_GLOW} !important;
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {ACCENT_ORANGE} 0%, #d97706 100%) !important;
            border: 1px solid #fbbf24 !important;
            color: #ffffff !important;
            box-shadow: 0 0 12px {ACCENT_ORANGE_GLOW} !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #fbbf24 0%, {ACCENT_ORANGE} 100%) !important;
            box-shadow: 0 0 18px rgba(255, 153, 0, 0.6) !important;
        }}

        /* Metric Cards matching DataV Airport / Cyber HUD */
        .metric-card {{
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 2px;
            padding: 0.75rem 1rem;
            position: relative;
        }}
        .metric-card::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 24px; height: 2px;
            background: {ACCENT_CYAN};
        }}
        .metric-value {{
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            color: {TEXT_WHITE};
            font-family: 'Electrolize', sans-serif;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }}
        .metric-label {{
            color: {TEXT_MUTED};
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.2rem;
        }}

        /* Threat Velocity Bar Fill (DataV Orange to Cyan gradient) */
        .threat-bar-container {{
            width: 100%;
            height: 12px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid #141e2e;
            border-radius: 2px;
            overflow: hidden;
        }}
        .threat-bar-fill {{
            height: 100%;
            border-radius: 1px;
            background: linear-gradient(90deg, #ff8800 0%, #ffaa00 50%, #00f0ff 100%);
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.35);
        }}

        /* Form Inputs */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            background: {BG_PANEL} !important;
            border: 1px solid {BORDER} !important;
            color: {TEXT_WHITE} !important;
            border-radius: 2px !important;
            font-size: 0.82rem !important;
        }}
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {ACCENT_CYAN} !important;
            box-shadow: 0 0 8px {ACCENT_CYAN_GLOW} !important;
        }}
        [data-baseweb="select"] > div {{
            background: {BG_PANEL} !important;
            border-color: {BORDER} !important;
            border-radius: 2px !important;
        }}

        /* Status Badges */
        .status-badge {{
            display: inline-block;
            padding: 0.18rem 0.55rem;
            border-radius: 2px;
            font-weight: 700;
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-family: 'Electrolize', sans-serif;
            border: 1px solid transparent;
        }}
        .status-open {{
            color: {ACCENT_RED};
            background: rgba(255, 34, 68, 0.1);
            border-color: rgba(255, 34, 68, 0.4);
            box-shadow: 0 0 8px {ACCENT_RED_GLOW};
        }}
        .status-dispatched {{
            color: {ACCENT_ORANGE};
            background: rgba(255, 153, 0, 0.1);
            border-color: rgba(255, 153, 0, 0.4);
        }}
        .status-acknowledged {{
            color: {ACCENT_CYAN};
            background: rgba(0, 240, 255, 0.1);
            border-color: rgba(0, 240, 255, 0.4);
        }}
        .status-resolved {{
            color: {ACCENT_GREEN};
            background: rgba(0, 255, 102, 0.1);
            border-color: rgba(0, 255, 102, 0.4);
        }}

        /* Phishing Banner Alert */
        .phishing-danger {{
            background: rgba(255, 34, 68, 0.08);
            border: 1px solid {ACCENT_RED};
            border-radius: 2px;
            padding: 1.15rem;
            color: #fecaca;
            box-shadow: 0 0 16px {ACCENT_RED_GLOW};
        }}
        .phishing-safe {{
            background: rgba(0, 255, 102, 0.08);
            border: 1px solid {ACCENT_GREEN};
            border-radius: 2px;
            padding: 1.15rem;
            color: #a7f3d0;
            box-shadow: 0 0 16px rgba(0, 255, 102, 0.2);
        }}

        /* Custom Minimalist Scrollbars */
        ::-webkit-scrollbar {{
            width: 4px;
            height: 4px;
        }}
        ::-webkit-scrollbar-track {{
            background: #000000;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #1b2536;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {ACCENT_CYAN};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_tactical_header(title: str = "Prahari", subtitle: str = "Cyber Saver") -> None:
    logo_html = get_logo_img(38)
    st.markdown(
        f"""
        <div class="tactical-top-bar">
            <div class="tactical-brand">
                {logo_html}
                <div>
                    <div style="font-weight: 800; font-size: 1.2rem; letter-spacing: 0.08em;">{title}</div>
                    <div style="font-size: 0.72rem; color: {ACCENT_CYAN}; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;">
                        // {subtitle}
                    </div>
                </div>
            </div>
            <div class="tactical-badges">
                <div class="hud-pill live">RADAR ONLINE // 007</div>
                <div class="hud-pill">MHA-SIH26184</div>
                <div class="hud-pill" style="border-color: {ACCENT_ORANGE}; color: {ACCENT_ORANGE};">EARLY WARNING ACTIVE</div>
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
            <div style="color: {ACCENT_CYAN}; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem;">
                ■ {title}
            </div>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )

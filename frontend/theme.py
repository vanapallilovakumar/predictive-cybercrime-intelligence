import base64
from pathlib import Path
import streamlit as st

# Strict Minimalist Black & White Palette (matching docs/ui.jpg)
BG_MAIN = "#000000"
BG_PANEL = "#000000"
BG_CARD = "#050505"
BG_SURFACE_HOVER = "#121212"

# Monochrome Borders & Dividers
BORDER = "#262626"
BORDER_LIGHT = "#404040"
BORDER_WHITE = "#ffffff"

# Monochrome Typography
TEXT_WHITE = "#ffffff"
TEXT_MUTED = "#a3a3a3"
TEXT_DIM = "#525252"

_LOGO_PATH = Path(__file__).resolve().parents[1] / "docs" / "logo.jpg"
_LOGO_B64 = ""
if _LOGO_PATH.exists():
    _LOGO_B64 = f"data:image/jpeg;base64,{base64.b64encode(_LOGO_PATH.read_bytes()).decode()}"


def get_logo_img(size: int = 36) -> str:
    if _LOGO_B64:
        return f'<img src="{_LOGO_B64}" style="width: {size}px; height: {size}px; border-radius: 2px; object-fit: contain; vertical-align: middle; border: 1px solid {BORDER_LIGHT};">'
    return '<span style="color: #ffffff; font-size: 1.1rem; font-weight: 800;">[◈]</span>'


def apply_unified_theme(mode: str = "citizen") -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Electrolize&display=swap');

        /* Universal Electrolize Font Override */
        *, html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], [data-testid="stMain"], .stApp, section.main, p, span, div, label, input, button, select, textarea, code, pre {{
            font-family: 'Electrolize', sans-serif !important;
        }}

        /* Strict Minimal Black Background */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], [data-testid="stMain"], .stApp, section.main {{
            background: {BG_MAIN} !important;
            background-color: {BG_MAIN} !important;
            color: {TEXT_WHITE} !important;
        }}

        iframe {{
            background-color: {BG_MAIN} !important;
            color-scheme: dark;
            border: 1px solid {BORDER} !important;
        }}

        /* Header & Nav */
        [data-testid="stHeader"] {{
            background: {BG_MAIN} !important;
            border-bottom: 1px solid {BORDER};
        }}

        /* Sidebar - Strict Minimal Monochrome */
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
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.05em !important;
            padding: 0.35rem 0.6rem !important;
            border-radius: 2px !important;
            border-left: 2px solid transparent !important;
            transition: all 0.15s ease !important;
        }}
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {{
            background: {BG_SURFACE_HOVER} !important;
            color: {TEXT_WHITE} !important;
            font-weight: 800 !important;
            border-left-color: {BORDER_WHITE} !important;
        }}

        /* Minimal Wireframe Panels (matching docs/ui.jpg) */
        .prahari-card {{
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 2px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.85rem;
            position: relative;
        }}
        .prahari-card::before {{
            content: "┌";
            position: absolute;
            top: 2px;
            left: 4px;
            color: {TEXT_MUTED};
            font-size: 0.7rem;
            line-height: 1;
        }}

        /* Watermark */
        .tactical-watermark {{
            position: relative;
            text-align: center;
            font-size: 3.5rem;
            font-weight: 900;
            letter-spacing: 0.35em;
            color: rgba(255, 255, 255, 0.04);
            text-transform: uppercase;
            user-select: none;
            margin: -1rem 0 0.4rem 0;
            pointer-events: none;
            font-family: 'Electrolize', sans-serif;
        }}

        /* Tactical Top Header Bar */
        .tactical-top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: {BG_PANEL};
            border: 1px solid {BORDER};
            border-radius: 2px;
            padding: 0.75rem 1.25rem;
            margin-bottom: 0.85rem;
            position: relative;
        }}
        .tactical-top-bar::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 40px; height: 1px;
            background: {BORDER_WHITE};
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
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            padding: 0.2rem 0.55rem;
            border-radius: 2px;
            border: 1px solid {BORDER_LIGHT};
            background: {BG_PANEL};
            color: {TEXT_MUTED};
        }}
        .hud-pill.live {{
            border-color: {BORDER_WHITE};
            color: {TEXT_WHITE};
            font-weight: 800 !important;
        }}

        /* Slim, Side-by-Side Minimalist Buttons (Inverted on Hover) */
        .stButton > button {{
            background: #000000 !important;
            color: {TEXT_WHITE} !important;
            border: 1px solid {BORDER_LIGHT} !important;
            border-radius: 2px !important;
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            padding: 0.2rem 0.55rem !important;
            min-height: 28px !important;
            height: 28px !important;
            line-height: 1 !important;
            transition: all 0.1s ease !important;
            box-shadow: none !important;
        }}
        .stButton > button:hover {{
            background: #ffffff !important;
            color: #000000 !important;
            font-weight: 800 !important;
            border-color: #ffffff !important;
        }}
        .stButton > button[kind="primary"] {{
            background: #ffffff !important;
            border: 1px solid #ffffff !important;
            color: #000000 !important;
            font-weight: 800 !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: #e5e5e5 !important;
            color: #000000 !important;
        }}

        /* Metric Cards matching DataV Airport / Cyber Wireframes */
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
            top: 0; left: 0; width: 18px; height: 1px;
            background: {BORDER_WHITE};
        }}
        .metric-value {{
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            color: {TEXT_WHITE};
            font-family: 'Electrolize', sans-serif;
        }}
        .metric-label {{
            color: {TEXT_MUTED};
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.2rem;
        }}

        /* Strict B&W Threat Meter */
        .threat-bar-container {{
            width: 100%;
            height: 8px;
            background: #121212;
            border: 1px solid {BORDER};
            border-radius: 1px;
            overflow: hidden;
        }}
        .threat-bar-fill {{
            height: 100%;
            border-radius: 0;
            background: #ffffff;
        }}

        /* Form Inputs in Pure Black */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            background: #000000 !important;
            border: 1px solid {BORDER} !important;
            color: {TEXT_WHITE} !important;
            border-radius: 2px !important;
            font-size: 0.82rem !important;
        }}
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {BORDER_WHITE} !important;
            box-shadow: none !important;
        }}
        [data-baseweb="select"] > div {{
            background: #000000 !important;
            border-color: {BORDER} !important;
            border-radius: 2px !important;
        }}

        /* Status Badges - Monochrome with Bolder Text */
        .status-badge {{
            display: inline-block;
            padding: 0.18rem 0.55rem;
            border-radius: 2px;
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-family: 'Electrolize', sans-serif;
            background: #000000;
            border: 1px solid {BORDER_LIGHT};
            color: {TEXT_MUTED};
            font-weight: 500;
        }}
        /* For alerts / important, just the text is BOLDER */
        .status-open {{
            border-color: #ffffff;
            color: #ffffff;
            font-weight: 900 !important;
            letter-spacing: 0.1em;
        }}
        .status-dispatched {{
            border-color: #a3a3a3;
            color: #ffffff;
            font-weight: 800 !important;
        }}
        .status-acknowledged {{
            border-color: {BORDER_LIGHT};
            color: #d4d4d4;
            font-weight: 700 !important;
        }}
        .status-resolved {{
            border-color: {BORDER};
            color: #a3a3a3;
            font-weight: 500;
        }}

        /* Minimal Alerts without Loud Colors */
        .phishing-danger {{
            background: #000000;
            border: 1px solid #ffffff;
            border-radius: 2px;
            padding: 1.15rem;
            color: #ffffff;
        }}
        .phishing-danger h3 {{
            font-weight: 900 !important;
            color: #ffffff !important;
            letter-spacing: 0.05em;
        }}
        .phishing-safe {{
            background: #000000;
            border: 1px solid {BORDER_LIGHT};
            border-radius: 2px;
            padding: 1.15rem;
            color: #d4d4d4;
        }}

        /* Custom Wireframe Scrollbars */
        ::-webkit-scrollbar {{
            width: 3px;
            height: 3px;
        }}
        ::-webkit-scrollbar-track {{
            background: #000000;
        }}
        ::-webkit-scrollbar-thumb {{
            background: {BORDER};
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #ffffff;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_tactical_header(title: str = "Prahari", subtitle: str = "Cyber Saver") -> None:
    logo_html = get_logo_img(36)
    st.markdown(
        f"""
        <div class="tactical-top-bar">
            <div class="tactical-brand">
                {logo_html}
                <div>
                    <div style="font-weight: 800; font-size: 1.15rem; letter-spacing: 0.08em; color: #ffffff;">{title}</div>
                    <div style="font-size: 0.7rem; color: #a3a3a3; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase;">
                        // {subtitle}
                    </div>
                </div>
            </div>
            <div class="tactical-badges">
                <div class="hud-pill live">RADAR ONLINE // 007</div>
                <div class="hud-pill">MHA-SIH26184</div>
                <div class="hud-pill" style="border-color: #ffffff; color: #ffffff; font-weight: 800;">[!] CRITICAL MONITOR ACTIVE</div>
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
            <div style="color: #a3a3a3; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem;">
                ■ {title}
            </div>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )

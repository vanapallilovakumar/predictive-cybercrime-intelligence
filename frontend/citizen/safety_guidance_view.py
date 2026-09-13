import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("GUIDANCE")

    st.markdown(
        """
        <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #f8fafc;">
                NATIONAL CYBERCRIME CITIZEN ADVISORY
            </div>
            <div style="font-size: 0.76rem; color: #8b949e; margin-top: 0.2rem;">
                Ministry of Home Affairs (MHA) Golden Hour Protocol & Typology Defense Playbook.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    data = api_client.guidance()
    golden = data.get("golden_hour", {})

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(225, 29, 72, 0.15) 0%, rgba(19, 24, 36, 0.95) 100%); border: 1px solid #e11d48; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.25rem; box-shadow: 0 0 20px rgba(225, 29, 72, 0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="font-size: 1.1rem; font-weight: 800; color: #f43f5e; letter-spacing: 0.03em;">
                    ⚡ {golden.get("title", "GOLDEN HOUR EMERGENCY RESPONSE")}
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.95rem; font-weight: 800; color: #ffffff; background: #e11d48; padding: 0.35rem 0.85rem; border-radius: 4px;">
                    DIAL: {golden.get("helpline", "1930")}
                </div>
            </div>
            <div style="font-size: 0.85rem; color: #fecdd3; margin-bottom: 0.75rem;">
                {golden.get("summary", "Reporting within the first 120 minutes increases stolen funds recovery probability by over 80%.")}
            </div>
            <div style="font-size: 0.76rem; color: #8b949e; font-family: 'Electrolize', sans-serif;">
                OFFICIAL PORTAL: <a href="https://cybercrime.gov.in" target="_blank" style="color: #60a5fa; text-decoration: none;">{golden.get("portal", "cybercrime.gov.in")}</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    steps = golden.get("steps", [])
    if steps:
        st.markdown(
            '<div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Immediate Action Checklist</div>',
            unsafe_allow_html=True,
        )
        cols_step = st.columns(len(steps))
        for idx, (col, step) in enumerate(zip(cols_step, steps), 1):
            with col:
                st.markdown(
                    f"""
                    <div style="background: #131824; border: 1px solid #222c3d; border-radius: 6px; padding: 0.85rem; height: 100%;">
                        <div style="font-family: 'Electrolize', sans-serif; font-size: 0.75rem; font-weight: 800; color: #e11d48; margin-bottom: 0.35rem;">
                            STEP 0{idx}
                        </div>
                        <div style="font-size: 0.8rem; color: #f8fafc; font-weight: 500;">
                            {step}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Typology Defense Guides</div>',
        unsafe_allow_html=True,
    )

    typologies = data.get("typologies", [])
    columns = st.columns(2)
    for index, item in enumerate(typologies):
        with columns[index % 2]:
            st.markdown(
                f"""
                <div style="background: #131824; border: 1px solid #222c3d; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">
                        <span style="color: #e11d48; margin-right: 0.4rem;">{item.get('icon', '🛡️')}</span> {item.get('typology', 'Fraud')}
                    </div>
                    <div style="font-size: 0.75rem; color: #f43f5e; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">
                        Danger Signs:
                    </div>
                    <div style="font-size: 0.78rem; color: #cbd5e1; margin-bottom: 0.6rem;">
                        {' • '.join(item.get('danger_signs', []))}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.75rem;">
                        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 4px; padding: 0.5rem; color: #a7f3d0;">
                            <b>DO:</b><br>{'<br>'.join(item.get('dos', []))}
                        </div>
                        <div style="background: rgba(225, 29, 72, 0.08); border: 1px solid rgba(225, 29, 72, 0.3); border-radius: 4px; padding: 0.5rem; color: #fecdd3;">
                            <b>DO NOT:</b><br>{'<br>'.join(item.get('donts', []))}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

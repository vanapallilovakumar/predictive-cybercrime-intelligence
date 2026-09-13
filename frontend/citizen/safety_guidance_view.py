import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("GUIDANCE")

    st.markdown(
        """
        <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.04em; color: #ffffff;">
                ■ NATIONAL CYBERCRIME CITIZEN ADVISORY
            </div>
            <div style="font-size: 0.76rem; color: #a3a3a3; margin-top: 0.2rem;">
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
        <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 1.25rem; margin-bottom: 1.25rem; position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff; letter-spacing: 0.05em;">
                    [!] {golden.get("title", "GOLDEN HOUR EMERGENCY RESPONSE")}
                </div>
                <div style="font-family: 'Electrolize', sans-serif; font-size: 0.9rem; font-weight: 900; color: #ffffff; background: #000000; border: 1px solid #ffffff; padding: 0.35rem 0.85rem; border-radius: 2px;">
                    DIAL: {golden.get("helpline", "1930")}
                </div>
            </div>
            <div style="font-size: 0.85rem; color: #d4d4d4; margin-bottom: 0.75rem;">
                {golden.get("summary", "Reporting within the first 120 minutes increases stolen funds recovery probability by over 80%.")}
            </div>
            <div style="font-size: 0.76rem; color: #a3a3a3; font-family: 'Electrolize', sans-serif;">
                OFFICIAL PORTAL: <a href="https://cybercrime.gov.in" target="_blank" style="color: #ffffff; font-weight: 800; text-decoration: underline;">{golden.get("portal", "cybercrime.gov.in")}</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    steps = golden.get("steps", [])
    if steps:
        st.markdown(
            '<div style="font-size: 0.82rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">■ IMMEDIATE ACTION CHECKLIST</div>',
            unsafe_allow_html=True,
        )
        cols_step = st.columns(len(steps))
        for idx, (col, step) in enumerate(zip(cols_step, steps), 1):
            with col:
                st.markdown(
                    f"""
                    <div style="background: #000000; border: 1px solid #262626; border-radius: 2px; padding: 0.85rem; height: 100%;">
                        <div style="font-family: 'Electrolize', sans-serif; font-size: 0.75rem; font-weight: 800; color: #ffffff; margin-bottom: 0.35rem;">
                            STEP 0{idx}
                        </div>
                        <div style="font-size: 0.8rem; color: #d4d4d4; font-weight: 500;">
                            {step}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size: 0.82rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">■ TYPOLOGY DEFENSE GUIDES</div>',
        unsafe_allow_html=True,
    )

    typologies = data.get("typologies", [])
    columns = st.columns(2)
    for index, item in enumerate(typologies):
        with columns[index % 2]:
            st.markdown(
                f"""
                <div style="background: #000000; border: 1px solid #262626; border-radius: 2px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="font-size: 0.95rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem;">
                        <span style="color: #ffffff; margin-right: 0.4rem;">{item.get('icon', '◈')}</span> {item.get('typology', 'Fraud')}
                    </div>
                    <div style="font-size: 0.75rem; color: #ffffff; font-weight: 900; text-transform: uppercase; margin-bottom: 0.25rem;">
                        [!] DANGER SIGNS:
                    </div>
                    <div style="font-size: 0.78rem; color: #d4d4d4; margin-bottom: 0.6rem;">
                        {' • '.join(item.get('danger_signs', []))}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.75rem;">
                        <div style="background: #000000; border: 1px solid #404040; border-radius: 2px; padding: 0.5rem; color: #ffffff;">
                            <b style="font-weight: 800;">DO:</b><br>{'<br>'.join(item.get('dos', []))}
                        </div>
                        <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 0.5rem; color: #ffffff;">
                            <b style="font-weight: 900;">[!] DO NOT:</b><br>{'<br>'.join(item.get('donts', []))}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

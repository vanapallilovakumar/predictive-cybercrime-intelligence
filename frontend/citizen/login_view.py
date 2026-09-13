import streamlit as st

from frontend import api_client
from frontend import theme


def render() -> None:
    theme.render_watermark("SECURITY")

    c_left, c_card, c_right = st.columns([1, 2.2, 1])

    with c_card:
        logo_html = theme.get_logo_img(48)
        st.markdown(
            f"""
            <div style="background: #000000; border: 1px solid #ffffff; border-radius: 2px; padding: 1.75rem 2rem; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 1px; background: #ffffff;"></div>
                <div style="display: flex; align-items: center; gap: 0.85rem; margin-bottom: 0.35rem;">
                    {logo_html}
                    <div>
                        <div style="font-weight: 900; font-size: 1.35rem; letter-spacing: 0.08em; color: #ffffff; line-height: 1.1;">
                            PRAHARI
                        </div>
                        <div style="font-size: 0.7rem; color: #a3a3a3; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;">
                            Cyber Saver • Gateway
                        </div>
                    </div>
                </div>
                <div style="font-size: 0.78rem; color: #a3a3a3; margin-bottom: 1.25rem;">
                    Universal Authenticator • SIH26184 Citizen & Police Defense Grid
                </div>
                <div style="background: #000000; border: 1px solid #404040; border-radius: 2px; padding: 0.75rem 1rem; font-size: 0.76rem; color: #ffffff; font-family: 'Electrolize', sans-serif; margin-bottom: 1.25rem;">
                    ■ DEMO ACCESS: Any email accepted. Use bypass code <b style="font-weight: 900;">123456</b>
                </div>
            """,
            unsafe_allow_html=True,
        )

        email = st.text_input("Enter Registered Email", placeholder="officer@cybercell.gov.in or citizen@domain.com")

        if st.button("Request Security OTP", type="primary", use_container_width=True):
            if not email or "@" not in email:
                st.error("Please enter a valid email address.")
            else:
                result = api_client.request_otp(email)
                if result and result.get("success"):
                    st.session_state["login_email"] = email
                    st.session_state["otp_requested"] = True
                    st.success(result.get("message", "One-time passcode dispatched."))
                else:
                    st.error("Unable to dispatch OTP code.")

        if st.session_state.get("otp_requested"):
            st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)
            otp = st.text_input("6-Digit Verification Code", max_chars=6, type="password", placeholder="123456")
            
            if st.button("Verify Credentials & Enter", type="primary", use_container_width=True):
                result = api_client.verify_otp(st.session_state["login_email"], otp)
                if result and result.get("success"):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = result.get("user") or {"email": st.session_state["login_email"], "name": "Citizen User"}
                    st.rerun()
                else:
                    st.error("Verification code invalid or expired.")

        st.markdown("</div>", unsafe_allow_html=True)

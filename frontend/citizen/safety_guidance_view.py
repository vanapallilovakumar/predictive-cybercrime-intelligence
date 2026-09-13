import streamlit as st

from frontend import api_client


def render() -> None:
    st.markdown("## Safety Guidance")
    data = api_client.guidance()
    golden = data.get("golden_hour", {})
    st.markdown(
        f'<div class="phishing-danger"><h3>{golden.get("title", "Golden Hour Advisory")}</h3>'
        f'<p>{golden.get("summary", "Call 1930 immediately after a cyber fraud.")}</p>'
        f'<p><b>Helpline: {golden.get("helpline", "1930")}</b> | {golden.get("portal", "cybercrime.gov.in")}</p></div>',
        unsafe_allow_html=True,
    )
    steps = golden.get("steps", [])
    if steps:
        st.markdown("#### Immediate actions")
        for step in steps:
            st.write(step)
    typologies = data.get("typologies", [])
    columns = st.columns(2)
    for index, item in enumerate(typologies):
        with columns[index % 2]:
            st.markdown(f"### {item.get('icon', '')} {item.get('typology', 'Safety tip')}")
            st.markdown("**Warning signs**")
            for value in item.get("danger_signs", []):
                st.write(f"- {value}")
            st.markdown("**Do**")
            for value in item.get("dos", []):
                st.write(f"- {value}")
            st.markdown("**Do not**")
            for value in item.get("donts", []):
                st.write(f"- {value}")

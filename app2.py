import streamlit as st
from backend import generate_signed_url

st.set_page_config(page_title="MultiClassClassificationInput App", layout="wide")
st.logo(generate_signed_url("pvz.gif"), size="large")
pages = [
    st.Page("Pages/Home_Page.py", title="Home",icon="🏠"),
    st.Page("Pages/Start_Task.py", title="Start Task",icon="🧑🏻‍💻"),
    st.Page("Pages/Meta_Data.py", title="Meta Data",icon="📊"),
    st.Page("Pages/Glossary.py", title="Glossary",icon="📖"),
    st.Page("Pages/Demonstration.py", title="Demonstration",icon="🎬"),
    st.Page("Pages/About.py", title="About",icon="❔"),
]
pg = st.navigation(pages, position="sidebar", expanded=True)

pg.run()

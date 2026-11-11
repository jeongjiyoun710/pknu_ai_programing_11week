import streamlit as st
from openai import OpenAI

# streamlit_app.py
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")
if api_key:
    st.session_state["OpenAI_API"] = OpenAI(api_key=api_key)

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
    st.Page("app_pages/PKNU_Chat.py", title="도서관 챗봇", icon=":material/local_library:"),
    st.Page("app_pages/ChatPDF.py", title="PDF 파일 읽기", icon=":material/picture_as_pdf:"),
])

pg.run()
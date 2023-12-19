import streamlit as st
from model import OpenAIBot
st.header('ChatBot', divider='rainbow')

if "bot" not in st.session_state:
    st.session_state.bot = OpenAIBot()


for m in st.session_state.bot.getMessages():
    with st.chat_message(m.role):
        st.markdown(m.content)

if prompt := st.chat_input("Please Ask a Question"):
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.bot.send_message(prompt)
    with st.chat_message(response.role):
        st.markdown(response.content)
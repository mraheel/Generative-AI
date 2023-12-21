import streamlit as st
from model import OpenAIBot, MessageItem

st.header('ChatBot', divider='rainbow')

if "bot" not in st.session_state:
    st.session_state.bot = OpenAIBot(name="Math Tutor", instructions="You are a personal math tutor. Write and run code to answer math questions.")


for m in st.session_state.bot.getMessages():
    with st.chat_message(m.role):
        st.markdown(m.content)

if prompt := st.chat_input("Please Ask a Question"):
    st.session_state.bot.send_message(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        placehplder = st.empty()
        placehplder.write('...')
        if(st.session_state.bot.isCompleted()):
            response: MessageItem = st.session_state.bot.get_lastest_response()
            # with st.chat_message(response.role):
            placehplder.markdown(response.content)


    # if(st.session_state.bot.isCompleted()):
    #     response: MessageItem = st.session_state.bot.get_lastest_response()
    #     with st.chat_message(response.role):
    #         st.markdown(response.content)
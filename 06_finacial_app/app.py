import streamlit as st

st.set_page_config('ChatBot')
st.title('ChatBot')

if 'messages' not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("Say something")
if prompt:
    st.session_state.messages.append(prompt)
    
    for m in st.session_state.messages:
        with st.chat_message('R'):
            st.markdown(m)
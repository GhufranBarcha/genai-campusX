import streamlit as st


with st.chat_message("user"):
    st.text('Hi')

with st.chat_message("assistant"):
    st.text('How are you?')

with st.chat_message("user"):
    st.text('I am fine')    



user_input = st.chat_input('Type here')


if user_input:
    with st.chat_message("assistant"):
        st.text(user_input)
import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# Display past messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# Chat input box
user_input = st.chat_input("Type here")

if user_input:
    # Store user message
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.text(user_input)

    # Send user message to chatbot
    config = {"configurable": {"thread_id": 1}}
    response = chatbot.invoke(
        {"message": HumanMessage(content=user_input)},
        config=config
    )

    # Store assistant message
    assistant_reply = response["message"][-1].content
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": assistant_reply
    })

    with st.chat_message("assistant"):
        st.text(assistant_reply)

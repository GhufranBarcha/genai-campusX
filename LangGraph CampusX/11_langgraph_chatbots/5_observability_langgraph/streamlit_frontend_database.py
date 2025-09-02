import streamlit as st
from langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid


## Utility function

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    config = {'configurable': {'thread_id': thread_id}}
    state = chatbot.get_state(config=config).values

    # Check if thread exists and has 'message' key
    if 'message' in state and state['message']:
        return state['message']
    else:
        return None


# ---------------------------
# Initialize session state
# ---------------------------
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()   

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads() 
add_thread(st.session_state['thread_id'])


## Side bar UI

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    if len(st.session_state['message_history']) != 0: 
        reset_chat()

st.sidebar.header('My Conversation')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        if messages is None:
            st.session_state['message_history'] = []
            continue

        temp_message = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else: 
                role = 'assistant'

            temp_message.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = temp_message


# Display past messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
    # config = {"configurable": {'thread_id': st.session_state['thread_id']}}


    ## for langgraph metadata
    config = {"configurable": {'thread_id': st.session_state['thread_id']},
              "metadata":{
                  "thread_id": st.session_state["thread_id"]
              },
              "run_name": "chat_turn",
              }

    # Store assistant message
    with st.chat_message('assistant'):
        assistant_reply = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
            {"message": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode= 'messages')
        )
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": assistant_reply
    })
from langgraph.graph import StateGraph , START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)


## Initialize chatbot
llm = ChatOpenAI()
 

## Create a state
class ChatState(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):  
    ## Take user query from state
    message = state['message']
    ## Send to llm
    response = llm.invoke(message)
    ## response store
    return {'message': [response]}

## FOr memory
checkpointer = SqliteSaver(conn = conn)
graph = StateGraph(ChatState)

## add node
graph.add_node('chat_node',chat_node )

## Edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


chatbot = graph.compile(checkpointer = checkpointer)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)    


# config = {"configurable": {"thread_id": 1}}

# for message_chunk, metadata in chatbot.stream(
#         {"message": [HumanMessage(content="what is the recipe for making kadahii?")]},
#         config=config,
#         stream_mode= 'messages'
#         ):

#     if message_chunk.content:
#         print(message_chunk.content, end="", flush=True)


# config = {"configurable": {'thread_id': 'thread-1'}}
# response = chatbot.invoke(
#             {"message": [HumanMessage(content='What are you doing')]},
#             config=config,
#             stream_mode= 'messages')
# print(chatbot.get_state(config=config).values['message'])


# ## Test the sqlite chatnot


# config = {"configurable": {'thread_id': 'thread-1'}}

# response = chatbot.invoke({"message": [HumanMessage(content= 'Hi my name is ghufran')]}, config=config, stream_mode= 'messages')
# print(response)
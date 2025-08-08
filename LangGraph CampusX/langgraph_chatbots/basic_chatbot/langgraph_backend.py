from langgraph.graph import StateGraph , START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages


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
checkpointer = MemorySaver()
graph = StateGraph(ChatState)

## add node
graph.add_node('chat_node',chat_node )

## Edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


chatbot = graph.compile(checkpointer = checkpointer)

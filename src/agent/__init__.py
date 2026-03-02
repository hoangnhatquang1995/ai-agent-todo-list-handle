from . import embedding
from . import llm 
from . import graph

from langchain.messages import HumanMessage

graph = graph.build_graph()

def talk_to_agent(user_input : str):
    initial_message = HumanMessage(content=user_input)
    result = graph.invoke({
        "messages" : [initial_message]
    })
    return result
